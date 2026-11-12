/* Menü numaralandırması (2026-11-11, kullanıcı istekleri: "her bir maddeyi 1. / 1.1 / 1.1.1 şeklinde numaralandır" ve aynı gün
   "numaralandırma ana kategoriden başlamalı: 3. Pazarlama › 3.1. Strateji › 3.1.1 Pazarlama Planı ve Hedefler › 3.1.1.1 Plan
   Dönemi; numaralandırılacak menüler: Ortak Bilgiler, Kararlar, Pazarlama, SEO Denetimi, Google, Meta").
   Ana menü numarası modül şeridi sırasıdır (MT_NUM; şeritte Kararlar'ın kimliği "config"): 1 Ortak Bilgiler, 2 Kararlar, 3 Pazarlama, 4 SEO Denetimi, 5 Google,
   6 Meta, 7 Yapay Zekâ (2026-11-12). Gruplu alanda (Kararlar, Pazarlama) ana menü › grup › bölüm › karar = "3." › "3.1." › "3.1.1" › "3.1.1.1";
   tek gruplu alanda (grup başlığı gizli) ana menü › bölüm › karar = "6." › "6.1." › "6.1.1". İlk iki seviye noktayla biter
   (kullanıcının örneği). Numara: modül şeridi etiketi, sol menünün başlık şeridi (.areaBand; Kararlar'da şerit yoktu, eklenir),
   grup başlığı (.ngT), bölüm (.menuTitle), karar (.subText), sayfadaki bölüm ve karar başlıkları (titleNumber) ve ≤ 900 px çekmecedeki alt menü düğmeleri. Yalnız görünen öğeler
   sayılır (koşullu karar açılınca sonrakiler kayar). Yalnız görünüm: kurallar, prompt ve bölüm kodları (00–120) değişmez.
   renderSideNav sarmalanır (V26 sarmalayıcısından sonra). Kaynak docs/v26/v26-nav-numbers.js → docs/v26/menu_numara_ekle.py */
(function(){
const MT_NUM={common:1,project:2,marketing:3,audit:4,google:5,meta:6,ai:7};
window.MT_NUM=MT_NUM;
const fmt=p=>p.join(".")+(p.length<=2?".":""),NUM={sec:{},fld:{}};
function setNum(el,n){if(!el)return;let x=el.querySelector(":scope>.navNum");if(!n){if(x)x.remove();return}if(!x){x=document.createElement("span");x.className="navNum";el.prepend(x)}if(x.textContent!==n)x.textContent=n}
function navNumber(){if(typeof sideNav==="undefined"||!sideNav)return;NUM.sec={};NUM.fld={};
 // başlık şeridi: Kararlar'da yoksa ekle, hepsinde ana menü numarası
 let ca=typeof curArea==="function"?curArea():"project";
 if(ca==="project"&&!sideNav.querySelector(":scope>.areaBand")){let d=document.createElement("div"),b=document.createElement("b");d.className="areaBand nnBand";b.textContent="Kararlar";d.appendChild(b);sideNav.prepend(d)}
 let band=sideNav.querySelector(":scope>.areaBand b");if(band&&MT_NUM[ca])setNum(band,MT_NUM[ca]+".");
 const by={};sideNav.querySelectorAll(".navGroup").forEach(g=>{const a=g.dataset.area||"";(by[a]=by[a]||[]).push(g)});
 Object.entries(by).forEach(([a,gs])=>{const A=MT_NUM[a];if(!A)return;const three=gs.length>1;
  gs.forEach((g,gi)=>{const gp=three?[A,gi+1]:[A];if(three)setNum(g.querySelector(".ngHead .ngT"),fmt(gp));
   [...g.children].filter(x=>x.classList.contains("menuSection")).forEach((sec,si)=>{const sp=gp.concat(si+1);
    setNum(sec.querySelector(".menuParent .menuTitle"),fmt(sp));if(sec.dataset.section)NUM.sec[sec.dataset.section]=fmt(sp);
    sec.querySelectorAll(".submenu>.subItem").forEach((b,di)=>{const n=fmt(sp.concat(di+1));setNum(b.querySelector(".subText")||b,n);if(b.dataset.fid)NUM.fld[b.dataset.fid]=n})})})});titleNumber()}
/* Başlıklar (2026-11-11, kullanıcı isteği: "numaralandırmayı başlıkta da gösterelim fakat json dosyada mükerrerlik olmasın"):
   bölüm başlığı h1#title ve karar başlıkları .field[data-field-id]>h2 menüdeki numarayı ayrı bir span.navNum olarak alır;
   veri, etiket ve kayıt değişmez — JSON / kurallar / prompt numara içermez. Menüde olmayan alan (ör. Proje Adı) numarasız. */
function titleNumber(){if(typeof title!=="undefined"&&title&&typeof active!=="undefined")setNum(title,NUM.sec[active]);
 if(typeof fieldBox!=="undefined"&&fieldBox)fieldBox.querySelectorAll(".field[data-field-id]>h2").forEach(h=>setNum(h,NUM.fld[h.parentElement.dataset.fieldId]))}
function railNumber(){document.querySelectorAll("#modRail .mrBtn[data-mod]").forEach(b=>{let n=MT_NUM[b.dataset.mod==="config"?"project":b.dataset.mod],l=b.querySelector(":scope>span");if(n&&l)setNum(l,n+".")});
 [["sideCommonBtn","common"],["sideMkPlanBtn","marketing"],["sideAuditBtn","audit"],["sideGoogleBtn","google"],["sideMetaBtn","meta"],["sideAiBtn","ai"]].forEach(([id,a])=>{let b=document.getElementById(id);if(!b||b.querySelector(".navNum"))return;let t=b.firstChild,m=t&&t.nodeType===3&&t.nodeValue.match(/^([^A-Za-zÇĞİÖŞÜçğıöşü]+)(.*)$/s),x=document.createElement("span");x.className="navNum";x.textContent=MT_NUM[a]+".";if(m){t.nodeValue=m[2];b.insertBefore(document.createTextNode(m[1]),t);b.insertBefore(x,t)}else b.prepend(x)})}
window.navNumber=navNumber;
const _rsn=renderSideNav;renderSideNav=function(){const r=_rsn.apply(this,arguments);navNumber();return r};
const _rf=renderFields;renderFields=function(){const r=_rf.apply(this,arguments);titleNumber();return r};
if(typeof refreshField==="function"){const _rfx=refreshField;refreshField=function(){const r=_rfx.apply(this,arguments);titleNumber();return r}}
railNumber();navNumber();
})();
