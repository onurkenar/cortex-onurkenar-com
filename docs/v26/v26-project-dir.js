/* Proje dosyasının klasörü (2026-11-20, kullanıcı isteği: "sarı işaretli alanda dokümanın kayıtlı olduğu dizini gösterebilir misin";
   karar: "Klasörü seçtir"). Tarayıcı (File System Access) güvenlik gereği dosyanın tam yolunu vermez, yalnız adını verir. Kullanıcı dosyanın
   bulunduğu klasörü bir kez seçer (showDirectoryPicker, salt okunur; pencere dosyanın klasöründe açılır — startIn: dosya tanıtıcısı);
   klasör tanıtıcısı IndexedDB'de ("web-project-configurator" / "handles", anahtar "projectDir") saklanır. Dashboard › Proje kartında
   Proje Adı ile Proje Dosyası kutusu arasında "Klasör: <klasör adı> › <alt klasörler> › <dosya adı>" satırı (dir.resolve(dosya)),
   dosya o klasörde değilse uyarı. Yalnız görünüm: state, kayıt, kurallar ve dışa aktarma değişmez. Kaynak docs/v26/v26-project-dir.{js,css}
   → docs/v26/proje_klasoru_ekle.py. Test kancası window.PD. */
(function(){
 if(typeof renderFileBox!=="function"||typeof pfIdb!=="function")return;
 const OK=typeof window.showDirectoryPicker==="function"&&typeof PF_OK!=="undefined"&&PF_OK;
 const PD={dir:null,rel:undefined,for:null,dirFor:null,busy:false,loaded:false};
 const esc=s=>typeof E==="function"?E(s):String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
 async function resolve(){
  let h=pf&&pf.handle,d=PD.dir;
  if(!h||!d){PD.rel=undefined;PD.for=h;PD.dirFor=d;return}
  if(PD.for===h&&PD.dirFor===d&&PD.rel!==undefined)return;
  PD.for=h;PD.dirFor=d;
  try{let r=await d.resolve(h);PD.rel=Array.isArray(r)?r:null}catch(e){PD.rel=null}
  draw();
 }
 function line(){
  let h=pf&&pf.handle;if(!OK||!h)return "";
  let d=PD.dir,btn=(t,fn,cls)=>`<button type="button" class="pdBtn${cls?" "+cls:""}" data-v26 onclick="${fn}">${esc(t)}</button>`,
   note=`<span class="pdNote">Tarayıcı güvenlik gereği bilgisayardaki tam yolu göstermez; yalnız seçtiğiniz klasörün adı görünür.</span>`;
  if(!d)return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV pdNone">Gösterilmiyor — dosyanın bulunduğu klasörü bir kez seçin.</span>${btn("Klasörü seç","PD.pick()","pdMain")}${note}</div>`;
  if(PD.rel===undefined)return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV">${esc(d.name)} › …</span>${note}</div>`;
  if(PD.rel===null)return `<div class="pdLoc pdWarn" data-v26><span class="pdK">Klasör</span><span class="pdV">“${esc(d.name)}” klasöründe “${esc(h.name)}” bulunamadı. Dosya başka bir klasörde ya da taşınmış.</span>${btn("Klasörü yeniden seç","PD.pick()","pdMain")}${btn("Kaldır","PD.clear()")}${note}</div>`;
  let parts=[d.name].concat(PD.rel);
  return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV" title="${esc(parts.join(" / "))}">${parts.map((p,i)=>i===parts.length-1?`<b>${esc(p)}</b>`:`<span class="pdDir">${esc(p)}</span>`).join('<span class="pdSep" aria-hidden="true">›</span>')}</span>${btn("Klasörü değiştir","PD.pick()")}${btn("Kaldır","PD.clear()")}${note}</div>`;
 }
 function draw(){
  let box=document.querySelector("#overviewPage .ovProject #projectFileBox");if(!box)return;
  let old=box.parentNode.querySelector(":scope > .pdLoc"),html=line();
  if(!html){if(old)old.remove();return}
  let t=document.createElement("template");t.innerHTML=html;let n=t.content.firstElementChild;
  if(old){if(old.outerHTML!==n.outerHTML)old.replaceWith(n)}else box.parentNode.insertBefore(n,box);
  if(PD.dir&&pf&&pf.handle&&(PD.for!==pf.handle||PD.dirFor!==PD.dir))resolve();
 }
 PD.pick=async function(){
  let h=pf&&pf.handle,d;
  try{d=await showDirectoryPicker({id:"wpc-proje",mode:"read",startIn:h||"documents"})}
  catch(e){if(e&&e.name==="AbortError")return;try{d=await showDirectoryPicker({id:"wpc-proje",mode:"read"})}catch(e2){if(!(e2&&e2.name==="AbortError"))alert("Klasör seçilemedi: "+(e2&&e2.message||e2));return}}
  PD.set(d);
 };
 PD.set=function(d){PD.dir=d||null;PD.rel=undefined;PD.for=null;PD.dirFor=null;
  pfIdb("readwrite",s=>d?s.put(d,"projectDir"):s.delete("projectDir")).catch(()=>{});draw();resolve()};
 PD.clear=function(){PD.set(null)};
 PD.line=line;PD.draw=draw;PD.resolve=resolve;
 window.PD=PD;
 const _r=renderFileBox;renderFileBox=function(){let x=_r.apply(this,arguments);try{draw()}catch(e){}return x};
 if(OK)pfIdb("readonly",s=>s.get("projectDir")).then(d=>{if(d&&!PD.dir){PD.dir=d;draw();resolve()}PD.loaded=true}).catch(()=>{PD.loaded=true});
 draw();
})();
