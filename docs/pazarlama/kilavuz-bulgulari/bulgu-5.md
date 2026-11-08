# Bulgu 5 — Sunum, Fiyat Teklifi, Hizmet Tanıtım Föyü

Okunan kılavuzlar (üçü de baştan sona, bütün bölümler):
- `Sunum_Olusturma_Kilavuzu_Kurumsal.txt` (399 satır, 18 bölüm)
- `Fiyat_Teklifi_Olusturma_Kilavuzu_Kurumsal.txt` (410 satır, 16 bölüm — içindekilerde 15 yazıyor, 16. "Dosya İsimlendirme Standardı" sonda ek olarak var)
- `Hizmet_Tanitim_Foyu_Olusturma_Kilavuzu_Kurumsal.txt` (408 satır, 15 bölüm)

Üç kılavuzda da şirket adı, telefonu ya da rengi yok. Tek istisna: föy §10 örnek satırında bir telefon numarası (`444 4 908`) geçiyor. Bu bir örnek; seçenek ya da varsayılan yapılmamalı. Bütün kılavuzlar `[MARKA]`, `[TELEFON]`, `[CTA_LINK]` gibi genel yer tutucularla yazılmış.

---

## 0. Karar: tek bir "Satış Dokümanları" bölümü mü, ayrı bölümler mi?

**Öneri: tek bölüm değil. Menüde yeni bir "Satış Dokümanları" grubu (kategori) açılsın; altında üç ayrı bölüm olsun: Sunum, Hizmet Tanıtım Föyü, Fiyat Teklifi. Üç belgenin ortak kullandığı kurum bilgileri Ortak Bilgiler'e konsun.**

Gerekçeler:
1. **Alan sayısı.** Üç kılavuzdan çıkan A sınıfı kararlar ortak alanlar hariç yaklaşık 22 alan ediyor: sunum 6, föy 6, teklif 11. Bunlar tek bölümde toplanırsa bölüm başına ~8–10 alan sınırı aşılır. Ayrı bölümlerde dağılım 6 / 6 / 11 olur.
2. **Belgeler birbirinden bağımsız açılıp kapanıyor.** Sunum yapan birçok kurum teklif hazırlamaz (ör. B2C e-ticaret). Föy de basılı ya da PDF bir materyal olarak ayrı bir karardır. Uygulamanın kalıbı "bölüm açma boolean'ı + showIf"tir (`mk_mail_on`, `mk_evt_on`). Tek bölümde bu ancak bir tür seçimi (multiselect) ve onun altında üç showIf zinciriyle olur. Bu da rehberi, ilerlemeyi ve kural metnini karıştırır.
3. **Biçimler ve teknik standartlar farklı.**
   - Sunum: 16:9, 1920×1080, PPTX + PDF, punto 34–44 / 18–24.
   - Föy: A4 dikey, baskıda 300 DPI CMYK ve taşma payı, DOCX / InDesign / Figma / Canva.
   - Teklif: A4 dikey, punto 9–11 / 8–9, para birimi, KDV, geçerlilik, hukuki nitelik.

   Kural metinleri ortak değil.
4. **Sahipler ve onay zincirleri farklı.** Sunum ve föy pazarlamanın içeriğidir; mevcut `mk_flow` / `mk_approvers` onay akışından geçer. Teklif ise ayrı bir iç onay zinciri kullanır: "Satış / Pazarlama → Hizmet / Proje Ekibi → Finans / Yönetim → Hukuk / Uzman → Kurumsal İletişim" (teklif §13). Teklifin sorumlu ajanı da farklı: sunum ve föy için Pazarlama (09), teklif için Satış (08) ile Finans (02) uygun. Bölüm varsayılan ajanı (`agents`) ayrı bölümde temiz kurulur.
5. **"Birlikte görünsün" isteğini grup karşılıyor.** Sol menüdeki "Satış Dokümanları" başlığı üç belgeyi art arda gösterir. Gruplar zaten bölümler arası kategori işi görüyor.
6. **Ortak veriler tekrarlanmamalı.** Üç kılavuzun tekrar tekrar istediği kurum bilgileri Ortak Bilgiler'e gider (§5'teki öneriler): satış iletişimi, teklif / iletişim formu adresi, ana çağrılar (CTA), referans–sertifika–metrik listesi, ofis belgelerinde yedek font. Logo, renk, font, ikon, ton ve hitap zaten 01 `brand` ve 79 `oc_brand`'da var. Üç bölüme `refs` verilip `ocRefBox` ile gösterilir.

Önerilen yer: pazarlama alanında **İçerik** grubundan (52–55) sonra, **Kanallar** grubundan (56 `mk_days`) önce. Sıra: `mk_deck` → `mk_flyer` → `mk_quote`. Bölüm kodları (48–66 …) yeniden numaralanır.

Daha az bölüm istenirse alternatif: föy `mk_prod`'a (51 Ürün & Hizmet Tanıtımı) eklenebilir. Bunun emsali var: aynı bölümdeki `mk_prod_mail` "Tanıtım Maili" boolean'ı türetilmiş bir çıktıyı açıyor. Föy alanları `mk_prod_flyer` boolean'ına showIf ile bağlanır, bölüm 7+6=13 alana çıkar. Bunu önermiyorum: sınır aşılır ve "Hizmet Tanıtım Sayfası" kılavuzunu inceleyen ajan da büyük olasılıkla `mk_prod`'a alan ekleyecek.

---

## 1. SUNUM OLUŞTURMA KILAVUZU

### 1.1 Özet
**Amaç (§1):** Sunumu yalnız slayt seti olarak değil, "karar vericiyi yönlendiren, markayı temsil eden ve hedeflenen aksiyonu üreten kurumsal iletişim araçları" olarak üretmek. Kısa ve uzun versiyon için ayrı akış tanımlar.

**Bölümler (sırasıyla):**
1. Amaç ve Kapsam
2. Sunum Türleri
3. Kısa / Uzun Karar Matrisi
4. Ön Hazırlık Briefi
5. Teknik Tasarım Standartları
6. Görsel Hiyerarşi ve Yerleşim
7. Kısa Versiyon (7 slaytlık akış)
8. Uzun Versiyon (9 bölüm: Açılış, Bağlam, İçgörü, Çözüm, Metodoloji, Kanıt, Teknik Detay, Teklif / Paket, Kapanış)
9. Slayt Tipleri (Kapak, Bölüm Ayırıcı, Problem, Veri / Grafik, Süreç, Karşılaştırma, Case Study, CTA)
10. Grafik / Tablo / Veri
11. Medya / Video / Animasyon
12. Konuşmacı Notları
13. Platform ve Çıktı (PPTX, PDF, Google Slides, Keynote, SlideShare / Web, Webinar, Video, Görsel Export)
14. Erişilebilirlik
15. Dosya İsimlendirme
16. Yayın / Dağıtım
17. Final Checklist
18. Kopyalanabilir Brief

**Sunum türleri (§2) ve önerilen versiyon:**

| Tür | Önerilen versiyon |
|---|---|
| Kurumsal tanıtım | Kısa + uzun |
| Hizmet / ürün | Kısa + uzun |
| Satış | Kısa |
| Eğitim | Uzun |
| Webinar / etkinlik | Uzun |
| Yönetim | Kısa + uzun |
| Pitch / yatırımcı | Kısa |
| Rapor | Uzun |

**Sayısal standartlar:**

| Konu | Standart |
|---|---|
| Kısa versiyon | 5–10 slayt, 3–10 dakika |
| Uzun versiyon | 15–35 slayt (eğitimde daha uzun olabilir), 15–60 dakika |
| Sunum başlığı | En fazla 6–8 kelime |
| Varsayılan oran | 16:9 (13,333 × 7,5 inç = 1920×1080 px). 4:3 yalnız eski projeksiyon ya da kurum standardında. A4 yalnız föy / PDF doküman çıktısında |
| Güvenli alan | Kenarlardan en az %5 |
| Punto | Başlık 34–44 pt (yoğun slaytta en az 28). Alt başlık 20–28 pt. Gövde 18–24 pt, hiçbir zaman 16 pt'nin altında değil. Dipnot / kaynak 9–11 pt |
| Görsel | Tam ekran en az 1920×1080; mümkünse 2x |
| Tablo | 5–7 satırı aşarsa eke ya da özete |
| Geçiş | 0,3–0,7 sn |
| Gömülü video | MP4 / H.264 + harici yedek |
| Video sunum | MP4 / H.264, 1920×1080, AAC ses, gerekirse SRT ya da gömülü altyazı |
| Slayt görsel export | 1920×1080 PNG / JPG; sosyal medya uyarlaması 1080×1350 ve 1080×1920 ayrı çalışılır |
| Süreç slaytı | 3–6 adım |
| Kısa versiyonda süreç | 3–4 adım |
| Kısa versiyonda fayda | 3–5 madde |
| Karşılaştırma slaytı | 2–3 kolon |

**Süreç:** brief (§4) → tür ve versiyon seçimi (§3) → teknik şablon (§5) → slayt akışı (§7 ya da §8) → veri ve medya (§10–11) → konuşmacı notları (§12) → çıktılar (§13) → isimlendirme (§15) → dağıtım (§16) → checklist ve "Final onay süreci" (§17).

**Uyum maddeleri:**
- Kaynak kullanılan her verinin slayt altında kaynak notu olur (§10).
- Görsellere alt açıklama eklenir (§14).
- Renkle verilen bilgi metin ya da şekille desteklenir (§14).
- "Final onay süreci tamamlandı mı?" (§17).
- Font dosyaları paylaşılmaz: "font dosyaları kullanıcıyla paylaşılmamalı, yalnızca font adı belirtilmelidir" (§5) — lisans maddesi.

### 1.2 A sınıfı bilgiler

| Alıntı | Mevcut karşılık | Durum ve eksik |
|---|---|---|
| "Varsayılan Oran — 16:9 geniş ekran … 4:3 yalnızca eski projeksiyon veya kurum standardı gerektiriyorsa" | yok | Yok. Sunum en-boy oranı kararı yok. |
| "Kurumsal Tanıtım Sunumu … Satış Sunumu … Eğitim … Webinar … Yönetim … Pitch … Rapor" | yok | Yok. Kurumun hangi sunum türlerini ürettiği bilinmiyor. |
| "Dosya Çıktısı — PPTX kaynak, PDF yayın, PNG/JPG slayt exportu, gerekiyorsa MP4 video çıktı" / §13 Google Slides, Keynote | yok | Yok. |
| "konuşmacı notları slayt içeriğini tamamlayan ayrı bir anlatım katmanı olarak hazırlanmalıdır" | yok | Yok. |
| "Slaytlar carousel, kısa video veya tek görsel formatına yeniden uyarlanmalıdır" / "1080x1350 ve 1080x1920 ayrı çalışılmalıdır" | `mk_derive` (yalnız blog → sosyal), `mk_formats` | Kısmi. Sunumdan sosyal medya türetme yok. |
| "Kurumsal font ailesi kullanılmalı; … yalnızca font adı belirtilmelidir" | `brand_font_heading`, `brand_font_body` (79) | Tam. Ofis yazılımında yedek font eksik; bkz. teklif ve §5 `oc_font_office`. |
| "Marka renkleri korunmalı; ana zemin, ana metin, vurgu ve CTA rengi açıkça tanımlanmalıdır" | `brand_color_primary/secondary/accent` (79), `brand_neutral` (01) | Tam. |
| "İkon — Aynı stil ailesinden seçilmeli; outline/flat karışık kullanılmamalıdır" | `brand_icons` (01) | Tam. |
| "Yüksek çözünürlüklü, düşük stok hissi veren … görseller" | `brand_imagery` (01), `mk_visual_source` (55) | Tam. |
| "Master slide, tema renkleri ve font ayarları korunmalıdır" (PPTX) | `brand_deliverables` (01) | Kısmi. "Sunum ana şablonu (PPTX master)" teslim dosyası yok; bkz. §6 değişiklik önerileri. |
| "CTA … Teklif al, iletişime geç, demo talep et, kaydol, form doldur, danışmanlık talep et" | yok | Yok. Kurumun varsayılan çağrıları yok; bkz. §5 `oc_cta`. |
| "Telefon / İletişim — CTA ile birlikte kullanılacak telefon, e-posta veya form linki" | `mk_contact` (77) | Kısmi. Telefon ve e-posta var; varsayılan form adresi yok (bkz. `oc_lead_url`). |
| "Kanıt — Referans, vaka, başarı metriği, müşteri yorumu, sertifika" | `social_proof` (04, yalnız site), `mk_banned` client_logo | Kısmi. Kullanılabilecek referans / sertifika listesi yok (bkz. `oc_proof`). |
| "Kurumsal Tanıtım Sunumu — Marka, şirket, vizyon, hizmetler ve güven unsurlarını tanıtmak" | `mk_slogan`, `oc_tagline` (77) | Kısmi. Vizyon / misyon yok (bkz. `oc_mission`). |
| "[MARKA]_[SUNUM_KONUSU]_[VERSIYON]_[TARIH].pptx" | `mk_prefix` (66), `mk_brand_name` | Kısmi. [MARKA] kısaltması `mk_prefix`'ten alınabilir; kalıbın kendisi C sınıfı (kural metni). |
| "Final onay süreci tamamlandı mı?" | `mk_flow`, `mk_approvers` (63) | Tam. Akış var; onaylayanlarda "Satış yöneticisi" eksik (bkz. §6). |

### 1.3 Yeni alan önerileri — yeni bölüm `mk_deck` "Sunum Standardı" (grup: **Satış Dokümanları**; İçerik grubu da olabilir)

Bölüm `refs`: `mk_brand_name`, `brand_color_*`, `brand_font_*`, `oc_font_office`, `mk_contact`, `oc_sales_contact`, `oc_lead_url`, `oc_cta`, `oc_proof`, `oc_logo`.

**1) `mk_deck_on` — boolean — "Sunum Standardı"**
- **Evet:**
  - Ne zaman doğru: Kurum satış görüşmesi, webinar, eğitim ya da yönetim toplantısı için düzenli sunum hazırlıyorsa.
  - Nasıl görünür: Claude her sunumu 16:9 şablonda, kısa ya da uzun akışla, konuşmacı notları ve kapanış CTA'sıyla üretir.
- **Hayır:**
  - Ne zaman doğru: Kurum sunum üretmiyor.
  - Nasıl görünür: Sunum kuralı yazılmaz.
- Kanıt: "Kapsam — Kısa sunum, uzun sunum, satış sunumu, hizmet tanıtımı, eğitim, webinar, yönetim sunumu, yatırımcı/pitch sunumu".

**2) `mk_deck_types` — multiselect — "Sunum Türleri"** (showIf `mk_deck_on` = true)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Kurumsal tanıtım = `corporate` | Marka, vizyon ve hizmetler ilk temasta tanıtılıyorsa | Kısa ve uzun sürüm. Vizyon, hizmetler ve güven slaytları |
| Hizmet / ürün tanıtımı = `service` | Tek bir hizmetin kapsamı ve süreci anlatılıyorsa | Kapsam, fayda, süreç ve CTA slaytları |
| Satış = `sales` | Müşteri ihtiyacı çözüm ve teklif yapısına bağlanıyorsa | 5–10 slaytlık kısa akış, erken CTA |
| Eğitim = `training` | Katılımcıya süreç ve uygulama öğretiliyorsa | 15–35+ slayt, bölüm ayırıcılar, soru alanları |
| Webinar / etkinlik = `webinar` | Canlı anlatım destekleniyorsa | Konuşmacı penceresi için boş alan, ara CTA'lar |
| Yönetim = `management` | KPI, hedef ve karar aktarılıyorsa | Yönetici özeti, veri slaytları, aksiyon planı |
| Yatırımcı (pitch) = `pitch` | Problem, pazar, model ve talep anlatılıyorsa | Kısa, hikâye akışlı sunum |
| Rapor = `report` | Bulgular ve öneriler sunuluyorsa | Uzun sürüm; tablolar ekte, her grafikte kaynak notu |

- Kanıt: §2 tablosu. Her türün önerilen versiyonu kural metnine yazılır (C).

**3) `mk_deck_ratio` — select — "Slayt Oranı"** (showIf `mk_deck_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| 16:9 geniş ekran (1920×1080) **(önerilen)** = `r169` | Ekran, online toplantı, webinar ve PDF paylaşımı | 13,333 × 7,5 inç PPTX |
| 4:3 = `r43` | Eski projeksiyon ya da kurum standardı gerektiriyorsa | 4:3 şablon; görsel export oranı da 4:3 |

- Kanıt: "Varsayılan Oran — 16:9 geniş ekran … 4:3 yalnızca eski projeksiyon veya kurum standardı gerektiriyorsa".

**4) `mk_deck_outputs` — multiselect — "Teslim Çıktıları"** (showIf `mk_deck_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| PPTX kaynak dosya **(önerilen)** = `pptx` | Düzenlenebilir ana kaynak her zaman saklanacaksa | Master slayt, tema renkleri ve fontlar ayarlı .pptx |
| PDF **(önerilen)** = `pdf` | E-postayla ya da indirme için paylaşılacaksa | Bağlantıları tıklanabilir, sayfa kırılımı kontrollü PDF |
| Google Slides = `gslides` | Ekip bulutta çalışıyorsa | Font ve görsel kayma kontrolü notu |
| Keynote = `keynote` | Mac ortamında teslim isteniyorsa | Font, animasyon ve video uyumu testi |
| Slayt görselleri (PNG / JPG 1920×1080) = `images` | Slaytlar web'de ya da yazıda görsel olarak kullanılacaksa | `[MARKA]_[KONU]_Slide01_1920x1080.png` |
| Video sunum (MP4) = `mp4` | Sunum kayıtlı video olarak yayımlanacaksa | MP4 / H.264, AAC, altyazı SRT ya da gömülü |

- Kanıt: "Dosya Çıktısı — PPTX kaynak, PDF yayın, PNG/JPG slayt exportu, gerekiyorsa MP4 video çıktı" ve §13 tablosu.

**5) `mk_deck_notes` — select — "Konuşmacı Notları"** (showIf `mk_deck_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Her slaytta not, süre planı ve geçiş cümlesi **(önerilen)** = `full` | Sunumu anlatan kişi slayttan farklı biri olabiliyorsa | Notlar bölmesinde konuşmacı notu, hedef süre, geçiş cümlesi; webinar ve eğitimde soru noktası; kapanışta CTA anlatımı |
| Yalnız yönetim, satış ve webinar sunumlarında = `selected` | Diğer sunumlar kendi kendine okunacaksa | Bu üç türde not katmanı, diğerlerinde yok |
| Konuşmacı notu yok = `none` | Sunumlar yalnız PDF olarak gönderiliyorsa | Notlar bölmesi boş |

- Kanıt: "Sunum yalnızca slayt üstü metinden oluşmamalıdır. Özellikle yönetici, satış ve webinar sunumlarında konuşmacı notları … hazırlanmalıdır." ve §12 tablosu (Konuşmacı Notu, Süre Planı, Geçiş Cümlesi, Soru Alanı, CTA Anlatımı).

**6) `mk_deck_social` — boolean — "Sosyal Medya Uyarlaması"** (showIf `mk_deck_on`)
- **Evet:**
  - Ne zaman doğru: Sunumlar sosyal medyada da kullanılacaksa (kısa versiyonun "sosyal paylaşım kaynağı" senaryosu).
  - Nasıl görünür: Claude seçili slaytlardan 1080×1350 carousel ve 1080×1920 dikey sürüm çıkarır; metni mobilde okunacak kadar sadeleştirir.
- **Hayır:**
  - Nasıl görünür: Yalnız 16:9 çıktı üretilir.
- Kanıt: "sosyal medya uyarlamasında 1080x1350 ve 1080x1920 ayrı çalışılmalıdır" ve "Sosyal Medya Uyarlaması — Slaytlar carousel, kısa video veya tek görsel formatına yeniden uyarlanmalıdır".
- Not: `mk_platforms` boşsa öneri notu verilebilir.

### 1.4 B sınıfı (sunum briefi, form alanı değil)
- Sunum başlığı (en fazla 6–8 kelime)
- Marka / şirket (çok markalı yapıda)
- Sunum türü
- Versiyon (kısa / uzun / ikisi)
- Hedef kitle ve karar verici seviyesi
- Sunum amacı
- Ana mesaj (tek cümle)
- Bu sunumun CTA metni ve linki
- Sunum ortamı (yüz yüze, online, webinar, sahne, PDF)
- Planlanan slayt sayısı
- Teknik format
- Tasarım notu
- Teslim formatı
- Deadline
- Slayt başına konuşmacı notu ve süre
- Grafiklerin verisi ve kaynağı
- E-posta gönderim konu ve açıklama metni (§16)

### 1.5 C sınıfı ilkeler (kurala / rehbere)
1. Her slaytta tek ana mesaj. Başlık, ana içerik, destek notu ve CTA sırasıyla okunur.
2. Punto: başlık 34–44 pt (en az 28), alt başlık 20–28, gövde 18–24, hiçbir metin 16 pt altında değil, dipnot 9–11.
3. Kenarlardan en az %5 güvenli alan. Logo, sayfa numarası, footer ve CTA bu alana taşmaz.
4. Kısa versiyon 5–10 slayt / 3–10 dk, erken ve son slaytta CTA. Uzun versiyon 15–35 slayt / 15–60 dk, bölüm sonu ara CTA ve kapanış CTA'sı.
5. Grafik başlığı sonucu yorumlar ("Satış Grafiği" değil). Her veri slaytında tek bulgu ve kaynak notu. Tablo 5–7 satırı aşarsa eke alınır.
6. Animasyon yalnız anlatımı kolaylaştırmak için. Sade geçiş, 0,3–0,7 sn.
7. Gömülü video MP4 / H.264 ve harici yedeği tutulur. Ses ve video toplantı ortamında önceden test edilir.
8. Renkle verilen kritik bilgi metin, ikon ya da şekille de verilir. Görsellerde alt açıklama bulunur.
9. Dosya adı: `[MARKA]_[KONU]_[Kisa|Uzun]_Sunum_v01.pptx`, PDF `…_[TARIH]_final.pdf` ([MARKA] = `mk_prefix` ya da marka adı).
10. Font dosyası paylaşılmaz, yalnız font adı yazılır. Webinar slaytlarında konuşmacı penceresi için sağda ya da solda boş alan bırakılır.

---

## 2. FİYAT TEKLİFİ OLUŞTURMA KILAVUZU

### 2.1 Özet
**Amaç (§1):** Teklifi "müşterinin ihtiyacını anlayan, çözümü netleştiren, kapsamı sınırlayan ve karar sürecini hızlandıran profesyonel bir satış aracı" yapmak. Ana hedef: "Kapsam, fiyat, koşul, süre, teslim ve sonraki adımı tek bakışta anlaşılır hale getirmek."

**Bölümler (sırasıyla):**
1. Amaç
2. Teklif Türleri
3. Temel İlkeler
4. İş Akışı (8 aşama)
5. Keşif Bilgileri
6. Fiyatlandırma ve Hesaplama
7. Kısa Versiyon (+7.1 kopyalanabilir akış)
8. Uzun Versiyon (14 bölüm)
9. Teklif Tablosu (+9.1 Ödeme ve Geçerlilik)
10. Hukuki / Ticari / Operasyonel Koşullar
11. Tasarım ve Teknik Doküman
12. E-posta / Sunum / CRM Teslim
13. Onay, Revizyon, Takip
14. Şablon Alanları
15. Final Checklist
16. Dosya İsimlendirme

**Teklif türleri (§2):**

| Tür | Uzunluk |
|---|---|
| Kısa | 1–2 sayfa |
| Uzun | 6–15 sayfa |
| Revizyon | 1–4 sayfa |
| Paket karşılaştırmalı | 2–6 sayfa ("Standart/Profesyonel/Enterprise") |
| Abonelik / yenileme | 1–4 sayfa (SaaS, bakım, retainer) |

**Sayısal standartlar:**

| Konu | Standart |
|---|---|
| Kısa teklif | İhtiyaç özeti 40–70 kelime, koşullar en fazla 5–7 madde, tek fiyat tablosu |
| Uzun teklif | Yönetici özeti 100–180 kelime |
| Sayfa | A4 dikey (geniş tabloda A4 yatay ek) |
| Punto | Başlık 16–24, alt başlık 11–14, gövde 9–11, tablo 8–9 pt |
| Font | Kurumsal font; alternatif Arial / Calibri |
| Toplantı desteği | 5–8 slaytlık yönetici özeti |

Fiyat tablosu sütunları (§9):

| Sütun | Zorunluluk |
|---|---|
| No | Zorunlu |
| Ürün / Hizmet | Zorunlu |
| Açıklama / Kapsam | Zorunlu |
| Birim | Zorunlu |
| Adet / Süre | Zorunlu |
| Birim Fiyat | Zorunlu |
| İskonto | Opsiyonel |
| Toplam | Zorunlu |
| Not | Opsiyonel |

Hesap (§6):
- Ara Toplam = Birim Fiyat × Adet / Süre
- İskontolu = Ara Toplam − İskonto
- KDV Dahil = İskontolu + KDV
- KDV hariç toplam, KDV tutarı ve KDV dahil toplam ayrı satırlarda gösterilir.

**İş akışı (§4):** Talep Alma → Keşif ve Analiz → Çözüm Kurgusu → Fiyatlandırma → Koşullar → İç Onay (satış, finans, operasyon, hukuk, marka) → Müşteri Paylaşımı → Takip ve Revizyon.

**Uyum maddeleri:**
- KDV oranı teklif tarihinde geçerli mevzuata göre kontrol edilir.
- Dövizli teklifte kur tarihi, kur kaynağı ve ödeme tarihindeki kur uygulaması yazılır.
- Teklif sözleşme yerine geçiyorsa açıkça belirtilir; aksi halde "Bu teklif bilgilendirme ve ticari öneri niteliğindedir."
- Kişisel veri, finans, bordro, SGK, vergi, İSG, yazılım ya da entegrasyon içeren tekliflerde uzman ya da hukuk kontrolü alınır.
- Performans, tasarruf, süre ya da sonuç iddiaları doğrulanabilir olmalı.
- Dosya paylaşımında güvenli link, süre ve yetki kontrolü yapılır.
- WhatsApp yalnız ön bilgilendirme için kullanılır.

### 2.2 A sınıfı bilgiler

| Alıntı | Mevcut karşılık | Durum ve eksik |
|---|---|---|
| "Kısa Versiyon … Uzun Versiyon … Revizyon … Paket Karşılaştırmalı … Abonelik / Yenileme Teklifi" | yok | Yok. |
| "Teklif No — [MARKA]-FT-[YYYYMMDD]-[MUSTERI]-v01" | `mk_prefix` (66), `mk_brief_no` (55, yalnız brief) | Kısmi. Önek var; teklif numarası kalıbı yok. |
| "Para Birimi — TRY, USD, EUR veya kurum standardına göre belirtilir" | `locale_rules` Currency Intl (08, yalnız biçim) | Yok. Kurumun teklif para birimi yok. |
| "Dövizli tekliflerde kur tarihi ve kur kaynağı ayrıca yazılır" / "ödeme tarihindeki kur uygulaması ayrıca belirtilmelidir" | yok | Yok. |
| "KDV dahil/hariç durumu mutlaka yazılır" / "KDV hariç toplam, KDV tutarı ve KDV dahil toplam ayrı satırlarda" | yok | Yok. |
| "Bu teklif, teklif tarihinden itibaren [X gün] süreyle geçerlidir." | yok | Yok. Geçerlilik süresi standardı yok. |
| "Teklif, sözleşme yerine geçiyorsa bu durum açıkça belirtilmelidir. Aksi halde 'Bu teklif bilgilendirme ve ticari öneri niteliğindedir.'" | yok | Yok. |
| "Kabul ve İmza — Yetkili kişi, imza, tarih, kaşe, e-onay bilgisi" / kısa: "Müşteri onay imza alanı veya onay cümlesi" | yok | Yok. |
| §13: Satış / Pazarlama, Hizmet / Proje Ekibi, Finans / Yönetim, Hukuk / Uzman, Kurumsal İletişim | `mk_approvers` (63: pazarlama yöneticisi, marka sahibi, hukuk, ürün sorumlusu) | Kısmi. Finans, operasyon ve satış yok; bu zincir pazarlama içerik onayından ayrı. |
| §12: "E-posta … PDF ek … Toplantı / Sunum … 5-8 slaytlık yönetici özeti … CRM … WhatsApp … Dosya Paylaşımı — Güvenli link" | `modules_extra` crm (00, yalnız site modülü) | Yok. Teslim kanalları yok. |
| "Kişisel veri, finans, bordro, SGK, vergi … içeren tekliflerde ilgili uzman/hukuk kontrolü alınmalıdır" | `mk_legal_scope` (64: product, regulated) | Kısmi. "Fiyat teklifleri" kapsamı yok (bkz. §6). |
| "Teklifte yer alan performans, tasarruf, süre veya sonuç iddiaları doğrulanabilir olmalıdır" | `mk_banned` superlative / price_claim, `mk_ads_claims` | Kısmi. Doğrulanmamış rakam / sonuç iddiası maddesi yok (bkz. §6). |
| "Font — Kurumsal font ailesi. Alternatif olarak Arial / Calibri kullanılabilir." | `brand_font_*` | Kısmi. Ofis yedek fontu yok (bkz. `oc_font_office`). |
| "Standart/Profesyonel/Enterprise gibi seçenekli teklifler" | `mk_prod_types` package (51) | Kısmi. Paket kademe adları yok (bkz. §6 `mk_prod_tiers`). |
| "CTA açık olmalıdır: 'Teklifi Onaylayın', 'Görüşme Planlayın', 'Satın Alma Sürecini Başlatalım'" | yok | Yok. Bkz. `oc_cta`. |
| "CTA + link + telefon + e-posta" | `mk_contact` (77) | Kısmi. Satış iletişimi ve form adresi yok. |
| "Referans / Kanıt — Referans, başarı metrikleri, vaka özeti, sertifika" | yok | Yok. Bkz. `oc_proof`. |
| "[MARKA]_[MUSTERI]_[HIZMET]_FiyatTeklifi_v01.docx" | `mk_prefix` | Kısmi. Kalıp C sınıfı. |

Fiyatın gösterim politikası (`mk_prod_price` open / from / quote) teklifle çelişmez. "Teklif üzerine" seçiliyse teklif bölümünün açılması önerilebilir (bkz. §6).

### 2.3 Yeni alan önerileri — yeni bölüm `mk_quote` "Fiyat Teklifi" (grup: **Satış Dokümanları**)

Bölüm `refs`: `mk_brand_name`, `oc_legal_name`, `oc_logo`, `brand_color_*`, `oc_font_office`, `mk_contact`, `oc_sales_contact`, `oc_lead_url`, `oc_cta`, `oc_proof`, `oc_services`, `mk_prefix`.

Varsayılan sorumlu ajan: 08 Satış (teklif yönetimi pozisyonu); finans alanlarında 02 Finans.

**1) `mk_quote_on` — boolean — "Fiyat Teklifi Standardı"**
- **Evet:**
  - Ne zaman doğru: Kurum B2B hizmet, proje, abonelik ya da paket için yazılı teklif veriyorsa.
  - Nasıl görünür: Claude teklifleri numaralı, geçerlilik süreli, KDV ve toplamları ayrı satırlı, kabul alanlı PDF olarak hazırlar.
- **Hayır:**
  - Ne zaman doğru: Fiyatlar yalnız sitede ya da sepette gösteriliyorsa.
  - Nasıl görünür: Teklif kuralı yazılmaz.
- Kanıt: "Kullanım Alanı — B2B hizmet, ürün, danışmanlık, proje, abonelik, eğitim, yazılım, bakım ve paket teklifleri".
- Öneri bağlantısı (isteğe bağlı): `mk_prod_price` = quote ya da `business_model` b2b / b2g iken açılması önerilir.

**2) `mk_quote_types` — multiselect — "Teklif Türleri"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Kısa teklif (1–2 sayfa) = `short` | Standart paket, mevcut müşteri, hızlı karar | Tek fiyat tablosu, 5–7 koşul maddesi, CTA, kabul alanı |
| Uzun teklif (6–15 sayfa) = `long` | Kurumsal satış, yüksek bütçe, çok paydaşlı karar | Yönetici özeti, kapsam, süreç, zaman planı, ekip, risk ve varsayımlar, ekler |
| Revizyon teklifi = `revision` | Müşteri geri bildirimiyle kapsam, fiyat ya da süre değişiyorsa | Değişikliklerin gösterildiği v02, v03 sürümü |
| Paket karşılaştırmalı = `packages` | Birden çok paket sunuluyorsa | Paket kartları ya da karşılaştırma tablosu |
| Abonelik / yenileme = `subscription` | SaaS, bakım, destek, retainer | Aylık / yıllık bedel, yenileme dönemi, kullanıcı / adet, SLA |

- Kanıt: §2 tablosu.

**3) `mk_quote_no` — select — "Teklif Numarası"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Önek + FT + tarih + müşteri + sürüm **(önerilen)** = `guide` | Teklifler kurum içinde üretilip dosyalanıyorsa | `ORN-FT-20261107-MUSTERI-v01` (önek = `mk_prefix`) |
| CRM / muhasebe sisteminin numarası = `system` | Numara satış ya da muhasebe yazılımından geliyorsa | Claude numarayı uydurmaz, `[TEKLİF_NO]` yer tutucusu bırakır |

- Kanıt: "Teklif No — [MARKA]-FT-[YYYYMMDD]-[MUSTERI]-v01" ve "CRM — Teklif numarası, müşteri, tutar … girilmelidir."

**4) `mk_quote_currency` — multiselect — "Para Birimleri"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Türk lirası (TRY) = `TRY` | Yurt içi teklifler | "12.500,00 TL", toplamlar sağa hizalı |
| ABD doları (USD) = `USD` | Dövize bağlı hizmet ya da yurt dışı müşteri | Tutar USD; kur tarihi ve kaynağı ayrıca yazılır |
| Avro (EUR) = `EUR` | AB müşterisi ya da avro maliyetli hizmet | Tutar EUR; kur notu |

- Varsayılan önerilmez ("kurum standardına göre").
- Kanıt: "Para Birimi — TRY, USD, EUR veya kurum standardına göre belirtilir."

**5) `mk_quote_fx` — select — "Dövizli Teklifte Kur"** (showIf `mk_quote_currency` in [USD, EUR])

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Ödeme tarihindeki kur uygulanır **(önerilen)** = `payment_date` | Tutar dövizle sabit, TL karşılığı ödemede hesaplanıyorsa | Koşullarda "Dövizli tutarlar ödeme tarihindeki kur üzerinden TL'ye çevrilir; kur kaynağı: […]" |
| Teklif tarihindeki kur sabitlenir = `quote_date` | Müşteriye TL karşılığı teklif günü garanti ediliyorsa | Koşullarda kur tarihi ve kur değeri yazılı |

- Kanıt: "Dövizli tekliflerde kur tarihi ve kur kaynağı ayrıca yazılır." ve "Dövizli tutarlar için ödeme tarihindeki kur uygulaması ayrıca belirtilmelidir."
- İsteğe bağlı: kurum kur kaynağını sabit yazmak isterse aynı showIf ile `mk_quote_fx_source` [text] "Kur Kaynağı" eklenebilir. Kılavuz kaynağın yazılmasını istiyor ama bir kaynak adı vermiyor; o yüzden seçenek değil, metin olmalı.

**6) `mk_quote_vat` — select — "KDV Gösterimi"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Fiyatlar KDV hariç; KDV ve genel toplam ayrı satırda **(önerilen)** = `excl` | Kurumsal müşteriye birim fiyat KDV hariç veriliyorsa | Tablo sonunda "KDV hariç toplam / KDV (%…) / KDV dahil toplam" |
| Fiyatlar KDV dahil = `incl` | Kurum standardı KDV dahil fiyat ise | Birim fiyatlar KDV dahil; altta KDV tutarı ayrıca belirtilir |

- Kanıt: "KDV / Vergi — KDV dahil/hariç durumu mutlaka yazılır." ve "Genel Toplam — KDV hariç toplam, KDV tutarı ve KDV dahil toplam ayrı satırlarda gösterilir."
- (önerilen) etiketi ayrı satır yapısına dayanıyor. Kılavuz hariç / dahil arasında bir tercih belirtmiyor; ana asistan isterse (önerilen)'i kaldırabilir.

**7) `mk_quote_validity` — select — "Teklif Geçerlilik Süresi"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| 7 gün = `d7` | Fiyatı kura ya da kampanyaya bağlı, hızlı değişen hizmetler | "Bu teklif, teklif tarihinden itibaren 7 gün süreyle geçerlidir." |
| 15 gün = `d15` | Standart paketler | Aynı cümle, 15 gün |
| 30 gün = `d30` | Kurumsal satın alma süreci olan müşteriler | Aynı cümle, 30 gün |
| 60 gün = `d60` | İhale ya da kurul onayı gereken uzun süreçler | Aynı cümle, 60 gün |
| Her teklifte ayrıca belirlenir = `per_quote` | Süre müşteriye göre değişiyorsa | `[X gün]` yer tutucusu; Claude süreyi sorar |

- Kılavuz bir değer önermiyor; (önerilen) yok.
- Kanıt: "Teklif Geçerliliği — Bu teklif, teklif tarihinden itibaren [X gün] süreyle geçerlidir." ve "Her teklif dokümanında … geçerlilik süresi … bulunmalıdır."
- İsteğe bağlı: `mk_b2b_process` = tender / committee iken 30 ya da 60 önerilebilir.

**8) `mk_quote_legal` — select — "Teklifin Hukuki Niteliği"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Bilgilendirme ve ticari öneri; sözleşme ayrıca yapılır **(önerilen)** = `proposal` | Onaydan sonra ayrı sözleşme imzalanıyorsa | Koşullarda "Bu teklif bilgilendirme ve ticari öneri niteliğindedir." |
| Onaylanan teklif sözleşme yerine geçer = `contract` | Kurum teklif onayıyla işe başlıyorsa | Kapakta ve kabul alanında bu durum açıkça yazılır; iptal ve erteleme koşulları teklifte bulunur; hukuk kontrolü önerilir |

- Kanıt: "Teklif, sözleşme yerine geçiyorsa bu durum açıkça belirtilmelidir. Aksi halde 'Bu teklif bilgilendirme ve ticari öneri niteliğindedir.' ifadesi kullanılabilir."
- Öneri bağlantısı: `contract` seçilirse `mk_quote_approval`'a legal önerilir.

**9) `mk_quote_accept` — multiselect — "Kabul Yöntemi"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| İmza alanı: ad soyad, unvan, tarih, imza, kaşe **(önerilen)** = `signature` | Islak imza ya da kaşeli onay isteniyorsa | Son sayfada imza bloğu |
| E-onay (e-posta ya da elektronik onay) = `e_approval` | Onay dijital alınıyorsa | "Onayınızı … adresine yanıtla / bağlantıyla iletebilirsiniz" |
| Onay cümlesi (kısa tekliflerde) = `statement` | Hızlı, düşük tutarlı teklifler | "Bu teklifi kabul ediyorum" cümlesi ve tarih |

- Kanıt: "Kabul Alanı — Müşteri onay imza alanı veya onay cümlesi. Ad soyad, unvan, tarih, imza alanı." ve "Kabul ve İmza — Yetkili kişi, imza, tarih, kaşe, e-onay bilgisi."

**10) `mk_quote_approval` — multiselect — "Teklif İç Onayı"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Satış (ilk taslak) **(önerilen)** = `sales` | Her teklifte | Promptta "Satış taslağı kontrol eder: ihtiyaç, kapsam, fiyat yapısı" |
| Operasyon / hizmet ekibi **(önerilen)** = `operations` | Teslim kapasitesi ve süre gerçekçi olmalıysa | "Teslim süresi ve kapsam kontrolü" |
| Finans / yönetim **(önerilen)** = `finance` | İskonto, ödeme planı ve kârlılık kontrol edilecekse | "Fiyat, iskonto, ödeme planı kontrolü" |
| Hukuk / uzman = `legal` | Taahhüt, kişisel veri, mevzuat ya da sözleşme niteliği varsa | "Taahhüt, veri, sorumluluk kontrolü" |
| Kurumsal iletişim (marka) = `brand` | Dil, tasarım ve logo standardı denetleniyorsa | "Dil, tasarım, logo kontrolü" |

- Kanıt: §13 tablosu ve checklist "Satış, finans, operasyon ve gerekiyorsa hukuk onayı alındı mı?"
- Claude onay vermez; promptta "onaysız teklif müşteriye gönderilmez, onay durumu kullanıcıya sorulur" olarak yazılır.

**11) `mk_quote_delivery` — multiselect — "Teslim Kanalları"** (showIf `mk_quote_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| E-posta + PDF ek **(önerilen)** = `email_pdf` | Ana kanal; her zaman | Claude kısa açıklama, teklif özeti, CTA, telefon ve toplantı önerisi içeren e-posta metni yazar |
| Toplantı sunumu (5–8 slaytlık yönetici özeti) = `deck` | Uzun teklif toplantıda savunulacaksa | Uzun tekliften 5–8 slayt (`mk_deck` kurallarıyla) |
| CRM kaydı = `crm` | Satış ekibi CRM kullanıyorsa | CRM alanları: teklif no, müşteri, tutar, para birimi, kapanış tarihi, olasılık, dosya, takip tarihi; başlık "[Müşteri] - [Hizmet] - [Tutar] - [Tahmini Kapanış Tarihi]" |
| Güvenli paylaşım bağlantısı = `secure_link` | Dosya e-posta eki yerine bağlantıyla paylaşılıyorsa | Erişim süresi ve yetki kontrollü bağlantı notu |
| WhatsApp / kısa mesaj (yalnız ön bilgi) = `whatsapp` | Müşteriyle mesajlaşma kullanılıyorsa | Yalnız hatırlatma ve ön bilgi metni; teklif PDF'i e-postayla |

- Kanıt: §12 tablosu, "PDF/e-posta ana kanal olmalıdır" ve "Müşteriyle paylaşılan final teklif PDF olmalı".

Bölüm 11 alan (açma boolean'ı ve showIf'li kur alanı dahil). Ödeme planı bilinçli olarak eklenmedi. Kılavuz onu `[%X peşin], [%Y teslimde]` yer tutucusuyla teklife özgü yazıyor (B). Kurum sabit bir ödeme standardı isterse `mk_quote_payment` select eklenebilir; seçenekleri peşin / kısmi peşin + teslimde / aylık-yıllık / teklif bazında olur.

### 2.4 B sınıfı (teklif başına, form alanı değil)
- Müşteri adı, iletişim kişisi, teklif sahibi, tarih, revizyon numarası.
- Keşif bilgileri:
  - müşteri profili (sektör, çalışan sayısı, lokasyon, karar verici, satın alma süreci, mevcut tedarikçi),
  - ihtiyaç / problem,
  - kapsam (kullanıcı / adet / lokasyon),
  - süre ve deadline,
  - başarı kriteri,
  - bütçe ve onay makamı,
  - risk ve bağımlılık.
- Kalemler: ürün / hizmet, açıklama, birim, adet / süre, birim fiyat, iskonto oranı ve nedeni, opsiyonel kalemler.
- Fiyat tipi (tek seferlik, aylık, kullanıcı başı …).
- Dahil / hariç kapsam ve varsayımlar.
- Hizmet süreci, zaman planı ve kilometre taşları.
- Ekip ve kurum / müşteri sorumlulukları.
- Ödeme planı, fatura dönemi, iptal / erteleme koşulları, SLA / destek saati.
- Ekler (SLA, teknik şartname, ürün listesi).
- Bu teklifin CTA'sı.
- CRM'de kapanış tarihi, olasılık ve takip tarihi.

### 2.5 C sınıfı ilkeler
1. İhtiyaç ve beklenen sonuç fiyat tablosundan önce anlatılır.
2. Her teklifte teklif no, tarih, geçerlilik, müşteri adı, iletişim kişisi, teklif sahibi ve revizyon bilgisi bulunur.
3. Fiyatlar para birimi, KDV durumu, ödeme planı, geçerlilik ve dahil / hariç kapsamla birlikte yazılır. Opsiyonel kalemler ana toplamdan ayrı gösterilir.
4. Hesap sırası: Ara Toplam = Birim Fiyat × Adet / Süre → İskonto (oran ve neden) → KDV → KDV dahil toplam. Yuvarlama ve kur farkı koşullarda açıklanır. KDV oranı teklif tarihinde güncel mevzuattan kontrol edilir.
5. Kısa teklif 1–2 sayfa: özet 40–70 kelime, tek tablo, 5–7 koşul. Uzun teklif 6–15 sayfa: yönetici özeti 100–180 kelime ve 14 bölümlük akış.
6. A4 dikey. Punto: başlık 16–24, alt başlık 11–14, gövde 9–11, tablo 8–9. Tablo başlık satırı koyu, toplam satırı belirgin, tutarlar sağa hizalı. Siyah-beyaz çıktıda da okunur.
7. Müşteriye final PDF gider; düzenlenebilir DOCX kurum içinde kalır. Sürümler v01, v02, final olarak adlandırılır.
8. Performans, tasarruf, süre ve sonuç iddiaları doğrulanabilir olur. Fiyat dışı vaatler kapsam dışı iş doğurmayacak şekilde yazılır. Müşteriden beklenen veri, erişim ve onay sorumlulukları açıkça listelenir.
9. Kişisel veri, finans, bordro, SGK, vergi, İSG, yazılım ya da entegrasyon içeren tekliflerde uzman / hukuk kontrolü işaretlenir.
10. Dosya adları:
    - `[MARKA]_[MUSTERI]_[HIZMET]_FiyatTeklifi_v01.docx`
    - PDF: `…_[YYYYMMDD]_v01.pdf`
    - Revizyon: `…_v02.pdf`
    - Teknik ek: `…_TeknikEk_…`

---

## 3. HİZMET TANITIM FÖYÜ OLUŞTURMA KILAVUZU

### 3.1 Özet
**Amaç (§1):** Föy, "bir hizmetin değer teklifini, kapsamını, çözüm yaklaşımını, metodolojisini, faydalarını ve iletişim yönlendirmesini satış veya pazarlama kullanımına uygun şekilde özetleyen kurumsal doküman"dır. "Kısa versiyon karar hızlandırır; uzun versiyon güven, kapsam ve metodoloji derinliği sağlar."

Kılavuzun kullanım notu: "Marka renkleri ve görsel kimlik değerleri ilgili alanlarda tanımlanır". Yani marka değerleri forma (01 / 79) bırakılmış.

**Bölümler (sırasıyla):**
1. Amaç
2. Föy Türleri
3. Karar Matrisi
4. Ortak Stratejik Hazırlık Alanları
5. Ortak Teknik Tasarım
6. Kısa Versiyon (sayfa akışı, metin limitleri, tasarım kuralları)
7. Uzun Versiyon (12 bölüm, metin limitleri, tasarım)
8. İçerik Yazım
9. Görsel / İkon / Medya
10. CTA ve İletişim
11. Dijital / Baskı / PDF Çıktıları
12. Dosya İsimlendirme
13. Kalite Kontrol ve Onay
14. Brief Şablonları (kısa ve uzun)
15. Final Checklist

**Karar matrisi (§3):**

| Durum | Önerilen föy |
|---|---|
| Hızlı farkındalık | Kısa |
| Karar vericiye detaylı kapsam | Uzun |
| Mailing eki | Kısa ya da 3–4 sayfalık özet |
| Satış ekibinin yüz yüze görüşmesi | Kısa + uzun birlikte |
| Karmaşık, regülasyonlu ya da teknik hizmet | Uzun |
| Etkinlikte dağıtım | Kısa |
| Web'de form karşılığı indirme | Uzun |

**Sayısal standartlar:**

| Konu | Kısa föy | Uzun föy |
|---|---|---|
| Uzunluk | 1–2 sayfa | 6–12 sayfa (teknikte 16'ya kadar) |
| Kapak başlığı | En fazla 6–8 kelime | En fazla 6–8 kelime |
| Alt başlık / slogan; kapak alt metni | Slogan en fazla 12–16 kelime | Kapak alt metni 20–35 kelime |
| Hizmet tanımı | 40–60 kelime | 80–150 kelime |
| Problem maddeleri | 3–4 madde, her biri en fazla 12 kelime | — |
| Fayda maddeleri | 3–5 madde, her biri en fazla 14 kelime | — |
| Bölüm açıklamaları | — | Her biri 60–120 kelime |
| Metodoloji | — | 4–6 adım, her adım 20–40 kelime |
| Paketler | — | Her paket 3–5 madde |
| SSS | — | 4–7 soru, cevaplar 35–70 kelime |
| CTA | 2–5 kelime | 2–5 kelime |
| Metin yoğunluğu | Sayfa başına 250–450 kelime | — |

Teknik standartlar:

| Konu | Standart |
|---|---|
| Sayfa | A4 dikey; dijital uyarlama 1920×1080 ya da 1080×1350 |
| Kenar boşluğu | Baskıda en az 10–12 mm, dijital PDF'te en az 32–48 px |
| Grid | 2–3 kolon |
| Görsel | Baskı 300 DPI; dijital en az 1440 px genişlik |
| PDF boyutu | Kısa dijital 2–5 MB, web PDF 2–8 MB |
| Baskı | 300 DPI, CMYK, taşma payı |
| Dijital | RGB, sıkıştırılmış PDF |

**Süreç:** stratejik hazırlık (§4: hizmet adı, hedef kitle, tanım, değer teklifi, kapsam, zorluk / çözüm, CTA, iletişim) → versiyon seçimi (§3) → sayfa akışı (§6 ya da §7) → yazım (§8) → görsel (§9) → CTA (§10) → çıktı (§11) → isimlendirme ve revizyon kaydı (§12) → kalite kontrol ve final onay (§13: içerik, marka, satış, hukuki / teknik, tasarım, PDF, final onay — hazırlayan, kontrol eden, onaylayan ve yayın tarihi kaydedilir).

**Uyum maddeleri:**
- Yasaklı dil: "Kesin başarı vaadi, abartılı iddia, doğrulanmamış rakam, korku dili ve agresif satış dili".
- Hukuki / teknik kontrol: "Mevzuat, regülasyon, fiyat, belge veya iddia içeren alanlarda risk var mı?"
- Referans, metrik ve sertifika doğrulanır.
- Görsellerde alt metin bulunur.
- Paket / fiyat alanı "yanlış beklenti oluşturmayacak şekilde" yazılır.

### 3.2 A sınıfı bilgiler

| Alıntı | Mevcut karşılık | Durum ve eksik |
|---|---|---|
| "Kısa Versiyon Föy 1-2 sayfa … Uzun Versiyon Föy 6-12 sayfa" ve §3 matris | yok | Yok. Kurumun hangi sürümleri tuttuğu bilinmiyor. |
| "Kullanım Alanı — Satış görüşmesi, teklif öncesi bilgilendirme, web indirme, mailing eki, etkinlik paylaşımı, saha sunumu" | `mk_lead_magnet` (52, boolean), `mk_mail_formats` pdf (57) | Kısmi. Föyün kullanım yerleri ayrı değil. |
| "Sayfa Boyutu — A4 dikey önerilir. Dijital kullanım için 1920x1080 veya 1080x1350 uyarlama üretilebilir." | yok | Yok. |
| "Baskı Çözünürlüğü — 300 DPI, CMYK renk profili ve baskı taşma payı" | yok | Yok. Föyün basılıp basılmayacağı belirsiz. |
| "Kaynak Dosya — DOCX / PPTX / InDesign / Figma / Canva kaynak dosyası saklanmalıdır." | `brand_deliverables` Figma (01) | Kısmi. |
| "Paketler ve Fiyatlandırma — Standart, Profesyonel, Enterprise gibi paket isimleri; kapsam farkları; teklif al çağrısı" | `mk_prod_types` package, `mk_prod_price` (51) | Kısmi. Kademe adları yok; fiyat gösterimi var ama yalnız tanıtım sayfası için yazılmış. |
| "Telefon — CTA alanında mutlaka telefon numarası yer almalıdır." / "E-posta — Satış veya ilgili departman e-posta adresi kullanılmalıdır." | `mk_contact` (77) | Kısmi. Satış / departman iletişimi ayrı değil (bkz. `oc_sales_contact`). |
| "Çağrı ve İletişim — Satış sorumlusu, telefon, e-posta, web sitesi, hizmet sayfası" | `mk_contact`, `oc_services` (hizmet sayfası adresi) | Kısmi. Satış sorumlusu yok. |
| "CTA Linki — Hizmet sayfası, iletişim formu, kampanya sayfası veya teklif formu linki" | `oc_services` (hizmet sayfası) | Kısmi. Form adresi yok (bkz. `oc_lead_url`). |
| "CTA Metni — Teklif Alın / Keşif Görüşmesi Planlayın / Bilgi Alın / Hizmeti İnceleyin / Randevu Oluşturun" | yok | Yok. Bkz. `oc_cta`. |
| "Neden Biz? — Uzmanlık, deneyim, sektör bilgisi, vaka çalışmaları, sertifikalar, akreditasyonlar." / "Referans ve Müşteri Yorumları — Logo galerisi, kısa alıntılar, başarı metrikleri" | `mk_banned` client_logo (onaysız logo yasağı) | Yok. Kullanılabilir kanıt listesi yok (bkz. `oc_proof`). |
| "Kapak ve Giriş — Logo, kurumsal renkler, hizmet adı, vizyon/misyon sloganı" | `mk_slogan`, `oc_logo`, `brand_color_*` | Kısmi. Vizyon / misyon yok (bkz. `oc_mission`). |
| "Dil ve Ton — Kurumsal, güven veren, sade, çözüm odaklı" | `brand_tone`, `brand_address` (01) | Tam. |
| "Yasaklı Dil — Kesin başarı vaadi, abartılı iddia, doğrulanmamış rakam, korku dili ve agresif satış dili" | `mk_banned` (55) | Kısmi. Korku dili, agresif satış ve doğrulanmamış rakam yok. |
| "İkon Dili — Tek stil: outline veya flat." | `brand_icons` | Tam. |
| "Logo … sıkıştırılmamalı veya renklendirilmemelidir." | `brand_logo_rules` NoDistort | Tam. |
| "Fotoğraf — Gerçekçi, kurumsal, doğal ışıklı ve düşük stok hissine sahip" | `brand_imagery` | Tam. |
| "Alt Metin — Dijital erişilebilirlik için görsellere kısa açıklayıcı alt metin" | `mk_visual_meta` alt (55) | Tam. |
| §4 Hizmet Adı, Hedef Kitle, Hizmet Tanımı, Değer Teklifi | `oc_services`, `mk_prod_fields` (summary, value, audience, benefits, faq, proof), `mk_target` (49) | Kısmi. Kayıt alanlarında "problem / zorluk", "süreç / metodoloji", "kapsam ve sektörler", "neden biz" yok (bkz. §6). |
| §13 "Satış Kontrolü" / "Marka Kontrolü" / "Hukuki / Teknik Kontrol" | `mk_flow`, `mk_approvers`, `mk_legal_scope` | Kısmi. Onaylayanlarda satış yöneticisi ve kurumsal iletişim yok. |
| "Revizyon Kaydı — Revizyon tarihi, revizyonu isteyen kişi, değişiklik açıklaması ve onay durumu" | `mk_flow_log` (63) | Tam (akış düzeyinde). |

### 3.3 Yeni alan önerileri — yeni bölüm `mk_flyer` "Hizmet Tanıtım Föyü" (grup: **Satış Dokümanları**)

Bölüm `refs`: `oc_services`, `mk_slogan`, `oc_tagline`, `oc_logo`, `brand_color_*`, `brand_font_*`, `oc_font_office`, `mk_contact`, `oc_sales_contact`, `oc_lead_url`, `oc_cta`, `oc_proof`, `oc_mission`.

İçerik kaynağı `mk_prod` kayıtlarıdır. Rehberde "föy metni Ürün & Hizmet Tanıtımı kayıtlarından türetilir" notu yer alır.

**1) `mk_flyer_on` — boolean — "Hizmet Tanıtım Föyü"**
- **Evet:**
  - Ne zaman doğru: Hizmetler satış görüşmesinde, mailing ekinde ya da etkinlikte PDF / basılı belgeyle anlatılıyorsa.
  - Nasıl görünür: Claude her hizmet için föyü kısa ve / veya uzun akışla, metin limitleriyle ve son sayfada CTA + telefon + QR ile üretir.
- **Hayır:**
  - Nasıl görünür: Föy kuralı yazılmaz.
- Kanıt: §1 ve kapak özeti "Kullanım Alanı".
- Öneri bağlantısı: `mk_prod_on` = true iken önerilir.

**2) `mk_flyer_channels` — multiselect — "Föyün Kullanım Yerleri"** (showIf `mk_flyer_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Satış görüşmesi = `sales_meeting` | Satış ekibi yüz yüze anlatıyorsa | Kısa + uzun birlikte |
| Mailing eki = `mail` | Föy e-postaya ek olarak gidiyorsa | Kısa ya da 3–4 sayfalık özet, 2–5 MB |
| WhatsApp paylaşımı = `whatsapp` | Görüşme sonrası mesajla gönderiliyorsa | Kısa, hafif PDF |
| Etkinlik dağıtımı = `event` | Fuar ya da seminerde dağıtılıyorsa | Kısa; basılı ise baskı PDF'i |
| Web'den indirme (form karşılığı) = `gated` | Föy sitede lead toplamak için sunuluyorsa | Uzun; `mk_lead_magnet` ile bağlantılı |
| Teklif öncesi bilgilendirme / sunum eki = `pre_quote` | Teklif ya da kurumsal sunumla gönderiliyorsa | Uzun |

- Kanıt: kapak özeti "Kullanım Alanı — Satış görüşmesi, teklif öncesi bilgilendirme, web indirme, mailing eki, etkinlik paylaşımı, saha sunumu" ve §2 "WhatsApp paylaşımı".

**3) `mk_flyer_versions` — select — "Föy Sürümleri"** (showIf `mk_flyer_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Kısa + uzun birlikte = `both` | Satış ekibi yüz yüze kullanıyorsa ya da hem hızlı hem detaylı kullanım varsa | Her hizmet için iki PDF |
| Yalnız kısa (1–2 sayfa) = `short` | Hızlı farkındalık, mailing, etkinlik | 7 bölümlük tek föy |
| Yalnız uzun (6–12 sayfa) = `long` | Karmaşık, regülasyonlu ya da teknik hizmet; form karşılığı indirme | 12 bölümlük föy |

- `recommend` (§3 matristen): `mk_flyer_channels` sales_meeting → both; mail / whatsapp / event → short, both; gated / pre_quote → long, both. `sector_regulations` dolu (None dışı) → long, both.
- Kanıt: §3 karar matrisi.

**4) `mk_flyer_sizes` — multiselect — "Sayfa Ölçüleri"** (showIf `mk_flyer_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| A4 dikey **(önerilen)** = `a4` | Baskı ve PDF | 2–3 kolon grid; kenarlar baskıda 10–12 mm |
| Dijital yatay 1920×1080 = `d169` | Ekranda ya da sunum ekinde | Yatay sayfa |
| Dijital dikey 1080×1350 = `d45` | Sosyal medya ya da mobil paylaşım | Dikey uyarlama |

- Kanıt: "Sayfa Boyutu — A4 dikey önerilir. Dijital kullanım için 1920x1080 veya 1080x1350 uyarlama üretilebilir."

**5) `mk_flyer_print` — boolean — "Basılı Föy"** (showIf `mk_flyer_on`)
- **Evet:**
  - Ne zaman doğru: Föy matbaada basılıp dağıtılıyorsa.
  - Nasıl görünür: Web PDF'ine ek olarak ayrı yüksek çözünürlüklü baskı PDF'i (300 DPI, CMYK, taşma payı, 10–12 mm kenar) ve QR kodlu CTA.
- **Hayır:**
  - Nasıl görünür: Yalnız RGB, sıkıştırılmış, bağlantıları tıklanabilir dijital PDF (2–8 MB).
- Kanıt: "PDF Export — Web için optimize edilmiş PDF; baskı için yüksek çözünürlüklü PDF ayrı alınmalıdır." ve "Baskı Çözünürlüğü — 300 DPI, CMYK renk profili ve baskı taşma payı gereksinimi kontrol edilmelidir."

**6) `mk_flyer_source` — multiselect — "Kaynak Dosya Biçimi"** (showIf `mk_flyer_on`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Word (DOCX) = `docx` | Föy ofis yazılımıyla güncelleniyorsa | Stilleri tanımlı .docx |
| PowerPoint (PPTX) = `pptx` | Sunum şablonuyla aynı ekip hazırlıyorsa | Sayfa ölçüsünde .pptx |
| InDesign = `indesign` | Matbaa için profesyonel dizgi yapılıyorsa | Claude metni ve yerleşim notunu verir; dosyayı tasarımcı üretir |
| Figma = `figma` | Tasarım ekibi Figma'da çalışıyorsa | Kare (frame) yapısına uygun içerik |
| Canva = `canva` | Ekip Canva marka kitini kullanıyorsa | Canva şablonuna aktarılacak metin blokları |

- Kanıt: "Kaynak Dosya — DOCX / PPTX / InDesign / Figma / Canva kaynak dosyası saklanmalıdır."

QR kod ayrı alan yapılmadı. Kılavuz "QR kod önerilir" diyor; kural metninde varsayılan olarak bulunur (C). Kurum QR istemiyorsa sonradan boolean eklenebilir.

### 3.4 B sınıfı (föy başına, form alanı değil)
- Föy tipi (kısa / uzun), hizmet adı.
- Hedef kitle (karar verici, sektör, işletme tipi).
- Ana mesaj / tek cümlelik değer teklifi.
- Hizmet tanımı.
- Problem / ihtiyaç maddeleri, çözüm ve fayda maddeleri.
- Görsel konsept (kapak görseli, ikon, infografik yönü).
- Kapsam (sektörler, süreçler).
- Hizmet süreci adımları.
- Paketler.
- Neden biz.
- SSS (4–7).
- Bu föyün CTA metni ve linki.
- Revizyon kaydı (tarih, isteyen, açıklama, onay).

### 3.5 C sınıfı ilkeler
1. Kısa föy akışı: Kapak, Hizmet Tanımı, Kimler İçin, Problem, Çözümümüz, Ana Faydalar, CTA ve İletişim. Uzun föy akışı 12 bölümdür: Kapak … SSS, Çağrı ve İletişim, Ek Bölümler.
2. Metin limitleri §3.1 tablosundaki gibidir. Sayfa başına 250–450 kelime aşılmaz (kısa).
3. İlk bakışta hizmet adı, fayda ve CTA anlaşılır. Kısa föyde uzun paragraf yoktur.
4. Fayda dili: özellik değil, kullanıcının elde edeceği çıktı yazılır. Her iddia rakam, vaka, referans ya da sertifikayla desteklenir.
5. Kısaltma ilk kullanımda açık yazılır, kısaltma parantez içinde verilir. Teknik terim sadeleştirilir.
6. Süreç timeline ya da ikonlu akışla, paket karşılaştırması tabloyla verilir. Her sayfada tek ana mesaj olur.
7. CTA alanında telefon zorunludur. Son sayfada CTA, telefon, e-posta, web ve QR bulunur. PDF içindeki web, mail, telefon ve QR bağlantıları tıklanabilir ve test edilmiştir.
8. Görsel: baskıda 300 DPI, dijitalde en az 1440 px. Alt metin verilir. Logo kapakta görünür, iç sayfalarda küçük ve sabit konumdadır.
9. Dosya adları:
   - Kaynak: `[MARKA]_[HIZMET_ADI]_Foy_[Kisa|Uzun]_v01.docx`
   - PDF: `…_YAYIN_TARIHI_v01.pdf`
   - Görsel: `…_Foy_Gorsel_01.webp`
   - QR: `…_QR_v01.png`
10. Final onayda hazırlayan, kontrol eden, onaylayan ve yayın tarihi kaydedilir. Paket / fiyat alanı yanlış beklenti yaratmayacak şekilde yazılır (`mk_prod_price` ile uyumlu).

---

## 4. Üç kılavuzda ortak olan ve tek yerde tutulması gerekenler
- CTA + link + telefon + e-posta her üç belgede zorunlu → Ortak Bilgiler (`oc_cta`, `oc_lead_url`, `oc_sales_contact`, mevcut `mk_contact`).
- Kanıt / referans / sertifika her üçünde var:
  - sunum §8 "Kanıt",
  - teklif §8.12 "Referans / Kanıt",
  - föy §7.1 "Neden Biz?" ve "Referans".

  → `oc_proof`.
- Kurumsal font ve ofis yedeği → `brand_font_*` + `oc_font_office`.
- Dosya adı `[MARKA]` öneki → mevcut `mk_prefix` (66). Rehberde "satış dokümanlarında da kullanılır" notu eklenir.
- Kısa / uzun versiyon ikiliği üçünde de var. Ancak sunum ve teklifte versiyon belge başına seçilir (B). Föyde kurum düzeyinde bir "hangi sürümler tutulacak" kararı olarak öneriliyor.

## 5. Ortak Bilgiler'e önerilen yeni alanlar

**5.1 `oc_sales_contact` — textarea — "Satış İletişim Bilgileri"** (bölüm 77 `oc_identity`, `mk_contact`'tan sonra)
- ph: "Örn. Satış sorumlusu: … · Telefon: … · E-posta: satis@… (boşsa genel iletişim bilgileri kullanılır)".
- Ne zaman doğru: Satış belgelerinde genel iletişimden farklı bir departman numarası, e-postası ya da sorumlu kişi gösterilecekse.
- Nasıl görünür: Föyün son sayfasında, sunumun CTA slaytında ve teklifin CTA alanında bu bilgiler yer alır.
- Kanıt:
  - föy §10 "E-posta — Satış veya ilgili departman e-posta adresi kullanılmalıdır.",
  - föy §7.1 "Çağrı ve İletişim — Satış sorumlusu, telefon, e-posta",
  - föy §4 "İletişim — Telefon, e-posta, web sitesi, hizmet sayfası ve varsa satış sorumlusu bilgileri."
- Not: Basın bülteni kılavuzunu inceleyen ajan "basın iletişim kişisi" önerebilir. İkisi tek bir "Departman İletişimleri" (Satış | Basın | Destek) alanında birleştirilebilir.

**5.2 `oc_lead_url` — url — "Teklif / İletişim Formu Adresi"** (bölüm 77)
- ph: "Örn. https://www.ornekfirma.com/teklif-al/".
- Ne zaman doğru: Belgelerdeki çağrının yönlendirileceği varsayılan bir form sayfası varsa.
- Nasıl görünür: CTA linki ve QR kodu bu adrese gider. Hizmete özel sayfa `oc_services`'ten alınır.
- Kanıt:
  - föy §10 "CTA Linki — Hizmet sayfası, iletişim formu, kampanya sayfası veya teklif formu linki",
  - sunum §4 "CTA ile birlikte kullanılacak telefon, e-posta veya form linki",
  - teklif §7.1 "Link: [CTA_LINK]".

**5.3 `oc_cta` — multiselect — "Ana Çağrılar (CTA)"** (bölüm 78 `oc_market`)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Teklif alın = `quote` | Fiyat teklif üzerineyse (`mk_prod_price` = quote) | Föy, sunum ve reklamlarda "Teklif Alın" düğmesi |
| Keşif / ön görüşme planlayın = `discovery` | Danışmanlık ve B2B hizmet | "Ücretsiz keşif görüşmesi planlayın" |
| Bilgi alın = `info` | Karar süreci uzunsa | "Bilgi Alın" |
| Demo talep edin = `demo` | Yazılım / SaaS | "Demo talep edin" |
| Randevu oluşturun = `appointment` | Randevuyla çalışan işletme (`module_booking`) | "Randevu Oluşturun" |
| Kaydolun / formu doldurun = `signup` | Etkinlik, eğitim, üyelik | "Kaydolun" |

- Kanıt:
  - föy §10 "CTA Metni — Teklif Alın / Keşif Görüşmesi Planlayın / Bilgi Alın / Hizmeti İnceleyin / Randevu Oluşturun",
  - sunum §4 "CTA — Teklif al, iletişime geç, demo talep et, kaydol, form doldur, danışmanlık talep et",
  - föy §6.2 "CTA Metni — 2-5 kelime".
- İsteğe bağlı `recommend`: `mk_prod_price` quote → quote; `module_booking` dolu → appointment; `project_type` SaaS → demo.

**5.4 `oc_proof` — textarea — "Referanslar, Sertifikalar ve Başarı Metrikleri"** (bölüm 78 `oc_market`, `oc_services`'ten sonra)
- ph: "Ad | tür (referans / vaka / sertifika / ödül / metrik) | kaynak ya da kullanım izni — örn. ISO 27001 | sertifika | belge no … ; Örnek AŞ | referans | yazılı izin var".
- Ne zaman doğru: Kurumun belgelerde gösterebileceği, doğrulanmış ve kullanım izni alınmış kanıtları varsa.
- Nasıl görünür: Claude "Neden Biz?", "Kanıt" ve "Referans" bölümlerinde yalnız bu listedeki kanıtları kullanır. Listede yoksa kanıt uydurmaz, bölümü yer tutucuyla bırakır. İzinsiz müşteri adı ya da logosu kullanılmaz (`mk_banned` client_logo ile uyumlu).
- Kanıt:
  - föy §7.1 "Neden Biz? — … vaka çalışmaları, sertifikalar, akreditasyonlar" ve "Referans ve Müşteri Yorumları — Logo galerisi, kısa alıntılar, başarı metrikleri",
  - föy §15 "Referans, başarı metriği, sertifika veya kanıt alanları doğrulandı.",
  - teklif §8 "12. Referans / Kanıt",
  - sunum §8 "Kanıt — Referans, vaka, başarı metriği, müşteri yorumu, sertifika".

**5.5 `oc_font_office` — select — "Ofis Belgelerinde Yedek Font"** (bölüm 79 `oc_brand`, fontlardan sonra)

| Etiket = değer | Ne zaman doğru | Nasıl görünür |
|---|---|---|
| Arial = `arial` | Kurumsal font alıcının bilgisayarında yoksa | DOCX / PPTX dosyalarında Arial; PDF'te kurumsal font |
| Calibri = `calibri` | Ekip Microsoft Office varsayılanıyla çalışıyorsa | Düzenlenebilir dosyalarda Calibri |

- Kanıt:
  - teklif §11 "Font — Kurumsal font ailesi. Alternatif olarak Arial / Calibri kullanılabilir.",
  - sunum §5 "font dosyaları kullanıcıyla paylaşılmamalı, yalnızca font adı belirtilmelidir",
  - sunum §13 "Google Slides — Bulut paylaşımında font ve görsel kaymaları kontrol edilmelidir."

**5.6 (isteğe bağlı) `oc_mission` — textarea — "Vizyon ve Misyon"** (bölüm 77)
- Ne zaman doğru: Kurumsal tanıtım sunumunda ve uzun föy kapağında kullanılacak onaylı bir vizyon / misyon cümlesi varsa.
- Nasıl görünür: Kapak ya da "Biz Kimiz" slaytında birebir yer alır.
- Kanıt:
  - föy §7.1 "Kapak ve Giriş — Logo, kurumsal renkler, hizmet adı, vizyon/misyon sloganı",
  - sunum §2 "Kurumsal Tanıtım Sunumu — Marka, şirket, vizyon, hizmetler ve güven unsurlarını tanıtmak."
- Not: Marka Kimliği kılavuzunu inceleyen ajanın önerisiyle çakışabilir; tek alan olarak birleştirin.

## 6. Mevcut alanlarda değişiklik önerileri

1. **`mk_approvers` (63)** — seçenek ekle: "Satış yöneticisi = `sales_manager`" ve "Kurumsal iletişim (marka kontrolü) = `brand`".
   - Kanıt: föy §13 "Satış Kontrolü — Değer teklifi, paketler, fiyatlandırma ve teklif yönlendirmesi satış stratejisine uygun mu?" ve "Marka Kontrolü — Logo, renk, font, görsel dil ve kurumsal ton uyumlu mu?"; teklif §13 "Marka Kontrolü — Kurumsal İletişim".
   - Finans ve operasyon buraya değil, `mk_quote_approval`'a.
2. **`mk_legal_scope` (64)** — seçenek ekle: "Fiyat teklifleri = `quotes`".
   - Kanıt: teklif §10 "Kişisel veri, finans, bordro, SGK, vergi, iş sağlığı, yazılım veya entegrasyon içeren tekliflerde ilgili uzman/hukuk kontrolü alınmalıdır."
   - Ayrıca "Satış dokümanları (sunum, föy) = `sales_docs`" eklenebilir. Kanıt: föy §13 "Hukuki / Teknik Kontrol — Mevzuat, regülasyon, fiyat, belge veya iddia içeren alanlarda risk var mı?"
3. **`mk_banned` (55)** — seçenek ekle: "Korku dili = `fear`", "Agresif satış baskısı = `pressure`", "Doğrulanmamış rakam ve sonuç iddiası = `unverified_claim`".
   - Kanıt: föy §8 "Yasaklı Dil — Kesin başarı vaadi, abartılı iddia, doğrulanmamış rakam, korku dili ve agresif satış dili kullanılmamalıdır."; teklif §10 "Teklifte yer alan performans, tasarruf, süre veya sonuç iddiaları doğrulanabilir olmalıdır."
   - Mevcut `superlative` "kesin başarı vaadi / abartılı iddia"yı karşılıyor.
4. **`mk_prod` (51) — yeni alan `mk_prod_tiers` [text] "Paket Kademe Adları"** (showIf `mk_prod_types` in [package]).
   - ph: "Örn. Standart | Profesyonel | Kurumsal".
   - Ne zaman doğru: Hizmetler kademeli paketlerle satılıyorsa.
   - Nasıl görünür: Föyün "Paketler" bölümünde, teklifin paket karşılaştırma tablosunda ve tanıtım sayfasında aynı adlar kullanılır.
   - Kanıt: föy §7.1 "Paketler ve Fiyatlandırma — Standart, Profesyonel, Enterprise gibi paket isimleri; kapsam farkları"; teklif §2 "Standart/Profesyonel/Enterprise gibi seçenekli teklifler."
5. **`mk_prod_fields` (51)** — seçenek ekle: "Karşılaşılan problemler = `problems`", "Hizmet süreci / metodoloji = `process`", "Kapsam ve sektörler = `scope`", "Neden biz = `why_us`".
   - Föy metni aynı kayıtlardan türetilir.
   - Kanıt: föy §6.1 "Karşılaşılan Problem — … 3-4 temel zorluk"; §7.1 "Hizmet Süreci / Metodoloji", "Kapsam ve Sektörler", "Neden Biz?".
   - Hizmet Tanıtım Sayfası ajanının önerisiyle birleştirin.
6. **`mk_prod_price` (51)** — seçenek değişmez. Kural metninin kapsamı tanıtım sayfasından föy, sunum ("Teklif / Paket — Paketler, çıktı, opsiyonlar, fiyatlandırma notu") ve teklif CTA'sına genişletilir.
   - "Teklif üzerine" seçiliyse föy ve sunumda fiyat yazılmaz, "Teklif Alın" çağrısı kullanılır.
   - `recommend` ile `mk_quote_on` ve `oc_cta` quote önerilir.
   - Kanıt: föy §15 "Paket / fiyatlandırma alanı varsa yanlış beklenti oluşturmayacak şekilde yazıldı."; föy §7.1 "… teklif al çağrısı."
7. **`brand_deliverables` (01)** — seçenek ekle: "Sunum ana şablonu (PPTX master) = `SlideMaster`" ve "Ofis belge şablonu (teklif, föy DOCX) = `DocTemplate`".
   - Kanıt: sunum §13 "PPTX — Düzenlenebilir ana kaynak dosya. Master slide, tema renkleri ve font ayarları korunmalıdır."; föy §11 "Kaynak Dosya — DOCX / PPTX / InDesign / Figma / Canva kaynak dosyası saklanmalıdır."
8. **`mk_lead_magnet` (52)** — seçenek değişmez. Rehbere şu not eklenir: "Uzun föy form karşılığı indirilebilir içerik olarak kullanılabilir."
   - Kanıt: föy §3 "Web sitesinde form karşılığı indirilebilir içerik olacaksa — Uzun Versiyon".
9. **`mk_prefix` (66)** — etiket ve açıklamaya "fiyat teklifi numarası ve satış dokümanı dosya adlarında da kullanılır" eklenir. Alan şu an Plan Dosyası bölümünde; satış dokümanları da kullanacaksa Ortak Bilgiler › Kimlik'e taşınması düşünülebilir (kimlik aynı kalır).
   - Kanıt: teklif §14 "[MARKA]-FT-[YYYYMMDD]-[MUSTERI]-v01"; föy §12 ve sunum §15 dosya adı kalıpları.
10. **`oc_tax_ids` (77)** — değişiklik yok. Üç kılavuzda vergi / MERSİS bilgisinin teklifte ya da föyde gösterilmesi istenmiyor; teklif kapağı "Logo, teklif başlığı, müşteri adı, teklif no, tarih, geçerlilik" ile sınırlı. Teklif kuralında "kurum bilgileri isteğe bağlı alt bilgi" olarak anılabilir, ama kanıt yok; öneri değil.
11. **`mk_contact` (77)** — değişiklik yok. Telefon ve e-posta CTA'yı karşılıyor; satış / departman ayrımı için 5.1 öneriliyor.

## 7. Bölüm başına sorumlu ajan (öneri)
- `mk_deck`, `mk_flyer`: 09 Pazarlama ve Büyüme (içerik / tasarım pozisyonları). Teklif ekiyle ilgili satış alanları 08 Satış olabilir.
- `mk_quote`: 08 Satış (teklif hazırlayan pozisyon). `mk_quote_currency`, `mk_quote_fx`, `mk_quote_vat` için ek olarak 02 Finans.
- Tam pozisyon kimlikleri `dpPos` ile seçilmeli; bu dosyada uydurulmadı.
