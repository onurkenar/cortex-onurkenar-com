/* Hazır Prompt Kütüphanesi — hazır kategoriler ve modüller (2026-11-08).
   Kaynak adresleri 2026-11-08'de açılarak doğrulandı (HTTP 200). Yeni hazır modül: PL_BUILTIN'e ekle, id benzersiz ve [a-z0-9-] olsun. */
const PL_CATS0=[
 {id:"kvkk",name:"KVKK / GDPR",desc:"Kişisel verilerin korunması, rıza, başvuru, saklama ve imha."},
 {id:"a11y",name:"Erişilebilirlik",desc:"WCAG 2.2 AA, klavye, ekran okuyucu, formlar ve etkileşimli bileşenler."},
 {id:"guvenlik",name:"Güvenlik",desc:"Kimlik doğrulama, yetkilendirme, girdi doğrulama, gizli anahtarlar."},
 {id:"performans",name:"Performans",desc:"Core Web Vitals, önbellek, görsel ve betik optimizasyonu."},
 {id:"seo",name:"SEO & GEO",desc:"Teknik SEO, yapısal veri, AI arama görünürlüğü."},
 {id:"odeme",name:"Ödeme",desc:"Ödeme sağlayıcı entegrasyonu, 3DS, iade, mutabakat."},
 {id:"kimlik",name:"Kimlik & Üyelik",desc:"Kayıt, giriş, oturum, şifre sıfırlama, çok faktörlü doğrulama."},
 {id:"arayuz",name:"Arayüz Bileşenleri",desc:"Tekrar kullanılabilir bileşen ve sayfa kalıpları."},
 {id:"entegrasyon",name:"Entegrasyonlar",desc:"CRM, e-posta, analitik ve üçüncü taraf servisler."},
 {id:"test",name:"Test & Kalite",desc:"Birim, entegrasyon, uçtan uca test ve kalite kapıları."}
];
const PL_SVG=(w,h,body)=>"data:image/svg+xml;charset=utf-8,"+encodeURIComponent(`<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" font-family="Urbanist, Arial, sans-serif"><rect width="${w}" height="${h}" fill="#f4f5f7"/>${body}</svg>`);
const PL_IMG={
 banner:PL_SVG(800,500,`<rect x="40" y="30" width="720" height="44" rx="8" fill="#fff" stroke="#d9dde2"/><rect x="60" y="45" width="120" height="14" rx="4" fill="#c9ced6"/><rect x="40" y="96" width="720" height="150" rx="10" fill="#e6e9ee"/><rect x="40" y="262" width="350" height="70" rx="10" fill="#e6e9ee"/><rect x="410" y="262" width="350" height="70" rx="10" fill="#e6e9ee"/><rect x="64" y="352" width="712" height="128" rx="14" fill="#fff" stroke="#1f2937" stroke-width="2"/><circle cx="32" cy="466" r="18" fill="#1f2937"/><circle cx="26" cy="461" r="2.6" fill="#fff"/><circle cx="36" cy="470" r="2.2" fill="#fff"/><circle cx="37" cy="458" r="1.8" fill="#fff"/><text x="32" y="496" font-size="10" fill="#2453d6" text-anchor="middle">sol alt ikon</text><text x="88" y="384" font-size="18" font-weight="700" fill="#111">Çerez tercihleriniz</text><text x="88" y="410" font-size="13" fill="#4b5563">Zorunlu çerezler dışındaki çerezleri yalnız onay verirseniz kullanırız. Çerez Politikası · Aydınlatma Metni</text>${["Tümünü Kabul Et","Tümünü Reddet","Tercihleri Yönet"].map((b,i)=>`<rect x="${88+i*216}" y="428" width="200" height="38" rx="19" fill="#1f2937"/><text x="${188+i*216}" y="452" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">${b}</text>`).join("")}<text x="400" y="342" font-size="12" fill="#2453d6" text-anchor="middle">Üç düğme aynı boyut, renk ve ağırlıkta, aynı katmanda</text>`),
 prefs:PL_SVG(800,500,`<rect width="800" height="500" fill="#9aa1ab"/><rect x="150" y="40" width="500" height="420" rx="16" fill="#fff"/><text x="180" y="82" font-size="20" font-weight="700" fill="#111">Çerez tercihleri</text><text x="620" y="80" font-size="20" fill="#4b5563" text-anchor="middle">×</text>${[["Zorunlu","Oturum, güvenlik, onay kaydı · kapatılamaz",1,1],["İşlevsel","Sohbet aracı, harita",0,0],["Analitik","Ziyaret istatistikleri · Sağlayıcı: GA4",0,0],["Pazarlama","Reklam ölçümü · Sağlayıcı: Meta, Google Ads",0,0]].map((r,i)=>{let y=110+i*68;return `<rect x="180" y="${y}" width="440" height="56" rx="10" fill="#f7f8fa" stroke="#e1e4e8"/><text x="198" y="${y+24}" font-size="15" font-weight="700" fill="#111">${r[0]}</text><text x="198" y="${y+43}" font-size="12" fill="#4b5563">${r[1]}</text><rect x="552" y="${y+16}" width="48" height="24" rx="12" fill="${r[2]?"#9ca3af":"#d1d5db"}"/><circle cx="${r[2]?588:564}" cy="${y+28}" r="9" fill="#fff"/>${r[3]?`<text x="576" y="${y+54}" font-size="10" fill="#6b7280" text-anchor="middle">her zaman açık</text>`:""}`}).join("")}${["Tümünü Kabul Et","Tümünü Reddet","Seçimi Kaydet"].map((b,i)=>`<rect x="${180+i*152}" y="398" width="136" height="38" rx="19" fill="#1f2937"/><text x="${248+i*152}" y="422" font-size="13" font-weight="700" fill="#fff" text-anchor="middle">${b}</text>`).join("")}`),
 form:PL_SVG(800,560,`<rect x="160" y="24" width="480" height="512" rx="16" fill="#fff" stroke="#d9dde2"/><text x="190" y="66" font-size="20" font-weight="700" fill="#111">Teklif isteyin</text>${[["Ad Soyad *",92],["E-posta *",162],["Mesajınız *",232]].map(r=>`<text x="190" y="${r[1]}" font-size="13" font-weight="700" fill="#1f2937">${r[0]}</text><rect x="190" y="${r[1]+8}" width="420" height="${r[0].startsWith("Mesaj")?70:38}" rx="8" fill="#fff" stroke="#9ca3af"/>`).join("")}<rect x="190" y="332" width="420" height="58" rx="8" fill="#f1f5ff"/><text x="204" y="354" font-size="12" fill="#1f2937">Kişisel verileriniz teklif hazırlamak amacıyla işlenir.</text><text x="204" y="374" font-size="12" fill="#2453d6" text-decoration="underline">Aydınlatma Metni'nin tamamı</text><rect x="190" y="406" width="20" height="20" rx="4" fill="#fff" stroke="#4b5563" stroke-width="2"/><text x="220" y="421" font-size="12" fill="#1f2937">Kampanya e-postaları almak istiyorum (isteğe bağlı)</text><rect x="190" y="440" width="20" height="20" rx="4" fill="#fff" stroke="#4b5563" stroke-width="2"/><text x="220" y="455" font-size="12" fill="#1f2937">SMS ile bilgilendirilmek istiyorum (isteğe bağlı)</text><rect x="190" y="480" width="160" height="40" rx="20" fill="#1f2937"/><text x="270" y="505" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">Gönder</text><text x="660" y="370" font-size="12" fill="#2453d6">← aydınlatma: bilgi, onay kutusu değil</text><text x="660" y="440" font-size="12" fill="#2453d6">← rıza: amaç başına, ön işaretsiz</text>`),
 dsar:PL_SVG(900,300,`${[["Başvuru","form · hesap · e-posta"],["Kimlik doğrulama","orantılı yöntem"],["Kayıt ve süre","no + son tarih (30 gün)"],["İnceleme","envanter + saklama kuralı"],["Yanıt","dışa aktarım · silme · ret"]].map((r,i)=>{let x=20+i*176;return `<rect x="${x}" y="90" width="150" height="90" rx="12" fill="#fff" stroke="#1f2937" stroke-width="2"/><text x="${x+75}" y="128" font-size="15" font-weight="700" fill="#111" text-anchor="middle">${r[0]}</text><text x="${x+75}" y="152" font-size="11" fill="#4b5563" text-anchor="middle">${r[1]}</text>${i<4?`<path d="M${x+152} 135h20" stroke="#1f2937" stroke-width="2"/><path d="M${x+166} 129l7 6-7 6" fill="none" stroke="#1f2937" stroke-width="2"/>`:""}`}).join("")}<rect x="20" y="214" width="854" height="44" rx="10" fill="#eef2ff" stroke="#c7d2fe"/><text x="447" y="241" font-size="13" fill="#1d45b8" text-anchor="middle">Her adım değiştirilemez denetim günlüğüne yazılır · son 7 günde panel uyarısı</text><text x="447" y="56" font-size="18" font-weight="700" fill="#111" text-anchor="middle">İlgili kişi başvuru akışı</text>`),
 retention:PL_SVG(800,360,`<text x="40" y="48" font-size="18" font-weight="700" fill="#111">Saklama politikası → periyodik imha işi</text><rect x="40" y="70" width="720" height="40" rx="8" fill="#1f2937"/>${["Veri kategorisi","Hukuki sebep","Süre","Yöntem"].map((h,i)=>`<text x="${60+i*180}" y="96" font-size="13" font-weight="700" fill="#fff">${h}</text>`).join("")}${[["İletişim formu","Meşru menfaat","2 yıl","Silme"],["Sipariş / fatura","Kanuni yükümlülük","10 yıl","Arşiv → silme"],["Uygulama logu","Meşru menfaat","90 gün","Silme"],["Pazarlama izni","Açık rıza","Geri alınana dek","Anonimleştirme"]].map((r,j)=>`<rect x="40" y="${114+j*44}" width="720" height="40" rx="6" fill="${j%2?"#fff":"#f9fafb"}" stroke="#e5e7eb"/>${r.map((c,i)=>`<text x="${60+i*180}" y="${139+j*44}" font-size="13" fill="#1f2937">${c}</text>`).join("")}`).join("")}<text x="40" y="320" font-size="12" fill="#2453d6">Süreler örnektir; projenin hukuki değerlendirmesine göre doldurulur. İmha işi her çalışmada tutanak yazar.</text>`)
};
const PL_D="2026-11-08";
/* KVKK modülünün promptu docs/v26/prompt-kutuphanesi/kvkk-gdpr-cerez.md'den gelir (prompt_kutuphanesi_ekle.py JSON olarak yazar). Kabul kriterleri promptun "17. Kabul Kriterleri" maddeleri, resmî kaynaklar "9." bölümündeki adreslerdir — tek kaynak. */
const PL_KVKK_PROMPT=/*PL_FILE:kvkk-gdpr-cerez.md*/"";
/* Erişilebilirlik modülü: master prompt, referans uygulamanın işleyiş dokümanı (onurkenar.com) ve 16 referans görsel (WebP; ad, alt metin dokümandan, açıklama dokümandaki bölümden) — betik yazar. */
const PL_A11Y_PROMPT=/*PL_FILE:erisilebilirlik.md*/"",PL_A11Y_DOC=/*PL_FILE:erisilebilirlik-dokuman.md*/"",PL_A11Y_IMGS=/*PL_IMGS:erisilebilirlik-gorseller*/[];
const plSec=(t,a,b)=>{let i=t.indexOf(a);if(i<0)return"";let j=b?t.indexOf(b,i+a.length):-1;return t.slice(i+a.length,j<0?undefined:j)};
const PL_A11Y_CRIT=plSec(PL_A11Y_PROMPT,"\n## 20. Tamamlanma ve Kabul Kriterleri","\n### Nihai teslimat").split("\n").map(l=>/^\d+\.\s+(.+)$/.exec(l)).filter(Boolean).map(m=>m[1].trim());
const PL_KVKK_CRIT=plSec(PL_KVKK_PROMPT,"\n17. Kabul Kriterleri","\nTeslimat:").split("\n").map(l=>/^\d+\.\s+(.+)$/.exec(l)).filter(Boolean).map(m=>m[1].trim());
const PL_KVKK_REFS=[...plSec(PL_KVKK_PROMPT,"\n9. Yasal Metinlerde Resmi Kaynak","\nKaynak kullanım kuralları").matchAll(/^\d+\.\s+(.+?)\s+—\s+(https?:\/\/\S+)$/gm)].map(m=>({t:m[1],u:m[2]}));
/* Bölümler: iki hazır modülün (KVKK / GDPR & Çerez Yönetimi, Erişilebilirlik) içeriği — tek başına modül değildir (kullanıcı kararı 2026-11-08: her alan tek başlık, tek prompt). */
const PL_PARTS=[
{id:"kvkk-cerez-onayi",short:"Çerez",cat:"kvkk",version:"1.0.0",updated:PL_D,title:"Çerez Onay Yönetimi (CMP)",
 desc:"Zorunlu olmayan çerezleri ve izleme etiketlerini kullanıcı onay verene kadar çalıştırmayan, kabul ve reddi eşit kolaylıkta sunan, onay kaydını tutan çerez onay altyapısı.",
 tags:["çerez","rıza","consent-mode","analitik","kvkk","gdpr"],deps:["a11y-etkilesimli-bilesenler"],
 prompt:`Siteye KVKK ve GDPR ile uyumlu bir çerez onay yönetimi (CMP) kur. Zorunlu çerezler dışındaki bütün çerezler, pikseller ve etiketler (fonksiyonel, analitik, pazarlama) kullanıcı ilgili kategoriye onay verene kadar yüklenmesin. İlk katmanda "Tümünü reddet", "Tercihler" ve "Tümünü kabul et" seçenekleri aynı görsel ağırlıkta ve aynı tıklama sayısıyla sunulsun; ön işaretli kutu kullanma, sayfada gezinmeyi ya da kaydırmayı onay sayma. Tercihler penceresinde kategori başına açıklama, sağlayıcı listesi, saklama süresi ve aktarım ülkesi olsun. Onay kaydını (kategori kararları, onay metni sürümü, sunucu zamanı, rastgele anonim kimlik) sunucuda sakla; ham IP ya da kimlik bilgisi yazma. Kullanıcı kararını her sayfadan (alt bilgideki "Çerez tercihleri" bağlantısı) değiştirebilsin ve geri alabilsin; geri alınan kategorinin çerezlerini sil. Google etiketleri varsa Consent Mode v2'yi dört parametrede varsayılan "denied" ile etiketlerden önce başlat ve karara göre güncelle. Banner ve tercih penceresi klavye ve ekran okuyucuyla tam kullanılabilir olsun.`,
 criteria:["İlk ziyarette, karar verilmeden önce ağ isteklerinde analitik / pazarlama etiketi ve zorunlu olmayan çerez yok (DevTools › Network ve Application › Cookies ile temiz profilde doğrulanır).","\"Tümünü reddet\" ilk katmanda ve \"Tümünü kabul et\" ile aynı boyut, renk ağırlığı ve tıklama sayısında.","Hiçbir kategori ön işaretli değil; zorunlu çerezler \"her zaman açık\" olarak gerekçesiyle açıklanmış.","Onay kaydı kategori kararları, onay metni sürümü, sunucu zamanı ve anonim kimlikle saklanıyor; ham IP, e-posta ya da kullanıcı adı içermiyor.","Karar her sayfadaki \"Çerez tercihleri\" bağlantısıyla değiştirilebiliyor; geri alınan kategorinin çerezleri siliniyor, etiketleri bir sonraki yüklemede çalışmıyor.","Consent Mode v2 kullanılıyorsa ad_storage, analytics_storage, ad_user_data ve ad_personalization varsayılanı \"denied\" ve bu çağrı etiketlerden önce çalışıyor.","Onay metni ya da çerez listesi değişince (metin sürümü artınca) kullanıcıdan yeniden karar isteniyor.","Banner ve tercih penceresi yalnız klavyeyle kullanılabiliyor; pencere açıkken odak içeride kalıyor, kapanınca açan öğeye dönüyor."],
 images:[{id:"img-1",src:PL_IMG.banner,alt:"Sayfanın altında çerez banner'ı: Tümünü Kabul Et, Tümünü Reddet ve Tercihleri Yönet düğmeleri aynı boyut ve renkte yan yana; sol alt köşede sürekli görünen çerez ikonu",caption:"İlk katman — üç düğme eşit öncelikte; sol alttaki ikon tercih merkezini her sayfadan açar."},{id:"img-2",src:PL_IMG.prefs,alt:"Çerez tercihleri penceresi: Zorunlu (her zaman açık), İşlevsel, Analitik ve Pazarlama kategorileri kapalı anahtarlarla; altta aynı görünümde üç düğme",caption:"Tercihler katmanı — kategoriler varsayılan kapalı, sağlayıcılar adıyla."}],
 refs:[{t:"EDPB — Guidelines 05/2020 on consent under Regulation 2016/679",u:"https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en"},{t:"KVKK — Açık Rıza Alırken Dikkat Edilecek Hususlar",u:"https://www.kvkk.gov.tr/Icerik/2037/Acik-Riza-Alirken-Dikkat-Edilecek-Hususlar"},{t:"KVKK — Yurt Dışı Aktarım",u:"https://www.kvkk.gov.tr/Icerik/2053/Yurtdisina-Aktarim"},{t:"KVKK — Rehberler",u:"https://www.kvkk.gov.tr/Icerik/2030/rehberler"},{t:"Google — Set up consent mode on websites",u:"https://developers.google.com/tag-platform/security/guides/consent"}],
 doc:`# Çerez Onay Yönetimi (CMP) — Teknik Doküman

## Kapsam
- İlk katman (banner: Tümünü Kabul Et / Tümünü Reddet / Tercihleri Yönet, eşit öncelikte), tercih merkezi, sol altta sürekli çerez ikonu, onay kaydı API'si, etiket yükleyici ve alt bilgideki "Çerez tercihleri" bağlantısı.
- Zorunlu çerezler (oturum, güvenlik, yük dengeleme, onay kararının kendisi) onaysız çalışır; diğer bütün kategoriler onaya bağlıdır.

## Kategoriler
| Kategori | Örnek | Varsayılan |
|---|---|---|
| Zorunlu | oturum, CSRF, dil tercihi | Açık (kapatılamaz) |
| İşlevsel | sohbet aracı, harita | Kapalı |
| Analitik | GA4, ısı haritası | Kapalı |
| Pazarlama | Meta Pixel, Google Ads | Kapalı |

## Bileşenler
1. **Onay deposu (istemci):** birinci taraf çerez ya da localStorage — \`{v, ts, cats:{necessary:true, functional, analytics, marketing}, textVersion}\`; varsayılan hepsi \`false\` (zorunlu hariç). Yalnız karar ve sürüm; kişisel veri yok.
2. **Etiket yükleyici:** zorunlu olmayan betikler \`type="text/plain" data-consent="analytics"\` ile işaretlenir ya da etiket yöneticisinde onay tetikleyicisine bağlanır; karar gelince yüklenir.
3. **Onay kaydı API'si:** \`POST /api/consent\` — gövde: rastgele anonim kimlik (UUID), kararlar, metin sürümü, kaynak sayfa. Zaman damgasını sunucu yazar; oran sınırlaması uygulanır.
4. **Tercih penceresi:** yerel \`<dialog>\`; kategori başına açıklama, sağlayıcılar, saklama süresi, aktarım ülkesi.
5. **Sol alt çerez ikonu ve alt bilgi bağlantısı:** tercih merkezini her sayfadan açar; konum ve boyut yönetimden ayarlanır, mobilde gezinme / CTA alanını kapatmaz.

## Akış
1. Sayfa açılır → onay deposu okunur. Kayıt yoksa ya da \`textVersion\` eskiyse banner gösterilir.
2. Consent Mode varsa şu çağrı bütün etiketlerden önce çalışır:

\`\`\`js
gtag('consent', 'default', {
  ad_storage: 'denied',
  analytics_storage: 'denied',
  ad_user_data: 'denied',
  ad_personalization: 'denied'
});
\`\`\`

3. Kullanıcı karar verir → depo yazılır → API'ye kayıt gönderilir → \`gtag('consent', 'update', …)\` → izin verilen kategorinin betikleri yüklenir.
4. Geri alma → kategori çerezleri aynı alan adı ve yol ile silinir; betikler sonraki yüklemede çalışmaz.

## Veri modeli (sunucu)
\`consent_records(id, anon_id, decisions jsonb, text_version, page, created_at)\` — kişisel veri yok; saklama süresi saklama-imha politikasında tanımlanır.

## Uygulama notları
- Reddetmek kabul etmek kadar kolay olmalı; kaydırma, sayfada gezinme ya da banner'ı kapatmak onay sayılmaz.
- Çerez politikası ve aydınlatma metni bağlantısı ilk katmanda görünür olmalı.
- Yurt dışındaki sağlayıcılara aktarım için (ör. yurt dışında barındırılan analitik) KVKK md. 9 kapsamındaki dayanağı uyum ekibiyle doğrulayın.
- Onay kararının geçerlilik süresi politikada tanımlı olsun (öneri: 6–12 ay); süre dolunca yeniden sorulur.

## Test
- Temiz profille ilk ziyaret: Network'te üçüncü taraf etiket yok.
- Reddet → sayfayı yenile → hâlâ yok. Yalnız analitiği kabul et → yalnız analitik yükleniyor.
- Klavye: bütün düğmelere Tab ile ulaşılıyor, odak görünür, Esc davranışı tanımlı (karar verilmemiş sayılır).
- Ekran okuyucu: banner bölgesi (\`role="region"\` + \`aria-label\`) ve pencere başlığı okunuyor.

## Kaçınılacaklar
- "Kabul et" yanında yalnız "Daha fazla bilgi" sunmak; reddi ikinci katmana gizlemek.
- Onaydan önce "yalnız sayfa görüntüleme" gerekçesiyle analitik çalıştırmak.
- Onay kaydına ham IP, e-posta ya da kullanıcı adı yazmak.`},
{id:"kvkk-aydinlatma-riza",short:"Aydınlatma ve rıza",cat:"kvkk",version:"1.0.0",updated:PL_D,title:"Aydınlatma ve Açık Rıza Formları",
 desc:"Kişisel veri toplayan her formda aydınlatmayı doğru yerde gösteren, açık rızayı ve ticari ileti onayını hizmet şartından ayıran, onayların kanıtını metin sürümüyle saklayan form altyapısı.",
 tags:["aydınlatma","açık-rıza","form","iys","kvkk","gdpr"],deps:["a11y-formlar"],
 prompt:`Sitedeki kişisel veri toplayan bütün formlara (iletişim, teklif, üyelik, bülten, başvuru) KVKK md. 10'a uygun aydınlatma ve gerektiğinde açık rıza adımı ekle. Aydınlatma metni formun gönder düğmesinden önce kısa özet ve tam metin bağlantısıyla gösterilsin; aydınlatma bir onay kutusuna bağlanmasın. Açık rıza yalnız gerçekten rızaya dayanan işlemler (ör. pazarlama iletişimi, rızaya dayanan yurt dışı aktarım, özel nitelikli veri) için alınsın: her amaç ayrı, ön işaretsiz ve isteğe bağlı kutuyla; formun gönderilmesi ya da hizmet rızaya bağlanmasın. Ticari elektronik ileti onayı kanal bazında (e-posta, SMS, arama) ayrı alınsın ve İleti Yönetim Sistemi'ne (İYS) aktarılabilecek biçimde kaydedilsin. Her onay için amaç, metin sürümü, kanal, sunucu zamanı ve kayıt kimliği değiştirilemez günlükte saklansın; rızayı geri alma yolu sağlansın. Formlar yalnız amaç için gerekli alanları istesin.`,
 criteria:["Kişisel veri toplayan her formda aydınlatma özeti ve tam metin bağlantısı gönder düğmesinden önce görünüyor; aydınlatma için zorunlu \"okudum, onaylıyorum\" kutusu yok.","Açık rıza kutuları amaç başına ayrı, ön işaretsiz ve isteğe bağlı; hizmet için gerekli olmayan rızalar işaretlenmeden form gönderilebiliyor.","Ticari elektronik ileti onayı kanal bazında ayrı alınıyor ve kaydediliyor.","Onay kaydında amaç, metin sürümü (sürüm no ya da içerik özeti), kanal, sunucu zamanı ve kayıt kimliği var; kayıtlar güncellenmiyor, yalnız yeni kayıt ekleniyor.","Rızayı geri alma bağlantısı / hesap ayarı var; geri alınınca ilgili işlem duruyor ve geri alma da kaydediliyor.","Her form alanının amaçla bağlantısı belgelenmiş; amaç dışı alan (ör. T.C. kimlik no, doğum tarihi) istenmiyor.","Aydınlatma ya da rıza metni değişince yeni sürüm oluşuyor; eski onaylar kendi sürümüyle ilişkili kalıyor."],
 images:[{id:"img-1",src:PL_IMG.form,alt:"Teklif formu: ad, e-posta ve mesaj alanlarının altında aydınlatma özeti ve bağlantısı; altında ön işaretsiz iki isteğe bağlı onay kutusu ve Gönder düğmesi",caption:"Aydınlatma bilgi olarak, rızalar amaç başına ayrı ve isteğe bağlı."}],
 refs:[{t:"KVKK — Aydınlatma Yükümlülüğü",u:"https://www.kvkk.gov.tr/Icerik/2033/Aydinlatma-Yukumlulugu-"},{t:"KVKK — Açık Rıza Alırken Dikkat Edilecek Hususlar",u:"https://www.kvkk.gov.tr/Icerik/2037/Acik-Riza-Alirken-Dikkat-Edilecek-Hususlar"},{t:"6698 sayılı Kişisel Verilerin Korunması Kanunu (PDF)",u:"https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf"},{t:"İleti Yönetim Sistemi (İYS)",u:"https://iys.org.tr/"},{t:"GDPR — Regulation (EU) 2016/679",u:"https://eur-lex.europa.eu/eli/reg/2016/679/oj"}],
 doc:`# Aydınlatma ve Açık Rıza Formları — Teknik Doküman

## Kavramlar
- **Aydınlatma (KVKK md. 10):** veri toplanırken kişiyi bilgilendirme yükümlülüğü — veri sorumlusu, amaç, aktarım, toplama yöntemi ve hukuki sebep, md. 11 hakları. Onay gerektirmez; bilgiye erişim yeterlidir.
- **Açık rıza (KVKK md. 3):** belirli bir konuya ilişkin, bilgilendirmeye dayanan ve özgür iradeyle açıklanan rıza. Sözleşme, kanuni yükümlülük ya da meşru menfaat gibi diğer işleme şartlarından biri varsa ayrıca rıza istenmez.
- **GDPR md. 7:** rızanın kanıtlanabilmesi ve verildiği kadar kolay geri alınabilmesi gerekir.

## Form düzeni
1. Alanlar (yalnız amaç için gerekenler; zorunlu olanlar işaretli).
2. Aydınlatma özeti: 1–2 cümle + "Aydınlatma Metni'nin tamamı" bağlantısı (yeni sekmede değil, aynı sayfada açılır pencere ya da sayfa).
3. Rıza kutuları: amaç başına ayrı, ön işaretsiz, "(isteğe bağlı)" etiketli.
4. Gönder düğmesi.

## Veri modeli
\`\`\`sql
consent_texts(id, purpose, version, body_hash, published_at)
consents(id, subject_ref, purpose, channel, text_version, granted boolean,
         source_form, created_at)  -- yalnız INSERT; güncelleme ve silme yok
\`\`\`
- \`subject_ref\`: üye kimliği ya da doğrulanmış e-posta / telefonun özeti.
- Geri alma = \`granted=false\` ile yeni kayıt. Geçerli durum = amaç + kanal için en son kayıt.

## API
- \`POST /api/forms/:formId\` — form verisi ve \`consents[]\` (amaç, kanal, granted) birlikte gelir; sunucu metin sürümünü kendi tarafında eşler, istemciden gelen sürüme güvenmez.
- \`POST /api/consents/withdraw\` — doğrulanmış kişi için geri alma.

## Ticari elektronik ileti
- Türkiye'de ticari elektronik ileti onayları İleti Yönetim Sistemi'ne (İYS) kaydedilir; entegrasyonu (API ya da hizmet sağlayıcı) bu modülün kayıtlarından besleyin.
- Onay kanal bazındadır: e-posta, SMS, arama ayrı ayrı.

## Test
- Rıza kutusu işaretlenmeden form gönderilebiliyor ve hizmet çalışıyor.
- Aynı kişi rızasını geri alınca pazarlama listesinden çıkıyor; kayıt tablosunda iki satır var.
- Metin sürümü değişince yeni onaylar yeni sürüme bağlanıyor.

## Kaçınılacaklar
- Aydınlatma ile rızayı tek kutuda birleştirmek ("Aydınlatma metnini okudum ve onaylıyorum").
- Rızayı üyelik ya da hizmet şartına bağlamak.
- Onay kaydını istemcide (yalnız localStorage) tutmak.`},
{id:"kvkk-ilgili-kisi-basvuru",short:"Başvuru",cat:"kvkk",version:"1.0.0",updated:PL_D,title:"İlgili Kişi Başvuru Akışı",
 desc:"İlgili kişinin erişim, düzeltme, silme, itiraz ve veri taşınabilirliği taleplerini kimlik doğrulamayla alan, yasal yanıt süresini izleyen ve her adımı kayıt altına alan başvuru modülü.",
 tags:["başvuru","dsar","silme","veri-taşınabilirliği","kvkk","gdpr"],deps:["kvkk-aydinlatma-riza","kvkk-saklama-imha","a11y-formlar"],
 prompt:`Siteye ilgili kişi başvuru modülü ekle: KVKK md. 11'deki haklar ve AB'deki kullanıcılar varsa GDPR md. 15–22 hakları için herkese açık başvuru formu, hesap içinden başvuru ve yönetim panelinde başvuru kuyruğu. Başvuru sahibinin kimliğini veri türüyle orantılı bir yöntemle doğrula (oturum, kayıtlı e-postaya doğrulama bağlantısı); gereğinden fazla belge isteme. Her başvuruya kayıt numarası ve son yanıt tarihi ver (KVKK md. 13: en geç 30 gün; GDPR md. 12: 1 ay, gerekçeyle uzatılabilir) ve süre dolmadan panelde uyarı göster. Erişim talebinde kişinin verilerini veri envanterindeki bütün kaynaklardan makinece okunabilir biçimde (JSON ve CSV) dışa aktar; silme talebinde yasal saklama yükümlülüğü olan kayıtları gerekçesiyle ayır, kalanları sil ya da anonimleştir ve sonucu bildir. Başvurular yalnız sahibi ve yetkili personel tarafından görülsün; bütün adımları değiştirilemez denetim günlüğüne yaz.`,
 criteria:["Başvuru formu ve hesap içi başvuru, KVKK md. 11 haklarının her birini ayrı talep türü olarak sunuyor.","Her başvuruya benzersiz kayıt numarası ve son yanıt tarihi atanıyor; panelde kalan gün görünüyor, son 7 günde uyarı çıkıyor.","Kimlik doğrulanmadan hiçbir kişisel veri gösterilmiyor ya da gönderilmiyor; vekâleten başvuru ayrı akışta yetki belgesiyle.","Erişim çıktısı JSON ve CSV; veri envanterindeki her kaynağı (tablolar, dosyalar, e-posta sağlayıcısı, analitik) kapsadığı envanter listesiyle doğrulanıyor.","Silmede yasal saklama gerektiren kayıtlar gerekçesiyle tutuluyor; diğerleri siliniyor ya da anonimleştiriliyor; arama dizini ve önbellek de temizleniyor.","Kabul, kısmi kabul ve gerekçeli ret yanıt şablonları var; yanıt kanal ve tarihle kaydediliyor.","Denetim günlüğü başvuru, doğrulama, işlem ve yanıt adımlarını kim / ne zaman bilgisiyle tutuyor ve değiştirilemiyor.","Başvuru uç noktaları oran sınırlı; başvuru kimliği tahmin edilemez ve sahiplik kontrolü yapılıyor (IDOR yok)."],
 images:[{id:"img-1",src:PL_IMG.dsar,alt:"Beş adımlı akış şeması: Başvuru, Kimlik doğrulama, Kayıt ve süre, İnceleme, Yanıt; altında her adımın denetim günlüğüne yazıldığı notu",caption:"Başvurudan yanıta akış ve denetim izi."}],
 refs:[{t:"KVKK — İlgili Kişinin Hakları",u:"https://www.kvkk.gov.tr/Icerik/2036/Ilgili-Kisinin-Haklari"},{t:"KVKK — Başvuruların Cevaplanması Yükümlülüğü",u:"https://www.kvkk.gov.tr/Icerik/2046/Ilgili-Kisiler-Tarafindan-Yapilan-Basvurularin-Cevaplanmasi-Yukumlulugu"},{t:"6698 sayılı Kişisel Verilerin Korunması Kanunu (PDF)",u:"https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6698.pdf"},{t:"GDPR — Regulation (EU) 2016/679",u:"https://eur-lex.europa.eu/eli/reg/2016/679/oj"}],
 doc:`# İlgili Kişi Başvuru Akışı — Teknik Doküman

## Talep türleri (KVKK md. 11)
| Tür | Kod | Çıktı |
|---|---|---|
| İşlenip işlenmediğini öğrenme | \`exists\` | Evet / hayır + özet |
| Bilgi talep etme / erişim | \`access\` | JSON + CSV dışa aktarım |
| Amaç ve amaca uygunluk | \`purpose\` | Envanterden üretilen açıklama |
| Aktarılan üçüncü kişiler | \`recipients\` | Alıcı listesi |
| Düzeltme | \`rectify\` | Değişiklik kaydı |
| Silme / yok etme | \`erase\` | Silme raporu + tutulan kayıtların gerekçesi |
| Üçüncü kişilere bildirim | \`notify\` | Bildirim kaydı |
| Otomatik analize itiraz | \`object\` | Değerlendirme |
| Zararın giderilmesi | \`damage\` | Hukuk birimine yönlendirme |
GDPR için ek: \`portability\` (md. 20), \`restrict\` (md. 18).

## Durum makinesi
\`alındı → kimlik_doğrulama → incelemede → yanıtlandı | kısmen_kabul | reddedildi\` — GDPR'da \`süre_uzatıldı\` ara durumu (gerekçe ve kişiye bildirim zorunlu).

## Veri modeli
\`\`\`sql
dsr_requests(id uuid, ref_no, type, subject_ref, channel, status,
             received_at, due_at, verified_at, closed_at)
dsr_events(id, request_id, actor, action, note, created_at)  -- yalnız INSERT
\`\`\`
\`due_at\` = \`received_at\` + 30 gün (KVKK); AB kullanıcısında 1 ay.

## Dışa aktarım
- Veri envanteri haritası: \`kaynak → kişi anahtarı → alanlar\`. Dışa aktarım bu haritadan üretilir; yeni tablo eklenince haritaya eklenmezse CI uyarır.
- Paket: \`veriler.json\`, tablo başına \`*.csv\`, \`BENIOKU.txt\` (alan açıklamaları). Bağlantı süreli ve tek kullanımlık.

## Silme
- Kanuni saklama yükümlülüğü (ör. fatura) olan kayıtlar silinmez; gerekçesiyle listelenir ve erişimi kısıtlanır.
- Silinemeyen ilişkili kayıtlarda kişisel alanlar anonimleştirilir.
- Arama dizini, önbellek, CDN, e-posta pazarlama listesi ve analitik kimlikleri de kapsanır; yedekler saklama-imha politikasına göre döner.

## Güvenlik
- Başvuru kimliği UUID; panelde yalnız yetkili rol; her sorgu sahiplik kontrolüyle.
- Dışa aktarım dosyası şifreli depoda, süreli imzalı bağlantıyla.

## Test
- Başka kullanıcının başvuru kimliğiyle erişim denemesi 404 dönüyor.
- 30. günü geçen başvuru panelde kırmızı; günlükte bütün adımlar var.`},
{id:"kvkk-saklama-imha",short:"Saklama ve imha",cat:"kvkk",version:"1.0.0",updated:PL_D,title:"Saklama, İmha ve Veri Minimizasyonu",
 desc:"Her kişisel veri kategorisinin saklama süresini koda bağlayan, süresi dolan veriyi periyodik işle silen ya da anonimleştiren, loglarda ve yedeklerde kişisel veriyi sınırlayan altyapı.",
 tags:["saklama","imha","anonimleştirme","log","veri-envanteri","kvkk"],deps:[],
 prompt:`Projede kişisel verinin saklama süresini koda bağlayan bir saklama-imha altyapısı kur. Önce veri envanteri çıkar: hangi tabloda / alanda hangi kişisel veri, hangi amaçla, hangi hukuki sebeple ve ne kadar süre tutuluyor. Süreleri tek bir yapılandırma dosyasında (saklama politikası) tanımla. Süresi dolan kayıtları silen, yok eden ya da anonimleştiren periyodik bir iş yaz; iş idempotent olsun ve her çalışmasını (kategori, etkilenen kayıt sayısı, yöntem, zaman) imha tutanağı olarak kaydetsin. Periyodik imha aralığı ilgili yönetmelikteki azami süreyi (6 ay) aşmasın; daha sık çalıştırmak tercih edilir. Uygulama loglarına kişisel veri yazma, gerekiyorsa maskele; log ve yedek saklama sürelerini politikaya bağla. Yeni bir kişisel veri alanı saklama süresi tanımlanmadan eklenirse CI uyarı versin.`,
 criteria:["Veri envanteri depoda (kaynak, alan, amaç, hukuki sebep, süre, yöntem) güncel ve kod incelemesinde zorunlu.","Saklama süreleri tek yapılandırma dosyasında; iş mantığında sabit süre yok.","Periyodik imha işi idempotent; iki kez çalıştırınca ikinci çalışma 0 kayıt etkiliyor.","Her çalışma imha tutanağı yazıyor (kategori, sayı, yöntem, zaman, iş sürümü); tutanak kişisel veri içermiyor.","İş en az 6 ayda bir (önerilen: günlük ya da haftalık) çalışıyor ve hata olursa alarm üretiyor.","Uygulama loglarında e-posta, telefon, T.C. kimlik no, kart verisi yok ya da maskeli (log örneklemesiyle doğrulanır).","Yedeklerin saklama süresi politikada tanımlı; süresi dolan yedekler otomatik siliniyor.","Envantere eklenmemiş yeni kişisel veri alanı CI'da uyarı üretiyor."],
 images:[{id:"img-1",src:PL_IMG.retention,alt:"Saklama politikası tablosu: veri kategorisi, hukuki sebep, süre ve yöntem sütunları; iletişim formu, sipariş, log ve pazarlama izni örnek satırları",caption:"Örnek saklama politikası — süreler projeye göre belirlenir."}],
 refs:[{t:"KVKK — Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi",u:"https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi"},{t:"KVKK — Veri Güvenliğine İlişkin Yükümlülükler",u:"https://www.kvkk.gov.tr/Icerik/2040/Veri-Guvenligine-Iliskin-Yukumlulukler"},{t:"KVKK — Kişisel Verilerin İşlenmesinde Temel İlkeler",u:"https://www.kvkk.gov.tr/Icerik/2049/Kisisel-Verilerin-Islenmesinde-Genel-(Temel)-Ilkeler"}],
 doc:`# Saklama, İmha ve Veri Minimizasyonu — Teknik Doküman

## İlkeler
- KVKK md. 4: işlendikleri amaç için gerekli süre kadar muhafaza; amaçla bağlantılı, sınırlı ve ölçülü işleme.
- KVKK md. 7: işleme şartları ortadan kalkınca silme, yok etme ya da anonim hale getirme.
- Saklama ve imha politikası hazırlayan veri sorumlusu, yükümlülüğün doğduğu tarihi izleyen ilk periyodik imhada veriyi imha eder.

## Saklama politikası dosyası
\`\`\`yaml
# config/retention.yaml
contact_messages:   { basis: legitimate_interest, keep: P2Y,  method: delete }
orders:             { basis: legal_obligation,    keep: P10Y, method: archive_then_delete }
app_logs:           { basis: legitimate_interest, keep: P90D, method: delete }
marketing_consent:  { basis: explicit_consent,    keep: until_withdrawn, method: anonymize }
\`\`\`
Süreler ISO 8601 biçiminde; değerler örnektir, hukuki değerlendirmeyle belirlenir.

## Periyodik imha işi
1. Politika dosyasını okur, kategori başına süresi dolan kayıtları seçer (\`created_at < now() - keep\`).
2. Yönteme göre siler, anonimleştirir ya da arşive taşır; ilişkili dosya, arama dizini ve önbellek kayıtlarını da temizler.
3. \`retention_runs(id, category, affected, method, started_at, finished_at, job_version)\` tablosuna tutanak yazar.
4. Hata olursa yeniden denenir, kalıcı hatada alarm verir; yarım kalan iş tekrar çalıştırılabilir (idempotent).

## Anonimleştirme
- Kişiyi doğrudan ya da dolaylı tanımlayan alanlar geri döndürülemez biçimde kaldırılır; yalnız takma ad (pseudonym) vermek anonimleştirme değildir.
- İstatistik için gereken alanlar genelleştirilir (doğum tarihi → yaş aralığı, adres → il).

## Log hijyeni
- Yapılandırılmış log; kişisel alanlar ya hiç yazılmaz ya da maskelenir (\`a***@alanadi.com\`).
- İstek gövdeleri loglanmaz; hata ayıklama için istek kimliği kullanılır.

## Yedekler
- Yedek saklama süresi politikada; şifreli; süresi dolan otomatik silinir.
- Geri yüklemeden sonra imha işi yeniden çalıştırılır (silinmiş verinin geri gelmemesi için).

## Test
- Sabit saat ile işi çalıştır: yalnız süresi dolan kayıtlar etkileniyor, tutanak sayısı eşleşiyor.
- İş iki kez çalışınca ikinci tutanak 0 kayıt.`}
];
const PL_PART=Object.fromEntries(PL_PARTS.map(p=>[p.id,p]));
/* Bölümleri tek modülde birleştirir (meta.cover: görselleri önce gelen bölüm — kart küçük resmi): doküman = baş + "## N. Bölüm" (bölüm başlıkları bir düzey aşağı) + son; kriterler "Bölüm: …"; görsel ve kaynaklar tekrarsız. */
function plJoin(meta,ids){const P=ids.map(i=>PL_PART[i]),seenI=new Set(),seenR=new Set();
 const sh=d=>{let inC=false;return d.replace(/^# .*\n+/,"").split("\n").map(l=>{if(/^\s*```/.test(l)){inC=!inC;return l}return !inC&&/^#{1,5}\s/.test(l)?"#"+l:l}).join("\n")};
 return{id:meta.id,cat:meta.cat,version:meta.version||"1.0.0",updated:PL_D,history:meta.history||[],title:meta.title,desc:meta.desc,tags:meta.tags,deps:meta.deps||[],prompt:meta.prompt,
  criteria:meta.criteria&&meta.criteria.length?meta.criteria:P.flatMap(p=>p.criteria.map(c=>`${p.short}: ${c}`)),
  images:(meta.cover?[PL_PART[meta.cover]].concat(P.filter(p=>p.id!==meta.cover)):P).flatMap(p=>p.images).filter(i=>!seenI.has(i.src)&&seenI.add(i.src)).map((i,n)=>Object.assign({},i,{id:"img-"+(n+1)})),
  refs:(meta.refs||[]).concat(P.flatMap(p=>p.refs)).filter(r=>!seenR.has(r.u)&&seenR.add(r.u)),
  doc:[meta.docHead.trim(),...P.map((p,i)=>`## ${i+1}. ${p.title}\n\n${sh(p.doc).trim()}`),meta.docTail.trim()].join("\n\n")}}
const PL_BUILTIN=[
{id:"erisilebilirlik",cat:"a11y",version:"2.0.0",updated:PL_D,title:"Erişilebilirlik (WCAG 2.2 AA)",
 history:[{version:"1.0.0",date:PL_D,note:"Dört bölümlü kısa prompt (temel uyum, klavye-odak, formlar, etkileşimli bileşenler) ve 3 şematik çizim. 2026-11-08'de kullanıcının \"Evrensel Web Erişilebilirlik Modülü\" master promptu, referans uygulamanın işleyiş dokümanı ve 16 ekran görüntüsüyle değiştirildi.",data:null}],
 desc:"Ziyaretçi Erişilebilirlik Asistanı (28 hızlı ayar, 9 profil, ayrıntılı kontroller, sesli okuma ve komut), 11 bölümlü Erişilebilirlik Merkezi ve Playwright + axe-core denetim altyapısıyla (CI kapısı, CMS yayın kontrolleri, raporlar) WCAG 2.2 A/AA'yı destekleyen, üçüncü taraf widget'a bağımlı olmayan modül.",
 tags:["wcag","erişilebilirlik","asistan","profiller","axe-core","playwright","ci","cms","ekran-okuyucu","klavye"],deps:[],
 prompt:PL_A11Y_PROMPT,criteria:PL_A11Y_CRIT,images:PL_A11Y_IMGS,
 doc:`> **Bu doküman hakkında (Prompt Kütüphanesi notu).** Aşağıdaki metin, bu master promptla geliştirilmiş referans uygulamanın (onurkenar.com · v1 · 8 Kasım 2026) işleyiş dokümanıdır. Yollar, port, tablo ve dosya adları, komutlar, e-posta sağlayıcısı ve ürün adları o projeye özgüdür; yeni bir projede bağlayıcı olan prompttur ve o projenin mimarisine uyarlanır. Dokümandaki ekran görüntülerinden 16'sı bu modülün referans görselleridir; diğerleri yalnız açıklamasıyla anılır.

`+PL_A11Y_DOC,
 refs:[{t:"W3C — Web Content Accessibility Guidelines (WCAG) 2.2",u:"https://www.w3.org/TR/WCAG22/"},{t:"W3C — How to Meet WCAG (Quick Reference)",u:"https://www.w3.org/WAI/WCAG22/quickref/"},{t:"W3C — Understanding WCAG 2.2",u:"https://www.w3.org/WAI/WCAG22/Understanding/"},{t:"W3C — ARIA Authoring Practices Guide (APG)",u:"https://www.w3.org/WAI/ARIA/apg/"},{t:"W3C APG — Dialog (Modal) Pattern",u:"https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/"},{t:"W3C — Accessibility Conformance Testing (ACT)",u:"https://www.w3.org/WAI/standards-guidelines/act/"},{t:"W3C — Developing an Accessibility Statement",u:"https://www.w3.org/WAI/planning/statements/"},{t:"Understanding 2.4.11 Focus Not Obscured (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html"},{t:"Understanding 2.5.8 Target Size (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html"},{t:"Understanding 3.3.8 Accessible Authentication (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html"},{t:"axe-core (Deque) — kural motoru",u:"https://github.com/dequelabs/axe-core"},{t:"Playwright — Accessibility testing",u:"https://playwright.dev/docs/accessibility-testing"},{t:"MDN — Web Speech API",u:"https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API"},{t:"MDN — CSS Custom Highlight API",u:"https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API"},{t:"MDN — inert global attribute",u:"https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert"}]},
plJoin({id:"kvkk-gdpr-cerez",cat:"kvkk",title:"KVKK / GDPR & Çerez Yönetimi",version:"2.0.0",
 history:[{version:"1.0.0",date:PL_D,note:"Dört bölümlü kısa prompt (saklama-imha, aydınlatma-rıza, çerez, başvuru). 2026-11-08'de kullanıcının \"KVKK, GDPR, Yasal Belgeler ve Çerez Yönetim Sistemi\" geliştirme promptuyla değiştirildi; kabul kriterleri ve resmî kaynaklar o prompttan alınır.",data:null}],
 desc:"Yasal belgeler ve uygunluk taraması, gerçek tarayıcıyla çerez taraması ve envanter, çerez politikasına otomatik tablo, default deny rıza motoru, eşit öncelikli banner ve sol alt çerez ikonu, Consent Mode, rıza kayıtları, veri sahibi başvuruları ve çok dilli içerikleri CMS üzerinden yöneten KVKK / GDPR modülü.",
 tags:["kvkk","gdpr","çerez","cmp","consent-mode","yasal-belgeler","uygunluk-taraması","rıza","başvuru","çok-dilli"],deps:["erisilebilirlik"],cover:"kvkk-cerez-onayi",
 prompt:PL_KVKK_PROMPT,criteria:PL_KVKK_CRIT,refs:PL_KVKK_REFS,
 docHead:`# KVKK / GDPR & Çerez Yönetimi — Teknik Doküman

## Bu doküman nasıl kullanılır
- Bağlayıcı olan prompttur (17 bölüm, Faz 00–11, 20 kabul kriteri). Bu doküman promptu tekrar etmez; uygulamada sık karşılaşılan teknik ayrıntıları ve tuzakları verir.
- Faz sırası ve faz geçiş kuralları prompttaki gibidir; aşağıdaki tablo hangi fazda hangi bölüme bakılacağını gösterir.

| Faz | Konu | Bu dokümandaki bölüm |
|---|---|---|
| 01 | Veri modeli, saklama süreleri, audit | 1. Saklama, İmha ve Veri Minimizasyonu |
| 02–04 | Consent engine, default deny, script engelleme, Consent Mode, banner ve tercih merkezi | 3. Çerez Onay Yönetimi (CMP), 5. Merkezi consent API |
| 05 | Yasal belgeler, form izinleri, ticari ileti | 2. Aydınlatma ve Açık Rıza Formları |
| 06–07 | Çerez taraması, envanter, dinamik çerez tablosu | 6. Tarama ve dinamik çerez tablosu |
| 10 | Veri sahibi başvuruları, bölgesel kurallar | 4. İlgili Kişi Başvuru Akışı |

- Hukuki metinler yer tutucu ve taslaktır; içerik uyum ekibi / avukat tarafından onaylanmadan yayınlanmaz. Bu doküman hukuki görüş değildir.`,
 docTail:`## 5. Merkezi consent API

\`\`\`ts
type Category = 'necessary' | 'functional' | 'analytics' | 'marketing';
interface ConsentState {
  categories: Record<Category, boolean>;   // necessary her zaman true
  services: Record<string, boolean>;        // servis kimliği → izin
  policyVersion: string;                    // onay anındaki çerez politikası sürümü
  region: string;                           // uygulanan bölgesel kural (dil değil)
  updatedAt: string;
}
getConsentState(): ConsentState
hasConsent(categoryOrService: string): boolean
updateConsent(preferences: Partial<ConsentState>): Promise<void>
withdrawConsent(): Promise<void>
subscribeToConsentChanges(cb: (s: ConsentState) => void): () => void
\`\`\`
- Servis izni kategori iznini aşamaz: \`hasConsent('ga4')\` = analitik kategorisi açık **ve** servis kapatılmamış.
- Sunucu tarafı aktarımlar (ör. Conversions API, sunucu tarafı etiketleme) istemcinin beyanına değil, sunucuda saklanan son rıza kaydına bakar.
- Script registry'deki her kayıt: servis, kategori, yükleme koşulu, bağlı çerezler, iframe / SDK yer tutucusu. Kayıtsız üçüncü taraf betik yüklenmez (CSP ile desteklenir).

## 6. Tarama ve dinamik çerez tablosu
- Tarama gerçek tarayıcıyla, temiz profilde, her senaryo için ayrı oturumda yapılır (rıza yok, tümünü reddet, tümünü kabul et, kategori bazlı); her senaryoda çerezler, localStorage, sessionStorage, IndexedDB ve ağ istekleri kaydedilir.
- Envanter kaydı: ad, sağlayıcı, domain, path, amaç, kategori, süre, oturum / kalıcı, birinci / üçüncü taraf, bağlı servis, ilk / son tespit, rıza gereksinimi, doğrulama durumu (tespit edildi → sınıflandırıldı → onaylandı).
- Önceki taramayla fark: yeni, kaybolan, süresi / sağlayıcısı / domaini / kategorisi değişen, rıza öncesi çalışan. Fark varsa çerez politikasının yeni taslak sürümü açılır; yayındaki sürüme dokunulmaz.
- Dinamik tablo yalnız onaylı envanterden çizilir; yayınlanan belge sürümü o anki envanterin anlık görüntüsünü saklar. Tablo başlıkları ve amaçlar dile göre çevrilir, çerez adı / domain / süre çevrilmez.

## Ortak test ve teslim
- Faz 11 kabul testleri: temiz profilde rıza öncesi üçüncü taraf ağ isteği yok; kabul, ret, kısmi izin ve geri çekme senaryoları ağ kaydıyla doğrulanır; Consent Mode sinyali ile etiket engelleme birlikte çalışır.
- Yasal belge akışı: taslak → inceleme → onay → yayın; otomatik taslak onaysız yayınlanmaz; onaylı sürüm değiştirilemez.
- Teslimde: gerçek tarama çıktıları, envanter, belge taslakları ve kaynakları (kontrol tarihiyle), kabul kriterleri tablosu (geçti / kaldı / kanıt), sınırlamalar ve deployment checklist.`},
 ["kvkk-saklama-imha","kvkk-aydinlatma-riza","kvkk-cerez-onayi","kvkk-ilgili-kisi-basvuru"])
];
