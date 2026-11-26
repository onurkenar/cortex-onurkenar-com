/* Özel ders platformları ayrı karar (2026-11-26, kullanıcı isteği: "özel ders platformlarını ayrı bir alana taşı").
   Özel Ders Alanı ve Mentural, 1.6.7 Online Eğitim Platformu Hesapları'ndan (oc_eduplatforms) 1.6.8 Özel Ders ve Mentorluk
   Platformu Profilleri'ne (oc_tutoring) taşındı. Eski kayıtlardaki bu iki kutu ocMig sonunda bir kez taşınır (ocTutorMig):
   hedef kutu boşsa değer olduğu gibi, doluysa ve farklıysa "Diğer" satırına "Ad | adres" olarak eklenir — veri kaybolmaz;
   kaynakta başka kutu kalmazsa oc_eduplatforms silinir. Kaynak docs/v26/v26-tutoring.js → docs/v26/ozel_ders_ekle.py */
function ocTutorMig(st){let e=st.oc_eduplatforms;if(!e||typeof e!=="object")return;
 const M={ozeldersalani:"Özel Ders Alanı",mentural:"Mentural"};let ks=Object.keys(M).filter(k=>e[k]!==undefined);if(!ks.length)return;
 let src=Object.assign({},e),t=Object.assign({},st.oc_tutoring&&typeof st.oc_tutoring==="object"?st.oc_tutoring:{});
 ks.forEach(k=>{let v=String(src[k]??"").trim();delete src[k];if(!v)return;let cur=String(t[k]??"").trim();
  if(!cur)t[k]=v;else if(cur!==v)t.diger=(String(t.diger||"").trim()?String(t.diger).replace(/\s+$/,"")+"\n":"")+M[k]+" | "+v});
 if(Object.keys(src).length)st.oc_eduplatforms=src;else delete st.oc_eduplatforms;
 if(Object.keys(t).length)st.oc_tutoring=t}
