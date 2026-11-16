/* 8.7 Mailing — kayıt düzenleyicisi (2026-11-15). Kullanıcı kararları: plan + içerik (konu satırı ≤ 60, ön izleme ≤ 110,
   selamlama, giriş, alt başlıklı bölümler, CTA); blogdan türetme başlık grubundan 2'li (1. Tanıtım: grubun F yazısından bir gün
   sonra, yazıya yönlendirir; 2. Karar: K yazısından bir gün sonra, en az 7 gün arayla, teklif / form); ekler ikinci CTA, A/B konu
   satırı ve ön izleme (Pazarlama › A/B Testi'nde seçiliyse; plana mailing.notlar olarak gider), ilgili bağlantılar. Alan ip_mails
   type "records", showIf mk_mail_on. Değer: state.ip_mails = {M-001: {tarih, saat, tur, sira, kategori, segment, konu, blog, urun,
   subject, preheader, subjectB, preheaderB, selam, giris, bolumler ("Alt başlık | metin" satırları), ctaM, ctaYol, ikinciM,
   ikinciYol, ilgili ("Metin | /yol" satırları)}}. Seri no <önek>-ML-NNN yalnız gösterilir. Aktarım mailing.liste[] (KILAVUZ 18.9).
   Kaynak docs/v26/v26-mailing.{js,css} → docs/v26/mailing_ekle.py */
(function(){
const FID="ip_mails";
if(!FI[FID]||!window.REC||!window.BL)return;
const BL=window.BL,OPEN=new Set();let IMP=false;
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const pairs=s=>lines(s).map(x=>{let i=x.indexOf("|");return i<0?{h:x,m:""}:{h:x.slice(0,i).trim(),m:x.slice(i+1).trim()}});
const DRE=/^\d{4}-\d{2}-\d{2}$/,TRE=/^([01]\d|2[0-3]):[0-5]\d$/;
function store(){let v=state[FID];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
function filled(r){return !!r&&Object.values(r).some(v=>String(v||"").trim()!=="")}
function types(){let v=sv("mk_mail_types");return Array.isArray(v)?v.map(x=>[x,clean(lab(FI.mk_mail_types,x))]):[]}
function ab(){let v=sv("mk_mail_ab");return Array.isArray(v)?v:[]}
function blogs(){let S=BL.store();return BL.sorted().map(id=>[id,`${id} · ${S[id].tarih||"tarih yok"} · ${S[id].baslik||"Başlıksız"}`])}
function blogUrl(r){let y={blog:"/blog/{slug}/",root:"/{slug}/"}[sv("mk_blog_path")]||"/blog/{slug}/";return r&&r.slug?y.replace("{slug}",r.slug):""}
const SIRA=[["1","1 — Tanıtım"],["2","2 — Karar"]];
/* biçim */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function inp(id,p,label,kind,val,o,ph){let a=`data-m="${E(p)}" ${q(id)} aria-label="${E(label)}"`,ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:5}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${o?BL.meter(val,o):""}</label>`}
function sel(id,p,label,opts,val,empty){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-m="${E(p)}" ${q(id)} aria-label="${E(label)}"><option value="">${E(empty||"Seçin")}</option>${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
function warn(r){let w=[],P=BL.period();if(r.tarih&&!DRE.test(r.tarih))w.push("Tarih YYYY-AA-GG biçiminde olmalı.");else if(r.tarih&&P&&(r.tarih<P[0]||r.tarih>P[1]))w.push(`Tarih plan döneminin (${P[0]} – ${P[1]}) dışında.`);if(r.saat&&!TRE.test(r.saat))w.push("Saat SS:DD biçiminde olmalı.");
 if(r.subject&&r.preheader&&r.preheader.toLocaleLowerCase("tr").startsWith(r.subject.toLocaleLowerCase("tr").slice(0,25)))w.push("Ön izleme konu satırını tekrar ediyor.");return w}
function form(id,r){let g=p=>r[p]||"",T=types(),Bl=blogs(),Pr=BL.prods(),A=ab(),multi=sv("mk_mail_layout")==="multi";
 let plan=`<div class="blGrid">${inp(id,"tarih","Gönderim tarihi","text",g("tarih"),null,"YYYY-AA-GG")}${inp(id,"saat","Saat","text",g("saat"),null,"SS:DD")}</div><small class="prMeter bad mlW" aria-live="polite">${E(warn(r).join(" "))}</small>`+
  `<div class="blGrid">${T.length?sel(id,"tur","Mail türü",T,g("tur")):""}${sel(id,"sira","Sıra",SIRA,g("sira"),"—")}</div><div class="blGrid">${sel(id,"kategori","Kategori",BL.cats(),g("kategori"))}${inp(id,"segment","Segment (alıcı grubu)","text",g("segment"),null,"Örn. KOBİ sahipleri, izinli aboneler")}</div>`+
  inp(id,"konu","Konu / başlık grubu","text",g("konu"))+(Bl.length?sel(id,"blog","Bağlı blog yazısı",Bl,g("blog"),"Bağlı değil"):"")+(Pr.length?sel(id,"urun","İlgili ürün / hizmet",Pr,g("urun"),"İlişki yok"):"");
 let met=inp(id,"subject","Konu satırı","text",g("subject"),{max:60})+inp(id,"preheader","Ön izleme metni (konuyu tekrar etmez)","text",g("preheader"),{max:110})+
  (A.includes("subject")?inp(id,"subjectB","Konu satırı — B sürümü (A/B testi)","text",g("subjectB"),{max:60}):"")+(A.includes("preheader")?inp(id,"preheaderB","Ön izleme — B sürümü (A/B testi)","text",g("preheaderB"),{max:110}):"")+
  inp(id,"selam","Selamlama","text",g("selam"),null,"Merhaba {ad},")+inp(id,"giris","Giriş","area",g("giris"))+
  inp(id,"bolumler",multi?"Bölümler (her satıra: Alt başlık | metin; çok bölümlü bülten)":"Bölümler (her satıra: Alt başlık | metin; tek konu — 1–3 bölüm)","lines",g("bolumler"))+
  `<div class="blGrid">${inp(id,"ctaM","CTA metni","text",g("ctaM"),{w:[2,6]})}${inp(id,"ctaYol","CTA adresi","text",g("ctaYol"),null,"/blog/… ya da /iletisim")}</div>`+
  `<div class="blGrid">${inp(id,"ikinciM","İkinci CTA metni (isteğe bağlı)","text",g("ikinciM"))}${inp(id,"ikinciYol","İkinci CTA adresi","text",g("ikinciYol"))}</div>`+
  inp(id,"ilgili","İlgili bağlantılar (her satıra: Metin | /yol; en çok 3)","lines",g("ilgili"));
 return [["Plan",plan],["Metin",met]].map(([t,x])=>`<fieldset class="prSec"><legend>${E(t)}</legend>${x}</fieldset>`).join("")+`<div class="blAct"><button type="button" class="prAdd blDelRec" data-del ${q(id)}>Maili sil</button></div>`}
function sorted(){let S=store();return Object.keys(S).sort((a,b)=>{let x=(S[a].tarih||"9999")+(S[a].saat||""),y=(S[b].tarih||"9999")+(S[b].saat||"");return x<y?-1:x>y?1:a<b?-1:1})}
function fillPct(r){let P=["tarih","subject","preheader","giris","bolumler","ctaM","ctaYol","segment"];return Math.round(P.filter(p=>String(r[p]||"").trim()).length/P.length*100)}
function box(f){let S=store(),ids=sorted(),pre=String(mkT("mk_prefix")||"ÖNEK").toUpperCase(),T=Object.fromEntries(types());
 let rows=ids.map((id,n)=>{let r=S[id],pc=fillPct(r);return `<details class="prRec" data-mid="${E(id)}"${OPEN.has(id)?" open":""}><summary><span class="prPath">${E(pre)}-ML-${String(n+1).padStart(3,"0")}</span><span class="prPath">${E(r.tarih||"tarih yok")}${r.saat?" "+E(r.saat):""}</span>${r.sira?`<span class="prChip">${r.sira==="2"?"2 · Karar":"1 · Tanıtım"}</span>`:""}${r.tur&&T[r.tur]?`<span class="prChip">${E(T[r.tur])}</span>`:""}<span class="prName">${E(r.subject||"Konu satırı yok")}</span><span class="prPct${pc===100?" ok":""}" title="Plan ve metin alanlarının doluluğu">%${pc}</span></summary><div class="prBody">${OPEN.has(id)?form(id,r):""}</div></details>`}).join("");
 let imp=IMP?`<div class="blImp"><label class="prF"><span>Claude'un ürettiği mailing planını yapıştırın (JSON dizi ya da {"mailing": […]})</span><textarea class="control" rows="8" id="mlImpTx" aria-label="İçe aktarılacak JSON"></textarea></label><div class="blAct"><button type="button" class="btn dark" data-impgo>İçe aktar</button><button type="button" class="btn" data-impcopy>Claude için talimatı kopyala</button><button type="button" class="btn" data-impx>Vazgeç</button></div><p class="prHint" id="mlImpMsg" aria-live="polite"></p></div>`:"";
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox mlBox"><div class="prHead"><p><b>${ids.length}</b> mail · yalnız ticari ileti izni olan alıcılara; her mailde abonelikten çıkma bağlantısı.</p><div class="blAct"><button type="button" class="prAdd" data-add>+ Mail ekle</button><button type="button" class="prAdd" data-imp>İçe aktar (JSON)</button></div></div>${imp}${ids.length?`<div class="prList">${rows}</div>`:`<p class="prEmpty">Henüz mail yok. “+ Mail ekle” ile ekleyin, Claude'un ürettiği planı içe aktarın ya da 8. menü › Blog Yazıları'nda bir yazının “Mailing taslakları oluştur” düğmesini kullanın.</p>`}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt işlemleri */
function nextId(){let S=store(),n=Object.keys(S).map(k=>+((k.match(/^M-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "M-"+String(n+1).padStart(3,"0")}
function commit(redraw){let S=store();if(Object.keys(S).length)state[FID]=S;else delete state[FID];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
function put(id,p,v){let S=store();S[id]=S[id]||{};if(v==="")delete S[id][p];else S[id][p]=v;state[FID]=S;commit(false);
 let d=document.querySelector(`.prRec[data-mid="${CSS.escape(id)}"]`);if(!d)return;let k=S[id],pc=d.querySelector(".prPct");if(pc){let x=fillPct(k);pc.textContent="%"+x;pc.classList.toggle("ok",x===100)}
 if(p==="subject"){let n=d.querySelector(".prName");if(n)n.textContent=v||"Konu satırı yok"}let w=d.querySelector(".mlW");if(w)w.textContent=warn(k).join(" ")}
const MO={subject:{max:60},preheader:{max:110},subjectB:{max:60},preheaderB:{max:110},ctaM:{w:[2,6]}};
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.dataset.mid)return;let id=d.dataset.mid;if(d.open){OPEN.add(id);let b=d.querySelector(".prBody");if(b&&!b.children.length)b.innerHTML=form(id,store()[id]||{})}else OPEN.delete(id)},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".mlBox")||!t.dataset.m)return;if(!requireProject()){refreshField(FID);return}put(JSON.parse(t.dataset.r),t.dataset.m,t.value);
 let o=MO[t.dataset.m],m=t.parentElement.querySelector(".prMeter");if(o&&m){let w=document.createElement("div");w.innerHTML=BL.meter(t.value,o);m.replaceWith(w.firstChild)}},true);
document.addEventListener("change",e=>{let t=e.target;if(t.closest&&t.closest(".mlBox")&&t.matches("select[data-m]"))t.dispatchEvent(new Event("input",{bubbles:true}))},true);
/* blogdan türetme: başlık grubundan 2'li */
function addDays(d,n){let x=new Date(d+"T00:00:00Z");x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10)}
const first=s=>{let m=String(s||"").match(/^[^.!?]*[.!?]/);return (m?m[0]:String(s||"")).trim()};
window.mlDerive=function(bid){let BS=BL.store(),b=BS[bid];if(!b)return "Blog kaydı bulunamadı.";
 let grp=b.grup?Object.keys(BS).filter(k=>BS[k].grup===b.grup&&BS[k].tarih&&DRE.test(BS[k].tarih)):[bid];grp=grp.filter(k=>BS[k].tarih&&DRE.test(BS[k].tarih)).sort((x,y)=>BS[x].tarih<BS[y].tarih?-1:1);if(!grp.length)return "Önce yazının yayın tarihini girin.";
 let F=grp.find(k=>BS[k].huni==="F")||grp[0],K=grp.slice().reverse().find(k=>BS[k].huni==="K")||(grp.length>1?grp[grp.length-1]:null),S=store(),made=0,msg=[],konu=b.grup||b.baslik||"",cta=clean(lab(FI.oc_cta_primary,state.oc_cta_primary))||"Teklif alın";
 if(!Object.values(S).some(m=>m.blog===F&&m.sira==="1")){let r=BS[F],id=nextId();S[id]={tarih:addDays(r.tarih,1),saat:"10:00",sira:"1",konu,blog:F,subject:(r.baslik||"").slice(0,60),preheader:first(r.ozet).slice(0,110),giris:r.ozet||"",bolumler:lines(r.h2).filter(x=>!/sss|sık sorulan/i.test(x)).map(x=>x+" | ").join("\n"),ctaM:"Yazının tamamını okuyun",ctaYol:blogUrl(r)};
  if(r.kategori)S[id].kategori=r.kategori;if(r.urun)S[id].urun=r.urun;Object.keys(S[id]).forEach(k=>{if(!S[id][k])delete S[id][k]});state[FID]=S;made++}else msg.push("Tanıtım maili zaten var");
 if(K&&K!==F){if(!Object.values(S).some(m=>m.blog===K&&m.sira==="2")){let r=BS[K],m1=Object.values(S).find(m=>m.blog===F&&m.sira==="1"),t=addDays(r.tarih,1);if(m1&&m1.tarih&&t<addDays(m1.tarih,7))t=addDays(m1.tarih,7);let id=nextId();
  S[id]={tarih:t,saat:"10:00",sira:"2",konu,blog:K,subject:(r.baslik||"").slice(0,60),preheader:first(r.ozet).slice(0,110),giris:r.ozet||"",bolumler:lines(r.h2).filter(x=>!/sss|sık sorulan/i.test(x)).map(x=>x+" | ").join("\n"),ctaM:r.cta||cta,ctaYol:r.link||String(state.oc_cta_url||"/iletisim"),ikinciM:"Yazının tamamını okuyun",ikinciYol:blogUrl(r)};
  if(r.kategori)S[id].kategori=r.kategori;if(r.urun)S[id].urun=r.urun;Object.keys(S[id]).forEach(k=>{if(!S[id][k])delete S[id][k]});state[FID]=S;made++}else msg.push("Karar maili zaten var")}
 else msg.push(b.grup?"grubun K (karar) yazısı yok, yalnız tanıtım maili":"yazının başlık grubu yok, yalnız tanıtım maili");
 commit(false);return (made?`${made} mailing taslağı oluşturuldu (8. menü › Mailing)`:"Yeni taslak yok")+(msg.length?" — "+msg.join("; "):"")+"."};
/* içe aktarma */
function imp(txt){let d;try{d=JSON.parse(txt)}catch(e){return "JSON okunamadı: "+e.message}let L=Array.isArray(d)?d:d&&Array.isArray(d.mailing)?d.mailing:d&&d.mailing&&Array.isArray(d.mailing.liste)?d.mailing.liste:d&&Array.isArray(d.liste)?d.liste:null;if(!L)return "Bir dizi ya da {\"mailing\": […]} bekleniyor.";
 let S=store(),add=0,upd=0,skip=0,pm={},pi=typeof window.prIdMap==="function"?window.prIdMap():{};Object.entries(pi).forEach(([k,v])=>pm[v]=k);
 L.forEach(x=>{if(!x||typeof x!=="object"){skip++;return}let id=String(x.id||"").trim();if(!/^[A-Za-z0-9_-]{1,40}$/.test(id))id="";if(!x.subject&&!(id&&S[id])){skip++;return}
  let r={},s=(k,v)=>{if(v!=null&&String(v).trim())r[k]=String(v).trim()};s("tarih",x.d||x.tarih);s("saat",x.t||x.saat);s("kategori",x.kat||x.kategori);["segment","konu","blog","subject","preheader","selam","giris","subjectB","preheaderB"].forEach(k=>s(k,x[k]));
  if(x.sira!=null)s("sira",String(x.sira));if(x.tur){let t=types().find(([v,l])=>v===x.tur||norm(l)===norm(x.tur));if(t)r.tur=t[0]}if(x.urun)r.urun=pm[x.urun]||String(x.urun);
  if(Array.isArray(x.bolumler))r.bolumler=x.bolumler.map(b=>typeof b==="object"?`${b.h||""} | ${b.m||""}`:String(b)).join("\n");if(x.cta){s("ctaM",x.cta.m);s("ctaYol",x.cta.yol)}if(x.ikinci){s("ikinciM",x.ikinci.m);s("ikinciYol",x.ikinci.yol)}
  if(Array.isArray(x.ilgili))r.ilgili=x.ilgili.map(b=>`${b.m||""} | ${b.yol||""}`).join("\n");if(r.tarih&&!DRE.test(r.tarih)){skip++;return}
  if(id&&S[id]){Object.assign(S[id],r);upd++}else{let n=id&&!S[id]?id:nextId();S[n]=r;state[FID]=S;add++}});
 commit(true);return `${add} mail eklendi, ${upd} mail güncellendi${skip?`, ${skip} kayıt atlandı (konu satırı ya da geçerli tarih yok)`:""}.`}
function impPrompt(){let P=BL.period(),b=blogs().map(x=>x[1]).slice(0,40).join("\n  ");
 return `Mailing planını yalnız JSON olarak ver (açıklama yazma): {"mailing": [ … ]}. Her mail bir nesne:
- id: kalıcı kimlik (M-001 …; mevcut maili güncelliyorsan onun kimliği)
- d: YYYY-AA-GG${P?` (${P[0]} – ${P[1]} arasında)`:""}, t: SS:DD
- sira: 1 (tanıtım, yazıya yönlendirir) ya da 2 (karar, teklif / form); aynı konunun iki maili arasında en az 7 gün
${types().length?`- tur: ${types().map(x=>x[0]+" ("+x[1]+")").join(", ")}\n`:""}- kat: kategori anahtarı: ${BL.cats().map(x=>x[0]).join(", ")}
- konu (başlık grubu), segment (alıcı grubu)${b?`, blog (bağlı yazının kimliği):\n  ${b}`:""}
- subject (en çok 60 karakter), preheader (en çok 110 karakter, konuyu tekrar etmez), selam ("Merhaba {ad},"), giris
- bolumler: [{"h": alt başlık, "m": metin}], cta: {"m": metin, "yol": adres}${", ikinci: {\"m\", \"yol\"} (isteğe bağlı), ilgili: [{\"m\", \"yol\"}] (en çok 3)"}${ab().includes("subject")?', subjectB (A/B konu satırı)':""}${ab().includes("preheader")?', preheaderB (A/B ön izleme)':""}
Tek net CTA; rakam, fiyat ve müşteri adı uydurma.`}
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".mlBox button");if(!b)return;
 if(b.hasAttribute("data-add")){if(!requireProject())return;let id=nextId(),S=store(),P=BL.period();S[id]={subject:""};if(P)S[id].tarih=P[0];state[FID]=S;OPEN.add(id);commit(true);let x=document.querySelector(`.prRec[data-mid="${CSS.escape(id)}"] [data-m="subject"]`);if(x)x.focus()}
 else if(b.hasAttribute("data-del")){if(!requireProject())return;let id=JSON.parse(b.dataset.r);if(!confirm("Bu mail kaydı silinsin mi?"))return;let S=store();delete S[id];OPEN.delete(id);state[FID]=S;commit(true)}
 else if(b.hasAttribute("data-imp")){IMP=true;refreshField(FID);let t=document.getElementById("mlImpTx");if(t)t.focus()}
 else if(b.hasAttribute("data-impx")){IMP=false;refreshField(FID)}
 else if(b.hasAttribute("data-impgo")){if(!requireProject())return;let t=document.getElementById("mlImpTx"),msg=imp(t?t.value:"");IMP=!/eklendi/.test(msg);if(!IMP)refreshField(FID);let m=document.getElementById("mlImpMsg");if(m)m.textContent=msg;else{let x=document.querySelector(".mlBox .prHead p");if(x)x.insertAdjacentText("beforeend"," — "+msg)}}
 else if(b.hasAttribute("data-impcopy")){let x=impPrompt();(navigator.clipboard?navigator.clipboard.writeText(x):Promise.reject()).then(()=>{let m=document.getElementById("mlImpMsg");if(m)m.textContent="Talimat kopyalandı; Claude'a yapıştırın, gelen JSON'u buraya yapıştırın."},()=>{let t=document.getElementById("mlImpTx");if(t){t.value=x;t.select()}})}},true);
/* kural, özet, kayıt */
function recSum(){let n=Object.keys(store()).length;return n?n+" mail":""}
function recRule(){let S=store(),ids=sorted(),d=ids.map(i=>S[i].tarih).filter(Boolean),T=ids.map(i=>S[i].subject).filter(Boolean),abL=ids.filter(i=>S[i].subjectB||S[i].preheaderB).length;
 return `Mailing kayıtları: ${ids.length} mail${d.length?` (${d[0]} – ${d[d.length-1]})`:""}${T.length?`; konu satırları: ${T.slice(0,8).join("; ")}${T.length>8?` ve ${T.length-8} mail daha`:""}`:""}. Konu satırı en çok 60, ön izleme en çok 110 karakterdir ve konuyu tekrar etmez; her mailde tek net CTA vardır. Mailler yalnız ticari elektronik ileti izni olan alıcılara gönderilir ve her mailde abonelikten çıkma bağlantısı bulunur; kayıtlar plan dosyasının Mailing bölümüne aktarılır.${abL?` ${abL} mailde A/B testi için B konu satırı ya da ön izlemesi var; iki sürüm eşit segmentlere gönderilir, kazanan açılma oranıyla seçilir.`:""}`}
window.REC[FID]={isset:()=>Object.keys(store()).some(k=>filled(store()[k])),rule:recRule,sum:recSum,box,
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Mailing, Pazarlama › Mailing › E-posta Pazarlaması “Evet” iken kullanılır.</p><p><button type="button" class="btn dark" onclick="goToField('mk_mail','mk_mail_on')">Kararı aç →</button></p></section>`};
/* plan dosyasına aktarım */
function exportList(B){let S=store(),pm=typeof window.prIdMap==="function"?window.prIdMap():{},K=(B.mailing.kategoriler||[]).map(x=>x.k),bl=new Set((B.bloglar||[]).map(x=>x.id)),T=Object.fromEntries(types()),notes=[];
 let L=sorted().map(id=>{let r=S[id],o={id};if(r.tarih)o.d=r.tarih;if(r.saat)o.t=r.saat;if(r.kategori&&K.includes(r.kategori))o.kat=r.kategori;["konu","segment","subject","preheader","selam","giris"].forEach(k=>{if(r[k])o[k]=r[k]});
  if(r.sira)o.sira=+r.sira;o.tur=r.tur&&T[r.tur]?T[r.tur]:r.sira==="2"?"Karar":"Tanıtım";if(r.bolumler)o.bolumler=pairs(r.bolumler);if(r.ctaM||r.ctaYol)o.cta={m:r.ctaM||"",yol:r.ctaYol||""};if(r.ikinciM&&r.ikinciYol)o.ikinci={m:r.ikinciM,yol:r.ikinciYol};
  if(r.ilgili){let I=lines(r.ilgili).slice(0,3).map(x=>{let i=x.indexOf("|");return {m:(i<0?x:x.slice(0,i)).trim(),yol:i<0?"":x.slice(i+1).trim()}}).filter(x=>x.m&&x.yol);if(I.length)o.ilgili=I}
  if(r.blog&&bl.has(r.blog))o.blog=r.blog;if(r.urun&&B.urunler&&pm[r.urun])o.urun=pm[r.urun];
  if(r.subjectB||r.preheaderB)notes.push(`${id} A/B: ${r.subjectB?`B konu satırı “${r.subjectB}”`:""}${r.subjectB&&r.preheaderB?", ":""}${r.preheaderB?`B ön izleme “${r.preheaderB}”`:""}.`);return o});
 return {L,notes}}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(B.mailing&&shown(FI[FID])){let {L,notes}=exportList(B);if(L.length)B.mailing.liste=L;if(notes.length)B.mailing.notlar=(B.mailing.notlar||[]).concat(notes)}}catch(e){console.error("Mailing aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments);if(!shown(FI[FID]))return L;let S=store(),ids=Object.keys(S),c=`<button type="button" class="linkBtn" onclick="goToField('ip_mail','${FID}')">İçerik Planlama › Mailing</button>`;
 let ns=ids.filter(i=>!S[i].subject),lg=ids.filter(i=>(S[i].subject||"").length>60||(S[i].preheader||"").length>110),nd=ids.filter(i=>!S[i].tarih||!DRE.test(S[i].tarih));
 if(ns.length)L.push(`${ns.length} mailin konu satırı yok — ${c}.`);if(lg.length)L.push(`${lg.length} mailde konu satırı 60 ya da ön izleme 110 karakteri aşıyor — ${c}.`);if(nd.length)L.push(`${nd.length} mailin tarihi yok ya da YYYY-AA-GG biçiminde değil — ${c}.`);return L}}
window.mlImport=imp;window.mlPrompt=impPrompt;window.ML={store,sorted};
})();
