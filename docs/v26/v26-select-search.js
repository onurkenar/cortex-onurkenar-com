/* Açılır listelerde arama (2026-11-13, kullanıcı isteği: "dropdown list içerisinde kelime ile arama yapılabilsin … tüm dropdownlarda").
   Bütün tek seçimli <select>'ler (sonradan çizilenler dahil) tıklanınca, Enter / Boşluk / ok tuşu / Alt+↓ / F4 ile ya da dokunmatikte
   dokununca yerel liste yerine arama kutulu bir pencere açar. Seçenekler açılış anında <select>'ten okunur (geç doldurulan listeler —
   ör. "Sorumlu ajan" faFill — önce kendi onfocus / onmousedown işleyicisini çalıştırır), seçim select.value'ya yazılır ve
   input + change olayları gönderilir: var olan onchange işleyicileri aynen çalışır, veri / kural / kayıt değişmez.
   Arama menü aramasıyla aynı (norm + hit: Türkçe harf katlama, her kelime geçmeli, 3 harf ve altı kelime başında); grup başlığı
   (ör. departman adı) da aranır. Hariç: multiple, size > 1, disabled, data-native; kilitli projede karar alanlarındaki listeler.
   Kaynak docs/v26/v26-select-search.{js,css} → docs/v26/acilir_arama_ekle.py */
(function(){
"use strict";
var N=function(t){return typeof norm==="function"?norm(t):String(t).toLocaleLowerCase("tr").trim()},
    H=function(h,q){return typeof hit==="function"?hit(h,q):q.split(" ").every(function(w){return h.indexOf(w)>=0})};
var pop=null,cur=null,items=[],act=-1,uid=0,touch=null;
function esc(t){return String(t).replace(/[&<>"']/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]})}
function ok(s){
  if(!s||s.tagName!=="SELECT"||s.multiple||s.size>1||s.disabled||s.hasAttribute("data-native"))return false;
  if(s.closest(".slxPop"))return false;
  try{var fb=document.getElementById("fieldBox"),fl=s.closest(".field");
    if(fb&&fl&&fb.contains(fl)&&typeof projectReady==="function"&&!projectReady()&&fl.dataset.fieldId!=="project_name")return false}catch(e){}
  return true}
function close(back){
  if(!pop)return;var s=cur;pop.remove();pop=null;cur=null;items=[];act=-1;
  if(s){s.removeAttribute("aria-expanded");if(back&&document.contains(s))try{s.focus({preventScroll:true})}catch(e){s.focus()}}}
function rows(){
  var out=[];Array.prototype.forEach.call(cur.options,function(o,i){
    if(o.hidden)return;var g=o.parentElement&&o.parentElement.tagName==="OPTGROUP"?o.parentElement:null;
    if(g&&g.hidden)return;
    out.push({i:i,t:o.textContent.trim(),g:g?g.label:"",dis:o.disabled||(g&&g.disabled),sel:o.selected,ph:o.value===""&&i===0})});
  return out}
function draw(q){
  var L=pop.querySelector(".slxList"),k=N(q||""),R=rows(),h="",lastG=null,n=0;items=[];
  R.forEach(function(r){
    if(k&&(r.ph||!H(N(r.t+" "+r.g),k)))return;
    if(r.g!==lastG&&r.g){h+='<li class="slxGrp" role="presentation">'+esc(r.g)+"</li>";}
    lastG=r.g;var id="slx"+uid+"-"+r.i;
    h+='<li id="'+id+'" role="option" class="slxOpt'+(r.sel?" on":"")+(r.dis?" dis":"")+'" data-i="'+r.i+'" aria-selected="'+(r.sel?"true":"false")+'"'+(r.dis?' aria-disabled="true"':"")+">"+esc(r.t||"—")+"</li>";
    if(!r.dis)items.push(r.i);if(!r.ph)n++});
  L.innerHTML=h||'<li class="slxNone" role="presentation">Eşleşen seçenek yok</li>';
  pop.querySelector(".slxN").textContent=k?n+" sonuç":n+" seçenek";
  var si=items.indexOf(cur.selectedIndex);setAct(k?(items.length?0:-1):(si>=0?si:(items.length?0:-1)),true)}
function setAct(j,scroll){
  act=j;var L=pop.querySelector(".slxList"),inp=pop.querySelector(".slxQ");
  Array.prototype.forEach.call(L.querySelectorAll(".slxOpt.act"),function(x){x.classList.remove("act")});
  if(j<0){inp.removeAttribute("aria-activedescendant");return}
  var el=L.querySelector('[data-i="'+items[j]+'"]');if(!el)return;el.classList.add("act");inp.setAttribute("aria-activedescendant",el.id);
  if(scroll)el.scrollIntoView({block:"nearest"})}
function pick(i){
  var s=cur;if(!s)return;var o=s.options[i];if(!o||o.disabled)return;
  close(true);if(s.selectedIndex===i)return;
  s.selectedIndex=i;s.dispatchEvent(new Event("input",{bubbles:true}));s.dispatchEvent(new Event("change",{bubbles:true}))}
function place(){
  if(!pop||!cur)return;var r=cur.getBoundingClientRect(),vw=document.documentElement.clientWidth,vh=window.innerHeight,
    w=Math.min(Math.max(r.width,340),560,vw-16),left=Math.min(Math.max(r.left,8),vw-w-8),below=vh-r.bottom-12,above=r.top-12,
    up=below<260&&above>below,room=Math.max(160,Math.min(440,up?above:below));
  pop.style.width=w+"px";pop.style.left=left+"px";pop.style.maxHeight=room+"px";
  if(up){pop.style.top="";pop.style.bottom=(vh-r.top+4)+"px"}else{pop.style.bottom="";pop.style.top=(r.bottom+4)+"px"}}
function open(s){
  if(pop)close(false);cur=s;uid++;
  var lab=s.getAttribute("aria-label")||(s.labels&&s.labels[0]&&s.labels[0].textContent)||"Seçenekler";
  pop=document.createElement("div");pop.className="slxPop";
  pop.innerHTML='<div class="slxHead"><input class="slxQ" type="search" autocomplete="off" spellcheck="false" role="combobox" aria-expanded="true" aria-autocomplete="list" aria-controls="slxL'+uid+'" aria-label="'+esc(lab)+' — seçeneklerde ara" placeholder="Seçeneklerde ara…"><span class="slxN" aria-live="polite"></span></div><ul class="slxList" id="slxL'+uid+'" role="listbox" aria-label="'+esc(lab)+'"></ul>';
  (s.closest("dialog[open]")||document.body).appendChild(pop);
  s.setAttribute("aria-expanded","true");
  var inp=pop.querySelector(".slxQ");
  inp.addEventListener("input",function(){draw(inp.value)});
  inp.addEventListener("keydown",function(e){
    if(e.key==="ArrowDown"){e.preventDefault();if(items.length)setAct(Math.min(act+1,items.length-1),true)}
    else if(e.key==="ArrowUp"){e.preventDefault();if(items.length)setAct(Math.max(act-1,0),true)}
    else if(e.key==="Home"&&!inp.value){e.preventDefault();if(items.length)setAct(0,true)}
    else if(e.key==="End"&&!inp.value){e.preventDefault();if(items.length)setAct(items.length-1,true)}
    else if(e.key==="PageDown"){e.preventDefault();if(items.length)setAct(Math.min(act+8,items.length-1),true)}
    else if(e.key==="PageUp"){e.preventDefault();if(items.length)setAct(Math.max(act-8,0),true)}
    else if(e.key==="Enter"){e.preventDefault();if(act>=0)pick(items[act])}
    else if(e.key==="Escape"){e.preventDefault();e.stopPropagation();close(true)}
    else if(e.key==="Tab"){close(true)}});
  var L=pop.querySelector(".slxList");
  L.addEventListener("mousemove",function(e){var li=e.target.closest(".slxOpt:not(.dis)");if(li){var j=items.indexOf(+li.dataset.i);if(j!==act)setAct(j,false)}});
  L.addEventListener("click",function(e){var li=e.target.closest(".slxOpt");if(li&&!li.classList.contains("dis"))pick(+li.dataset.i)});
  ["mousedown","click","pointerdown","touchend"].forEach(function(t){pop.addEventListener(t,function(e){e.stopPropagation()})});
  L.addEventListener("mousedown",function(e){e.preventDefault()});
  draw("");place();
  if(!window.matchMedia||matchMedia("(pointer:fine)").matches)inp.focus({preventScroll:true})}
function later(s){try{s.focus({preventScroll:true})}catch(e){s.focus()}setTimeout(function(){if(document.contains(s))open(s)},0)}
document.addEventListener("mousedown",function(e){
  if(e.button!==0)return;var s=e.target.closest&&e.target.closest("select");
  if(pop&&!pop.contains(e.target)&&s!==cur)close(false);
  if(!s||!ok(s))return;if(s===cur&&pop){e.preventDefault();close(true);return}
  e.preventDefault();later(s)},true);
document.addEventListener("touchstart",function(e){var t=e.touches[0];touch=t?{x:t.clientX,y:t.clientY}:null},{capture:true,passive:true});
document.addEventListener("touchend",function(e){
  var s=e.target.closest&&e.target.closest("select"),t=e.changedTouches[0];
  if(pop&&!pop.contains(e.target)&&s!==cur)close(false);
  if(!s||!ok(s)||!touch||!t||Math.abs(t.clientX-touch.x)>10||Math.abs(t.clientY-touch.y)>10)return;
  e.preventDefault();later(s)},{capture:true,passive:false});
document.addEventListener("keydown",function(e){
  var s=e.target;if(!s||s.tagName!=="SELECT"||!ok(s)||pop)return;
  var k=e.key;if(k===" "||k==="Enter"||k==="F4"||k==="ArrowDown"||k==="ArrowUp"){
    if((k==="ArrowDown"||k==="ArrowUp")&&!e.altKey&&!/Mac|iP/.test(navigator.platform||""))return;
    e.preventDefault();open(s)}},true);
function follow(){if(!pop||!cur)return;if(!document.contains(cur)){close(false);return}var r=cur.getBoundingClientRect();if(r.bottom<0||r.top>window.innerHeight){close(false);return}place()}
window.addEventListener("resize",follow);
document.addEventListener("scroll",function(e){if(pop&&!(e.target&&e.target.nodeType===1&&pop.contains(e.target)))follow()},true);
window.v26SelectSearch={open:function(s){if(ok(s))open(s)},close:close,state:function(){return{open:!!pop,items:items.length,act:act}}};
})();
