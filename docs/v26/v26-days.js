/* 8.6 Özel Günler (2026-11-15). Kullanıcı kararları: önem işaretleme, gün gizleme, marka günü ekleme, gün başına içerik önerisi
   notu; hareketli günlerin (Hicrî takvime bağlı bayram, kandil, arefe, aşure) tarihleri plan yılları için elle girilir — tarih
   uydurulmaz, girilmeyen gün takvime düşmez; liste plan dönemindeki günleri gösterir (Gün Türleri kararına göre süzülür).
   Alan ip_daylist type "records", showIf mk_days_on. Değer: state.ip_daylist = {m: {OG-…: {onem, gizli, oneri, t: {yıl: tarih},
   b: {yıl: bitiş}}}, x: {OG-M01: {ad, tarih, bitis, yillik, tur, ton, onem, oneri}}}. window.OG.options() 8.3 / 8.4 / 8.5'in özel
   gün seçeneklerini verir (gizlenen yok, marka günleri ve elle girilen tarihler var). Aktarım: ozelGunler.liste (gizlenenler
   çıkarılır, önem / öneri / tarihler işlenir, marka günleri eklenir), yillar ← plan yılları. Kaynak docs/v26/v26-days.{js,css}
   → docs/v26/ozel_gun_ekle.py */
(function(){
const FID="ip_daylist";
if(!FI[FID]||!window.REC||!window.BL)return;
let ADD=false,HID=false;
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const DRE=/^\d{4}-\d{2}-\d{2}$/;
const TUR=["Resmî tatil","Ulusal gün","Anma günü","Dinî / kültürel gün","Ticari özel gün","Meslek günü","Mali takvim","Hafta / dönem","Farkındalık günü","Sosyal medya / eğlence günü","Diğer"];
const TON={kutlama:"Kutlama (satışsız)",anma:"Anma (sade, satışsız)",saygi:"Saygı (satışsız)",bilgi:"Bilgi",satis:"Satış (kampanya uygun)",eglence:"Eğlence"};
const ONEM=["Yüksek","Orta","Düşük"];
const TT={official:["Resmî tatil"],national:["Ulusal gün"],memorial:["Anma günü"],religious:["Dinî / kültürel gün"],commercial:["Ticari özel gün","Sosyal medya / eğlence günü"],profession:["Meslek günü"],awareness:["Farkındalık günü","Hafta / dönem"],fiscal:["Mali takvim"]};
const AY=["Ocak","Şubat","Mart","Nisan","Mayıs","Haziran","Temmuz","Ağustos","Eylül","Ekim","Kasım","Aralık"],GUN=["Pazar","Pazartesi","Salı","Çarşamba","Perşembe","Cuma","Cumartesi"];
const pad=n=>String(n).padStart(2,"0"),iso=(y,m,d)=>y+"-"+pad(m)+"-"+pad(d);
function store(){let v=state[FID];v=v&&typeof v==="object"&&!Array.isArray(v)?v:{};v.m=v.m&&typeof v.m==="object"?v.m:{};v.x=v.x&&typeof v.x==="object"?v.x:{};return v}
function commit(redraw){let S=store();Object.keys(S.m).forEach(k=>{let r=S.m[k];if(r.t&&!Object.keys(r.t).length)delete r.t;if(r.b&&!Object.keys(r.b).length)delete r.b;if(!Object.keys(r).length)delete S.m[k]});
 if(Object.keys(S.m).length||Object.keys(S.x).length)state[FID]={...(Object.keys(S.m).length?{m:S.m}:{}),...(Object.keys(S.x).length?{x:S.x}:{})};else delete state[FID];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
function base(){let L=(MKT.ozelGunler&&MKT.ozelGunler.liste)||[],t=sv("mk_days_types");if(Array.isArray(t)&&t.length){let ok=t.flatMap(x=>TT[x]||[]);L=L.filter(x=>ok.includes(x.tur))}return L}
function years(){let P=BL.period();if(!P)return [new Date().getFullYear()];let a=+P[0].slice(0,4),b=+P[1].slice(0,4),Y=[];for(let y=a;y<=b;y++)Y.push(y);return Y}
function occ(g,y,m){let s=null,e=null;if(g.yillik&&g.ay&&g.gun){s=iso(y,g.ay,g.gun);if(g.bitisAy)e=iso(y,g.bitisAy,g.bitisGun||g.gun)}
 else if(g.kural){let k=g.kural,d=new Date(Date.UTC(y,k.ay-1,1)),off=(k.gun-d.getUTCDay()+7)%7;s=iso(y,k.ay,1+off+(k.hafta-1)*7)}
 else if(g.hareketli){s=(m&&m.t&&m.t[y])||(g.tarihler&&g.tarihler[y])||null;e=(m&&m.b&&m.b[y])||(g.bitisler&&g.bitisler[y])||null}return s?[s,e]:null}
function inP(s,e){let P=BL.period();if(!P)return true;return (e||s)>=P[0]&&s<=P[1]}
/* plan dönemindeki günler: [{id, ad, tur, ton, onem, s, e, custom, hidden, oneri}] + tarihi girilmemiş hareketli günler */
function rows(){let S=store(),R=[],miss=[];
 base().forEach(g=>{let m=S.m[g.id]||{};years().forEach(y=>{let o=occ(g,y,m);if(!o){if(g.hareketli)miss.push({g,y});return}if(!inP(o[0],o[1]))return;R.push({id:g.id,ad:g.ad,tur:g.tur,ton:g.ton,onem:m.onem||g.onem||"Düşük",s:o[0],e:o[1],hidden:!!m.gizli,oneri:m.oneri||"",resmi:!!g.resmi,mov:!!g.hareketli,y})})});
 Object.entries(S.x).forEach(([id,x])=>{if(!x.ad||!DRE.test(x.tarih||""))return;let ys=x.yillik?years():[+x.tarih.slice(0,4)];ys.forEach(y=>{let s=x.yillik?y+x.tarih.slice(4):x.tarih,e=x.bitis&&DRE.test(x.bitis)?(x.yillik?y+x.bitis.slice(4):x.bitis):null;if(inP(s,e))R.push({id,ad:x.ad,tur:x.tur||"Diğer",ton:x.ton||"bilgi",onem:x.onem||"Orta",s,e,custom:true,oneri:x.oneri||""})})});
 R.sort((a,b)=>a.s<b.s?-1:a.s>b.s?1:a.ad<b.ad?-1:1);return {R,miss}}
window.OG={options:()=>rows().R.filter(r=>!r.hidden).map(r=>[r.id,`${r.s} · ${r.ad}`])};
/* görünüm */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function dlab(s,e){let d=new Date(s+"T00:00:00Z"),t=`${d.getUTCDate()} ${AY[d.getUTCMonth()]} ${GUN[d.getUTCDay()]}`;if(e&&e!==s){let x=new Date(e+"T00:00:00Z");t+=` – ${x.getUTCDate()} ${AY[x.getUTCMonth()]}`}return t}
function row(r){let sel=`<select class="control ogOn" data-native data-on ${q(r.id)} aria-label="${E(r.ad)}: önem">${ONEM.map(o=>`<option${o===r.onem?" selected":""}>${o}</option>`).join("")}</select>`;
 return `<li class="ogR${r.hidden?" ogHid":""} og-${E(norm(r.onem))}"><span class="ogD">${E(dlab(r.s,r.e))}</span><span class="ogN"><b>${E(r.ad)}</b><span class="ogMeta">${E(r.tur)} · ${E(TON[r.ton]||r.ton||"")}${r.resmi?" · resmî tatil":""}${r.custom?" · marka günü":""}</span>
  <input class="control ogNote" type="text" data-not ${q(r.id)} value="${E(r.oneri)}" placeholder="İçerik önerisi / not" aria-label="${E(r.ad)}: içerik önerisi"></span>${sel}
  ${r.custom?`<button type="button" class="prDel" data-xdel ${q(r.id)} title="Sil" aria-label="${E(r.ad)} gününü sil">×</button>`:`<button type="button" class="prAdd ogHide" data-hide ${q(r.id)} aria-pressed="${r.hidden}">${r.hidden?"Geri al":"Gizle"}</button>`}</li>`}
function box(f){let {R,miss}=rows(),vis=R.filter(r=>!r.hidden),hid=R.filter(r=>r.hidden),P=BL.period(),S=store(),G={};
 vis.forEach(r=>{let k=r.s.slice(0,7);(G[k]=G[k]||[]).push(r)});
 let hi=vis.filter(r=>r.onem==="Yüksek").length,cx=Object.keys(S.x).length;
 let add=ADD?`<div class="blImp ogAdd"><div class="blGrid">${`<label class="prF"><span>Ad</span><input class="control" id="ogA_ad" type="text" placeholder="Örn. Kuruluş yıl dönümü"></label><label class="prF"><span>Tarih</span><input class="control" id="ogA_t" type="text" placeholder="YYYY-AA-GG"></label>`}</div><div class="blGrid"><label class="prF"><span>Bitiş (aralıksa)</span><input class="control" id="ogA_b" type="text" placeholder="YYYY-AA-GG"></label><label class="prF"><span>Tür</span><select class="control" data-native id="ogA_tur">${TUR.map(t=>`<option${t==="Diğer"?" selected":""}>${t}</option>`).join("")}</select></label></div><div class="blGrid"><label class="prF"><span>Ton</span><select class="control" data-native id="ogA_ton">${Object.entries(TON).map(([k,v])=>`<option value="${k}"${k==="kutlama"?" selected":""}>${E(v)}</option>`).join("")}</select></label><label class="prF"><span>Önem</span><select class="control" data-native id="ogA_on">${ONEM.map(o=>`<option${o==="Yüksek"?" selected":""}>${o}</option>`).join("")}</select></label></div><label class="prF"><span>İçerik önerisi</span><input class="control" id="ogA_o" type="text"></label><label class="blChk"><input type="checkbox" id="ogA_y" checked> Her yıl aynı gün tekrarlanır</label><div class="blAct"><button type="button" class="btn dark" data-xadd>Ekle</button><button type="button" class="btn" data-xcancel>Vazgeç</button></div><p class="prHint" id="ogA_m" aria-live="polite"></p></div>`:"";
 let mv=miss.length?`<details class="ogMiss"><summary>Tarihi girilmemiş hareketli günler (${miss.length})</summary><p class="prHint">Hicrî takvime bağlı günlerin tarihi her yıl değişir; Diyanet takvimine bakarak girin. Girilmeyen gün listede ve takvimde görünmez.</p>${miss.map(({g,y})=>`<div class="ogMR"><b>${E(g.ad)} (${y})</b><input class="control" type="text" data-mt="${y}" ${q(g.id)} placeholder="${y}-AA-GG" aria-label="${E(g.ad)} ${y} tarihi">${g.bitisler?`<input class="control" type="text" data-mb="${y}" ${q(g.id)} placeholder="Bitiş ${y}-AA-GG" aria-label="${E(g.ad)} ${y} bitiş tarihi">`:""}</div>`).join("")}</details>`:"";
 let hb=hid.length?`<details class="ogHidBox"${HID?" open":""}><summary>Gizlenen günler (${hid.length})</summary><ul class="ogL">${hid.map(row).join("")}</ul></details>`:"";
 let list=Object.keys(G).sort().map(k=>{let [y,m]=k.split("-");return `<section class="ogM"><h4>${AY[+m-1]} ${y} · ${G[k].length} gün</h4><ul class="ogL">${G[k].map(row).join("")}</ul></section>`}).join("");
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox ogBox"><div class="prHead"><p><b>${vis.length}</b> gün${P?` (${P[0]} – ${P[1]})`:" (plan dönemi girilmedi; bu yıl gösteriliyor)"} · ${hi} yüksek önemli${hid.length?` · ${hid.length} gizli`:""}${cx?` · ${cx} marka günü`:""}</p><div class="blAct"><button type="button" class="prAdd" data-xopen>+ Marka günü ekle</button></div></div>${add}${mv}${list||`<p class="prEmpty">Plan döneminde gösterilecek özel gün yok.</p>`}${hb}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* olaylar */
function mod(id){let S=store();S.m[id]=S.m[id]||{};state[FID]=S;return S.m[id]}
document.addEventListener("change",e=>{let t=e.target;if(!t.closest||!t.closest(".ogBox"))return;if(!requireProject()){refreshField(FID);return}let id=t.dataset.r&&JSON.parse(t.dataset.r);
 if(t.hasAttribute("data-on")){let S=store();if(S.x[id])S.x[id].onem=t.value;else{let g=base().find(x=>x.id===id),m=mod(id);if(g&&t.value===(g.onem||"Düşük"))delete m.onem;else m.onem=t.value}commit(true)}
 else if(t.dataset.mt||t.dataset.mb){let v=t.value.trim();if(v&&!DRE.test(v)){t.setAttribute("aria-invalid","true");return}let m=mod(id),k=t.dataset.mt?"t":"b",y=t.dataset.mt||t.dataset.mb;m[k]=m[k]||{};if(v)m[k][y]=v;else delete m[k][y];commit(!!t.dataset.mt&&!!v)}},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".ogBox")||!t.hasAttribute("data-not"))return;if(!requireProject())return;let id=JSON.parse(t.dataset.r),S=store(),v=t.value;
 if(S.x[id]){if(v)S.x[id].oneri=v;else delete S.x[id].oneri}else{let m=mod(id);if(v)m.oneri=v;else delete m.oneri}commit(false)},true);
document.addEventListener("toggle",e=>{if(e.target.classList&&e.target.classList.contains("ogHidBox"))HID=e.target.open},true);
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".ogBox button");if(!b)return;
 if(b.hasAttribute("data-hide")){if(!requireProject())return;let id=JSON.parse(b.dataset.r),m=mod(id);if(m.gizli)delete m.gizli;else m.gizli="1";commit(true)}
 else if(b.hasAttribute("data-xdel")){if(!requireProject())return;if(!confirm("Bu marka günü silinsin mi?"))return;let S=store();delete S.x[JSON.parse(b.dataset.r)];state[FID]=S;commit(true)}
 else if(b.hasAttribute("data-xopen")){ADD=true;refreshField(FID);let i=document.getElementById("ogA_ad");if(i)i.focus()}
 else if(b.hasAttribute("data-xcancel")){ADD=false;refreshField(FID)}
 else if(b.hasAttribute("data-xadd")){if(!requireProject())return;let g=id=>(document.getElementById(id)||{}).value||"",ad=g("ogA_ad").trim(),t=g("ogA_t").trim(),bt=g("ogA_b").trim(),msg=document.getElementById("ogA_m");
  if(!ad||!DRE.test(t)){if(msg)msg.textContent="Ad ve YYYY-AA-GG biçiminde tarih zorunlu.";return}if(bt&&(!DRE.test(bt)||bt<t)){if(msg)msg.textContent="Bitiş YYYY-AA-GG biçiminde ve başlangıçtan sonra olmalı.";return}
  let S=store(),n=Object.keys(S.x).map(k=>+((k.match(/^OG-M(\d+)$/)||[])[1]||0)).reduce((a,c)=>Math.max(a,c),0),id="OG-M"+pad(n+1);
  S.x[id]={ad,tarih:t,tur:g("ogA_tur")||"Diğer",ton:g("ogA_ton")||"kutlama",onem:g("ogA_on")||"Orta"};if(bt)S.x[id].bitis=bt;if(document.getElementById("ogA_y")&&document.getElementById("ogA_y").checked)S.x[id].yillik="1";if(g("ogA_o").trim())S.x[id].oneri=g("ogA_o").trim();
  state[FID]=S;ADD=false;commit(true)}},true);
/* kural, özet, kayıt */
function recSum(){let {R}=rows(),v=R.filter(r=>!r.hidden);return v.length?`${v.length} gün · ${v.filter(r=>r.onem==="Yüksek").length} yüksek önemli`:""}
function recRule(){let {R,miss}=rows(),v=R.filter(r=>!r.hidden),h=v.filter(r=>r.onem==="Yüksek"),S=store(),cx=Object.values(S.x).filter(x=>x.ad);
 return `Plan dönemindeki özel günler: ${v.length} gün${h.length?`; yüksek önemli: ${h.slice(0,15).map(r=>`${r.ad} (${r.s})`).join(", ")}${h.length>15?` ve ${h.length-15} gün daha`:""}`:""}${cx.length?`; marka günleri: ${cx.map(x=>x.ad).join(", ")}`:""}${R.length-v.length?`; markayla ilgisiz bulunup gizlenen ${R.length-v.length} gün içerik planına alınmaz`:""}. Her günün tonu içerik dilini belirler: kutlama, anma ve saygı tonlu günlerde satış mesajı kullanılmaz; günlere yazılan içerik önerileri brief'te esas alınır.${miss.length?` Tarihi girilmemiş ${miss.length} hareketli gün (Hicrî takvim) planlanmaz; tarih uydurulmaz.`:""}`}
window.REC[FID]={isset:()=>{let S=store();return Object.keys(S.m).length>0||Object.keys(S.x).length>0},rule:recRule,sum:recSum,box,
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Özel Günler, Pazarlama › Özel Günler › Özel Gün Takvimi “Evet” iken kullanılır.</p><p><button type="button" class="btn dark" onclick="goToField('mk_days','mk_days_on')">Kararı aç →</button></p></section>`};
/* plan dosyasına aktarım */
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(B.ozelGunler&&shown(FI[FID])){let O=B.ozelGunler,S=store();
  O.liste=(O.liste||[]).filter(g=>!(S.m[g.id]&&S.m[g.id].gizli)).map(g=>{let m=S.m[g.id];if(!m)return g;let x=Object.assign({},g);if(m.onem)x.onem=m.onem;if(m.oneri)x.oneri=m.oneri;if(m.t)x.tarihler=Object.assign({},g.tarihler,m.t);if(m.b)x.bitisler=Object.assign({},g.bitisler,m.b);return x});
  Object.entries(S.x).forEach(([id,x])=>{if(!x.ad||!DRE.test(x.tarih||""))return;let o={id,ad:x.ad,tur:TUR.includes(x.tur)?x.tur:"Diğer",ton:x.ton||"bilgi",onem:x.onem||"Orta"};if(x.oneri)o.oneri=x.oneri;
   if(x.yillik){o.yillik=true;o.ay=+x.tarih.slice(5,7);o.gun=+x.tarih.slice(8,10);if(x.bitis&&DRE.test(x.bitis)){o.bitisAy=+x.bitis.slice(5,7);o.bitisGun=+x.bitis.slice(8,10)}}
   else{let y=x.tarih.slice(0,4);o.hareketli=true;o.tarihler={[y]:x.tarih};if(x.bitis&&DRE.test(x.bitis))o.bitisler={[y]:x.bitis}}O.liste.push(o)});
  O.yillar=[...new Set((O.yillar||[]).concat(years()))].sort()}}catch(e){console.error("Özel gün aktarımı",e)}return B}}
window.ogRows=rows;
})();
