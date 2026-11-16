/* 8.3 Blog Yazıları — kayıt düzenleyicisi (2026-11-15). Kullanıcı kararları: kayıt derinliği plan + SEO alanları; kayıtlar elle
   eklenir ya da Claude'un ürettiği içerik planı (JSON) içe aktarılır (aynı kimlik güncellenir); ek alanlar yazı türü, ilgili ürün /
   hizmet, özel gün, yardımcı kelimeler / etiketler / 📥; alt menü Pazarlama › Blog Yayın Sıklığı "Blog yok" değilse görünür.
   Değer: state.ip_blogs = {id: {tarih, saat, kategori, grup, huni, baslik, anahtar, h2, link, slug, metaTitle, metaDesc, ozet, cta,
   tur, urun (8.2 kalem anahtarı), ozelGun (OG-…), yardimci, etiketler, dl}} — listeler satır satır metin. Kimlik B-001, B-002 …
   (kalıcı); seri no plan sayfasında tarih sırasından üretilir. Seçenekler Pazarlama kararlarından: kategori ← İçerik Kategorileri
   (mkPlanData ile aynı anahtarlar), huni ← Huni Modeli (AIDA / TOFU etiketleri F / D / K olarak saklanır; F / D / K / S'de S
   şablona huni.S olarak gider), yazı türü ← Yazı Türleri, ölçüler ← Meta Alan ve Başlık Ölçüleri, 📥 ← İndirilebilir İçerik,
   özel gün ← Özel Gün Takvimi (plan dönemindeki günler). Aktarım bloglar[] (KILAVUZ 18.4). Kaynak docs/v26/v26-blog.js →
   docs/v26/blog_ekle.py. Blog kaydında "Paylaşım taslakları oluştur" (İçerik Türetme Modeli her blogdan türeyen / karma iken; window.spDerive,
   v26-social.js); seçenek yardımcıları window.BL ile 8.4'e açılır. */
(function(){
const FID="ip_blogs";
if(!FI[FID]||!window.REC)return;
const OPEN=new Set();let IMP=false;
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const words=s=>String(s||"").trim().split(/\s+/).filter(Boolean).length;
const DRE=/^\d{4}-\d{2}-\d{2}$/,TRE=/^([01]\d|2[0-3]):[0-5]\d$/;
function store(){let v=state[FID];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
function filled(r){return !!r&&Object.values(r).some(v=>String(v||"").trim()!=="")}
/* ölçüler — Pazarlama › Meta Alan ve Başlık Ölçüleri */
const LIM={template:{baslik:{c:[35,65]},slug:{c:[20,60],w:[2,6]},metaTitle:{c:[45,60]},metaDesc:{c:[140,160]},ozet:{w:[40,70],c:[250,450]},cta:{w:[3,6],c:[15,35]},anahtar:{w:[2,5]}},
 chars:{baslik:{max:64},slug:{max:75},metaTitle:{c:[35,60]},metaDesc:{c:[120,160]},ozet:{w:[40,60]},cta:{w:[3,6],c:[15,35]},anahtar:{w:[1,3]}},
 brief:{baslik:{c:[35,65]},slug:{max:75},metaTitle:{max:55},metaDesc:{c:[150,155]},ozet:{w:[40,60]},cta:{w:[3,6],c:[15,35]},anahtar:{w:[2,5]}}};
LIM.chars_px=LIM.chars;
const lim=()=>LIM[sv("mk_blog_limits")]||LIM.template;
function meter(v,o){if(!o)return "";let c=String(v||"").length,w=words(v),bad=(o.c&&c&&(c<o.c[0]||c>o.c[1]))||(o.w&&w&&(w<o.w[0]||w>o.w[1]))||(o.max&&c>o.max);
 let t=[o.c?`${c} karakter (hedef ${o.c[0]}–${o.c[1]})`:"",o.max?`${c} / en çok ${o.max} karakter`:"",o.w?`${w} kelime (hedef ${o.w[0]}–${o.w[1]})`:""].filter(Boolean).join(" · ");return `<small class="prMeter${bad?" bad":""}" aria-live="polite">${t}${bad?" — ölçü dışı":""}</small>`}
/* seçenekler */
function cats(){let L=typeof mkCols==="function"&&sv("mk_categories")?mkCols(sv("mk_categories")):[],o=[],used={};
 L.forEach(c=>{if(!c[0])return;let k=mkSlug(c[0])||"kategori",x=k,i=2;while(used[x])x=k+"-"+i++;used[x]=1;o.push([x,c[0],norm(c[2]||"").includes("satis")])});
 if(!o.length){let K=(MKT.bos&&MKT.bos.kategoriler)||{};Object.keys(K).forEach(k=>o.push([k,K[k].ad,!!K[k].saticisiz]))}
 else if(sv("mk_days_on")===true&&!o.some(x=>x[2])&&!o.some(x=>x[0]==="ozel"))o.push(["ozel","Özel gün",true]);return o.map(x=>[x[0],x[1]])}
function hunis(){let m=sv("mk_funnel");if(m==="none")return null;
 return {aida:[["F","F — Dikkat ve İlgi"],["D","D — İstek"],["K","K — Eylem"]],tofu:[["F","F — TOFU"],["D","D — MOFU"],["K","K — BOFU"]],fdks:[["F","F — Farkındalık"],["D","D — Değerlendirme"],["K","K — Karar"],["S","S — Sadakat"]]}[m]||[["F","F — Farkındalık"],["D","D — Değerlendirme"],["K","K — Karar"]]}
function types(){let v=sv("mk_blog_types");return Array.isArray(v)?v.map(x=>[x,clean(lab(FI.mk_blog_types,x))]):[]}
function prods(){return typeof window.prItems==="function"&&sv("mk_prod_on")===true?window.prItems().map(x=>[x.k,x.ad]):[]}
const pad=n=>String(n).padStart(2,"0"),iso=(y,m,d)=>y+"-"+pad(m)+"-"+pad(d);
function period(){let s=typeof mkDate==="function"?mkDate(mkT("mk_period_start")):null,e=s&&mkEnd(s);return s&&e?[s.toISOString().slice(0,10),e.toISOString().slice(0,10)]:null}
function ogDate(g,y){if(g.yillik&&g.ay&&g.gun)return iso(y,g.ay,g.gun);if(g.kural){let k=g.kural,d=new Date(Date.UTC(y,k.ay-1,1)),off=(k.gun-d.getUTCDay()+7)%7;return iso(y,k.ay,1+off+(k.hafta-1)*7)}if(g.hareketli&&g.tarihler)return g.tarihler[y]||null;return null}
function days(){if(sv("mk_days_on")!==true||!MKT.ozelGunler)return [];if(window.OG&&typeof window.OG.options==="function")return window.OG.options();let P=period(),L=MKT.ozelGunler.liste||[];
 if(!P)return L.map(g=>[g.id,g.ad]);let y0=+P[0].slice(0,4),y1=+P[1].slice(0,4),o=[];L.forEach(g=>{for(let y=y0;y<=y1;y++){let d=ogDate(g,y);if(d&&d>=P[0]&&d<=P[1])o.push([g.id,`${d} · ${g.ad}`,d])}});return o.sort((a,b)=>a[2]<b[2]?-1:1).map(x=>[x[0],x[1]])}
/* biçim */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function inp(id,p,label,kind,val,o,ph){let a=`data-b="${E(p)}" ${q(id)} aria-label="${E(label)}"`,ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:4}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${meter(val,o)}</label>`}
function sel(id,p,label,opts,val,empty){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-b="${E(p)}" ${q(id)} aria-label="${E(label)}"><option value="">${E(empty||"Seçin")}</option>${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
function dateWarn(r){let w=[],P=period();if(r.tarih&&!DRE.test(r.tarih))w.push("Tarih YYYY-AA-GG biçiminde olmalı.");else if(r.tarih&&P&&(r.tarih<P[0]||r.tarih>P[1]))w.push(`Tarih plan döneminin (${P[0]} – ${P[1]}) dışında.`);if(r.saat&&!TRE.test(r.saat))w.push("Saat SS:DD biçiminde olmalı.");return w}
function form(id,r){let L=lim(),g=p=>r[p]||"",h=hunis(),T=types(),Pr=prods(),Dy=days(),secs=[];
 secs.push(["Plan",`<div class="blGrid">${inp(id,"tarih","Yayın tarihi","text",g("tarih"),null,"YYYY-AA-GG")}${inp(id,"saat","Saat","text",g("saat"),null,"SS:DD")}</div><small class="prMeter bad blDW" aria-live="polite">${E(dateWarn(r).join(" "))}</small>`+
  `<div class="blGrid">${sel(id,"kategori","Kategori",cats(),g("kategori"))}${h?sel(id,"huni","Huni",h,g("huni")):""}</div>`+
  inp(id,"grup","Başlık grubu (aynı konunun yazıları)","text",g("grup"),null,"Örn. Süreç Otomasyonu")+inp(id,"baslik","Başlık","text",g("baslik"),L.baslik)+inp(id,"anahtar","Odak anahtar kelime","text",g("anahtar"),L.anahtar)+
  inp(id,"h2","H2 planı (her satıra bir ara başlık; son madde SSS + CTA)","lines",g("h2"))+inp(id,"link","Hedef sayfa (CTA'nın gideceği adres)","text",g("link"),null,"/iletisim")]);
 secs.push(["SEO alanları",inp(id,"slug","Adres (slug)","text",g("slug"),L.slug,"kucuk-harf-tireli")+inp(id,"metaTitle","Meta title","text",g("metaTitle"),L.metaTitle)+inp(id,"metaDesc","Meta description","area",g("metaDesc"),L.metaDesc)+inp(id,"ozet","Sayfa özeti","area",g("ozet"),L.ozet)+inp(id,"cta","CTA önerisi","text",g("cta"),L.cta)]);
 let ex=(T.length?sel(id,"tur","Yazı türü",T,g("tur")):"")+(Pr.length?sel(id,"urun","İlgili ürün / hizmet",Pr,g("urun"),"İlişki yok"):"")+(Dy.length?sel(id,"ozelGun","Özel gün",Dy,g("ozelGun"),"Bağlı değil"):"")+
  inp(id,"yardimci","Yardımcı anahtar kelimeler (her satıra bir kelime)","lines",g("yardimci"))+inp(id,"etiketler","Etiketler (her satıra bir etiket)","lines",g("etiketler"))+
  (sv("mk_lead_magnet")===true?`<label class="blChk"><input type="checkbox" data-b="dl" ${q(id)}${g("dl")?" checked":""}> 📥 İndirilebilir içerik (e-posta karşılığı)</label>`:"");
 secs.push(["Bağlantılar ve etiketler",ex]);
 return secs.map(([t,x])=>`<fieldset class="prSec"><legend>${E(t)}</legend>${x}</fieldset>`).join("")+`<div class="blAct">${typeof window.spDerive==="function"&&["hub","mixed"].includes(sv("mk_derive"))?`<button type="button" class="prAdd" data-derive ${q(id)}>Paylaşım taslakları oluştur</button><small class="prHint blDerMsg" aria-live="polite"></small>`:""}${typeof window.mlDerive==="function"&&sv("mk_mail_on")===true?`<button type="button" class="prAdd" data-mlderive ${q(id)}>Mailing taslakları oluştur</button><small class="prHint blMlMsg" aria-live="polite"></small>`:""}<button type="button" class="prAdd blDelRec" data-del ${q(id)}>Yazıyı sil</button></div>`}
function sorted(){let S=store();return Object.keys(S).sort((a,b)=>{let x=(S[a].tarih||"9999")+(S[a].saat||""),y=(S[b].tarih||"9999")+(S[b].saat||"");return x<y?-1:x>y?1:a<b?-1:1})}
function fillPct(r){let P=["tarih","kategori","baslik","anahtar","h2","slug","metaTitle","metaDesc","ozet","cta"];if(hunis())P.push("huni");return Math.round(P.filter(p=>String(r[p]||"").trim()).length/P.length*100)}
function box(f){let S=store(),ids=sorted(),pre=String(mkT("mk_prefix")||"ÖNEK").toUpperCase(),hl=Object.fromEntries((hunis()||[]).map(x=>[x[0],x[0]]));
 let rows=ids.map((id,n)=>{let r=S[id],pc=fillPct(r);return `<details class="prRec" data-bid="${E(id)}"${OPEN.has(id)?" open":""}><summary><span class="prPath">${E(pre)}-BLG-${String(n+1).padStart(3,"0")}</span><span class="prPath">${E(r.tarih||"tarih yok")}${r.saat?" "+E(r.saat):""}</span>${r.huni&&hl[r.huni]?`<span class="prChip">${E(r.huni)}</span>`:""}<span class="prName">${E(r.baslik||"Başlıksız yazı")}</span><span class="prPct${pc===100?" ok":""}" title="Plan ve SEO alanlarının doluluğu">%${pc}</span></summary><div class="prBody">${OPEN.has(id)?form(id,r):""}</div></details>`}).join("");
 let imp=IMP?`<div class="blImp"><label class="prF"><span>Claude'un ürettiği blog planını yapıştırın (JSON dizi ya da {"bloglar": […]})</span><textarea class="control" rows="8" id="blImpTx" aria-label="İçe aktarılacak JSON"></textarea></label><div class="blAct"><button type="button" class="btn dark" data-impgo>İçe aktar</button><button type="button" class="btn" data-impcopy>Claude için talimatı kopyala</button><button type="button" class="btn" data-impx>Vazgeç</button></div><p class="prHint" id="blImpMsg" aria-live="polite"></p></div>`:"";
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox blBox"><div class="prHead"><p><b>${ids.length}</b> yazı · seri numaraları tarih sırasından üretilir (önek 8.1 Plan & Dönem'den).</p><div class="blAct"><button type="button" class="prAdd" data-add>+ Yazı ekle</button><button type="button" class="prAdd" data-imp>İçe aktar (JSON)</button></div></div>${imp}${ids.length?`<div class="prList">${rows}</div>`:`<p class="prEmpty">Henüz yazı yok. “+ Yazı ekle” ile tek tek ekleyin ya da Claude'un ürettiği planı içe aktarın.</p>`}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt işlemleri */
function nextId(){let S=store(),n=Object.keys(S).map(k=>+((k.match(/^B-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "B-"+String(n+1).padStart(3,"0")}
function commit(id,redraw){let S=store();if(id&&S[id]&&!filled(S[id]))delete S[id];if(Object.keys(S).length)state[FID]=S;else delete state[FID];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
function setv(id,p,v){let S=store();S[id]=S[id]||{};if(v===""||v===false)delete S[id][p];else S[id][p]=v;state[FID]=S;let k=S[id];commit(null);
 let d=document.querySelector(`.prRec[data-bid="${CSS.escape(id)}"]`);if(!d)return;let pc=d.querySelector(".prPct");if(pc){let x=fillPct(k);pc.textContent="%"+x;pc.classList.toggle("ok",x===100)}
 if(p==="baslik"){let n=d.querySelector(".prName");if(n)n.textContent=v||"Başlıksız yazı"}if(p==="tarih"||p==="saat"){let w=d.querySelector(".blDW");if(w)w.textContent=dateWarn(k).join(" ")}}
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.dataset.bid)return;let id=d.dataset.bid;if(d.open){OPEN.add(id);let b=d.querySelector(".prBody");if(b&&!b.children.length)b.innerHTML=form(id,store()[id]||{})}else OPEN.delete(id)},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".blBox")||!t.dataset.b)return;if(!requireProject()){refreshField(FID);return}let id=JSON.parse(t.dataset.r),v=t.type==="checkbox"?(t.checked?"1":""):t.value;setv(id,t.dataset.b,v);
 let m=t.parentElement.querySelector(".prMeter"),o=lim()[t.dataset.b];if(m&&o){let w=document.createElement("div");w.innerHTML=meter(t.value,o);m.replaceWith(w.firstChild)}},true);
document.addEventListener("change",e=>{let t=e.target;if(t.closest&&t.closest(".blBox")&&t.matches("select[data-b],input[type=checkbox][data-b]"))t.dispatchEvent(new Event("input",{bubbles:true}))},true);
/* içe aktarma */
const AL=["tarih","saat","kategori","grup","huni","baslik","anahtar","link","slug","metaTitle","metaDesc","ozet","cta","tur","ozelGun"];
function imp(txt){let d;try{d=JSON.parse(txt)}catch(e){return "JSON okunamadı: "+e.message}let L=Array.isArray(d)?d:d&&Array.isArray(d.bloglar)?d.bloglar:null;if(!L)return "Bir dizi ya da {\"bloglar\": […]} bekleniyor.";
 let S=store(),add=0,upd=0,skip=0,pm={},pi=typeof window.prIdMap==="function"?window.prIdMap():{};Object.entries(pi).forEach(([k,v])=>pm[v]=k);
 L.forEach(x=>{if(!x||typeof x!=="object"){skip++;return}let id=String(x.id||"").trim();if(!/^[A-Za-z0-9_-]{1,40}$/.test(id))id="";
  if(!(x.baslik||x.title)&&!(id&&S[id])){skip++;return}
  let r={};AL.forEach(k=>{if(x[k]!=null&&String(x[k]).trim())r[k]=String(x[k]).trim()});if(!r.baslik&&x.title)r.baslik=String(x.title);
  ["h2","yardimci","etiketler"].forEach(k=>{if(Array.isArray(x[k]))r[k]=x[k].map(String).join("\n");else if(x[k])r[k]=String(x[k])});
  if(!r.tur&&x.alanlar&&x.alanlar.tip)r.tur=String(x.alanlar.tip);if(r.tur){let t=types().find(([v,l])=>v===r.tur||norm(l)===norm(r.tur));if(t)r.tur=t[0];else delete r.tur}
  if(x.urun){let k=pm[x.urun]||x.urun;if(prods().some(p=>p[0]===k))r.urun=k}if(x.dl===true||x.dl==="1")r.dl="1";
  if(r.tarih&&!DRE.test(r.tarih)){skip++;return}if(id&&S[id]){Object.assign(S[id],r);upd++}else{let n=id&&!S[id]?id:nextId();S[n]=r;state[FID]=S;add++}});
 commit(null,true);return `${add} yazı eklendi, ${upd} yazı güncellendi${skip?`, ${skip} kayıt atlandı (başlık ya da geçerli tarih yok)`:""}.`}
function impPrompt(){let c=cats().map(x=>x[0]+" ("+x[1]+")").join(", "),h=(hunis()||[]).map(x=>x[1]).join(", "),t=types().map(x=>x[0]+" ("+x[1]+")").join(", "),p=typeof window.prIdMap==="function"?Object.entries(window.prIdMap()).map(([k,v])=>v+" ("+((window.prItems().find(i=>i.k===k)||{}).ad||k)+")").join(", "):"",P=period(),L=lim();
 return `Blog içerik planını yalnız JSON olarak ver (açıklama yazma): {"bloglar": [ … ]}. Her yazı bir nesne:
- id: kalıcı kimlik (B-001, B-002 …; mevcut yazıyı güncelliyorsan onun kimliği)
- tarih: YYYY-AA-GG${P?` (${P[0]} – ${P[1]} arasında)`:""}, saat: SS:DD
- kategori: şu anahtarlardan biri: ${c||"—"}
${h?`- huni: F, D ya da K${h.includes("S —")?" ya da S":""} (${h}); aynı başlık grubunun yazıları F → D → K sırasıyla yayımlanır\n`:""}- grup: başlık grubu (aynı konunun yazıları için ortak ad)
- baslik (${L.baslik.c?L.baslik.c.join("–")+" karakter":"en çok "+L.baslik.max+" karakter"}), anahtar (odak anahtar kelime), h2 (ara başlık dizisi; son madde "Sık Sorulan Sorular + CTA"), link (CTA'nın gideceği sayfa)
- slug (küçük harf, tireli, Türkçe karaktersiz), metaTitle, metaDesc, ozet, cta (3–6 kelime, fiille biter)
${t?`- tur: ${t}\n`:""}${p?`- urun: ilgili ürün / hizmet kimliği: ${p}\n`:""}- yardimci (dizi), etiketler (dizi)${sv("mk_lead_magnet")===true?", dl (indirilebilir içerikse true)":""}
Rakam, fiyat ve müşteri adı uydurma; kaynak gerektiren iddiayı yazma.`}
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".blBox button");if(!b)return;
 if(b.hasAttribute("data-add")){if(!requireProject())return;let id=nextId(),S=store(),P=period();S[id]={tarih:P?P[0]:""};if(!S[id].tarih)delete S[id].tarih;S[id].baslik="";state[FID]=S;OPEN.add(id);commit(null);refreshField(FID);let d=document.querySelector(`.prRec[data-bid="${CSS.escape(id)}"] [data-b="baslik"]`);if(d)d.focus()}
 else if(b.hasAttribute("data-del")){if(!requireProject())return;let id=JSON.parse(b.dataset.r);if(!confirm("Bu yazı kaydı silinsin mi?"))return;let S=store();delete S[id];OPEN.delete(id);state[FID]=S;commit(null,true)}
 else if(b.hasAttribute("data-derive")){if(!requireProject())return;let id=JSON.parse(b.dataset.r),m=window.spDerive(id),x=b.parentElement.querySelector(".blDerMsg");if(x)x.textContent=m}
 else if(b.hasAttribute("data-mlderive")){if(!requireProject())return;let id=JSON.parse(b.dataset.r),m=window.mlDerive(id),x=b.parentElement.querySelector(".blMlMsg");if(x)x.textContent=m}
 else if(b.hasAttribute("data-imp")){IMP=true;refreshField(FID);let t=document.getElementById("blImpTx");if(t)t.focus()}
 else if(b.hasAttribute("data-impx")){IMP=false;refreshField(FID)}
 else if(b.hasAttribute("data-impgo")){if(!requireProject())return;let t=document.getElementById("blImpTx"),msg=imp(t?t.value:"");IMP=!/eklendi/.test(msg);if(!IMP)refreshField(FID);let m=document.getElementById("blImpMsg");if(m)m.textContent=msg;else{let x=document.querySelector(".blBox .prHead p");if(x)x.insertAdjacentText("beforeend"," — "+msg)}}
 else if(b.hasAttribute("data-impcopy")){let x=impPrompt();(navigator.clipboard?navigator.clipboard.writeText(x):Promise.reject()).then(()=>{let m=document.getElementById("blImpMsg");if(m)m.textContent="Talimat kopyalandı; Claude'a yapıştırın, gelen JSON'u buraya yapıştırın."},()=>{let t=document.getElementById("blImpTx");if(t){t.value=x;t.select()}})}},true);
/* kural, özet, kayıt */
function recSum(){let n=Object.keys(store()).length;return n?n+" yazı":""}
function recRule(){let S=store(),ids=sorted(),d=ids.map(i=>S[i].tarih).filter(Boolean),T=ids.map(i=>S[i].baslik).filter(Boolean);
 return `Blog yazısı kayıtları: ${ids.length} yazı${d.length?` (${d[0]} – ${d[d.length-1]})`:""}${T.length?`; başlıklar: ${T.slice(0,12).join("; ")}${T.length>12?` ve ${T.length-12} yazı daha`:""}`:""}. Her kaydın tarihi, kategorisi, hunisi, odak anahtar kelimesi, H2 planı ve SEO alanları plan dosyasının Konular › Blog yazıları bölümüne aktarılır; yazının gövdesi bu H2 planına ve SEO alanlarına uyularak üretilir, iç bağlantı yalnız yayımlanmış yazılara verilir.`}
window.REC[FID]={isset:()=>Object.keys(store()).some(k=>filled(store()[k])),rule:recRule,sum:recSum,box,hide:()=>state.mk_blog_cadence==="none",
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Blog Yazıları, Pazarlama › İçerik Stratejisi › Blog Yayın Sıklığı “Blog yok” seçiliyken kullanılmaz.</p><p><button type="button" class="btn dark" onclick="goToField('mk_content','mk_blog_cadence')">Kararı aç →</button></p></section>`};
/* plan dosyasına aktarım */
function exportList(B){let S=store(),pm=typeof window.prIdMap==="function"?window.prIdMap():{},K=Object.keys(B.kategoriler||{}),og=B.ozelGunler?new Set((B.ozelGunler.liste||[]).map(x=>x.id)):null,usedS=false;
 let L=sorted().map(id=>{let r=S[id],o={id};["tarih","saat"].forEach(k=>{if(r[k])o[k]=r[k]});if(r.kategori&&K.includes(r.kategori))o.kategori=r.kategori;if(r.grup)o.grup=r.grup;
  if(r.huni&&hunis()){o.huni=r.huni;if(r.huni==="S")usedS=true}if(r.dl)o.dl=true;["baslik","slug","anahtar","metaTitle","metaDesc","ozet","cta","link"].forEach(k=>{if(r[k])o[k]=r[k]});
  ["yardimci","etiketler","h2"].forEach(k=>{if(r[k])o[k]=lines(r[k])});if(r.tur){let t=types().find(x=>x[0]===r.tur);if(t)o.alanlar={tip:t[1]}}
  if(r.urun&&B.urunler&&pm[r.urun])o.urun=pm[r.urun];if(r.ozelGun&&og&&og.has(r.ozelGun))o.ozelGun=r.ozelGun;return o});
 if(usedS)B.huni=Object.assign({},B.huni,{S:"Sadakat"});return L}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(shown(FI[FID])){let L=exportList(B);if(L.length)B.bloglar=L}}catch(e){console.error("Blog kayıtları aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments);if(!shown(FI[FID]))return L;let S=store(),ids=Object.keys(S),c=`<button type="button" class="linkBtn" onclick="goToField('ip_blog','${FID}')">İçerik Planlama › Blog Yazıları</button>`;
 let nt=ids.filter(i=>!S[i].baslik),nd=ids.filter(i=>!S[i].tarih||!DRE.test(S[i].tarih)),P=period(),out=P?ids.filter(i=>S[i].tarih&&DRE.test(S[i].tarih)&&(S[i].tarih<P[0]||S[i].tarih>P[1])):[];
 if(nt.length)L.push(`${nt.length} blog yazısının başlığı yok — ${c}.`);if(nd.length)L.push(`${nd.length} blog yazısının tarihi yok ya da YYYY-AA-GG biçiminde değil; plan sayfasında tarihsiz görünür — ${c}.`);if(out.length)L.push(`${out.length} blog yazısının tarihi plan döneminin dışında; dönem süzgecinde hiçbir döneme düşmez — ${c}.`);return L}}
window.blExport=()=>exportList(mkPlanData());window.blImport=imp;window.blPrompt=impPrompt;
/* 8.4 Sosyal Paylaşımlar ortak seçenekleri buradan kullanır */
window.BL={cats,hunis,days,period,prods,meter,store,sorted,types,open:id=>OPEN.add(id)};
})();
