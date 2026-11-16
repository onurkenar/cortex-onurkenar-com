/* 8.5 Takvim — kayıtların takvim görünümü (2026-11-15). Kullanıcı kararları: liste + ay görünümü (kayda tıklayınca ilgili alt
   menüde kayıt açılır, tarih kayıt formunda değiştirilir), içerik blog yazıları + sosyal paylaşımlar + türetilen story'ler + özel
   günler, .ics dışa aktarımı. Bölüm ip_calendar kararsızdır; görünüm rehber sayfasında çizilir (guideHtml sarmalanır). Kayıt
   tutmaz: blog (8.3, window.BL), paylaşım (8.4, window.SP), story (Story Kullanımı "her paylaşımın Story sürümü" iken her
   paylaşımın story'si — Story Saati'nde, aynı gün), özel gün (Özel Gün Takvimi açıkken plan dönemindeki günler). Görünüm,
   süzgeçler ve ay seçimi oturumluktur. .ics: görünen kayıtlar; saatli kayıt 30 dk (Türkiye saati UTC+3 → UTC), özel gün tüm gün;
   CRLF + 75 bayt katlama. 8.8 Etkinlikler eklenince (window.ET.cal) etkinlik (başlangıç–bitiş saati) ve aktiviteleri (30 dk)
   "Etkinlik" / "Etkinlik aktivitesi" olarak görünür; tıklayınca 8.8'de kayıt açılır. 8.12 Ölçüm'ün rapor günleri (window.OLC.cal) "Rapor" olarak görünür. Kaynak docs/v26/v26-calendar.{js,css} → docs/v26/takvim_ekle.py */
(function(){
const SID="ip_calendar";
if(!SI[SID]||!window.BL)return;
const CV={view:"list",month:"",show:{blog:true,post:true,story:true,day:true,evt:true,act:true,rep:true}};
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const DRE=/^\d{4}-\d{2}-\d{2}$/;
const AY=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],GUN=["Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi","Pazar"];
const TYP={blog:"Blog",post:"Paylaşım",story:"Story",day:"Özel gün",evt:"Etkinlik",act:"Etkinlik aktivitesi",rep:"Rapor"};
const hasRep=()=>!!(window.OLC&&FI.ip_ms_reports&&shown(FI.ip_ms_reports));
const hasET=()=>!!(window.ET&&FI.ip_events_rec&&shown(FI.ip_events_rec));
const dt=s=>new Date(s+"T00:00:00Z"),ymd=d=>d.toISOString().slice(0,10),wd=s=>(dt(s).getUTCDay()+6)%7;
function isoWeek(s){let d=dt(s),day=(d.getUTCDay()+6)%7;d.setUTCDate(d.getUTCDate()-day+3);let y=d.getUTCFullYear(),j=new Date(Date.UTC(y,0,4));return 1+Math.round(((d-j)/864e5-3+((j.getUTCDay()+6)%7))/7)}
function storyTime(){return {t1830:"18:30",t1230:"12:30",t0900:"09:00"}[sv("mk_story_time")]||"18:30"}
function events(){let E0=[],pre=String(mkT("mk_prefix")||"ÖNEK").toUpperCase();
 if(FI.ip_blogs&&shown(FI.ip_blogs)){let S=BL.store();BL.sorted().forEach((id,n)=>{let r=S[id];if(r.tarih&&DRE.test(r.tarih))E0.push({k:"blog",d:r.tarih,t:r.saat||"",id,no:`${pre}-BLG-${String(n+1).padStart(3,"0")}`,title:r.baslik||"Başlıksız yazı",chip:r.huni||""})})}
 if(window.SP&&FI.ip_posts&&shown(FI.ip_posts)){let S=SP.store(),fs=Array.isArray(state.mk_formats)?state.mk_formats:[],der=fs.includes("S")&&sv("mk_story")==="every";
  SP.sorted().forEach((id,n)=>{let r=S[id];if(!r.tarih||!DRE.test(r.tarih))return;let no=`${pre}-SM-${String(n+1).padStart(3,"0")}`;E0.push({k:r.f==="S"?"story":"post",d:r.tarih,t:r.saat||"",id,no,title:r.title||"Başlıksız paylaşım",chip:SP.fmtAd(r.f||"")});
   if(der&&r.f!=="S")E0.push({k:"story",d:r.tarih,t:storyTime(),id,no:no+"-S",title:"Story: "+(r.title||"paylaşım"),chip:"Story (türetilen)",derived:1})})}
 BL.days().forEach(([id,lab])=>{let m=/^(\d{4}-\d{2}-\d{2}) · (.*)$/.exec(lab);if(m)E0.push({k:"day",d:m[1],t:"",id,title:m[2],chip:"Özel gün"})});
 if(hasET())window.ET.cal().forEach(e=>E0.push(e));
 if(hasRep())window.OLC.cal().forEach(e=>E0.push(e));
 return E0.sort((a,b)=>(a.d+(a.t||"00:00"))<(b.d+(b.t||"00:00"))?-1:(a.d+(a.t||"00:00"))>(b.d+(b.t||"00:00"))?1:0)}
const vis=L=>L.filter(e=>CV.show[e.k]);
function open(e){if(e.k==="blog"){BL.open(e.id);goToField("ip_blog","ip_blogs")}else if(e.k==="post"||(e.k==="story"&&!e.derived)){SP.open(e.id);goToField("ip_social","ip_posts")}else if(e.k==="story"){SP.open(e.id);goToField("ip_social","ip_posts")}else if(e.k==="evt"||e.k==="act"){window.ET.open(e.id);goToField("ip_events","ip_events_rec")}else if(e.k==="rep"){goToField("ip_measure","ip_ms_reports");return}
 setTimeout(()=>{let d=document.querySelector(`.prRec[data-${e.k==="blog"?"bid":e.k==="evt"||e.k==="act"?"eid":"pid"}="${CSS.escape(e.id)}"]`);if(d){d.scrollIntoView({block:"start"});let s=d.querySelector("summary");if(s)s.focus()}},60)}
function item(e,i){let a=e.k==="day"?"":` data-cv="${i}" tabindex="0" role="button"`;return `<li class="cvI cv-${e.k}" title="${E((e.t?e.t+" · ":"")+e.title)}"${a}><span class="cvT">${E(e.t||"")}</span><span class="cvK">${E(TYP[e.k])}</span>${e.chip?`<span class="prChip">${E(e.chip)}</span>`:""}<span class="cvTi">${E(e.title)}</span>${e.no?`<code class="prPath">${E(e.no)}</code>`:""}</li>`}
function list(L){if(!L.length)return `<p class="prEmpty">Takvimde gösterilecek kayıt yok. Blog yazıları, sosyal paylaşımlar ve etkinlikler 8. menüdeki alt menülerinde eklenir.</p>`;
 let W={},o=[];L.forEach((e,i)=>{let d=dt(e.d);d.setUTCDate(d.getUTCDate()-wd(e.d));let k=ymd(d);(W[k]=W[k]||[]).push([e,i])});
 Object.keys(W).sort().forEach(k=>{let s=dt(k),e=new Date(s.getTime()+6*864e5);o.push(`<section class="cvW"><h4>${s.getUTCDate()} ${AY[s.getUTCMonth()]} – ${e.getUTCDate()} ${AY[e.getUTCMonth()]} ${e.getUTCFullYear()} · Hafta ${isoWeek(k)} · ${W[k].length} kayıt</h4><ul>${W[k].map(([x,i])=>`<li class="cvDay"><b>${E(GUN[wd(x.d)])} ${dt(x.d).getUTCDate()}</b><ul>${item(x,i)}</ul></li>`).join("")}</ul></section>`)});return o.join("")}
function month(L,ym){let [y,m]=ym.split("-").map(Number),first=`${y}-${String(m).padStart(2,"0")}-01`,days=new Date(Date.UTC(y,m,0)).getUTCDate(),lead=wd(first),cells=[];
 for(let i=0;i<lead;i++)cells.push(`<div class="cvC cvX" aria-hidden="true"></div>`);
 for(let d=1;d<=days;d++){let s=`${y}-${String(m).padStart(2,"0")}-${String(d).padStart(2,"0")}`,it=L.map((e,i)=>[e,i]).filter(([e])=>e.d===s);cells.push(`<div class="cvC${wd(s)>4?" cvWe":""}"><b>${d}</b>${it.length?`<ul>${it.map(([e,i])=>item(e,i)).join("")}</ul>`:""}</div>`)}
 return `<div class="cvM" role="grid" aria-label="${E(AY[m-1]+" "+y)}">${["Pzt","Sal","Çar","Per","Cum","Cmt","Paz"].map((g,i)=>`<div class="cvH" role="columnheader" aria-label="${E(GUN[i])}">${E(g)}</div>`).join("")}${cells.join("")}</div>`}
function months(L){let P=BL.period(),set=new Set(L.map(e=>e.d.slice(0,7)));if(P){let d=dt(P[0].slice(0,7)+"-01");while(ymd(d).slice(0,7)<=P[1].slice(0,7)){set.add(ymd(d).slice(0,7));d.setUTCMonth(d.getUTCMonth()+1)}}if(!set.size)set.add(new Date().toISOString().slice(0,7));return [...set].sort()}
function view(){let all=events(),L=vis(all),M=months(L.length?L:all);if(!M.includes(CV.month))CV.month=M[0];let mi=M.indexOf(CV.month),[y,m]=CV.month.split("-").map(Number);window.__cvL=L;
 let cnt=k=>all.filter(e=>e.k===k).length,tg=Object.keys(TYP).filter(k=>(k==="rep"?hasRep():(k!=="evt"&&k!=="act")||hasET())).map(k=>`<label class="blChk"><input type="checkbox" data-cvs="${k}"${CV.show[k]?" checked":""}> ${E(TYP[k])} (${cnt(k)})</label>`).join("");
 return `<section class="gCard cvBox" aria-label="İçerik takvimi"><div class="cvBar"><div class="cvSeg" role="group" aria-label="Görünüm"><button type="button" class="btn${CV.view==="list"?" dark":""}" data-cvv="list" aria-pressed="${CV.view==="list"}">Liste</button><button type="button" class="btn${CV.view==="month"?" dark":""}" data-cvv="month" aria-pressed="${CV.view==="month"}">Ay</button></div><div class="blAct">${tg}</div><button type="button" class="btn" data-cvics${L.length?"":" disabled"}>Takvime aktar (.ics)</button></div>`+
  (CV.view==="month"?`<div class="cvNav"><button type="button" class="btn" data-cvm="-1"${mi>0?"":" disabled"} aria-label="Önceki ay">‹</button><b>${E(AY[m-1]+" "+y)}</b><button type="button" class="btn" data-cvm="1"${mi<M.length-1?"":" disabled"} aria-label="Sonraki ay">›</button></div>${month(L,CV.month)}`:list(L))+
  (state.ip_cal_note?`<p class="prHint">Takvim notu: ${E(state.ip_cal_note)}</p>`:"")+`</section>`}
/* .ics */
function icsEsc(s){return String(s||"").replace(/\\/g,"\\\\").replace(/;/g,"\\;").replace(/,/g,"\\,").replace(/\r?\n/g,"\\n")}
function fold(l){let o=[],b=new TextEncoder(),cur="";for(const ch of l){if(b.encode(cur+ch).length>(o.length?74:75)){o.push(cur);cur=ch}else cur+=ch}o.push(cur);return o.join("\r\n ")}
function utc(d,t){let [h,mi]=(t||"09:00").split(":").map(Number),x=new Date(Date.UTC(+d.slice(0,4),+d.slice(5,7)-1,+d.slice(8,10),h-3,mi));return x.toISOString().replace(/[-:]/g,"").slice(0,15)+"Z"}
function ics(L){let now=new Date().toISOString().replace(/[-:]/g,"").slice(0,15)+"Z",host=String(state.domain_name||"cortex").replace(/^https?:\/\//,"").split("/")[0]||"cortex",out=["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Cortex Configurator//Icerik Takvimi//TR","CALSCALE:GREGORIAN","METHOD:PUBLISH"];
 L.forEach((e,i)=>{let uid=`${e.k}-${e.k==="act"?e.no:e.id}-${e.d}${e.derived?"-s":""}@${host}`,sum=`[${e.k==="post"||e.k==="story"?e.chip||TYP[e.k]:TYP[e.k]}] ${e.title}`;out.push("BEGIN:VEVENT","UID:"+uid,"DTSTAMP:"+now);
  if(e.t){let s=utc(e.d,e.t),en=e.te&&e.te>e.t?utc(e.d,e.te):new Date(Date.UTC(+s.slice(0,4),+s.slice(4,6)-1,+s.slice(6,8),+s.slice(9,11),+s.slice(11,13)+30)).toISOString().replace(/[-:]/g,"").slice(0,15)+"Z";out.push("DTSTART:"+s,"DTEND:"+en)}
  else{let n=new Date(dt(e.d).getTime()+864e5);out.push("DTSTART;VALUE=DATE:"+e.d.replace(/-/g,""),"DTEND;VALUE=DATE:"+ymd(n).replace(/-/g,""))}
  out.push("SUMMARY:"+icsEsc(sum));if(e.no)out.push("DESCRIPTION:"+icsEsc(e.no));out.push("END:VEVENT")});out.push("END:VCALENDAR");return out.map(fold).join("\r\n")+"\r\n"}
window.cvIcs=()=>ics(vis(events()));window.cvEvents=events;
/* rehber sayfasına çizim */
const _gh=guideHtml;guideHtml=function(s){let h=_gh.apply(this,arguments);if(s&&s.id===SID)h=h.replace(/^(<div class="guide">)/,"$1"+view());return h};
function redraw(){if(active===SID&&typeof guideMode==="function"&&guideMode()){let y=window.scrollY;renderFields();window.scrollTo(0,y)}}
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".cvBox [data-cvv],.cvBox [data-cvm],.cvBox [data-cvics],.cvBox [data-cv]");if(!b)return;
 if(b.dataset.cvv){CV.view=b.dataset.cvv;redraw()}else if(b.dataset.cvm){let M=months(vis(events()).length?vis(events()):events()),i=M.indexOf(CV.month)+(+b.dataset.cvm);if(M[i]){CV.month=M[i];redraw()}}
 else if(b.hasAttribute("data-cvics")){let pre=String(mkT("mk_prefix")||"icerik").toLowerCase(),a=document.createElement("a"),u=URL.createObjectURL(new Blob([window.cvIcs()],{type:"text/calendar"}));a.href=u;a.download=pre+"-icerik-takvimi.ics";document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1000)}
 else if(b.dataset.cv!==undefined){let x=(window.__cvL||[])[+b.dataset.cv];if(x)open(x)}},true);
document.addEventListener("keydown",e=>{let b=e.target.closest&&e.target.closest(".cvBox [data-cv]");if(b&&(e.key==="Enter"||e.key===" ")){e.preventDefault();b.click()}},true);
document.addEventListener("change",e=>{let t=e.target;if(t.dataset&&t.dataset.cvs){CV.show[t.dataset.cvs]=t.checked;redraw()}},true);
})();
