import glob, re, html, json, os, itertools, collections, sys
from html.parser import HTMLParser
os.chdir(sys.argv[1])
pages = sorted(glob.glob('*.html'))
noindex = {f for f in pages if 'noindex' in open(f).read()}
sitemap = set(re.findall(r'<loc>https://upliftavtech.com/([^<]*)</loc>', open('sitemap.xml').read()))

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.h=[]; s.cur=None; s.txt=''; s.text=[]; s.skip=0; s.imgs=[]; s.links=[]; s.in_main=0
    def handle_starttag(s,t,a):
        a=dict(a)
        if t in ('script','style','nav','footer','header'): s.skip+=1
        if t=='main': s.in_main+=1
        if re.fullmatch(r'h[1-6]',t): s.cur=int(t[1]); s.txt=''
        if t=='img': s.imgs.append(a)
        if t=='a' and 'href' in a: s.links.append((a['href'], s.in_main and not s.skip))
    def handle_endtag(s,t):
        if t in ('script','style','nav','footer','header'): s.skip-=1
        if t=='main': s.in_main-=1
        if s.cur and t==f'h{s.cur}': s.h.append((s.cur,' '.join(s.txt.split()))); s.cur=None
    def handle_data(s,d):
        if s.cur: s.txt+=d
        if not s.skip and s.in_main: s.text.append(d)

R={}
for f in pages:
    t=open(f).read(); p=P(); p.feed(t)
    slug=f[:-5]
    R[slug]=dict(
        title=html.unescape(re.search(r'<title>(.*?)</title>',t).group(1)),
        desc=html.unescape(re.search(r'name="description" content="([^"]*)',t).group(1)),
        canon=(re.search(r'rel="canonical" href="([^"]+)"',t) or [None,'(none)'])[1],
        robots=re.search(r'name="robots" content="([^"]+)"',t).group(1),
        h=p.h, imgs=p.imgs, links=p.links,
        words=' '.join(' '.join(p.text).split()),
        ld=[json.loads(m) for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)],
        crumbs_visible='class="crumbs"' in t,
        bgimgs=re.findall(r'background-image:url\(([^)]+)\)',t),
    )
issues=collections.defaultdict(list)
def add(k,v): issues[k].append(v)
idx=[s for s in R if s+'.html' not in noindex]
# 2 breadcrumbs + canonical
for s,d in R.items():
    want='https://upliftavtech.com/'+('' if s=='index' else s)
    if d['canon']!=want and not (s=='404' and d['canon']=='(none)'): add('2 canonical mismatch',(s,d['canon']))
    types=[x.get('@type') for x in d['ld']]
    if s not in('index','404','thanks') and 'BreadcrumbList' not in types: add('2 no BreadcrumbList schema',s)
    if s not in('index','404','thanks') and not d['crumbs_visible']: add('2 no visible breadcrumbs',s)
    for x in d['ld']:
        if x.get('@type')=='BreadcrumbList':
            for it in x['itemListElement']:
                if it['item'].endswith('.html'): add('2 breadcrumb schema uses .html URL',(s,it['item']))
# 3 orphans
inb=collections.Counter()
for s,d in R.items():
    for h,_ in d['links']:
        m=re.match(r'^/([a-z0-9-]*)(#.*)?$',h)
        if m: inb[m.group(1) or 'index']+= (m.group(1) or 'index')!=s
for s in idx:
    if inb[s]==0: add('3 orphan',s)
# 4 headings + duplicates
for s,d in R.items():
    h1=[t for l,t in d['h'] if l==1]
    if len(h1)!=1: add('4 h1 count',(s,len(h1)))
    if sum(1 for l,_ in d['h'] if l==2)==0: add('4 no H2',s)
    prev=0
    for l,t in d['h']:
        if prev and l>prev+1: add('4 heading skip',(s,prev,l,t))
        prev=l
def sh(t,k=6):
    w=re.findall(r'[a-z0-9]+',t.lower()); return {' '.join(w[i:i+k]) for i in range(len(w)-k)}
SH={s:sh(R[s]['words']) for s in idx}
sims=[]
for a,b in itertools.combinations(idx,2):
    A,B=SH[a],SH[b]
    if A and B:
        j=len(A&B)/len(A|B); sims.append((round(j,2),a,b))
sims.sort(reverse=True)
for j,a,b in sims[:8]:
    if j>0.25: add('4 near-duplicate content (6-word shingle Jaccard)',(j,a,b))
for s in idx:
    n=len(R[s]['words'].split())
    if n<300: add('4 thin main content (<300 words)',(s,n))
# 5 links
for s,d in R.items():
    for h,_ in d['links']:
        if h.startswith(('mailto:','tel:','http')): continue
        m=re.match(r'^/?([a-z0-9-]*)(#([a-z0-9-]+))?$',h)
        if not m: add('5 odd href',(s,h)); continue
        tgt=(m.group(1) or 'index')
        if tgt not in R: add('5 broken internal link',(s,h))
        elif m.group(3) and f'id="{m.group(3)}"' not in open(tgt+'.html').read(): add('5 broken anchor',(s,h))
    for h,_ in d['links']:
        if h.startswith('http') and 'upliftavtech.com' not in h: add('5 external link',(s,h))
# 6 cannibalization: titles sharing primary phrase
def core(t): return re.sub(r'\s*\|.*$','',t).lower()
titles={s:core(R[s]['title']) for s in idx}
for a,b in itertools.combinations(idx,2):
    A=set(re.findall(r'[a-z]+',titles[a]))-{'in','and','the','for','myrtle','beach','sc','uplift','av','event','events','of','with','a'}
    B=set(re.findall(r'[a-z]+',titles[b]))-{'in','and','the','for','myrtle','beach','sc','uplift','av','event','events','of','with','a'}
    if A and B and len(A&B)/len(A|B)>=0.6: add('6 possible cannibalization (title overlap)',(a,b,titles[a],titles[b]))
# 8/9 titles + desc
tl=collections.Counter(R[s]['title'] for s in idx); dl=collections.Counter(R[s]['desc'] for s in idx)
for s in idx:
    T=R[s]['title']; D=R[s]['desc']
    if not 50<=len(T)<=60: add('8 title length outside 50-60',(s,len(T),T))
    if tl[T]>1: add('8 duplicate title',(s,T))
    if not 120<=len(D)<=160: add('9 description length outside 120-160',(s,len(D)))
    if dl[D]>1: add('9 duplicate description',(s,))
# 10 images
for s,d in R.items():
    for im in d['imgs']:
        if 'alt' not in im: add('10 img missing alt',(s,im.get('src')))
        if not (im.get('width') and im.get('height')): add('10 img missing width/height',(s,im.get('src')))
        if im.get('src','').endswith(('.png','.jpg')): add('10 img not webp',(s,im.get('src')))
    for b in d['bgimgs']:
        if b.endswith('.jpg'): add('10 bg image not webp',(s,b))
# sitemap
for s in idx:
    key='' if s=='index' else s
    if key not in sitemap: add('sitemap missing indexable page',s)
for u in sitemap:
    if (u or 'index')+'.html' in noindex: add('sitemap includes noindex',u)
print(json.dumps({k:v for k,v in issues.items()},indent=1,default=str))
print('TOP SIMILARITY',sims[:6])
print('PAGES',len(pages),'indexable',len(idx),'sitemap',len(sitemap))
print('WORDS',sorted((len(R[s]['words'].split()),s) for s in idx)[:6])
