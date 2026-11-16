/* 8.4 Sosyal Paylaşımlar — kayıt düzenleyicisi (2026-11-15). Kullanıcı kararları: kayıt derinliği plan + içerik planı (sahne /
   slayt planı, gönderi metni, etiketler); paylaşımlar blog kaydından taslak olarak türetilebilir (İçerik Türetme Modeli her blogdan
   türeyen ya da karma iken), elle eklenir ya da JSON içe aktarılır; story'ler Pazarlama › Story Kullanımı'na göre: "her paylaşımın
   Story sürümü" → şablon türetir (S formatı sunulmaz), "yalnız seçili paylaşımlar" → S ayrı kayıt; Story formatı seçilmemişse ya da
   seçili modda şablona storyTuret:false; ek alanlar ilgili ürün / hizmet, özel gün, referans firma (Ortak Bilgiler › Referanslar),
   📥. Değer: state.ip_posts = {P-001: {tarih, saat, f, kategori, huni, title, hook, konu (blog kimliği), cta, link, plan, cap,
   tags, note, urun, ozelGun, ref, dl}}. Seri no <önek>-SM-NNN tarih sırasından yalnız gösterilir. Ortak seçenekler 8.3'ten
   (window.BL). Aktarım paylasimlar[] (KILAVUZ 18.5). Kaynak docs/v26/v26-social.{js,css} → docs/v26/sosyal_ekle.py */
(function(){
const FID="ip_posts";
if(!FI[FID]||!window.REC||!window.BL)return;
const BL=window.BL,OPEN=new Set();let IMP=false;
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const DRE=/^\d{4}-\d{2}-\d{2}$/,TRE=/^([01]\d|2[0-3]):[0-5]\d$/;
function store(){let v=state[FID];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
function filled(r){return !!r&&Object.values(r).some(v=>String(v||"").trim()!=="")}
const FMT_AD={R:"Reels / kısa video",C:"Carousel",T:"Tek görsel",S:"Story",V:"Uzun video",M:"Metin gönderisi",A:"Anket",K:"Makale",E:"Etkinlik duyurusu",TH:"Thread / seri gönderi",L:"Canlı yayın"};
function storySel(){return sv("mk_story")==="selected"}
function fmts(){let v=sv("mk_formats"),L=Array.isArray(v)&&v.length?v:["R","C","T"];return L.filter(x=>x!=="S"||storySel()).map(x=>[x,FMT_AD[x]||clean(lab(FI.mk_formats,x))])}
function blogs(){let S=BL.store();return BL.sorted().map(id=>[id,`${id} · ${S[id].tarih||"tarih yok"} · ${S[id].baslik||"Başlıksız"}`])}
function refs(){let v=sv("oc_proof");if(!v||typeof refParse!=="function")return [];return refParse(v).map(r=>r.name).filter(Boolean).map(n=>[n,n])}
const PLAN_PH={R:"Sahne 1 (0–3 sn, kanca): …\nSahne 2: …\nSon kare: CTA kartı",C:"Slayt 1 (kapak): …\nSlayt 2: …\nSon slayt: CTA",T:"Görsel: …\nAlt satır: …",S:"Kare 1 (kanca): …\nKare 2: …\nKare 3: bağlantı etiketi"};
/* biçim */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function inp(id,p,label,kind,val,o,ph){let a=`data-s="${E(p)}" ${q(id)} aria-label="${E(label)}"`,ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:5}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${o?BL.meter(val,o):""}</label>`}
function sel(id,p,label,opts,val,empty){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-s="${E(p)}" ${q(id)} aria-label="${E(label)}"><option value="">${E(empty||"Seçin")}</option>${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
function dateWarn(r){let w=[],P=BL.period();if(r.tarih&&!DRE.test(r.tarih))w.push("Tarih YYYY-AA-GG biçiminde olmalı.");else if(r.tarih&&P&&(r.tarih<P[0]||r.tarih>P[1]))w.push(`Tarih plan döneminin (${P[0]} – ${P[1]}) dışında.`);if(r.saat&&!TRE.test(r.saat))w.push("Saat SS:DD biçiminde olmalı.");return w}
function fmtHint(f){let x=(typeof MKT!=="undefined"&&MKT.formatlar||{})[f];return x?[x.olcu,x.sure].filter(Boolean).join(" · "):""}
function form(id,r){let g=p=>r[p]||"",h=BL.hunis(),Bl=blogs(),Pr=BL.prods(),Dy=BL.days(),Rf=refs(),cap=sv("mk_caption")==="structured"?"Kanca (ilk satır)\n\nAna mesaj\n\nCTA: {link}":"Gönderi metni; {link} yazılan yere UTM'li bağlantı gelir";
 let plan=`<div class="blGrid">${inp(id,"tarih","Yayın tarihi","text",g("tarih"),null,"YYYY-AA-GG")}${inp(id,"saat","Saat","text",g("saat"),null,"SS:DD")}</div><small class="prMeter bad spDW" aria-live="polite">${E(dateWarn(r).join(" "))}</small>`+
  `<div class="blGrid">${sel(id,"f","Format",fmts(),g("f"))}${sel(id,"kategori","Kategori",BL.cats(),g("kategori"))}</div>`+(h?sel(id,"huni","Huni",h,g("huni")):"")+
  inp(id,"title","Başlık (konu)","text",g("title"))+inp(id,"hook","Kanca (ilk 3 saniye / ilk satır)","area",g("hook"))+
  (Bl.length?sel(id,"konu","Bağlı blog yazısı",Bl,g("konu"),"Bağlı değil"):"")+`<div class="blGrid">${inp(id,"cta","CTA","text",g("cta"),{w:[2,6]})}${inp(id,"link","Bağlantı (hedef sayfa)","text",g("link"),null,"/blog/…")}</div>`;
 let ip=`<p class="prHint spFH">${E(fmtHint(g("f")))}</p>`+inp(id,"plan",g("f")==="C"?"Slayt planı (her satıra bir slayt)":g("f")==="R"?"Sahne planı (her satıra bir sahne)":"Görsel / içerik planı (her satıra bir madde)","lines",g("plan"),null,PLAN_PH[g("f")]||"")+
  inp(id,"cap","Gönderi metni","lines",g("cap"),null,cap)+inp(id,"tags","Etiketler (#Etiket #Etiket)","text",g("tags"))+inp(id,"note","Üretim notu","area",g("note"));
 let ex=(Pr.length?sel(id,"urun","İlgili ürün / hizmet",Pr,g("urun"),"İlişki yok"):"")+(Dy.length?sel(id,"ozelGun","Özel gün",Dy,g("ozelGun"),"Bağlı değil"):"")+(Rf.length?sel(id,"ref","Referans firma (müşteri hikâyesi)",Rf,g("ref"),"Yok"):"")+
  (sv("mk_lead_magnet")===true?`<label class="blChk"><input type="checkbox" data-s="dl" ${q(id)}${g("dl")?" checked":""}> 📥 İndirilebilir içeriğe yönlendirir</label>`:"");
 return [["Plan",plan],["İçerik planı",ip],["Bağlantılar",ex||`<p class="prHint">Ek bağlantı yok (ürün kaydı, özel gün takvimi ya da referans tanımlı değil).</p>`]].map(([t,x])=>`<fieldset class="prSec"><legend>${E(t)}</legend>${x}</fieldset>`).join("")+`<div class="blAct"><button type="button" class="prAdd blDelRec" data-del ${q(id)}>Paylaşımı sil</button></div>`}
function sorted(){let S=store();return Object.keys(S).sort((a,b)=>{let x=(S[a].tarih||"9999")+(S[a].saat||""),y=(S[b].tarih||"9999")+(S[b].saat||"");return x<y?-1:x>y?1:a<b?-1:1})}
function fillPct(r){let P=["tarih","f","kategori","title","hook","plan","cap"];if(BL.hunis())P.push("huni");return Math.round(P.filter(p=>String(r[p]||"").trim()).length/P.length*100)}
function storyNote(){let fs=sv("mk_formats");if(!Array.isArray(fs)||!fs.includes("S"))return "Story formatı seçilmedi; plan sayfasında story türetilmez.";return storySel()?"Story'ler ayrı kayıt olarak (format Story) girilir.":"Story'ler plan sayfasında her paylaşımdan kendiliğinden türetilir (Pazarlama › Story Kullanımı).";}
function box(f){let S=store(),ids=sorted(),pre=String(mkT("mk_prefix")||"ÖNEK").toUpperCase();
 let rows=ids.map((id,n)=>{let r=S[id],pc=fillPct(r);return `<details class="prRec" data-pid="${E(id)}"${OPEN.has(id)?" open":""}><summary><span class="prPath">${E(pre)}-SM-${String(n+1).padStart(3,"0")}</span><span class="prPath">${E(r.tarih||"tarih yok")}${r.saat?" "+E(r.saat):""}</span>${r.f?`<span class="prChip">${E(FMT_AD[r.f]||r.f)}</span>`:""}${r.huni?`<span class="prChip">${E(r.huni)}</span>`:""}<span class="prName">${E(r.title||"Başlıksız paylaşım")}</span>${r.konu?`<code class="prPath">${E(r.konu)}</code>`:""}<span class="prPct${pc===100?" ok":""}" title="Plan ve içerik alanlarının doluluğu">%${pc}</span></summary><div class="prBody">${OPEN.has(id)?form(id,r):""}</div></details>`}).join("");
 let imp=IMP?`<div class="blImp"><label class="prF"><span>Claude'un ürettiği paylaşım planını yapıştırın (JSON dizi ya da {"paylasimlar": […]})</span><textarea class="control" rows="8" id="spImpTx" aria-label="İçe aktarılacak JSON"></textarea></label><div class="blAct"><button type="button" class="btn dark" data-impgo>İçe aktar</button><button type="button" class="btn" data-impcopy>Claude için talimatı kopyala</button><button type="button" class="btn" data-impx>Vazgeç</button></div><p class="prHint" id="spImpMsg" aria-live="polite"></p></div>`:"";
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox spBox"><div class="prHead"><p><b>${ids.length}</b> paylaşım · ${E(storyNote())}</p><div class="blAct"><button type="button" class="prAdd" data-add>+ Paylaşım ekle</button><button type="button" class="prAdd" data-imp>İçe aktar (JSON)</button></div></div>${imp}${ids.length?`<div class="prList">${rows}</div>`:`<p class="prEmpty">Henüz paylaşım yok. “+ Paylaşım ekle” ile ekleyin, Claude'un ürettiği planı içe aktarın${["hub","mixed"].includes(sv("mk_derive"))?" ya da 8. menü › Blog Yazıları'nda bir yazının “Paylaşım taslakları oluştur” düğmesini kullanın":""}.</p>`}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt işlemleri */
function nextId(){let S=store(),n=Object.keys(S).map(k=>+((k.match(/^P-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "P-"+String(n+1).padStart(3,"0")}
function commit(redraw){let S=store();if(Object.keys(S).length)state[FID]=S;else delete state[FID];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
function put(id,p,v){let S=store();S[id]=S[id]||{};if(v===""||v===false)delete S[id][p];else S[id][p]=v;state[FID]=S;commit(false);
 let d=document.querySelector(`.prRec[data-pid="${CSS.escape(id)}"]`);if(!d)return;let k=S[id],pc=d.querySelector(".prPct");if(pc){let x=fillPct(k);pc.textContent="%"+x;pc.classList.toggle("ok",x===100)}
 if(p==="title"){let n=d.querySelector(".prName");if(n)n.textContent=v||"Başlıksız paylaşım"}if(p==="tarih"||p==="saat"){let w=d.querySelector(".spDW");if(w)w.textContent=dateWarn(k).join(" ")}if(p==="f"){let h=d.querySelector(".spFH");if(h)h.textContent=fmtHint(v)}}
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.dataset.pid)return;let id=d.dataset.pid;if(d.open){OPEN.add(id);let b=d.querySelector(".prBody");if(b&&!b.children.length)b.innerHTML=form(id,store()[id]||{})}else OPEN.delete(id)},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".spBox")||!t.dataset.s)return;if(!requireProject()){refreshField(FID);return}let id=JSON.parse(t.dataset.r);put(id,t.dataset.s,t.type==="checkbox"?(t.checked?"1":""):t.value);
 if(t.dataset.s==="cta"){let m=t.parentElement.querySelector(".prMeter");if(m){let w=document.createElement("div");w.innerHTML=BL.meter(t.value,{w:[2,6]});m.replaceWith(w.firstChild)}}},true);
document.addEventListener("change",e=>{let t=e.target;if(t.closest&&t.closest(".spBox")&&t.matches("select[data-s],input[type=checkbox][data-s]"))t.dispatchEvent(new Event("input",{bubbles:true}))},true);
/* blogdan taslak (8.3'teki düğme) */
function blogUrl(r){let y={blog:"/blog/{slug}/",root:"/{slug}/"}[sv("mk_blog_path")]||"/blog/{slug}/";return r.slug?y.replace("{slug}",r.slug):""}
function addDays(d,n){let x=new Date(d+"T00:00:00Z");x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10)}
window.spDerive=function(bid){let b=BL.store()[bid];if(!b)return "Blog kaydı bulunamadı.";if(!b.tarih||!DRE.test(b.tarih))return "Önce yazının yayın tarihini girin.";
 let F0=fmts().map(x=>x[0]),want=["R","C","T"].filter(x=>F0.includes(x));if(!want.length)want=F0.slice(0,1);let S=store(),made=0,n=0;
 want.forEach(f=>{n++;if(Object.values(S).some(p=>p.konu===bid&&p.f===f))return;let id=nextId(),r={tarih:addDays(b.tarih,n),saat:"12:00",f,konu:bid,title:b.baslik||""};
  ["kategori","huni","cta","urun","ozelGun"].forEach(k=>{if(b[k])r[k]=b[k]});let u=blogUrl(b);if(u)r.link=u;if(b.dl)r.dl="1";Object.keys(r).forEach(k=>{if(!r[k])delete r[k]});S[id]=r;state[FID]=S;made++});
 commit(false);return made?`${made} paylaşım taslağı oluşturuldu (8. menü › Sosyal Paylaşımlar); kanca, plan ve metin orada doldurulur.`:"Bu yazının taslakları zaten var."};
/* içe aktarma */
const MAP={d:"tarih",t:"saat",cat:"kategori",h:"huni"},AL=["tarih","saat","f","kategori","huni","title","hook","konu","cta","link","tags","note","urun","ozelGun","ref"];
function imp(txt){let d;try{d=JSON.parse(txt)}catch(e){return "JSON okunamadı: "+e.message}let L=Array.isArray(d)?d:d&&Array.isArray(d.paylasimlar)?d.paylasimlar:null;if(!L)return "Bir dizi ya da {\"paylasimlar\": […]} bekleniyor.";
 let S=store(),add=0,upd=0,skip=0,pm={},pi=typeof window.prIdMap==="function"?window.prIdMap():{};Object.entries(pi).forEach(([k,v])=>pm[v]=k);
 L.forEach(x0=>{if(!x0||typeof x0!=="object"){skip++;return}let x={};Object.entries(x0).forEach(([k,v])=>x[MAP[k]||k]=v);let id=String(x.id||"").trim();if(!/^[A-Za-z0-9_-]{1,40}$/.test(id))id="";
  if(!x.title&&!(id&&S[id])){skip++;return}let r={};AL.forEach(k=>{if(x[k]!=null&&String(x[k]).trim())r[k]=String(x[k]).trim()});["plan","cap"].forEach(k=>{if(Array.isArray(x[k]))r[k]=x[k].map(String).join("\n");else if(x[k])r[k]=String(x[k])});
  if(Array.isArray(x.tags))r.tags=x.tags.join(" ");if(r.urun)r.urun=pm[r.urun]||r.urun;if(x.dl===true||x.dl==="1")r.dl="1";
  if(r.tarih&&!DRE.test(r.tarih)){skip++;return}if(id&&S[id]){Object.assign(S[id],r);upd++}else{let n=id&&!S[id]?id:nextId();S[n]=r;state[FID]=S;add++}});
 commit(true);return `${add} paylaşım eklendi, ${upd} paylaşım güncellendi${skip?`, ${skip} kayıt atlandı (başlık ya da geçerli tarih yok)`:""}.`}
function impPrompt(){let P=BL.period(),c=BL.cats().map(x=>x[0]+" ("+x[1]+")").join(", "),h=(BL.hunis()||[]).map(x=>x[1]).join(", "),b=blogs().map(x=>x[1]).slice(0,40).join("\n  ");
 return `Sosyal medya paylaşım planını yalnız JSON olarak ver (açıklama yazma): {"paylasimlar": [ … ]}. Her paylaşım bir nesne:
- id: kalıcı kimlik (P-001, P-002 …; mevcut paylaşımı güncelliyorsan onun kimliği)
- d: YYYY-AA-GG${P?` (${P[0]} – ${P[1]} arasında)`:""}, t: SS:DD
- f: format kodu: ${fmts().map(x=>x[0]+" ("+x[1]+")").join(", ")}
- cat: kategori anahtarı: ${c||"—"}${h?`\n- h: huni (${h})`:""}
- title: konu, hook: ilk 3 saniye / ilk satır, plan: dizi (Reels'te sahneler, Carousel'de slaytlar, tek görselde görsel maddeleri)
- cap: gönderi metni; bağlantının geleceği yere {link} yaz${sv("mk_caption")==="structured"?" (kanca + ana mesaj + CTA + etiketler yapısında)":""}
- cta, link (hedef sayfa), tags ("#Etiket #Etiket")${b?`\n- konu: bağlı blog yazısının kimliği (varsa):\n  ${b}`:""}
Rakam, fiyat ve müşteri adı uydurma; müşteri adı yalnız yazılı onaylı referanslar için kullanılır.`}
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".spBox button");if(!b)return;
 if(b.hasAttribute("data-add")){if(!requireProject())return;let id=nextId(),S=store(),P=BL.period();S[id]={title:""};if(P)S[id].tarih=P[0];let f=fmts()[0];if(f)S[id].f=f[0];state[FID]=S;OPEN.add(id);commit(true);let x=document.querySelector(`.prRec[data-pid="${CSS.escape(id)}"] [data-s="title"]`);if(x)x.focus()}
 else if(b.hasAttribute("data-del")){if(!requireProject())return;let id=JSON.parse(b.dataset.r);if(!confirm("Bu paylaşım kaydı silinsin mi?"))return;let S=store();delete S[id];OPEN.delete(id);state[FID]=S;commit(true)}
 else if(b.hasAttribute("data-imp")){IMP=true;refreshField(FID);let t=document.getElementById("spImpTx");if(t)t.focus()}
 else if(b.hasAttribute("data-impx")){IMP=false;refreshField(FID)}
 else if(b.hasAttribute("data-impgo")){if(!requireProject())return;let t=document.getElementById("spImpTx"),msg=imp(t?t.value:"");IMP=!/eklendi/.test(msg);if(!IMP)refreshField(FID);let m=document.getElementById("spImpMsg");if(m)m.textContent=msg;else{let x=document.querySelector(".spBox .prHead p");if(x)x.insertAdjacentText("beforeend"," — "+msg)}}
 else if(b.hasAttribute("data-impcopy")){let x=impPrompt();(navigator.clipboard?navigator.clipboard.writeText(x):Promise.reject()).then(()=>{let m=document.getElementById("spImpMsg");if(m)m.textContent="Talimat kopyalandı; Claude'a yapıştırın, gelen JSON'u buraya yapıştırın."},()=>{let t=document.getElementById("spImpTx");if(t){t.value=x;t.select()}})}},true);
/* kural, özet, kayıt */
function dist(){let S=store(),c={};Object.values(S).forEach(r=>{let k=FMT_AD[r.f]||r.f||"format yok";c[k]=(c[k]||0)+1});return Object.entries(c).map(([k,n])=>k+" "+n).join(", ")}
function recSum(){let n=Object.keys(store()).length;return n?n+" paylaşım":""}
function recRule(){let S=store(),ids=sorted(),d=ids.map(i=>S[i].tarih).filter(Boolean);
 return `Sosyal paylaşım kayıtları: ${ids.length} paylaşım${d.length?` (${d[0]} – ${d[d.length-1]})`:""}; format dağılımı: ${dist()}. Her kaydın tarihi, formatı, kategorisi, hunisi, kancası, sahne / slayt planı ve gönderi metni plan dosyasının Konular › Sosyal paylaşımlar bölümüne aktarılır; mecra metinleri bu gönderi metninden mecranın karakter sınırına ve bağlantı davranışına göre uyarlanır. ${storyNote()}`}
window.REC[FID]={isset:()=>Object.keys(store()).some(k=>filled(store()[k])),rule:recRule,sum:recSum,box};
/* plan dosyasına aktarım */
function exportList(B){let S=store(),pm=typeof window.prIdMap==="function"?window.prIdMap():{},K=Object.keys(B.kategoriler||{}),og=B.ozelGunler?new Set((B.ozelGunler.liste||[]).map(x=>x.id)):null,bl=new Set((B.bloglar||[]).map(x=>x.id)),FS=Object.keys(B.formatlar||{});
 return sorted().filter(id=>{let f=S[id].f;return f&&(f==="S"?storySel():FS.includes(f))}).map(id=>{let r=S[id],o={f:r.f};if(r.tarih)o.d=r.tarih;if(r.saat)o.t=r.saat;if(r.kategori&&K.includes(r.kategori))o.cat=r.kategori;if(r.huni&&BL.hunis())o.h=r.huni;if(r.dl)o.dl=true;
  ["title","hook","cap","cta","link","tags","note","ref"].forEach(k=>{if(r[k])o[k]=r[k]});if(r.plan)o.plan=lines(r.plan);if(r.konu&&bl.has(r.konu))o.konu=r.konu;if(r.urun&&B.urunler&&pm[r.urun])o.urun=pm[r.urun];if(r.ozelGun&&og&&og.has(r.ozelGun))o.ozelGun=r.ozelGun;return o})}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{let L=exportList(B);if(L.length)B.paylasimlar=L;let fs=Array.isArray(state.mk_formats)?state.mk_formats:[];if(!fs.includes("S")||storySel())B.storyTuret=false}catch(e){console.error("Paylaşım kayıtları aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments),S=store(),ids=Object.keys(S),c=`<button type="button" class="linkBtn" onclick="goToField('ip_social','${FID}')">İçerik Planlama › Sosyal Paylaşımlar</button>`,F0=fmts().map(x=>x[0]);if(storySel())F0.push("S");
 let nf=ids.filter(i=>!S[i].f||!F0.includes(S[i].f)),nd=ids.filter(i=>!S[i].tarih||!DRE.test(S[i].tarih)),P=BL.period(),out=P?ids.filter(i=>S[i].tarih&&DRE.test(S[i].tarih)&&(S[i].tarih<P[0]||S[i].tarih>P[1])):[];
 if(nf.length)L.push(`${nf.length} paylaşımın formatı yok ya da İçerik Formatları'nda seçili değil; bu paylaşımlar plan dosyasına aktarılmaz — ${c}.`);if(nd.length)L.push(`${nd.length} paylaşımın tarihi yok ya da YYYY-AA-GG biçiminde değil — ${c}.`);if(out.length)L.push(`${out.length} paylaşımın tarihi plan döneminin dışında — ${c}.`);return L}}
window.SP={store,sorted,storySel,open:id=>OPEN.add(id),fmtAd:f=>FMT_AD[f]||f};
window.spImport=imp;window.spPrompt=impPrompt;window.spExport=()=>exportList(mkPlanData());
})();
