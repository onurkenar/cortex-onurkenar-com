/* V26 mobil kullanım (2026-11-12): ekrandan taşan tabloları işaretler, klavye açıkken alt şeridi serbest bırakır.
   Yalnız görünüm — veri, kural, prompt ve kayıt değişmez. */
(function(){
"use strict";
var MQ=matchMedia("(max-width:900px)"),root=document.documentElement,raf=0;
function scrolled(el){for(var p=el.parentElement;p&&p!==document.body;p=p.parentElement){var o=getComputedStyle(p).overflowX;if(o==="auto"||o==="scroll")return true}return false}
function tables(){raf=0;var all=document.querySelectorAll("table");for(var i=0;i<all.length;i++){var t=all[i];
 if(!MQ.matches){t.classList.remove("v26Scroll");continue}
 if(t.classList.contains("v26Scroll")||!t.offsetWidth)continue;
 var p=t.parentElement;if(p&&t.offsetWidth>p.clientWidth+1&&!scrolled(t))t.classList.add("v26Scroll")}}
function later(){if(!raf)raf=requestAnimationFrame(tables)}
new MutationObserver(later).observe(document.body,{childList:true,subtree:true});
(MQ.addEventListener?MQ.addEventListener("change",later):MQ.addListener(later));
addEventListener("resize",later);
function typing(el){if(!el||!el.matches)return false;if(el.isContentEditable)return true;
 if(el.matches("textarea:not([readonly]),select"))return true;
 return el.matches("input:not([readonly])")&&!/^(checkbox|radio|range|color|file|button|submit|reset|image)$/.test(el.type)}
document.addEventListener("focusin",function(e){if(MQ.matches&&typing(e.target))root.classList.add("v26Typing")});
document.addEventListener("focusout",function(){setTimeout(function(){if(!typing(document.activeElement))root.classList.remove("v26Typing")},0)});
later();
window.v26MobileDebug={tables:tables};
})();
