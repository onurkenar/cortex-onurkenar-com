/* İçerik Planlama (2026-11-15, kullanıcı isteği: "sol menüye 8. madde olarak "İçerik Planlama" başlığı ekle, menü içeriğinde
   olması gerekenleri sonra vereceğim"). Modül şeridinde Yapay Zekâ'dan sonra (Kurallar'dan önce) "8. İçerik Planlama"
   (data-mod="plan"), ≤ 900 px çekmecede #sidePlanBtn (Yapılacaklar'dan önce); sayfa #cpPage (showPage("plan"), cpGo()),
   açıkken v26NoSide. İçerik verilene kadar yer tutucu sayfa: karar, kural, prompt, JSON ve Yapılacaklar'a hiçbir şey eklemez.
   Numara MT_NUM'a yazılmaz (karar yokken şeritte "0/0 - %0" çıkmasın diye); "8." etikete doğrudan yazılır — içerik karar
   olarak eklendiğinde MT_NUM.plan = 8 yapılıp numaralandırma ve ilerleme genel mekanizmaya bırakılır.
   Kaynak docs/v26/v26-content-plan.{js,css} → docs/v26/icerik_planlama_ekle.py */
(function(){
const N="8.",LB="İçerik Planlama",ICON="M7 3v3M17 3v3M4 9h16M5.5 5h13A1.5 1.5 0 0 1 20 6.5v12a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18.5v-12A1.5 1.5 0 0 1 5.5 5ZM8 13h3M8 16.5h7";
const PG=document.createElement("section");PG.id="cpPage";PG.setAttribute("aria-label",LB);
configPage.parentNode.insertBefore(PG,configPage);
const isOn=()=>PG.classList.contains("active");
function nav(){let rail=document.getElementById("modRail");if(rail&&!rail.querySelector('[data-mod="plan"]')){let b=document.createElement("button");b.type="button";b.className="mrBtn";b.dataset.mod="plan";b.title=LB;b.setAttribute("aria-label",N+" "+LB);
  b.innerHTML=`<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><path d="${ICON}"/></svg><span><span class="navNum">${N}</span>${LB}</span>`;
  b.onclick=()=>window.cpGo();let ai=rail.querySelector('[data-mod="ai"]');rail.insertBefore(b,ai?ai.nextSibling:rail.querySelector('[data-mod="rules"]'))}
 let ref=document.getElementById("sideTodoBtn")||document.getElementById("sideLibBtn")||document.getElementById("sideDocsBtn");
 if(ref&&!document.getElementById("sidePlanBtn")){let s=document.createElement("button");s.type="button";s.id="sidePlanBtn";s.textContent="▦\u00a0\u00a0"+N+" "+LB;s.onclick=()=>window.cpGo();ref.parentNode.insertBefore(s,ref)}}
function sync(){let on=isOn(),rail=document.getElementById("modRail");if(rail)rail.querySelectorAll(".mrBtn").forEach(b=>{if(on){let a=b.dataset.mod==="plan";b.classList.toggle("active",a);b.toggleAttribute("aria-current",a)}else if(b.dataset.mod==="plan"){b.classList.remove("active");b.removeAttribute("aria-current")}});
 if(on)document.documentElement.classList.add("v26NoSide");let s=document.getElementById("sidePlanBtn");if(s){s.classList.toggle("active",on);s.toggleAttribute("aria-current",on)}}
function render(){PG.innerHTML=`<div class="cpHead"><p class="cpEye">${N} ${LB.toLocaleUpperCase("tr")}</p><h1>${LB}</h1><p class="cpLead">Bu menünün içeriği henüz eklenmedi. Maddeler eklendiğinde burada görünecek.</p></div>`}
const _sp=showPage;
showPage=function(p){if(p==="plan"){_sp("config");configPage.classList.add("hidden");PG.classList.add("active");render();window.scrollTo(0,0);sync();return}PG.classList.remove("active");_sp(p);sync()};
const _ab=areaBtn;areaBtn=function(){_ab();if(isOn())sync()};
window.cpGo=()=>{if(typeof closeNav==="function")closeNav();showPage("plan")};
nav();
})();
