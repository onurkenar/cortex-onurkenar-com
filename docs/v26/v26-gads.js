/* 8.9 Google Ads — kampanya / grup / metin düzenleyicisi (2026-11-15). Kullanıcı kararları: kampanya + grup + metin (sayaçlı);
   taslaklar ürün / hizmetlerden (8.2) Pazarlama › Kampanya Yapısı'na göre türetilir; ekler bütçe payı ve günlük tutar, Google Ads
   Editor CSV (şablonun toplu yükleme paneli), marka hariç tutma / rakip negatifleri, arama sonucu önizlemesi; kampanya adı
   Önek_Tür_Konu_YYYYAA. Alan ip_gads_rec type "records", showIf mk_ads_channels ∋ google.
   Değer: state.ip_gads = {K-01: {tur ("search" | "pmax" | "remarketing"), konu, ad (boşsa önerilen ad), hub, pay, gerekce,
   sitelinks ("Metin | Açıklama 1 | Açıklama 2 | URL"), callout, snippetB, snippetD, negatifler, markaHaric, not (satır satır),
   g: {G-01-1: {ad, urun, url, yol ("parça1/parça2"), basliklar, uzunBasliklar, aciklamalar, anahtarlar, temalar, negatifler,
   cta}}}}; hesap düzeyi negatifler state.ip_gads_neg (satır satır). Aktarım ads.kampanyalar[] / ads.butce[] / ads.negatifler[]
   (KILAVUZ 18 · Google Ads); kayıt yoksa temel dışa aktarımın kararlardan kurduğu boş kampanyalar kalır.
   Kaynak docs/v26/v26-gads.{js,css} → docs/v26/google_ads_ekle.py */
(function(){
const FID="ip_gads_rec",KEY="ip_gads",NKEY="ip_gads_neg";
if(!FI[FID]||!window.REC||!window.BL)return;
const BL=window.BL,OPEN=new Set(),GOPEN=new Set();
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const has=(id,x)=>{let v=sv(id);return Array.isArray(v)&&v.includes(x)};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const cells=x=>x.split("|").map(y=>y.trim());
const uniq=a=>{let s=new Set;return a.filter(x=>{let k=String(x).toLocaleLowerCase("tr");if(!x||s.has(k))return false;s.add(k);return true})};
const first=s=>{let m=String(s||"").match(/^[^.!?]*[.!?]/);return (m?m[0]:String(s||"")).trim()};
const slug=x=>norm(String(x||"")).replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"")||"grup";
const TUR={search:"Arama Ağı",pmax:"Maks. Performans",remarketing:"Yeniden Pazarlama"},TK={search:"Search",pmax:"PMax",remarketing:"Remarketing"};
/* ölçüler: [satır sınırı, en az, en çok] */
const LIM={basliklar:[30,3,15],uzunBasliklar:[90,1,5],aciklamalar:[90,2,4],temalar:[80,0,25],callout:[25,0,20],snippetD:[25,3,10]};
const lim=(p,tur)=>p==="aciklamalar"&&tur!=="search"?[90,2,5,60]:LIM[p];
function store(){let v=state[KEY];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
function types(){let t=(sv("mk_gads_types")||[]).filter(x=>TUR[x]);return t.length?t:["search"]}
function brand(){return String(state.mk_brand_name||state.project_name||"").trim()}
function ctaLab(){return clean(lab(FI.oc_cta_primary,state.oc_cta_primary))||"Teklif Alın"}
const now=()=>"Hemen "+ctaLab().toLocaleLowerCase("tr")+".";
function rivals(){return lines(state.oc_competitors).map(x=>cells(x)[0]).filter(Boolean)}
function locs(){return String(sv("mk_geo_detail")||"").split(/[,;\n]/).map(x=>x.trim()).filter(Boolean)}
function items(){return typeof window.prItems==="function"?window.prItems():[]}
function asc(s){return String(s||"").replace(/[çÇ]/g,c=>c==="ç"?"c":"C").replace(/[ğĞ]/g,c=>c==="ğ"?"g":"G").replace(/[ıİ]/g,c=>c==="ı"?"i":"I").replace(/[öÖ]/g,c=>c==="ö"?"o":"O").replace(/[şŞ]/g,c=>c==="ş"?"s":"S").replace(/[üÜ]/g,c=>c==="ü"?"u":"U")}
function suggest(r){let p=String(mkT("mk_prefix")||"ONEK").toUpperCase(),d=String(mkT("mk_period_start")||""),ym=/^\d{4}-\d{2}/.test(d)?d.slice(0,4)+d.slice(5,7):"YYYYAA",k=asc(r.konu||"Genel").split(/[^A-Za-z0-9]+/).filter(Boolean).map(w=>w[0].toUpperCase()+w.slice(1)).join("")||"Genel";return `${p}_${TK[r.tur]||"Search"}_${k}_${ym}`}
const cname=r=>String(r.ad||"").trim()||suggest(r);
/* sayaçlar */
function lm(v,L){let a=lines(v),[mx,mn,n,sh]=L,over=a.filter(x=>[...x].length>mx).length,ns=sh&&a.length&&!a.some(x=>[...x].length<=sh),bad=over||ns||(a.length&&a.length<mn)||a.length>n;return `<small class="prMeter${bad?" bad":a.length?" ok":""}">${a.length} satır (${mn?mn+"–":"en çok "}${n})${over?` · ${over} satır ${mx} karakteri aşıyor`:` · satır başına en çok ${mx}`}${sh?` · en az biri ≤ ${sh}`:""}${ns?" — yok":""}</small>`}
function ylm(v){let p=String(v||"").split("/").map(x=>x.trim()).filter(Boolean),bad=p.length>2||p.some(x=>[...x].length>15);return `<small class="prMeter${bad?" bad":p.length?" ok":""}">${p.length} parça (en çok 2) · parça başına en çok 15 karakter</small>`}
/* biçim */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function inp(k,p,label,kind,val,meter,ph){let a=`data-m="${E(p)}" ${q(k)} aria-label="${E(label)}"`,ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:5}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${meter||""}</label>`}
function sel(k,p,label,opts,val,empty){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-m="${E(p)}" ${q(k)} aria-label="${E(label)}">${empty!==false?`<option value="">${E(empty||"Seçin")}</option>`:""}${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
const sec=(t,x)=>`<fieldset class="prSec"><legend>${E(t)}</legend>${x}</fieldset>`;
function host(){return String(state.domain_name||"ornek.com").replace(/^https?:\/\//,"").replace(/\/.*$/,"")||"ornek.com"}
function serp(g){let B=lines(g.basliklar).filter(x=>[...x].length<=30).slice(0,3),D=lines(g.aciklamalar).filter(x=>[...x].length<=90).slice(0,2),Y=String(g.yol||"").split("/").map(x=>x.trim()).filter(Boolean).slice(0,2);
 return `<div class="gaSerp" aria-label="Arama sonucu önizlemesi"><small>Sponsorlu</small><div class="gaUrl">${E([host()].concat(Y).join(" › "))}</div><div class="gaT">${B.length?B.map(E).join(" | "):"Başlık 1 | Başlık 2 | Başlık 3"}</div><div class="gaD">${D.length?D.map(E).join(" "):"Açıklama 1 ve açıklama 2 burada görünür."}</div></div><p class="prHint">Önizleme ilk üç başlıkla ilk iki açıklamayı gösterir; Google başlık ve açıklamaları farklı birleşimlerle döndürür, her başlık tek başına anlamlı olmalı.</p>`}
function gForm(cid,gid,g,tur){let k=[cid,gid],v=p=>g[p]||"",Pr=items().map(x=>[x.k,x.ad]);
 let a=`<div class="blGrid">${inp(k,"ad","Grup adı","text",v("ad"))}${Pr.length?sel(k,"urun","Bağlı ürün / hizmet",Pr,v("urun"),"Bağlı değil"):""}</div><div class="blGrid">${inp(k,"url","Nihai URL (site içi yol)","text",v("url"),"","/hizmetler/…")}${inp(k,"yol","Görünen yol (parça1/parça2)","text",v("yol"),ylm(v("yol")),"hizmetler/otomasyon")}</div>`+
  inp(k,"basliklar","Başlıklar (her satıra bir başlık)","lines",v("basliklar"),lm(v("basliklar"),lim("basliklar",tur)))+(tur!=="search"?inp(k,"uzunBasliklar","Uzun başlıklar","lines",v("uzunBasliklar"),lm(v("uzunBasliklar"),lim("uzunBasliklar",tur))):"")+
  inp(k,"aciklamalar","Açıklamalar (her satıra bir açıklama)","lines",v("aciklamalar"),lm(v("aciklamalar"),lim("aciklamalar",tur)))+
  (tur==="search"?inp(k,"anahtarlar","Anahtar kelimeler (her satıra bir kelime: [tam], \"sıralı\", geniş)","lines",v("anahtarlar"))+inp(k,"negatifler","Grup negatifleri","lines",v("negatifler"))+`<div class="gaPrev">${serp(g)}</div>`
   :inp(k,"temalar","Arama temaları (her satıra bir tema)","lines",v("temalar"),lm(v("temalar"),LIM.temalar))+inp(k,"cta","Harekete geçirici (boşsa Ana CTA)","text",v("cta"),"",ctaLab()));
 return a+`<div class="blAct"><button type="button" class="prAdd blDelRec" data-gdel ${q(k)}>Grubu sil</button></div>`}
function gHead(gid,g,tur){let n=lines(g.basliklar).length,d=lines(g.aciklamalar).length,ok=n>=3&&d>=2&&(tur!=="search"||lines(g.anahtarlar).length);return `<span class="prPath">${E(gid)}</span><span class="prName">${E(g.ad||"Adsız grup")}</span><span class="prChip">${n} başlık · ${d} açıklama</span><span class="prPct${ok?" ok":""}">${ok?"hazır":"eksik"}</span>`}
function form(id,r){let k=id,v=p=>r[p]||"",A=sv("mk_gads_assets"),as=x=>!Array.isArray(A)||!A.length||A.includes(x),T=uniq(types().concat(r.tur?[r.tur]:[])).map(t=>[t,TUR[t]]),G=r.g||{};
 let kmp=`<div class="blGrid">${sel(k,"tur","Kampanya türü",T,v("tur")||"search",false)}${inp(k,"konu","Konu (kampanya adına girer)","text",v("konu"))}</div>`+inp(k,"ad","Kampanya adı (boşsa önerilen)","text",v("ad"),`<small class="prMeter">Önerilen: <code class="gaSug">${E(suggest(r))}</code></small>`,suggest(r))+
  `<div class="blGrid">${inp(k,"hub","Açılış (hub) sayfası","text",v("hub"),"","/hizmetler")}${inp(k,"pay","Bütçe payı (%)","text",v("pay"),gPay(r),"örn. 40")}</div>`+inp(k,"gerekce","Bütçe gerekçesi","text",v("gerekce"))+inp(k,"not","Not (kampanya kartında uyarı olarak görünür)","text",v("not"));
 let oge=(as("sitelinks")?inp(k,"sitelinks","Site bağlantıları (her satıra: Metin ≤25 | Açıklama 1 ≤35 | Açıklama 2 ≤35 | URL)","lines",v("sitelinks"),slm(v("sitelinks"))):"")+(as("callouts")?inp(k,"callout","Açıklama metinleri / callout (her satıra bir metin)","lines",v("callout"),lm(v("callout"),LIM.callout)):"")+
  (as("snippet")?`<div class="blGrid">${inp(k,"snippetB","Yapılandırılmış snippet başlığı","text",v("snippetB"),"","Hizmetler")}${inp(k,"snippetD","Snippet değerleri (her satıra bir değer)","lines",v("snippetD"),lm(v("snippetD"),LIM.snippetD))}</div>`:"")+
  inp(k,"negatifler","Kampanya negatifleri (her satıra bir kelime)","lines",v("negatifler"))+(r.tur==="pmax"?inp(k,"markaHaric","Marka hariç tutma (her satıra bir marka adı)","lines",v("markaHaric")):"");
 let gr=Object.keys(G).map(gid=>`<details class="prRec gaG" data-gid="${E(gid)}"${GOPEN.has(gid)?" open":""}><summary>${gHead(gid,G[gid],r.tur||"search")}</summary><div class="prBody">${GOPEN.has(gid)?gForm(id,gid,G[gid],r.tur||"search"):""}</div></details>`).join("");
 return sec("Kampanya",kmp)+sec("Öğeler ve negatifler",oge)+sec(`${r.tur==="search"||!r.tur?"Reklam grupları":"Öğe grupları"} (${Object.keys(G).length})`,`<div class="prList">${gr}</div><div class="blAct"><button type="button" class="prAdd" data-gadd ${q(id)}>+ Grup ekle</button></div>`)+`<div class="blAct"><button type="button" class="prAdd blDelRec" data-del ${q(id)}>Kampanyayı sil</button></div>`}
function slm(v){let a=lines(v).map(cells),over=a.filter(c=>[...(c[0]||"")].length>25||[...(c[1]||"")].length>35||[...(c[2]||"")].length>35).length;return `<small class="prMeter${over?" bad":a.length?" ok":""}">${a.length} bağlantı (en az 2 önerilir)${over?` · ${over} satırda ölçü aşımı`:""}</small>`}
function gPay(r){let S=store(),t=Object.values(S).reduce((a,x)=>a+(parseFloat(String(x.pay||"").replace(",","."))||0),0),n=mkNum("mk_gads_budget"),p=parseFloat(String(r.pay||"").replace(",","."))||0;
 return `<small class="prMeter${t&&Math.round(t)!==100?" bad":t?" ok":""}">Toplam pay %${Math.round(t*10)/10}${n>0&&p?` · aylık ≈ ${Math.round(n*p/100).toLocaleString("tr-TR")} TL · günlük ≈ ${Math.round(n*p/100/30.4).toLocaleString("tr-TR")} TL`:n>0?"":" · tutar için Pazarlama › Google Ads › Aylık Bütçe"}</small>`}
function sorted(){let S=store();return Object.keys(S).sort((a,b)=>{let x=+((a.match(/\d+/)||[0])[0]),y=+((b.match(/\d+/)||[0])[0]);return x-y||(a<b?-1:1)})}
function head(id,r){let G=r.g||{},n=Object.keys(G).length,ok=n&&Object.values(G).every(g=>lines(g.basliklar).length>=3&&lines(g.aciklamalar).length>=2);return `<span class="prPath">${E(id)}</span><span class="prChip">${E(TUR[r.tur]||TUR.search)}</span><span class="prName">${E(cname(r))}</span><span class="prChip">${n} grup</span>${r.pay?`<span class="prChip">%${E(r.pay)}</span>`:""}<span class="prPct${ok?" ok":""}">${ok?"hazır":"eksik"}</span>`}
function box(f){let S=store(),ids=sorted(),neg=has("mk_gads_brand","account_negative")||state[NKEY];
 let rows=ids.map(id=>`<details class="prRec" data-kid="${E(id)}"${OPEN.has(id)?" open":""}><summary>${head(id,S[id])}</summary><div class="prBody">${OPEN.has(id)?form(id,S[id]):""}</div></details>`).join("");
 let ng=neg?`<details class="gaNeg"${state[NKEY]?"":" open"}><summary>Hesap düzeyi negatif liste (${lines(state[NKEY]).length})</summary><label class="prF"><span>Her satıra bir kelime; bütün kampanyalara uygulanır</span><textarea class="control" rows="4" data-neg aria-label="Hesap düzeyi negatif kelimeler">${E(state[NKEY]||"")}</textarea></label></details>`:"";
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox gaBox"><div class="prHead"><p><b>${ids.length}</b> kampanya · yapı: ${E(clean(lab(FI.mk_gads_structure,sv("mk_gads_structure")))||"Hizmet bazında")} · türler: ${E(types().map(t=>TUR[t]).join(", "))}.</p><div class="blAct"><button type="button" class="prAdd" data-add>+ Kampanya ekle</button><button type="button" class="prAdd" data-derive>Ürün / hizmetlerden taslak oluştur</button></div></div><p class="prHint gaMsg" aria-live="polite"></p>${ng}${ids.length?`<div class="prList">${rows}</div>`:`<p class="prEmpty">Henüz kampanya yok. “Ürün / hizmetlerden taslak oluştur” Ortak Bilgiler › Ürün / Hizmet Listesi ve 8. menü › Ürün ve Hizmetler kayıtlarından kampanya ve grupları kurar; “+ Kampanya ekle” ile elle de eklenir.</p>`}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt işlemleri */
function nextId(){let n=Object.keys(store()).map(k=>+((k.match(/^K-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "K-"+String(n+1).padStart(2,"0")}
function nextG(cid,r){let n=Object.keys(r.g||{}).map(k=>+((k.match(/-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "G-"+cid.slice(2)+"-"+(n+1)}
function commit(redraw){let S=store();if(Object.keys(S).length)state[KEY]=S;else delete state[KEY];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
const rec=id=>document.querySelector(`.gaBox .prRec[data-kid="${CSS.escape(id)}"]`),grec=gid=>document.querySelector(`.gaG[data-gid="${CSS.escape(gid)}"]`);
function put(k,p,v){let S=store();if(Array.isArray(k)){let [cid,gid]=k,r=S[cid];if(!r||!r.g||!r.g[gid])return;let g=r.g[gid];if(v==="")delete g[p];else g[p]=v;state[KEY]=S;commit(false);let d=grec(gid);if(!d)return;let s=d.querySelector(":scope>summary");if(s)s.innerHTML=gHead(gid,g,r.tur||"search");let pv=d.querySelector(".gaPrev");if(pv&&["basliklar","aciklamalar","yol"].includes(p))pv.innerHTML=serp(g);let c=rec(cid);c=c&&c.querySelector(":scope>summary");if(c)c.innerHTML=head(cid,r);return}
 let r=S[k];if(!r)return;if(v==="")delete r[p];else r[p]=v;state[KEY]=S;commit(false);if(p==="tur"){refreshField(FID);return}let d=rec(k);if(!d)return;let s=d.querySelector(":scope>summary");if(s)s.innerHTML=head(k,r);if(p==="konu"){let g=d.querySelector(".gaSug");if(g)g.textContent=suggest(r);let a=d.querySelector('[data-m="ad"]:not([data-r*=","])');if(a)a.placeholder=suggest(r)}
 if(p==="pay")document.querySelectorAll('.gaBox [data-m="pay"]').forEach(x=>{let m=x.parentElement.querySelector(".prMeter"),id=JSON.parse(x.dataset.r);if(m){let w=document.createElement("div");w.innerHTML=gPay(store()[id]||{});m.replaceWith(w.firstChild)}})}
function meterFor(t){let k=JSON.parse(t.dataset.r),p=t.dataset.m,S=store(),tur=Array.isArray(k)?((S[k[0]]||{}).tur||"search"):((S[k]||{}).tur||"search");
 if(LIM[p])return lm(t.value,lim(p,tur));if(p==="yol")return ylm(t.value);if(p==="sitelinks")return slm(t.value);return null}
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement))return;if(d.dataset.kid&&d.closest(".gaBox")){let id=d.dataset.kid;if(d.open){OPEN.add(id);let b=d.querySelector(":scope>.prBody");if(b&&!b.children.length)b.innerHTML=form(id,store()[id]||{})}else OPEN.delete(id)}
 else if(d.dataset.gid){let gid=d.dataset.gid,cid=d.closest(".prRec[data-kid]").dataset.kid,r=store()[cid]||{};if(d.open){GOPEN.add(gid);let b=d.querySelector(":scope>.prBody");if(b&&!b.children.length)b.innerHTML=gForm(cid,gid,(r.g||{})[gid]||{},r.tur||"search")}else GOPEN.delete(gid)}},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".gaBox"))return;if(t.hasAttribute("data-neg")){if(!requireProject()){refreshField(FID);return}if(t.value.trim())state[NKEY]=t.value;else delete state[NKEY];save();renderRules();return}
 if(!t.dataset.m)return;if(!requireProject()){refreshField(FID);return}put(JSON.parse(t.dataset.r),t.dataset.m,t.value);let mh=meterFor(t),m=t.parentElement.querySelector(".prMeter");if(mh&&m){let w=document.createElement("div");w.innerHTML=mh;m.replaceWith(w.firstChild)}},true);
document.addEventListener("change",e=>{let t=e.target;if(t.closest&&t.closest(".gaBox")&&t.matches("select[data-m]"))t.dispatchEvent(new Event("input",{bubbles:true}))},true);
/* ürün / hizmetlerden türetme */
const fit=(a,n)=>a.filter(x=>x&&[...x].length<=n);
function pGroup(it,loc,tur){let P=(state.ip_products||{})[it.k]||{},kw=Array.isArray(P.kw)?P.kw.filter(x=>x&&x.k&&x.durum!=="Bırakıldı"):[],pos=kw.filter(x=>x.tur!=="Negatif"),b=brand(),c=ctaLab(),lc=s=>String(s).toLocaleLowerCase("tr"),L=loc?" "+lc(loc):"";
 let fay=lines(P.faydalar).map(cells),bas=uniq(fit([it.ad+(loc?" "+loc:""),it.ad,P.slogan,...fay.map(x=>x[0]),c,b],30)).slice(0,15),uz=uniq(fit([P.deger,P.slogan,first(P.ozet)],90)).slice(0,5),ac=uniq(fit([first(P.ozet),...fay.map(x=>x[1]&&first(x[1])),now()],90)).slice(0,tur==="search"?4:5);
 let g={ad:it.ad+(loc?" – "+loc:""),urun:it.k,url:it.yol||"",yol:slug(it.ad).split("-").reduce((o,w)=>{let x=o.length?o[o.length-1]:"";if(o.length&&[...(x+"-"+w)].length<=15)o[o.length-1]=x+"-"+w;else if(o.length<2&&[...w].length<=15)o.push(w);return o},[]).join("/"),basliklar:bas.join("\n"),aciklamalar:ac.join("\n")};
 if(tur==="search"){let a=(pos.filter(x=>x.niyet!=="Bilgi").length?pos.filter(x=>x.niyet!=="Bilgi"):pos).map(x=>(x.tur==="Odak"||x.tur==="Marka"?"[":"\"")+lc(x.k)+L+(x.tur==="Odak"||x.tur==="Marka"?"]":"\""));if(!a.length)a=[`[${lc(it.ad)}${L}]`,`"${lc(it.ad)}${L}"`];g.anahtarlar=uniq(a).join("\n");let n=kw.filter(x=>x.tur==="Negatif").map(x=>lc(x.k));if(n.length)g.negatifler=uniq(n).join("\n")}
 else{g.uzunBasliklar=uz.join("\n");let t=pos.map(x=>lc(x.k)+L);if(!t.length)t=[lc(it.ad)+L];g.temalar=uniq(t).slice(0,25).join("\n")}
 Object.keys(g).forEach(x=>{if(!g[x])delete g[x]});return g}
function derive(){let I=items();if(!I.length)return "Önce Ortak Bilgiler › Ürün / Hizmet Listesi'ni doldurun.";let S=store(),st=sv("mk_gads_structure")||"service",L=locs(),T=types(),br=sv("mk_gads_brand")||[],b=brand(),A=sv("mk_gads_assets"),as=x=>!Array.isArray(A)||!A.length||A.includes(x),made=0,gm=0,msg=[];
 if(st==="location_service"&&!L.length){msg.push("Hizmet Bölgesi Ayrıntısı boş; hizmet bazında kuruldu");st="service"}
 const find=(tur,konu)=>Object.keys(S).find(k=>S[k].tur===tur&&String(S[k].konu||"").toLocaleLowerCase("tr")===String(konu).toLocaleLowerCase("tr"));
 const camp=(tur,konu,x)=>{let id=find(tur,konu);if(!id){id=nextId();S[id]=Object.assign({tur,konu,g:{}},x||{});state[KEY]=S;made++}return id};
 const addG=(id,g)=>{let r=S[id];if(Object.values(r.g||{}).some(x=>(g.urun&&x.urun===g.urun&&x.ad===g.ad)||(!g.urun&&x.ad===g.ad)))return;r.g=r.g||{};r.g[nextG(id,r)]=g;gm++};
 const sl=me=>as("sitelinks")?I.filter(x=>x!==me&&x.yol).slice(0,4).map(x=>`${[...x.ad].slice(0,25).join("")} |  |  | ${x.yol}`).join("\n"):"",co=it=>{if(!as("callouts"))return "";let P=it?(state.ip_products||{})[it.k]||{}:{};return uniq(fit(lines(P.faydalar).map(x=>cells(x)[0]),25)).slice(0,4).join("\n")};
 const hub=it=>sv("mk_ads_landing")==="home"?"/":it&&it.yol||"/";
 T.filter(t=>t!=="remarketing").forEach(tur=>{
  if(st==="single"){let id=camp(tur,"Hizmetler",{hub:hub(null),sitelinks:sl(null)});I.forEach(it=>addG(id,pGroup(it,"",tur)))}
  else if(st==="location_service")L.forEach(l=>{let id=camp(tur,l,{hub:"/"});I.forEach(it=>addG(id,pGroup(it,l,tur)))});
  else I.forEach(it=>{let id=camp(tur,it.ad,{hub:hub(it),sitelinks:sl(it),callout:co(it)});addG(id,pGroup(it,"",tur))})});
 if(T.includes("remarketing")){let id=camp("remarketing","Site ziyaretçileri",{hub:"/"}),c=ctaLab();addG(id,{ad:"Site ziyaretçileri (son 30 gün)",url:"/",basliklar:uniq(fit([b,c,b&&b+" Resmî Site"],30)).join("\n"),uzunBasliklar:uniq(fit([first(state.oc_tagline)],90)).join("\n"),aciklamalar:uniq(fit([first(state.oc_tagline),now()],90)).join("\n")})}
 if(br.includes("brand")&&b){let lc=b.toLocaleLowerCase("tr"),c=ctaLab(),id=camp("search","Marka",{hub:"/",gerekce:"Marka aramalarını korur."});addG(id,{ad:b+" (Marka)",url:"/",yol:slug(b).slice(0,15),basliklar:uniq(fit([b,b+" Resmî Site",c],30)).join("\n"),aciklamalar:uniq(fit([first(state.oc_tagline),now()],90)).join("\n"),anahtarlar:`[${lc}]\n"${lc}"\n[${lc} iletişim]`})}
 let R=rivals();if(br.includes("competitor")&&R.length){let id=camp("search","Rakip",{hub:"/",not:"Rakip markası reklam metninde kullanılmaz; rakip adının anahtar kelime olarak kullanımı yayından önce hukuk onayından geçer."}),c=ctaLab();R.forEach(n=>{let lc=n.toLocaleLowerCase("tr");addG(id,{ad:n+" (Rakip)",url:"/",basliklar:uniq(fit([b,b&&b+" Resmî Site",c],30)).join("\n"),aciklamalar:uniq(fit([first(state.oc_tagline),now()],90)).join("\n"),anahtarlar:`"${lc}"\n[${lc}]`})})}
 /* çakışma: marka adı ve rakipler marka / rakip kampanyası dışındaki arama kampanyalarında negatif; kampanyalar arası odak kelimeleri; PMax'ta marka hariç tutma */
 let isB=k=>S[k].konu==="Marka"||S[k].konu==="Rakip",focus=k=>Object.values(S[k].g||{}).flatMap(g=>lines(g.anahtarlar).filter(x=>/^\[/.test(x)));
 Object.keys(S).forEach(k=>{let r=S[k],n=lines(r.negatifler);if(r.tur==="search"&&!isB(k)){if(br.includes("brand")&&b)n.push(`"${b.toLocaleLowerCase("tr")}"`);R.forEach(x=>n.push(`"${x.toLocaleLowerCase("tr")}"`));if(br.includes("cross_negative")&&st!=="single")Object.keys(S).filter(j=>j!==k&&S[j].tur==="search"&&!isB(j)).forEach(j=>focus(j).forEach(x=>n.push(x)))}
  if(n.length)r.negatifler=uniq(n).join("\n");if(r.tur==="pmax"){let m=lines(r.markaHaric);if(br.includes("brand")&&b)m.push(b);R.forEach(x=>m.push(x));if(m.length)r.markaHaric=uniq(m).join("\n")}});
 /* bütçe payı: boşsa marka %10, kalanı eşit */
 let ks=Object.keys(S),free=ks.filter(k=>!String(S[k].pay||"").trim());if(free.length===ks.length){let bk=ks.filter(k=>S[k].konu==="Marka"),rest=ks.filter(k=>!bk.includes(k)),bp=bk.length?10:0,each=rest.length?Math.floor((100-bp)/rest.length):0;bk.forEach(k=>S[k].pay=String(bp));rest.forEach((k,i)=>{S[k].pay=String(i===rest.length-1?100-bp-each*(rest.length-1):each);if(!S[k].gerekce)S[k].gerekce="Eşit dağıtım; ilk iki haftanın dönüşüm verisine göre güncelleyin."})}
 if(br.includes("account_negative")&&!String(state[NKEY]||"").trim()){let n=uniq(Object.values(state.ip_products||{}).flatMap(p=>Array.isArray(p.kw)?p.kw.filter(x=>x&&x.tur==="Negatif").map(x=>String(x.k).toLocaleLowerCase("tr")):[]).concat(["iş ilanı","maaş","staj","kurs","ücretsiz indir","pdf"]));state[NKEY]=n.join("\n")}
 Object.values(S).forEach(r=>{Object.keys(r).forEach(x=>{if(r[x]===""||r[x]==null)delete r[x]})});state[KEY]=S;commit(true);
 return `${made} kampanya ve ${gm} grup oluşturuldu${made||gm?"":" (hepsi zaten var)"}${msg.length?" — "+msg.join("; "):""}. Metinleri sayaçlara göre gözden geçirin; ölçüyü aşan aday metinler eklenmedi.`}
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".gaBox button");if(!b)return;if(!requireProject())return;
 if(b.hasAttribute("data-add")){let id=nextId(),S=store();S[id]={tur:types()[0],g:{}};state[KEY]=S;OPEN.add(id);commit(true);let x=rec(id);x=x&&x.querySelector('[data-m="konu"]');if(x)x.focus();return}
 if(b.hasAttribute("data-derive")){let m=derive(),p=document.querySelector(".gaBox .gaMsg");if(p)p.textContent=m;return}
 let k=JSON.parse(b.dataset.r||"null"),S=store();
 if(b.hasAttribute("data-del")){if(!confirm("Bu kampanya ve grupları silinsin mi?"))return;delete S[k];OPEN.delete(k);state[KEY]=S;commit(true)}
 else if(b.hasAttribute("data-gadd")){let r=S[k];if(!r)return;r.g=r.g||{};let gid=nextG(k,r);r.g[gid]={ad:""};state[KEY]=S;OPEN.add(k);GOPEN.add(gid);commit(true);let x=grec(gid);x=x&&x.querySelector('[data-m="ad"]');if(x)x.focus()}
 else if(b.hasAttribute("data-gdel")){let [cid,gid]=k,r=S[cid];if(!r||!r.g)return;if(!confirm("Bu grup silinsin mi?"))return;delete r.g[gid];GOPEN.delete(gid);state[KEY]=S;commit(true)}},true);
/* kural, özet */
function recSum(){let n=Object.keys(store()).length;return n?n+" kampanya":""}
function recRule(){let S=store(),ids=sorted(),gn=ids.reduce((a,i)=>a+Object.keys(S[i].g||{}).length,0),by=t=>ids.filter(i=>(S[i].tur||"search")===t).length,pay=ids.filter(i=>S[i].pay).map(i=>`${cname(S[i])} %${S[i].pay}`);
 return `Google Ads kayıtları: ${ids.length} kampanya, ${gn} grup (${Object.keys(TUR).filter(t=>by(t)).map(t=>`${TUR[t]} ${by(t)}`).join(", ")})${ids.length?`; kampanyalar: ${ids.slice(0,6).map(i=>cname(S[i])).join(", ")}${ids.length>6?` ve ${ids.length-6} kampanya daha`:""}`:""}. Kampanya adları Önek_Tür_Konu_YYYYAA kalıbındadır. Her grupta en az 3 başlık (≤ 30 karakter) ve 2 açıklama (≤ 90) bulunur; görünen yol iki parça, parça başına ≤ 15 karakterdir; Arama Ağı gruplarında anahtar kelimeler [tam] ve "sıralı" eşlemeyle yazılır.${pay.length?` Bütçe payları: ${pay.join(", ")}.`:""} Marka ve rakip adları marka / rakip kampanyası dışındaki arama kampanyalarında negatif, Maksimum Performans'ta marka hariç tutma listesindedir; rakip markası reklam metninde kullanılmaz. Kayıtlar plan dosyasının Google Ads bölümüne aktarılır.`}
window.REC[FID]={isset:()=>Object.keys(store()).length>0,rule:recRule,sum:recSum,box,
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Google Ads, Pazarlama › Reklam Ortak Kuralları › Reklam Kanalları'nda Google Ads seçiliyken kullanılır.</p><p><button type="button" class="btn dark" onclick="goToField('mk_ads','mk_ads_channels')">Kararı aç →</button></p></section>`};
/* plan dosyasına aktarım */
function exportAds(A){let S=store(),ids=sorted();if(!ids.length)return;
 A.kampanyalar=ids.map(id=>{let r=S[id],tur=r.tur||"search",o={id,ad:cname(r),tur,hub:r.hub||"/"},sl=lines(r.sitelinks).map(cells).filter(c=>c[0]);
  if(sl.length)o.sitelinks=sl.some(c=>c[2]||c[3])?sl.map(c=>[c[0],c[1]||"",c[2]||"",c[3]||""]):sl.map(c=>[c[0],c[1]||""]);else o.sitelinks=[];o.callout=lines(r.callout);
  if(r.snippetB&&lines(r.snippetD).length)o.snippet={baslik:r.snippetB,degerler:lines(r.snippetD)};if(lines(r.negatifler).length)o.negatifler=lines(r.negatifler);if(tur==="pmax"&&lines(r.markaHaric).length)o.markaHaric=lines(r.markaHaric);
  let p=parseFloat(String(r.pay||"").replace(",","."));if(p>=0&&String(r.pay||"").trim())o.butcePay=p;if(r.not)o.not=r.not;
  o.gruplar=Object.keys(r.g||{}).map(gid=>{let g=r.g[gid],x={id:gid,ad:g.ad||gid,url:g.url||r.hub||"/",yol:String(g.yol||"").split("/").map(y=>y.trim()).filter(Boolean).slice(0,2),basliklar:lines(g.basliklar),uzunBasliklar:lines(g.uzunBasliklar),aciklamalar:lines(g.aciklamalar)};
   if(tur==="search"){x.anahtarlar=lines(g.anahtarlar);if(lines(g.negatifler).length)x.negatifler=lines(g.negatifler)}else{x.temalar=lines(g.temalar);if(g.cta)x.cta=g.cta}return x});return o});
 let B=ids.filter(id=>String(S[id].pay||"").trim()).map(id=>[cname(S[id]),parseFloat(String(S[id].pay).replace(",","."))||0,S[id].gerekce||""]);if(B.length)A.butce=B;
 if(lines(state[NKEY]).length)A.negatifler=lines(state[NKEY]);if(ids.some(id=>(S[id].tur||"search")==="search"))A.editorCsv=true}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(B.ads&&shown(FI[FID]))exportAds(B.ads)}catch(e){console.error("Google Ads aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments);if(!shown(FI[FID]))return L;let S=store(),ids=Object.keys(S),c=`<button type="button" class="linkBtn" onclick="goToField('ip_gads','${FID}')">İçerik Planlama › Google Ads</button>`,G=ids.flatMap(i=>Object.values(S[i].g||{}).map(g=>[g,S[i].tur||"search"]));
 let ng=ids.filter(i=>!Object.keys(S[i].g||{}).length),few=G.filter(([g])=>lines(g.basliklar).length<3||lines(g.aciklamalar).length<2),over=G.filter(([g,t])=>["basliklar","uzunBasliklar","aciklamalar"].some(p=>lines(g[p]).some(x=>[...x].length>lim(p,t)[0]))),nk=G.filter(([g,t])=>t==="search"&&!lines(g.anahtarlar).length),
  tp=ids.reduce((a,i)=>a+(parseFloat(String(S[i].pay||"").replace(",","."))||0),0);
 if(ng.length)L.push(`${ng.length} Google Ads kampanyasında grup yok — ${c}.`);if(few.length)L.push(`${few.length} Google Ads grubunda 3 başlık / 2 açıklamadan az metin var — ${c}.`);if(over.length)L.push(`${over.length} Google Ads grubunda karakter sınırını aşan başlık ya da açıklama var — ${c}.`);
 if(nk.length)L.push(`${nk.length} Arama Ağı grubunda anahtar kelime yok — ${c}.`);let sd=G.filter(([g,t])=>t!=="search"&&lines(g.aciklamalar).length&&!lines(g.aciklamalar).some(x=>[...x].length<=60));if(sd.length)L.push(`${sd.length} Maksimum Performans / Yeniden Pazarlama grubunda 60 karakteri aşmayan kısa açıklama yok — ${c}.`);if(tp&&Math.round(tp)!==100)L.push(`Google Ads bütçe paylarının toplamı %${Math.round(tp*10)/10}; %100 olmalı — ${c}.`);return L}}
window.gaDerive=derive;window.GA={store,sorted,suggest};
})();
