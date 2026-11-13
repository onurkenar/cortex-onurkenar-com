/* Para birimi biçimi (2026-11-14, kullanıcı isteği: "para birimi (örneğin bütçe) girdiğim alanlarda currency kuralı uygulansın,
   örneğin 30000 yerine 30.000,00 (TL/USD/EURO) şeklinde").
   Tutar alanları (2026-11-14'te Google Cloud › Aylık Harcama Limiti eklendi): CUR_F (metin kararları) ve CUR_ROWS (accounts satırları). Tutar kutusu + para birimi seçimi (TL / USD / EUR);
   kutudan çıkınca tutar 30.000,00 biçimine döner, kayıt "30.000,00 TL" metnidir. Eski kayıtlar ("15000") silinmez; kuralda,
   promptta ve dışa aktarımda curShow ile biçimlenir (para birimi yazılmamışsa TL). Alan etiketindeki "(TL)" ve kural şablonundaki
   "{value} TL" açılışta kaldırılır — para birimi artık değerin içindedir. mkNum USD / EUR'yu da okur; içerik planı dosyası tutarları
   TL kabul ettiği için TL dışı tutar mkIssues'ta uyarı verir. Kaynak docs/v26/v26-currency.js → docs/v26/para_birimi_ekle.py */
const CUR_F=["mk_gads_budget","mk_meta_budget","mk_li_budget","mk_tt_budget","mk_labor_rate","gg_gc_budget"],CUR_ROWS=[["oc_tax_ids","sermaye","250000"]],
 CUR_LIST=[["TL","TL (₺)"],["USD","USD ($)"],["EUR","EUR (€)"]],CUR_PLAN=["mk_gads_budget","mk_meta_budget","mk_labor_rate"];
function curParse(s){let t=String(s??"").trim();if(!t)return null;let cur="";
 t=t.replace(/₺|TRY|TL|\$|USD|€|EURO|EUR/gi,m=>{m=m.toUpperCase();cur=m==="₺"||m==="TRY"||m==="TL"?"TL":m==="$"||m==="USD"?"USD":"EUR";return""}).replace(/\s/g,"");
 if(!/^\d[\d.,]*$/.test(t))return {n:NaN,cur};let d=t.lastIndexOf(","),p=t.lastIndexOf("."),x;
 if(d>=0&&p>=0)x=d>p?t.replace(/\./g,"").replace(",","."):t.replace(/,/g,"");
 else if(d>=0)x=/^\d{1,3}(,\d{3})+$/.test(t)?t.replace(/,/g,""):t.replace(",",".");
 else if(p>=0)x=/^\d{1,3}(\.\d{3})+$/.test(t)?t.replace(/\./g,""):t;
 else x=t;
 if(!/^\d+(\.\d+)?$/.test(x))return {n:NaN,cur};return {n:Math.round(Number(x)*100)/100,cur}}
function curFmt(n){let [i,f]=Number(n).toFixed(2).split(".");return i.replace(/\B(?=(\d{3})+(?!\d))/g,".")+","+f}
function curOk(s){let r=curParse(s);return !!r&&isFinite(r.n)}
function curShow(s){let t=String(s??"").trim(),r=curParse(t);return r&&isFinite(r.n)?curFmt(r.n)+" "+(r.cur||"TL"):t}
CUR_F.forEach(id=>{let f=FI[id];if(!f)return;f.money=1;f.label=String(f.label||"").replace(/\s*\(TL\)\s*$/,"");if(f.en)f.en=f.en.replace(/\s*\(TRY\)\s*$/,"");
 f.rule=String(f.rule||"").replace("{value} TL","{value}");
 if(f.explanation)f.explanation=f.explanation.replace(" (TL).",".").replace("; yalnız rakam girin.",".")+" Tutar 30.000,00 biçiminde kaydedilir; para birimi (TL, USD, EUR) yanındaki listeden seçilir.";
 if(f.example)f.example=f.example.replace(/^(\d+) yazılırsa/,(m,n)=>curFmt(n)+" TL girilirse");let r=curParse(String(f.placeholder||"").replace(/^Örn\.\s*/,""));if(r&&r.n>0)f.placeholder="Örn. "+curFmt(r.n)});
CUR_ROWS.forEach(([id,k,ex])=>{let a=((FI[id]||{}).accounts||[]).find(x=>x.k===k);if(a){a.money=1;a.ph="Örn. "+curFmt(ex)}});
function curHint(v){let t=String(v??"").trim();if(!t)return "Tutarı yazın (ör. 30000); kutudan çıkınca 30.000,00 biçimine döner.";
 return curOk(t)?"Kayda geçen: <b>"+E(curShow(t))+"</b>":'<span class="fiWarn">Tutar sayı olarak okunamadı.</span> Örnek: 30.000,00 — binlik ayıracı nokta, kuruş ayıracı virgül.'}
function curBoxHtml(id,v,lab,arg){let r=curParse(v),ok=r&&isFinite(r.n),amt=ok?curFmt(r.n):String(v??"").trim(),cur=(r&&r.cur)||"TL",q=E(arg);
 return `<span class="curBox"><input class="control curAmt" id="${id}" type="text" inputmode="decimal" autocomplete="off" spellcheck="false" value="${E(amt)}" placeholder="${E(lab)}" aria-describedby="${id}-h" aria-invalid="${!!amt&&!ok}" oninput="curSet(${q},this)" onblur="curBlur(${q},this)"><select class="control curSel" data-native aria-label="Para birimi" onchange="curSet(${q},this.parentNode.querySelector('.curAmt'))">${CUR_LIST.map(([c,l])=>`<option value="${c}"${c===cur?" selected":""}>${l}</option>`).join("")}</select></span><small class="fontInfo curHint" id="${id}-h" aria-live="polite">${curHint(v)}</small>`}
function curInput(f){return `<div class="curField">${curBoxHtml("cur-"+f.id,state[f.id],f.placeholder||"Örn. 15.000,00",JSON.stringify([f.id]))}</div>`}
function curAccCell(f,a){let id="acc-"+f.id+"-"+a.k;return `<label class="accRow curRow" for="${id}"><span>${E(a.label)}</span>${curBoxHtml(id,accVal(f)[a.k],a.ph,JSON.stringify([f.id,a.k]))}</label>`}
function curVal(el){let t=String(el.value||"").trim();if(!t)return "";let s=el.parentNode.querySelector(".curSel"),c=s?s.value:"TL",r=curParse(t);return r&&isFinite(r.n)?curFmt(r.n)+" "+(r.cur||c):t}
function curSet(arg,el){if(!requireProject())return;let [id,k]=arg,f=FI[id],v=curVal(el);
 if(k){let o=Object.assign({},accVal(f));if(v)o[k]=v;else delete o[k];if(Object.keys(o).length)state[id]=o;else delete state[id]}
 else{if(v)state[id]=v;else delete state[id];faAuto(id)}
 let r=curParse(el.value),s=el.parentNode.querySelector(".curSel");if(r&&r.cur&&s&&s.value!==r.cur)s.value=r.cur;
 el.setAttribute("aria-invalid",String(!!v&&!curOk(v)));let h=document.getElementById(el.id+"-h");if(h)h.innerHTML=curHint(v);
 save();renderRules();renderProgress();curRule(f)}
function curBlur(arg,el){let r=curParse(el.value);if(r&&isFinite(r.n))el.value=curFmt(r.n)}
function curRule(f){let el=document.querySelector('.field[data-field-id="'+f.id+'"]');if(!el)return;let rb=el.querySelector(".rule"),r=rule(f);
 if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(f,r):E(r));else if(typeof refreshRule==="function")refreshRule(f)}
function curIssues(L,c){CUR_PLAN.forEach(k=>{let t=mkT(k),r=curParse(t);if(t&&r&&isFinite(r.n)&&r.cur&&r.cur!=="TL")L.push(`${c(k)} ${E(r.cur)} olarak girildi; içerik planı dosyası tutarları TL kabul eder — planda TL karşılığını kullanın ya da tutarı TL girin.`)})}
