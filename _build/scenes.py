import numpy as np, random, math
from PIL import Image, ImageDraw, ImageFilter
OUT='gen_img/'
def blank(w,h,c=(0,0,0)): return Image.new('RGB',(w,h),c)
def add(img,layer,blur=0,k=1.0):
    if blur: layer=layer.filter(ImageFilter.GaussianBlur(blur))
    a=np.asarray(img).astype(np.float32)+np.asarray(layer).astype(np.float32)*k
    return Image.fromarray(np.clip(a,0,255).astype('uint8'))
def screen_mult(img,layer):
    a=np.asarray(img).astype(np.float32)/255; b=np.asarray(layer).astype(np.float32)/255
    return Image.fromarray((255*(1-(1-a)*(1-b))).astype('uint8'))
def grad(w,h,top,bot):
    y=np.linspace(0,1,h)[:,None,None]; a=np.array(top,np.float32); b=np.array(bot,np.float32)
    return Image.fromarray(((a*(1-y)+b*y)*np.ones((h,w,3))).astype('uint8'))
def beams(img,origins,cols,alpha,spread,blur=28,width=(.02,.05),length=1.15):
    w,h=img.size
    for (ox,oy) in origins:
        L=blank(w,h); d=ImageDraw.Draw(L)
        tx=ox+random.uniform(-spread,spread)*w; wd=random.uniform(*width)*w
        c=random.choice(cols); k=alpha*random.uniform(.5,1)
        d.polygon([(ox-2,oy),(ox+2,oy),(tx+wd,h*length),(tx-wd,h*length)],fill=tuple(int(v*k) for v in c))
        img=add(img,L,blur)
    return img
def haze(img,amt=18,col=(40,34,30)):
    w,h=img.size; n=np.random.rand(h//8,w//8).astype(np.float32)
    n=np.asarray(Image.fromarray((n*255).astype('uint8')).resize((w,h),Image.BICUBIC).filter(ImageFilter.GaussianBlur(40))).astype(np.float32)/255
    L=(n[:,:,None]*np.array(col,np.float32)*amt/18).astype('uint8'); return add(img,Image.fromarray(L))
def crowd(img,y0,rows,scale,col=(6,6,8),blur=2.2,density=1.0,hands=0.0,seed=1):
    rnd=random.Random(seed); w,h=img.size; L=Image.new('L',(w,h),0); d=ImageDraw.Draw(L)
    for r in range(rows):
        t=r/max(1,rows-1); s=scale*(0.45+0.9*t); y=y0+(h-y0)*t*0.9
        x=-rnd.uniform(0,30)
        while x<w+40:
            hr=rnd.uniform(.85,1.15)*11*s; sw=hr*rnd.uniform(2.1,2.6)
            yy=y+rnd.uniform(-4,4)*s
            d.ellipse([x-hr,yy-hr*2.15,x+hr,yy-hr*.15],fill=255)
            d.rounded_rectangle([x-sw,yy-hr*.35,x+sw,h+60],radius=int(sw*.8),fill=255)
            if hands and rnd.random()<hands:
                ang=rnd.uniform(-.5,.5); ln=hr*rnd.uniform(3.2,4.4); bx=x+rnd.choice([-1,1])*sw*.6
                ex=bx+math.sin(ang)*ln; ey=yy-hr*.2-math.cos(ang)*ln
                d.line([(bx,yy-hr*.2),(ex,ey)],fill=255,width=max(2,int(hr*.55)))
                d.ellipse([ex-hr*.4,ey-hr*.5,ex+hr*.4,ey+hr*.3],fill=255)
            x+=rnd.uniform(1.7,2.5)*sw*density
    L=L.filter(ImageFilter.GaussianBlur(blur)); a=np.asarray(L).astype(np.float32)[:,:,None]/255
    base=np.asarray(img).astype(np.float32); c=np.array(col,np.float32)
    return Image.fromarray((base*(1-a)+c*a).astype('uint8'))
def glow_rect(img,box,inner,glow,gblur=60,radius=4):
    w,h=img.size; G=blank(w,h); ImageDraw.Draw(G).rectangle(box,fill=glow); img=add(img,G,gblur)
    if isinstance(inner,Image.Image):
        im=inner.resize((box[2]-box[0],box[3]-box[1])); img.paste(im,(box[0],box[1]))
    else: ImageDraw.Draw(img).rounded_rectangle(box,radius=radius,fill=inner)
    return img
def screen_content(w,h,kind,seed=0):
    rnd=random.Random(seed)
    if kind=='slide':
        im=grad(w,h,(238,233,224),(214,205,190)); d=ImageDraw.Draw(im)
        d.rectangle([int(w*.08),int(h*.30),int(w*.55),int(h*.36)],fill=(40,40,44)); d.rectangle([int(w*.08),int(h*.42),int(w*.42),int(h*.46)],fill=(120,110,98))
        d.rectangle([int(w*.08),int(h*.50),int(w*.38),int(h*.54)],fill=(120,110,98)); d.rectangle([int(w*.62),int(h*.25),int(w*.92),int(h*.75)],fill=(201,162,110))
        return im.filter(ImageFilter.GaussianBlur(1.2))
    if kind=='speaker':
        im=grad(w,h,(30,34,46),(12,13,18)); a=np.asarray(im).astype(np.float32)
        y,x=np.mgrid[0:h,0:w]; cx=w*.5
        head=((x-cx)/(h*.12))**2+((y-h*.36)/(h*.15))**2<1
        body=(((x-cx)/(h*.36))**2+((y-h*1.05)/(h*.55))**2<1)
        rim=np.clip(1-np.abs(((x-cx)/(h*.12))**2+((y-h*.36)/(h*.15))**2-1)*3,0,1)*(x>cx)
        a[body]=[44,46,58]; a[head]=[128,108,94]; a+=rim[:,:,None]*np.array([120,95,70],np.float32)*.5
        im=Image.fromarray(np.clip(a,0,255).astype('uint8')); d=ImageDraw.Draw(im)
        d.rectangle([int(w*.06),int(h*.78),int(w*.5),int(h*.9)],fill=(14,15,18)); d.rectangle([int(w*.06),int(h*.78),int(w*.075),int(h*.9)],fill=(201,162,110))
        d.rectangle([int(w*.1),int(h*.805),int(w*.34),int(h*.83)],fill=(230,230,234)); d.rectangle([int(w*.1),int(h*.85),int(w*.28),int(h*.868)],fill=(201,162,110))
        return im.filter(ImageFilter.GaussianBlur(max(1.5,w/260)))
    if kind=='led':
        y,x=np.mgrid[0:h,0:w].astype(np.float32); a=np.zeros((h,w,3),np.float32)
        base=np.exp(-((y-h*.55)/(h*.45))**2)*.55
        streak=sum(np.exp(-((y-h*p)/(h*.012))**2)*q for p,q in [(.38,.7),(.5,1),(.62,.6),(.74,.35)])
        fall=np.exp(-((x-w*.5)/(w*.6))**2)
        v=(base+streak*.9)*fall
        a=v[:,:,None]*np.array([235,170,95],np.float32)+ (1-fall)[:,:,None]*np.array([10,8,12],np.float32)
        im=Image.fromarray(np.clip(a,0,255).astype('uint8')); return im.filter(ImageFilter.GaussianBlur(3))
def bokeh(img,n,cols,rmin,rmax,ymin,ymax,alpha,blur=3,seed=0):
    rnd=random.Random(seed); w,h=img.size; L=blank(w,h); d=ImageDraw.Draw(L)
    for i in range(n):
        x=rnd.uniform(0,w); y=rnd.uniform(h*ymin,h*ymax); r=rnd.uniform(rmin,rmax); k=alpha*rnd.uniform(.35,1)
        c=rnd.choice(cols); d.ellipse([x-r,y-r,x+r,y+r],fill=tuple(int(v*k) for v in c))
    return add(img,L,blur)
def grain_vig(img,g=4,v=.5):
    w,h=img.size; y,x=np.ogrid[:h,:w]; dd=np.sqrt(((x-w/2)/(w/2))**2+((y-h/2)/(h/2))**2); m=np.clip(1-v*dd**2,.25,1)[:,:,None]
    a=np.asarray(img).astype(np.float32)*m; a+=np.random.normal(0,g,a.shape); return Image.fromarray(np.clip(a,0,255).astype('uint8'))
GOLD=(232,190,128); WARM=(255,228,190); AMBER=(255,160,70); COOL=(150,180,230); WHITE=(255,250,240)
random.seed(4); np.random.seed(4)

# 1 hero: keynote LED wall + side IMAG + crowd
W,H=1920,1080; im=grad(W,H,(4,4,6),(10,8,8))
im=beams(im,[(W*x,-20) for x in (.18,.3,.42,.58,.7,.82)],[WARM,GOLD,COOL],.22,.18,blur=34,width=(.012,.03))
im=haze(im,22)
im=glow_rect(im,(560,250,1360,700),screen_content(800,450,'led'),(110,80,45),90)
im=glow_rect(im,(150,330,500,527),screen_content(350,197,'speaker',1),(50,55,75),50)
im=glow_rect(im,(1420,330,1770,527),screen_content(350,197,'speaker',2),(50,55,75),50)
d=ImageDraw.Draw(im); d.rectangle([0,760,W,800],fill=(18,15,14)); d.rectangle([0,756,W,760],fill=(70,55,40))
im=add(im,Image.fromarray((np.zeros((H,W,3))).astype('uint8')))
im=crowd(im,800,5,2.2,blur=2.5,seed=3)
im=grain_vig(im,3.5,.45); im.save(OUT+'hero-stage.jpg',quality=84,optimize=True,progressive=True)

# 2 conference: ballroom keynote, slide screen, tables bokeh
W,H=1600,1000; im=grad(W,H,(8,8,11),(14,11,10))
im=beams(im,[(W*x,-20) for x in (.25,.5,.75)],[WARM,COOL],.14,.1,blur=40)
im=haze(im,16)
im=glow_rect(im,(420,180,1180,607),screen_content(760,427,'slide',3),(120,110,95),80)
d=ImageDraw.Draw(im); d.rectangle([0,690,W,712],fill=(20,17,15))
d.polygon([(1240,600),(1300,600),(1290,700),(1250,700)],fill=(10,9,9)); d.ellipse([1255,560,1285,592],fill=(10,9,9)); d.rectangle([1258,592,1282,640],fill=(10,9,9))
im=bokeh(im,80,[WARM,GOLD,AMBER],5,16,.72,.98,.55,blur=4,seed=5)
im=crowd(im,760,4,1.7,blur=3,seed=9)
im=grain_vig(im,3.5,.5); im.save(OUT+'conference.jpg',quality=84,optimize=True,progressive=True)

# 3 festival: big stage beams, crowd hands
W,H=1600,1000; im=grad(W,H,(3,3,6),(12,8,6))
random.seed(11); im=beams(im,[(W*x,180) for x in np.linspace(.1,.9,9)],[GOLD,AMBER,WARM,COOL],.38,.45,blur=22,width=(.01,.03))
im=beams(im,[(W*x,-40) for x in (.2,.5,.8)],[WHITE],.2,.25,blur=30)
im=haze(im,26,(50,36,26))
d=ImageDraw.Draw(im); d.rectangle([0,170,W,190],fill=(30,26,24))
for x in np.linspace(.1,.9,9): d.ellipse([W*x-10,170,W*x+10,190],fill=(255,236,200))
im=im.filter(ImageFilter.GaussianBlur(.6))
im=crowd(im,640,6,2.0,blur=2.0,hands=.18,seed=13)
im=grain_vig(im,4,.45); im.save(OUT+'festival.jpg',quality=84,optimize=True,progressive=True)

# 4 broadcast: control room multiview wall
W,H=1600,1000; im=grad(W,H,(4,5,8),(8,8,10))
tiles=[]; kinds=['speaker','led','slide','speaker','led','speaker','slide','led']
x0,y0,tw,th,gap=210,150,280,158,18
for r in range(3):
    for c in range(4):
        k=kinds[(r*4+c)%len(kinds)]; bx=x0+c*(tw+gap); by=y0+r*(th+gap)
        im=glow_rect(im,(bx,by,bx+tw,by+th),screen_content(tw,th,k,r*4+c),(30,32,40),36)
d=ImageDraw.Draw(im)
d.rectangle([x0-6,y0-6,x0+tw+6,y0+th+6],outline=(229,72,77),width=4); d.rectangle([x0+tw+gap-6,y0-6,x0+2*tw+gap+6,y0+th+6],outline=(47,163,107),width=4)
d.polygon([(0,760),(W,700),(W,H),(0,H)],fill=(14,14,16))
for i in range(28):
    bx=380+i*30; d.rounded_rectangle([bx,800,bx+20,818],radius=3,fill=(30,30,34) if i%5 else (201,162,110))
im=im.filter(ImageFilter.GaussianBlur(1.6)); im=bokeh(im,30,[GOLD,(229,72,77)],3,6,.78,.95,.6,blur=2,seed=2)
im=grain_vig(im,3.5,.5); im.save(OUT+'broadcast.jpg',quality=84,optimize=True,progressive=True)

# 5 imag: close-up big screen speaker with audience
W,H=1600,1000; im=grad(W,H,(4,4,6),(9,8,8)); im=haze(im,14)
im=glow_rect(im,(300,120,1300,682),screen_content(1000,562,'speaker',7),(60,62,80),110)
im=crowd(im,720,4,2.4,blur=3.2,seed=17)
im=grain_vig(im,3.5,.5); im.save(OUT+'imag.jpg',quality=84,optimize=True,progressive=True)

# 6 gala: warm ballroom bokeh, tables
W,H=1600,1000; im=grad(W,H,(12,9,7),(6,5,5))
im=bokeh(im,160,[GOLD,WARM,AMBER],8,40,.05,.6,.42,blur=5,seed=21)
im=bokeh(im,60,[WARM,GOLD],4,10,.55,.9,.7,blur=2,seed=22)
d=ImageDraw.Draw(im)
for (cx,cy,rw) in [(300,820,240),(800,860,280),(1300,820,240),(550,700,170),(1060,700,170)]:
    d.ellipse([cx-rw,cy-rw*.22,cx+rw,cy+rw*.22],fill=(20,16,13))
    d.ellipse([cx-rw*.9,cy-rw*.2,cx+rw*.9,cy+rw*.05],fill=(58,48,40))
im=im.filter(ImageFilter.GaussianBlur(1.2)); im=bokeh(im,30,[WARM],3,6,.65,.85,.9,blur=1,seed=23)
im=grain_vig(im,4,.5); im.save(OUT+'gala.jpg',quality=84,optimize=True,progressive=True)

# 7 beams: abstract signal lines (cta)
W,H=1600,700; im=grad(W,H,(4,4,6),(8,7,7)); L=blank(W,H); d=ImageDraw.Draw(L)
for i in range(46):
    y=H*.5+math.sin(i*.37)*120; pts=[(x, y+math.sin(x/170+i*.21)*(40+i*1.6)) for x in range(0,W+20,20)]
    k=.15+.85*(1-abs(i-23)/23); d.line(pts,fill=(int(201*k*.6),int(162*k*.6),int(110*k*.6)),width=2)
im=add(im,L,1.2); im=add(im,L,14,.8); im=grain_vig(im,3,.4); im.save(OUT+'beams.jpg',quality=84,optimize=True,progressive=True)

# 8 town hall: wide room, single speaker, two screens
W,H=1600,1000; im=grad(W,H,(7,8,11),(11,10,10)); im=beams(im,[(W*.5,-30)],[WARM],.28,.02,blur=50,width=(.06,.08)); im=haze(im,14)
im=glow_rect(im,(180,240,620,488),screen_content(440,248,'speaker',31),(60,62,80),60)
im=glow_rect(im,(980,240,1420,488),screen_content(440,248,'slide',32),(110,100,88),60)
d=ImageDraw.Draw(im); d.rectangle([0,640,W,660],fill=(22,19,17))
d.polygon([(770,560),(830,560),(820,640),(780,640)],fill=(10,9,9)); d.ellipse([786,512,814,542],fill=(10,9,9)); d.rectangle([788,540,812,580],fill=(10,9,9))
im=crowd(im,720,5,1.9,blur=2.6,seed=41)
im=grain_vig(im,3.5,.5); im.save(OUT+'town-hall.jpg',quality=84,optimize=True,progressive=True)
print('ok')
