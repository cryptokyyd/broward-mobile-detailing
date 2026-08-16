/* BROWARD MOBILE DETAILING — shared behaviour.
   No framework, no build step. Progressive: every page works with JS off.
   Without JS the quote form still posts (native form POST to /api/lead) and
   every phone/text link is a real href in the markup. */

/* ------------------------------------------------------------------
   1. CONTACT CONFIG  ← the only block you need to edit.
   Put the real numbers in and every CTA on every page updates.

   These are PLACEHOLDERS. Nothing here is a working line yet — see
   README.md "Before this goes live". Search the HTML for the same
   literals too: they are hard-coded as href fallbacks so the buttons
   work with JS disabled.
   ------------------------------------------------------------------ */
const BMD = {
  whatsapp: '19545550147',        // international format, digits only, for wa.me
  phone:    '(954) 555-0147',
  email:    'quotes@browardcardetailing.com',
  instagram: '',                  // '' hides the Instagram link in the footer

  /* Call tracking. One Twilio number per channel: whichever number rings
     tells you which channel produced the call, with no dashboard involved.
     Buy a number, point it at /api/voice, and paste it here as the display
     format you want shown. Leave a channel '' and it falls back to .phone.

     The number in .phone above is the one crawlers and direct visitors see,
     so keep that one stable — it is what ends up in search results. */
  tracking: {
    google:   '',                 // ?utm_source=google  (and gclid)
    facebook: '',                 // ?utm_source=facebook (and fbclid)
    bing:     '',
    yelp:     ''
  }
};

document.documentElement.classList.add('js');

/* ------------------------------------------------------------------
   1b. Resolve the tracking number BEFORE anything wires a phone link.

   Runs ahead of the contact block on purpose: once [data-tel] hrefs are
   written, swapping the number would mean rewriting them all again. Reads
   the URL first (a first landing has no stored attribution yet), then falls
   back to what an earlier page view stored.
   ------------------------------------------------------------------ */
(function trackingNumber() {
  var numbers = BMD.tracking || {};
  if (!Object.keys(numbers).some(function (k) { return numbers[k]; })) return;

  function sourceFromQuery() {
    var q = new URLSearchParams(location.search);
    var s = (q.get('utm_source') || '').toLowerCase();
    if (s) return s;
    // Ad platforms often send only their click id, with no utm_source.
    if (q.get('gclid')) return 'google';
    if (q.get('fbclid')) return 'facebook';
    return '';
  }

  function sourceFromStorage() {
    try {
      var a = JSON.parse(sessionStorage.getItem('bmd-attr') || '{}');
      return (a.utm_source || (a.gclid ? 'google' : a.fbclid ? 'facebook' : '') || '').toLowerCase();
    } catch (e) { return ''; }
  }

  var source = sourceFromQuery() || sourceFromStorage();
  var swap = source && numbers[source];
  if (!swap) return;

  BMD.phone = swap;
  BMD.whatsapp = '1' + swap.replace(/\D/g, '').slice(-10);
})();

/* ------------------------------------------------------------------
   2. Wire contact config into the page
   ------------------------------------------------------------------ */
(function contact() {
  document.querySelectorAll('[data-tel]').forEach(function (el) {
    el.href = 'tel:' + BMD.phone.replace(/[^\d+]/g, '');
    if (el.dataset.tel === 'text') el.textContent = BMD.phone;
  });
  document.querySelectorAll('[data-sms]').forEach(function (el) {
    var body = el.dataset.sms || '';
    // ?&body= is the cross-platform form: iOS wants &, Android wants ?.
    el.href = 'sms:' + BMD.phone.replace(/[^\d+]/g, '') + (body ? '?&body=' + encodeURIComponent(body) : '');
  });
  document.querySelectorAll('[data-wa]').forEach(function (el) {
    var msg = el.dataset.wa || '';
    el.href = 'https://wa.me/' + BMD.whatsapp + (msg ? '?text=' + encodeURIComponent(msg) : '');
    el.target = '_blank';
    el.rel = 'noopener';
  });
  document.querySelectorAll('[data-email]').forEach(function (el) {
    el.href = 'mailto:' + BMD.email;
    if (el.dataset.email === 'text') el.textContent = BMD.email;
  });
})();

/* ------------------------------------------------------------------
   3. Language toggle (ES/EN)
   Broward is roughly a third Hispanic and the ES pages under /es/ are real
   URLs, not this toggle — Google only indexes what is in the HTML. This
   toggle is a convenience on the English pages, nothing more.
   ------------------------------------------------------------------ */
(function language() {
  var btn = document.querySelector('[data-lang-toggle]');
  if (!btn) return;

  var nodes = document.querySelectorAll('[data-es]');
  var fields = document.querySelectorAll('[data-es-ph]');

  nodes.forEach(function (el) { el.dataset.en = el.innerHTML; });
  fields.forEach(function (el) { el.dataset.enPh = el.placeholder; });

  function apply(lang) {
    var es = lang === 'es';
    nodes.forEach(function (el) { el.innerHTML = es ? el.dataset.es : el.dataset.en; });
    fields.forEach(function (el) { el.placeholder = es ? el.dataset.esPh : el.dataset.enPh; });
    document.documentElement.lang = es ? 'es' : 'en';
    btn.textContent = es ? 'EN' : 'ES';
    btn.setAttribute('aria-label', es ? 'Switch to English' : 'Cambiar a español');
    try { localStorage.setItem('bmd-lang', lang); } catch (e) { /* private mode */ }
  }

  var saved;
  try { saved = localStorage.getItem('bmd-lang'); } catch (e) { saved = null; }
  if (!saved && (navigator.language || '').toLowerCase().indexOf('es') === 0) saved = 'es';
  apply(saved === 'es' ? 'es' : 'en');

  btn.addEventListener('click', function () {
    apply(document.documentElement.lang === 'es' ? 'en' : 'es');
  });
})();

/* ------------------------------------------------------------------
   4. Mobile nav
   ------------------------------------------------------------------ */
(function nav() {
  var burger = document.querySelector('.burger');
  var panel = document.getElementById('mobile-nav');
  if (!burger || !panel) return;

  function close() {
    panel.classList.remove('is-open');
    burger.setAttribute('aria-expanded', 'false');
    document.body.classList.remove('nav-open');
  }
  burger.addEventListener('click', function () {
    var open = burger.getAttribute('aria-expanded') === 'true';
    panel.classList.toggle('is-open', !open);
    burger.setAttribute('aria-expanded', String(!open));
    // The sticky CTA hides while the drawer is open; a tall drawer reaches the
    // bottom of the screen and would otherwise run underneath it.
    document.body.classList.toggle('nav-open', !open);
  });
  panel.addEventListener('click', function (e) { if (e.target.tagName === 'A') close(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();

/* ------------------------------------------------------------------
   4b. Nav dropdowns.
   CSS opens them on hover and on focus-within, which covers mouse and
   keyboard. This adds the tap: a touch device fires no hover, so the chevron
   has to be a real button.
   ------------------------------------------------------------------ */
(function navMenus() {
  var items = document.querySelectorAll('.nav__item');
  if (!items.length) return;

  function closeAll(except) {
    items.forEach(function (item) {
      if (item === except) return;
      item.classList.remove('is-open');
      var b = item.querySelector('.nav__more');
      if (b) b.setAttribute('aria-expanded', 'false');
    });
  }

  items.forEach(function (item) {
    var btn = item.querySelector('.nav__more');
    if (!btn) return;
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      var open = item.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
      closeAll(item);
    });
  });

  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    var open = document.querySelector('.nav__item.is-open');
    closeAll(null);
    if (open) { var b = open.querySelector('.nav__more'); if (b) b.focus(); }
  });

  document.addEventListener('click', function (e) {
    if (!e.target.closest('.nav__item')) closeAll(null);
  });
})();

/* ------------------------------------------------------------------
   5. Reveal — enhances content that is already visible and already painted.
   Nothing is gated on this running.
   ------------------------------------------------------------------ */
(function reveal() {
  var items = document.querySelectorAll('.rise');
  if (!items.length) return;

  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('is-in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry, i) {
      if (!entry.isIntersecting) return;
      var el = entry.target;
      var delay = parseInt(el.dataset.delay || (i * 70), 10);
      setTimeout(function () { el.classList.add('is-in'); }, delay);
      io.unobserve(el);
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

  items.forEach(function (el) { io.observe(el); });

  // Safety net: if anything is still hidden after load, show it.
  window.addEventListener('load', function () {
    setTimeout(function () {
      document.querySelectorAll('.rise:not(.is-in)').forEach(function (el) {
        var r = el.getBoundingClientRect();
        if (r.top < window.innerHeight) el.classList.add('is-in');
      });
    }, 400);
  });
})();

/* ------------------------------------------------------------------
   6. Attribution capture.
   The lead IS the product here, and a lead nobody can source is worth less
   than one tagged to the campaign that produced it. Grab the UTM tags on
   first landing and keep them for the session, so a visitor who arrives on
   an ad and converts three pages later still carries the source.

   Deliberately NOT captured: anything that identifies the person before they
   choose to identify themselves. No fingerprinting, no third-party pixels.
   ------------------------------------------------------------------ */
var attribution = (function () {
  var KEY = 'bmd-attr';
  var FIELDS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'fbclid'];

  function read() {
    try { return JSON.parse(sessionStorage.getItem(KEY) || '{}'); } catch (e) { return {}; }
  }

  var stored = read();
  var q = new URLSearchParams(location.search);
  var fresh = {};
  FIELDS.forEach(function (f) { if (q.get(f)) fresh[f] = q.get(f).slice(0, 120); });

  // First touch wins: overwriting on a later page view would credit the last
  // internal click instead of the ad that actually paid for the visit.
  if (Object.keys(fresh).length && !Object.keys(stored).length) {
    if (document.referrer && document.referrer.indexOf(location.host) === -1) {
      fresh.referrer = document.referrer.slice(0, 200);
    }
    fresh.landing = location.pathname.slice(0, 120);
    stored = fresh;
    try { sessionStorage.setItem(KEY, JSON.stringify(stored)); } catch (e) { /* private mode */ }
  } else if (!Object.keys(stored).length) {
    stored = { landing: location.pathname.slice(0, 120) };
    if (document.referrer && document.referrer.indexOf(location.host) === -1) {
      stored.referrer = document.referrer.slice(0, 200);
    }
    try { sessionStorage.setItem(KEY, JSON.stringify(stored)); } catch (e) { /* private mode */ }
  }

  return function () { return read(); };
})();

/* ------------------------------------------------------------------
   7. Quote form.
   Posts JSON to /api/lead. The form element carries a real action and method,
   so with JS off the browser does a normal POST and the function replies with
   a plain HTML thank-you. With JS on we stay on the page and swap in a
   confirmation, which is worth a few percent of completions.
   ------------------------------------------------------------------ */
(function quoteForm() {
  var forms = document.querySelectorAll('form[data-quote]');
  if (!forms.length) return;

  forms.forEach(function (form) {
    var status = form.querySelector('[data-status]');
    var submit = form.querySelector('button[type="submit"], input[type="submit"]');

    form.addEventListener('submit', function (e) {
      if (!form.reportValidity()) return;          // let the browser speak first
      e.preventDefault();

      var es = document.documentElement.lang === 'es';
      var data = {};
      new FormData(form).forEach(function (v, k) { data[k] = typeof v === 'string' ? v : ''; });
      data.attribution = attribution();
      data.page = location.pathname;

      if (submit) { submit.disabled = true; }
      if (status) {
        status.classList.remove('is-error', 'vh');
        status.textContent = es ? 'Enviando…' : 'Sending…';
      }

      fetch(form.getAttribute('action') || '/api/lead', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      }).then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      }).then(function () {
        var ok = document.createElement('div');
        ok.className = 'quote-ok';
        ok.setAttribute('role', 'status');
        ok.innerHTML = es
          ? '<h3>Recibido. Le llamamos hoy.</h3><p>Le enviamos el precio cerrado por mensaje. Si tiene prisa, llame al <a data-tel="text" href="#">' + BMD.phone + '</a>.</p>'
          : '<h3>Got it. We’ll call you today.</h3><p>You’ll get the full price by text — no visit needed. In a hurry? Call <a data-tel="text" href="#">' + BMD.phone + '</a>.</p>';
        form.replaceWith(ok);
        // The swapped-in block has its own phone link; wire it like the rest.
        ok.querySelectorAll('[data-tel]').forEach(function (el) {
          el.href = 'tel:' + BMD.phone.replace(/[^\d+]/g, '');
        });
        ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }).catch(function () {
        if (submit) { submit.disabled = false; }
        if (status) {
          status.classList.add('is-error');
          // Never strand the lead on a failure — hand them the phone number.
          status.textContent = es
            ? 'No se pudo enviar. Llame o escriba al ' + BMD.phone + '.'
            : 'That didn’t send. Please call or text ' + BMD.phone + '.';
        }
      });
    });
  });
})();

/* ------------------------------------------------------------------
   8. Sticky call bar.
   Phones and tablets only. Shows once the opening CTAs have scrolled away and
   hides again over the closing one, so the page never offers the same action
   twice at the same time.
   ------------------------------------------------------------------ */
(function stickyCta() {
  if (!document.querySelector('.hero')) return;

  var es = document.documentElement.lang === 'es';
  var bar = document.createElement('div');
  bar.className = 'sticky-cta';
  bar.hidden = true;

  var a = document.createElement('a');
  a.className = 'btn btn--primary';
  a.href = 'tel:' + BMD.phone.replace(/[^\d+]/g, '');
  a.textContent = (es ? 'Llamar ' : 'Call ') + BMD.phone;
  bar.appendChild(a);
  document.body.appendChild(bar);

  var opening = document.querySelector('.hero .btn-row') || document.querySelector('.strip');
  var closing = document.querySelector('.cta-final');
  var passedOpening = false, overClosing = false;

  function sync() {
    var show = passedOpening && !overClosing;
    bar.hidden = !show;
    document.body.classList.toggle('has-sticky-cta', show);
  }

  if (!('IntersectionObserver' in window)) return;   // bar simply stays hidden

  if (opening) {
    new IntersectionObserver(function (entries) {
      var e = entries[0];
      passedOpening = !e.isIntersecting && e.boundingClientRect.top < 0;
      sync();
    }, { threshold: 0 }).observe(opening);
  } else {
    window.addEventListener('scroll', function () {
      var passed = window.scrollY > window.innerHeight * 0.6;
      if (passed !== passedOpening) { passedOpening = passed; sync(); }
    }, { passive: true });
  }

  if (closing) {
    new IntersectionObserver(function (entries) {
      overClosing = entries[0].isIntersecting;
      sync();
    }, { threshold: 0 }).observe(closing);
  }
  sync();
})();
