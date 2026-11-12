/* Claude talimat dosyası (2026-11-08, kullanıcı isteği: "prompt çok uzun; md dosyası olarak indir, kullanıcının verdiği hazır bir promptla bu dosyadaki talimatları fazlar hâlinde yaptır").
   Üst şeritteki "Claude Promptu" düğmesi panel açar: CLAUDE-TALIMATLARI.md indir, kısa başlatma promptunu kopyala, tam promptu tek parça kopyala.
   master.value (Claude promptu) değişmez; dosya aynı kurallardan fazlara bölünerek üretilir. */
(()=>{
const PR_FILE="CLAUDE-TALIMATLARI.md",PR_LOG="CLAUDE-ILERLEME.md",
 PR_PH=[
  {t:"Proje temeli ve mimari",g:["Başlangıç","Teknik Mimari","Sunucu & Altyapı"],a:"Projenin kapsamını, teknoloji yığınını, veri modelini, panel ve portal mimarisini, ortamları ve altyapıyı kararlara göre kurmak ya da hizalamak.",pz:true},
  {t:"Tasarım ve arayüz",g:["Tasarım & Arayüz"],a:"Kurumsal kimliği, tasarım stilini, düzeni, tema ve hareket dilini, erişilebilirlik temelini arayüze uygulamak.",ds:true},
  {t:"İçerik ve yönetim",g:["İçerik & Yönetim"],a:"İçerik yönetimi, medya, çok dillilik ve içerik yapısını kurmak."},
  {t:"SEO ve görünürlük",g:["SEO & Görünürlük"],a:"Teknik SEO, yapısal veri, GEO / AI arama ve yerel görünürlük kurallarını uygulamak."},
  {t:"Güvenlik ve gizlilik",g:["Güvenlik & Gizlilik"],a:"Kimlik doğrulama, yetkilendirme, veri koruma, KVKK / GDPR ve güvenlik başlıklarını denetlemek ve eksikleri kapatmak."},
  {t:"Performans, test ve geliştirme süreci",g:["Performans & Test","Geliştirme Süreci"],a:"Performans bütçesini, test stratejisini, kod kalitesi ve geliştirme sürecini kurmak."},
  {t:"Yayın ve operasyon",g:["Yayın & Operasyon"],a:"Yayın, izleme, yedekleme ve operasyon kurallarını uygulamak."}],
 PR_DONE="Bu fazdaki kurallar uygulandı ya da uygulanamayanlar gerekçesiyle raporlandı; ilgili testler ve kontroller çalıştırıldı; önceki fazlarda çalışan özellikler bozulmadı; kullanıcı onayı alındı.",
 PR_CT=["Kod yazmadan önce repository'yi ve mevcut mimariyi incele.","Bu dosyadaki kararları bağlayıcı kabul et.","Çalışan özellikleri ve onaylanmış arayüzü izinsiz kaldırma.","En küçük güvenli değişiklik setini uygula.","Güvenlik, erişilebilirlik, SEO / GEO / AIO, performans ve veri bütünlüğünü kontrol et.","Test, type-check, lint ve build kontrollerini çalıştır.","Sonuçları ve açık riskleri raporla."];
const n=L=>L.map((x,i)=>`${i+1}. ${x}`).join("\n"),day=()=>new Date().toLocaleDateString("sv-SE"),pname=()=>String(state.project_name||"").trim()||"Proje";
function groups(area){return S.filter(s=>AREA(s)===area).map(s=>({s,rs:F.filter(f=>f.section===s.id&&isset(f)&&shown(f)).map(ruleAg).filter(Boolean)})).filter(g=>g.rs.length)}
function secMd(g){return `### ${g.s.code} — ${g.s.name}\n${n(g.rs)}`}
function plain(t){return String(t||"").replace(/^\s+/,"").replace(/\s+$/,"")}
function phases(){let P=groups("project"),used=new Set(),out=[];PR_PH.forEach(p=>{let G=P.filter(g=>p.g.includes(g.s.group));G.forEach(g=>used.add(g.s.id));let ds=p.ds&&typeof dsActive==="function"&&dsActive(),pz=p.pz&&typeof pzActive==="function"&&pzActive();if(G.length||ds||pz)out.push({t:p.t,a:p.a,G,ds,pz})});
 let rest=P.filter(g=>!used.has(g.s.id));if(rest.length)out.push({t:"Diğer proje kararları",a:"Yukarıdaki fazlara girmeyen proje kararlarını uygulamak.",G:rest});
 let M=typeof mkRuleGroups==="function"?mkRuleGroups():[];if(M.length)out.push({t:"Pazarlama ve içerik altyapısı",a:"Sitede karşılığı olan pazarlama kurallarını (ölçüm olayları, blog alanları, paylaşım bağlantıları, formlar, CTA'lar) uygulamak; içerik planı ve reklam işleri bu fazın dışındadır.",G:M});
 return out}
function dsMd(){let c=dsConfig();return `### Tasarım şartnamesi (tasarım yapılandırması 2.0)\n${n(dsSpecItems(c))}\n\n#### Bileşen kuralları\n${n(dsCompRules(c))}\n\n#### Responsive kurallar\n${n(dsRespRules(c))}\n\n#### UI/UX uygulama yönergeleri\n${n(dsGuide(c))}\n\n#### CSS tasarım token'ları\nProje stil dosyasının başına eklenir; değerler değişirse önce bu yapılandırma güncellenir.\n\n\`\`\`css\n${dsTokensCss(c)}\n\`\`\`\n\n#### Tasarım yapılandırması (JSON)\n\`\`\`json\n${JSON.stringify(c,null,2)}\n\`\`\``}
function prStats(){let ph=phases(),r=ph.reduce((a,p)=>a+p.G.reduce((b,g)=>b+g.rs.length,0),0)+groups("common").reduce((a,g)=>a+g.rs.length,0);return {ph,r}}
function prMd(){renderRules();let {ph,r}=prStats(),C=groups("common"),last=ph.length+1,custom=state.project_type==="Other"&&state.project_type_other?`\n\nÖzel proje türü açıklaması: ${state.project_type_other}`:"",ag=plain(typeof agPrompt==="function"?agPrompt():""),mc=plain(typeof mcPrompt==="function"?mcPrompt():"");
 let md=`# ${pname()} — Claude proje talimatları\n\n> Cortex Configurator ile üretildi · ${day()} · ${ph.length+2} faz · ${r} kural.\n> Bu dosya projenin bağlayıcı talimatıdır (source of truth). Seçilmemiş alternatif teknoloji veya servisleri açık onay olmadan ekleme.\n\n## Nasıl çalışılır\n${n([
  "Önce bu bölümü, İçindekiler'i ve Genel kuralları oku. Dosya büyük olabilir: her fazda yalnız o fazın bölümünü ve gerekirse Ek A'yı oku (satır numaraları İçindekiler'de); Ek B'yi (ajanlar, skill'ler, kurullar) yalnız iş devrederken ya da ilgili ajanı ararken oku.",
  "Fazları sırayla uygula; bir faz bitmeden sonrakine geçme.",
  "Her fazın başında o fazın kurallarını mevcut kodla karşılaştır ve yapılacakları kısa bir plan olarak yaz.",
  `Her fazın sonunda aşağıdaki "Faz raporu" biçimiyle rapor ver ve kullanıcının onayını bekle. Kullanıcı açıkça onay vermeden sonraki faza geçme.`,
  `İlerlemeyi \`${PR_LOG}\` dosyasına yaz: tamamlanan fazlar, uygulanan ve uygulanamayan kurallar, açık işler, kullanıcı kararları. Yeni bir oturumda önce o dosyayı ve bu dosyayı oku, kaldığın fazdan devam et.`,
  "Ek A'daki Ortak Bilgiler (marka, iletişim, renkler, hesaplar…) bütün fazlarda kullanılır; bu değerleri uydurma, değiştirme.",
  "Güvenlik ve erişilebilirlik kuralları ilk fazdan itibaren göz önünde tutulur; kendi fazlarında ayrıca denetlenir.",
  "Bir kural uygulanamıyorsa, mevcut kodla ya da başka bir kuralla çelişiyorsa tahmin yürütme; raporda belirt ve kullanıcıya sor.",
  "Kuralların sonundaki “(Sorumlu ajan: …)” işi yürütecek alt ajanı gösterir; ajan yapısı Ek B'dedir. Alt ajanlar birbirini çağıramaz, işi ana asistan dağıtır."])}\n\n### Faz raporu biçimi\n- Yapılanlar (dosyalar ve değişiklikler)\n- Uygulanan kurallar (numaralarıyla) ve uygulanamayanlar (gerekçesiyle)\n- Çalıştırılan testler, kontroller ve sonuçları\n- Açık riskler ve kullanıcı kararı bekleyen konular\n- Sonraki faz ve kısa planı\n\n## Genel kurallar (her fazda geçerli)\n${n(R)}\n\n### Çalışma ilkeleri\n${n(PR_CT)}${custom}\n\n## Faz listesi\n| Faz | Kapsam | Kural |\n|---|---|---|\n| 0 | İnceleme ve plan | — |\n${ph.map((p,i)=>`| ${i+1} | ${p.t} | ${p.G.reduce((a,g)=>a+g.rs.length,0)}${p.ds?" + tasarım şartnamesi":""}${p.pz?" + panel mimarisi":""} |`).join("\n")}\n| ${last} | Doğrulama ve teslim | — |\n\n## Faz 0 — İnceleme ve plan\n**Amaç:** Kod yazmadan önce repository'yi ve mevcut mimariyi incelemek; bu dosyadaki kararları mevcut durumla karşılaştırmak.\n\n${n(["Proje yapısını, kullanılan teknolojileri ve mevcut özellikleri çıkar.","Her fazın kurallarından hangilerinin zaten karşılandığını, hangilerinin eksik ya da mevcut kodla çelişkili olduğunu listele.","Fazların sırasına göre uygulama planını, tahmini kapsamı ve riskleri yaz.",`\`${PR_LOG}\` dosyasını oluştur.`])}\n\n**Bitti ölçütü:** Boşluk listesi ve plan kullanıcıya sunuldu; kod değişikliği yapılmadı.\n`;
 ph.forEach((p,i)=>{md+=`\n## Faz ${i+1} — ${p.t}\n**Amaç:** ${p.a}\n\n**Kapsam:** ${p.G.map(g=>`${g.s.code} ${g.s.name}`).join(" · ")||"Tasarım şartnamesi"}\n\n${p.G.map(secMd).join("\n\n")}${p.ds?(p.G.length?"\n\n":"")+dsMd():""}${p.pz?"\n\n"+pzMd():""}\n\n**Bitti ölçütü:** ${PR_DONE}\n`});
 md+=`\n## Faz ${last} — Doğrulama ve teslim\n${n(["Bütün fazların kurallarını baştan kontrol et; uygulanmamış ya da yarım kalan kural kalmadığını doğrula.","Test, type-check, lint ve build kontrollerini çalıştır.","Erişilebilirlik (klavye, odak, kontrast, ekran okuyucu), güvenlik, SEO / GEO ve performans kontrollerini yap.",`Son raporu ver: tamamlananlar, uygulanamayanlar ve gerekçeleri, açık riskler, sonraki adımlar; \`${PR_LOG}\`'yu güncelle.`])}\n\n**Bitti ölçütü:** Bütün kontroller geçti ya da kalan sorunlar gerekçesiyle raporlandı; kullanıcı teslimi onayladı.\n`;
 md+=`\n## Ek A — Ortak Bilgiler (bütün fazlarda kullanılan referans veriler)\n${C.length?C.map(secMd).join("\n\n"):"Ortak Bilgiler'de karar verilmedi."}\n`;
 md+=`\n## Ek B — Ajan yapısı, skill'ler, kurullar ve bağlantılar\n${ag||mc?[ag,mc].filter(Boolean).join("\n\n"):"Projeye ajan, skill ya da bağlantı eklenmedi."}\n`;
 let L=md.split("\n"),k=L.indexOf("## Nasıl çalışılır"),H=L.slice(0,k),B=L.slice(k),idx=B.map((l,i)=>l.startsWith("## ")?i:-1).filter(i=>i>=0),rows=idx.map((i,j)=>[B[i].slice(3),i,B.slice(i,j+1<idx.length?idx[j+1]:B.length).join("\n").length]),T=["## İçindekiler","","| Bölüm | Satır | Boyut |","|---|---|---|"].concat(rows.map(r=>"")),off=H.length+T.length+1;
 T=T.slice(0,4).concat(rows.map(([t,i,b])=>`| ${t.replace(/\|/g,"/")} | ${off+i} | ${Math.max(1,Math.round(b/1024))} KB |`),[""]);off=H.length+T.length+1;T=T.slice(0,4).concat(rows.map(([t,i,b])=>`| ${t.replace(/\|/g,"/")} | ${off+i} | ${Math.max(1,Math.round(b/1024))} KB |`),[""]);
 return H.concat(T,B).join("\n")}
function prStart(){return `Proje kök dizinindeki (ya da bu sohbete eklediğim) ${PR_FILE} dosyasının başındaki "Nasıl çalışılır", "İçindekiler" ve "Genel kurallar" bölümlerini oku. Bu dosya projenin bağlayıcı talimatıdır; başka bir talimatla çelişirse dosya geçerlidir. Dosya büyük olabilir: her fazda yalnız o fazın bölümünü ve gerekirse Ek A'yı oku.

Çalışma şekli:
1. Dosyadaki "Nasıl çalışılır" bölümüne uy ve Faz 0'dan başla.
2. Fazları sırayla yap; bir fazı bitirmeden sonrakine geçme.
3. Her fazın sonunda dosyadaki "Faz raporu" biçimiyle rapor ver ve onayımı bekle. Ben "devam" demeden sonraki faza geçme.
4. İlerlemeyi ${PR_LOG} dosyasına yaz.
5. Yeni bir oturumda "kaldığın yerden devam et" dersem önce bu iki dosyayı oku, sonra sıradaki fazdan devam et.

Şimdi Faz 0'ı (inceleme ve plan) yap; kod yazmadan önce planını sun.`}
function prHtml(){let {ph,r}=prStats(),w=typeof window.v26DlWarn==="function"?window.v26DlWarn():"",kb=Math.max(1,Math.round(new Blob([prMd()]).size/1024));
 return `<div class="exHead"><b id="prMenuT">Claude talimatları</b><button type="button" class="exX" onclick="prClose(true)" aria-label="Kapat">✕</button></div><p class="exIntro">Tam prompt uzun olduğu için iki parçaya ayrılır: kararlarınızı fazlara bölen bir talimat dosyası ve Claude'a o dosyayı fazlar hâlinde uygulatan kısa bir başlatma promptu.</p>${w}
 <ol class="prSteps"><li><b>Talimat dosyasını indirin</b><span>${ph.length+2} faz (inceleme, ${ph.length} uygulama fazı, doğrulama) · ${r} kural · yaklaşık ${kb} KB. Claude Code'da proje köküne koyun; claude.ai'da projeye ya da sohbete dosya olarak ekleyin.</span><button type="button" class="btn dark" data-pr="md">${PR_FILE} indir</button></li>
 <li><b>Başlatma promptunu Claude'a yapıştırın</b><span>Claude dosyayı okur, Faz 0'da planını sunar; her fazın sonunda rapor verir ve sizin “devam” onayınızı bekler. İlerlemeyi ${PR_LOG} dosyasına yazar; yeni oturumda “kaldığın yerden devam et” demeniz yeterli.</span><textarea class="prTa" readonly rows="9" aria-label="Başlatma promptu">${E(prStart())}</textarea><button type="button" class="btn" data-pr="start">Başlatma promptunu kopyala</button></li></ol>
 <p class="prFull">Eski yöntem: <button type="button" class="linkBtn" data-pr="full">Tam promptu tek parça kopyala</button> (Proje Kuralları sayfasındaki metin; fazlara bölünmez).</p>`}
function prPlace(m){let r=copyMaster.getBoundingClientRect(),w=m.offsetWidth;m.style.top=Math.round(r.bottom+8)+"px";m.style.left=Math.round(Math.max(12,Math.min(r.right-w,innerWidth-w-12)))+"px"}
function prClose(f){let m=document.getElementById("prMenu");if(m)m.hidden=true;copyMaster.setAttribute("aria-expanded","false");if(f)copyMaster.focus()}
function prToggle(){let m=document.getElementById("prMenu");if(m&&!m.hidden){prClose(true);return}try{exClose()}catch(e){}if(!m){m=document.createElement("div");m.id="prMenu";m.className="exMenu prMenu";m.setAttribute("role","dialog");m.setAttribute("aria-labelledby","prMenuT");document.body.appendChild(m);
  document.addEventListener("mousedown",e=>{let x=document.getElementById("prMenu");if(x&&!x.hidden&&!x.contains(e.target)&&!copyMaster.contains(e.target))prClose()});
  document.addEventListener("keydown",e=>{let x=document.getElementById("prMenu");if(e.key==="Escape"&&x&&!x.hidden)prClose(true)});
  addEventListener("resize",()=>{let x=document.getElementById("prMenu");if(x&&!x.hidden)prPlace(x)});
  m.addEventListener("click",e=>{let b=e.target.closest("[data-pr]");if(!b)return;let k=b.dataset.pr;if(k==="md")mkSave(prMd(),PR_FILE,"text/markdown");else prCopy(k==="start"?prStart():(renderRules(),master.value),b)})}
 m.innerHTML=prHtml();m.hidden=false;prPlace(m);copyMaster.setAttribute("aria-expanded","true");let b=m.querySelector("[data-pr]");if(b)b.focus()}
async function prCopy(t,b){let o=b.textContent,ok=true;try{await navigator.clipboard.writeText(t)}catch(e){ok=false}b.textContent=ok?"Kopyalandı ✓":"Kopyalanamadı — metni seçip kopyalayın";if(!ok){let ta=b.parentNode.querySelector(".prTa");if(ta){ta.focus();ta.select()}}setTimeout(()=>b.textContent=o,ok?1400:3500)}
window.prMd=prMd;window.prStart=prStart;window.prToggle=prToggle;window.prClose=prClose;
copyMaster.onclick=prToggle;copyMaster.textContent="Claude Promptu";copyMaster.setAttribute("aria-haspopup","dialog");copyMaster.setAttribute("aria-expanded","false");copyMaster.setAttribute("aria-controls","prMenu");copyMaster.title="Talimat dosyasını (.md) indir, başlatma promptunu kopyala";
})();
