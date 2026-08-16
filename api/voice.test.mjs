/**
 * node api/voice.test.mjs
 *
 * The signature check is the security boundary on this endpoint — get it
 * wrong and anyone who finds the URL can place calls on your Twilio balance.
 * These vectors are built with Twilio's documented algorithm.
 */
import assert from 'node:assert/strict';
import { test } from 'node:test';
import crypto from 'node:crypto';
import { expectedSignature, signatureValid, requestUrl, buildCallLead } from './voice.js';

const TOKEN = 'test_auth_token_12345';
const URL_ = 'https://browardcardetailing.com/api/voice';

function sign(url, params, token = TOKEN) {
  let data = url;
  for (const k of Object.keys(params).sort()) data += k + params[k];
  return crypto.createHmac('sha1', token).update(Buffer.from(data, 'utf-8')).digest('base64');
}

test('expectedSignature matches an independent implementation', () => {
  const params = { CallSid: 'CA123', From: '+17865572897', To: '+19545550147' };
  assert.equal(expectedSignature(URL_, params, TOKEN), sign(URL_, params));
});

test('params are concatenated in lexical key order, not insertion order', () => {
  const a = { Zebra: '1', Apple: '2' };
  const b = { Apple: '2', Zebra: '1' };
  assert.equal(expectedSignature(URL_, a, TOKEN), expectedSignature(URL_, b, TOKEN));
});

test('signatureValid accepts a correct signature', () => {
  const params = { CallSid: 'CA123', From: '+17865572897' };
  assert.ok(signatureValid(URL_, params, sign(URL_, params), TOKEN));
});

test('signatureValid rejects tampering', () => {
  const params = { CallSid: 'CA123', From: '+17865572897' };
  const good = sign(URL_, params);
  assert.ok(!signatureValid(URL_, { ...params, From: '+19995551234' }, good, TOKEN),
    'a changed param must invalidate');
  assert.ok(!signatureValid('https://evil.example/api/voice', params, good, TOKEN),
    'a changed URL must invalidate');
  assert.ok(!signatureValid(URL_, params, good, 'wrong_token'),
    'a wrong auth token must invalidate');
  assert.ok(!signatureValid(URL_, params, 'bm90LWEtc2ln', TOKEN), 'garbage must fail');
});

test('signatureValid fails closed on missing inputs', () => {
  const params = { CallSid: 'CA123' };
  assert.ok(!signatureValid(URL_, params, undefined, TOKEN), 'no signature header');
  assert.ok(!signatureValid(URL_, params, sign(URL_, params), undefined), 'no auth token');
  assert.ok(!signatureValid(URL_, params, '', TOKEN), 'empty signature');
});

test('signatureValid survives a length mismatch without throwing', () => {
  // timingSafeEqual throws when buffers differ in length; we must not.
  assert.doesNotThrow(() => signatureValid(URL_, { A: '1' }, 'short', TOKEN));
  assert.equal(signatureValid(URL_, { A: '1' }, 'short', TOKEN), false);
});

test('requestUrl rebuilds the public URL from forwarded headers', () => {
  const req = {
    headers: { 'x-forwarded-proto': 'https', 'x-forwarded-host': 'browardcardetailing.com' },
    url: '/api/voice?event=complete',
  };
  assert.equal(requestUrl(req), 'https://browardcardetailing.com/api/voice?event=complete');
});

test('requestUrl falls back to host when x-forwarded-host is absent', () => {
  const req = { headers: { host: 'localhost:4400' }, url: '/api/voice' };
  assert.equal(requestUrl(req), 'https://localhost:4400/api/voice');
});

test('buildCallLead carries the caller and the tracking number', () => {
  const lead = buildCallLead({
    From: '+17865572897', To: '+19545550147', CallSid: 'CA9',
    FromCity: 'HIALEAH', FromState: 'FL',
  });
  assert.equal(lead.kind, 'call');
  assert.equal(lead.phone_e164, '+17865572897');
  assert.equal(lead.city, 'HIALEAH, FL');
  assert.equal(lead.attribution.tracking_number, '+19545550147');
});

test('buildCallLead marks a missed call', () => {
  const lead = buildCallLead({ From: '+1786', To: '+1954' },
    { call_status: 'no-answer', missed: true });
  assert.equal(lead.missed, true);
  assert.equal(lead.call_status, 'no-answer');
});

test('buildCallLead tolerates an empty payload', () => {
  const lead = buildCallLead({});
  assert.equal(lead.phone, '');
  assert.equal(lead.city, '');
  assert.equal(lead.attribution, undefined, 'no To means no tracking attribution');
});
