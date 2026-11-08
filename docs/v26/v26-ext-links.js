/* Dış bağlantılar (2026-11-08, kullanıcı isteği): GitHub reposu ve onurkenar.com.
   Modül şeridinde boşluğun (.mrSep) hemen altına, tema düğmesinin üstüne; mobil çekmecede alt menünün sonuna. Yeni sekmede açılır. */
(()=>{
const L=[
 {k:"gh",href:"https://github.com/onurkenar/cortex-onurkenar-com",t:"GitHub",title:"GitHub reposu (yeni sekmede açılır)",svg:'<svg viewBox="0 0 16 16" aria-hidden="true" fill="currentColor"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg>'},
 {k:"web",href:"https://onurkenar.com/",utm:true,t:"onurkenar.com",short:"Web sitesi",title:"onurkenar.com (yeni sekmede açılır)",svg:'<svg viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.6 3.8 5.6 3.8 9S14.5 18.4 12 21M12 3C9.5 5.6 8.2 8.6 8.2 12s1.3 6.4 3.8 9"/></svg>'}];
/* onurkenar.com bağlantısı UTM'li (2026-11-08, kullanıcı isteği): kaynak bu uygulama, içerik tıklanan yer */
const UTM={utm_source:"cortex.onurkenar.com",utm_medium:"referral",utm_campaign:"cortex"};
const url=(x,pos)=>{if(!x.utm)return x.href;let u=new URL(x.href);Object.entries(UTM).forEach(([k,v])=>u.searchParams.set(k,v));u.searchParams.set("utm_content",pos);return u.href};
const a=(x,cls,label,pos)=>{let e=document.createElement("a");e.className=cls;e.href=url(x,pos);e.target="_blank";e.rel="noopener noreferrer";e.title=x.title;e.setAttribute("aria-label",x.title);e.dataset.ext=x.k;e.innerHTML=x.svg+`<span>${label}</span>`;return e};
function rail(){let r=document.getElementById("modRail");if(!r||r.querySelector(".mrExt"))return;let sep=r.querySelector(".mrSep"),ref=sep?sep.nextSibling:null;L.forEach(x=>r.insertBefore(a(x,"mrBtn mrExt",x.short||x.t,"sidebar"),ref))}
function foot(){let f=document.querySelector(".sideFooter");if(!f||f.querySelector(".sideExt"))return;let d=document.createElement("div");d.className="sideExt";d.setAttribute("role","group");d.setAttribute("aria-label","Dış bağlantılar");L.forEach(x=>d.appendChild(a(x,"",x.t,"mobile_menu")));f.appendChild(d)}
try{rail();foot()}catch(e){console.error("ext links",e)}
})();
