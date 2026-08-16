# Broward Mobile Detailing — lead-generation site

Static site. No build step to deploy, no dependencies. Every page is committed
HTML; `build-pages.py` regenerates them from the data at the top of that file.

```bash
python build-pages.py          # regenerate all 65 pages + sitemap.xml
python -m http.server 4400     # then open http://localhost:4400
node api/lead.test.mjs         # test the lead endpoint's logic
```

## What's here

| File | What it is |
|---|---|
| `build-pages.py` | **The whole site comes out of here.** Services, cities, core pages, sitemap |
| `index.html` | Home — hero, quote form, services, packages, county grid, FAQ |
| `services.html` | All nine services with starting prices |
| `pricing.html` | Every price plus what each vehicle size adds |
| `areas.html` | All 31 Broward municipalities |
| `about.html` | The straight-price argument |
| `contact.html` | The long quote form |
| `*-mobile-detailing.html` | 20 city landing pages (ES twins in `es/`) |
| `*-broward.html` | 9 service landing pages (ES twins in `es/`) |
| `es/` | Real Spanish URLs, joined to the English pages with hreflang |
| `api/lead.js` | Serverless lead capture — the only server-side code |
| `styles.css` | The whole design system, OKLCH tokens at the top |
| `main.js` | Contact config, attribution capture, form, nav, reveal |

Page count: 9 services + 20 cities, each in two languages, plus 6 core pages
and a Spanish home. 65 HTML files, 65 URLs in `sitemap.xml`.

## Before this goes live — the blockers

> ### ⚠️ The site is currently `noindex`, on purpose
>
> `vercel.json` sends `X-Robots-Tag: noindex, nofollow` on every path, so
> Google will not index a site advertising the placeholder number
> `(954) 555-0147`. A test number in live search results is genuinely painful
> to undo.
>
> **To launch: delete the `/(.*)` block from `headers` in `vercel.json` and
> push.** Do that only once item 1 below is done. It is the last step, not
> the first.

These are in order. The first three are genuine blockers; nothing should get
ad spend until they are done.

1. **The phone number and email are fake.** `(954) 555-0147` is a reserved
   test number and it is on every page. Change `BMD.phone`, `BMD.whatsapp` and
   `BMD.email` at the top of `main.js`, then search-replace `+19545550147`,
   `(954) 555-0147` and `quotes@browardmobiledetailing.com` across the HTML and
   in `build-pages.py` — they are hard-coded as `href` fallbacks so the buttons
   still work with JavaScript disabled. Regenerate after editing the script.

2. **Nothing receives the leads yet.** `api/lead.js` accepts a submission and,
   with no environment variables set, writes it to the Vercel log and returns
   success. Logs roll off. Set at least `LEAD_WEBHOOK_URL` before you send
   anyone to this site. See "Turning on lead delivery" below.

3. **There are no photographs.** Detailing is a before-and-after trade and this
   site currently has zero proof. The layout has slots waiting for it — the
   service tiles on the home page take a background image, and `.ba` renders a
   labelled frame for before/after pairs. Drop files into `assets/media/` and
   reference them. **Ten real phone photos of finished cars will do more for
   conversion than any further change to this code.** Do not use stock images
   of cars that are not yours; the whole argument this site makes is that the
   price and the work are honest.

4. **The prices are researched, not quoted by you.** $99 exterior / $199 full /
   $699 ceramic are plausible Broward market rates, and they are on 65 pages and
   in the JSON-LD. Whoever actually does the work has to honour them. If you are
   selling these leads on, agree the price list with the detailer buying them
   **before** launch — a lead that arrives expecting $199 and gets quoted $340
   is a lead that gets refunded and a buyer you lose.

5. **The domain.** Every canonical URL and the sitemap point at
   `https://browardmobiledetailing.com`. That is the one you bought — of the
   variants I checked, it is the only one already registered. If it is actually
   a different one, change `BASE` at the top of `build-pages.py` and rerun.
   Getting this wrong tells Google to index a hostname that does not resolve.

6. **Business facts to confirm or remove.** "Mon–Sat, 8am–6pm" on
   `contact.html` and the twelve-month headlight guarantee are assumptions.
   Make them true or take them out.

## Turning on lead delivery

Vercel → Settings → Environment Variables. Every channel configured is
attempted, and the lead is accepted if at least one succeeds.

| Variable | Needed | What it does |
|---|---|---|
| `LEAD_WEBHOOK_URL` | Recommended | POSTs the lead as JSON. Zapier, Make, n8n, or your own CRM |
| `RESEND_API_KEY` | Optional | Emails the lead |
| `LEAD_EMAIL_TO` | With Resend | Where it goes. Comma-separated for several |
| `LEAD_EMAIL_FROM` | With Resend | Must be on a domain verified in Resend |

The fastest working setup: a Zapier catch hook into a Google Sheet, plus an SMS
to yourself. Ninety seconds, and you stop losing leads.

### What a lead looks like

```json
{
  "name": "Ana Ruiz",
  "phone": "(954) 555-0147",
  "phone_e164": "+19545550147",
  "city": "Pembroke Pines",
  "vehicle": "2021 Toyota Camry",
  "service": "Full detail",
  "attribution": { "utm_source": "google", "utm_campaign": "broward-full-detail",
                   "landing": "/pembroke-pines-mobile-detailing.html" },
  "page": "/contact.html",
  "received_at": "2026-08-15T18:04:11.204Z"
}
```

`attribution` is the field that matters if you sell these on. It is captured on
first landing and survives across pages, so a lead that arrived on an ad and
converted three pages later still carries the campaign that paid for it. First
touch wins deliberately — overwriting it later would credit the last internal
click instead of the ad.

Nothing identifying is collected before someone fills the form in. No
fingerprinting, no third-party pixels.

## Spam handling

Two filters, both in `api/lead.js`:

- a honeypot field named `company`, positioned off-screen rather than
  `display:none` because some bots skip hidden inputs
- a submit-speed check — anything completed in under 2.5 seconds is a script

Both fail **silently with a 200**. Telling a bot it was blocked only teaches it
to try again with the hidden field left alone.

## Adding a city

Add an entry to `CITIES` in `build-pages.py` and rerun it. It needs its own
`para` and `para_es` paragraphs — genuinely about that city.

This is not a style preference. Twenty pages that differ only by a swapped city
name are the textbook definition of doorway pages, and Google demotes the whole
domain for it, not just the thin pages. If you cannot write something true and
specific about a city, leave it off the list — it is still covered by
`areas.html`, which is enough to be findable.

The eleven smallest municipalities are deliberately listed as plain text on
`areas.html` rather than given pages, for exactly this reason.

## Deploying

Vercel, connected to this repository. `vercel.json` sets `cleanUrls`, so
`/pricing.html` is served at `/pricing` — `sitemap.xml` already emits the clean
form, and the two must not drift apart or every sitemap entry becomes a
redirect.

**There is deliberately no `build` script in `package.json`.** The generator is
`npm run pages`, and that name is load bearing: Vercel auto-runs any script
called `build`, then fails the deploy hunting for a `public/` directory that a
site of committed HTML never produces. That exact error killed the first
deploy. `outputDirectory: "."` in `vercel.json` states the same thing a second
way — the site *is* the repo root, there is no build output.

Regenerate pages locally and commit the result. That keeps the deploy a plain
file copy with no dependency on Python being present in Vercel's build image.

<details>
<summary>How this repo was split out of <code>luxsea-miami</code> (historical)</summary>

The site began as a subdirectory of the `luxsea-miami` repository and was
moved with:

```bash
git subtree split --prefix=broward-mobile-detailing -b broward-only
git push git@github.com:<you>/broward-mobile-detailing.git broward-only:main
```

That carried the commit history across, which is why the first commit here
predates the repository.

</details>

## What was reused

The layout engine came from the LuxSea Miami site: the grid and band system,
buttons, nav with its dropdowns, forms, the reveal-on-scroll, the sticky mobile
bar, and the generate-pages-from-a-data-file approach. All of the tokens, the
type, the components specific to this trade, every word of copy, and the
lead endpoint are new. There is no shared code at runtime — the two sites do
not depend on each other, and editing one cannot break the other.
