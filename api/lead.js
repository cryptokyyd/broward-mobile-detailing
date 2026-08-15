/**
 * POST /api/lead
 *
 * The lead is the product, so this function's job is: never lose one, never
 * forward junk, and never hold customer data longer than it takes to hand it
 * on.
 *
 * Accepts both shapes:
 *   - application/json           — the fetch() path in main.js
 *   - form-urlencoded            — a plain browser POST with JS disabled
 * and answers in kind (JSON, or a small HTML thank-you page).
 *
 * Delivery, in order. Every configured channel is attempted; the lead is
 * accepted if AT LEAST ONE succeeds:
 *   1. LEAD_WEBHOOK_URL   — POST the JSON anywhere (Zapier, Make, n8n, your CRM)
 *   2. RESEND_API_KEY     — email it to LEAD_EMAIL_TO
 *   3. console            — always, as the last-resort record in Vercel logs
 *
 * Set these in Vercel → Settings → Environment Variables:
 *   LEAD_WEBHOOK_URL   (optional)  https://hooks.zapier.com/...
 *   RESEND_API_KEY     (optional)  re_...
 *   LEAD_EMAIL_TO      (required if RESEND_API_KEY is set)
 *   LEAD_EMAIL_FROM    (required if RESEND_API_KEY is set)  must be a verified domain
 *
 * With NOTHING configured the endpoint still returns 200 and the lead lands in
 * the Vercel log. That is a safety net for launch day, not a place to run a
 * business from — logs roll off. Wire up a webhook before spending on ads.
 */

const MAX_BODY = 16 * 1024;          // a quote form has no business being bigger

/** Fields we keep. Anything else a client posts is dropped on the floor. */
const FIELDS = {
  name:     { max: 80,  required: true },
  phone:    { max: 32,  required: true },
  email:    { max: 120, required: false },
  city:     { max: 60,  required: false },
  vehicle:  { max: 80,  required: false },
  service:  { max: 60,  required: false },
  notes:    { max: 800, required: false },
};

export function normalizePhone(raw) {
  const digits = String(raw || '').replace(/\D/g, '');
  // US numbers arrive as 10, or 11 with the country code.
  if (digits.length === 11 && digits[0] === '1') return digits.slice(1);
  return digits;
}

export function validPhone(raw) {
  const d = normalizePhone(raw);
  if (d.length !== 10) return false;
  if (/^(\d)\1{9}$/.test(d)) return false;         // 0000000000, 5555555555
  if (d[0] === '0' || d[0] === '1') return false;  // no valid NANP area code starts here
  return true;
}

export function validEmail(raw) {
  const v = String(raw || '').trim();
  if (!v) return true;                              // optional field
  return /^[^\s@]+@[^\s@]+\.[a-z]{2,}$/i.test(v);
}

/**
 * Strip and bound every field. Returns {lead, errors}.
 * Nothing reaches a webhook or an inbox without passing through here.
 */
export function buildLead(body) {
  const errors = [];
  const lead = {};

  for (const [key, rule] of Object.entries(FIELDS)) {
    const value = String(body[key] ?? '').trim().slice(0, rule.max);
    if (rule.required && !value) errors.push(`${key} is required`);
    if (value) lead[key] = value;
  }

  if (lead.phone && !validPhone(lead.phone)) errors.push('phone is not a valid US number');
  if (lead.email && !validEmail(lead.email)) errors.push('email is not valid');

  if (lead.phone) {
    lead.phone_e164 = '+1' + normalizePhone(lead.phone);
  }

  // Attribution rides along so a bought lead can be traced to the campaign
  // that produced it. Bounded the same way as everything else.
  const attr = body.attribution;
  if (attr && typeof attr === 'object' && !Array.isArray(attr)) {
    const clean = {};
    for (const [k, v] of Object.entries(attr).slice(0, 12)) {
      if (typeof v === 'string' && v) clean[String(k).slice(0, 40)] = v.slice(0, 200);
    }
    if (Object.keys(clean).length) lead.attribution = clean;
  }
  if (body.page) lead.page = String(body.page).slice(0, 120);

  return { lead, errors };
}

/** Honeypot + submit-speed. Bots fill hidden inputs and submit instantly. */
export function looksAutomated(body) {
  if (String(body.company ?? '').trim()) return true;        // hidden field, humans never see it
  const elapsed = Number(body.elapsed);
  if (Number.isFinite(elapsed) && elapsed > 0 && elapsed < 2500) return true;
  return false;
}

function parseBody(req) {
  const type = String(req.headers['content-type'] || '');
  const raw = req.body;

  // Vercel's Node runtime parses JSON and urlencoded bodies for us, but a
  // string can still arrive when the content-type is unexpected.
  if (raw && typeof raw === 'object') return raw;
  if (typeof raw === 'string') {
    if (raw.length > MAX_BODY) throw new Error('body too large');
    if (type.includes('application/json')) return JSON.parse(raw);
    return Object.fromEntries(new URLSearchParams(raw));
  }
  return {};
}

async function deliver(lead) {
  const results = [];

  if (process.env.LEAD_WEBHOOK_URL) {
    results.push(
      fetch(process.env.LEAD_WEBHOOK_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(lead),
      }).then((r) => {
        if (!r.ok) throw new Error(`webhook ${r.status}`);
        return 'webhook';
      })
    );
  }

  if (process.env.RESEND_API_KEY && process.env.LEAD_EMAIL_TO && process.env.LEAD_EMAIL_FROM) {
    const rows = Object.entries(lead)
      .filter(([k]) => k !== 'attribution')
      .map(([k, v]) => `<tr><td style="padding:4px 12px 4px 0;color:#666">${k}</td><td><b>${escapeHtml(String(v))}</b></td></tr>`)
      .join('');
    const attrRows = lead.attribution
      ? Object.entries(lead.attribution).map(([k, v]) => `<tr><td style="padding:2px 12px 2px 0;color:#999">${k}</td><td>${escapeHtml(v)}</td></tr>`).join('')
      : '';

    results.push(
      fetch('https://api.resend.com/emails', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          from: process.env.LEAD_EMAIL_FROM,
          to: process.env.LEAD_EMAIL_TO.split(',').map((s) => s.trim()).filter(Boolean),
          reply_to: lead.email || undefined,
          subject: `New detail lead — ${lead.name}${lead.city ? ', ' + lead.city : ''}`,
          html: `<h2 style="font:600 18px system-ui">New lead</h2>
<table style="font:14px system-ui;border-collapse:collapse">${rows}</table>
${attrRows ? `<h3 style="font:600 13px system-ui;color:#666;margin-top:20px">Source</h3><table style="font:12px system-ui;border-collapse:collapse">${attrRows}</table>` : ''}`,
        }),
      }).then((r) => {
        if (!r.ok) throw new Error(`resend ${r.status}`);
        return 'email';
      })
    );
  }

  if (!results.length) {
    // Nothing wired up. The log is the record — see the header comment.
    console.log('LEAD (no delivery channel configured)', JSON.stringify(lead));
    return { delivered: ['log'], failed: [] };
  }

  const settled = await Promise.allSettled(results);
  const delivered = settled.filter((s) => s.status === 'fulfilled').map((s) => s.value);
  const failed = settled.filter((s) => s.status === 'rejected').map((s) => String(s.reason));

  if (!delivered.length) {
    // Every channel failed. Log it so the lead is recoverable by hand.
    console.error('LEAD DELIVERY FAILED', JSON.stringify(lead), failed);
  } else if (failed.length) {
    console.warn('lead partially delivered', failed);
  }

  return { delivered, failed };
}

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

export default async function handler(req, res) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'Method not allowed' });
  }

  let body;
  try {
    body = parseBody(req);
  } catch {
    return res.status(400).json({ error: 'Bad request' });
  }

  const wantsHtml = !String(req.headers['content-type'] || '').includes('application/json');

  // Silently accept bot submissions. Telling a bot it failed just teaches it
  // to try again with the hidden field left blank.
  if (looksAutomated(body)) {
    return wantsHtml ? htmlReply(res, 200) : res.status(200).json({ ok: true });
  }

  const { lead, errors } = buildLead(body);
  if (errors.length) {
    return wantsHtml
      ? htmlReply(res, 400, errors.join('. '))
      : res.status(400).json({ error: 'Validation failed', details: errors });
  }

  lead.received_at = new Date().toISOString();

  let outcome;
  try {
    outcome = await deliver(lead);
  } catch (err) {
    console.error('LEAD DELIVERY THREW', JSON.stringify(lead), err);
    outcome = { delivered: [], failed: [String(err)] };
  }

  // A lead that reached no channel is a lost sale — say so, so the browser can
  // show the phone number instead of a false confirmation.
  if (!outcome.delivered.length) {
    return wantsHtml
      ? htmlReply(res, 502, 'We could not record that. Please call us.')
      : res.status(502).json({ error: 'Could not record the request' });
  }

  return wantsHtml
    ? htmlReply(res, 200)
    : res.status(200).json({ ok: true, delivered: outcome.delivered });
}

/** The no-JS path. Small, self-contained, no stylesheet dependency. */
function htmlReply(res, status, problem) {
  const ok = status === 200;
  res.setHeader('Content-Type', 'text/html; charset=utf-8');
  return res.status(status).send(`<!doctype html>
<html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex">
<title>${ok ? 'Request received' : 'Something went wrong'}</title>
<body style="font:16px/1.6 system-ui,sans-serif;max-width:34rem;margin:12vh auto;padding:0 1.25rem;color:#1b1d26">
<h1 style="font-size:1.6rem">${ok ? 'Got it. We’ll call you today.' : 'That didn’t go through.'}</h1>
<p>${ok
    ? 'You’ll get the full price by text — no visit needed.'
    : escapeHtml(problem || 'Please try again.')}</p>
<p><a href="/" style="color:#2f57c9">Back to the site</a></p>
</body></html>`);
}
