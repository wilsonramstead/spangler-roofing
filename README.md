# Spangler Roofing — website redesign (demo)

A static, multi-page marketing site for **Spangler Roofing LLC** (St. Petersburg, FL).
No build tools, no frameworks, no backend — it runs by opening `index.html` directly
from disk (`file://`) or from any static host.

## Files
- `index.html` — home
- `roofing.html` — roofing services (shingle / tile / flat + repairs, storm, insurance)
- `gallery.html` — "Our Work" project gallery with lightbox
- `estimate.html` — free-estimate pitch, FAQ, contact, and request form
- `styles.css` — shared styles (design system, responsive, light/AA-contrast)
- `script.js` — shared behavior (nav, scroll reveals, FAQ, lightbox, demo form)
- `assets/` — real project photos scraped from the current site + `manifest.json`

## Demo notes for go-live
- **Remove the noindex tag.** Every page has `<meta name="robots" content="noindex">`
  with a `<!-- DEMO: remove noindex when site goes live -->` comment. Delete these so
  search engines can index the site.
- **Wire up the estimate form.** `estimate.html`'s form is demo-only: on submit it shows
  an inline "Demo mode — goes live with the site" notice and no data is sent. Connect it
  to a form service (Formspree, Netlify Forms, or a backend endpoint) — see the commented
  block in `script.js` (`#estimate-form` handler).
- **Blog + remaining content migrates on go-live.** The current Wix site includes a blog
  and some additional pages that are intentionally **not** part of this redesign demo.
  They will be migrated during launch. Plan to keep the existing domain
  **spanglerroofingllc.com** and set up **301 redirects** from all old Wix URLs to their
  new equivalents so existing SEO and inbound links are preserved.
- **Logo.** No usable logo file was present in the scraped assets (the `home_*` PNGs were a
  phone mockup, an Instagram icon, a Google-review badge, and a Florida map), so the header
  uses a clean typographic wordmark built from the brand's navy + brick-red colors. Drop in
  the real logo art when available.

## Business facts used (verify before launch)
- Spangler Roofing LLC · 5765 61st St N, St. Petersburg, FL 33709
- Phone (727) 397-3800 · spanglerroof@gmail.com
- Hours: Mon–Fri 9 AM–4 PM; Sat–Sun closed
- FL State Certified License **CCC1333650** · Established 1989 · family owned
- Google rating 4.7 (112 reviews) · Owners: Christian & Jessica

_Website by Wilson Innovations — https://wilsoninnovations.net_
