/**
 * node api/lead.test.mjs
 *
 * Covers the pure helpers only — the parts that decide whether a lead is real
 * and what gets forwarded. Delivery is network and is exercised by actually
 * submitting the form against a preview deployment.
 */
import assert from 'node:assert/strict';
import { test } from 'node:test';
import { normalizePhone, validPhone, validEmail, buildLead, looksAutomated } from './lead.js';

test('normalizePhone strips formatting and the country code', () => {
  assert.equal(normalizePhone('(954) 555-0147'), '9545550147');
  assert.equal(normalizePhone('+1 954 555 0147'), '9545550147');
  assert.equal(normalizePhone('19545550147'), '9545550147');
  assert.equal(normalizePhone(''), '');
  assert.equal(normalizePhone(null), '');
});

test('validPhone accepts real US numbers', () => {
  assert.ok(validPhone('954-555-0147'));
  assert.ok(validPhone('+1 (754) 555 0198'));
  assert.ok(validPhone('7865550123'));
});

test('validPhone rejects junk', () => {
  assert.ok(!validPhone('5550147'), 'too short');
  assert.ok(!validPhone('9545550147999'), 'too long');
  assert.ok(!validPhone('0000000000'), 'all same digit');
  assert.ok(!validPhone('1234567890'), 'area code cannot start with 1');
  assert.ok(!validPhone('0123456789'), 'area code cannot start with 0');
  assert.ok(!validPhone(''), 'empty');
});

test('validEmail treats blank as fine, since the field is optional', () => {
  assert.ok(validEmail(''));
  assert.ok(validEmail('  '));
  assert.ok(validEmail('me@example.com'));
  assert.ok(!validEmail('me@example'));
  assert.ok(!validEmail('nope'));
});

test('buildLead requires a name and a phone', () => {
  const { errors } = buildLead({});
  assert.ok(errors.some((e) => e.includes('name')));
  assert.ok(errors.some((e) => e.includes('phone')));
});

test('buildLead adds E.164 and keeps only known fields', () => {
  const { lead, errors } = buildLead({
    name: 'Ana Ruiz',
    phone: '(954) 555-0147',
    city: 'Pembroke Pines',
    service: 'Full detail',
    evil: 'DROP TABLE leads',
  });
  assert.deepEqual(errors, []);
  assert.equal(lead.phone_e164, '+19545550147');
  assert.equal(lead.city, 'Pembroke Pines');
  assert.equal(lead.evil, undefined, 'unknown fields must not survive');
});

test('buildLead bounds long input rather than rejecting it', () => {
  const { lead } = buildLead({ name: 'x'.repeat(500), phone: '9545550147' });
  assert.equal(lead.name.length, 80);
});

test('buildLead keeps attribution but bounds it', () => {
  const { lead } = buildLead({
    name: 'Ana',
    phone: '9545550147',
    attribution: { utm_source: 'google', utm_campaign: 'y'.repeat(400), junk: 42 },
  });
  assert.equal(lead.attribution.utm_source, 'google');
  assert.equal(lead.attribution.utm_campaign.length, 200);
  assert.equal(lead.attribution.junk, undefined, 'non-strings are dropped');
});

test('buildLead survives a non-object attribution', () => {
  for (const bad of ['nope', 42, null, ['a'], undefined]) {
    const { lead } = buildLead({ name: 'Ana', phone: '9545550147', attribution: bad });
    assert.equal(lead.attribution, undefined);
  }
});

test('looksAutomated catches the honeypot and instant submits', () => {
  assert.ok(looksAutomated({ company: 'SEO Services Ltd' }), 'honeypot filled');
  assert.ok(looksAutomated({ elapsed: '400' }), 'submitted in 0.4s');
  assert.ok(!looksAutomated({ elapsed: '9000' }), 'a real fill takes seconds');
  assert.ok(!looksAutomated({}), 'no signal is not a bot');
  assert.ok(!looksAutomated({ elapsed: 'abc' }), 'unparseable is not a bot');
});
