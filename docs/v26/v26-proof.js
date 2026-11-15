/* Referanslar, sertifikalar ve başarı metrikleri ayrı kararlar (2026-11-15, kullanıcı isteği: "1.3.7 Referanslar, Sertifikalar ve
   Başarı Metrikleri — referanslar, sertifikalar, başarı metriklerini ayrıştır"). oc_proof artık yalnız "Referanslar"; yeni
   oc_certs "Sertifikalar ve Belgeler" ve oc_metrics "Başarı Metrikleri". Eski karışık listedeki "Ad | tür | kaynak" satırları
   türüne göre bir kez taşınır (ocMig sonunda ocProofMig): tür sütunu sertifika / belge / akreditasyon / lisans / ödül / üyelik →
   oc_certs, metrik / başarı / istatistik → oc_metrics, referans / müşteri → oc_proof'ta kalır; tür sütunu çıkarılır. Hedef alan
   doluysa satır olduğu gibi oc_proof'ta kalır; tür sütunu olmayan satıra dokunulmaz. Kaynak docs/v26/v26-proof.js →
   docs/ortak-bilgiler/kanit_ayir_ekle.py */
function ocProofMig(st){let t=st.oc_proof;if(typeof t!=="string"||!t.trim())return;let A=[],hit=false;
 t.split(/\r?\n/).forEach(raw=>{let x=raw.trim();if(!x)return;let p=x.split("|").map(s=>s.trim()),k=p.length>=3||p.length===2?norm(p[1]):"",
  ty=/^(sertifika|belge|akreditasyon|lisans|odul|uyelik)/.test(k)?"c":/^(metrik|basari|istatistik|rakam)/.test(k)?"m":/^(referans|musteri)/.test(k)?"r":"";
  if(ty)hit=true;let q=p.slice();if(ty)q.splice(1,1);A.push({ty,orig:x,clean:q.filter(Boolean).join(" | ")})});
 if(!hit)return;let keep=[],put=(key,ty)=>{let L=A.filter(a=>a.ty===ty);if(!L.length)return;if(String(st[key]??"").trim())L.forEach(a=>a.keepOrig=true);else st[key]=L.map(a=>a.clean).join("\n")};
 put("oc_certs","c");put("oc_metrics","m");
 A.forEach(a=>{if(a.ty==="c"||a.ty==="m"){if(a.keepOrig)keep.push(a.orig)}else keep.push(a.ty==="r"?a.clean:a.orig)});
 if(keep.length)st.oc_proof=keep.join("\n");else delete st.oc_proof}
