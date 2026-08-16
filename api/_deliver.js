/**
 * Shared lead delivery. Imported by lead.js (form fills) and voice.js (calls),
 * so a phone lead and a web lead arrive in the same place, in the same shape,
 * carrying the same attribution fields.
 *
 * Files under api/ that start with "_" are not routed by Vercel, so this is a
 * module rather than an endpoint.
 *
 * Env vars (all optional; every configured channel is attempted and the lead
 * is accepted if at least one succeeds):
 *   LEAD_WEBHOOK_URL   POST the JSON anywhere (Zapier, Make, n8n, your CRM)
 *   RESEND_API_KEY     email it
 *   LEAD_EMAIL_TO      where to (comma-separated for several)
 *   LEAD_EMAIL_FROM    must be a domain verified in Resend
 */

export function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) => (
    { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]
  ));
}

export async function deliver(lead) {
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

    // A call lead and a form lead want different subject lines — you triage
    // a missed call differently from a form fill.
    const subject = lead.kind === 'call'
      ? `${lead.call_status === 'completed' ? 'Call' : 'MISSED CALL'} — ${lead.phone}${lead.city ? ', ' + lead.city : ''}`
      : `New detail lead — ${lead.name}${lead.city ? ', ' + lead.city : ''}`;

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
          subject,
          html: `<h2 style="font:600 18px system-ui">${lead.kind === 'call' ? 'Phone lead' : 'New lead'}</h2>
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
    // Nothing wired up. The log is the record — see README, it rolls off.
    console.log('LEAD (no delivery channel configured)', JSON.stringify(lead));
    return { delivered: ['log'], failed: [] };
  }

  const settled = await Promise.allSettled(results);
  const delivered = settled.filter((s) => s.status === 'fulfilled').map((s) => s.value);
  const failed = settled.filter((s) => s.status === 'rejected').map((s) => String(s.reason));

  if (!delivered.length) {
    console.error('LEAD DELIVERY FAILED', JSON.stringify(lead), failed);
  } else if (failed.length) {
    console.warn('lead partially delivered', failed);
  }

  return { delivered, failed };
}
