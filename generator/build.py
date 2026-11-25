#!/usr/bin/env python3
"""Generator for the 5 Star Small Engines demo site (RGWebD). Writes /workspace/fivestar/site.
Facts come from /workspace/lead-kufw/notes.md (Google Maps listing, Facebook page, GreenPal listing)."""
import json, shutil, html, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
GEN=Path(__file__).parent; OUT=Path('/workspace/fivestar/site')
REPO='5starsmallengines'; BASE=f'https://rgwebd.github.io/{REPO}/'
NAME='5 Star Small Engines'
PHONE='(478) 808-3415'; TEL='tel:+14788083415'; EMAIL='for5star@gmail.com'
ADDR='8094 Eisenhower Pkwy, Lizella, GA 31052'
FB='https://www.facebook.com/5StarSmallEngines'
GMAPS='https://maps.google.com/?cid=8058230847359779966'
GREV='https://maps.app.goo.gl/KufWtvhDoCWq91qb7'
DIR='https://www.google.com/maps/dir/?api=1&destination=5+Star+Small+Engines%2C+8094+Eisenhower+Pkwy%2C+Lizella%2C+GA+31052'
MAPEMBED='https://www.google.com/maps?q=5+Star+Small+Engines,+8094+Eisenhower+Pkwy,+Lizella,+GA+31052&z=14&output=embed'
RATING=4.9; COUNT=169
e=html.escape

# ---------------- assets ----------------
OUT.mkdir(parents=True,exist_ok=True)
for p in OUT.iterdir():
    if p.name in ('.git',): continue
    shutil.rmtree(p) if p.is_dir() else p.unlink()
A=OUT/'assets'; shutil.copytree(GEN/'assets'/'img',A/'img'); (A/'brand').mkdir()
for f in ['logo-640.webp','logo-256.webp','logo-512.png','logo-32.png']: shutil.copy(GEN/'assets/brand'/f,A/'brand'/f)
shutil.copy(GEN/'assets/brand/favicon.ico',OUT/'favicon.ico'); shutil.copy(GEN/'assets/brand/logo-180.png',OUT/'apple-touch-icon.png')
shutil.copy(GEN/'src/styles.css',A/'styles.css'); shutil.copy(GEN/'src/script.js',A/'script.js')
# keep the generator code in the repo (no images) so the site can be rebuilt
G=OUT/'generator'; G.mkdir(); (G/'src').mkdir()
for f in ['build.py','process.py','qa.py','shots.py']:
    if (GEN/f).exists(): shutil.copy(GEN/f,G/f)
for f in ['styles.css','script.js']: shutil.copy(GEN/'src'/f,G/'src'/f)
# OG image: hero photo + logo
og=Image.open(GEN/'assets/img/g05-1600.webp').convert('RGB').resize((1200,900)).crop((0,140,1200,770))
dk=Image.new('RGB',og.size,(6,7,9)); m=Image.linear_gradient('L').rotate(90).resize(og.size)
og=Image.composite(og,dk,m.point(lambda v:int(60+v*.7)))
lg=Image.open(GEN/'assets/brand/logo-1600.png').convert('RGBA').resize((420,420),Image.LANCZOS)
og=og.convert('RGBA'); og.alpha_composite(lg,(60,105)); og.convert('RGB').save(A/'og-image.jpg',quality=86)

def dims(n,w=1600): return Image.open(A/'img'/f'{n}-{w}.webp').size
def pic(n,alt,cls='',sizes='(max-width:900px) 100vw, 50vw',eager=False,attrs=''):
    w,h=dims(n); w8,_=dims(n,800)
    ld='fetchpriority="high"' if eager else 'loading="lazy"'
    return (f'<img src="assets/img/{n}-1600.webp" srcset="assets/img/{n}-800.webp {w8}w, assets/img/{n}-1600.webp {w}w" sizes="{sizes}" '
            f'width="{w}" height="{h}" alt="{e(alt)}" {ld} decoding="async"{(" class=\""+cls+"\"") if cls else ""} {attrs}>')

PH={ # checked by eye, one by one
'g01':'Blue Yamaha quads lined up in the 5 Star showroom','g03':'The Dynojet Model 200i dyno cell with its tuning screen and cooling fans',
'g04':'Engine cases split open with the crank and transmission gears exposed','g05':'A tech strapping a red and white quad onto the 5 Star branded dyno',
'g06':'Yellow and blue Suzuki sport quad on the shop floor','g07':'Red and white Yamaha Raptor up on a lift',
'g08':'Cylinder, gasket kit and performance parts laid out on the bench','g09':'The 5 Star Small Engines storefront on Eisenhower Pkwy, signed ATV · Motorcycle · Jet Ski',
'g10':'Red sport bike on paddock stands in the service bay','g12':'A freshly polished carburetor held up in front of the 5 Star tool wall',
'g13':'A Yamaha engine on the bench under the 5 Star tool wall','g14':'Wide view of the showroom floor packed with quads and side-by-sides',
'g15':'Custom golf cart with zebra-print bodywork and lifted off-road tires','g16':'Red custom drag trike with racing slicks',
'g17':'Low-angle shot of a red custom sport quad','g18':'The parts counter and showroom with a quad out front',
'g19':'Custom long-travel trike build with bright wraps in the shop','g21':'A quad’s rear tire spinning on the dyno drum',
'g22':'Crankshaft and gear set inside split engine cases','g23':'Blue Yamaha race quad strapped down on the Dynojet dyno',
'g25':'Three sport quads on the showroom floor by the parts counter','g26':'A 5 Star tech working on a Yamaha quad on the lift',
'g27':'Ported cylinder head, valves and throttle body on the bench','g28':'Yamaha quad stripped down for engine and electrical work',
'g29':'Red custom trike with spoke wheels and drag slicks','g30':'Carburetor with a polished velocity stack on an orange pit bike',
'g31':'Two-stroke engine with new pistons ready for assembly','g32':'Quad frame with the engine and exhaust routing exposed',
'g35':'Dial indicators measuring a machined cylinder head','cover':'A custom green drag trike in front of the 5 Star shop truck',
}

IC={ # inline icons
'phone':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1 1 .4 1.9.7 2.8a2 2 0 0 1-.5 2.1L8 9.9a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.8.7a2 2 0 0 1 1.7 2z"/></svg>',
'arrow':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>',
'left':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M15 6l-6 6 6 6"/></svg>',
'right':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M9 6l6 6-6 6"/></svg>',
'x':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>',
'pin':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 0 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.6"/></svg>',
'gauge':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 17a8 8 0 1 1 16 0"/><path d="M12 17l4-5"/></svg>',
'wrench':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/></svg>',
'chat':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12a8 8 0 0 1-11.8 7L3 21l2-6.2A8 8 0 1 1 21 12z"/></svg>',
'road':'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M8 3L4 21M16 3l4 18M12 4v3M12 11v3M12 18v2"/></svg>',
'g':'<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="#4285F4" d="M22.5 12.3c0-.8-.1-1.5-.2-2.2H12v4.2h5.9a5 5 0 0 1-2.2 3.3v2.7h3.5c2.1-1.9 3.3-4.7 3.3-8z"/><path fill="#34A853" d="M12 23c3 0 5.5-1 7.3-2.7l-3.5-2.7c-1 .7-2.3 1.1-3.8 1.1-2.9 0-5.4-2-6.3-4.7H2.1v2.8A11 11 0 0 0 12 23z"/><path fill="#FBBC05" d="M5.7 14a6.6 6.6 0 0 1 0-4.2V7H2.1a11 11 0 0 0 0 9.9z"/><path fill="#EA4335" d="M12 5.4c1.6 0 3.1.6 4.3 1.7l3.1-3.1A11 11 0 0 0 2.1 7l3.6 2.8C6.6 7.3 9.1 5.4 12 5.4z"/></svg>',
}
def btn_call(cls='',lbl=None): return f'<a class="btn mag {cls}" href="{TEL}">{IC["phone"]}<span>{lbl or "Call "+PHONE}</span></a>'
def stars(r,cls=''): return f'<span class="stars5 {cls}" role="img" aria-label="{r} out of 5 stars"><i style="--w:{r/5*100:.1f}%"></i></span>'

# ---------------- reviews (Google, 5★, word for word) ----------------
REV={
'morgan':('Morgan Moss','3 weeks ago','Mitch and his team are awesome, they do not cut corners and they get it done right the first time. 5star is the ONLY place to take your toys for maintenance or fixing or upgrades. I drive 4 hours to take my stuff to them because they do such a great job! Have been a customer for 4 years and will be for life!'),
'corey':('Corey Turner','3 weeks ago','Hands down greatest shop with zero complaints. Customer service was great throughout the diagnosis, and even took the time to help me with understanding preventative maintenance I can do to stop future problems. Very knowledgeable and no complaints on my end.  Happy to be a repeat customer in the future.'),
'trsvis':('Trsvis Ward','3 weeks ago','I have nothing but great things to say about these guys ive been dumping money into my bike time after time only to be disappointed but I finally found someone that can work on carburetor\'s and tune is perfect i appreciate the great work Mitch and his team......'),
'dominque':('Dominque Riley','4 months ago','Mitch went above and beyond and I really appreciate him.  I took my LTR450 in to be dyno tuned today. It was a 3 hr drive and well worth it.  Even when he wasn\'t able to tune it because the bike had a problem i was unfamiliar with; he fixed the problem and then clean her up and she is riding wonderfully. Very  knowledgeable and helpful!!'),
'rayy':('Rayy Boatwright','4 months ago','Mitch & his team are the guys you want to go to for all of your atv work! They are well advanced in other areas also but if you’re looking for a trusted shop to take your machine to I highly recommend checking these guys out.!!'),
'brandon':('Brandon Alexander','3 weeks ago','Took my TRX450ER to Byron Powersports and got the run around for months. Part swap after part swap with no results.  Finally got tired of it and took it to Mitch at 5 Star. He had it repaired in short order, honestly and transparent.  Highly recommend.'),
'brenton':('Brenton field','9 months ago','Guys got me in quick. 3 employees knocked out raptor.  Pipe / power commander / dyno all within couple hours.  They know their stuff. Finding a good clean shop is very hard to find.  These guys are your answer'),
'angie':('Angie Tolbert','2 weeks ago','5 Star has repaired and serviced multiple things for us,  4 wheeler,  golf  cart and jet ski and always do a great job.  I\'ve also referred friends and family who have used others and needed to find a better service and they\'re so thankful I got them to Mitch and 5Star, they always do it right the first time😁 …'),
}
def rtext(k): return e(' '.join(REV[k][2].split()))  # collapse double spaces only

# ---------------- svg builders ----------------
def tach(cls='tach',lab='RPM ×1000',redfrom=11):
    """Tachometer 0–13 across -120..120 degrees. Needle is .ndl"""
    cx=cy=150; R=122; s=[f'<svg class="{cls}" viewBox="0 0 300 300" aria-hidden="true">',
       '<defs><radialGradient id="tface" cx="50%" cy="45%"><stop offset="0" stop-color="#1e2127"/><stop offset="1" stop-color="#07080a"/></radialGradient></defs>',
       f'<circle cx="150" cy="150" r="146" fill="url(#tface)" stroke="#3a3f47" stroke-width="3"/><circle cx="150" cy="150" r="138" fill="none" stroke="#c9ced6" stroke-opacity=".25" stroke-width="1"/>']
    def pt(a,r): a=math.radians(a-90); return cx+r*math.cos(a), cy+r*math.sin(a)
    a0=-120+240*redfrom/13; x1,y1=pt(a0,R); x2,y2=pt(120,R)
    s.append(f'<path d="M{x1:.1f} {y1:.1f} A{R} {R} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="#e3141f" stroke-width="10"/>')
    for i in range(0,131):
        v=i/10; a=-120+240*v/13
        if i%10==0: L,w=16,3
        elif i%5==0: L,w=10,2
        else: continue
        xa,ya=pt(a,R-2); xb,yb=pt(a,R-2-L)
        col='#ff2b36' if v>=redfrom else '#d9dde3'
        s.append(f'<line x1="{xa:.1f}" y1="{ya:.1f}" x2="{xb:.1f}" y2="{yb:.1f}" stroke="{col}" stroke-width="{w}"/>')
        if i%10==0:
            xt,yt=pt(a,R-36); s.append(f'<text x="{xt:.1f}" y="{yt+5:.1f}" text-anchor="middle"{" style=\"fill:#ff2b36\"" if v>=redfrom else ""}>{int(v)}</text>')
    s.append(f'<text x="150" y="208" text-anchor="middle" style="font-size:11px;letter-spacing:3px;fill:#8c939d">{lab}</text>')
    s.append('<g class="ndl"><path d="M147 160 L150 40 L153 160 Z" fill="#ff2b36"/><circle cx="150" cy="150" r="14" fill="#16181c" stroke="#c9ced6" stroke-width="2"/><circle cx="150" cy="150" r="4" fill="#ff2b36"/></g></svg>')
    return ''.join(s)

def gauge(val,maxv,dec,lab,src,unit=''):
    frac=min(1,val/maxv); R=90; L=R*math.radians(240)
    def pt(a,r): a=math.radians(a-90); return 110+r*math.cos(a), 110+r*math.sin(a)
    x1,y1=pt(-120,R); x2,y2=pt(120,R)
    arc=f'M{x1:.1f} {y1:.1f} A{R} {R} 0 1 1 {x2:.1f} {y2:.1f}'
    ticks=''.join(f'<line class="tick" x1="{pt(a,R-16)[0]:.1f}" y1="{pt(a,R-16)[1]:.1f}" x2="{pt(a,R-24)[0]:.1f}" y2="{pt(a,R-24)[1]:.1f}"/>' for a in range(-120,121,24))
    deg=-120+240*frac
    disp=f'{val:.{dec}f}'
    return (f'<div class="gauge" data-r><svg viewBox="0 0 220 190" aria-hidden="true"><path class="trk" d="{arc}"/>'
            f'<path class="val" d="{arc}" stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}" data-len="{L:.1f}" data-frac="{frac:.4f}"/>{ticks}'
            f'<g class="ndl" data-deg="{deg:.1f}" style="transform:rotate(-120deg)"><path d="M108 110 L110 34 L112 110Z" fill="#fff"/><circle cx="110" cy="110" r="8" fill="#e3141f"/></g></svg>'
            f'<div class="read" data-count="{val}" data-dec="{dec}"><b>{disp}</b>{f"<small>{unit}</small>" if unit else ""}</div>'
            f'<div class="lab">{lab}</div><div class="src">{src}</div></div>')
GDEF='<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs><linearGradient id="gred" x1="0" x2="1"><stop offset="0" stop-color="#9c0a12"/><stop offset="1" stop-color="#ff2b36"/></linearGradient></defs></svg>'

# ---------------- page shell ----------------
NAVL=[('index.html','Home'),('services.html','Services'),('dyno.html','Dyno Tuning'),('shop.html','The Shop'),('reviews.html','Reviews'),('visit.html','Visit')]
HOURS=[(2,'Tuesday','9 AM – 6 PM'),(3,'Wednesday','9 AM – 6 PM'),(4,'Thursday','9 AM – 6 PM'),(5,'Friday','9 AM – 6 PM'),(6,'Saturday','9 AM – 2 PM'),(0,'Sunday','Closed'),(1,'Monday','Closed')]
def hours_tbl(cls='hours'):
    return f'<table class="{cls}"><caption class="sr" style="position:absolute;left:-9999px">Business hours</caption><tbody>'+''.join(f'<tr data-d="{d}"{" class=off" if h=="Closed" else ""}><td>{n}</td><td>{h}</td></tr>' for d,n,h in HOURS)+'</tbody></table>'
def header(cur):
    nav=''.join(f'<a href="{f}"{" aria-current=page" if f==cur else ""}>{t}</a>' for f,t in NAVL)
    mnav=''.join(f'<a class="l" href="{f}"{" aria-current=page" if f==cur else ""}>{t}</a>' for f,t in NAVL)
    return f'''<a class="skip" href="#main">Skip to content</a><div class="progress" aria-hidden="true"></div>
<header class="hdr"><div class="wrap"><a class="brand" href="index.html" aria-label="{NAME} home"><img src="assets/brand/logo-256.webp" width="256" height="256" alt="{NAME} logo"><b>5 Star<small>Small Engines</small></b></a>
<nav class="nav" aria-label="Main">{nav}</nav><a class="btn hcall mag" href="{TEL}">{IC["phone"]}<span>{PHONE}</span></a>
<button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="mnav"><span></span></button></div></header>
<nav class="mnav" id="mnav" aria-label="Mobile">{mnav}<div class="ctas">{btn_call()}<a class="btn ghost" href="{DIR}" target="_blank" rel="noopener">{IC["pin"]}<span>Directions</span></a></div></nav>'''
def footer():
    pages=''.join(f'<li><a href="{f}">{t}</a></li>' for f,t in NAVL)
    hrs=''.join(f'<tr><td>{n[:3]}</td><td>{h}</td></tr>' for d,n,h in HOURS)
    return f'''<footer class="ftr"><div class="wrap"><div class="grid">
<div><img class="logo" src="assets/brand/logo-256.webp" width="256" height="256" alt="{NAME} logo" loading="lazy"><p><b style="color:#fff">{NAME}</b><br>ATV, motorcycle, side-by-side, jet ski, golf cart and small-engine repair, service and dyno tuning in Lizella, near Macon, Georgia.</p></div>
<div><h4>Pages</h4><ul>{pages}</ul></div>
<div><h4>Contact</h4><ul><li><a href="{DIR}" target="_blank" rel="noopener">8094 Eisenhower Pkwy<br>Lizella, GA 31052</a></li><li><a href="{TEL}">{PHONE}</a></li><li><a href="mailto:{EMAIL}">{EMAIL}</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{GMAPS}" target="_blank" rel="noopener">Google</a></li></ul></div>
<div><h4>Hours</h4><table class="hrs"><tbody>{hrs}</tbody></table></div>
</div><div class="legal"><span>© 2026 {NAME}. All rights reserved.</span><span>Design preview by <a href="https://rgwebd.github.io/" style="color:#fff">RGWebD</a></span></div></div></footer>
<div class="mbar">{btn_call("","Call")}<a class="btn ghost" href="{DIR}" target="_blank" rel="noopener">{IC["pin"]}<span>Directions</span></a></div>
<div class="demo" role="note">Design preview by&nbsp;<a href="https://rgwebd.github.io/">RGWebD</a><button type="button" aria-label="Dismiss design preview note">×</button></div>'''

def phero(cur,kicker,h1,lead,bg,frame,ctas=None):
    crumb=dict(NAVL)[cur]
    return f'''<section class="phero"><div class="bg" data-px=".18">{pic(bg,PH[bg],sizes="100vw",eager=True,attrs='aria-hidden="true"').replace(f'alt="{e(PH[bg])}"','alt=""')}</div>
<div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span aria-hidden="true">/</span><span aria-current="page">{crumb}</span></nav>
<p class="kicker">{kicker}</p><h1><span class="slant">{h1}</span></h1><p class="lead">{lead}</p><div class="ctas" style="margin-top:26px">{ctas or btn_call()}</div></div>
<div class="frame">{pic(frame,PH[frame],sizes="(max-width:980px) 100vw, 460px",eager=True)}</div></section>'''

def cta_band(h,p,img=None,giant='Full throttle'):
    bgx=f'<div class="bg">{pic(img,"",sizes="100vw").replace("alt=\"\"","alt=\"\" aria-hidden=\"true\"")}</div>' if img else f'<div class="giant" aria-hidden="true">{giant}</div>'
    return f'''<section class="cta{"" if img else " graphic"}">{bgx}<div class="wrap" data-r><p class="kicker" style="justify-content:center">Lizella · Macon area</p><h2><span class="slant">{h}</span></h2><p class="lead" style="margin:0 auto">{p}</p>
<div class="ctas">{btn_call("xl")}<a class="btn ghost xl" href="visit.html#request"><span>Send a service request</span>{IC["arrow"]}</a></div></div></section>'''

def biz(extra=None):
    d={"@context":"https://schema.org","@type":["MotorcycleRepair","AutoRepair"],"@id":BASE+"#business","name":NAME,"url":BASE,
       "image":[BASE+"assets/img/g05-1600.webp",BASE+"assets/img/g09-1600.webp"],"logo":BASE+"assets/brand/logo-512.png",
       "description":"ATV, motorcycle, side-by-side, jet ski, golf cart, mower and handheld small-engine repair shop in Lizella, GA near Macon, with an in-house dyno for tuning.",
       "telephone":"+1-478-808-3415","email":EMAIL,
       "address":{"@type":"PostalAddress","streetAddress":"8094 Eisenhower Pkwy","addressLocality":"Lizella","addressRegion":"GA","postalCode":"31052","addressCountry":"US"},
       "geo":{"@type":"GeoCoordinates","latitude":32.8052674,"longitude":-83.8162097},"hasMap":GMAPS,
       "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"18:00"},
                                    {"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"09:00","closes":"14:00"}],
       "sameAs":[FB,GMAPS],"paymentAccepted":"Credit card, debit card, NFC mobile payments",
       "areaServed":[{"@type":"City","name":"Lizella, GA"},{"@type":"City","name":"Macon, GA"}],
       "amenityFeature":[{"@type":"LocationFeatureSpecification","name":"Wheelchair-accessible entrance","value":True},{"@type":"LocationFeatureSpecification","name":"Wheelchair-accessible parking","value":True},{"@type":"LocationFeatureSpecification","name":"Restroom","value":True}],
       "aggregateRating":{"@type":"AggregateRating","ratingValue":RATING,"reviewCount":COUNT,"bestRating":5,"worstRating":1},
       "knowsAbout":["ATV repair","Motorcycle repair","Dyno tuning","Carburetor rebuilds","Engine rebuilds","Fuel programmer installs","Exhaust installs","Jet ski repair","Golf cart repair","Small engine repair"]}
    if extra: d.update(extra)
    return d
def reviews_ld(keys):
    return {"review":[{"@type":"Review","author":{"@type":"Person","name":REV[k][0]},"reviewRating":{"@type":"Rating","ratingValue":5,"bestRating":5},"reviewBody":' '.join(REV[k][2].split()),"publisher":{"@type":"Organization","name":"Google"}} for k in keys]}
def crumbs_ld(name,f):
    it=[{"@type":"ListItem","position":1,"name":"Home","item":BASE}]
    if f!='index.html': it.append({"@type":"ListItem","position":2,"name":name,"item":BASE+f})
    return {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":it}

def page(f,title,desc,body,ld,home=False):
    url=BASE+('' if f=='index.html' else f)
    lds=''.join(f'<script type="application/ld+json">{json.dumps(x,ensure_ascii=False)}</script>' for x in ld)
    loader=f'''<div class="loader" aria-hidden="true"><div>{tach("tach",lab="RPM ×1000")}<div class="stars"><i></i><i></i><i></i><i></i><i></i></div><p>Warming up</p></div></div>''' if home else ''
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}"><meta name="robots" content="index,follow">
<meta name="theme-color" content="#08090b"><link rel="icon" href="favicon.ico" sizes="any"><link rel="icon" type="image/png" sizes="32x32" href="assets/brand/logo-32.png"><link rel="apple-touch-icon" href="apple-touch-icon.png">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}assets/og-image.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:locale" content="en_US">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}assets/og-image.jpg">
<meta name="geo.region" content="US-GA"><meta name="geo.placename" content="Lizella"><meta name="geo.position" content="32.8052674;-83.8162097">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=Inter:wght@400;500;600&family=Saira+Condensed:wght@600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/styles.css">{lds}</head><body>{loader}{GDEF}{header(f)}<main id="main">{body}</main>{footer()}<script src="assets/script.js" defer></script></body></html>'''

# ================= HOME =================
SV=[ # id, title, short, photo (home card)
('rebuilds','Engine rebuilds','Top ends, bottom ends and full overhauls, measured and built right the first time.','g13'),
('carbs','Carburetor work','Rebuilds, cleaning and jetting for bikes, quads and small engines that won’t idle or pull clean.','g12'),
('tune-ups','Tune-ups & service','Oil, filters, plugs and the preventative maintenance that keeps your machine out of the shop.','g07'),
('diagnosis','Electrical & bog diagnosis','Intermittent bogs, no-starts and electrical gremlins tracked down instead of parts-swapped.','g28'),
('dyno','In-house dyno tuning','A Dynojet dyno right in the shop. Riders tow in from hours away to get dialed in.','g23'),
('performance','Programmers & exhaust','Fuel programmer installs, pipes and the dyno time to make the combo actually work.','g08'),
]
cards=''.join(f'''<a class="scard" href="{"dyno.html" if i=="dyno" else "services.html#"+i}" data-r><div class="ph">{pic(img,PH[img],sizes="(max-width:620px) 100vw, (max-width:980px) 50vw, 33vw")}</div><span class="go">{IC["arrow"]}</span>
<div class="tx"><span class="num">0{n+1} /</span><h3>{t}</h3><p>{s}</p></div></a>''' for n,(i,t,s,img) in enumerate(SV))
MACH=['ATVs & Quads','Motorcycles','Side-by-sides','Jet Skis','Golf Carts','Mowers','Handhelds','Dyno Tuning']
marq=''.join(f'<span>{m}</span>' for m in MACH)
home_rev=['morgan','dominque','corey','brenton','rayy']
slides=''.join(f'''<div class="rslide"><blockquote>{stars(5)}<p style="margin-top:16px">“{rtext(k)}”</p><footer><span class="av" aria-hidden="true">{REV[k][0][0]}</span><span>{e(REV[k][0])} · Google review · {REV[k][1]}</span></footer></blockquote></div>''' for k in home_rev)
home=f'''<section class="hero"><div class="bg">{pic("g05",PH["g05"],sizes="100vw",eager=True)}</div><div class="streaks" aria-hidden="true"><i></i><i></i><i></i></div>
<div class="outline" aria-hidden="true">5 Star</div>
<div class="wrap"><div class="trust fade"><span class="g">{IC["g"]}<b>{RATING}</b>{stars(RATING)}</span><span class="sep"></span><span>{COUNT} Google reviews</span><span class="sep"></span><span class="status" data-status><span>Checking hours…</span></span></div>
<h1><span class="ln"><span>Fixed right.</span></span><span class="ln"><span class="chrome">Tuned on</span></span><span class="ln"><span class="red">the dyno.</span></span></h1>
<p class="lead fade">ATV, motorcycle, side-by-side, jet ski, golf cart and small-engine repair in Lizella, just outside Macon. Rebuilds, carb work, diagnostics and in-house dyno tuning that riders drive hours for.</p>
<div class="ctas fade" style="margin-top:28px">{btn_call("xl")}<a class="btn ghost xl mag" href="dyno.html"><span>Dyno tuning</span>{IC["arrow"]}</a></div></div>
<div class="scrollcue" aria-hidden="true">Scroll</div></section>
<div class="marq" aria-hidden="true"><div class="track">{marq}{marq}</div></div>
<section class="sec"><div class="wrap"><div class="shead"><div><p class="kicker">What we do</p><h2><span class="slant">Every job, <span class="red">done right</span></span></h2></div><p>From a carb that won’t idle to a full engine build and a dyno-tuned finish, the whole job happens under one roof on Eisenhower Pkwy.</p></div>
<div class="scards">{cards}</div><p style="margin-top:30px"><a class="btn ghost mag" href="services.html"><span>All services</span>{IC["arrow"]}</a></p></div></section>
<section class="sec carbon" style="padding-block:clamp(70px,8vw,110px)"><div class="wrap"><div class="shead"><div><p class="kicker">By the numbers</p><h2><span class="slant">The <span class="chrome">readout</span></span></h2></div><p>Straight from their Google Business Profile and their customers’ own reviews.</p></div>
<div class="gauges">{gauge(4.9,5,1,"Google rating","Out of 5 stars")}{gauge(169,200,0,"Google reviews","And counting")}{gauge(161,169,0,"Five-star reviews","Of 169 on Google")}{gauge(4,5,0,"Hours some riders drive","To get here, per reviews","hrs")}</div></div></section>
<section class="sec"><div class="wrap split"><div class="collage" data-r="left"><div class="pframe a">{pic("g14",PH["g14"])}</div><div class="pframe b">{pic("g18",PH["g18"],sizes="(max-width:900px) 50vw, 25vw")}</div>
<svg class="stamp" viewBox="0 0 150 150" aria-hidden="true"><defs><path id="circ" d="M75 75 m-58 0 a58 58 0 1 1 116 0 a58 58 0 1 1 -116 0"/></defs><circle cx="75" cy="75" r="74" fill="#e3141f"/><text><textPath href="#circ">Service · Parts · Sales · Lizella GA · </textPath></text></svg></div>
<div data-r="right"><p class="kicker">Why riders come here</p><h2><span class="slant">Worth the <span class="red">drive</span></span></h2><p class="lead">The reviews say it again and again: Mitch and the crew fix it right the first time, explain what they find and get you back out riding.</p>
<ul class="points"><li><span class="ic">{IC["wrench"]}</span><div><b>Right the first time</b><span>“They do not cut corners and they get it done right the first time.” Morgan Moss</span></div></li>
<li><span class="ic">{IC["chat"]}</span><div><b>Straight answers</b><span>Diagnosis explained, plus tips on the preventative maintenance you can do yourself.</span></div></li>
<li><span class="ic">{IC["gauge"]}</span><div><b>Dyno in the building</b><span>Pipe, programmer and dyno tune done in one visit, often within a couple of hours.</span></div></li>
<li><span class="ic">{IC["road"]}</span><div><b>Riders tow in from hours away</b><span>Reviewers mention 3- and 4-hour drives for a tune.</span></div></li></ul>
<a class="btn mag" href="shop.html"><span>See the shop</span>{IC["arrow"]}</a></div></div></section>
<div style="overflow:hidden;padding:14px 0"><div class="marq red" aria-hidden="true"><div class="track">{"".join(f"<span>{w}</span>" for w in ["Unparalleled performance","Service","Parts","Sales","Dyno tuned"]*2)}{"".join(f"<span>{w}</span>" for w in ["Unparalleled performance","Service","Parts","Sales","Dyno tuned"]*2)}</div></div></div>
<section class="sec rv"><div class="q-big" aria-hidden="true">“</div><div class="wrap"><div class="shead"><div><p class="kicker">Five-star reviews</p><h2><span class="slant">Riders <span class="red">say it</span> best</span></h2></div><p>{stars(RATING)} <b>{RATING}</b> from {COUNT} Google reviews. Quoted word for word.</p></div>
<div class="rcar" aria-roledescription="carousel" aria-label="Customer reviews"><div class="rcar-vp"><div class="rcar-track">{slides}</div></div>
<div class="rctl"><button class="ar pv" type="button" aria-label="Previous review">{IC["left"]}</button><button class="ar nx" type="button" aria-label="Next review">{IC["right"]}</button><div class="rdots"></div><a class="btn ghost" style="margin-left:auto" href="reviews.html"><span>All reviews</span>{IC["arrow"]}</a></div></div></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap"><div class="teasers stagger">
<a class="tcard" href="dyno.html">{pic("g21",PH["g21"],sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>Dyno tuning</span><h3>Get it dialed</h3></div></a>
<a class="tcard" href="shop.html">{pic("g25",PH["g25"],sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>The shop</span><h3>Builds & showroom</h3></div></a>
<a class="tcard" href="visit.html">{pic("g09",PH["g09"],sizes="(max-width:900px) 100vw, 33vw")}<div class="tx"><span>Visit</span><h3>Hours & directions</h3></div></a></div></div></section>
{cta_band("Bring it in. Ride it out.","Call the shop to get your machine on the schedule. Open Tuesday to Friday 9 to 6 and Saturday 9 to 2.","g16")}'''

# ================= SERVICES =================
SVC=[
('rebuilds','Engine rebuilds','g22','When an engine is tired, knocking or blown, the shop tears it down, measures it and builds it back up: top ends, bottom ends and complete overhauls for quads, bikes and small engines.',['Engine overhauls','Top & bottom ends','Cylinder & head work','Measured, not guessed'],None),
('carbs','Carburetor work','g30','Hard starts, rough idle and a machine that won’t pull clean usually trace back to fuel. Carburetor rebuilds, cleaning and jetting are everyday work here.',['Carb rebuilds','Cleaning & jetting','Idle & starting issues','Small engines too'],'trsvis'),
('tune-ups','Tune-ups & service','g10','Oil, filters, plugs and a once-over that catches small problems before they turn into big ones. Oil changes are listed right on their Google profile.',['Oil changes','Filters & plugs','Preventative maintenance','Seasonal service'],'corey'),
('diagnosis','Electrical & bog diagnosis','g26','An intermittent bog or an electrical fault that comes and goes is the kind of problem other shops throw parts at. Here it gets diagnosed, explained and fixed.',['Intermittent bog diagnosis','Electrical troubleshooting','No-start problems','Clear explanations'],'brandon'),
('dyno','In-house dyno tuning','g23','A Dynojet dyno lives in its own cell in the shop, so tuning is measured on the rollers instead of guessed on the road. Customers tow race quads in from hours away for it.',['Dyno tuning','Quad & bike tuning','Before & after pulls','Race quads welcome'],'dominque'),
('performance','Fuel programmers & exhaust','g32','Adding a pipe or a fuel programmer only pays off when the tune matches. The shop installs the parts and dials them in on the dyno in the same visit.',['Fuel programmer installs','Exhaust installs','Power Commander tuning','Pipe + tune packages'],'brenton'),
]
svc_html=''.join(f'''<article class="svc" id="{i}"><div class="pframe" data-r="{"left" if n%2==0 else "right"}">{pic(img,PH[img])}<span class="tag">0{n+1} · {t}</span></div>
<div data-r><span class="no" aria-hidden="true">0{n+1}</span><h2 style="font-size:clamp(38px,4.6vw,64px)"><span class="slant">{t}</span></h2><p class="lead">{p}</p><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul>
{f'<blockquote>“{rtext(q)}”<cite>{e(REV[q][0])} · Google review</cite></blockquote>' if q else ''}
{f'<p style="margin-top:22px"><a class="btn mag" href="dyno.html"><span>More on dyno tuning</span>{IC["arrow"]}</a></p>' if i=="dyno" else ''}</div></article>''' for n,(i,t,img,p,li,q) in enumerate(SVC))
MS=[ # machine selector: label, title, bullets, source note
('atv','ATVs & quads','ATVs & quads',['Repair, service and tune-ups','Engine rebuilds and carb work','Pipes, programmers and dyno tuning','Sport and race quads welcome'],'ATV repair is their primary Google category.'),
('moto','Motorcycles','Motorcycles & dirt bikes',['Service and repair','Carburetor work and tuning','Dyno tuning','Diagnosis of bogs and electrical faults'],'Listed as a Motorcycle Repair Shop on Facebook.'),
('sxs','Side-by-sides','Side-by-sides',['Repair and service','Tuning'],'“ATV, Motorcycle, SXS Repair+Service+Tuning” from their Facebook bio.'),
('jet','Jet skis','Jet skis',['Service and repair'],'Jet ski is on the shop sign, and reviewers mention jet ski work.'),
('golf','Golf carts','Golf carts',['Service and repair'],'Reviewers mention golf cart repairs.'),
('mower','Mowers','Mowers & small engines',['Small-engine repair','Carb cleaning and tune-ups','Engines like Briggs & Stratton, Kohler and Kawasaki'],'As listed on their GreenPal profile.'),
('hand','Handhelds','Handheld equipment',['Trimmers, blowers and saws','Brands like Stihl and Echo'],'As listed on their GreenPal profile.'),
]
degs=[-100,-66,-33,0,33,66,100]
tabs=''.join(f'<button type="button" role="tab" id="t-{k}" aria-controls="p-{k}" aria-selected="{"true" if n==0 else "false"}" data-deg="{degs[n]}">{lab}</button>' for n,(k,lab,*_) in enumerate(MS))
panels=''.join(f'<div class="mpanel" role="tabpanel" id="p-{k}" aria-labelledby="t-{k}"{" hidden" if n else ""}><h3><span class="slant">{t}</span></h3><ul>{"".join(f"<li>{x}</li>" for x in li)}</ul><p class="srcn">{src}</p></div>' for n,(k,lab,t,li,src) in enumerate(MS))
STEPS=[('Call or roll in','Call (478) 808-3415 or bring the machine by during shop hours, Tuesday to Saturday.'),
('Diagnosis','The problem gets tracked down properly, so you are not paying for part after part.'),
('A straight answer','You hear what is wrong and what it takes. As their GreenPal listing puts it: “If it’s fixable, I’ll get it running; if it’s not worth the money to fix, I’ll tell you straight.”'),
('The work','Repair, rebuild or performance parts, with dyno time when the job calls for it.'),
('Ride out','Pick it up running right, with tips to keep it that way.')]
tl='<div class="tl"><svg class="line" aria-hidden="true"><line class="base" x1="3" y1="0" x2="3" y2="100"/><line class="draw" x1="3" y1="0" x2="3" y2="100"/></svg>'+''.join(f'<div class="step" data-n="{n+1}"><h3>{t}</h3><p>{p}</p></div>' for n,(t,p) in enumerate(STEPS))+'</div>'
services=f'''{phero("services.html","Services","Repair. Rebuild. <span class='red'>Tune.</span>","Everything from a carb clean to a full engine build and a dyno-tuned finish, for ATVs, motorcycles, side-by-sides, jet skis, golf carts, mowers and handhelds.","g04","g27")}
<section class="sec" style="padding-top:40px"><div class="wrap">{svc_html}</div></section>
<section class="sec carbon"><div class="wrap"><div class="shead"><div><p class="kicker">What are you bringing in?</p><h2><span class="slant">Pick your <span class="red">machine</span></span></h2></div><p>Tap a machine type to swing the tach and see what the shop handles for it.</p></div>
<div class="msel"><div data-r="zoom">{tach("tach",lab="SELECT MACHINE")}</div><div><div class="mtabs" role="tablist" aria-label="Machine type">{tabs}</div>{panels}</div></div></div></section>
<section class="sec"><div class="wrap split"><div><p class="kicker">How it works</p><h2><span class="slant">From drop-off to <span class="red">ride-out</span></span></h2><p class="lead">No runaround, no part-swapping guesswork. Here is how a typical job goes.</p></div>{tl}</div></section>
{cta_band("Not sure what it needs?","Describe the problem on the phone or send a quick service request and the shop will take it from there.","g06")}'''

# ================= DYNO =================
PINS=[('63%','76%','82%','The rollers','The drive wheel spins the drum under load while the software records the run.'),
('36%','61%','66%','Wheel chock','Holds the front end steady while the machine is strapped down.'),
('40%','55%','56%','Cooling fans','Keep the engine at temperature through back-to-back pulls.'),
('31%','21%','18%','Tuning station','The live readout on screen guides each change to the fuel map.'),
('59%','33%','31%','Dynojet','The machine is a Dynojet Model 200i, the name on its yellow base.')]
pins=''.join(f'<div class="pin" style="--x:{x};--y:{y}"><button type="button" aria-expanded="false" aria-label="{t}">{n+1}</button><span class="lbl" role="tooltip"><b>{t}</b>{p}</span></div>' for n,(x,y,ym,t,p) in enumerate(PINS))
hslist=''.join(f'<li><span><b>{t}.</b> {p}</span></li>' for x,y,ym,t,p in PINS)
DSTEPS=[('Strap down','The machine is rolled onto the dyno and strapped down tight.'),('Baseline pull','A first run shows where the engine is making power, and where it isn’t.'),('Dial it in','Jetting or the fuel programmer map gets adjusted between pulls.'),('Prove it','More pulls on the rollers until the numbers and the feel line up.'),('Ride it','You leave with a machine that pulls clean through the rev range.')]
dtl='<div class="tl"><svg class="line" aria-hidden="true"><line class="base" x1="3" y1="0" x2="3" y2="100"/><line class="draw" x1="3" y1="0" x2="3" y2="100"/></svg>'+''.join(f'<div class="step" data-n="{n+1}"><h3>{t}</h3><p>{p}</p></div>' for n,(t,p) in enumerate(DSTEPS))+'</div>'
dyno=f'''{phero("dyno.html","In-house dyno tuning","Dialed in on <span class='red'>the rollers</span>","Riders tow race quads and bikes from hours away to get tuned on the 5 Star dyno in Lizella. Pipe, programmer and tune, often in one visit.","g05","g23")}
<section class="sec"><div class="wrap"><div class="shead"><div><p class="kicker">Inside the dyno cell</p><h2><span class="slant">Take the <span class="red">tour</span></span></h2></div><p>Tap the numbered pins to see what each part of the dyno setup does.</p></div>
<div class="hs" data-r="zoom">{pic("g03",PH["g03"],sizes="(max-width:1240px) 100vw, 1240px")}{pins}</div><ol class="hslist">{hslist}</ol></div></section>
<section class="sec carbon"><div class="wrap revit"><div data-r="left"><p class="kicker">Just for fun</p><h2><span class="slant">Make a <span class="red">pull</span></span></h2><p class="lead">Press and hold the button to rev it up, watch the shift lights climb and let go before the limiter. The real thing happens on the rollers in Lizella.</p>
<blockquote style="margin:26px 0 0;padding:18px 20px;border-left:3px solid var(--rd);background:rgba(255,255,255,.03);border-radius:0 10px 10px 0;color:#e3e5e9">“{rtext("dominque")}”<cite style="display:block;font:600 12px var(--hud);letter-spacing:.14em;color:var(--si2);margin-top:8px;text-transform:uppercase;font-style:normal">{REV["dominque"][0]} · Google review</cite></blockquote></div>
<div class="revbox" data-r="right"><div class="shift" aria-hidden="true"><i></i><i></i><i></i><i></i><i></i><i></i></div>{tach("tach")}<div class="rpm" aria-live="off"><b>1,200</b> RPM</div><div class="drum" aria-hidden="true"></div><button class="btn xl hold" type="button" aria-pressed="false">Hold to rev</button></div></div></section>
<section class="sec"><div class="wrap split"><div><p class="kicker">How a dyno session goes</p><h2><span class="slant">Five steps to <span class="red">dialed</span></span></h2><p class="lead">A typical tune, start to finish.</p>
<div class="pframe" style="margin-top:30px;aspect-ratio:1/1" data-r>{pic("g08",PH["g08"])}</div></div>{dtl}</div></section>
<section class="sec" style="padding-top:0"><div class="wrap split rev"><div class="pframe" style="aspect-ratio:3/4" data-r="right">{pic("g35",PH["g35"])}<span class="tag">Measured to the thousandth</span></div>
<div data-r="left"><p class="kicker">Parts + tune, one visit</p><h2><span class="slant">Pipe. Programmer. <span class="red">Dyno.</span></span></h2><p class="lead">A new exhaust or fuel programmer only pays off when the tune matches it. Here the install and the dyno time happen together.</p>
<blockquote style="margin:22px 0;padding:18px 20px;border-left:3px solid var(--rd);background:rgba(255,255,255,.03);border-radius:0 10px 10px 0;color:#e3e5e9">“{rtext("brenton")}”<cite style="display:block;font:600 12px var(--hud);letter-spacing:.14em;color:var(--si2);margin-top:8px;text-transform:uppercase;font-style:normal">{REV["brenton"][0]} · Google review</cite></blockquote>
{btn_call("","Book dyno time")}</div></div></section>
{cta_band("Tow it in. Get it dialed.","Call to set up dyno time. Tell the shop what you’re running and what you’ve already done to it.",None,"Dyno tuned")}'''

# ================= SHOP =================
GAL=[('g16','builds'),('g17','builds'),('g29','builds'),('g19','builds'),('cover','builds'),('g06','builds'),('g15','builds'),('g07','machines'),('g10','machines'),
('g04','engines'),('g13','engines'),('g12','engines'),('g22','engines'),('g27','engines'),('g31','engines'),('g35','engines'),('g30','engines'),('g08','engines'),
('g03','dyno'),('g05','dyno'),('g21','dyno'),('g23','dyno'),('g28','machines'),('g32','machines')]
LABS={'builds':'Custom builds','engines':'Engine work','dyno':'Dyno','machines':'Machines'}
def gitem(n,c):
    w,h=dims(n,800)
    return f'<button type="button" class="gal-item" data-c="{c}" data-full="assets/img/{n}-1600.webp" aria-label="Open photo: {e(PH[n])}"><img src="assets/img/{n}-800.webp" width="{w}" height="{h}" alt="{e(PH[n])}" loading="lazy" decoding="async" style="aspect-ratio:{w}/{h}"><span>{LABS[c]}</span></button>'
gal=''.join(gitem(n,c) for n,c in GAL)
fil=''.join(f'<button type="button" aria-pressed="{"true" if k=="all" else "false"}" data-f="{k}">{l}</button>' for k,l in [('all','All'),('builds','Custom builds'),('engines','Engine work'),('dyno','Dyno'),('machines','Machines')])
shop=f'''{phero("shop.html","The shop","Service. Parts. <span class='red'>Sales.</span>","A clean, well-stocked shop on Eisenhower Pkwy in Lizella with a showroom, parts counter, tool wall and its own dyno cell.","g14","g09")}
<section class="sec"><div class="wrap"><div class="shead"><div><p class="kicker">Inside 5 Star</p><h2><span class="slant">Clean shop. <span class="red">Serious work.</span></span></h2></div><p>“Finding a good clean shop is very hard to find. These guys are your answer.” Brenton field, Google review</p></div>
<div class="bento stagger"><div class="pframe w2 h2">{pic("g01",PH["g01"])}</div><div class="card red"><b>Buy · Sell · Trade</b><span>Straight from their Facebook bio. Call to ask what’s on the floor.</span></div><div class="pframe">{pic("g18",PH["g18"],sizes="(max-width:900px) 50vw, 25vw")}</div>
<div class="pframe">{pic("g25",PH["g25"],sizes="(max-width:900px) 50vw, 25vw")}</div><div class="card"><b>Easy to get in</b><span>Wheelchair-accessible entrance and parking, plus a restroom on site.</span></div>
<div class="pframe w2">{pic("g26",PH["g26"])}</div><div class="card"><b>Pay your way</b><span>Credit, debit and NFC mobile payments accepted.</span></div><a class="card red" href="dyno.html" style="text-decoration:none"><b>Own dyno cell →</b><span>Tuning happens in-house. Take the dyno tour.</span></a></div></div></section>
<section class="sec carbon" style="padding-inline:0"><div class="wrap"><div class="shead"><div><p class="kicker">Gallery</p><h2><span class="slant">Out of the <span class="red">shop</span></span></h2></div><p>Builds, engines and dyno days, all from the shop’s own Google and Facebook photos. Drag or swipe, tap to enlarge.</p></div>
<div class="gfil" data-for="gtrack" role="group" aria-label="Filter photos">{fil}</div></div><div class="gal-track" id="gtrack">{gal}</div></section>
<div class="tlb" aria-hidden="true" role="dialog" aria-modal="true" aria-label="Photo viewer"><button class="x1" type="button" aria-label="Close">{IC["x"]}</button><button class="pv" type="button" aria-label="Previous photo">{IC["left"]}</button><figure><img alt=""><figcaption></figcaption></figure><button class="nx" type="button" aria-label="Next photo">{IC["right"]}</button></div>
{cta_band("Come see the shop.","8094 Eisenhower Pkwy in Lizella. Open Tuesday to Friday 9 to 6, Saturday 9 to 2.",None,"Service Parts Sales")}'''

# ================= REVIEWS =================
DIST=[(5,161),(4,4),(3,1),(2,1),(1,2)]
bars=''.join(f'<div class="row"><span>{s}★</span><div class="bar"><i style="--w:{c/COUNT*100:.1f}%"></i></div><span>{c}</span></div>' for s,c in DIST)
CHIPS=['dyno tuning','small engine repair','intermittent bog diagnosis','quad tuning','bike tuning','reliable staff','quality parts','easy process','cleanliness','workmanship']
allrev=['morgan','corey','dominque','brandon','trsvis','rayy','brenton','angie']
rcards=''.join(f'<article class="rcard" data-r>{stars(5)}<p>“{rtext(k)}”</p><footer><b>{e(REV[k][0])}</b>Google review · {REV[k][1]}</footer></article>' for k in allrev)
reviews=f'''{phero("reviews.html","Reviews",f"{RATING} stars. <span class='red'>{COUNT} reviews.</span>","What riders say about 5 Star Small Engines on Google, with five-star reviews quoted word for word.","g17","g29",f'<a class="btn mag" href="{GREV}" target="_blank" rel="noopener">{IC["g"]}<span>Read them on Google</span></a>{btn_call("ghost")}')}
<section class="sec" style="padding-top:40px"><div class="wrap"><div class="rsum" data-r><div><div class="big">{RATING}</div>{stars(RATING)}<p class="muted" style="margin:0">{COUNT} Google reviews · 161 of them five stars</p></div>
<div><div class="bars">{bars}</div><div class="chips" aria-label="What reviewers mention most">{"".join(f"<span>{c}</span>" for c in CHIPS)}</div><p class="muted" style="font-size:13px;margin:14px 0 0">Rating, counts and review topics as shown on the Google Business Profile, November 2026.</p></div></div></div></section>
<section class="sec" style="padding-top:0"><div class="wrap"><div class="shead"><div><p class="kicker">In their words</p><h2><span class="slant">Straight from <span class="red">Google</span></span></h2></div><p>Every review below is a five-star Google review, copied exactly as written.</p></div><div class="rgrid">{rcards}</div></div></section>
{cta_band("Join the five-star crowd.","Get your machine on the schedule and see what the reviews are talking about.","g19")}'''

# ================= VISIT =================
FAQ=[('What do you work on?','ATVs and quads, motorcycles and dirt bikes, side-by-sides, jet skis, golf carts, mowers and handheld equipment like trimmers and blowers.'),
('Do you do dyno tuning?','Yes. The shop has its own Dynojet dyno in-house for tuning quads and bikes, including fuel programmer and exhaust setups. Customers drive in from 3 to 4 hours away for it.'),
('What are your hours?','Tuesday to Friday 9 AM to 6 PM and Saturday 9 AM to 2 PM. Closed Sunday and Monday. Holiday hours, such as Thanksgiving and Black Friday, might differ, so call ahead.'),
('Where are you located?','8094 Eisenhower Pkwy, Lizella, GA 31052, just outside Macon.'),
('How much does a repair cost?','It depends on the machine and the problem. Call (478) 808-3415 to describe what is going on and ask about pricing.'),
('Do you sell machines or parts?','The shop sign reads Service · Parts · Sales, and their Facebook bio says Buy + Sell + Trade. Call to ask what is in stock.'),
('What payments do you take?','Credit cards, debit cards and NFC mobile payments.'),
('Is the shop accessible?','Yes. There is a wheelchair-accessible entrance and parking, and a restroom on site.')]
faq_html=''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in FAQ)
faq_ld={"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in FAQ]}
opts=''.join(f'<option>{m}</option>' for m in ['ATV / quad','Motorcycle / dirt bike','Side-by-side','Jet ski','Golf cart','Mower','Handheld equipment','Other'])
needs=''.join(f'<option>{m}</option>' for m in ['Repair / diagnosis','Tune-up / service','Carburetor work','Engine rebuild','Dyno tuning','Fuel programmer / exhaust','Not sure yet'])
visit=f'''{phero("visit.html","Visit the shop","Find us in <span class='red'>Lizella</span>","8094 Eisenhower Pkwy, Lizella, GA 31052, just outside Macon. Call ahead, roll in, or send a service request.","g25","g09",f'{btn_call()}<a class="btn ghost" href="{DIR}" target="_blank" rel="noopener">{IC["pin"]}<span>Get directions</span></a>')}
<section class="sec" style="padding-top:40px"><div class="wrap visit"><div class="vcard" data-r><p class="kicker">Call the shop</p><a class="bigphone chrome" href="{TEL}">{PHONE}</a>
<p class="status" data-status style="font:600 15px var(--hud)"><span>Checking hours…</span></p>{hours_tbl()}
<p class="note">Thanksgiving (Thu, Nov 26) and Black Friday (Fri, Nov 27): Google lists 9 AM to 6 PM but says hours might differ. Call before you head over.</p>
<p style="margin:18px 0 0"><b>Address</b><br><a href="{DIR}" target="_blank" rel="noopener">{ADDR}</a></p><p><b>Email</b><br><a href="mailto:{EMAIL}">{EMAIL}</a></p><p style="margin:0"><b>Follow</b><br><a href="{FB}" target="_blank" rel="noopener">Facebook</a> · <a href="{GMAPS}" target="_blank" rel="noopener">Google Maps</a></p></div>
<div class="mapf" data-r><iframe title="Map to 5 Star Small Engines, 8094 Eisenhower Pkwy, Lizella GA" src="{MAPEMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div></div></section>
<section class="sec carbon" id="request"><div class="wrap split"><div><p class="kicker">Service request</p><h2><span class="slant">Tell us what it’s <span class="red">doing</span></span></h2><p class="lead">Fill this in and it opens a ready-to-send email to the shop at {EMAIL}. Nothing is sent until you hit send in your own email app. For anything urgent, just call.</p>{btn_call("ghost")}</div>
<form class="form vcard" data-mailto="{EMAIL}" data-r><label>Your name<input name="name" autocomplete="name" required></label><label>Phone<input name="phone" type="tel" autocomplete="tel" required></label>
<label>Machine<select name="machine">{opts}</select></label><label>What you need<select name="need">{needs}</select></label>
<label class="full">Make / model / year<input name="make" placeholder="e.g. Yamaha Raptor 700, 2019"></label><label class="full">What’s going on?<textarea name="msg" placeholder="Symptoms, when it started, anything already tried"></textarea></label>
<div class="full"><button class="btn xl" type="submit" style="width:100%">Open email to the shop {IC["arrow"]}</button></div></form></div></section>
<section class="sec"><div class="wrap split" style="align-items:start"><div><p class="kicker">FAQ</p><h2><span class="slant">Good to <span class="red">know</span></span></h2><p class="lead">Quick answers before you load up the trailer.</p></div><div class="faq">{faq_html}</div></div></section>'''

PAGES=[
('index.html','5 Star Small Engines | ATV, Motorcycle & Small Engine Repair + Dyno Tuning in Lizella, GA','ATV, motorcycle, side-by-side, jet ski, golf cart and small-engine repair near Macon, GA. In-house dyno tuning. 4.9★ from 169 Google reviews. Call (478) 808-3415.',home,[biz(reviews_ld(home_rev)),crumbs_ld('Home','index.html')],True),
('services.html','Services | Engine Rebuilds, Carb Work, Tune-ups & Diagnosis | 5 Star Small Engines','Engine rebuilds, carburetor work, tune-ups, electrical and bog diagnosis, dyno tuning, fuel programmers and exhaust for ATVs, bikes, jet skis, golf carts and mowers in Lizella, GA.',services,[biz({"hasOfferCatalog":{"@type":"OfferCatalog","name":"Services","itemListElement":[{"@type":"Offer","itemOffered":{"@type":"Service","name":t,"description":p}} for i,t,img,p,li,q in SVC]}}),crumbs_ld('Services','services.html')],False),
('dyno.html','Dyno Tuning in Lizella, GA (Macon Area) | 5 Star Small Engines','In-house Dynojet dyno tuning for ATVs, race quads and motorcycles near Macon, GA. Pipe, fuel programmer and tune in one visit. Riders drive 3–4 hours for it.',dyno,[biz(),crumbs_ld('Dyno Tuning','dyno.html'),{"@context":"https://schema.org","@type":"Service","name":"Dyno tuning","serviceType":"ATV and motorcycle dyno tuning","provider":{"@id":BASE+"#business"},"areaServed":"Middle Georgia"}],False),
('shop.html','The Shop & Gallery | Service, Parts, Sales | 5 Star Small Engines, Lizella GA','Inside 5 Star Small Engines in Lizella, GA: showroom, parts counter, tool wall, dyno cell and a gallery of custom trikes, quads and engine builds.',shop,[biz(),crumbs_ld('The Shop','shop.html')],False),
('reviews.html',f'Reviews | {RATING} Stars from {COUNT} Google Reviews | 5 Star Small Engines','5 Star Small Engines in Lizella, GA is rated 4.9 stars from 169 Google reviews. Read five-star reviews from ATV, motorcycle and dyno tuning customers, word for word.',reviews,[biz(reviews_ld(allrev)),crumbs_ld('Reviews','reviews.html')],False),
('visit.html','Visit | Hours, Directions & Service Requests | 5 Star Small Engines, Lizella GA','5 Star Small Engines: 8094 Eisenhower Pkwy, Lizella, GA 31052. Call (478) 808-3415. Open Tue–Fri 9–6, Sat 9–2. Map, hours, FAQ and service request form.',visit,[biz(),crumbs_ld('Visit','visit.html'),faq_ld],False),
]
for f,t,dsc,b,ld,hm in PAGES: (OUT/f).write_text(page(f,t,dsc,b,ld,hm))
nf=f'''<section class="phero" style="min-height:82vh"><div class="wrap"><p class="kicker">Error 404</p><h1><span class="slant">Stalled <span class="red">out.</span></span></h1><p class="lead">That page isn’t here. Head back home or give the shop a call.</p><div class="ctas" style="margin-top:24px"><a class="btn mag" href="index.html"><span>Back home</span></a>{btn_call("ghost")}</div></div></section>'''
p404=page('404.html','Page not found | 5 Star Small Engines','This page could not be found.',nf,[biz()])
for a in ['href="index.html"','href="services.html"','href="dyno.html"','href="shop.html"','href="reviews.html"','href="visit.html"']:
    p404=p404.replace(a,a.replace('href="',f'href="/{REPO}/'))
p404=p404.replace('src="assets/',f'src="/{REPO}/assets/').replace('href="assets/',f'href="/{REPO}/assets/').replace('href="favicon.ico"',f'href="/{REPO}/favicon.ico"').replace('href="apple-touch-icon.png"',f'href="/{REPO}/apple-touch-icon.png"').replace('content="index,follow"','content="noindex"')
(OUT/'404.html').write_text(p404)
(OUT/'robots.txt').write_text(f'User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n')
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{BASE}{"" if f=="index.html" else f}</loc><lastmod>2026-11-25</lastmod></url>\n' for f,*_ in PAGES)+'</urlset>\n')
(OUT/'llms.txt').write_text(f'''# {NAME}

> ATV, motorcycle, side-by-side, jet ski, golf cart, mower and handheld small-engine repair shop with an in-house Dynojet dyno, at {ADDR} (just outside Macon, Georgia). Phone {PHONE}. Email {EMAIL}. Open Tuesday–Friday 9 AM–6 PM and Saturday 9 AM–2 PM; closed Sunday and Monday. Rated {RATING} stars from {COUNT} Google reviews.

## Key facts
- Google category: ATV repair shop. Facebook category: Motorcycle Repair Shop.
- Services: engine rebuilds and overhauls; carburetor rebuilds, cleaning and jetting; tune-ups and oil changes; electrical troubleshooting and intermittent bog diagnosis; in-house dyno tuning; fuel programmer installs; exhaust work.
- Machines: ATVs and quads, motorcycles and dirt bikes, side-by-sides, jet skis, golf carts, mowers, handheld equipment.
- Also: service, parts and sales (shop sign); buy, sell and trade (Facebook bio).
- Customers report driving 3–4 hours for dyno tuning.
- Payments: credit cards, debit cards, NFC mobile payments.
- Accessibility: wheelchair-accessible entrance and parking; restroom.
- Holiday hours (Thanksgiving, Black Friday) might differ; call ahead.
- Facebook: {FB}
- Google Maps: {GMAPS}

## Pages
- [Home]({BASE}): overview, services, ratings, reviews
- [Services]({BASE}services.html): each service in detail, machines worked on, how a job works
- [Dyno Tuning]({BASE}dyno.html): the in-house dyno and how a tuning session goes
- [The Shop]({BASE}shop.html): showroom, amenities, payments and photo gallery
- [Reviews]({BASE}reviews.html): rating breakdown and five-star Google reviews quoted verbatim
- [Visit]({BASE}visit.html): hours, map, directions, service request form and FAQ
''')
(OUT/'.nojekyll').write_text('')
(OUT/'README.md').write_text(f'# {NAME} — demo website\n\nDesign preview by RGWebD. Live: {BASE}\n\nStatic site generated by `generator/build.py` (photo processing in `generator/process.py`).\n')
print('built',[p[0] for p in PAGES])
