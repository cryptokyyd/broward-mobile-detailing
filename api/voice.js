/**
 * Twilio inbound-call webhook. This is the call-tracking half of the site:
 * a customer rings the tracking number, we announce recording, connect them to
 * the real phone, and log the call as a lead through the same pipeline the
 * quote form uses.
 *
 * ─────────────────────────────────────────────────────────────────────────
 * FLORIDA IS AN ALL-PARTY CONSENT STATE. Fla. Stat. § 934.03 makes it a
 * criminal offence to record a call without the consent of EVERY party.
 * The <Say> announcement below is not decoration and must not be removed —
 * it is what makes the recording lawful, because continuing the call after
 * a clear notice is treated as consent. Both callers hear it: the customer
 * before connection, and whoever answers is a party to a call they know is
 * recorded on their own tracking line.
 *
 * If you turn recording off (RECORD_CALLS=false) the announcement goes away
 * with it, because there is then nothing to disclose.
 * ─────────────────────────────────────────────────────────────────────────
 *
 * Point your Twilio number's "A CALL COMES IN" webhook at:
 *     https://<your-domain>/api/voice        (HTTP POST)
 *
 * Env vars:
 *   TWILIO_AUTH_TOKEN   required — validates that requests really came from
 *                       Twilio. Without it this endpoint refuses to run:
 *                       an open voice webhook lets anyone burn your balance.
 *   FORWARD_TO_NUMBER   required — the real phone, E.164 (e.g. +17865572897)
 *   RECORD_CALLS        "false" disables recording (and the announcement)
 *   DIAL_TIMEOUT        seconds to ring before giving up (default 20)
 */
import crypto from 'node:crypto';
import { deliver } from './_deliver.js';

const XML = 'text/xml; charset=utf-8';

/** Escape for XML text nodes and attribute values. */
function x(s) {
  return String(s ?? '').replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&apos;' }[c]
  ));
}

/**
 * Reconstruct the exact URL Twilio signed. It signs the full public URL
 * including the query string, which behind Vercel's proxy has to be rebuilt
 * from the forwarded headers rather than read off the socket.
 */
export function requestUrl(req) {
  const proto = req.headers['x-forwarded-proto'] || 'https';
  const host = req.headers['x-forwarded-host'] || req.headers.host;
  return `${proto}://${host}${req.url}`;
}

/**
 * Twilio's signature scheme: the URL, then every POST param appended as
 * key immediately followed by value, in lexical key order, HMAC-SHA1'd with
 * the auth token and base64'd.
 */
export function expectedSignature(url, params, authToken) {
  let data = url;
  for (const key of Object.keys(params).sort()) data += key + params[key];
  return crypto.createHmac('sha1', authToken).update(Buffer.from(data, 'utf-8')).digest('base64');
}

export function signatureValid(url, params, signature, authToken) {
  if (!signature || !authToken) return false;
  const expected = expectedSignature(url, params, authToken);
  const a = Buffer.from(expected);
  const b = Buffer.from(String(signature));
  // Length check first: timingSafeEqual throws on a length mismatch.
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

/** Twilio posts form-urlencoded; Vercel may hand it over parsed or raw. */
function parseBody(req) {
  const raw = req.body;
  if (raw && typeof raw === 'object') return raw;
  if (typeof raw === 'string') return Object.fromEntries(new URLSearchParams(raw));
  return {};
}

function twiml(res, body, status = 200) {
  res.setHeader('Content-Type', XML);
  return res.status(status).send(`<?xml version="1.0" encoding="UTF-8"?>\n<Response>${body}</Response>`);
}

/** A call, shaped like everything else that reaches deliver(). */
export function buildCallLead(p, extra = {}) {
  const lead = {
    kind: 'call',
    name: 'Phone caller',
    phone: p.From || '',
    phone_e164: p.From || '',
    city: [p.FromCity, p.FromState].filter(Boolean).join(', '),
    service: 'Inbound call',
    tracking_number: p.To || '',
    call_sid: p.CallSid || '',
    received_at: new Date().toISOString(),
    ...extra,
  };
  // The tracking number IS the attribution: one number per channel means the
  // number that rang tells you which channel produced the call.
  if (p.To) lead.attribution = { tracking_number: p.To };
  return lead;
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const params = parseBody(req);
  const token = process.env.TWILIO_AUTH_TOKEN;

  // Refuse to operate unauthenticated. An unsigned voice webhook is a way for
  // a stranger to place calls on your account.
  if (!token) {
    console.error('TWILIO_AUTH_TOKEN is not set — refusing to handle a call webhook');
    return twiml(res, '<Say>This number is not configured yet. Goodbye.</Say><Hangup/>', 500);
  }
  if (!signatureValid(requestUrl(req), params, req.headers['x-twilio-signature'], token)) {
    console.warn('rejected a voice webhook with a bad Twilio signature');
    return res.status(403).json({ error: 'Invalid signature' });
  }

  const event = new URL(requestUrl(req)).searchParams.get('event');

  // ---- the dial finished: log the call, answered or missed ----------------
  if (event === 'complete') {
    const status = params.DialCallStatus || 'unknown';
    await deliver(buildCallLead(params, {
      call_status: status,
      // "completed" means it connected. Anything else is a lead you did not
      // pick up — which is the one you most want to know about.
      missed: status !== 'completed',
      duration_seconds: params.DialCallDuration || '0',
    }));
    return twiml(res, '');
  }

  // ---- the recording is ready: send the link through as a follow-up -------
  if (event === 'recording') {
    if (params.RecordingUrl) {
      await deliver(buildCallLead(params, {
        call_status: 'recording',
        recording_url: params.RecordingUrl + '.mp3',
        duration_seconds: params.RecordingDuration || '0',
      }));
    }
    return twiml(res, '');
  }

  // ---- a call is coming in: announce, then connect ------------------------
  const forwardTo = process.env.FORWARD_TO_NUMBER;
  if (!forwardTo) {
    console.error('FORWARD_TO_NUMBER is not set — cannot connect the call');
    return twiml(res, '<Say>Thanks for calling. Our line is not available right now. Please try again shortly.</Say><Hangup/>');
  }

  const record = process.env.RECORD_CALLS !== 'false';
  const timeout = Number(process.env.DIAL_TIMEOUT) || 20;

  // See the header comment: in Florida this notice is what makes recording
  // lawful, so it is emitted if and only if recording is on.
  const notice = record
    ? '<Say voice="Polly.Joanna">Thanks for calling Broward Car Detailing. This call is recorded for quality. Connecting you now.</Say>'
    : '<Say voice="Polly.Joanna">Thanks for calling Broward Car Detailing. Connecting you now.</Say>';

  const dialAttrs = [
    `action="/api/voice?event=complete"`,
    `method="POST"`,
    `timeout="${timeout}"`,
    `callerId="${x(params.To || '')}"`,
    record ? 'record="record-from-answer-dual"' : '',
    record ? 'recordingStatusCallback="/api/voice?event=recording"' : '',
    record ? 'recordingStatusCallbackMethod="POST"' : '',
  ].filter(Boolean).join(' ');

  return twiml(res,
    `${notice}<Dial ${dialAttrs}><Number>${x(forwardTo)}</Number></Dial>` +
    // Reached only if the dial failed outright; a no-answer still runs action.
    `<Say voice="Polly.Joanna">Sorry, we could not connect you. Please try again or use the form on our website.</Say>`
  );
}
