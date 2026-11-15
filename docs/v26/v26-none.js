/* "Yok" seçeneği olan serbest metin kararları (2026-11-15, kullanıcı isteği: "1.2.11 Ek İletişim Notları > 'Ek İletişim Notu Yok'
   seçeneği ekle"). NONE_F'deki metin kararında kutunun altında işaret kutusu; işaretlenince karar verilmiş sayılır (isset), kural
   NONE_F[id].rule olur, yazılmış metin silinmez ama kurala girmez. Kayıt state.fieldNone = {alan id: true} (boşalınca silinir;
   JSON İndir'de Proje Kararları parçasındadır — yalnız proje / Ortak Bilgiler alanlarında kullanın). Kutuya yeniden metin
   yazılınca işaret kendiliğinden kalkar. Kaynak docs/v26/v26-none.js → docs/v26/yok_secenegi_ekle.py */
const NONE_F={
 mk_contact:{label:"Ek iletişim notu yok",rule:"Ek iletişim notu yoktur: faks, KEP adresi, ikinci e-posta gibi ek iletişim bilgisi kullanılmaz; iletişim bilgileri yalnız İletişim & Adres bölümündeki alanlardan alınır."}};
function noneOn(f){let n=state.fieldNone;return !!f&&!!NONE_F[f.id]&&!!n&&typeof n==="object"&&n[f.id]===true}
function noneRule(f){return NONE_F[f.id].rule}
function noneBox(f){let d=NONE_F[f.id];if(!d||(f.type!=="text"&&f.type!=="textarea"))return "";let on=noneOn(f),has=String(state[f.id]??"").trim()!=="",id="none-"+f.id;
 return `<div class="noneBox${on?" on":""}"><label for="${id}" data-v26="none"><input type="checkbox" id="${id}" data-v26="none"${on?" checked":""} onchange="noneSet(${E(JSON.stringify(f.id))},this.checked,this)"><span>${E(d.label)}</span></label>${on&&has?'<small class="noneHint">Yazdığınız metin silinmedi ama kurala girmez; kutuya yeniden yazarsanız bu işaret kalkar.</small>':""}</div>`}
function noneSet(id,on,el,quiet){if(!quiet&&!requireProject()){if(el)el.checked=!on;return}
 let n=Object.assign({},state.fieldNone&&typeof state.fieldNone==="object"?state.fieldNone:{});if(on)n[id]=true;else delete n[id];
 if(Object.keys(n).length)state.fieldNone=n;else delete state.fieldNone;save();renderRules();renderProgress();
 if(quiet){let b=document.querySelector('.field[data-field-id="'+id+'"] .noneBox');if(b){b.classList.remove("on");let c=b.querySelector("input");if(c)c.checked=false;let h=b.querySelector(".noneHint");if(h)h.remove()}return}
 if(typeof refreshField==="function")refreshField(id);else renderFields()}
document.addEventListener("input",e=>{let t=e.target;if(!t||t.tagName!=="TEXTAREA"&&t.tagName!=="INPUT")return;let fd=t.closest&&t.closest(".field[data-field-id]");if(!fd)return;
 let id=fd.getAttribute("data-field-id"),f=FI[id];if(f&&noneOn(f)&&!t.closest(".noneBox")&&String(t.value).trim())noneSet(id,false,null,true)},true);
