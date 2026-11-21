/* Proje dosyasının klasörü (2026-11-20, kullanıcı isteği: "sarı işaretli alanda dokümanın kayıtlı olduğu dizini gösterebilir misin";
   karar: "Klasörü seçtir"). Tarayıcı (File System Access) güvenlik gereği dosyanın tam yolunu vermez, yalnız adını verir. Kullanıcı dosyanın
   bulunduğu klasörü bir kez seçer (showDirectoryPicker, salt okunur; pencere dosyanın klasöründe açılır — startIn: dosya tanıtıcısı);
   klasör tanıtıcısı IndexedDB'de ("web-project-configurator" / "handles", anahtar "projectDir") saklanır. Dashboard › Proje kartında
   Proje Adı ile Proje Dosyası kutusu arasında "Klasör: <klasör adı> › <alt klasörler> › <dosya adı>" satırı (dir.resolve(dosya)),
   dosya o klasörde değilse uyarı.
   2026-11-21 (kullanıcı isteği: "proje dosyasını seçtiğimde dosya adını ve dosya yolunu otomatik getirmeli"; karar: "Klasörden aç"):
   - Proje Dosyası kutusunda "Proje klasörünü aç" (PD.openDir): klasör seçilir (okuma-yazma), içindeki proje dosyaları (format
     web-project-configurator, parça olmayan) bulunur; tek dosya doğrudan, birden çoksa listeden seçilerek açılır. Açma işini temel
     openProjectFile yapar (seçilen tanıtıcı showOpenFilePicker yerine verilir) — onay sorusu, proje adı, bağlama aynen. Klasör saklanır.
   - "Farklı kaydet" / "dosyasını oluştur" (createProjectFile sarmalanır): kaydetme penceresi yerine klasör seçilir, dosya Proje Adı'ndan
     oluşan adla o klasöre yazılır (aynı adlı dosya varsa onay); klasör saklanır. Klasör seçici yoksa ya da açılamazsa eski pencere.
   - Dashboard › Proje Adı kutusu ve başlık her proje dosyası kutusu çiziminde state ile eşitlenir (dosya açılınca ad state'e yazılıyor
     ama kart yeniden çizilmediği için kutu boş görünüyordu; kutuya yazılırken dokunulmaz).
   - Proje Adı boşken bağlı dosya görülünce (açma, geri yükleme) ad dosyanın projectName'inden, yoksa dosya adından doldurulur (tanıtıcı
     başına bir kez).
   State'e, kurallara ve dışa aktarmaya yalnız Proje Adı (boşken) yazılır. Kaynak docs/v26/v26-project-dir.{js,css} →
   docs/v26/proje_klasoru_ekle.py. Test kancası window.PD. */
(function(){
 if(typeof renderFileBox!=="function"||typeof pfIdb!=="function")return;
 const OK=typeof window.showDirectoryPicker==="function"&&typeof PF_OK!=="undefined"&&PF_OK;
 const PD={dir:null,rel:undefined,for:null,dirFor:null,nameFor:null,list:null,msg:"",loaded:false};
 const esc=s=>typeof E==="function"?E(s):String(s).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
 const tm=x=>{try{return x?new Date(x).toLocaleString("tr-TR",{day:"2-digit",month:"2-digit",year:"numeric",hour:"2-digit",minute:"2-digit"}):""}catch(e){return ""}};
 async function resolve(){
  let h=pf&&pf.handle,d=PD.dir;
  if(!h||!d){PD.rel=undefined;PD.for=h;PD.dirFor=d;return}
  if(PD.for===h&&PD.dirFor===d&&PD.rel!==undefined)return;
  PD.for=h;PD.dirFor=d;
  try{let r=await d.resolve(h);PD.rel=Array.isArray(r)?r:null}catch(e){PD.rel=null}
  draw();
 }
 /* Proje Adı boşken dosyadan */
 async function fillName(h){
  if(!h||PD.nameFor===h)return;PD.nameFor=h;
  if(String(state.project_name||"").trim())return;
  let n="";
  try{if(await h.queryPermission({mode:"read"})==="granted"){let d=JSON.parse(await (await h.getFile()).text());n=String(d&&(d.projectName||(d.state&&d.state.project_name))||"").trim()}}catch(e){}
  n=n||String(h.name||"").replace(/\.json$/i,"").trim();
  if(!n||String(state.project_name||"").trim())return;
  if(typeof pnSet==="function")pnSet(n);else{state.project_name=n;save();renderFileBox()}
  let i=document.getElementById("pnInput");if(i&&!i.value)i.value=n;
 }
 const btn=(t,fn,cls)=>`<button type="button" class="pdBtn${cls?" "+cls:""}" data-v26 onclick="${fn}">${esc(t)}</button>`;
 const NOTE=`<span class="pdNote">Tarayıcı güvenlik gereği bilgisayardaki tam yolu göstermez; yalnız seçtiğiniz klasörün adı görünür.</span>`;
 function line(){
  if(!OK)return "";
  if(PD.list)return `<div class="pdLoc pdPick" data-v26><span class="pdK">Klasör</span><span class="pdV">“${esc(PD.dir?PD.dir.name:"")}” klasöründe ${PD.list.length} proje dosyası var; hangisi açılsın?</span>${btn("Vazgeç","PD.cancel()")}<ul class="pdList">${PD.list.map((x,i)=>`<li><button type="button" class="pdFile" data-v26 onclick="PD.pickFile(${i})"><b>${esc(x.name)}</b><span>${esc([x.pn,x.at?"son kayıt "+tm(x.at):""].filter(Boolean).join(" · "))}</span></button></li>`).join("")}</ul></div>`;
  if(PD.msg)return `<div class="pdLoc pdWarn" data-v26><span class="pdK">Klasör</span><span class="pdV">${esc(PD.msg)}</span>${btn("Kapat","PD.cancel()")}</div>`;
  let h=pf&&pf.handle;if(!h)return "";
  let d=PD.dir;
  if(!d)return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV pdNone">Gösterilmiyor — dosyanın bulunduğu klasörü bir kez seçin ya da projeyi “Proje klasörünü aç” ile açın.</span>${btn("Klasörü seç","PD.pick()","pdMain")}${NOTE}</div>`;
  if(PD.rel===undefined)return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV">${esc(d.name)} › …</span>${NOTE}</div>`;
  if(PD.rel===null)return `<div class="pdLoc pdWarn" data-v26><span class="pdK">Klasör</span><span class="pdV">“${esc(d.name)}” klasöründe “${esc(h.name)}” bulunamadı. Dosya başka bir klasörde ya da taşınmış.</span>${btn("Klasörü yeniden seç","PD.pick()","pdMain")}${btn("Kaldır","PD.clear()")}${NOTE}</div>`;
  let parts=[d.name].concat(PD.rel);
  return `<div class="pdLoc" data-v26><span class="pdK">Klasör</span><span class="pdV" title="${esc(parts.join(" / "))}">${parts.map((p,i)=>i===parts.length-1?`<b>${esc(p)}</b>`:`<span class="pdDir">${esc(p)}</span>`).join('<span class="pdSep" aria-hidden="true">›</span>')}</span>${btn("Klasörü değiştir","PD.pick()")}${btn("Kaldır","PD.clear()")}${NOTE}</div>`;
 }
 /* "Proje klasörünü aç" düğmesi — "Mevcut proje dosyasını aç"ın önüne */
 function addOpenBtn(box){
  if(!OK||!box||box.querySelector(".pdOpenBtn"))return;
  let ref=[...box.querySelectorAll(".pfActions button")].find(b=>/openProjectFile\(\)/.test(b.getAttribute("onclick")||""));if(!ref)return;
  let b=document.createElement("button");b.type="button";b.className="btn pdOpenBtn";b.textContent="Proje klasörünü aç";b.title="Klasörü seçin; içindeki proje dosyası açılır ve klasör adı gösterilir";b.setAttribute("onclick","PD.openDir()");
  ref.parentNode.insertBefore(b,ref);
 }
 /* Dashboard › Proje Adı kutusu ve başlık: dosya açılınca state değişir ama kart yeniden çizilmez — eşitle (kutuya yazılırken dokunma) */
 function syncName(){let v=String(state.project_name||""),i=document.getElementById("pnInput");if(i&&document.activeElement!==i&&i.value!==v)i.value=v;
  let t=document.querySelector("#overviewPage .ovTxt h1");if(t&&document.activeElement!==i){let w=v.trim()||"Adsız proje";if(t.textContent!==w)t.textContent=w}}
 function draw(){
  syncName();let all=document.querySelectorAll("#projectFileBox");all.forEach(addOpenBtn);
  let box=document.querySelector("#overviewPage .ovProject #projectFileBox");if(!box)return;
  let old=box.parentNode.querySelector(":scope > .pdLoc"),html=line();
  if(!html){if(old)old.remove();return}
  let t=document.createElement("template");t.innerHTML=html;let n=t.content.firstElementChild;
  if(old){if(old.outerHTML!==n.outerHTML)old.replaceWith(n)}else box.parentNode.insertBefore(n,box);
  if(PD.dir&&pf&&pf.handle&&(PD.for!==pf.handle||PD.dirFor!==PD.dir))resolve();
 }
 async function pickDir(mode){
  let o={id:"wpc-proje",mode};
  try{return await showDirectoryPicker(Object.assign({startIn:PD.dir||(pf&&pf.handle)||"documents"},o))}
  catch(e){if(e&&e.name==="AbortError")return null;try{return await showDirectoryPicker(o)}catch(e2){if(!(e2&&e2.name==="AbortError"))alert("Klasör seçilemedi: "+(e2&&e2.message||e2));return null}}
 }
 PD.pick=async function(){let d=await pickDir("read");if(d)PD.set(d)};
 PD.set=function(d){PD.dir=d||null;PD.rel=undefined;PD.for=null;PD.dirFor=null;
  pfIdb("readwrite",s=>d?s.put(d,"projectDir"):s.delete("projectDir")).catch(()=>{});draw();resolve()};
 PD.clear=function(){PD.set(null)};
 PD.cancel=function(){PD.list=null;PD.msg="";draw()};
 /* klasördeki proje dosyaları: tam proje dosyası (parça JSON'ları değil), en son kaydedilen önce */
 PD.scan=async function(d){let L=[];for await(const [n,h] of d.entries()){if(!h||h.kind!=="file"||!/\.json$/i.test(n))continue;
   try{let f=await h.getFile();if(f.size>60e6)continue;let j=JSON.parse(await f.text());if(j&&typeof j==="object"&&j.format==="web-project-configurator"&&!j.part&&j.state&&typeof j.state==="object")L.push({h,name:n,pn:String(j.projectName||j.state.project_name||"").trim(),at:j.savedAt||"",mod:f.lastModified||0})}catch(e){}}
  return L.sort((a,b)=>String(b.at).localeCompare(String(a.at))||b.mod-a.mod||a.name.localeCompare(b.name,"tr"))};
 PD.useFile=async function(h){let o=window.showOpenFilePicker;window.showOpenFilePicker=async()=>[h];try{await openProjectFile()}finally{window.showOpenFilePicker=o}PD.list=null;PD.msg="";PD.nameFor=null;draw();resolve();if(pf&&pf.handle===h)fillName(h)};
 PD.pickFile=function(i){let x=PD.list&&PD.list[i];if(x)PD.useFile(x.h)};
 PD.openDir=async function(){if(!OK){if(typeof openProjectFile==="function")openProjectFile();return}
  let d=await pickDir("readwrite");if(!d)return;PD.list=null;PD.msg="";let L;
  try{L=await PD.scan(d)}catch(e){alert("Klasör okunamadı: "+(e&&e.message||e));return}
  PD.set(d);
  if(!L.length){PD.msg=`“${d.name}” klasöründe proje dosyası bulunamadı. Yeni proje için Proje Adı'nı yazıp dosyayı oluşturun; kaydederken bu klasörü seçebilirsiniz.`;draw();return}
  if(L.length===1){await PD.useFile(L[0].h);return}
  PD.list=L;draw()};
 /* Farklı kaydet / dosyasını oluştur → klasöre kaydet */
 if(typeof createProjectFile==="function"){const _c=createProjectFile;createProjectFile=async function(){
  let name=typeof pfFileName==="function"?pfFileName():"";if(!OK||!name)return _c.apply(this,arguments);
  let d=await pickDir("readwrite");if(!d)return;
  let h=null;try{h=await d.getFileHandle(name)}catch(e){h=null}
  if(h&&!(pf&&pf.handle&&await h.isSameEntry(pf.handle).catch(()=>false))&&!confirm(`“${d.name}” klasöründe “${name}” zaten var. Üzerine yazılsın mı?\n\nİptal: kaydetmekten vazgeç.`))return;
  try{h=h||await d.getFileHandle(name,{create:true})}catch(e){alert("Dosya oluşturulamadı: "+(e&&e.message||e));return}
  PD.set(d);pfLink(h,"linked");PD.nameFor=h;await pfWrite()}}
 PD.line=line;PD.draw=draw;PD.resolve=resolve;PD.fillName=fillName;
 window.PD=PD;
 const _r=renderFileBox;renderFileBox=function(){let x=_r.apply(this,arguments);try{draw();if(pf&&pf.handle)fillName(pf.handle)}catch(e){}return x};
 if(OK)pfIdb("readonly",s=>s.get("projectDir")).then(d=>{if(d&&!PD.dir){PD.dir=d;draw();resolve()}PD.loaded=true}).catch(()=>{PD.loaded=true});
 draw();
})();
