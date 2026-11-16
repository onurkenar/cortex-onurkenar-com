/* 8.8 Etkinlikler — kayıt düzenleyicisi (2026-11-15). Kullanıcı kararları: bilgi + program (ad, kısa ad, tür, sayfa yolu, tarih,
   başlangıç / bitiş saati, format, ücret, son kayıt, konuşmacılar, program, konular, hedef kitle, sunulanlar, notlar); aktivite
   planı burada, kararlara göre kurulur; ekler ölçüm hedefleri, aktiviteler takvimde (8.5), bağlı ürün / blog. Alan ip_events_rec
   type "records", showIf mk_evt_on. Değer: state.ip_events = {E-01: {ad, kisaAd, tur, yol, d, bas, bit, kayitSon, format, ucret,
   utm, ozet, konusmacilar ("Ad | Unvan"), program ("Saat | Başlık | Konuşmacı"), konular, hedefKitle, sunulanlar, notlar (satır
   satır), olcum ("Gösterge | Hedef | Nasıl ölçülür"), urun, blog, akt: {E-01-A04: {d?, t?, s?, x?}}}}.
   Aktivite planı saklanmaz, her seferinde hesaplanır: şablonun standart planı (ET_STD, 29 aktivite; docs/icerik-planlama/
   etkinlik-standart-plan.json) Pazarlama › Aktivite Planı'na göre (standart = tümü, kısa = 12, plan yok = hiç), Duyuru
   Kanalları + Mecralar + Reklam Kanalları'na göre (iç işler her zaman) ve Etkinlik Sonrası'na göre süzülür; gün farkı etkinlik
   gününe eklenir, hafta sonu / resmî tatil (window.pfHolidays) en yakın iş gününe kayar (şablonun etStdPlan mantığı). Aktivite
   kimliği şablondaki sırayla sabittir (E-01-A01 … A29); akt yalnız elle değiştirilen tarih / saat / sorumluyu ve plandan
   çıkarılanları (x) tutar — elle değiştirilen aktivite etkinlik tarihi değişince yeniden hesaplanmaz. Aktarım etkinlikler.liste[]
   (KILAVUZ 18.9); metinlerde {marka} {etiket} {onek} doldurulur, {link} {ad} {tarih} … şablona bırakılır.
   Kaynak docs/v26/v26-events.{js,css} → docs/v26/etkinlik_ekle.py */
(function(){
const FID="ip_events_rec",KEY="ip_events";
if(!FI[FID]||!window.REC||!window.BL)return;
const STD=/*ET_STD*/[],KISA=/*ET_KISA*/[];
const BL=window.BL,OPEN=new Set();
const sv=id=>{let f=FI[id];return f&&shown(f)?state[id]:undefined};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const lines=s=>String(s||"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean);
const cells=x=>x.split("|").map(y=>y.trim());
const DRE=/^\d{4}-\d{2}-\d{2}$/,TRE=/^([01]\d|2[0-3]):[0-5]\d$/;
const FAZ={hazirlik:"Hazırlık",duyuru:"Duyuru ve kayıt",hatirlatma:"Hatırlatma",gun:"Etkinlik günü",sonrasi:"Etkinlik sonrası"};
const KAN={ic:"İç iş",eposta:"E-posta",linkedin:"LinkedIn",instagram:"Instagram",facebook:"Facebook",x:"X",whatsapp:"WhatsApp Kanalı",meta:"Meta Ads",google:"Google Ads"};
const SOC=["linkedin","instagram","facebook","x","whatsapp"];
function store(){let v=state[KEY];return v&&typeof v==="object"&&!Array.isArray(v)?v:{}}
function filled(r){return !!r&&Object.keys(r).some(k=>k!=="akt"&&String(r[k]||"").trim()!=="")}
function types(){let v=sv("mk_evt_types");return Array.isArray(v)?v.map(x=>[x,clean(lab(FI.mk_evt_types,x))]):[]}
function blogs(){let S=BL.store();return BL.sorted().map(id=>[id,`${id} · ${S[id].tarih||"tarih yok"} · ${S[id].baslik||"Başlıksız"}`])}
function addDays(d,n){let x=new Date(d+"T00:00:00Z");x.setUTCDate(x.getUTCDate()+n);return x.toISOString().slice(0,10)}
function hol(d){let y=+d.slice(0,4);return typeof window.pfHolidays==="function"?window.pfHolidays([y-1,y,y+1]):[]}
function work(d,H){let w=new Date(d+"T00:00:00Z").getUTCDay();return w!==0&&w!==6&&!H.includes(d)}
function shift(d,dir,H){let x=d;for(let i=0;i<10;i++){if(work(x,H))return x;x=addDays(x,dir)}return d}
function minus(t,m){let [h,mi]=t.split(":").map(Number),v=Math.max(0,h*60+mi-m);return String(Math.floor(v/60)).padStart(2,"0")+":"+String(v%60).padStart(2,"0")}
const ONLINE=["webinar","live"];
/* aktivite planı */
function planMode(){let p=sv("mk_evt_plan");return p==="short"||p==="none"?p:"standard"}
function keep(row,i){let m=planMode();if(m==="none"||(m==="short"&&!KISA.includes(i)))return false;let k=row[3],ch=sv("mk_evt_channels");
 if(k!=="ic"&&Array.isArray(ch)&&ch.length){if(k==="eposta"&&!ch.includes("email"))return false;
  if(SOC.includes(k)){if(!ch.includes("social"))return false;let P=sv("mk_platforms");if(Array.isArray(P)&&P.length&&!P.includes(k))return false}
  if(k==="meta"||k==="google"){if(!ch.includes("ads"))return false;let A=sv("mk_ads_channels");if(Array.isArray(A)&&A.length&&!A.includes(k))return false}}
 let af=sv("mk_evt_after");if(Array.isArray(af)&&af.length){if((i===25||i===26)&&!af.includes("recording_share"))return false;if(i===27&&!af.includes("lead_followup"))return false;if(i===28&&!af.includes("report"))return false}
 return true}
function acts(id,r){if(!r||!r.d||!DRE.test(r.d))return [];let H=hol(r.d),O=r.akt||{},on=!r.tur||ONLINE.includes(r.tur),L=[];
 STD.forEach((row,i)=>{if(!keep(row,i))return;let [gun,t,faz,kanal,tur,baslik,sorumlu,ek]=row,aid=id+"-A"+String(i+1).padStart(2,"0"),o=O[aid]||{},d=addDays(r.d,gun);if(gun!==0)d=shift(d,gun<0?-1:1,H);
  if(TRE.test(r.bas||"")){if(i===21)t=r.bas;if(i===20)t=minus(r.bas,15)}if(!on){if(i===21)baslik="ETKİNLİK: oturum";if(i===20)baslik="Etkinlik alanı hazırlık ve kontrol"}
  L.push({aid,i,gun,d:o.d||d,t:o.t||t,faz,kanal,tur,baslik,sorumlu:o.s||sorumlu,ek,x:!!o.x,ed:!!(o.d||o.t||o.s)})});
 return L.sort((a,b)=>(a.d+a.t)<(b.d+b.t)?-1:(a.d+a.t)>(b.d+b.t)?1:a.i-b.i)}
const tLab=g=>g===0?"T":g<0?"T"+g:"T+"+g;
/* biçim */
const q=k=>`data-r='${E(JSON.stringify(k))}'`;
function inp(id,p,label,kind,val,o,ph){let a=`data-m="${E(p)}" ${q(id)} aria-label="${E(label)}"`,ctl=kind==="text"?`<input class="control" type="text" ${a} value="${E(val||"")}" placeholder="${E(ph||"")}" autocomplete="off">`:`<textarea class="control" rows="${kind==="area"?3:4}" ${a} placeholder="${E(ph||"")}">${E(val||"")}</textarea>`;
 return `<label class="prF"><span>${E(label)}</span>${ctl}${o?BL.meter(val,o):""}</label>`}
function sel(id,p,label,opts,val,empty){return `<label class="prF"><span>${E(label)}</span><select class="control" data-native data-m="${E(p)}" ${q(id)} aria-label="${E(label)}"><option value="">${E(empty||"Seçin")}</option>${opts.map(([v,t])=>`<option value="${E(v)}"${v===val?" selected":""}>${E(t)}</option>`).join("")}</select></label>`}
function warn(r){let w=[],P=BL.period();["d","kayitSon"].forEach(k=>{if(r[k]&&!DRE.test(r[k]))w.push((k==="d"?"Tarih":"Son kayıt günü")+" YYYY-AA-GG biçiminde olmalı.")});["bas","bit"].forEach(k=>{if(r[k]&&!TRE.test(r[k]))w.push((k==="bas"?"Başlangıç":"Bitiş")+" saati SS:DD biçiminde olmalı.")});
 if(DRE.test(r.d||"")&&P&&(r.d<P[0]||r.d>P[1]))w.push(`Tarih plan döneminin (${P[0]} – ${P[1]}) dışında.`);if(DRE.test(r.d||"")&&DRE.test(r.kayitSon||"")&&r.kayitSon>r.d)w.push("Son kayıt günü etkinlikten sonra olamaz.");
 if(TRE.test(r.bas||"")&&TRE.test(r.bit||"")&&r.bit<r.bas)w.push("Bitiş saati başlangıçtan önce.");return w}
function actHtml(id,r){let A=acts(id,r),m=planMode();if(m==="none")return `<p class="prHint">Pazarlama › Etkinlikler › Aktivite Planı “Plan yok”; aktivite kurulmaz. Plan için kararı değiştirin.</p>`;
 if(!r.d||!DRE.test(r.d))return `<p class="prHint">Aktivite planı etkinlik tarihi girilince kurulur.</p>`;
 let on=A.filter(a=>!a.x),off=A.filter(a=>a.x),row=a=>`<li class="etA${a.ed?" etEd":""}" data-aid="${E(a.aid)}"><code class="prPath" title="Etkinliğe göre gün farkı">${E(tLab(a.gun))}</code><span class="etTi"><span class="prChip">${E(KAN[a.kanal]||a.kanal)}</span> ${E(a.baslik)}<small>${E(FAZ[a.faz]||a.faz)} · ${E(a.tur)} · ${E(a.aid)}</small></span>`+
  `<input class="control" type="text" data-a="d" ${q([id,a.aid])} value="${E(a.d)}" aria-label="${E(a.baslik+" — tarih")}" placeholder="YYYY-AA-GG"><input class="control" type="text" data-a="t" ${q([id,a.aid])} value="${E(a.t)}" aria-label="${E(a.baslik+" — saat")}" placeholder="SS:DD"><input class="control" type="text" data-a="s" ${q([id,a.aid])} value="${E(a.sorumlu)}" aria-label="${E(a.baslik+" — sorumlu")}">`+
  `<span class="etBt">${a.ed?`<button type="button" class="linkBtn" data-ar ${q([id,a.aid])} title="Elle girilen tarih, saat ve sorumluyu siler; hesaplanan değerlere döner">Sıfırla</button>`:""}<button type="button" class="linkBtn" data-ax ${q([id,a.aid])}>Çıkar</button></span></li>`;
 return `<p class="prHint">${m==="short"?"Kısa plan":"Standart plan"} · ${on.length} aktivite (${E(on[0]?on[0].d:"")} – ${E(on.length?on[on.length-1].d:"")}). Hafta sonu ve resmî tatile düşen aktivite en yakın iş gününe kayar; elle değiştirdiğiniz tarih, saat ve sorumlu etkinlik tarihi değişince korunur. Metinler (e-posta, gönderi, reklam) plan dosyasında, şablonun Etkinlikler sekmesinde açılır.</p><ul class="etAL">${on.map(row).join("")}</ul>`+
  (off.length?`<details class="etOff"><summary>Plandan çıkarılan aktiviteler (${off.length})</summary><ul class="etAL">${off.map(a=>`<li class="etA etX"><code class="prPath">${E(tLab(a.gun))}</code><span class="etTi"><span class="prChip">${E(KAN[a.kanal]||a.kanal)}</span> ${E(a.baslik)}</span><span class="etBt"><button type="button" class="linkBtn" data-au ${q([id,a.aid])}>Geri al</button></span></li>`).join("")}</ul></details>`:"")}
const OLC="Kayıt sayısı | 150 | Kayıt formu gönderimi (form_submit); utm_source ve utm_content ile kanal kırılımı\nKatılım oranı | %40 | Katılımcı raporundaki katılan ÷ kayıtlı kişi sayısı\nE-posta performansı | %30 açılma, %5 tıklama | Açılma ve tıklama oranı; utm_content = aktivite kodu";
function form(id,r){let g=p=>r[p]||"",T=types(),Pr=BL.prods(),Bl=blogs();
 let bil=inp(id,"ad","Etkinlik adı","text",g("ad"),{max:100})+`<div class="blGrid">${inp(id,"kisaAd","Kısa ad (konu satırı ve gönderilerde)","text",g("kisaAd"),{max:40})}${T.length?sel(id,"tur","Etkinlik türü",T,g("tur")):""}</div>`+
  `<div class="blGrid">${inp(id,"d","Etkinlik günü","text",g("d"),null,"YYYY-AA-GG")}${inp(id,"kayitSon","Son kayıt günü","text",g("kayitSon"),null,"YYYY-AA-GG")}</div><div class="blGrid">${inp(id,"bas","Başlangıç saati","text",g("bas"),null,"SS:DD")}${inp(id,"bit","Bitiş saati","text",g("bit"),null,"SS:DD")}</div><small class="prMeter bad etW" aria-live="polite">${E(warn(r).join(" "))}</small>`+
  `<div class="blGrid">${inp(id,"format","Format","text",g("format"),null,"Online · Zoom ya da salon adı, şehir")}${inp(id,"ucret","Ücret","text",g("ucret"),null,"Ücretsiz")}</div><div class="blGrid">${inp(id,"yol","Etkinlik sayfası (yol ya da adres)","text",g("yol"),null,"/etkinlikler/…/")}${inp(id,"utm","UTM kampanya adı (boşsa etkinlik-"+id.toLowerCase()+")","text",g("utm"))}</div>`+
  inp(id,"ozet","Özet","area",g("ozet"));
 let prg=inp(id,"konusmacilar","Konuşmacılar (her satıra: Ad | Unvan)","lines",g("konusmacilar"))+inp(id,"program","Program (her satıra: Saat | Başlık | Konuşmacı)","lines",g("program"),null,"11:00–11:25 | Açılış ve gündem | Ad Soyad")+
  inp(id,"konular","Konular (her satıra bir konu)","lines",g("konular"))+`<div class="blGrid">${inp(id,"hedefKitle","Hedef kitle (her satıra bir grup)","lines",g("hedefKitle"))}${inp(id,"sunulanlar","Katılımcılara sunulanlar (her satıra bir öğe)","lines",g("sunulanlar"))}</div>`+inp(id,"notlar","Notlar (her satıra bir not)","lines",g("notlar"));
 let olc=inp(id,"olcum","Ölçüm hedefleri (her satıra: Gösterge | Hedef | Nasıl ölçülür)","lines",g("olcum"))+(g("olcum")?"":`<div class="blAct"><button type="button" class="prAdd" data-olc ${q(id)}>Önerilen göstergeleri ekle</button></div>`)+
  `<div class="blGrid">${Pr.length?sel(id,"urun","Bağlı ürün / hizmet",Pr,g("urun"),"İlişki yok"):""}${Bl.length?sel(id,"blog","Bağlı blog yazısı",Bl,g("blog"),"Bağlı değil"):""}</div>`;
 return [["Bilgi",bil],["Program ve içerik",prg],["Ölçüm ve bağlantılar",olc],["Aktivite planı",`<div class="etActs">${actHtml(id,r)}</div>`]].map(([t,x])=>`<fieldset class="prSec"><legend>${E(t)}</legend>${x}</fieldset>`).join("")+`<div class="blAct"><button type="button" class="prAdd blDelRec" data-del ${q(id)}>Etkinliği sil</button></div>`}
function sorted(){let S=store();return Object.keys(S).sort((a,b)=>{let x=(S[a].d||"9999")+(S[a].bas||""),y=(S[b].d||"9999")+(S[b].bas||"");return x<y?-1:x>y?1:a<b?-1:1})}
function fillPct(r){let P=["ad","d","bas","bit","format","yol","program","olcum"];return Math.round(P.filter(p=>String(r[p]||"").trim()).length/P.length*100)}
function head(id,r,T){let pc=fillPct(r),n=acts(id,r).filter(a=>!a.x).length;return `<span class="prPath">${E(id)}</span><span class="prPath">${E(r.d||"tarih yok")}${r.bas?" "+E(r.bas):""}</span>${r.tur&&T[r.tur]?`<span class="prChip">${E(T[r.tur])}</span>`:""}<span class="prName">${E(r.ad||"Adsız etkinlik")}</span><span class="prChip etN">${n} aktivite</span><span class="prPct${pc===100?" ok":""}" title="Bilgi, program ve ölçüm alanlarının doluluğu">%${pc}</span>`}
function box(f){let S=store(),ids=sorted(),T=Object.fromEntries(types());
 let rows=ids.map(id=>`<details class="prRec" data-eid="${E(id)}"${OPEN.has(id)?" open":""}><summary>${head(id,S[id],T)}</summary><div class="prBody">${OPEN.has(id)?form(id,S[id]):""}</div></details>`).join("");
 return `<div class="field" data-field-id="${FID}"><h2>${E(f.label)}</h2><div class="explain">${E(f.explanation)}</div><div class="prBox etBox"><div class="prHead"><p><b>${ids.length}</b> etkinlik · aktivite planı: ${planMode()==="short"?"kısa":planMode()==="none"?"yok":"standart"} (Pazarlama › Etkinlikler).</p><div class="blAct"><button type="button" class="prAdd" data-add>+ Etkinlik ekle</button></div></div>${ids.length?`<div class="prList">${rows}</div>`:`<p class="prEmpty">Henüz etkinlik yok. “+ Etkinlik ekle” ile ekleyin; tarih girilince aktivite planı kendiliğinden kurulur.</p>`}</div>${rule(f)?`<div class="rule"><b>BU SEÇİMDEN OLUŞAN KURAL</b>${E(rule(f))}</div>`:""}</div>`}
/* kayıt işlemleri */
function nextId(){let n=Object.keys(store()).map(k=>+((k.match(/^E-(\d+)$/)||[])[1]||0)).reduce((a,b)=>Math.max(a,b),0);return "E-"+String(n+1).padStart(2,"0")}
function commit(redraw){let S=store();if(Object.keys(S).length)state[KEY]=S;else delete state[KEY];faAuto(FID);save();renderRules();renderProgress();if(redraw)refreshField(FID)}
function rec(id){return document.querySelector(`.prRec[data-eid="${CSS.escape(id)}"]`)}
function redrawActs(id){let d=rec(id),r=store()[id]||{};if(!d)return;let a=d.querySelector(".etActs");if(a&&!a.contains(document.activeElement))a.innerHTML=actHtml(id,r);let s=d.querySelector("summary");if(s)s.innerHTML=head(id,r,Object.fromEntries(types()))}
function put(id,p,v){let S=store();S[id]=S[id]||{};if(v==="")delete S[id][p];else S[id][p]=v;state[KEY]=S;commit(false);let d=rec(id);if(!d)return;let w=d.querySelector(".etW");if(w)w.textContent=warn(S[id]).join(" ");
 if(["d","bas","tur"].includes(p))redrawActs(id);else{let s=d.querySelector("summary");if(s)s.innerHTML=head(id,S[id],Object.fromEntries(types()))}}
function putA(id,aid,p,v){let S=store(),r=S[id];if(!r)return;let O=r.akt=r.akt||{},o=O[aid]=O[aid]||{},A=acts(id,Object.assign({},r,{akt:{}})).find(a=>a.aid===aid),base=A?{d:A.d,t:A.t,s:A.sorumlu}[p]:"";
 if(v===""||v===base)delete o[p];else o[p]=v;if(!Object.keys(o).length)delete O[aid];if(!Object.keys(O).length)delete r.akt;state[KEY]=S;commit(false);let li=document.querySelector(`.etA[data-aid="${CSS.escape(aid)}"]`);if(li)li.classList.toggle("etEd",!!(O[aid]&&(O[aid].d||O[aid].t||O[aid].s)))}
const MO={ad:{max:100},kisaAd:{max:40}};
document.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!d.dataset.eid)return;let id=d.dataset.eid;if(d.open){OPEN.add(id);let b=d.querySelector(".prBody");if(b&&!b.children.length)b.innerHTML=form(id,store()[id]||{})}else OPEN.delete(id)},true);
document.addEventListener("input",e=>{let t=e.target;if(!t.closest||!t.closest(".etBox"))return;if(t.dataset.a){if(!requireProject()){refreshField(FID);return}let [id,aid]=JSON.parse(t.dataset.r),v=t.value.trim();if(t.dataset.a==="d"&&v&&!DRE.test(v))return;if(t.dataset.a==="t"&&v&&!TRE.test(v))return;putA(id,aid,t.dataset.a,v);return}
 if(!t.dataset.m)return;if(!requireProject()){refreshField(FID);return}put(JSON.parse(t.dataset.r),t.dataset.m,t.value);let o=MO[t.dataset.m],m=t.parentElement.querySelector(".prMeter");if(o&&m){let w=document.createElement("div");w.innerHTML=BL.meter(t.value,o);m.replaceWith(w.firstChild)}},true);
document.addEventListener("change",e=>{let t=e.target;if(!t.closest||!t.closest(".etBox"))return;if(t.matches("select[data-m]"))t.dispatchEvent(new Event("input",{bubbles:true}));else if(t.dataset.a){let [id]=JSON.parse(t.dataset.r);setTimeout(()=>redrawActs(id),0)}},true);
document.addEventListener("click",e=>{let b=e.target.closest&&e.target.closest(".etBox button");if(!b)return;
 if(b.hasAttribute("data-add")){if(!requireProject())return;let id=nextId(),S=store(),P=BL.period(),T=types();S[id]={ad:""};if(T.length===1)S[id].tur=T[0][0];if(P)S[id].d=P[0];state[KEY]=S;OPEN.add(id);commit(true);let x=rec(id);x=x&&x.querySelector('[data-m="ad"]');if(x)x.focus();return}
 if(!requireProject())return;let k=JSON.parse(b.dataset.r||"null");
 if(b.hasAttribute("data-del")){if(!confirm("Bu etkinlik ve aktivite planı silinsin mi?"))return;let S=store();delete S[k];OPEN.delete(k);state[KEY]=S;commit(true)}
 else if(b.hasAttribute("data-olc")){put(k,"olcum",OLC);refreshField(FID)}
 else if(b.hasAttribute("data-ax")||b.hasAttribute("data-au")||b.hasAttribute("data-ar")){let [id,aid]=k,S=store(),r=S[id];if(!r)return;let O=r.akt=r.akt||{},o=O[aid]=O[aid]||{};
  if(b.hasAttribute("data-ax"))o.x=1;else if(b.hasAttribute("data-au"))delete o.x;else{delete o.d;delete o.t;delete o.s}
  if(!Object.keys(o).length)delete O[aid];if(!Object.keys(O).length)delete r.akt;state[KEY]=S;commit(false);let a=rec(id);a=a&&a.querySelector(".etActs");if(a)a.innerHTML=actHtml(id,r);redrawActs(id)}},true);
/* kural, özet, kayıt */
function recSum(){let n=Object.keys(store()).length;return n?n+" etkinlik":""}
function recRule(){let S=store(),ids=sorted(),T=Object.fromEntries(types()),L=ids.map(i=>`${S[i].ad||"Adsız"}${S[i].d?" ("+S[i].d+(S[i].tur&&T[S[i].tur]?", "+T[S[i].tur]:"")+")":""}`),n=ids.reduce((a,i)=>a+acts(i,S[i]).filter(x=>!x.x).length,0),o=ids.filter(i=>S[i].olcum).length;
 return `Etkinlik kayıtları: ${ids.length} etkinlik${L.length?` — ${L.slice(0,6).join("; ")}${L.length>6?` ve ${L.length-6} etkinlik daha`:""}`:""}. Aktivite planı ${planMode()==="short"?"kısa plan":planMode()==="none"?"kurulmaz":"standart plan"}${n?` (${n} aktivite)`:""}; aktiviteler etkinlik gününe göre gün farkıyla sıralanır, hafta sonu ve resmî tatile düşen aktivite en yakın iş gününe kayar. Son kayıt günü etkinlikten sonra olamaz; her kanalın kayıt bağlantısı ayrı UTM taşır (utm_content = aktivite kodu).${o?` ${o} etkinlikte ölçüm hedefi var.`:""} Kayıtlar plan dosyasının Etkinlikler bölümüne aktarılır.`}
window.REC[FID]={isset:()=>Object.keys(store()).some(k=>filled(store()[k])),rule:recRule,sum:recSum,box,
 closed:`<section class="gCard"><h3>Bu alt menü şu an kapalı</h3><p>Etkinlikler, Pazarlama › Etkinlikler › Etkinlik Planlaması “Evet” iken kullanılır.</p><p><button type="button" class="btn dark" onclick="goToField('mk_events','mk_evt_on')">Kararı aç →</button></p></section>`};
/* takvim (8.5) */
function cal(){if(!shown(FI[FID]))return [];let S=store(),T=Object.fromEntries(types()),o=[];sorted().forEach(id=>{let r=S[id];if(!r.d||!DRE.test(r.d))return;o.push({k:"evt",d:r.d,t:TRE.test(r.bas||"")?r.bas:"",te:TRE.test(r.bit||"")?r.bit:"",id,no:id,title:r.ad||"Adsız etkinlik",chip:r.tur&&T[r.tur]?T[r.tur]:"Etkinlik"});
 acts(id,r).filter(a=>!a.x).forEach(a=>o.push({k:"act",d:a.d,t:a.t,id,no:a.aid,title:a.baslik,chip:KAN[a.kanal]||a.kanal}))});return o}
window.ET={store,sorted,acts,cal,open:id=>OPEN.add(id)};
/* plan dosyasına aktarım */
function fill(v,M){if(typeof v==="string"){let s=v.split("{marka}").join(M.marka).split("{onek}").join(M.onek);return M.etiket?s.split("{etiket}").join(M.etiket):s.replace(/[ \t]*\n*[ \t]*\{etiket\}/g,"")}if(Array.isArray(v))return v.map(x=>fill(x,M));if(v&&typeof v==="object"){let o={};Object.keys(v).forEach(k=>o[k]=fill(v[k],M));return o}return v}
function extra(i,M){let x=[];if(i===0&&M.pr.includes("retention"))x.push("Katılımcı listesinin saklama süresini aydınlatma metnine yazın; süre dolunca liste silinir.");if(i===21&&M.pr.includes("recording"))x.push("Oturum başında fotoğraf / video kaydı yapıldığını duyurun.");if(i===24&&M.af.includes("survey"))x.push("Memnuniyet anketi bağlantısını ekleyin (en çok 5 soru).");return x}
function exportList(B){let S=store(),pm=typeof window.prIdMap==="function"?window.prIdMap():{},PI=typeof window.prItems==="function"?window.prItems():[],BS=BL.store(),T=Object.fromEntries(types()),skip=[];
 let tag=String(sv("mk_brand_hashtag")||"").trim(),M={marka:String(state.mk_brand_name||state.project_name||"Marka").trim()||"Marka",etiket:tag?(tag[0]==="#"?tag:"#"+tag):"",onek:String(mkT("mk_prefix")||"{{ONEK}}").toUpperCase(),pr:sv("mk_evt_privacy")||[],af:sv("mk_evt_after")||[]};
 let L=sorted().filter(id=>{let r=S[id],ok=DRE.test(r.d||"")&&TRE.test(r.bas||"")&&TRE.test(r.bit||"")&&r.bit>=r.bas;if(!ok)skip.push(id);return ok}).map(id=>{let r=S[id],o={id,utm:r.utm||"etkinlik-"+id.toLowerCase(),ad:r.ad||id,kisaAd:r.kisaAd||r.ad||id,ozet:r.ozet||"",yol:r.yol||"",d:r.d,bas:r.bas,bit:r.bit,format:r.format||"",ucret:r.ucret||""};
  if(DRE.test(r.kayitSon||"")&&r.kayitSon<=r.d)o.kayitSon=r.kayitSon;
  o.konusmacilar=lines(r.konusmacilar).map(x=>{let c=cells(x);return {ad:c[0],unvan:c[1]||""}});o.program=lines(r.program).map(x=>{let c=cells(x);return c.length>2?{saat:c[0],baslik:c[1],konusmaci:c[2]}:c.length===2?{saat:c[0],baslik:c[1],konusmaci:""}:{saat:"",baslik:c[0],konusmaci:""}});
  ["konular","hedefKitle","sunulanlar","notlar"].forEach(k=>o[k]=lines(r[k]));if(T[r.tur])o.notlar.unshift("Etkinlik türü: "+T[r.tur]+".");
  if(r.urun){let u=PI.find(x=>x.k===r.urun);o.notlar.push("Bağlı ürün / hizmet: "+(u?u.ad:r.urun)+(pm[r.urun]?" ("+pm[r.urun]+")":"")+".")}if(r.blog&&BS[r.blog])o.notlar.push("Bağlı blog yazısı: "+r.blog+" · "+(BS[r.blog].baslik||"")+".");
  o.olcum=lines(r.olcum).map(x=>{let c=cells(x);return c.length>2?[c[0]+(c[1]?" — hedef: "+c[1]:""),c[2]]:[c[0],c[1]||""]});
  o.aktiviteler=acts(id,r).filter(a=>!a.x).map(a=>{let ek=fill(JSON.parse(JSON.stringify(a.ek||{})),M),x=extra(a.i,M);if(x.length)ek.maddeler=(ek.maddeler||[]).concat(x);return Object.assign({id:a.aid,d:a.d,t:a.t,faz:a.faz,kanal:a.kanal,tur:a.tur,baslik:a.baslik,sorumlu:a.sorumlu},ek)});return o});
 return {L,skip}}
if(typeof mkPlanData==="function"){const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{if(B.etkinlikler&&shown(FI[FID])){let {L}=exportList(B);if(L.length)B.etkinlikler.liste=L}}catch(e){console.error("Etkinlik aktarımı",e)}return B}}
if(typeof mkIssues==="function"){const _mi=mkIssues;mkIssues=function(){let L=_mi.apply(this,arguments);if(!shown(FI[FID]))return L;let S=store(),ids=Object.keys(S),c=`<button type="button" class="linkBtn" onclick="goToField('ip_events','${FID}')">İçerik Planlama › Etkinlikler</button>`;
 let nd=ids.filter(i=>!DRE.test(S[i].d||"")||!TRE.test(S[i].bas||"")||!TRE.test(S[i].bit||"")||S[i].bit<S[i].bas),ks=ids.filter(i=>DRE.test(S[i].kayitSon||"")&&DRE.test(S[i].d||"")&&S[i].kayitSon>S[i].d);
 if(nd.length)L.push(`${nd.length} etkinliğin tarihi ya da başlangıç / bitiş saati eksik veya hatalı; bu etkinlikler dosyaya aktarılmaz — ${c}.`);if(ks.length)L.push(`${ks.length} etkinlikte son kayıt günü etkinlikten sonra; dosyaya yazılmaz — ${c}.`);return L}}
window.etExport=exportList;
})();
