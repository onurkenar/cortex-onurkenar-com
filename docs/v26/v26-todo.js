/* Yapılacaklar (2026-11-12, kullanıcı isteği: "yapılan seçimlerden oluşan bir todo list hazırla").
   Sayfa #todoPage (showPage("todo")), modül şeridinde "Yapılacaklar" (Kurallar'dan sonra), çekmecede #sideTodoBtn.
   Görevler verilmiş kararlardan türetilir (görünen + menüde olan + dolu: shown && navF && isset): Ortak Bilgiler, Kararlar
   (CLAUDE-TALIMATLARI.md'deki fazlara göre), Pazarlama, SEO Denetimi, Google, Meta, Yapay Zekâ. Çoklu seçimli kararda her seçenek
   ayrı alt görevdir (yaprak görev). Kurallar, Claude promptu, talimat dosyası ve ajan dosyaları değişmez.
   Yinelenen görevler (2026-11-13, kullanıcı istekleri: "tekrarlı şekilde yapılması gerekenleri tekrarlayan görev olarak belirle";
   kararlar: sıklık her görevde değiştirilebilir, her yapılışın geçmişi tutulur, takvim dosyası (.ics), aralığı yazılmayan
   "dönemsel" işler 3 ayda bir): varsayılan sıklık RC (sıklığı kararın kendisi olan alanlar: seçilen değer → sıklık) ve RO
   ("alan|seçenek" → sıklık; metninde sıklık yazan seçenekler) tablolarından gelir; kullanıcı değişikliği state.todo.freq[anahtar]
   ("once" = tek seferlik). Takvimli sıklıkta son yapılıştan sonraki tarih gelince görev "Zamanı geldi", min(30 gün, aralık) daha
   geçince "Gecikti" olur; olaya bağlı sıklıkta ("Her yeni sürümde", "Her kampanyada") olay düğmesi görevleri yeniden açar.
   Kayıt: state.todo = {done:{anahtar:{d:son tarih, h:parmak izi, log?:["YYYY-AA-GG SS:DD:ss", …]}}, freq?:{anahtar:sıklık},
   ev?:{rel:[…], camp:[…]}} — yalnız işaret / değişiklik varken; anahtar alan kimliği ya da "alan|değer". Karar değişirse parmak izi
   tutmaz, görev "Karar değişti" olur. YAPILACAKLAR.md (todoMd) ve YAPILACAKLAR.ics (todoIcs) Dashboard › İndirmeler'de de var.
   Kaynak docs/v26/v26-todo.{js,css} → docs/v26/yapilacaklar_ekle.py */
(()=>{
const AREAS=[["common","Ortak Bilgiler"],["project","Kararlar"],["marketing","Pazarlama"],["audit","SEO Denetimi"],["google","Google Servisleri"],["meta","Meta Servisleri"],["ai","Yapay Zekâ"]],
 PH=[["Proje temeli ve mimari",["Başlangıç","Teknik Mimari","Sunucu & Altyapı"]],["Tasarım ve arayüz",["Tasarım & Arayüz"]],["İçerik ve yönetim",["İçerik & Yönetim"]],["İş modülleri",["İş Modülleri"]],["SEO ve görünürlük",["SEO & Görünürlük"]],["Güvenlik ve gizlilik",["Güvenlik & Gizlilik"]],["Performans, test ve geliştirme süreci",["Performans & Test","Geliştirme Süreci"]],["Yayın ve operasyon",["Yayın & Operasyon"]]],
 ICON="M10 6h10M10 12h10M10 18h10M3.5 6l1.5 1.5L7.5 5M3.5 12l1.5 1.5 2.5-2.5M3.5 18l1.5 1.5 2.5-2.5",
 /* sıklıklar: ad, takvim aralığı (d gün / m ay) ya da olay */
 PER={"1w":["Haftalık",{d:7}],"2w":["2 haftada bir",{d:14}],"1m":["Aylık",{m:1}],"3m":["3 ayda bir",{m:3}],"6m":["6 ayda bir",{m:6}],"1y":["Yılda bir",{m:12}],"rel":["Her yeni sürümde",null,"rel"],"camp":["Her kampanyada",null,"camp"]},
 EVN={rel:["Yeni sürüm yayınlandı","sürüm"],camp:["Yeni kampanya başladı","kampanya"]},
 /* sıklığı kararın kendisi olan alanlar (seçilen değer → sıklık) */
 RC={restore_testing:{Quarterly:"3m",Biannual:"6m",Annual:"1y","Before Major Release":"rel"},
  au_recheck:{monthly:"1m",quarterly:"3m"},
  mk_plan_period:{monthly:"1m",quarterly:"3m",half:"6m",yearly:"1y"},
  mk_comp_refresh:{monthly:"1m",quarterly:"3m",campaign:"camp"},
  mk_mail_freq:{weekly:"1w",biweekly:"2w",monthly:"1m",campaign:"camp"},
  mk_pod_freq:{weekly:"1w",biweekly:"2w",monthly:"1m"},
  mk_ads_pacing:{weekly:"1w",biweekly:"2w",monthly:"1m"},
  mk_report_rhythm:{weekly_monthly:"1w",monthly:"1m",campaign:"camp"},
  mk_backup:{shared:"1w"},
  mk_post_times:{data:"1m"},mk_st_audit_freq:{weekly:"1w",monthly:"1m",release:"rel"}},
 /* metninde sıklık yazan seçenekler ("dönemsel" → 3 ay, kullanıcı kararı) */
 RO={"privacy_retention|periodic_auto":"6m","privacy_retention|archive":"6m","yz_bots_train|allow":"1y","yz_cg_claim|wait":"1m",
  "yz_meta_ai|use":"1w","yz_meta_ai|waitlist":"1m","pentest_executor|hybrid":"1y","pentest_schedule|annual":"1y","pentest_schedule|ci_dast":"rel",
  "mt_cat_source|manual":"1m","slo_practices|error_budget":"1m","gg_gc_billing|monthly":"1m","gg_gc_iam|review":"3m","gg_gc_apis|rotate":"1y","slo_practices|capacity_review":"3m","admin_user_mgmt|periodic_review":"3m",
  "approval_roles|periodic_review":"3m","cookie_behavior|inventory":"1m","privacy_breach|response_plan":"1y","privacy_breach|drill":"1y",
  "privacy_rights|register":"3m","dr_measures|drill":"1y","mobile_release|privacy_labels":"rel","gg_access|review":"3m","mt_access|review":"3m",
  "mt_access|system_user":"3m","gg_gtm_settings|naming":"3m","gg_gsc_settings|monitor":"1m","gg_ads_settings|auto_apply_off":"1w",
  "gg_ads_settings|negatives":"1m","gg_mc_settings|diagnostics":"1w","gg_handover|quarterly":"3m","mt_handover|quarterly":"3m",
  "yz_handover|tests":"1m","yz_handover|review":"3m","mt_px_settings|emq":"1m","mt_page_settings|moderation":"1w","mt_page_inbox|sla":"1m",
  "mt_ig_settings|links":"1m","mt_ig_settings|insights":"1m","mt_wa_settings|payment":"1m","mt_wa_settings|quality":"1w","mt_wa_messaging|cost":"1m",
  "mt_ads_settings|billing":"1m","mt_cat_settings|price_stock":"1w","mt_cat_settings|diagnostics":"1w","yz_ads_setup|review":"1w",
  "yz_google|merchant":"1w","yz_microsoft|bwt":"1m","yz_as_rules|quality":"1w","yz_monitor_set|hub_insights":"1m","yz_monitor_set|bing_ai":"1m",
  "yz_monitor_set|prompt_tests":"1m","yz_monitor_set|quarterly":"3m","yz_cg_ops|insights":"1m","sv_triggers|periodic":"3m","ml_deliverability|spf_dkim":"3m",
  "mk_measure_scope|social":"3m","mk_post_check|d7":"camp","mk_post_check|month":"1m","mk_gads_structure|location_service":"3m",
  "mk_report_outputs|exec":"1m","mk_platforms|google":"1w","mk_st_access|review":"3m","mk_st_access|billing":"1y","mk_st_links|monitor":"1m","mk_st_kw_source|gsc":"3m","mk_st_comp|visibility":"3m","mk_st_comp|market":"3m"},
 TD={q:"",f:"all",a:"all"},
 pad=n=>String(n).padStart(2,"0"),
 fmt=x=>x.getFullYear()+"-"+pad(x.getMonth()+1)+"-"+pad(x.getDate()),
 today=()=>window.TODO_TODAY||fmt(new Date()),
 stamp=()=>{let x=new Date();return (window.TODO_TODAY||fmt(x))+" "+pad(x.getHours())+":"+pad(x.getMinutes())+":"+pad(x.getSeconds())},
 pname=()=>String(state.project_name||"").trim()||"Proje",
 clean=t=>String(t??"").replace(/\s*\(önerilen\)/g,"").trim(),
 cut=(t,n)=>{t=String(t||"").replace(/\s+/g," ").trim();return t.length>n?t.slice(0,n-1)+"…":t};
function fp(v){let s=String(v??""),h=2166136261;for(let i=0;i<s.length;i++){h^=s.charCodeAt(i);h=Math.imul(h,16777619)}return (h>>>0).toString(36)}
function T0(){let t=state.todo;return t&&typeof t==="object"?t:{}}
function rec(){let t=T0();return t.done&&typeof t.done==="object"?t.done:{}}
function fq(){let t=T0();return t.freq&&typeof t.freq==="object"?t.freq:{}}
function evs(k){let t=T0(),L=t.ev&&Array.isArray(t.ev[k])?t.ev[k]:[];return L}
function num(id,sec){let N=window.NAV_NUM;return N?(id?N.fld[id]:N.sec[sec])||"":""}
/* tarih */
function addP(ds,P){let [y,m,d]=ds.split("-").map(Number),x;if(P.d)x=new Date(y,m-1,d+P.d);else{x=new Date(y,m-1+P.m,1);x.setDate(Math.min(d,new Date(x.getFullYear(),x.getMonth()+1,0).getDate()))}return fmt(x)}
const pDays=P=>P.d||P.m*30;
/* yaprak görevin varsayılan sıklığı: alanın kendisi (RC) ya da seçenek (RO) */
function defPer(f,val){if(val==null&&RC[f.id])return RC[f.id][state[f.id]]||"";let v=val;if(v==null){let s=state[f.id];v=Array.isArray(s)&&s.length===1?s[0]:s}return RO[f.id+"|"+v]||""}
/* yaprağın durumu */
function leaf(L,f,val){let D=rec()[L.k],def=defPer(f,val),o=fq()[L.k],per=o===undefined?def:(o==="once"?"":o);
 L.def=def;L.per=PER[per]?per:"";L.log=D&&Array.isArray(D.log)?D.log:(D&&D.d?[D.d]:[]);L.last=D?D.d:"";L.next="";
 if(!D)L.st="open";else if(D.h!==L.h)L.st="changed";
 else if(!L.per)L.st="done";
 else{let P=PER[L.per];if(P[1]){L.next=addP(L.last,P[1]);let t=today();L.st=t<L.next?"done":t>=addP(L.next,{d:Math.min(30,pDays(P[1]))})?"late":"due"}
  else{let e=evs(P[2]),le=e[e.length-1]||"",ll=L.log[L.log.length-1]||L.last;L.st=le&&le>ll?"due":"done"}}
 return L}
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
const RANK={late:5,due:4,changed:3,open:2,done:1};
/* görev listesi: alan → bölüm → görev (alt görevler) */
function build(){let out=AREAS.map(([a,t])=>({a,t,n:(window.MT_NUM||{})[a]||"",G:[]})),by={};out.forEach(x=>by[x.a]=x);
 let secs={};
 F.forEach(f=>{let s=SI[f.section];if(!s||!navF(f)||!shown(f)||!isset(f))return;let a=AREA(s),A=by[a];if(!A)return;
  let r=rule(f)||"",it={f,s,k:f.id,num:num(f.id),t:clean(f.label),sum:sum(f),r,ag:agents(f),subs:[]},v=state[f.id];
  if(f.type==="multiselect"&&Array.isArray(v)&&v.length>1)it.subs=v.map(x=>{let o=opts(f).find(o=>o.value===x)||{};return leaf({k:f.id+"|"+x,h:fp(x+"\u0001"+(o.ruleDetail||"")),t:clean(o.label||x),r:o.ruleDetail||"",sub:true},f,x)});
  else{it.h=fp(r);leaf(it,f,null)}
  if(it.subs.length){let S=it.subs.map(x=>x.st);it.st=S.every(x=>x==="done")?"done":S.reduce((a,b)=>RANK[b]>RANK[a]?b:a,"done");if(it.st==="done"&&!S.every(x=>x==="done"))it.st="open"}
  let key=a+":"+s.id;if(!secs[key]){secs[key]={s,num:num(null,s.id),I:[]};
   let gname=a==="project"?((PH.find(p=>p[1].includes(s.group))||["Diğer proje kararları"])[0]):(a==="marketing"?s.group:"");
   let g=A.G.find(x=>x.name===gname);if(!g){g={name:gname,S:[]};A.G.push(g)}g.S.push(secs[key])}
  secs[key].I.push(it)});
 out.forEach(A=>{if(A.a==="project")A.G.sort((x,y)=>idx(x.name)-idx(y.name))});
 return out.filter(A=>A.G.length)}
const idx=n=>{let i=PH.findIndex(p=>p[0]===n);return i<0?99:i};
function leaves(it){return it.subs.length?it.subs:[it]}
/* Kurulum: her yaprak bir kez (yinelenen görevin ilk yapılışı kurulumdur). Bakım: yinelenen yapraklar. */
function stats(L){let a=0,d=0,c=0,r=0,ok=0,due=0,late=0,ev=0;L.forEach(it=>leaves(it).forEach(x=>{a++;let set=x.st!=="open"&&x.st!=="changed";if(set)d++;else if(x.st==="changed")c++;
  if(x.per){r++;if(PER[x.per][2])ev++;if(x.st==="done")ok++;else if(x.st==="due")due++;else if(x.st==="late")late++}}));
 return {a,d,c,o:a-d,p:a?Math.round(d/a*100):0,r,ok,due,late,ev}}
function allItems(T){let L=[];T.forEach(A=>A.G.forEach(g=>g.S.forEach(s=>L.push(...s.I))));return L}
function areaItems(A){let L=[];A.G.forEach(g=>g.S.forEach(s=>L.push(...s.I)));return L}
/* filtre */
function hay(it,s){return norm([it.num,it.t,it.sum,it.r,s.name,s.code,...leaves(it).map(x=>(x.per?PER[x.per][0]:"")+" "+(x.sub?x.t+" "+x.r:"")),...it.ag.map(a=>a.name)].join(" "))}
function pass(it,s){let Lv=leaves(it),f=TD.f;
 if(f==="open"&&!Lv.some(x=>x.st==="open"||x.st==="changed"))return false;
 if(f==="done"&&!Lv.every(x=>x.st!=="open"&&x.st!=="changed"))return false;
 if(f==="changed"&&!Lv.some(x=>x.st==="changed"))return false;
 if(f==="rec"&&!Lv.some(x=>x.per))return false;
 if(f==="due"&&!Lv.some(x=>x.st==="due"||x.st==="late"))return false;
 let raw=String(TD.q||"").trim();if(!raw)return true;let h=hay(it,s),toks=raw.split(/\s+/).filter(t=>norm(t)||TD_NQ.test(t));if(!toks.length)return true;
 /* madde numarasıyla arama (2026-11-13): "2.11.3.1" o karar, "2.11.3" / "2.11" altındakiler; noktasız sayı numara ya da metin */
 return toks.every(t=>TD_NQ.test(t)?(tdNHit(it.num,t)||(!/\./.test(t)&&hit(h,norm(t)))):hit(h,norm(t)))}
const TD_NQ=/^\d+(\.\d+)*\.?$/;function tdNHit(n,t){n=String(n||"").replace(/\.$/,"");t=String(t||"").replace(/\.$/,"");return !!n&&(n===t||n.startsWith(t+"."))}

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
function evBar(T){let L=allItems(T),has={};L.forEach(it=>leaves(it).forEach(x=>{if(x.per&&PER[x.per][2]&&x.st!=="open"&&x.st!=="changed")has[PER[x.per][2]]=(has[PER[x.per][2]]||0)+1}));
 let B=Object.keys(EVN).filter(k=>has[k]).map(k=>{let e=evs(k),le=e[e.length-1];return `<button type="button" class="btn" data-td-ev="${k}" title="${has[k]} görev yeniden açılır">${E(EVN[k][0])}</button>${le?`<span class="tdEvLast">Son ${E(EVN[k][1])}: ${E(le)}</span>`:""}`});
 return B.length?`<div class="tdEv"><span>Olaya bağlı görevler:</span>${B.join("")}</div>`:""}
function render(){if(!isOn())return;let T=build(),L=allItems(T),S=stats(L);
 if(!L.length){PG.innerHTML=`<div class="tdHead"><div><p class="tdEye">GÖREV LİSTESİ</p><h1>Yapılacaklar</h1><p class="tdLead">Henüz karar verilmedi. Kararlar, Ortak Bilgiler ve Pazarlama menülerinde yaptığınız her seçim burada uygulanacak bir görev olur.</p></div></div><div class="tdEmpty"><button type="button" class="btn primary" onclick="goArea('project')">Kararlara git</button></div>`;return}
 PG.innerHTML=`<div class="tdHead"><div><p class="tdEye">GÖREV LİSTESİ</p><h1>Yapılacaklar</h1><p class="tdLead">Verdiğiniz ${L.length} karardan oluşan uygulama listesi. Uygulanan görevi işaretleyin; karar sonradan değişirse görev “Karar değişti” olarak yeniden açılır. ↻ işaretli görevler yinelenir: her yapılışta işaretleyin, tarih geçmişe yazılır ve sonraki tarih hesaplanır. Sıklığı her görevde değiştirebilirsiniz.</p></div>
 <div class="tdTools"><button type="button" class="btn" data-td-act="copy">Kopyala</button>${S.r?`<button type="button" class="btn" data-td-act="ics" title="Yinelenen görevlerin takvim dosyası">Takvim (.ics)</button>`:""}<button type="button" class="btn primary" data-td-act="md">YAPILACAKLAR.md indir</button></div></div>
 <div class="tdSum" role="group" aria-label="İlerleme"><div class="tdBar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${S.p}" aria-label="Kurulum ilerlemesi"><i style="width:${S.p}%"></i></div><p><b>Kurulum: ${S.d}/${S.a} - %${S.p}</b> · ${S.o} açık${S.c?` · <span class="tdWarn">${S.c} karar değişti</span>`:""}</p>
 ${S.r?`<p class="tdMaint"><b>↻ Bakım:</b> ${S.r} yinelenen görev · ${S.ok} güncel${S.due?` · <span class="tdWarn">${S.due} zamanı geldi</span>`:""}${S.late?` · <span class="tdLate">${S.late} gecikti</span>`:""}${S.r-S.ok-S.due-S.late?` · ${S.r-S.ok-S.due-S.late} henüz yapılmadı`:""}</p>`:""}
 <div class="tdAreas">${T.map(A=>{let s=stats(areaItems(A));return `<button type="button" class="tdArea${TD.a===A.a?" on":""}${s.a&&s.d===s.a&&!s.due&&!s.late?" done":""}" data-td-area="${A.a}" aria-pressed="${TD.a===A.a}"><b>${A.n?A.n+". ":""}${E(A.t)}</b><span>${s.d}/${s.a} - %${s.p}</span>${s.due+s.late?`<em>${s.due+s.late} bakım zamanı</em>`:""}</button>`}).join("")}</div>${evBar(T)}</div>
 <div class="tdBarTools"><label class="tdSearch"><span class="sr">Görevlerde ara</span><input type="search" id="tdQ" placeholder="Görevlerde ara (numara, karar, seçim, kural, sıklık, ajan)" value="${E(TD.q)}"></label>
 <div class="tdChips" role="group" aria-label="Duruma göre süz">${chip("all","Tümü",S.a,TD.f==="all","f")}${chip("open","Açık",S.o,TD.f==="open","f")}${chip("done","Tamamlanan",S.d,TD.f==="done","f")}${S.r?chip("rec","↻ Yinelenen",S.r,TD.f==="rec","f"):""}${S.due+S.late?chip("due","Zamanı gelen",S.due+S.late,TD.f==="due","f"):""}${S.c?chip("changed","Karar değişti",S.c,TD.f==="changed","f"):""}${TD.a!=="all"?chip("all","Bütün menüler",null,false,"area"):""}</div></div>
 <div id="tdList">${list(T)}</div>
 ${Object.keys(T0()).length?`<p class="tdFoot"><button type="button" class="linkBtn" data-td-act="reset">Bütün işaretleri ve geçmişi kaldır</button></p>`:""}`}
function list(T){let h="";T.forEach(A=>{if(TD.a!=="all"&&TD.a!==A.a)return;let s=stats(areaItems(A)),body="";
 A.G.forEach(g=>{let gb="";g.S.forEach(x=>{let I=x.I.filter(it=>pass(it,x.s));if(!I.length)return;let ss=stats(x.I);
   gb+=`<div class="tdSec"><h4><span class="tdNum">${E(x.num||x.s.code)}</span> ${E(x.s.name)} <small>${ss.d}/${ss.a}</small> <button type="button" class="linkBtn" data-td-sec="${E(x.s.id)}">Bölüme git</button></h4><ul>${I.map(item).join("")}</ul></div>`});
  if(gb)body+=g.name?`<div class="tdGroup"><h3>${A.a==="project"?"Faz: ":""}${E(g.name)}</h3>${gb}</div>`:gb});
 if(body)h+=`<section class="tdAreaBox"><h2>${A.n?`<span class="tdNum">${A.n}.</span> `:""}${E(A.t)} <small>${s.d}/${s.a} - %${s.p}</small></h2>${body}</section>`});
 return h||`<p class="tdNone">Bu süzgece uyan görev yok. <button type="button" class="linkBtn" data-td-act="clear">Süzgeci temizle</button></p>`}
function box(x,lbl){return `<input type="checkbox" data-td-k="${E(x.k)}"${x.st==="done"?" checked":""} aria-label="${E(lbl)}">`}
function perSel(x,lbl){let o=[["once","Tek seferlik"],...Object.keys(PER).map(k=>[k,PER[k][0]])],cur=x.per||"once";
 return `<select class="tdFq" data-td-fq="${E(x.k)}" aria-label="${E(lbl)} — sıklık">${o.map(([v,t])=>`<option value="${v}"${v===cur?" selected":""}>${E(t)}${v===(x.def||"once")?" (varsayılan)":""}</option>`).join("")}</select>`}
const BADGE={changed:"Karar değişti · yeniden kontrol edin",due:"Zamanı geldi",late:"Gecikti"};
function badge(x,short){return BADGE[x.st]?`<span class="tdBadge ${x.st}">${short&&x.st==="changed"?"değişti":BADGE[x.st]}</span>`:""}
function recLine(x,lbl){if(!x.per)return "";let P=PER[x.per],n=x.log.length,
 when=(x.st==="done"?`<button type="button" class="linkBtn tdLogBtn" data-td-log="${E(x.k)}" title="Vadesinden önce yapıldıysa bugünü geçmişe ekler">＋ Bugün yapıldı</button>`:"")+(x.last?`Son: ${E(x.last)}${P[1]?` · Sonraki: <b>${E(x.next)}</b>`:` · ${E(P[0].toLocaleLowerCase("tr"))} yeniden açılır`}`:`Henüz yapılmadı`);
 return `<div class="tdRec"><span class="tdRecI" aria-hidden="true">↻</span>${perSel(x,lbl)}<span>${when}</span>${n?`<details class="tdLog"><summary>Geçmiş (${n})</summary><ol>${x.log.slice().reverse().map(d=>`<li>${E(d)}</li>`).join("")}</ol></details>`:""}</div>`}
function item(it){let id="td-"+it.k.replace(/[^a-z0-9_-]/gi,"_"),off=it.ag.filter(a=>!a.on).length,
 ag=it.ag.length?`<p class="tdAg">Sorumlu ajan: ${it.ag.map(a=>`<span${a.on?"":` class="off" title="Projede değil"`}>${E(a.name)}</span>`).join(", ")}${off?" <em>(soluk olanlar projede değil)</em>":""}</p>`:"",
 hasSub=it.subs.length,
 date=!hasSub&&!it.per&&it.st==="done"&&it.last?`<span class="tdDate">${E(it.last)}</span>`:"",
 subs=hasSub?`<ul class="tdSubs">${it.subs.map(x=>`<li class="tdSub ${x.st}${x.per?" rec":""}"><label>${box(x,it.t+": "+x.t)}<span>${E(x.t)}</span>${badge(x,true)}</label>${recLine(x,it.t+": "+x.t)}${x.r?`<p class="tdSubR">${E(cut(x.r,320))}</p>`:""}</li>`).join("")}</ul>`:"",
 once=hasSub?it.subs.filter(x=>!x.per):(it.per?[]:[it]),
 fqRows=once.length?`<div class="tdFqRows"><p>Yinelensin mi?</p>${once.map(x=>`<label>${hasSub?`<span>${E(x.t)}</span>`:""}${perSel(x,hasSub?it.t+": "+x.t:it.t)}</label>`).join("")}</div>`:"";
 let main=hasSub?`<input type="checkbox" data-td-all="${E(it.k)}"${it.st==="done"?" checked":""} aria-label="${E(it.t)} — bütün seçenekler">`:box(it,it.t);
 return `<li class="tdIt ${it.st}${leaves(it).some(x=>x.per)?" rec":""}" id="${id}"><div class="tdRow"><label class="tdMain">${main}<span class="tdTx"><b>${it.num?`<span class="tdNum">${E(it.num)}</span> `:""}${E(it.t)}${!hasSub&&it.per?` <span class="tdRecTag">↻ ${E(PER[it.per][0])}</span>`:""}</b><span class="tdVal">${E(it.sum)}</span></span></label>${hasSub?badge(it):badge(it)}${date}<button type="button" class="linkBtn tdGo" data-td-go="${E(it.f.section)}|${E(it.f.id)}">Karara git</button></div>
 ${hasSub?"":recLine(it,it.t)}${subs}<details class="tdMore"><summary>Kural, sorumlu ve sıklık</summary><p class="tdRule">${E(it.r)}</p>${ag}${fqRows}</details></li>`}

/* ---------- İşlemler ---------- */
function tw(){if(!state.todo||typeof state.todo!=="object")state.todo={};let t=state.todo;if(!t.done||typeof t.done!=="object")t.done={};return t}
function tidy(){let t=state.todo;if(!t)return;["done","freq","ev"].forEach(k=>{if(t[k]&&!Object.keys(t[k]).length)delete t[k]});if(t.ev)Object.keys(t.ev).forEach(k=>{if(!t.ev[k].length)delete t.ev[k]});if(t.ev&&!Object.keys(t.ev).length)delete t.ev;if(!Object.keys(t).length)delete state.todo}
/* işaretle: tek seferlikte kayıt / sil; yinelenende yapılışı geçmişe ekle / son yapılışı geri al */
function mark(x,on){let t=tw(),D=t.done[x.k];
 if(on){if(x.per){let L=D&&Array.isArray(D.log)?D.log.slice():(D&&D.d&&D.h===x.h?[D.d]:[]);L.push(stamp());t.done[x.k]={d:today(),h:x.h,log:L}}else t.done[x.k]={d:today(),h:x.h}}
 else if(D){if(x.per&&Array.isArray(D.log)&&D.log.length>1){let L=D.log.slice(0,-1);t.done[x.k]={d:L[L.length-1].slice(0,10),h:D.h,log:L}}else delete t.done[x.k]}}
function setDone(L,on){if(!requireProject())return false;L.forEach(x=>{if(on?x.st!=="done":x.st==="done")mark(x,on)});tidy();save();return true}
function findIt(k){let L=allItems(build());for(let it of L){if(it.k===k)return {it};for(let x of it.subs)if(x.k===k)return {it,x}}return null}
function redraw(focusSel){let y=window.scrollY;render();window.scrollTo(0,y);if(focusSel){let el=PG.querySelector(focusSel);if(el)el.focus()}}
PG.addEventListener("change",e=>{let c=e.target;if(c.matches("input[data-td-k]")){let r=findIt(c.dataset.tdK);if(!r){redraw();return}let x=r.x||r.it;if(!setDone([x],c.checked))c.checked=!c.checked;else redraw(`input[data-td-k="${CSS.escape(x.k)}"]`)}
 else if(c.matches("input[data-td-all]")){let r=findIt(c.dataset.tdAll);if(!r){redraw();return}if(!setDone(r.it.subs,c.checked))c.checked=!c.checked;else redraw(`input[data-td-all="${CSS.escape(r.it.k)}"]`)}
 else if(c.matches("select[data-td-fq]")){let k=c.dataset.tdFq,r=findIt(k);if(!r||!requireProject()){redraw();return}let x=r.x||r.it,v=c.value,t=tw();if(!t.freq)t.freq={};
  if(v===(x.def||"once"))delete t.freq[k];else t.freq[k]=v;
  /* tek seferlikten yinelenene geçen ve daha önce yapılmış görevin ilk yapılışı geçmişe yazılır */
  let D=t.done[k];if(D&&v!=="once"&&!Array.isArray(D.log))D.log=[D.d];tidy();save();redraw(`select[data-td-fq="${CSS.escape(k)}"]`)}});
PG.addEventListener("input",e=>{if(e.target.id==="tdQ"){TD.q=e.target.value;let l=document.getElementById("tdList");if(l)l.innerHTML=list(build())}});
PG.addEventListener("keydown",e=>{if(e.target.id==="tdQ"&&e.key==="Escape"&&TD.q){TD.q="";e.target.value="";let l=document.getElementById("tdList");if(l)l.innerHTML=list(build())}});
PG.addEventListener("click",e=>{let b=e.target.closest("button");if(!b||!PG.contains(b))return;let d=b.dataset;
 if(d.tdF){TD.f=d.tdF;redraw()}
 else if(d.tdArea){TD.a=TD.a===d.tdArea?"all":d.tdArea;redraw()}
 else if(d.tdSec)goToSection(d.tdSec)
 else if(d.tdGo){let [s,f]=d.tdGo.split("|");goToField(s,f)}
 else if(d.tdLog){let r=findIt(d.tdLog);if(!r||!requireProject())return;mark(r.x||r.it,true);tidy();save();redraw(`[data-td-log="${CSS.escape(d.tdLog)}"]`)}
 else if(d.tdEv){let k=d.tdEv;if(!requireProject()||!EVN[k])return;if(!confirm(`“${EVN[k][0]}” kaydedilsin mi? ${PER[k][0].toLocaleLowerCase("tr")} yapılan görevler yeniden açılır.`))return;let t=tw();if(!t.ev)t.ev={};(t.ev[k]=t.ev[k]||[]).push(stamp());save();redraw()}
 else if(d.tdAct==="md")mkSave(todoMd(),"YAPILACAKLAR-"+slug()+".md","text/markdown;charset=utf-8");
 else if(d.tdAct==="ics")mkSave(todoIcs(),"YAPILACAKLAR-"+slug()+".ics","text/calendar;charset=utf-8");
 else if(d.tdAct==="copy"){let t=todoMd();(navigator.clipboard?navigator.clipboard.writeText(t):Promise.reject()).then(()=>note(b,"Kopyalandı"),()=>note(b,"Kopyalanamadı"))}
 else if(d.tdAct==="clear"){TD.q="";TD.f="all";TD.a="all";redraw()}
 else if(d.tdAct==="reset"){if(!requireProject())return;if(confirm("Bütün görevlerin işaretleri, yapılış geçmişi ve sıklık değişiklikleri kaldırılsın mı? Kararlar değişmez.")){delete state.todo;save();redraw()}}});
const slug=()=>(typeof exSlug==="function"&&exSlug(pname()))||"proje";
function goToSection(id){showPage("config");if(typeof closeNav==="function")closeNav();active=id;openSection=id;activeFieldId=null;showAll=false;renderConfig();window.scrollTo(0,0)}
function note(b,t){let o=b.textContent;b.textContent=t;setTimeout(()=>{b.textContent=o},1400)}

/* ---------- YAPILACAKLAR.md ---------- */
const STW={open:"",done:"",changed:" _(karar değişti, yeniden kontrol edin)_",due:" **(zamanı geldi)**",late:" **(gecikti)**"};
function recMd(x){if(!x.per)return "";let P=PER[x.per];return ` ↻ ${P[0]}${x.last?` · son ${x.last}${x.next?` · sonraki ${x.next}`:""}`:" · henüz yapılmadı"}`}
function todoMd(){let T=build(),L=allItems(T),S=stats(L),ck=st=>st==="done"?"[x]":"[ ]",md=`# ${pname()} — Yapılacaklar\n\n> Cortex Configurator ile üretildi · ${today()} · ${S.a} görev · kurulum ${S.d}/${S.a} (%${S.p})${S.r?` · ${S.r} yinelenen görev (${S.ok} güncel, ${S.due} zamanı geldi, ${S.late} gecikti)`:""}${S.c?` · ${S.c} görevin kararı işaretlendikten sonra değişti`:""}.\n> Görevler projede verilen kararlardan türetildi. Ayrıntılı kurallar CLAUDE-TALIMATLARI.md'dedir; bir görevi uyguladıktan sonra işaretleyin. ↻ işaretli görevler yinelenir.\n`;
 if(!L.length)return md+"\nHenüz karar verilmedi.\n";
 T.forEach(A=>{let s=stats(areaItems(A));md+=`\n## ${A.n?A.n+". ":""}${A.t} (${s.d}/${s.a})\n`;
  A.G.forEach(g=>{if(g.name)md+=`\n### ${A.a==="project"?"Faz: ":""}${g.name}\n`;
   g.S.forEach(x=>{md+=`\n${g.name?"####":"###"} ${x.num||x.s.code} ${x.s.name}\n\n`;
    x.I.forEach(it=>{md+=`- ${ck(it.st)} **${it.num?it.num+" ":""}${it.t}** — ${it.sum}${it.subs.length?STW[it.st]:STW[it.st]+recMd(it)}\n`;
     it.subs.forEach(o=>{md+=`  - ${ck(o.st)} ${o.t}${STW[o.st]}${recMd(o)}${o.r?` — ${o.r}`:""}\n`});
     if(!it.subs.length&&it.r)md+=`  - Kural: ${it.r}\n`;
     if(it.ag.length)md+=`  - Sorumlu ajan: ${it.ag.map(a=>a.name+(a.on?"":" (projede değil)")).join(", ")}\n`})})})});
 let R=[];L.forEach(it=>leaves(it).forEach(x=>{if(x.per)R.push([it,x])}));
 if(R.length){md+=`\n## Bakım takvimi\n\n| Görev | Sıklık | Son yapılış | Sonraki | Durum | Yapılış |\n|---|---|---|---|---|---|\n`;
  const ST={open:"Henüz yapılmadı",done:"Güncel",changed:"Karar değişti",due:"Zamanı geldi",late:"Gecikti"},c=t=>String(t).replace(/\|/g,"/");
  R.forEach(([it,x])=>{md+=`| ${c((it.num?it.num+" ":"")+it.t+(x.sub?" › "+x.t:""))} | ${PER[x.per][0]} | ${x.last||"—"} | ${x.next||(PER[x.per][2]?"olaydan sonra":"—")} | ${ST[x.st]} | ${x.log.length} |\n`});
  let H=R.filter(([,x])=>x.log.length);if(H.length){md+=`\n### Yapılış geçmişi\n\n`;H.forEach(([it,x])=>{md+=`- **${(it.num?it.num+" ":"")+it.t+(x.sub?" › "+x.t:"")}:** ${x.log.join(", ")}\n`})}
  Object.keys(EVN).forEach(k=>{let e=evs(k);if(e.length)md+=`\n_${EVN[k][0]} kayıtları: ${e.join(", ")}_\n`})}
 return md}

/* ---------- YAPILACAKLAR.ics (yalnız takvimli yinelenen görevler) ---------- */
function icsEsc(t){return String(t||"").replace(/\\/g,"\\\\").replace(/;/g,"\\;").replace(/,/g,"\\,").replace(/\r?\n/g,"\\n")}
function fold(l){let out=[],cur="",n=0,enc=new TextEncoder();for(const ch of l){let b=enc.encode(ch).length;if(n+b>(out.length?74:75)){out.push(cur);cur="";n=0}cur+=ch;n+=b}out.push(cur);return out.join("\r\n ")}
function todoIcs(){let L=allItems(build()),t=today(),now=new Date().toISOString().replace(/[-:]/g,"").replace(/\.\d+Z$/,"Z"),ev=[],pn=pname();
 L.forEach(it=>leaves(it).forEach(x=>{let P=x.per&&PER[x.per];if(!P||!P[1])return;let start=x.next&&x.next>t?x.next:t,d=start.replace(/-/g,""),end=addP(start,{d:1}).replace(/-/g,""),
  rr=P[1].d?`FREQ=WEEKLY;INTERVAL=${P[1].d/7}`:P[1].m%12===0?`FREQ=YEARLY;INTERVAL=${P[1].m/12}`:`FREQ=MONTHLY;INTERVAL=${P[1].m}`,
  title=`${pn}: ${it.t}${x.sub?" › "+x.t:""}`,desc=[`${P[0]} yinelenen görev (${(it.num?it.num+" ":"")+it.t}).`,x.sub&&x.r?x.r:it.r,x.last?`Son yapılış: ${x.last}.`:"Henüz yapılmadı.","Yapınca Cortex Configurator › Yapılacaklar'da işaretleyin."].filter(Boolean).join("\n");
  ev.push(["BEGIN:VEVENT",`UID:${fp(pn)}-${x.k.replace(/[^A-Za-z0-9_-]/g,"_")}@cortex.onurkenar.com`,`DTSTAMP:${now}`,`DTSTART;VALUE=DATE:${d}`,`DTEND;VALUE=DATE:${end}`,`RRULE:${rr}`,`SUMMARY:${icsEsc(title)}`,`DESCRIPTION:${icsEsc(desc)}`,"TRANSP:TRANSPARENT","BEGIN:VALARM","ACTION:DISPLAY",`DESCRIPTION:${icsEsc(title)}`,"TRIGGER:PT9H","END:VALARM","END:VEVENT"])}));
 return ["BEGIN:VCALENDAR","VERSION:2.0","PRODID:-//Cortex Configurator//Yapilacaklar//TR","CALSCALE:GREGORIAN","METHOD:PUBLISH",`X-WR-CALNAME:${icsEsc(pn+" — Bakım takvimi")}`,...ev.flat(),"END:VCALENDAR"].map(fold).join("\r\n")+"\r\n"}
window.todoMd=todoMd;window.todoIcs=todoIcs;window.todoStats=()=>stats(allItems(build()));
window.todoRecurring=()=>{let n=0;allItems(build()).forEach(it=>leaves(it).forEach(x=>{if(x.per&&PER[x.per][1])n++}));return n};

nav();
const _rp=typeof renderProgress==="function"?renderProgress:null;
if(_rp)renderProgress=function(){let r=_rp.apply(this,arguments);if(isOn()&&!PG.contains(document.activeElement))render();return r};
})();
