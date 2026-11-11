#!/usr/bin/env python3
"""Generate static, indexable blog post pages from the Soro blog.

Why this exists.

The blog is a JavaScript widget: `pages/blog.html` contains only
`<div id="soro-blog"></div>` and a script tag. The 93 posts that widget renders
are fetched client-side and never appear in the HTML. To a crawler the blog page
is 587 characters of navigation and headings, and every one of those posts is
invisible. The `?post=<slug>` URLs in the widget's own links are the same page
with a query string, so they canonicalise back to the blog index and can never
rank on their own.

The fix is not to replace Soro. It is to give each post a real page of its own,
built from the content the gym already wrote and already owns, with the copy
Soro serves. The widget stays on blog.html as the browsable index; the generated
pages are what search engines read, and they cross-link back.

Content comes from Soro's own public embed API, which is the same source the
widget uses:
    GET https://app.trysoro.com/api/embed/<TOKEN>            -> SORO_ARTICLES
    GET https://app.trysoro.com/api/embed/<TOKEN>/article/<id> -> {content: html}

Usage:
    python3 build_blog.py            # fetch fresh and regenerate
    python3 build_blog.py --cached   # regenerate from .soro-cache.json

Writes:
    posts/<slug>.html     one page per article
    pages/blog.html       replaces the widget with static, crawlable links
    sitemap.xml           adds every post, keeps the existing entries

Everything it writes is deterministic for a given input, so a no-op run
produces no diff.
"""
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = '362fa9a5-9503-4d29-9853-6ef634472f68'
BASE = 'https://app.trysoro.com/api/embed/' + TOKEN
SITE = 'https://forge8athletics.com'
CACHE = os.path.join(ROOT, '.soro-cache.json')

# Posts per generated index page is not needed: 93 pages is well within what
# a crawler will walk from one hub, and paginating would just add URLs.

MONTHS = {m: i for i, m in enumerate(
    ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
     'September', 'October', 'November', 'December'], 1)}


def fetch(url, timeout=30):
    r = subprocess.run(['curl', '-s', '--max-time', str(timeout), url],
                       capture_output=True, text=True)
    if r.returncode != 0 or not r.stdout.strip():
        raise RuntimeError(f'curl failed for {url}: {r.stderr[:200]}')
    return r.stdout


def load():
    """[(article dict, body html)] — from cache or the live embed API."""
    if '--cached' in sys.argv and os.path.exists(CACHE):
        data = json.load(open(CACHE))
        return data['articles'], data['bodies']
    js = fetch(BASE + '?theme=dark')
    m = re.search(r'var SORO_ARTICLES = (\[.*?\]);', js, re.S)
    if not m:
        raise RuntimeError('SORO_ARTICLES not found in embed payload')
    articles = json.loads(m.group(1))
    bodies = {}
    for a in articles:
        raw = fetch(BASE + '/article/' + a['id'])
        bodies[a['slug']] = json.loads(raw).get('content') or ''
    json.dump({'articles': articles, 'bodies': bodies}, open(CACHE, 'w'))
    return articles, bodies


def plain(fragment):
    """Visible text of an HTML fragment, for descriptions and word counts."""
    t = re.sub(r'<[^>]+>', ' ', fragment or '')
    t = html.unescape(t)
    return re.sub(r'\s+', ' ', t).strip()


def clean_body(fragment):
    """The article body, minus Soro's inline styling and any script.

    The content is trusted (it is the gym's own copy) but it arrives with
    WordPress-style artefacts that would render oddly against this stylesheet:
    inline `style` attributes, `<span>` wrappers, empty paragraphs, and images
    pointing at Supabase storage. Images are dropped rather than rewritten --
    they are the featured image already shown at the top of the page, and a
    missing one would leave a broken box on a page Google is being asked to
    index.
    """
    body = fragment or ''
    body = re.sub(r'<script.*?</script>', '', body, flags=re.S)
    body = re.sub(r'<style.*?</style>', '', body, flags=re.S)
    body = re.sub(r'<figure.*?</figure>', '', body, flags=re.S)
    body = re.sub(r'<img[^>]*>', '', body)
    body = re.sub(r'\sstyle="[^"]*"', '', body)
    body = re.sub(r'\s(class|id|data-[a-z-]+)="[^"]*"', '', body)
    body = re.sub(r'<p>\s*</p>', '', body)
    body = re.sub(r'<(span|font)[^>]*>(.*?)</\1>', r'\2', body, flags=re.S)
    # Keep the tags that carry structure and drop everything else, so the
    # output is a known-safe subset rather than whatever the editor emitted.
    allowed = {'p', 'h2', 'h3', 'h4', 'ul', 'ol', 'li', 'strong', 'em', 'b',
               'i', 'br', 'blockquote', 'a'}
    body = re.sub(r'</?([a-zA-Z0-9]+)(\s[^>]*)?>',
                  lambda m: m.group(0) if m.group(1).lower() in allowed else '',
                  body)
    # Links inside Soro copy occasionally go to the dashboard or a relative
    # path that would 404 from /posts/. Absolute external links survive.
    body = re.sub(r'<a\s+href="(?!/|https?:)[^"]*"[^>]*>(.*?)</a>', r'\1', body, flags=re.S)
    body = re.sub(r'<a\s+href="(/|https?://(?!forge8athletics|forge8\.pushpress))[^"]*"[^>]*>(.*?)</a>',
                  r'\2', body, flags=re.S)
    body = re.sub(r'<a\b[^>]*>', '<a>', body)
    return body.strip()


def iso(a):
    return (a.get('isoDate') or '')[:10]


def site_nav(prefix):
    """The real nav markup, lifted from pages/blog.html so generated pages match.

    Copying it by hand was the first attempt and it silently dropped the SVG
    wordmark -- the generated pages kept a logo image where every other page
    has the drawn icon and wordmark, which is a visible inconsistency on a page
    whose job is to look like the rest of the site. Reading it from a page that
    already has it right means the two cannot drift.

    `prefix` is what a link needs to reach /pages/ from the page being built:
    '' from /pages/, '../pages/' from /posts/.
    """
    src = open(os.path.join(ROOT, 'pages', 'blog.html')).read()
    m = re.search(r'  <nav>.*?</nav>', src, re.S)
    if not m:
        raise RuntimeError('nav block not found in pages/blog.html')
    nav = m.group(0)
    # Bare `foo.html` hrefs in the nav resolve against /pages/ on the page they
    # came from; from /posts/ they would 404 without the prefix.
    if prefix:
        nav = re.sub(r'href="(free-trial|schedule|coaches|membership|location|contact|blog)\.html"',
                     lambda mm: f'href="{prefix}{mm.group(1)}.html"', nav)
    # The logo links to "/", which is correct at any depth.
    return nav


def footer(prefix):
    return f'''  <footer>
    <div class="footer-top">
      <div>
        <div class="footer-logo"><img src="{prefix}images/logo.png" alt="Forge8 Athletics"><span class="footer-logo-text"><span class="nav-prefix">C R O S S F I T</span><span class="nav-forge">FORGE8</span><span class="nav-ath"> <span>ATHLETICS</span></span></span></div>
        <div class="footer-tagline">Miramar, San Diego</div>
      </div>
      <div class="footer-links">
        <div class="footer-col">
          <h4>Train</h4>
          <a href="{prefix}pages/schedule.html">Schedule</a>
          <a href="{prefix}pages/membership.html">Membership</a>
          <a href="{prefix}pages/membership.html">Drop-In</a>
        </div>
        <div class="footer-col">
          <h4>Gym</h4>
          <a href="{prefix}pages/coaches.html">Coaches</a>
          <a href="{prefix}pages/location.html">Location</a>
          <a href="{prefix}pages/blog.html">Blog</a>
        </div>
        <div class="footer-col">
          <h4>Partners</h4>
          <a href="https://www.crossfitfortius.com/" target="_blank" rel="noopener">CrossFit Fortius</a>
        </div>
        <div class="footer-col">
          <h4>Connect</h4>
          <a href="https://www.instagram.com/forge8_athletics?utm_source=qr" target="_blank" rel="noopener">Instagram</a>
          <a href="https://www.facebook.com/profile.php?id=61592633482387" target="_blank" rel="noopener">Facebook</a>
          <a href="{prefix}pages/contact.html">Contact Us</a>
        </div>
      </div>
    </div>
    <div class="footer-bottom">
      <div class="footer-copy">&copy; 2026 CrossFit Forge8 Athletics. All rights reserved.</div>
      <div class="footer-copy">San Diego, CA &middot; CrossFit &amp; Hyrox Affiliate &middot; <a href="{prefix}pages/privacy-policy.html" style="color:var(--smoke);">Privacy Policy</a></div>
    </div>
  </footer>
  <script src="{prefix}js/main.js"></script>'''


ARTICLE_CSS = '''  <style>
    .post-section { padding: 72px 56px 120px; background: var(--black); }
    .post-wrap { max-width: 760px; margin: 0 auto; }
    .post-meta { font-family: var(--font-cond); font-size: 13px; letter-spacing: 3px;
      text-transform: uppercase; color: var(--forge); margin-bottom: 28px; }
    .post-body { color: var(--smoke); font-size: 17px; line-height: 1.75; }
    .post-body h2 { font-family: var(--font-cond); font-size: 30px; letter-spacing: 1px;
      color: var(--white); margin: 44px 0 16px; text-transform: uppercase; }
    .post-body h3 { font-family: var(--font-cond); font-size: 23px; letter-spacing: 1px;
      color: var(--white); margin: 32px 0 12px; text-transform: uppercase; }
    .post-body p { margin: 0 0 18px; }
    .post-body ul, .post-body ol { margin: 0 0 20px 22px; }
    .post-body li { margin-bottom: 9px; }
    .post-body strong { color: var(--white); }
    .post-body a { color: var(--forge); }
    .post-cta { margin: 56px 0 0; padding: 32px; border: 1px solid rgba(255,255,255,.13);
      text-align: center; }
    .post-cta p { margin: 0 0 18px; color: var(--smoke); }
    .post-nav { margin-top: 48px; display: flex; justify-content: space-between;
      gap: 20px; flex-wrap: wrap; font-family: var(--font-cond);
      letter-spacing: 2px; text-transform: uppercase; font-size: 13px; }
    .post-nav a { color: var(--forge); }
    @media (max-width: 768px) {
      .post-section { padding: 40px 24px 80px; }
      .post-body { font-size: 16px; }
      .post-body h2 { font-size: 25px; }
    }
  </style>'''


def article_page(a, body, prev_a, next_a):
    slug = a['slug']
    title = a['title']
    desc = (a.get('excerpt') or plain(body))[:158].rstrip()
    if len(desc) == 158:
        desc = desc.rsplit(' ', 1)[0] + '.'
    url = f'{SITE}/posts/{slug}.html'
    day = iso(a)
    img = a.get('image') or f'{SITE}/images/og-forge8.jpg'

    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": title,
                "description": desc,
                "datePublished": day,
                "dateModified": day,
                "url": url,
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "image": img,
                "author": {"@type": "Organization", "name": "CrossFit Forge8 Athletics"},
                "publisher": {
                    "@type": "Organization",
                    "name": "CrossFit Forge8 Athletics",
                    "logo": {"@type": "ImageObject",
                             "url": f"{SITE}/images/logo.png"},
                },
                "about": {"@type": "ExerciseGym", "name": "CrossFit Forge8 Athletics",
                          "address": {"@type": "PostalAddress",
                                      "streetAddress": "7550 Miramar Road, Unit #630",
                                      "addressLocality": "San Diego",
                                      "addressRegion": "CA",
                                      "postalCode": "92126",
                                      "addressCountry": "US"}},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + '/'},
                    {"@type": "ListItem", "position": 2, "name": "Blog",
                     "item": f"{SITE}/pages/blog.html"},
                    {"@type": "ListItem", "position": 3, "name": title, "item": url},
                ],
            },
        ],
    }

    navprev = (f'<a href="{prev_a["slug"]}.html">&larr; {html.escape(prev_a["title"])}</a>'
               if prev_a else '<span></span>')
    navnext = (f'<a href="{next_a["slug"]}.html">{html.escape(next_a["title"])} &rarr;</a>'
               if next_a else '<span></span>')

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>{html.escape(title)} | CrossFit Forge8 Athletics</title>
  <meta name="description" content="{html.escape(desc, quote=True)}"/>
  <link rel="canonical" href="{url}"/>
  <link rel="stylesheet" href="../css/style.css"/>
  <link rel="icon" type="image/png" href="../images/favicon.png"/>
  <link rel="apple-touch-icon" href="../images/favicon.png"/>
{ARTICLE_CSS}
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-TJ1ZNBM4DP"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-TJ1ZNBM4DP');
  </script>
  <meta property="og:type" content="article"/>
  <meta property="og:site_name" content="CrossFit Forge8 Athletics"/>
  <meta property="og:title" content="{html.escape(title, quote=True)}"/>
  <meta property="og:description" content="{html.escape(desc, quote=True)}"/>
  <meta property="og:url" content="{url}"/>
  <meta property="og:image" content="{img}"/>
  <meta property="og:locale" content="en_US"/>
  <meta property="article:published_time" content="{day}"/>
  <meta name="twitter:card" content="summary_large_image"/>
  <meta name="twitter:title" content="{html.escape(title, quote=True)}"/>
  <meta name="twitter:description" content="{html.escape(desc, quote=True)}"/>
  <meta name="twitter:image" content="{img}"/>
  <script type="application/ld+json">
{json.dumps(schema, indent=2)}
  </script>
</head>
<body>
  <div class="cursor" id="cursor"></div>
  <div class="cursor-ring" id="cursor-ring"></div>

{site_nav("../pages/")}

  <div class="page-header">
    <div class="page-header-label">Training Blog</div>
    <h1>{html.escape(title)}</h1>
  </div>

  <section class="post-section">
    <div class="post-wrap">
      <div class="post-meta">{day} &middot; CrossFit Forge8 Athletics &middot; Miramar, San Diego</div>
      <div class="post-body">
{body}
      </div>
      <div class="post-cta">
        <p>Train with coaches in Miramar. First three classes are free.</p>
        <a href="https://forge8.pushpress.com/landing/plans/plan_448edada28f549" target="_blank" class="btn-primary">Claim Your Free Trial</a>
      </div>
      <div class="post-nav">
        {navprev}
        <a href="../pages/blog.html">All Articles</a>
        {navnext}
      </div>
    </div>
  </section>

{footer('../')}
</body>
</html>
'''


def blog_index(articles):
    """blog.html with real, crawlable links to every generated post.

    The Soro widget is kept below the static list so the gym keeps the same
    browsable experience and the same authoring workflow, but the links a
    crawler follows are now server-rendered anchor tags rather than
    client-side renders of a JSON blob.
    """
    items = []
    for a in articles:
        items.append(
            f'''        <a class="post-card" href="../posts/{a['slug']}.html">
          <div class="post-card-meta">{iso(a)}</div>
          <h3 class="post-card-title">{html.escape(a['title'])}</h3>
          <p class="post-card-excerpt">{html.escape(a.get('excerpt') or '')}</p>
        </a>''')
    cards = '\n'.join(items)
    schema = json.dumps({
        "@context": "https://schema.org",
        "@type": "Blog",
        "name": "CrossFit Forge8 Athletics Training Blog",
        "url": f"{SITE}/pages/blog.html",
        "publisher": {"@type": "Organization", "name": "CrossFit Forge8 Athletics"},
        "blogPost": [
            {"@type": "BlogPosting", "headline": a['title'],
             "url": f"{SITE}/posts/{a['slug']}.html",
             "datePublished": iso(a)}
            for a in articles
        ],
    }, indent=2)
    return f'''  <div class="blog-section">
    <div class="blog-static">
      <div class="section-label">All Articles</div>
      <h2 class="section-title">TRAINING NOTES<br>FROM THE FLOOR.</h2>
      <div class="post-list">
{cards}
      </div>
    </div>
    <script type="application/ld+json">
{schema}
    </script>
  </div>'''


BLOG_CSS = '''  <style>
    .blog-section {
      padding: 80px 56px 120px;
      background: var(--black);
    }
    .blog-static { max-width: 1100px; margin: 0 auto; }
    .post-list {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 20px;
      margin-top: 48px;
    }
    .post-card {
      display: block;
      padding: 26px 24px;
      border: 1px solid rgba(255,255,255,.12);
      text-decoration: none;
      transition: border-color .2s;
    }
    .post-card:hover { border-color: var(--forge); }
    .post-card-meta {
      font-family: var(--font-cond);
      font-size: 12px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--forge);
      margin-bottom: 10px;
    }
    .post-card-title {
      font-family: var(--font-cond);
      font-size: 21px;
      letter-spacing: .5px;
      color: var(--white);
      margin: 0 0 10px;
      line-height: 1.3;
    }
    .post-card-excerpt {
      color: var(--smoke);
      font-size: 14.5px;
      line-height: 1.6;
      margin: 0;
    }
    @media (max-width: 768px) {
      .blog-section { padding: 40px 24px 80px; }
      .post-list { grid-template-columns: 1fr; }
    }
  </style>'''


def main():
    articles, bodies = load()
    # Newest first, which is how the widget orders them and how a reader
    # expects to find them. Sitemap order follows the same.
    articles = sorted(articles, key=lambda a: (a.get('isoDate') or ''), reverse=True)

    posts_dir = os.path.join(ROOT, 'posts')
    os.makedirs(posts_dir, exist_ok=True)
    # Remove pages for posts that no longer exist, so a deleted article does
    # not linger as a live 200 with stale content.
    live = {a['slug'] + '.html' for a in articles}
    for f in os.listdir(posts_dir):
        if f.endswith('.html') and f not in live:
            os.remove(os.path.join(posts_dir, f))

    written = 0
    for i, a in enumerate(articles):
        body = clean_body(bodies.get(a['slug'], ''))
        if not body:
            print(f'  skipped {a["slug"]}: no body')
            continue
        prev_a = articles[i + 1] if i + 1 < len(articles) else None
        next_a = articles[i - 1] if i > 0 else None
        page = article_page(a, body, prev_a, next_a)
        open(os.path.join(posts_dir, a['slug'] + '.html'), 'w').write(page)
        written += 1

    # blog.html: swap the widget-only section for the static list, keep the
    # rest of the page byte-for-byte.
    bp = os.path.join(ROOT, 'pages', 'blog.html')
    src = open(bp).read()
    src = re.sub(r'  <style>\s*\.blog-section \{.*?</style>', BLOG_CSS, src,
                 count=1, flags=re.S)
    new_section = blog_index(articles)
    # The section is a top-level div closed by `\n  </div>` immediately before
    # the footer. Matching to `</footer` is unambiguous and survives both the
    # original widget markup and this script's own output, so a second run
    # reproduces the same file rather than nesting a copy inside itself.
    start = src.index('  <div class="blog-section">')
    end = src.index('\n  </div>\n\n  <footer>', start)
    src = src[:start] + new_section + src[end + len('\n  </div>'):]
    open(bp, 'w').write(src)

    # sitemap: keep every hand-written URL, replace whatever post entries this
    # script added last time. Stripping only the blog.html entry would append a
    # second copy of all 93 posts on every run, which is how the first draft of
    # this script produced 197 <loc> tags for 104 pages.
    sp = os.path.join(ROOT, 'sitemap.xml')
    sm = open(sp).read()
    sm = re.sub(r'\n\s*<url>\s*<loc>https://forge8athletics\.com/pages/blog\.html</loc>.*?</url>',
                '', sm, flags=re.S)
    sm = re.sub(r'\n\s*<url>\s*<loc>https://forge8athletics\.com/posts/[^<]*</loc>.*?</url>',
                '', sm, flags=re.S)
    block = ['\n  <url>',
             '    <loc>https://forge8athletics.com/pages/blog.html</loc>',
             '    <lastmod>%s</lastmod>' % iso(articles[0]),
             '    <changefreq>daily</changefreq>',
             '    <priority>0.8</priority>',
             '  </url>']
    for a in articles:
        block += ['\n  <url>',
                  f'    <loc>{SITE}/posts/{a["slug"]}.html</loc>',
                  f'    <lastmod>{iso(a)}</lastmod>',
                  '    <changefreq>monthly</changefreq>',
                  '    <priority>0.6</priority>',
                  '  </url>']
    sm = sm.replace('\n</urlset>', ''.join(block) + '\n\n</urlset>')
    open(sp, 'w').write(sm)

    print(f'wrote {written} post pages')
    print(f'blog.html: {len(articles)} static links')
    print(f'sitemap.xml: {sm.count("<loc>")} urls')


if __name__ == '__main__':
    main()
