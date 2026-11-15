/* Referanslar satır düzenleyicisi (2026-11-15, kullanıcı isteği: "1.3.7 Referanslar maddesinde her bir referans ayrı satıra girilsin,
   referans marka adı, web sayfası, logo kullanım izni ayrı alanlarda belirtilsin"). REF_F'deki metin kararı (oc_proof) satır satır
   çizilir: marka adı + web sayfası (adres, yumuşak doğrulama) + logo kullanım izni (REF_LOGO listesi) + isteğe bağlı not + sil; altta
   "Referans ekle". Değer yine metindir, her referans bir satır: "Marka adı | https://… | Logo: Var (yazılı izin) | Not: …" (boş parçalar
   yazılmaz; girilen "|" → "/") — kural, prompt, JSON İndir, Ortak Bilgiler kartı, Yapılacaklar ve ocProofMig değişmeden çalışır. Okurken
   parça içeriğine bakılır: "Logo:" → izin, "Not:" → not, adres biçimi → web sayfası, ilk kalan parça → marka adı, diğerleri nota; böylece
   eski "Ad | izin | kaynak" satırları ad + not olarak okunur. Boş ya da yalnız logo izni seçilmiş satır kayda girmez, oturum boyunca
   REF_DRAFT'ta durur. Sertifikalar düzenleyicisiyle (v26-certs) aynı yapı. Kaynak docs/v26/v26-refs.js → docs/v26/referans_satir_ekle.py */
const REF_F={oc_proof:1},REF_LOGO=["Var (yazılı izin)","Yok","Bekleniyor (izin istendi)"],REF_DRAFT={},
 REF_URL=/^(https?:\/\/)?([a-z0-9-]+\.)+[a-z]{2,}(\/\S*)?$/i;
(f=>{if(!f)return;f.placeholder=""})(FI.oc_proof);
function refClean(s){return String(s??"").replace(/[\r\n]+/g," ").replace(/\|/g,"/").trim()}
function refParse(v){return String(v??"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>{let r={name:"",url:"",logo:"",note:""},N=[];
 x.split("|").map(s=>s.trim()).filter(Boolean).forEach(p=>{let m;if((m=/^logo\s*:\s*(.*)$/i.exec(p)))r.logo=m[1].trim();else if((m=/^not\s*:\s*(.*)$/i.exec(p)))N.push(m[1].trim());
  else if(!r.url&&REF_URL.test(p)&&!/\s/.test(p))r.url=p;else if(!r.name)r.name=p;else N.push(p)});r.note=N.filter(Boolean).join(" / ");return r})}
function refLogoSel(t){let x=norm(t||"");if(!x)return "";let i=REF_LOGO.findIndex(l=>norm(l)===x);if(i>=0)return REF_LOGO[i];return /^var|izin var|kullanilabilir/.test(x)?REF_LOGO[0]:/^yok|izinsiz/.test(x)?REF_LOGO[1]:/bekle|isten/.test(x)?REF_LOGO[2]:""}
function refRow(r){return {name:r.name,url:r.url,logo:refLogoSel(r.logo),logoTxt:refLogoSel(r.logo)?"":r.logo,note:r.note}}
function refLine(w){let name=refClean(w.name),url=refClean(w.url),note=refClean(w.note),lg=refClean(w.logo||w.logoTxt);if(!name&&!url&&!note)return "";
 return [name,url,lg?"Logo: "+lg:"",note?"Not: "+note:""].filter(Boolean).join(" | ")}
function refSer(L){return L.map(refLine).filter(Boolean).join("\n")}
function refRows(f){let L=refParse(state[f.id]).map(refRow),d=REF_DRAFT[f.id];if(d&&refSer(d)===refSer(L))L=d;return L.length?L:[{name:"",url:"",logo:"",logoTxt:"",note:""}]}
function refUrlBad(u){u=String(u||"").trim();return !!u&&!REF_URL.test(u)}
function refRowHtml(f,w,i){let n=i+1,q=E(JSON.stringify(f.id)),ph=(a,b)=>E(i?a:b),bad=refUrlBad(w.url),
 inp=(c,cc,v,L,l,p,t,x)=>`<label class="refCell ${cc}"><span class="refL" aria-hidden="true">${L}</span><input class="control ${c}" type="${t||"text"}" inputmode="${t==="url"?"url":"text"}" autocomplete="off" spellcheck="false" aria-label="Referans ${n}: ${l}" placeholder="${p}" value="${E(v)}" oninput="refIn(${q},this)"${x||""}></label>`;
 return `<div class="refRow" role="group" aria-label="Referans ${n}">`+
  inp("refName","refCN",w.name,"Marka adı","marka adı",ph("Marka adı","Örn. Örnek AŞ"))+
  inp("refUrl","refCU",w.url,"Web sayfası","web sayfası",ph("https://…","Örn. https://www.ornek.com.tr"),"url",` aria-invalid="${bad}"`)+
  `<span class="refCell refCG"><span class="refL" aria-hidden="true">Logo kullanım izni</span><select class="control refLogo" data-native aria-label="Referans ${n}: logo kullanım izni" onchange="refIn(${q},this)"><option value="">İzin durumu seçin</option>${REF_LOGO.map(t=>`<option value="${E(t)}"${t===w.logo?" selected":""}>${E(t)}</option>`).join("")}${w.logoTxt?`<option value="${E(w.logoTxt)}" selected>${E(w.logoTxt)}</option>`:""}</select></span>`+
  inp("refNote","refCT",w.note,"Not (isteğe bağlı)","not",ph("İzin kaynağı, tarih …","Örn. e-posta ile izin, 2026-03"))+
  `<button type="button" class="refDel" aria-label="Referans ${n} satırını sil" title="Satırı sil" onclick="refDel(${q},this)">×</button>`+
  `<small class="refWarn" aria-live="polite"${bad?"":" hidden"}>Web sayfası adresi gibi görünmüyor. Örnek: https://www.ornek.com.tr</small></div>`}
function refInput(f){let q=E(JSON.stringify(f.id));
 return `<div class="refBox"><div class="refHead" aria-hidden="true"><span>Marka adı</span><span>Web sayfası</span><span>Logo kullanım izni</span><span>Not (isteğe bağlı)</span><span></span></div><div class="refList">${refRows(f).map((w,i)=>refRowHtml(f,w,i)).join("")}</div><button type="button" class="refAdd" onclick="refAdd(${q})">+ Referans ekle</button></div>`}
function refBox(id){return document.querySelector('.field[data-field-id="'+id+'"] .refBox')}
function refRead(b){return [...b.querySelectorAll(".refRow")].map(r=>{let lg=r.querySelector(".refLogo").value;return {name:r.querySelector(".refName").value,url:r.querySelector(".refUrl").value,logo:REF_LOGO.includes(lg)?lg:"",logoTxt:REF_LOGO.includes(lg)?"":lg,note:r.querySelector(".refNote").value}})}
function refRule(f){let el=document.querySelector('.field[data-field-id="'+f.id+'"]');if(!el)return;let rb=el.querySelector(".rule"),r=rule(f);
 if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(f,r):E(r));else if(typeof refreshRule==="function")refreshRule(f)}
function refSave(id,b){let L=refRead(b),v=refSer(L);REF_DRAFT[id]=L;if(v)state[id]=v;else delete state[id];faAuto(id);save();renderRules();renderProgress();refRule(FI[id])}
function refIn(id,el){if(!requireProject()){refreshField(id);return}let b=el.closest(".refBox");
 if(el.classList.contains("refUrl")){let bad=refUrlBad(el.value),w=el.closest(".refRow").querySelector(".refWarn");el.setAttribute("aria-invalid",String(bad));if(w)w.hidden=!bad}refSave(id,b)}
function refAdd(id){if(!requireProject())return;let b=refBox(id);if(!b)return;let l=b.querySelector(".refList"),n=l.children.length,t=document.createElement("template");
 t.innerHTML=refRowHtml(FI[id],{name:"",url:"",logo:"",logoTxt:"",note:""},n);l.appendChild(t.content.firstElementChild);REF_DRAFT[id]=refRead(b);l.lastElementChild.querySelector(".refName").focus()}
function refDel(id,btn){if(!requireProject())return;let b=btn.closest(".refBox"),r=btn.closest(".refRow"),rows=[...b.querySelectorAll(".refRow")],i=rows.indexOf(r);
 if(rows.length>1)r.remove();else{r.querySelectorAll("input").forEach(x=>x.value="");r.querySelector(".refLogo").value=""}refSave(id,b);refreshField(id);
 let nb=refBox(id);if(nb){let L=nb.querySelectorAll(".refRow"),t=L[Math.min(i,L.length-1)];(t?t.querySelector(".refName"):nb.querySelector(".refAdd")).focus()}}
