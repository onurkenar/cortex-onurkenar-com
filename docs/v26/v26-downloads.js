/* Dışa Aktar sayfası (2026-11-15, kullanıcı istekleri: "İndirmeler ekranını teknik bilgisi olmayan işletme sahipleri için
   yeniden düzenle" + Claude Design prototipi; "json indir, claude promptu gibi tüm dışa aktarmaları ve genel promptları Dışa
   Aktar menüsü altında topla"). Önceki sürüm: Dashboard › İndirmeler (2026-11-12).
   - Sayfa #dlxPage (showPage("dlx"), DLX.go(paket)): modül şeridinde ve çekmecede "Dışa Aktar" (8. İçerik Planlama'dan hemen sonra); üstte karar durumu kutusu
     ("X / Y karar", "Eksikleri gör" → Modül · Bölüm · Karar listesi, tıklayınca karara gider), solda paket listesi (hazır/toplam
     + ilerleme; ≤ 900 px yatay şerit), sağda seçili paketin kartı (eksik karar çipleri, dosya satırları: Önizle / Kopyala / İndir,
     hazır olmayanda "Bu projede yok" + gerekçe + düzeltme bağlantısı, isteğe bağlı satırda işaret kutusu; altta zip adı, içerik
     özeti ve "Paketi zip olarak indir").
   - Üst şerit: "Claude Promptu" düğmesi "Dışa Aktar" olur ve bu sayfayı açar; "JSON İndir" ve "Ajanları İndir" gizlenir (paketlerde),
     ⋯ menüsünden de kalkar. "JSON İçe Aktar" kalır. exportBtn.click() çağıranlar Tam yedek paketini açar.
   - Dashboard'un sonunda yalnız kısa özet kartı (#dlPkgs) kalır.
   - Yeni dosyalar: Google / Meta / Yapay Zekâ Kararları JSON'u (part "google" | "meta" | "ai"; kullanıcı kararı); JSON İçe Aktar bu
     parçaları da okur (yalnız o modülün seçimleri değişir). Diğer bütün dosya içerikleri var olan üreticilerden, değişmeden gelir
     (exData, projectFileData, prMd, prStart, todoMd, todoIcs, agZipFiles, mcJson, mkJson, dsConfig, dsTokensCss, pzPf, rgFiles,
     auPrompt, mkMarketingPrompt, gg/mt/yzSetupMd, cvIcs). İçerik yalnız Önizle / Kopyala / İndir / zip'te üretilir; zip boyutu
     yalnız Dışa Aktar sayfası açıkken, seçili paket için boşta hesaplanır. Zip içi tarihler zipStore'da sabit (0).
   Ad "dlRender" kullanılmaz (tasarım kütüphanesinin layout önizleme işlevi; çakışma 2026-11-12). Global adlar: DLX, dlPackages,
   dlZip, dlPkgRender, dlAll, dlDebug.
   Kaynak docs/v26/v26-downloads.js → docs/v26/indirmeler_ekle.py */
(()=>{
const has=n=>typeof window[n]==="function";
const slug=()=>{try{return (typeof exBrand==="function"&&exBrand())||"proje"}catch(e){return "proje"}};
const host=()=>String(state.domain_name||"").trim().replace(/^[a-z]+:\/\//i,"").replace(/[\/?#].*$/,"").replace(/^www\./i,"").toLocaleLowerCase("tr").replace(/[^a-z0-9.-]+/g,"-").replace(/^[-.]+|[-.]+$/g,"")||slug();
const J=o=>JSON.stringify(o,null,2);
const pfBase=()=>(typeof pfFileName==="function"&&pfFileName().replace(/\.json$/,""))||slug();

/* ---------- kararlar ---------- */
const AREAS=[["common","Ortak Bilgiler"],["project","Kararlar"],["marketing","Pazarlama"],["audit","SEO Denetimi"],["google","Google Servisleri"],["meta","Meta Servisleri"],["ai","Yapay Zekâ"],["plan","İçerik Planlama"]];
const ALB=Object.fromEntries(AREAS);
function fieldsOf(a){try{return F.filter(f=>shown(f)&&navF(f)&&AREA(SI[f.section])===a)}catch(e){return []}}
function fieldsIn(areas){return areas.flatMap(fieldsOf)}
function designFields(){try{let ids=["page_design_style","secondary_design_styles","page_layout_approach"].concat(typeof DS_NEWF!=="undefined"?DS_NEWF:[],typeof DS_PARAMS!=="undefined"?DS_PARAMS:[]),secs=new Set(ids.map(id=>FI[id]&&FI[id].section).filter(Boolean));return F.filter(f=>secs.has(f.section)&&shown(f)&&navF(f))}catch(e){return []}}
const decN=areas=>fieldsIn(areas).filter(isset).length;
function goF(f){if(!f)return;goToField(f.section,f.id)}
function goArea2(areas){let L=fieldsIn(areas);goF(L.find(f=>!isset(f))||L[0])}
function goSec(id){showPage("config");if(typeof closeNav==="function")closeNav();active=id;openSection=id;activeFieldId=null;showAll=false;renderConfig();window.scrollTo(0,0)}
const agN=()=>{try{return agOn("dev").length}catch(e){return 0}};
const skN=()=>{try{return Object.keys(skSlugs()).length}catch(e){return 0}};

/* ---------- modül JSON'u (Google / Meta / Yapay Zekâ) ---------- */
const MODP={
 google:{t:"Google Servisleri Kararları",f:"google-kararlari",d:"Google Servisleri kararları (Tag Manager, Analytics 4, Consent Mode, Search Console, Ads, Merchant Center, İşletme Profili, Looker Studio), kuralları ve kurulum talimatı. Ortak Bilgiler'in bir kopyası bağlam olarak eklenir.",pf:()=>ggPf()},
 meta:{t:"Meta Servisleri Kararları",f:"meta-kararlari",d:"Meta Servisleri kararları (işletme portföyü, Facebook Sayfası, Instagram, WhatsApp Business, Meta Pikseli ve Conversions API, reklam hesabı, katalog), kuralları ve kurulum talimatı. Ortak Bilgiler'in bir kopyası bağlam olarak eklenir.",pf:()=>mtPf()},
 ai:{t:"Yapay Zekâ Kararları",f:"yapay-zeka-kararlari",d:"Yapay zekâ görünürlüğü ve ayarları kararları, kuralları ve talimatı. Ortak Bilgiler'in bir kopyası bağlam olarak eklenir.",pf:()=>yzPf()}};
const PFX={gg:"google",mt:"meta",yz:"ai"};
function modOwn(k){let f=FI[k];if(f)return AREA(SI[f.section]);let m=/^(gg|mt|yz)_/.exec(k);return m?PFX[m[1]]:null}
function modState(a){let o={};Object.keys(state).forEach(k=>{if(k!=="fieldAgents"&&k!=="fieldNotes"&&modOwn(k)===a)o[k]=state[k]});
 ["fieldAgents","fieldNotes"].forEach(n=>{let fa=state[n];if(fa&&typeof fa==="object"){let x={};Object.keys(fa).forEach(k=>{if(modOwn(k)===a)x[k]=fa[k]});if(Object.keys(x).length)o[n]=x}});return o}
function modData(a){renderRules();let P=MODP[a];return {format:"web-project-configurator",version:25,part:a,partName:P.t,description:P.d,projectName:String(state.project_name||"").trim(),brandName:String(state.mk_brand_name||"").trim(),savedAt:new Date().toISOString(),state:modState(a),common:exCommon(),rules:{sections:exRules([a])},...P.pf()}}
const modName=a=>slug()+"-"+MODP[a].f+".json";
function modImport(d,fn){let a=d.part,P=MODP[a];if(!d.state||typeof d.state!=="object"||Array.isArray(d.state))throw new Error("Bu dosya bir proje yapılandırması değil.");
 let empty=v=>v===undefined||v===null||(Array.isArray(v)?!v.length:typeof v==="object"?!Object.keys(v).length:String(v).trim()==="");
 if(Object.keys(state).some(k=>k!=="fieldAgents"&&k!=="fieldNotes"&&modOwn(k)===a&&!empty(state[k]))&&!confirm("“"+fn+"” dosyasındaki "+P.t+" mevcut "+P.t.toLocaleLowerCase("tr")+" seçimlerinizin yerini alacak; diğer seçimleriniz korunur. Devam edilsin mi?"))return false;
 let s={...state},fa={...(s.fieldAgents||{})},fnn={...(s.fieldNotes&&typeof s.fieldNotes==="object"?s.fieldNotes:{})};
 Object.keys(s).forEach(k=>{if(k!=="fieldAgents"&&k!=="fieldNotes"&&modOwn(k)===a)delete s[k]});Object.keys(fa).forEach(k=>{if(modOwn(k)===a)delete fa[k]});Object.keys(fnn).forEach(k=>{if(modOwn(k)===a)delete fnn[k]});
 Object.entries(d.state).forEach(([k,v])=>{if(k==="fieldAgents"){if(v&&typeof v==="object")Object.keys(v).forEach(x=>{if(modOwn(x)===a)fa[x]=v[x]})}else if(k==="fieldNotes"){if(v&&typeof v==="object")Object.keys(v).forEach(x=>{if(modOwn(x)===a&&typeof v[x]==="string")fnn[x]=v[x]})}else if(modOwn(k)===a)s[k]=v});
 if(Object.keys(fa).length)s.fieldAgents=fa;else delete s.fieldAgents;if(Object.keys(fnn).length)s.fieldNotes=fnn;else delete s.fieldNotes;
 if(d.common&&typeof d.common==="object")Object.entries(d.common).forEach(([k,v])=>{let f=FI[k];if(f&&AREA(SI[f.section])==="common"&&empty(s[k]))s[k]=v});
 state=pfName(s,d,fn);save();renderConfig();renderRules();return true}
if(typeof exImport==="function"){const _ei=exImport;exImport=function(d,fn){if(d&&typeof d==="object"&&MODP[d.part])return modImport(d,fn);return _ei.apply(this,arguments)}}

/* ---------- katalog ----------
   Satır: k anahtar, t ad, ty rozet (MD / JSON / CSS / ZIP / PROMPT / ICS / KLASÖR), d açıklama, name() indirme adı, yol() zip içindeki
   yol (yoksa name()), gen() metin ya da files() dosya listesi (klasör / zip satırı), ok() hazır mı, why() gerekçe, fix {t, go} düzeltme,
   st() durum, copy kopyalanabilir mi, opt isteğe bağlı (işaret kutusu; varsayılan boş, işaretlenirse zip'e girer), dir klasör. */
const noDec="Bu modülde henüz karar verilmedi.";
const areaRow=(areas,lbl)=>({ok0:()=>decN(areas)>0,why:()=>noDec,fix:{t:lbl+" kararlarını ver",go:()=>goArea2(areas)}});
const R={
 md:{k:"md",t:"CLAUDE-TALIMATLARI.md",ty:"MD",d:"Fazlara bölünmüş ana talimat dosyası. Claude Code'da proje köküne konur; claude.ai'da projeye ya da sohbete dosya olarak eklenir.",name:()=>"CLAUDE-TALIMATLARI.md",gen:()=>prMd(),ok:()=>has("prMd"),copy:true},
 todo:{k:"todo",t:"YAPILACAKLAR.md",ty:"MD",d:"Verilen kararlardan oluşan, işaretlenebilir görev listesi.",name:()=>"YAPILACAKLAR.md",gen:()=>todoMd(),ok:()=>has("todoMd"),copy:true},
 ics:{k:"ics",t:"YAPILACAKLAR.ics",ty:"ICS",d:"Yinelenen görevlerin bakım takvimi; Google Takvim, Outlook ya da Apple Takvim'e aktarılır.",name:()=>"YAPILACAKLAR.ics",gen:()=>todoIcs(),ok:()=>has("todoIcs")&&typeof todoRecurring==="function"&&todoRecurring()>0,why:()=>"Yinelenen görev yok.",fix:{t:"Yapılacaklar'ı aç",go:()=>window.todoGo&&todoGo()}},
 start:{k:"start",t:"Başlatma promptu",ty:"PROMPT",d:"Claude'a yapıştırılan kısa prompt: talimat dosyasını fazlar hâlinde uygulatır, her fazın sonunda onayınızı bekler.",name:()=>"BASLATMA-PROMPTU.md",gen:()=>prStart(),ok:()=>has("prStart"),copy:true},
 master:{k:"master",t:"Claude promptu (tam)",ty:"PROMPT",d:"Proje Kuralları'nın tek parça hâli; talimat dosyasının yerine kullanılabilir.",name:()=>"CLAUDE-PROMPTU.md",gen:()=>{renderRules();return master.value},ok:()=>true,copy:true},
 project:{k:"project",t:"Proje Kararları",ty:"JSON",d:"Proje ve Ortak Bilgiler kararları, kurallar, ajanlar, skill'ler ve Claude promptu.",name:()=>exName("project"),gen:()=>J(exData("project")),ok:()=>has("exData"),copy:true},
 agents:{k:"agents",t:"Ajanlar",ty:"KLASÖR",dir:".claude/agents/",d:"Projede seçili geliştirme ajanları; proje köküne açılır, Claude Code'da /agents ile görünür.",name:()=>pfBase()+"-claude-agents.zip",yol:()=>".claude/agents/",files:()=>agZipFiles().filter(f=>f.name.startsWith(".claude/agents/")),ok:()=>has("agZipFiles")&&agN()>0,why:()=>"Geliştirme ajanı seçilmedi.",fix:{t:"Ajan seçimini yap",go:()=>{showPage("agents");ksGo("dev")}},st:()=>agN()?agN()+" ajan":""},
 skills:{k:"skills",t:"Skill'ler",ty:"KLASÖR",dir:".claude/skills/",d:"Seçili ajanların kullandığı skill dosyaları.",name:()=>pfBase()+"-claude-skills.zip",yol:()=>".claude/skills/",files:()=>agZipFiles().filter(f=>f.name.startsWith(".claude/skills/")),ok:()=>has("agZipFiles")&&agN()>0&&skN()>0,why:()=>agN()?"Skill seçilmedi.":"Geliştirme ajanı seçilmedi.",fix:{t:"Skill seçimini yap",go:()=>{showPage("agents");ksGo(agN()?"skills":"dev")}},st:()=>skN()?skN()+" skill":""},
 mcp:{k:"mcp",t:".mcp.json",ty:"JSON",d:"Seçilen MCP bağlantılarının Claude Code yapılandırması.",name:()=>".mcp.json",gen:()=>mcJson(),ok:()=>has("mcJson")&&has("mcOn")&&mcOn().some(x=>typeof mcCfg!=="function"||mcCfg(x)),why:()=>"MCP bağlantısı seçilmedi.",fix:{t:"MCP bağlantısını seç",go:()=>{showPage("agents");ksGo("mcp")}},copy:true,st:()=>has("mcOn")&&mcOn().length?mcOn().length+" bağlantı":""},
 dsjson:{k:"dsjson",t:"Tasarım yapılandırması",ty:"JSON",d:"Tasarım sistemi kararları: stil, layout ve parametreler.",name:()=>dsFileBase()+"-tasarim-yapilandirmasi.json",gen:()=>J(dsConfig()),ok:()=>has("dsActive")&&dsActive(),why:()=>"Tasarım kararı verilmedi.",fix:{t:"Tasarım kararını ver",go:()=>goF(FI.page_design_style)},copy:true},
 dscss:{k:"dscss",t:"Tasarım token'ları",ty:"CSS",d:"Tasarım kararlarından üretilen CSS değişkenleri; stil dosyasının başına eklenir.",name:()=>dsFileBase()+"-tasarim-tokenlari.css",gen:()=>dsTokensCss(),ok:()=>has("dsActive")&&dsActive(),why:()=>"Tasarım kararı verilmedi.",fix:{t:"Tasarım kararını ver",go:()=>goF(FI.page_design_style)},copy:true},
 panels:{k:"panels",t:"Panel ve portal mimarisi",ty:"JSON",d:"Panel envanteri, adresler, roller, modüller ve izolasyon.",name:()=>slug()+"-panel-mimarisi.json",gen:()=>J(pzPf().panelArchitecture),ok:()=>has("pzPf")&&!!(pzPf()||{}).panelArchitecture,why:()=>"Panel eklenmedi.",fix:{t:"Panel envanterini doldur",go:()=>goF(FI.panel_inventory)},copy:true},
 registry:{k:"registry",t:"Ajan Kaydı",ty:"ZIP",d:"AGENT_REGISTRY, SKILL_REGISTRY ve AGENT_ORGANIZATION_MAP dosyaları; paketin köküne açılır.",name:()=>slug()+"-ajan-kaydi.zip",yol:()=>"AGENT_REGISTRY.json · SKILL_REGISTRY.json · AGENT_ORGANIZATION_MAP.json",files:()=>Object.entries(rgFiles()).map(([name,data])=>({name,data})),ok:()=>has("rgFiles")&&!!state.registry,why:()=>"Ajan Kaydı oluşturulmadı.",fix:{t:"Ajan Kaydı'nı aç",go:()=>{showPage("agents");ksGo("registry")}}},
 mkjson:{k:"mkjson",t:"Pazarlama Kararları",ty:"JSON",d:"Pazarlama, Google, Meta, Yapay Zekâ ve İçerik Planlama kararları, kuralları ve pazarlama promptu.",name:()=>exName("marketing"),gen:()=>J(exData("marketing")),ok:()=>has("exData"),...areaRow(["marketing","google","meta","ai","plan"],"Pazarlama"),copy:true},
 mkprompt:{k:"mkprompt",t:"Pazarlama promptu",ty:"PROMPT",d:"İçerik üretecek Claude oturumu için marka, kitle, kanal ve içerik kuralları.",name:()=>"pazarlama-promptu-"+slug()+".md",gen:()=>mkMarketingPrompt(),ok:()=>has("mkMarketingPrompt"),...areaRow(["marketing"],"Pazarlama"),copy:true},
 mkplan:{k:"mkplan",t:"İçerik ve reklam planı verisi",ty:"JSON",d:"İçerik ve Reklam Planı şablonunun (icerik-plani-SABLON.html) veri dosyası.",name:()=>"veri."+mkBase()+".json",gen:()=>mkJson(),ok:()=>has("mkJson")&&has("mkBase"),...areaRow(["marketing","plan"],"Pazarlama"),copy:true},
 cvics:{k:"cvics",t:"İçerik takvimi",ty:"ICS",opt:true,d:"İçerik Planlama › Takvim'deki kayıtlar; takvim uygulamasına aktarılır.",name:()=>String((typeof mkT==="function"&&mkT("mk_prefix"))||"icerik").toLowerCase()+"-icerik-takvimi.ics",gen:()=>window.cvIcs(),ok:()=>typeof window.cvIcs==="function"&&typeof window.cvEvents==="function"&&window.cvEvents().length>0,why:()=>"Takvimde kayıt yok.",fix:{t:"Takvimi aç",go:()=>goSec("ip_calendar")}},
 aujson:{k:"aujson",t:"SEO Denetimi",ty:"JSON",d:"Denetim kararları, kontroller ve denetim promptu.",name:()=>exName("audit"),gen:()=>J(exData("audit")),ok:()=>has("exData"),...areaRow(["audit"],"SEO Denetimi"),copy:true},
 auprompt:{k:"auprompt",t:"SEO denetim promptu",ty:"PROMPT",d:"Yayındaki siteyi denetleyecek Claude oturumu için kapsam, kontroller ve rapor biçimi.",name:()=>"seo-denetimi-"+host()+".md",gen:()=>auPrompt(),ok:()=>has("auPrompt"),...areaRow(["audit"],"SEO Denetimi"),copy:true},
 ggmd:{k:"ggmd",t:"Google kurulum talimatı",ty:"MD",d:"Adım adım kurulum talimatı: bağlam, kimlikler, çalışma kuralları ve uygulama sırası.",name:()=>"google-kurulum-"+host()+".md",gen:()=>ggSetupMd(),ok:()=>has("ggSetupMd"),...areaRow(["google"],"Google"),copy:true},
 ggjson:{k:"ggjson",t:"Google kararları",ty:"JSON",d:"Google Servisleri kararları ve kuralları; JSON İçe Aktar ile yalnız bu bölüm geri yüklenir.",name:()=>modName("google"),gen:()=>J(modData("google")),ok:()=>has("exCommon"),...areaRow(["google"],"Google"),copy:true},
 mtmd:{k:"mtmd",t:"Meta kurulum talimatı",ty:"MD",d:"Adım adım kurulum talimatı: bağlam, kimlikler, çalışma kuralları ve uygulama sırası.",name:()=>"meta-kurulum-"+host()+".md",gen:()=>mtSetupMd(),ok:()=>has("mtSetupMd"),...areaRow(["meta"],"Meta"),copy:true},
 mtjson:{k:"mtjson",t:"Meta kararları",ty:"JSON",d:"Meta Servisleri kararları ve kuralları; JSON İçe Aktar ile yalnız bu bölüm geri yüklenir.",name:()=>modName("meta"),gen:()=>J(modData("meta")),ok:()=>has("exCommon"),...areaRow(["meta"],"Meta"),copy:true},
 yzmd:{k:"yzmd",t:"Yapay zekâ talimatı",ty:"MD",d:"Yapay zekâ görünürlüğü talimatı: bağlam, çalışma kuralları ve uygulama sırası.",name:()=>"yapay-zeka-"+host()+".md",gen:()=>yzSetupMd(),ok:()=>has("yzSetupMd"),...areaRow(["ai"],"Yapay Zekâ"),copy:true},
 yzjson:{k:"yzjson",t:"Yapay zekâ kararları",ty:"JSON",d:"Yapay Zekâ kararları ve kuralları; JSON İçe Aktar ile yalnız bu bölüm geri yüklenir.",name:()=>modName("ai"),gen:()=>J(modData("ai")),ok:()=>has("exCommon"),...areaRow(["ai"],"Yapay Zekâ"),copy:true},
 full:{k:"full",t:"Proje dosyası (tam yedek)",ty:"JSON",d:"Bütün seçimler tek dosyada; JSON İçe Aktar ile geri yüklenir.",name:()=>(typeof pfFileName==="function"&&pfFileName())||"web-project-config-v25.json",gen:()=>J(projectFileData()),ok:()=>has("projectFileData"),copy:true}};
/* Paketler: dir → "Tümünü zip olarak indir" klasörü (yoksa o pakete girmez: Claude Design ve Promptlar başka paketlerdeki dosyaları gösterir);
   zip → paket zip'inin adı (<marka>-<zip>-paketi.zip); areas / fields → paketin eksik kararları. */
const PK=[
 {k:"claude",t:"Claude Code proje paketi",d:"Siteyi geliştirecek Claude oturumu için talimat dosyası, promptlar, proje kararları, ajan ve skill dosyaları; projede seçildiyse MCP, tasarım ve panel yapılandırmaları.",note:"Nasıl kullanılır: CLAUDE-TALIMATLARI.md'yi proje köküne koyun, başlatma promptunu Claude'a yapıştırın. Claude her fazın sonunda rapor verir ve onayınızı bekler.",dir:"1-claude-code",zip:"claude-code",areas:["project","common"],items:["md","todo","ics","start","master","project","agents","skills","mcp","dsjson","dscss","panels","registry"]},
 {k:"design",t:"Claude Design paketi",d:"Arayüz tasarımı için tasarım kararları ve CSS token'ları. Aynı dosyalar Claude Code paketinde de vardır.",zip:"claude-design",fields:designFields,items:["dsjson","dscss"]},
 {k:"prompts",t:"Promptlar",d:"Projenin ürettiği bütün promptlar ve talimatlar bir arada: kopyalayıp ilgili Claude oturumuna yapıştırın. Dosyalar kendi paketlerinde de vardır.",zip:"promptlar",items:["start","master","md","mkprompt","auprompt","ggmd","mtmd","yzmd"]},
 {k:"marketing",t:"Pazarlama paketi",d:"Pazarlama kararlarının dosyası, içerik üretimi için pazarlama promptu ve içerik ve reklam planının veri dosyası.",dir:"2-pazarlama",zip:"pazarlama",areas:["marketing","plan"],items:["mkjson","mkprompt","mkplan","cvics"]},
 {k:"audit",t:"SEO Denetimi paketi",d:"Yayındaki siteyi denetleyecek Claude oturumu için denetim promptu ve kararlar.",dir:"3-seo-denetimi",zip:"seo-denetimi",areas:["audit"],items:["aujson","auprompt"]},
 {k:"google",t:"Google Servisleri paketi",d:"Tag Manager, Analytics 4, Consent Mode, Search Console, Ads, Merchant Center, İşletme Profili ve Looker Studio kurulumu.",dir:"4-google",zip:"google",areas:["google"],items:["ggmd","ggjson"]},
 {k:"meta",t:"Meta Servisleri paketi",d:"İşletme portföyü, Facebook Sayfası, Instagram, WhatsApp, Meta Pikseli / Conversions API, reklam hesabı ve katalog kurulumu.",dir:"5-meta",zip:"meta",areas:["meta"],items:["mtmd","mtjson"]},
 {k:"ai",t:"Yapay Zekâ paketi",d:"ChatGPT'de işletme, yapay zekâ platformları, tarayıcı izinleri, sitedeki asistan ve ölçüm talimatı.",dir:"6-yapay-zeka",zip:"yapay-zeka",areas:["ai"],items:["yzmd","yzjson"]},
 {k:"backup",t:"Tam yedek",d:"Bütün seçimleri tek dosyada taşıyan proje dosyası. Başka bir bilgisayarda ya da tarayıcıda JSON İçe Aktar ile açılır.",dir:"7-yedek",zip:"yedek",items:["full"]}];
PK.forEach(p=>p.rows=p.items.map(k=>R[k]));
const pk=k=>PK.find(p=>p.k===k);
const OPT={};
const uid=(p,x)=>p.k+"."+x.k;
const rowOf=u=>{let [a,b]=String(u).split(".");let p=pk(a);return p&&{p,x:p.rows.find(x=>x.k===b)}};
const ok=x=>{try{return !!x.ok()&&(!x.ok0||!!x.ok0())}catch(e){return false}};
const inZip=(p,x)=>ok(x)&&(!x.opt||!!OPT[uid(p,x)]);
const st=x=>{try{return x.st?x.st():""}catch(e){return ""}};
const why=x=>{try{return x.why?x.why():"Bu projede üretilmiyor."}catch(e){return ""}};
const nm=x=>{try{return x.name()}catch(e){return x.t}};
const yol=x=>{try{return x.yol?x.yol():nm(x)}catch(e){return x.t}};
const text=x=>String(x.gen()||"");
const files=x=>x.files?x.files():[{name:nm(x),data:text(x)}];
function pkFiles(p,prefix,all){let o=[];p.rows.filter(x=>all?ok(x)&&!x.opt:inZip(p,x)).forEach(x=>files(x).forEach(f=>o.push({name:(prefix||"")+f.name,data:f.data})));return o}
const zipName=p=>slug()+"-"+p.zip+"-paketi.zip";
const pkMiss=p=>{try{return (p.fields?p.fields():p.areas?fieldsIn(p.areas):[]).filter(f=>!isset(f))}catch(e){return []}};

/* ---------- dosya işlemleri ---------- */
function saveBlob(blob,name){let a=document.createElement("a"),u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500)}
function zip(list,name){if(!list.length)return;saveBlob(zipStore(list),name)}
const MIME={JSON:"application/json",CSS:"text/css",ICS:"text/calendar"};
function toast(msg,err){let b=document.getElementById("dlxToast");if(!b)return;b.textContent=msg;b.className="dlxToast show"+(err?" err":"");clearTimeout(toast.t);toast.t=setTimeout(()=>b.className="dlxToast",err?5000:2400)}
function guard(fn){try{return fn()}catch(e){console.error("dışa aktarma",e);toast("Dosya üretilemedi: "+(e&&e.message||e),1)}}
function dlRow(p,x){guard(()=>{if(x.files)zip(x.files(),nm(x));else saveBlob(new Blob([text(x)],{type:MIME[x.ty]||"text/markdown"}),nm(x));toast(nm(x)+" indirildi.")})}
async function copyText(t){try{await navigator.clipboard.writeText(t);return true}catch(e){try{let ta=document.createElement("textarea");ta.value=t;ta.style.cssText="position:fixed;opacity:0;left:0;top:0";document.body.appendChild(ta);ta.select();let r=document.execCommand("copy");ta.remove();return r}catch(e2){return false}}}
function dlZip(k){let p=pk(k);if(!p)return;guard(()=>{let L=pkFiles(p,"");if(!L.length){toast("Bu pakette indirilecek dosya yok.",1);return}zip(L,zipName(p));toast(p.t+" indirildi ("+L.length+" dosya).")})}
function readme(){let d=new Date().toLocaleDateString("sv-SE"),P=PK.filter(p=>p.dir);return `# ${String(state.project_name||"").trim()||"Proje"} — indirmeler\n\nCortex Configurator ile ${d} tarihinde üretildi. Her klasör bir pakettir:\n\n`+P.map(p=>`## ${p.dir}\n${p.d}\n\n`+p.rows.filter(x=>ok(x)&&!x.opt).map(x=>`- **${x.t}** (${x.dir||nm(x)}): ${x.d}`).join("\n")).join("\n\n")+`\n\nDosyalar seçimlerin indirme anındaki hâlidir; seçim değişince Dışa Aktar sayfasından yeniden alın.\n`}
function dlAll(){guard(()=>{let L=[];PK.filter(p=>p.dir).forEach(p=>L.push(...pkFiles(p,p.dir+"/",true)));L.unshift({name:"OKU-BENI.md",data:readme()});zip(L,slug()+"-tum-indirmeler.zip");toast("Bütün paketler indirildi ("+(L.length-1)+" dosya).")})}
const kb=n=>n<1024?"1 KB'tan küçük":(n/1024<10?(n/1024).toFixed(1).replace(".",","):Math.round(n/1024))+" KB";

/* ---------- sayfa ---------- */
const PG=document.createElement("section");PG.id="dlxPage";PG.setAttribute("aria-label","Dışa Aktar");
configPage.parentNode.insertBefore(PG,configPage);
const isOn=()=>PG.classList.contains("active");
let SEL="claude",PREV=null,MISS=false,SIG="",SIZE_T=0;
function stat(){let L=AREAS.map(([a,t])=>{let V=fieldsOf(a);return {a,t,V,n:V.filter(isset).length}});let N=L.reduce((s,x)=>s+x.V.length,0),n=L.reduce((s,x)=>s+x.n,0);return {L,N,n,miss:N-n}}
const pct=(n,N)=>N?Math.round(n/N*100):0;
const crumb=f=>{let s=SI[f.section]||{};return (ALB[AREA(s)]||"")+" · "+(s.name||"")+" · "+(f.label||f.id)};
function statH(S){let m=S.miss,p=pct(S.n,S.N),nm0=!String(state.project_name||"").trim();
 let list=MISS&&m?`<div class="dlxMiss" id="dlxMiss">${S.L.filter(x=>x.n<x.V.length).map(x=>{let M=x.V.filter(f=>!isset(f)),sh=M.slice(0,40);return `<div class="dlxMissG"><h3>${E(x.t)} <small>${M.length} eksik</small></h3><ul>${sh.map(f=>`<li><button type="button" class="dlxMissI" data-a="go" data-f="${E(f.id)}">${E(crumb(f))}</button></li>`).join("")}</ul>${M.length>sh.length?`<button type="button" class="linkBtn" data-a="area" data-ar="${x.a}">ve ${M.length-sh.length} karar daha — ${E(x.t)}'a git →</button>`:""}</div>`}).join("")}</div>`:"";
 return `<section class="dlxStat${m?" warn":" ok"}" aria-labelledby="dlxStatT"><div class="dlxStatTx"><b id="dlxStatT">${m?m+" karar eksik":"Bütün kararlar verildi"}</b><span>${m?"Şimdi indirebilirsiniz. Eksik kararlara bağlı dosyalar “Bu projede yok” olarak işaretlenir; kararı verdikten sonra yeniden indirin.":"İndirdiğiniz dosyalar projenin tamamını yansıtır."}${nm0?" Proje adı yazılmadı.":""}</span></div><div class="dlxProg"><div class="dlxProgT"><b>${S.n} / ${S.N} karar</b><span>%${p}</span></div><div class="dlxBar" role="progressbar" aria-label="Verilen kararlar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${p}"><i style="width:${p}%"></i></div></div>${m?`<button type="button" class="btn dlxMissBtn" data-a="miss" aria-expanded="${MISS}" aria-controls="dlxMiss">${MISS?"Eksikleri gizle":"Eksikleri gör"} (${m})</button>`:""}${list}</section>`}
function cnt(p){let N=p.rows.length,n=p.rows.filter(ok).length;return [n,N]}
function listH(){return `<nav class="dlxList" aria-label="Paketler">${PK.map(p=>{let [n,N]=cnt(p),on=p.k===SEL;return `<button type="button" class="dlxPk${on?" on":""}${n===N?" full":""}" data-a="sel" data-p="${p.k}"${on?' aria-current="true"':""}><span class="dlxPkT">${E(p.t)}</span><span class="dlxPkN">${n}/${N}</span><span class="dlxPkBar" aria-hidden="true"><i style="width:${pct(n,N)}%"></i></span></button>`}).join("")}</nav>`}
function rowH(p,x){let u=uid(p,x),on=ok(x),s=on?st(x):"",multi=!!x.files,tyc=x.ty==="KLASÖR"?"dir":x.ty.toLowerCase();
 let cb=x.opt?`<label class="dlxOpt"><input type="checkbox" data-a="opt" data-u="${u}"${OPT[u]?" checked":""}${on?"":" disabled"}><span class="sr">${E(x.t)} zip'e eklensin</span></label>`:"";
 let act=on?`<div class="dlxAct"><button type="button" class="linkBtn dlxPv" data-a="prev" data-u="${u}" aria-expanded="${PREV===u}">Önizle</button>${multi?"":`<button type="button" class="btn" data-a="copy" data-u="${u}">Kopyala</button>`}<button type="button" class="btn dark dlxDl" data-a="dl" data-u="${u}">İndir</button></div>`
  :`<div class="dlxNo"><span class="dlxNoTag">Bu projede yok</span><span class="dlxWhy">${E(why(x))}</span>${x.fix?`<button type="button" class="linkBtn" data-a="fix" data-u="${u}">${E(x.fix.t)} →</button>`:""}</div>`;
 return `<li class="dlxRow${on?"":" off"}${x.opt?" opt":""}" data-u="${u}">${cb}<span class="dlxTy dlxTy-${tyc}">${E(x.ty)}</span><div class="dlxTx"><b class="dlxPath">${E(yol(x))}</b><span class="dlxDs">${E(x.d)}${x.opt?` <em>İsteğe bağlı: işaretlerseniz zip'e eklenir.</em>`:""}</span>${s?`<span class="dlxSt">${E(s)}</span>`:""}</div>${act}</li>`}
function fileBoxH(){let c=document.getElementById("fileChip"),t=c&&!c.hidden?c.textContent.trim():"";return `<div class="dlxBk"><p>${t?`Bağlı proje dosyası: <b>${E(t)}</b>. Seçimleriniz bu dosyaya otomatik kaydedilir.`:"Proje dosyası bağlı değil; seçimler yalnız bu tarayıcıda saklanır. Yedeği indirip güvenli bir yerde tutun."}</p><div class="dlxBkB"><button type="button" class="btn" data-a="import">JSON İçe Aktar</button><button type="button" class="linkBtn" data-a="pfile">Proje dosyası ayarları →</button></div></div>`}
function sumBase(p){let R0=p.rows.filter(x=>inZip(p,x)),dirs=[...new Set(R0.map(x=>x.dir).filter(Boolean))];return {R0,dirs}}
function cardH(p){let [n,N]=cnt(p),M=pkMiss(p),{R0,dirs}=sumBase(p);
 let chips=M.length?`<div class="dlxPkMiss" role="note"><b>${M.length} karar eksik</b><span>Bu paketteki bazı dosyalar eksik kararlar verilince hazırlanır.</span><div class="dlxChips">${M.slice(0,6).map(f=>`<button type="button" class="dlxChip" data-a="go" data-f="${E(f.id)}">${E((SI[f.section]||{}).name||"")} › ${E(f.label||f.id)}</button>`).join("")}${M.length>6?`<button type="button" class="dlxChip more" data-a="miss-all">+${M.length-6} karar daha</button>`:""}</div></div>`:"";
 return `<article class="dlxCard" aria-labelledby="dlxCardT"><div class="dlxCardH"><div><h2 id="dlxCardT">${E(p.t)}</h2><p>${E(p.d)}</p>${p.note?`<p class="dlxNote">${E(p.note)}</p>`:""}</div><span class="dlxBadge${n===N?" full":""}">${n}/${N} dosya</span></div>${chips}<ul class="dlxRows">${p.rows.map(x=>rowH(p,x)).join("")}</ul>${p.k==="backup"?fileBoxH():""}
 <div class="dlxFoot"><div class="dlxFootTx"><b class="dlxZipN">${E(zipName(p))}</b><span class="dlxZipIn" id="dlxZipIn">${R0.length?`Zip içeriği: ${R0.length} satır${dirs.length?" · klasörler: "+dirs.map(E).join(", "):""} · boyut hesaplanıyor…`:"Bu pakette indirilecek dosya yok."}</span></div><button type="button" class="btn dlxZipBtn" data-a="zip"${R0.length?"":" disabled"}>Paketi zip olarak indir</button></div></article>`}
function sizeLater(){let t=++SIZE_T,p=pk(SEL);const run=()=>{if(t!==SIZE_T||!isOn())return;let el=document.getElementById("dlxZipIn");if(!el)return;let {R0,dirs}=sumBase(p);if(!R0.length)return;
 try{let te=new TextEncoder(),L=pkFiles(p,""),b=L.reduce((s,f)=>s+te.encode(f.data).length,0);el.textContent=`Zip içeriği: ${L.length} dosya · ${kb(b)}${dirs.length?" · klasörler: "+dirs.join(", "):""}`}catch(e){console.error("zip boyutu",e);el.textContent=`Zip içeriği: ${R0.length} satır`}};
 (window.requestIdleCallback||(f=>setTimeout(f,60)))(run,{timeout:1200})}
function sig(){let S=stat();return S.n+"/"+S.N+"|"+PK.map(p=>p.rows.map(x=>ok(x)?1:0).join("")).join(".")+"|"+String(state.project_name||"")}
function render(){if(!PK.some(p=>p.k===SEL))SEL="claude";PREV=null;let S=stat(),p=pk(SEL);SIG=sig();
 PG.innerHTML=`<div class="dlxHead"><div><p class="dlxEye">DIŞA AKTAR</p><h1>İndirmeler</h1><p class="dlxLead">Kararlarınız paketler hâlinde hazırlanır. Bir paket seçin; dosyaları tek tek alın ya da paketi zip olarak indirin. Dosyalar indirme anındaki seçimlerden üretilir.</p></div><button type="button" class="btn" data-a="all">Tümünü zip olarak indir</button></div>${statH(S)}<div class="dlxGrid">${listH()}<div class="dlxMain">${cardH(p)}</div></div><div id="dlxToast" class="dlxToast" role="status" aria-live="polite"></div>`;
 stripSel();sizeLater()}
function stripSel(){let l=PG.querySelector(".dlxList"),o=l&&l.querySelector(".dlxPk.on");if(l&&o&&l.scrollWidth>l.clientWidth+1)l.scrollLeft=Math.max(0,o.offsetLeft-l.offsetLeft-8)}
function redrawCard(){PREV=null;let m=PG.querySelector(".dlxMain"),l=PG.querySelector(".dlxList");if(!m||!l)return render();l.outerHTML=listH();m.innerHTML=cardH(pk(SEL));stripSel();sizeLater()}
function redrawStat(){let s=PG.querySelector(".dlxStat");if(s)s.outerHTML=statH(stat())}
function preview(u,btn){let li=PG.querySelector(`.dlxRow[data-u="${u}"]`),old=PG.querySelector(".dlxPrev");if(old){let o=old.closest(".dlxRow");old.remove();let b=o&&o.querySelector(".dlxPv");if(b)b.setAttribute("aria-expanded","false");if(PREV===u){PREV=null;return}}PREV=u;
 let {x}=rowOf(u),body;try{if(x.files){let te=new TextEncoder(),L=x.files();body=L.length?L.map(f=>f.name+"  ·  "+kb(te.encode(f.data).length)).join("\n"):"(boş)"}else{body=text(x);if(body.length>200000)body=body.slice(0,200000)+"\n\n… (önizleme ilk 200.000 karakterle sınırlı; dosyanın tamamı için İndir)"}}catch(e){console.error("önizleme",e);body="Önizleme üretilemedi: "+(e&&e.message||e)}
 li.insertAdjacentHTML("beforeend",`<div class="dlxPrev"><pre tabindex="0" aria-label="${E(x.t)} önizlemesi">${E(body)}</pre></div>`);if(btn)btn.setAttribute("aria-expanded","true")}
PG.addEventListener("click",async e=>{let b=e.target.closest("[data-a]");if(!b||!PG.contains(b))return;let a=b.dataset.a;
 if(a==="opt")return;
 if(a==="sel"){SEL=b.dataset.p;redrawCard();if(matchMedia("(max-width:900px)").matches){let c=PG.querySelector(".dlxCard");if(c)c.scrollIntoView({block:"start",behavior:"smooth"})}let n=PG.querySelector(`.dlxPk[data-p="${SEL}"]`);if(n)n.focus({preventScroll:true});return}
 if(a==="miss"){MISS=!MISS;redrawStat();let x=PG.querySelector(".dlxMissBtn");if(x)x.focus();return}
 if(a==="miss-all"){MISS=true;redrawStat();let x=document.getElementById("dlxMiss");if(x)x.scrollIntoView({block:"start",behavior:"smooth"});return}
 if(a==="go"){let f=FI[b.dataset.f];if(f)goF(f);return}
 if(a==="area"){goArea2([b.dataset.ar]);return}
 if(a==="all"){dlAll();return}
 if(a==="zip"){dlZip(SEL);return}
 if(a==="import"){importBtn.click();return}
 if(a==="pfile"){if(typeof v26Overview==="function")v26Overview();setTimeout(()=>{let c=document.querySelector("#overviewPage .ovProject");if(c)c.scrollIntoView({block:"start"})},0);return}
 let r=rowOf(b.dataset.u);if(!r||!r.x)return;
 if(a==="fix"){guard(()=>r.x.fix.go());return}
 if(a==="prev"){preview(b.dataset.u,b);return}
 if(a==="dl"){dlRow(r.p,r.x);return}
 if(a==="copy"){let t;try{t=text(r.x)}catch(err){console.error("kopyalama",err);toast("Metin üretilemedi.",1);return}let okk=await copyText(t),o=b.dataset.o||b.textContent;b.dataset.o=o;b.textContent=okk?"Kopyalandı ✓":"Kopyalanamadı";b.classList.toggle("done",okk);clearTimeout(b._t);b._t=setTimeout(()=>{b.textContent=o;b.classList.remove("done")},2000);return}});
PG.addEventListener("change",e=>{let c=e.target.closest('input[data-a="opt"]');if(!c)return;OPT[c.dataset.u]=c.checked;let p=pk(SEL),{R0,dirs}=sumBase(p),el=document.getElementById("dlxZipIn"),zb=PG.querySelector(".dlxZipBtn");if(zb)zb.disabled=!R0.length;if(el)el.textContent=R0.length?`Zip içeriği: ${R0.length} satır${dirs.length?" · klasörler: "+dirs.join(", "):""} · boyut hesaplanıyor…`:"Bu pakette indirilecek dosya yok.";sizeLater()});

/* ---------- gezinme: modül şeridi, çekmece, üst şerit, ⋯ menüsü ---------- */
const ICON="M12 3v12m0 0-4.5-4.5M12 15l4.5-4.5M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2";
const svgI=`<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="${ICON}"/></svg>`;
function nav(){let rail=document.getElementById("modRail");if(rail&&!rail.querySelector('[data-mod="dlx"]')){let b=document.createElement("button");b.type="button";b.className="mrBtn";b.dataset.mod="dlx";b.title="Dışa Aktar — bütün dosyalar, JSON'lar ve promptlar";b.innerHTML=svgI+"<span>Dışa Aktar</span>";b.onclick=()=>DLX.go();let ref=rail.querySelector('[data-mod="plan"]')||rail.querySelector('[data-mod="agents"]');if(ref)ref.after(b);else rail.insertBefore(b,rail.querySelector(".mrSep"))}
 let ab=document.getElementById("sideAgentsBtn");if(ab&&!document.getElementById("sideDlBtn")){let s=document.createElement("button");s.type="button";s.id="sideDlBtn";s.innerHTML="⇩ &nbsp; Dışa Aktar";s.onclick=()=>DLX.go();ab.after(s)}sidePlace()}
/* çekmecede İçerik Planlama'dan sonra (kullanıcı isteği 2026-11-15: "Dışa Aktar menüsü 8. İçerik Planlama'dan sonra gelsin"); #sidePlanBtn sonraki betikte oluşur */
function sidePlace(){let s=document.getElementById("sideDlBtn"),p=document.getElementById("sidePlanBtn");if(s&&p&&p.nextElementSibling!==s)p.after(s)}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",sidePlace);
function sync(){let on=isOn(),rail=document.getElementById("modRail");if(rail)rail.querySelectorAll(".mrBtn").forEach(b=>{if(on){let a=b.dataset.mod==="dlx";b.classList.toggle("active",a);b.toggleAttribute("aria-current",a)}else if(b.dataset.mod==="dlx"){b.classList.remove("active");b.removeAttribute("aria-current")}});
 if(on)document.documentElement.classList.add("v26NoSide");let s=document.getElementById("sideDlBtn");if(s){s.classList.toggle("active",on);s.toggleAttribute("aria-current",on)}copyMaster.classList.toggle("on",on)}
const _sp=showPage;
showPage=function(p){if(p==="dlx"){_sp("config");configPage.classList.add("hidden");PG.classList.add("active");render();window.scrollTo(0,0);sync();return}PG.classList.remove("active");let r=_sp.apply(this,arguments);if(p==="overview")dlPkgRender();sync();return r};
const _ab=areaBtn;areaBtn=function(){_ab();if(isOn())sync()};
function closePanels(){["exClose","prClose","dlClose"].forEach(n=>{try{if(typeof window[n]==="function")window[n]()}catch(e){}});try{if(typeof exClose==="function")exClose()}catch(e){}}
window.DLX={go(k){closePanels();if(typeof closeNav==="function")closeNav();if(k&&pk(k))SEL=k;MISS=false;showPage("dlx")},sel(k){if(pk(k)){SEL=k;if(isOn())redrawCard()}},stat,modData,modImport};
/* üst şerit: "Claude Promptu" → "Dışa Aktar" (≤ 900 px'te de görünen ana düğme); JSON İndir / Ajanları İndir gizli (CSS), programlı tıklamalar da buraya gelir */
copyMaster.onclick=()=>DLX.go("claude");copyMaster.textContent="Dışa Aktar";copyMaster.removeAttribute("aria-haspopup");copyMaster.removeAttribute("aria-expanded");copyMaster.removeAttribute("aria-controls");copyMaster.title="Dosyaları, JSON'ları ve promptları indir";
if(typeof exportBtn!=="undefined"&&exportBtn){exportBtn.onclick=()=>DLX.go("backup")}
{let mb=document.getElementById("moreBtn"),mm=document.getElementById("moreMenu");if(mb&&mm&&mb.onclick){const _mo=mb.onclick;mb.onclick=function(e){let r=_mo.apply(this,arguments);if(!mm.hidden){mm.querySelectorAll('[data-a="ag"],[data-a="ex"]').forEach(x=>x.remove());let ov=mm.querySelector('[data-a="ov"]');if(ov&&!mm.querySelector('[data-a="dlx"]'))ov.insertAdjacentHTML("afterend",'<button type="button" role="menuitem" data-a="dlx">Dışa Aktar</button>')}return r};
 const _mc=mm.onclick;mm.onclick=function(e){let b=e.target.closest&&e.target.closest("button");if(b&&b.dataset.a==="dlx"){e.stopPropagation();mm.hidden=true;mb.setAttribute("aria-expanded","false");DLX.go();return}return _mc&&_mc.apply(this,arguments)}}}

/* ---------- Dashboard: kısa özet kartı ---------- */
window.dlPkgRender=()=>{let ov=document.getElementById("overviewPage");if(!ov)return;let old=document.getElementById("dlPkgs");if(old)old.remove();
 let S=stat(),D=PK.filter(p=>p.dir),n=D.reduce((s,p)=>s+cnt(p)[0],0),N=D.reduce((s,p)=>s+cnt(p)[1],0);
 ov.insertAdjacentHTML("beforeend",`<section class="dlPkgs dlxMini" id="dlPkgs" aria-labelledby="dlMiniT"><div><h2 id="dlMiniT">Dışa Aktar</h2><p><b>${n} / ${N} dosya hazır</b> · ${S.miss?S.miss+" karar eksik":"bütün kararlar verildi"}. Bütün dosyalar, JSON'lar ve promptlar Dışa Aktar sayfasında paketler hâlinde.</p></div><button type="button" class="btn dark" onclick="DLX.go()">Dışa Aktar'ı aç →</button></section>`)};
const ovp=document.getElementById("overviewPage");
if(ovp){new MutationObserver(()=>{if(ovp.classList.contains("active")&&!document.getElementById("dlPkgs"))dlPkgRender()}).observe(ovp,{childList:true,attributes:true,attributeFilter:["class"]});
 if(ovp.classList.contains("active"))dlPkgRender()}

/* karar değişince sayfa açıksa durum ve sayaçlar yenilenir (yalnız hazır olma durumu değiştiyse) */
if(typeof renderProgress==="function"){const _rp=renderProgress;let tm=0;renderProgress=function(){const r=_rp.apply(this,arguments);if(isOn()){clearTimeout(tm);tm=setTimeout(()=>{try{if(isOn()&&sig()!==SIG)render()}catch(e){console.error("Dışa Aktar yenileme",e)}},200)}return r}}

nav();
window.dlPackages=()=>PK;window.dlZip=dlZip;window.dlAll=dlAll;
window.dlDebug={PK,R,pkFiles,readme,OPT,ok,inZip,zipName,modOwn};
})();
