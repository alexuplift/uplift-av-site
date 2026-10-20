# Post-process generated pages: clean URLs, tuned titles/descriptions, hero preload, sitemap lastmod.
import re, glob, os, datetime, html, json
OUT=os.path.join(os.path.dirname(os.path.abspath(__file__)),'out'); D='https://upliftavtech.com'
TODAY=datetime.date.today().isoformat()
T={
 'index':("Event Production & Livestreaming Myrtle Beach | Uplift AV","Event production and livestreaming on the Grand Strand: multi-camera, IMAG screens and recap video for conventions, corporate events, festivals and tournaments."),
 'services':("Event Production Services in Myrtle Beach | Uplift AV","Livestreaming, multi-camera crews, IMAG, presentation graphics, event internet, audio and recap video for conventions, corporate events and festivals."),
 'packages':("Livestream & Event AV Packages and Pricing | Uplift AV","Compare Essential, Professional and Executive event livestream packages. Flat pricing with crew, live switching and your recording included. Grand Strand, SC."),
 'faq':("Event Production & Livestream FAQ | Uplift AV","Answers for event planners: internet and stream planning, cost, working with hotel AV, remote Q&A, what the venue provides and what you receive afterward."),
 'contact':("Get an Event Production Quote | Contact Uplift AV","Request a quote for event production and livestreaming in Myrtle Beach and the Grand Strand: conventions, corporate events, festivals and tournaments."),
 'areas':("Event Production Service Areas, Grand Strand | Uplift AV","Event production and livestreaming in Myrtle Beach, North Myrtle Beach, Conway, Murrells Inlet, Pawleys Island, Georgetown, Little River and Ocean Isle Beach."),
 'corporate-livestream-production':("Event Livestream Production, Myrtle Beach SC | Uplift AV","Multi-camera event livestreams and hybrid events on the Grand Strand. Private viewing pages, Zoom, LinkedIn or YouTube, live Q&A and a full recording."),
 'multi-camera-event-production':("Multi-Camera Event Production, Myrtle Beach | Uplift AV",None),
 'event-presentation-graphics':("Event Presentation Graphics & Lower Thirds | Uplift AV",None),
 'imag-event-screens':("IMAG & Event Screens in Myrtle Beach, SC | Uplift AV",None),
 'event-internet-starlink':("Event Internet & Starlink for Livestreams | Uplift AV",None),
 'event-audio':("Event Audio for Livestreams & Live Events | Uplift AV",None),
 'event-photo-video':("Event Photography & Recap Video, Myrtle Beach | Uplift AV",None),
}
SHORT={'surfside-beach-garden-city':('Surfside Beach','SC'),'pawleys-island-litchfield':('Pawleys Island','SC'),'sunset-beach-calabash':('Sunset Beach','NC')}
def city_meta(slug,h1):
    m=re.search(r'in (.+), (SC|NC)$',h1); name,st=(m.group(1),m.group(2)) if m else (slug,'SC')
    short,st2=SHORT.get(slug,(name,st))
    title=f"Event Production & Livestreaming {short}, {st2} | Uplift AV"
    if len(title)>60: title=f"Event Production & Livestreaming {short} | Uplift AV"
    if len(title)>60: title=f"Event AV & Livestreaming {short} {st2} | Uplift AV"
    desc=f"Event production, livestreaming and IMAG in {name}, {st} for conventions, corporate events, festivals and tournaments. Flat package pricing."
    if len(desc)>158: desc=f"Event production, livestreaming and IMAG in {name}, {st}. Crew, graphics and recording included."
    return title,desc
def clean(t):
    t=re.sub(r'(https://upliftavtech\.com/)index\.html',r'\1',t)
    t=re.sub(r'(https://upliftavtech\.com/[a-z0-9-]+)\.html',r'\1',t)
    t=re.sub(r'href="index\.html(#[^"]*)?"',lambda m:'href="/'+(m.group(1) or '')+'"',t)
    t=re.sub(r'href="([a-z0-9-]+)\.html(#[^"]*)?"',lambda m:'href="/'+m.group(1)+(m.group(2) or '')+'"',t)
    return t
for f in glob.glob(os.path.join(OUT,'*.html')):
    slug=os.path.basename(f)[:-5]; t=open(f).read()
    title=desc=None
    if slug in T: title,desc=T[slug]
    elif slug.startswith('event-av-'):
        h1=re.sub('<[^>]+>','',re.search(r'<h1[^>]*>(.*?)</h1>',t,re.S).group(1)); title,desc=city_meta(slug[9:],html.unescape(h1))
    if title:
        et=html.escape(title)
        t=re.sub(r'<title>.*?</title>',f'<title>{et}</title>',t,count=1)
        t=re.sub(r'(property="og:title" content=")[^"]*',r'\g<1>'+et.replace('\\','\\\\'),t,1)
        t=re.sub(r'(name="twitter:title" content=")[^"]*',r'\g<1>'+et.replace('\\','\\\\'),t,1)
    if desc:
        ed=html.escape(desc)
        for k in ('name="description"','property="og:description"','name="twitter:description"'):
            t=re.sub(r'('+k+r' content=")[^"]*',r'\g<1>'+ed.replace('\\','\\\\'),t,1)
    if slug=='index':
        t=t.replace('<link rel="preconnect" href="https://fonts.googleapis.com">','<link rel="preload" as="image" href="images/hero-stage.jpg" fetchpriority="high">\n<link rel="preconnect" href="https://fonts.googleapis.com">',1)
    t=t.replace('"slogan":"Elevated production. Expanded reach."','"slogan":"Elevated production. Expanded reach.","priceRange":"$$$"',1)
    t=clean(t)
    open(f,'w').write(t)
sm=os.path.join(OUT,'sitemap.xml'); s=open(sm).read(); s=clean(s); s=re.sub(r'<lastmod>[^<]*</lastmod>',f'<lastmod>{TODAY}</lastmod>',s); open(sm,'w').write(s)
print('seo post ok')
