# Pazarlama Modülü — Tasarım ve Uygulama Planı (V24)

Durum: **Uygulandı — V24** (2026-10-29). Ayrıntı ve testler: [YOL-HARITASI.md](YOL-HARITASI.md) › V24.

> **Uygulamada plandan farklar:**
> - Alan sayısı 123 (plan "yaklaşık 115").
> - Google Ads'e iş günü bütçe takvimi yazılmaz. Sebep: Google 1 Haziran 2026'dan beri gün bazlı zamanlamada da aylık günlük × 30,4 harcar (Google Ads Yardım 16913225). Meta'ya yazılır.
> - "Emek takibi: Hayır" `isGucu:false` olarak aktarılmaz. Sebep: şablonun `dogrula.mjs`'i bunu reddeder; sekme açık kalır, kartta uyarı çıkar.
> - Blog adresinde `/{kategori}/{slug}/` şablona aktarılamaz; şablon yalnız `{slug}` kalıbını destekler.
> - "Reklam yok" tek başına seçilir (`exclusive`).
> - V20'den beri var olan evet / hayır kural hatası düzeltildi.
> - Sonradan eklenen (kullanıcı isteği): **Hedef Kitle** bölümü (49, 19 karar; eski serbest metin "Kitle Notları ve Persona Açıklaması" olarak korunur) ve Sosyal Medya'da platform başına hesap kutuları (`accounts` tipi); Ölçüm & Raporlama'da Hesap ve Etiket Kimlikleri (`mk_ids`). Pazarlama bölümleri artık 48–66.
Kaynaklar: `~/Downloads/Projeler/icerik_planlama` (İçerik ve Reklam Planı Şablonu 1.44.0, KILAVUZ.md §18 veri şeması, ICERIK-URETIM-REHBERI.md) ve bu şablonla üretilmiş Workland planı.

Kullanıcı kararları:

1. **A + B:** Pazarlama kararları yapılandırıcıda karar bölümleri olarak verilir (A); seçimlerden içerik planı şablonunun veri dosyası üretilir (B).
2. **Kapsam:** şablonun bütün modülleri (15 sekme ve pencere grubu).
3. **Alternatifli seçenekler:** her kararda alternatifler bulunur. Workland'e özgü kurallar (hafta sonu reklam kapalı, yalnız doğrulanmış olgu iddia kuralı, lokasyon × hizmet kampanya yapısı vb.) varsayılan değildir; en fazla alternatiflerden biri olarak yer alır.
4. **Menü:** sol menüde **Ajanlar**'ın altında **Pazarlama** başlığı.

---

## 1. Yerleşim ve gezinme

### 1.1 Sol menü

Alt bölümdeki düğmelere **◈ Pazarlama** eklenir. Sıra: Proje Kuralları · Ajanlar · **Pazarlama** · Dokümantasyon.

**Pazarlama**'ya tıklanınca sol menünün kaydırılan alanı (`#sideNav`) pazarlama bölümlerini gösterir. Görünüm proje menüsüyle aynıdır: kategori başlığı, bölüm, alt kararlar, sayı rozeti. Üstte ince bir şerit vardır: **PAZARLAMA · ← Proje menüsü**. Şeritteki bağlantı, proje menüsünde en son açık olan bölüme döner. Pazarlama düğmesi etkin görünür.

```
┌ W  Web Configurator ─────────────┐
│ [ Menüde ara…                  ] │
│ PAZARLAMA          ← Proje menüsü│
│ STRATEJİ                         │
│  ◎ Pazarlama Planı & Hedefler  7 │
│  ⚑ Rakip Analizi               8 │
│  ▣ Ürün & Hizmet Tanıtımı      7 │
│ İÇERİK                           │
│  ☰ İçerik Stratejisi          10 │
│    · Blog yayın sıklığı          │
│    · …                           │
│  …                               │
├──────────────────────────────────┤
│ ◫ Proje Kuralları                │
│ ◎ Ajanlar                        │
│ ◈ Pazarlama               (etkin)│
│ ⓘ Dokümantasyon                  │
└──────────────────────────────────┘
```

- **Teknik model:** bölümler `area:"marketing"` alır. Menü iki alanı da çizer; açık olmayan alanın grupları gizlenir. Etkin alan, açık bölümün `area` değerinden türer; ayrı bir durum değişkeni yoktur. Başka bir yerden bir pazarlama kararına gidilince (`goToField`, `jump`) menü kendiliğinden pazarlama alanına geçer.
- **Arama:** menü araması iki alanda birden arar. Pazarlama sonuçları "Pazarlama › <kategori>" başlığıyla gelir. Arama temizlenince menü etkin alana döner.
- Alt bölümde bir düğme daha olduğu için `#sideNav`'ın alt boşluğu bir düğme yüksekliği (yaklaşık 39 px) artar. Mobilde menü paneli de aynı şekilde çalışır.

### 1.2 İçerik alanı

Mevcut üç görünüm aynen kullanılır: **rehber** (varsayılan), **tüm kararlar** ve **tek karar**.

- Başlık satırı: `52 — PAZARLAMA · İÇERİK`. Bölüm kodları 00–47'den sonra gelir (48+); sırayla yeniden numaralanır.
- **Önceki / Sonraki** düğmeleri yalnız aynı alan içinde gezer. Son proje bölümü bugünkü gibi "Proje Kurallarını Gör"e gider. Son pazarlama bölümü (Plan Dosyası) da "Proje Kurallarını Gör"e gider.
- **İlerleme çubuğu:** proje alanında hiçbir şey değişmez (yalnız proje kararları sayılır). Pazarlama alanında "Pazarlama · n/N karar · %p" yazar. "Proje Kuralları (n)" sayacı iki alanın toplam kural sayısıdır.
- **Proje kilidi:** pazarlama kararları da `requireProject()` ile korunur. Proje Adı ve proje dosyası olmadan seçim yapılamaz.

### 1.3 Proje Kuralları ve Claude promptu

- **Proje Kuralları sayfası:** proje kural grupları → **PAZARLAMA** ara başlığı → pazarlama kural grupları → ajan grupları.
- **Claude promptu:** `PROJECT RULES` ile `AJAN YAPISI` arasına **`PAZARLAMA VE İÇERİK KURALLARI`** bölümü girer. Bu bölüm yalnız pazarlama kararı varsa eklenir.
- **Pazarlama promptunu kopyala** (Plan Dosyası bölümünde): içerik üretecek Claude oturumu için ayrı bir metin. İçeriği marka özeti (ad, site, ses tonu, hitap, renkler, fontlar; Kurumsal Kimlik'ten), pazarlama kuralları ve seçili Pazarlama kategorisindeki ajanlardır.

### 1.4 Kayıt ve sürüm

- Seçimler mevcut `state` içinde, alan kimliğiyle saklanır. Pazarlama alanlarının ön eki `mk_`'dir. localStorage anahtarı (`web-project-configurator-v16`) değişmez.
- Proje dosyası ve JSON dışa aktarımı `version:24` olur. V23 dosyaları değişiklik gerekmeden açılır. Yeni alanlar yalnız boş görünür.
- `<title>` V24 olur. Görsel değişiklikler yeni `<style id="v24-marketing">` bloğuna yazılır. Koyu tema karşılıkları aynı blokta ve `v17-dark-mode` değişkenleriyle (`--bg`, `--surface`, `--text` …) tanımlanır.

---

## 2. A — Karar bölümleri

Her alan ve her seçenek bugünkü standarda uyar: `explanation` (seçeneğin açıklaması), `scenario` (ne zaman doğru seçim), `example` (nasıl görünür) ve kural şablonu (`rule`; `{label}` / `{booltext}`; gerekirse `ruleDetail`). Boolean alanlarda `yes` / `no` nesneleri doldurulur.

- **Kapı alanları:** modülün kullanılıp kullanılmayacağını soran ilk alandır. Modülün diğer alanları `showIf` ile buna bağlanır. Gizlenen seçimler silinmez (§34).
- **Öneri:** `recommend` yalnız proje türünden (`project_type`) beslenir ve yalnız `select` alanlarda kullanılır.
- **Ortak kararlar tekrarlanmaz.** Bir karar zaten başka bir bölümde veriliyorsa, pazarlama bölümü o karara `jump` bağlantısı koyar:

| Proje bölümündeki karar | Pazarlamada nasıl kullanılır |
|---|---|
| Kurumsal Kimlik: renkler, fontlar, ses tonu, hitap, görsel dili | Tekrar sorulmaz; B dışa aktarımında `marka` alanına aktarılır, promptta marka özeti olur |
| Canlı Site Adresi (`domain_name`) | `marka.site` |
| Analitik aracı, Consent Mode | Ölçüm bölümünden `jump` ile bağlanır |
| İşlemsel E-posta (`mail_provider`) | Mailing bölümü pazarlama e-posta aracını ayrıca sorar; ikisinin farkı açıklamada yazar |
| SEO, Yapısal Veri, GEO | Blog standardındaki meta, SSS, kısa cevap kararları bunlara `jump` ile bağlanır; aynı karar yeniden sorulmaz |
| Gizlilik / KVKK | Mailing, Etkinlik ve Hukuk izin kurallarında bağlanır |

### 2.1 Bölüm kataloğu

Bölüm kodları 48–65 arasıdır (18 bölüm, yaklaşık 115 alan). Satırlardaki "→" işareti B dışa aktarımında hangi şablon anahtarına gittiğini gösterir.

#### STRATEJİ

**48 · Pazarlama Planı & Hedefler** (`mk_plan`) → `pazarlama`

| Alan | Tip | Seçenekler |
|---|---|---|
| Plan dönemi | select | Aylık · Çeyreklik · 6 aylık · Yıllık |
| Pazarlama hedefleri | multiselect | Marka bilinirliği · Potansiyel müşteri (lead) · Online satış · Teklif / randevu talebi · Topluluk ve etkileşim · İşveren markası · Müşteri sadakati |
| Kuzey yıldızı metriği | select | Nitelikli lead · Satış geliri · Organik trafik · Etkileşim oranı · Abone sayısı (öneri: proje türü) |
| Hedef kitle tanımı | textarea | → `marka.kitle` |
| Plan belgeleri | multiselect | Ana plan · Rakip analizi eki · Persona eki · Kanal planı · Bütçe planı · Marka planları → `pazarlama.belgeler` |
| Belge takibi | select | Durum + sorumlu + termin · Yalnız durum · Takip yok |
| Marka yapısı | select | Tek marka · Çok marka (marka bazında plan) |

**49 · Rakip Analizi** (`mk_comp`) → `rakipler`

| Alan | Tip | Seçenekler |
|---|---|---|
| Rakip analizi yapılacak mı | boolean (kapı) | |
| Rakip evreni | select | 5'e kadar doğrudan rakip · 10–20 rakip · Geniş evren (30+) |
| Toplanacak bilgiler | multiselect | Ürün / hizmet · Fiyat · Kanal ve sosyal hesaplar · Şube / lokasyon (Google İşletme Profili) · Reklamlar (Google Reklam Şeffaflık Merkezi, Meta Reklam Kütüphanesi) · SEO (kelime / trafik) · İçerik ve mesaj |
| Kanıt kuralı | select | Her bilgi kaynak bağlantısı ve tarihle · Kaynak isteğe bağlı |
| Önceliklendirme | select | P0–P3 öncelik sınıfı · Doğrudan / dolaylı ayrımı · Sınıflama yok |
| Toplama yöntemi | select | Elle araştırma · Betikle toplama (yalnız herkese açık kaynak, istek aralığı, hizmet şartlarına uyum) · Ücretli araç |
| Güncelleme sıklığı | select | Aylık · Çeyreklik · Kampanya öncesi |
| Karşı aksiyon listesi | boolean | |

**50 · Ürün & Hizmet Tanıtımı** (`mk_prod`) → `urunler`

| Alan | Tip | Seçenekler |
|---|---|---|
| Ürün / hizmet tanıtımı planlanacak mı | boolean (kapı) | |
| Kayıt türleri | multiselect | Hizmet · Ürün · Paket |
| Tanıtım sayfası alanları | multiselect | Slogan · Özet · Değer önerisi · Hedef kitle · Faydalar · Özellikler · Fiyat açıklaması · SSS · Öne çıkan görsel · Sosyal kanıt |
| Fiyat gösterimi | select | Açık fiyat · Başlangıç fiyatı · "Teklif üzerine" |
| Anahtar kelime planı | select | Ürün başına kelime seti (ana + yardımcı) · Yalnız ana kelime · Yok |
| İlişkili içerik bağlantısı | boolean | Blog, paylaşım ve mailing bağı |
| Tanıtım maili | boolean | HTML + düz metin, PDF ek |

#### İÇERİK

**51 · İçerik Stratejisi** (`mk_content`) → `kategoriler`, `haftaSatiri`, `donem.blogYol`

| Alan | Tip | Seçenekler |
|---|---|---|
| Blog yayın sıklığı | select | Haftada 2–3 · Haftada 1 · Ayda 2 · Ayda 1 · Blog yok (öneri: proje türü) |
| Sosyal yayın sıklığı | select | Haftada 1–2 · Haftada 3–4 · Haftada 5+ · Günlük |
| İçerik türetme modeli | select | Her blogdan türeyen paylaşımlar · Bağımsız sosyal takvim · Karma |
| Huni modeli | select | F / D / K · AIDA · TOFU / MOFU / BOFU · Huni etiketi yok |
| İçerik kategorileri | textarea | Satır başına "Ad \| KOD" → `kategoriler` |
| Seri içerik | boolean | Örn. müşteri hikâyesi → `vurgu` |
| İndirilebilir içerik (📥) | boolean | → `dl` |
| Konu kaynakları | multiselect | Anahtar kelime araştırması · Müşteri soruları · Satış ekibi geri bildirimi · Rakip içerik boşluğu · Gündem / sezon · Eski yazıları güncelleme |
| Plan görünümü | select | Hafta görünümü (blog ve paylaşımlar tek satırda) · Ayrı listeler → `haftaSatiri` |
| Mevcut yayınları plana alma | boolean | Site haritasından arşiv, "Yayınlandı" işaretli |

**52 · Blog Yazı Standardı** (`mk_blog`) → `kisaCevapKutusu`, `icindekilerKutusu`

| Alan | Tip | Seçenekler |
|---|---|---|
| Blog alan seti | select | Tam panel seti (19 alan) · Temel set (başlık, slug, meta, özet, odak kelime) |
| Yazı uzunluğu | select | 600–900 · 1000–1500 · 1500–2500 kelime · Konuya göre |
| Yazı blokları | multiselect | Kısa cevap kutusu · İçindekiler · SSS · Kaynaklar · İç linkler · Yazar kutusu · CTA kutusu · Güncelleme tarihi (SEO / GEO'ya `jump`) |
| Blog adresi | select | `/blog/{slug}/` · `/{slug}/` · `/{kategori}/{slug}/` → `donem.blogYol` |
| Kapak görseli | select | 16:9 · 1200×675 WebP · 16:9 · 1920×1080 WebP · 1:1 · 1200×1200 (alt metin her seçenekte zorunlu) |
| Çıktı biçimleri | multiselect | JSON (CMS'e aktarım) · HTML · Düz metin |
| Yazar gösterimi | select | Gerçek yazar + biyografi · Kurumsal editör ekibi · Yazar gösterilmez |
| Yapay zekâ kullanımı | select | Yapay zekâ taslağı + insan editörlüğü ve doğrulama · Yalnız insan · Serbest (açıklama kuralıyla) |

**53 · Sosyal Medya** (`mk_social`) → `mecralar`, `formatlar`, `storySaati`, `marka.etiket`, `marka.hesaplar`

| Alan | Tip | Seçenekler |
|---|---|---|
| Mecralar | multiselect | Instagram · Facebook · LinkedIn · X · YouTube · TikTok · Threads · Pinterest · WhatsApp Kanal · Google İşletme Profili gönderileri |
| Formatlar | multiselect | Reels / kısa video · Carousel · Tek görsel · Story · Uzun video · Metin gönderisi |
| Story kullanımı | select | Her paylaşımın Story sürümü · Yalnız seçili paylaşımlar · Story yok |
| Story saati | select | 18:30 · 12:30 · 09:00 · Ana paylaşımla aynı (kapı: Story açık) |
| Gönderi metni yapısı | select | Kanca + ana mesaj + CTA + etiket · Serbest |
| Etiket politikası | select | Marka etiketi + 3–5 konu etiketi · Yalnız marka etiketi · Etiket yok |
| Marka etiketi | text | Örn. #MarkaAdı → `marka.etiket` |
| Bağlantı kuralı | select | Her gönderide UTM'li bağlantı (bağlantı desteklemeyen mecrada "link profilde") · Yalnız profil bağlantısı |
| Paylaşım saatleri | select | Mecra başına sabit ritim · Platform analizine göre · Serbest |
| Sosyal hesap adresleri | textarea | Satır başına "Ad \| URL" → `marka.hesaplar` |

**54 · Brief & Görsel Üretimi** (`mk_creative`) → `yasaklar`

| Alan | Tip | Seçenekler |
|---|---|---|
| Brief biçimi | select | Kurumsal tek tip brief · Kısa brief · Brief yok |
| Brief numarası | select | Yıl + sıra · Önek + sıra · Numara yok |
| Brief teslimi | multiselect | Word · PDF · Paylaşılan klasör · Proje yönetim aracı |
| Görsel kaynağı | multiselect | Kendi çekim · Tasarımcı · Lisanslı stok · Yapay zekâ (etiketli) (Kurumsal Kimlik › Görsel dili'ne `jump`) |
| Görsel bilgileri | multiselect | Dosya adı · Alt metin · Başlık · Altyazı · Kaynak / lisans · Kişi rızası · Yapay zekâ etiketi |
| Görsel aday seçimi | boolean | Aday + kredi tahmini |
| Paylaşım başına ZIP paketi | boolean | |
| Kullanılmayacaklar | multiselect | Kanıtsız üstünlük iddiası · Onaysız müşteri logosu / adı · Rızasız kişi görüntüsü · Rakip adı · Telifli müzik / görsel · Kaynaksız fiyat / indirim vaadi → `yasaklar` |

#### KANALLAR

**55 · Özel Günler** (`mk_days`) → `ozelGunler`

| Alan | Tip | Seçenekler |
|---|---|---|
| Özel gün takvimi kullanılacak mı | boolean (kapı) | |
| Gün türleri | multiselect | Resmî tatil · Ulusal gün · Anma günü · Dinî bayram · Ticari gün · Meslek günü · Farkındalık günü / haftası · Mali tarihler |
| Mesaj politikası | select | Anma ve yas günlerinde satış mesajı yok · Her günde marka mesajı · Yalnız ticari günlerde |
| Hazırlık süresi | select | 2 hafta önce · 1 hafta önce · Ay başında toplu |

**56 · Mailing** (`mk_mail`) → `mailing`

| Alan | Tip | Seçenekler |
|---|---|---|
| E-posta pazarlaması yapılacak mı | boolean (kapı) | |
| Mail türleri | multiselect | Bülten · Blog özeti · Ürün / hizmet tanıtımı · Etkinlik daveti · Otomatik akış · Kampanya duyurusu |
| Sıklık | select | Haftalık · 2 haftada bir · Aylık · Kampanya bazlı |
| Düzen | select | Tek konu · Çok bölümlü bülten |
| Biçimler | multiselect | HTML · Düz metin · PDF ek |
| İzin ve uyum | multiselect | İYS kaydı · Çift onay · Her mailde abonelikten çıkma · Gönderen kimliği ve adres · Segment bazlı gönderim |
| Gönderim aracı | select | Mailchimp · Brevo · EuroMsg · HubSpot · Klaviyo · Kendi sistemimiz · Diğer |

**57 · Etkinlikler** (`mk_events`) → `etkinlikler`

| Alan | Tip | Seçenekler |
|---|---|---|
| Etkinlik yapılacak mı | boolean (kapı) | |
| Etkinlik türleri | multiselect | Webinar · Seminer / konferans · Fuar · Lansman · Atölye · Müşteri buluşması |
| Aktivite planı | select | Standart plan (öncesi / sırası / sonrası) · Kısa plan · Plan yok |
| Duyuru kanalları | multiselect | E-posta · Sosyal medya · Site · Reklam · İş ortakları |
| Kayıt ve kişisel veri | multiselect | Aydınlatma metni · Pazarlama izni ayrı onay · Katılımcı listesi saklama süresi · Çekim bildirimi |
| Etkinlik sonrası | multiselect | Kayıt / sunum paylaşımı · Memnuniyet anketi · Lead takibi · Etkinlik raporu |

#### REKLAM

**58 · Reklam Ortak Kuralları** (`mk_ads`)

| Alan | Tip | Seçenekler |
|---|---|---|
| Reklam kanalları | multiselect (kapı) | Google Ads · Meta Ads · LinkedIn Ads · TikTok Ads · Reklam yok |
| Reklam metni iddia kuralı | select | Yalnız sitede doğrulanmış olgular · Kaynağı gösterilen fiyat ve kampanya bilgisi · Hukuk onayıyla serbest |
| Yayın günleri | select | Her gün · Yalnız hafta içi (günlük bütçe iş gününe bölünür) · Saat bazında zamanlama |
| Açılış sayfası | select | Reklam başına ilgili hizmet / lokasyon sayfası · Kampanyaya özel açılış sayfası · Ana sayfa |
| Bütçe dağılımı | select | Arama ağırlıklı · Dengeli · Sosyal ağırlıklı |
| Tempo kontrolü | select | Haftalık · 2 haftada bir · Aylık |

**59 · Google Ads** (`mk_gads`, kapı: Reklam kanalları ∋ Google Ads) → `ads`

| Alan | Tip | Seçenekler |
|---|---|---|
| Kampanya türleri | multiselect | Arama Ağı · Maksimum Performans · Yeniden pazarlama · Görüntülü · YouTube · Demand Gen · Alışveriş |
| Kampanya yapısı | select | Hizmet bazında · Lokasyon × hizmet · Tek kampanya |
| Marka, rakip ve çakışma | multiselect | Ayrı marka kampanyası · Rakip kampanyası (hukuk kontrolüyle) · Kampanyalar arası negatif kelime · Hesap düzeyi negatif liste |
| Teklif stratejisi | select | Tıklamaları en üst düzeye çıkar + maks. TBM (dönüşüm ölçümü yokken) · Dönüşümleri en üst düzeye çıkar · Hedef EBM · Manuel TBM |
| Öğeler | multiselect | Site bağlantıları · Açıklama metinleri · Görsel · İşletme adı ve logo · Arama · Fiyat / promosyon · Mesaj (WhatsApp) |
| Dil | select | Yalnız Türkçe · Türkçe + İngilizce |
| Aylık bütçe (TL) | text | → `ads.butceToplam`; günlük bütçe yayın günlerine göre hesaplanır → `ads.butceTakvim` |

**60 · Meta Ads** (`mk_meta`, kapı: Reklam kanalları ∋ Meta Ads) → `meta`

| Alan | Tip | Seçenekler |
|---|---|---|
| Kampanya amaçları | multiselect | Anlık Form (lead) · WhatsApp / Messenger mesaj · Web sitesi dönüşümü · Trafik · Video kitlesi · Yeniden hedefleme · Katalog satışı |
| Ön koşullar | multiselect | Meta Pixel · Conversions API · Canlı gizlilik / aydınlatma sayfası · Doğrulanmış alan adı · Business Manager yetkileri → `meta.onkosul` |
| Kitle | multiselect | Konum + ilgi alanı · Benzer kitle · Site ziyaretçisi · Rızalı müşteri listesi · Advantage+ geniş kitle |
| Kreatif ölçüleri | multiselect | 4:5 görsel · 1:1 görsel · 9:16 video · Carousel |
| Anlık Form ayarları | multiselect | Yüksek niyet (inceleme ekranı) · Özel sorular · Teşekkür ekranı CTA · KVKK onay kutusu (kapı: amaç ∋ Anlık Form) |
| Aylık bütçe (TL) | text | → `meta.butce.toplam` |

#### ÖLÇÜM

**61 · Ölçüm & Raporlama** (`mk_measure`) → `donem.utm`, istatistik bölümleri

| Alan | Tip | Seçenekler |
|---|---|---|
| Ölçülecek veriler | multiselect | Sosyal mecra (dönemsel) · Gönderi bazında · Takipçi · Blog sayfası · Google Ads · Meta Ads |
| Rapor ritmi | select | Haftalık + aylık özet · Yalnız aylık · Kampanya sonunda |
| Dönüşüm olayları | multiselect | Form gönderimi (GA4 `generate_lead` + Meta `Lead`) · Telefon tıklaması · WhatsApp tıklaması · E-posta tıklaması · Dosya indirme · Satın alma (Analitik'e `jump`; sitede kodlanacak olaylar olarak proje kuralına da yazılır) |
| UTM standardı | select | Standart şema (kaynak = mecra, ortam = social / cpc / email, kampanya = dönem) · Yalnız kampanya etiketi · UTM yok |
| UTM kampanya adı | text | → `donem.utm` |
| Rapor çıktıları | multiselect | PDF rapor · Yönetici özeti · CSV · Takvim (.ics) |
| Veri girişi | select | Elle giriş (şablon) · Platform dışa aktarımlarından içe alma · API bağlantısı |
| Yedek | select | Tek sorumlu + değişiklik hatırlatıcısı · Paylaşılan klasörde haftalık yedek · Yedek yok |

#### SÜREÇ & EKİP

**62 · İş Akışı & Onay** (`mk_flow`) → `akis`, `yayinlandiKutusu`

| Alan | Tip | Seçenekler |
|---|---|---|
| Onay akışı | select | Taslak → Onay → Yayın · Taslak → Hukuk → Onay → Yayın · Onaysız |
| Hukuk onayı zorunlu | boolean | → `akis.hukukZorunlu` (kapı: akış hukuklu) |
| Yayınlandı işareti ve "Tarihi geçti" uyarısı | boolean | → `yayinlandiKutusu` |
| Kim / ne zaman geçmişi | boolean | |
| Onaylayanlar | multiselect | Pazarlama yöneticisi · Marka sahibi / genel müdür · Hukuk · Ürün sorumlusu |

**63 · Hukuk Değerlendirmesi** (`mk_legal`) → `hukuk`

| Alan | Tip | Seçenekler |
|---|---|---|
| Hukuk değerlendirmesi olacak mı | boolean (kapı) | |
| Hukuka gidecek içerikler | multiselect | Tüm içerikler · Reklam metinleri · Ürün / fiyat içerikleri · Karşılaştırmalı içerik · Kişisel veri veya müşteri adı içeren içerik · Düzenlenmiş sektör konuları · Etkinlik kayıt formları |
| Durum seti | select | Altı durum (Beklemede · İncelemede · Uygun · Şartlı uygun · Düzeltme gerekli · Uygun değil) · İki durum (Uygun · Uygun değil) |
| Dayanaklar | multiselect | KVKK · Ticari Reklam ve Haksız Ticari Uygulamalar Yönetmeliği · 6502 Tüketicinin Korunması · 6563 Elektronik Ticaret / İYS · 5846 FSEK |
| Değerlendiren | select | Kurum içi hukuk · Dış avukat · Uyum sorumlusu → `hukuk.birim` |

**64 · İş Gücü & Roller** (`mk_labor`) → `isGucu`

| Alan | Tip | Seçenekler |
|---|---|---|
| Emek takibi | boolean (kapı) | |
| Birim | select | Dakika · Saat |
| Maliyet | select | Saat ücretiyle tahmini maliyet · Hesaplanmaz |
| Saat ücreti (TL) | text | → `isGucu.saatUcreti` (kapı: maliyet hesaplanır) |
| Roller | multiselect | İçerik editörü · Metin yazarı · Grafik tasarımcı · Video editörü · Sosyal medya uzmanı · Reklam uzmanı · SEO uzmanı · Hukuk · Pazarlama yöneticisi |

#### PLAN DOSYASI

**65 · Plan Dosyası & Dışa Aktarım** (`mk_planfile`): B'nin bölümü.

| Alan | Tip | Not |
|---|---|---|
| Marka adı | text | Boşsa Proje Adı → `marka.ad` |
| Seri no öneki | text | 2–5 büyük harf, Türkçe karakter ve boşluk yok (uyarılı) → `marka.onek` |
| Slogan | text | → `marka.slogan` |
| Dönem etiketi ve başlangıç | text | "2026 Q4", "YYYY-AA-GG" → `donem` |
| İletişim | textarea | Telefon / e-posta / adres → `marka.telefon/eposta/adres` |

> Bölüm sayısı, Plan Dosyası ile birlikte 18'dir (48–65). Kategoriler: Strateji 3 · İçerik 4 · Kanallar 3 · Reklam 3 · Ölçüm 1 · Süreç & Ekip 3 · Plan Dosyası 1.

### 2.2 Bölüm rehberleri

Her pazarlama bölümüne `sectionGuides` kaydı yazılır: `purpose`, `criteria[]`, `pitfalls[]`, `resources[]`. Kaynak adresleri eklenmeden önce gerçekten açılarak doğrulanır. Aday kaynaklar:

- Google Ads Yardım Merkezi
- Meta İşletme Yardım Merkezi
- İYS
- KVKK Kurumu
- Ticaret Bakanlığı Reklam Kurulu
- Google Search Central
- Google Analytics 4 olay belgeleri

### 2.3 Ajan bağlantısı (isteğe bağlı küçük ekleme)

Pazarlama bölümlerinin rehberinde **İlgili ajanlar** kartı gösterilir. Kartta mevcut Pazarlama kategorisindeki ajanlar listelenir (`sosyal-medya`, `icerik-yazari`, `seo-geo`, `kampanya-analist`, `bulten`, `analitik`, `cro-uzmani`, `seo-oneri`). Her birinin yanında "Ajanlar'da aç" bağlantısı olur. Yeni ajan eklenmez.

---

## 3. B — İçerik planı veri dosyası

**Plan Dosyası** bölümünün rehber görünümünde bir dışa aktarım kartı yer alır:

```
┌ İÇERİK PLANI ŞABLONU İÇİN VERİ ────────────────────────────┐
│ Şablon sürümü: 1.44.0 · Etkin modüller: Konular, Takvim,   │
│ Kılavuz, Google Ads, Mailing, Hukuk …                      │
│ ⚠ Eksik: Seri no öneki · Sosyal hesap adresleri            │
│ [ Veri dosyasını indir (.json) ]  [ Şablona yerleştir… ]   │
│ [ Pazarlama promptunu kopyala ]                            │
│ Nasıl kullanılır? (açılır: build.mjs yolu / şablona yapıştırma) │
└────────────────────────────────────────────────────────────┘
```

- **Veri dosyasını indir:** şablonun §18 şemasına uygun `veri.<önek>.json` dosyasını indirir.
- **Şablona yerleştir:** kullanıcı `icerik-plani-SABLON.html` dosyasını seçer. Araç dosyadaki `<script id="veri" type="application/json">` bloğunu üretilen veriyle değiştirir (`</script>` → `<\/script>`) ve `<önek>-icerik-plani.html` olarak indirir. Şablon WP-OnKe'ye gömülmez.

**Eşleme** (§2.1'deki "→" satırları; özet):

| Şablon anahtarı | Kaynak |
|---|---|
| `marka.ad`, `marka.onek`, `marka.slogan` | Plan Dosyası; marka adı boşsa Proje Adı |
| `marka.site` | Canlı Site Adresi (`https://` eklenir) |
| `marka.telefon`, `eposta`, `adres` | Plan Dosyası › İletişim |
| `marka.etiket`, `marka.hesaplar` | Sosyal Medya |
| `marka.renk` | `ana` = ana marka rengi · `vurgu` = vurgu rengi · `zemin` = nötr seçimine göre açık ton |
| `marka.renkler` | Ana / ikincil / vurgu rengi kartları |
| `marka.yaziTipi` | Başlık + metin fontu |
| `marka.kitle` | Pazarlama Planı › Hedef kitle |
| `donem` | Plan dönemi, etiket, başlangıç, UTM kampanya adı; `surum` = dışa aktarım tarihi; `blogYol` |
| `kategoriler` | İçerik Stratejisi (seri ve satış mesajsız kategori bayraklarıyla) |
| `mecralar` | Seçilen mecralar; karakter sınırı ve istatistik alanları şablonun kendi varsayılanlarından (DATA'ya `marketingTemplate` olarak kopyalanır, şablon 1.44.0) |
| `formatlar` | Seçilen formatlar (`R`, `C`, `T`, `S`), şablon varsayılanlarıyla |
| `storySaati`, `yasaklar` | Sosyal Medya, Brief & Görsel |
| `ads` | Google Ads: hedef, işletme adı (≤25 karakter), ayarlar, bütçe toplamı, bütçe takvimi, kampanya iskeletleri (`id`, `ad`, `tur`, boş `gruplar`) |
| `meta` | Meta Ads: ön koşullar, kampanya iskeletleri, bütçe |
| `urunler`, `mailing`, `etkinlikler`, `hukuk`, `isGucu`, `rakipler`, `pazarlama`, `ozelGunler` | Modülün kapısı açıksa eklenir, kapalıysa anahtar hiç yazılmaz. Şablon, sekmeyi anahtarın varlığına göre açar. |
| `akis`, `yayinlandiKutusu`, `haftaSatiri`, `kisaCevapKutusu`, `icindekilerKutusu` | İş Akışı, İçerik Stratejisi, Blog Standardı |
| `bloglar`, `paylasimlar` | Boş liste. İçerik üretimi şablonda ya da pazarlama promptuyla yapılır. |
| `yardim` | `{url:"kullanim-kilavuzu.html"}` |

**Kabul ölçütleri:**

- Üç senaryoda üretilen dosya `node kaynak/dogrula.mjs <dosya>` ile **0 HATA** verir: bütün modüller açık, bütün modüller kapalı, karışık.
- "Şablona yerleştir" çıktısı başsız Chrome'da açılınca kırmızı `HATA:` şeridi ve `Uncaught` olmaz. Seçilen modüllerin sekmeleri görünür, seçilmeyenlerinki görünmez.

---

## 4. Teknik değişiklik listesi

| Yer | Değişiklik |
|---|---|
| `DATA.sections` | 18 bölüm: `area:"marketing"`, `group` = pazarlama kategorisi, kod 48–65 |
| `DATA.fields` | Yaklaşık 115 alan (`mk_` ön eki) ve seçenekleri; hepsinde senaryo, örnek ve kural |
| `DATA.sectionGuides` | 18 rehber |
| `DATA.marketingTemplate` | Şablonun mecra ve format varsayılanları, şablon sürümü |
| `MENU_ICONS` | 18 ikon |
| HTML | `#sideMarketingBtn` (alt bölüm), Dokümantasyon sayfasına "Pazarlama" kartı |
| JS | `areaOf()`, `renderSideNav` (iki alan + arama), alt bölüm düğmesi, `renderStepNav` (alan içi), `renderProgress` (alan bazında), `renderConfig` başlık satırı, `renderRules` + master prompt bölümü, `mkPrompt()`, `mkPlanData()`, `mkDownload()`, `mkFillTemplate()`, `mkExportBox()`, `projectFileData` `version:24` |
| CSS | `<style id="v24-marketing">`: alan şeridi, dışa aktarım kartı, koyu tema karşılıkları |
| Belgeler | `CLAUDE.md` (alan modeli, `mk_` ön eki, dışa aktarım), `YOL-HARITASI.md` (V24), `MASTER-PROMPT.md`'ye yeni bölüm (Pazarlama modülü kapsamı), bu plan |

**Tahmini boyut:** yaklaşık +400 KB, büyük kısmı açıklama, senaryo ve örnek metinleri. Dosya 2,1 MB'tan yaklaşık 2,5 MB'a çıkar.

---

## 5. Uygulama fazları

Her fazdan önce `_yedek/`'e tarihli kopya alınır. Düzenleme Python ile yapılır: tam eşleşme ve "metin dosyada tam 1 kez geçer" doğrulaması (`python3 -I`). Her faz sonunda doğrulama yapılır.

1. **Altyapı:**
   - Alan modeli, alt bölüm düğmesi, menü şeridi, arama, önceki / sonraki, ilerleme, kurallar ve prompt.
   - Bölüm başına bir alanlık iskeletle test edilir.
2. **Strateji + İçerik:** 48–54 bölümlerinin alanları, seçenekleri ve rehberleri.
3. **Kanallar + Reklam:** 55–60.
4. **Ölçüm + Süreç & Ekip:** 61–64.
5. **Plan Dosyası ve B:**
   - Dışa aktarım ve şablona yerleştirme.
   - Pazarlama promptu.
   - `dogrula.mjs` ile kabul testi.
6. **Belgeler ve son regresyon.**

2–4. fazlardaki metinler paralel yazılabilir: her bölüm grubu ayrı bir taslak JSON olur, birleştirme ve doğrulama tek elden yapılır.

---

## 6. Doğrulama planı

**Mevcut regresyon listesi (§41):** sidebar, gezinme, seçenek seçimi, kural üretimi, localStorage, JSON dışa / içe aktarma, Claude promptu, responsive. Açık ve koyu temada, 1440 ve 700 px'de.

**Yeni senaryolar:**

- Pazarlama ↔ Proje menüsü geçişi.
- 18 bölüm ileri / geri; tek karar zincirinde alan sınırı.
- `jump` ile alanlar arası geçiş.
- İki alanda arama.
- Her kapı alanı için `showIf` ve "N önceki kararınız gizlendi" notu.
- `recommend`.
- Kilit.
- Proje dosyasında `mk_` alanları ve `version:24`.
- V23 dosyasını içe aktarma.
- Proje alanında ilerleme sayısının değişmemesi.

**B:** `dogrula.mjs` üç senaryo ve şablona yerleştirme çıktısının başsız Chrome kontrolü (§3).

---

## 7. Riskler ve notlar

- **Eşzamanlı düzenleme:** 29 Ekim 2026, 15:27'de `web-proje-gelistirme.html` başka bir oturumda değişiyordu (robots / sitemap; alan sayısı 162 → 164). Uygulama, o oturum bitip dosya sabitlendikten sonra başlamalı. Aksi hâlde iki oturumun yazmaları birbirini ezer.
- **Şablon bağımlılığı:** B, şablonun 1.44.0 veri şemasına bağlıdır. Şablonda MAJOR sürüm değişirse eşleme güncellenmelidir. `marketingTemplate.surum` bu kontrol için tutulur.
- **"Pazarlama" adı:** CMS Modülleri'ndeki "Pazarlama" (panel modülü) ile karışmasın diye pazarlama kuralları "Pazarlama planı" diliyle yazılır.
- **Hukuki metinler:** Hukuk ve Mailing bölümlerindeki mevzuat adları genel bilgidir; kural metinleri bağlayıcı hukuki tavsiye gibi yazılmaz.
