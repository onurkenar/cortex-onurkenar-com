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
 retention:PL_SVG(800,360,`<text x="40" y="48" font-size="18" font-weight="700" fill="#111">Saklama politikası → periyodik imha işi</text><rect x="40" y="70" width="720" height="40" rx="8" fill="#1f2937"/>${["Veri kategorisi","Hukuki sebep","Süre","Yöntem"].map((h,i)=>`<text x="${60+i*180}" y="96" font-size="13" font-weight="700" fill="#fff">${h}</text>`).join("")}${[["İletişim formu","Meşru menfaat","2 yıl","Silme"],["Sipariş / fatura","Kanuni yükümlülük","10 yıl","Arşiv → silme"],["Uygulama logu","Meşru menfaat","90 gün","Silme"],["Pazarlama izni","Açık rıza","Geri alınana dek","Anonimleştirme"]].map((r,j)=>`<rect x="40" y="${114+j*44}" width="720" height="40" rx="6" fill="${j%2?"#fff":"#f9fafb"}" stroke="#e5e7eb"/>${r.map((c,i)=>`<text x="${60+i*180}" y="${139+j*44}" font-size="13" fill="#1f2937">${c}</text>`).join("")}`).join("")}<text x="40" y="320" font-size="12" fill="#2453d6">Süreler örnektir; projenin hukuki değerlendirmesine göre doldurulur. İmha işi her çalışmada tutanak yazar.</text>`),
 focus:PL_SVG(800,360,`<text x="40" y="48" font-size="18" font-weight="700" fill="#111">Görünür odak ve hedef boyutu</text><rect x="60" y="90" width="200" height="48" rx="24" fill="#1f2937"/><text x="160" y="120" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">Odaksız</text><rect x="300" y="90" width="200" height="48" rx="24" fill="#1f2937"/><rect x="295" y="85" width="210" height="58" rx="29" fill="none" stroke="#2453d6" stroke-width="3"/><text x="400" y="120" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">Odakta</text><text x="400" y="166" font-size="12" fill="#2453d6" text-anchor="middle">en az 2 px, 3:1 kontrastlı halka, ofsetli</text><rect x="560" y="90" width="200" height="48" rx="24" fill="#1f2937"/><text x="660" y="120" font-size="15" font-weight="700" fill="#fff" text-anchor="middle">outline: none ✗</text><rect x="60" y="214" width="24" height="24" fill="#2453d6"/><text x="96" y="232" font-size="13" fill="#1f2937">24 × 24 CSS px — WCAG 2.2 · 2.5.8 asgari hedef</text><rect x="60" y="262" width="44" height="44" fill="none" stroke="#2453d6" stroke-width="2" stroke-dasharray="4 3"/><text x="116" y="290" font-size="13" fill="#1f2937">44 × 44 önerilen dokunma alanı (görsel küçük olsa da tıklama alanı büyük)</text><rect x="430" y="214" width="330" height="96" rx="10" fill="#fff" stroke="#d9dde2"/><rect x="430" y="214" width="330" height="30" rx="10" fill="#1f2937"/><text x="446" y="234" font-size="12" fill="#fff">Yapışkan başlık</text><rect x="446" y="252" width="140" height="30" rx="6" fill="none" stroke="#2453d6" stroke-width="3"/><text x="600" y="272" font-size="11" fill="#1f2937">odaklanan öğe başlığın</text><text x="600" y="288" font-size="11" fill="#1f2937">altında kalmaz (2.4.11)</text>`),
 errors:PL_SVG(800,520,`<rect x="160" y="20" width="480" height="480" rx="16" fill="#fff" stroke="#d9dde2"/><rect x="190" y="44" width="420" height="96" rx="10" fill="#fef2f2" stroke="#b91c1c" stroke-width="2"/><text x="208" y="72" font-size="15" font-weight="700" fill="#991b1b">2 alanda hata var</text><text x="208" y="96" font-size="13" fill="#b91c1c" text-decoration="underline">E-posta adresi geçerli değil</text><text x="208" y="120" font-size="13" fill="#b91c1c" text-decoration="underline">Telefon numarası 10 haneli olmalı</text><text x="190" y="176" font-size="13" font-weight="700" fill="#1f2937">E-posta *</text><rect x="190" y="186" width="420" height="40" rx="8" fill="#fff" stroke="#b91c1c" stroke-width="2"/><text x="204" y="211" font-size="13" fill="#1f2937">ornek@</text><text x="190" y="246" font-size="12" fill="#b91c1c">⚠ Geçerli bir e-posta yazın, ör. ad@alanadi.com</text><text x="190" y="286" font-size="13" font-weight="700" fill="#1f2937">Telefon *</text><rect x="190" y="296" width="420" height="40" rx="8" fill="#fff" stroke="#b91c1c" stroke-width="2"/><text x="190" y="356" font-size="12" fill="#b91c1c">⚠ 10 haneli numara yazın, ör. 5321234567</text><rect x="190" y="420" width="160" height="40" rx="20" fill="#1f2937"/><text x="270" y="445" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">Gönder</text><text x="20" y="96" font-size="11" fill="#2453d6">özet: odak buraya,</text><text x="20" y="112" font-size="11" fill="#2453d6">bağlantılar alana gider</text><text x="20" y="246" font-size="11" fill="#2453d6">aria-describedby +</text><text x="20" y="262" font-size="11" fill="#2453d6">aria-invalid="true"</text>`),
 dialog:PL_SVG(800,460,`<rect width="800" height="460" fill="#9aa1ab"/><text x="400" y="34" font-size="12" fill="#fff" text-anchor="middle">Arka plan inert — odak ve ekran okuyucu dışarı çıkamaz</text><rect x="180" y="60" width="440" height="330" rx="16" fill="#fff"/><text x="210" y="104" font-size="20" font-weight="700" fill="#111">Adresi sil</text><rect x="572" y="80" width="32" height="32" rx="8" fill="none" stroke="#2453d6" stroke-width="3"/><text x="588" y="103" font-size="18" fill="#111" text-anchor="middle">×</text><text x="210" y="140" font-size="13" fill="#4b5563">Kayıtlı adres kalıcı olarak silinecek.</text><text x="210" y="160" font-size="13" fill="#4b5563">Bu işlem geri alınamaz.</text><rect x="210" y="320" width="170" height="42" rx="21" fill="#fff" stroke="#1f2937" stroke-width="2"/><text x="295" y="346" font-size="14" font-weight="700" fill="#111" text-anchor="middle">Vazgeç</text><rect x="400" y="320" width="190" height="42" rx="21" fill="#b91c1c"/><text x="495" y="346" font-size="14" font-weight="700" fill="#fff" text-anchor="middle">Kalıcı olarak sil</text><text x="400" y="420" font-size="12" fill="#fff" text-anchor="middle">aria-labelledby = başlık · Esc kapatır · kapanınca odak açan düğmeye döner</text><path d="M560 230 q30 40 -20 80" fill="none" stroke="#2453d6" stroke-width="2" stroke-dasharray="5 4"/><text x="470" y="228" font-size="11" fill="#2453d6">Tab döngüsü pencere içinde</text>`)
};
const PL_D="2026-11-08";
/* KVKK modülünün promptu docs/v26/prompt-kutuphanesi/kvkk-gdpr-cerez.md'den gelir (prompt_kutuphanesi_ekle.py JSON olarak yazar). Kabul kriterleri promptun "17. Kabul Kriterleri" maddeleri, resmî kaynaklar "9." bölümündeki adreslerdir — tek kaynak. */
const PL_KVKK_PROMPT=/*PL_KVKK_PROMPT*/"";
const plSec=(t,a,b)=>{let i=t.indexOf(a);if(i<0)return"";let j=b?t.indexOf(b,i+a.length):-1;return t.slice(i+a.length,j<0?undefined:j)};
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
- İş iki kez çalışınca ikinci tutanak 0 kayıt.`},
{id:"a11y-wcag22-temel",short:"Temel",cat:"a11y",version:"1.0.0",updated:PL_D,title:"WCAG 2.2 AA Temel Uyum",
 desc:"Sayfa yapısı, metin alternatifleri, kontrast, yeniden akış, hareket ve WCAG 2.2 ile gelen yeni ölçütleri kapsayan, bütün sayfalarda geçerli erişilebilirlik temeli.",
 tags:["wcag","kontrast","landmark","alt-metin","ekran-okuyucu","reduced-motion"],deps:[],
 prompt:`Sitenin bütün sayfa şablonlarını WCAG 2.2 AA düzeyine getir. Her sayfada doğru lang özniteliği, anlamlı title, tek h1 ve atlamasız başlık hiyerarşisi, header / nav / main / footer yer işaretleri ve "İçeriğe atla" bağlantısı olsun. Bilgi taşıyan her görselin anlamlı alt metni olsun, süs görselleri alt="" ile gizlensin. Metin kontrastı en az 4.5:1 (büyük metin 3:1), arayüz bileşenleri ve odak göstergesi en az 3:1 olsun; bilgi yalnız renkle verilmesin. Sayfa 320 CSS px genişlikte ve %200 yakınlaştırmada yatay kaydırmasız okunabilsin, metin aralığı artırıldığında içerik kırpılmasın. prefers-reduced-motion'a uy, otomatik oynayan içeriği durdurulabilir yap. WCAG 2.2'nin yeni ölçütlerini (2.4.11 odak gizlenmemeli, 2.5.7 sürükleme alternatifi, 2.5.8 hedef boyutu, 3.2.6 tutarlı yardım, 3.3.7 tekrarlı giriş, 3.3.8 erişilebilir kimlik doğrulama) uygula. Değişiklikleri otomatik araçla (axe vb.) ve elle (klavye + ekran okuyucu) doğrula.`,
 criteria:["Her şablonda lang, anlamlı title, tek h1, atlamasız başlıklar ve header / nav / main / footer yer işaretleri var.","\"İçeriğe atla\" bağlantısı ilk Tab'da görünüyor ve main'e odak taşıyor.","Bilgi taşıyan görsellerin alt metni anlamlı; süs görselleri alt=\"\"; ikon düğmelerin erişilebilir adı var.","Metin kontrastı ≥ 4.5:1 (büyük metin ≥ 3:1), arayüz bileşenleri ve odak göstergesi ≥ 3:1 — açık ve koyu temada ölçüldü.","320 CSS px genişlikte ve %200 yakınlaştırmada yatay kaydırma yok (veri tabloları ve haritalar hariç), içerik kaybolmuyor.","prefers-reduced-motion: reduce iken animasyonlar kapalı ya da azaltılmış; 5 saniyeden uzun otomatik hareket durdurulabiliyor.","Tıklama hedefleri en az 24 × 24 CSS px ya da yeterli boşluklu (2.5.8).","axe (ya da eşdeğeri) taramasında kritik / ciddi ihlal yok; elle klavye ve ekran okuyucu testi raporlandı."],
 images:[{id:"img-1",src:PL_IMG.focus,alt:"Üç düğme: odaksız, mavi halkalı odakta ve outline none ile görünmez odak; altında 24 piksel ve 44 piksel hedef boyutu kareleri ve yapışkan başlığın altında kalmayan odak örneği",caption:"Odak göstergesi, hedef boyutu ve gizlenmeyen odak."}],
 refs:[{t:"W3C — Web Content Accessibility Guidelines (WCAG) 2.2",u:"https://www.w3.org/TR/WCAG22/"},{t:"W3C — How to Meet WCAG (Quick Reference)",u:"https://www.w3.org/WAI/WCAG22/quickref/"},{t:"W3C — Understanding WCAG 2.2",u:"https://www.w3.org/WAI/WCAG22/Understanding/"},{t:"Understanding 2.5.8 Target Size (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html"}],
 doc:`# WCAG 2.2 AA Temel Uyum — Teknik Doküman

## Sayfa iskeleti
\`\`\`html
<html lang="tr">
<body>
  <a class="skip" href="#main">İçeriğe atla</a>
  <header>…<nav aria-label="Ana menü">…</nav></header>
  <main id="main" tabindex="-1"><h1>Sayfa başlığı</h1>…</main>
  <footer>…</footer>
</body>
\`\`\`
- Birden fazla \`nav\` varsa her birine farklı \`aria-label\`.
- Dil değişen bölümlerde \`lang\` (ör. \`<span lang="en">\`).

## Metin alternatifleri
| Görsel türü | Kural |
|---|---|
| Bilgi taşıyan | İşlevi / içeriği anlatan alt metin |
| Süs | \`alt=""\` ya da CSS arka planı |
| İkon düğme | \`aria-label\` ya da görsel olarak gizli metin |
| Grafik / diyagram | Kısa alt + yakında ayrıntılı açıklama ya da tablo |

## Renk ve kontrast
- Normal metin 4.5:1, büyük metin (≈ 24 px ya da 18.66 px kalın) 3:1 (1.4.3).
- Arayüz bileşeni sınırları ve odak göstergesi 3:1 (1.4.11).
- Hata, zorunlu alan, durum yalnız renkle değil, metin ya da ikonla da belirtilir (1.4.1).
- Tasarım token'larında her ön plan / arka plan çifti açık ve koyu tema için ölçülür.

## Yeniden akış ve metin aralığı
- 320 CSS px'te tek sütun; yatay kaydırma yok (1.4.10).
- Satır yüksekliği 1.5, paragraf aralığı 2×, harf 0.12em, kelime 0.16em uygulanınca içerik kırpılmaz (1.4.12) — sabit yükseklikli metin kutusu kullanma.

## Hareket
\`\`\`css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation-duration: .01ms !important;
    animation-iteration-count: 1 !important; transition-duration: .01ms !important;
    scroll-behavior: auto !important; }
}
\`\`\`
- Kaydırıcı / video gibi 5 saniyeden uzun otomatik hareket için durdur düğmesi (2.2.2).

## WCAG 2.2 ile gelen AA ölçütleri
| No | Ölçüt | Uygulama |
|---|---|---|
| 2.4.11 | Odak gizlenmemeli (asgari) | \`scroll-padding-top\` = yapışkan başlık yüksekliği; çerez banner'ı odağı kapatmamalı |
| 2.5.7 | Sürükleme hareketleri | Sürükle-bırak için düğme / seçim alternatifi |
| 2.5.8 | Hedef boyutu (asgari) | 24 × 24 CSS px ya da boşluk istisnası |
| 3.2.6 | Tutarlı yardım | Yardım / iletişim bağlantısı her sayfada aynı yerde |
| 3.3.7 | Tekrarlı giriş | Aynı süreçte girilen bilgi yeniden istenmez, otomatik doldurulur |
| 3.3.8 | Erişilebilir kimlik doğrulama | Bilişsel test yok; yapıştırma ve parola yöneticisi serbest |

## Test
- Otomatik: axe-core / Lighthouse erişilebilirlik — CI'da kritik ihlal kapısı.
- Elle: yalnız klavye ile ana akışlar; NVDA + Firefox / Chrome ve VoiceOver + Safari ile başlık ve yer işareti gezintisi; %200 ve %400 yakınlaştırma.`},
{id:"a11y-klavye-odak",short:"Klavye ve odak",cat:"a11y",version:"1.0.0",updated:PL_D,title:"Klavye Erişimi ve Odak Yönetimi",
 desc:"Bütün işlevlerin yalnız klavyeyle kullanılabilmesini, mantıklı odak sırasını, her zaman görünür ve gizlenmeyen odak göstergesini ve dinamik içerikte odağın doğru yere taşınmasını sağlar.",
 tags:["klavye","odak","focus-visible","tab-sırası","wcag"],deps:["a11y-wcag22-temel"],
 prompt:`Sitedeki her etkileşimi yalnız klavyeyle kullanılabilir yap. Tıklanabilir her öğe yerel button / a / input olsun; div ve span'e onclick verme. Tab sırası görsel okuma sırasını izlesin, pozitif tabindex kullanma. Bütün odaklanabilir öğelerde :focus-visible ile en az 2 px, çevresine karşı en az 3:1 kontrastlı odak göstergesi olsun; outline'ı göstergesiz kaldırma. Yapışkan başlık, çerez banner'ı ya da sohbet balonu odaklanan öğeyi kapatmasın (scroll-padding). Klavye tuzağı olmasın; menü, sekme ve liste kutusu gibi bileşik bileşenlerde ok tuşları ve roving tabindex uygula. Sayfa içi yönlendirme, filtre sonucu, açılan panel ve kapanan pencere sonrasında odağı mantıklı yere taşı ve gerekiyorsa aria-live ile duyur. Tek karakterli kısayollar varsa kapatılabilir ya da değiştirilebilir olsun.`,
 criteria:["Bütün işlevler fare kullanmadan Tab, Shift+Tab, Enter, Space, ok tuşları ve Esc ile yapılabiliyor.","Tıklanabilir div / span yok; etkileşimli öğeler yerel HTML öğesi ya da tam ARIA kalıbı.","Pozitif tabindex yok; odak sırası görsel sırayla aynı.","Her odaklanabilir öğede görünür odak göstergesi var (≥ 2 px, ≥ 3:1); outline: none yalnız yerine gösterge konmuşsa.","Yapışkan başlık ya da banner odaklanan öğeyi tamamen kapatmıyor (2.4.11).","Klavye tuzağı yok; gömülü içerikten (harita, video) Tab ile çıkılabiliyor.","Bileşik bileşenlerde ok tuşları çalışıyor, bileşene tek Tab ile girilip çıkılıyor.","Dinamik değişiklikten sonra (filtre, sayfalama, pencere kapanması) odak tanımlı bir yere gidiyor; sonuç sayısı aria-live ile duyuruluyor."],
 images:[{id:"img-1",src:PL_IMG.focus,alt:"Üç düğme: odaksız, mavi halkalı odakta ve outline none ile görünmez odak; altında hedef boyutu kareleri ve yapışkan başlığın altında kalmayan odak örneği",caption:"Görünür ve gizlenmeyen odak."}],
 refs:[{t:"W3C — ARIA Authoring Practices Guide (APG)",u:"https://www.w3.org/WAI/ARIA/apg/"},{t:"Understanding 2.4.11 Focus Not Obscured (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html"},{t:"W3C — WCAG 2.2",u:"https://www.w3.org/TR/WCAG22/"}],
 doc:`# Klavye Erişimi ve Odak Yönetimi — Teknik Doküman

## Temel kurallar
- Yerel öğe önce: \`<button>\` eylem, \`<a href>\` gezinti. \`role="button"\` gerekiyorsa \`tabindex="0"\` + Enter ve Space işleyicisi.
- \`tabindex\`: yalnız \`0\` (sıraya ekle) ve \`-1\` (programla odak). Pozitif değer yasak.
- DOM sırası = görsel sıra. CSS \`order\` / \`flex-direction: row-reverse\` ile sırayı ters çevirme.

## Odak göstergesi
\`\`\`css
:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
:focus:not(:focus-visible) { outline: none; }
html { scroll-padding-top: var(--header-h); }   /* 2.4.11 */
\`\`\`
- \`--focus\` hem açık hem koyu temada çevresine karşı ≥ 3:1.

## Bileşik bileşenler (roving tabindex)
1. Gruptaki yalnız bir öğe \`tabindex="0"\`, diğerleri \`-1\`.
2. Ok tuşları odağı taşır ve \`tabindex\` değerlerini değiştirir; Home / End uçlara gider.
3. Gruptan Tab ile tek adımda çıkılır.
Kalıplar: sekmeler, menü çubuğu, araç çubuğu, liste kutusu, ağaç — APG'deki klavye tablolarına uyulur.

## Dinamik içerik
| Olay | Odak | Duyuru |
|---|---|---|
| SPA sayfa geçişi | Yeni sayfanın h1'i (\`tabindex="-1"\`) | Sayfa başlığı |
| Filtre uygulandı | Odak yerinde kalır | \`aria-live="polite"\`: "24 sonuç" |
| Pencere kapandı | Açan öğe | — |
| Öğe silindi | Sonraki öğe ya da liste başlığı | "Silindi" |
| Form hatası | Hata özeti | Özet başlığı |

## Test
- Fareyi kaldırıp ana akışları baştan sona tamamla (kayıt, arama, sepet, iletişim).
- Her adımda odağın nerede olduğu görünüyor mu? Yapışkan başlık kapatıyor mu?
- Tab ile sayfa sonuna kadar git ve geri dön; tuzak yok.`},
{id:"a11y-formlar",short:"Formlar",cat:"a11y",version:"1.0.0",updated:PL_D,title:"Erişilebilir Formlar ve Hata Yönetimi",
 desc:"Etiket, yardım metni, otomatik doldurma, zorunlu alan, hata mesajı ve hata özeti kalıplarıyla formların ekran okuyucu, klavye ve bilişsel erişilebilirlik açısından eksiksiz çalışmasını sağlar.",
 tags:["form","etiket","hata-mesajı","autocomplete","aria","wcag"],deps:["a11y-wcag22-temel","a11y-klavye-odak"],
 prompt:`Sitedeki bütün formları erişilebilir hale getir. Her alanın görünür ve programatik olarak bağlı bir label'ı olsun (placeholder etiket yerine geçmesin); yardım metni ve hata mesajı aria-describedby ile alana bağlansın. Kişisel bilgi alanlarında doğru autocomplete değerleri kullan. Zorunlu alanları metinle ("zorunlu" ya da * ve açıklaması) belirt. Doğrulamayı gönderimde yap; hatalı alanda aria-invalid="true" ve sorunu ve çözümü anlatan metin göster, form üstünde alanlara bağlantılı hata özeti çıkar ve odağı özete taşı. Kullanıcının girdiği veriyi hata sonrası silme. Aynı süreçte daha önce girilen bilgiyi yeniden isteme (3.3.7); girişte bilişsel test isteme, parola alanında yapıştırmayı ve parola yöneticilerini engelleme (3.3.8). Radyo ve onay kutusu gruplarını fieldset / legend ile grupla. Başarılı gönderimi aria-live ya da odak taşıyarak duyur.`,
 criteria:["Her alanın görünür label'ı for / id ile bağlı; yalnız placeholder ile etiketlenmiş alan yok.","Yardım ve hata metinleri aria-describedby ile alana bağlı; ekran okuyucu alanla birlikte okuyor.","Ad, e-posta, telefon, adres, posta kodu gibi alanlarda uygun autocomplete değeri var.","Zorunlu alanlar metinle belirtilmiş ve formun başında açıklanmış.","Gönderimde hatalı alanlar aria-invalid=\"true\" alıyor; mesaj sorunu ve çözüm örneğini söylüyor; renk tek gösterge değil.","Form üstünde hata özeti çıkıyor, odak özete gidiyor, özetteki bağlantılar ilgili alana odaklıyor.","Hata sonrası girilmiş değerler korunuyor; aynı süreçte tekrar giriş istenmiyor (3.3.7).","Parola alanında yapıştırma serbest, autocomplete=\"current-password\" / \"new-password\" doğru; CAPTCHA varsa bilişsel test içermeyen alternatif var (3.3.8).","Radyo / onay grupları fieldset + legend ile; başarı mesajı duyuruluyor."],
 images:[{id:"img-1",src:PL_IMG.errors,alt:"Formun üstünde kırmızı çerçeveli hata özeti ve iki bağlantı; altında kırmızı çerçeveli e-posta ve telefon alanları ve uyarı ikonlu çözüm önerili hata mesajları",caption:"Hata özeti + alan altı mesajlar."}],
 refs:[{t:"W3C WAI — Forms Tutorial",u:"https://www.w3.org/WAI/tutorials/forms/"},{t:"MDN — HTML autocomplete attribute",u:"https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Attributes/autocomplete"},{t:"Understanding 3.3.7 Redundant Entry",u:"https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html"},{t:"Understanding 3.3.8 Accessible Authentication (Minimum)",u:"https://www.w3.org/WAI/WCAG22/Understanding/accessible-authentication-minimum.html"}],
 doc:`# Erişilebilir Formlar ve Hata Yönetimi — Teknik Doküman

## Alan kalıbı
\`\`\`html
<div class="field">
  <label for="email">E-posta <span aria-hidden="true">*</span><span class="sr-only">(zorunlu)</span></label>
  <p id="email-help" class="help">Teklifi bu adrese göndereceğiz.</p>
  <input id="email" name="email" type="email" autocomplete="email" required
         aria-describedby="email-help email-err">
  <p id="email-err" class="error" hidden></p>
</div>
\`\`\`
- Hata görününce: \`aria-invalid="true"\`, \`#email-err\` metni dolar ve \`hidden\` kalkar.

## Hata özeti
\`\`\`html
<div id="error-summary" role="alert" tabindex="-1">
  <h2>2 alanda hata var</h2>
  <ul><li><a href="#email">E-posta adresi geçerli değil</a></li>…</ul>
</div>
\`\`\`
- Gönderimde hata varsa özet çizilir ve \`focus()\` edilir; bağlantı tıklanınca alan odaklanır.

## Hata metni yazımı
| Kötü | İyi |
|---|---|
| Geçersiz giriş | Geçerli bir e-posta yazın, ör. ad@alanadi.com |
| Hata! | Telefon numarası 10 haneli olmalı, ör. 5321234567 |
| Zorunlu | Adınızı yazın |

## autocomplete değerleri
\`name\`, \`given-name\`, \`family-name\`, \`email\`, \`tel\`, \`street-address\`, \`address-level1\` (il), \`address-level2\` (ilçe), \`postal-code\`, \`country\`, \`organization\`, \`current-password\`, \`new-password\`, \`one-time-code\`.

## Gruplar
\`\`\`html
<fieldset><legend>İletişim tercihi</legend>
  <input type="radio" id="c1" name="c" value="email"><label for="c1">E-posta</label>
  …
</fieldset>
\`\`\`

## Kimlik doğrulama (3.3.8)
- Parola ve kod alanlarında yapıştırma engellenmez; \`one-time-code\` ile SMS kodu otomatik dolar.
- Bulmaca / resim seçme CAPTCHA'sı tek yol olamaz; görünmez doğrulama (ör. Turnstile) ya da e-posta bağlantısı alternatif olur.

## Test
- Ekran okuyucuyla her alanda etiket + yardım + hata okunuyor.
- Boş formu gönder: odak özete gidiyor, bağlantılar çalışıyor, değerler korunuyor.`},
{id:"a11y-etkilesimli-bilesenler",short:"Bileşenler",cat:"a11y",version:"1.0.0",updated:PL_D,title:"Erişilebilir Etkileşimli Bileşenler",
 desc:"Modal pencere, açılır menü, sekmeler, akordeon ve bildirim gibi etkileşimli bileşenleri WAI-ARIA kalıplarına göre klavye ve ekran okuyucu uyumlu kurar.",
 tags:["modal","dialog","menü","sekme","akordeon","aria","wcag"],deps:["a11y-klavye-odak"],
 prompt:`Sitedeki etkileşimli bileşenleri WAI-ARIA Authoring Practices kalıplarına göre yeniden düzenle. Modal pencerelerde yerel <dialog> ve showModal() kullan; başlığı aria-labelledby ile bağla, açılınca odağı ilk anlamlı öğeye taşı, odağı pencere içinde tut, Esc ile kapat, kapanınca odağı açan öğeye geri ver, arka planı etkileşimsiz yap. Açılır menü ve akordeonda tetikleyici button olsun ve aria-expanded / aria-controls taşısın. Sekmelerde tablist / tab / tabpanel rolleri, aria-selected ve ok tuşlarıyla gezinti olsun. Bildirim ve toast mesajlarını aria-live bölgesiyle duyur, kendiliğinden kaybolan kritik mesaj kullanma. Bileşenleri tek bir bileşen kütüphanesinde topla ve her birinin klavye etkileşim tablosunu belgede yaz.`,
 criteria:["Modal: <dialog> + showModal(); aria-labelledby başlığa bağlı; açılınca odak içeride; Tab döngüsü pencere içinde; Esc kapatıyor; kapanınca odak açan öğede.","Modal açıkken arka plan inert (fare, klavye ve ekran okuyucu ile erişilemiyor), sayfa kaydırması kilitli.","Açılır menü ve akordeon tetikleyicileri button; aria-expanded durumu doğru güncelleniyor; aria-controls panel id'sine bağlı.","Sekmelerde tablist / tab / tabpanel rolleri, aria-selected, ok tuşları ve Home / End çalışıyor; panel sekmeye aria-labelledby ile bağlı.","Bildirimler aria-live=\"polite\" (kritik hata assertive) ile duyuruluyor; kritik mesaj kendiliğinden kaybolmuyor.","Her bileşenin klavye etkileşim tablosu bileşen belgesinde var ve testle doğrulanıyor.","Bileşenler açık ve koyu temada kontrast ölçütlerini sağlıyor; hareketleri prefers-reduced-motion'a uyuyor."],
 images:[{id:"img-1",src:PL_IMG.dialog,alt:"Gri arka plan üzerinde Adresi sil başlıklı pencere: kapatma düğmesi odakta, Vazgeç ve kırmızı Kalıcı olarak sil düğmeleri; Tab döngüsünün pencere içinde kaldığını ve Esc ile kapandığını anlatan notlar",caption:"Modal pencere: odak içeride, arka plan inert, kapanınca odak geri döner."}],
 refs:[{t:"W3C APG — Dialog (Modal) Pattern",u:"https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/"},{t:"W3C APG — Disclosure (Show/Hide) Pattern",u:"https://www.w3.org/WAI/ARIA/apg/patterns/disclosure/"},{t:"MDN — <dialog> element",u:"https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog"},{t:"MDN — inert global attribute",u:"https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Global_attributes/inert"}],
 doc:`# Erişilebilir Etkileşimli Bileşenler — Teknik Doküman

## Modal pencere
\`\`\`html
<button type="button" id="del-open">Adresi sil</button>
<dialog id="del-dlg" aria-labelledby="del-title">
  <h2 id="del-title">Adresi sil</h2>
  <p>Kayıtlı adres kalıcı olarak silinecek.</p>
  <button type="button" value="cancel" autofocus>Vazgeç</button>
  <button type="button" value="ok">Kalıcı olarak sil</button>
</dialog>
\`\`\`
\`\`\`js
const dlg = document.getElementById('del-dlg'), opener = document.getElementById('del-open');
opener.addEventListener('click', () => dlg.showModal());
dlg.addEventListener('close', () => opener.focus());
\`\`\`
- \`showModal()\` arka planı tarayıcı düzeyinde etkileşimsiz yapar ve Esc'i yönetir; özel pencere yazılıyorsa arka plana \`inert\` verilir.
- Yıkıcı işlemde odak "Vazgeç"te başlar.

## Açılır menü / akordeon (disclosure)
\`\`\`html
<button type="button" aria-expanded="false" aria-controls="faq1">Teslimat ne kadar sürer?</button>
<div id="faq1" hidden>…</div>
\`\`\`
- Tıklama \`aria-expanded\`'ı ve \`hidden\`'ı birlikte değiştirir.

## Sekmeler
| Tuş | Davranış |
|---|---|
| ← / → | Önceki / sonraki sekme (sona gelince başa döner) |
| Home / End | İlk / son sekme |
| Tab | Sekme listesinden etkin panele |
Seçim ok tuşuyla otomatik ya da Enter / Space ile elle yapılabilir; panel yükleme gecikmesi varsa elle seçim tercih edilir.

## Bildirimler
\`\`\`html
<div id="toast" role="status" aria-live="polite"></div>
<div id="alert" role="alert"></div>
\`\`\`
- \`#toast\` bilgi mesajları için, \`#alert\` yalnız kritik hatalar için.
- Bölge sayfa yüklenirken DOM'da boş olarak bulunur; metin sonradan yazılır.

## Bileşen belgesi şablonu
Her bileşen için: amaç, HTML yapısı, ARIA öznitelikleri, klavye tablosu, odak davranışı, ekran okuyucu çıktısı, açık / koyu tema kontrastı, hareket davranışı, test senaryoları.

## Test
- Her bileşen yalnız klavyeyle; NVDA ve VoiceOver ile rol, ad ve durum okunuyor.
- Modal açıkken Tab 20 kez basıldığında odak hiç dışarı çıkmıyor.`}
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
plJoin({id:"erisilebilirlik",cat:"a11y",title:"Erişilebilirlik (WCAG 2.2 AA)",
 desc:"Sayfa yapısı, metin alternatifleri, kontrast, yeniden akış, klavye ve odak yönetimi, formlar ve etkileşimli bileşenlerle bütün sitenin WCAG 2.2 AA düzeyinde erişilebilir olmasını sağlayan tek modül.",
 tags:["wcag","erişilebilirlik","klavye","odak","form","aria","modal","kontrast","ekran-okuyucu"],
 prompt:`Sitenin bütün sayfa şablonlarını ve bileşenlerini WCAG 2.2 AA düzeyine getir. Aşağıdaki dört bölümü bu sırayla uygula ve her birini teknik dokümandaki ilgili bölüme göre doğrula:
1. Temel uyum: her sayfada doğru lang, anlamlı title, tek h1 ve atlamasız başlıklar, header / nav / main / footer yer işaretleri ve "İçeriğe atla" bağlantısı olsun. Bilgi taşıyan görsellere anlamlı alt metin ver, süsleri alt="" ile gizle. Metin kontrastı en az 4.5:1 (büyük metin 3:1), arayüz bileşenleri ve odak göstergesi en az 3:1 olsun; bilgi yalnız renkle verilmesin. Sayfa 320 CSS px'te ve %200 yakınlaştırmada yatay kaydırmasız okunsun, metin aralığı artınca kırpılmasın; prefers-reduced-motion'a uy, otomatik hareketi durdurulabilir yap; WCAG 2.2'nin yeni ölçütlerini (2.4.11, 2.5.7, 2.5.8, 3.2.6, 3.3.7, 3.3.8) uygula.
2. Klavye ve odak: her işlev yalnız klavyeyle kullanılabilsin; etkileşimli öğeler yerel button / a / input olsun, pozitif tabindex kullanma, odak sırası görsel sırayı izlesin. :focus-visible ile her zaman görünür odak göstergesi ver; yapışkan başlık ya da banner odağı kapatmasın; klavye tuzağı olmasın; bileşik bileşenlerde ok tuşları ve roving tabindex kullan; dinamik değişiklikten sonra odağı mantıklı yere taşı ve sonucu aria-live ile duyur.
3. Formlar: her alana görünür ve bağlı label ver, yardım ve hata metnini aria-describedby ile bağla, doğru autocomplete değerlerini kullan, zorunlu alanları metinle belirt. Gönderimde hatalı alanlara aria-invalid ve çözüm öneren mesaj ver, form üstünde alanlara bağlantılı hata özeti çıkarıp odağı oraya taşı, girilen veriyi silme; aynı süreçte bilgiyi tekrar isteme, parola alanında yapıştırmayı ve parola yöneticilerini engelleme; grupları fieldset / legend ile kur.
4. Etkileşimli bileşenler: modal pencerede yerel <dialog> + showModal() kullan (başlık aria-labelledby ile bağlı, odak içeride, Esc kapatır, kapanınca odak açan öğeye döner, arka plan etkileşimsiz); açılır menü ve akordeonda aria-expanded / aria-controls, sekmelerde tablist / tab / tabpanel ve ok tuşları; bildirimleri aria-live ile duyur. Bileşenleri tek bileşen kütüphanesinde topla ve her birinin klavye etkileşim tablosunu belgele.
Değişiklikleri axe (ya da eşdeğeri) ile otomatik, yalnız klavye ve ekran okuyucuyla (NVDA, VoiceOver) elle doğrula; kontrastı açık ve koyu temada ölç; doğrulanamayan kriteri gerekçesiyle raporla.`,
 docHead:`# Erişilebilirlik (WCAG 2.2 AA) — Teknik Doküman

## Kapsam ve uygulama sırası
| Sıra | Bölüm | Çıktı |
|---|---|---|
| 1 | Temel uyum | Sayfa iskeleti, metin alternatifleri, kontrast, yeniden akış, hareket |
| 2 | Klavye ve odak | Odak göstergesi, odak sırası, dinamik içerikte odak yönetimi |
| 3 | Formlar | Alan kalıbı, hata özeti, otomatik doldurma, kimlik doğrulama |
| 4 | Etkileşimli bileşenler | Modal, açılır menü, sekmeler, bildirimler |
- Bölümler tek modüldür; sıra, sonraki bölümün öncekinin kurallarını kullanmasından gelir (formlar ve bileşenler klavye / odak kurallarına dayanır).`,
 docTail:`## Ortak test ve teslim
- Otomatik: axe-core / Lighthouse erişilebilirlik taraması CI'da; kritik ve ciddi ihlal yayını durdurur.
- Elle: ana akışlar (kayıt, arama, iletişim, satın alma) yalnız klavyeyle; NVDA + Chrome / Firefox ve VoiceOver + Safari ile başlık, yer işareti, form ve pencere gezintisi; %200 ve %400 yakınlaştırma; açık ve koyu temada kontrast ölçümü.
- Teslimde: kabul kriterleri tablosu (geçti / kaldı / kanıt), bilinen sınırlamalar ve düzeltme planı.`},
 ["a11y-wcag22-temel","a11y-klavye-odak","a11y-formlar","a11y-etkilesimli-bilesenler"]),
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
