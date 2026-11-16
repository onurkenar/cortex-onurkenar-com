/* Adım Adım Kılavuz (2026-11-15, kullanıcı isteği: "hiç teknik bilgisi olmayan biri için ana modüllerin uygulamaya alma
   sıralaması 'Yapılacaklar' menüsü altında adım adım verilsin; her madde yapıldı olarak işaretlenip sıradakine geçilsin").
   Yapılacaklar sayfasının ilk sekmesi (todo betiği TD.tab === "guide" iken window.GUIDE.html() çizer).
   Sıra (bağımlılığa göre): Hazırlık → 1. Ortak Bilgiler → 2. Kararlar → 3. Pazarlama → 5. Google · 6. Meta · 7. Yapay Zekâ
   → 8. İçerik Planlama → (mevcut site varsa 4. SEO Denetimi ön denetimi) → Claude Code ile kurulum (CLAUDE-TALIMATLARI.md
   fazları, prMd()'den okunur) → 4. SEO Denetimi (yayındaki site) → pazarlama ve içerik üretimi → bakım.
   Yalnız yaprak adımlar işaretlenir; sıradaki (ilk açık) yapraktan sonrakiler kilitlidir. İsteğe bağlı adım atlanabilir;
   bu projede gerekmeyen adım (ör. eklenti / MCP yoksa) listelenmez.
   Kayıt: state.guide = {done:{id:"YYYY-AA-GG"}, skip:{id:1}, ex:"yes"|"no"} — yalnız işaret varken. Kurallar, Claude promptu,
   talimat dosyası, YAPILACAKLAR.md ve paketler değişmez. Kaynak docs/v26/v26-guide.{js,css} → docs/v26/yapilacaklar_ekle.py */
(()=>{
const PG=document.getElementById("todoPage");if(!PG)return;
const GD={open:new Set(),closed:new Set(),pv:new Set()};
const pad=n=>String(n).padStart(2,"0"),
 today=()=>{let x=new Date();return window.TODO_TODAY||x.getFullYear()+"-"+pad(x.getMonth()+1)+"-"+pad(x.getDate())},
 pname=()=>String(state.project_name||"").trim()||"Proje",
 slugT=t=>String(t||"").toLocaleLowerCase("tr").replace(/ç/g,"c").replace(/ğ/g,"g").replace(/ı/g,"i").replace(/ö/g,"o").replace(/ş/g,"s").replace(/ü/g,"u").replace(/â/g,"a").replace(/[^a-z0-9]+/g,"-").replace(/^-|-$/g,""),
 folder=()=>(typeof exSlug==="function"&&exSlug(pname()))||slugT(pname())||"proje",
 tr=n=>Number(n).toLocaleString("tr");
function G0(){let g=state.guide;return g&&typeof g==="object"?g:{}}
function gw(){if(!state.guide||typeof state.guide!=="object")state.guide={};let g=state.guide;if(!g.done||typeof g.done!=="object")g.done={};if(!g.skip||typeof g.skip!=="object")g.skip={};return g}
function gtidy(){let g=state.guide;if(!g)return;["done","skip"].forEach(k=>{if(g[k]&&!Object.keys(g[k]).length)delete g[k]});if(!Object.keys(g).length)delete state.guide}
const isDone=id=>!!(G0().done||{})[id],isSkip=id=>!!(G0().skip||{})[id];

/* ---------- karar sayaçları ---------- */
function cnt(test){let L=F.filter(f=>{let s=SI[f.section];return s&&test(s)&&navF(f)&&shown(f)}),D=L.filter(isset);return {a:L.length,d:D.length,first:L.find(f=>!isset(f))||null,firstAny:L[0]||null}}
const inArea=a=>s=>AREA(s)===a;
function secsOf(a){return S.filter(s=>AREA(s)===a)}
/* CLAUDE-TALIMATLARI.md'deki faz grupları (v26-prompt-md PR_PH ile aynı sıra) */
const PHG=[["Proje temeli ve mimari",["Başlangıç","Teknik Mimari","Sunucu & Altyapı"]],["Tasarım ve arayüz",["Tasarım & Arayüz"]],["İçerik ve yönetim",["İçerik & Yönetim"]],["İş modülleri",["İş Modülleri"]],["SEO ve görünürlük",["SEO & Görünürlük"]],["Güvenlik ve gizlilik",["Güvenlik & Gizlilik"]],["Performans, test ve geliştirme süreci",["Performans & Test","Geliştirme Süreci"]],["Yayın ve operasyon",["Yayın & Operasyon"]]];
/* talimat dosyasının fazları — dosyanın kendisinden okunur (kısa süreli önbellek) */
let PC=null;
function phases(){let now=Date.now();if(PC&&now-PC.t<2000)return PC.v;let v=[];try{if(typeof window.prMd==="function")String(window.prMd()).split("\n").forEach(l=>{let m=/^## Faz (\d+) — (.+)$/.exec(l);if(m)v.push({n:+m[1],t:m[2].trim()})})}catch(e){v=[]}PC={t:now,v};return v}

/* ---------- kopyalanacak metinler ---------- */
const BASE_ADD="\n\nEK TALİMAT (yenileme öncesi ön denetim)\nBu site yeniden yapılacak. Denetimi yalnız mevcut durumu kayıt altına almak için yap; siteyi değiştirme. Raporu proje klasörüne MEVCUT-SITE-DENETIMI.md adıyla kaydet. Rapora ayrıca mevcut sitedeki bütün sayfa adreslerinin listesini (yeni sitede 301 yönlendirme haritası için), en çok trafik ve sıralama alan sayfaları ve korunması gereken içerikleri ekle.",
 FIX="SEO denetim raporundaki bulguları önceliğe göre düzelt: önce P0, sonra P1. CLAUDE-TALIMATLARI.md'deki kararlarla çelişen bir düzeltme gerekirse uygulamadan önce bana sor. Her düzeltmeden sonra ilgili kontrolü yeniden çalıştır; sonunda düzeltilenleri, kalanları ve gerekçelerini rapor et ve CLAUDE-ILERLEME.md'yi güncelle.",
 UPD="CLAUDE-TALIMATLARI.md güncellendi. Önce CLAUDE-ILERLEME.md'yi ve talimat dosyasını oku; değişen kuralları mevcut kodla karşılaştır ve yapılacakları kısa bir plan olarak sun. Onayımdan sonra uygula; çalışan özellikleri bozma, sonunda rapor ver.",
 RESUME="Kaldığın yerden devam et.";
const GEN={
 start:{t:"Başlatma promptu",f:()=>window.prStart()},
 base:{t:"Ön denetim promptu",f:()=>auPrompt()+BASE_ADD},
 audit:{t:"SEO denetim promptu",f:()=>auPrompt()},
 fix:{t:"Düzeltme promptu",f:()=>FIX},
 mk:{t:"Pazarlama promptu",f:()=>mkMarketingPrompt()},
 upd:{t:"Güncelleme promptu",f:()=>UPD},
 resume:{t:"Devam promptu",f:()=>RESUME}};
const genText=k=>{try{return String(GEN[k].f()||"")}catch(e){return ""}};
const genOk=k=>!!genText(k);

/* ---------- ortak parçalar ---------- */
const btn=(attr,t,cls)=>`<button type="button" class="btn${cls?" "+cls:""}" ${attr}>${t}</button>`,
 link=(attr,t)=>`<button type="button" class="linkBtn" ${attr}>${t}</button>`,
 ext=(u,t)=>`<a href="${E(u)}" target="_blank" rel="noopener">${t} ↗</a>`,
 kbd=t=>`<kbd>${t}</kbd>`,
 copyB=(k,t)=>btn(`data-gd-copy="${k}"`,t||"Kopyala","dark"),
 pv=k=>`<details class="gdPv" data-gd-pv="${k}"${GD.pv.has(k)?" open":""}><summary>Metni göster</summary>${GD.pv.has(k)?`<textarea readonly rows="8" aria-label="${E(GEN[k].t)}">${E(genText(k))}</textarea>`:""}</details>`,
 meter=c=>`<span class="gdCnt${c.a&&c.d===c.a?" ok":""}">${tr(c.d)} / ${tr(c.a)} karar</span>`,
 goMiss=(c,a)=>c.first?link(`data-gd-field="${E(c.first.section)}|${E(c.first.id)}"`,"Sıradaki eksik karara git →"):(c.firstAny?link(`data-gd-sec="${E(c.firstAny.section)}"`,"Bölümü aç →"):"");
function decLeaf(id,t,c,d){return {id,t,h:`${d?`<p>${d}</p>`:""}<p class="gdMeta">${meter(c)} ${goMiss(c)}</p>`,cnt:c}}

/* ---------- adım ağacı ---------- */
function tree(){let g=G0(),ex=g.ex,T=[],PH=phases(),fz=PH.slice(1,-1),f0=PH[0],fl=PH.length>1?PH[PH.length-1]:null,
 hasDir=typeof skOn==="function"&&typeof skDirP==="function"&&skOn().some(x=>skDirP(x)||x.ref),hasMcp=typeof mcOn==="function"&&mcOn().length>0;
 /* 1 — Hazırlık */
 T.push({id:"s-prep",sh:"Hazırlık",t:"Hazırlık: araçları kurun",tag:"Bir kez",why:"Siteyi bilgisayarınızda Claude yazacak. Bunun için bir kod düzenleyicisi (Visual Studio Code) ve içine Claude Code eklentisi gerekir. Bu adımlar bir kez yapılır; sonraki projelerde atlanır.",kids:[
  {id:"prep-vscode",t:"Visual Studio Code'u indirip kurun",h:`<p>${ext("https://code.visualstudio.com/download","code.visualstudio.com/download")} adresinden bilgisayarınıza uygun sürümü indirin. Mac'te indirilen uygulamayı <b>Uygulamalar</b> klasörüne sürükleyin; Windows'ta kurulum dosyasını çalıştırıp varsayılan seçeneklerle ilerleyin.</p>`},
  {id:"prep-ext",t:"Claude Code eklentisini kurun",kids:[
   {id:"prep-ext-open",t:"VS Code'u açıp Uzantılar bölümüne girin",h:`<p>Sol kenardaki dört kareli <b>Uzantılar</b> simgesine tıklayın ya da ${kbd("⇧⌘X")} (Windows: ${kbd("Ctrl+Shift+X")}) tuşlarına basın.</p>`},
   {id:"prep-ext-install",t:"“Claude Code” eklentisini yükleyin",h:`<p>Arama kutusuna <b>Claude Code</b> yazın, yayıncısı <b>Anthropic</b> olan eklentide <b>Install</b> (Yükle) düğmesine basın. Doğrudan bağlantı: ${ext("https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code","Claude Code eklentisi")}</p>`},
   {id:"prep-ext-login",t:"Claude hesabınızla giriş yapın",h:`<p>Sağ üstteki Claude simgesine tıklayın (ya da ${kbd("⌘⎋")} / ${kbd("Ctrl+Esc")}) ve açılan pencerede Claude hesabınızla oturum açın. Claude Code için Claude Pro, Max ya da kurumsal (Team / Enterprise) hesap gerekir.</p>`}]},
  {id:"prep-folder",t:"Bilgisayarınızda proje klasörünü oluşturun",h:`<p>Örneğin <b>Belgeler</b> içinde <code>${E(folder())}</code> adlı boş bir klasör açın. Klasör adında boşluk ve Türkçe karakter kullanmayın. Projenin bütün dosyaları bu klasörde duracak.</p>`},
  {id:"prep-file",t:"Bu uygulamada proje dosyasını oluşturun",h:`<p>Proje dosyası verdiğiniz bütün kararları ve bu kılavuzdaki işaretleri kaydeder; tarayıcı kapansa da kaybolmaz. Proje adını yazıp dosyayı proje klasörünüze kaydedin.</p><p class="gdMeta">${typeof projectReady==="function"&&projectReady()?`<span class="gdCnt ok">Proje dosyası hazır</span>`:link(`data-gd-act="pfile"`,"Proje dosyasını oluştur →")}</p>`},
  {id:"prep-existing",t:"Yayında mevcut bir siteniz var mı?",ask:true,h:`<p>Var olan bir siteyi yeniliyorsanız, kuruluma başlamadan önce mevcut sitenin bir ön denetimi yapılır: eski sayfa adresleri ve sıralamalar kaybolmasın, yeni sitede doğru yönlendirmeler kurulsun.</p><div class="gdAsk" role="group" aria-label="Mevcut site">${btn(`data-gd-ex="yes" aria-pressed="${ex==="yes"}"`,"Evet, mevcut siteyi yeniliyorum",ex==="yes"?"dark":"")}${btn(`data-gd-ex="no" aria-pressed="${ex==="no"}"`,"Hayır, yeni bir site",ex==="no"?"dark":"")}</div>`}]});
 /* 2 — Ortak Bilgiler */
 T.push({id:"s-common",sh:"Ortak Bilgiler",t:"Ortak Bilgiler'i doldurun",mod:"common",why:"Marka adı, iletişim bilgileri, renkler, hesaplar ve rakipler bütün promptlarda ve kurulum talimatlarında kullanılır. Önce bunlar girilir; böylece hiçbir adımda bilgi eksik kalmaz ve Claude değer uydurmaz.",
  kids:secsOf("common").map(s=>{let c=cnt(x=>x.id===s.id);return c.a?decLeaf("common-"+s.id,s.name,c):null}).filter(Boolean)});
 /* 3 — Kararlar */
 T.push({id:"s-project",sh:"Kararlar",t:"Kararlar'ı verin",mod:"project",why:"Sitenin teknik ve tasarım kararları. “Proje” bölümündeki tür ve modül seçimleri sonraki soruların hangilerinin sorulacağını belirlediği için önce o doldurulur. Gruplar, Claude'un siteyi kuracağı fazlarla aynı sıradadır.",
  kids:PHG.map(([t,gs],i)=>{let c=cnt(s=>AREA(s)==="project"&&gs.includes(s.group));return c.a?decLeaf("proj-"+(i+1),t,c,i===0?"Proje tanımı, tür, modüller, teknoloji yığını, mimari, alan adı ve sunucu.":""):null}).filter(Boolean)});
 /* 4 — Pazarlama */
 let mg=[];secsOf("marketing").forEach(s=>{if(!mg.includes(s.group))mg.push(s.group)});
 T.push({id:"s-mk",sh:"Pazarlama",t:"Pazarlama kararlarını verin",mod:"marketing",why:"Hedef kitle, mesaj, kanallar, dönüşüm olayları ve reklam kampanya türleri burada belirlenir. Google ve Meta kurulum talimatları bu seçimleri kullandığı için Pazarlama, servislerden önce gelir.",
  kids:mg.map(gn=>{let c=cnt(s=>AREA(s)==="marketing"&&s.group===gn);return c.a?decLeaf("mk-"+slugT(gn),gn,c):null}).filter(Boolean)});
 /* 5 — Google, Meta, Yapay Zekâ */
 T.push({id:"s-svc",sh:"Google · Meta · Yapay Zekâ",t:"Google, Meta ve Yapay Zekâ kararlarını verin",mod:["google","meta","ai"],why:"Ölçüm ve reklam altyapısı. Google önce gelir: Tag Manager ve Onay Modu, Meta Pikseli dahil diğer etiketlerin de taşıyıcısıdır. Meta, Google'dan sonra; Yapay Zekâ görünürlüğü ise Search Console, Merchant Center ve İşletme Profili gibi kayıtlara dayandığı için en son.",kids:[
  decLeaf("svc-google","Google Servisleri kararları",cnt(inArea("google")),"Tag Manager, Analytics 4, Onay Modu, Search Console, Ads, Merchant Center, İşletme Profili. Kullanmayacağınız servisi kapsam bölümünde kapatın."),
  decLeaf("svc-meta","Meta Servisleri kararları",cnt(inArea("meta")),"İşletme portföyü, Facebook Sayfası, Instagram, WhatsApp, Meta Pikseli ve reklam hesabı."),
  decLeaf("svc-ai","Yapay Zekâ kararları",cnt(inArea("ai")),"ChatGPT ve diğer yapay zekâ asistanlarında görünürlük, tarayıcı izinleri, sitedeki asistan.")]});
 /* 6 — İçerik Planlama */
 T.push({id:"s-plan",sh:"İçerik Planlama",t:"İçerik Planlama ayarlarını yapın",mod:"plan",why:"Plan dönemi, ürünler, blog, sosyal medya, özel günler ve reklam takvimi. Pazarlama kararlarına dayanır; site kurulurken plan ayarları da talimat dosyasına girer.",kids:[
  decLeaf("plan-decide","İçerik Planlama kararları",cnt(s=>AREA(s)==="plan"&&s.id!=="mk_planfile"))]});
 /* 7 — Mevcut site ön denetimi (yalnız yenilemede) */
 if(ex==="yes")T.push({id:"s-base",sh:"Mevcut site ön denetimi",t:"Mevcut sitenin ön denetimini yapın",mod:"audit",why:"Yenileme öncesi mevcut durumun kaydı: eski adresler, en çok ziyaret alan sayfalar ve sıralamalar. Claude yeni siteyi kurarken bu rapora bakarak doğru yönlendirmeleri kurar, değerli içerikleri korur.",kids:[
  decLeaf("base-decide","SEO Denetimi kararlarını verin",cnt(inArea("audit")),"“Denetlenecek site” olarak mevcut sitenizi seçin."),
  {id:"base-run",t:"Ön denetim promptunu Claude'a verin",h:`<p>VS Code'da <b>Dosya › Klasör Aç</b> (File › Open Folder) ile proje klasörünüzü açın, Claude panelini açın ve promptu yapıştırıp ${kbd("Enter")}'a basın. Claude raporu proje klasörüne <code>MEVCUT-SITE-DENETIMI.md</code> adıyla kaydeder.</p><p class="gdActs">${copyB("base","Ön denetim promptunu kopyala")}</p>${pv("base")}`},
  {id:"base-check",t:"Raporun proje klasörüne kaydedildiğini kontrol edin",h:`<p>Proje klasöründe <code>MEVCUT-SITE-DENETIMI.md</code> dosyasını görün. Bu dosya kurulum sırasında klasörde kalmalı; Claude yeni siteyi kurarken ona bakacak.</p>`}]});
 /* 8 — Claude Code ile kurulum */
 let B=[
  {id:"build-zip",t:"Claude Code proje paketini indirin",h:`<p>Paket; Claude'un uygulayacağı talimat dosyasını (<code>CLAUDE-TALIMATLARI.md</code>), başlatma promptunu, proje kararlarını, ajan ve skill dosyalarını içerir. İndirmeden önce eksik karar kalmadığını Dışa Aktar sayfasından kontrol edebilirsiniz.</p><p class="gdActs">${btn(`data-gd-zip="claude"`,"Paketi zip olarak indir","dark")}${link(`data-gd-dlx="claude"`,"Dışa Aktar'da aç →")}</p>`},
  {id:"build-unzip",t:"Zip'i proje klasörüne çıkartın",kids:[
   {id:"build-unzip-open",t:"İndirilen zip'i açın",h:`<p><b>İndirilenler</b> klasöründe adı <code>…-claude-code-paketi.zip</code> ile biten dosyaya çift tıklayın (Windows: sağ tık › <b>Tümünü Ayıkla</b>). Zip'in adıyla bir klasör oluşur.</p>`},
   {id:"build-unzip-move",t:"İçindekilerin hepsini proje klasörüne taşıyın",h:`<p>Oluşan klasörün <b>içindeki</b> her şeyi seçip <code>${E(folder())}</code> klasörüne taşıyın. <code>CLAUDE-TALIMATLARI.md</code> proje klasörünün en üst düzeyinde olmalı. Adı nokta ile başlayan <code>.claude</code> klasörü gizlidir: Mac'te ${kbd("⌘⇧.")} ile, Windows'ta Gezgin › <b>Görünüm › Göster › Gizli öğeler</b> ile görünür; onu da taşıyın.</p>`}]},
  {id:"build-open",t:"Proje klasörünü VS Code'da açın",h:`<p>VS Code'da <b>Dosya › Klasör Aç</b> (File › Open Folder) ile <code>${E(folder())}</code> klasörünü seçin. “Bu klasördeki dosyaların yazarlarına güveniyor musunuz?” sorusuna <b>Evet</b> deyin. Soldaki dosya listesinde <code>CLAUDE-TALIMATLARI.md</code>'yi görmelisiniz.</p>`},
  {id:"build-claude",t:"Claude Code panelini açın",h:`<p>Sağ üstteki Claude simgesine tıklayın (ya da ${kbd("⌘⎋")} / ${kbd("Ctrl+Esc")}). Claude, açık klasörde çalışır; dosya düzenlemek ya da komut çalıştırmak istediğinde izin sorar. Açıklamayı okuyup onaylayın; emin değilseniz “bu ne işe yarar?” diye sorun.</p>`}];
 if(hasDir||hasMcp)B.push({id:"build-plugins",t:"Eklenti ve bağlantıları kurun",opt:true,h:`<p>Bu projede ${[hasDir?"ayrıca kurulan skill eklentileri":"",hasMcp?"MCP bağlantıları":""].filter(Boolean).join(" ve ")} var. Ajanlar › Kurulum Kılavuzu'ndaki 4. ve 5. adımlar bunları komutlarıyla gösterir. Emin değilseniz atlayabilirsiniz; site kurulumu bunlar olmadan da çalışır.</p><p class="gdActs">${link(`data-gd-act="setup"`,"Kurulum Kılavuzu'nu aç →")}</p>`});
 B.push({id:"build-start",t:"Başlatma promptunu Claude'a yapıştırın",h:`<p>Promptu kopyalayın, Claude panelindeki mesaj kutusuna yapıştırın ve ${kbd("Enter")}'a basın. Claude talimat dosyasını okur ve önce incelemesini ve planını sunar; kod yazmaya sizin onayınızla başlar.</p><p class="gdActs">${copyB("start","Başlatma promptunu kopyala")}</p>${pv("start")}`});
 let PHK=[];
 if(f0)PHK.push({id:"faz-0",t:`Faz 0 — ${f0.t}: planı onaylayın`,h:`<p>Claude projeyi inceler, yapılacakları ve riskleri listeler. Planı okuyun; sorduğu soruları yanıtlayın. Uygunsa <b>devam</b> yazın.</p>`});
 fz.forEach(p=>{let id="faz-"+slugT(p.t),base=`<p>Claude bu fazı uygular ve sonunda rapor verir: yapılanlar, uygulanamayanlar, testler ve sizin kararınızı bekleyen konular. Raporu okuyun, sorulara yanıt verin; her şey yolundaysa <b>devam</b> yazın.</p>`,
  svc=/^Google servisleri/.test(p.t)?"google":/^Meta servisleri/.test(p.t)?"meta":/^Yapay zekâ/.test(p.t)?"ai":"";
  if(svc){let nm={google:"Google",meta:"Meta",ai:"Yapay zekâ platformları"}[svc],ids={google:"Analytics ölçüm kimliği, Tag Manager kapsayıcı kimliği, Ads dönüşüm kimliği",meta:"Piksel kimliği, işletme portföyü ve reklam hesabı kimliği",ai:"işletme ve satıcı kayıtlarının adresleri"}[svc];
   PHK.push({id,t:`Faz ${p.n} — ${p.t}`,kids:[
    {id:id+"-run",t:"Claude'un sitede yaptığı kurulumu onaylayın",d:base},
    {id:id+"-panel",t:`${nm} panellerindeki ayarları yapın`,h:`<p>Claude, panellerde sizin yapmanız gereken ayarları menü yoluyla adım adım listeler (hesap açma, doğrulama, bağlantılar). Listeyi sırayla uygulayın; takıldığınız adımı Claude'a sorun. Şifre ve doğrulama kodlarını Claude'a vermeyin.</p>`},
    {id:id+"-ids",t:"Oluşan kimlikleri Ortak Bilgiler'e yazın",opt:true,h:`<p>Hesaplar açıldıkça oluşan kimlikleri (${ids}) Ortak Bilgiler › Dijital Hesaplar'a girin; sonraki promptlar ve güncellemeler bunları kullanır.</p><p class="gdActs">${link(`data-gd-sec="oc_accounts"`,"Dijital Hesaplar'ı aç →")}</p>`}]})}
  else PHK.push({id,t:`Faz ${p.n} — ${p.t}`,d:base})});
 if(fl)PHK.push({id:"faz-son",t:`Faz ${fl.n} — ${fl.t}`,h:`<p>Claude bütün fazları baştan kontrol eder, testleri çalıştırır ve son raporu verir. Uygulanamayan kural kaldıysa gerekçesini okuyun; teslimi onaylayın.</p>`});
 if(PHK.length)B.push({id:"build-phases",t:"Fazları sırayla tamamlayın",h:`<p>Her faz bitince Claude onayınızı bekler. Oturum kapanırsa ya da ertesi gün devam edecekseniz aynı klasörü açıp şunu yazın:</p><p class="gdActs">${copyB("resume","“Kaldığın yerden devam et” kopyala")}</p>`,kids:PHK});
 else B.push({id:"build-phases-none",t:"Claude'un fazlarını tamamlayın",h:`<p>Talimat dosyası henüz faz içermiyor; önce kararları verin. Claude her fazın sonunda rapor verir ve <b>devam</b> onayınızı bekler.</p>`});
 B.push({id:"build-live",t:"Yayındaki siteyi kendiniz kontrol edin",h:`<p>Site yayına alındıktan sonra telefonda ve bilgisayarda açın: ana sayfa, menü, iletişim formu, çerez onay penceresi ve iletişim bilgileri doğru mu? Gördüğünüz sorunu Claude'a kendi cümlelerinizle yazın.</p>`});
 T.push({id:"s-build",sh:"Claude Code ile kurulum",t:"Siteyi Claude Code ile kurun",tag:"Kararlar · Pazarlama altyapısı · Google · Meta · Yapay Zekâ",why:"Verdiğiniz bütün kararlar tek bir talimat dosyasında fazlara bölünür: önce proje temeli, tasarım, içerik, modüller, SEO, güvenlik, performans ve yayın; ardından pazarlama altyapısı, Google, Meta ve Yapay Zekâ kurulumu. Claude her fazı bitirince onayınızı bekler.",kids:B});
 /* 9 — SEO Denetimi (yayındaki site) */
 T.push({id:"s-audit",sh:"SEO Denetimi",t:"Yayındaki siteyi denetleyin",mod:"audit",why:"SEO Denetimi yayındaki siteyi inceler; bu yüzden numarası 4 olsa da uygulamada kurulumdan sonra gelir. Bulgular düzeltilir, ardından düzenli aralıklarla yeniden denetlenir.",kids:[
  ex==="yes"?{id:"audit-decide",t:"SEO Denetimi kararlarını yeni site için güncelleyin",h:`<p>Ön denetimde mevcut siteyi seçtiyseniz “Denetlenecek site”yi bu projenin canlı sitesi yapın.</p><p class="gdActs">${link(`data-gd-sec="au_scope"`,"Denetim Kapsamı'nı aç →")}</p>`}:decLeaf("audit-decide","SEO Denetimi kararlarını verin",cnt(inArea("audit"))),
  {id:"audit-run",t:"Denetim promptunu Claude'a verin",h:`<p>Claude panelinde yeni bir sohbet açın (sağ üstteki <b>+</b>), promptu yapıştırın. Claude siteyi denetler ve öncelikli bulgu raporu hazırlar.</p><p class="gdActs">${copyB("audit","Denetim promptunu kopyala")}</p>${pv("audit")}`},
  {id:"audit-fix",t:"Bulguları Claude'a düzelttirin",h:`<p>Raporu okuyun; ardından düzeltme promptunu aynı sohbete yapıştırın. Claude önce en kritik (P0, P1) bulguları düzeltir.</p><p class="gdActs">${copyB("fix","Düzeltme promptunu kopyala")}</p>${pv("fix")}`},
  {id:"audit-recheck",t:"Yeniden denetimi takvime bağlayın",h:`<p>Yeniden denetim sıklığı SEO Denetimi › Denetim Raporu'ndaki seçiminizden gelir ve <b>Karar Görevleri</b> sekmesinde yinelenen görev olarak durur. Takvim dosyasını indirip takviminize ekleyebilirsiniz.</p><p class="gdActs">${link(`data-gd-tab="tasks"`,"Karar Görevleri'ni aç →")}</p>`}]});
 /* 10 — Pazarlama ve içerik üretimi */
 T.push({id:"s-grow",sh:"Pazarlama ve içerik üretimi",t:"Pazarlama ve içerik üretimine başlayın",mod:["marketing","plan"],why:"Site ve ölçüm altyapısı hazır olduğunda içerik ve reklam çalışmaları başlar; böylece her kampanyanın sonucu ölçülebilir.",kids:[
  {id:"grow-project",t:"İçerik üretimi için Claude'da bir Proje açın",h:`<p>${ext("https://claude.ai/projects","claude.ai › Projeler")} sayfasında “Pazarlama — ${E(pname())}” adlı yeni bir Proje oluşturun. İçerik, sosyal medya, e-posta ve reklam metinlerini bu projede ürettireceksiniz.</p>`},
  {id:"grow-prompt",t:"Pazarlama promptunu Proje talimatlarına yapıştırın",h:`<p>Promptu kopyalayıp Projenin <b>talimatlar</b> alanına yapıştırın. Claude o projedeki her sohbette marka, kitle, kanal ve içerik kurallarınıza uyar.</p><p class="gdActs">${copyB("mk","Pazarlama promptunu kopyala")}</p>${pv("mk")}`},
  {id:"grow-plan",t:"İçerik ve reklam planı dosyasını oluşturun",h:`<p>İçerik Planlama › Dışa Aktarım bölümünden plan dosyasını oluşturun; yıllık içerik ve reklam takviminiz bu dosyada tutulur.</p><p class="gdActs">${link(`data-gd-sec="mk_planfile"`,"Dışa Aktarım'ı aç →")}${link(`data-gd-dlx="marketing"`,"Pazarlama paketini aç →")}</p>`}]});
 /* 11 — Bakım */
 T.push({id:"s-maint",sh:"Bakım",t:"Bakım: düzenli işler ve güncellemeler",why:"Yedek kontrolü, rapor, denetim ve hesap gözden geçirmesi gibi işler düzenli tekrarlanır. Bir kararı değiştirdiğinizde siteyi de güncellemek gerekir.",kids:[
  {id:"maint-tasks",t:"Yinelenen görevleri takvime ekleyin",h:`<p><b>Karar Görevleri</b> sekmesinde ↻ işaretli görevler yinelenir; her yapılışta işaretleyin. Takvim dosyasını (.ics) Google Takvim, Outlook ya da Apple Takvim'e aktarırsanız zamanı gelince hatırlatılır.</p><p class="gdActs">${typeof window.todoRecurring==="function"&&window.todoRecurring()?btn(`data-gd-act="ics"`,"Takvim dosyasını indir (.ics)"):""}${link(`data-gd-tab="tasks"`,"Karar Görevleri'ni aç →")}</p>`},
  {id:"maint-update",t:"Karar değiştirdiğinizde siteyi güncellemeyi öğrenin",h:`<p>Bir kararı değiştirdiğinizde: Claude Code paketini yeniden indirip proje klasörüne çıkartın (eski dosyaların üzerine yazın), ardından Claude'a güncelleme promptunu verin. Karar Görevleri sekmesinde değişen görevler “Karar değişti” olarak işaretlenir.</p><p class="gdActs">${copyB("upd","Güncelleme promptunu kopyala")}${btn(`data-gd-zip="claude"`,"Paketi yeniden indir")}</p>${pv("upd")}`}]});
 return T.filter(s=>s.kids&&s.kids.length)}

/* ---------- numaralandırma, durum ---------- */
function walk(T){let L=[],P=[];
 const go=(n,num,depth,par)=>{n.num=num;n.depth=depth;n.par=par;if(n.kids&&n.kids.length){P.push(n);n.kids.forEach((k,i)=>go(k,num+"."+(i+1),depth+1,n))}else{n.leaf=true;L.push(n)}};
 T.forEach((s,i)=>go(s,String(i+1),0,null));
 let cur=null;L.forEach(x=>{x.st=isDone(x.id)?"done":(x.opt&&isSkip(x.id)?"skip":"open");if(!cur&&x.st==="open")cur=x});
 let locked=false;L.forEach(x=>{if(x===cur){x.cur=true;locked=true}else if(locked&&x.st==="open")x.lock=true});
 const agg=n=>{if(n.leaf)return [n.st!=="open"?1:0,1];let d=0,a=0;n.kids.forEach(k=>{let [x,y]=agg(k);d+=x;a+=y});n.d=d;n.a=a;n.has=hasCur(n);return [d,a]};
 const hasCur=n=>n.leaf?!!n.cur:n.kids.some(hasCur);
 T.forEach(agg);
 return {L,cur}}

/* ---------- çizim ---------- */
const MODN={common:["1","Ortak Bilgiler"],project:["2","Kararlar"],marketing:["3","Pazarlama"],audit:["4","SEO Denetimi"],google:["5","Google"],meta:["6","Meta"],ai:["7","Yapay Zekâ"],plan:["8","İçerik Planlama"]};
function modTag(m){if(!m)return "";let L=Array.isArray(m)?m:[m];return L.map(k=>MODN[k]?`<span class="gdMod">Menü ${MODN[k][0]} · ${E(MODN[k][1])}</span>`:"").join("")}
function stLbl(x){if(x.st==="done")return `<span class="gdSt done">Yapıldı${G0().done&&typeof G0().done[x.id]==="string"?" · "+E(G0().done[x.id]):""}</span>`;if(x.st==="skip")return `<span class="gdSt skip">Atlandı</span>`;if(x.cur)return `<span class="gdSt cur">Sıradaki adım</span>`;return ""}
function leafHtml(x){let dis=x.lock?" disabled":"",
 box=x.ask?`<span class="gdBoxSp" aria-hidden="true">${x.st==="done"?"✓":""}</span>`:`<input type="checkbox" data-gd-k="${E(x.id)}"${x.st==="done"?" checked":""}${dis} aria-label="${E(x.num+" "+x.t)}${x.lock?" (önce önceki adımları tamamlayın)":""}">`,
 acts=x.opt?(x.st==="skip"?link(`data-gd-unskip="${E(x.id)}"`,"Atlamayı geri al"):(x.st==="open"&&!x.lock?link(`data-gd-skip="${E(x.id)}"`,"Bu adımı atla"):"")):"",
 body=x.h&&(x.cur||!x.lock||GD.open.has(x.id))?`<div class="gdBody">${x.h}${acts?`<p class="gdSkip">${acts}</p>`:""}</div>`:(x.h?`<p class="gdLockNote">Önce önceki adımları tamamlayın. ${link(`data-gd-peek="${E(x.id)}"`,"Ayrıntıyı göster")}</p>`:"");
 return `<li class="gdLeaf ${x.st}${x.cur?" cur":""}${x.lock?" lock":""}" id="gd-${E(x.id)}"><div class="gdRow"><label class="gdMain">${box}<span class="gdNum">${E(x.num)}</span><span class="gdT">${E(x.t)}</span></label>${stLbl(x)}</div>${body}</li>`}
function nodeHtml(n){if(n.leaf)return leafHtml(n);
 return `<li class="gdNode${n.d===n.a?" done":""}${n.has?" cur":""}"><div class="gdRow gdNodeRow"><span class="gdNum">${E(n.num)}</span><span class="gdT">${E(n.t)}</span><span class="gdPart">${n.d}/${n.a}</span></div>${n.h?`<div class="gdBody">${n.h}</div>`:""}<ol class="gdKids">${n.kids.map(nodeHtml).join("")}</ol></li>`}
function stageHtml(s){let done=s.d===s.a,open=GD.open.has(s.id)||(!GD.closed.has(s.id)&&s.has),pc=s.a?Math.round(s.d/s.a*100):0;
 return `<details class="gdStage${done?" done":""}${s.has?" cur":""}" data-gd-stage="${E(s.id)}"${open?" open":""}><summary><span class="gdSNum" aria-hidden="true">${done?"✓":E(s.num)}</span><span class="gdSHead"><b><span class="sr">Adım ${E(s.num)}: </span>${E(s.t)}</b><span class="gdTags">${modTag(s.mod)}${s.tag?`<span class="gdMod alt">${E(s.tag)}</span>`:""}</span></span><span class="gdSProg"><span>${s.d}/${s.a}</span><i style="--p:${pc}%"></i></span></summary>
 <div class="gdSBody"><p class="gdWhy"><b>Neden bu sırada?</b> ${E(s.why)}</p><ol class="gdKids">${s.kids.map(nodeHtml).join("")}</ol></div></details>`}
function html(){let T=tree(),{L,cur}=walk(T);
 let d=L.filter(x=>x.st!=="open").length,a=L.length,pc=a?Math.round(d/a*100):0,
  order=T.map(s=>`<li class="${s.d===s.a?"done":""}${s.has?" cur":""}"><button type="button" data-gd-jump="${E(s.id)}"><span>${E(s.num)}</span>${E(s.sh||s.t)}</button></li>`).join(""),
  nx=cur?`<div class="gdNext"><div><p class="gdEye2">SIRADAKİ ADIM</p><p class="gdNextT"><span class="gdNum">${E(cur.num)}</span> ${E(cur.t)}</p><p class="gdNextP">${E(pathOf(cur))}</p></div>${btn(`data-gd-goto="${E(cur.id)}"`,"Adıma git","dark")}</div>`:`<div class="gdNext fin"><div><p class="gdEye2">TAMAMLANDI</p><p class="gdNextT">Bütün adımlar tamamlandı.</p><p class="gdNextP">Düzenli işler için Karar Görevleri sekmesindeki yinelenen görevleri takip edin.</p></div>${btn(`data-gd-tab="tasks"`,"Karar Görevleri'ni aç","dark")}</div>`;
 return `<div class="gdSum" role="group" aria-label="Kılavuz ilerlemesi"><div class="tdBar" role="progressbar" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${pc}" aria-label="Kılavuz ilerlemesi"><i style="width:${pc}%"></i></div><p><b>${d}/${a} adım - %${pc}</b> · Her adımı yaptıktan sonra işaretleyin; sıradaki adım açılır. İşaretler proje dosyasına kaydedilir.</p>${nx}
 <details class="gdOrder"${GD.open.has("order")?" open":""} data-gd-ord><summary>Uygulama sırası ve nedeni</summary><ol class="gdOrderL">${order}</ol><p class="gdOrderN">Menü numaraları kararları doldurma sırasıdır. Uygulamada tek fark SEO Denetimi'dir: yayındaki siteyi incelediği için kurulumdan sonra gelir (mevcut siteyi yeniliyorsanız kurulumdan önce bir ön denetim de yapılır). Google, Meta ve Yapay Zekâ kurulumları talimat dosyasının son fazlarındadır; Pazarlama'daki dönüşüm ve kampanya seçimlerini kullanırlar.</p></details></div>
 <div class="gdList">${T.map(stageHtml).join("")}</div>
 ${Object.keys(G0()).length?`<p class="tdFoot"><button type="button" class="linkBtn" data-gd-act="reset">Kılavuzdaki bütün işaretleri kaldır</button></p>`:""}`}
function pathOf(x){let p=[],n=x.par;while(n){p.unshift(n.t);n=n.par}return p.join(" › ")}

/* ---------- işlemler ---------- */
function redraw(sel){if(typeof window.todoRedraw==="function")window.todoRedraw(sel)}
function findLeaf(id){let {L}=walk(tree());return L.find(x=>x.id===id)}
function note(b,t,ms){if(!b)return;let o=b.innerHTML;b.textContent=t;b.disabled=true;setTimeout(()=>{b.innerHTML=o;b.disabled=false},ms||1600)}
function copyText(t,b){const ok=()=>note(b,"Kopyalandı ✓"),bad=()=>{let ta=document.createElement("textarea");ta.value=t;ta.setAttribute("readonly","");ta.style.cssText="position:fixed;top:0;left:0;opacity:0";document.body.appendChild(ta);ta.select();let r=false;try{r=document.execCommand("copy")}catch(e){}ta.remove();r?ok():note(b,"Kopyalanamadı — “Metni göster”den seçin",3200)};
 if(navigator.clipboard&&window.isSecureContext)navigator.clipboard.writeText(t).then(ok,bad);else bad()}
function setLeaf(x,on){if(!requireProject())return false;let g=gw();if(on){g.done[x.id]=today();delete g.skip[x.id]}else delete g.done[x.id];gtidy();save();return true}
PG.addEventListener("change",e=>{let c=e.target;if(!c.matches("input[data-gd-k]"))return;let x=findLeaf(c.dataset.gdK);if(!x||(x.lock&&c.checked)){c.checked=!c.checked;return}
 if(!setLeaf(x,c.checked)){c.checked=!c.checked;return}
 if(c.checked){let n=walk(tree()).cur;redraw(n?`#gd-${CSS.escape(n.id)} input, #gd-${CSS.escape(n.id)} button`:null)}else redraw(`input[data-gd-k="${CSS.escape(x.id)}"]`)});
PG.addEventListener("toggle",e=>{let d=e.target;if(!(d instanceof HTMLDetailsElement)||!PG.contains(d))return;
 if(d.dataset.gdStage){let id=d.dataset.gdStage;if(d.open){GD.open.add(id);GD.closed.delete(id)}else{GD.open.delete(id);GD.closed.add(id)}}
 else if(d.hasAttribute("data-gd-ord")){d.open?GD.open.add("order"):GD.open.delete("order")}
 else if(d.dataset.gdPv){let k=d.dataset.gdPv;if(d.open){GD.pv.add(k);if(!d.querySelector("textarea")){let ta=document.createElement("textarea");ta.readOnly=true;ta.rows=8;ta.setAttribute("aria-label",GEN[k].t);ta.value=genText(k);d.appendChild(ta)}}else GD.pv.delete(k)}},true);
PG.addEventListener("click",e=>{let b=e.target.closest("button");if(!b||!PG.contains(b))return;let d=b.dataset;
 if(d.gdCopy){let t=genText(d.gdCopy);if(!t){note(b,"Bu projede henüz üretilmiyor",2200);return}copyText(t,b)}
 else if(d.gdEx){if(!requireProject())return;let g=gw();g.ex=d.gdEx;g.done["prep-existing"]=today();gtidy();save();redraw(`[data-gd-ex="${d.gdEx}"]`)}
 else if(d.gdSkip){if(!requireProject())return;let g=gw();g.skip[d.gdSkip]=1;delete g.done[d.gdSkip];gtidy();save();redraw()}
 else if(d.gdUnskip){if(!requireProject())return;let g=gw();delete g.skip[d.gdUnskip];gtidy();save();redraw()}
 else if(d.gdPeek){GD.open.add(d.gdPeek);redraw()}
 else if(d.gdGoto||d.gdJump){let id=d.gdGoto||d.gdJump,T=tree(),{L}=walk(T),x=L.find(l=>l.id===id),sid=id;
  if(x){let n=x;while(n.par)n=n.par;sid=n.id}GD.open.add(sid);GD.closed.delete(sid);if(!d.gdGoto)GD.closed.delete(sid);redraw();
  let el=document.getElementById(d.gdGoto?"gd-"+id:"")||PG.querySelector(`[data-gd-stage="${CSS.escape(sid)}"]`);if(el){el.scrollIntoView({block:"start",behavior:"smooth"});let f=el.querySelector("input:not([disabled]),button,summary");if(f)f.focus({preventScroll:true})}}
 else if(d.gdField){let [s,f]=d.gdField.split("|");goToField(s,f)}
 else if(d.gdSec){if(typeof goStep==="function")goStep(d.gdSec)}
 else if(d.gdZip){if(typeof window.dlZip==="function")window.dlZip(d.gdZip)}
 else if(d.gdDlx){if(window.DLX)window.DLX.go(d.gdDlx)}
 else if(d.gdTab){if(typeof window.todoTab==="function")window.todoTab(d.gdTab)}
 else if(d.gdAct==="pfile"){if(typeof pnFocus==="function")pnFocus()}
 else if(d.gdAct==="setup"){showPage("agents");if(typeof ksGo==="function")ksGo("setup")}
 else if(d.gdAct==="ics"){if(typeof window.todoIcs==="function")mkSave(window.todoIcs(),"YAPILACAKLAR-"+((typeof exSlug==="function"&&exSlug(pname()))||"proje")+".ics","text/calendar;charset=utf-8")}
 else if(d.gdAct==="reset"){if(!requireProject())return;if(confirm("Kılavuzdaki bütün işaretler kaldırılsın mı? Kararlar ve Karar Görevleri değişmez.")){delete state.guide;save();GD.open.clear();GD.closed.clear();redraw()}}});
window.GUIDE={html,stats:()=>{let {L,cur}=walk(tree());return {d:L.filter(x=>x.st!=="open").length,a:L.length,cur:cur?cur.num+" "+cur.t:""}},tree:()=>{let T=tree();walk(T);return T}};
})();
