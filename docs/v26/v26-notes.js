/* Ek açıklama (2026-11-13, kullanıcı isteği: "seçimlere ilave açıklama ekleyebilmeliyim").
   Her karara (serbest metin alanları hariç) isteğe bağlı açıklama: state.fieldNotes = {alan id: metin}; boşalınca silinir.
   Açıklama karar verilmişse kuralın sonuna "Ek açıklama: …" olarak eklenir (rule → fnAdd); böylece Proje Kuralları,
   Claude promptu, talimat dosyası, JSON, Yapılacaklar ve SEO denetim promptu aynı metni alır. Kaynak docs/v26/v26-notes.js
   → docs/v26/ek_aciklama_ekle.py */
const FN_OPEN={};
function fnOk(f){return !!f&&f.type!=="text"&&f.type!=="textarea"}
function fnGet(id){let n=state.fieldNotes;return n&&typeof n==="object"&&typeof n[id]==="string"?n[id]:""}
function fnClean(t){let x=String(t||"").replace(/\s+/g," ").trim();return !x||/[.!?…)\]"”]$/.test(x)?x:x+"."}
function fnAdd(f,r){if(!r||!fnOk(f))return r;let t=fnClean(fnGet(f.id));return t?r.replace(/\s+$/,"")+" Ek açıklama: "+t:r}
function fnHint(f){return isset(f)?"Kuralın sonuna “Ek açıklama:” olarak eklenir; Proje Kuralları’na, Claude promptuna, talimat dosyasına ve JSON’a girer.":"Karar verildiğinde kuralın sonuna “Ek açıklama:” olarak eklenir."}
function fnBox(f){if(!fnOk(f))return "";let v=fnGet(f.id),has=!!v.trim(),q=E(JSON.stringify(f.id)),open=FN_OPEN[f.id]!==undefined?FN_OPEN[f.id]:has;
 return `<details class="fnBox${has?" has":""}"${open?" open":""} ontoggle="fnTog(${q},this.open)"><summary data-v26="fn">Ek açıklama <span class="fnSt">${has?"eklendi":"isteğe bağlı"}</span></summary><div class="fnIn"><textarea class="control fnText" rows="3" aria-label="${E(f.label)} için ek açıklama" placeholder="Bu seçimle ilgili ayrıntı, istisna ya da gerekçe yazın…" oninput="fnSet(${q},this.value)">${E(v)}</textarea><small class="fnHint">${fnHint(f)}</small></div></details>`}
function fnTog(id,o){FN_OPEN[id]=o}
function fnSet(id,v){if(!requireProject())return;let n=state.fieldNotes&&typeof state.fieldNotes==="object"&&!Array.isArray(state.fieldNotes)?state.fieldNotes:(state.fieldNotes={});if(String(v).trim())n[id]=String(v);else delete n[id];if(!Object.keys(n).length)delete state.fieldNotes;save();fnSync(id);renderRules()}
function fnSync(id){let f=FI[id],el=document.querySelector('.field[data-field-id="'+id+'"]');if(!f||!el)return;let has=!!fnGet(id).trim(),b=el.querySelector(".fnBox");if(b){b.classList.toggle("has",has);let s=b.querySelector(".fnSt");if(s)s.textContent=has?"eklendi":"isteğe bağlı"}let rb=el.querySelector(".rule"),r=rule(f);if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+ruleAgText(f,r)}
