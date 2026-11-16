/* Ürün / Hizmet Listesi satır düzenleyicisi (2026-11-15, kullanıcı isteği: "link ve ürün adı ayrı textbox alanları girilsin").
   SVC_F'deki metin kararı (oc_services) satır satır çizilir: ürün / hizmet adı + sayfa adresi (isteğe bağlı; "/yol/" ya da tam adres,
   yumuşak doğrulama) + sil; altta "Kalem ekle". Değer yine metindir, her kalem bir satır: "Ad | /sayfa-adresi/" (adres boşsa yalnız
   ad; girilen "|" → "/") — kural, prompt, JSON İndir, Ortak Bilgiler kartı ve oc_services'i "Ad | sayfa adresi" satırları olarak
   okuyan 8.2 Ürün ve Hizmetler / 8.9 Google Ads / 8.10 Meta Ads (v26-products.js items(), kayıt anahtarı prSlug(ad)) değişmeden
   çalışır. Okurken ilk parça ad, kalan parçalar adres olur (fazla parça " / " ile birleşir, kayıp yok). Adı boş satır (yalnız
   adres) kayda girmez — 8. menü adsız kalemi zaten yok sayar —, oturum boyunca SVC_DRAFT'ta durur. Referanslar düzenleyicisiyle (v26-refs) aynı yapı. Kaynak docs/v26/v26-svc.js →
   docs/v26/urun_satir_ekle.py */
const SVC_F={oc_services:1},SVC_DRAFT={},SVC_URL=/^(\/\S*|(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?)$/i;
function svcClean(s){return String(s??"").replace(/[\r\n]+/g," ").replace(/\|/g,"/").trim()}
function svcParse(v){return String(v??"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>{let p=x.split("|").map(s=>s.trim());return {name:p[0]||"",url:p.slice(1).filter(Boolean).join(" / ")}})}
function svcLine(w){let name=svcClean(w.name),url=svcClean(w.url);if(!name)return "";return url?name+" | "+url:name}
function svcSer(L){return L.map(svcLine).filter(Boolean).join("\n")}
function svcRows(f){let L=svcParse(state[f.id]),d=SVC_DRAFT[f.id];if(d&&svcSer(d)===svcSer(L))L=d;return L.length?L:[{name:"",url:""}]}
function svcUrlBad(u){u=String(u||"").trim();return !!u&&(!SVC_URL.test(u)||/\s/.test(u))}
function svcRowHtml(f,w,i){let n=i+1,q=E(JSON.stringify(f.id)),ph=(a,b)=>E(i?a:b),bad=svcUrlBad(w.url),
 inp=(c,cc,v,L,l,p,x)=>`<label class="svcCell ${cc}"><span class="svcL" aria-hidden="true">${L}</span><input class="control ${c}" type="text" autocomplete="off" spellcheck="${c==="svcName"}" aria-label="Kalem ${n}: ${l}" placeholder="${p}" value="${E(v)}" oninput="svcIn(${q},this)"${x||""}></label>`;
 return `<div class="svcRow" role="group" aria-label="Kalem ${n}">`+
  inp("svcName","svcCN",w.name,"Ürün / hizmet adı","ürün / hizmet adı",ph("Ürün / hizmet adı","Örn. İmplant tedavisi"))+
  inp("svcUrl","svcCU",w.url,"Sayfa adresi (isteğe bağlı)","sayfa adresi",ph("/sayfa-adresi/","Örn. /implant-tedavisi/")," inputmode=\"url\" aria-invalid=\""+bad+"\"")+
  `<button type="button" class="svcDel" aria-label="Kalem ${n} satırını sil" title="Satırı sil" onclick="svcDel(${q},this)">×</button>`+
  `<small class="svcWarn" aria-live="polite"${bad?"":" hidden"}>Sayfa adresi gibi görünmüyor. Örnek: /implant-tedavisi/ ya da https://www.ornek.com.tr/implant-tedavisi/</small></div>`}
function svcInput(f){let q=E(JSON.stringify(f.id));
 return `<div class="svcBox"><div class="svcHead" aria-hidden="true"><span>Ürün / hizmet adı</span><span>Sayfa adresi (isteğe bağlı)</span><span></span></div><div class="svcList">${svcRows(f).map((w,i)=>svcRowHtml(f,w,i)).join("")}</div><button type="button" class="svcAdd" onclick="svcAdd(${q})">+ Kalem ekle</button></div>`}
function svcBox(id){return document.querySelector('.field[data-field-id="'+id+'"] .svcBox')}
function svcRead(b){return [...b.querySelectorAll(".svcRow")].map(r=>({name:r.querySelector(".svcName").value,url:r.querySelector(".svcUrl").value}))}
function svcRule(f){let el=document.querySelector('.field[data-field-id="'+f.id+'"]');if(!el)return;let rb=el.querySelector(".rule"),r=rule(f);
 if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(f,r):E(r));else if(typeof refreshRule==="function")refreshRule(f)}
function svcSave(id,b){let L=svcRead(b),v=svcSer(L);SVC_DRAFT[id]=L;if(v)state[id]=v;else delete state[id];faAuto(id);save();renderRules();renderProgress();svcRule(FI[id])}
function svcIn(id,el){if(!requireProject()){refreshField(id);return}let b=el.closest(".svcBox");
 if(el.classList.contains("svcUrl")){let bad=svcUrlBad(el.value),w=el.closest(".svcRow").querySelector(".svcWarn");el.setAttribute("aria-invalid",String(bad));if(w)w.hidden=!bad}svcSave(id,b)}
function svcAdd(id){if(!requireProject())return;let b=svcBox(id);if(!b)return;let l=b.querySelector(".svcList"),n=l.children.length,t=document.createElement("template");
 t.innerHTML=svcRowHtml(FI[id],{name:"",url:""},n);l.appendChild(t.content.firstElementChild);SVC_DRAFT[id]=svcRead(b);l.lastElementChild.querySelector(".svcName").focus()}
function svcDel(id,btn){if(!requireProject())return;let b=btn.closest(".svcBox"),r=btn.closest(".svcRow"),rows=[...b.querySelectorAll(".svcRow")],i=rows.indexOf(r);
 if(rows.length>1)r.remove();else r.querySelectorAll("input").forEach(x=>x.value="");svcSave(id,b);refreshField(id);
 let nb=svcBox(id);if(nb){let L=nb.querySelectorAll(".svcRow"),t=L[Math.min(i,L.length-1)];(t?t.querySelector(".svcName"):nb.querySelector(".svcAdd")).focus()}}
