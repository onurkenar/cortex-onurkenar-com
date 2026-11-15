/* Sertifikalar ve Belgeler satır düzenleyicisi (2026-11-15, kullanıcı isteği: "1.3.8 Sertifikalar ve Belgeler'de ... her bir belge ve
   sertifika ayrı textbox'a girilsin, dropdown listten belge / sertifika türü belirlensin (diğer seçeneği ile metin olarak belge türü
   yazılabilsin)"). CERT_F'deki metin kararı (oc_certs) satır satır çizilir: tür listesi (CERT_TYPES; "Diğer" seçilince tür metin
   kutusu açılır) + belge adı + veren kuruluş ve belge no + geçerlilik bitişi + sil; altta "Belge ekle". Değer yine metindir, her
   belge bir satır: "[Tür] Belge adı | veren kuruluş ve belge no | bitiş tarihi" (sondaki boş sütunlar yazılmaz; "|" girilirse "/"
   olur) — kural, prompt, JSON İndir, Ortak Bilgiler kartı, Yapılacaklar ve ocProofMig değişmeden çalışır; eski "Ad | kuruluş |
   tarih" satırları türsüz okunur. Boş ya da yalnız türü seçilmiş satır kayda girmez, oturum boyunca CERT_DRAFT'ta durur.
   Kaynak docs/v26/v26-certs.js → docs/v26/sertifika_satir_ekle.py */
const CERT_F={oc_certs:1},CERT_OTHER="Diğer",
 CERT_TYPES=["Yönetim sistemi sertifikası (ISO vb.)","Ürün / hizmet belgesi (TSE, CE vb.)","Akreditasyon","Lisans, ruhsat ya da izin belgesi","Mesleki yeterlilik / personel belgesi","Mesleki kuruluş üyeliği","Ödül",CERT_OTHER],
 CERT_DRAFT={};
(f=>{if(!f)return;f.placeholder="";f.explanation="Kurumun sahip olduğu yönetim sistemi sertifikaları, akreditasyonlar, lisanslar, mesleki üyelikler ve ödüllerdir. Her belgeyi ayrı satıra girin: listeden türünü seçin (listede yoksa “Diğer”i seçip türü yazın), belge adını, veren kuruluşu ve belge numarasını, geçerlilik bitiş tarihini yazın; yeni belge için “Belge ekle”. Kurumun belgesi yoksa “Sertifika ve belge yok”u işaretleyin."})(FI.oc_certs);
function certClean(s){return String(s??"").replace(/[\r\n]+/g," ").replace(/\|/g,"/").trim()}
function certParse(v){return String(v??"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>{let ty="",m=/^\[([^\]]*)\]\s*(.*)$/.exec(x);if(m){ty=m[1].trim();x=m[2]}
 let p=x.split("|").map(s=>s.trim()),r={ty,name:p[0]||"",org:"",date:""};if(p.length===2)r.org=p[1];else if(p.length>2){r.date=p[p.length-1];r.org=p.slice(1,-1).join(" / ")}return r})}
function certRow(r){let t=r.ty||"",sel=!t?"":CERT_TYPES.includes(t)?t:CERT_OTHER;return {sel,other:sel===CERT_OTHER&&t!==CERT_OTHER?t:"",name:r.name,org:r.org,date:r.date}}
function certTy(w){return certClean(w.sel===CERT_OTHER?(certClean(w.other)||CERT_OTHER):w.sel).replace(/[\[\]]/g,"")}
function certLine(w){let a=[certClean(w.name),certClean(w.org),certClean(w.date)];while(a.length&&!a[a.length-1])a.pop();if(!a.length)return "";let t=certTy(w);return (t?"["+t+"] ":"")+a.join(" | ")}
function certSer(L){return L.map(certLine).filter(Boolean).join("\n")}
function certRows(f){let L=certParse(state[f.id]).map(certRow),d=CERT_DRAFT[f.id];if(d&&certSer(d)===certSer(L))L=d;return L.length?L:[{sel:"",other:"",name:"",org:"",date:""}]}
function certRowHtml(f,w,i){let n=i+1,q=E(JSON.stringify(f.id)),o=w.sel===CERT_OTHER,ph=(a,b)=>E(i?a:b),inp=(c,cc,v,L,l,p)=>`<label class="certCell ${cc}"><span class="certL" aria-hidden="true">${L}</span><input class="control ${c}" type="text" autocomplete="off" aria-label="Belge ${n}: ${l}" placeholder="${p}" value="${E(v)}" oninput="certIn(${q},this)"></label>`;
 return `<div class="certRow${o?" other":""}" role="group" aria-label="Belge ${n}"><span class="certTy certCell"><span class="certL" aria-hidden="true">Tür</span><select class="control certSel" data-native aria-label="Belge ${n}: tür" onchange="certIn(${q},this)"><option value="">Tür seçin</option>${CERT_TYPES.map(t=>`<option value="${E(t)}"${t===w.sel?" selected":""}>${E(t)}</option>`).join("")}</select>`+
  `<input class="control certOther" type="text" autocomplete="off" aria-label="Belge ${n}: tür (Diğer)" placeholder="Belge türünü yazın" value="${E(w.other)}" oninput="certIn(${q},this)"${o?"":" hidden"}></span>`+
  inp("certName","certCN",w.name,"Belge adı","belge adı",ph("Belge adı","Örn. ISO 9001:2015"))+inp("certOrg","certCO",w.org,"Veren kuruluş ve belge no","veren kuruluş ve belge no",ph("Veren kuruluş, belge no","Örn. Örnek Belgelendirme, belge no 12345"))+inp("certDate","certCD",w.date,"Geçerlilik bitişi","geçerlilik bitişi",ph("Bitiş tarihi","Örn. 2027-05-14"))+
  `<button type="button" class="certDel" aria-label="Belge ${n} satırını sil" title="Satırı sil" onclick="certDel(${q},this)">×</button></div>`}
function certInput(f){let q=E(JSON.stringify(f.id));
 return `<div class="certBox"><div class="certHead" aria-hidden="true"><span>Tür</span><span>Belge adı</span><span>Veren kuruluş ve belge no</span><span>Geçerlilik bitişi</span><span></span></div><div class="certList">${certRows(f).map((w,i)=>certRowHtml(f,w,i)).join("")}</div><button type="button" class="certAdd" onclick="certAdd(${q})">+ Belge ekle</button></div>`}
function certBox(id){return document.querySelector('.field[data-field-id="'+id+'"] .certBox')}
function certRead(b){return [...b.querySelectorAll(".certRow")].map(r=>({sel:r.querySelector(".certSel").value,other:r.querySelector(".certOther").value,name:r.querySelector(".certName").value,org:r.querySelector(".certOrg").value,date:r.querySelector(".certDate").value}))}
function certRule(f){let el=document.querySelector('.field[data-field-id="'+f.id+'"]');if(!el)return;let rb=el.querySelector(":scope>.rule"),r=rule(f);
 if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(f,r):E(r));else if(typeof refreshRule==="function")refreshRule(f)}
function certSave(id,b){let L=certRead(b),v=certSer(L);CERT_DRAFT[id]=L;if(v)state[id]=v;else delete state[id];faAuto(id);save();renderRules();renderProgress();certRule(FI[id])}
function certIn(id,el){if(!requireProject()){refreshField(id);return}let b=el.closest(".certBox"),r=el.closest(".certRow");
 if(el.classList.contains("certSel")){let o=el.value===CERT_OTHER,x=r.querySelector(".certOther");r.classList.toggle("other",o);x.hidden=!o;if(o)x.focus()}certSave(id,b)}
function certAdd(id){if(!requireProject())return;let b=certBox(id);if(!b)return;let l=b.querySelector(".certList"),n=l.children.length,t=document.createElement("template");
 t.innerHTML=certRowHtml(FI[id],{sel:"",other:"",name:"",org:"",date:""},n);l.appendChild(t.content.firstElementChild);CERT_DRAFT[id]=certRead(b);l.lastElementChild.querySelector(".certSel").focus()}
function certDel(id,btn){if(!requireProject())return;let b=btn.closest(".certBox"),r=btn.closest(".certRow"),rows=[...b.querySelectorAll(".certRow")],i=rows.indexOf(r);
 if(rows.length>1)r.remove();else r.querySelectorAll("input").forEach(x=>x.value=""),r.querySelector(".certSel").value="";certSave(id,b);refreshField(id);
 let nb=certBox(id);if(nb){let L=nb.querySelectorAll(".certRow"),t=L[Math.min(i,L.length-1)];(t?t.querySelector(".certSel"):nb.querySelector(".certAdd")).focus()}}
