# Blog build step. Executed by gen.py after core pages are written and before seo_post.py.
# - Publishes posts whose date <= today (America/New_York); future posts stay out of the site entirely.
# - Writes /blog/<slug>.html, /blog.html (index), /rss.xml, appends to sitemap.xml,
#   and injects a "Planning guides" section into each money page that published posts link to.
# Override the date with env BUILD_DATE=YYYY-MM-DD for testing.
import os, re, json, html as _html, datetime, importlib.util as _iu
try:
    from zoneinfo import ZoneInfo
    _today = datetime.datetime.now(ZoneInfo('America/New_York')).date()
except Exception:
    _today = datetime.date.today()
TODAY_D = datetime.date.fromisoformat(os.environ['BUILD_DATE']) if os.environ.get('BUILD_DATE') else _today
import markdown as _md

_s = _iu.spec_from_file_location('posts_src', os.path.join(D, 'posts_src.py')); _pm = _iu.module_from_spec(_s); _s.loader.exec_module(_pm)
ALL_POSTS = sorted(_pm.POSTS, key=lambda p: p['date'])
LIVE = [p for p in ALL_POSTS if datetime.date.fromisoformat(p['date']) <= TODAY_D]
BYSLUG = {p['slug']: p for p in ALL_POSTS}
OUTD = os.path.join(D, 'out')

def _abs(t):
    """Make every internal reference root-absolute so pages work inside /blog/."""
    t = re.sub(r'(src|href)="(images|fonts)/', r'\1="/\2/', t)
    t = t.replace('url(images/', 'url(/images/').replace('url(fonts/', 'url(/fonts/')
    t = re.sub(r'(https://upliftavtech\.com/)index\.html', r'\1', t)
    t = re.sub(r'(https://upliftavtech\.com/[a-z0-9/-]+)\.html', r'\1', t)
    t = re.sub(r'href="index\.html(#[^"]*)?"', lambda m: 'href="/' + (m.group(1) or '') + '"', t)
    t = re.sub(r'href="([a-z0-9/-]+)\.html(#[^"]*)?"', lambda m: 'href="/' + m.group(1) + (m.group(2) or '') + '"', t)
    return t

def _fmt(d):
    d = datetime.date.fromisoformat(d); return d.strftime('%B ') + str(d.day) + d.strftime(', %Y')

def _words(md_text):
    return len(re.findall(r'\w+', md_text))

def _md2html(md_text):
    h = _md.markdown(md_text, extensions=['tables', 'sane_lists'])
    # anchor ids on H2s for the jump list
    def _id(m):
        txt = re.sub('<[^>]+>', '', m.group(1)); slug = re.sub(r'[^a-z0-9]+', '-', txt.lower()).strip('-')[:60]
        return f'<h2 id="{slug}">{m.group(1)}</h2>'
    h = re.sub(r'<h2>(.*?)</h2>', _id, h)
    h = h.replace('<table>', '<div class="ptbl" tabindex="0" role="region" aria-label="Table"><table>').replace('</table>', '</table></div>')
    return h

def _faq_pairs(md_text):
    """Question H2s + first paragraph under each, for FAQ-style structured data and on-page summary."""
    pairs = []
    for m in re.finditer(r'^## (.+?\?)\s*\n\n(.+?)(?:\n\n|\Z)', md_text, re.S | re.M):
        a = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', m.group(2)).replace('**', '')
        if a.startswith(('|', '-', '1.')): continue
        pairs.append((m.group(1), ' '.join(a.split())))
    return pairs

def _post_url(p): return DOMAIN + '/' + p['slug']

def _card(p):
    return (f'<a class="tile post-card" href="/{p["slug"]}"><span class="eyebrow">{_fmt(p["date"])}</span>'
            f'<h3>{p["h1"]}</h3><p>{_html.escape(p["desc"])}</p><span class="more arrow">Read the guide </span></a>')

def post_page(p):
    body_html = _md2html(p['body'])
    answer_html = _md.markdown(p['answer'])
    toc = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', body_html))
    mins = max(3, round((_words(p['body']) + _words(p['answer'])) / 220))
    rel = [BYSLUG[r] for r in p['related'] if r in BYSLUG and BYSLUG[r] in LIVE]
    rel_html = ''.join(_card(r) for r in rel)
    i = LIVE.index(p)
    prev_p = LIVE[i - 1] if i > 0 else None
    next_p = LIVE[i + 1] if i + 1 < len(LIVE) else None
    nav = ''
    if prev_p or next_p:
        nav = '<nav class="post-nav" aria-label="More guides">' + \
              (f'<a href="/{prev_p["slug"]}"><span>Previous guide</span>{prev_p["h1"]}</a>' if prev_p else '<span></span>') + \
              (f'<a href="/{next_p["slug"]}" style="text-align:right"><span>Next guide</span>{next_p["h1"]}</a>' if next_p else '') + '</nav>'
    body = f"""
<article itemscope itemtype="https://schema.org/BlogPosting">
<section class="stage page-hero post-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(/images/{p['img']})"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog">Planning guides</a> / {p['h1']}</nav>
  <span class="eyebrow">Planning guide · {p['audience']}</span>
  <h1 id="h1" itemprop="headline">{p['h1']}</h1>
  <p class="post-meta">By the Uplift AV production team · Published <time datetime="{p['date']}" itemprop="datePublished">{_fmt(p['date'])}</time> · {mins} min read</p>
</div></section>
<section aria-label="Guide"><div class="wrap prose">
  <div class="answer" role="note" aria-label="Short answer"><span class="eyebrow">Short answer</span>{answer_html}</div>
  <nav class="toc-box" aria-label="In this guide"><strong>In this guide</strong><ol>{toc}</ol></nav>
  <div itemprop="articleBody">{body_html}</div>
  <h2 id="bottom-line">Bottom line</h2>
  <p>{p['bottom']}</p>
  <p class="post-cta"><a class="btn btn-gold arrow" href="/{p['money'][0].replace('.html','')}">{p['money'][1]}</a> <a class="btn btn-dark" href="/contact">Ask us about your event</a></p>
  <p class="post-updated">Last reviewed {_fmt(p.get('updated', p['date']))}. Prices and venue details change; your written quote is final.</p>
  {nav}
</div></section>
</article>
{f'<section style="background:var(--paper-2)" aria-labelledby="relg"><div class="wrap"><div class="section-head"><span class="eyebrow">Keep reading</span><h2 id="relg">Related planning guides</h2></div><div class="bento" style="grid-template-columns:repeat(2,minmax(0,1fr))">{rel_html}</div></div></section>' if rel_html else ''}
{cta()}
"""
    url = _post_url(p)
    ld = [{
        "@context": "https://schema.org", "@type": "BlogPosting", "@id": url + "#article",
        "headline": p['h1'], "description": p['desc'], "url": url, "mainEntityOfPage": url,
        "datePublished": p['date'], "dateModified": p.get('updated', p['date']),
        "inLanguage": "en-US", "wordCount": _words(p['body']) + _words(p['answer']),
        "image": DOMAIN + '/images/' + p['img'],
        "articleSection": "Planning guides", "audience": {"@type": "Audience", "audienceType": p['audience']},
        "author": {"@type": "Organization", "name": "Uplift AV production team", "url": DOMAIN + "/about"},
        "publisher": {"@id": DOMAIN + "/#business"},
        "about": [{"@type": "Thing", "name": n} for n in ("Event livestreaming", "Event audio visual production")],
        "isPartOf": {"@type": "Blog", "@id": DOMAIN + "/blog#blog", "name": "Uplift AV Planning Guides"},
        "spatialCoverage": {"@type": "Place", "name": "Myrtle Beach and the Grand Strand, SC"},
      },
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
        {"@type": "ListItem", "position": 2, "name": "Planning guides", "item": DOMAIN + "/blog"},
        {"@type": "ListItem", "position": 3, "name": p['h1'], "item": url}]},
    ]
    qa = _faq_pairs(p['body'])
    if qa:
        ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": p['h1'], "acceptedAnswer": {"@type": "Answer", "text": re.sub(r'\*\*', '', p['answer'])}}] +
            [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qa]})
    t = page(p['slug'] + '.html', p['title'], p['desc'], body, ld)
    t = t.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">\n<meta property="article:published_time" content="' + p['date'] + '">', 1)
    t = t.replace('<link rel="preload" href="fonts/', f'<link rel="preload" as="image" href="/images/{p["img"]}" fetchpriority="high">\n<link rel="preload" href="fonts/', 1)
    return _abs(t)

def blog_index():
    cards = ''.join(_card(p) for p in reversed(LIVE))
    up = [p for p in ALL_POSTS if p not in LIVE]
    body = f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(/images/conference.webp)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / Planning guides</nav>
  <span class="eyebrow">Planning guides</span><h1 id="h1">Event AV and livestream planning guides</h1>
  <p class="lede">Straight answers to the questions planners ask us most: costs, venues, timelines, screens and streams. Written for association leaders, event coordinators, festival producers and tournament directors on the Grand Strand.</p>
</div></section>
<section aria-labelledby="latest"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Latest</span><h2 id="latest">Guides for planners</h2>
  <p class="lede">New guides publish weekly.{' Next up: ' + up[0]['h1'] if up else ''}</p></div>
  <div class="bento" style="grid-template-columns:repeat(2,minmax(0,1fr))">{cards}</div>
  <p style="margin-top:28px;text-align:center"><a href="/rss.xml">Subscribe with RSS</a></p>
</div></section>
{cta()}
"""
    ld = [{"@context": "https://schema.org", "@type": "Blog", "@id": DOMAIN + "/blog#blog", "name": "Uplift AV Planning Guides",
           "url": DOMAIN + "/blog", "publisher": {"@id": DOMAIN + "/#business"},
           "blogPost": [{"@type": "BlogPosting", "headline": p['h1'], "url": _post_url(p), "datePublished": p['date']} for p in LIVE]},
          crumbs('Planning guides', 'blog.html')]
    t = page('blog.html', 'Event AV & Livestream Planning Guides | Uplift AV',
             'Answers to the questions event planners ask about livestream costs, venue AV, IMAG, kickoff timelines and festival screens, from a Myrtle Beach production crew.', body, ld)
    t = t.replace('<link rel="preload" href="fonts/', '<link rel="preload" as="image" href="/images/conference.webp" fetchpriority="high">\n<link rel="preload" href="fonts/', 1)
    t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n<link rel="alternate" type="application/rss+xml" title="Uplift AV Planning Guides" href="/rss.xml">', 1)
    return _abs(t)

def rss():
    items = ''.join(f"""  <item><title>{_html.escape(p['h1'])}</title><link>{_post_url(p)}</link><guid>{_post_url(p)}</guid>
    <pubDate>{datetime.datetime.fromisoformat(p['date'] + 'T09:00:00-05:00').strftime('%a, %d %b %Y %H:%M:%S -0500')}</pubDate>
    <description>{_html.escape(p['desc'])}</description></item>\n""" for p in reversed(LIVE))
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0"><channel>
  <title>Uplift AV Planning Guides</title><link>{DOMAIN}/blog</link>
  <description>Event AV and livestream planning guides for the Grand Strand.</description><language>en-us</language>
{items}</channel></rss>
"""

if LIVE:
    os.makedirs(os.path.join(OUTD, 'blog'), exist_ok=True)
    for p in LIVE:
        open(os.path.join(OUTD, p['slug'] + '.html'), 'w').write(post_page(p))
    open(os.path.join(OUTD, 'blog.html'), 'w').write(blog_index())
    open(os.path.join(OUTD, 'rss.xml'), 'w').write(rss())
    # Planning guides on money pages (posts that link to that page as their main CTA)
    by_money = {}
    for p in LIVE: by_money.setdefault(p['money'][0], []).append(p)
    for f, ps in by_money.items():
        fp = os.path.join(OUTD, f)
        if not os.path.exists(fp): continue
        t = open(fp).read()
        if 'aria-labelledby="guides"' in t: continue
        sec = ('<section aria-labelledby="guides"><div class="wrap"><div class="section-head"><span class="eyebrow">Planning guides</span>'
               '<h2 id="guides">Questions planners ask</h2></div><div class="bento" style="grid-template-columns:repeat(2,minmax(0,1fr))">'
               + ''.join(_card(p) for p in reversed(ps)) + '</div></div></section>\n')
        i = t.rfind('<section class="stage cta">')
        if i > 0: open(fp, 'w').write(t[:i] + sec + t[i:])
    # sitemap: add blog index + posts with their own dates
    sm = os.path.join(OUTD, 'sitemap.xml'); s = open(sm).read()
    add = f'  <url><loc>{DOMAIN}/blog</loc><lastmod>{LIVE[-1]["date"]}</lastmod></url>\n' + ''.join(
        f'  <url><loc>{DOMAIN}/{p["slug"]}</loc><lastmod>{p.get("updated", p["date"])}</lastmod></url>\n' for p in LIVE)
    s = s.replace('</urlset>', add + '</urlset>')
    open(sm, 'w').write(s)
print('posts live:', len(LIVE), 'of', len(ALL_POSTS), 'build date', TODAY_D)
