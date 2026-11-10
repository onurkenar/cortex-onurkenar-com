/* Renk Paleti ve kontrast denetimi (2026-11-10, kullanıcı isteği: "renk seçtiğim alanlarda kontrast uygunluğunu belirt,
   ana renk ve yardımcı renkleri seçtiğim alan aynı menü olsun ve uyarıları burada ver").
   Ortak Bilgiler › Marka Görünümü'ndeki renk kararları tek "Renk Paleti" kararında (alan tipi "palette", oc_palette) seçilir.
   Renkler yine kendi alan kimlikleriyle saklanır (brand_color_*); kuralları, prompt, proje dosyası ve dışa aktarımlar aynen.
   Üye alanlar sol menüden, ilerlemeden ve karar listelerinden düşer (navF); onlara giden bağlantılar paletteki satıra gider.
   Ölçüt WCAG 2.2: 1.4.3 (normal metin 4.5:1, büyük metin 3:1), 1.4.6 (AAA 7:1), 1.4.11 (arayüz bileşeni 3:1).
   Kaynak docs/v26/v26-palette.js → docs/v26/renk_paleti_ekle.py (ana betikte function one(f){ öncesine). */
const PAL_F=(DATA.fields||[]).find(f=>f.type==="palette");
const PAL_IDS=new Set(PAL_F?(PAL_F.palette||[]).flatMap(g=>g.ids):[]);
const PAL_HEX=/^#[0-9A-F]{6}$/i,PAL_WHITE="#FFFFFF",PAL_INK="#111111";
function palHex(id){let v=state[id];return PAL_HEX.test(v||"")?v.toUpperCase():""}
function palRgb(h){h=h.replace("#","");return[0,2,4].map(i=>parseInt(h.slice(i,i+2),16))}
function palLum(h){let[r,g,b]=palRgb(h).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return .2126*r+.7152*g+.0722*b}
function palRatio(a,b){let x=palLum(a),y=palLum(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05)}
function palFmt(r){return(Math.floor(r*100)/100).toFixed(2).replace(".",",")+":1"}
function palMix(h,t,k){let a=palRgb(h),b=palRgb(t);return"#"+a.map((x,i)=>Math.round(x+(b[i]-x)*k).toString(16).padStart(2,"0")).join("").toUpperCase()}
/* fg'yi siyaha ya da beyaza doğru en az kaydırarak bg üzerinde hedef orana ulaştırır */
function palFix(fg,bg,need){let to=palLum(bg)>.18?"#000000":PAL_WHITE;for(let k=.02;k<=1.0001;k+=.02){let c=palMix(fg,to,k);if(palRatio(c,bg)>=need+.02)return c}return""}
/* üzerindeki yazı için beyaz ya da koyu metinden hangisi daha iyi */
function palOn(bg){let ink=palHex("brand_color_dark")||PAL_INK,w=palRatio(PAL_WHITE,bg),d=palRatio(ink,bg);return w>=d?{c:PAL_WHITE,n:"beyaz yazı",r:w}:{c:ink,n:"koyu yazı",r:d}}
function palBg(){return palHex("brand_color_light")||PAL_WHITE}
function palLevel(r){return r>=7?"AAA":r>=4.5?"AA":r>=3?"Büyük metin":"Yetersiz"}
function palShown(id){let f=FI[id];return !!f&&shown(f)}
/* Denetlenen çiftler: {ids (satırlar), name, fg, bg, need, kind text|large|ui, soft, fix: {id?, c, txt}} */
function palChecks(){let L=[],bg=palBg(),bgN=palHex("brand_color_light")?"açık zemin":"beyaz zemin",dk=palHex("brand_color_dark");
 let add=(o)=>{o.r=palRatio(o.fg,o.bg);o.ok=o.r>=o.need;L.push(o)};
 if(dk)add({ids:["brand_color_dark","brand_color_light"],key:"text",name:"Koyu renk metin, "+bgN+" (ve tersi)",fg:dk,bg,need:4.5,kind:"text",fixId:"brand_color_dark"});
 let p=palHex("brand_color_primary");
 if(p){add({ids:["brand_color_primary"],key:"p-link",name:"Ana renk bağlantı / metin olarak "+bgN+"de",fg:p,bg,need:4.5,kind:"text",tone:"--color-primary-text"});
  let o=palOn(p);add({ids:["brand_color_primary"],key:"p-btn",name:"Ana renk buton, üzerinde "+o.n,fg:o.c,bg:p,need:4.5,kind:"text",btn:1,base:p})}
 let s=palHex("brand_color_secondary");
 if(s){let o=palOn(s);add({ids:["brand_color_secondary"],key:"s-on",name:"İkincil renk zemin, üzerinde "+o.n,fg:o.c,bg:s,need:4.5,kind:"text",btn:1,base:s});
  add({ids:["brand_color_secondary"],key:"s-ui",name:"İkincil renk ikon / grafik olarak "+bgN+"de",fg:s,bg,need:3,kind:"ui",soft:1})}
 let a=palHex("brand_color_accent");
 if(a){let o=palOn(a);add({ids:["brand_color_accent"],key:"a-btn",name:"Vurgu (CTA) butonu, üzerinde "+o.n,fg:o.c,bg:a,need:4.5,kind:"text",btn:1,base:a});
  add({ids:["brand_color_accent"],key:"a-ui",name:"Vurgu butonunun "+bgN+"den ayrışması",fg:a,bg,need:3,kind:"ui",soft:1})}
 let n=palHex("brand_color_neutral");
 if(n)add({ids:["brand_color_neutral"],key:"n-ui",name:"Nötr gri form alanı kenarlığı olarak "+bgN+"de",fg:n,bg,need:3,kind:"ui",soft:1,fixId:"brand_color_neutral",note:"Yalnız dekoratif çizgi ve pasif (devre dışı) alanda kullanılacaksa oran şartı yoktur."});
 [["brand_color_success","Başarı"],["brand_color_warning","Uyarı"],["brand_color_error","Hata"],["brand_color_info","Bilgi"]].forEach(([id,nm])=>{let c=palHex(id);if(!c||!palShown(id))return;
  add({ids:[id],key:id+"-t",name:nm+" rengi mesaj metni olarak "+bgN+"de",fg:c,bg,need:4.5,kind:"text",tone:"--color-"+id.split("_").pop()+"-text"});
  let o=palOn(c);add({ids:[id],key:id+"-b",name:nm+" rozeti, üzerinde "+o.n,fg:o.c,bg:c,need:4.5,kind:"text",btn:1,base:c})});
 L.forEach(x=>{if(x.ok)return;if(x.btn){let f=palFix(x.base,x.fg,x.need);x.fix=f?{c:f,txt:`buton / rozet zemininde ${f} tonu (${x.fg===PAL_WHITE?"beyaz":"koyu"} yazıyla ${palFmt(palRatio(x.fg,f))})`}:null}
  else{let f=palFix(x.fg,x.bg,x.need);if(f)x.fix={c:f,id:x.fixId,txt:x.fixId?`${f} (${palFmt(palRatio(f,x.bg))})`:`metin ve bağlantıda ${f} tonu (${palFmt(palRatio(f,x.bg))}${x.tone?", "+x.tone:""})`}}});
 return L}
function palState(x){return x.ok?"ok":x.soft?"note":x.kind==="text"&&x.r>=3?"warn":"fail"}
function palHas(){return [...PAL_IDS].some(id=>palShown(id)&&palHex(id))}
function palProblems(L){return L.filter(x=>!x.ok)}
function palRule(f){if(!palHas())return"";let L=palChecks(),bg=palBg(),parts=[];
 let ok=L.filter(x=>x.ok).map(x=>`${x.name} ${palFmt(x.r)} (${palLevel(x.r)})`),bad=palProblems(L).map(x=>`${x.name} ${palFmt(x.r)} — en az ${String(x.need).replace(".",",")}:1 gerekir${x.fix?"; "+x.fix.txt+" kullanılır":""}${x.note?" ("+x.note+")":""}`);
 parts.push(`Zemin ${bg}${palHex("brand_color_light")?"":" (açık renk seçilmediği için beyaz kabul edildi)"}`);
 if(ok.length)parts.push("Uygun çiftler: "+ok.join("; "));
 if(bad.length)parts.push("Düzeltilecek çiftler: "+bad.join("; "));
 if(!L.length)parts.push("Denetlenecek renk çifti oluşmadı");
 return String(f.rule||"").replaceAll("{contrast}",parts.join(". ")+".")}
/* --- Arayüz --- */
function palBadge(x){let st=palState(x),t={ok:"Uygun",warn:"Yalnız büyük metin",fail:"Yetersiz",note:"Kullanıma bağlı"}[st];
 return `<li class="palB ${st}"><span class="palSw" style="background:${x.bg};color:${x.fg}" aria-hidden="true">Aa</span><span class="palBT"><b>${E(x.name)}</b><span>${palFmt(x.r)} · ${x.ok?palLevel(x.r):t} <em>(gerekli ${String(x.need).replace(".",",")}:1)</em></span></span><span class="palBS" aria-hidden="true">${st==="ok"?"✓":st==="note"?"i":"!"}</span></li>`}
function palFixBtn(x){if(!x.fix)return"";return x.fix.id?`<button type="button" class="palFixB" onclick="palApply('${x.fix.id}','${x.fix.c}')"><span class="palDot" style="background:${x.fix.c}"></span>${E(x.fix.c)} tonunu uygula</button>`:`<button type="button" class="palFixB" data-v26="1" onclick="palCopy('${x.fix.c}',this)"><span class="palDot" style="background:${x.fix.c}"></span>${E(x.fix.c)} kopyala</button>`}
function palSum(L){let bad=palProblems(L),hard=bad.filter(x=>!x.soft),soft=bad.filter(x=>x.soft);
 if(!palHas())return `<div class="palSumBox"><b>Kontrast denetimi</b><span>Renkleri seçtikçe her rengin altında kontrast oranı, burada da düzeltilmesi gereken çiftler ve önerilen tonlar görünür.</span></div>`;
 if(!L.length)return `<div class="palSumBox"><b>Kontrast denetimi</b><span>Denetlenecek renk çifti henüz oluşmadı.</span></div>`;
 let li=x=>`<li class="${palState(x)}"><div><b>${E(x.name)}: ${palFmt(x.r)}</b><span>En az ${String(x.need).replace(".",",")}:1 gerekir.${x.fix?" Öneri: "+E(x.fix.txt)+".":" Bu çift için uygun ton bulunamadı; rengi değiştirin."}${x.note?" "+E(x.note):""}</span></div>${palFixBtn(x)}</li>`;
 return `<div class="palSumBox ${hard.length?"bad":soft.length?"soft":"good"}"><b>${hard.length?`${hard.length} renk çiftinde kontrast yetersiz`:soft.length?"Metin kontrastı uygun · kullanıma bağlı uyarılar var":"Bütün renk çiftleri WCAG 2.2 AA'ya uygun"}</b><span>${L.length} çift denetlendi · ${L.filter(x=>x.ok).length} uygun${hard.length?` · ${hard.length} düzeltilmeli`:""}${soft.length?` · ${soft.length} kullanıma bağlı`:""}${palHex("brand_color_light")?"":" · zemin beyaz kabul edildi"}</span>${bad.length?`<ul class="palProb">${hard.concat(soft).map(li).join("")}</ul>`:""}</div>`}
function palPreview(){let bg=palBg(),tx=palHex("brand_color_dark")||PAL_INK,p=palHex("brand_color_primary"),a=palHex("brand_color_accent")||p,s=palHex("brand_color_secondary"),n=palHex("brand_color_neutral")||"#D0D5DD";
 if(!p&&!a&&!s&&!palHex("brand_color_dark")&&!palHex("brand_color_light"))return"";
 let st=[["brand_color_success","Onaylandı"],["brand_color_warning","Bekliyor"],["brand_color_error","Hata"],["brand_color_info","Bilgi"]].filter(([id])=>palShown(id)&&palHex(id)).map(([id,t])=>{let c=palHex(id),o=palOn(c);return `<span class="palPvBadge" style="background:${c};color:${o.c}">${t}</span>`}).join("");
 let ao=a?palOn(a):null;
 return `<figure class="palPv" aria-label="Paletin örnek kartta görünümü"><div class="palPvCard" style="background:${bg};color:${tx};border-color:${n}"><span class="palPvKick" style="color:${s||tx}">ÖRNEK KART</span><b class="palPvH">Randevunuzu birkaç adımda alın</b><p>Metin rengi bu zeminde okunur; ${p?`<a style="color:${p}">ayrıntılı bilgi</a> bağlantısı ana renkle gösterilir.`:"bağlantı rengi için ana rengi seçin."}</p><div class="palPvRow">${a?`<span class="palPvBtn" style="background:${a};color:${ao.c}">Randevu al</span>`:""}<span class="palPvIn" style="border-color:${n}">Ad Soyad</span>${st}</div></div><figcaption>Önizleme yalnız fikir verir; kesin sonuç yukarıdaki oranlardır.</figcaption></figure>`}
function palTable(L){if(!L.length)return"";return `<details class="palTbl"><summary>Bütün renk çiftlerinin kontrast tablosu (${L.length})</summary><div class="palTblW"><table><thead><tr><th scope="col">Kullanım</th><th scope="col">Örnek</th><th scope="col">Oran</th><th scope="col">Normal metin (4,5)</th><th scope="col">Büyük metin / arayüz (3)</th><th scope="col">AAA (7)</th></tr></thead><tbody>${L.map(x=>`<tr><th scope="row">${E(x.name)}</th><td><span class="palSw" style="background:${x.bg};color:${x.fg}">Aa</span> <small>${x.fg} / ${x.bg}</small></td><td><b>${palFmt(x.r)}</b></td>${[4.5,3,7].map(t=>`<td class="${x.r>=t?"y":"n"}">${x.r>=t?"✓ Geçer":"✗ Geçmez"}</td>`).join("")}</tr>`).join("")}</tbody></table></div></details>`}
function palRowChk(id,L){let m=L.filter(x=>x.ids.includes(id));if(!palHex(id))return `<p class="palEmpty">Renk seçince kontrast oranı burada görünür.</p>`;if(!m.length)return `<p class="palEmpty">${id==="brand_color_light"?"Koyu renk seçilince metin kontrastı burada denetlenir.":"Bu renk için denetlenecek çift yok."}</p>`;return `<ul class="palBs">${m.map(palBadge).join("")}</ul>`}
function palInput(f){let L=palChecks(),gs=(f.palette||[]).map(g=>{let ids=g.ids.filter(palShown);let rows=ids.map(id=>{let m=FI[id];return `<div class="palRow" id="pal-${id}" data-pal-id="${id}"><div class="palHd"><b>${E(m.label)}</b><small>${E(m.explanation||"")}</small></div>${colorInput(m)}<div class="palChk" data-pal-chk="${id}" aria-live="polite">${palRowChk(id,L)}</div></div>`}).join("");
  if(!ids.length&&g.gate)return `<section class="palGrp"><h3>${E(g.title)}</h3><p class="palGrpD">${E(g.gate.text)} <button type="button" class="palLink" data-v26="1" onclick="goToField('${FI[g.gate.field].section}','${g.gate.field}')">${E(g.gate.link)} →</button></p></section>`;
  return ids.length?`<section class="palGrp"><h3>${E(g.title)}</h3>${g.desc?`<p class="palGrpD">${E(g.desc)}</p>`:""}<div class="palRows">${rows}</div></section>`:""}).join("");
 return `<div class="palBox"><div class="palTop"><div class="palSum" aria-live="polite">${palSum(L)}</div><div class="palPvSlot">${palPreview()}</div></div>${gs}<div class="palTblSlot">${palTable(L)}</div><p class="palNote">Ölçüt WCAG 2.2: normal metin en az 4,5:1, büyük metin (24 px ya da 18,66 px kalın) ve arayüz bileşenleri (ikon, form kenarlığı, odak çerçevesi) en az 3:1, AAA düzeyi 7:1. Logo ve dekoratif öğeler oran şartından muaftır; durum hiçbir zaman yalnız renkle anlatılmaz.</p></div>`}
function palUpdate(){let fe=[...document.querySelectorAll('.field[data-field-id="'+PAL_F.id+'"]')];if(!fe.length)return;let L=palChecks();
 fe.forEach(el=>{let q=s=>el.querySelector(s);if(q(".palSum"))q(".palSum").innerHTML=palSum(L);if(q(".palPvSlot"))q(".palPvSlot").innerHTML=palPreview();if(q(".palTblSlot")){let o=q(".palTbl")&&q(".palTbl").open;q(".palTblSlot").innerHTML=palTable(L);if(o&&q(".palTbl"))q(".palTbl").open=true}
  el.querySelectorAll("[data-pal-chk]").forEach(c=>c.innerHTML=palRowChk(c.dataset.palChk,L));
  let r=rule(PAL_F),b=el.querySelector(".rule");if(!r){if(b)b.remove()}else{if(!b){b=document.createElement("div");b.className="rule";(el.querySelector(".v26Aside")||el).appendChild(b)}b.innerHTML="<b>BU SEÇİMDEN OLUŞAN KURAL</b>"+(typeof ruleAgText==="function"?ruleAgText(PAL_F,r):E(r))}})}
function palApply(id,c){if(!requireProject())return;state[id]=c;faAuto(id);save();renderRules();renderProgress();refreshField(PAL_F.id);let i=document.querySelector("#pal-"+id+" .control");if(i)i.focus({preventScroll:true})}
function palCopy(c,b){let done=()=>{let t=b.lastChild.textContent;b.lastChild.textContent=" kopyalandı";setTimeout(()=>b.lastChild.textContent=t,1400)};try{navigator.clipboard.writeText(c).then(done,()=>prompt("Renk kodu:",c))}catch(e){prompt("Renk kodu:",c)}}
if(PAL_F){
 const _palNavF=navF;navF=function(f){return _palNavF(f)&&!(f&&PAL_IDS.has(f.id))};
 const _palGo=goToField;goToField=function(sec,id){if(PAL_IDS.has(id)){_palGo(PAL_F.section,PAL_F.id);setTimeout(()=>{let r=document.getElementById("pal-"+id);if(!r)return;r.scrollIntoView({block:"center"});r.classList.remove("attn");void r.offsetWidth;r.classList.add("attn");let i=r.querySelector(".control");if(i)i.focus({preventScroll:true})},40);return}return _palGo.apply(this,arguments)};
 const _palSet=setColor;setColor=function(id){let r=_palSet.apply(this,arguments);if(PAL_IDS.has(id))try{palUpdate()}catch(e){console.error("palette",e)}return r};
}
