/* Yapılacaklar (2026-11-12, kullanıcı isteği: "yapılan seçimlerden oluşan bir todo list hazırla").
   Sayfa #todoPage (showPage("todo")), modül şeridinde "Yapılacaklar" (Kurallar'dan sonra), çekmecede #sideTodoBtn.
   Görevler verilmiş kararlardan türetilir (görünen + menüde olan + dolu: shown && navF && isset): Ortak Bilgiler, Kararlar
   (CLAUDE-TALIMATLARI.md'deki fazlara göre), Pazarlama, SEO Denetimi, Google, Meta, Yapay Zekâ. Çoklu seçimli kararda her seçenek
   ayrı alt görevdir. İşaretler state.todo = {done:{anahtar:{d:tarih,h:parmak izi}}} (yalnız işaret varken; anahtar alan kimliği ya da
   "alan|değer"); karar sonradan değişirse parmak izi tutmaz ve görev "Karar değişti" olur. Kurallar, Claude promptu, talimat
   dosyası ve ajan dosyaları değişmez; YAPILACAKLAR.md (todoMd) Dashboard › İndirmeler'de de var.
   Kaynak docs/v26/v26-todo.{js,css} → docs/v26/yapilacaklar_ekle.py */
(()=>{
const AREAS=[["common","Ortak Bilgiler"],["project","Kararlar"],["marketing","Pazarlama"],["audit","SEO Denetimi"],["google","Google Servisleri"],["meta","Meta Servisleri"],["ai","Yapay Zekâ"]],
 PH=[["Proje temeli ve mimari",["Başlangıç","Teknik Mimari","Sunucu & Altyapı"]],["Tasarım ve arayüz",["Tasarım & Arayüz"]],["İçerik ve yönetim",["İçerik & Yönetim"]],["İş modülleri",["İş Modülleri"]],["SEO ve görünürlük",["SEO & Görünürlük"]],["Güvenlik ve gizlilik",["Güvenlik & Gizlilik"]],["Performans, test ve geliştirme süreci",["Performans & Test","Geliştirme Süreci"]],["Yayın ve operasyon",["Yayın & Operasyon"]]],
 ICON="M10 6h10M10 12h10M10 18h10M3.5 6l1.5 1.5L7.5 5M3.5 12l1.5 1.5 2.5-2.5M3.5 18l1.5 1.5 2.5-2.5",
 TD={q:"",f:"all",a:"all"},
 day=()=>new Date().toLocaleDateString("sv-SE"),
 pname=()=>String(state.project_name||"").trim()||"Proje",
 clean=t=>String(t??"").replace(/\s*\(önerilen\)/g,"").trim(),
 cut=(t,n)=>{t=String(t||"").replace(/\s+/g," ").trim();return t.length>n?t.slice(0,n-1)+"…":t};
function fp(v){let s=String(v??""),h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0).toString(36)}
function rec(){let t=state.todo;return t&&typeof t==="object"&&t.done&&typeof t.done==="object"?t.done:{}}
function num(id,sec){let N=window.NAV_NUM;return N?(id?N.fld[id]:N.sec[sec])||"":""}
/* karar özeti: kısa, okunur değer */
function sum(f){let v=state[f.id];try{
 if(f.type==="multiselect")return v.map(x=>clean(lab(f,x))).join(", ");
 if(f.type==="boolean")return v?"Evet":"Hayır";
 if(f.type==="select")return clean(lab(f,v));
 if(f.type==="accounts"){let L=accList(f);return L.length+" kayıt: "+L.slice(0,3).map(x=>x[0]).join(", ")+(L.length>3?"…":"")}
 if(f.type==="hours")return hrText(f);
 if(f.type==="palette")return "Renk paleti ve kontrast denetimi";
 if(f.type==="panels"){let p=state.panelArch;return (p&&p.panels?p.panels.length:0)+" panel"}
 return cut(v,160)}catch(e){return cut(rule(f),160)}}
function agents(f){try{return faGet(f).map(agGet).filter(Boolean)}catch(e){return []}}
/* görev listesi: alan → bölüm → görev (alt görevler) */
function build(){let D=rec(),out=AREAS.map(([a,t])=>({a,t,n:(window.MT_NUM||{})[a]||"",G:[]})),by={};out.forEach(x=>by[x.a]=x);
 let secs={};
 F.forEach(f=>{let s=SI[f.section];if(!s||!navF(f)||!shown(f)||!isset(f))return;let a=AREA(s),A=by[a];if(!A)return;
  let r=rule(f)||"",it={f,s,k:f.id,num:num(f.id),t:clean(f.label),sum:sum(f),r,ag:agents(f),subs:[]},v=state[f.id];
  if(f.type==="multiselect"&&Array.isArray(v)&&v.length>1)it.subs=v.map(x=>{let o=opts(f).find(o=>o.value===x)||{},k=f.id+"|"+x,h=fp(x+"\u0001"+(o.ruleDetail||"")),d=D[k];return {k,h,t:clean(o.label||x),r:o.ruleDetail||"",st:d?(d.h===h?"done":"changed"):"open",d:d&&d.d}});
  else{it.h=fp(r);let d=D[it.k];it.st=d?(d.h===it.h?"done":"changed"):"open";it.d=d&&d.d}
  if(it.subs.length){let S=it.subs.map(x=>x.st);it.st=S.every(x=>x==="done")?"done":S.some(x=>x==="changed")?"changed":"open"}
  let key=a+":"+s.id;if(!secs[key]){secs[key]={s,num:num(null,s.id),I:[]};
   let gname=a==="project"?((PH.find(p=>p[1].includes(s.group))||["Diğer proje kararları"])[0]):(a==="marketing"?s.group:"");
   let g=A.G.find(x=>x.name===gname);if(!g){g={name:gname,S:[]};A.G.push(g)}g.S.push(secs[key])}
  secs[key].I.push(it)});
 out.forEach(A=>{if(A.a==="project")A.G.sort((x,y)=>idx(x.name)-idx(y.name))});
 return out.filter(A=>A.G.length)}
const idx=n=>{let i=PH.findIndex(p=>p[0]===n);return i<0?99:i};
function leaves(it){return it.subs.length?it.subs:[it]}
function stats(L){let a=0,d=0,c=0;L.forEach(it=>leaves(it).forEach(x=>{a++;if(x.st==="done")d++;else if(x.st==="changed")c++}));return {a,d,c,o:a-d,p:a?Math.round(d/a*100):0}}
function allItems(T){let L=[];T.forEach(A=>A.G.forEach(g=>g.S.forEach(s=>L.push(...s.I))));return L}
function areaItems(A){let L=[];A.G.forEach(g=>g.S.forEach(s=>L.push(...s.I)));return L}
/* filtre */
function hay(it,s){return norm([it.num,it.t,it.sum,it.r,s.name,s.code,...it.subs.map(x=>x.t+" "+x.r),...it.ag.map(a=>a.name)].join(" "))}
function pass(it,s){if(TD.f==="open"&&it.st==="done")return false;if(TD.f==="done"&&it.st!=="done")return false;if(TD.f==="changed"&&it.st!=="changed")return false;
 let q=norm(TD.q);return !q||hit(hay(it,s),q)}

/* ---------- Sayfa ---------- */
const PG=document.createElement("section");PG.id="todoPage";PG.setAttribute("aria-label","Yapılacaklar");
configPage.parentNode.insertBefore(PG,configPage);
const isOn=()=>PG.classList.contains("active");
function nav(){let rail=document.getElementById("modRail");if(rail&&!rail.querySelector('[data-mod="todo"]')){let b=document.createElement("button");b.type="button";b.className="mrBtn";b.dataset.mod="todo";b.title="Yapılacaklar — kararlardan oluşan görev listesi";b.setAttribute("aria-label","Yapılacaklar");b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="${ICON}"/></svg><span>Yapılacaklar</span>`;b.onclick=()=>window.todoGo();rail.insertBefore(b,rail.querySelector('[data-mod="library"]')||rail.querySelector('[data-mod="docs"]'))}
 let ref=document.getElementById("sideLibBtn")||document.getElementById("sideDocsBtn");if(ref&&!document.getElementById("sideTodoBtn")){let s=document.createElement("button");s.type="button";s.id="sideTodoBtn";s.innerHTML="☑ &nbsp; Yapılacaklar";s.onclick=()=>window.todoGo();ref.parentNode.insertBefore(s,ref)}}
function sync(){let on=isOn(),rail=document.getElementById("modRail");if(rail)rail.querySelectorAll(".mrBtn").forEach(b=>{if(on){let a=b.dataset.mod==="todo";b.classList.toggle("active",a);b.toggleAttribute("aria-current",a)}else if(b.dataset.mod==="todo"){b.classList.remove("active");b.removeAttribute("aria-current")}});
 if(on)document.documentElement.classList.add("v26NoSide");let s=document.getElementById("sideTodoBtn");if(s){s.classList.toggle("active",on);s.toggleAttribute("aria-current",on)}}
const _sp=showPage;
showPage=function(p){if(p==="todo"){_sp("config");configPage.classList.add("hidden");PG.classList.add("active");render();window.scrollTo(0,0);sync();return}PG.classList.remove("active");_sp(p);sync()};
const _ab=areaBtn;areaBtn=function(){_ab();if(isOn())sync()};
window.todoGo=()=>{if(typeof closeNav==="function")closeNav();showPage("todo")};

function chip(k,t,n,cur,attr){return `<button type="button" class="tdChip${cur?" on":""}" data-td-${attr}="${k}" aria-pressed="${cur}">${E(t)}${n!=null?` <span>${n}</span>`:""}</button>`}
function render(){if(!isOn())return;let T=build(),L=allItems(T),S=stats(L);
 if(!L.length){PG.innerHTML=`<div class="tdHead"><div><p class="tdEye">GÖREV LİSTESİ</p><h1>Yapılacaklar</h1><p class="tdLead">Henüz karar verilmedi. Kararlar, Ortak Bilgiler ve Pazarlama menülerinde yaptığınız her seçim burada uygulanacak bir görev olur.</p></div></div><div class="tdEmpty"><button type="button" class="btn primary" onclick="goArea('project')">Kararlara git</button></div>`;return}
 PG.innerHTML=`<div class="tdHead"><div><p class="tdEye">GÖREV LİSTESİ</p><h1>Yapılacaklar</h1><p class="tdLead">Verdiğiniz ${L.length} karardan oluşan uygulama listesi. Uygulanan görevi işaretleyin; karar sonradan değişirse görev “Karar değişti” olarak yeniden açılır. Liste kararlarla birlikte güncellenir.</p></div>
 <div class="tdTools"><button type="button" class="btn" data-td-act="copy">Kopyala</button><button type="button" class="btn primary" data-td-act="md">YAPILACAKLAR.md indir</button></div></div>
 <div class="tdSum" role="group" aria-label="İlerleme"><div class="tdBar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${S.p}" aria-label="Tamamlanan görevler"><i style="width:${S.p}%"></i></div><p><b>${S.d}/${S.a} - %${S.p}</b> tamamlandı · ${S.o} açık${S.c?` · <span class="tdWarn">${S.c} karar değişti</span>`:""}</p>
 <div class="tdAreas">${T.map(A=>{let s=stats(areaItems(A));return `<button type="button" class="tdArea${TD.a===A.a?" on":""}${s.a&&s.d===s.a?" done":""}" data-td-area="${A.a}" aria-pressed="${TD.a===A.a}"><b>${A.n?A.n+". ":""}${E(A.t)}</b><span>${s.d}/${s.a} - %${s.p}</span></button>`}).join("")}</div></div>
 <div class="tdBarTools"><label class="tdSearch"><span class="sr">Görevlerde ara</span><input type="search" id="tdQ" placeholder="Görevlerde ara (karar, seçim, kural, ajan)" value="${E(TD.q)}"></label>
 <div class="tdChips" role="group" aria-label="Duruma göre süz">${chip("all","Tümü",S.a,TD.f==="all","f")}${chip("open","Açık",S.o,TD.f==="open","f")}${chip("done","Tamamlanan",S.d,TD.f==="done","f")}${S.c?chip("changed","Karar değişti",S.c,TD.f==="changed","f"):""}${TD.a!=="all"?chip("all","Bütün menüler",null,false,"area"):""}</div></div>
 <div id="tdList">${list(T)}</div>
 ${Object.keys(rec()).length?`<p class="tdFoot"><button type="button" class="linkBtn" data-td-act="reset">Bütün işaretleri kaldır</button></p>`:""}`}
function list(T){let h="";T.forEach(A=>{if(TD.a!=="all"&&TD.a!==A.a)return;let s=stats(areaItems(A)),body="";
 A.G.forEach(g=>{let gb="";g.S.forEach(x=>{let I=x.I.filter(it=>pass(it,x.s));if(!I.length)return;let ss=stats(x.I);
   gb+=`<div class="tdSec"><h4><span class="tdNum">${E(x.num||x.s.code)}</span> ${E(x.s.name)} <small>${ss.d}/${ss.a}</small> <button type="button" class="linkBtn" data-td-sec="${E(x.s.id)}">Bölüme git</button></h4><ul>${I.map(item).join("")}</ul></div>`});
  if(gb)body+=g.name?`<div class="tdGroup"><h3>${A.a==="project"?"Faz: ":""}${E(g.name)}</h3>${gb}</div>`:gb});
 if(body)h+=`<section class="tdAreaBox"><h2>${A.n?`<span class="tdNum">${A.n}.</span> `:""}${E(A.t)} <small>${s.d}/${s.a} - %${s.p}</small></h2>${body}</section>`});
 return h||`<p class="tdNone">Bu süzgece uyan görev yok. <button type="button" class="linkBtn" data-td-act="clear">Süzgeci temizle</button></p>`}
function box(k,st,lbl){return `<input type="checkbox" data-td-k="${E(k)}"${st==="done"?" checked":""} aria-label="${E(lbl)}">`}
function item(it){let id="td-"+it.k.replace(/[^a-z0-9_-]/gi,"_"),off=it.ag.filter(a=>!a.on).length,
 ag=it.ag.length?`<p class="tdAg">Sorumlu ajan: ${it.ag.map(a=>`<span${a.on?"":` class="off" title="Projede değil"`}>${E(a.name)}</span>`).join(", ")}${off?" <em>(soluk olanlar projede değil)</em>":""}</p>`:"",
 badge=it.st==="changed"?`<span class="tdBadge">Karar değişti · yeniden kontrol edin</span>`:it.st==="done"&&it.d?`<span class="tdDate">${E(it.d)}</span>`:"",
 subs=it.subs.length?`<ul class="tdSubs">${it.subs.map(x=>`<li class="tdSub ${x.st}"><label>${box(x.k,x.st,it.t+": "+x.t)}<span>${E(x.t)}</span>${x.st==="changed"?`<span class="tdBadge">değişti</span>`:""}</label>${x.r?`<p class="tdSubR">${E(cut(x.r,320))}</p>`:""}</li>`).join("")}</ul>`:"";
 let main=it.subs.length?`<input type="checkbox" data-td-all="${E(it.k)}"${it.st==="done"?" checked":""} aria-label="${E(it.t)} — bütün seçenekler">`:box(it.k,it.st,it.t);
 return `<li class="tdIt ${it.st}" id="${id}"><div class="tdRow"><label class="tdMain">${main}<span class="tdTx"><b>${it.num?`<span class="tdNum">${E(it.num)}</span> `:""}${E(it.t)}</b><span class="tdVal">${E(it.sum)}</span></span></label>${badge}<button type="button" class="linkBtn tdGo" data-td-go="${E(it.f.section)}|${E(it.f.id)}">Karara git</button></div>
 ${subs}<details class="tdMore"><summary>Kural ve sorumlu</summary><p class="tdRule">${E(it.r)}</p>${ag}</details></li>`}

/* ---------- İşlemler ---------- */
function setDone(keys,on){if(!requireProject())return false;let t=state.todo&&typeof state.todo==="object"&&state.todo.done?state.todo:{done:{}};
 keys.forEach(([k,h])=>{if(on)t.done[k]={d:day(),h};else delete t.done[k]});
 if(Object.keys(t.done).length)state.todo=t;else delete state.todo;save();return true}
function findIt(k){let L=allItems(build());for(let it of L){if(it.k===k)return {it};for(let x of it.subs)if(x.k===k)return {it,x}}return null}
function redraw(focusSel){let y=window.scrollY;render();window.scrollTo(0,y);if(focusSel){let el=PG.querySelector(focusSel);if(el)el.focus()}}
PG.addEventListener("change",e=>{let c=e.target;if(c.matches("input[data-td-k]")){let r=findIt(c.dataset.tdK);if(!r){redraw();return}let x=r.x||r.it;if(!setDone([[x.k,x.h]],c.checked))c.checked=!c.checked;else redraw(`input[data-td-k="${CSS.escape(x.k)}"]`)}
 else if(c.matches("input[data-td-all]")){let r=findIt(c.dataset.tdAll);if(!r){redraw();return}if(!setDone(r.it.subs.map(x=>[x.k,x.h]),c.checked))c.checked=!c.checked;else redraw(`input[data-td-all="${CSS.escape(r.it.k)}"]`)}});
PG.addEventListener("input",e=>{if(e.target.id==="tdQ"){TD.q=e.target.value;let l=document.getElementById("tdList");if(l)l.innerHTML=list(build())}});
PG.addEventListener("keydown",e=>{if(e.target.id==="tdQ"&&e.key==="Escape"&&TD.q){TD.q="";e.target.value="";let l=document.getElementById("tdList");if(l)l.innerHTML=list(build())}});
PG.addEventListener("click",e=>{let b=e.target.closest("button");if(!b||!PG.contains(b))return;let d=b.dataset;
 if(d.tdF){TD.f=d.tdF;redraw()}
 else if(d.tdArea){TD.a=TD.a===d.tdArea?"all":d.tdArea;redraw()}
 else if(d.tdSec)goToSection(d.tdSec)
 else if(d.tdGo){let [s,f]=d.tdGo.split("|");goToField(s,f)}
 else if(d.tdAct==="md")mkSave(todoMd(),"YAPILACAKLAR-"+((typeof exSlug==="function"&&exSlug(pname()))||"proje")+".md","text/markdown;charset=utf-8");
 else if(d.tdAct==="copy"){let t=todoMd();(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>note(b,"Kopyalandı"),()=>note(b,"Kopyalanamadı"))}
 else if(d.tdAct==="clear"){TD.q="";TD.f="all";TD.a="all";redraw()}
 else if(d.tdAct==="reset"){if(!requireProject())return;if(confirm("Bütün görevlerin işaretleri kaldırılsın mı? Kararlar değişmez.")){delete state.todo;save();redraw()}}});
function goToSection(id){showPage("config");if(typeof closeNav==="function")closeNav();active=id;openSection=id;activeFieldId=null;showAll=false;renderConfig();window.scrollTo(0,0)}
function note(b,t){let o=b.textContent;b.textContent=t;setTimeout(()=>{b.textContent=o},1400)}

/* ---------- YAPILACAKLAR.md ---------- */
function todoMd(){let T=build(),L=allItems(T),S=stats(L),ck=st=>st==="done"?"[x]":"[ ]",md=`# ${pname()} — Yapılacaklar\n\n> Cortex Configurator ile üretildi · ${day()} · ${S.a} görev · ${S.d} tamamlandı (%${S.p})${S.c?` · ${S.c} görevin kararı işaretlendikten sonra değişti`:""}.\n> Görevler projede verilen kararlardan türetildi. Ayrıntılı kurallar CLAUDE-TALIMATLARI.md'dedir; bir görevi uyguladıktan sonra işaretleyin.\n`;
 if(!L.length)return md+"\nHenüz karar verilmedi.\n";
 T.forEach(A=>{let s=stats(areaItems(A));md+=`\n## ${A.n?A.n+". ":""}${A.t} (${s.d}/${s.a})\n`;
  A.G.forEach(g=>{if(g.name)md+=`\n### ${A.a==="project"?"Faz: ":""}${g.name}\n`;
   g.S.forEach(x=>{md+=`\n${g.name?"####":"###"} ${x.num||x.s.code} ${x.s.name}\n\n`;
    x.I.forEach(it=>{md+=`- ${ck(it.st)} **${it.num?it.num+" ":""}${it.t}** — ${it.sum}${it.st==="changed"?" _(karar değişti, yeniden kontrol edin)_":""}\n`;
     it.subs.forEach(o=>{md+=`  - ${ck(o.st)} ${o.t}${o.r?` — ${o.r}`:""}\n`});
     if(!it.subs.length&&it.r)md+=`  - Kural: ${it.r}\n`;
     if(it.ag.length)md+=`  - Sorumlu ajan: ${it.ag.map(a=>a.name+(a.on?"":" (projede değil)")).join(", ")}\n`})})})});
 return md}
window.todoMd=todoMd;window.todoStats=()=>stats(allItems(build()));

nav();
const _rp=typeof renderProgress==="function"?renderProgress:null;
if(_rp)renderProgress=function(){let r=_rp.apply(this,arguments);if(isOn()&&!PG.contains(document.activeElement))render();return r};
})();
