src=open('scenes.py').read().split('# 1 hero')[0]; exec(src)
random.seed(51); np.random.seed(51)
W,H=1600,1000; im=grad(W,H,(5,6,9),(9,8,8))
im=beams(im,[(W*x,-20) for x in (.15,.32,.5,.68,.85)],[WHITE,COOL],.20,.06,blur=40,width=(.03,.05))
im=haze(im,16,(30,32,38))
# court floor in perspective
L=blank(W,H); d=ImageDraw.Draw(L)
d.polygon([(380,560),(1220,560),(1560,900),(40,900)],fill=(120,82,46))
im=add(im,L,2,.9)
d=ImageDraw.Draw(im)
d.line([(380,560),(1220,560),(1560,900),(40,900),(380,560)],fill=(200,190,170),width=3)
d.line([(800,560),(800,900)],fill=(200,190,170),width=3)
d.ellipse([700,690,900,760],outline=(200,190,170),width=3)
# center-hung scoreboard
sb=grad(420,170,(18,20,28),(10,10,14)); sd=ImageDraw.Draw(sb)
sd.rectangle([0,0,420,26],fill=(201,162,110))
for i,(x0) in enumerate((30,250)):
    for k in range(2):
        sd.rectangle([x0+k*70,50,x0+k*70+50,140],outline=(255,190,110),width=8)
sd.rectangle([196,70,224,120],fill=(229,72,77))
im=glow_rect(im,(590,90,1010,260),sb.filter(ImageFilter.GaussianBlur(1.2)),(90,70,50),70)
d=ImageDraw.Draw(im); d.line([(650,0),(650,90)],fill=(30,30,34),width=4); d.line([(950,0),(950,90)],fill=(30,30,34),width=4)
# stands crowd (lit) at left and right
im=bokeh(im,140,[WARM,COOL,GOLD],2,5,.38,.55,.5,blur=1.5,seed=52)
im=crowd(im,830,3,2.3,blur=2.8,hands=.12,seed=53)
im=grain_vig(im,3.5,.48); im.save('gen_img/arena.jpg',quality=84,optimize=True,progressive=True); print('ok')
