/* 4 Göz Onay Akışı — akış diyagramı, durum göstergeleri ve etkinleştirme anahtarı (2026-11-10, kullanıcının
   "Modül: 4 Göz Onay Akışı (Four-Eyes Approval Workflow)" yönergesi). Bölüm: İş Akışları ve Onay Mekanizmaları (approvals).
   Kararlar ve kurallar genel mekanizmayla çalışır (veri: docs/onay-akisi/); bu betik yalnız görünüm ekler:
   - rehberde ve "tüm kararlar" görünümünde akış diyagramı + durum göstergeleri (seçimlere göre canlı),
   - tek karar görünümünde akışla ilgili kararlarda kısa diyagram,
   - approval_enabled kararında Evet / Hayır kartları yerine anahtar (checkbox / switch) + "Kullanmayacağım".
   Kaynak docs/v26/v26-approval.{js,css} → docs/v26/onay_arayuz_ekle.py */
(()=>{
const SEC="approvals",EN="approval_enabled",FLOWF=new Set([EN,"approval_levels","approval_stage_mode","approval_extra_states","approval_scope"]);
if(!(DATA.sections||[]).some(s=>s.id===SEC))return;
const lb=(id,v)=>{let f=FI[id];return f?String(lab(f,v)).replace(/\s*\(önerilen\)/g,""):v};
const on=()=>state[EN]===true,decided=()=>state[EN]===true||state[EN]===false;
function stages(){let lv=state.approval_levels,md=state.approval_stage_mode;
 if(lv==="six")return md==="parallel"||md==="mixed"?[["Onay Bekliyor","2 bağımsız onaylayan · paralel"]]:[["Onay Bekliyor","1. onaylayan"],["Onay Bekliyor","2. onaylayan (bağımsız)"]];
 if(lv==="multi")return md==="parallel"?[["Onay Bekliyor","Bütün aşamalar · paralel"]]:[["Aşama 1","Ekip / birim yöneticisi"],["Aşama 2","İlgili birim"+(md==="mixed"?" · paralel":"")],["Aşama 3","Üst onay"]];
 if(lv==="dynamic")return [["Onay Bekliyor","Kurala göre 1–3 onay"]];
 return [["Onay Bekliyor","Onaylayan (Checker)"]]}
const XS={withdrawn:["↩","Geri çekildi"],expired:["⌛","Süresi doldu"],cancelled:["⊘","İptal edildi"],on_hold:["…","Bilgi bekleniyor"],failed:["⚠","Uygulama hatası"]};
function st(cls,ic,t,s){return `<li class="apSt ${cls}"><span class="apIc" aria-hidden="true">${ic}</span><span class="apTx"><b>${E(t)}</b>${s?`<small>${E(s)}</small>`:""}</span></li>`}
function box(compact){let ids=F.filter(f=>f.section===SEC&&shown(f)&&navF(f)),done=ids.filter(isset).length,en=on();
 let pill=en?'<span class="apPill on">● Etkin</span>':decided()?'<span class="apPill off">○ Kullanılmıyor</span>':'<span class="apPill none">◌ Karar verilmedi</span>';
 let sg=stages(),flow=`<ol class="apFlow" aria-label="Onay durumları sırasıyla">${st("draft","✎","Taslak","Hazırlayan (Maker)")}${sg.map(([t,s])=>st("pend","⏳",t,s)).join("")}<li class="apSt apOut"><ul aria-label="Onay kararı">${st("ok","✓","Onaylandı","")}${st("rev","↺","Revizyon İstendi","Taslak'a döner")}${st("rej","✕","Reddedildi","")}</ul></li>${st("done","●","Tamamlandı","İşlem uygulanır")}</ol>`;
 let xs=(Array.isArray(state.approval_extra_states)&&en?state.approval_extra_states:[]).filter(k=>XS[k]).map(k=>`<span class="apX">${XS[k][0]} ${E(XS[k][1])}</span>`).join("");
 let facts=[];
 if(en){if(state.approval_levels)facts.push(["Onay seviyesi",lb("approval_levels",state.approval_levels)]);
  let sc=state.approval_scope;if(Array.isArray(sc)&&sc.length)facts.push(["Onaya tabi işlem",sc.length+" tür"]);
  let ru=state.approval_rules;if(Array.isArray(ru)&&ru.length)facts.push(["Kural ölçütleri",ru.map(v=>lb("approval_rules",v)).join(", ")]);
  if(state.approval_sla)facts.push(["Onay süresi",lb("approval_sla",state.approval_sla)])}
 let guard=`<ul class="apGuard" aria-label="Her durumda geçerli kurallar"><li>✕ Kendi işlemini onaylama engelli (sunucuda)</li><li>↺ Onay sonrası kritik değişiklik → yeniden onay</li><li>☰ Değiştirilemez denetim kaydı</li></ul>`;
 let note=en?"":`<p class="apOffNote">${decided()?"Modül kapalı: projeye onay kuralı, tablosu ya da bağımlılığı eklenmez. Aşağıdaki akış, etkinleştirilirse nasıl çalışacağını gösterir.":"Modülü kullanıp kullanmayacağınıza 4 Göz Onay Akışı kararında karar verin; etkinleştirince ayarlar açılır."}</p>`;
 return `<section class="apBox${en?"":" apMuted"}${compact?" apCompact":""}" aria-label="4 Göz Onay Akışı durumu"><div class="apHead"><b>4 Göz Onay Akışı</b>${pill}${en?`<span class="apCnt">${done}/${ids.length} karar verildi</span>`:""}</div>${note}${flow}${xs?`<div class="apXs"><span>Ek durumlar:</span>${xs}</div>`:""}${compact?"":guard}${facts.length&&!compact?`<dl class="apFacts">${facts.map(([k,v])=>`<div><dt>${E(k)}</dt><dd>${E(v)}</dd></div>`).join("")}</dl>`:""}</section>`}
function toggle(fe){let o=fe.querySelector(":scope > .options");if(!o||fe.querySelector(".apToggle"))return;let f=FI[EN],en=on(),d=decided();
 let w=document.createElement("div");w.className="apToggle";
 w.innerHTML=`<div class="apTgRow"><button type="button" class="apSw" role="switch" aria-checked="${en}" aria-labelledby="apTgL" onclick="apSet(${!en})"><span class="apKnob" aria-hidden="true"></span></button><div class="apTgT"><b id="apTgL">4 Göz Onay Akışını etkinleştir</b><span>${en?"Etkin — onaya tabi işlemler, roller ve kurallar aşağıdaki ayarlarda yapılandırılır.":d?"Kullanılmıyor — projeye onay modülü eklenmez.":"Henüz karar verilmedi."}</span></div>${!d?`<button type="button" class="apNo" onclick="apSet(false)">Kullanmayacağım</button>`:""}</div><details class="apWhen"><summary>Ne zaman etkinleştirilir, ne zaman gerekmez?</summary><dl><dt>Etkinleştirin</dt><dd>${E(f.yes.scenario)} <i>${E(f.yes.example)}</i></dd><dt>Gerekmez</dt><dd>${E(f.no.scenario)} <i>${E(f.no.example)}</i></dd></dl></details>`;
 o.replaceWith(w)}
window.apSet=v=>setv(EN,v);
function deco(){if(active!==SEC)return;
 let fe=fieldBox.querySelector(`.field[data-field-id="${EN}"]`);if(fe)toggle(fe);
 if(fieldBox.querySelector(".apBox"))return;
 if(typeof guideMode==="function"&&guideMode()){let g=fieldBox.querySelector(".guide .gStart");if(g)g.insertAdjacentHTML("afterend",box(false));return}
 let first=fieldBox.querySelector(":scope > .field");if(!first)return;
 if(!activeFieldId)first.insertAdjacentHTML("beforebegin",box(false));
 else if(FLOWF.has(activeFieldId))first.insertAdjacentHTML("beforebegin",box(true))}
const _rf=renderFields;renderFields=function(){let r=_rf.apply(this,arguments);try{deco()}catch(e){console.error("approval",e)}return r};
const _ref=refreshField;refreshField=function(id){let r=_ref.apply(this,arguments);try{if(id===EN){let fe=fieldBox.querySelector(`.field[data-field-id="${EN}"]`);if(fe)toggle(fe)}}catch(e){console.error("approval",e)}return r};
try{deco()}catch(e){console.error("approval",e)}
})();
