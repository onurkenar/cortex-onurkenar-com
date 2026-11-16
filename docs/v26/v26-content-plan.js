/* 8. İçerik Planlama menü alanı — arayüz bağlantıları (2026-11-15; ilk sürüm aynı gün yer tutucu sayfaydı).
   Kullanıcı kararları: 8. menü aşamalı çalışma alanı olacak; Pazarlama › Plan Dosyası buraya taşınır (8.1 Plan & Dönem +
   son alt menü Dışa Aktarım); alt menüler sırayla birlikte kurgulanır. Menü alanı "plan" (AREA), şerit düğmesi MODS'tan
   (data-mod="plan", numara MT_NUM.plan = 8), ≤ 900 px çekmecede #sidePlanBtn → goArea("plan"). Bu blok:
   çekmece düğmesi ve etkin durumu (areaBtn sarmalanır), eski cpGo() adı (goArea'ya yönlenir), kararı olmayan bölümlerde (Dışa Aktarım,
   Takvim) rehberin "0/0 karar" başlangıç kutusu ve başlıktaki "Her seçeneğin…" cümlesi gizlenir, pazarlama promptuna İÇERİK PLANI AYARLARI eklenir.
   Kaynak docs/v26/v26-content-plan.{js,css} → docs/v26/icerik_planlama_ekle.py */
(function(){
function nav(){let ref=document.getElementById("sideTodoBtn")||document.getElementById("sideLibBtn")||document.getElementById("sideDocsBtn");
 if(ref&&!document.getElementById("sidePlanBtn")){let s=document.createElement("button");s.type="button";s.id="sidePlanBtn";s.textContent="▦  İçerik Planlama";s.onclick=()=>goArea("plan");ref.parentNode.insertBefore(s,ref)}}
function sync(){let s=document.getElementById("sidePlanBtn");if(!s)return;let on=!configPage.classList.contains("hidden")&&curArea()==="plan";s.classList.toggle("active",on);s.toggleAttribute("aria-current",on)}
const _ab=areaBtn;areaBtn=function(){let r=_ab.apply(this,arguments);sync();return r};
window.cpGo=()=>goArea("plan");
const noF=sid=>!!SI[sid]&&AREA(SI[sid])==="plan"&&!F.some(f=>f.section===sid);
const _gh=guideHtml;guideHtml=function(s){let h=_gh.apply(this,arguments);if(s&&noF(s.id))h=h.replace(/<div class="gStart">[\s\S]*?<div class="gBtns">[\s\S]*?<\/button><\/div><\/div>/,"");return h};
const _rc=renderConfig;renderConfig=function(){let r=_rc.apply(this,arguments);if(noF(active))desc.textContent=SI[active].desc.replace(/\.\s*$/,"")+".";return r};
if(typeof mkMarketingPrompt==="function"){const _mp=mkMarketingPrompt;mkMarketingPrompt=function(){let t=_mp.apply(this,arguments);return t+(typeof ipPrompt==="function"?ipPrompt(ipRuleGroups()):"")}}
nav();sync();
})();
