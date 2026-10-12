"""Spangler Roofing: per-post blog pages + site-wide SEO pass.

Sources (read from git tag `pre-seo-blog`, so the build is repeatable):
  blog.html (shell + 5 original posts), index/roofing/gallery/estimate.html
Writes:
  blog.html (index of all posts), blog/<slug>/index.html (one page per post),
  the four root pages with SEO fixes, robots.txt, sitemap.xml, 404.html
"""
import html, json, pathlib, re, subprocess, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from blog_new_posts import NEW_POSTS

ROOT = pathlib.Path(__file__).parent
SITE = "https://spanglerroofingllc.com"
TAG = "pre-seo-blog"
REVIEWS = ("4.7", "115")
MAPS = "https://maps.google.com/?cid=16899887521762870685"

def src(name):
    return subprocess.run(["git", "show", f"{TAG}:{name}"], cwd=ROOT, capture_output=True, text=True, encoding="utf-8", check=True).stdout

# ------------------------------------------------------------------ existing posts
OLD = src("blog.html")
EXISTING = [  # old anchor id -> new slug, ISO date, hero image
    ("roof-maintenance", "florida-roof-maintenance-saves-money", "2026-08-03", "blog_maintenance.jpg"),
    ("hurricane-clips", "hurricane-clips-florida-roofs", "2026-07-28", "blog_hurricane_repair.jpg"),
    ("el-nino-prep", "el-nino-roof-storm-prep-checklist", "2026-07-15", "blog_elnino.jpg"),
    ("treasure-island", "treasure-island-flat-roof-replacement", "2026-06-03", "blog_ti_1.jpg"),
    ("rotten-decking", "st-petersburg-new-roof-rotten-decking", "2026-05-14", "blog_stpete_2.jpg"),
]
RELATED_OLD = {
    "florida-roof-maintenance-saves-money": ["atlas-pinnacle-shingles-algae-protection", "el-nino-rain-roof-leaks"],
    "hurricane-clips-florida-roofs": ["hurricane-roof-prep-and-storm-damage-recovery", "florida-roof-maintenance-saves-money"],
    "el-nino-roof-storm-prep-checklist": ["el-nino-rain-roof-leaks", "hurricane-roof-prep-and-storm-damage-recovery"],
    "treasure-island-flat-roof-replacement": ["st-petersburg-new-roof-rotten-decking", "el-nino-rain-roof-leaks"],
    "st-petersburg-new-roof-rotten-decking": ["treasure-island-flat-roof-replacement", "florida-roof-maintenance-saves-money"],
}
META_OLD = {
    "florida-roof-maintenance-saves-money": "How routine roof maintenance protects Florida homes from leaks, storm damage and early replacement, and how often Tampa Bay roofs should be inspected. Spangler Roofing, St. Petersburg FL.",
    "hurricane-clips-florida-roofs": "What hurricane clips are, why they keep your roof on in high wind, how to add them during a reroof, and how they can lower Florida insurance premiums. Spangler Roofing, St. Petersburg FL.",
    "el-nino-roof-storm-prep-checklist": "A seven-step roof checklist for a strong El Nino season in Florida: inspections, gutters, trees, attic checks, flashing and insurance. Spangler Roofing, St. Petersburg FL.",
    "treasure-island-flat-roof-replacement": "A flat roof lift kit and full plywood decking replacement on a Treasure Island apartment building, and why drainage and decking matter on flat roofs. Spangler Roofing.",
    "st-petersburg-new-roof-rotten-decking": "A St. Petersburg roof replacement where soft, rotted decking was found under the shingles, and why replacing damaged wood before a new roof matters. Spangler Roofing.",
}

toc = dict(re.findall(r'<a class="toc-card" href="#([^"]+)">.*?<p>(.*?)</p>', OLD, re.S))
posts = []
for anchor, slug, iso, hero in EXISTING:
    m = re.search(r'<article class="blog-post" id="%s">(.*?)</article>' % anchor, OLD, re.S)
    art = m.group(1)
    title_html = re.search(r"<h2>(.*?)</h2>", art).group(1)
    hero_m = re.search(r'<img class="bp-hero" src="assets/([^"]+)" alt="([^"]*)"', art)
    body = re.search(r'<div class="bp-body">(.*?)</div>\s*<div class="bp-cta">', art, re.S).group(1)
    cta = re.search(r'<div class="bp-cta">\s*<p>(.*?)</p>\s*<a class="btn btn-primary" href="([^"]+)">(.*?)</a>', art, re.S)
    posts.append(dict(
        slug=slug, date=iso, title=html.unescape(title_html), title_html=title_html,
        meta=META_OLD[slug], excerpt=html.unescape(toc[anchor]),
        hero=hero_m.group(1) if hero_m else hero, hero_alt=hero_m.group(2) if hero_m else html.unescape(title_html),
        hero_in_body=bool(hero_m), body=body, cta_text=cta.group(1), cta_href=cta.group(2), cta_btn=cta.group(3),
        related=RELATED_OLD[slug], old_anchor=anchor))
for p in NEW_POSTS:
    p = dict(p); p["title_html"] = html.escape(p["title"], quote=False).replace("&#x27;", "&rsquo;").replace("'", "&rsquo;")
    p["hero_in_body"] = True; posts.append(p)
posts.sort(key=lambda p: p["date"], reverse=True)
BY = {p["slug"]: p for p in posts}

def nice(iso):
    from datetime import date
    y, m, d = map(int, iso.split("-")); return date(y, m, d).strftime("%B %-d, %Y") if sys.platform != "win32" else date(y, m, d).strftime("%B %#d, %Y")

# ------------------------------------------------------------------ shared head
def head(title, desc, path, image="assets/og-preview.jpg", og_type="website", extra=""):
    url = SITE + "/" + path
    img = SITE + "/" + image
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta name="author" content="Spangler Roofing LLC">
<meta name="theme-color" content="#15294c">
<meta property="og:type" content="{og_type}">
<meta property="og:site_name" content="Spangler Roofing">
<meta property="og:locale" content="en_US">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{img}">
{extra}"""

def esc_attr(s): return html.escape(s, quote=True)

# ------------------------------------------------------------------ root pages SEO pass
def fix_root(name, path):
    s = src(name)
    s = s.replace("<!-- DEMO: remove noindex when site goes live -->\n", "").replace('<meta name="robots" content="noindex">\n', "")
    assert "noindex" not in s, name
    t = re.search(r"<title>(.*?)</title>", s).group(1)
    d = re.search(r'<meta name="description" content="([^"]*)">', s).group(1)
    # drop the old loose head lines we regenerate
    for pat in [r'<meta charset="utf-8">\n', r'<meta name="viewport"[^>]*>\n', r"<title>.*?</title>\n", r'<meta name="description"[^>]*>\n',
                r'<meta name="author"[^>]*>\n', r'<meta name="theme-color"[^>]*>\n', r'<meta property="og:[^>]*>\n', r'<meta name="twitter:[^>]*>\n']:
        s = re.sub(pat, "", s)
    s = s.replace("4.7 · 112 Google reviews", "4.7 · 115 Google reviews").replace('"reviewCount": "112"', '"reviewCount": "115"').replace("112 Google reviews", "115 Google reviews").replace("112 reviews", "115 reviews")
    skip = s.index('<a class="skip-link"')
    s = head(t, d, path) + s[:skip].lstrip() + "</head>\n<body>\n" + s[skip:].rstrip() + "\n</body>\n</html>\n"
    return s

index = fix_root("index.html", "")
# richer LocalBusiness data
index = index.replace('"name": "Spangler Roofing LLC",', '"name": "Spangler Roofing LLC",\n  "@id": "%s/#business",\n  "url": "%s/",\n  "image": "%s/assets/og-preview.jpg",\n  "priceRange": "$$",\n  "hasMap": "%s",\n  "sameAs": ["%s"],\n  "geo": {"@type": "GeoCoordinates", "latitude": 27.8242016, "longitude": -82.7176493},' % (SITE, SITE, SITE, MAPS, MAPS), 1)
index = index.replace('"areaServed": ["St. Petersburg, FL", "Pinellas County, FL", "Tampa Bay, FL"],',
  '"areaServed": ["St. Petersburg, FL", "Pinellas County, FL", "Clearwater, FL", "Largo, FL", "Seminole, FL", "Pinellas Park, FL", "Treasure Island, FL", "St. Pete Beach, FL", "Gulfport, FL", "Dunedin, FL", "Palm Harbor, FL", "Tampa, FL"],')
assert '"@id"' in index and "Gulfport" in index
(ROOT / "index.html").write_text(index, encoding="utf-8")
for name in ["roofing.html", "gallery.html", "estimate.html"]:
    (ROOT / name).write_text(fix_root(name, name), encoding="utf-8")

# ------------------------------------------------------------------ shell for blog pages
shell_top = OLD[OLD.index('<a class="skip-link"'):OLD.index('<main id="main">')]
shell_bot = OLD[OLD.index("</main>"):]
shell_top = shell_top.replace("4.7 · 112 Google reviews", "4.7 · 115 Google reviews")

def prefix_paths(frag, pre):
    """Make root-relative asset/page links work from blog/<slug>/."""
    def fix(m):
        attr, val = m.group(1), m.group(2)
        if re.match(r"^(https?:|mailto:|tel:|#|/|data:)", val): return m.group(0)
        return f'{attr}="{pre}{val}"'
    return re.sub(r'\b(href|src)="([^"]*)"', fix, frag)

POST_CSS = """
/* ---- per-post pages (SEO pass, Oct 2026) ---- */
.post-hero-img{width:100%;height:auto;border-radius:var(--radius-lg);box-shadow:var(--shadow);aspect-ratio:16/9;object-fit:cover;margin:8px 0 24px}
.bp-figure{margin:22px 0}
.bp-figure img{width:100%;height:auto;border-radius:14px;border:1px solid var(--line);aspect-ratio:16/9;object-fit:cover}
.bp-figure figcaption{font-size:.85rem;color:var(--muted);margin-top:8px}
.bp-body a{color:var(--brick);font-weight:700;text-decoration:underline;text-underline-offset:3px}
.bp-body strong,.bp-body em{color:var(--navy)}
.related{max-width:820px;margin:0 auto;padding:10px 0 56px}
.related h2{color:var(--navy);font-size:1.3rem;margin-bottom:14px}
.related-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:16px}
@media(max-width:720px){.related-grid{grid-template-columns:1fr}}
.toc-card .tc-img{width:calc(100% + 44px);max-width:none;height:auto;flex:0 0 auto;margin:-24px -22px 6px;aspect-ratio:16/9;object-fit:cover;border-radius:var(--radius) var(--radius) 0 0}
.toc-card{overflow:hidden}
.blog-toc.three{grid-template-columns:repeat(3,1fr)}
@media(max-width:1000px){.blog-toc.three{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.blog-toc.three{grid-template-columns:1fr}}
"""
css = src("styles.css")
(ROOT / "styles.css").write_text(css.rstrip() + "\n" + POST_CSS, encoding="utf-8")

def card(p, pre=""):
    return (f'<a class="toc-card" href="{pre}blog/{p["slug"]}/">'
            f'<img class="tc-img" src="{pre}assets/{p["hero"]}" alt="{esc_attr(p["hero_alt"])}" loading="lazy" width="1600" height="900">'
            f'<span class="tc-date"><time datetime="{p["date"]}">{nice(p["date"])}</time></span>'
            f'<h3>{p["title_html"]}</h3><p>{html.escape(p["excerpt"], quote=False)}</p>'
            f'<span class="tc-read">Read the post &rarr;</span></a>')

# ------------------------------------------------------------------ post pages
for p in posts:
    pre = "../../"
    path = f'blog/{p["slug"]}/'
    url = SITE + "/" + path
    title = f'{p["title"]} | Spangler Roofing'
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "BlogPosting", "headline": p["title"], "description": p["meta"], "datePublished": p["date"], "dateModified": p["date"],
             "image": f'{SITE}/assets/{p["hero"]}', "url": url, "mainEntityOfPage": url,
             "author": {"@type": "Organization", "name": "Spangler Roofing LLC", "url": SITE + "/"},
             "publisher": {"@type": "Organization", "name": "Spangler Roofing LLC", "url": SITE + "/"}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog.html"},
                {"@type": "ListItem", "position": 3, "name": p["title"], "item": url}]}]}
    extra = (f'<meta property="article:published_time" content="{p["date"]}">\n'
             '<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
             '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Mulish:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
             f'<link rel="stylesheet" href="{pre}styles.css">\n<script type="application/ld+json">\n{json.dumps(ld, indent=1, ensure_ascii=False)}\n</script>\n')
    hero_img = (f'<img class="post-hero-img" src="assets/{p["hero"]}" alt="{esc_attr(p["hero_alt"])}" width="1600" height="900" fetchpriority="high">'
                if p["hero_in_body"] else "")
    body = p["body"]
    rel = "".join(card(BY[s]) for s in p["related"])
    main = f"""<main id="main">
<section class="page-hero">
  <div class="page-hero-media"><img src="assets/{p["hero"]}" alt=""></div>
  <div class="wrap page-hero-inner">
    <div class="reveal in">
      <div class="crumbs"><a href="index.html">Home</a><span>/</span><a href="blog.html">Blog</a></div>
      <h1 style="max-width:24ch">{p["title_html"]}</h1>
      <p><time datetime="{p["date"]}">{nice(p["date"])}</time> &middot; By Spangler Roofing LLC &middot; Serving Florida since 1989</p>
    </div>
  </div>
</section>
<section style="padding-top:8px;padding-bottom:0">
  <div class="wrap">
    <article class="blog-post">
      {hero_img}
      <div class="bp-body">{body}</div>
      <div class="bp-cta">
        <p>{p["cta_text"]}</p>
        <a class="btn btn-primary" href="{p["cta_href"]}">{p["cta_btn"]}</a>
      </div>
      <a class="bp-top" href="blog.html">&larr; All posts</a>
    </article>
    <aside class="related" aria-label="More from the blog">
      <h2>Keep reading</h2>
      <div class="related-grid">{rel}</div>
    </aside>
  </div>
</section>
"""
    page = head(esc_attr(title), esc_attr(p["meta"]), path, image=f'assets/{p["hero"]}', og_type="article", extra=extra)
    page += "</head>\n<body>\n" + prefix_paths(shell_top.replace('class="active"', ""), pre) + prefix_paths(main, pre) + prefix_paths(shell_bot, pre).rstrip() + "\n</body>\n</html>\n"
    out = ROOT / "blog" / p["slug"]; out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(page, encoding="utf-8")

# ------------------------------------------------------------------ blog index
old_head_desc = "Roofing advice and recent project stories from Spangler Roofing in St. Petersburg, FL: Atlas algae-resistant shingles, clay vs. concrete tile, hurricane prep and storm recovery, El Ni&ntilde;o rain and leaks, and more. Call (727) 397-3800."
ld_blog = {"@context": "https://schema.org", "@type": "Blog", "name": "Spangler Roofing Blog", "url": SITE + "/blog.html",
           "publisher": {"@type": "Organization", "name": "Spangler Roofing LLC"},
           "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "datePublished": p["date"], "url": f'{SITE}/blog/{p["slug"]}/'} for p in posts]}
extra = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700;12..96,800&family=Mulish:wght@400;500;600;700;800&display=swap" rel="stylesheet">\n'
         f'<link rel="stylesheet" href="styles.css">\n<script type="application/ld+json">\n{json.dumps(ld_blog, indent=1, ensure_ascii=False)}\n</script>\n')
redirect_map = {p["old_anchor"]: f'blog/{p["slug"]}/' for p in posts if p.get("old_anchor")}
hero_sec = OLD[OLD.index("<!-- ===== Page hero ===== -->"):OLD.index("<!-- ===== Post index ===== -->")]
index_main = f"""<main id="main">
{hero_sec}
<section>
  <div class="wrap">
    <div class="blog-toc three">
      {"".join(card(p) for p in posts)}
    </div>
  </div>
</section>
"""
cta_band = OLD[OLD.index("<!-- ===== CTA band ===== -->"):OLD.index("</main>")]
redirect_js = ("<script>(function(){var m=" + json.dumps(redirect_map) +
               ";var h=location.hash.slice(1);if(m[h])location.replace(m[h]);})();</script>\n")
blog = head("Roofing Blog | Tips, Projects &amp; Storm Prep — Spangler Roofing, St. Petersburg FL", old_head_desc, "blog.html", extra=extra)
blog += "</head>\n<body>\n" + redirect_js + shell_top + index_main + cta_band + shell_bot.rstrip() + "\n</body>\n</html>\n"
(ROOT / "blog.html").write_text(blog, encoding="utf-8")

# ------------------------------------------------------------------ robots, sitemap, 404
(ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
urls = [("", "2026-10-12", "1.0"), ("roofing.html", "2026-10-12", "0.9"), ("gallery.html", "2026-10-12", "0.7"),
        ("estimate.html", "2026-10-12", "0.8"), ("blog.html", posts[0]["date"], "0.7")]
urls += [(f'blog/{p["slug"]}/', p["date"], "0.6") for p in posts]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
sm += "".join(f"  <url><loc>{SITE}/{u}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for u, d, pr in urls)
sm += "</urlset>\n"
(ROOT / "sitemap.xml").write_text(sm, encoding="utf-8")

nf_main = """<main id="main">
<section class="page-hero">
  <div class="page-hero-media"><img src="/assets/blog_stpete_1.jpg" alt=""></div>
  <div class="wrap page-hero-inner"><div class="reveal in">
    <h1>That page has moved.</h1>
    <p>Our website was rebuilt, so some old links point to pages that no longer exist. Everything is still here.</p>
    <div class="hero-cta" style="margin-top:22px">
      <a class="btn btn-primary btn-lg" href="/">Go to the home page</a>
      <a class="btn btn-outline-light btn-lg" href="/blog.html">Read the blog</a>
    </div>
  </div></div>
</section>
"""
nf_js = ("<script>(function(){var p=location.pathname.toLowerCase();"
         "if(/^\\/(blog|post|posts)(\\/|$)/.test(p)){location.replace('/blog.html');return;}"
         "if(/(roof|service|repair|tile|metal|shingle)/.test(p)){location.replace('/roofing.html');return;}"
         "if(/(contact|estimate|quote)/.test(p)){location.replace('/estimate.html');return;}"
         "if(/(gallery|project|work|photo)/.test(p)){location.replace('/gallery.html');return;}})();</script>\n")
nf = head("Page not found | Spangler Roofing", "This page has moved. Visit Spangler Roofing, St. Petersburg's family roofer since 1989.", "404.html",
          extra='<meta name="robots" content="noindex">\n<link rel="stylesheet" href="/styles.css">\n')
nf += "</head>\n<body>\n" + nf_js + prefix_paths(shell_top, "/") + nf_main + prefix_paths(shell_bot, "/").rstrip() + "\n</body>\n</html>\n"
(ROOT / "404.html").write_text(nf, encoding="utf-8")

print(f"{len(posts)} posts:")
for p in posts: print(" ", p["date"], p["slug"])
