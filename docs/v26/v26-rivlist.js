/* Rakip Listesi satır düzenleyicisi (2026-11-16, kullanıcı isteği: "1.7.1 Rakip Listesi ile 8.10.1 Rakip Kayıtları aynı içerik,
   1.7.1 Rakip Listesi'nde birleştirelim"; kararlar: satır + açılır ayrıntı — ayrıntılar yalnız Pazarlama › Rakip Analizi açıkken —,
   8. menüde Karşı Aksiyonlar ve Potansiyel Müşteri Adayları kalır). RIV_F'deki metin kararı (oc_competitors) satır satır çizilir:
   marka adı, web sitesi, tür (Doğrudan / Dolaylı / İkame) + sil; altta "+ Rakip ekle". Değer yine metindir, her rakip bir satır
   "Ad | adres | tür" (boş sondaki parçalar yazılmaz; adı yoksa "adres |  | tür" — ocRivals adı alan adından türetir; girilen "|" → "/"),
   bu yüzden ocRivals ve onu okuyan her şey (SEO denetimi, Google / Meta Ads, içerik planının Rakipler sekmesi, 8. menü) değişmez.
   Rakip Analizi açıkken her dolu satırın altında "Ayrıntılar" (window.RVD, v26-rivals.js: profil … reklam, kaynak uyarısı, Claude
   talimatı; değer state.ip_rv_list[slug]); ad değişince ayrıntılar yeni anahtara taşınır (RVD.remap; karşı aksiyon ve aday bağlantıları da). Boş satır kayda girmez,
   oturum boyunca RIV_DRAFT'ta durur. Ürün / Hizmet Listesi düzenleyicisiyle (v26-svc) aynı yapı. Kaynak docs/v26/v26-rivlist.js →
   docs/v26/rakip_ekle.py */
const RIV_F={oc_competitors:1},RIV_DRAFT={},RIV_TUR=["Doğrudan","Dolaylı","İkame"];
function rivClean(s){return String(s??"").replace(/[\r\n]+/g," ").replace(/\|/g,"/").trim()}
function rivTur(t){let n=norm(String(t||""));return n.startsWith("dog")?"Doğrudan":n.startsWith("dol")?"Dolaylı":n.startsWith("ika")?"İkame":""}
function rivParse(v){return String(v??"").split(/\r?\n/).map(x=>x.trim()).filter(Boolean).map(x=>{let p=x.split("|").map(s=>s.trim()),t=rivTur(p[2]);return {name:p[0]||"",url:p[1]||"",tur:t,extra:t?"":p.slice(2).filter(Boolean).join(" / ")}})}
function rivLine(w){let n=rivClean(w.name),u=rivClean(w.url),t=rivClean(w.tur||w.extra);if(!n&&!u)return "";let p=n?[n,u,t]:[u,"",t];while(p.length&&!p[p.length-1])p.pop();return p.join(" | ")}
function rivSer(L){return L.map(rivLine).filter(Boolean).join("\n")}
function rivRows(f){let L=rivParse(state[f.id]),d=RIV_DRAFT[f.id];if(d&&rivSer(d)===rivSer(L))L=d;return L.length?L:[{name:"",url:"",tur:""}]}
function rivRowHtml(f,w,i,j){let n=i+1,q=E(JSON.stringify(f.id)),ph=(a,b)=>E(i?a:b),RD=typeof RVD!=="undefined"?RVD:null,filled=rivLine(w)!=="",
 inp=(c,cc,v,L,l,p,x)=>`<label class="rivCell ${cc}"><span class="rivL" aria-hidden="true">${L}</span><input class="control ${c}" type="text" autocomplete="off" aria-label="Rakip ${n}: ${l}" placeholder="${p}" value="${E(v)}" oninput="rivIn(${q},this)"${x||""}></label>`,
 tur=w.tur||"",ex=w.extra&&!w.tur?w.extra:"";
 return `<div class="rivRow" role="group" aria-label="Rakip ${n}">`+
  inp("rivName","rivCN",w.name,"Marka adı","marka adı",ph("Marka adı","Örn. Örnek Diş Kliniği"))+
  inp("rivUrl","rivCU",w.url,"Web sitesi","web sitesi",ph("https://…","Örn. https://www.ornekdis.com")," inputmode=\"url\"")+
  `<label class="rivCell rivCT"><span class="rivL" aria-hidden="true">Tür</span><select class="control rivTur" data-native aria-label="Rakip ${n}: tür" onchange="rivIn(${q},this)"><option value="">Tür seçin</option>${RIV_TUR.map(t=>`<option${t===tur?" selected":""}>${t}</option>`).join("")}${ex?`<option value="${E(ex)}" selected>${E(ex)}</option>`:""}</select></label>`+
  `<button type="button" class="rivDel" aria-label="Rakip ${n} satırını sil" title="Satırı sil" onclick="rivDel(${q},this)">×</button>`+
  (RD&&RD.on()&&filled&&j>=0?RD.row(j):"")+`</div>`}
function rivInput(f){let q=E(JSON.stringify(f.id)),RD=typeof RVD!=="undefined"?RVD:null,j=0,rows=rivRows(f);
 return `<div class="rivBox rvBox rvList">${RD&&RD.on()?RD.top():""}<div class="rivHead" aria-hidden="true"><span>Marka adı</span><span>Web sitesi</span><span>Tür</span><span></span></div><div class="rivList">${rows.map((w,i)=>rivRowHtml(f,w,i,rivLine(w)?j++:-1)).join("")}</div><button type="button" class="rivAdd" onclick="rivAdd(${q})">+ Rakip ekle</button>${RD?(RD.on()?RD.bottom():RD.note()):""}</div>`}
function rivBox(id){return document.querySelector('.field[data-field-id="'+id+'"] .rivBox')}
function rivRead(b){return [...b.querySelectorAll(".rivRow")].map(r=>{let t=r.querySelector(".rivTur").value;return {name:r.querySelector(".rivName").value,url:r.querySelector(".rivUrl").value,tur:RIV_TUR.includes(t)?t:"",extra:RIV_TUR.includes(t)?"":t}})}
function rivRule(f){let el=document.querySelector('.field[data-field-id="'+f.id+'"]');if(!el)return;let rb=el.querySelector(".rule"),r=rule(f);
 if(rb&&r)rb.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(f,r):E(r));else if(typeof refreshRule==="function")refreshRule(f)}
function rivSave(id,b){let RD=typeof RVD!=="undefined"?RVD:null,before=RD?RD.keys():[],L=rivRead(b),v=rivSer(L);RIV_DRAFT[id]=L;if(v)state[id]=v;else delete state[id];
 if(RD){let after=RD.keys();if(after.length===before.length&&after.some((k,i)=>k!==before[i]))RD.remap(before,after);RD.sync(b)}
 faAuto(id);save();renderRules();renderProgress();rivRule(FI[id])}
function rivIn(id,el){if(!requireProject()){refreshField(id);return}rivSave(id,el.closest(".rivBox"))}
function rivAdd(id){if(!requireProject())return;let b=rivBox(id);if(!b)return;let l=b.querySelector(".rivList"),n=l.children.length,t=document.createElement("template");
 t.innerHTML=rivRowHtml(FI[id],{name:"",url:"",tur:""},n,-1);l.appendChild(t.content.firstElementChild);RIV_DRAFT[id]=rivRead(b);l.lastElementChild.querySelector(".rivName").focus()}
function rivDel(id,btn){if(!requireProject())return;let b=btn.closest(".rivBox"),r=btn.closest(".rivRow"),rows=[...b.querySelectorAll(".rivRow")],i=rows.indexOf(r),RD=typeof RVD!=="undefined"?RVD:null,
 j=rows.slice(0,i).filter(x=>rivLine({name:x.querySelector(".rivName").value,url:x.querySelector(".rivUrl").value})).length,k=RD&&rivLine({name:r.querySelector(".rivName").value,url:r.querySelector(".rivUrl").value})?RD.keys()[j]:"";
 if(k&&RD.has(k)){if(!confirm("Bu rakibin girilmiş ayrıntıları (profil, fiyat, şube, reklam …) da silinsin mi?\nİptal: yalnız listeden çıkar, ayrıntılar “Listede adı bulunmayan kayıtlar” altında kalır."))k=""}
 if(rows.length>1)r.remove();else{r.querySelectorAll("input").forEach(x=>x.value="");r.querySelector(".rivTur").value=""}rivSave(id,b);if(k)RD.drop(k);refreshField(id);
 let nb=rivBox(id);if(nb){let L=nb.querySelectorAll(".rivRow"),t=L[Math.min(i,L.length-1)];(t?t.querySelector(".rivName"):nb.querySelector(".rivAdd")).focus()}}
