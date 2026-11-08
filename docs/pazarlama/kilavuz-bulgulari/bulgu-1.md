# Bulgu 1 — Blog, Sosyal Medya, İçerik Yayım ve Dağıtım kılavuzları

Okunanlar (tamamı): `Blog_Yazisi_Olusturma_Kilavuzu.txt` (305 satır), `Sosyal_Medya_Icerik_Olusturma_Kilavuzu_V2.txt` (1000 satır), `Icerik_Yayim_ve_Dagitim_Kilavuzu_Kurumsal.txt` (607 satır), `alan-envanteri.md` (531 satır). Mevcut alanların kural / `ruleDetail` metinleri DATA'dan salt okunarak karşılaştırıldı (52, 53, 54, 55, 57, 62, 63, 09, 07). İçerik planı şablonunun 19 blog alanı ve ölçüleri `~/Downloads/Projeler/icerik_planlama/KILAVUZ.md` §7.2'den okundu (salt okuma).

Kılavuzlarda geçen şirket adı (rasyotek.com.tr örnek adresi, "Rasyotek İçerik Yayım Kılavuzu", sgk / bordro kampanya adları) hiçbir öneride seçenek ya da varsayılan yapılmadı.

---

## KILAVUZ 1 — Blog Yazısı Oluşturma Kılavuzu

### 1. Özet

**Amaç:** "her blog içeriğinin yalnızca bilgi veren bir yazı değil, aynı zamanda marka uzmanlığını güçlendiren, kullanıcıyı doğru aksiyona yönlendiren ve web sitesi performansına katkı sağlayan stratejik bir içerik varlığı olarak üretilmesini sağlamak".

**Bölümler (sırasıyla):** 1 Amaç · 2 Kapsam (8 yazı türü) · 3 Üretim süreci / 3.1 Ön hazırlık (10 brief alanı) · 4 SEO ve sayfa meta alanları · 5 Öne çıkan görsel · 6 Video kullanımı · 7 İçerik mimarisi (7.1 Hero, 7.2 Giriş, 7.3 Gelişme, 7.4 Sonuç) · 8 H etiket yapısı · 9 Kopyalanabilir içerik formatı (şablon) · 10 İç linkleme · 11 Dış kaynak · 12 SSS · 13 Hizmet odaklı ek modüller · 14 CTA standardı · 15 WordPress yayına alma · 16 RankMath SEO ayarları · 17 Yayın öncesi SEO alanı kontrolü · 18 Son checklist · 19 Yayınlama ve yayın sonrası (19.1 zamanlama, 19.2 kontrol) · 20 İçerik kalite standardı.

**Sayısal standartlar:**
| Öğe | Standart |
|---|---|
| URL slug | en çok 75 karakter, ideal 30–60; küçük harf, tire, Türkçe karakter / boşluk / alt çizgi / özel karakter yok |
| Anahtar kelime / odak kelime | en çok 3 kelime |
| Meta title | 35–60 karakter (boşluk dahil), 285–580 px |
| Meta description | 120–160 karakter, 680–920 px (RankMath: 160'ı aşmamalı) |
| Sayfa özet yazısı | 40–60 kelime |
| Hero ana başlık | en çok 6 kelime; alt başlık en çok 6–7 kelime; açıklama 40–60 kelime |
| Gelişme paragrafı | ortalama 60 kelime |
| Başlıklar (H1–H6) | en çok 64 karakter; H1 sayfada tek |
| Öne çıkan görsel | 16:9, tercihen 1920×1080, .webp |
| WordPress etiketi | ana anahtar kelime + 2–3 ek etiket |
| TOC | uzun yazılarda H2/H3'e göre |

**Süreç:** ön hazırlık (konu, kitle, kelime, amaç, CTA) → SEO alanları → görsel / video → içerik mimarisi (hero → giriş → gelişme → sonuç) → H yapısı → şablona göre yazım → iç link, dış kaynak, SSS, hizmet modülleri, CTA → WordPress'e ekleme (yazı, kategori, etiket, özet, görsel) → RankMath (odak kelime, SEO başlığı, açıklama, schema, OG) → yayın öncesi SEO kontrolü + son checklist → zamanlama (sosyal, mailing, WhatsApp Business ile uyumlu) → yayın sonrası kontrol (URL, mobil/masaüstü, linkler, görsel, UTM'li kısa link, sosyal ekibe iletme, diğer kanallara yönlendirme).

**Uyum maddeleri:** Dış kaynakta resmî / .gov / .edu / meslek kuruluşu / mevzuat öncelik; ticari siteler öncelikli kaynak değil. Logo "Briefte belirtilmedikçe otomatik eklenmemelidir." Fiyat içermeyen paket karşılaştırması. Yazım ve imla kontrolü. (KVKK / İYS / hukuk onayı bu kılavuzda yok.)

### 2. A sınıfı bilgiler

| Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|
| "Kurumsal blog yazıları / Hizmet tanıtım odaklı blog içerikleri / Mevzuat, duyuru ve güncel gelişme yazıları / Rehber içerikler / Karşılaştırma içerikleri / Soru-cevap odaklı bilgilendirme yazıları / Kampanya veya lead toplama destekli blog içerikleri / SEO odaklı kategori destek yazıları" | `mk_categories` (konu kategorisi, serbest metin) — **yok** (yazı *türü* kararı yok) | Yazı türü seti yok; tür, kaynak ve modül kuralını değiştiriyor |
| "URL Slug: Maksimum 75 karakter olmalıdır. İdeal uzunluk 30-60 karakter aralığıdır." / "Meta Title: Boşluklar dahil minimum 35, maksimum 60 karakter … minimum 285 px, maksimum 580 px" / "Meta Description: … minimum 120, maksimum 160 karakter … minimum 680 px, maksimum 920 px" / "Sayfa Özet Yazısı: 40-60 kelime" / "Anahtar Kelime: Maksimum 3 kelime" / "Başlıklar maksimum 64 karakter olmalıdır." | `mk_blog_fieldset` — **kısmi**: kural "meta başlık ve meta açıklama SEO / Semantik bölümündeki standarda göre yazılır" diyor ama 09 seo'da uzunluk standardı yok; plan şablonunun 19 alanı farklı ölçü kullanıyor (Meta Title 45–60, Meta Description 140–160, slug 20–60, özet 40–70 kelime, odak kelime 2–5 kelime) | Kurumun ölçü standardı seçilemiyor; piksel sınırı hiç yok |
| "Yayın öncesinde SEO alanlarının hem karakter hem de piksel uzunlukları kontrol edilmelidir." | `mk_blog_fieldset` kural: "karakter ve kelime aralıkları yol göstericidir, yayın engeli değildir"; `seo_gate` (proje) — **kısmi** | Piksel kontrolü yok |
| "Görsel Boyutu: 16:9 formatında, tercihen 1920x1080 px" / "Dosya Formatı: .webp" | `mk_blog_cover` = `w1920` — **tam** | — (kılavuz varsayılanı w1920) |
| "Dosya Adı / Alternatif Metin / Başlık / Alt Yazı / Açıklama" (görsel alanları); "Alternatif metin, başlık, alt yazı ve açıklama alanları doldurulur." | `mk_visual_meta` (filename, alt, title, caption, license, consent, ai_label) — **kısmi** | "Açıklama" (medya açıklaması) seçeneği yok |
| "Logo Kullanımı: Briefte belirtilmedikçe otomatik eklenmemelidir." | **yok** | Görselde logo politikası yok (sosyal kılavuzla ortak — aşağıda `mk_logo_use`) |
| "Blog içinde video kullanılacaksa video başlığı, alt yazısı ve açıklaması ayrı şekilde hazırlanmalı" | `video_seo` (proje) — **kısmi**; `mk_blog_blocks`'ta video bloğu yok | Blok seçeneği yok |
| "Ana Başlık: Maksimum 6 kelime" / "Kısa Alt Başlık: Maksimum 6-7 kelimelik" / "Açıklama Metni: Ortalama 40-60 kelime" (Hero) | **yok** | Hero bloğu yok |
| "Table of Content: Uzun yazılarda H2 ve H3 başlık yapısına göre içindekiler alanı oluşturulmalıdır." | `mk_blog_blocks` = `toc` — **tam** | — |
| "SSS" bölümü (§12) | `mk_blog_blocks` = `faq` — **tam** | ruleDetail'e "marka yönlendirmesi son soruda" eklenebilir (C) |
| "İLGİLİ BLOG YAZILARI / İÇ LİNKLER • [Hizmet sayfası linki] • [İlgili blog linki] • [Kategori linki]" | `mk_blog_blocks` = `internal` — **kısmi** | Yazı sonu "İlgili yazılar" listesi ayrı blok değil |
| §13 "Hizmet Özeti / Fiyatlandırma / Paket Karşılaştırması / Teknik Bilgiler ve Metodoloji / Neden Bu Hizmet? / Referanslar ve Başarı Hikayeleri / Uzman Kadro" | **yok** (`social_proof` proje düzeyinde yalnız hizmet sayfası) | Hizmet odaklı yazı modülleri yok |
| "Gerekli durumlarda fiyat içermeyen paket karşılaştırması yapılabilir. Paket A, Paket B, Paket C ve Enterprise/Kurumsal Paket yapısı kullanılabilir." | `mk_prod_price` (51) — **kısmi** | Blogda fiyatsız paket karşılaştırması kuralı yok |
| "CTA Metni: Teklif Alın / Danışmanlık Talep Edin / Bize Ulaşın / Formu Doldurun / Detaylı Bilgi Alın / Randevu Oluşturun / Hizmeti İnceleyin" | `mk_blog_blocks` = `cta_box` ("3–6 kelimelik … çağrı") — **kısmi** | Kurumun onaylı CTA ifadeleri listesi yok |
| "CTA: [CTA_METNİ] Link: [CTA_LINK] Telefon: [TELEFON_NUMARASI]" / "Telefon: CTA ile birlikte kullanılacak kurumsal telefon numarası" | `mk_contact` (77, serbest metin, çok satır) — **kısmi** | CTA'da hangi telefonun kullanılacağı ve CTA'nın telefonla birlikte verilip verilmeyeceği kararı yok |
| "CTA başlık altında, içerik ortasında ve yazı sonunda stratejik olarak kullanılabilir." | `cta_box` — **kısmi** | CTA konumları belirtilmiyor (ruleDetail) |
| "Etiket Ekleme: Ana anahtar kelime ve yazı kapsamını anlatan 2-3 ek etiket girilir." | `mk_blog_fieldset` (etiketler alanı var, sayı yok) — **kısmi** | Sayı standardı (limit alanına katılır) |
| "RankMath SEO Ayarları … Odak Anahtar Kelime … SEO Başlığı … Açıklama … Schema … OG Ayarları" | `cms_mode` = WordPress (06); SEO eklentisi kararı **yok** | Paneldeki SEO eklentisi seçilemiyor (aşağıda isteğe bağlı öneri) |
| "OG Ayarları: Sosyal medya paylaşım başlığı ve görseli kontrol edilmelidir." | 19 alanlı sette OG yok — **yok** | Paylaşım önizleme alanları |
| "Dış kaynak … Resmi kurum web siteleri, .gov ve .edu uzantılı kaynaklar … öncelikli olmalıdır. Ticari web siteleri kaynak olarak öncelikli tercih edilmemelidir." | `mk_blog_blocks` = `sources` ("en az biri resmî") — **kısmi** | Ticari site önceliği kuralı yok (ruleDetail) |
| "Blog yazısı yayın takvimine göre planlanmalı … Yayın tarihi ve saati sosyal medya, mailing ve WhatsApp Business dağıtımıyla uyumlu olmalıdır." | `mk_derive` hub ("paylaşım, kaynak yazı yayınlanmadan yayınlanmaz") — **kısmi** | Kanal dağıtım seti yok (yayım kılavuzunda `mk_cross_derive`) |
| "UTM kodlu kısa link oluşturulur." | `mk_utm`, `mk_links` — **kısmi** | Kısa link kararı yok (`mk_shortlink`) |

### 3. Yeni alan önerileri (Blog)

Bölüm: **53 mk_blog** (grup İçerik). Mevcut 8 alan + 3 = 11 (sınırı hafif aşar; `mk_blog_service_modules` showIf ile çoğu projede gizli kalır).

#### 3.1 `mk_blog_types` — multiselect — "Yazı Türleri"
Kanıt: §2 Kapsam listesi.
| Etiket | Değer | Ne zaman doğru (scenario) | İçerikte nasıl görünür (example) |
|---|---|---|---|
| Kurumsal blog yazısı | `corporate` | Markanın görüş, kültür ve uzmanlık anlatımı yapılacaksa. | "Neden şeffaf fiyat gösteriyoruz?" gibi markanın yaklaşımını anlatan yazı. |
| Hizmet tanıtım odaklı yazı | `service` | Yazı bir hizmet sayfasına talep taşıyacaksa; §13 ek modülleri bu türde açılır. | Yazının ortasında hizmet özeti kutusu, sonunda "Teklif Alın" CTA'sı. |
| Mevzuat, duyuru ve güncel gelişme | `regulation` | Sektörde yönetmelik, tebliğ veya kurum duyurusu sık değişiyorsa. | Yazı resmî kaynağa bağlantı verir, yürürlük tarihi ilk paragrafta yazar. |
| Rehber | `guide` | "Nasıl yapılır?" aramaları hedefleniyorsa; kılavuz "nasıl yapılır? anlatımlarında mutlaka maddeler" ister. | Numaralı adımlar ve H4 kontrol listesiyle ilerleyen yazı. |
| Karşılaştırma | `comparison` | Kullanıcı iki yöntem, ürün veya paket arasında karar veriyorsa. | Fiyat içermeyen paket / yöntem karşılaştırma tablosu. |
| Soru-cevap odaklı bilgilendirme | `qa` | Müşterilerin tekrar eden sorularını yanıtlamak isteniyorsa. | Başlığı soru olan, H3 soru-cevaplardan oluşan yazı. |
| Kampanya / lead destekli yazı | `lead` | Yazı form, indirilebilir içerik veya kampanya sayfasına talep toplayacaksa. | Yazıda üç noktada CTA, sonunda form bağlantısı. |
| Kategori destek (SEO) yazısı | `category_support` | Bir hizmet veya kategori sayfasının konu otoritesini desteklemek isteniyorsa. | Kategori sayfasına bağlanan, alt sorguyu derinlemesine işleyen yazı. |

ruleDetail önerileri: `regulation` → "Kaynak olarak yalnız resmî metin ve kurum duyurusu kullanılır; yazıda mevzuatın tarihi ve sayısı belirtilir." (Kanıt §11) · `comparison` → `mk_legal_scope` = `comparative` ile bağlanabilir (recommend). · `service` → `mk_blog_service_modules`'ı açar.

#### 3.2 `mk_blog_service_modules` — multiselect — "Hizmet Odaklı Yazı Modülleri"
showIf: `[{field:"mk_blog_types", in:["service"]}]`. Kanıt: §13 tablo.
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Hizmet özeti | `summary` | Yazı tek bir hizmete bağlanıyorsa. | "Hizmetin temel özellikleri, kapsamı, hangi sorunu çözdüğü … kısa maddelerle" anlatılan kutu. |
| Paket karşılaştırması (fiyatsız) | `packages` | Hizmetin birden çok paketi varsa ve fiyat yazıda gösterilmeyecekse. | "Paket A, Paket B, Paket C ve Kurumsal Paket" sütunlu, fiyatsız tablo. |
| Teknik bilgiler ve metodoloji | `method` | Hizmetin işleyişi müşterinin karar vermesini etkiliyorsa. | Süreç adımları ve kullanılan araçların sade anlatımı. |
| Neden bu hizmet? | `why` | Rakiplerden farklılaşma anlatılacaksa. | Hız, standart, güven, raporlama veya maliyet avantajı maddeleri. |
| Referanslar ve başarı hikâyeleri | `cases` | İzinli müşteri deneyimi veya ölçülebilir sonuç varsa. | Kısa vaka: sorun → çözüm → ölçülebilir sonuç. (`mk_banned` = `client_logo` ile birlikte: onaysız müşteri adı kullanılmaz.) |
| Uzman kadro | `team` | Hizmeti sunan ekibin deneyimi güven üretiyorsa. | Uzmanın adı, unvanı, deneyimi. |

#### 3.3 `mk_blog_limits` — select — "Meta Alan ve Başlık Ölçüleri"
Kanıt: §4, §8 sonu, §15 etiket, §16, §17. Mevcut 19 alanlı plan şablonunun ölçüleri farklı olduğu için seçim gerekir.
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Karakter + piksel sınırı: meta başlık 35–60 karakter / 285–580 px, meta açıklama 120–160 karakter / 680–920 px, slug en çok 75 (ideal 30–60) karakter, özet 40–60 kelime, odak kelime en çok 3 kelime, başlıklar en çok 64 karakter, 2–3 ek etiket (önerilen) | `chars_px` | Kurum, arama sonuçlarında kırpılmayı azaltmak için hem karakter hem piksel kontrolü istiyorsa (§17: "hem karakter hem de piksel uzunlukları kontrol edilmelidir"). | Her yazının alan listesinde "Meta başlık: 52 karakter · ~470 px ✓" gibi ölçü notu. |
| Yalnız karakter sınırı (aynı karakter aralıkları, piksel ölçülmez) | `chars` | Piksel ölçecek araç (RankMath önizlemesi vb.) yoksa. | Aynı aralıklar, piksel notu olmadan. |
| İçerik planı şablonunun ölçüleri (meta başlık 45–60, meta açıklama 140–160, slug 20–60, özet 40–70 kelime, odak kelime 2–5 kelime) | `template` | Kurumun ayrı bir ölçü standardı yoksa; plan dosyasının ölçü rozetleriyle birebir aynıdır. | Plan dosyasındaki yeşil ✓ / turuncu ! rozetleriyle aynı aralıklar. |

Not: Plan dosyasının ölçü rozetleri şablonda sabit (KILAVUZ.md §7.2). `chars_px` / `chars` seçilirse ya şablona aralık parametresi gerekir ya da seçim yalnız kurala ve prompta yazılır — ana asistanın kararı. Bu alan eklenirse `mk_blog_fieldset` kural metnindeki "SEO / Semantik bölümündeki standarda göre" ifadesi bu alana yönlendirilmeli (09'da ölçü yok).

#### 3.4 (isteğe bağlı, proje bölümü) `cms_seo_plugin` — select — "SEO Eklentisi"
Bölüm 06 cms, showIf `cms_mode` = `WordPress`. Kanıt: §16 "RankMath SEO Ayarları" ve §18 "RankMath title, description, schema ve OG ayarları yapıldı mı?". Kılavuzda yalnız Rank Math geçer; diğer seçenekler genel alternatiftir (uydurma riskine karşı ana asistan karar versin): Rank Math (`rankmath`, kılavuz), Yoast SEO (`yoast`), All in One SEO (`aioseo`), Eklenti yok — tema / panel alanları (`none`). Etki: blog çıktısında alan adları eklentinin adlarıyla yazılır ("Odak Anahtar Kelime", "SEO Başlığı", schema türü, OG başlık / görsel).

### 4. Mevcut alanlarda değişiklik önerileri (Blog)
1. **`mk_blog_blocks` — yeni seçenekler:**
   - `hero` "Hero bölümü (başlık, alt başlık, açıklama)" — ruleDetail: "Ana başlık en çok 6 kelime, alt başlık en çok 6–7 kelime, açıklama 40–60 kelime; konu, sorun ve kullanıcı faydasını anlatır." Kanıt §7.1.
   - `video` "Video bölümü" — ruleDetail: "Video ilgili başlığın altında, akışı kesmeden yer alır; video başlığı (anahtar kelimeli), alt yazısı ve açıklaması (içerik, fayda, CTA) ayrı hazırlanır." Kanıt §6.
   - `related` "İlgili yazılar ve bağlantılar listesi" — ruleDetail: "Yazı sonunda hizmet sayfası, ilgili blog yazısı ve kategori bağlantıları listelenir; aynı bağlantı tekrar edilmez." Kanıt §9 şablon, §10.
2. **`mk_blog_blocks` ruleDetail güncellemeleri:**
   - `cta_box`: "CTA başlık altında, içerik ortasında ve yazı sonunda kullanılabilir; CTA metni, bağlantı ve telefon birlikte verilir." Kanıt §14.
   - `faq`: "Sorular gerçek arama niyetinden seçilir, cevaplar kısa ve nettir; marka / hizmet yönlendirmesi yalnız son soruda yapılır." Kanıt §12.
   - `sources`: mevcut metne "ticari web siteleri öncelikli kaynak olarak kullanılmaz; .gov, .edu, meslek kuruluşu ve mevzuat kaynakları önce gelir" eklenir. Kanıt §11.
3. **`mk_blog_fieldset` — üçüncü seçenek önerisi:** `extended` "Genişletilmiş set (19 alan + öne çıkan görsel bilgileri, hero, video ve paylaşım önizlemesi (OG) alanları)". Kanıt: §4, §5, §6, §7.1, §16 "OG Ayarları". Mevcut 19 alan görsel alt metni / başlık / altyazı / açıklama, hero, OG ve schema türünü içermiyor.
4. **`mk_blog_fieldset` kural metni:** "meta başlık ve meta açıklama SEO / Semantik bölümündeki standarda göre yazılır" ifadesi gösterecek alanı bulamıyor (09'da uzunluk yok). `mk_blog_limits` eklenirse ona, eklenmezse rehberde kılavuzdaki aralığa yönlendirilmeli.
5. **`mk_visual_meta` — yeni seçenek:** `description` "Açıklama (medya açıklaması)" — ruleDetail: "Görselin ne anlattığını açıklayan metin; CMS medya kütüphanesinin açıklama alanına girilir." Kanıt §5 "Açıklama: Görselin ne anlattığını açıklayan metin", §15.
6. **`mk_visual_meta` = `filename` ruleDetail:** "Blog görsellerinde dosya adı anahtar kelimeyi içerir (ör. anahtar-kelime-blog-gorseli.webp)". Kanıt §5 "Dosya Adı: Anahtar kelime içeren, küçük harf ve tireli format"; yayım kılavuzu §4.
7. **`mk_blog_length` ruleDetail (tüm seçenekler):** "Gelişme paragrafları ortalama 60 kelimedir; uzun açıklamalar maddelerle desteklenir." Kanıt §7.3.
8. **`mk_blog_cover`:** kılavuzun varsayılanı `w1920` ("tercihen 1920x1080 px") — öneri etiketi gerekiyorsa buraya.

### 5. B sınıfı brief alanları (form alanı değil)
Marka / Şirket (çok markalı yapıda) · Hizmet / Ürün · Konu başlığı · Anahtar kelime · Hedef kitle · İçerik amacı (bilgilendirme, lead, hizmet tanıtımı, farkındalık, trafik) · CTA · CTA linki · Telefon (varsayılan `oc_cta_phone`'dan gelir) · Kaynaklar · URL / slug · Meta title · Meta description · Sayfa özet yazısı · Öne çıkan görsel dosya adı, alt metin, başlık, alt yazı, açıklama · Video başlık, alt yazı, açıklama · Hero ana başlık, alt başlık, açıklama · H1–H6 başlıkları · SSS soruları · İç linkler · WordPress kategorisi · Etiketler · Yayın tarihi / saati.

### 6. C sınıfı ilkeler (kural / rehber)
1. H1 sayfada yalnız bir kez kullanılır; H2 ana bölüm, H3 H2'nin detayı; H4–H6 kontrol listesi, marka yaklaşımı, beklenen çıktı gibi alt kırılımlar için; başlık mümkünse anahtar kelimeyle başlar.
2. Teknik terimler parantez içinde açıklanır; kısaltmalar ilk kullanımda açık hâliyle yazılır.
3. Ürün, hizmet, süreç ve "nasıl yapılır?" anlatımlarında madde kullanılır.
4. Giriş konunun önemini, kitlenin ihtiyacını, yazının vaadini ve marka / hizmet bağlantısını kurar; sonuç ana mesajı toparlar ve CTA'yı doğal verir.
5. Anahtar kelime doğal şekilde hizmet sayfasına bağlanır; iç bağlantı kullanıcı deneyimi için de konumlandırılır.
6. Slug küçük harfli, tireli; Türkçe karakter, boşluk, alt çizgi ve özel karakter içermez (mevcut `mk_blog_path` kuralıyla aynı).
7. Yayın öncesi: H1, H yapısı, meta ölçüleri, odak kelime, slug, özet, iç link, dış kaynak, WebP, alt metin, öne çıkan görsel, CTA linki / telefonu, SSS, SEO eklentisi ayarları, mobil okunabilirlik, yazım ve imla kontrol edilir (§18).
8. Yayın sonrası: URL, mobil / masaüstü görünüm, linkler, görsel yüklenmesi kontrol edilir; UTM'li kısa link üretilip sosyal ekibe iletilir (§19.2).
9. İçerik kalitesi: kurumsal ve güven veren, sade dil; arama niyetine cevap; gereksiz uzun paragraf yok (§20).

---

## KILAVUZ 2 — Sosyal Medya İçerik Oluşturma Kılavuzu V2

### 1. Özet

**Amaç:** "Sosyal medya içeriklerinin platform teknik standartlarına uygun, marka tutarlılığı olan, tasarım ve metin açısından yayınlanabilir kalitede üretilmesini sağlamak."

**Bölümler:** 1 Amaç ve kapsam · 2 Genel ilkeler · 2.1 Gündemdeki format taraması ve konsept uyarlama (+ amaç → format matrisi) · 2.2 Tasarımcı için görsel yerleşim tarifi (+ kopyalanabilir yerleşim briefi + ek kontrol) · 3 Ortak teknik standartlar ve güvenli alan · 4 Meta (4.1 FB video, 4.2 FB post, 4.3 IG video, 4.4 IG post, 4.5 IG carousel, 4.6 WhatsApp Kanal video, 4.7 WhatsApp Kanal post) · 5 YouTube video · 6 YouTube Shorts · 7 YouTube Post · 8 LinkedIn post · 9 LinkedIn video · 10 LinkedIn etkinlik · 11 LinkedIn makale · 12 LinkedIn anket · 13 LinkedIn "Önemli bir an" · 14 Pinterest · 15 Google My Business · 16 SlideShare · 17 Threads · 18 X · 19 TikTok · 20 Caption yazım standardı · 21 Yayın öncesi teknik checklist · 22 Kaynakça. Her format: amaç, teknik tablo (boyut, format, süre, altyazı, kapak), tasarım tanımı, içerik akışı, caption şablonu, yayın öncesi kontrol.

**Sayısal standartlar (özet):**
| Format | Ölçü | Süre / adet / metin |
|---|---|---|
| Feed dikey | 1080×1350 (4:5) | IG post: başlık 6–8 kelime, destek 15–20 kelime |
| Kare | 1080×1080 (1:1) | YouTube Post 1:1, en çok 10 görsel, 16 MB |
| Yatay | 1920×1080 (16:9) | YouTube video; thumbnail 1280×720 (en az 640 px), 3–5 kelime başlık |
| Dikey video | 1080×1920 (9:16) | güvenli alan: üst ve alt %10–15 |
| FB link görseli | 1200×628 (1.91:1) | — |
| FB / IG video | — | organik 15–60 sn, reklam 6–30 sn, uzman 45–90 sn; kapak başlığı 6–8 kelime; ilk 2 sn kanca, ilk 5 sn değer vaadi |
| IG carousel | 1080×1350 | 5–8 slayt (kapak + 3–5 bilgi + CTA) |
| WhatsApp Kanal video | 9:16 / 4:5 | 15–60 sn; ~100 MB / 720p |
| YouTube Shorts | 1080×1920 | 15–60 sn önerilir (en çok 3 dk); başlık 40–60 karakter |
| LinkedIn post | 1200×627 / 1200×1200 / 1080×1350 | 3–6 nitelikli etiket; ilk 2 satırda ana fikir |
| LinkedIn video | 9:16–16:9 | organik B2B 45–120 sn |
| LinkedIn etkinlik kapağı | 1280×720 (16:9) | — |
| LinkedIn makale | kapak 1920×1080 | başlık 60–90 karakter, 600–1.500 kelime |
| LinkedIn anket | — | soru ≤140 karakter, 2–4 seçenek ≤30 karakter, süre 1 gün–2 hafta (B2B 1 hafta) |
| Pinterest | 1000×1500 (2:3) | — |
| Google Business | 720×720 (en az 250×250), 10 KB–5 MB | — |
| SlideShare | 16:9 | 8–20 slayt ideal (en çok 300), en çok 300 MB |
| Threads | 4:5 / 1:1 / 9:16 | ana metin 500 karakter (ekip standardı) |
| X | 1200×675 / 1600×900 | — |
| TikTok | 1080×1920 (en az 540×960) | organik 15–45 sn; bitrate ≥516 kbps, kalite için 4–8 Mbps |
| Dosya adı | `[MARKA]_[KONU]_[PLATFORM]_[FORMAT]_[TARIH]_v01` | — |

**Süreç:** konu → güncel format taraması ve benchmark → format seçimi (amaç matrisi) → konsept soruları ("hangi güncel formata uyarlandı?", "neden bu format seçildi?", "kullanıcı hangi aksiyona yönlendirilecek?") → tasarımcıya yerleşim tarifi → üretim (ölçü, güvenli alan, altyazı) → platforma özel caption → yayın öncesi teknik checklist.

**Uyum maddeleri:** telif (müzik, ses trendi), fotoğraf izni ("Tarih, isimler, unvanlar, logo, fotoğraf izni"), reklam politikaları ve yaratıcı kısıtlar, anket "hassas veri riski", trendde "Kurumsal güveni zedeleyecek mizah, argo … kullanılmamalıdır", erişilebilirlik (altyazı, alt metin).

### 2. A sınıfı bilgiler

| Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|
| Kapsam: "Meta, YouTube, LinkedIn, Pinterest, Google My Business, SlideShare, Threads, X ve TikTok" | `mk_platforms` — **kısmi** | SlideShare yok; `mk_accounts`'ta da yok |
| "Organik post, video, carousel, story/reels, kanal duyurusu, YouTube içerikleri, LinkedIn formatları …" (LinkedIn etkinlik, makale, anket, önemli an, doküman post; YouTube Post; X thread; video pin) | `mk_formats` (R, C, T, S, V, M) — **kısmi** | Anket, makale, etkinlik, doküman / PDF, kurumsal duyuru (önemli an), thread yok |
| "Video içeriklerde ses kapalı izleme davranışı dikkate alınmalı; altyazı veya ekran yazısı kullanılmalıdır." / "Altyazı: Zorunlu üretim standardı" (FB, IG, LinkedIn video) | `mk_formats` = `R` ruleDetail ("altyazı zorunludur") — **kısmi** | Uzun video ve diğer videolar için altyazı politikası yok |
| §2.1 "İçerik, marka kimliğini bozmadan gündemdeki format mantığına uyarlanmalı … Trend yalnızca marka tonu, hedef kitle ve içerik amacıyla uyumluysa kullanılmalıdır." | **yok** | Trend / gündem format politikası yok |
| §2.2 "Her sosyal medya briefinde tasarımcıya … resim, başlık, alt açıklama, buton, logo, ikon, iletişim bilgisi ve boşluk alanlarının nerede konumlanacağı açık şekilde tarif edilmelidir." | `mk_brief_format` (full / short) — **kısmi** | Yerleşim tarifi bloğu brief'te tanımlı değil |
| "Logo kullanılacaksa konumu ve boyutu belirtilmelidir … Blog görseli veya belirli formatlarda logo kullanılmayacaksa açıkça yazılmalıdır." | **yok** | Logo politikası (`mk_logo_use`) |
| "Dosya isimlendirme: [MARKA]_[KONU]_[PLATFORM]_[FORMAT]_[TARIH]_v01" | `mk_brief_format` = `full` ruleDetail: "Marka_BriefNo_FORMAT_YAYINTARİHİ_v01" — **kısmi / çelişkili** | Kurumun adlandırma şeması seçilemiyor |
| "Genel Yapı: Kanca cümle > kısa bağlam > marka/hizmet çözümü > CTA > etiketler." | `mk_caption` = `structured` — **tam** | — |
| "CTA Formatı: CTA: [CTA_METNİ]: [CTA_LINK] \| Telefon: [TELEFON]" (her formatta) | `mk_caption` structured (tek CTA) — **kısmi** | Telefonun CTA'ya eklenmesi kararı yok (`mk_cta_format`) |
| "Etiketler: #[Etiket1] #[Etiket2] #[Etiket3] #[Marka]"; LinkedIn "3-6 nitelikli etiket"; Threads "Sınırlı kullanılmalıdır" | `mk_hashtags` = `brand_topic` (marka + 3–5) — **tam** (platform sayıları C) | — |
| Carousel: "Genellikle 5-8 slayt … Kapak + 3-5 bilgi slaytı + CTA kapanışı ideal yapıdır." | `mk_formats` = `C` ruleDetail "6–9 slayt" — **kısmi / çelişkili** | Sayı farklı |
| IG post: "Başlık 6-8 kelime; destek metni 15-20 kelime; CTA kısa." / FB post: "Görselde 1 ana başlık + 1 kısa destek cümlesi + CTA." | `mk_formats` = `T` ruleDetail "görsel üzerindeki metin en çok 12 kelimedir" — **kısmi / çelişkili** | Sayı farklı |
| "İlk 2 saniye hook, ilk 5 saniye değer vaadi vermelidir." | `R` ruleDetail "ilk 3 saniyede kanca" — **kısmi** | Değer vaadi ve 2 sn |
| Video süreleri (organik 15–60, reklam 6–30, uzman 45–90, LinkedIn 45–120, TikTok 15–45) | **yok** | Süre standardı kuralda yok (ruleDetail önerisi) |
| YouTube: "Thumbnail 16:9; pratik standart 1280x720 px"; "Açıklama ilk 2 satırda değer vaadi ve CTA içermelidir."; "Uzun videolarda bölüm zamanları eklenmelidir." | `mk_formats` = `V` ruleDetail boş; `mk_platforms` = `youtube` ruleDetail kısmen — **kısmi** | V için kural boş |
| LinkedIn anket: "Anket sorusu maksimum 140 karakter … Minimum 2, maksimum 4 seçenek; seçenekler maksimum 30 karakter … Sonuç postu veya blog yönlendirmesi hazırlanmalıdır." | **yok** | Anket formatı yok |
| Pinterest: "Konuya göre panolar: hizmet, sektör, rehber, trend" (yayım kılavuzu 6.10 ile aynı) | `mk_platforms` = `pinterest` ruleDetail — **kısmi** | Pano yapısı kuralı yok (ruleDetail) |
| Google Business: "Post Türleri: Güncelleme, teklif, etkinlik, ürün/hizmet duyurusu." / "CTA Butonları: Ara, Yol tarifi, Rezervasyon, Daha fazla bilgi, Kaydol" | `mk_platforms` = `google` ruleDetail (türler var) — **kısmi** | Görsel ölçüsü ve düğme kuralı |
| "Her platform için aynı mesaj kopyalanmamalı; platformun tüketim alışkanlığına göre yeniden yazılmalıdır." | `mk_platforms` kural ("aynı metin bütün mecralara kopyalanmaz") — **tam** | — |
| Threads: "Ana metin için 500 karakter ekip standardı olarak alınmalıdır." | `mk_platforms` kural ("karakter sınırına uyar") — **kısmi** | threads ruleDetail boş |

### 3. Yeni alan önerileri (Sosyal medya)

Bölüm: **54 mk_social** (grup İçerik); 9 alan + 2 = 11.

#### 3.1 `mk_subtitles` — select — "Video Altyazı Politikası"
showIf: `[{field:"mk_formats", in:["R","V"]}]`. Kanıt: §2 "Video içeriklerde ses kapalı izleme davranışı dikkate alınmalı; altyazı veya ekran yazısı kullanılmalıdır."; 4.1, 4.3, 9 "Altyazı: Zorunlu üretim standardı"; yayım kılavuzu §4 "altyazılı versiyon hazırlanmalı". (Video kılavuzlarını okuyan ajan da altyazı önerirse tek alanda birleştirin.)
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Her videoda altyazı veya ekran yazısı zorunlu (önerilen) | `required` | Videolar akışta sesi kapalı izleniyorsa — kılavuz bunu bütün mecralar için standart sayar. | Reels'te konuşma ekranda büyük altyazıyla akar; ana mesaj sessiz izlemede de anlaşılır. |
| Altyazılı ve altyazısız iki sürüm | `two_versions` | Aynı video hem sosyal akışta hem altyazının platformdan eklendiği YouTube gibi yerlerde kullanılacaksa (yayım kılavuzu §4). | Dosyalar `…_v01.mp4` ve `…_altyazili_v01.mp4` olarak teslim edilir. |
| Yalnız konuşma içeren videolarda | `speech_only` | Videoların çoğu müzikli ürün / mekân görüntüsüyse. | Konuşmasız ürün videosunda yalnız ekran başlığı bulunur. |

#### 3.2 `mk_trends` — select — "Gündem ve Trend Formatları"
Kanıt: §2.1 ve "Trend uyarlama kriteri".
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Marka tonuna uyan trend formatlara uyarlanır (önerilen) | `fit_only` | Kurum güncel formatlardan yararlanmak ama güven algısını korumak istiyorsa. ruleDetail: "Trend yalnız marka tonu, hedef kitle ve içerik amacıyla uyumluysa kullanılır; kurumsal güveni zedeleyen mizah, argo, bağlam dışı akım kullanılmaz; her içerikte 'hangi güncel formata uyarlandı, neden, hangi aksiyon' brief'e yazılır; rakip içerik kopyalanmaz." | Brief'te "Format: güncel 'önce / sonra' carousel akımı — neden: süreç anlatımı — aksiyon: teklif formu" satırı. |
| Trend akımları kullanılmaz | `none` | Düzenlenmiş sektörde ya da çok resmî ses tonunda. | Paylaşımlar kurumun kendi şablonlarıyla üretilir. |
| Trend formatları serbest | `free` | Genç / eğlenceli tonlu markalarda. | Platformdaki akım sesleri ve kalıpları doğrudan kullanılır (telif kontrolüyle). |

`brand_tone` (01) ile recommend bağlanabilir: Formal / Luxury → `fit_only` / `none`; Energetic → `free` / `fit_only`.

#### 3.3 `mk_logo_use` — select — "Görsellerde Logo Kullanımı"
Bölüm: **55 mk_creative** (blog ve sosyal görseller için ortak; 8 alan + `mk_logo_use` + `mk_file_naming` = 10). Kanıt: blog §5 "Logo Kullanımı: Briefte belirtilmedikçe otomatik eklenmemelidir."; sosyal §2.2 "Logo kullanılacaksa konumu ve boyutu belirtilmelidir … Blog görseli veya belirli formatlarda logo kullanılmayacaksa açıkça yazılmalıdır."; 4.6 "Logo ve telefon görünür olmalıdır."
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Sosyal görsellerde logo var, blog kapağında yok (brief'te istenmedikçe) (önerilen) | `social_only` | Blog kapağının sade ve konu odaklı kalması, sosyal paylaşımın marka taşıması isteniyorsa. | Instagram postunda sol üstte küçük logo; blog kapağında logo yok. |
| Yalnız brief'te istenirse | `brief` | Logo kullanımı her işte ayrı karar veriliyorsa. | Brief'in "Logo yerleşimi" satırı boşsa logo eklenmez. |
| Tüm görsellerde logo | `all` | Görsellerin sık izinsiz paylaşıldığı ya da marka bilinirliğinin öncelikli olduğu işlerde. | Blog kapağı dahil her görselin sağ alt köşesinde logo. |

ruleDetail ortak: "Logo kullanılan her görselde konum ve boyut brief'e yazılır; logo güvenli alanda kalır; logo kuralları Kurumsal Kimlik › Logo Kullanım Kuralları'na uyar."

#### 3.4 `mk_file_naming` — select — "Teslim Dosyası Adlandırma"
Bölüm: **55 mk_creative**. Kanıt: sosyal §3 "Dosya isimlendirme: [MARKA]_[KONU]_[PLATFORM]_[FORMAT]_[TARIH]_v01 … Kaynak ve export dosyaları versiyonlu saklanmalıdır."; yayım §4 "Marka_Konu_Platform_Post_20260701_v01.png", "Marka_Konu_Reels_20260701_v01.mp4", "anahtar-kelime-blog-gorseli.webp". Mevcut `mk_brief_format` = `full` ruleDetail farklı bir şema sabitliyor.
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Marka_Konu_Platform_Format_Tarih_v01 (önerilen) | `topic` | Dosyalar konu ve platforma göre aranacaksa. | `Marka_KiraStopaji_Instagram_Carousel_20261105_v01.png` |
| Marka_BriefNo_Format_YayınTarihi_v01 | `brief_no` | Brief numarası kullanılıyorsa (`mk_brief_no` ≠ none) ve işler numarayla takip ediliyorsa. | `Marka_B2026014_Reels_20261105_v02.mp4` |

İki seçenekte de: blog ve site görselleri SEO için `anahtar-kelime.webp` biçiminde (küçük harf, tireli) adlandırılır; sürüm `v01, v02` ekiyle artar. Bu alan eklenirse `mk_brief_format` = `full` ruleDetail'indeki adlandırma cümlesi bu alana devredilmeli.

### 4. Mevcut alanlarda değişiklik önerileri (Sosyal medya)
1. **`mk_platforms` — yeni seçenek `slideshare` "SlideShare (doküman)"**; ruleDetail: "PDF / PPTX olarak 16:9 yüklenir; kurumsal yayında 8–20 slayt; kapakta başlık, marka, tarih ve değer vaadi, son slaytta CTA; LinkedIn doküman postuyla desteklenir." Kanıt §16, yayım 6.11. Plan dosyası için `mecra` tanımı gerekir (`marketingTemplate.mecralar`'da yoksa, WhatsApp Grup örneğindeki gibi). **`mk_accounts` (80)** satırı da eklenmeli: `slideshare` (SlideShare), hosts `slideshare.net`.
2. **`mk_platforms` boş ruleDetail'leri** (kılavuzdan):
   - `facebook`: "Facebook metni Instagram'dan daha açıklayıcı olabilir; link önizlemesi 1200×628 (1.91:1) görselle kontrol edilir." (4.2)
   - `instagram`: "Görselde metin az, caption kısa; feed 1080×1350." (4.4, yayım 6.2)
   - `whatsapp`: "Ana mesaj + 1–2 cümle açıklama + CTA; bağlantı ve telefon her paylaşımda bulunur; bir kampanya için aşırı sık paylaşım yapılmaz." (4.7, yayım 6.3)
   - `threads`: "Ana metin en çok 500 karakter (ekip standardı); konuşma başlatan ton, sınırlı etiket; Instagram içeriği paylaşılırsa metin yeniden yazılır." (17, yayım 6.9)
   - `tiktok`: "İlk saniyede konuya girilir; uzun logo animasyonu ve ağır kurumsal giriş kullanılmaz; alt caption ve sağ ikon alanında metin olmaz." (19)
   - `linkedin` (mevcut metne ek): "3–6 nitelikli etiket; gereksiz slogan dili kullanılmaz." (8)
   - `google` (mevcut metne ek): "Görsel 720×720; gönderi türüne uygun düğme (Ara, Yol tarifi, Rezervasyon, Daha fazla bilgi, Kaydol) seçilir; haftalık güncelleme ritmi." (15, yayım §7)
   - `pinterest` (ek): "1000×1500 (2:3); her pin konuya göre doğru panoya (hizmet, sektör, rehber, trend) eklenir; başlık ve açıklama anahtar kelime odaklıdır." (14, yayım 6.10)
   - `youtube` (ek): "Uzun videoda açıklamanın ilk 2 satırı değer vaadi ve CTA; bölüm zamanları, oynatma listesi, kart ve bitiş ekranı; Shorts başlığı 40–60 karakter." (5, 6, yayım 6.6)
3. **`mk_formats` — yeni seçenekler** (plan şablonundaki `formatlar` kodlarıyla uyum kontrol edilmeli):
   - `A` "Anket" — ruleDetail: "Soru en çok 140 karakter, 2–4 seçenek, seçenek en çok 30 karakter; soru yönlendirici değildir ve kişisel / hassas veri istemez; B2B anket süresi 1 hafta; ardından sonuç postu planlanır." (12, yayım 6.4)
   - `K` "Makale (LinkedIn makale / uzun metin)" — ruleDetail: "Başlık 60–90 karakteri aşmaz, 600–1.500 kelime, ara başlık ve madde; sonunda hizmet / blog / form CTA'sı." (11)
   - `D` "Doküman / PDF carousel" — ruleDetail: "Her sayfada tek fikir, kapak güçlü, son sayfa CTA." (yayım 6.4 "LinkedIn Doküman / Carousel")
   - `E` "Etkinlik duyurusu" — ruleDetail: "Kapak 16:9 (1280×720); tarih, saat, format, konuşmacı ve kayıt bağlantısı ilk bakışta görünür; etkinlik sonrası hatırlatma postları planlanır." (10, yayım 6.4)
   - `N` "Kurumsal duyuru / önemli an" — ruleDetail: "Kutlama odaklı ama kurumsal ton, abartılı satış dili yok; CTA zorunlu değil, telefon yalnız iş geliştirme bağlantısı varsa; isim, unvan ve fotoğraf izni kontrol edilir." (13)
   - `TH` "Thread / seri gönderi" — ruleDetail: "X'te 3–5 postluk akış; ilk post ana iddia, son post CTA." (yayım 6.5)
4. **`mk_formats` ruleDetail çelişkileri:**
   - `C` carousel: mevcut "6–9 slayt" ↔ kılavuz "Genellikle 5-8 slayt … Kapak + 3-5 bilgi slaytı + CTA kapanışı ideal" (yayım 6.2: "5-10 slayt"). Öneri: "5–8 slayt (kapak + 3–5 bilgi + CTA), tüm slaytlar aynı oranda, sayfa numarası ve sabit ızgara".
   - `T` tek görsel: mevcut "görsel üzerindeki metin en çok 12 kelime" ↔ kılavuz "Başlık 6-8 kelime; destek metni 15-20 kelime; CTA kısa". Öneri: "başlık 6–8 kelime + destek cümlesi 15–20 kelime + kısa CTA; uzun açıklama caption'a".
   - `R` Reels: mevcut "ilk 3 saniyede kanca" ↔ kılavuz "İlk 2 saniye hook, ilk 5 saniye değer vaadi". Öneri: ek olarak "süre: organik 15–60 sn, uzman anlatımı 45–90 sn; 9:16'da üst ve alt %10–15 alanda kritik metin yok".
   - `V` uzun video (boş): "1920×1080 (16:9), MP4 / H.264 / AAC; thumbnail 1280×720, 3–5 kelimelik başlık; açıklamanın ilk 2 satırı değer vaadi ve CTA; bölüm zamanları; altyazı." (5)
   - `S` Story: mevcut "3 kare" kılavuzda sayı yok; ek: "üst ve alt güvenli alan boş, bağlantı çıkartması kontrol edilir" (yayım 6.2).
5. **`mk_brief_format` = `full` ruleDetail ek:** "Brief'te görsel yerleşim tarifi bulunur: ana kompozisyon, resim, başlık (konum, en çok satır, hizalama), açıklama, CTA (konum, metin, link / telefon), logo, ikon / yardımcı öğeler, güvenli alan, mobil okunabilirlik." Kanıt §2.2 "Görsel Yerleşim Briefi Kopyalanabilir Format". (Tek tip brief kılavuzunu okuyan ajanın önerisiyle birleştirilmeli; ayrı boolean önermedim.)
6. **`mk_hashtags` kural metni:** "X'te en çok 2 etiket" ↔ yayım 6.5 "Ana mesaj + kısa link + 1-3 etiket". Küçük fark; kurum kılavuzuna uymak için "1–3" yapılabilir ya da 2 korunur (mevcut plan şablonu X metnini en çok 2 etiketle üretiyor — şablonla uyum için 2'de kalmak daha güvenli). Ek: "LinkedIn'de 3–6 nitelikli etiket; Threads'te sınırlı".

### 5. B sınıfı brief alanları
Platform ve içerik tipi · Konu / tek ana mesaj · Hook cümlesi · İçerik amacı (farkındalık, eğitici, lead, etkinlik, sosyal kanıt) · Seçilen güncel format ve gerekçesi · Görsel yerleşim tarifi (kompozisyon, resim, başlık, açıklama, CTA, logo, ikon, güvenli alan, mobil okunabilirlik) · Slayt metinleri · Video senaryosu / sahne akışı · Kapak / thumbnail metni · Caption · CTA metni ve linki · Etiketler · Etkinlik adı, tarih, saat, konuşmacı, kayıt linki · Anket sorusu ve seçenekleri · Yayın tarihi / saati · Dosya adı.

### 6. C sınıfı ilkeler
1. Her içerik tek ana mesaj taşır; görselde birden fazla ana fikir verilmez.
2. Logo, ana başlık, CTA ve kritik metin güvenli alanda kalır; 9:16'da üst ve alt %10–15 boş bırakılır; TikTok'ta alt caption ve sağ ikon alanı da boş.
3. Koyu görsel üstüne açık metin, açık zemin üstüne koyu metin; kritik metin görsel karmaşasına bindirilmez.
4. Amaç → format eşlemesi: farkındalık → kısa video / Reels / Shorts / Story; eğitici → carousel / doküman / SlideShare; lead → tek görsel / carousel (problem > çözüm > fayda > CTA); etkinlik → LinkedIn etkinlik / story / video davet; sosyal kanıt → referans postu / başarı hikâyesi / önce-sonra.
5. Video akışı: Hook > Problem > Çözüm > Fayda > CTA; her sahne tek fikir.
6. Benchmark incelenir ama içerik doğrudan kopyalanmaz.
7. Caption'da ilk cümle tek başına değer taşır; paragraflar kısa, uzun metinde madde.
8. Kurumsal prodüksiyonda MP4 / H.264 / AAC dışa aktarım; metinli görselde PNG, fotoğraf ağırlıklıda JPG.
9. Platform limitleri değişebilir; kritik yayın ve reklam öncesi platformun güncel yardım merkezi kontrol edilir.
10. Yayın öncesi teknik checklist (§21): tip, ölçü, format, dosya boyutu, güvenli alan, hook, altyazı / ses, kapak, caption, CTA linki / telefon, etiket sayısı, logo, yazım / isim / unvan / tarih, UTM / kısa link, sürümlü dosya adı, reklamda kullanılacaksa reklam politikası.

---

## KILAVUZ 3 — İçerik Yayım ve Dağıtım Kılavuzu

### 1. Özet

**Amaç:** "içerik üretimi tamamlandıktan sonra yayım sürecinde format, ölçü, link, UTM, zamanlama, onay, erişilebilirlik ve raporlama hatalarını azaltmak; tüm platformlarda ölçülebilir ve tutarlı bir marka deneyimi oluşturmak". Kapakta iki bağlayıcı standart: "CTA linki ve telefon numarası birlikte kullanılmalıdır." ve "Tüm linklerde UTM parametreleri ve kısa link standardı uygulanmalıdır."

**Bölümler:** 1 Amaç · 2 Temel yayım ilkeleri (kaynak içerik, platforma özel uyarlama, ölçülebilirlik, CTA tutarlılığı, görsel tutarlılık, yayın öncesi kontrol, yayın sonrası izleme) · 3 Yayım operasyonu iş akışı (7 aşama, sorumlu, kontrol, çıktı) · 4 Dosya / asset / isimlendirme · 5 CTA, telefon ve UTM standardı · 6 Platform bazlı yayım (6.1 Blog ana kaynak, 6.2 Meta Business Suite, 6.3 WhatsApp Business Kanal, 6.4 LinkedIn şirket sayfası, 6.5 X, 6.6 YouTube, 6.7 Google Business Profile, 6.8 TikTok, 6.9 Threads, 6.10 Pinterest, 6.11 SlideShare, 6.12 Mailing, 6.13 Podcast, 6.14 SMS, 6.15 Basın bülteni / PR, 6.16 Reklam ve organik entegrasyon) · 7 Zamanlama ve frekans · 8 Çapraz dağıtım matrisi · 9 Final checklist · 10 Yayın sonrası izleme · 11 KPI seti · 12 Kaynak ve güncellik.

**Sayısal standartlar:** sosyal görsel RGB 72–150 dpi; mailing banner 600–800 px; carousel 5–10 slayt; LinkedIn video 3 sn–30 dk; X ücretsiz hesap 280 karakter, 1–3 etiket, thread 3–5 post; çalışan paylaşımı ana paylaşımdan 1–3 saat sonra; YouTube / TikTok 24–72 saat izleme; izleme noktaları ilk 30 dk, 24 saat, 48–72 saat, 7 gün, aylık; SMS tek segment; video izlenme 3 sn, %25, %50, %75, %100.

**Süreç (7 aşama):** 1 Ana kaynak hazırlığı (İçerik / Web → yayın URL'si) · 2 UTM ve kısa link (Dijital Pazarlama → kısa link listesi) · 3 Platform uyarlaması (Sosyal Medya / İçerik → içerik seti) · 4 Tasarım export (Tasarım → platform dosyaları) · 5 Zamanlama (Sosyal Medya / CRM → planlanmış içerik) · 6 Yayın kontrolü (Sosyal Medya / Web → canlı içerik) · 7 Raporlama (Dijital Pazarlama → performans raporu).

**Uyum maddeleri:** Mailing "KVKK/İYS, unsubscribe ve gönderici alanı kontrol edilir"; SMS "Ticari ileti izinleri, İYS ve KVKK uyumu"; final checklist "KVKK, telif, izin ve marka onayı tamamlandı"; TikTok / reklam "telifli müzik"; basın "Dosya adları ve erişim izinleri".

### 2. A sınıfı bilgiler

| Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|
| "CTA linki ve telefon numarası birlikte kullanılmalıdır." / "Kurumsal standartta CTA metni, link ve telefon bilgisi birlikte verilmelidir." / "CTA: Detaylı Bilgi Alın: [Kısa Link] \| Telefon: [Telefon]" | **yok** (`mk_caption` tek CTA; `mk_contact` serbest metin) | CTA biçimi + CTA telefonu |
| "CTA metni, CTA linki ve telefon numarası tüm platformlarda aynı kampanya amacıyla uyumlu olmalıdır." | **yok** | Aynı |
| "Tüm harici yönlendirmelerde UTM parametreli ve kısaltılmış link kullanılmalıdır." / "Kısa Link: Kurumsal link kısaltma sistemi üzerinden oluşturulmalıdır." | `mk_utm`, `mk_links` — **kısmi** | Kısa link kararı ve kısa alan adı yok |
| "utm_medium … social, cpc, newsletter, banner, referral, organic" / "utm_source … linkedin, facebook, instagram, x, youtube, google, whatsapp, email" | `mk_utm` = `standard` ("e-postada email") — **kısmi / çelişkili** | E-postada medium = `newsletter`, source = `email` (mevcut: medium = email); `banner`, `referral` yok |
| "utm_campaign: Kampanya veya içerik adını belirtir" (ör. konu-blog adları) | `mk_utm` standard: "kampanya = dönem", `mk_utm_campaign` dönem adı — **kısmi / çelişkili** | Kampanya = içerik / kampanya adı seçeneği yok |
| "utm_content: Aynı kampanyadaki varyasyonları ayırır — video-reel, carousel-slide1, mail-footer, banner-ust" | `mk_utm` standard: "utm_content gönderi veya mail kimliğini taşır" — **kısmi** | Varyasyon / konum değeri |
| "utm_term: … Google Ads için anahtar kelime; organik sosyalde boş bırakılabilir" | **yok** | utm_term kuralı |
| "Kaynak İçerik Mantığı: Blog yazısı, hizmet sayfası, landing page veya kampanya sayfası ana kaynak olarak kabul edilir. Diğer platform içerikleri bu ana kaynaktan türetilir." | `mk_derive` = `hub` — **tam** (blog için); hizmet / landing sayfası kaynak değil | — |
| §8 "Blog Yazısı → LinkedIn post, X kısa post, GMB güncelleme, Instagram carousel, WhatsApp duyuru, mailing bölümü" | `mk_derive` hub — **kısmi** | Hangi türev içeriklerin üretileceği seçilemiyor |
| §8 "Video → Shorts, Reels, TikTok, LinkedIn video, WhatsApp kısa video, YouTube ana video" / "PDF / Föy → LinkedIn doküman, SlideShare, mailing eki/linki, satış follow-up materyali" / "Podcast → …" / "Basın Bülteni → …" / "Etkinlik → LinkedIn etkinlik, mailing daveti, GMB etkinlik, WhatsApp hatırlatma, sosyal medya postları" | **yok** | Diğer kaynak türleri için dağıtım seti (ilgili kanal bölümleri açılırsa) |
| §3 yedi aşamalı yayım operasyonu ve sorumlu ekipler | `mk_flow` (yalnız onay adımları), `mk_roles` — **kısmi** | Yayım operasyonu aşamaları yok |
| Sorumlular: "İçerik / Web Ekibi", "Dijital Pazarlama", "Sosyal Medya / CRM", "Tasarım Ekibi" | `mk_roles` (editor, copywriter, designer, video, social, ads, seo, legal, manager) — **kısmi** | Web / CMS sorumlusu, CRM sorumlusu, dijital pazarlama / ölçüm uzmanı yok |
| "Çalışan paylaşımları ana paylaşım sonrası 1-3 saat içinde yapılabilir." / LinkedIn: "çalışan paylaşımı kontrol edilir" | **yok** | Çalışan paylaşımı (employee advocacy) kararı |
| §10 "İlk 30 dakika … İlk 24 saat … 48-72 saat … 7 gün … Aylık" | `mk_report_rhythm` — **kısmi** | Yayın sonrası izleme noktaları yok |
| §11 KPI seti: Erişim / Gösterim, Tıklama, CTR, Etkileşim, Video İzlenme, Form / Lead, Telefon Araması, Mailing Verisi, PR Etkisi, Dönüşüm | `mk_measure_scope`, `mk_conversions` — **kısmi** | Mailing, video izlenme, GBP performansı, PR, CRM lead, çağrı raporu yok |
| "Aylık: Kanal bazlı içerik performansı — Şirket, hizmet, platform ve format bazlı rapor" | `mk_report_outputs` — **kısmi** | Rapor kırılımları (ruleDetail) |
| "Organik ve reklam UTM'leri ayrı raporlanır." | `mk_utm` (social / cpc) — **tam** | — |
| "Organik İçerikten Reklama: İyi performans gösteren organik içerik reklam varyasyonuna dönüştürülebilir." / TikTok "Spark Destek" | `mk_ads_channels` — **yok** | Organik içeriği reklama taşıma kararı |
| §7 Zamanlama: "Blog Yayını — Ana kampanya gününden önce veya aynı gün sabah"; "LinkedIn — B2B içerikler için iş saatleri öncelikli"; "WhatsApp Kanal — Kısa duyuru için öğle veya mesai sonu öncesi"; "Mailing — Segment ve konuya göre sabah/öğle test edilmeli"; "Google Business Profile — Haftalık güncelleme ritmi" | `mk_post_times` (fixed / data / free) — **kısmi** | Kanal varsayılan ritmi (ruleDetail) |
| Mailing: "Preheader … Boş bırakılmamalıdır." / "Hero / Banner 600-800 px genişlik" / "Tek ana CTA + telefon + UTM link" / "A/B konu başlığı testi uygulanabilir." | `mk_mail_layout`, `mk_mail_formats` — **kısmi** | Preheader, banner genişliği, A/B konu testi (Mailing kılavuzu ajanıyla birleştir) |
| SMS: "Tek segment hedeflenmeli; Türkçe karakter kullanımı segmenti etkileyebilir." / "Çalışma saatleri ve hedef kitle alışkanlığına uygun gönderim." / "İYS ve KVKK" / "Teslim, tıklama, dönüşüm, opt-out" | **yok** (SMS bölümü yok) | SMS kılavuzu ajanının önereceği bölüme katılmalı |
| Podcast: "MP3 dağıtım, WAV arşiv"; "Kare podcast cover"; "Başlık, açıklama, kategori, bölüm numarası, transkript"; "RSS / Spotify / Apple / YouTube / web blog destekli"; "Dinleme, tamamlanma, kanal, CTA tıklaması" | **yok** | Podcast kılavuzu ajanının bölümüne katılmalı |
| Basın: "DOCX + PDF; başlık, spot, tarih, şehir, gövde, alıntı, boilerplate, medya iletişim"; "Medya Kiti: Logo, görseller, sözcü fotoğrafı …"; "Medya listesi segmentlenir: ekonomi, teknoloji, İK, hukuk, yerel vb."; "Kliping ve rapor" | **yok** | Basın bülteni kılavuzu ajanının bölümüne katılmalı |
| LinkedIn Ads: "Single Image, Video, Document, Event, Lead Gen" — "Insight Tag, hedef kitle, form alanları"; TikTok Ads: "In-feed / Spark / lead yönlendirme" | `mk_ads_channels` linkedin / tiktok var, alt bölüm yok — **kısmi**; `mk_ids` linkedin_partner / tiktok_pixel var | Reklam kılavuzu ajanıyla birleştir |
| "PDF / Föy — PDF — Web için optimize, baskı gerekiyorsa ayrıca CMYK/PDF-X" | **yok** | Föy kılavuzu ajanıyla birleştir |

### 3. Yeni alan önerileri (Yayım ve dağıtım)

**Yerleşim önerisi — yeni bölüm `mk_dist` "Yayım & Dağıtım"** (grup: Süreç & Ekip, `mk_flow`'dan önce; ya da grup Kanallar). Gerekçe: kılavuzun kendisi tek bir operasyon standardıdır ve CTA, kısa link, çapraz dağıtım, çalışan paylaşımı, yayım aşamaları ve yayın sonrası izleme birlikte tanımlanır; bu alanları 52 (10 alan), 62 (8 alan) ve 63'e dağıtmak 52 ve 62'yi sınırın üstüne çıkarır. Kanal değil süreç olduğu için açma boolean'ı önermiyorum (bütün içerikler için geçerli). İstenirse yedek yerleşim her alanın yanında yazıyor.

Ortak Bilgiler'e (77 `oc_identity`) iki kimlik verisi:

#### 3.1 `oc_cta_phone` — text — "CTA Telefonu" (77 oc_identity)
Kanıt: blog §3.1 "Telefon: CTA ile birlikte kullanılacak kurumsal telefon numarası"; yayım kapak "CTA linki ve telefon numarası birlikte kullanılmalıdır." `mk_contact` birden çok numara içerebildiği için CTA'da hangi numaranın kullanılacağı tek satır olmalı. Placeholder: "Örn. 0850 000 00 00 — CTA'larda ve görsel alt bantlarında kullanılacak numara". scenario: "Birden çok telefon varsa (santral, şube, WhatsApp) içeriklerde hep aynı numaranın görünmesi ve çağrı ölçümünün tek numarada toplanması isteniyorsa." example: "Her paylaşımın sonunda 'CTA: Teklif Alın: kisa.link/x | Telefon: 0850 000 00 00' satırı." Boşsa `mk_contact`'taki ilk telefon kullanılır.

#### 3.2 `oc_cta_url` — url — "Varsayılan CTA Sayfası" (77 oc_identity)
Kanıt: blog §3.1 "CTA Linki: Form, hizmet sayfası, iletişim sayfası veya kampanya linki"; yayım §5 "Ana URL: Trafiğin yönlendirileceği blog, hizmet, landing veya form sayfası". İçerik başına değişir (B) ama brief'te verilmediğinde kullanılacak varsayılan (iletişim / teklif formu) kurum düzeyindedir. scenario: "İçeriklerin çoğu aynı teklif veya iletişim formuna yönleniyorsa." example: "Brief'te link yoksa CTA https://…/teklif-al/ adresine UTM'li verilir." (Gereğinden çok alan sayılırsa bu alan atlanabilir; telefon alanı daha güçlü kanıtlı.)

#### 3.3 `mk_cta_format` — select — "CTA Biçimi" (`mk_dist`; yedek: 52 mk_content)
Kanıt: yayım kapak ve §5; sosyal §20 "CTA Formatı: CTA: [CTA_METNİ]: [CTA_LINK] | Telefon: [TELEFON]"; blog §14.
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| CTA metni + bağlantı + telefon (önerilen) | `text_link_phone` | Telefonla gelen talep önemliyse; kılavuz "CTA linki ve telefon numarası birlikte kullanılmalıdır" der. ruleDetail: "CTA 'CTA: [metin]: [kısa link] \| Telefon: [CTA telefonu]' satırıyla yazılır; telefon CTA Telefonu alanından alınır; CTA metni, link ve telefon bir kampanyanın bütün mecralarında aynıdır." | "CTA: Detaylı Bilgi Alın: kisa.link/abc \| Telefon: 0850 000 00 00" |
| CTA metni + bağlantı | `text_link` | Satış çevrim içi kapanıyorsa ya da telefonla talep alınmıyorsa. | "Detaylı bilgi: kisa.link/abc" |
| Mecraya göre (bağlantı, telefon ya da mesaj) | `per_platform` | Kanal davranışı farklıysa (kılavuz §2: "CTA, platform davranışına uygun olmalı; link, telefon veya DM yönlendirmesi net verilmelidir"). | LinkedIn'de bağlantı, WhatsApp'ta bağlantı + telefon, Instagram'da "DM ile yazın". |

Not: LinkedIn "Önemli bir an" için kılavuz "CTA … Zorunlu değildir; … Telefon yalnızca iş geliştirme bağlantısı varsa eklenmelidir" der → `text_link_phone` ruleDetail'ine istisna olarak yazılmalı.

#### 3.4 `mk_cta_phrases` — multiselect — "Onaylı CTA İfadeleri" (`mk_dist`; yedek: 52)
Kanıt: blog §14 "CTA Metni: Teklif Alın / Danışmanlık Talep Edin / Bize Ulaşın / Formu Doldurun / Detaylı Bilgi Alın / Randevu Oluşturun / Hizmeti İnceleyin"; sosyal 10 "CTA: Kayıt Olun"; GBP "Ara, Yol tarifi, Rezervasyon, Daha fazla bilgi, Kaydol". Rule: "CTA metinleri yalnız bu ifadelerden seçilir; içerik huni aşamasına uygun olanı kullanılır."
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Teklif Alın | `quote` | Teklifle satılan hizmet / ürün. | "CTA: Teklif Alın: …" |
| Danışmanlık Talep Edin | `consult` | Ön görüşmeyle başlayan danışmanlık hizmeti. | Yazı sonu kutusunda düğme. |
| Bize Ulaşın | `contact` | Genel iletişim; farkındalık içerikleri. | Alt bantta "Bize Ulaşın". |
| Formu Doldurun | `form` | Lead formu olan kampanyalar. | Kampanya postunda form bağlantısı. |
| Detaylı Bilgi Alın | `info` | Değerlendirme aşaması içerikleri. | Carousel son slaytı. |
| Randevu Oluşturun | `booking` | Randevulu hizmetler (`modules_extra` = booking ile recommend). | "Randevu Oluşturun: …" |
| Hizmeti İnceleyin | `service` | Hizmet sayfasına trafik. | Blog içi CTA. |
| Kayıt Olun | `register` | Etkinlik, webinar, eğitim (`mk_evt_on` ile recommend). | LinkedIn etkinlik postu. |

(İsteğe bağlı: `mk_cta_custom` text "Diğer CTA ifadeleri" — kurumun kendi ifadeleri için. Alan sayısını artırmamak için `mk_cta_phrases`'e "Diğer" + metin yerine `mk_brand_*` gibi tek text tercih edilebilir; ana asistan karar versin.)

#### 3.5 `mk_cross_derive` — multiselect — "Blogdan Türetilecek İçerikler" (`mk_dist`; yedek: 52, `mk_derive`'in altında)
showIf: `[{field:"mk_derive", in:["hub","mixed"]}, {field:"mk_blog_cadence", in:["w2_3","w1","m2","m1"]}]`. Kanıt: §8 "Blog Yazısı → LinkedIn post, X kısa post, GMB güncelleme, Instagram carousel, WhatsApp duyuru, mailing bölümü"; blog §19.2 "Gerekirse mailing, WhatsApp Business, LinkedIn ve Google My Business paylaşımları için içerik ekibine yönlendirme yapılır."
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| LinkedIn postu (2–4 paragraf + bağlantı) | `linkedin` | B2B kitle; `mk_platforms` = linkedin. | Yazının stratejik özeti + blog kısa linki. |
| X kısa postu | `x` | `mk_platforms` = x. | Ana iddia + kısa link + etiket. |
| Google İşletme Profili güncellemesi | `gbp` | Yerel / hizmet niyeti; `mk_platforms` = google. | Kısa hizmet / fayda metni + "Daha fazla bilgi" düğmesi. |
| Instagram carousel | `ig_carousel` | Eğitici / rehber yazılar. | Kapak hook → bilgi slaytları → CTA slaytı. |
| WhatsApp Kanal duyurusu | `whatsapp` | `mk_platforms` = whatsapp. | Tek cümle ana mesaj + kısa link + telefon. |
| Mailing / bülten bölümü | `mail` | `mk_mail_on` = true. | Bültende başlık, kısa özet ve tek bağlantılı kart. |

ruleDetail ortak: "Türetilen içerikler kaynak yazı yayınlandıktan sonra hazırlanır; dağıtım linkleri yazının yayın URL'sinden üretilir (§7); her türev metin mecraya göre yeniden yazılır." Seçilmeyen mecra için türev üretilmez (recommend: `mk_platforms`'tan).

#### 3.6 `mk_shortlink` — select — "Kısa Bağlantı" (`mk_dist`; yedek: 62 mk_measure, `mk_utm`'nin altında)
Kanıt: kapak "Tüm linklerde UTM parametreleri ve kısa link standardı uygulanmalıdır."; §5 "Kısa Link: Kurumsal link kısaltma sistemi üzerinden oluşturulmalıdır."; blog §19.2 "UTM kodlu kısa link oluşturulur."
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Kurumsal kısa alan adıyla kısa bağlantı (önerilen) | `brand` | Kurum kendi kısa alan adını (ör. markaadi.link) kullanıyorsa; tıklama markalı ve ölçülebilir olur. | "kisa.markaadi.com/kira-stopaji" |
| Hazır kısaltma servisi | `service` | Kurumsal kısa alan adı yoksa. | Servisin alan adıyla kısa bağlantı. |
| Kısa bağlantı kullanılmaz (UTM'li tam adres) | `none` | Bağlantı yalnız tıklanabilir alanlarda (e-posta, LinkedIn) paylaşılıyorsa. | Tam UTM'li adres. |

ruleDetail ortak: "Kısa bağlantı UTM'li adresten üretilir, yayından önce test edilir ve kısa link listesine (kaynak URL, UTM'li URL, kısa link, mecra) yazılır." (§3 aşama 2 çıktısı "Kısa link listesi").

#### 3.7 `mk_shortlink_domain` — text — "Kısa Bağlantı Alan Adı" (showIf `mk_shortlink` = `brand`)
Kanıt: §5 aynı satır. Placeholder "Örn. kisa.ornekfirma.com". (İstenirse Ortak Bilgiler 77'ye de konabilir; yalnız bağlantı üretiminde kullanıldığı için bölüm içinde öneriyorum.)

#### 3.8 `mk_employee_share` — boolean — "Çalışan Paylaşımları" (`mk_dist`; yedek: 54 mk_social)
Kanıt: §7 "Çalışan paylaşımları ana paylaşım sonrası 1-3 saat içinde yapılabilir."; 6.4 "Link, başlık, CTA, telefon, etiket ve çalışan paylaşımı kontrol edilir." showIf (öneri): `mk_platforms` içinde `linkedin`. yes.scenario: "Çalışanların LinkedIn hesaplarından kurumsal paylaşımı yaymak isteniyorsa." yes.example: "Kurum postundan 1–3 saat sonra çalışanların kendi sözcükleriyle paylaşacağı kısa metin önerisi plan kartında hazır gelir." no.scenario: "Çalışan paylaşımı programı yoksa ya da kişisel hesaplar kurumsal içerikte kullanılmayacaksa." no.example: "Yalnız şirket sayfasından paylaşılır." Kural (açıkken): "Çalışanlar için ayrı ve kısa metin önerisi hazırlanır; paylaşım ana paylaşımdan 1–3 saat sonra ve gönüllüdür; çalışanın adına paylaşım yapılmaz."

#### 3.9 `mk_pub_steps` — multiselect — "Yayım Operasyonu Adımları" (`mk_dist`; yedek: 63 mk_flow)
Kanıt: §3 tablo. Rule: "Her içerik seçili adımlardan sırayla geçer; her adımın çıktısı plan kartına yazılır." (Onay akışı `mk_flow` ayrı kalır; bu adımlar onaydan sonraki yayım operasyonudur.)
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| Ana kaynak hazırlığı (yayın URL'si, SEO, görseller) | `source` | Dağıtım bir blog / landing sayfasına bağlanıyorsa. | Plan kartında "Kaynak URL: …" yazılmadan dağıtım adımı açılmaz. |
| UTM ve kısa bağlantı listesi | `utm` | `mk_utm` ≠ none. | Mecra başına UTM'li adres + kısa link tablosu. |
| Platform uyarlaması (caption, ölçü, etiket, CTA) | `adapt` | Birden çok mecra seçiliyse. | Her mecra için ayrı metin. |
| Tasarım dışa aktarımı (PNG / JPG / MP4 / PDF) | `export` | Tasarım ekibi ayrıysa. | Platform başına doğru ölçüde dosyalar. |
| Zamanlama (tarih, saat, saat dilimi) | `schedule` | Zamanlama aracı (Meta Business Suite Planner vb.) kullanılıyorsa. | "Planlandı · 12 Kasım 09:30 (GMT+3)". |
| Yayın kontrolü (görünüm, link, CTA) | `live_check` | Her zaman önerilir. | "Canlı · bağlantı ve CTA test edildi". |
| Raporlama (UTM, GA4, platform, form, arama) | `report` | `mk_measure_scope` seçiliyse. | Performans raporuna satır. |

Seçeneklere sorumlu rol `mk_roles`'tan bağlanabilir (aşağıdaki değişiklik).

#### 3.10 `mk_post_check` — multiselect — "Yayın Sonrası İzleme" (`mk_dist`; yedek: 62 mk_measure)
Kanıt: §2 "İlk 24 saat erişim, tıklama, yorum, form, arama ve hata kontrolü yapılmalıdır."; §10 tablo; 6.6 "İlk 24 saat izlenme, CTR …"; 6.8 "24-72 saat performans izlenir."
| Etiket | Değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|---|
| İlk 30 dakika canlılık kontrolü (görünüm, link, görsel, hatalı kırpma, yorum) (önerilen) | `m30` | Her yayında; hata erken yakalanır. | "Canlılık kontrol notu" kaydı. |
| İlk 24 saat performansı (erişim, gösterim, tıklama, yorum, paylaşım, form, arama) | `h24` | Kampanya ve reklam destekli içerikler. | Platform insight + GA4 UTM verisi. |
| 48–72 saat karşılaştırma, yorum yanıtları, ek dağıtım ihtiyacı | `h72` | Video (YouTube, TikTok) ve kampanyalar. | "Öğrenim notu ve optimizasyon". |
| 7 gün kampanya toplam etkisi | `d7` | Kampanya bazlı çalışmalar. | Haftalık rapor / dashboard. |
| Aylık kanal bazlı performans | `month` | Düzenli içerik akışı. | Şirket, hizmet, platform ve format bazlı rapor. |

Not: `mk_report_rhythm` ile çakışmaz; o rapor ritmidir, bu içerik başına izleme noktalarıdır.

#### 3.11 `mk_ads_boost` — boolean — "Organik İçerikten Reklam" (59 mk_ads, showIf `mk_ads_channels` ≠ none)
Kanıt: 6.16 "Organik İçerikten Reklama: İyi performans gösteren organik içerik reklam varyasyonuna dönüştürülebilir. — CTA, landing, kreatif ve UTM ayrılaştırılır."; 6.8 "Organik performans iyi ise reklam dağıtımı için yeniden kullanılabilir." yes.scenario: "Organik paylaşımlardan iyi performans gösterenleri reklamla büyütmek isteniyorsa." yes.example: "48–72 saat izlemede öne çıkan Reels, reklam varyasyonu olarak ayrı UTM (utm_medium=cpc) ve kampanyaya özel açılış sayfasıyla yayınlanır." no: "Reklam kreatifleri ayrı üretilir." (Reklam kılavuzu ajanıyla birleştirin.)

### 4. Mevcut alanlarda değişiklik önerileri (Yayım ve dağıtım)
1. **`mk_utm` — yeni seçenek `content_based`** "İçerik bazlı şema (kaynak = platform, ortam = social / cpc / newsletter / banner / referral, kampanya = kampanya veya içerik adı, içerik = varyasyon / konum, term = reklam anahtar kelimesi)". ruleDetail: "utm_source mecra adıdır (linkedin, facebook, instagram, x, youtube, google, whatsapp, email); utm_medium organik sosyalde social, reklamda cpc, bültende newsletter, banner'da banner, iş ortağında referral; utm_campaign kampanya ya da içerik adıdır (küçük harf, tireli, Türkçe karaktersiz); utm_content aynı kampanyadaki varyasyonu ve konumu ayırır (video-reel, carousel-slide1, mail-footer, banner-ust); utm_term yalnız Google Ads anahtar kelimesinde kullanılır, organik sosyalde boş bırakılır; organik ve reklam UTM'leri ayrı raporlanır." Kanıt §5 tablo, 6.16. `mk_utm_campaign` showIf'i bu seçenekte gizlenmeli (kampanya adı içerik başına verilir → B). Mevcut `standard` seçeneği korunur (dönem bazlı plan şablonu ona göre çalışıyor).
2. **`mk_utm` = `standard` ruleDetail:** e-posta için kılavuz `utm_source=email`, `utm_medium=newsletter` kullanıyor; mevcut kural "e-postada email" (medium). Plan şablonu `standard`'a göre üretiyorsa bu seçenek değişmemeli; fark `content_based` ile karşılanır.
3. **`mk_measure_scope` — yeni seçenekler** (§11 KPI seti, 6.6, 6.7, 6.12–6.15):
   - `mail` "Mailing (açılma, tıklama, CTOR, bounce, abonelikten çıkma, form dönüşümü)" — showIf yok, ama recommend `mk_mail_on`; ruleDetail "GA4 ve mailing raporu eşleştirilir".
   - `video` "Video izlenme (3 sn, %25, %50, %75, %100, ortalama izleme süresi, CTR)".
   - `gbp` "Google İşletme Profili performansı (arama, yol tarifi, arama düğmesi, web tıklaması)" — ruleDetail "UTM link raporuyla eşleştirilir".
   - `crm` "Form / lead ve CRM verisi" — ruleDetail "Platform metrikleri + GA4 + CRM dönüşüm verisi birlikte raporlanır".
   - `calls` "Telefon aramaları (çağrı raporu)" — `mk_conversions` = phone tıklamayı ölçer, çağrı sistemi verisi ayrı.
   - `pr` "PR etkisi (yayın sayısı, backlink, erişim, tonlama — kliping)" — basın bülteni bölümü açılırsa.
   - (SMS ve podcast bölümleri eklenirse: `sms` "SMS (teslim, tıklama, dönüşüm, opt-out)", `podcast` "Podcast (dinleme, tamamlanma, kanal, CTA tıklaması)".)
4. **`mk_report_outputs` = `exec` / aylık rapor ruleDetail:** "Aylık rapor şirket (çok markalı yapıda), hizmet, platform ve format kırılımlarıyla hazırlanır." Kanıt §10 "Aylık … Şirket, hizmet, platform ve format bazlı rapor".
5. **`mk_roles` — yeni seçenekler:** `web` "Web / CMS sorumlusu" (§3 "İçerik / Web Ekibi", "Sosyal Medya / Web"), `crm` "CRM sorumlusu" (§3 "Sosyal Medya / CRM"), `analytics` "Dijital pazarlama ve ölçüm uzmanı" (§3 "Dijital Pazarlama" — UTM, kısa link, raporlama; mevcut `ads` yalnız reklam). Basın bülteni bölümü eklenirse `pr` "Kurumsal iletişim / PR".
6. **`mk_post_times` = `fixed` ruleDetail ek (kanal varsayılanları):** "Blog ana kampanya gününden önce ya da aynı gün sabah; LinkedIn B2B'de iş saatleri; Instagram / Facebook kitlenin aktif saatleri ve farklı metin; WhatsApp Kanal öğle ya da mesai sonu öncesi, gereksiz tekrar yok; mailing sabah / öğle test edilir; Google İşletme Profili haftalık; saat dilimi her zamanlamada kontrol edilir." Kanıt §7, §3 aşama 5.
7. **`mk_derive` = `hub` ruleDetail ek:** "Hizmet sayfası, landing page veya kampanya sayfası da ana kaynak olabilir; dağıtım linkleri kaynak yayına alındıktan sonra üretilir." Kanıt §2, §7 "Dağıtım linkleri blog yayına alındıktan sonra hazırlanır."
8. **`mk_mail_*` (Mailing kılavuzu ajanıyla birleştirilecek):** `mk_mail_formats` = `html` ruleDetail'e "hero / banner 600–800 px genişlik, düşük dosya boyutu; preheader boş bırakılmaz; tek ana CTA + telefon + UTM'li link"; isteğe bağlı boolean `mk_mail_ab` "Konu Satırı A/B Testi" (Kanıt §7 "A/B konu başlığı testi uygulanabilir.").
9. **`mk_flow` / final checklist:** kural metnine "yayından önce KVKK, telif, izin ve marka onayı tamamlanır" (§9) eklenebilir; `mk_flow` = `none` ruleDetail'i zaten "yayın öncesi kontrol listesini içeriği hazırlayan kişi uygular" diyor — listenin içeriği §9'dan alınabilir (C).

### 5. B sınıfı brief alanları
Ana URL / kaynak URL · utm_campaign (içerik bazlı şemada) · utm_content varyasyonu · utm_term (Ads) · Kısa link · Platform başına caption · Yayın tarihi, saati, saat dilimi · Hedef segment (mailing / SMS) · Mailing konu başlığı ve preheader · SMS metni · Podcast bölüm başlığı, açıklaması, bölüm numarası, transkript · Basın bülteni başlığı, spotu, tarih, şehir, alıntı · Medya listesi segmenti · GBP teklif / etkinlik başlangıç–bitiş tarihi · LinkedIn etkinlik bilgileri · Reklam varyasyonu · Rapor dosyası.

### 6. C sınıfı ilkeler
1. Aynı içerik tüm platformlara birebir kopyalanmaz; metin uzunluğu, görsel ölçü, CTA ve ton platforma göre uyarlanır.
2. Yayın tarihi, saat, ölçü, link, etiket, görsel, metin, UTM ve telefon kontrol edilmeden içerik yayına alınmaz.
3. Dağıtım linkleri kaynak içerik yayına alındıktan sonra hazırlanır; kaynak URL yayında ve çalışır olmalıdır.
4. Kısa link yayından önce test edilir; CTA linki ve telefon her platformda doğrulanır.
5. Görsel tutarlılık: logo, renk, font, güvenli alan ve görsel dil marka kimliğine uyar.
6. Dosyalar sürümlü adlandırılır; video için altyazılı sürüm, podcast için MP3 dağıtım + WAV arşiv + transkript, PDF için web optimize (baskıda CMYK / PDF-X) hazırlanır.
7. Meta Business Suite'te Facebook ve Instagram birlikte planlansa da ölçü, metin uzunluğu, etiket ve CTA dili ayrı optimize edilir; doğru hesap, tarih, saat ve saat dilimi kontrol edilir.
8. WhatsApp Kanal ve SMS'te tek aksiyon; bir kampanya için aşırı sık paylaşım / gönderim yapılmaz.
9. Platform teknik gereklilikleri değişebilir; video süreleri, dosya boyutları, reklam formatları ve yetkiler için yayım öncesi güncel yardım merkezi kontrol edilir.
10. Final checklist (§9): kaynak URL, UTM, kısa link, CTA + telefon, ölçü, güvenli alan / logo / altyazı / CTA çakışması, platform dili, etiketler, tarih–saat–saat dilimi, mobil önizleme, KVKK / telif / izin / marka onayı, raporlama dosyası.

---

## Diğer ajanlarla çakışma notları
- Altyazı (`mk_subtitles`), video süreleri: Video ve Uzun Formatlı Video kılavuzları.
- Brief yerleşim tarifi, dosya adlandırma: Tek tip tasarım brief kılavuzu, F/Z patern kılavuzu.
- Mailing preheader / banner / A/B: Mailing kılavuzu.
- SMS, podcast, basın, reklam (LinkedIn / TikTok Ads, organikten reklama), föy (CMYK): ilgili kılavuzlar. Bu raporda yalnız yayım kılavuzundaki alıntılar listelendi, bölüm önerilmedi.
- CTA telefonu / CTA biçimi: Hizmet tanıtım sayfası / föy / mailing kılavuzları da CTA + telefon isteyebilir; tek alan (`oc_cta_phone`, `mk_cta_format`) yeterli.
