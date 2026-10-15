# Old URLs from the domain's earlier sites (2016 site, 2022/2024 WordPress, 2026 Wix),
# found via the Internet Archive. Each gets a tiny stub page that sends visitors and
# Google to the closest page on the current site. Stub = meta refresh + canonical + JS.
B = "blog/"
REDIRECTS = {
  # 2026 Wix blog posts -> the same posts on the new site
  "post/new-flat-roof-lift-replacement-underway-on-treasure-island-florida": B + "treasure-island-flat-roof-replacement/",
  "post/new-roof-installation-in-st-petersburg-florida-why-replacing-rotten-roof-decking-matters": B + "st-petersburg-new-roof-rotten-decking/",
  "post/why-you-should-repair-your-roof-sooner-rather-than-later": B + "florida-roof-maintenance-saves-money/",
  "blog-1": "blog.html",
  "get-estimate": "estimate.html",
  # 2024 SEO articles -> closest new post
  "7-best-roof-shingles-for-extreme-weather-conditions": B + "atlas-pinnacle-shingles-algae-protection/",
  "7-reasons-to-choose-quality-residential-roofing-services": B + "florida-roof-maintenance-saves-money/",
  "7-reasons-to-hire-quality-roofing-services-for-your-home": B + "florida-roof-maintenance-saves-money/",
  "7-signs-your-shingle-roof-leak-repair-needs-attention": B + "el-nino-rain-roof-leaks/",
  "addressing-7-common-issues-with-low-slope-flat-roofs": B + "treasure-island-flat-roof-replacement/",
  "choosing-the-right-roof-tiles-repair-services-for-your-home": B + "clay-vs-concrete-roof-tile-florida/",
  "expert-shingle-roofing-repair-services-for-durable-protection": "roofing.html#shingle",
  "high-quality-results-with-affordable-roofing-services": "roofing.html",
  "reliable-roofing-solutions-for-all-types-of-roofs": "roofing.html",
  "roof-repair-specialist-your-key-to-saving-money": B + "florida-roof-maintenance-saves-money/",
  "secure-your-business-with-expert-industrial-roofing-services": "roofing.html#flat",
  "top-benefits-of-commercial-tile-roofing-for-your-business": B + "clay-vs-concrete-roof-tile-florida/",
  "top-rated-roof-installation-services-for-every-home": "roofing.html",
  "top-signs-you-need-emergency-roof-repair-service-right-now": B + "hurricane-roof-prep-and-storm-damage-recovery/",
  "why-you-need-professional-roof-services-for-your-property": B + "florida-roof-maintenance-saves-money/",
  "your-guide-to-7-essential-roof-services-for-homeowners": B + "florida-roof-maintenance-saves-money/",
  "roofing-problems-and-solutions": "roofing.html#repairs",
  "author/admin": "blog.html",
  # 2016 / 2022 service pages
  "residential": "roofing.html", "commercial": "roofing.html#flat",
  "shingles": "roofing.html#shingle", "3-tab-shingles": "roofing.html#shingle", "dimensional-shingle": "roofing.html#shingle",
  "tile": "roofing.html#tile", "tile-1": "roofing.html#tile",
  "tpo": "roofing.html#flat", "flat-low-slope": "roofing.html#flat", "flatlow-slope": "roofing.html#flat", "flatlow-slope-1": "roofing.html#flat",
  "shingletile-repairs": "roofing.html#repairs",
  "residential-and-commercial-re-roofing": "roofing.html", "residential-n-commercial-re-roofing": "roofing.html",
  "residential-and-commercial-roof-repairs": "roofing.html#repairs", "residential-n-commercial-roof-repairs": "roofing.html#repairs",
  "roofing-category/Residential-and-Commercial-Re-roofing": "roofing.html",
  "roofing-category/Residential-and-Commercial-Roof-Repairs": "roofing.html#repairs",
  "before-after": "gallery.html", "before-and-after": "gallery.html", "before-n-after": "gallery.html", "gallery-2": "gallery.html",
  "contact-us": "estimate.html", "financing": "estimate.html", "special-offers": "estimate.html", "specialoffer": "estimate.html",
  "q-a": "estimate.html", "q-n-a": "estimate.html", "QA": "estimate.html",
  "meet-the-owners": "", "review": "", "testimonial": "", "testimonials": "",
}
CATEGORY_TAG_SLUGS = [
  "affordable-roof-installation-service", "affordable-roofing-services", "best-roof-shingles", "best-roofing-shingles",
  "commercial-tile-roof-repair", "emergency-roof-repair-service", "emergency-roofing-services", "emergency-roofing-solutions",
  "flat-low-slope-roofing", "flat-low-sloped-roofing", "industrial-roofing-services", "leaky-roof-repairs", "low-slope-flat-roof",
  "premium-roof-services", "quality-roofing-solutions", "residential-roof-services", "residential-roofing-services",
  "roof-leak-repairs", "roof-repair-specialist", "roof-service-repair", "roof-services", "roof-tiles-installation-service",
  "roof-tiles-repair-services", "roofing-solutions", "shingle-roof-leak-repair", "shingle-roof-repair",
  "shingle-roof-repair-coatings", "shingle-roofing-repair", "uncategorized",
]
for kind in ("category", "tag"):
    for s in CATEGORY_TAG_SLUGS:
        REDIRECTS[f"{kind}/{s}"] = "blog.html"
