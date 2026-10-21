import json, os, html, re
PROMO_END='2027-01-01T00:00:00-05:00'
FORM_KEY='83d41300-159b-4f70-9da2-161ecf736240'
AREA_LIST=['Myrtle Beach','North Myrtle Beach','Conway','Little River','Surfside Beach / Garden City','Murrells Inlet','Pawleys Island / Litchfield','Georgetown','Sunset Beach / Calabash','Ocean Isle Beach']
AREA_OPTS=''.join(f'<option>{a}</option>' for a in AREA_LIST)
ADDON_CHECKS=''.join(f'<label><input type="checkbox" name="addons" value="{a}"> {a}</label>' for a in ['IMAG to venue screens','Extra cameras','Hosted viewing page','Multiple platforms','Sound package','Starlink internet','Photography','Recap film','Social reels'])
def P(promo, after=''):
    return f'<span data-promo>{promo}</span>' + (f'<span data-after>{after}</span>' if after else '')
def ld_text(t):
    t=re.sub(r'<span data-promo>.*?</span>','',t); return re.sub(r'<[^>]+>','',t).strip()
D = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(D, 'site.css')).read()
DOMAIN = 'https://upliftavtech.com'
EMAIL = 'info@upliftavtech.com'
AREA = 'Myrtle Beach & the Grand Strand, SC'
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap">')
JS = """<script>
(function(){
  var b=document.querySelector('.menu-btn'), m=document.getElementById('menu');
  if(b&&m){b.addEventListener('click',function(){var o=m.classList.toggle('open');b.setAttribute('aria-expanded',o);b.textContent=o?'Close':'Menu';});
    m.addEventListener('click',function(e){if(e.target.closest('a')){m.classList.remove('open');b.setAttribute('aria-expanded','false');b.textContent='Menu';}});}
  document.querySelectorAll('[data-copy]').forEach(function(btn){btn.addEventListener('click',function(){
    var t=btn.getAttribute('data-copy'), done=function(){btn.textContent='Copied';setTimeout(function(){btn.textContent='Copy email';},1800);};
    if(navigator.clipboard){navigator.clipboard.writeText(t).then(done,function(){sel(btn)});}else sel(btn);});});
  function sel(btn){var el=document.querySelector('.email');if(!el)return;var r=document.createRange();r.selectNodeContents(el);var s=getSelection();s.removeAllRanges();s.addRange(r);btn.textContent='Press Ctrl/Cmd+C';}
  var f=document.getElementById('quote-form');
  if(f){f.addEventListener('submit',function(e){
    e.preventDefault(); var st=document.getElementById('f-status'), btn=document.getElementById('f-submit');
    if(!f.checkValidity()){var bad=f.querySelector(':invalid'); st.textContent='Please fill in the required fields.'; st.className='fstatus err'; if(bad) bad.focus(); return;}
    if(f.access_key.value.indexOf('PASTE')===0){st.textContent='The form is not connected yet. Please email info@upliftavtech.com.'; st.className='fstatus err'; return;}
    var data=new FormData(f), obj={}; data.forEach(function(v,k){ if(k==='addons'){obj[k]=obj[k]?obj[k]+', '+v:v;} else obj[k]=v; }); delete obj.redirect;
    btn.disabled=true; btn.textContent='Sending...'; st.textContent=''; st.className='fstatus';
    fetch(f.action,{method:'POST',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify(obj)})
      .then(function(r){return r.json();}).then(function(j){
        if(j.success){f.reset(); st.textContent='Thanks. Your request was sent. We will reply by email soon.'; st.className='fstatus ok'; btn.textContent='Sent';}
        else throw new Error(j.message||'error');})
      .catch(function(){st.textContent='Something went wrong. Please try again or email info@upliftavtech.com.'; st.className='fstatus err'; btn.disabled=false; btn.textContent='Send request';});
  });}
})();
</script>"""

ICON = {
 'stream':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="2"/><path d="M16.2 7.8a6 6 0 0 1 0 8.4M7.8 16.2a6 6 0 0 1 0-8.4M19 5a10 10 0 0 1 0 14M5 19A10 10 0 0 1 5 5"/></svg>',
 'cam':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="6" width="14" height="12" rx="2"/><path d="M16 10l6-3v10l-6-3z"/></svg>',
 'slides':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="12" rx="1.5"/><path d="M12 16v4M8 20h8M7 9h6M7 12h10"/></svg>',
 'screen':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="3" width="20" height="13" rx="1.5"/><path d="M7 21h10M12 16v5"/><circle cx="12" cy="9.5" r="2.5"/></svg>',
 'net':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 14a8 8 0 0 1 16 0"/><path d="M12 14l3-4"/><path d="M3 18h18"/></svg>',
 'mic':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="9" y="2" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v4"/></svg>',
 'photo':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 7h3l2-3h6l2 3h3v13H4z"/><circle cx="12" cy="13" r="3.5"/></svg>',
 'users':'<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="9" cy="8" r="3.5"/><path d="M2 20a7 7 0 0 1 14 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M22 20a7 7 0 0 0-4-6.3"/></svg>',
}

import importlib.util as _iu2
_sp2=_iu2.spec_from_file_location('services_data',os.path.join(D,'services_data.py')); _m2=_iu2.module_from_spec(_sp2); _sp2.loader.exec_module(_m2)
SERVICES=_m2.SERVICES; SBY={x['key']:x for x in SERVICES}; SFILE={x['key']:x['file'] for x in SERVICES}
_sp3=_iu2.spec_from_file_location('audiences',os.path.join(D,'audiences.py')); _m3=_iu2.module_from_spec(_sp3); _sp3.loader.exec_module(_m3)
AUDS=_m3.AUDIENCES; ABY={a['key']:a for a in AUDS}
NAV = [('index.html','Home'),('who-we-serve.html','Who we serve'),('services.html','Services'),('packages.html','Packages'),('areas.html','Areas'),('faq.html','FAQ'),('contact.html','Contact')]

ORG = {"@context":"https://schema.org","@type":"ProfessionalService","@id":DOMAIN+"/#business","name":"Uplift AV",
 "description":"Event production and livestreaming on the Grand Strand: multi-camera production, livestreams, IMAG screens, presentation and sponsor graphics, and recap video for association conventions, corporate events, festivals and sports tournaments.",
 "url":DOMAIN+"/","email":EMAIL,"logo":DOMAIN+"/images/uplift-av-logo.png","image":DOMAIN+"/images/og-image.jpg",
 "areaServed":[{"@type":"City","name":"Myrtle Beach, SC"},{"@type":"City","name":"North Myrtle Beach, SC"},{"@type":"City","name":"Conway, SC"},{"@type":"City","name":"Surfside Beach, SC"},{"@type":"Place","name":"Murrells Inlet, SC"},{"@type":"Place","name":"Pawleys Island, SC"},{"@type":"City","name":"Georgetown, SC"},{"@type":"City","name":"Little River, SC"},{"@type":"Town","name":"Sunset Beach, NC"},{"@type":"Town","name":"Calabash, NC"},{"@type":"Town","name":"Ocean Isle Beach, NC"},{"@type":"AdministrativeArea","name":"Horry County, SC"},{"@type":"AdministrativeArea","name":"Georgetown County, SC"},{"@type":"AdministrativeArea","name":"Brunswick County, NC"}],
 "slogan":"Elevated production. Expanded reach.",
 "knowsAbout":["Event production","Conference and convention AV","Corporate event production","Festival and concert IMAG","Tournament livestreaming","Hybrid event production","Multi-camera video production","Town hall streaming"]}

def head(slug, title, desc, extra_ld=None):
    url = DOMAIN + '/' + ('' if slug=='index.html' else slug)
    lds = [ORG] + (extra_ld or [])
    ld = '\n'.join('<script type="application/ld+json">'+json.dumps(x, ensure_ascii=False).replace('</','<\\/')+'</script>' for x in lds)
    return f'''<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="canonical" href="{url}">
<meta name="robots" content="index,follow">
<meta name="theme-color" content="#161B24">
<meta name="apple-mobile-web-app-title" content="Uplift AV">
<meta name="format-detection" content="telephone=no">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Uplift AV">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMAIN}/images/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Uplift AV: Elevated production. Expanded reach. Livestream and event AV in Myrtle Beach and the Grand Strand.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(title)}">
<meta name="twitter:description" content="{html.escape(desc)}">
<meta name="twitter:image" content="{DOMAIN}/images/og-image.jpg">
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/images/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/images/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{FONTS}
{ld}
<script>if(Date.now()>=Date.parse('{PROMO_END}'))document.documentElement.classList.add('promo-over');</script>
<style>{CSS}html:not(.promo-over) [data-after]{{display:none!important}}html.promo-over [data-promo]{{display:none!important}}</style>'''

def top(slug):
    links = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h==slug else ""}>{t}</a></li>' for h,t in NAV if h!='contact.html')
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="strip" data-promo><div class="wrap"><span>Launch pricing: 15% off every package booked before Jan. 1, 2027.</span><a href="packages.html">See packages</a></div></div>
<header class="nav"><div class="wrap">
  <a class="logo" href="index.html" aria-label="Uplift AV home"><img src="images/uplift-av-logo.png" alt="Uplift AV" width="180" height="45"></a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
  <nav aria-label="Main"><ul id="menu">{links}<li><a class="btn btn-gold" href="contact.html"{" aria-current=\"page\"" if slug=="contact.html" else ""}>Get a quote</a></li></ul></nav>
</div></header>'''

FOOT = f'''<footer><div class="wrap">
  <div><a class="logo" href="index.html" aria-label="Uplift AV home"><img src="images/uplift-av-logo.png" alt="Uplift AV" width="180" height="45"></a>
  <p>Event production and livestreaming for conventions, corporate events, festivals and tournaments across {AREA}.</p></div>
  <div><h4>Explore</h4><ul>{''.join(f'<li><a href="{h}">{t}</a></li>' for h,t in NAV)}</ul></div>
  <div><h4>Services</h4><ul>{''.join(f'<li><a href="{x["file"]}">{x["name"]}</a></li>' for x in SERVICES)}</ul></div>
  <div><h4>Areas</h4><ul>{''.join(f'<li><a href="event-av-{c_}.html">{n_}</a></li>' for c_,n_ in [('myrtle-beach','Myrtle Beach'),('north-myrtle-beach','North Myrtle Beach'),('conway','Conway'),('murrells-inlet','Murrells Inlet'),('pawleys-island-litchfield','Pawleys Island'),('georgetown','Georgetown'),('little-river','Little River'),('sunset-beach-calabash','Sunset Beach'),('ocean-isle-beach','Ocean Isle Beach')])}<li><a href="areas.html">All areas</a></li></ul></div>
  <div><h4>Contact</h4><ul><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li>Serving {AREA}</li><li><a href="contact.html">Request a quote</a></li></ul></div>
  <div class="legal"><span>© 2026 Uplift AV. All rights reserved.</span><span>Event production · Livestreaming · IMAG · Recap video</span></div>
</div></footer>'''

def cta(h="Let's talk about your event.", p="Tell us what you're planning. We'll send a clear quote."):
    return f'''<section class="stage cta"><div class="stage-img" style="background-image:url(images/beams.jpg)"></div><div class="wrap">
  <div style="display:flex;flex-direction:column;gap:14px"><h2>{h}</h2><p class="lede">{p}</p></div>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Get a quote</a><a class="btn btn-line" href="packages.html">Compare packages</a></div>
</div></section>'''

def page(slug, title, desc, body, ld=None):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
{head(slug,title,desc,ld)}
</head>
<body>
{top(slug)}
<main id="main">
{body}
</main>
{FOOT}
{JS}
</body>
</html>'''

def crumbs(name, slug):
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},
        {"@type":"ListItem","position":2,"name":name,"item":DOMAIN+"/"+slug}]}

# ---------------- shared content ----------------
QA = [
 ('Is the stream going to hold up?', "We plug into a wired line and test it before anyone walks in. Hotel WiFi isn't an option for us; it's shared with every phone in the building. We also record on site the whole time, so if the internet hiccups, you still have the full event. Venues without a wired line get Starlink.", 'event-internet-starlink.html'),
 ('Will it look like our brand?', "Send us your logo, colors and fonts and we'll use them on the speaker names, the slides and the sponsor graphics. If a deck doesn't fit the screen, we fix it before anyone sees it.", 'event-presentation-graphics.html'),
 ("Can you work with the hotel's AV team?", "Yes, and we'd rather talk to them early. Internet, power, screens. If they charge for any of it, you'll know before you book, not after.", 'faq.html#logistics'),
 ('Can people watching online take part?', "They can. We set up a private viewing page for up to 1,000 people, and their questions get read on stage like everyone else's.", 'corporate-livestream-production.html'),
 ('What does it cost?', "Each package is one flat price. Add-ons are listed on your quote up front. We don't like surprise invoices either. Packages start at "+P('$2,890 during launch pricing','$3,400')+'.', 'packages.html'),
 ('What do we get afterward?', 'The full recording, as a download. If marketing wants photos, a highlight video or social clips, we can add those.', 'faq.html#deliverables'),
]

def qa_grid():
    return '<div class="qa-grid">' + ''.join(f'<article class="qa"><h3>{q}</h3><p>{a}</p><a href="{l}" class="arrow">More detail </a></article>' for q,a,l in QA) + '</div>'

PK = [
 ('Essential','1 camera · up to 2 hours','$2,890','$3,400',False,'Board meetings, town halls and single-speaker sessions.',
  ['1 camera, framed and switched','Technical director on site','Live switching with your slides','Stream to your platform, Zoom, LinkedIn or YouTube','Program recording delivered']),
 ('Professional','2 cameras · up to 4 hours','$4,930','$5,800',True,'Conferences, panels, trainings and webinars.',
  ['2 cameras with a camera operator','Technical director on site','Branded on-screen names and titles','Branded logo, agenda and key-point graphics','1 presentation formatted for your screens','Program recording delivered']),
 ('Executive','3 cameras · up to 6 hours','$7,905','$9,300',False,'Multi-session conferences, product launches, galas and award shows.',
  ['3 cameras with 2 camera operators','Technical director on site','Stream to multiple platforms at once','Custom on-screen names, sponsor and brand graphics','Up to 3 presentations formatted','Program plus individual camera files']),
]
def pk_cards(starts=True):
    out=[]
    for n,meta,now,was,feat,best,items in PK:
        pre = 'Starts at ' if (starts and n!='Essential') else ''
        out.append(f'''<article class="pcard{' feat' if feat else ''}">{'<span class="badge">MOST POPULAR</span>' if feat else ''}
  <div><h3 style="font-size:26px">{n}</h3><p class="meta">{meta}</p></div>
  <div class="price"><span class="now">{P(now,was)}</span><s data-promo>{was}</s><small>{P(pre+"launch price · save 15%", "Starts at · flat package price" if pre else "Flat package price")}</small></div>
  <p style="color:var(--ink-2);font-size:16px">{best}</p>
  <ul class="checks">{''.join(f'<li>{i}</li>' for i in items)}</ul>
  <a class="btn {'btn-gold' if feat else 'btn-dark'} arrow" href="contact.html">Request {n}</a>
</article>''')
    return '<div class="pk">'+''.join(out)+'</div>'

def multiview():
    return '''<div class="multiview" role="img" aria-label="Illustration of a live production multiview: program feed with a speaker lower third, two camera angles and a slide">
  <div class="mv pgm" style="background-image:url(images/town-hall.jpg)"><span class="tally">LIVE</span><span>PROGRAM</span>
    <div class="lt"><b>Chief Executive Officer</b><i>Your Company · Annual Conference</i></div></div>
  <div class="mv pvw" style="background-image:url(images/festival.jpg)"><span>CAM 2 · PREVIEW</span></div>
  <div class="mv slide"><b>2027 Sales Kickoff</b><i>Formatted for every screen in the room</i><span>SLIDES</span></div>
  <div class="mv-meta"><span>REC 01:12:44</span><span><b>●</b> STREAMING · 1080p</span></div>
</div>'''

# ---------------- HOME ----------------
AUD_CARDS=''.join(f'<a href="{a["file"]}" style="background-image:url(images/{a["img"]})"><h3>{a["name"]}</h3><p>{a["card"]}</p><span class="more arrow">{a["short"]}</span></a>' for a in AUDS)
home = f'''
<section class="stage hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/hero-stage.jpg)"></div><div class="wrap">
  <div class="hero-copy">
    <h1 id="h1" class="eyebrow">Event production &amp; livestreaming in Myrtle Beach, SC</h1>
    <p class="display">Your moment, <span>on every screen.</span></p>
    <p class="lede">Livestreaming, multi-camera production, IMAG screens and recap video for conventions, corporate events, festivals and tournaments.</p>
    <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Start with a conversation</a><a class="btn btn-line" href="packages.html">See packages</a></div>
  </div>
  {multiview()}
</div></section>

<section aria-labelledby="listen"><div class="wrap statement">
  <span class="eyebrow">We listen first</span>
  <h2 id="listen">You don't need to speak AV.</h2>
  <p class="big">You run the event. We run the tech.</p>
  <p>Tell us what matters. We handle the cameras, cables and connections, and only bring you the decisions that need you.</p>
</div></section>

<section style="background:var(--paper-2)" aria-labelledby="who"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Who we work with</span><h2 id="who">Built for the events the Grand Strand hosts.</h2>
  <p class="lede">Conventions, companies, festivals and tournaments. Different crowds, the same standard.</p></div>
  <div class="feel">{AUD_CARDS}</div>
</div></section>

<section class="stage" aria-labelledby="exp"><div class="stage-img" style="background-image:url(images/festival.jpg)"></div><div class="wrap statement">
  <span class="eyebrow">Experience</span>
  <h2 id="exp">Built on festival stages and broadcast sets.</h2>
  <p>Since 2016: corporate events, music festivals, commercial productions and live TV broadcasts. Your event gets the same preparation.</p>
  <div class="creds"><div><b>Corporate</b><span>Conferences and leadership events</span></div><div><b>Music festivals</b><span>Large crowds, big stages</span></div><div><b>Commercials</b><span>Large commercial productions</span></div><div><b>TV and broadcast</b><span>Live, on schedule</span></div></div>
</div></section>

<section style="background:var(--paper-2)" aria-labelledby="feel"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What you get</span><h2 id="feel">It's about how it feels.</h2>
  <p class="lede">What your audience experiences, in the room and online.</p></div>
  <div class="feel">
    <a href="imag-event-screens.html" style="background-image:url(images/imag.jpg)"><h3>The room feels close.</h3><p>IMAG puts your speakers on the big screens for the whole room.</p><span class="more arrow">IMAG</span></a>
    <a href="corporate-livestream-production.html" style="background-image:url(images/broadcast.jpg)"><h3>People far away feel invited.</h3><p>A multi-camera livestream for remote attendees, with live Q&amp;A.</p><span class="more arrow">Livestreaming</span></a>
    <a href="event-presentation-graphics.html" style="background-image:url(images/conference.jpg)"><h3>Your brand looks like you.</h3><p>Slides, speaker names and sponsor graphics in your colors and fonts.</p><span class="more arrow">Graphics</span></a>
    <a href="multi-camera-event-production.html" style="background-image:url(images/gala.jpg)"><h3>And you get to enjoy it.</h3><p>Our crew runs the production. You stay with your guests.</p><span class="more arrow">Cameras and crew</span></a>
  </div>
</div></section>

<section aria-labelledby="how"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it goes</span><h2 id="how">Simple, from the first call.</h2></div>
  <ol class="steps">
    <li><h3>Tell us about it</h3><p>A short call about the event, the audience and your goals.</p></li>
    <li><h3>We plan it</h3><p>We coordinate with the venue, plan cameras and build your graphics. You approve.</p></li>
    <li><h3>You host</h3><p>We arrive early and run everything. One crew, start to finish.</p></li>
    <li><h3>You keep it</h3><p>The full recording, plus photos and a highlight film if you want them.</p></li>
  </ol>
</div></section>

<section style="background:var(--paper-2)" aria-labelledby="pkh"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Packages</span><h2 id="pkh">Clear pricing. No surprises.</h2>
  <p class="lede">Crew, gear, live switching and your recording come with every package.{P(" Book before January 1, 2027 and it's 15% off.")}</p></div>
  {pk_cards()}
  <p style="margin-top:28px;text-align:center"><a class="arrow" href="packages.html" style="font-weight:500">Compare every feature and add-on</a></p>
</div></section>

<section aria-labelledby="need"><div class="wrap">
  <div class="section-head"><span class="eyebrow">The fine print, in plain words</span><h2 id="need">A few things we'll need from you.</h2>
  <p class="lede">These come from you or your venue. We put them in writing up front.</p></div>
  <div class="needs">
    <div><b>A wired internet line</b><p>A dedicated line from the venue. We don't stream over WiFi. If there's no line, we can bring Starlink.</p></div>
    <div><b>A sound feed</b><p>A feed from the venue's sound system, or our sound package if they don't have one.</p></div>
    <div><b>Your materials, 3 weeks out</b><p>Slides, logos and speaker names, so everything is built and tested before the day.</p></div>
    <div><b>A table and power</b><p>One spot near the stage for our production table.</p></div>
    <div><b>Venue fees</b><p>Some venues charge for internet or screen connections. Those are billed by the venue, and we'll tell you about them before you book.</p></div>
    <div><b>An honest note on internet</b><p>No one can guarantee an internet connection, us included. That's why we record the full event on site, every time.</p></div>
  </div>
</div></section>

<section style="background:var(--paper-2)" aria-labelledby="areas"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Where we work</span><h2 id="areas">Georgetown to Ocean Isle Beach.</h2></div>
  <div class="chips">{''.join(f'<a href="event-av-{a_}.html">{n_}</a>' for a_,n_ in [('myrtle-beach','Myrtle Beach'),('north-myrtle-beach','North Myrtle Beach'),('conway','Conway'),('little-river','Little River'),('surfside-beach-garden-city','Surfside Beach & Garden City'),('murrells-inlet','Murrells Inlet'),('pawleys-island-litchfield','Pawleys Island & Litchfield'),('georgetown','Georgetown'),('sunset-beach-calabash','Sunset Beach & Calabash'),('ocean-isle-beach','Ocean Isle Beach')])}<a href="areas.html">All areas</a></div>
</div></section>
{cta()}
'''

# ---------------- SERVICES ----------------
SVCS = [
 ('livestream','stream','Livestreaming','For the people who couldn\'t be in the room.',
  "Remote people usually get one laptop camera and room audio. Most of them drift off. The recording isn't much use either.",
  "We switch between cameras and slides live, put your graphics on it, take audio straight from the sound system, and send it where your audience is. Private page, Zoom, LinkedIn, YouTube, your intranet.",
  "Remote people actually see the event. And you keep a recording worth putting in the library.",
  ['Private viewing page for up to 500 or 1,000 people','Live Q&A for remote attendees through Zoom','Several platforms at once (Executive, or add it on)','Test stream before doors open']),
 ('production','cam','Cameras and crew','Your team runs the event. We run the video.',
  "Your people are already handling registration, speakers and sponsors. Running cameras on top of that? Not realistic.",
  "A technical director runs the whole thing from one table while camera operators get the close, steady shots. For an extra angle without another person, there's a robotic PTZ camera.",
  "Your staff stays with your guests. We handle the shots.",
  ['1 to 3 cameras, depending on the package','Operators for close, steady shots','Robotic PTZ camera (add-on)','Live switching between cameras and slides']),
 ('graphics','slides','Slides and graphics','Your brand on every screen.',
  "Every speaker shows up with a different deck. Different sizes, different fonts, one that's stretched. It adds up, and it looks sloppy.",
  "Send us the presentations and your brand guidelines about 3 weeks out. We format every deck for your screens and build the name graphics, the agenda and the sponsor slides.",
  "Speakers look ready. Sponsors get seen. It looks like one event.",
  ['Presentations formatted for your screens','Name and title graphics, branded or custom','Agenda, sponsor and key-point graphics','Presenter clicker and laptop if you need them']),
 ('imag','screen','IMAG','So the back of the room can see.',
  "In a big ballroom, half the room is watching your CEO from very far away.",
  "We send our camera shots and the slides to the venue's projectors and TVs. Same feed as the stream, more or less.",
  "Everyone in the room can see who's talking. The room pays attention longer.",
  ['Live close-ups and slides on venue screens','Feeds to overflow rooms and confidence monitors','Signal distribution for long runs','Screens come from the venue']),
 ('internet','net','Internet','Wired first. Starlink if there\'s no wire.',
  "Venue WiFi is shared with every phone in the building. It's not built for live video.",
  "We plug into a dedicated wired line and run cable up to 600 feet. Where there's no line at all, we bring Starlink, with a cellular backup for multi-day events.",
  "The best connection the venue can give you. And a full recording on site no matter what the internet does.",
  ['Dedicated wired connection, up to 600 ft','No streaming over venue WiFi','Starlink (add-on)','Starlink with cellular backup for multi-day events']),
 ('audio','mic','Audio','Bad audio sinks a good stream.',
  "Great picture, muddy sound. People leave.",
  "We take a feed straight from the house sound system. If the venue doesn't have one, our sound package brings an engineer, a mixer and mics.",
  "People hear every word, in the room or at home.",
  ['Feed from the venue sound system','Audio engineer and digital soundboard (add-on)','Mic and connection kit','Projection and lighting: ask us']),
 ('content','photo','Photo and recap video','Something to use after it\'s over.',
  "The event ends and marketing has nothing to post. Next year's promotion starts from zero.",
  "Add a photographer with an edited online gallery. Add a videographer for a 2 to 3 minute highlight film. Short social clips too, if you want them.",
  "Content that sells next year's event and thanks this year's sponsors.",
  ['Event photographer and online gallery','2 to 3 minute highlight film','15 to 30 second vertical social clips','Raw footage and individual camera files']),
]
svc_ld = [{"@context":"https://schema.org","@type":"Service","name":t,"serviceType":t,"provider":{"@id":DOMAIN+"/#business"},"areaServed":"Myrtle Beach and the Grand Strand, SC","audience":{"@type":"BusinessAudience","name":"Associations, corporate teams, event producers and tournament organizers"},"description":s} for _,_,t,_,_,s,_,_ in SVCS]
services = f'''
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/broadcast.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Services</nav>
  <span class="eyebrow">Services</span><h1 id="h1">Everything happens in the background.</h1>
  <p class="lede">Livestreaming, cameras and crew, IMAG, graphics, internet, audio and recap video for conventions, corporate events, festivals and tournaments on the Grand Strand.</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Get a quote</a><a class="btn btn-line" href="packages.html">See packages</a></div>
</div></section>
<div class="wrap">
''' + ''.join(f'''<article class="svc" id="{a}" style="scroll-margin-top:80px">
  <div class="head"><span class="ic" style="width:48px;height:48px;border-radius:12px;background:#F6EEE2;display:grid;place-items:center;color:var(--gold-ink)">{ICON[ic]}</span><h2>{t}</h2><p class="lede">{tag}</p><a class="btn btn-dark arrow" style="align-self:flex-start" href="{SFILE[a]}">{t} details</a></div>
  <div><div class="pso"><div><b>The problem</b><p>{p}</p></div><div><b>What we do</b><p>{s}</p></div><div><b>What you get</b><p>{o}</p></div></div>
  <ul class="checks">{''.join(f'<li>{x}</li>' for x in li)}</ul></div>
</article>''' for a,ic,t,tag,p,s,o,li in SVCS) + '</div>\n' + cta('Not sure what you need?','Tell us about the event. Most fit one of the three packages. If yours doesn\'t, we\'ll put something together.')

# ---------------- PACKAGES ----------------
ROWS = [
 ('Best for','Board meetings, town halls, single-speaker sessions','Conferences, panels, trainings','Multi-session conferences, launches, galas, award shows','Multi-day, multi-room conferences and trade shows'),
 ('Cameras','1','2','3','Custom'),
 ('Program length','Up to 2 hours','Up to 4 hours','Up to 6 hours','Full day or multi-day'),
 ('Production crew','Technical director','Technical director + camera operator','Technical director + 2 camera operators','Scaled to your event'),
 ('Live stream + live switching','✓','✓','✓','✓'),
 ('Streaming destination','1 platform','1 platform','Multiple platforms at once','Multiple platforms at once'),
 ('Presentation / slide integration','✓','✓','✓','✓'),
 ('Presentation prep','Add-on','1 presentation','Up to 3 presentations','Custom'),
 ('On-screen names and titles','—','Branded','✓','✓'),
 ('On-screen graphics','—','Branded logo + key points','✓','✓'),
 ('Recording delivery','Program recording','Program recording','Program + individual camera files','Program + individual camera files'),
]
ADDONS = [('Extra cameras','Another angle with an operator. Wide shot, the audience, a second stage.'),('Robotic PTZ camera','An extra angle with preset shots. No extra person.'),
 ('IMAG','Close-ups and slides on the venue projectors and TVs.'),('Sound package','Audio engineer, digital soundboard, connection kit.'),
 ('Private viewing page','We set it up and pay for it. Up to 500 or 1,000 viewers.'),('Starlink','For venues with no wired line. Cellular backup available.'),
 ('Photography','A photographer and an edited online gallery.'),('Recap video and social clips','A 2 to 3 minute highlight film. Short vertical clips.'),
 ('More presentation prep','More speakers, more decks, all formatted for your screens.'),('Projection and lighting','Projectors, screens, LED color lighting. Ask us.')]

MOB_PRICE=[(P('<s>$3,400</s> <b>$2,890</b>','<b>$3,400</b>')),(P('<s>$5,800</s> <b>from $4,930</b>','<b>from $5,800</b>')),(P('<s>$9,300</s> <b>from $7,905</b>','<b>from $9,300</b>')),('<b>Inquire</b>')]
MOB_NAME=['Essential','Professional','Executive','Custom']
def mob_card(i):
    rows=''.join(f'<div class="r"><dt>{r[0]}</dt><dd>{r[i+1]}</dd></div>' for r in ROWS)
    feat=' feat' if i==1 else ''
    btn=f'<a class="btn {"btn-gold" if i==1 else "btn-dark"} arrow" href="contact.html">{"Ask about Custom" if i==3 else "Request "+MOB_NAME[i]}</a>'
    return f'<article class="mcard{feat}"><div class="mh"><h3>{MOB_NAME[i]}</h3><div class="mp">{MOB_PRICE[i]}</div>{P("<small>Launch price · save 15%</small>") if i<3 else ""}</div><dl>{rows}</dl>{btn}</article>'
offer_ld = {"@context":"https://schema.org","@type":"OfferCatalog","name":"Uplift AV livestream packages","itemListElement":[
  {"@type":"Offer","name":n+" livestream package","price":was.replace('$','').replace(',',''),"priceCurrency":"USD","description":best,"seller":{"@id":DOMAIN+"/#business"}} for n,meta,now,was,feat,best,items in PK]}
packages = f'''
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/gala.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Packages</nav>
  <span class="eyebrow">Packages and pricing</span><h1 id="h1">Clear pricing. No surprises.</h1>
  <p class="lede">Crew, gear, live switching and your recording come with every package, so you can compare them fairly.{P(" Book before January 1, 2027 and it's 15% off.")}</p>
</div></section>
<section aria-label="Package cards"><div class="wrap">{pk_cards()}
  <p style="margin-top:18px;color:var(--muted);font-size:15px">{P("Launch prices apply to events booked before January 1, 2027. ")}Prices shown are per event day. Multi-day and multi-room events are quoted as Custom.</p>
</div></section>
<section style="background:var(--paper-2);padding-top:clamp(56px,7vw,96px)" aria-labelledby="cmp"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Compare</span><h2 id="cmp">Choose your livestream package</h2></div>
  <div class="tbl"><table>
    <thead><tr><th scope="col" style="text-align:left">Feature</th><th scope="col">Essential</th><th scope="col" class="hl">Professional</th><th scope="col">Executive</th><th scope="col">Custom</th></tr></thead>
    <tbody>{''.join(f'<tr><th scope="row">{r[0]}</th>'+''.join(f'<td>{c}</td>' for c in r[1:])+'</tr>' for r in ROWS)}
    <tr><th scope="row">{P('Standard rate','Price')}</th><td><s data-promo>$3,400</s><span data-after><strong>$3,400</strong></span></td><td><s data-promo>$5,800</s><span data-after><strong>from $5,800</strong></span></td><td><s data-promo>$9,300</s><span data-after><strong>from $9,300</strong></span></td><td>{P('—','Inquire')}</td></tr>
    <tr class="launch" data-promo><th scope="row">Launch price (save 15%)</th><td>$2,890</td><td>from $4,930</td><td>from $7,905</td><td>Inquire</td></tr>
    </tbody></table></div>
  <div class="cmp-m">{''.join(mob_card(i) for i in range(4))}</div>
</div></section>
<section aria-labelledby="add"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Add-ons</span><h2 id="add">Add-ons</h2></div>
  <div class="qa-grid">{''.join(f'<article class="qa"><h3>{a}</h3><p>{b}</p></article>' for a,b in ADDONS)}</div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="need"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Before show day</span><h2 id="need">What we need from the venue</h2></div>
  <div class="qa-grid">
    <article class="qa"><h3>A wired internet line</h3><p>A dedicated line at a venue switch. We'll run cable up to 600 feet to it. WiFi doesn't count.</p></article>
    <article class="qa"><h3>Audio feed</h3><p>A feed from the house sound system. Or add our sound package.</p></article>
    <article class="qa"><h3>Screens for IMAG</h3><p>Their projectors or TVs. If they charge to connect, that fee is billed by the venue.</p></article>
    <article class="qa"><h3>Production space</h3><p>One table, power, and a view of the stage.</p></article>
    <article class="qa"><h3>Materials, 3 weeks out</h3><p>Decks, logos, speaker names. That gives us time to build and test the graphics.</p></article>
    <article class="qa"><h3>A venue contact</h3><p>Someone who can answer questions about internet, power and load-in.</p></article>
  </div>
</div></section>
{cta(P('Want the launch price?','Get a quote'),P('Book before January 1, 2027. Any package, 15% off.','Send the date, the venue and roughly how many people. We\'ll tell you which package fits.'))}
'''

# ---------------- FAQ ----------------
FAQ = [
 ('reliability','Reliability',[
  ('Will our livestream drop or lag?','We stream over a dedicated wired line, never venue WiFi, and run a full test before the event. No wired line? Starlink, with cellular backup for multi-day events. No one can guarantee internet, so we also record on site.'),
  ('What if the venue has no wired internet?','We run cable up to 600 feet from the venue switch. With no wired line, our Starlink add-on handles the stream.'),
  ('What happens if something goes wrong during the event?','The program records on site, separate from the stream, so you keep the full recording either way. Our technical director monitors the stream throughout.')]),
 ('cost','Cost',[
  ('How much does a livestream cost?','Essential is $3,400. That\'s 1 camera, up to 2 hours. Professional starts at $5,800 (2 cameras, up to 4 hours), and Executive starts at $9,300 (3 cameras, up to 6 hours). Add-ons are priced separately.'+P(' Book before January 1, 2027 and they\'re 15% off: $2,890, $4,930 and $7,905.')),
  ('Are there hidden fees?','No. Your quote lists the package and every add-on. Some venues charge for an internet line or projector connections; those are billed by the venue, and we flag them before you book.')]),
 ('logistics','Logistics',[
  ('What do we need to provide?','A wired internet line, a feed from the house sound system, a table with power near the stage. Screens too, if you want IMAG. We sort out the details with the venue.'),
  ("Can you work with the hotel or venue's in-house AV team?",'Yes. We coordinate internet, power, audio and screens with in-house AV before show day, and flag any venue fees before you book.'),
  ('Can remote attendees ask questions?','Yes. With a hosted viewing page, remote attendees submit questions through Zoom or your platform, and they\'re read on stage.'),
  ('Do we need our own staff to run it?','No. Our crew runs it. What we need from your team: the materials and the run of show, ahead of time.'),
  ('How far in advance should we book?','As early as you can. Then get us presentations, logos and speaker names about 3 weeks before, so the graphics are built and tested.'),
  ('Can you stream to Zoom, LinkedIn, YouTube and our website at the same time?','Yes. Executive includes multi-platform streaming; it\'s an add-on for other packages. We also host private viewing pages for up to 1,000 viewers.'),
  ('Can you put the speaker on the screens in the room?','Yes. That\'s IMAG. Our camera shots and slides go to the venue projectors and TVs while we stream.')]),
 ('deliverables','Deliverables',[
  ('Do we get a recording of the event?','Yes, every package. It comes as a download. Executive also includes the separate camera files, in case you want to edit later.'),
  ('Can you shoot photos and a highlight video?','Yes. Add a photographer with an edited online gallery. Add a videographer for a 2 to 3 minute highlight film, plus short social clips if you want them.'),
  ('Where do you work?','We\'re on the Grand Strand. Hotels, resorts and convention venues from Georgetown to Ocean Isle Beach. Farther than that? Ask.')]),
]
faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ld_text(a)}} for _,_,items in FAQ for q,a in items]}
faq = f'''
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/town-hall.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / FAQ</nav>
  <span class="eyebrow">FAQ</span><h1 id="h1">Good questions. Honest answers.</h1>
  <p class="lede">Livestream reliability, pricing, venue logistics and deliverables.</p>
</div></section>
<section><div class="wrap faq-cols">
  <nav class="toc" aria-label="FAQ topics">{''.join(f'<a href="#{a}">{t}</a>' for a,t,_ in FAQ)}</nav>
  <div>{''.join(f'<div class="faq-group" id="{a}"><h2 style="font-size:30px">{t}</h2><div class="faq">'+''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="a"><p>{ans}</p></div></details>' for i,(q,ans) in enumerate(items))+'</div></div>' for a,t,items in FAQ)}</div>
</div></section>
{cta('Still have a question?','Email it to us. We\'ll answer, and help you pick a package if you want.')}
'''

# ---------------- CONTACT ----------------
contact = f'''
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/beams.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Contact</nav>
  <span class="eyebrow">Contact</span><h1 id="h1">Tell us about your event.</h1>
  <p class="lede">We reply within one business day, usually sooner.</p>
</div></section>
<section><div class="wrap contact-grid">
  <form id="quote-form" class="qform" action="https://api.web3forms.com/submit" method="POST" novalidate>
    <input type="hidden" name="access_key" value="{FORM_KEY}">
    <input type="hidden" name="subject" value="New quote request from upliftavtech.com">
    <input type="hidden" name="from_name" value="Uplift AV website">
    <input type="hidden" name="redirect" value="{DOMAIN}/thanks.html">
    <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
    <h2 style="font-size:28px">Start here</h2>
    <p class="muted-sm">* Required</p>
    <div class="fgrid">
      <label class="fld">Name *<input id="f-name" name="name" required autocomplete="name"></label>
      <label class="fld">Company *<input id="f-company" name="company" required autocomplete="organization"></label>
      <label class="fld">Email *<input id="f-email" type="email" name="email" required autocomplete="email"></label>
      <label class="fld">Phone<input id="f-phone" type="tel" name="phone" autocomplete="tel"></label>
      <label class="fld">Event date *<input id="f-date" name="event_date" required placeholder="e.g. March 12, 2027"></label>
      <label class="fld">Start and end time<input id="f-time" name="event_time" placeholder="e.g. 9:00 am to 3:00 pm"></label>
      <label class="fld">Venue<input id="f-venue" name="venue" placeholder="Venue name and room"></label>
      <label class="fld">Area *<select id="f-area" name="area" required><option value="">Choose an area</option>{AREA_OPTS}<option>Other</option></select></label>
      <label class="fld">In-person attendance<select id="f-inperson" name="in_person"><option value="">Choose</option><option>Under 50</option><option>50 to 150</option><option>150 to 500</option><option>500 to 1,000</option><option>Over 1,000</option></select></label>
      <label class="fld">Online audience<select id="f-online" name="online_audience"><option value="">Choose</option><option>No livestream needed</option><option>Under 100</option><option>100 to 500</option><option>500 to 1,000</option><option>Over 1,000</option><option>Not sure yet</option></select></label>
      <label class="fld">Package<select id="f-package" name="package"><option value="">Not sure yet</option><option>Essential</option><option>Professional</option><option>Executive</option><option>Custom</option></select></label>
      <label class="fld">Where should it stream?<input id="f-platform" name="platform" placeholder="Zoom, LinkedIn, YouTube, private page"></label>
    </div>
    <fieldset class="fset"><legend>Add-ons you're interested in</legend>
      <div class="chk">{ADDON_CHECKS}</div></fieldset>
    <label class="fld" style="grid-column:1/-1">What would make this event a success for you?<textarea id="f-goal" name="success_looks_like" rows="3" placeholder="Who needs to feel included, what you want people to walk away with, anything you\'re worried about"></textarea></label>
    <label class="fld">Anything else we should know?<textarea id="f-msg" name="message" rows="5" placeholder="Agenda, number of speakers or presentations, special requests"></textarea></label>
    <div class="factions"><button class="btn btn-gold" type="submit" id="f-submit">Send request</button><p class="fstatus" id="f-status" role="status" aria-live="polite"></p></div>
  </form>
  <aside class="side" aria-label="Contact details">
    <div class="card"><span class="eyebrow">Email</span><a class="email" href="mailto:{EMAIL}">{EMAIL}</a><button class="copy" type="button" data-copy="{EMAIL}">Copy email</button></div>
    <div class="card"><span class="eyebrow">Include in your request</span><ul><li>Event date and start and end times</li><li>Venue name and room</li><li>Expected in-person and online audience</li><li>Run of show or agenda, if you have one</li><li>Where you want to stream</li><li>Number of speakers or presentations</li><li>Any add-ons, like IMAG, photography or Starlink</li></ul></div>
    <div class="card"><span class="eyebrow">Service area</span><p>{AREA}, plus the Brunswick County coast in North Carolina. Farther out? Ask.</p></div>
    <div class="card" style="background:#F6EEE2" data-promo><span class="eyebrow">Launch pricing</span><p><strong>15% off every package</strong> for events booked before January 1, 2027.</p><a class="arrow" style="font-weight:600" href="packages.html">See packages </a></div>
  </aside>
</div></section>
'''
contact_ld = {"@context":"https://schema.org","@type":"ContactPage","name":"Contact Uplift AV","url":DOMAIN+"/contact.html","mainEntity":{"@id":DOMAIN+"/#business"}}

# ---------------- CITY PAGES ----------------
import importlib.util as _iu
_sp=_iu.spec_from_file_location('cities',os.path.join(D,'cities.py')); _m=_iu.module_from_spec(_sp); _sp.loader.exec_module(_m)
CITIES=_m.CITIES; COUNTIES=_m.COUNTIES
CBY={c['slug']:c for c in CITIES}
def cfile(slug): return f'event-av-{slug}.html'
def city_page(c):
    nm, st = c['name'], c['st']
    venues=''.join(f'<li>{v}</li>' for v in c['venues'])
    focus=''.join(f'<article class="qa"><h3>{h}</h3><p>{p}</p></article>' for h,p in c['focus'])
    faqh=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for i,(q,a) in enumerate(c['faq']))
    near=''.join(f'<a class="btn btn-line" href="{cfile(n)}">{CBY[n]["name"]}</a>' for n in c['near'])
    body=f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/{c['img']})"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="areas.html">Areas</a> / {nm}</nav>
  <span class="eyebrow">{c['county']}, {st}</span>
  <h1 id="h1">Event production and livestreaming in {nm}, {st}</h1>
  <p class="lede">{c['intro']}</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Get a {nm} quote</a><a class="btn btn-line" href="packages.html">See packages</a></div>
</div></section>
<section aria-labelledby="fit"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How we help in {nm}</span><h2 id="fit">Built for {nm} events</h2>
  <p class="lede">Common events we produce here: {c['events']}</p></div>
  <div class="qa-grid">{focus}</div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="ven"><div class="wrap contact-grid">
  <div style="display:flex;flex-direction:column;gap:14px"><span class="eyebrow">Venues</span><h2 id="ven">Ready for {nm} venues</h2>
    <p class="lede">We bring our own cameras, switcher and crew, and coordinate with each venue's event or in-house AV team on internet, power and screens. Event venues in and around {nm} include:</p>
    <ul class="checks">{venues}</ul>
    <p style="color:var(--muted);font-size:15px">Venue names are listed for reference only and do not imply a partnership. We work at any venue with power and a place to set up.</p></div>
  <aside class="side"><div class="card"><span class="eyebrow">Every package includes</span><ul><li>Technical director and camera crew</li><li>Live switching with your slides</li><li>Stream to your platform, Zoom, LinkedIn or YouTube</li><li>Program recording delivered</li></ul></div>
  <div class="card" style="background:#F6EEE2" data-promo><span class="eyebrow">Launch pricing</span><p><strong>15% off every package</strong> for events booked before January 1, 2027. Packages from $2,890.</p><a class="arrow" style="font-weight:600" href="packages.html">Compare packages </a></div><div class="card" style="background:#F6EEE2" data-after><span class="eyebrow">Flat pricing</span><p>Packages from <strong>$3,400</strong>, with crew, switching and recording included.</p><a class="arrow" style="font-weight:600" href="packages.html">Compare packages </a></div></aside>
</div></section>
<section aria-labelledby="pk"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Packages</span><h2 id="pk">{nm} event livestream packages</h2></div>
  {pk_cards()}
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="lfaq"><div class="wrap">
  <div class="section-head"><span class="eyebrow">{nm} FAQ</span><h2 id="lfaq">Questions from {nm} event planners</h2></div>
  <div class="faq">{faqh}</div>
  <div style="margin-top:36px;display:flex;flex-direction:column;gap:12px"><span class="eyebrow">Nearby areas we serve</span><div class="btns">{near}<a class="btn btn-line" href="areas.html">All areas</a></div></div>
</div></section>
{cta(f'Planning an event in {nm}?','Tell us the date, venue and audience. We will recommend a package and send a clear, flat-price quote.')}
"""
    url=DOMAIN+'/'+cfile(c['slug'])
    ld=[{"@context":"https://schema.org","@type":"Service","name":f"Event production and livestreaming in {nm}, {st}","serviceType":"Event production and livestreaming","provider":{"@id":DOMAIN+"/#business"},"url":url,
         "areaServed":{"@type":"Place","name":f"{nm}, {st}","address":{"@type":"PostalAddress","addressLocality":nm.split(' & ')[0],"addressRegion":st,"addressCountry":"US"}}},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in c['faq']]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Areas","item":DOMAIN+"/areas.html"},{"@type":"ListItem","position":3,"name":nm,"item":url}]}]
    title=f"Corporate Event AV & Livestreaming in {nm}, {st} | Uplift AV"
    desc=f"Corporate event AV, hybrid livestreams and IMAG in {nm}, {st}. Crew, branded graphics and recording included. Serving {c['county']}. Flat package pricing."
    return (cfile(c['slug']), title, desc, body, ld)

areas_body = f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/beams.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Areas</nav>
  <span class="eyebrow">Service areas</span><h1 id="h1">Event production across the Grand Strand and Brunswick County coast</h1>
  <p class="lede">We produce conventions, corporate events, festivals, tournaments and livestreams from Georgetown, SC to Ocean Isle Beach, NC. Pick your area for local venues, common event types and answers for planners.</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Get a quote</a></div>
</div></section>
<section><div class="wrap" style="display:flex;flex-direction:column;gap:56px">
""" + ''.join(f"""<div><div class="section-head" style="margin-bottom:24px"><h2 style="font-size:32px">{cn}</h2></div><div class="qa-grid">""" + ''.join(f"""<article class="qa"><h3>{CBY[s_]['name']}</h3><p>{CBY[s_]['events']}</p><a class="arrow" href="{cfile(s_)}">{CBY[s_]['name']} event AV </a></article>""" for s_ in sl) + "</div></div>" for cn,sl in COUNTIES) + """
</div></section>
""" + cta()
areas_ld=[{"@context":"https://schema.org","@type":"CollectionPage","name":"Uplift AV service areas","url":DOMAIN+"/areas.html","about":{"@id":DOMAIN+"/#business"}}, crumbs('Areas','areas.html')]

# ---------------- SERVICE PAGES ----------------
AUD_CHIPS=''.join(f'<a href="{a["file"]}">{a["name"]}</a>' for a in AUDS)
def svc_page(x):
    inc=''.join(f'<li>{i}</li>' for i in x['includes'])
    opt=''.join(f'<li>{i}</li>' for i in x['options'])
    steps=''.join(f'<li><h3>{a}</h3><p>{b}</p></li>' for a,b in x['steps'])
    faqh=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for i,(q,a) in enumerate(x['faq']))
    rel=''.join(f'<a class="tile" href="{SBY[r]["file"]}"><span class="ic">{ICON[SBY[r]["icon"]]}</span><h3>{SBY[r]["name"]}</h3><p>{SBY[r]["lede"]}</p><span class="more arrow">Learn more </span></a>' for r in x['related'])
    chips=''.join(f'<a href="event-av-{a_}.html">{n_}</a>' for a_,n_ in [('myrtle-beach','Myrtle Beach'),('north-myrtle-beach','North Myrtle Beach'),('conway','Conway'),('little-river','Little River'),('surfside-beach-garden-city','Surfside Beach'),('murrells-inlet','Murrells Inlet'),('pawleys-island-litchfield','Pawleys Island'),('georgetown','Georgetown'),('sunset-beach-calabash','Sunset Beach'),('ocean-isle-beach','Ocean Isle Beach')])
    body=f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/{x['img']})"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="services.html">Services</a> / {x['name']}</nav>
  <span class="eyebrow">Services</span><h1 id="h1">{x['h1']}</h1>
  <p class="lede">{x['lede']}</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Get a quote</a><a class="btn btn-line" href="packages.html">See packages</a></div>
</div></section>
<section aria-labelledby="why"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Why it matters</span><h2 id="why">The problem, and how we solve it</h2></div>
  <div class="pso"><div><b>The problem</b><p>{x['problem']}</p></div><div><b>What we do</b><p>{x['solution']}</p></div><div><b>What you get</b><p>{x['outcome']}</p></div></div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="inc"><div class="wrap contact-grid">
  <div style="display:flex;flex-direction:column;gap:16px"><span class="eyebrow">What's included</span><h2 id="inc">What you get</h2><ul class="checks">{inc}</ul>
    <h3 style="margin-top:12px">Available add-ons</h3><ul class="checks">{opt}</ul></div>
  <aside class="side"><div class="card"><span class="eyebrow">Packages</span><h3>{x['pk'][0]}</h3><p>{x['pk'][1]}</p><a class="arrow" style="font-weight:600" href="packages.html">Compare packages </a></div>
  <div class="card" data-promo style="background:#F6EEE2"><span class="eyebrow">Launch pricing</span><p><strong>15% off every package</strong> for events booked before January 1, 2027.</p></div></aside>
</div></section>
<section aria-labelledby="how"><div class="wrap">
  <div class="section-head"><span class="eyebrow">How it works</span><h2 id="how">From booking to delivery</h2></div>
  <ol class="steps">{steps}</ol>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="sfaq"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2 id="sfaq">{x['name']} questions</h2></div>
  <div class="faq">{faqh}</div>
</div></section>
<section class="stage" aria-labelledby="rel"><div class="stage-img" style="background-image:url(images/gala.jpg)"></div><div class="wrap">
  <div class="section-head"><span class="eyebrow">Related services</span><h2 id="rel">Often booked together</h2></div>
  <div class="bento" style="grid-template-columns:repeat(3,minmax(0,1fr))">{rel}</div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="wf"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Who it's for</span><h2 id="wf">{x['name']} for every kind of event</h2></div>
  <div class="chips">{AUD_CHIPS}</div>
</div></section>
<section aria-labelledby="sa"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Service area</span><h2 id="sa">{x['name']} across the Grand Strand</h2></div>
  <div class="chips">{chips}<a href="areas.html">All areas →</a></div>
</div></section>
{cta()}
"""
    url=DOMAIN+'/'+x['file']
    ld=[{"@context":"https://schema.org","@type":"Service","name":x['h1'],"serviceType":x['name'],"description":x['desc'],"provider":{"@id":DOMAIN+"/#business"},"url":url,
         "areaServed":[{"@type":"AdministrativeArea","name":"Horry County, SC"},{"@type":"AdministrativeArea","name":"Georgetown County, SC"},{"@type":"AdministrativeArea","name":"Brunswick County, NC"}],
         "audience":{"@type":"BusinessAudience","name":"Associations, corporate teams, event producers and tournament organizers"}},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in x['faq']]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Services","item":DOMAIN+"/services.html"},{"@type":"ListItem","position":3,"name":x['name'],"item":url}]}]
    return (x['file'], x['title'], x['desc'], body, ld)


def aud_page(a):
    ev=''.join(f'<li>{i}</li>' for i in a['events'])
    inc=''.join(f'<li>{i}</li>' for i in a['includes'])
    faqh=''.join(f'<details{" open" if i==0 else ""}><summary>{q}</summary><div class="a"><p>{t}</p></div></details>' for i,(q,t) in enumerate(a['faq']))
    rel=''.join(f'<a class="tile" href="{SBY[r]["file"]}"><span class="ic">{ICON[SBY[r]["icon"]]}</span><h3>{SBY[r]["name"]}</h3><p>{SBY[r]["lede"]}</p><span class="more arrow">Learn more </span></a>' for r in a['related'])
    others=''.join(f'<a href="{o["file"]}">{o["name"]}</a>' for o in AUDS if o['key']!=a['key'])
    body=f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/{a['img']})"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / <a href="who-we-serve.html">Who we serve</a> / {a['name']}</nav>
  <h1 id="h1" class="eyebrow">{a['h1']}</h1>
  <p class="display" style="font-size:clamp(36px,5.2vw,64px)">{a['headline']}</p>
  <p class="lede">{a['lede']}</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Start with a conversation</a><a class="btn btn-line" href="packages.html">See packages</a></div>
</div></section>
<section aria-labelledby="why"><div class="wrap">
  <div class="section-head"><span class="eyebrow">What changes</span><h2 id="why">From the problem to the result</h2></div>
  <div class="pso"><div><b>The problem</b><p>{a['problem']}</p></div><div><b>What we do</b><p>{a['solution']}</p></div><div><b>What you get</b><p>{a['outcome']}</p></div></div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="inc"><div class="wrap contact-grid">
  <div style="display:flex;flex-direction:column;gap:16px"><span class="eyebrow">What we produce</span><h2 id="inc">Events we cover</h2><ul class="checks">{ev}</ul>
    <h3 style="margin-top:12px">What's included</h3><ul class="checks">{inc}</ul></div>
  <aside class="side"><div class="card"><span class="eyebrow">Recommended</span><h3>{a['pk'][0]}</h3><p>{a['pk'][1]}</p><a class="arrow" style="font-weight:600" href="packages.html">Compare packages </a></div>
  <div class="card" data-promo style="background:#F6EEE2"><span class="eyebrow">Launch pricing</span><p><strong>15% off every package</strong> for events booked before January 1, 2027.</p></div></aside>
</div></section>
<section aria-labelledby="afaq"><div class="wrap">
  <div class="section-head"><span class="eyebrow">FAQ</span><h2 id="afaq">Questions we hear</h2></div>
  <div class="faq">{faqh}</div>
</div></section>
<section class="stage" aria-labelledby="rel"><div class="stage-img" style="background-image:url(images/gala.jpg)"></div><div class="wrap">
  <div class="section-head"><span class="eyebrow">Services</span><h2 id="rel">What goes into it</h2></div>
  <div class="bento" style="grid-template-columns:repeat(3,minmax(0,1fr))">{rel}</div>
</div></section>
<section aria-labelledby="oth"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Also serving</span><h2 id="oth">Other events we produce</h2></div>
  <div class="chips">{others}<a href="areas.html">Service areas</a></div>
</div></section>
{cta()}
"""
    url=DOMAIN+'/'+a['file']
    ld=[{"@context":"https://schema.org","@type":"Service","name":a['h1'],"serviceType":a['name'],"description":a['desc'],"provider":{"@id":DOMAIN+"/#business"},"url":url,
         "areaServed":[{"@type":"AdministrativeArea","name":"Horry County, SC"},{"@type":"AdministrativeArea","name":"Georgetown County, SC"},{"@type":"AdministrativeArea","name":"Brunswick County, NC"}],
         "audience":{"@type":"Audience","audienceType":a['name']}},
        {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":t}} for q,t in a['faq']]},
        {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":"Who we serve","item":DOMAIN+"/who-we-serve.html"},{"@type":"ListItem","position":3,"name":a['name'],"item":url}]}]
    return (a['file'], a['title'], a['desc'], body, ld)

who_body = f"""
<section class="stage page-hero" aria-labelledby="h1"><div class="stage-img" style="background-image:url(images/hero-stage.jpg)"></div><div class="wrap">
  <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a> / Who we serve</nav>
  <span class="eyebrow">Who we serve</span><h1 id="h1">Event production for the Grand Strand's biggest gatherings</h1>
  <p class="lede">Association conventions, corporate events, festivals and tournaments. You run the event. We put it on every screen.</p>
  <div class="btns"><a class="btn btn-gold arrow" href="contact.html">Start with a conversation</a></div>
</div></section>
<section aria-labelledby="aud"><div class="wrap">
  <div class="section-head"><span class="eyebrow">Choose your event</span><h2 id="aud">Different crowds. The same standard.</h2></div>
  <div class="feel">{AUD_CARDS}</div>
</div></section>
<section style="background:var(--paper-2)" aria-labelledby="one"><div class="wrap statement">
  <span class="eyebrow">One team</span>
  <h2 id="one">The same crew, whatever the crowd.</h2>
  <p>A convention general session, a company town hall, a festival stage and a championship game need different setups. They need the same preparation: a venue walkthrough, a written plan, a tested stream and a crew that has done it before. Since 2016 we have produced events from Georgetown to Ocean Isle Beach, and every event gets that standard.</p>
</div></section>
{cta()}
"""
who_ld=[{"@context":"https://schema.org","@type":"CollectionPage","name":"Who Uplift AV serves","url":DOMAIN+"/who-we-serve.html","about":{"@id":DOMAIN+"/#business"},"hasPart":[{"@type":"WebPage","name":a['name'],"url":DOMAIN+"/"+a['file']} for a in AUDS]}, crumbs('Who we serve','who-we-serve.html')]

PAGES = [
 ('index.html','Corporate Event AV & Livestream Production in Myrtle Beach, SC | Uplift AV',
  'Corporate event AV and hybrid livestreams for conferences, sales kickoffs, product launches, town halls and galas in Myrtle Beach and the Grand Strand. Crew, branded graphics and IMAG included. Flat package pricing.', home, []),
 ('services.html','Corporate Event AV, Hybrid Events & IMAG Services | Uplift AV Myrtle Beach',
  'Hybrid event livestreams, multi-camera crews, branded presentation and sponsor graphics, IMAG, wired and Starlink internet, audio and recap content for corporate events on the Grand Strand.', services, svc_ld+[crumbs('Services','services.html')]),
 ('packages.html','Corporate Event Livestream Packages & Pricing | Uplift AV',
  'Compare Essential, Professional and Executive livestream packages. Flat pricing with crew, switching and recording included.', packages, [offer_ld, crumbs('Packages','packages.html')]),
 ('faq.html','Corporate Event Livestream & AV FAQ | Uplift AV',
  'Answers for event planners: stream reliability, cost, working with hotel AV, remote Q&A, what the venue provides and what you receive after the event.', faq, [faq_ld, crumbs('FAQ','faq.html')]),
 ('contact.html','Get a Corporate Event AV Quote | Contact Uplift AV',
  'Request a quote for corporate event AV and livestream production in Myrtle Beach and the Grand Strand. Email info@upliftavtech.com.', contact, [contact_ld, crumbs('Contact','contact.html')]),
]
PAGES.append(('thanks.html','Thanks | Uplift AV','Your quote request was sent.',f'''<section class="stage page-hero"><div class="stage-img" style="background-image:url(images/beams.jpg)"></div><div class="wrap"><span class="eyebrow">Request sent</span><h1 id="h1">Thanks. We got your request.</h1><p class="lede">We will reply by email, usually within one business day. If it is urgent, email {EMAIL}.</p><div class="btns"><a class="btn btn-gold" href="index.html">Back to home</a><a class="btn btn-line" href="packages.html">See packages</a></div></div></section>''',[]))
PAGES.append(('areas.html','Event AV Service Areas: Grand Strand & Brunswick County | Uplift AV','Corporate event AV and livestreaming in Myrtle Beach, North Myrtle Beach, Conway, Murrells Inlet, Pawleys Island, Georgetown, Little River, Sunset Beach and Ocean Isle Beach.',areas_body,areas_ld))
PAGES += [city_page(c) for c in CITIES]
PAGES += [svc_page(x) for x in SERVICES]
PAGES.append(('who-we-serve.html','Who We Serve | Uplift AV','Event production for association conventions, corporate events, festivals and tournaments on the Grand Strand.',who_body,who_ld))
PAGES += [aud_page(a) for a in AUDS]
out = os.path.join(D,'out'); os.makedirs(out, exist_ok=True)
for slug,t,d,b,ld in PAGES:
    open(os.path.join(out,slug),'w').write(page(slug,t,d,b,ld))
_t=os.path.join(out,'thanks.html'); _x=open(_t).read(); open(_t,'w').write(_x.replace('content="index,follow"','content="noindex,follow"'))
open(os.path.join(out,'robots.txt'),'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
open(os.path.join(out,'sitemap.xml'),'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{DOMAIN}/{"" if s=="index.html" else s}</loc><lastmod>2026-10-19</lastmod></url>\n' for s,*_ in PAGES if s!='thanks.html')+'</urlset>\n')
# artifact entry: index without document skeleton
idx = open(os.path.join(out,'index.html')).read()
h = idx[idx.index('<head>')+6:idx.index('</head>')].replace('<meta charset="utf-8">','')
bd = idx[idx.index('<body>')+6:idx.index('</body>')]
open(os.path.join(D,'artifact_index.html'),'w').write(h.strip()+'\n'+bd.strip())
print('done')

exec(open(os.path.join(D,'seo_post.py')).read())
