"""Photo + logo processing for 5 Star Small Engines (RGWebD). Writes assets/img/*.webp and assets/brand/*"""
from PIL import Image, ImageFilter, ImageDraw, ImageOps
from pathlib import Path
SRC=Path('/workspace/lead-kufw'); A=Path(__file__).parent/'assets'
KEEP=['g01','g03','g04','g05','g06','g07','g08','g09','g10','g12','g13','g14','g15','g16','g17','g18','g19','g21','g22','g23','g25','g26','g27','g28','g29','g30','g31','g32','g35']
def blur(im,box,r=22,feather=14):
    m=Image.new('L',im.size,0); ImageDraw.Draw(m).rounded_rectangle(box,radius=16,fill=255); m=m.filter(ImageFilter.GaussianBlur(feather))
    return Image.composite(im.filter(ImageFilter.GaussianBlur(r)),im,m)
for k in KEEP:
    im=ImageOps.exif_transpose(Image.open(SRC/'photos'/f'{k}.jpg')).convert('RGB')
    if k=='g10': im=blur(im,(1150,310,1272,405))
    for w in (800,1600):
        x=im.copy()
        if x.width>w: x=x.resize((w,round(x.height*w/x.width)),Image.LANCZOS)
        x.save(A/'img'/f'{k}-{w}.webp',quality=80,method=6)
# FB cover (their own truck + trike)
im=Image.open(SRC/'cover_fb.jpg').convert('RGB')
for w in (800,1600):
    x=im.copy()
    if x.width>w: x=x.resize((w,round(x.height*w/x.width)),Image.LANCZOS)
    x.save(A/'img'/f'cover-{w}.webp',quality=82,method=6)
# logo: circular cut-out, transparent outside the black ring
lg=Image.open(SRC/'logo_fb.jpg').convert('RGB'); W,H=lg.size
S=4; big=lg.resize((W*2,H*2),Image.LANCZOS)
cx,cy,r=448*2,448*2,431*2
m=Image.new('L',(W*2*S,H*2*S),0); ImageDraw.Draw(m).ellipse(((cx-r)*S,(cy-r)*S,(cx+r)*S,(cy+r)*S),fill=255); m=m.resize(big.size,Image.LANCZOS)
out=big.convert('RGBA'); out.putalpha(m)
bb=out.getbbox(); out=out.crop(bb)
out.save(A/'brand'/'logo-1600.png'); 
for s in (512,256,180,96,32,16):
    out.resize((s,s),Image.LANCZOS).save(A/'brand'/f'logo-{s}.png')
out.resize((640,640),Image.LANCZOS).save(A/'brand'/'logo-640.webp',quality=90)
out.resize((256,256),Image.LANCZOS).save(A/'brand'/'logo-256.webp',quality=90)
out.resize((256,256),Image.LANCZOS).save(A/'brand'/'favicon.ico',sizes=[(16,16),(32,32),(48,48)])
print('ok')
