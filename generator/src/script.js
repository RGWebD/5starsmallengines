(()=>{
const d=document,root=d.documentElement;
const RM=matchMedia('(prefers-reduced-motion: reduce)').matches;
const FINE=matchMedia('(hover:hover) and (pointer:fine)').matches;
const $=(s,c=d)=>c.querySelector(s),$$=(s,c=d)=>[...c.querySelectorAll(s)];
if(RM)root.classList.add('rm');

/* live open / closed badge, America/New_York. Tue–Fri 9–6, Sat 9–2, Sun & Mon closed.
   Holidays from the Google listing: Thanksgiving + Black Friday 2026 show "hours might differ". */
const HRS={2:[540,1080],3:[540,1080],4:[540,1080],5:[540,1080],6:[540,840]};
const UNK={'2026-11-26':1,'2026-11-27':1};
const DN=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
function ny(){const p=new Intl.DateTimeFormat('en-US',{timeZone:'America/New_York',year:'numeric',month:'2-digit',day:'2-digit',weekday:'short',hour:'2-digit',minute:'2-digit',hourCycle:'h23'}).formatToParts(new Date());const o={};p.forEach(x=>o[x.type]=x.value);return{day:DN.indexOf(o.weekday),min:(+o.hour%24)*60+(+o.minute),ymd:`${o.year}-${o.month}-${o.day}`}}
const fmt=m=>{const h=Math.floor(m/60),mm=m%60;return (h%12||12)+(mm?':'+String(mm).padStart(2,'0'):'')+(h<12?' AM':' PM')};
function nextOpen(day,min){for(let k=0;k<8;k++){const dd=(day+k)%7,h=HRS[dd];if(!h)continue;if(k===0&&min>=h[0])continue;return (k===0?'today':k===1?'tomorrow':DN[dd])+' '+fmt(h[0])}return''}
function status(){const n=ny(),h=HRS[n.day];let cls,t;
 if(UNK[n.ymd]){cls='unk';t='Holiday · hours might differ, call first'}
 else if(h&&n.min>=h[0]&&n.min<h[1]){cls='open';t='Open now · until '+fmt(h[1])}
 else{cls='closed';t='Closed · opens '+nextOpen(n.day,n.min)}
 $$('[data-status]').forEach(el=>{el.classList.remove('open','closed','unk');el.classList.add(cls);const s=$('span',el)||el;s.textContent=t});
 $$('.hours tr').forEach(tr=>tr.classList.toggle('today',+tr.dataset.d===n.day))}
status();setInterval(status,60000);

/* header, shift-light progress, mobile bar */
const hdr=$('.hdr'),prog=$('.progress'),mbar=$('.mbar');
function onScroll(){const y=scrollY,h=root.scrollHeight-innerHeight;hdr&&hdr.classList.toggle('scrolled',y>30);if(prog)prog.style.transform=`scaleX(${h>0?y/h:0})`;if(mbar)mbar.classList.toggle('show',y>260)}
addEventListener('scroll',onScroll,{passive:true});onScroll();

/* demo pill */
const demo=$('.demo');if(demo){if(sessionStorage.getItem('demoX'))demo.remove();else $('button',demo).onclick=()=>{demo.remove();sessionStorage.setItem('demoX',1)}}

/* mobile nav */
const bg=$('.burger'),mn=$('.mnav');
if(bg&&mn){const set=o=>{bg.setAttribute('aria-expanded',o);mn.classList.toggle('open',o);d.body.style.overflow=o?'hidden':''};
 bg.addEventListener('click',()=>set(bg.getAttribute('aria-expanded')!=='true'));
 $$('a',mn).forEach(a=>a.addEventListener('click',()=>set(false)));
 addEventListener('keydown',e=>{if(e.key==='Escape'&&mn.classList.contains('open')){set(false);bg.focus()}})}

/* reveals */
const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12,rootMargin:'0px 0px -5% 0px'});
$$('[data-r],.stagger,.bars').forEach(el=>{if(RM)el.classList.add('in');else io.observe(el)});
$$('.stagger').forEach(g=>[...g.children].forEach((c,i)=>c.style.transitionDelay=(i*90)+'ms'));

/* loader: tach sweep + five stars light up like a start tree */
const hero=$('.hero'),ld=$('.loader');
function heroGo(){hero&&hero.classList.add('go')}
if(ld){
 if(RM||sessionStorage.getItem('seen5')){ld.remove();heroGo()}
 else{sessionStorage.setItem('seen5',1);const n=$('.ndl',ld),S=$$('.stars i',ld);let done=false;
  const fin=()=>{if(done)return;done=true;$('.stars',ld).classList.add('go');ld.classList.add('done');setTimeout(heroGo,250);setTimeout(()=>ld.remove(),1300)};
  const t0=performance.now();(function f(t){const k=Math.min(1,(t-t0)/1300);const e=k<.75?k/.75:1-(k-.75)/.25*.35;n.style.transform=`rotate(${-120+240*e}deg)`;S.forEach((s,i)=>s.classList.toggle('on',k>i*.16+.05));if(k<1&&!done)requestAnimationFrame(f);else setTimeout(fin,180)})(t0);
  ld.addEventListener('click',fin);setTimeout(fin,3200)}
}else heroGo();

/* parallax page-hero backgrounds */
const px=$$('[data-px]');
if(!RM&&px.length){const tick=()=>px.forEach(el=>{const r=el.getBoundingClientRect();if(r.bottom<-100||r.top>innerHeight+100)return;el.style.transform=`translateY(${(scrollY*+el.dataset.px).toFixed(1)}px)`});addEventListener('scroll',()=>requestAnimationFrame(tick),{passive:true});tick()}

/* counters + dial gauges */
function runCount(el){const end=+el.dataset.count,dec=+(el.dataset.dec||0),out=$('b',el)||el;const g=el.closest('.gauge');
 if(g){const arc=$('.val',g);if(arc){const L=+arc.dataset.len,f=+arc.dataset.frac;arc.style.strokeDashoffset=(L*(1-f)).toFixed(1)}const n=$('.ndl',g);if(n)n.style.transform=`rotate(${n.dataset.deg}deg)`}
 if(RM){out.textContent=end.toFixed(dec);return}
 const t0=performance.now(),D=1900;(function f(t){const k=Math.min(1,(t-t0)/D),e=1-Math.pow(1-k,4);out.textContent=(end*e).toFixed(dec);if(k<1)requestAnimationFrame(f);else out.textContent=end.toFixed(dec)})(t0)}
const cio=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){runCount(e.target);cio.unobserve(e.target)}}),{threshold:.35});
$$('[data-count]').forEach(el=>cio.observe(el));

/* tilt + magnetic */
if(FINE&&!RM){
 $$('.scard,.tcard').forEach(c=>{c.addEventListener('pointermove',e=>{const r=c.getBoundingClientRect(),x=(e.clientX-r.left)/r.width-.5,y=(e.clientY-r.top)/r.height-.5;c.style.setProperty('--ry',(x*9).toFixed(2)+'deg');c.style.setProperty('--rx',(-y*9).toFixed(2)+'deg')});c.addEventListener('pointerleave',()=>{c.style.setProperty('--ry','0deg');c.style.setProperty('--rx','0deg')})});
 $$('.btn.mag').forEach(b=>{b.addEventListener('pointermove',e=>{const r=b.getBoundingClientRect();b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.2}px,${(e.clientY-r.top-r.height/2)*.3}px)`});b.addEventListener('pointerleave',()=>b.style.transform='')})}

/* scroll-drawn timeline (steps stay lit) */
$$('.tl').forEach(tl=>{const p=$('.draw',tl),steps=$$('.step',tl),svg=$('svg.line',tl);
 function upd(){const r=tl.getBoundingClientRect(),H=r.height;svg.setAttribute('viewBox',`0 0 6 ${H}`);$$('line',svg).forEach(l=>l.setAttribute('y2',H));p.style.strokeDasharray=H;
  const k=RM?1:Math.min(1,Math.max(0,(innerHeight*.65-r.top)/H));p.style.strokeDashoffset=H*(1-k);
  steps.forEach(s=>{if(RM||s.getBoundingClientRect().top+30<innerHeight*.65)s.classList.add('lit')})}
 addEventListener('scroll',()=>requestAnimationFrame(upd),{passive:true});addEventListener('resize',upd);upd()});

/* reviews carousel */
$$('.rcar').forEach(c=>{const tr=$('.rcar-track',c),sl=$$('.rslide',c),dots=$('.rdots',c);let i=0,tm;
 sl.forEach((s,k)=>{const b=d.createElement('button');b.type='button';b.setAttribute('aria-label','Show review '+(k+1));b.onclick=()=>go(k,1);dots.appendChild(b)});
 function go(k,user){i=(k+sl.length)%sl.length;tr.style.transform=`translateX(${-100*i}%)`;$$('button',dots).forEach((b,j)=>b.setAttribute('aria-current',j===i));sl.forEach((s,j)=>{s.setAttribute('aria-hidden',j!==i);s.inert=j!==i});if(user)auto()}
 function auto(){clearInterval(tm);if(!RM)tm=setInterval(()=>go(i+1),7000)}
 $('.pv',c).onclick=()=>go(i-1,1);$('.nx',c).onclick=()=>go(i+1,1);
 c.addEventListener('mouseenter',()=>clearInterval(tm));c.addEventListener('mouseleave',auto);c.addEventListener('focusin',()=>clearInterval(tm));c.addEventListener('focusout',auto);
 let sx=null;tr.addEventListener('pointerdown',e=>sx=e.clientX);addEventListener('pointerup',e=>{if(sx===null)return;const dx=e.clientX-sx;sx=null;if(Math.abs(dx)>50)go(i+(dx<0?1:-1),1)});
 go(0);auto()});

/* gallery: filters, drag-scroll, lightbox (scoped, focus-trapped) */
$$('.gfil').forEach(f=>{const tr=$('#'+f.dataset.for);$$('button',f).forEach(b=>b.addEventListener('click',()=>{$$('button',f).forEach(x=>x.setAttribute('aria-pressed',x===b));const c=b.dataset.f;$$('.gal-item',tr).forEach(it=>it.hidden=!(c==='all'||it.dataset.c.split(' ').includes(c)));tr.scrollLeft=0}))});
$$('.gal-track').forEach(t=>{let down=false,sx=0,sl=0,moved=0,v=0,lx=0,raf;
 t.addEventListener('pointerdown',e=>{if(e.pointerType!=='mouse')return;down=true;moved=0;sx=lx=e.clientX;sl=t.scrollLeft;t.classList.add('drag');cancelAnimationFrame(raf)});
 addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-sx;moved=Math.max(moved,Math.abs(dx));v=e.clientX-lx;lx=e.clientX;t.scrollLeft=sl-dx});
 addEventListener('pointerup',()=>{if(!down)return;down=false;t.classList.remove('drag');if(!RM){(function m(){v*=.92;t.scrollLeft-=v;if(Math.abs(v)>.5)raf=requestAnimationFrame(m)})()}});
 t.addEventListener('click',e=>{if(moved>6){e.preventDefault();e.stopPropagation();moved=0}},true)});
const lb=$('.tlb');
if(lb){const im=$('img',lb),cap=$('figcaption',lb);let list=[],k=0,last=null;
 function show(n){k=(n+list.length)%list.length;const it=list[k];im.src=it.dataset.full;im.alt=$('img',it).alt;cap.textContent=$('img',it).alt}
 $$('.gal-item').forEach(it=>it.addEventListener('click',()=>{const box=it.closest('.gal-track');list=$$('.gal-item',box).filter(x=>!x.hidden);last=it;show(list.indexOf(it));lb.classList.add('open');lb.setAttribute('aria-hidden','false');d.body.style.overflow='hidden';$('.x1',lb).focus()}));
 const close=()=>{lb.classList.remove('open');lb.setAttribute('aria-hidden','true');d.body.style.overflow='';last&&last.focus()};
 $('.x1',lb).onclick=close;$('.pv',lb).onclick=()=>show(k-1);$('.nx',lb).onclick=()=>show(k+1);
 lb.addEventListener('click',e=>{if(e.target===lb||e.target.tagName==='FIGURE')close()});
 let tx=null;lb.addEventListener('touchstart',e=>tx=e.touches[0].clientX,{passive:true});lb.addEventListener('touchend',e=>{if(tx===null)return;const dx=e.changedTouches[0].clientX-tx;tx=null;if(Math.abs(dx)>50)show(k+(dx<0?1:-1))});
 addEventListener('keydown',e=>{if(!lb.classList.contains('open'))return;if(e.key==='Escape')close();if(e.key==='ArrowLeft')show(k-1);if(e.key==='ArrowRight')show(k+1);
  if(e.key==='Tab'){const f=$$('button',lb),a=f[0],z=f[f.length-1];if(e.shiftKey&&d.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&d.activeElement===z){e.preventDefault();a.focus()}}})}

/* machine selector: tabs swing the tach needle */
$$('.msel').forEach(m=>{const tabs=$$('[role=tab]',m),n=$('.tach .ndl',m);
 function sel(t,focus){tabs.forEach(x=>{const on=x===t;x.setAttribute('aria-selected',on);x.tabIndex=on?0:-1;$('#'+x.getAttribute('aria-controls')).hidden=!on});n.style.transform=`rotate(${t.dataset.deg}deg)`;if(focus)t.focus()}
 tabs.forEach((t,i)=>{t.addEventListener('click',()=>sel(t));t.addEventListener('keydown',e=>{let j=null;if(e.key==='ArrowRight'||e.key==='ArrowDown')j=i+1;if(e.key==='ArrowLeft'||e.key==='ArrowUp')j=i-1;if(e.key==='Home')j=0;if(e.key==='End')j=tabs.length-1;if(j!==null){e.preventDefault();sel(tabs[(j+tabs.length)%tabs.length],1)}})});
 sel(tabs[0])});

/* hotspot pins: flip labels that would leave the viewport */
function fitHs(){$$('.pin').forEach(p=>{p.classList.remove('rev');const l=$('.lbl',p);if(!l)return;const r=p.getBoundingClientRect();if(r.right+50+l.offsetWidth>Math.min(innerWidth,p.closest('.hs').getBoundingClientRect().right+40))p.classList.add('rev')})}
$$('.pin button').forEach(b=>b.addEventListener('click',()=>{const p=b.parentElement,on=!p.classList.contains('on');$$('.pin').forEach(x=>x.classList.remove('on'));p.classList.toggle('on',on);b.setAttribute('aria-expanded',on)}));
addEventListener('load',fitHs);addEventListener('resize',fitHs);fitHs();

/* hold-to-rev tach on the dyno page */
$$('.revbox').forEach(bx=>{const btn=$('.hold',bx),t=$('.tach',bx),out=$('.rpm b',bx),L=$$('.shift i',bx);let v=0,hold=false,raf=null;
 function draw(){t.style.setProperty('--a',(-120+240*v/13)+'deg');out.textContent=Math.round(v*1000).toLocaleString('en-US');L.forEach((l,i)=>{l.className=v>8+i*.9?(i<2?'g':i<4?'y':'r'):''})}
 function loop(){v=hold?Math.min(13,v+(13.2-v)*.035+.05):Math.max(1.2,v-.22);if(hold&&v>12.6)v=12.1+Math.random()*.5;draw();bx.classList.toggle('pull',v>1.3);if(hold||v>1.21)raf=requestAnimationFrame(loop);else{raf=null;bx.classList.remove('pull')}}
 const on=e=>{e.preventDefault();hold=true;btn.setAttribute('aria-pressed','true');if(!raf)loop()},off=()=>{hold=false;btn.setAttribute('aria-pressed','false');if(!raf)loop()};
 btn.addEventListener('pointerdown',on);addEventListener('pointerup',off);btn.addEventListener('pointerleave',off);
 btn.addEventListener('keydown',e=>{if((e.key===' '||e.key==='Enter')&&!e.repeat)on(e)});btn.addEventListener('keyup',e=>{if(e.key===' '||e.key==='Enter')off()});
 v=1.2;draw()});

/* service request form -> pre-filled email to the shop */
$$('form[data-mailto]').forEach(f=>f.addEventListener('submit',e=>{e.preventDefault();const fd=new FormData(f);const g=k=>(fd.get(k)||'').toString().trim();
 const sub=`Service request: ${g('machine')} ${g('make')}`.trim();
 const body=`Name: ${g('name')}\nPhone: ${g('phone')}\nMachine: ${g('machine')}\nMake / model / year: ${g('make')}\nWhat I need: ${g('need')}\n\nWhat's going on:\n${g('msg')}\n`;
 location.href=`mailto:${f.dataset.mailto}?subject=${encodeURIComponent(sub)}&body=${encodeURIComponent(body)}`}));
root.classList.add('ready');
})();
