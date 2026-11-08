/* Hazır Prompt Kütüphanesi (2026-11-08, kullanıcı isteği: "Web OnKe projesine Hazır Prompt Kütüphanesi menüsü ekle …").
   Modül şeridinde "Promptlar" (Kurallar ile Doküman arasında), çekmecede "Hazır Prompt Kütüphanesi" → showPage("library").
   Kütüphane (özel modüller, hazır modül düzenlemeleri, gizlenen hazır modüller, özel kategoriler) projeden bağımsızdır:
   IndexedDB "web-project-configurator-prompts" / "kv" / "library" (yoksa localStorage "web-project-configurator-promptlib", o da yoksa bellek).
   Projedeki seçim state.promptLib = {sel:[id], names:{id:"Başlık vX"}} (proje hazır değilken oturumluk bellek).
   Kurallar, Claude promptu, CLAUDE-TALIMATLARI.md ve proje dosyası biçimi değişmez; birleştirilmiş talimat ayrı kopyalanır / indirilir. */
(()=>{
/*PL_DATA*/
PL_CATS0.push({id:"diger",name:"Diğer",desc:"Henüz bir kategoriye bağlanmamış modüller."});
const PL_DBN="web-project-configurator-prompts",PL_ST="kv",PL_K="library",PL_LS="web-project-configurator-promptlib",PL_FMT="wpc-prompt-library",
 PL_MAXIMG=1600,PL_HIST=10,PL_VER_RE=/^\d+\.\d+\.\d+$/,PL_SRC_RE=/^(data:image\/(png|jpe?g|webp|gif|svg\+xml)[;,]|https:\/\/)/i,
 PL_TEXT=["title","desc","cat","tags","prompt","doc","criteria","deps","refs"],
 PL_EXT={"image/webp":"webp","image/png":"png","image/jpeg":"jpg","image/gif":"gif","image/svg+xml":"svg"};
let LIB={v:1,cats:[],mods:{},over:{},hidden:[]},LIB_MODE="load",MEM_SEL=[];
const PL={view:"list",id:null,q:"",cat:"",tag:"",sort:"cat",only:false,tagsAll:false,draft:null,dirty:false,errs:[],mdPrev:false,raw:false,combo:{deps:true,docs:"full"}};
const BI={};PL_BUILTIN.forEach(m=>BI[m.id]=m);
/* 2026-11-08 (kullanıcı kararı): 8 hazır alt modül iki tek modülde birleşti — eski kimlikler seçimde ve bağımlılıklarda yeni kimliğe çözülür. */
const PL_LEGACY={"kvkk-cerez-onayi":"kvkk-gdpr-cerez","kvkk-aydinlatma-riza":"kvkk-gdpr-cerez","kvkk-ilgili-kisi-basvuru":"kvkk-gdpr-cerez","kvkk-saklama-imha":"kvkk-gdpr-cerez","a11y-wcag22-temel":"erisilebilirlik","a11y-klavye-odak":"erisilebilirlik","a11y-formlar":"erisilebilirlik","a11y-etkilesimli-bilesenler":"erisilebilirlik"};
const plLg=id=>!LIB.mods[id]&&PL_LEGACY[id]||id;
const plLgL=(L,self)=>[...new Set((L||[]).map(plLg))].filter(x=>x!==self);
const today=()=>new Date().toLocaleDateString("sv-SE");
const clone=o=>JSON.parse(JSON.stringify(o));
const plSlug=t=>norm(String(t||"")).replace(/ /g,"-").slice(0,60).replace(/-+$/,"");
const nf=n=>Number(n).toLocaleString("tr-TR");

/* ---------- Kalıcı depo ---------- */
function plNorm(v){let L=v&&typeof v==="object"?v:{};return{v:1,cats:Array.isArray(L.cats)?L.cats.filter(c=>c&&c.id&&c.name):[],mods:L.mods&&typeof L.mods==="object"&&!Array.isArray(L.mods)?L.mods:{},over:L.over&&typeof L.over==="object"&&!Array.isArray(L.over)?L.over:{},hidden:Array.isArray(L.hidden)?L.hidden.filter(x=>typeof x==="string"):[]}}
function plDb(){return new Promise((ok,no)=>{try{let r=indexedDB.open(PL_DBN,1);r.onupgradeneeded=()=>r.result.createObjectStore(PL_ST);r.onsuccess=()=>ok(r.result);r.onerror=()=>no(r.error);r.onblocked=()=>no(new Error("blocked"))}catch(e){no(e)}})}
function plTx(mode,fn){return plDb().then(db=>new Promise((ok,no)=>{let t=db.transaction(PL_ST,mode),q=fn(t.objectStore(PL_ST));t.oncomplete=()=>{db.close();ok(q&&q.result)};t.onerror=t.onabort=()=>{db.close();no(t.error)}}))}
async function plLoad(){try{LIB=plNorm(await plTx("readonly",s=>s.get(PL_K)));LIB_MODE="idb"}catch(e){try{LIB=plNorm(JSON.parse(localStorage.getItem(PL_LS)||"null"));LIB_MODE="ls"}catch(e2){LIB=plNorm(null);LIB_MODE="mem"}}if(plActive())plRender()}
let PL_Q=Promise.resolve();
function plSave(){let snap=clone(LIB);PL_Q=PL_Q.then(async()=>{if(LIB_MODE==="idb"){try{await plTx("readwrite",s=>s.put(snap,PL_K));return}catch(e){LIB_MODE="ls"}}if(LIB_MODE==="ls"){try{localStorage.setItem(PL_LS,JSON.stringify(snap));return}catch(e){LIB_MODE="mem";plToast("Kütüphane bu tarayıcıda kalıcı olarak kaydedilemedi. Değişikliklerinizi kaybetmemek için kütüphaneyi dışa aktarın.",1);plRender()}}});return PL_Q}

/* ---------- Modeller ---------- */
function plMods(){let o=[];PL_BUILTIN.forEach(b=>{if(LIB.hidden.includes(b.id))return;let x=LIB.over[b.id];o.push(Object.assign({history:[]},x||b,{id:b.id,builtin:true,edited:!!x}))});Object.keys(LIB.mods).forEach(k=>{if(!BI[k])o.push(Object.assign({history:[]},LIB.mods[k],{id:k,builtin:false,edited:false}))});o.forEach(m=>m.deps=plLgL(m.deps,m.id));return o}
function plMod(id){return plMods().find(m=>m.id===id)||null}
function plCats(){let o=PL_CATS0.map(c=>Object.assign({builtin:true},c));LIB.cats.forEach(c=>{if(!o.some(x=>x.id===c.id))o.push({id:c.id,name:c.name,desc:c.desc||"",builtin:false})});return o}
function plCatName(id){let c=plCats().find(x=>x.id===id);return c?c.name:"Diğer"}
function plCatOf(m){return plCats().some(c=>c.id===m.cat)?m.cat:"diger"}
function plTextOnly(m){let o={};PL_TEXT.forEach(k=>{if(m[k]!==undefined)o[k]=clone(m[k])});return o}
function plBump(v,k){let p=(PL_VER_RE.test(v)?v:"1.0.0").split(".").map(Number);if(k==="major")return `${p[0]+1}.0.0`;if(k==="minor")return `${p[0]}.${p[1]+1}.0`;return `${p[0]}.${p[1]}.${p[2]+1}`}
function plStore(m){let x=clone(m);delete x.builtin;delete x.edited;if(BI[m.id]){LIB.over[m.id]=x;LIB.hidden=LIB.hidden.filter(i=>i!==m.id)}else LIB.mods[m.id]=x}
function plUniqId(base){let b=plSlug(base)||"modul",id=b,n=2,taken=new Set(plMods().map(m=>m.id).concat(Object.keys(BI)));while(taken.has(id))id=b+"-"+n++;return id}

/* ---------- Seçim (proje) ---------- */
function plSel(){if(typeof projectReady==="function"&&projectReady()){let s=state.promptLib&&Array.isArray(state.promptLib.sel)?state.promptLib.sel:[];return plLgL(s.length?s:MEM_SEL)}return plLgL(MEM_SEL)}
function plSetSel(a){a=[...new Set(a)];if(typeof projectReady==="function"&&projectReady()){if(a.length){let old=state.promptLib&&state.promptLib.names||{},names={};a.forEach(id=>{let m=plMod(id);names[id]=m?`${m.title} v${m.version}`:(old[id]||id)});state.promptLib={sel:a,names}}else delete state.promptLib;save();MEM_SEL=[]}else MEM_SEL=a}
window.plToggle=id=>{id=plLg(id);let s=plSel(),i=s.indexOf(id);if(i<0)s.push(id);else s.splice(i,1);plSetSel(s);plRefresh()};
window.plSelMany=(ids,on)=>{ids=ids.map(plLg);let s=plSel();ids.forEach(id=>{let i=s.indexOf(id);if(on&&i<0)s.push(id);if(!on&&i>=0)s.splice(i,1)});plSetSel(s);plRefresh()};
window.plSelVisible=on=>plSelMany(plFilter().map(m=>m.id),on);
window.plSelClear=()=>{plSetSel([]);plRefresh()};

/* ---------- Bağımlılıklar ---------- */
function plResolve(ids,withDeps){let M={};plMods().forEach(m=>M[m.id]=m);let order=[],st={},missing=[],cycles=[],why={},loose=[];
 const visit=(id,from,stack)=>{if(!M[id]){if(!missing.some(x=>x.id===id&&x.from===from))missing.push({id,from});return}if(st[id]===2)return;if(st[id]===1){cycles.push(stack.slice(stack.indexOf(id)).concat(id));return}st[id]=1;
  (M[id].deps||[]).forEach(d=>{if(withDeps){if(!ids.includes(d)&&!why[d])why[d]=id;visit(d,id,stack.concat(id))}else if(!ids.includes(d))loose.push({id:d,from:id,known:!!M[d]})});st[id]=2;order.push(M[id])};
 ids.forEach(id=>visit(id,null,[]));
 return{order,missing,cycles,why,loose,added:order.filter(m=>!ids.includes(m.id))}}
function plDependents(id){return plMods().filter(m=>(m.deps||[]).includes(id))}
function plCycleWith(id,deps){let M={};plMods().forEach(m=>M[m.id]=m);let seen=new Set(),st=[...deps];while(st.length){let d=st.pop();if(d===id)return true;if(seen.has(d)||!M[d])continue;seen.add(d);st.push(...(M[d].deps||[]))}return false}

/* ---------- Görseller ---------- */
const IMG=new Map();
function plBytes(src){let m=/^data:([^;,]+)((?:;[^;,]*)*),([\s\S]*)$/.exec(src);if(!m)return null;let mime=m[1].toLowerCase(),body=m[3];if(/;base64/i.test(m[2])){let b=atob(body),u=new Uint8Array(b.length);for(let i=0;i<b.length;i++)u[i]=b.charCodeAt(i);return{mime,u}}return{mime,u:new TextEncoder().encode(decodeURIComponent(body))}}
function plUrl(src){if(!/^data:/i.test(src))return src;let u=IMG.get(src);if(!u){try{let b=plBytes(src);u=URL.createObjectURL(new Blob([b.u],{type:b.mime}))}catch(e){u=""}IMG.set(src,u)}return u}
async function plFileImg(f){if(!/^image\/(png|jpeg|webp|gif|svg\+xml)$/.test(f.type))throw new Error(`${f.name}: desteklenmeyen biçim (PNG, JPEG, WebP, GIF, SVG)`);if(f.size>15e6)throw new Error(`${f.name}: 15 MB'tan büyük`);
 if(f.type==="image/svg+xml"){if(f.size>5e5)throw new Error(`${f.name}: SVG 500 KB'tan büyük`);return "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(await f.text())}
 if(f.type==="image/gif"&&f.size<15e5)return await new Promise((ok,no)=>{let r=new FileReader();r.onload=()=>ok(r.result);r.onerror=()=>no(r.error);r.readAsDataURL(f)});
 let bmp=await createImageBitmap(f),s=Math.min(1,PL_MAXIMG/Math.max(bmp.width,bmp.height)),c=document.createElement("canvas");c.width=Math.max(1,Math.round(bmp.width*s));c.height=Math.max(1,Math.round(bmp.height*s));c.getContext("2d").drawImage(bmp,0,0,c.width,c.height);let d=c.toDataURL("image/webp",.82);if(!/^data:image\/webp/.test(d))d=c.toDataURL("image/jpeg",.85);return d}

/* ---------- Markdown (güvenli, küçük) ---------- */
/* Markdown içindeki görsel: ![alt](yol) — yolun dosya adı modülün bir görselinin adıyla eşleşirse o görsel (tıklayınca büyür), yoksa not. Çapalar (#…) sayfa içi başlığa, göreli bağlantılar yalnız metin. */
let PL_MD_MOD=null;
const plImgBase=u=>String(u).replace(/&amp;/g,"&").split(/[?#]/)[0].split("/").pop().replace(/\.[a-z0-9]+$/i,"");
const plAnchor=t=>String(t).replace(/`|\*\*/g,"").toLowerCase().replace(/[^\p{L}\p{N}\s_-]/gu,"").trim().replace(/\s/g,"-");
function plImgTok(alt,u){let m=PL_MD_MOD,L=m&&m.images||[],b=plImgBase(u),i=L.findIndex(x=>x.name&&x.name===b),a=E(alt);
 return i>=0?`<button type="button" class="plMdImgBtn" onclick="plZoom('${m.id}',${i})" aria-label="Büyüt: ${a}"><img src="${E(plUrl(L[i].src))}" alt="${a}" loading="lazy" decoding="async"></button>`:`<span class="plMdNoImg">[Görsel bu kütüphanede yok: ${a}]</span>`}
function plLinkTok(tx,u){let h=plInline(tx);if(/^#/.test(u))return `<a href="#plmd-${E(plAnchor(decodeURIComponent(u.slice(1))))}">${h}</a>`;return /^(https?:|mailto:)/i.test(u)?`<a href="${E(u)}" target="_blank" rel="noopener noreferrer">${h}</a>`:h}
/* Bağlantı ve görseller önce yer tutucuya alınır (bağlantı metni kod içerebilir), sonra kod / kalın / italik işlenir. */
function plInline(t){let P=[];t=String(t).replace(/\u0000/g,"").replace(/(!?)\[([^\]]*)\]\(([^)\s]+)\)/g,(a,bang,tx,u)=>{P.push(bang?plImgTok(tx,u):plLinkTok(tx,u));return "\u0000"+(P.length-1)+"\u0000"});
 return t.split(/(`[^`]+`)/).map(seg=>{if(/^`[^`]+`$/.test(seg))return "<code>"+E(seg.slice(1,-1))+"</code>";
 return E(seg).replace(/\*\*([^*]+)\*\*/g,"<strong>$1</strong>").replace(/(^|[^*\w])\*([^*\s][^*]*?)\*(?!\*)/g,"$1<em>$2</em>")}).join("").replace(/\u0000(\d+)\u0000/g,(a,i)=>P[+i])}
function plMd(src,mod){PL_MD_MOD=mod||null;let L=String(src||"").replace(/\r/g,"").split("\n"),h=[],P=[],i=0;const LI=/^\s*([-*]|\d+\.)\s+/;
 const flush=()=>{if(P.length){h.push("<p>"+plInline(P.join(" "))+"</p>");P=[]}};
 while(i<L.length){let l=L[i],m;
  if(/^\s*```/.test(l)){flush();let b=[];i++;while(i<L.length&&!/^\s*```/.test(L[i]))b.push(L[i++]);i++;h.push(`<pre class="plCode"><code>${E(b.join("\n"))}</code></pre>`);continue}
  if(m=/^(#{1,6})\s+(.*)$/.exec(l)){flush();let n=Math.min(6,m[1].length+2);h.push(`<h${n} id="plmd-${E(plAnchor(m[2]))}">${plInline(m[2])}</h${n}>`);i++;continue}
  if(/^\s*(---|\*\*\*)\s*$/.test(l)){flush();h.push("<hr>");i++;continue}
  if(/^\s*\|/.test(l)&&i+1<L.length&&/^\s*\|?\s*:?-{2,}/.test(L[i+1])){flush();const row=r=>r.trim().replace(/^\||\|$/g,"").split("|").map(c=>c.trim());let hd=row(l),R=[];i+=2;while(i<L.length&&/^\s*\|/.test(L[i]))R.push(row(L[i++]));
   h.push(`<div class="plTblWrap"><table class="plTbl"><thead><tr>${hd.map(c=>`<th scope="col">${plInline(c)}</th>`).join("")}</tr></thead><tbody>${R.map(r=>`<tr>${r.map(c=>`<td>${plInline(c)}</td>`).join("")}</tr>`).join("")}</tbody></table></div>`);continue}
  if(/^>\s?/.test(l)){flush();let b=[];while(i<L.length&&/^>\s?/.test(L[i]))b.push(L[i++].replace(/^>\s?/,""));h.push("<blockquote>"+plInline(b.join(" "))+"</blockquote>");continue}
  if(LI.test(l)){flush();let ol=/^\s*\d+\./.test(l),start=ol?parseInt(l,10)||1:1,it=[];while(i<L.length&&LI.test(L[i])){let t=L[i].replace(LI,""),cb=/^\[( |x|X)\]\s+(.*)$/.exec(t);it.push(cb?`<li class="plCb"><span aria-hidden="true">${cb[1]===" "?"☐":"☑"}</span> ${plInline(cb[2])}`:`<li>${plInline(t)}`);i++;while(i<L.length&&/^\s{2,}\S/.test(L[i])&&!LI.test(L[i])){it[it.length-1]+=" "+plInline(L[i].trim());i++}}
   h.push(ol?`<ol${start>1?` start="${start}"`:""}>${it.map(x=>x+"</li>").join("")}</ol>`:`<ul>${it.map(x=>x+"</li>").join("")}</ul>`);continue}
  if(!l.trim()){flush();i++;continue}
  P.push(l.trim());i++}
 flush();return h.join("")}

/* ---------- Yardımcılar ---------- */
function plToast(t,err){let x=document.getElementById("plToast");if(!x)return;x.textContent=t;x.className="plToast show"+(err?" err":"");clearTimeout(plToast.t);plToast.t=setTimeout(()=>x.className="plToast",err?6000:2600)}
window.plCopy=async(t,btn)=>{let ok=true;try{await navigator.clipboard.writeText(t)}catch(e){try{let ta=document.createElement("textarea");ta.value=t;ta.setAttribute("readonly","");ta.style.cssText="position:fixed;opacity:0;left:0;top:0";document.body.appendChild(ta);ta.select();ok=document.execCommand("copy");ta.remove()}catch(e2){ok=false}}
 plToast(ok?"Panoya kopyalandı.":"Kopyalanamadı — metni elle seçip kopyalayın.",!ok);if(btn){let o=btn.dataset.l||btn.textContent;btn.dataset.l=o;btn.textContent=ok?"Kopyalandı ✓":"Kopyalanamadı";setTimeout(()=>btn.textContent=o,1500)}return ok};
function plBlob(blob,name){let a=document.createElement("a"),u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500)}
function plZip(files){let te=new TextEncoder(),parts=[],cd=[],off=0;files.forEach(f=>{let n=te.encode(f.name),dt=f.data instanceof Uint8Array?f.data:te.encode(f.data),c=crc32(dt),h=new DataView(new ArrayBuffer(30)),e=new DataView(new ArrayBuffer(46));h.setUint32(0,0x04034b50,true);h.setUint16(4,20,true);h.setUint16(6,0x0800,true);h.setUint16(12,0x21,true);h.setUint32(14,c,true);h.setUint32(18,dt.length,true);h.setUint32(22,dt.length,true);h.setUint16(26,n.length,true);e.setUint32(0,0x02014b50,true);e.setUint16(4,20,true);e.setUint16(6,20,true);e.setUint16(8,0x0800,true);e.setUint16(14,0x21,true);e.setUint32(16,c,true);e.setUint32(20,dt.length,true);e.setUint32(24,dt.length,true);e.setUint16(28,n.length,true);e.setUint32(42,off,true);parts.push(h,n,dt);cd.push(e,n);off+=30+n.length+dt.length});let size=cd.reduce((a,x)=>a+x.byteLength,0),z=new DataView(new ArrayBuffer(22));z.setUint32(0,0x06054b50,true);z.setUint16(8,files.length,true);z.setUint16(10,files.length,true);z.setUint32(12,size,true);z.setUint32(16,off,true);return new Blob(parts.concat(cd,[z]),{type:"application/zip"})}
const pname=()=>String(state.project_name||"").trim();
const fslug=()=>(typeof exSlug==="function"?exSlug(pname()):plSlug(pname()))||"proje";
function plImgName(m,i,im){if(!/^data:/i.test(im.src))return null;let b=plBytes(im.src);return `gorseller/${m.id}-${im.name||i+1}.${PL_EXT[b&&b.mime]||"img"}`}
/* Dışa aktarılan Markdown'da doküman görselleri zip'teki dosyaya bağlanır (rel: dosyanın zip köküne göre yolu); eşleşmeyen görsel not olur. */
function plDocOut(m,rel){let L=m.images||[];return String(m.doc||"").replace(/!\[([^\]]*)\]\(([^)\s]+)\)/g,(a,alt,u)=>{let b=plImgBase(u),i=L.findIndex(x=>x.name&&x.name===b),f=i>=0?plImgName(m,i,L[i]):null;return f?`![${alt}](${rel}${f})`:(i>=0?`![${alt}](${L[i].src.slice(0,8)==="https://"?L[i].src:""})`:`*[Görsel bu kütüphanede yok: ${alt}]*`)})}

/* ---------- Sayfa ---------- */
const PG=document.createElement("section");PG.id="libraryPage";PG.setAttribute("aria-label","Hazır Prompt Kütüphanesi");
configPage.parentNode.insertBefore(PG,configPage);
const TO=document.createElement("div");TO.id="plToast";TO.className="plToast";TO.setAttribute("role","status");TO.setAttribute("aria-live","polite");document.body.appendChild(TO);
const ZD=document.createElement("dialog");ZD.id="plZoom";ZD.setAttribute("aria-labelledby","plZoomT");document.body.appendChild(ZD);
ZD.addEventListener("click",e=>{if(e.target===ZD)ZD.close()});
const plActive=()=>PG.classList.contains("active");
const ICON="M4 5a1 1 0 0 1 1-1h6v16H5a1 1 0 0 1-1-1V5ZM13 4h6a1 1 0 0 1 1 1v6h-7V4ZM13 13h7v6a1 1 0 0 1-1 1h-6v-7ZM7 8h2M7 11h2M7 14h2";
function plNav(){let rail=document.getElementById("modRail");if(rail&&!rail.querySelector('[data-mod="library"]')){let b=document.createElement("button");b.type="button";b.className="mrBtn";b.dataset.mod="library";b.title="Hazır Prompt Kütüphanesi";b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="${ICON}"/></svg><span>Promptlar</span>`;b.setAttribute("aria-label","Hazır Prompt Kütüphanesi");b.onclick=()=>plGo();rail.insertBefore(b,rail.querySelector('[data-mod="docs"]'))}
 let docs=document.getElementById("sideDocsBtn");if(docs&&!document.getElementById("sideLibBtn")){let s=document.createElement("button");s.type="button";s.id="sideLibBtn";s.innerHTML="▤ &nbsp; Hazır Prompt Kütüphanesi";s.onclick=()=>plGo();docs.parentNode.insertBefore(s,docs)}}
function plSync(){let on=plActive(),rail=document.getElementById("modRail");if(rail)rail.querySelectorAll(".mrBtn").forEach(b=>{if(on){let a=b.dataset.mod==="library";b.classList.toggle("active",a);b.toggleAttribute("aria-current",a)}else if(b.dataset.mod==="library"){b.classList.remove("active");b.removeAttribute("aria-current")}});
 if(on)document.documentElement.classList.add("v26NoSide");let s=document.getElementById("sideLibBtn");if(s){s.classList.toggle("active",on);s.toggleAttribute("aria-current",on)}}
const _sp=showPage;
showPage=function(p){if(p==="library"){_sp("config");configPage.classList.add("hidden");PG.classList.add("active");plRender();window.scrollTo(0,0);plSync();return}if(plActive()&&PL.view==="edit"&&PL.dirty&&!confirm("Kaydedilmemiş değişiklikler var. Sayfadan çıkılsın mı?"))return;PG.classList.remove("active");if(PL.view==="edit"){PL.view=PL.id?"detail":"list";PL.draft=null;PL.dirty=false}_sp(p);plSync()};
const _ab=areaBtn;areaBtn=function(){_ab();if(plActive())plSync()};
window.plGo=()=>{if(typeof closeNav==="function")closeNav();showPage("library")};
plNav();

function plRender(){if(!plActive())return;let v=PL.view,h;
 if(LIB_MODE==="load")h=`<p class="plMuted">Kütüphane yükleniyor…</p>`;
 else if(v==="detail"&&plMod(PL.id))h=plDetail(plMod(PL.id));
 else if(v==="edit"&&PL.draft)h=plEdit();
 else if(v==="combine")h=plCombine();
 else{PL.view="list";h=plList()}
 PG.innerHTML=h;if(PL.view==="list")plResDraw()}
function plRefresh(){if(!plActive())return;if(PL.view==="list"){plResDraw();plSelBarDraw();let o=document.getElementById("plOnlyN");if(o)o.textContent=plSel().length}else plRender()}
function plIntro(){return `<div class="intro"><div class="eyebrow">HAZIR PROMPT KÜTÜPHANESİ</div><h1>Hazır Prompt Kütüphanesi</h1><p class="plLead">Sık tekrarlanan geliştirme işlerini hazır modüller olarak saklayın: her modülde kısa prompt, Markdown teknik doküman, referans görseller, kabul kriterleri, bağımlılıklar ve sürüm bulunur. Projeniz için modülleri seçin; araç seçtiklerinizi bağımlılıklarıyla birlikte doğru sırada <b>tek bir geliştirme talimatında</b> birleştirir. Kütüphane bu tarayıcıda saklanır ve bütün projelerde ortaktır; projedeki seçim proje dosyasına yazılır.</p>${LIB_MODE==="mem"?`<p class="plWarn" role="alert">Bu tarayıcı kütüphaneyi kalıcı olarak saklayamıyor (özel pencere ya da engellenmiş depolama). Yaptığınız değişiklikler sayfa kapanınca kaybolur; <button type="button" class="plLink" onclick="plExport('all')">kütüphaneyi dışa aktararak</button> yedekleyin.</p>`:""}</div>`}

/* ---------- Liste ---------- */
function plHay(m){return norm([m.title,m.desc,plCatName(plCatOf(m)),(m.tags||[]).join(" "),m.prompt,(m.criteria||[]).join(" "),m.doc,m.id].join(" "))}
function plFilter(){let q=norm(PL.q||""),sel=new Set(plSel());return plMods().filter(m=>(!PL.cat||plCatOf(m)===PL.cat)&&(!PL.tag||(m.tags||[]).includes(PL.tag))&&(!PL.only||sel.has(m.id))&&(!q||hit(plHay(m),q)))}
function plSorted(L){let C=plCats().map(c=>c.id);if(PL.sort==="title")return L.sort((a,b)=>a.title.localeCompare(b.title,"tr"));if(PL.sort==="updated")return L.sort((a,b)=>String(b.updated||"").localeCompare(String(a.updated||""))||a.title.localeCompare(b.title,"tr"));return L.sort((a,b)=>C.indexOf(plCatOf(a))-C.indexOf(plCatOf(b)))}
function plList(){let all=plMods(),sel=plSel(),cnt={};all.forEach(m=>{let c=plCatOf(m);cnt[c]=(cnt[c]||0)+1});
 let cats=plCats().filter(c=>cnt[c.id]),tags={};all.forEach(m=>(m.tags||[]).forEach(t=>tags[t]=(tags[t]||0)+1));
 let T=Object.keys(tags).sort((a,b)=>tags[b]-tags[a]||a.localeCompare(b,"tr")),TS=PL.tagsAll?T:T.slice(0,14);if(PL.tag&&!TS.includes(PL.tag))TS.push(PL.tag);
 let chip=(on,lab,n,fn,extra="")=>`<button type="button" class="plChip${on?" on":""}" aria-pressed="${on}" onclick="${fn}"${extra}>${lab}${n!==undefined?` <span>${n}</span>`:""}</button>`;
 return plIntro()+`<div class="plBar"><div class="plSearch"><svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14ZM20 20l-4-4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg><input id="plQ" type="search" autocomplete="off" placeholder="Modül, etiket ya da içerik ara…" aria-label="Kütüphanede ara" aria-describedby="plN" value="${E(PL.q)}" oninput="plQuery(this.value)" onkeydown="if(event.key==='Escape'){this.value='';plQuery('')}"><span id="plN" class="plN" aria-live="polite"></span></div>
 <label class="plSort"><span>Sırala</span><select onchange="plSortBy(this.value)">${[["cat","Kategoriye göre"],["title","Ada göre"],["updated","Son güncellenen"]].map(o=>`<option value="${o[0]}"${PL.sort===o[0]?" selected":""}>${o[1]}</option>`).join("")}</select></label>
 <div class="plActs"><button type="button" class="btn dark" onclick="plNew()">+ Yeni modül</button><button type="button" class="btn" onclick="plImportPick()">İçe aktar</button><button type="button" class="btn" onclick="plExport('all')">Tümünü dışa aktar</button></div></div>
 <div class="plChips" role="group" aria-label="Kategori filtresi">${chip(!PL.cat&&!PL.only,"Tümü",all.length,"plCat('')")}${cats.map(c=>chip(PL.cat===c.id,E(c.name),cnt[c.id],`plCat('${c.id}')`,` title="${E(c.desc||"")}"`)).join("")}${chip(PL.only,"Yalnız seçililer",undefined,"plOnly()").replace("</button>",` <span id="plOnlyN">${sel.length}</span></button>`)}</div>
 ${T.length?`<div class="plTags" role="group" aria-label="Etiket filtresi"><span class="plTagsL">Etiket</span>${TS.map(t=>`<button type="button" class="plTag${PL.tag===t?" on":""}" aria-pressed="${PL.tag===t}" onclick="plTagF(${E(JSON.stringify(t))})">#${E(t)}</button>`).join("")}${T.length>14?`<button type="button" class="plLink" onclick="plTagsAll()">${PL.tagsAll?"Daha az göster":`Tüm etiketler (${T.length})`}</button>`:""}</div>`:""}
 <div id="plRes"></div><div id="plSelBar"></div>
 <details class="plCats"><summary>Kategorileri yönet</summary>${plCatAdmin()}</details>`}
window.plQuery=v=>{PL.q=v;plResDraw()};
window.plSortBy=v=>{PL.sort=v;plResDraw()};
window.plCat=c=>{PL.cat=c;PL.only=false;plRender()};
window.plOnly=()=>{PL.only=!PL.only;if(PL.only)PL.cat="";plRender()};
window.plTagF=t=>{PL.tag=PL.tag===t?"":t;plRender()};
window.plTagsAll=()=>{PL.tagsAll=!PL.tagsAll;plRender()};
function plResDraw(){let box=document.getElementById("plRes");if(!box)return;let L=plSorted(plFilter()),sel=new Set(plSel()),n=document.getElementById("plN");if(n)n.textContent=`${nf(L.length)} modül`;
 if(!L.length){box.innerHTML=`<div class="plEmpty"><b>Eşleşen modül yok.</b><p>${PL.q||PL.tag||PL.cat||PL.only?`Filtreleri gevşetin ya da <button type="button" class="plLink" onclick="plClearF()">bütün filtreleri temizleyin</button>.`:`Kütüphane boş. <button type="button" class="plLink" onclick="plNew()">İlk modülü oluşturun</button> ya da bir kütüphane dosyası içe aktarın.`}</p></div>`;plSelBarDraw();return}
 let groups=PL.sort==="cat"?plCats().map(c=>({c,L:L.filter(m=>plCatOf(m)===c.id)})).filter(g=>g.L.length):[{c:null,L}];
 box.innerHTML=groups.map(g=>{let ids=g.L.map(m=>m.id),all=ids.every(i=>sel.has(i));return `<section class="plGroup"${g.c?` aria-labelledby="plG-${g.c.id}"`:` aria-label="Modüller"`}>${g.c?`<div class="plGHead"><h2 id="plG-${g.c.id}">${E(g.c.name)} <span>${g.L.length}</span></h2>${g.c.desc?`<p>${E(g.c.desc)}</p>`:""}<button type="button" class="plLink" onclick='plSelMany(${JSON.stringify(ids)},${!all})'>${all?"Seçimi kaldır":"Tümünü seç"}</button></div>`:""}<div class="plGrid">${g.L.map(m=>plCard(m,sel.has(m.id))).join("")}</div></section>`}).join("");
 plSelBarDraw()}
window.plClearF=()=>{PL.q="";PL.tag="";PL.cat="";PL.only=false;plRender()};
function plCard(m,on){let im=(m.images||[])[0],deps=(m.deps||[]).map(d=>{let x=plMod(d);return x?x.title:d});
 return `<article class="plCard${on?" sel":""}" data-pl="${m.id}">${im?`<button type="button" class="plThumb" onclick="plOpen('${m.id}')" tabindex="-1" aria-hidden="true"><img src="${E(plUrl(im.src))}" alt="" loading="lazy" decoding="async"></button>`:""}
 <div class="plCardBody"><div class="plCardTop"><label class="plChk"><input type="checkbox"${on?" checked":""} onchange="plToggle('${m.id}')"><span class="plSr">${E(m.title)} modülünü seç</span></label><span class="plCatB">${E(plCatName(plCatOf(m)))}</span><span class="plVer">v${E(m.version)}</span>${m.builtin?`<span class="plBadge">${m.edited?"Hazır · düzenlendi":"Hazır"}</span>`:`<span class="plBadge own">Özel</span>`}</div>
 <h3><button type="button" class="plTitle" onclick="plOpen('${m.id}')">${E(m.title)}</button></h3><p class="plDesc">${E(m.desc)}</p>
 ${(m.tags||[]).length?`<div class="plCardTags">${m.tags.slice(0,6).map(t=>`<span>#${E(t)}</span>`).join("")}${m.tags.length>6?`<span>+${m.tags.length-6}</span>`:""}</div>`:""}
 <ul class="plFacts"><li>${(m.criteria||[]).length} kabul kriteri</li><li>${(m.images||[]).length} görsel</li><li>${m.doc&&m.doc.trim()?"Teknik doküman":"Doküman yok"}</li>${deps.length?`<li title="${E(deps.join(", "))}">${deps.length} bağımlılık</li>`:""}</ul>
 <div class="plCardActs"><button type="button" class="btn" onclick="plCopyPrompt('${m.id}',this)">Promptu kopyala</button><button type="button" class="btn" onclick="plOpen('${m.id}')">Ayrıntılar</button></div></div></article>`}
function plSelBarDraw(){let bar=document.getElementById("plSelBar");if(!bar)return;let s=plSel();if(!s.length){bar.innerHTML="";bar.className="";return}let r=plResolve(s,true),miss=s.filter(id=>!plMod(id));
 bar.className="plSelBar";bar.innerHTML=`<div class="plSelInfo"><b>${s.length} modül seçili</b>${r.added.length?` <span>+ ${r.added.length} bağımlılık eklenecek</span>`:""}${miss.length?` <span class="plBad">${miss.length} seçim kütüphanede yok</span>`:""}${projectReady()?"":` <span class="plMuted">· proje başlatılmadığı için seçim kaydedilmiyor</span>`}</div><div class="plSelActs"><button type="button" class="btn dark" onclick="plComboOpen()">Birleştirilmiş talimat →</button><button type="button" class="btn" onclick="plExport('sel')">Seçilenleri dışa aktar</button><button type="button" class="btn" onclick="plDelSel()">Seçilenleri sil</button><button type="button" class="btn" onclick="plSelClear()">Seçimi temizle</button></div>`}
window.plCopyPrompt=(id,btn)=>{let m=plMod(id);if(m)plCopy(m.prompt,btn)};
window.plOpen=id=>{PL.view="detail";PL.id=id;PL.raw=false;plRender();window.scrollTo(0,0);let h=PG.querySelector("h1");if(h){h.setAttribute("tabindex","-1");h.focus({preventScroll:true})}};
window.plBack=()=>{PL.view="list";PL.id=null;plRender();window.scrollTo(0,0)};

/* ---------- Kategoriler ---------- */
function plCatAdmin(){let all=plMods(),hid=PL_BUILTIN.filter(b=>LIB.hidden.includes(b.id));return `<p class="plMuted">Hazır kategoriler sabittir; kendi kategorilerinizi ekleyebilir, adlandırabilir ve boşken silebilirsiniz. Yeni bir alan (ör. Güvenlik, Ödeme) için modül eklemek yeterlidir; kategori filtresi modülü olan kategorileri gösterir.</p>
 <ul class="plCatList">${plCats().map(c=>{let n=all.filter(m=>plCatOf(m)===c.id).length;return `<li><b>${E(c.name)}</b> <span class="plMuted">${n} modül${c.builtin?" · hazır":""}</span>${c.builtin?"":` <button type="button" class="plLink" onclick="plCatRen('${c.id}')">Yeniden adlandır</button>${n?"":` <button type="button" class="plLink" onclick="plCatDel('${c.id}')">Sil</button>`}`}</li>`}).join("")}</ul>
 <form class="plCatAdd" onsubmit="event.preventDefault();plCatAdd(this.n.value,this.d.value);this.reset()"><label>Yeni kategori adı<input name="n" required maxlength="60" class="control"></label><label>Kısa açıklama<input name="d" maxlength="160" class="control"></label><button class="btn" type="submit">Kategori ekle</button></form>
 ${hid.length?`<div class="plHidden"><b>Gizlenen hazır modüller</b><ul>${hid.map(b=>`<li>${E(b.title)} <button type="button" class="plLink" onclick="plUnhide('${b.id}')">Geri getir</button></li>`).join("")}</ul></div>`:""}`}
window.plCatAdd=(n,d)=>{n=String(n||"").trim();if(!n)return null;let id=plSlug(n);if(!id)return null;if(plCats().some(c=>c.id===id||norm(c.name)===norm(n))){plToast("Bu adla bir kategori zaten var.",1);return plCats().find(c=>c.id===id||norm(c.name)===norm(n)).id}LIB.cats.push({id,name:n,desc:String(d||"").trim()});plSave();plToast(`"${n}" kategorisi eklendi.`);if(PL.view==="list")plRender();return id};
window.plCatRen=id=>{let c=LIB.cats.find(x=>x.id===id);if(!c)return;let n=prompt("Kategorinin yeni adı",c.name);if(n&&n.trim()){c.name=n.trim();plSave();plRender()}};
window.plCatDel=id=>{if(plMods().some(m=>m.cat===id))return plToast("Kategoride modül var; önce modülleri başka kategoriye taşıyın.",1);LIB.cats=LIB.cats.filter(c=>c.id!==id);plSave();plRender()};
window.plUnhide=id=>{LIB.hidden=LIB.hidden.filter(x=>x!==id);plSave();plToast("Modül geri getirildi.");plRender()};

/* ---------- Ayrıntı ---------- */
function plDetail(m){let sel=plSel().includes(m.id),deps=m.deps||[],rev=plDependents(m.id),imgs=m.images||[];
 const depLi=d=>{let x=plMod(d);return x?`<li><button type="button" class="plLink" onclick="plOpen('${x.id}')">${E(x.title)}</button> <span class="plMuted">v${E(x.version)} · ${E(plCatName(plCatOf(x)))}</span></li>`:`<li class="plBad">${E(d)} — kütüphanede bulunamadı</li>`};
 return `<nav class="plCrumb" aria-label="Konum"><button type="button" class="plLink" onclick="plBack()">← Hazır Prompt Kütüphanesi</button> <span aria-hidden="true">›</span> ${E(plCatName(plCatOf(m)))}</nav>
 <div class="plDHead"><div class="plCardTop"><span class="plCatB">${E(plCatName(plCatOf(m)))}</span><span class="plVer">v${E(m.version)}</span>${m.builtin?`<span class="plBadge">${m.edited?"Hazır · düzenlendi":"Hazır modül"}</span>`:`<span class="plBadge own">Özel modül</span>`}<span class="plMuted">Güncelleme: ${E(m.updated||"—")} · Kimlik: <code>${E(m.id)}</code></span></div>
 <h1>${E(m.title)}</h1><p class="plLead">${E(m.desc)}</p>${(m.tags||[]).length?`<div class="plCardTags">${m.tags.map(t=>`<span>#${E(t)}</span>`).join("")}</div>`:""}
 <div class="plDActs"><button type="button" class="btn${sel?"":" dark"}" aria-pressed="${sel}" onclick="plToggle('${m.id}')">${sel?"✓ Seçildi — seçimden çıkar":"Projeye seç"}</button><button type="button" class="btn" onclick="plCopyPrompt('${m.id}',this)">Promptu kopyala</button><button type="button" class="btn" onclick="plEditOpen('${m.id}')">Düzenle</button><button type="button" class="btn" onclick="plDup('${m.id}')">Kopyasını oluştur</button><button type="button" class="btn" onclick="plModMdDl('${m.id}')">Modülü indir (.md)</button><button type="button" class="btn" onclick="plExport('one','${m.id}')">Dışa aktar (.json)</button>${m.edited?`<button type="button" class="btn" onclick="plReset('${m.id}')">Hazır sürüme dön</button>`:""}<button type="button" class="btn plDanger" onclick="plDel('${m.id}')">${m.builtin?"Kütüphaneden gizle":"Sil"}</button></div></div>
 <div class="plDGrid"><div class="plDMain">
 <section class="plBox" aria-labelledby="plSecP"><div class="plBoxH"><h2 id="plSecP">Prompt <span class="plMuted">${nf(m.prompt.trim()?m.prompt.trim().split(/\s+/).length:0)} kelime</span></h2><button type="button" class="plLink" onclick="plCopyPrompt('${m.id}',this)">Kopyala</button></div><div class="plPrompt" tabindex="0" role="region" aria-label="Prompt metni">${E(m.prompt)}</div></section>
 <section class="plBox" aria-labelledby="plSecC"><h2 id="plSecC">Kabul kriterleri <span class="plMuted">${(m.criteria||[]).length}</span></h2><ol class="plCrit">${(m.criteria||[]).map(c=>`<li>${plInline(c)}</li>`).join("")||"<li class='plMuted'>Kabul kriteri yok.</li>"}</ol></section>
 ${imgs.length?`<section class="plBox" aria-labelledby="plSecI"><h2 id="plSecI">Referans görseller <span class="plMuted">${imgs.length}</span></h2><div class="plImgs">${imgs.map((im,i)=>`<figure><button type="button" class="plImgBtn" onclick="plZoom('${m.id}',${i})" aria-label="Büyüt: ${E(im.alt)}"><img src="${E(plUrl(im.src))}" alt="${E(im.alt)}" loading="lazy" decoding="async"></button>${im.caption?`<figcaption>${E(im.caption)}</figcaption>`:""}</figure>`).join("")}</div></section>`:""}
 <section class="plBox" aria-labelledby="plSecD"><div class="plBoxH"><h2 id="plSecD">Teknik doküman</h2>${m.doc&&m.doc.trim()?`<span><button type="button" class="plLink" aria-pressed="${PL.raw}" onclick="plRaw()">${PL.raw?"Biçimli göster":"Ham Markdown"}</button> · <button type="button" class="plLink" onclick="plDocCopy('${m.id}',this)">Kopyala</button></span>`:""}</div>${m.doc&&m.doc.trim()?(PL.raw?`<pre class="plCode plRawMd">${E(m.doc)}</pre>`:`<div class="plMdView">${plMd(m.doc,m)}</div>`):`<p class="plMuted">Bu modülde teknik doküman yok. <button type="button" class="plLink" onclick="plEditOpen('${m.id}')">Doküman ekle</button></p>`}</section>
 </div><aside class="plDSide">
 <section class="plBox"><h2>Bağımlılıklar</h2>${deps.length?`<p class="plMuted">Bu modülden önce uygulanmalı:</p><ul class="plDeps">${deps.map(depLi).join("")}</ul>`:`<p class="plMuted">Bağımlılığı yok.</p>`}${rev.length?`<p class="plMuted">Bu modüle bağımlı olanlar:</p><ul class="plDeps">${rev.map(x=>depLi(x.id)).join("")}</ul>`:""}</section>
 ${(m.refs||[]).length?`<section class="plBox"><h2>Teknik doküman referansları</h2><ul class="plRefs">${m.refs.map(r=>`<li><a href="${E(r.u)}" target="_blank" rel="noopener noreferrer">${E(r.t||r.u)}</a></li>`).join("")}</ul></section>`:""}
 <section class="plBox"><h2>Sürüm geçmişi</h2><ul class="plHist"><li><b>v${E(m.version)}</b> <span class="plMuted">${E(m.updated||"")} · güncel</span></li>${(m.history||[]).map((h,i)=>`<li><b>v${E(h.version)}</b> <span class="plMuted">${E(h.date||"")}</span>${h.note?`<br><span>${E(h.note)}</span>`:""}${h.data?` <button type="button" class="plLink" onclick="plRestore('${m.id}',${i})">Bu sürümün metnini geri yükle</button>`:""}</li>`).join("")}</ul>${m.builtin?`<p class="plMuted">Hazır modülü düzenlediğinizde değişiklik yalnız bu tarayıcıdaki kütüphanenize kaydedilir; "Hazır sürüme dön" ile aslına dönebilirsiniz.</p>`:""}</section>
 </aside></div>`}
window.plRaw=()=>{PL.raw=!PL.raw;plRender()};
window.plDocCopy=(id,b)=>{let m=plMod(id);if(m)plCopy(m.doc,b)};
window.plZoom=(id,i)=>{let m=plMod(id);if(!m)return;let L=m.images||[];i=(i+L.length)%L.length;let im=L[i];if(!im)return;
 ZD.innerHTML=`<div class="plZHead"><h2 id="plZoomT">${E(m.title)} — görsel ${i+1}/${L.length}</h2><button type="button" class="btn" onclick="document.getElementById('plZoom').close()" aria-label="Kapat">✕</button></div><div class="plZBody"><img src="${E(plUrl(im.src))}" alt="${E(im.alt)}"></div><p class="plZCap">${E(im.caption||im.alt)}</p>${L.length>1?`<div class="plZNav"><button type="button" class="btn" onclick="plZoom('${m.id}',${i-1})">‹ Önceki</button><button type="button" class="btn" onclick="plZoom('${m.id}',${i+1})">Sonraki ›</button></div>`:""}`;
 ZD.onkeydown=e=>{if(L.length>1&&(e.key==="ArrowLeft"||e.key==="ArrowRight")){e.preventDefault();plZoom(id,i+(e.key==="ArrowRight"?1:-1))}};
 if(!ZD.open){ZD.dataset.ret=document.activeElement&&document.activeElement.id||"";ZD._ret=document.activeElement;ZD.showModal()}let c=ZD.querySelector(".plZHead .btn");if(c)c.focus()};
ZD.addEventListener("close",()=>{if(ZD._ret&&document.contains(ZD._ret))ZD._ret.focus()});
window.plDup=id=>{let m=plMod(id);if(!m)return;let x=clone(m);x.id=plUniqId(m.id+"-kopya");x.title=m.title+" (kopya)";x.version="1.0.0";x.updated=today();x.history=[];plStore(x);plSave();plToast("Kopya oluşturuldu; düzenleyebilirsiniz.");plEditOpen(x.id)};
window.plReset=id=>{if(!BI[id]||!confirm("Bu hazır modüldeki bütün düzenlemeler silinip modül hazır sürümüne dönecek. Devam edilsin mi?"))return;delete LIB.over[id];plSave();plToast("Hazır sürüme dönüldü.");plRender()};
window.plDel=id=>{let m=plMod(id);if(!m)return;let rev=plDependents(id);if(!confirm(`"${m.title}" ${m.builtin?"kütüphaneden gizlenecek (Kategorileri yönet › Gizlenen hazır modüller'den geri getirebilirsiniz)":"kalıcı olarak silinecek"}.${rev.length?`\n\n${rev.length} modül buna bağımlı: ${rev.map(x=>x.title).join(", ")}. Bağımlılık kaydı kalır ve "kütüphanede bulunamadı" olarak işaretlenir.`:""}\n\nDevam edilsin mi?`))return;plRemove([id]);plToast(m.builtin?"Modül gizlendi.":"Modül silindi.");plBack()};
function plRemove(ids){ids.forEach(id=>{if(BI[id]){delete LIB.over[id];if(!LIB.hidden.includes(id))LIB.hidden.push(id)}else delete LIB.mods[id]});plSave();let s=plSel().filter(x=>!ids.includes(x));plSetSel(s)}
window.plDelSel=()=>{let ids=plSel().filter(id=>plMod(id));if(!ids.length)return;let bi=ids.filter(i=>BI[i]).length;if(!confirm(`${ids.length} modül ${bi?`(${bi} hazır modül gizlenir, ${ids.length-bi} özel modül kalıcı silinir)`:"kalıcı olarak silinecek"}. Devam edilsin mi?`))return;plRemove(ids);plToast(`${ids.length} modül kaldırıldı.`);plRender()};
window.plRestore=(id,i)=>{let m=plMod(id),h=m&&(m.history||[])[i];if(!h||!h.data||!confirm(`v${h.version} sürümünün metni yeni bir sürüm olarak geri yüklenecek. Devam edilsin mi?`))return;let x=clone(m);let prev={version:m.version,date:m.updated||today(),note:`v${h.version} geri yüklenmeden önceki sürüm`,data:plTextOnly(m)};Object.assign(x,clone(h.data));x.version=plBump(m.version,"minor");x.updated=today();x.history=[prev].concat(m.history||[]).slice(0,PL_HIST);plStore(x);plSave();plToast(`v${h.version} geri yüklendi (yeni sürüm v${x.version}).`);plRender()};

/* ---------- Düzenleme ---------- */
const PL_DOC0="# Modül adı — Teknik Doküman\n\n## Kapsam\n- \n\n## Bileşenler\n1. \n\n## Akış\n1. \n\n## Test\n- \n\n## Kaçınılacaklar\n- ";
window.plNew=()=>{PL.draft={id:"",title:"",desc:"",cat:PL.cat||"",tags:[],prompt:"",doc:PL_DOC0,images:[],criteria:[],deps:[],refs:[],version:"1.0.0",history:[],isNew:true,bump:"patch",note:"",newCat:""};PL.view="edit";PL.id=null;PL.dirty=false;PL.errs=[];PL.mdPrev=false;plRender();window.scrollTo(0,0);let f=document.getElementById("plF-title");if(f)f.focus()};
window.plEditOpen=id=>{let m=plMod(id);if(!m)return;PL.draft=Object.assign(clone(m),{isNew:false,bump:"patch",note:"",newCat:""});PL.view="edit";PL.id=id;PL.dirty=false;PL.errs=[];PL.mdPrev=false;plRender();window.scrollTo(0,0);let f=document.getElementById("plF-title");if(f)f.focus()};
window.plD=(k,v)=>{let d=PL.draft;if(!d)return;if(k==="tags")d.tags=String(v).split(",").map(t=>t.trim().replace(/^#/,"")).filter(Boolean).slice(0,30);else if(k==="criteria")d.criteria=String(v).split("\n").map(t=>t.replace(/^\s*([-*]|\d+[.)])\s+/,"").trim()).filter(Boolean);else if(k==="refs")d.refs=String(v).split("\n").map(l=>{let p=l.split("|").map(x=>x.trim());let u=p.length>1?p.slice(1).join("|").trim():p[0];return{t:p.length>1?p[0]:"",u}}).filter(r=>r.u);else d[k]=v;PL.dirty=true;
 if(k==="prompt"){let w=document.getElementById("plWc");if(w)w.textContent=`${nf(String(v).trim()?String(v).trim().split(/\s+/).length:0)} kelime`}
 if(k==="doc"&&PL.mdPrev){let p=document.getElementById("plMdPrev");if(p)p.innerHTML=plMd(v,PL.draft)}};
window.plDep=(id,on)=>{let d=PL.draft;d.deps=(d.deps||[]).filter(x=>x!==id);if(on)d.deps.push(id);PL.dirty=true};
window.plMdToggle=()=>{PL.mdPrev=!PL.mdPrev;let p=document.getElementById("plMdPrev"),b=document.getElementById("plMdBtn");if(p){p.hidden=!PL.mdPrev;if(PL.mdPrev)p.innerHTML=plMd(PL.draft.doc,PL.draft)}if(b){b.textContent=PL.mdPrev?"Önizlemeyi kapat":"Önizle";b.setAttribute("aria-pressed",PL.mdPrev)}};
function plImgsHtml(){let d=PL.draft;return (d.images||[]).map((im,i)=>`<li class="plImgRow"><img src="${E(plUrl(im.src))}" alt=""><div class="plImgF"><label>Alternatif metin <span class="plReq">*</span><input class="control" id="plF-alt-${i}" value="${E(im.alt)}" maxlength="500" oninput="plImgSet(${i},'alt',this.value)" aria-describedby="plAltHelp"></label><label>Açıklama (isteğe bağlı)<input class="control" value="${E(im.caption||"")}" maxlength="500" oninput="plImgSet(${i},'caption',this.value)"></label></div><div class="plImgOps"><button type="button" class="btn" onclick="plImgMove(${i},-1)" ${i?"":"disabled"} aria-label="Yukarı taşı">↑</button><button type="button" class="btn" onclick="plImgMove(${i},1)" ${i<d.images.length-1?"":"disabled"} aria-label="Aşağı taşı">↓</button><button type="button" class="btn plDanger" onclick="plImgDel(${i})" aria-label="Görseli kaldır">✕</button></div></li>`).join("")}
function plImgsDraw(){let u=document.getElementById("plImgList");if(u)u.innerHTML=plImgsHtml();let n=document.getElementById("plImgN");if(n)n.textContent=(PL.draft.images||[]).length}
window.plImgSet=(i,k,v)=>{PL.draft.images[i][k]=v;PL.dirty=true};
window.plImgMove=(i,dir)=>{let L=PL.draft.images,j=i+dir;if(j<0||j>=L.length)return;[L[i],L[j]]=[L[j],L[i]];PL.dirty=true;plImgsDraw()};
window.plImgDel=i=>{PL.draft.images.splice(i,1);PL.dirty=true;plImgsDraw()};
window.plImgFiles=async inp=>{let fs=[...inp.files],errs=[];inp.value="";for(const f of fs){if(PL.draft.images.length>=30){errs.push("En çok 30 görsel eklenebilir.");break}try{let src=await plFileImg(f);PL.draft.images.push({id:"img-"+Date.now().toString(36)+Math.random().toString(36).slice(2,6),src,alt:"",caption:""});PL.dirty=true}catch(e){errs.push(e.message||String(e))}}plImgsDraw();if(errs.length)plToast(errs.join(" · "),1);else if(fs.length)plToast(`${fs.length} görsel eklendi. Her görsele alternatif metin yazın.`)};
window.plImgUrl=()=>{let i=document.getElementById("plImgUrlIn"),u=(i&&i.value||"").trim();if(!/^https:\/\/\S+$/i.test(u))return plToast("Görsel adresi https:// ile başlamalı.",1);PL.draft.images.push({id:"img-"+Date.now().toString(36),src:u,alt:"",caption:""});i.value="";PL.dirty=true;plImgsDraw()};
function plEdit(){let d=PL.draft,others=plMods().filter(m=>m.id!==d.id),C=plCats(),e=PL.errs||[];
 const fe=k=>e.find(x=>x.k===k),err=k=>fe(k)?`<p class="plErr" id="plE-${k}">${E(fe(k).t)}</p>`:"",inv=k=>fe(k)?` aria-invalid="true" aria-describedby="plE-${k}"`:"";
 let vers=d.isNew?`<label for="plF-version">Sürüm</label><input id="plF-version" class="control plShort" value="${E(d.version)}" oninput="plD('version',this.value)"${inv("version")}>${err("version")}`:
  `<fieldset class="plFs"><legend>Yeni sürüm (şu an v${E(d.version)})</legend>${[["patch","Yama — düzeltme, yazım"],["minor","Küçük — yeni kriter / bölüm, geriye uyumlu"],["major","Büyük — kapsam ya da davranış değişti"]].map(o=>`<label class="plRad"><input type="radio" name="plBump" value="${o[0]}"${d.bump===o[0]?" checked":""} onchange="plD('bump','${o[0]}')"> v${plBump(d.version,o[0])} · ${o[1]}</label>`).join("")}</fieldset><label for="plF-note">Değişiklik notu</label><input id="plF-note" class="control" maxlength="300" value="${E(d.note||"")}" placeholder="Ör. Consent Mode parametreleri güncellendi" oninput="plD('note',this.value)">`;
 return `<nav class="plCrumb" aria-label="Konum"><button type="button" class="plLink" onclick="plCancel()">← ${d.isNew?"Hazır Prompt Kütüphanesi":E(d.title||"Modül")}</button></nav>
 <h1>${d.isNew?"Yeni modül":"Modülü düzenle"}</h1>${!d.isNew&&BI[d.id]?`<p class="plMuted">Bu bir hazır modül; değişiklikleriniz bu tarayıcıdaki kütüphanede saklanır ve "Hazır sürüme dön" ile geri alınabilir.</p>`:""}
 ${e.length?`<div class="plErrSum" id="plErrSum" role="alert" tabindex="-1"><h2>${e.length} alanda düzeltme gerekiyor</h2><ul>${e.map(x=>`<li><a href="#${x.f}" onclick="event.preventDefault();let t=document.getElementById('${x.f}');if(t)t.focus()">${E(x.t)}</a></li>`).join("")}</ul></div>`:""}
 <form class="plForm" onsubmit="event.preventDefault();plSaveDraft()" novalidate>
 <p class="plMuted"><span class="plReq">*</span> işaretli alanlar zorunludur.</p>
 <div class="plRow2"><div><label for="plF-title">Başlık <span class="plReq">*</span></label><input id="plF-title" class="control" maxlength="200" value="${E(d.title)}" oninput="plD('title',this.value)"${inv("title")}>${err("title")}</div>
 <div><label for="plF-cat">Kategori <span class="plReq">*</span></label><select id="plF-cat" class="control" onchange="plD('cat',this.value)"${inv("cat")}><option value="">Seçin…</option>${C.map(c=>`<option value="${c.id}"${d.cat===c.id?" selected":""}>${E(c.name)}</option>`).join("")}</select>${err("cat")}<label for="plF-newcat" class="plSub">ya da yeni kategori</label><input id="plF-newcat" class="control" maxlength="60" value="${E(d.newCat||"")}" placeholder="Ör. Güvenlik › Oturum yönetimi" oninput="plD('newCat',this.value)"></div></div>
 <label for="plF-desc">Açıklama <span class="plReq">*</span></label><p class="plHelp" id="plH-desc">Modülün ne yaptığını 1–2 cümleyle anlatın; listede ve birleştirilmiş talimatta "Amaç" olarak görünür.</p><textarea id="plF-desc" class="control" rows="2" maxlength="4000" oninput="plD('desc',this.value)" aria-describedby="plH-desc${fe("desc")?" plE-desc":""}"${fe("desc")?' aria-invalid="true"':""}>${E(d.desc)}</textarea>${err("desc")}
 <label for="plF-tags">Etiketler</label><p class="plHelp" id="plH-tags">Virgülle ayırın, ör. çerez, rıza, analitik.</p><input id="plF-tags" class="control" value="${E((d.tags||[]).join(", "))}" oninput="plD('tags',this.value)" aria-describedby="plH-tags">
 <label for="plF-prompt">Kısa prompt <span class="plReq">*</span></label><p class="plHelp" id="plH-prompt">Claude'a verilecek görev: ne yapılacak, hangi sınırlarla, nasıl doğrulanacak. Ayrıntılar teknik dokümanda durur.</p><textarea id="plF-prompt" class="control" rows="7" maxlength="50000" oninput="plD('prompt',this.value)" aria-describedby="plH-prompt plWc${fe("prompt")?" plE-prompt":""}"${fe("prompt")?' aria-invalid="true"':""}>${E(d.prompt)}</textarea><p class="plHelp" id="plWc" aria-live="off">${nf(d.prompt.trim()?d.prompt.trim().split(/\s+/).length:0)} kelime</p>${err("prompt")}
 <label for="plF-criteria">Kabul kriterleri <span class="plReq">*</span></label><p class="plHelp" id="plH-crit">Her satıra bir ölçülebilir kriter yazın; birleştirilmiş talimatta işaretlenebilir liste olur.</p><textarea id="plF-criteria" class="control" rows="6" oninput="plD('criteria',this.value)" aria-describedby="plH-crit${fe("criteria")?" plE-criteria":""}"${fe("criteria")?' aria-invalid="true"':""}>${E((d.criteria||[]).join("\n"))}</textarea>${err("criteria")}
 <div class="plBoxH"><label for="plF-doc">Teknik doküman (Markdown)</label><button type="button" class="plLink" id="plMdBtn" aria-pressed="${PL.mdPrev}" onclick="plMdToggle()">${PL.mdPrev?"Önizlemeyi kapat":"Önizle"}</button></div><p class="plHelp" id="plH-doc">Başlık (#), liste (-, 1.), tablo (| a | b |), kod bloğu (\`\`\`), kalın (**), satır içi kod (\`) ve bağlantı ([ad](https://…)) desteklenir.</p><textarea id="plF-doc" class="control plMono" rows="14" maxlength="500000" oninput="plD('doc',this.value)" aria-describedby="plH-doc">${E(d.doc||"")}</textarea><div id="plMdPrev" class="plMdView plPrev"${PL.mdPrev?"":" hidden"}>${PL.mdPrev?plMd(d.doc,d):""}</div>
 <fieldset class="plFs"><legend>Referans görseller <span class="plMuted" id="plImgN">${(d.images||[]).length}</span></legend><p class="plHelp" id="plAltHelp">PNG, JPEG, WebP, GIF ya da SVG; büyük görseller 1600 px'e küçültülüp WebP'ye çevrilir. Her görselin ne gösterdiğini anlatan alternatif metin zorunludur.</p>${err("images")}<ul class="plImgList" id="plImgList">${plImgsHtml()}</ul>
 <div class="plImgAdd"><label class="btn plFileBtn">Görsel yükle<input type="file" accept="image/png,image/jpeg,image/webp,image/gif,image/svg+xml" multiple onchange="plImgFiles(this)"></label><span class="plMuted">ya da</span><label for="plImgUrlIn" class="plSr">Görsel adresi</label><input id="plImgUrlIn" class="control" type="url" placeholder="https://… görsel adresi" onkeydown="if(event.key==='Enter'){event.preventDefault();plImgUrl()}"><button type="button" class="btn" onclick="plImgUrl()">Adresi ekle</button></div></fieldset>
 <fieldset class="plFs"><legend>Bağımlılıklar</legend><p class="plHelp">Bu modülden önce uygulanması gereken modüller. Birleştirilmiş talimatta önce bunlar sıralanır.</p>${err("deps")}${others.length?`<div class="plDepGrid">${C.map(c=>{let L=others.filter(m=>plCatOf(m)===c.id);return L.length?`<div><b>${E(c.name)}</b>${L.map(m=>`<label class="plCk"><input type="checkbox"${(d.deps||[]).includes(m.id)?" checked":""} onchange="plDep('${m.id}',this.checked)"> ${E(m.title)}</label>`).join("")}</div>`:""}).join("")}</div>`:`<p class="plMuted">Kütüphanede başka modül yok.</p>`}${(d.deps||[]).filter(x=>!plMod(x)).map(x=>`<p class="plBad">Kütüphanede olmayan bağımlılık: <code>${E(x)}</code> <button type="button" class="plLink" onclick="plDep(${E(JSON.stringify(x))},false);this.parentNode.remove()">Kaldır</button></p>`).join("")}</fieldset>
 <label for="plF-refs">Teknik doküman referansları</label><p class="plHelp" id="plH-refs">Her satıra "Başlık | https://adres". Yalnız http(s) adresleri kaydedilir.</p><textarea id="plF-refs" class="control" rows="4" oninput="plD('refs',this.value)" aria-describedby="plH-refs">${E((d.refs||[]).map(r=>r.t?`${r.t} | ${r.u}`:r.u).join("\n"))}</textarea>
 ${vers}
 <div class="plFormActs"><button type="submit" class="btn dark">${d.isNew?"Modülü oluştur":"Kaydet"}</button><button type="button" class="btn" onclick="plCancel()">Vazgeç</button></div></form>`}
window.plCancel=()=>{if(PL.dirty&&!confirm("Kaydedilmemiş değişiklikler silinecek. Devam edilsin mi?"))return;let id=PL.draft&&!PL.draft.isNew?PL.draft.id:null;PL.draft=null;PL.dirty=false;PL.errs=[];if(id&&plMod(id))plOpen(id);else plBack()};
window.plSaveDraft=()=>{let d=PL.draft;if(!d)return;let e=[];d.title=String(d.title||"").trim();d.desc=String(d.desc||"").trim();d.prompt=String(d.prompt||"").trim();
 if(String(d.newCat||"").trim()){let id=plCatAdd(d.newCat,"");if(id){d.cat=id;d.newCat=""}}
 if(!d.title)e.push({k:"title",f:"plF-title",t:"Başlık yazın."});
 if(!d.cat||!plCats().some(c=>c.id===d.cat))e.push({k:"cat",f:"plF-cat",t:"Bir kategori seçin ya da yeni kategori adı yazın."});
 if(!d.desc)e.push({k:"desc",f:"plF-desc",t:"Kısa bir açıklama yazın."});
 if(!d.prompt)e.push({k:"prompt",f:"plF-prompt",t:"Kısa promptu yazın."});
 if(!(d.criteria||[]).length)e.push({k:"criteria",f:"plF-criteria",t:"En az bir kabul kriteri yazın."});
 let noAlt=(d.images||[]).findIndex(im=>!String(im.alt||"").trim());if(noAlt>=0)e.push({k:"images",f:"plF-alt-"+noAlt,t:`${noAlt+1}. görselin alternatif metnini yazın.`});
 if(d.isNew&&!PL_VER_RE.test(String(d.version||"")))e.push({k:"version",f:"plF-version",t:"Sürümü 1.0.0 biçiminde yazın."});
 let id=d.isNew?plUniqId(d.title):d.id;if((d.deps||[]).some(x=>x===id)||plCycleWith(id,d.deps||[]))e.push({k:"deps",f:"plF-title",t:"Seçilen bağımlılıklar döngü oluşturuyor (bir bağımlılık zaten bu modüle bağımlı)."});
 PL.errs=e;if(e.length){plRender();let s=document.getElementById("plErrSum");if(s)s.focus();return}
 let old=d.isNew?null:plMod(d.id),x={id,title:d.title,desc:d.desc,cat:d.cat,tags:d.tags||[],prompt:d.prompt,doc:String(d.doc||""),images:(d.images||[]).map(im=>({id:im.id,name:im.name||"",src:im.src,alt:String(im.alt).trim(),caption:String(im.caption||"").trim()})),criteria:d.criteria||[],deps:[...new Set(d.deps||[])],refs:(d.refs||[]).filter(r=>/^https?:\/\//i.test(r.u)),updated:today()};
 if(old){let same=JSON.stringify(plTextOnly(old))===JSON.stringify(plTextOnly(x))&&JSON.stringify(old.images||[])===JSON.stringify(x.images);if(same){PL.dirty=false;PL.draft=null;plToast("Değişiklik yok.");return plOpen(id)}
  x.version=plBump(old.version,d.bump);x.history=[{version:old.version,date:old.updated||today(),note:String(d.note||"").trim(),data:plTextOnly(old)}].concat(old.history||[]).slice(0,PL_HIST)}
 else{x.version=d.version;x.history=[]}
 plStore(x);plSave();PL.dirty=false;PL.draft=null;PL.errs=[];let s=plSel();if(s.includes(id))plSetSel(s);plToast(old?`Kaydedildi — v${x.version}.`:"Modül oluşturuldu.");plOpen(id)};

/* ---------- Birleştirilmiş talimat ---------- */
window.plComboOpen=()=>{PL.view="combine";plRender();window.scrollTo(0,0);let h=PG.querySelector("h1");if(h){h.setAttribute("tabindex","-1");h.focus({preventScroll:true})}};
window.plCombo=(k,v)=>{PL.combo[k]=v;plRender()};
function plShift(md,by){let inC=false;return String(md||"").split("\n").map(l=>{if(/^\s*```/.test(l)){inC=!inC;return l}if(!inC&&/^#{1,6}\s/.test(l)){let m=/^(#+)/.exec(l)[1].length;return "#".repeat(Math.min(6,m+by))+l.slice(m)}return l}).join("\n")}
function plComboData(){let ids=plSel().filter(id=>plMod(id)),res=plResolve(ids,PL.combo.deps),miss=plSel().filter(id=>!plMod(id));return{ids,res,miss}}
function plComboText(D,opt){let {ids,res,miss}=D,O=res.order,zip=opt&&opt.zip,full=PL.combo.docs==="full",nm=pname(),L=[];
 const why=m=>ids.includes(m.id)?"Seçildi":`Bağımlılık (${(plMod(res.why[m.id])||{}).title||res.why[m.id]})`;
 L.push("# Geliştirme Talimatı — Hazır Prompt Modülleri","",nm?`- Proje: ${nm}`:"",`- Hazırlanma tarihi: ${today()}`,"- Kaynak: WP-OnKe · Hazır Prompt Kütüphanesi",`- Modül sayısı: ${O.length} (seçilen ${ids.length}${res.added.length?`, bağımlılık olarak eklenen ${res.added.length}`:""})`,"");
 L.push("## Nasıl uygulanır","1. Kod yazmadan önce repository'yi ve mevcut mimariyi incele; her modülün hangi dosyalara dokunacağını kısa bir planla çıkar.","2. Modülleri aşağıdaki sırayla uygula. Sıra bağımlılıklara göre belirlendi: bir modül, bağımlı olduğu modüller tamamlanmadan başlamaz.","3. Her modülde önce \"Görev\"i, ardından teknik dokümanı oku; doküman ile kod tabanındaki gerçek yapı çelişirse kod tabanını esas al ve farkı raporla.","4. Her modülün kabul kriterlerini tek tek doğrula (test, komut çıktısı, ekran görüntüsü); doğrulanamayanı gerekçesiyle raporla.","5. Çalışan özellikleri ve onaylanmış arayüzü izinsiz kaldırma; en küçük güvenli değişiklik setini uygula. Her modülden sonra test, lint ve build çalıştır.","6. Proje kararları dosyası (ör. CLAUDE-TALIMATLARI.md) da kullanılıyorsa önce onu esas al; bu talimatla çelişen bir nokta olursa kullanıcıya sor.","7. Modüller arasında kullanıcı onayı iste: her modülün sonunda kısa bir rapor ver ve \"devam\" demeden sonrakine geçme.","");
 L.push("## Uygulama sırası","| Sıra | Modül | Kimlik | Sürüm | Kategori | Önce tamamlanmalı | Neden listede |","|---|---|---|---|---|---|---|");
 O.forEach((m,i)=>L.push(`| ${i+1} | ${m.title.replace(/\|/g,"/")} | \`${m.id}\` | ${m.version} | ${plCatName(plCatOf(m))} | ${(m.deps||[]).map(d=>{let x=plMod(d);return x?x.title.replace(/\|/g,"/"):d}).join(", ")||"—"} | ${why(m)} |`));L.push("");
 let W=[];res.missing.forEach(x=>W.push(`Kütüphanede bulunamayan bağımlılık: \`${x.id}\` (${(plMod(x.from)||{}).title||x.from} istiyor). Karşılığını kod tabanında doğrula ya da kullanıcıya sor.`));
 res.cycles.forEach(c=>W.push(`Döngüsel bağımlılık: ${c.map(id=>(plMod(id)||{}).title||id).join(" → ")}. Sırayı uygulamadan önce kullanıcıyla netleştir.`));
 res.loose.forEach(x=>W.push(`Seçilmemiş bağımlılık: ${(plMod(x.from)||{}).title||x.from} → ${x.known?(plMod(x.id)||{}).title:`\`${x.id}\``}. Bu talimata eklenmedi; projede zaten uygulanmış olduğunu doğrula.`));
 miss.forEach(id=>W.push(`Projede seçili ama bu kütüphanede olmayan modül: \`${id}\`${state.promptLib&&state.promptLib.names&&state.promptLib.names[id]?` (${state.promptLib.names[id]})`:""}. Talimata eklenmedi.`));
 if(W.length)L.push("## Uyarılar",...W.map(w=>"- "+w),"");
 O.forEach((m,i)=>{L.push("---","",`## ${i+1}. ${m.title}`,"",`\`${m.id}\` · sürüm ${m.version} · ${plCatName(plCatOf(m))}${(m.tags||[]).length?` · Etiketler: ${m.tags.join(", ")}`:""}`,"",`**Amaç:** ${m.desc}`,"",`**Önce tamamlanmış olmalı:** ${(m.deps||[]).map(d=>{let x=plMod(d);return x?`${x.title} (\`${d}\`)`:`\`${d}\` (kütüphanede yok)`}).join(", ")||"—"}`,"","### Görev","",plShift(m.prompt.trim(),3),"","### Kabul kriterleri","",...(m.criteria||[]).map(c=>`- [ ] ${c}`),"");
  if(m.doc&&m.doc.trim()){L.push("### Teknik doküman","");if(full)L.push(plShift(plDocOut(m,"").trim(),3),"");else L.push(`Teknik doküman ayrı dosyada: \`prompt-moduller/${m.id}.md\`${zip?"":" (zip paketinde)"}. Uygulamaya başlamadan önce oku.`,"")}
  let im=m.images||[];if(im.length){L.push("### Referans görseller","");im.forEach((x,j)=>{let f=plImgName(m,j,x);L.push(`${j+1}. ${f?`\`${f}\``:x.src} — ${x.alt}${x.caption?` (${x.caption})`:""}`)});if(!zip&&im.some(x=>/^data:/i.test(x.src)))L.push("","Görsel dosyaları zip paketindedir; metin açıklamaları yukarıda.");L.push("")}
  if((m.refs||[]).length)L.push("### Teknik doküman referansları","",...m.refs.map(r=>`- [${r.t||r.u}](${r.u})`),"")});
 L.push("---","","## Son kontrol ve rapor","- Her modül için durum: uygulandı / kısmen / uygulanmadı + gerekçe.","- Kabul kriterlerinin her birinin nasıl doğrulandığı (test adı, komut çıktısı, ekran görüntüsü).","- Değişen dosyaların listesi, açık riskler ve kullanıcı kararı bekleyen konular.","");
 return L.filter((x,i,a)=>!(x===""&&a[i-1]==="")).join("\n").replace(/^\n+/,"")}
function plCombine(){let D=plComboData(),{ids,res,miss}=D;
 if(!ids.length)return `<nav class="plCrumb" aria-label="Konum"><button type="button" class="plLink" onclick="plBack()">← Hazır Prompt Kütüphanesi</button></nav><h1>Birleştirilmiş geliştirme talimatı</h1><div class="plEmpty"><b>Seçili modül yok.</b><p>Kütüphanede modüllerin onay kutusunu işaretleyin; seçtikleriniz burada tek talimatta birleşir.</p><button type="button" class="btn dark" onclick="plBack()">Modül seç</button></div>`;
 let txt=plComboText(D),words=txt.trim().split(/\s+/).length,imgs=res.order.reduce((a,m)=>a+(m.images||[]).filter(x=>/^data:/i.test(x.src)).length,0);
 let warn=res.missing.length+res.cycles.length+res.loose.length+miss.length;
 return `<nav class="plCrumb" aria-label="Konum"><button type="button" class="plLink" onclick="plBack()">← Hazır Prompt Kütüphanesi</button></nav>
 <h1>Birleştirilmiş geliştirme talimatı</h1><p class="plLead">Seçtiğiniz ${ids.length} modül${res.added.length?` ve ${res.added.length} bağımlılık`:""}, bağımlılık sırasına göre tek talimatta birleşti. Talimatı kopyalayıp Claude'a verin ya da teknik dokümanlar ve görsellerle birlikte zip olarak indirin.</p>
 <div class="plDGrid"><div class="plDMain">
 <section class="plBox" aria-labelledby="plCoO"><h2 id="plCoO">Uygulama sırası</h2><ol class="plOrder">${res.order.map(m=>`<li><button type="button" class="plLink" onclick="plOpen('${m.id}')">${E(m.title)}</button> <span class="plVer">v${E(m.version)}</span> <span class="plMuted">${E(plCatName(plCatOf(m)))}</span>${ids.includes(m.id)?"":` <span class="plBadge dep">bağımlılık · ${E((plMod(res.why[m.id])||{}).title||"")} için</span>`}</li>`).join("")}</ol>
 ${warn?`<div class="plWarn" role="status"><b>Dikkat</b><ul>${res.missing.map(x=>`<li>Kütüphanede bulunamayan bağımlılık: <code>${E(x.id)}</code> (${E((plMod(x.from)||{}).title||x.from)})</li>`).join("")}${res.cycles.map(c=>`<li>Döngüsel bağımlılık: ${c.map(id=>E((plMod(id)||{}).title||id)).join(" → ")}</li>`).join("")}${res.loose.map(x=>`<li>Seçilmemiş bağımlılık: ${E((plMod(x.from)||{}).title||x.from)} → ${E(x.known?(plMod(x.id)||{}).title:x.id)}</li>`).join("")}${miss.map(id=>`<li>Seçili ama kütüphanede olmayan modül: <code>${E(id)}</code></li>`).join("")}</ul><p class="plMuted">Uyarılar talimata da yazılır.</p></div>`:""}</section>
 <section class="plBox" aria-labelledby="plCoT"><div class="plBoxH"><h2 id="plCoT">Talimat önizlemesi</h2><span class="plMuted">${nf(words)} kelime · ${nf(txt.length)} karakter</span></div><label for="plComboTa" class="plSr">Birleştirilmiş talimat metni</label><textarea id="plComboTa" class="control plMono plComboTa" rows="22" readonly>${E(txt)}</textarea></section>
 </div><aside class="plDSide"><section class="plBox"><h2>Seçenekler</h2>
 <fieldset class="plFs"><legend>Bağımlılıklar</legend><label class="plRad"><input type="radio" name="plCD" ${PL.combo.deps?"checked":""} onchange="plCombo('deps',true)"> Seçilmemiş bağımlılıkları da ekle (önerilen)</label><label class="plRad"><input type="radio" name="plCD" ${PL.combo.deps?"":"checked"} onchange="plCombo('deps',false)"> Yalnız seçilenler; eksikleri uyarı olarak yaz</label></fieldset>
 <fieldset class="plFs"><legend>Teknik dokümanlar</legend><label class="plRad"><input type="radio" name="plDoc" ${PL.combo.docs==="full"?"checked":""} onchange="plCombo('docs','full')"> Talimatın içinde tam metin</label><label class="plRad"><input type="radio" name="plDoc" ${PL.combo.docs==="ref"?"checked":""} onchange="plCombo('docs','ref')"> Yalnız dosya referansı (zip'te ayrı dosyalar)</label></fieldset>
 <div class="plStack"><button type="button" class="btn dark" onclick="plCopy(document.getElementById('plComboTa').value,this)">Talimatı kopyala</button><button type="button" class="btn" onclick="plComboMd()">GELISTIRME-TALIMATI.md indir</button><button type="button" class="btn" onclick="plComboZip()">Zip indir (talimat + dokümanlar${imgs?` + ${imgs} görsel`:""})</button></div>
 <p class="plMuted">Zip içeriği: <code>GELISTIRME-TALIMATI.md</code>, her modül için <code>prompt-moduller/&lt;kimlik&gt;.md</code>, <code>gorseller/</code> ve modüllerin kütüphane kaydı <code>prompt-kutuphanesi-secim.json</code> (başka bir tarayıcıya içe aktarılabilir).</p></section></aside></div>`}
window.plComboMd=()=>{let D=plComboData();if(!D.ids.length)return;mkSave(plComboText(D),"GELISTIRME-TALIMATI.md","text/markdown;charset=utf-8")};
function plModMd(m,rel){let L=[`# ${m.title}`,"",`- Kimlik: \`${m.id}\``,`- Sürüm: ${m.version} (${m.updated||""})`,`- Kategori: ${plCatName(plCatOf(m))}`,(m.tags||[]).length?`- Etiketler: ${m.tags.join(", ")}`:"",(m.deps||[]).length?`- Bağımlılıklar: ${m.deps.map(d=>{let x=plMod(d);return x?`${x.title} (\`${d}\`)`:`\`${d}\``}).join(", ")}`:"","",`**Amaç:** ${m.desc}`,"","## Görev","",plShift(m.prompt.trim(),2),"","## Kabul kriterleri","",...(m.criteria||[]).map(c=>`- [ ] ${c}`),""];
 if(m.doc&&m.doc.trim())L.push("## Teknik doküman","",plShift(plDocOut(m,rel||"").trim(),2),"");
 if((m.images||[]).length)L.push("## Referans görseller","",...m.images.map((x,j)=>{let f=plImgName(m,j,x);return `${j+1}. ${f?`\`${f}\``:x.src} — ${x.alt}${x.caption?` (${x.caption})`:""}`}),"");
 if((m.refs||[]).length)L.push("## Teknik doküman referansları","",...m.refs.map(r=>`- [${r.t||r.u}](${r.u})`),"");
 return L.filter((x,i,a)=>!(x===""&&a[i-1]==="")).join("\n")}
window.plModMdDl=id=>{let m=plMod(id);if(m)mkSave(plModMd(m),`${m.id}.md`,"text/markdown;charset=utf-8")};
window.plComboZip=()=>{let D=plComboData();if(!D.ids.length)return;let files=[{name:"GELISTIRME-TALIMATI.md",data:plComboText(D,{zip:true})}];
 D.res.order.forEach(m=>{files.push({name:`prompt-moduller/${m.id}.md`,data:plModMd(m,"../")});(m.images||[]).forEach((x,j)=>{let f=plImgName(m,j,x);if(f){let b=plBytes(x.src);if(b)files.push({name:f,data:b.u})}})});
 files.push({name:"prompt-kutuphanesi-secim.json",data:JSON.stringify(plPack(D.res.order.map(m=>m.id)),null,2)});
 plBlob(plZip(files),`${fslug()}-gelistirme-talimati.zip`);plToast(`${files.length} dosyalık zip indirildi.`)};

/* ---------- İçe / dışa aktarma ---------- */
function plClean(m){let o={id:m.id,source:m.builtin?"builtin":"custom",title:m.title,desc:m.desc,cat:m.cat,tags:m.tags||[],prompt:m.prompt,doc:m.doc||"",images:m.images||[],criteria:m.criteria||[],deps:m.deps||[],refs:m.refs||[],version:m.version,updated:m.updated||"",history:m.history||[]};return clone(o)}
function plPack(ids){let mods=ids?ids.map(plMod).filter(Boolean):plMods(),used=new Set(mods.map(m=>m.cat));return{format:PL_FMT,version:1,app:"WP-OnKe",exportedAt:new Date().toISOString(),categories:plCats().filter(c=>!c.builtin&&used.has(c.id)).map(c=>({id:c.id,name:c.name,desc:c.desc||""})),modules:mods.map(plClean)}}
window.plExport=(k,id)=>{let ids=k==="sel"?plSel().filter(x=>plMod(x)):k==="one"?[id]:null;if(ids&&!ids.length)return;let p=plPack(ids),name=k==="one"?`prompt-modulu-${id}.json`:k==="sel"?`prompt-modulleri-${ids.length}-secili-${today()}.json`:`prompt-kutuphanesi-${today()}.json`;
 plBlob(new Blob([JSON.stringify(p,null,2)],{type:"application/json"}),name);plToast(`${p.modules.length} modül dışa aktarıldı.`)};
function plSan(x){if(!x||typeof x!=="object")return null;const s=v=>typeof v==="string"?v:"",A=v=>Array.isArray(v)?v:[];let title=s(x.title).trim().slice(0,200);if(!title)return null;let id=plSlug(s(x.id)||title);if(!id)return null;
 return{id,title,desc:s(x.desc).slice(0,4000),cat:plSlug(s(x.cat))||"diger",tags:A(x.tags).map(t=>s(t).trim().replace(/^#/,"").slice(0,40)).filter(Boolean).slice(0,30),prompt:s(x.prompt).slice(0,50000),doc:s(x.doc).slice(0,500000),
  criteria:A(x.criteria).map(c=>s(c).trim()).filter(Boolean).slice(0,100),deps:[...new Set(A(x.deps).map(d=>plSlug(s(d))).filter(d=>d&&d!==id))],refs:A(x.refs).map(r=>({t:s(r&&r.t).slice(0,300),u:s(r&&r.u).trim()})).filter(r=>/^https?:\/\/\S+$/i.test(r.u)).slice(0,50),
  images:A(x.images).map((im,i)=>({id:s(im&&im.id).slice(0,60)||"img-"+(i+1),name:s(im&&im.name).replace(/[^\w.-]/g,"").slice(0,80),src:s(im&&im.src),alt:s(im&&im.alt).slice(0,500).trim()||"Referans görsel "+(i+1),caption:s(im&&im.caption).slice(0,500)})).filter(im=>PL_SRC_RE.test(im.src)).slice(0,30),
  version:PL_VER_RE.test(s(x.version))?s(x.version):"1.0.0",updated:/^\d{4}-\d{2}-\d{2}/.test(s(x.updated))?s(x.updated).slice(0,10):today(),
  history:A(x.history).slice(0,PL_HIST).map(h=>({version:PL_VER_RE.test(s(h&&h.version))?s(h.version):"",date:s(h&&h.date).slice(0,10),note:s(h&&h.note).slice(0,500),data:h&&h.data&&typeof h.data==="object"?plTextOnly(plSan(Object.assign({title:title},h.data))||{}):null})).filter(h=>h.version)}}
const FI2=document.createElement("input");FI2.type="file";FI2.accept=".json,application/json";FI2.hidden=true;document.body.appendChild(FI2);
window.plImportPick=()=>{FI2.value="";FI2.click()};
FI2.onchange=async()=>{let f=FI2.files[0];if(!f)return;if(f.size>60e6)return plToast("Dosya 60 MB'tan büyük.",1);try{plImportText(await f.text())}catch(e){plToast("Dosya okunamadı: "+(e.message||e),1)}};
window.plImportText=(txt,mode)=>{let d;try{d=JSON.parse(txt)}catch(e){plToast("Geçerli bir JSON dosyası değil.",1);return null}
 let raw=Array.isArray(d)?d:Array.isArray(d&&d.modules)?d.modules:(d&&d.title&&d.prompt!==undefined?[d]:null);if(!raw){plToast(d&&d.format==="web-project-configurator"?"Bu bir proje dosyası; üst şeritteki JSON İçe Aktar ile açın.":"Dosyada prompt modülü bulunamadı.",1);return null}
 let M=raw.map(plSan).filter(Boolean),bad=raw.length-M.length;if(!M.length){plToast("Dosyadaki modüllerin hiçbiri geçerli değil (başlık zorunlu).",1);return null}
 let exist=new Set(plMods().map(m=>m.id).concat(LIB.hidden)),conf=M.filter(m=>exist.has(m.id)||LIB.mods[m.id]);
 let over=mode!==undefined?mode:(conf.length?confirm(`${conf.length} modül kütüphanede zaten var (aynı kimlik): ${conf.slice(0,5).map(m=>m.title).join(", ")}${conf.length>5?"…":""}.\n\nTamam: üzerine yaz (eski sürüm geçmişe eklenir) · İptal: yalnız yeni modülleri ekle`):false);
 (Array.isArray(d&&d.categories)?d.categories:[]).forEach(c=>{let id=plSlug(c&&c.id),n=String(c&&c.name||"").trim().slice(0,60);if(id&&n&&!plCats().some(x=>x.id===id))LIB.cats.push({id,name:n,desc:String(c.desc||"").slice(0,160)})});
 let add=0,upd=0,skip=0;M.forEach(m=>{if(!plCats().some(c=>c.id===m.cat))LIB.cats.push({id:m.cat,name:m.cat.replace(/-/g," ").replace(/^./,c=>c.toLocaleUpperCase("tr")),desc:""});
  let cur=plMod(m.id)||(LIB.mods[m.id]?Object.assign({},LIB.mods[m.id],{id:m.id}):null);
  if(cur&&!over){skip++;return}
  if(cur&&JSON.stringify(plClean(Object.assign({},cur,{builtin:!!BI[m.id]})))===JSON.stringify(plClean(Object.assign({},m,{builtin:!!BI[m.id]})))){skip++;return}
  if(cur&&cur.version!==m.version&&!(m.history||[]).some(h=>h.version===cur.version))m.history=[{version:cur.version,date:cur.updated||today(),note:"İçe aktarmadan önceki sürüm",data:plTextOnly(cur)}].concat(m.history||[]).slice(0,PL_HIST);
  if(BI[m.id]&&!cur&&LIB.hidden.includes(m.id)){LIB.hidden=LIB.hidden.filter(x=>x!==m.id)}
  if(BI[m.id]&&JSON.stringify(plTextOnly(m))===JSON.stringify(plTextOnly(BI[m.id]))&&JSON.stringify(m.images)===JSON.stringify(BI[m.id].images)){delete LIB.over[m.id];LIB.hidden=LIB.hidden.filter(x=>x!==m.id)}else plStore(m);
  cur?upd++:add++});
 plSave();let msg=`${add} modül eklendi, ${upd} güncellendi${skip?`, ${skip} atlandı`:""}${bad?`, ${bad} geçersiz kayıt alınmadı`:""}.`;plToast(msg,!add&&!upd);plRender();return{add,upd,skip,bad}};

const PL_LOAD=plLoad();window.plReady=()=>PL_LOAD.then(()=>PL_Q);
window.plDebug={LIB:()=>LIB,mode:()=>LIB_MODE,PL,plMods,plMod,plResolve,plComboText:()=>plComboText(plComboData()),plMd,plSan,plPack,plModMd,plSel};
})();
