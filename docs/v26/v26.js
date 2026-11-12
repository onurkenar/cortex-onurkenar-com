<script id="v26-ux-refresh-js">
/* V26 UI/UX yenileme — ayrıntı: v26-ux-refresh stil bloğundaki not. Var olan işlevler sarmalanır; seçim, kural, kayıt ve dışa aktarma mantığına dokunulmaz. */
(function(){
const V26_NG_KEY="web-project-configurator-navgroups",V26_META_KEY="web-project-configurator-optmeta",V26_SS_KEY="web-project-configurator-start-later";
const ls={get(k){try{return localStorage.getItem(k)}catch(e){return null}},set(k,v){try{localStorage.setItem(k,v)}catch(e){}}};
const ss={get(k){try{return sessionStorage.getItem(k)}catch(e){return null}},set(k,v){try{sessionStorage.setItem(k,v)}catch(e){}}};
let NG={};try{NG=JSON.parse(ls.get(V26_NG_KEY)||"{}")||{}}catch(e){NG={}}
let WHY_OPEN=false;const OPT_Q={},OPT_G={};
const svg=d=>`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="${d}"/></svg>`;
const ICON={
 overview:"M4 13h6V4H4v9Zm10 7h6v-9h-6v9ZM4 20h6v-4H4v4ZM14 4v4h6V4h-6Z",
 config:"M4 6h10M18 6h2M4 12h4M12 12h8M4 18h12M14 4v4M8 10v4M16 16v4",
 rules:"M9 6h11M9 12h11M9 18h11M4 6l1 1 2-2M4 12l1 1 2-2M4 18l1 1 2-2",
 agents:"M16 19v-1a4 4 0 0 0-4-4H7a4 4 0 0 0-4 4v1M9.5 10a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7ZM21 19v-1a4 4 0 0 0-3-3.9M15.5 3.2a3.5 3.5 0 0 1 0 6.6",
 marketing:"M3 11v2a1 1 0 0 0 1 1h3l6 4V6L7 10H4a1 1 0 0 0-1 1ZM17 8a5 5 0 0 1 0 8",
 audit:"M11 18a7 7 0 1 0 0-14 7 7 0 0 0 0 14ZM20 20l-4-4M8 13l2-2 2 1 2-3",
 common:"M12 3c4.4 0 8 1.3 8 3s-3.6 3-8 3-8-1.3-8-3 3.6-3 8-3ZM4 6v6c0 1.7 3.6 3 8 3s8-1.3 8-3V6M4 12v6c0 1.7 3.6 3 8 3s8-1.3 8-3v-6",
 docs:"M4 5a2 2 0 0 1 2-2h12v16H6a2 2 0 0 0-2 2V5ZM4 19a2 2 0 0 1 2-2h12M8 7h6"};
const MODS=[["overview","Dashboard","v26Overview()"],["common","Ortak Bilgiler","goArea('common')"],["config","Kararlar","goArea('project')"],["marketing","Pazarlama","goArea('marketing')"],["audit","SEO Denetimi","goArea('audit')"],["rules","Kurallar","showPage('rules')"],["docs","Doküman","showPage('docs')"],["agents","Ajanlar","showPage('agents')"]];

/* 1. Modül şeridi */
const rail=document.createElement("nav");rail.id="modRail";rail.setAttribute("aria-label","Modüller");
rail.innerHTML=`<div class="mrLogo" aria-hidden="true">W</div>`+MODS.map(m=>`<button type="button" class="mrBtn" data-mod="${m[0]}" onclick="${m[2]}">${svg(ICON[m[0]])}<span>${m[1]}</span></button>`).join("");
document.body.insertBefore(rail,document.body.firstChild);
/* Tema düğmesi şeridin sol alt köşesinde (kullanıcı isteği 2026-11-07); üst şeritteki #themeBtn > 900 px'te gizli, tıklama ona aktarılır (≤ 900 px'te ⋯ menüsünde) */
{let sp=document.createElement("div");sp.className="mrSep";sp.setAttribute("aria-hidden","true");rail.appendChild(sp);let tb=document.createElement("button");tb.type="button";tb.className="mrBtn mrTheme";tb.id="mrThemeBtn";rail.appendChild(tb);let sync=()=>{let dk=document.documentElement.dataset.theme==="dark";tb.innerHTML=svg(dk?"M12 4V2M12 22v-2M4 12H2M22 12h-2M5.6 5.6 4.2 4.2M19.8 19.8l-1.4-1.4M5.6 18.4l-1.4 1.4M19.8 4.2l-1.4 1.4M12 17a5 5 0 1 0 0-10 5 5 0 0 0 0 10Z":"M20 14.5A8 8 0 0 1 9.5 4a8 8 0 1 0 10.5 10.5Z")+`<span>${dk?"Açık tema":"Koyu tema"}</span>`;tb.setAttribute("aria-label",dk?"Açık temaya geç":"Koyu temaya geç");tb.title=tb.getAttribute("aria-label")};tb.onclick=()=>{themeBtn.click();sync()};sync();new MutationObserver(sync).observe(document.documentElement,{attributes:true,attributeFilter:["data-theme"]})}
/* Ajanlar en altta (kullanıcı isteği 2026-11-07): şeritte Doküman'dan sonra, çekmecenin alt menüsünde Dokümantasyon'dan sonra */
{let sf=document.querySelector(".sideFooter"),ab=document.getElementById("sideAgentsBtn");if(sf&&ab)sf.appendChild(ab)}
function railCur(){let o=document.getElementById("overviewPage");if(o&&o.classList.contains("active"))return"overview";if(rulesPage.classList.contains("active"))return"rules";if(agentsPage.classList.contains("active"))return"agents";if(docsPage.classList.contains("active"))return"docs";let a=curArea();return a==="project"?"config":a}
/* 2026-11-07 kullanıcı isteği: Kurallar, Doküman ve Ajanlar sayfalarında karar menüsü (kenar çubuğu) görünmez — html.v26NoSide */
function railSync(){let c=railCur();document.documentElement.classList.toggle("v26NoSide",c==="overview"||c==="rules"||c==="docs"||c==="agents");rail.querySelectorAll(".mrBtn").forEach(b=>{let on=b.dataset.mod===c;b.classList.toggle("active",on);b.toggleAttribute("aria-current",on)})}

/* 2. Dashboard sayfası (2026-11-12: menü adı "Özet" → "Dashboard", kullanıcı isteği; açıkken karar menüsü gizli — v26NoSide) */
const ov=document.createElement("section");ov.id="overviewPage";ov.setAttribute("aria-label","Proje özeti");
configPage.parentNode.insertBefore(ov,configPage);
const _showPage=showPage;
showPage=function(p){if(p==="overview"){_showPage("config");configPage.classList.add("hidden");ov.classList.add("active");renderOverview();scrollTo(0,0);railSync();return}ov.classList.remove("active");_showPage(p);railSync()};
window.v26Overview=function(){closeNav();showPage("overview")};
const _areaBtn=areaBtn;areaBtn=function(){_areaBtn();railSync()};
function areaFields(a){return F.filter(f=>shown(f)&&navF(f)&&AREA(SI[f.section])===a)}
function nextField(a){let V=areaFields(a);return V.find(f=>!isset(f))||null}
/* 2026-11-07: Proje kartı — proje adı ve proje dosyası (oluştur / aç / içe aktar / bağlantıyı kaldır) karar menülerinden bağımsız, Özet sayfasının başında */
function pnCard(){let r=projectReady();return `<section class="ovProject${r?"":" need"}" aria-labelledby="pnTitle"><div class="ovPHead"><b class="k" id="pnTitle">PROJE</b><span class="ovPState">${r?"Proje hazır":"Proje başlatılmadı"}</span></div><label class="ovPLabel" for="pnInput">Proje Adı <span class="req">*</span></label><p class="ovPHelp">${E((FI.project_name||{}).explanation||"")}</p><input class="control" id="pnInput" autocomplete="off" value="${E(state.project_name||"")}" placeholder="${E((FI.project_name||{}).placeholder||"")}" oninput="pnSet(this.value)">${r?"":'<p class="lockHint">Kararları işaretleyebilmek için önce proje adını yazıp aşağıdan proje dosyasını oluşturun ya da kayıtlı proje dosyanızı açın (proje adı dosyadan gelir). Seçimleriniz bu dosyaya kaydedilir.</p>'}<div id="projectFileBox" class="projectFile" aria-live="polite"></div></section>`}
const _renderFileBox=renderFileBox;renderFileBox=function(){_renderFileBox();let c=document.querySelector("#overviewPage .ovProject");if(c){let r=projectReady();c.classList.toggle("need",!r);let st=c.querySelector(".ovPState");if(st)st.textContent=r?"Proje hazır":"Proje başlatılmadı"}};
window.pnSet=function(v){state.project_name=v;save();renderRules();renderProgress();renderFileBox();let h=document.querySelector("#overviewPage .ovTxt h1");if(h)h.textContent=String(v).trim()||"Adsız proje";let st=document.querySelector(".ovPState");if(st)st.textContent=projectReady()?"Proje hazır":"Proje başlatılmadı"};
function renderOverview(){
 let V=areaFields("project"),n=V.filter(isset).length,t=V.length,p=t?Math.round(n/t*100):0,name=String(state.project_name||"").trim(),nx=nextField("project"),req=V.filter(f=>f.required&&!isset(f)),C=2*Math.PI*54,dash=(C*p/100).toFixed(1);
 let groups=[];S.filter(s=>AREA(s)==="project").forEach(s=>{let g=groups[groups.length-1];if(!g||g.t!==(s.group||""))groups.push(g={t:s.group||"",list:[]});g.list.push(s)});
 let gcard=(g,i)=>{let fs=V.filter(f=>g.list.some(s=>s.id===f.section)),d=fs.filter(isset).length,first=g.list.find(s=>fs.some(f=>f.section===s.id&&!isset(f)))||g.list[0],nm=g.list.map(s=>s.name),desc=nm.slice(0,4).join(", ")+(nm.length>4?` ve ${nm.length-4} bölüm daha`:"");return `<button type="button" class="ovCard${d?" on":""}" onclick="goStep('${E(first.id)}')"><span class="t"><span class="no">${i+1}</span>${E(g.t||"Proje")}</span><span class="d">${E(desc)}</span><span class="m"><span>${d} / ${fs.length} karar</span><span>${d===fs.length&&fs.length?"Tamamlandı":d?"Devam ediyor":"Başlanmadı"}</span></span><span class="ovBar"><i style="width:${fs.length?Math.round(d/fs.length*100):0}%"></i></span></button>`};
 let ap=a=>{let X=areaFields(a);return [X.filter(isset).length,X.length]},mk=ap("marketing"),au=ap("audit"),oc=ap("common"),rc=F.filter(f=>shown(f)&&isset(f)&&!auF(f)).length;
 let mod=(t,d,cta,fn)=>`<button type="button" class="ovCard" onclick="${fn}"><span class="t">${E(t)}</span><span class="d">${E(d)}</span><span class="go">${E(cta)} →</span></button>`;
 ov.innerHTML=`<div class="intro"><div class="eyebrow">DASHBOARD</div></div>
 ${pnCard()}
 <div class="ovTop"><div class="ovHero"><div class="ovRing"><svg width="128" height="128" viewBox="0 0 128 128" role="img" aria-label="Proje kararlarının yüzde ${p}'i verildi"><circle class="trk" cx="64" cy="64" r="54" fill="none" stroke="#eef0f3" stroke-width="12"/><circle class="val" cx="64" cy="64" r="54" fill="none" stroke="#2453d6" stroke-width="12" stroke-linecap="round" stroke-dasharray="${dash} ${C.toFixed(1)}" transform="rotate(-90 64 64)"/></svg><div><b>%${p}</b><span>${n} / ${t}</span></div></div>
 <div class="ovTxt"><h1>${E(name||"Adsız proje")}</h1><p>${n?`Proje yapılandırmasında ${n} karar verildi.`:"Henüz proje kararı verilmedi."} ${nx?`Sıradaki karar: <b>${E(SI[nx.section].name)} › ${E(nx.label)}</b>.`:"Bütün proje kararları verildi."}</p>
 <div class="ovBtns">${nx?`<button type="button" class="btn dark" onclick="goToField('${E(nx.section)}','${E(nx.id)}')">${n?"Kaldığın yerden devam et →":"Kararlara başla →"}</button><button type="button" class="btn" onclick="goStep('${E(nx.section)}')">Bölüm rehberini oku</button>`:`<button type="button" class="btn dark" onclick="showPage('rules')">Proje Kurallarını gör →</button>`}</div></div></div>
 <div class="ovSide">${req.length?`<div class="ovWarn"><b class="k">EKSİK ZORUNLU KARARLAR</b><span class="n">${req.length}</span><ul>${req.slice(0,6).map(f=>`<li><button type="button" onclick="goToField('${E(f.section)}','${E(f.id)}')">${E(SI[f.section].name)} › ${E(f.label)}</button></li>`).join("")}</ul>${req.length>6?`<span>ve ${req.length-6} karar daha</span>`:""}</div>`:`<div class="ovBox"><b class="k">ZORUNLU KARARLAR</b><span>Bütün zorunlu proje kararları verildi.</span></div>`}
 <div class="ovBox"><b class="k">ORTAK BİLGİLER</b><span>${oc[0]} / ${oc[1]} bilgi girildi. Bu bilgiler ilgili bölümlerde yeniden sorulmadan kullanılır.</span><button type="button" class="lk" onclick="goArea('common')">Ortak Bilgilere git →</button></div></div></div>
 <div class="ovH2"><h2>Proje yapılandırması · ${groups.length} aşama</h2><span>${S.filter(s=>AREA(s)==="project").length} bölüm, ${t} karar</span></div>
 <div class="ovGrid">${groups.map(gcard).join("")}</div>
 <div class="ovH2"><h2>Diğer modüller ve çıktılar</h2></div>
 <div class="ovGrid">${mod("Proje Kuralları",`Kararlarınızdan oluşan kural seti ve Claude promptu. Şu an ${rc} kural.`,"Kuralları incele","showPage('rules')")}${mod("Ajanlar","Ajan yapısı, kurullar, komiteler, skill dizini, MCP bağlantıları ve kurulum kılavuzu.","Ajanlara git","showPage('agents')")}${mod("Pazarlama Kararları",`${mk[0]} / ${mk[1]} karar verildi.`,"Pazarlamaya git","goArea('marketing')")}${mod("SEO Denetimi",`${au[0]} / ${au[1]} karar verildi.`,"Denetimi planla","goArea('audit')")}${mod("JSON dosyaları","Proje Kararları, Pazarlama Kararları ve SEO Denetimi ayrı dosyalar olarak indirilir.","Dosyaları indir","exportBtn.click()")}</div>`;
 renderFileBox();
}

/* 3. Menü grupları: katlanır başlık + ilerleme */
const _renderSideNav=renderSideNav;
renderSideNav=function(){_renderSideNav();
 sideNav.querySelectorAll(".navGroup").forEach(g=>{let tt=g.querySelector(".navGroupTitle");if(!tt||(!g.hidden&&getComputedStyle(tt).display==="none")||g.dataset.area==="common")return;let t=tt.textContent.trim(),a=g.dataset.area,secs=[...g.querySelectorAll(".menuSection")].map(x=>x.dataset.section),fs=F.filter(f=>shown(f)&&navF(f)&&secs.includes(f.section)),d=fs.filter(isset).length,key=a+"|"+t,hasOpen=secs.includes(openSection)||secs.includes(active),open=hasOpen||NG[key]===true||(NG[key]===undefined&&secs.length<=1);
  g.classList.toggle("ngClosed",!open);tt.classList.add("v26Hidden");
  let h=document.createElement("button");h.type="button";h.className="ngHead";h.setAttribute("aria-expanded",String(open));h.dataset.key=key;h.innerHTML=`<span class="ngT">${E(t.toLocaleUpperCase("tr"))}</span><span class="ngN">${d}/${fs.length}</span><svg class="ngChev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m9 6 6 6-6 6"/></svg>`;
  h.onclick=()=>{let o=g.classList.contains("ngClosed");g.classList.toggle("ngClosed",!o);h.setAttribute("aria-expanded",String(o));NG[key]=o;ls.set(V26_NG_KEY,JSON.stringify(NG))};
  let bar=document.createElement("span");bar.className="ngBar";bar.setAttribute("aria-hidden","true");bar.innerHTML=`<i style="width:${fs.length?Math.round(d/fs.length*100):0}%"></i>`;
  tt.after(h,bar)});
};

/* 4. Proje başlatma ekranı (kilit kutusunun yerine) */
const sc=document.createElement("div");sc.className="ssWrap";sc.id="startScreen";sc.hidden=true;
sc.innerHTML=`<div class="ssBox" role="dialog" aria-modal="true" aria-labelledby="ssT"><button type="button" class="ssX" aria-label="Kapat" onclick="ssClose()">✕</button>
<div class="ssHead"><div class="ssLogo" aria-hidden="true">W</div><h2 id="ssT">Bir projeyle başlayın</h2><p>Kararlarınız bir proje dosyasına kaydedilir. Yeni bir proje oluşturun ya da daha önce kaydettiğiniz proje dosyasını (.json) açın; proje adı dosyadan gelir.</p></div>
<div class="ssGrid"><div class="ssCard main"><span class="ssK">YENİ PROJE</span><label for="ssName">Proje adı</label><input id="ssName" type="text" autocomplete="off" placeholder="Örn. Kurumsal Web Projesi"><p id="ssNote">Adı kısa ve marka adıyla uyumlu tutun; belgelerde, yönetim panelinde ve Claude promptunda aynı yazım kullanılır.</p><button type="button" class="btn dark" onclick="ssCreate()">Proje dosyasını oluştur</button></div>
<div class="ssCard"><span class="ssK">KAYITLI PROJE</span><p>Daha önce kaydettiğiniz proje dosyasını açın. Proje adı ve bütün seçimler dosyadan gelir; bundan sonraki her seçim bu dosyaya otomatik kaydedilir.</p><button type="button" class="btn" onclick="ssOpenFile()">Proje dosyasını aç</button></div></div>
<div class="ssFoot"><span><i>1</i>Her seçim otomatik kaydedilir</span><span><i>2</i>Kararlar kurala dönüşür</span><span><i>3</i>Claude promptunu kopyalayın</span><button type="button" class="ssLater" onclick="ssLater()">Önce kararlara göz at</button></div></div>`;
document.body.appendChild(sc);
let ssBack=null;
window.ssOpen=function(){if(projectReady())return;ssBack=document.activeElement;closeNav();sc.hidden=false;let i=document.getElementById("ssName");i.value=String(state.project_name||"");i.removeAttribute("aria-invalid");setTimeout(()=>i.focus(),30)};
window.ssClose=function(){sc.hidden=true;if(ssBack&&ssBack.focus)ssBack.focus({preventScroll:true})};
window.ssLater=function(){ss.set(V26_SS_KEY,"1");ssClose()};
window.ssOpenFile=function(){ssClose();pfImport()};
window.ssCreate=function(){let i=document.getElementById("ssName"),v=i.value.trim();if(!v){i.setAttribute("aria-invalid","true");document.getElementById("ssNote").textContent="Devam etmek için proje adını yazın.";i.focus();return}state.project_name=v;save();ssClose();if(PF_OK&&!pf.handle){v26Overview();try{createProjectFile()}catch(e){}}else{renderConfig();renderRules()}};
sc.addEventListener("keydown",e=>{if(e.key==="Escape"){e.stopPropagation();ssClose()}if(e.key==="Enter"&&e.target.id==="ssName"){e.preventDefault();ssCreate()}if(e.key==="Tab"){let f=[...sc.querySelectorAll("button,input")].filter(x=>!x.disabled&&x.offsetParent),a=f[0],z=f[f.length-1];if(e.shiftKey&&document.activeElement===a){e.preventDefault();z.focus()}else if(!e.shiftKey&&document.activeElement===z){e.preventDefault();a.focus()}}});
sc.addEventListener("mousedown",e=>{if(e.target===sc)ssClose()});
lockNote=function(){return `<div class="lockNote v26Lock" role="note"><span><b>Proje başlatılmadı.</b> Kararları işaretlemek için bir proje oluşturun ya da kayıtlı proje dosyanızı açın; her seçim bu dosyaya otomatik kaydedilir.</span><span class="lockActs"><button type="button" class="btn dark" onclick="ssOpen()">Projeyi başlat</button><button type="button" class="btn" onclick="pfImport()">Proje dosyasını aç</button></span></div>`};
const _requireProject=requireProject;
requireProject=function(){if(projectReady())return true;if(PF_OK&&String(state.project_name||"").trim())return _requireProject();ssOpen();return false};

/* 5. Alanlar: görünüm anahtarı, Neden önemli?, seçenek araç çubuğu, yan panel */
const PT_GROUPS={tanitim:["Tanıtım",["Corporate Website","Personal Website","Portfolio","Landing Page","Event","Nonprofit"]],icerik:["İçerik",["Blog","News Media","Knowledge Base","Directory"]],uygulama:["Uygulama",["SaaS","Web App","Portal","Community","LMS","Intranet"]],ticaret:["Ticaret & işlem",["E-commerce","Marketplace","B2B Platform","Booking","Classifieds"]],diger:["Kamu & diğer",["Government","Other"]]};
const OPT_GROUPS={project_type:PT_GROUPS};
function optFilter(fid){let fe=fieldBox.querySelector(`.field[data-field-id="${fid}"]`);if(!fe)return;let f=FI[fid],q=norm(OPT_Q[fid]||""),g=OPT_G[fid]||"",G=OPT_GROUPS[fid],L=opts(f),els=[...fe.querySelectorAll(":scope .options > .option")],vis=0;
 els.forEach((el,k)=>{let o=L[k],okG=!g||!G||!o||(G[g]&&G[g][1].includes(o.value)),okQ=!q||hit(norm(el.textContent),q),show=okG&&okQ||el.classList.contains("selected");el.classList.toggle("v26Off",!show);if(show)vis++});
 let none=fe.querySelector(".v26None");if(none)none.hidden=vis>0;
 fe.querySelectorAll(".v26Chip").forEach(c=>c.setAttribute("aria-pressed",String((c.dataset.g||"")===g)))}
function optBar(fe,f){let box=fe.querySelector(":scope > .options");if(!box)return;let n=box.children.length,hasMeta=!!box.querySelector(".optMeta"),G=OPT_GROUPS[f.id];if(n<10&&!hasMeta&&!G)return;
 let bar=document.createElement("div");bar.className="v26OptBar";
 bar.innerHTML=(n>=10?`<input type="search" data-v26="q" data-fid="${E(f.id)}" placeholder="Seçeneklerde ara" aria-label="${E(f.label)}: seçeneklerde ara" value="${E(OPT_Q[f.id]||"")}">`:"")
  +(G?`<button type="button" class="v26Chip" data-v26="chip" data-fid="${E(f.id)}" data-g="" aria-pressed="true">Tümü<small>${n}</small></button>`+Object.keys(G).map(k=>`<button type="button" class="v26Chip" data-v26="chip" data-fid="${E(f.id)}" data-g="${k}" aria-pressed="false">${E(G[k][0])}<small>${G[k][1].length}</small></button>`).join(""):"")
  +(hasMeta?`<label class="v26MetaT" data-v26="metal"><input type="checkbox" data-v26="meta"${document.body.classList.contains("v26Meta")?" checked":""}>Senaryo ve örnekleri tüm kartlarda göster</label>`:"");
 box.before(bar);let none=document.createElement("p");none.className="v26None";none.hidden=true;none.textContent="Aramayla eşleşen seçenek yok.";box.after(none);optFilter(f.id)}
function whyWrap(fe){let m=fe.querySelector(":scope > .fieldMeta");if(!m)return;let d=document.createElement("details");d.className="v26Why";d.open=WHY_OPEN;d.innerHTML=`<summary data-v26="why">Neden önemli? Senaryo ve örnek</summary>`;m.before(d);d.appendChild(m);d.addEventListener("toggle",()=>{WHY_OPEN=d.open})}
function asideFor(fe,f){let rule=fe.querySelector(":scope > .rule"),ag=fe.querySelector(":scope > .fAgents");if(!rule&&!ag)return;let a=document.createElement("aside");a.className="v26Aside";a.setAttribute("aria-label","Seçimin etkisi");
 let sel=[...fe.querySelectorAll(".options > .option.selected")];
 if(sel.length){let c=document.createElement("div");c.className="v26Card v26Sel";c.innerHTML=`<b>SEÇİMİNİZ</b><span class="v26SelN">${sel.map(x=>E((x.querySelector(":scope > b")||x).textContent)).join(", ")}</span>`;if(sel.length===1){let m=sel[0].querySelector(":scope > .optMeta");if(m)c.appendChild(m.cloneNode(true))}a.appendChild(c)}
 /* 2026-11-07 kullanıcı isteği: sorumlu ajan üstte, oluşan kural altta */
 if(ag)a.appendChild(ag);
 if(rule)a.appendChild(rule);else if(f.type!=="text"&&f.type!=="textarea"){let c=document.createElement("div");c.className="v26Card v26Sel";c.innerHTML=`<b>BU SEÇİMDEN OLUŞAN KURAL</b><span>Bir seçim yaptığınızda oluşan kural burada görünür.</span>`;a.appendChild(c)}
 fe.appendChild(a);fe.classList.add("v26Split")}
function viewsBar(){let s=SI[active];if(!s)return;let fs=F.filter(f=>f.section===active&&shown(f)&&navF(f));if(!fs.length)return;let cur=activeFieldId?"single":showAll?"all":"guide",nx=fs.find(f=>f.id===activeFieldId)||fs.find(f=>!isset(f))||fs[0];
 let v=document.createElement("div");v.className="v26Views";v.setAttribute("role","tablist");v.setAttribute("aria-label","Bölüm görünümü");
 v.innerHTML=[["guide","Rehber","showGuide()"],["single","Tek karar",`goToField('${E(active)}','${E(nx.id)}')`],["all","Tüm kararlar","showSection()"]].map(x=>`<button type="button" role="tab" data-v26="view" aria-selected="${x[0]===cur}" onclick="${x[2]}">${x[1]}</button>`).join("");
 fieldBox.insertBefore(v,fieldBox.firstChild)}
const _renderFields=renderFields;
function v26Field(fe,f){whyWrap(fe);{let r=fe.querySelector(":scope > .rule"),g=fe.querySelector(":scope > .fAgents");if(r&&g&&(r.compareDocumentPosition(g)&Node.DOCUMENT_POSITION_FOLLOWING))fe.insertBefore(g,r)}if(f.type==="select"||f.type==="multiselect")optBar(fe,f);if(activeFieldId)asideFor(fe,f)}
renderFields=function(){_renderFields();try{viewsBar();fieldBox.querySelectorAll(":scope > .field").forEach(fe=>{let f=FI[fe.dataset.fieldId];if(f)v26Field(fe,f)})}catch(e){console.error("v26 renderFields",e)}};
/* 2026-11-07: tek alan yeniden çizilince (sorumlu ajan ekleme / kaldırma — refreshField) V26 eklemeleri (neden kutusu, seçenek çubuğu, yan panel) yeniden uygulanır */
const _refreshField=refreshField;
refreshField=function(id){_refreshField(id);try{let f=FI[id],fe=[...fieldBox.querySelectorAll(":scope > .field")].find(x=>x.dataset.fieldId===id);if(f&&fe)v26Field(fe,f)}catch(e){console.error("v26 refreshField",e)}};
/* Araç çubuğu kilitliyken de çalışsın: fieldBox'ın kilit dinleyicisinden önce yakalanır */
document.addEventListener("click",e=>{let t=e.target.closest&&e.target.closest("[data-v26]");if(!t||!fieldBox.contains(t))return;e.stopPropagation();if(t.dataset.v26==="chip"){OPT_G[t.dataset.fid]=t.dataset.g||"";optFilter(t.dataset.fid)}else if(t.dataset.v26==="view"){t.onclick&&t.onclick(e)}},true);
document.addEventListener("focusin",e=>{let t=e.target.closest&&e.target.closest("[data-v26]");if(t&&fieldBox.contains(t))e.stopPropagation()},true);
document.addEventListener("input",e=>{let t=e.target;if(t.dataset&&t.dataset.v26==="q"){OPT_Q[t.dataset.fid]=t.value;optFilter(t.dataset.fid)}});
document.addEventListener("change",e=>{let t=e.target;if(t.dataset&&t.dataset.v26==="meta"){document.body.classList.toggle("v26Meta",t.checked);ls.set(V26_META_KEY,t.checked?"1":"");fieldBox.querySelectorAll('[data-v26="meta"]').forEach(x=>x.checked=t.checked)}});
document.body.classList.toggle("v26Meta",ls.get(V26_META_KEY)==="1");

/* 6. Mobil ⋯ menüsü (901–1120 px'te kenar çubuğu açıkken de; Proje Özeti girişi mobilde Özet'e dönüş yolu) ve ⌘K */
const acts=document.querySelector("header .actions"),mb=document.createElement("button");mb.type="button";mb.id="moreBtn";mb.className="btn";mb.setAttribute("aria-label","Diğer işlemler");mb.setAttribute("aria-haspopup","menu");mb.setAttribute("aria-expanded","false");mb.setAttribute("aria-controls","moreMenu");mb.textContent="⋯";
acts.insertBefore(mb,copyMaster);
const mm=document.createElement("div");mm.id="moreMenu";mm.className="moreMenu";mm.setAttribute("role","menu");mm.hidden=true;document.body.appendChild(mm);
function mmClose(f){mm.hidden=true;mb.setAttribute("aria-expanded","false");if(f)mb.focus()}
mb.onclick=e=>{e.stopPropagation();if(!mm.hidden){mmClose();return}let dk=document.documentElement.dataset.theme==="dark";mm.innerHTML=`<button type="button" role="menuitem" data-a="ov">Dashboard</button><button type="button" role="menuitem" data-a="ag">Ajanları İndir</button><button type="button" role="menuitem" data-a="ex">JSON İndir</button><button type="button" role="menuitem" data-a="im">JSON İçe Aktar</button><button type="button" role="menuitem" data-a="th">${dk?"Açık temaya geç":"Koyu temaya geç"}</button>`;mm.hidden=false;mb.setAttribute("aria-expanded","true");let r=mb.getBoundingClientRect();mm.style.top=Math.round(r.bottom+8)+"px";mm.style.left=Math.round(Math.max(12,Math.min(r.right-mm.offsetWidth,innerWidth-mm.offsetWidth-12)))+"px";mm.querySelector("button").focus()};
mm.onclick=e=>{let b=e.target.closest("button");if(!b)return;e.stopPropagation();mmClose();if(b.dataset.a==="ex"){exportBtn.click();let x=document.getElementById("exMenu");if(x&&!x.hidden){let r=mb.getBoundingClientRect();x.style.top=Math.round(r.bottom+8)+"px";x.style.left=Math.round(Math.max(12,innerWidth-x.offsetWidth-12))+"px"}}else if(b.dataset.a==="im")importBtn.click();else if(b.dataset.a==="ov")v26Overview();else if(b.dataset.a==="ag")dlOpen();else themeBtn.click()};
document.addEventListener("mousedown",e=>{if(!mm.hidden&&!mm.contains(e.target)&&e.target!==mb)mmClose()});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!mm.hidden)mmClose(true);if((e.metaKey||e.ctrlKey)&&!e.altKey&&(e.key==="k"||e.key==="K")){e.preventDefault();if(matchMedia("(max-width:900px)").matches)setNav(true);else if(document.documentElement.classList.contains("sideHidden")&&typeof sideSet==="function")sideSet(false);sideSearchInput.focus();sideSearchInput.select()}});
sideSearchInput.placeholder="Menüde ara… (⌘K)";

/* 8. Ajan kurulum paketi (üst şerit "Ajanları İndir") ve indirme uyarısı — 2026-11-07 kullanıcı istekleri: yalnız projede seçili ajanların Claude kurulum dosyalarını indirme alanı; ajanları ve JSON dosyalarını indirirken projedeki bütün maddelerin tamamlanmış olmasına dikkat uyarısı. agZip() artık paneli açar, zip'i agZip(true) indirir. */
const DL_AREAS=[["project","Proje Kararları"],["common","Ortak Bilgiler"],["marketing","Pazarlama Kararları"],["audit","SEO Denetimi"]];
function dlStat(){let L=DL_AREAS.map(([a,t])=>{let X=areaFields(a);return {t,n:X.filter(isset).length,c:X.length}}),req=F.filter(f=>shown(f)&&navF(f)&&f.required&&!isset(f)),nm=!String(state.project_name||"").trim();return {L,req,nm,done:!nm&&!req.length&&L.every(x=>x.n===x.c)}}
function dlWarn(){let s=dlStat();if(s.done)return `<div class="dlWarn ok" role="note"><b>Bütün maddeler tamamlandı.</b><span>Projedeki bütün kararlar verildi; indirilen dosyalar projenin tamamını yansıtır.</span></div>`;
 return `<div class="dlWarn" role="note"><b>İndirmeden önce projedeki bütün maddelerin tamamlanmış olmasına dikkat edin.</b><span>Verilmemiş kararlar kurallara, Claude promptuna, ajan dosyalarına ve JSON dosyalarına yansımaz; sonradan tamamlarsanız dosyaları yeniden indirmeniz gerekir.</span><ul>${s.nm?'<li class="req">Proje adı yazılmadı</li>':""}${s.L.map(x=>`<li${x.n===x.c?' class="ok"':""}>${E(x.t)}: <b>${x.n} / ${x.c}</b></li>`).join("")}${s.req.length?`<li class="req">Eksik zorunlu karar: <b>${s.req.length}</b></li>`:""}</ul><button type="button" class="linkBtn" onclick="dlGo()">Eksik kararlara git →</button></div>`}
const _exHtml=exHtml;exHtml=function(){return _exHtml().replace('<ul class="exList">',dlWarn()+'<ul class="exList">')};
const dlb=document.createElement("button");dlb.type="button";dlb.className="btn";dlb.id="agDlBtn";dlb.setAttribute("aria-haspopup","dialog");dlb.setAttribute("aria-expanded","false");dlb.setAttribute("aria-controls","agDlMenu");exportBtn.parentNode.insertBefore(dlb,exportBtn);
const dm=document.createElement("div");dm.id="agDlMenu";dm.className="exMenu agDlMenu";dm.setAttribute("role","dialog");dm.setAttribute("aria-labelledby","agDlT");dm.hidden=true;document.body.appendChild(dm);
function dlName(){return (pfFileName().replace(/\.json$/,"")||"proje")+"-claude-ajan-skill.zip"}
function dlLabel(){let n=agOn("dev").length;dlb.innerHTML=`Ajanları İndir${n?` <span class="dlN">${n}</span>`:""}`;dlb.title=n?`Projede seçili ${n} ajanın Claude kurulum dosyalarını (.zip) indir`:"Projede seçili ajan yok"}
function dlHtml(){let A=agOn("dev"),Z=agZipFiles(),sk=Z.filter(x=>/\/SKILL\.md$/.test(x.name)).length;
 return `<div class="exHead"><b id="agDlT">Ajanları Claude'a kur</b><button type="button" class="exX" onclick="dlClose(true)" aria-label="Kapat">✕</button></div><p class="exIntro">Yalnız projede seçili ajanlar ve skill'leri tek zip dosyasında iner: <code>.claude/agents/</code> ve <code>.claude/skills/</code>. Zip'i projenizin kök klasörüne açın; Claude Code'da <code>/agents</code> ile doğrulayın.</p>${dlWarn()}`
 +(A.length?`<div class="dlSum"><b>${A.length} ajan · ${sk} skill dosyası</b><ul>${A.slice(0,8).map(a=>`<li>${E(a.name)}</li>`).join("")}${A.length>8?`<li class="more">ve ${A.length-8} ajan daha</li>`:""}</ul></div><code class="exName">${E(dlName())}</code><div class="dlActs"><button type="button" class="btn dark" onclick="agZip(true);dlClose()">Zip'i indir</button><button type="button" class="btn" onclick="dlClose();showPage('agents');ksGo('setup')">Nasıl kurulur?</button></div>`
 :`<div class="dlSum empty"><b>Projede seçili ajan yok.</b><span>Ajanlar sayfasındaki Pozisyon Ajanları sekmesinden projeye ajan ekleyin; burada yalnız seçtikleriniz iner.</span></div><div class="dlActs"><button type="button" class="btn dark" onclick="dlClose();showPage('agents');ksGo('dev')">Ajan seç</button></div>`)}
function dlPlace(){let a=[dlb,document.getElementById("moreBtn")].find(x=>x&&x.offsetParent),w=dm.offsetWidth;if(!a){dm.style.top="72px";dm.style.left=Math.max(12,innerWidth-w-12)+"px";return}let r=a.getBoundingClientRect();dm.style.top=Math.round(r.bottom+8)+"px";dm.style.left=Math.round(Math.max(12,Math.min(r.right-w,innerWidth-w-12)))+"px"}
window.dlOpen=function(){if(typeof exClose==="function")exClose();dm.innerHTML=dlHtml();dm.hidden=false;dlPlace();dlb.setAttribute("aria-expanded","true");let b=dm.querySelector(".dlActs .btn");if(b)b.focus()};
window.dlClose=function(f){dm.hidden=true;dlb.setAttribute("aria-expanded","false");if(f&&dlb.offsetParent)dlb.focus()};
window.dlGo=function(){dlClose();if(typeof exClose==="function")exClose();let s=dlStat();if(s.nm){pnFocus();return}let f=s.req[0]||DL_AREAS.map(([a])=>nextField(a)).find(Boolean);if(f)goToField(f.section,f.id)};
dlb.onclick=e=>{e.stopPropagation();if(!dm.hidden){dlClose(true);return}dlOpen()};
document.addEventListener("mousedown",e=>{if(!dm.hidden&&!dm.contains(e.target)&&!dlb.contains(e.target))dlClose()});
document.addEventListener("keydown",e=>{if(e.key==="Escape"&&!dm.hidden)dlClose(true)});
addEventListener("resize",()=>{if(!dm.hidden)dlPlace()});
const _agZip=agZip;agZip=function(force){if(force===true){_agZip();return}dlOpen()};
/* save() const olduğu için sarmalanamaz; her kayıtta çağrılan queueProjectFileWrite üzerinden sayaç güncellenir */
const _qpw=window.queueProjectFileWrite;window.queueProjectFileWrite=function(){try{dlLabel()}catch(e){}return typeof _qpw==="function"?_qpw.apply(this,arguments):undefined};
dlLabel();

/* 9. Verilmiş kararlar sol menüde yeşil (2026-11-07 kullanıcı isteği). Ana betik subItem'e "done" ve data-fid, bütün kararları verilmiş menuSection'a "done" yazar; değer değişince (renderProgress her değişiklikte çağrılır) sınıflar yeniden çizmeden güncellenir. */
const _renderProgress=renderProgress;renderProgress=function(){_renderProgress();try{sideNav.querySelectorAll(".subItem[data-fid]").forEach(b=>{let f=FI[b.dataset.fid];b.classList.toggle("done",!!f&&!!isset(f))});sideNav.querySelectorAll(".menuSection").forEach(sec=>{let L=[...sec.querySelectorAll(".subItem[data-fid]")];sec.classList.toggle("done",L.length>0&&L.every(b=>b.classList.contains("done")))})}catch(e){console.error("v26 done",e)}};

/* 7. İlk açılış */
renderConfig();railSync();
if(projectReady())showPage("overview");
setTimeout(()=>{if(!projectReady()&&!ss.get(V26_SS_KEY))ssOpen()},700);
})();
</script>
