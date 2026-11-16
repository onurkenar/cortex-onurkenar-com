/* Kayıt alanları çekirdeği (2026-11-15) — 8. İçerik Planlama'nın kayıt tutan alt menüleri (Ürün ve Hizmetler, Blog Yazıları,
   sonrakiler) için ortak sarmalayıcılar. Her alt menü window.REC[alanKimliği] = {isset, rule, sum, box, hide?, closed?} ile
   kaydolur; alanın DATA'daki tipi "records"tur. Çekirdek isset / ruleBase / one / shown / renderSideNav / guideHtml'i kimliğe göre
   yönlendirir: kayıt alanı kendi isset ve kural metnini verir, one() yerine kendi düzenleyicisini çizer; hide() doğruysa alan
   gizlidir (showIf'in anlatamadığı koşullar için, örn. "Blog yok"); gizli alanın bölümü sol menüden çıkarılır ve rehbere
   closed kartı eklenir. Yapılacaklar özeti window.recSum (v26-todo.js). Kaynak docs/v26/v26-records.js → urun_hizmet_ekle.py */
window.REC=window.REC||{};
(function(){
if(window.REC_CORE)return;window.REC_CORE=1;
const H=f=>f&&window.REC[f.id];
const _sh=shown;shown=function(f){let h=H(f);if(h&&h.hide&&h.hide())return false;return _sh.apply(this,arguments)};
const _is=isset;isset=function(f){let h=H(f);return h?!!h.isset():_is.apply(this,arguments)};
const _rb=ruleBase;ruleBase=function(f){let h=H(f);return h?(h.isset()?h.rule():""):_rb.apply(this,arguments)};
const _one=one;one=function(f){let h=H(f);return h?h.box(f):_one.apply(this,arguments)};
window.recSum=f=>{let h=H(f);return h?h.sum():""};
const _rsn=renderSideNav;renderSideNav=function(){let r=_rsn.apply(this,arguments),ch=0;
 Object.keys(window.REC).forEach(id=>{let f=FI[id];if(!f||shown(f))return;if(F.some(x=>x.section===f.section&&shown(x)&&navF(x)))return;let s=sideNav.querySelector(`.menuSection[data-section="${f.section}"]`);if(s){s.remove();ch=1}});
 if(ch&&typeof window.navNumber==="function")window.navNumber();return r};
const _gh=guideHtml;guideHtml=function(s){let h=_gh.apply(this,arguments),id=s&&Object.keys(window.REC).find(k=>FI[k]&&FI[k].section===s.id),x=id&&window.REC[id];
 if(x&&!shown(FI[id])&&x.closed)h=x.closed+h.replace(/<div class="gStart">[\s\S]*?<div class="gBtns">[\s\S]*?<\/button><\/div><\/div>/,"");return h};
})();
