/* Dashboard › İndirmeler (2026-11-12, kullanıcı isteği: "indirilebilir tüm json, md, promptları paketler halinde dashboard'da
   göster"). Uygulamanın ürettiği bütün dosyalar ve kopyalanabilir promptlar paketler hâlinde: her satırda İndir / Kopyala,
   her pakette "Paketi zip olarak indir" ve yanında zip'in içindeki dosyalar (2026-11-12, kullanıcı isteği: "paketin içerisinde hangi dosyalar var yanına yaz"; ajan / skill dosyaları ".claude/ klasörü (N ajan, M skill)" özetiyle), başta "Tümünü zip olarak indir" (paket başına klasör). Üreticiler var olan
   fonksiyonlardır (exData, projectFileData, prMd, prStart, agZipFiles, mcJson, mkJson, dsConfig, dsTokensCss, pzPf, rgFiles,
   auPrompt, mkMarketingPrompt, ggSetupMd, mtSetupMd, yzSetupMd); bu blok yalnız listeler ve paketler — dosya içerikleri
   değişmez. Metinler yalnız düğmeye basılınca üretilir. Projede olmayan çıktı (ör. MCP seçilmemişse .mcp.json) "Bu projede
   yok" olarak soluk görünür. Bölüm #overviewPage'in sonuna eklenir: showPage("overview") sarmalanır (eşzamanlı çizim), sayfa başka yoldan yeniden çizilirse MutationObserver geri ekler.
   Kaynak docs/v26/v26-downloads.js → docs/v26/indirmeler_ekle.py */
(()=>{
const has=n=>typeof window[n]==="function";
const slug=()=>{try{return (typeof exBrand==="function"&&exBrand())||"proje"}catch(e){return "proje"}};
const host=()=>String(state.domain_name||"").trim().replace(/^[a-z]+:\/\//i,"").replace(/[\/?#].*$/,"").replace(/^www\./i,"").toLocaleLowerCase("tr").replace(/[^a-z0-9.-]+/g,"-").replace(/^[-.]+|[-.]+$/g,"")||slug();
const J=o=>JSON.stringify(o,null,2);
const areaN=a=>{try{let V=F.filter(f=>shown(f)&&navF(f)&&AREA(SI[f.section])===a);return [V.filter(isset).length,V.length]}catch(e){return [0,0]}};
const dec=a=>{let [n,N]=areaN(a);return n?`${n}/${N} karar`:"Henüz karar verilmedi"};
/* Satır: k anahtar, t ad, d açıklama, ty tür (JSON / MD / CSS / ZIP / PROMPT), name() dosya adı, gen() içerik (metin) ya da
   files() (zip için dosya listesi), ok() projede var mı, st() durum metni, copy kopyalanabilir mi */
const PK=[
 {k:"claude",t:"Claude Code proje paketi",d:"Siteyi geliştirecek Claude oturumu için: talimat dosyası, promptlar, proje kararları, ajan ve skill dosyaları ve projede seçildiyse MCP, tasarım ve panel yapılandırmaları.",dir:"1-claude-code",items:[
  {k:"md",t:"CLAUDE-TALIMATLARI.md",ty:"MD",d:"Fazlara bölünmüş ana talimat dosyası; Claude Code'da proje köküne konur.",name:()=>"CLAUDE-TALIMATLARI.md",gen:()=>prMd(),ok:()=>has("prMd"),copy:false},
  {k:"start",t:"Başlatma promptu",ty:"PROMPT",d:"Talimat dosyasını fazlar hâlinde uygulatan kısa prompt.",name:()=>"BASLATMA-PROMPTU.md",gen:()=>prStart(),ok:()=>has("prStart"),copy:true},
  {k:"master",t:"Claude promptu (tam)",ty:"PROMPT",d:"Bütün kuralların tek parça hâli (talimat dosyasının yerine kullanılabilir).",name:()=>"CLAUDE-PROMPTU.md",gen:()=>{renderRules();return master.value},ok:()=>true,copy:true},
  {k:"project",t:"Proje Kararları",ty:"JSON",d:"Proje ve Ortak Bilgiler kararları, kurallar, ajanlar, skill'ler ve Claude promptu.",name:()=>exName("project"),gen:()=>J(exData("project")),ok:()=>has("exData"),st:()=>dec("project")},
  {k:"agents",t:"Ajanlar ve skill'ler",ty:"ZIP",d:".claude/agents ve .claude/skills dosyaları; proje köküne açılır.",name:()=>(typeof pfFileName==="function"&&pfFileName().replace(/\.json$/,"")||slug())+"-claude-ajan-skill.zip",files:()=>agZipFiles(),inside:()=>`.claude/ klasörü (${agOn("dev").length} ajan${typeof skSlugs==="function"&&Object.keys(skSlugs()).length?", "+Object.keys(skSlugs()).length+" skill":""})`,ok:()=>has("agZipFiles")&&agOn("dev").length>0,st:()=>has("agOn")&&agOn("dev").length?agOn("dev").length+" ajan":"Projeye ajan eklenmedi"},
  {k:"mcp",t:".mcp.json",ty:"JSON",d:"Seçilen MCP bağlantılarının Claude Code yapılandırması.",name:()=>".mcp.json",gen:()=>mcJson(),ok:()=>has("mcJson")&&has("mcOn")&&mcOn().some(x=>typeof mcCfg!=="function"||mcCfg(x)),st:()=>has("mcOn")&&mcOn().length?mcOn().length+" bağlantı":"MCP seçilmedi"},
  {k:"dsjson",t:"Tasarım yapılandırması",ty:"JSON",d:"Tasarım sistemi kararları (stil, layout, parametreler).",name:()=>dsFileBase()+"-tasarim-yapilandirmasi.json",gen:()=>J(dsConfig()),ok:()=>has("dsActive")&&dsActive(),st:()=>has("dsActive")&&dsActive()?"":"Tasarım şartnamesi kararı yok"},
  {k:"dscss",t:"Tasarım token'ları",ty:"CSS",d:"Tasarım kararlarından üretilen CSS değişkenleri.",name:()=>dsFileBase()+"-tasarim-tokenlari.css",gen:()=>dsTokensCss(),ok:()=>has("dsActive")&&dsActive(),st:()=>has("dsActive")&&dsActive()?"":"Tasarım şartnamesi kararı yok"},
  {k:"panels",t:"Panel ve portal mimarisi",ty:"JSON",d:"Panel envanteri, adresler, roller, modüller ve izolasyon.",name:()=>slug()+"-panel-mimarisi.json",gen:()=>J(pzPf().panelArchitecture),ok:()=>has("pzPf")&&!!(pzPf()||{}).panelArchitecture,st:()=>has("pzPf")&&(pzPf()||{}).panelArchitecture?"":"Panel eklenmedi"},
  {k:"registry",t:"Ajan Kaydı",ty:"ZIP",d:"AGENT_REGISTRY, SKILL_REGISTRY ve AGENT_ORGANIZATION_MAP JSON dosyaları.",name:()=>slug()+"-ajan-kaydi.zip",files:()=>Object.entries(rgFiles()).map(([name,data])=>({name,data})),inside:()=>"AGENT_REGISTRY.json, SKILL_REGISTRY.json, AGENT_ORGANIZATION_MAP.json",ok:()=>has("rgFiles")&&!!state.registry,st:()=>state.registry?"":"Ajan Kaydı kullanılmadı"}]},
 {k:"marketing",t:"Pazarlama paketi",d:"Pazarlama, Google, Meta ve Yapay Zekâ kararlarının dosyası, içerik üretimi için pazarlama promptu ve içerik planı şablonunun veri dosyası.",dir:"2-pazarlama",items:[
  {k:"json",t:"Pazarlama Kararları",ty:"JSON",d:"Pazarlama, Google Servisleri, Meta Servisleri ve Yapay Zekâ kararları, kuralları ve pazarlama promptu.",name:()=>exName("marketing"),gen:()=>J(exData("marketing")),ok:()=>has("exData"),st:()=>dec("marketing")},
  {k:"prompt",t:"Pazarlama promptu",ty:"PROMPT",d:"İçerik üretecek Claude oturumu için marka, kitle, kanal ve içerik kuralları.",name:()=>"pazarlama-promptu-"+slug()+".md",gen:()=>mkMarketingPrompt(),ok:()=>has("mkMarketingPrompt"),copy:true},
  {k:"plan",t:"İçerik planı veri dosyası",ty:"JSON",d:"İçerik planı şablonunun (icerik-plani-SABLON.html) veri dosyası.",name:()=>"veri."+mkBase()+".json",gen:()=>mkJson(),ok:()=>has("mkJson")&&has("mkBase"),st:()=>dec("marketing")}]},
 {k:"audit",t:"SEO Denetimi paketi",d:"Yayındaki siteyi denetleyecek Claude oturumu için denetim promptu ve kararlar.",dir:"3-seo-denetimi",items:[
  {k:"json",t:"SEO Denetimi",ty:"JSON",d:"Denetim kararları, kontroller ve denetim promptu.",name:()=>exName("audit"),gen:()=>J(exData("audit")),ok:()=>has("exData"),st:()=>dec("audit")},
  {k:"prompt",t:"SEO denetim promptu",ty:"PROMPT",d:"Kapsam, kontroller, çalışma kuralları ve rapor biçimi.",name:()=>"seo-denetimi-"+host()+".md",gen:()=>auPrompt(),ok:()=>has("auPrompt"),copy:true,st:()=>dec("audit")}]},
 {k:"google",t:"Google Servisleri paketi",d:"Tag Manager, Analytics 4, Consent Mode, Search Console, Ads, Merchant Center, İşletme Profili ve Data Studio kurulum talimatı. Kararlar Pazarlama Kararları dosyasındadır.",dir:"4-google",items:[
  {k:"md",t:"Google kurulum talimatı",ty:"MD",d:"Bağlam, kimlikler, çalışma kuralları, uygulama sırası ve bölüm kuralları.",name:()=>"google-kurulum-"+host()+".md",gen:()=>ggSetupMd(),ok:()=>has("ggSetupMd"),copy:true,st:()=>dec("google")}]},
 {k:"meta",t:"Meta Servisleri paketi",d:"İşletme portföyü, Facebook Sayfası, Instagram, WhatsApp, Meta Pikseli / Conversions API, reklam hesabı ve katalog kurulum talimatı.",dir:"5-meta",items:[
  {k:"md",t:"Meta kurulum talimatı",ty:"MD",d:"Bağlam, kimlikler, çalışma kuralları, uygulama sırası ve bölüm kuralları.",name:()=>"meta-kurulum-"+host()+".md",gen:()=>mtSetupMd(),ok:()=>has("mtSetupMd"),copy:true,st:()=>dec("meta")}]},
 {k:"ai",t:"Yapay Zekâ paketi",d:"ChatGPT'de işletme, yapay zekâ platformları, tarayıcı izinleri, sitedeki asistan ve ölçüm talimatı.",dir:"6-yapay-zeka",items:[
  {k:"md",t:"Yapay zekâ talimatı",ty:"MD",d:"Bağlam, çalışma kuralları, uygulama sırası ve bölüm kuralları.",name:()=>"yapay-zeka-"+host()+".md",gen:()=>yzSetupMd(),ok:()=>has("yzSetupMd"),copy:true,st:()=>dec("ai")}]},
 {k:"backup",t:"Tam yedek",d:"Bütün seçimleri tek dosyada taşıyan proje dosyası; JSON İçe Aktar ile geri yüklenir.",dir:"7-yedek",items:[
  {k:"full",t:"Proje dosyası (tam yedek)",ty:"JSON",d:"Proje, pazarlama ve denetim seçimlerinin tamamı.",name:()=>(typeof pfFileName==="function"&&pfFileName())||"web-project-config-v25.json",gen:()=>J(projectFileData()),ok:()=>has("projectFileData")}]}];
const pk=k=>PK.find(p=>p.k===k);
const it=(p,i)=>pk(p).items.find(x=>x.k===i);
const ok=x=>{try{return !!x.ok()}catch(e){return false}};
const st=x=>{try{return x.st?x.st():""}catch(e){return ""}};
const nm=x=>{try{return x.name()}catch(e){return x.t}};
const text=x=>String(x.gen()||"");
const files=x=>x.files?x.files():[{name:nm(x),data:text(x)}];
function save(blob,name){let a=document.createElement("a"),u=URL.createObjectURL(blob);a.href=u;a.download=name;document.body.appendChild(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(u),1500)}
function zip(list,name){if(!list.length)return;save(zipStore(list),name)}
function toast(msg,err){let b=document.getElementById("dlToast");if(!b)return;b.textContent=msg;b.className="dlToast show"+(err?" err":"");clearTimeout(toast.t);toast.t=setTimeout(()=>b.className="dlToast",err?5000:2400)}
function guard(fn){try{fn()}catch(e){console.error("indirme",e);toast("Dosya üretilemedi: "+(e&&e.message||e),1)}}
window.dlItem=(p,i)=>guard(()=>{let x=it(p,i);if(x.files)zip(x.files(),nm(x));else{let t=text(x),ty=x.ty==="JSON"?"application/json":x.ty==="CSS"?"text/css":"text/markdown";save(new Blob([t],{type:ty}),nm(x))}toast(nm(x)+" indirildi.")});
window.dlCopy=async(p,i,btn)=>{let t;try{t=text(it(p,i))}catch(e){toast("Prompt üretilemedi.",1);return}let okk=true;try{await navigator.clipboard.writeText(t)}catch(e){try{let ta=document.createElement("textarea");ta.value=t;ta.style.cssText="position:fixed;opacity:0;left:0;top:0";document.body.appendChild(ta);ta.select();okk=document.execCommand("copy");ta.remove()}catch(e2){okk=false}}
 if(btn){let o=btn.textContent;btn.textContent=okk?"Kopyalandı ✓":"Kopyalanamadı";setTimeout(()=>btn.textContent=o,1400)}};
function pkFiles(p,prefix){let o=[];p.items.filter(ok).forEach(x=>files(x).forEach(f=>o.push({name:(prefix||"")+f.name,data:f.data})));return o}
window.dlPack=k=>guard(()=>{let p=pk(k),L=pkFiles(p,"");if(!L.length){toast("Bu pakette indirilecek dosya yok.",1);return}zip(L,slug()+"-"+p.dir.replace(/^\d+-/,"")+".zip");toast(p.t+" indirildi ("+L.length+" dosya).")});
window.dlAll=()=>guard(()=>{let L=[];PK.forEach(p=>L.push(...pkFiles(p,p.dir+"/")));L.unshift({name:"OKU-BENI.md",data:readme()});zip(L,slug()+"-tum-indirmeler.zip");toast("Bütün paketler indirildi ("+(L.length-1)+" dosya).")});
function readme(){let d=new Date().toLocaleDateString("sv-SE");return `# ${String(state.project_name||"").trim()||"Proje"} — indirmeler\n\nCortex Configurator ile ${d} tarihinde üretildi. Her klasör bir pakettir:\n\n`+PK.map(p=>`## ${p.dir}\n${p.d}\n\n`+p.items.filter(ok).map(x=>`- **${x.t}** (${nm(x)}): ${x.d}`).join("\n")).join("\n\n")+`\n\nDosyalar seçimlerin indirme anındaki hâlidir; seçim değişince Dashboard › İndirmeler'den yeniden alın.\n`}
function row(p,x){let on=ok(x),s=st(x);return `<li class="dlRow${on?"":" off"}"><span class="dlTy dlTy-${x.ty.toLowerCase()}">${x.ty}</span><div class="dlTx"><b>${E(x.t)}</b><span class="dlFn">${E(on?nm(x):"Bu projede yok")}</span><span class="dlDs">${E(x.d)}</span>${s?`<span class="dlSt">${E(s)}</span>`:""}</div><div class="dlBt">${on?`${x.copy?`<button type="button" class="btn" onclick="dlCopy('${p.k}','${x.k}',this)">Kopyala</button>`:""}<button type="button" class="btn${x.copy?"":" dark"}" onclick="dlItem('${p.k}','${x.k}')">İndir</button>`:""}</div></li>`}
function inside(x){try{return x.inside?x.inside():nm(x)}catch(e){return x.t}}
function card(p){let n=p.items.filter(ok).length,inl=p.items.filter(ok).map(inside);return `<article class="dlPk" data-pk="${p.k}"><div class="dlPkH"><h3>${E(p.t)}</h3><span class="dlPkN">${n}/${p.items.length} dosya</span></div><p class="dlPkD">${E(p.d)}</p><ul class="dlList">${p.items.map(x=>row(p,x)).join("")}</ul><div class="dlPkF"><button type="button" class="btn dark" onclick="dlPack('${p.k}')"${n?"":" disabled"}>Paketi zip olarak indir</button><p class="dlPkIn">${n?`<b>Zip'in içinde:</b> ${inl.map(E).join(", ")}`:"Bu pakette henüz dosya yok."}</p></div></article>`}
function html(){return `<section class="dlPkgs" id="dlPkgs" aria-labelledby="dlH"><div class="dlHead"><div><h2 id="dlH">İndirmeler</h2><p>Projenin ürettiği bütün dosyalar ve promptlar paketler hâlinde. Dosyalar indirme anındaki seçimlerden üretilir; seçim değişince yeniden indirin. Paketi zip olarak alabilir ya da bütün paketleri klasörler hâlinde tek zip olarak indirebilirsiniz.</p></div><button type="button" class="btn dark" onclick="dlAll()">Tümünü zip olarak indir</button></div><div class="dlGrid">${PK.map(card).join("")}</div><div id="dlToast" class="dlToast" role="status" aria-live="polite"></div></section>`}
window.dlRender=()=>{let ov=document.getElementById("overviewPage");if(!ov)return;let old=document.getElementById("dlPkgs");if(old)old.remove();ov.insertAdjacentHTML("beforeend",html())};
const _sp=showPage;showPage=function(p){const r=_sp.apply(this,arguments);if(p==="overview")dlRender();return r};
const ov=document.getElementById("overviewPage");
if(ov){new MutationObserver(()=>{if(ov.classList.contains("active")&&!document.getElementById("dlPkgs"))dlRender()}).observe(ov,{childList:true,attributes:true,attributeFilter:["class"]});
 if(ov.classList.contains("active"))dlRender()}
window.dlDebug={PK,pkFiles,readme};
})();
