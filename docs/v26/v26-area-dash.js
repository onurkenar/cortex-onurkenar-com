/* Ana menü dashboard'ları (2026-11-15, kullanıcı isteği: "her ana menünün kendi dashboardı olsun").
   Modül şeridinde ya da ≤ 900 px çekmecede bir ana menüye (1. Ortak Bilgiler … 8. İçerik Planlama) tıklanınca — yani goArea(a)
   çağrılınca — o menünün ilk / son açılan bölümü yerine menünün dashboard'u açılır. Sol menü (o alanın bölümleri) görünür kalır;
   menünün başında "Dashboard" satırı vardır. Dashboard #configPage'in içindedir (#areaDash; açıkken #configPage.adOn > .layout
   gizli), bu yüzden curArea / areaBtn / railSync / kenar çubuğu davranışı değişmez. İçerik: ilerleme halkası (verilen / toplam
   karar — üst şerit ve modül şeridiyle aynı hesap: shown + navF + AREA), sıradaki karar ve "Kaldığın yerden devam et", son açılan
   bölüm, eksik zorunlu kararlar, bölüm durumu (tamamlanan / devam eden / başlanmayan), gruplara ayrılmış bölüm kartları (menüdeki
   numara, açıklama, karar sayısı, ilerleme çubuğu; tıklayınca bölüm rehberi). Yalnız görünüm: veri, kural, prompt, kayıt değişmez.
   Herhangi bir sayfa geçişi (showPage — goStep, goToField, menuClick da onu çağırır) dashboard'u kapatır. Kaynak
   docs/v26/v26-area-dash.{js,css} → docs/v26/alan_dashboard_ekle.py */
(function(){
if(typeof goArea!=="function"||typeof configPage==="undefined")return;
const LB={common:"Ortak Bilgiler",project:"Kararlar",marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google",meta:"Meta",ai:"Yapay Zekâ",plan:"İçerik Planlama"};
const DESC={
 common:"Marka, kurum, iletişim, işletme ve pazar, marka görünümü, eylem çağrıları, dijital hesaplar, rakipler ve hedef sorgular. Proje, pazarlama ve SEO bölümleri bu bilgileri yeniden sormadan buradan okur.",
 project:"Sitenin yapılandırma kararları: başlangıç, tasarım ve arayüz, içerik ve yönetim, iş modülleri, SEO, teknik mimari, sunucu, güvenlik, performans, geliştirme süreci ve yayın.",
 marketing:"Pazarlama stratejisi, içerik ve mesaj standartları, satış dokümanları, kanallar, reklam, ölçüm, SEO araçları ile süreç ve ekip kararları.",
 audit:"SEO denetiminin kapsamı; tarama, sayfa içi SEO, yapısal veri, performans, uluslararası ve yerel SEO, AI arama görünürlüğü, otorite ve ölçüm kararları ile denetim promptu.",
 google:"Google hesapları ve erişim, Cloud projesi, Onay Modu, Tag Manager, Analytics 4, Search Console, Ads, Merchant Center, İşletme Profili ve Looker Studio kurulum kararları.",
 meta:"Meta İşletme Portföyü ve erişim, rıza, Piksel ve Conversions API, Facebook, Instagram, WhatsApp Business, reklam hesabı ve katalog kurulum kararları.",
 ai:"Yapay zekâ servislerinde işletme görünürlüğü: ChatGPT, reklamlar, ürün beslemeleri, diğer yapay zekâ platformları, tarayıcı izinleri, sitedeki asistan ve ölçüm.",
 plan:"İçerik planının dönemi ve kayıtları: ürün ve hizmetler, blog, sosyal paylaşımlar, takvim, özel günler, mailing, etkinlikler, reklamlar, rakipler ve dışa aktarım."};
const ad=document.createElement("div");ad.id="areaDash";ad.hidden=true;
configPage.insertBefore(ad,configPage.firstChild);
let ON=false,CUR="";
const esc=x=>typeof E==="function"?E(x):String(x==null?"":x).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
const vis=f=>shown(f)&&navF(f),
 areaF=a=>F.filter(f=>vis(f)&&AREA(SI[f.section])===a),
 secF=id=>F.filter(f=>f.section===id&&vis(f)),
 pc=(d,t)=>t?Math.round(d/t*100):0,
 num=(a,id,gi,si,many)=>{let n=window.NAV_NUM&&NAV_NUM.sec[id];if(n)return n;let A=(window.MT_NUM||{})[a];if(!A)return"";let p=many?[A,gi+1,si+1]:[A,si+1];return p.join(".")+(p.length<=2?".":"")};
function setOn(o){ON=o;ad.hidden=!o;configPage.classList.toggle("adOn",o);document.documentElement.classList.toggle("adOn",o);
 sideNav.querySelectorAll(".adNav").forEach(b=>{b.classList.toggle("active",o);b.toggleAttribute("aria-current",o)})}
function render(a){CUR=a;
 let V=areaF(a),n=V.filter(isset).length,t=V.length,p=pc(n,t),nx=V.find(f=>!isset(f)),req=V.filter(f=>f.required&&!isset(f)),C=2*Math.PI*54,dash=(C*p/100).toFixed(1),
  A=(window.MT_NUM||{})[a],secs=S.filter(s=>AREA(s)===a),groups=[];
 /* Sol menüyle birebir: koşula bağlı olarak menüde gösterilmeyen bölüm (ör. kapalı İçerik Planlama › Etkinlikler) dashboard'da da yok; numaralar menüyle aynı kalır */
 let inNav=new Set([...sideNav.querySelectorAll(".menuSection[data-section]")].map(x=>x.dataset.section));if(secs.some(s=>inNav.has(s.id)))secs=secs.filter(s=>inNav.has(s.id));
 secs.forEach(s=>{let g=groups[groups.length-1];if(!g||g.t!==(s.group||""))groups.push(g={t:s.group||"",list:[]});g.list.push(s)});
 let many=groups.length>1,st={done:0,doing:0,todo:0,rec:0},last=LAST[a]&&SI[LAST[a]]&&AREA(SI[LAST[a]])===a?SI[LAST[a]]:null;
 let card=(s,gi,si)=>{let fs=secF(s.id),d=fs.filter(isset).length,k=fs.length,no=num(a,s.id,gi,si,many),
   lb=!k?"Kayıt ve liste":d===k?"Tamamlandı":d?"Devam ediyor":"Başlanmadı";
  if(!k)st.rec++;else if(d===k)st.done++;else if(d)st.doing++;else st.todo++;
  return `<button type="button" class="ovCard adCard${k&&d===k?" ok":d?" on":""}" onclick="goStep('${esc(s.id)}')"><span class="t">${no?`<span class="adNo">${esc(no)}</span>`:""}<span>${esc(s.name)}</span></span><span class="d">${esc(s.desc||"")}</span><span class="m"><span>${k?`${d} / ${k} karar`:"Bölümü aç"}</span><span>${lb}</span></span>${k?`<span class="ovBar" aria-hidden="true"><i style="width:${pc(d,k)}%"></i></span>`:""}</button>`};
 let body=groups.map((g,gi)=>{let fs=V.filter(f=>g.list.some(s=>s.id===f.section)),d=fs.filter(isset).length,cards=g.list.map((s,si)=>card(s,gi,si)).join("");
  return `<div class="ovH2 adH2"><h2>${many&&A?`<span class="adNo">${A}.${gi+1}.</span> `:""}${esc(many?g.t||LB[a]:"Bölümler")}</h2><span>${g.list.length} bölüm · ${d} / ${fs.length} karar${fs.length?` · %${pc(d,fs.length)}`:""}</span></div><div class="ovGrid">${cards}</div>`}).join("");
 let b=(cls,fn,tx)=>`<button type="button" class="btn${cls}" onclick="${fn}">${tx}</button>`,
  btns=nx?b(" dark",`goToField('${esc(nx.section)}','${esc(nx.id)}')`,n?"Kaldığın yerden devam et →":"Kararlara başla →"):t?b(" dark","showPage('rules')","Proje Kurallarını gör →"):"";
 if(last&&(!nx||last.id!==nx.section))btns+=b("",`goStep('${esc(last.id)}')`,"Son açılan bölüm: "+esc(last.name));
 else if(nx)btns+=b("",`goStep('${esc(nx.section)}')`,"Bölüm rehberini oku");
 else if(secs[0])btns+=b("",`goStep('${esc(secs[0].id)}')`,"Kararları gözden geçir");
 ad.innerHTML=`<div class="intro"><div class="eyebrow">${A?A+". ":""}${esc(LB[a].toLocaleUpperCase("tr"))} · DASHBOARD</div><h1>${A?`<span class="adNum">${A}.</span> `:""}${esc(LB[a])}</h1><p>${esc(DESC[a]||"")}</p></div>
 <div class="ovTop"><div class="ovHero"><div class="ovRing"><svg width="128" height="128" viewBox="0 0 128 128" role="img" aria-label="${esc(LB[a])} kararlarının yüzde ${p}'i verildi"><circle class="trk" cx="64" cy="64" r="54" fill="none" stroke="#eef0f3" stroke-width="12"/><circle class="val" cx="64" cy="64" r="54" fill="none" stroke="#2453d6" stroke-width="12" stroke-linecap="round" stroke-dasharray="${dash} ${C.toFixed(1)}" transform="rotate(-90 64 64)"/></svg><div><b>%${p}</b><span>${n} / ${t}</span></div></div>
 <div class="ovTxt"><h2 class="adH">${t?`${n} / ${t} karar verildi`:"Bu menüde karar yok"}</h2><p>${t?(nx?`${t-n} karar kaldı. Sıradaki karar: <b>${esc(SI[nx.section].name)} › ${esc(nx.label)}</b>.`:"Bu menüdeki bütün kararlar verildi; istediğiniz bölümü açıp değiştirebilirsiniz."):"Bölümleri aşağıdan açabilirsiniz."}</p><div class="ovBtns">${btns}</div></div></div>
 <div class="ovSide">${req.length?`<div class="ovWarn"><b class="k">EKSİK ZORUNLU KARARLAR</b><span class="n">${req.length}</span><ul>${req.slice(0,6).map(f=>`<li><button type="button" onclick="goToField('${esc(f.section)}','${esc(f.id)}')">${esc(SI[f.section].name)} › ${esc(f.label)}</button></li>`).join("")}</ul>${req.length>6?`<span>ve ${req.length-6} karar daha</span>`:""}</div>`:""}
 <div class="ovBox"><b class="k">BÖLÜM DURUMU</b><ul class="adStat"><li><b>${st.done}</b> tamamlandı</li><li><b>${st.doing}</b> devam ediyor</li><li><b>${st.todo}</b> başlanmadı</li>${st.rec?`<li><b>${st.rec}</b> kayıt / liste bölümü</li>`:""}</ul><span>${secs.length} bölüm${many?`, ${groups.length} grup`:""}${req.length?"":" · eksik zorunlu karar yok"}.</span><button type="button" class="lk" onclick="adDownloads()">Çıktılar ve indirmeler →</button></div></div></div>
 ${body}`;
}
/* Dashboard'u aç: alanı (sol menü) hazırla, açık bölümün kırmızı işaretini kaldır, sayfayı göster */
window.adShow=function(a){a=a||(typeof curArea==="function"?curArea():"project");if(!LB[a]||!S.some(s=>AREA(s)===a))return false;
 if(curArea()!==a||configPage.classList.contains("hidden"))_goArea(a);
 activeFieldId=null;openSection=null;setOn(true);renderSideNav();render(a);scrollTo(0,0);return true};
window.adDownloads=function(){if(typeof v26Overview==="function"){v26Overview();setTimeout(()=>{let d=document.getElementById("dlPkgs");if(d)d.scrollIntoView({block:"start"})},60)}else showPage("rules")};
const _goArea=goArea;
goArea=function(a){if(LB[a]&&S.some(s=>AREA(s)===a)){closeNav();_goArea(a);adShow(a);return}return _goArea.apply(this,arguments)};
const _sp=showPage;
showPage=function(){if(ON)setOn(false);return _sp.apply(this,arguments)};
/* Sol menünün başında "Dashboard" satırı (alan başlık şeridinden sonra) */
const _rsn=renderSideNav;
renderSideNav=function(){let r=_rsn.apply(this,arguments);try{
 let a=typeof curArea==="function"?curArea():"";if(!LB[a]||sideNav.classList.contains("searching"))return r;
 let V=areaF(a),n=V.filter(isset).length,b=document.createElement("button");b.type="button";b.className="adNav"+(ON?" active":"");if(ON)b.setAttribute("aria-current","true");
 b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 4h7v7H4zM13 4h7v4h-7zM13 10h7v10h-7zM4 13h7v7H4z"/></svg><span class="adNavT">Dashboard</span><span class="adNavP">%${pc(n,V.length)}</span>`;
 b.title=LB[a]+" dashboard'u — "+n+"/"+V.length+" karar verildi";b.onclick=()=>adShow(a);
 let band=sideNav.querySelector(":scope>.areaBand");if(band)band.after(b);else sideNav.prepend(b)}catch(e){console.error("adNav",e)}return r};
/* Karar değişince / dosya içe aktarılınca açık dashboard tazelenir */
if(typeof renderProgress==="function"){const _rp=renderProgress;renderProgress=function(){let r=_rp.apply(this,arguments);if(ON&&CUR)try{render(CUR)}catch(e){console.error("areaDash",e)}return r}}
window.adState=()=>({on:ON,area:CUR});
})();
