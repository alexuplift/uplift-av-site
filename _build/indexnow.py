# Ping IndexNow (Bing, Yahoo, DuckDuckGo, Yandex) with every URL in the live sitemap.
import json, re, sys, urllib.request
KEY='ff200833b5fe2f462357c4ec247a59fe'; HOST='upliftavtech.com'
urls=sys.argv[1:] or re.findall(r'<loc>([^<]+)</loc>', open('/home/claude/uplift-av-site/sitemap.xml').read())
body=json.dumps({"host":HOST,"key":KEY,"keyLocation":f"https://{HOST}/{KEY}.txt","urlList":urls}).encode()
req=urllib.request.Request('https://api.indexnow.org/indexnow',data=body,headers={'Content-Type':'application/json; charset=utf-8'})
try:
    r=urllib.request.urlopen(req,timeout=20); print(r.status, len(urls),'urls')
except urllib.error.HTTPError as e: print(e.code, e.read()[:300])
