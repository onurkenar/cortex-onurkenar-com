/* Panel & Portal Mimarisi (2026-11-08, kullanıcının "Panel & Portal Architecture" yönergesi).
   Veri: DATA.panelKit (docs/panel-portal/kaynak.py → panel_portal_ekle.py). Seçimler: state.panelArch
   {v, panels[], modules[] (özel modüller), apps[] (uygulamalar)} — yalnız ilk değişiklikte oluşur; kullanılmamış projede
   prompt, kurallar ve dışa aktarma öncekiyle aynıdır. Bölüm kararları (panel_*) normal alanlardır. */
(()=>{
const K=DATA.panelKit;if(!K)return;
const SEC=K.section,TP={},MD={},CT={};K.templates.forEach(t=>TP[t.id]=t);K.modules.forEach(m=>MD[m.id]=m);K.categories.forEach(c=>CT[c.id]=c);
const MODE={subdomain:"Alt alan adı",subdirectory:"Alt dizin",separate_domain:"Ayrı alan adı"},
 LV={r:"Görüntüle",w:"Düzenle",m:"Yönet"},LVE={r:"read",w:"write",m:"manage"},
 SCOPE={platform:"Platform geneli",org:"Organizasyon bağlamı",own:"Yalnız kendi kayıtları"},
 TABS=[["general","Genel"],["url","URL ve yönlendirme"],["auth","Kimlik doğrulama"],["roles","Roller ve izinler"],["modules","Modüller"],["data","Veri izolasyonu"],["brand","Marka ve arayüz"],["security","Güvenlik"],["deploy","Dağıtım"]],
 STS=[["","Tümü"],["in","Projede"],["on","Aktif"],["off","Pasif"],["warn","Uyarılı"],["out","Eklenmemiş"]],
 PH={mvp:"İlk sürüm (MVP)",phase2:"İkinci aşama",later:"Sonraki aşamalar"},
 ROUT={host:"Ana makine adına göre (host routing)",prefix:"Yol önekine göre (route prefix / basePath)",proxy:"Ters vekil / edge yönlendirme (rewrite)",own:"Ayrı uygulama kendi adresinde"},
 ASC={host:"Yalnız bu panelin adresi (host-only oturum)",idp:"Ortak kimlik sağlayıcı, panel başına oturum (SSO)",parent:"Üst alan adında paylaşılan oturum",shared:"Siteyle aynı oturum (aynı köken)",separate:"Bu panele özel kimlik"},
 BND={shared:"Ana uygulamayla aynı dağıtım birimi",separate:"Ayrı dağıtım birimi"},
 SRC={shared:"Projenin ortak kullanıcı deposu",internal:"Kurumsal kimlik sağlayıcı (çalışan SSO)",separate:"Bu panele özel kullanıcı deposu",external:"Müşterinin kimlik sağlayıcısı (kurumsal SSO / SAML / OIDC)"},
 METH=[["password","E-posta + parola"],["passkey","Passkey"],["magic","E-posta ile giriş bağlantısı"],["otp","Tek kullanımlık kod (SMS / e-posta)"],["sso","Kurumsal SSO (OIDC / SAML)"],["social","Sosyal hesap"]],
 MFA={required:"Herkes için zorunlu",privileged:"Yetkili roller için zorunlu",optional:"İsteğe bağlı",off:"Kapalı"},
 SESS={short:"Kısa (15 dk boşta, en çok 8 saat)",standard:"Standart (30 dk boşta, en çok 24 saat)",long:"Uzun (beni hatırla, 30 gün — yalnız düşük riskli portallar)"},
 DSC={platform:"Platform geneli (bütün organizasyonlar)",org:"Etkin organizasyon",tenant:"Çalışma alanı (kiracı)",own:"Yalnız kullanıcının kendi kayıtları"},
 CROSS={none:"Yok",audited:"Yalnız platform rolleri, gerekçe ve denetim kaydıyla",readonly:"Salt okunur toplu raporlama"},
 PII={mask:"Maskeli; tam değer yalnız yetkili role ve kayıtla",role:"Role göre",full:"Tam (yalnız gerekli rollerde)"},
 EXP={none:"Kapalı",role:"Yalnız yetkili rol, denetim kaydıyla",open:"Panel kullanıcılarına açık"},
 THEME={public:"Sitenin kurumsal kimliği",panel:"Ayrı, sade panel teması",tenant:"Kiracıya göre beyaz etiket"},
 LAY={sidebar:"Sol menü",topbar:"Üst menü",both:"Üst menü + sol alt menü"},DENS={comfortable:"Ferah",compact:"Yoğun (tablo ağırlıklı)"},
 LANG={site:"Sitenin dilleri",tr:"Yalnız Türkçe",user:"Kullanıcı seçer"},CMODE={site:"Sitenin renk modu",light:"Açık",dark:"Koyu",user:"Kullanıcı seçer"},
 SECO=[["noindex","Arama motorlarından gizle (X-Robots-Tag: noindex)"],["audit","Denetim kaydı"],["rate","Giriş ve API hız sınırı"],["csp","Katı içerik güvenliği politikası (CSP)"],["stepUp","Kritik işlemde yeniden doğrulama"],["captcha","Girişte bot koruması"],["zeroTrust","Ağ düzeyinde erişim kontrolü (Zero Trust / VPN)"],["ipAllow","IP izin listesi"],["exportApproval","Toplu dışa aktarma onaylı"]],
 ENV=[["dev","Geliştirme"],["staging","Test (staging)"],["production","Canlı"]],CACHE={private:"private, no-store (önerilen)",short:"Kısa süreli özel önbellek"},
 REL={with_site:"Siteyle birlikte",independent:"Bağımsız yayın",canary:"Kademeli (canary)"};
const UI={q:"",cat:"",st:"",sel:new Set(),open:null,tab:"general",sum:false,rec:true};
const LB=(o,k)=>o[k]||k||"—",fv=id=>state[id],fl=(id,v)=>FI[id]?lab(FI[id],v):v;
const uid=p=>(p||"p")+Date.now().toString(36)+Math.random().toString(36).slice(2,6);

/* ---------- durum ---------- */
function PA(){let p=state.panelArch;return p&&typeof p==="object"&&Array.isArray(p.panels)?p:null}
function pa(){let p=PA();if(!p){p={v:1,panels:[],modules:[],apps:[{id:"web",name:"Ana web uygulaması"}]};state.panelArch=p}return fixAll(p)}
function prune(a,ok){for(let i=a.length-1;i>=0;i--)if(!ok(a[i]))a.splice(i,1)}
function fixAll(p){if(!Array.isArray(p.modules))p.modules=[];prune(p.modules,m=>m&&m.id&&m.name);if(!Array.isArray(p.apps))p.apps=[];prune(p.apps,a=>a&&a.id&&a.name);if(!p.apps.some(a=>a.id==="web"))p.apps.unshift({id:"web",name:"Ana web uygulaması"});prune(p.panels,x=>x&&typeof x==="object");p.panels.forEach(fix);return p}
function perms(t,r){let o={};if(r.all)t.modules.forEach(m=>o[m]=r.all);else{r.r.forEach(m=>o[m]="r");r.w.forEach(m=>o[m]="w");r.m.forEach(m=>o[m]="m")}return o}
function secDef(t){let hi=t.risk==="high"||t.cat==="admin"||t.cat==="internal";return {noindex:true,audit:hi||t.cat==="business",rate:true,csp:hi,stepUp:hi,captcha:!hi,zeroTrust:false,ipAllow:false,exportApproval:hi}}
function fix(x){let t=TP[x.tpl]||TP.custom,ob=(k,d)=>{if(!x[k]||typeof x[k]!=="object"||Array.isArray(x[k]))x[k]={};Object.keys(d).forEach(j=>{if(x[k][j]===undefined)x[k][j]=d[j]})};
 if(!x.id)x.id=uid();if(!TP[x.tpl])x.tpl="custom";if(typeof x.name!=="string"||!x.name.trim())x.name=t.name;if(!CT[x.cat])x.cat=t.cat;
 ["desc","audience"].forEach(k=>{if(typeof x[k]!=="string")x[k]=t[k==="desc"?"desc":"audience"]});if(typeof x.on!=="boolean")x.on=true;if(!PH[x.phase])x.phase="mvp";
 ob("url",{mode:t.mode,slug:t.slug,base:"",domain:"",routing:"",app:"web",boundary:"",authScope:""});if(!MODE[x.url.mode])x.url.mode=t.mode;
 ob("auth",{source:t.idp==="internal"?"internal":"shared",methods:[],mfa:t.mfa,session:t.risk==="high"?"short":"standard",login:""});if(!Array.isArray(x.auth.methods))x.auth.methods=[];
 if(!Array.isArray(x.roles))x.roles=t.roles.map(r=>({id:r.id,name:r.name,scope:r.scope,perms:perms(t,r)}));prune(x.roles,r=>r&&typeof r==="object");x.roles.forEach(r=>{if(!r.id)r.id=uid("r");if(typeof r.name!=="string")r.name="Rol";if(!SCOPE[r.scope])r.scope="org";if(!r.perms||typeof r.perms!=="object")r.perms={}});
 if(typeof x.abac!=="string")x.abac="";if(!Array.isArray(x.modules))x.modules=t.modules.slice();
 ob("data",{scope:t.scope==="platform"?"platform":t.scope==="own"?"own":"org",cross:t.scope==="platform"?"audited":"none",pii:"mask",export:"role"});
 ob("brand",{theme:t.cat==="customer"||t.cat==="business"?"public":"panel",layout:"sidebar",density:t.cat==="customer"?"comfortable":"compact",lang:"site",mode:"site",whiteLabel:false});
 ob("sec",secDef(t));ob("deploy",{env:["staging","production"],cache:"private",region:"",release:"with_site"});if(!Array.isArray(x.deploy.env))x.deploy.env=["production"];return x}
function mk(tid,o){o=o||{};let t=TP[tid]||TP.custom,g=fv("panel_url_strategy"),mode=o.mode||(g&&g!=="hybrid"&&MODE[g]?g:t.mode),p=pa();
 let x=fix({id:uid(),tpl:t.id,url:{mode,slug:o.slug||t.slug}});if(o.name)x.name=o.name;if(state.cms_mode==="WordPress"&&tid==="cms_admin"&&!o.slug&&mode==="subdirectory")x.url.slug="wp-admin";
 let s=x.url.slug,n=2;while(p.panels.some(y=>full(y)===full(x))){x.url.slug=s+"-"+n++}return x}
const panels=()=>{let p=PA();return p?fixAll(p).panels:[]},act=()=>panels().filter(x=>x.on),get=id=>panels().find(x=>x.id===id);
function pzActive(){let p=PA();return !!(p&&p.panels.length)}
const FID="panel_inventory";
function commit(redraw){if(pzActive())try{faAuto(FID)}catch(e){}save();try{renderRules();renderProgress()}catch(e){}if(redraw!==false)draw();syncField()}
/* alanın kural kutusu ve sorumlu ajan satırı envanter değişince güncellensin (envanter kutusu yerinde kalır) */
function syncField(){let fe=fieldBox.querySelector(`.field[data-field-id="${FID}"]`);if(!fe||!BOX)return;let t=document.createElement("template");t.innerHTML=one(FI[FID]);let n=t.content.firstElementChild,P=[".fAgents",".rule"].map(c=>[fe.querySelector(c),n.querySelector(":scope > "+c)]);
 if(P.some(([x,y])=>!x!==!y)){refreshField(FID);return}P.forEach(([x,y])=>{if(x&&y)x.replaceWith(y)})}

/* ---------- adresler ---------- */
function host(){let d=String(fv("domain_name")||"").trim();if(!d)return "";try{return new URL(/^https?:/i.test(d)?d:"https://"+d).hostname.toLowerCase()}catch(e){return ""}}
const clean=s=>String(s||"").trim().toLowerCase().replace(/^https?:\/\//,"").replace(/[/?#].*$/,"");
function base(x){return clean(x.url.base)||host()||"alanadi.com"}
const apex=b=>b.replace(/^www\./,"");
function full(x){let u=x.url,b=base(x);if(u.mode==="subdomain")return `https://${u.slug||"?"}.${apex(b)}`;if(u.mode==="subdirectory")return `https://${b}/${String(u.slug||"?").replace(/^\/+|\/+$/g,"")}`;let d=clean(u.domain);return d?`https://${d}`:"https://(ayrı alan adı girilmedi)"}
const origin=x=>{let f=full(x);try{return new URL(f).origin}catch(e){return f}};
function app(id){let p=PA(),a=p&&p.apps.find(y=>y.id===id);return a||{id:"web",name:"Ana web uygulaması"}}
function effRouting(x){if(x.url.routing&&ROUT[x.url.routing])return x.url.routing;if(x.url.app!=="web")return "own";return x.url.mode==="subdirectory"?"prefix":"host"}
function effBoundary(x){if(BND[x.url.boundary])return x.url.boundary;let d=fv("panel_deploy_topology");if(d==="per_app")return x.url.app==="web"?"shared":"separate";return x.url.app==="web"?"shared":"separate"}
function effScope(x){if(ASC[x.url.authScope])return x.url.authScope;if(x.auth.source==="separate")return "separate";let id=fv("panel_identity"),se=fv("panel_session");if(x.url.mode==="subdirectory"&&(id==="shared_session"||!id))return "shared";if(se==="parent_domain"&&x.url.mode==="subdomain")return "parent";if(id==="shared_idp"||id==="hybrid"||x.url.mode==="separate_domain")return "idp";return "host"}
const RE_LABEL=/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/,RE_DOM=/^(?=.{1,253}$)(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,63}$/;
function risky(x){let t=TP[x.tpl];return x.cat==="admin"||x.cat==="internal"||(t&&t.risk==="high")}
function issues(x){let I=[],u=x.url,s=String(u.slug||"").trim(),add=(lv,t)=>I.push({lv,t});
 if(u.mode!=="separate_domain"){if(!s)add("err","Panel adı (slug) boş.");else{let segs=u.mode==="subdirectory"?s.replace(/^\/+|\/+$/g,"").split("/"):[s],bad=segs.find(g=>!RE_LABEL.test(g));
  if(/[çğıöşüâîûÇĞİÖŞÜ]/.test(s))add("err",`Slug Türkçe karakter içeriyor; “${exSlug(s)}” önerilir.`);else if(bad!==undefined)add("err",u.mode==="subdomain"?"Alt alan adı yalnız küçük harf, rakam ve kısa çizgi içerebilir; çizgiyle başlayıp bitemez, en çok 63 karakterdir.":"Alt dizin yolu yalnız küçük harf, rakam, kısa çizgi ve / içerebilir.");
  if(u.mode==="subdirectory"&&segs.length>3)add("warn","Panel yolu üç seviyeden derin; kısa ve sabit bir önek önerilir.");
  let f0=segs[0];if(u.mode==="subdomain"&&f0==="www")add("err","“www” alt alan adı ana site için ayrılmıştır.");else if(u.mode==="subdomain"&&K.reserved.subdomains.includes(f0))add("warn",`“${f0}” alt alan adı genellikle altyapı veya ortam için ayrılır (rezerve).`);
  if(u.mode==="subdirectory"&&K.reserved.paths.includes(f0))add("warn",`“/${f0}” yolu altyapı, kimlik doğrulama veya statik dosyalar için ayrılmış bir yoldur (rezerve).`)}}
 else{let d=clean(u.domain);if(!d)add("err","Ayrı alan adı girilmedi.");else if(!RE_DOM.test(d))add("err","Ayrı alan adı geçerli değil (ör. bayi-markasi.com).");else if(apex(d)===apex(base(x)))add("err","Ayrı alan adı ana alan adıyla aynı; alt alan adı ya da alt dizin seçin.")}
 if(clean(u.base)&&!RE_DOM.test(clean(u.base)))add("err","Ana alan adı geçerli değil.");
 if(!clean(u.base)&&!host())add("info","Ortak Bilgiler › Canlı Site Adresi girilmedi; önizlemede alanadi.com kullanılıyor.");
 if(x.on){let me=full(x);act().forEach(y=>{if(y.id===x.id)return;let o=full(y);if(o===me)add("err",`“${y.name}” paneliyle aynı adres: ${me}`);else if(x.url.mode==="subdirectory"&&y.url.mode==="subdirectory"&&base(x)===base(y)&&(me.startsWith(o+"/")||o.startsWith(me+"/")))add("warn",`“${y.name}” paneliyle iç içe yol: ${o} — yönlendirme sırası ve yetki ara katmanı ayrı tanımlanmalı.`)})}
 let g=fv("panel_url_strategy");if(g&&g!=="hybrid"&&g!==u.mode)add("warn",`Genel adres yaklaşımı “${fl("panel_url_strategy",g)}”, bu panel “${MODE[u.mode]}” kullanıyor. Genel yaklaşımı Hibrit yapın ya da paneli uyumlu hale getirin.`);
 let p=PA();if(p&&!p.apps.some(a=>a.id===u.app))add("warn","Seçilen uygulama listede yok; Ana web uygulaması varsayıldı.");
 if(!x.roles.length)add("err","En az bir rol tanımlayın.");else x.roles.forEach(r=>{if(!x.modules.some(m=>r.perms[m]))add("warn",`“${r.name}” rolünün bu paneldeki modüllerde hiçbir izni yok.`)});
 if(!x.modules.length)add("warn","Panelde modül seçilmedi.");
 let ugc=(fv("modules_extra")||[]).some(m=>["community","forum","listings"].includes(m))||["Open","Approval"].includes(fv("member_mode"));
 if(risky(x)&&u.mode==="subdirectory"&&ugc)add("warn","Yönetim paneli herkese açık siteyle aynı kökende ve sitede kullanıcı içeriği var: herkese açık sayfadaki bir XSS açığı panele ulaşabilir. Alt alan adı önerilir; değilse katı CSP ve içerik temizleme zorunlu.");
 if(risky(x)&&x.auth.mfa!=="required"&&x.auth.mfa!=="privileged")add("warn","Yetkili panelde çok adımlı doğrulama zorunlu değil.");
 if(!x.sec.noindex)add("warn","Panel arama motorlarından gizlenmiyor (noindex kapalı).");
 if(risky(x)&&effScope(x)==="parent")add("warn","Yetkili panel oturumu üst alan adında paylaşılıyor; yönetim oturumu host-only olmalı.");
 if(x.tpl==="cms_admin"&&fv("cms_mode")==="No CMS")add("warn","CMS Yönetim Paneli › CMS Yaklaşımı “CMS Yok” seçili.");
 if(x.tpl==="member_dashboard"&&fv("member_mode")==="None")add("warn","Üyelik & Giriş › Ziyaretçi Üyeliği “Üyelik yok” seçili.");
 if(fv("rbac")===false&&x.roles.length>1)add("info","Kimlik Doğrulama & Güvenlik › Rol Bazlı Yetki (RBAC) kapalı; birden çok rol tanımlandı.");
 if(x.data.scope==="platform"&&x.cat==="customer")add("warn","Müşteri tarafı panelin veri kapsamı “platform geneli”; organizasyon ya da kendi kayıtlarıyla sınırlanmalı.");
 return I}
const errN=x=>issues(x).filter(i=>i.lv!=="info").length;

/* ---------- teknik gereksinimler ---------- */
function req(x){let m=x.url.mode,R=[],sc=effScope(x),api=fv("panel_api_access");
 if(m==="subdomain")R.push("Ayrı köken: oturum çerezi Domain özelliği olmadan, __Host- önekiyle (Secure, HttpOnly, SameSite=Lax, Path=/) yazılır.","Alt alan adları aynı site (same-site) sayıldığından SameSite tek başına yetmez; durum değiştiren her istekte CSRF jetonu (senkronize ya da imzalı çift gönderim) doğrulanır.","DNS kaydı ve TLS sertifikası; HSTS includeSubDomains yalnız bütün alt alan adları HTTPS ise.");
 if(m==="subdirectory")R.push("Herkese açık siteyle aynı köken: çerez Path özelliği güvenlik sınırı değildir; panel oturumu ayrı ad (__Host-) taşır, CSRF jetonu zorunludur.","Panel rotalarına katı CSP (nonce), frame-ancestors 'none', Cache-Control: private, no-store ve X-Robots-Tag: noindex uygulanır.",`Yönlendirme: /${String(x.url.slug||"").replace(/^\/+|\/+$/g,"")} öneki uygulamada rota grubu (basePath) ya da edge / ters vekil kuralıyla ayrılır; site rotalarıyla çakışmaz.`);
 if(m==="separate_domain")R.push("Farklı site: çerez paylaşılamaz; ortak oturum yalnız OpenID Connect / SAML yönlendirmesiyle kurulur.","Ayrı TLS sertifikası, HSTS ve DNS; marka ve yasal metinler bu alan adında da yayınlanır.");
 if(api==="central_api"||(x.url.app!=="web"&&api!=="same_origin"))R.push(`API CORS izin listesine yalnız ${origin(x)} kökeni eklenir; Access-Control-Allow-Credentials yalnız bu listeye, joker (*) kullanılmaz.`);
 if(sc==="idp")R.push("Giriş ortak kimlik sağlayıcıya yönlenir (OIDC Authorization Code + PKCE); dönüş adresi tam eşleşmeyle kayıtlıdır, panel kendi oturumunu açar.");
 if(sc==="parent")R.push("Üst alan adına yazılan çerez yalnız kimlik sağlayıcı oturumu taşır; panel yetkisi host-only oturumda tutulur.");
 R.push("Her istek sunucuda kullanıcı + etkin organizasyon + rol + izin ile denetlenir; menü gizlemek yetkilendirme değildir. İstekle gelen kayıt kimliği etkin organizasyona ait değilse 404 döner (IDOR / BOLA).");
 return R}
function globalReq(){let L=["Kullanıcı, organizasyon, üyelik (kullanıcı + organizasyon + rol), rol, izin, rol-izin, panel ve panel erişimi ayrı tablolarda modellenir; bir kullanıcı birden çok organizasyona farklı rollerle üye olabilir.","Panel erişimi kullanıcının değil üyeliğin özelliğidir: kullanıcının etkin organizasyondaki rolü o panele erişim izni (panel.access) taşımıyorsa panel açılmaz.","Modül görünürlüğü izinden türetilir: kullanıcının hiçbir izni olmayan modül menüde gösterilmez; ancak asıl denetim her API çağrısında sunucuda yapılır.","Etkin organizasyon istemciden gelen değere değil, oturumdaki doğrulanmış üyeliğe göre belirlenir; organizasyon değiştirme ayrı bir uç noktadır ve denetim kaydına yazılır.","Yetki kararları tek bir politika katmanında (ör. can(kullanıcı, izin, kayıt)) verilir; denetleyiciler ve servisler bu katmanı çağırır, dağınık rol karşılaştırması yazılmaz.","Platform rolleri (süper yönetici, destek) organizasyon verisine yalnız gerekçe ve denetim kaydıyla, mümkünse kullanıcı adına görüntüleme (impersonation) ile erişir.","Rol ve izin değişiklikleri, panel erişimi verme / alma ve dışa aktarma işlemleri denetim kaydına yazılır."];
 if(fv("panel_authz")==="rbac_abac")L.push("ABAC kuralları (kayıt sahibi, durum, tutar, bölge…) RBAC izninin üstüne politika katmanında uygulanır ve birim testleriyle doğrulanır.");
 if(fv("panel_tenancy")==="multi_tenant")L.push("Her kiracı verisi tenant_id taşır; kiracı kimliği oturumdaki üyelikten alınır; kiracılar arası sorgu yalnız platform rolünde ve kayıtlıdır.");
 return L}

/* ---------- akıllı öneri ---------- */
function rec(){let ty=fv("project_type"),sc=K.scenarios.find(s=>s.types.includes(ty)),out=[],seen=new Set();if(sc)sc.panels.forEach(([tpl,mode,slug])=>{out.push({tpl,mode,slug,why:""});seen.add(tpl)});
 (fv("modules_extra")||[]).forEach(m=>K.extra.filter(e=>e.module===m).forEach(e=>{if(!seen.has(e.panel[0])){seen.add(e.panel[0]);out.push({tpl:e.panel[0],mode:e.panel[1],slug:e.panel[2],why:e.why})}}));return {sc,list:out}}
function recApply(){if(!requireProject())return;let {sc,list}=rec(),p=pa(),todo=list.filter(r=>!p.panels.some(x=>x.tpl===r.tpl));
 if(!todo.length&&!(sc&&sc.fields)){return}
 if(todo.length&&!confirm(`Önerilen ${todo.length} panel eklenecek:\n${todo.map(r=>"• "+TP[r.tpl].name+" — "+r.mode).join("\n")}\n\nMevcut paneller ve ayarlarınız değişmez.`))return;
 todo.forEach(r=>p.panels.push(mk(r.tpl,{mode:r.mode,slug:r.slug})));if(sc&&sc.fields)Object.entries(sc.fields).forEach(([k,v])=>{if(state[k]===undefined||state[k]===""){state[k]=v;try{faAuto(k)}catch(e){}}});
 commit(false);try{renderConfig()}catch(e){draw()}}

/* ---------- çıktı ---------- */
const g=id=>fv(id)?fl(id,fv(id)):"seçilmedi";
function permTxt(x,r){let L={m:[],w:[],r:[]};x.modules.forEach(m=>{let v=r.perms[m];if(L[v])L[v].push(mName(m))});return ["m","w","r"].filter(k=>L[k].length).map(k=>`${LV[k]}: ${L[k].join(", ")}`).join("; ")||"izin yok"}
function mName(id){if(MD[id])return MD[id].name;let p=PA(),c=p&&p.modules.find(m=>m.id===id);return c?c.name:id}
function allMods(){let p=PA();return K.modules.map(m=>({id:m.id,name:m.name,desc:m.desc,sensitive:m.sensitive,custom:false})).concat((p?p.modules:[]).map(m=>({id:m.id,name:m.name,desc:m.desc||"",sensitive:false,custom:true})))}
function pzConfig(){let P=panels(),p=PA()||{apps:[],modules:[]},h=host();
 return {panelArchitectureVersion:"1.0",baseDomain:h||null,publicSite:h?`https://${h}`:null,
  strategy:{url:fv("panel_url_strategy")||null,softwareArchitecture:fv("architecture_style")||null,appTopology:fv("panel_app_topology")||null,deploymentTopology:fv("panel_deploy_topology")||null,identity:fv("panel_identity")||null,authProvider:fv("auth_provider")||null,tenancy:fv("panel_tenancy")||null,dataIsolation:fv("panel_data_isolation")||null,authorization:fv("panel_authz")||null,session:fv("panel_session")||null,apiAccess:fv("panel_api_access")||null,adminHardening:fv("panel_admin_hardening")||[]},
  applications:p.apps.map(a=>({id:a.id,name:a.name,panels:P.filter(x=>x.url.app===a.id||(a.id==="web"&&!p.apps.some(b=>b.id===x.url.app))).map(x=>x.id)})),
  panels:P.map(x=>({id:x.id,template:x.tpl,name:x.name,category:x.cat,status:x.on?"active":"inactive",phase:x.phase,audience:x.audience,description:x.desc,
   url:{type:x.url.mode,slug:x.url.mode==="separate_domain"?null:x.url.slug,baseDomain:base(x),customDomain:x.url.mode==="separate_domain"?clean(x.url.domain)||null:null,fullUrl:full(x),routingMode:effRouting(x),application:app(x.url.app).id,deploymentBoundary:effBoundary(x),authenticationScope:effScope(x)},
   authentication:{identitySource:x.auth.source,methods:x.auth.methods,mfa:x.auth.mfa,session:x.auth.session,loginPath:x.auth.login||null},
   roles:x.roles.map(r=>{let o={};x.modules.forEach(m=>{if(LVE[r.perms[m]])o[m]=LVE[r.perms[m]]});return {id:r.id,name:r.name,scope:r.scope,permissions:o}}),abacRules:x.abac||null,
   modules:x.modules.slice(),dataIsolation:{scope:x.data.scope,crossOrganizationAccess:x.data.cross,piiMasking:x.data.pii,export:x.data.export},
   branding:Object.assign({},x.brand),security:Object.assign({},x.sec),deployment:Object.assign({},x.deploy,{boundary:effBoundary(x)}),
   requirements:req(x),issues:issues(x).map(i=>({level:i.lv==="err"?"error":i.lv==="warn"?"warning":"info",text:i.t}))})),
  modules:allMods().filter(m=>P.some(x=>x.modules.includes(m.id))).map(m=>({id:m.id,name:m.name,custom:m.custom,panels:P.filter(x=>x.modules.includes(m.id)).map(x=>x.id)})),
  model:{entities:["User","Organization","Membership(user, organization, role)","Role","Permission","RolePermission","Panel","PanelAccess(role, panel)","AuditLog"],rules:globalReq()},
  permissionLevels:{read:"Görüntüle",write:"Oluştur / düzenle",manage:"Sil, onayla, yapılandır"}}}
function specSections(){let A=act(),P=panels(),pas=P.filter(x=>!x.on),p=PA(),h=host(),n=a=>a.map((y,i)=>`${i+1}. ${y}`).join("\n"),S=[];
 S.push(["PANEL ENVANTERİ",A.map(x=>`${x.name} (${TP[x.tpl].en} şablonu) — ${PH[x.phase]} · Kitle: ${x.audience||"—"} · Amaç: ${x.desc||"—"}`).concat(pas.map(x=>`${x.name} — Pasif: bu sürümde kurulmayacak, adresi ve rolleri ayrılmış olarak kalır.`))]);
 S.push(["URL MİMARİSİ",[`Herkese açık site: ${h?"https://"+h:"(Ortak Bilgiler › Canlı Site Adresi girilmedi)"}`].concat(A.map(x=>`${x.name}: ${full(x)} — ${MODE[x.url.mode]}${x.url.mode!=="separate_domain"?`, slug “${x.url.slug}”`:""}`)),`Genel yaklaşım: ${g("panel_url_strategy")}. Rezerve yollar (${K.reserved.paths.slice(0,12).join(", ")} …) ve altyapı alt alan adları (${K.reserved.subdomains.slice(0,8).join(", ")} …) panel adresi olarak kullanılmaz.`]);
 S.push(["YÖNLENDİRME (ROUTING) KURALLARI",A.map(x=>`${x.name}: ${ROUT[effRouting(x)]}; ${app(x.url.app).name} sunar.`).concat(["Bir alt alan adı kendiliğinden ayrı uygulama demek değildir: aynı uygulama ana makine adına göre panel rota grubunu seçer; ayrı uygulama yalnız envanterde öyle tanımlanan panellerde kurulur.","Panel rotaları ortak yetki ara katmanından geçer; oturumu olmayan istek panelin giriş adresine, yetkisi olmayan istek 403 sayfasına yönlenir."])]);
 S.push(["UYGULAMA SINIRLARI",(p?p.apps:[]).map(a=>{let L=A.filter(x=>app(x.url.app).id===a.id);return L.length?`${a.name}: ${L.map(x=>`${x.name} (${BND[effBoundary(x)].toLocaleLowerCase("tr")})`).join(", ")}`:""}).filter(Boolean).concat([`Yazılım mimarisi: ${g("architecture_style")}; panel uygulama topolojisi: ${g("panel_app_topology")}; dağıtım topolojisi: ${g("panel_deploy_topology")}. Bu üç karar ayrı tutulur.`])]);
 S.push(["KULLANICI VE ORGANİZASYON İLİŞKİLERİ",[`Organizasyon modeli: ${g("panel_tenancy")}.`].concat(globalReq().slice(0,4))]);
 S.push(["KİMLİK DOĞRULAMA MİMARİSİ",[`Paneller arası kimlik: ${g("panel_identity")}; kimlik altyapısı: ${g("auth_provider")}; oturum ve çerez: ${g("panel_session")}.`].concat(A.map(x=>`${x.name}: ${SRC[x.auth.source]} · ${x.auth.methods.length?x.auth.methods.map(m=>(METH.find(z=>z[0]===m)||[0,m])[1]).join(", "):"giriş yöntemi proje kararından"} · MFA ${MFA[x.auth.mfa].toLocaleLowerCase("tr")} · oturum ${SESS[x.auth.session].toLocaleLowerCase("tr")} · kapsam: ${ASC[effScope(x)]}${x.auth.login?` · giriş adresi ${x.auth.login}`:""}`))]);
 S.push(["ROL VE İZİN MATRİSİ",[`Yetkilendirme modeli: ${g("panel_authz")}. İzin düzeyleri: Görüntüle (read), Düzenle (oluştur / güncelle), Yönet (sil, onayla, yapılandır). Belirtilmeyen modülde izin yoktur (varsayılan reddet).`].concat(A.flatMap(x=>x.roles.map(r=>`${x.name} › ${r.name} (${SCOPE[r.scope].toLocaleLowerCase("tr")}): ${permTxt(x,r)}`)).concat(A.filter(x=>x.abac.trim()).map(x=>`${x.name} ABAC kuralları: ${x.abac.trim().replace(/\s*\n\s*/g," · ")}`)))]);
 S.push(["MODÜL DAĞILIMI",allMods().filter(m=>A.some(x=>x.modules.includes(m.id))).map(m=>`${m.name}${m.custom?" (özel modül)":""}: ${A.filter(x=>x.modules.includes(m.id)).map(x=>x.name).join(", ")}`).concat(["Aynı modül birden çok panelde tek iş katmanını paylaşır; panel farkı yalnız rol, izin ve veri kapsamıyla yapılır, modül kodu kopyalanmaz."])]);
 S.push(["VERİTABANI ERİŞİM VE İZOLASYON KURALLARI",[`Veri izolasyonu: ${fv("panel_tenancy")==="single_org"||!fv("panel_tenancy")?"tek kurum (organizasyon tablosu yine tutulur)":g("panel_data_isolation")}.`].concat(A.map(x=>`${x.name}: kapsam ${DSC[x.data.scope].toLocaleLowerCase("tr")}; organizasyonlar arası erişim: ${CROSS[x.data.cross].toLocaleLowerCase("tr")}; kişisel veri: ${PII[x.data.pii].toLocaleLowerCase("tr")}; dışa aktarma: ${EXP[x.data.export].toLocaleLowerCase("tr")}.`)).concat(["Organizasyon kimliği taşıyan her sorgu etkin organizasyonla filtrelenir; filtre ORM varsayılan kapsamı ya da satır düzeyi güvenlikle zorunlu tutulur, atlanması kod incelemesinde reddedilir."])]);
 S.push(["DAĞITIM PLANI",A.map(x=>`${x.name}: ${BND[effBoundary(x)]} · ortamlar: ${x.deploy.env.map(e=>(ENV.find(z=>z[0]===e)||[0,e])[1]).join(", ")} · önbellek ${CACHE[x.deploy.cache]||x.deploy.cache} · yayın: ${REL[x.deploy.release]||x.deploy.release}${x.deploy.region?` · bölge ${x.deploy.region}`:""}`)]);
 S.push(["GÜVENLİK GEREKSİNİMLERİ",[`Yönetim panellerinde zorunlu önlemler: ${(fv("panel_admin_hardening")||[]).map(v=>fl("panel_admin_hardening",v)).join(", ")||"bölüm kararında seçilmedi"}.`].concat(A.map(x=>`${x.name}: ${SECO.filter(([k])=>x.sec[k]).map(z=>z[1]).join(", ")||"ek önlem yok"}.`)).concat(A.flatMap(x=>req(x).map(r=>`${x.name} — ${r}`)))]);
 let W=A.flatMap(x=>issues(x).filter(i=>i.lv!=="info").map(i=>`${x.name}: ${i.t}`));if(W.length)S.push(["AÇIK UYARILAR (kullanıcıya sorulmadan çözülmez)",W]);
 return S}
function pzPrompt(){if(!pzActive())return "";let S=specSections();return `\n\nPANEL VE PORTAL MİMARİSİ\nAşağıdakiler Panel & Portal Mimarisi bölümündeki envanterden üretilmiştir ve bağlayıcıdır. Yeni panel, adres veya rol açık onay olmadan eklenmez. Makine tarafından okunabilir yapılandırma proje dosyasında panelArchitecture alanındadır.\n`+S.map(([h,L],i)=>`\n${i+1}. ${h}\n${L.map(y=>"- "+y).join("\n")}`).join("\n")}
function pzMd(){if(!pzActive())return "";let S=specSections();return `### Panel ve portal mimarisi\nPanel & Portal Mimarisi envanterinden üretilmiştir ve bağlayıcıdır; yeni panel, adres veya rol açık onay olmadan eklenmez.\n\n`+S.map(([h,L])=>`#### ${h.charAt(0)+h.slice(1).toLocaleLowerCase("tr")}\n${L.map(y=>"- "+y).join("\n")}`).join("\n\n")+`\n\n#### Panel mimarisi (JSON)\n\`\`\`json\n${JSON.stringify(pzConfig(),null,2)}\n\`\`\``}
function ruleItems(){let A=act();return A.map(x=>`${x.name}: ${full(x)} · ${app(x.url.app).name} · ${ASC[effScope(x)]} · ${x.roles.length} rol · ${x.modules.length} modül${x.on?"":" · pasif"}.`).concat(panels().filter(x=>!x.on).map(x=>`${x.name}: pasif — bu sürümde kurulmayacak.`)).concat(globalReq().slice(1,3))}
function pzRuleGroups(){if(!pzActive())return "";return `<div class="rulegroup"><h3>Panel &amp; Portal Envanteri</h3><ol>${ruleItems().map(x=>`<li>${E(x)}</li>`).join("")}</ol></div>`}
function pzPf(){return pzActive()?{panelArchitecture:pzConfig()}:{}}
Object.assign(window,{pzActive,pzPrompt,pzMd,pzRuleGroups,pzPf,pzConfig});

/* ---------- çizim ---------- */
const opt=(o,v)=>Object.entries(o).map(([k,l])=>`<option value="${E(k)}"${k===v?" selected":""}>${E(l)}</option>`).join("");
const sel=(key,o,v,lb,extra)=>`<label class="pzF"><span>${lb}</span><select data-pzf="${key}" data-pzk="f:${key}">${extra||""}${opt(o,v)}</select></label>`;
const txt=(key,v,lb,ph,hint)=>`<label class="pzF"><span>${lb}</span><input type="text" data-pzf="${key}" data-pzk="f:${key}" value="${E(v||"")}" placeholder="${E(ph||"")}" autocomplete="off" spellcheck="false">${hint?`<small>${hint}</small>`:""}</label>`;
const fieldLink=(id,t)=>FI[id]?`<button type="button" class="linkBtn" data-pz="go" data-fid="${id}">${E(t||FI[id].label)} →</button>`:"";
function iss(x){let I=issues(x);return I.length?`<ul class="pzIss">${I.map(i=>`<li class="${i.lv}">${E(i.t)}</li>`).join("")}</ul>`:`<p class="pzOk">Adres ve yapılandırma uyarısı yok.</p>`}
function card(x){let n=errN(x),on=x.on,ch=UI.sel.has(x.id);return `<article class="pzCard ${on?"on":"off"}${ch?" sel":""}" data-id="${x.id}">
 <div class="pzCT"><input type="checkbox" data-pz="sel" data-id="${x.id}" data-pzk="sel:${x.id}" aria-label="Seç: ${E(x.name)}"${ch?" checked":""}><h4><button type="button" class="pzName" data-pz="open" data-id="${x.id}" data-pzk="open:${x.id}">${E(x.name)}</button></h4><span class="pzSt ${on?"on":"off"}">${on?"Aktif":"Pasif"}</span></div>
 <p class="pzUrl">${E(full(x))}</p><p class="pzMeta">${E(MODE[x.url.mode])} · ${x.modules.length} modül · ${x.roles.length} rol · ${E(app(x.url.app).name)}${x.tpl==="custom"?" · Özel":""}</p>
 ${n?`<p class="pzWarnN">${n} uyarı</p>`:""}
 <div class="pzActs"><button type="button" class="btn" data-pz="open" data-id="${x.id}">Düzenle</button><button type="button" class="btn" data-pz="toggle" data-id="${x.id}" data-pzk="tg:${x.id}">${on?"Pasifleştir":"Etkinleştir"}</button><button type="button" class="btn pzDel" data-pz="del" data-id="${x.id}">Kaldır</button></div></article>`}
function tcard(t){let g0=fv("panel_url_strategy"),m=g0&&g0!=="hybrid"&&MODE[g0]?g0:t.mode,pv=m==="subdomain"?`${t.slug}.${apex(host()||"alanadi.com")}`:m==="subdirectory"?`${host()||"alanadi.com"}/${t.slug}`:"ayrı alan adı";
 return `<article class="pzCard tpl"><div class="pzCT"><h4>${E(t.name)}</h4><small>${E(t.en)}</small></div><p class="pzDesc">${E(t.desc)}</p><p class="pzMeta">Kitle: ${E(t.audience)} · Önerilen adres: ${E(pv)} · ${t.modules.length} modül · ${t.roles.length} rol</p><div class="pzActs"><button type="button" class="btn dark" data-pz="add" data-tpl="${t.id}" data-pzk="add:${t.id}">Projeye ekle</button></div></article>`}
function hay(s){return norm(s)}
function match(o){let q=UI.q.trim();if(!q)return true;let h=hay(o);return norm(q).split(/\s+/).filter(Boolean).every(w=>typeof hit==="function"?hit(h,w):h.includes(w))}
function listHtml(){let P=panels(),items=[];P.forEach(x=>items.push({k:"p",x,cat:x.cat,h:[x.name,TP[x.tpl].name,TP[x.tpl].en,x.audience,x.desc,full(x)].join(" ")}));
 K.templates.forEach(t=>{if(t.id==="custom"||P.some(x=>x.tpl===t.id))return;items.push({k:"t",t,cat:t.cat,h:[t.name,t.en,t.audience,t.desc,t.slug].join(" ")})});
 let f=items.filter(i=>(!UI.cat||i.cat===UI.cat)&&match(i.h)&&(UI.st===""||(UI.st==="out"?i.k==="t":i.k==="p"&&(UI.st==="in"||(UI.st==="on"&&i.x.on)||(UI.st==="off"&&!i.x.on)||(UI.st==="warn"&&errN(i.x))))));
 let html=K.categories.map(c=>{let L=f.filter(i=>i.cat===c.id),add=c.id==="custom"&&(!UI.cat||UI.cat==="custom")&&UI.st!=="on"&&UI.st!=="off"&&UI.st!=="warn"&&UI.st!=="in";if(!L.length&&!add)return "";
  return `<section class="pzCat" aria-label="${E(c.name)}"><h4 class="pzCatH">${E(c.name)} <small>${L.length}</small></h4><div class="pzGrid">${L.map(i=>i.k==="p"?card(i.x):tcard(i.t)).join("")}${add?`<article class="pzCard newC"><h4>Özel panel</h4><p class="pzDesc">Şablonlarda karşılığı olmayan bir panel: adını, kitlesini, adresini, modüllerini ve rollerini siz belirlersiniz. İstediğiniz kadar özel panel eklenebilir.</p><div class="pzActs"><button type="button" class="btn dark" data-pz="new" data-pzk="new">+ Yeni özel panel</button></div></article>`:""}</div></section>`}).join("");
 return html||`<p class="pzEmpty">Aramaya uyan panel yok. <button type="button" class="linkBtn" data-pz="clearf">Filtreleri temizle</button></p>`}
function recHtml(){let {sc,list}=rec(),P=panels(),h=host()||"alanadi.com";if(!fv("project_type"))return `<div class="pzRec"><p><b>Akıllı öneri:</b> Proje türü seçilince başlangıç panel mimarisi önerilir. ${fieldLink("project_type","Proje Türü")}</p></div>`;
 if(!list.length)return "";let miss=list.filter(r=>!P.some(x=>x.tpl===r.tpl)).length,pv=r=>r.mode==="subdomain"?`${r.slug}.${apex(h)}`:`${h}/${r.slug}`;
 return `<div class="pzRec"><div class="pzRecH"><h4>Önerilen başlangıç mimarisi${sc?`: ${E(sc.name)}`:""}</h4>${miss?`<button type="button" class="btn dark" data-pz="recapply" data-pzk="recapply">Öneriyi uygula (${miss} panel)</button>`:`<span class="pzSt on">Öneri uygulandı</span>`}</div>
 ${sc?`<p>${E(sc.why)} Değiştirilebilir bir başlangıçtır, zorunlu kural değildir.</p>`:""}<ul><li><span>Herkese açık site</span><b>${E(h)}</b></li>${list.map(r=>`<li><span>${E(TP[r.tpl].name)}${r.why?` <small>(${E(r.why)})</small>`:""}</span><b>${E(pv(r))}</b>${P.some(x=>x.tpl===r.tpl)?'<em>Projede</em>':""}</li>`).join("")}</ul></div>`}
function toolbar(){let P=panels(),n=UI.sel.size,cnt=c=>panels().filter(x=>x.cat===c).length+K.templates.filter(t=>t.cat===c&&t.id!=="custom"&&!P.some(x=>x.tpl===t.id)).length;
 return `<div class="pzBar"><label class="pzSearch"><span class="sr">Panel ara</span><input type="search" data-pzq data-pzk="q" value="${E(UI.q)}" placeholder="Panel ara: ad, kitle, adres…" autocomplete="off"></label>
 <div class="pzChips" role="group" aria-label="Kategori"><button type="button" class="pzChip" data-pz="cat" data-c="" aria-pressed="${!UI.cat}" data-pzk="cat:">Tümü</button>${K.categories.map(c=>`<button type="button" class="pzChip" data-pz="cat" data-c="${c.id}" aria-pressed="${UI.cat===c.id}" data-pzk="cat:${c.id}">${E(c.name)}<small>${cnt(c.id)}</small></button>`).join("")}</div>
 <div class="pzChips" role="group" aria-label="Durum">${STS.map(([k,l])=>`<button type="button" class="pzChip sm" data-pz="st" data-s="${k}" aria-pressed="${UI.st===k}" data-pzk="st:${k}">${l}</button>`).join("")}</div>
 ${P.length?`<div class="pzBulk" role="group" aria-label="Çoklu seçim"><button type="button" class="linkBtn" data-pz="selall">Görünen panelleri seç</button>${n?`<b>${n} panel seçili:</b><button type="button" class="btn" data-pz="bulk" data-a="on">Etkinleştir</button><button type="button" class="btn" data-pz="bulk" data-a="off">Pasifleştir</button><button type="button" class="btn pzDel" data-pz="bulk" data-a="del">Kaldır</button><button type="button" class="linkBtn" data-pz="selnone">Seçimi temizle</button>`:""}</div>`:""}</div>`}
function tabHtml(x,t){let k=x.id,u=x.url,sc=fv("panel_tenancy");
 if(t==="general")return `<div class="pzForm">${txt("name",x.name,"Panel adı")}<label class="pzF"><span>Kategori</span><select data-pzf="cat" data-pzk="f:cat">${K.categories.map(c=>`<option value="${c.id}"${c.id===x.cat?" selected":""}>${E(c.name)}</option>`).join("")}</select></label>
  ${txt("audience",x.audience,"Kullanıcı kitlesi","Ör. bayi satış ekipleri")}${sel("on",{"true":"Aktif — bu sürümde kurulacak","false":"Pasif — envanterde kalır, kurulmaz"},String(x.on),"Durum")}${sel("phase",PH,x.phase,"Yayın aşaması")}
  <label class="pzF wide"><span>Amaç ve kapsam</span><textarea data-pzf="desc" data-pzk="f:desc" rows="3">${E(x.desc)}</textarea></label></div><p class="pzNote">Şablon: ${E(TP[x.tpl].name)} (${E(TP[x.tpl].en)}). Şablon yalnız başlangıç önerisidir; modül, rol ve izinler bu panelde serbestçe değiştirilebilir.</p>`;
 if(t==="url"){let p=pa();return `<div class="pzForm">${sel("url.mode",MODE,u.mode,"Adres türü")}${u.mode==="separate_domain"?txt("url.domain",u.domain,"Ayrı alan adı","bayi-markasi.com","Yalnız alan adı; https:// gerekmez."):txt("url.slug",u.slug,u.mode==="subdomain"?"Alt alan adı (slug)":"Alt dizin yolu (slug)",u.mode==="subdomain"?"admin":"admin","Küçük harf, rakam ve kısa çizgi.")}
  ${txt("url.base",u.base,"Ana alan adı",host()||"alanadi.com",host()?`Boş bırakılırsa Ortak Bilgiler › Canlı Site Adresi: ${E(host())}`:"Ortak Bilgiler › Canlı Site Adresi girilmedi.")}
  <div class="pzF wide pzPrev"><span>Tam adres önizlemesi</span><output data-pzlive="url">${E(full(x))}</output></div>
  ${sel("url.routing",ROUT,u.routing,"Yönlendirme modu",`<option value="">Otomatik: ${E(ROUT[effRouting(Object.assign({},x,{url:Object.assign({},u,{routing:""})}))])}</option>`)}
  <label class="pzF"><span>Sunan uygulama</span><select data-pzf="url.app" data-pzk="f:url.app">${p.apps.map(a=>`<option value="${E(a.id)}"${a.id===u.app?" selected":""}>${E(a.name)}</option>`).join("")}</select><small>Alt alan adı ayrı uygulama gerektirmez; aynı uygulama ana makine adına göre yönlendirebilir.</small></label>
  <div class="pzF pzAddApp"><span>Yeni uygulama</span><div><input type="text" data-pzk="newapp" id="pzNewApp" placeholder="Ör. Yönetim uygulaması" autocomplete="off"><button type="button" class="btn" data-pz="addapp">Ekle ve seç</button></div></div>
  ${sel("url.boundary",BND,u.boundary,"Dağıtım sınırı",`<option value="">Kararı izle: ${E(BND[effBoundary(Object.assign({},x,{url:Object.assign({},u,{boundary:""})}))])}</option>`)}
  ${sel("url.authScope",ASC,u.authScope,"Kimlik doğrulama kapsamı",`<option value="">Otomatik: ${E(ASC[effScope(Object.assign({},x,{url:Object.assign({},u,{authScope:""})}))])}</option>`)}</div>
  <div data-pzlive="issues">${iss(x)}</div><h5>Bu adres türü için teknik gereksinimler</h5><ul class="pzReq">${req(x).map(r=>`<li>${E(r)}</li>`).join("")}</ul>`}
 if(t==="auth")return `<div class="pzForm">${sel("auth.source",SRC,x.auth.source,"Kimlik kaynağı")}${sel("auth.mfa",MFA,x.auth.mfa,"Çok adımlı doğrulama")}${sel("auth.session",SESS,x.auth.session,"Oturum süresi")}${txt("auth.login",x.auth.login,"Giriş adresi (isteğe bağlı)",x.url.mode==="subdirectory"?`/${x.url.slug}/giris`:"/giris")}
  <fieldset class="pzF wide pzChecks"><legend>Giriş yöntemleri</legend>${METH.map(([v,l])=>`<label><input type="checkbox" data-pzarr="auth.methods" value="${v}" data-pzk="m:${v}"${x.auth.methods.includes(v)?" checked":""}> ${E(l)}</label>`).join("")}<small>Boş bırakılırsa Üyelik & Giriş › Giriş Yöntemleri kararı uygulanır.</small></fieldset></div>
  <p class="pzNote">Paneller arası kimlik: <b>${E(g("panel_identity"))}</b> ${fieldLink("panel_identity","Değiştir")} · Kimlik altyapısı: <b>${E(g("auth_provider"))}</b> ${fieldLink("auth_provider","Değiştir")} · Bu panelin kapsamı: <b>${E(ASC[effScope(x)])}</b></p>`;
 if(t==="roles"){let M=x.modules.map(m=>({id:m,name:mName(m)}));return `<p class="pzNote">Yetkilendirme modeli: <b>${E(g("panel_authz"))}</b> ${fieldLink("panel_authz","Değiştir")}. İzinler her istekte sunucuda denetlenir; menüde gizlemek yetki değildir. Görüntüle &lt; Düzenle (oluştur / güncelle) &lt; Yönet (sil, onayla, yapılandır).</p>
  <div class="pzRoles">${x.roles.map((r,i)=>`<div class="pzRole"><label class="pzF"><span>Rol adı</span><input type="text" data-pzr="${i}|name" data-pzk="r:${i}:n" value="${E(r.name)}"></label><label class="pzF"><span>Kapsam</span><select data-pzr="${i}|scope" data-pzk="r:${i}:s">${opt(SCOPE,r.scope)}</select></label><button type="button" class="btn pzDel" data-pz="delrole" data-i="${i}" aria-label="${E(r.name)} rolünü sil">Sil</button></div>`).join("")}</div>
  <div class="pzActs"><button type="button" class="btn" data-pz="addrole" data-pzk="addrole">+ Rol ekle</button><button type="button" class="linkBtn" data-pz="resetroles">Şablonun rollerine dön</button></div>
  ${M.length&&x.roles.length?`<div class="pzMatrixW" tabindex="0" role="region" aria-label="İzin matrisi"><table class="pzMatrix"><caption class="sr">${E(x.name)} izin matrisi</caption><thead><tr><th scope="col">Modül</th>${x.roles.map(r=>`<th scope="col">${E(r.name)}</th>`).join("")}</tr></thead><tbody>${M.map(m=>`<tr><th scope="row">${E(m.name)}</th>${x.roles.map((r,i)=>`<td><select data-pzp="${i}|${E(m.id)}" data-pzk="p:${i}:${E(m.id)}" aria-label="${E(r.name)} — ${E(m.name)}" class="lv${r.perms[m.id]||"0"}"><option value="">—</option>${opt(LV,r.perms[m.id]||"")}</select></td>`).join("")}</tr>`).join("")}</tbody></table></div>`:`<p class="pzEmpty">Matris için önce modül ve rol ekleyin.</p>`}
  <label class="pzF wide"><span>ABAC kuralları (isteğe bağlı, satır başına bir kural)</span><textarea data-pzf="abac" data-pzk="f:abac" rows="3" placeholder="Ör. Satış temsilcisi yalnız kendi atandığı müşterileri görür.&#10;250.000 TL üstü teklif onayı için Satın alma müdürü gerekir.">${E(x.abac)}</textarea>${fv("panel_authz")==="rbac_abac"?"":"<small>Yetkilendirme modeli “RBAC + ABAC” değilse bu kurallar uyarı olarak prompta yazılır.</small>"}</label>`}
 if(t==="modules"){let A=allMods();return `<p class="pzNote">Aynı modül birden çok panelde kullanılabilir; panel farkı rol, izin ve veri kapsamıyla yapılır. Modül kaldırılınca rol izinleri saklanır ama çıktıya yazılmaz.</p>
  <fieldset class="pzChecks pzMods"><legend>Modüller (${x.modules.length})</legend>${A.map(m=>`<label class="${m.custom?"cm":""}"><input type="checkbox" data-pzmod="${E(m.id)}" data-pzk="mod:${E(m.id)}"${x.modules.includes(m.id)?" checked":""}> <span><b>${E(m.name)}</b>${m.sensitive?' <em>hassas</em>':""}${m.custom?' <em class="c">özel</em>':""}<small>${E(m.desc||"")}</small></span>${m.custom?`<button type="button" class="linkBtn" data-pz="delmod" data-m="${E(m.id)}" aria-label="${E(m.name)} özel modülünü sil">Sil</button>`:""}</label>`).join("")}</fieldset>
  <div class="pzF wide pzAddApp"><span>Yeni özel modül (bütün panellerde seçilebilir)</span><div><input type="text" id="pzNewMod" data-pzk="newmod" placeholder="Ör. Garanti kayıtları" autocomplete="off"><input type="text" id="pzNewModD" data-pzk="newmodd" placeholder="Kısa açıklama (isteğe bağlı)" autocomplete="off"><button type="button" class="btn" data-pz="addmod">Ekle</button></div></div>`}
 if(t==="data")return `<div class="pzForm">${sel("data.scope",DSC,x.data.scope,"Veri kapsamı")}${sel("data.cross",CROSS,x.data.cross,"Organizasyonlar arası erişim")}${sel("data.pii",PII,x.data.pii,"Kişisel veri gösterimi")}${sel("data.export",EXP,x.data.export,"Toplu dışa aktarma")}</div>
  <p class="pzNote">Organizasyon modeli: <b>${E(g("panel_tenancy"))}</b> ${fieldLink("panel_tenancy","Değiştir")}${sc&&sc!=="single_org"?` · İzolasyon yöntemi: <b>${E(g("panel_data_isolation"))}</b> ${fieldLink("panel_data_isolation","Değiştir")}`:""}. Etkin organizasyon her zaman oturumdaki doğrulanmış üyelikten alınır.</p>`;
 if(t==="brand")return `<div class="pzForm">${sel("brand.theme",THEME,x.brand.theme,"Tema kaynağı")}${sel("brand.layout",LAY,x.brand.layout,"Gezinme düzeni")}${sel("brand.density",DENS,x.brand.density,"Yoğunluk")}${sel("brand.lang",LANG,x.brand.lang,"Dil")}${sel("brand.mode",CMODE,x.brand.mode,"Renk modu")}</div><p class="pzNote">Renk ve yazı tipleri Ortak Bilgiler › Marka Görünümü’nden alınır; panelde ayrı marka yalnız “beyaz etiket” seçilince uygulanır.</p>`;
 if(t==="security"){let H=fv("panel_admin_hardening")||[];return `<fieldset class="pzChecks"><legend>Bu paneldeki güvenlik önlemleri</legend>${SECO.map(([k2,l])=>`<label><input type="checkbox" data-pzbool="sec.${k2}" data-pzk="s:${k2}"${x.sec[k2]?" checked":""}> ${E(l)}</label>`).join("")}</fieldset>
  ${risky(x)?`<p class="pzNote">Yetkili panel: bölüm kararındaki zorunlu önlemler de uygulanır — ${H.length?E(H.map(v=>fl("panel_admin_hardening",v)).join(", ")):"henüz seçilmedi"} ${fieldLink("panel_admin_hardening","Düzenle")}</p>`:""}<p class="pzNote">CSRF koruması, Secure + HttpOnly çerez ve sunucu tarafı yetki denetimi her panelde zorunludur ve kapatılamaz.</p><div data-pzlive="issues">${iss(x)}</div>`}
 if(t==="deploy")return `<div class="pzForm">${sel("url.boundary",BND,u.boundary,"Dağıtım sınırı",`<option value="">Kararı izle: ${E(BND[effBoundary(Object.assign({},x,{url:Object.assign({},u,{boundary:""})}))])}</option>`).replace('data-pzk="f:url.boundary"','data-pzk="f:url.boundary2"')}${sel("deploy.release",REL,x.deploy.release,"Yayın stratejisi")}${sel("deploy.cache",CACHE,x.deploy.cache,"Önbellek")}${txt("deploy.region",x.deploy.region,"Bölge (isteğe bağlı)","Ör. AB / Türkiye")}
  <fieldset class="pzF wide pzChecks"><legend>Ortamlar</legend>${ENV.map(([v,l])=>`<label><input type="checkbox" data-pzarr="deploy.env" value="${v}" data-pzk="e:${v}"${x.deploy.env.includes(v)?" checked":""}> ${E(l)}</label>`).join("")}</fieldset></div>
  <p class="pzNote">Panel dağıtım topolojisi: <b>${E(g("panel_deploy_topology"))}</b> ${fieldLink("panel_deploy_topology","Değiştir")} · Sunan uygulama: <b>${E(app(u.app).name)}</b></p>`;
 return ""}
function detail(x){let t=TABS.find(z=>z[0]===UI.tab)?UI.tab:"general";return `<div class="pzDetail"><div class="pzDH"><div class="pzBack"><button type="button" class="linkBtn" data-pz="back" data-pzk="back">← Panel listesi</button></div><h4 data-pzlive="name">${E(x.name)}</h4><span class="pzSt ${x.on?"on":"off"}">${x.on?"Aktif":"Pasif"}</span><p class="pzUrl" data-pzlive="url">${E(full(x))}</p>
 <div class="pzActs"><button type="button" class="btn" data-pz="toggle" data-id="${x.id}" data-pzk="dtg">${x.on?"Pasifleştir":"Etkinleştir"}</button><button type="button" class="btn" data-pz="dup" data-id="${x.id}">Çoğalt</button><button type="button" class="btn pzDel" data-pz="del" data-id="${x.id}">Kaldır</button></div></div>
 <div class="pzTabs" role="tablist" aria-label="${E(x.name)} ayarları">${TABS.map(([k,l])=>`<button type="button" role="tab" id="pzt-${k}" aria-controls="pztp" aria-selected="${k===t}" tabindex="${k===t?0:-1}" data-pz="tab" data-t="${k}" data-pzk="tab:${k}">${l}</button>`).join("")}</div>
 <div class="pzTP" role="tabpanel" id="pztp" aria-labelledby="pzt-${t}" tabindex="0">${tabHtml(x,t)}</div></div>`}
function sumHtml(){let A=act(),p=PA();if(!p||!panels().length)return "";let W=A.flatMap(x=>issues(x).filter(i=>i.lv!=="info").map(i=>[x.name,i]));
 return `<details class="pzSum" data-pz="sumtg"${UI.sum?" open":""}><summary>Mimari özeti <small>${A.length} aktif panel · ${p.apps.length} uygulama${W.length?` · ${W.length} uyarı`:""}</small></summary>
 <dl class="pzKV">${[["panel_url_strategy","Adres yaklaşımı"],["architecture_style","Yazılım mimarisi"],["panel_app_topology","Uygulama topolojisi"],["panel_deploy_topology","Dağıtım topolojisi"],["panel_identity","Paneller arası kimlik"],["panel_tenancy","Organizasyon modeli"],["panel_authz","Yetkilendirme"],["panel_session","Oturum ve çerez"],["panel_api_access","API erişimi"]].map(([id,l])=>`<dt>${l}</dt><dd>${E(g(id))} ${fieldLink(id,"Değiştir")}</dd>`).join("")}</dl>
 <h5>Uygulamalar</h5><div class="pzApps">${p.apps.map(a=>`<div class="pzAppR"><input type="text" data-pzapp="${E(a.id)}" data-pzk="app:${E(a.id)}" value="${E(a.name)}" aria-label="Uygulama adı"><span>${A.filter(x=>app(x.url.app).id===a.id).map(x=>E(x.name)).join(", ")||"Panel yok"}</span>${a.id==="web"?"":`<button type="button" class="linkBtn" data-pz="delapp" data-a="${E(a.id)}">Kaldır</button>`}</div>`).join("")}</div>
 <h5>URL tablosu</h5><div class="pzMatrixW" tabindex="0" role="region" aria-label="URL tablosu"><table class="pzT"><thead><tr><th>Panel</th><th>Adres</th><th>Tür</th><th>Uygulama</th><th>Dağıtım</th><th>Oturum kapsamı</th></tr></thead><tbody><tr><td>Herkese açık site</td><td>${E(host()?"https://"+host():"—")}</td><td>—</td><td>Ana web uygulaması</td><td>—</td><td>—</td></tr>${A.map(x=>`<tr><td>${E(x.name)}</td><td>${E(full(x))}</td><td>${E(MODE[x.url.mode])}</td><td>${E(app(x.url.app).name)}</td><td>${E(BND[effBoundary(x)])}</td><td>${E(ASC[effScope(x)])}</td></tr>`).join("")}</tbody></table></div>
 <h5>Modül dağılımı</h5><ul class="pzReq">${allMods().filter(m=>A.some(x=>x.modules.includes(m.id))).map(m=>`<li><b>${E(m.name)}</b>: ${A.filter(x=>x.modules.includes(m.id)).map(x=>E(x.name)).join(", ")}</li>`).join("")||"<li>Modül yok.</li>"}</ul>
 ${W.length?`<h5>Uyarılar</h5><ul class="pzIss">${W.map(([n,i])=>`<li class="${i.lv}"><b>${E(n)}:</b> ${E(i.t)}</li>`).join("")}</ul>`:""}
 <h5>Ortak yetki ve veri kuralları</h5><ul class="pzReq">${globalReq().map(r=>`<li>${E(r)}</li>`).join("")}</ul>
 <div class="pzActs"><button type="button" class="btn" data-pz="dl">Mimariyi JSON olarak indir</button><button type="button" class="btn" data-pz="copy" data-pzk="copy">Şartnameyi kopyala</button></div></details>`}
function boxHtml(){let P=panels(),A=act(),open=UI.open&&get(UI.open);
 return `<div class="pzHead"><p>${P.length?`${P.length} panel · ${A.length} aktif · ${A.reduce((a,x)=>a+errN(x),0)} uyarı. ${pzActive()?"Envanter Claude promptuna (PANEL VE PORTAL MİMARİSİ), Proje Kuralları’na ve proje dosyasına (<code>panelArchitecture</code>) yazılıyor.":""}`:"Henüz panel eklenmedi. Şablonlardan ekleyin, öneriyi uygulayın ya da özel panel oluşturun; ilk panel eklenince envanter Claude promptuna ve proje dosyasına yazılır."}</p></div>
 ${open?detail(open):recHtml()+toolbar()+`<div class="pzList">${listHtml()}</div>`}${open?"":sumHtml()}`}
let BOX=null;
function draw(){if(!BOX||!BOX.isConnected)return;let a=document.activeElement,key=a&&BOX.contains(a)?a.dataset.pzk:null,ss=a&&key&&"selectionStart" in a?[a.selectionStart,a.selectionEnd]:null;BOX.innerHTML=boxHtml();
 if(key){let n=BOX.querySelector(`[data-pzk="${CSS.escape(key)}"]`);if(n){n.focus({preventScroll:true});if(ss&&"setSelectionRange" in n)try{n.setSelectionRange(ss[0],ss[1])}catch(e){}}}}
function deco(){let slot=fieldBox.querySelector(`.field[data-field-id="${FID}"] .pzSlot`);if(!slot){BOX=null;return}
 let b=slot.querySelector(":scope > .pzBox");if(!b){b=document.createElement("section");b.className="pzBox";b.setAttribute("aria-label","Panel ve portal envanteri");slot.appendChild(b)}BOX=b;draw()}
window.pzDecorate=deco;
const _rf=renderFields;renderFields=function(){let r=_rf.apply(this,arguments);try{deco()}catch(e){console.error("pz renderFields",e)}return r};
if(typeof refreshField==="function"){const _ref=refreshField;refreshField=function(id){let r=_ref.apply(this,arguments);if(id===FID)try{deco()}catch(e){console.error("pz refreshField",e)}return r}}

/* ---------- olaylar ---------- */
function setPath(x,path,v){let ks=path.split("."),o=x;for(let i=0;i<ks.length-1;i++)o=o[ks[i]];o[ks[ks.length-1]]=v}
function getPath(x,path){return path.split(".").reduce((o,k)=>o==null?o:o[k],x)}
function live(x){if(!BOX)return;BOX.querySelectorAll('[data-pzlive="url"]').forEach(n=>n.textContent=full(x));BOX.querySelectorAll('[data-pzlive="issues"]').forEach(n=>n.innerHTML=iss(x));BOX.querySelectorAll('[data-pzlive="name"]').forEach(n=>n.textContent=x.name)}
const cur=()=>UI.open&&get(UI.open);
function visibleIds(){return BOX?[...BOX.querySelectorAll('.pzCard[data-id]')].map(n=>n.dataset.id):[]}
function del(ids){let p=pa(),L=p.panels.filter(x=>ids.includes(x.id));if(!L.length)return;if(!confirm(`${L.length===1?`“${L[0].name}” paneli`:`${L.length} panel`} envanterden kaldırılacak (rolleri, modül seçimleri ve adres tanımı silinir). Devam edilsin mi?`))return;
 p.panels=p.panels.filter(x=>!ids.includes(x.id));ids.forEach(i=>UI.sel.delete(i));if(ids.includes(UI.open))UI.open=null;if(!p.panels.length&&!p.modules.length&&p.apps.length<=1)delete state.panelArch;commit()}
document.addEventListener("click",e=>{let t=e.target.closest&&e.target.closest("[data-pz]");if(!t||!BOX||!BOX.contains(t))return;let k=t.dataset.pz;if(k==="sel"||k==="sumtg")return;e.preventDefault();e.stopPropagation();
 if(k==="cat"){UI.cat=t.dataset.c;draw()}else if(k==="st"){UI.st=t.dataset.s;draw()}else if(k==="clearf"){UI.q="";UI.cat="";UI.st="";draw()}
 else if(k==="go"){let f=FI[t.dataset.fid];if(f)goToField(f.section,f.id)}
 else if(k==="open"){UI.open=t.dataset.id;UI.tab="general";draw();let h=BOX.querySelector(".pzDetail");if(h)h.scrollIntoView({block:"start"});let b=BOX.querySelector('[data-pzk="back"]');if(b)b.focus({preventScroll:true})}
 else if(k==="back"){let id=UI.open;UI.open=null;draw();let n=BOX.querySelector(`[data-pzk="open:${CSS.escape(id||"")}"]`);if(n){n.focus({preventScroll:true});n.scrollIntoView({block:"center"})}}
 else if(k==="tab"){UI.tab=t.dataset.t;draw()}
 else if(k==="selall"){visibleIds().forEach(i=>UI.sel.add(i));draw()}else if(k==="selnone"){UI.sel.clear();draw()}
 else if(k==="recapply")recApply();
 else if(k==="dl")mkSave(JSON.stringify(pzConfig(),null,2),(exSlug(fv("mk_brand_name")||fv("project_name")||"proje")||"proje")+"-panel-mimarisi.json","application/json");
 else if(k==="copy"){let s=pzPrompt().trim()||"Henüz panel eklenmedi.";navigator.clipboard.writeText(s).then(()=>{t.textContent="Kopyalandı ✓";setTimeout(()=>t.textContent="Şartnameyi kopyala",2000)},()=>{t.textContent="Kopyalanamadı"})}
 else{if(!requireProject())return;let p=pa(),x=t.dataset.id?p.panels.find(y=>y.id===t.dataset.id):cur();
  if(k==="add"){let n=mk(t.dataset.tpl);p.panels.push(n);commit();let b=BOX&&BOX.querySelector(`[data-pzk="open:${n.id}"]`);if(b)b.focus()}
  else if(k==="new"){let n=mk("custom",{name:"Özel panel "+(p.panels.filter(y=>y.tpl==="custom").length+1)});p.panels.push(n);UI.open=n.id;UI.tab="general";commit();let f=BOX&&BOX.querySelector('[data-pzk="f:name"]');if(f){f.focus();f.select()}}
  else if(k==="toggle"&&x){x.on=!x.on;commit()}
  else if(k==="dup"&&x){let n=JSON.parse(JSON.stringify(x));n.id=uid();n.name=x.name+" (kopya)";n.url.slug=(x.url.slug||"panel")+"-2";n.url.domain="";p.panels.push(n);UI.open=n.id;commit()}
  else if(k==="del"&&x)del([x.id]);
  else if(k==="bulk"){let ids=[...UI.sel].filter(i=>p.panels.some(y=>y.id===i));if(t.dataset.a==="del")del(ids);else{p.panels.forEach(y=>{if(ids.includes(y.id))y.on=t.dataset.a==="on"});commit()}}
  else if(k==="addrole"&&x){x.roles.push({id:uid("r"),name:"Yeni rol",scope:"org",perms:{}});commit();let f=BOX.querySelector(`[data-pzk="r:${x.roles.length-1}:n"]`);if(f){f.focus();f.select()}}
  else if(k==="delrole"&&x){let i=+t.dataset.i,r=x.roles[i];if(r&&confirm(`“${r.name}” rolü silinsin mi?`)){x.roles.splice(i,1);commit()}}
  else if(k==="resetroles"&&x){if(confirm("Bu paneldeki roller ve izinler şablondaki varsayılanlara döndürülsün mü?")){let tp=TP[x.tpl];x.roles=tp.roles.map(r=>({id:r.id,name:r.name,scope:r.scope,perms:perms(tp,r)}));commit()}}
  else if(k==="addapp"&&x){let i=BOX.querySelector("#pzNewApp"),n=i&&i.value.trim();if(!n){i&&i.focus();return}let id=exSlug(n)||uid("a");while(p.apps.some(a=>a.id===id))id+="-2";p.apps.push({id,name:n});x.url.app=id;commit()}
  else if(k==="delapp"){let id=t.dataset.a;if(id==="web")return;p.apps=p.apps.filter(a=>a.id!==id);p.panels.forEach(y=>{if(y.url.app===id)y.url.app="web"});commit()}
  else if(k==="addmod"&&x){let i=BOX.querySelector("#pzNewMod"),d=BOX.querySelector("#pzNewModD"),n=i&&i.value.trim();if(!n){i&&i.focus();return}let id="cm-"+(exSlug(n)||uid("m"));while(p.modules.some(m=>m.id===id)||MD[id])id+="-2";p.modules.push({id,name:n,desc:d?d.value.trim():""});x.modules.push(id);commit();let f=BOX.querySelector("#pzNewMod");if(f)f.focus()}
  else if(k==="delmod"){let id=t.dataset.m,m=p.modules.find(z=>z.id===id);if(m&&confirm(`“${m.name}” özel modülü bütün panellerden kaldırılsın mı?`)){p.modules=p.modules.filter(z=>z.id!==id);p.panels.forEach(y=>{y.modules=y.modules.filter(z=>z!==id);y.roles.forEach(r=>delete r.perms[id])});commit()}}}},true);
document.addEventListener("toggle",e=>{if(e.target.classList&&e.target.classList.contains("pzSum"))UI.sum=e.target.open},true);
document.addEventListener("input",e=>{let t=e.target;if(!BOX||!BOX.contains(t))return;
 if(t.matches("[data-pzq]")){UI.q=t.value;let L=BOX.querySelector(".pzList");if(L)L.innerHTML=listHtml();return}
 if(!projectReady())return;let x=cur();
 if(t.matches("input[data-pzf],textarea[data-pzf]")&&x){setPath(x,t.dataset.pzf,t.value);live(x)}
 else if(t.matches("input[data-pzr]")&&x){let [i,f]=t.dataset.pzr.split("|");if(x.roles[i])x.roles[i][f]=t.value}
 else if(t.matches("input[data-pzapp]")){let a=pa().apps.find(z=>z.id===t.dataset.pzapp);if(a&&t.value.trim())a.name=t.value}},true);
document.addEventListener("change",e=>{let t=e.target;if(!BOX||!BOX.contains(t)||t.matches("[data-pzq],#pzNewApp,#pzNewMod,#pzNewModD"))return;
 if(t.matches('[data-pz="sel"]')){if(t.checked)UI.sel.add(t.dataset.id);else UI.sel.delete(t.dataset.id);draw();return}
 if(!requireProject()){draw();return}let x=cur();
 if(t.matches("input[type=text][data-pzf],textarea[data-pzf],input[data-pzr],input[data-pzapp]")){if(x&&t.dataset.pzf==="name"&&!x.name.trim()){x.name=TP[x.tpl].name;t.value=x.name;live(x)}commit(false);return}
 if(!x&&!t.matches("[data-pzapp]"))return;
 if(t.matches("select[data-pzf]")){let v=t.value,f=t.dataset.pzf;if(f==="on")v=v==="true";setPath(x,f,v);if(f==="url.mode"&&v!=="separate_domain"&&!x.url.slug)x.url.slug=TP[x.tpl].slug;commit()}
 else if(t.matches("select[data-pzr]")){let [i,f]=t.dataset.pzr.split("|");if(x.roles[i]){x.roles[i][f]=t.value;commit()}}
 else if(t.matches("select[data-pzp]")){let [i,m]=t.dataset.pzp.split("|"),r=x.roles[i];if(r){if(t.value)r.perms[m]=t.value;else delete r.perms[m];commit()}}
 else if(t.matches("input[data-pzmod]")){let m=t.dataset.pzmod;x.modules=t.checked?(x.modules.includes(m)?x.modules:x.modules.concat(m)):x.modules.filter(z=>z!==m);commit()}
 else if(t.matches("input[data-pzarr]")){let a=getPath(x,t.dataset.pzarr)||[],v=t.value;setPath(x,t.dataset.pzarr,t.checked?(a.includes(v)?a:a.concat(v)):a.filter(z=>z!==v));commit()}
 else if(t.matches("input[data-pzbool]")){setPath(x,t.dataset.pzbool,t.checked);commit()}},true);
document.addEventListener("keydown",e=>{let t=e.target;if(!BOX||!BOX.contains(t))return;
 if(t.getAttribute&&t.getAttribute("role")==="tab"){let L=[...BOX.querySelectorAll('[role="tab"]')],i=L.indexOf(t),j=e.key==="ArrowRight"?i+1:e.key==="ArrowLeft"?i-1:e.key==="Home"?0:e.key==="End"?L.length-1:null;if(j===null)return;e.preventDefault();j=(j+L.length)%L.length;UI.tab=L[j].dataset.t;draw();let n=BOX.querySelector(`[data-pzk="tab:${UI.tab}"]`);if(n)n.focus();return}
 if(e.key==="Escape"&&UI.open&&!t.matches("input,textarea,select")){e.preventDefault();BOX.querySelector('[data-pz="back"]').click()}
 if(e.key==="Enter"&&(t.id==="pzNewApp"||t.id==="pzNewMod"||t.id==="pzNewModD")){e.preventDefault();BOX.querySelector(`[data-pz="${t.id==="pzNewApp"?"addapp":"addmod"}"]`).click()}},true);
try{deco();renderRules()}catch(e){console.error("pz init",e)}
})();
