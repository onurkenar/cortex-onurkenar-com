/* Tutarlılık katmanı (2026-11-15, kullanıcı isteği: "birbiri ile çakışan veya çok benzer olan maddeler var mı analizi yap"
   → A / B / C maddeleri). Veri tarafı (derive, etiketler, taşıma, refs) docs/v26/tutarlilik.json → tutarlilik_ekle.py.
   Bu blok:
   1) ocDv'ye görünürlük şartı: türetmenin kaynağı gizliyse (koşulu kalkmışsa) türetme uygulanmaz, karar normal sorulur.
   2) Seçenek bağlantıları (LN; imply:1 olanlar tek yönlü — yalnız kaynakta seçiliyken kilitler ve açar, değilse serbest): bir kararın tek bir seçeneği başka bir karardan gelir. Kaynak karar görünür ve verilmişse
      hedef seçenek kilitlidir (tıklanamaz, "… kararından gelir · Kaynağı düzenle →" notu) ve hedef karar verilmişse
      ocSync sırasında state'e kaynağa göre yazılır (açık / kapalı). Hedef karar hiç verilmemişse state'e dokunulmaz
      (karar kendiliğinden "verildi" sayılmasın diye). Böylece Proje Kuralları, Claude promptu, JSON ve Yapılacaklar
      çelişkili kural taşımaz.
   3) Çelişki uyarıları (CF): iki karar birlikte çelişen değer taşıyorsa her iki kararın üstünde "⚠ Çelişki" kutusu ve
      diğer karara bağlantı. Değerler değiştirilmez; karar kullanıcıda kalır.
   Kaynak docs/v26/v26-consistency.{js,css} → docs/v26/tutarlilik_ekle.py */
(function(){
const LN=[
 // A2 — onay penceresinin davranışı Gizlilik / KVKK › Çerez İzin Davranışı'ndan
 {t:"gg_cm_checks",v:"equal",s:"cookie_behavior",on:["equal_buttons"]},
 {t:"gg_cm_checks",v:"withdraw",s:"cookie_behavior",on:["revisit"]},
 {t:"gg_cm_checks",v:"log",s:"cookie_behavior",on:["consent_log"]},
 // A6 — e-posta izin politikası Pazarlama › Mailing'den, modül onu uygular
 {t:"ml_subscription",v:"double_optin",s:"mk_mail_consent",on:["double"]},
 {t:"ml_subscription",v:"iys_sync",s:"mk_mail_consent",on:["iys"]},
 {t:"ml_deliverability",v:"warmup",s:"mk_mail_consent",on:["warmup"]},
 // A7 — panelden sosyal paylaşımın onayı Pazarlama › İş Akışı & Onay'dan
 {t:"sp_publishing",v:"approval",s:"mk_flow",on:["simple","legal","staged"]},
 // A9 — Meta reklam ön koşulları Meta Servisleri kurulumundan
 {t:"mk_meta_prereq",v:"pixel",s:"mt_services",on:["pixel"]},
 {t:"mk_meta_prereq",v:"capi",s:"mt_px_method",on:["server","gateway","partner","sgtm"]},
 {t:"mk_meta_prereq",v:"domain",s:"mt_px_settings",on:["domain"]},
 {t:"mk_meta_prereq",v:"bm",s:"mt_services",on:["portfolio"]},
 // A10 — kod kalite kapısındaki kontrol tamamlanma kontrollerinde de olur (tek yönlü: kapıda olmayan serbest)
 {t:"definition_done",v:"Build",s:"quality_gate",on:["Build"],imply:1},
 {t:"definition_done",v:"Type Check",s:"quality_gate",on:["Type Check"],imply:1},
 {t:"definition_done",v:"Lint",s:"quality_gate",on:["Lint"],imply:1},
 {t:"definition_done",v:"Unit Tests",s:"quality_gate",on:["Tests"],imply:1},
 {t:"definition_done",v:"Security",s:"quality_gate",on:["Security Scan"],imply:1}];
const CF=[
 // A3 — yüzey efekti × yüzey işleme
 {a:"design_surface",av:["Glassmorphism","Liquid Glass"],b:"design_surface_treatment",bv:["Flat"],m:"Cam efekti “Flat — Düz” yüzey işlemesiyle birlikte uygulanamaz. Yüzey İşleme “Glass — Cam” ya da “Layered — Katmanlı” olmalı ya da yüzey efekti değiştirilmeli."},
 {a:"design_surface",av:["Skeuomorphism","Neumorphism","Claymorphism"],b:"design_surface_treatment",bv:["Flat"],m:"Gölge ve hacme dayanan yüzey efekti “Flat — Düz” yüzey işlemesiyle çelişir. Yüzey İşleme “Elevated”, “Layered” ya da “Textured” olmalı ya da yüzey efekti değiştirilmeli."},
 {a:"design_surface",av:["None Surface"],b:"design_surface_treatment",bv:["Glass"],m:"“Yüzey efekti yok — düz yüzeyler” seçiliyken Yüzey İşleme “Glass — Cam” olamaz; ikisinden biri değiştirilmeli."},
 // A4 — tema yaklaşımı × renk teması
 {a:"design_theme_interaction",av:["Dark-First"],b:"color_theme",bv:["Light"],m:"“Dark-First — Önce Koyu Tasarım” yalnız açık temalı bir siteyle çelişir. Renk teması “Dark Mode”, “Light + Dark Mode” ya da “System Preference” olmalı ya da Dark-First kaldırılmalı."},
 // A1 / A2 — onay modu bir onay penceresi ister
 {a:"gg_cm_mode",av:["basic","advanced"],b:"cookie_manager",bv:["None"],m:"Onay modu, ziyaretçiden onay alan bir çerez / onay penceresiyle çalışır; Çerez / Onay Platformu “Yok” iken onay modu uygulanamaz."}];
const act=s=>{let f=FI[s];return !!f&&shown(f)&&isset(f)};
const has=(s,on)=>{let v=state[s];return Array.isArray(v)?v.some(x=>on.includes(x)):on.includes(v)};
const path=f=>{let a=AREA(SI[f.section]);return (AREA_LB[a]||"Kararlar")+" › "+SI[f.section].name+" › "+f.label};
const vlab=f=>{let v=state[f.id];return (Array.isArray(v)?v:[v]).map(x=>String(lab(f,x)).replace(/\s*\(önerilen\)/g,"")).join(", ")};
const cfOn=c=>FI[c.a]&&FI[c.b]&&shown(FI[c.a])&&shown(FI[c.b])&&has(c.a,c.av)&&has(c.b,c.bv);
const lnOn=l=>act(l.s)&&(!l.imply||has(l.s,l.on));
function lnLock(id,v){return LN.find(l=>l.t===id&&l.v===v&&lnOn(l))}
function lnSync(){LN.forEach(l=>{let t=FI[l.t];if(!t||!lnOn(l)||!shown(t)||!isset(t))return;let a=[...state[l.t]],want=has(l.s,l.on),inn=a.includes(l.v);
 if(want&&!inn)state[l.t]=opts(t).map(o=>o.value).filter(x=>x===l.v||a.includes(x)).concat(a.filter(x=>!opts(t).some(o=>o.value===x)));
 else if(!want&&inn)state[l.t]=a.filter(x=>x!==l.v)})}
/* 1) türetme yalnız görünür kaynaktan */
const _dv=ocDv;ocDv=function(f){let d=f&&f.derive,s=d&&FI[d.from];if(s&&!shown(s))return null;return _dv.apply(this,arguments)};
/* 2) bağlantılar ocSync'te (save ve renderRules başında) uygulanır */
const _os=ocSync;ocSync=function(){let r=_os.apply(this,arguments);lnSync();return r};
const _sv=setv;setv=function(id,v){let l=lnLock(id,v);if(l){let el=document.querySelector('.field[data-field-id="'+id+'"] .lnNote[data-v="'+CSS.escape(String(v))+'"]');if(el){el.classList.remove("lnFlash");void el.offsetWidth;el.classList.add("lnFlash");el.focus&&el.querySelector("button")&&el.querySelector("button").focus()}return}return _sv.apply(this,arguments)};
function deco(){document.querySelectorAll(".field[data-field-id]").forEach(el=>{let id=el.dataset.fieldId,f=FI[id];if(!f)return;
 el.querySelectorAll(":scope>.cfWarn").forEach(x=>x.remove());
 let L=LN.filter(l=>l.t===id);if(L.length){let os=el.querySelectorAll(":scope>.options>.option"),O=opts(f);L.forEach(l=>{let o=os[O.findIndex(x=>x.value===l.v)];if(!o)return;
  o.querySelectorAll(":scope>.lnNote").forEach(x=>x.remove());let on=lnOn(l);o.classList.toggle("lnLock",on);if(on)o.setAttribute("aria-disabled","true");else o.removeAttribute("aria-disabled");if(!on)return;
  let s=FI[l.s];o.insertAdjacentHTML("beforeend",`<small class="lnNote" data-v="${E(String(l.v))}">🔗 ${E(path(s))} kararından gelir — ${l.imply?"orada seçili olduğu için burada da zorunlu":has(l.s,l.on)?"açık":"kapalı"}. Burada değiştirilemez. <button type="button" class="linkBtn" onclick="event.stopPropagation();goToField('${s.section}','${s.id}')">Kaynağı düzenle →</button></small>`)})}
 let C=CF.filter(c=>(c.a===id||c.b===id)&&cfOn(c));if(!C.length)return;
 let html=C.map(c=>{let o=FI[c.a===id?c.b:c.a];return `<div class="cfWarn" role="note"><b>⚠ Çelişki</b> ${E(c.m)} <span class="cfOther">Diğer karar: ${E(path(o))} — “${E(vlab(o))}”.</span> <button type="button" class="linkBtn" onclick="goToField('${o.section}','${o.id}')">Diğer karara git →</button></div>`}).join("");
 let ex=el.querySelector(":scope>.explain");if(ex)ex.insertAdjacentHTML("afterend",html);else el.insertAdjacentHTML("afterbegin",html)})}
window.cfList=()=>CF.filter(cfOn).map(c=>[c.a,c.b,c.m]);window.lnLock=lnLock;
const _rf=renderFields;renderFields=function(){let r=_rf.apply(this,arguments);deco();return r};
const _rr=renderRules;renderRules=function(){let r=_rr.apply(this,arguments);deco();return r};
if(typeof refreshField==="function"){const _rfi=refreshField;refreshField=function(){let r=_rfi.apply(this,arguments);deco();return r}}
})();
