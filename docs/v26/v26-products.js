/* 8.2 Ürün ve Hizmetler — kayıt düzenleyicisi (2026-11-15). Kullanıcı kararları: kalemlerin listesi Ortak Bilgiler › Ürün /
   Hizmet Listesi'nde kalır (oc_services, "Ad | sayfa adresi" satırları), 8. menüde her satır bir kayıttır ve yalnız ayrıntılar
   doldurulur; form Pazarlama › Tanıtım Sayfası Alanları (mk_prod_fields) seçimine göre şekillenir; ilk sürümde anahtar
   kelimeler, brief, sosyal medya metinleri ve tanıtım maili de var; alt menü yalnız Pazarlama › Ürün / Hizmet Tanıtımı
   (mk_prod_on) açıkken görünür.
   Değer: state.ip_products = {anahtar: {yol: metin, …, kw: [{k, tur, niyet, oncelik, durum, not, hacim, zorluk, cpc, guven}]}};
   anahtar kalem adından (prSlug). Metin alanları ham metin saklanır (satır listeleri "Başlık | açıklama", SSS "Soru | Cevap");
   plan dosyasına aktarımda şablonun biçimine çevrilir (urunler.liste[], KILAVUZ 18.10 / 18.16 / 18.17).
   Alan tipi "records": kayıt alanı çekirdeğine (v26-records.js) window.REC.ip_products ile kaydolur. Kaynak docs/v26/v26-products.{js,css}
   → docs/v26/urun_hizmet_ekle.py
   2026-11-20 (kullanıcı isteği: "8.2.1 maddesinde bu alanda kelime, tür, niyet gibi alanlar ayrı hücrelere girilsin"): "Yardımcı kelimeler"
   metin kutusu kalktı; her kelime tabloda ayrı satır (kelime, tür, niyet, öncelik, durum, hacim, KD, TBM, güven hücreleri). Eski
   yardimci metninin satırları bir kez tabloya “Yardımcı” türüyle taşınır (kwMig; tabloda olan kelime eklenmez). Hızlı giriş için
   "Toplu ekle" kutusu satırları ayrı kelime satırına çevirir. Plan dosyasındaki yardimci listesi tablodaki Yardımcı satırlarından türer. */
(function(){
const FID="ip_products";
if(!FI[FID])return;
const TYPES={service:["hizmet","Hizmet"],product:["urun","Ürün"],package:["paket","Paket"]};
/* Pazarlama › Tanıtım Sayfası Alanları → kayıt alanı: [yol, etiket, biçim, ölçü?]; şablonda karşılığı olmayanlar sayfa bölümü olur */
const PF={slogan:["slogan","Slogan","text",{c:[20,70]}],summary:["ozet","Özet","area",{w:[40,70],c:[250,450]}],value:["deger","Değer önerisi (tek cümle)","area"],
 audience:["hedefKitle","Hedef kitle (her satıra bir grup)","lines"],benefits:["faydalar","Faydalar (her satıra: Başlık | açıklama)","pairs"],
 features:["ozellikler","Özellikler (her satıra: Başlık | açıklama)","pairs"],process:["surec","Nasıl çalışır? (her adım: Başlık | açıklama)","pairs"],
 price_note:["fiyat","Fiyat açıklaması","text"],faq:["sss","Sık sorulan sorular (her satıra: Soru | Cevap)","pairs"],proof:["kanit","Sosyal kanıt (her satıra bir kanıt; yalnız yazılı onaylı)","lines"],
 problems:["x.problemler","Karşılaşılan problemler (her satıra bir problem)","lines"],scope:["x.kapsam","Kapsam, teknik özellikler ve sektörler","lines"],
 why_us:["x.nedenBiz","Neden biz? (her satıra bir avantaj)","lines"],certificates:["x.sertifikalar","Sertifika ve belgeler","lines"],stats:["x.rakamlar","Öne çıkan rakamlar (kaynağıyla)","lines"],
 cases:["x.vakalar","Başarı hikâyeleri / vaka çalışmaları","lines"],packages:["x.paketler","Paket karşılaştırması (her satıra: Paket | içerik)","lines"],download:["x.indirilebilir","İndirilebilir içerik","text"]};
const XH={problemler:"Karşılaşılan problemler",kapsam:"Kapsam, teknik özellikler ve sektörler",nedenBiz:"Neden biz?",sertifikalar:"Sertifika ve belgeler",rakamlar:"Öne çıkan rakamlar",vakalar:"Başarı hikâyeleri",paketler:"Paket karşılaştırması",indirilebilir:"İndirilebilir içerik"};
const KW={tur:["Odak","Yardımcı","Uzun kuyruk","Marka","Etiket","Negatif"],niyet:["Bilgi","Ticari","İşlem","Marka"],oncelik:["P1","P2","P3"],durum:["Hedefleniyor","Planlı","Önerilen","Bırakıldı"],guven:["Kesin","Olası","Tahmin"]};
const OPEN=new Set();
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const has=(id,x)=>{let v=sv(id);return Array.isArray(v)&&v.includes(x)};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
function prSlug(s){return norm(String(s||"")).replace(/[^a-z0-9]+/g,"-").replace(/^-+|-+$/g,"")||"kalem"}
/* Ortak Bilgiler › Ürün / Hizmet Listesi */
function items(){let seen={};return String(state.oc_services||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>{let p=x.split("|").map(y=>y.trim()),ad=p[0]||"",k=prSlug(ad),n=2;while(seen[k])k=prSlug(ad)+"-"+n++;seen[k]=1;return {k,ad,yol:p[1]||""}}).filter(x=>x.ad)}
function store(){let v=state[FID];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
/* eski "Yardımcı kelimeler" metni → tablo satırları (bir kez; kayıt yalnız proje hazırsa) */
function kwMig(){let S=store(),ch=0;Object.values(S).forEach(r=>{if(!r||typeof r!=="object"||r.yardimci===undefined)return;let L=Array.isArray(r.kw)?r.kw:[],have=new Set(L.map(x=>norm(String(x&&x.k||"").trim())));
 String(r.yardimci||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).forEach(k=>{let n=norm(k);if(!have.has(n)){have.add(n);L.push({k,tur:"Yardımcı"})}});if(L.length)r.kw=L;delete r.yardimci;ch=1});
 if(ch){state[FID]=S;if(typeof projectReady!=="function"||projectReady())save()}return ch}
function filled(r){return !!r&&Object.entries(r).some(([k,v])=>k==="kw"?Array.isArray(v)&&v.some(x=>x&&String(x.k||"").trim()):String(v||"").trim()!=="")}
function typesOn(){let t=sv("mk_prod_types");return Array.isArray(t)&&t.length?t.filter(x=>TYPES[x]):["service"]}
function mecralar(){let sel=sv("mk_platforms")||[],T=(typeof MKT!=="undefined"&&MKT.mecralar)||[];return T.filter(m=>sel.includes(m.k))}
/* ölçü */
const words=s=>String(s||"").trim().split(/\s+/).filter(Boolean).length;
function meter(v,o){if(!o)return "";let c=String(v||"").length,w=words(v),bad=(o.c&&c&&(c<o.c[0]||c>o.c[1]))||(o.w&&w&&(w<o.w[0]||w>o.w[1]))||(o.max&&c>o.max);
 let t=[o.c?`${c} karakter (hedef ${o.c[0]}–${o.c[1]})`:"",o.w?`${w} kelime (hedef ${o.w[0]}–${o.w[1]})`:"",o.max?`${c} / ${o.max} karakter`:""].filter(Boolean).join(" · ");return `<small class="prMeter${bad?" bad":""}" aria-live="polite">${t}${bad?" — ölçü dışı":""}</small>`}
const METER={"sayfa.h1":{c:[35,65]},"sayfa.metaTitle":{c:[45,60]},"sayfa.metaDesc":{c:[140,160]},"cta.m":{w:[3,6],c:[15,35]},"mail.konu":{max:60},"mail.onizleme":{max:110},"anahtar":{w:[2,5]}};
function inp(key,path,label,kind,val,o,ph){let a=`data-k="${E(path)}" data-r='${E(JSON.stringify(key))}' aria-label="${E(label)}"`,m=meter(val,o||METER[path]);
 let ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:4}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${m}</label>`}
function sel(key,path,label,opts,val){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-k="${E(path)}" data-r='${E(JSON.stringify(key))}' aria-label="${E(label)}">${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
const KWL={k:"Kelime",tur:"Tür",niyet:"Niyet",oncelik:"Öncelik",durum:"Durum",hacim:"Hacim",zorluk:"KD",cpc:"TBM",guven:"Güven"};
function kwTable(key,r){let L=Array.isArray(r.kw)?r.kw:[],q=E(JSON.stringify(key)),c=(f,h)=>`<label class="prKwC"><span class="prKwL" aria-hidden="true">${KWL[f]}</span>${h}</label>`,s=(n,f,v)=>c(f,`<select class="control" data-native data-kw="${n}" data-f="${f}" data-r='${q}' aria-label="Kelime ${n+1}: ${KWL[f]}"><option value="">—</option>${KW[f].map(x=>`<option${x===v?" selected":""}>${E(x)}</option>`).join("")}</select>`),
 t=(n,f,v,w,ph)=>c(f,`<input class="control" type="text" data-kw="${n}" data-f="${f}" data-r='${q}' value="${E(v||"")}" placeholder="${E(ph||"")}" aria-label="Kelime ${n+1}: ${KWL[f]}" style="${w?"max-width:"+w:""}">`);
 return `${L.length?"":`<p class="prHint">Henüz kelime yok. Her kelimeyi “+ Kelime ekle” ile ayrı satıra girin ya da aşağıdaki “Toplu ekle” kutusuna yapıştırın.</p>`}<div class="prKw" role="table" aria-label="Anahtar kelimeler"><div class="prKwH" role="row"><span>Kelime</span><span>Tür</span><span>Niyet</span><span>Öncelik</span><span>Durum</span><span>Hacim</span><span>KD</span><span>TBM</span><span>Güven</span><span></span></div>${L.map((x,n)=>`<div class="prKwR" role="row">${t(n,"k",x.k,"","Kelime")}${s(n,"tur",x.tur)}${s(n,"niyet",x.niyet)}${s(n,"oncelik",x.oncelik)}${s(n,"durum",x.durum)}${t(n,"hacim",x.hacim,"","—")}${t(n,"zorluk",x.zorluk,"","0–100")}${t(n,"cpc",x.cpc,"","—")}${s(n,"guven",x.guven)}<button type="button" class="prDel" data-kwdel="${n}" data-r='${q}' aria-label="Kelime ${n+1} satırını sil" title="Sil">×</button></div>`).join("")}</div><button type="button" class="prAdd" data-kwadd data-r='${q}'>+ Kelime ekle</button><details class="prKwBulk"><summary>Toplu ekle (her satıra bir kelime)</summary><textarea class="control" rows="4" data-kwbulk aria-label="Toplu kelime ekle: her satıra bir kelime" placeholder="kvkk uyum süreci&#10;verbis kaydı"></textarea><button type="button" class="prAdd" data-kwbulkadd data-r='${q}'>Satır olarak ekle</button><p class="prHint">Her satır “Yardımcı” türünde ayrı bir kelime satırı olur; tabloda zaten olan kelime yeniden eklenmez. Tür, niyet ve diğer hücreleri sonra tabloda seçin.</p></details><p class="prHint">Hacim, KD ve TBM yalnız araçtan (Anahtar Kelime Planlayıcı, Semrush, Ahrefs) alınır; tahmin yazılmaz, kaynağı Güven sütununda belirtilir.</p>`}
function recForm(it,r){let k=it.k,g=p=>r[p]||"",T=typesOn(),secs=[];
 let core=(T.length>1?sel(k,"kat","Kayıt türü",T.map(x=>[x,TYPES[x][1]]),g("kat")||T[0]):"")+inp(k,"sayfa.h1","Sayfa başlığı (H1)","text",g("sayfa.h1"))+inp(k,"sayfa.metaTitle","Meta title","text",g("sayfa.metaTitle"))+inp(k,"sayfa.metaDesc","Meta description","area",g("sayfa.metaDesc"))+
  inp(k,"cta.m","CTA metni","text",g("cta.m"),null,clean(lab(FI.oc_cta_primary,state.oc_cta_primary))||"Örn. Teklif alın")+inp(k,"cta.yol","CTA adresi","text",g("cta.yol"),null,String(state.oc_cta_url||"/iletisim"));
 secs.push(["Sayfa alanları ve CTA",core]);
 let pf=sv("mk_prod_fields")||[],tf=pf.filter(x=>PF[x]).map(x=>{let [p,l,kind,o]=PF[x];return inp(k,p,l,kind,g(p),o)}).join(""),skip=pf.filter(x=>!PF[x]&&x!=="cta").map(x=>clean(lab(FI.mk_prod_fields,x)));
 secs.push(["Tanıtım sayfası",tf?tf+(skip.length?`<p class="prHint">${E(skip.join(", "))} sayfa üretiminde kullanılır; burada metin girilmez.</p>`:""):`<p class="prHint">Pazarlama › Tanıtım Sayfası Alanları'nda metin alanı seçilmedi. <button type="button" class="linkBtn" onclick="goToField('mk_prod','mk_prod_fields')">Kararı aç →</button></p>`]);
 let kp=sv("mk_prod_keywords");
 if(kp!=="none")secs.push(["Anahtar kelimeler",inp(k,"anahtar","Odak anahtar kelime","text",g("anahtar"))+(kp==="main"?"":kwTable(k,r))]);
 secs.push(["Brief",inp(k,"brief.amac","Amaç","area",g("brief.amac"))+inp(k,"brief.icgoru","İçgörü","area",g("brief.icgoru"))+inp(k,"brief.sorun","Müşterinin sorunu","area",g("brief.sorun"))+inp(k,"brief.mesaj","Ana mesaj","area",g("brief.mesaj"))+inp(k,"brief.ton","Ton","text",g("brief.ton"))+inp(k,"brief.kanit","Kanıtlar (her satıra bir kanıt)","lines",g("brief.kanit"))+inp(k,"brief.yasak","Kullanılmayacaklar (her satıra bir madde)","lines",g("brief.yasak"))+inp(k,"brief.gorsel","Görsel yön","area",g("brief.gorsel"))]);
 let M=mecralar();secs.push(["Sosyal medya metinleri",M.length?M.map(m=>inp(k,"sosyal."+m.k,m.ad,"lines",g("sosyal."+m.k),m.max?{max:m.max}:null)).join(""):`<p class="prHint">Pazarlama › Sosyal Medya › Mecralar seçilmedi. <button type="button" class="linkBtn" onclick="goToField('mk_social','mk_platforms')">Kararı aç →</button></p>`]);
 if(sv("mk_prod_mail")===true)secs.push(["Tanıtım maili",inp(k,"mail.konu","Konu satırı","text",g("mail.konu"))+inp(k,"mail.onizleme","Ön izleme metni (konuyu tekrar etmez)","text",g("mail.onizleme"))+inp(k,"mail.selamlama","Selamlama","text",g("mail.selamlama"),null,"Merhaba {ad},")+inp(k,"mail.giris","Giriş","area",g("mail.giris"))+inp(k,"mail.maddeler","Maddeler (her satıra bir madde)","lines",g("mail.maddeler"))+inp(k,"mail.ctaM","Mail CTA metni","text",g("mail.ctaM"))+inp(k,"mail.ctaYol","Mail CTA adresi","text",g("mail.ctaYol"))+inp(k,"mail.kapanis","Kapanış","area",g("mail.kapanis"))]);
 secs.push(["Sorumlu ve not",inp(k,"sorumlu","Sorumlu","text",g("sorumlu"))+inp(k,"editorNotu","Editör notu","area",g("editorNotu"))]);
 return secs.map(([t,h])=>`<fieldset class="prSec"><legend>${E(t)}</legend>${h}</fieldset>`).join("")}
function fillPct(r){let n=0,c=0,P=["sayfa.h1","sayfa.metaTitle","sayfa.metaDesc","cta.m"].concat((sv("mk_prod_fields")||[]).filter(x=>PF[x]).map(x=>PF[x][0]));P.forEach(p=>{c++;if(String(r[p]||"").trim())n++});return c?Math.round(n/c*100):0}
function recBox(f){kwMig();let L=items(),S=store(),T=typesOn(),ks=new Set(L.map(x=>x.k)),orph=Object.keys(S).filter(k=>!ks.has(k)&&filled(S[k]));
 let head=`<div class="prHead"><p>Kalemler <b>Ortak Bilgiler › Ürün / Hizmet Listesi</b>'nden gelir; ad ve sayfa adresi orada düzenlenir.</p><button type="button" class="linkBtn" onclick="goToField('oc_market','oc_services')">Listeyi düzenle →</button></div>`;
 if(!L.length)return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox">${head}<p class="prEmpty">Ortak Bilgiler › Ürün / Hizmet Listesi boş. Önce kalemleri orada “Ad | sayfa adresi” biçiminde yazın.</p></div></div>`;
 let rows=L.map(it=>{let r=S[it.k]||{},kat=r.kat||T[0],pc=fillPct(r);return `<details class="prRec" data-key="${E(it.k)}"${OPEN.has(it.k)?" open":""}><summary><span class="prName">${E(it.ad)}</span><span class="prChip">${E((TYPES[kat]||TYPES.service)[1])}</span>${it.yol?`<code class="prPath">${E(it.yol)}</code>`:`<span class="prWarn">sayfa adresi yok</span>`}<span class="prPct${pc===100?" ok":""}" title="Sayfa ve tanıtım alanlarının doluluğu">%${pc}</span></summary><div class="prBody">${OPEN.has(it.k)?recForm(it,r):""}</div></details>`}).join("");
 let ob=orph.length?`<div class="prOrph"><h3>Eşleşmeyen kayıtlar</h3><p>Bu ayrıntılar artık listede olmayan bir kaleme ait (kalem yeniden adlandırılmış ya da silinmiş olabilir). Yeni kaleme bağlayın ya da silin.</p>${orph.map(k=>`<div class="prOrphR"><b>${E(k)}</b><select class="control" data-native data-orph='${E(JSON.stringify(k))}' aria-label="${E(k)} ayrıntılarını bağla"><option value="">Şu kaleme bağla…</option>${L.filter(x=>!filled(S[x.k])).map(x=>`<option value="${E(x.k)}">${E(x.ad)}</option>`).join("")}</select><button type="button" class="prDel" data-orphdel='${E(JSON.stringify(k))}' aria-label="${E(k)} ayrıntılarını sil" title="Sil">×</button></div>`).join("")}</div>`:"";
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox">${head}<div class="prList">${rows}</div>${ob}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt */
function rec(k){let S=store();if(!S[k])S[k]={};state[FID]=S;return S[k]}
function commit(k){let S=store();if(S[k]&&!filled(S[k]))delete S[k];if(Object.keys(S).length)state[FID]=S;else delete state[FID];faAuto(FID);save();renderRules();renderProgress();
 let el=document.querySelector(`.prRec[data-key="${CSS.escape(k)}"] .prPct`);if(el){let p=fillPct(store()[k]||{});el.textContent="%"+p;el.classList.toggle("ok",p===100)}}
function setPath(k,p,v){let r=rec(k);if(String(v).trim()==="")delete r[p];else r[p]=v;commit(k)}
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.classList.contains("prRec"))return;let k=d.dataset.key;if(d.open){OPEN.add(k);let b=d.querySelector(".prBody");if(b&&!b.children.length){let it=items().find(x=>x.k===k);if(it)b.innerHTML=recForm(it,store()[k]||{})}}else OPEN.delete(k)},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".prBox"))return;
 if(t.dataset.k){if(!requireProject()){refreshField(FID);return}let k=JSON.parse(t.dataset.r);setPath(k,t.dataset.k,t.value);let m=t.parentElement.querySelector(".prMeter"),o=METER[t.dataset.k]||(t.dataset.k.startsWith("sosyal.")?(()=>{let mm=mecralar().find(x=>"sosyal."+x.k===t.dataset.k);return mm&&mm.max?{max:mm.max}:null})():Object.values(PF).find(x=>x[0]===t.dataset.k)?.[3]);if(m&&o){let w=document.createElement("div");w.innerHTML=meter(t.value,o);m.replaceWith(w.firstChild)}
  if(t.dataset.k==="kat"){let d=t.closest(".prRec"),c=d&&d.querySelector(".prChip");if(c)c.textContent=(TYPES[t.value]||TYPES.service)[1]}return}
 if(t.dataset.kw!==undefined){if(!requireProject())return;let k=JSON.parse(t.dataset.r),r=rec(k),L=r.kw=Array.isArray(r.kw)?r.kw:[],n=+t.dataset.kw;L[n]=L[n]||{};if(String(t.value).trim()==="")delete L[n][t.dataset.f];else L[n][t.dataset.f]=t.value;commit(k)}},true);
document.addEventListener("change",e=>{let t=e.target;if(!t.closest||!t.closest(".prBox"))return;
 if(t.matches("select[data-k],select[data-kw]")){t.dispatchEvent(new Event("input",{bubbles:true}));return}
 if(t.dataset.orph){if(!requireProject()||!t.value)return;let from=JSON.parse(t.dataset.orph),S=store();S[t.value]=S[from];delete S[from];state[FID]=S;commit(t.value);refreshField(FID)}},true);
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".prBox button");if(!b)return;
 if(b.hasAttribute("data-kwadd")){if(!requireProject())return;let k=JSON.parse(b.dataset.r),r=rec(k);r.kw=(Array.isArray(r.kw)?r.kw:[]).concat([{}]);state[FID]=store();OPEN.add(k);refreshField(FID);let rr=document.querySelectorAll(`.prRec[data-key="${CSS.escape(k)}"] .prKwR`);if(rr.length)rr[rr.length-1].querySelector("input").focus()}
 else if(b.hasAttribute("data-kwbulkadd")){if(!requireProject())return;let ta=b.parentElement.querySelector("textarea[data-kwbulk]"),add=String(ta&&ta.value||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);if(!add.length){if(ta)ta.focus();return}
  let k=JSON.parse(b.dataset.r),r=rec(k),L=r.kw=Array.isArray(r.kw)?r.kw:[],have=new Set(L.map(x=>norm(String(x&&x.k||"").trim())));add.forEach(w=>{let n=norm(w);if(!have.has(n)){have.add(n);L.push({k:w,tur:"Yardımcı"})}});commit(k);OPEN.add(k);refreshField(FID)}
 else if(b.dataset.kwdel!==undefined){if(!requireProject())return;let k=JSON.parse(b.dataset.r),r=rec(k);(r.kw||[]).splice(+b.dataset.kwdel,1);if(!r.kw.length)delete r.kw;commit(k);OPEN.add(k);refreshField(FID)}
 else if(b.dataset.orphdel){if(!requireProject())return;let k=JSON.parse(b.dataset.orphdel),S=store();delete S[k];if(Object.keys(S).length)state[FID]=S;else delete state[FID];save();renderRules();renderProgress();refreshField(FID)}},true);
/* kayıt alanı çekirdeğine kayıt (v26-records.js: isset, kural, Yapılacaklar özeti, düzenleyici, kapalı alt menü) */
function recSum(){let S=store(),L=items().filter(x=>filled(S[x.k]));return L.length?L.map(x=>x.ad).join(", "):""}
function recRule(){let S=store(),L=items().filter(x=>filled(S[x.k])).map(x=>{let r=S[x.k],t=(TYPES[r.kat||typesOn()[0]]||TYPES.service)[1].toLocaleLowerCase("tr");return `${x.ad} (${t}${x.yol?", "+x.yol:""})`});
 return `Ürün ve hizmet kayıtları: ${L.join("; ")}. Kalemlerin adı ve sayfa adresi Ortak Bilgiler › Ürün / Hizmet Listesi'ndedir; her kaydın tanıtım metinleri, sayfa başlığı ve meta alanları, CTA'sı, anahtar kelimeleri, brief'i, sosyal medya metinleri ve tanıtım maili plan dosyasının Ürün ve Hizmetler bölümüne aktarılır. İçerik ve sayfa üretiminde bu kayıtlardaki değer önerisi, faydalar, kanıtlar ve fiyat ifadesi esas alınır; kayıtta olmayan rakam, fiyat ya da müşteri adı eklenmez.`}
window.REC[FID]={isset:()=>{let S=store();return Object.keys(S).some(k=>filled(S[k]))},rule:recRule,sum:recSum,box:recBox,
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Ürün ve Hizmetler, Pazarlama › Ürün / Hizmet Tanıtımı “Evet” iken kullanılır.</p><p><button type="button" class="btn dark" onclick="goToField('mk_prod','mk_prod_on')">Kararı aç →</button></p></section>`};
/* plan dosyasına aktarım */
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const pairs=s=>lines(s).map(x=>{let i=x.indexOf("|");return i<0?{b:x,m:""}:{b:x.slice(0,i).trim(),m:x.slice(i+1).trim()}});
function rid(L){let used={};return L.map(x=>{let b="U-"+(x.k.replace(/-/g,"").toUpperCase().replace(/[^A-Z0-9]/g,"").slice(0,4)||"KLM"),id=b,n=2;while(used[id])id=b+n++;used[id]=1;return id})}
function exportList(){kwMig();let L=items(),S=store(),T=typesOn(),ids=rid(L),M=mecralar();
 return L.map((it,n)=>{let r=S[it.k]||{},g=p=>String(r[p]||"").trim(),o={id:ids[n],kat:(TYPES[r.kat||T[0]]||TYPES.service)[0],ad:it.ad};if(it.yol)o.yol=it.yol;
  ["slogan","ozet","deger","fiyat"].forEach(p=>{if(g(p))o[p]=g(p)});
  if(g("hedefKitle"))o.hedefKitle=lines(r.hedefKitle);["faydalar","ozellikler","surec"].forEach(p=>{if(g(p))o[p]=pairs(r[p])});
  if(g("kanit"))o.kanit=lines(r.kanit);if(g("sss"))o.sss=pairs(r.sss).map(x=>[x.b,x.m]);
  if(g("cta.m")||g("cta.yol"))o.cta={m:g("cta.m"),yol:g("cta.yol")};
  let sy={};if(g("sayfa.h1"))sy.h1=g("sayfa.h1");if(g("sayfa.metaTitle"))sy.metaTitle=g("sayfa.metaTitle");if(g("sayfa.metaDesc"))sy.metaDesc=g("sayfa.metaDesc");
  let bl=Object.keys(XH).filter(x=>g("x."+x)).map(x=>({h2:XH[x],p:lines(r["x."+x])}));if(bl.length)sy.bolumler=bl;if(Object.keys(sy).length)o.sayfa=sy;
  if(g("anahtar"))o.anahtar=g("anahtar");{let y=(Array.isArray(r.kw)?r.kw:[]).filter(x=>x&&x.tur==="Yardımcı"&&x.durum!=="Bırakıldı"&&String(x.k||"").trim()).map(x=>String(x.k).trim());if(y.length)o.yardimci=y}
  let kw=(Array.isArray(r.kw)?r.kw:[]).filter(x=>x&&String(x.k||"").trim()).map(x=>{let y={k:String(x.k).trim()};["tur","niyet","oncelik","durum","not","guven"].forEach(z=>{if(x[z])y[z]=x[z]});["hacim","zorluk","cpc"].forEach(z=>{let v=String(x[z]||"").replace(/\./g,"").replace(",",".").trim();if(v&&Number.isFinite(+v))y[z]=+v});if(it.yol)y.sayfa=it.yol;return y});if(kw.length)o.kelimeler=kw;
  let br={};["amac","icgoru","sorun","mesaj","ton","gorsel"].forEach(z=>{if(g("brief."+z))br[z]=g("brief."+z)});["kanit","yasak"].forEach(z=>{if(g("brief."+z))br[z]=lines(r["brief."+z])});if(Object.keys(br).length)o.brief=br;
  let so={};M.forEach(m=>{if(g("sosyal."+m.k))so[m.k]=g("sosyal."+m.k)});if(Object.keys(so).length)o.sosyal=so;
  if(sv("mk_prod_mail")===true&&(g("mail.konu")||g("mail.giris"))){let s={v:"1.0",tarih:new Date().toISOString().slice(0,10),konu:g("mail.konu"),onizleme:g("mail.onizleme"),selamlama:g("mail.selamlama")||"Merhaba {ad},",giris:g("mail.giris"),maddeler:lines(r["mail.maddeler"]),ctaM:g("mail.ctaM")||g("cta.m"),ctaYol:g("mail.ctaYol")||g("cta.yol"),kapanis:g("mail.kapanis")};o.mail={surumler:[s]}}
  if(g("sorumlu"))o.sorumlu=g("sorumlu");if(g("editorNotu"))o.editorNotu=g("editorNotu");return o})}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(B.urunler){let L=exportList();if(L.length)B.urunler.liste=L;
  if(sv("mk_prod_mail")===true){let c=typeof ocContact==="function"?ocContact():{};B.urunler.mail=Object.assign({kampanya:"urun-tanitim",imza:{ad:(B.marka&&B.marka.ad)||"",unvan:"",telefon:c.tel||"",eposta:c.mail||""},ekler:[],abonelik:"Bu e-posta, ticari elektronik ileti onayınız kapsamında gönderilmiştir. Almak istemiyorsanız e-postadaki abonelikten çıkma bağlantısını kullanın."},B.urunler.mail||{})}}}catch(e){console.error("Ürün kayıtları aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments);if(sv("mk_prod_on")===true){let I=items(),S=store(),c=`<button type="button" class="linkBtn" onclick="goToField('ip_products','ip_products')">İçerik Planlama › Ürün ve Hizmetler</button>`;
  if(!I.length)L.push(`Ürün / hizmet tanıtımı açık ama Ortak Bilgiler › Ürün / Hizmet Listesi boş; plan sayfasının Ürün ve Hizmetler sekmesi boş gelir.`);
  else{let e=I.filter(x=>!filled(S[x.k]));if(e.length)L.push(`${e.length} ürün / hizmet kaleminin ayrıntısı girilmedi (${E(e.map(x=>x.ad).join(", "))}); plan sayfasında yalnız adıyla görünür — ${c}.`)}}return L}}
kwMig();
window.prItems=items;window.prExport=exportList;window.prKwMig=kwMig;
window.prIdMap=()=>{let L=items(),ids=rid(L),o={};L.forEach((x,n)=>o[x.k]=ids[n]);return o};
})();
