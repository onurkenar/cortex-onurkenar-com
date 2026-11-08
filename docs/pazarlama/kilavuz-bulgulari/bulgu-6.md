# Bulgu 6 — Tek Tip Brief + Marka Kimliği şablonu + Şirket / İletişim şablonu

Okunan dosyalar (üçü de baştan sona):
- `tek_tip_tasarim_brief_cikti_formati_V001.txt` (1.237 satır, 17 ana başlık + İş Akış Raporu)
- `Rasyotek - Marka Kimliği Kılavuzu.txt` (13 bölüm) — **şablon olarak**: yalnız alan başlıkları çıkarıldı, değerler kullanılmadı
- `Rasyotek Şirket ve İletişim Bilgileri.txt` (5 bölüm) — **şablon olarak**

Karşılaştırılan form: `alan-envanteri.md` (tamamı) + `web-proje-gelistirme.html` içindeki DATA (`rule`, `ruleDetail`, `explanation`) ve ilgili JS (`mkPlanData`, `AU_CTX`, `mkPrompt`, `shown`, `accRows`, `ocDv`). Yerel SEO / yapısal veri iddiaları Google belgelerinden doğrulandı (2026-11-07):
- LocalBusiness: zorunlu `name`, `address`; önerilen `geo`, `telephone`, `openingHoursSpecification`, `url`; adres için "Include as many properties as possible" (örnekte `streetAddress`, `addressLocality`, `addressRegion`, `postalCode`, `addressCountry`); koordinat için "The precision must be at least 5 decimal places"; telefon için "Be sure to include the country code and area code"; ayrı fiziksel konumlar için "Define each local business location as a" LocalBusiness alt türü. (developers.google.com/search/docs/appearance/structured-data/local-business)
- Organization: `contactPoint` (telephone, email; örnekte `contactType: "Customer Service"`), `addressCountry` "two-letter ISO 3166-1 alpha-2", `taxID` "matches the country that you provided in the address field", `logo` "112x112px, at minimum", birden çok `sameAs`. (…/structured-data/organization)

---

## 0. Sorulan konulara doğrudan yanıt (kanıtlı)

| Konu | Şablondaki başlık | Bugünkü karşılık | Sonuç |
|---|---|---|---|
| Telefon | "Telefon Numarası" | `mk_contact` (tek serbest metin) | **Ayrı alan olmalı** |
| WhatsApp | "WhatsApp / Mobil İletişim" | yok (`mk_accounts.whatsapp` = **WhatsApp Kanal adresi**, numara değil) | **Ayrı alan olmalı** — `mk_conversions: whatsapp`, `mk_gads_assets: message`, `mk_meta_objectives: messages` bu numaraya dayanıyor ama formda numara yok |
| Destek hattı | "Çağrı Merkezi / Destek Hattı" | yok (`mk_contact` içine yazılırsa kayboluyor, aşağıda) | **Ayrı alan olmalı** (Organization `contactPoint`) |
| E-posta | "E-posta Adresi" | `mk_contact` | **Ayrı alan olmalı** |
| Açık adres + bileşenler | "Ülke, İl, İlçe, Mahalle, Bulvar / Cadde / Sokak, Bina Adı, Bina No, Kat, İç Kapı No, Posta Kodu, Açık Adres" | `mk_contact` (tek satır "Adres: …") | **Bileşenli alan olmalı** (PostalAddress) |
| Adres tipi | "Genel Merkez / Şube / Bölge Müdürlüğü" | yok (`location_pages` yalnız boolean) | **Yeni alan** + şube listesi |
| Koordinat | "Latitude / Longitude" | yok | **Ayrı alan** (Google: ≥ 5 ondalık) |
| Harita bağlantısı | "Harita Linki" | yok | **Ayrı alan** (url) |
| Koyu / açık renk | "Koyu Renk … Metin, footer, koyu zemin", "Açık Renk … Arka plan, kart, blok alan" | yok — `brand_neutral` yalnız karakter seçer (Cool/Warm/Pure/Tinted), HEX yok; `mkPlanData` zemini bu seçimden sabit kodla üretiyor (`{Cool:"#F4F6F8",…}`) | **2 color alanı** |
| Başarı / uyarı / nötr | "Başarı / Onay Rengi", "Uyarı Rengi", "Nötr Gri" | `brand_status_colors=Guide` "kurumsal kılavuzdaki kodlarla birebir kullanılır" diyor **ama kodun girileceği alan yok** | **HEX alanları** (Guide seçilince) + nötr gri color |
| Tipografi ölçüleri | "Ana Başlık / H1 … Font Ağırlığı … Punto / PX … Satır Aralığı" (6 satır) | `brand_type_scale` (oran), `brand_body_text` (16/17/18 px web), `brand_type_rules: Weights` (sayı sınırı) — seviye başına ağırlık / boyut / satır aralığı yok | **Kısmi** — web tarafı yeterli; görsel tasarım tablosu için 1 textarea |
| Başlık uzunlukları | "H1 4-8 kelime, H2 4-10, H3 3-8, Spot 1-2 cümle, Gövde 40-70 kelime, CTA 2-5 kelime" | yok (yalnız `mk_formats: T` "en çok 12 kelime") | **Yeni select** (standart / özel) |
| CTA standardı | "Ana CTA Metni", "Buton Konumu", "CTA Formatı: CTA: [CTA_METNİ]: [CTA_LINK] \| Telefon: [TELEFON_NUMARASI]"; tek tip: "CTA kullanılan tüm alanlarda linke ek olarak telefon numarası da belirtilir" | renk = `brand_color_accent` (tam), köşe = `brand_radius` (tam); **metin, bağlantı, biçim, konum yok** | **Yeni alanlar** |
| Sosyal medya ölçüleri | "Instagram Post 1080x1350 px · Kenarlardan min. 80 px …" (7 satır) + tek tip §2 (15 satır) | `mk_formats` (format başına: R/S 1080×1920, C/T 1080×1350), `mk_meta_creative` (oran), `mk_blog_cover` — **platform başına ölçü ve güvenli kenar yok** | **Yeni select + özel tablo** |
| Dosya isimlendirme | "marka_adi_platform_konu_format_tarih" (6 içerik türü) + tek tip "[MARKA]_[BRIEF_NO]_[FORMAT]_[PLATFORM]_[YAYIN_TARIHI]_v01" | `mk_brief_format=full` ruleDetail "Marka_BriefNo_FORMAT_YAYINTARİHİ_v01" (PLATFORM eksik); `mk_visual_meta: filename` "küçük harf, Türkçe karaktersiz ve **tireli**" (kılavuz **alt çizgi**) | **Kısmi + çelişki** → yeni alan |
| Dosya formatları | "Logo SVG, PNG, PDF · Görsel JPG, PNG, WEBP · Video MP4 · Sunum PPTX, PDF · Doküman DOCX, PDF · Tasarım Kaynağı AI, PSD, Figma, Canva linki" | `image_format` (yalnız web yayını), `brand_deliverables: LogoPack` (SVG/PNG), `mk_brief_delivery` (yalnız brief'in kendisi) | **Kısmi** → 2 yeni alan |
| Logo varyant dosya adları | "Ana Logo / Yatay / Dikey / İkon / Beyaz / Siyah" + dosya adı sütunu | `brand_logo_variants` hangi varyantın olacağını seçer; `oc_logo` **tek** adres tutar | **Kısmi** → 1 textarea |

### `mk_contact` tek metin alanının somut hatası (kanıt)

`mkPlanData` (plan dosyasının `marka` nesnesi) `mk_contact`'ı şöyle ayrıştırıyor:

```js
mkLines(mkV("mk_contact")).forEach(x=>{let v=x.replace(/^[^:]{1,14}:\s*/,"");
  if(/@/.test(v)&&!mail)mail=v;
  else if((v.match(/\d/g)||[]).length>=7&&!tel)tel=v;
  else adr.push(v)});
```

Şablondaki başlıklarla doldurulmuş örnek (değerler uydurma) aynı mantıkla çalıştırıldı:

- Girdi: Telefon / WhatsApp / "Çağrı Merkezi / Destek Hattı" / E-posta / Adres / Konum / Harita satırları
  → `telefon` = ilk telefon, **`adres` = "+90 5xx …, Çağrı Merkezi / Destek Hattı: 444 …, <açık adres>, 41.01417, 28.81438, https://maps.app.goo.gl/…"** — WhatsApp, destek hattı, koordinat ve harita adrese karışıyor; "Çağrı Merkezi / Destek Hattı" etiketi 14 karakteri aştığı için silinmiyor.
- Girdi: önce "Adres: … No: 11, Kat: 8, İç Kapı No: 38, 34197 …", sonra Telefon
  → adresin içinde 10 rakam olduğu için **`telefon` = açık adres**, **`adres` = telefon numarası**.

Ayrıca `AU_CTX` (SEO denetim promptu) ve pazarlama promptunun MARKA bölümü `mk_contact`'ı ham metin olarak veriyor; yapısal veri (Organization / LocalBusiness `telephone`, `address`, `geo`, `contactPoint`) ve NAP tutarlılığı (`au_intl_checks: nap`, `location_pages` kuralı "NAP tutarlılığı") için alan bazlı veri yok. Google LocalBusiness telefon için ülke ve alan kodu, koordinat için en az 5 ondalık istiyor — serbest metinde bunlar denetlenemiyor.

**Sonuç:** İletişim bilgileri ayrı alanlara bölünmeli; `mk_contact` "Ek İletişim Notları" olarak kalmalı ve eski kayıt `ocMig()` ile bir kez ayrıştırılmalı (§3.1).

---

## 1. Kılavuz: Tek Tip Tasarım Brief Çıktı Formatı (V001)

### 1.1 Özet

**Amaç:** "Tüm şirket ve markalar için ortak siyah-beyaz brief şablonu". Bir içerik konusundan 360° üretim (blog, sosyal, video, podcast, PDF, sunum, canlı yayın, SMS, basın bülteni, mailing, reklam) için tek belge.

**Bölümler (sırasıyla):** Kapak Özeti → 1 Kapak ve Genel Brief Bilgileri → 2 Platformlar, Boyutlar ve Yayın Uyarlamaları → 3 İçerik Stratejisi → 4 Stratejik İçerik Omurgası → 5 Ton, Dil ve Marka Kişiliği → 6 Görsel Tasarım Yönü → 7 Marka Kimliği ve Teknik Tasarım Kılavuzu → 8 İçerik Formatları (8A tüm formatlar, 8B blog içeriği, 8C blog öne çıkan görsel ve meta, 8D tek görsel, 8D.i carousel, 8E story, 8F Reels / Shorts storyboard, 8G anket, 8H etkinlik (içerik + duyuru), 8I podcast, 8J PDF, 8K sunum, 8L canlı yayın, 8M SMS, 8N basın bülteni, 8O mailing) → 9 Kullanılmaması Gerekenler → 10 Platform Bazlı Caption Seti (Meta, LinkedIn, X, GMB, WhatsApp Business, YouTube, Threads, TikTok) → 11 Stock, Prompt ve Üretim Kaynakları → 12 Başarı Kriteri → 13 Teslim Notu ve Dosya Çıktıları → 14 Onay ve Revizyon Süreci → 15 Final Checklist → 16 Reklamcılık (Google Ads; Meta, LinkedIn, TikTok) → 17 Kopyalanabilir Kısa Brief Özeti → İş Akış Raporu.

**Sayısal standartlar:**
- Ana fikir "maksimum 1 cümle"; görsel slogan "Maksimum 6-8 kelime"; alt açıklama "15-20 kelimelik"; alternatif başlık 3 adet.
- Platform ölçüleri (§2): LinkedIn feed 1080x1350 / 1200x1500; LinkedIn etkinlik kapağı 1200x627; LinkedIn video 1080x1920 / 1920x1080; Instagram feed / carousel 1080x1350; Story / Reels 1080x1920; Facebook 1080x1350 / 1200x1500, video 1080x1920; X 1200x675; GMB 1200x900 / 1080x1080; WhatsApp Kanal 1080x1350 / 1080x1920; YouTube Shorts 1080x1920, post 1080x1080, video 1920x1080; Threads 1080x1350; TikTok 1080x1920; blog öne çıkan 1920x1080 (16:9); mailing banner 600–800 px genişlik.
- Story "5-7 kare"; carousel "5-8 slayt", "başlık maksimum 6-8 kelime, destek metni 1-2 kısa cümle"; video 9:16 "30-45 sn / 45-55 sn / 60 sn", "ilk 3 saniye güçlü hook", altyazılı; podcast "1 dakikalık"; PDF "5-7 sayfalık"; sunum 8 slayt akışı; canlı yayın "20-25 dakika / 45 dakika / 60 dakika"; SMS "160 karakter"; preheader "70-100 karakterlik"; blog meta title "55 karakteri aşmayacak", meta description "150-155 karakter", özet "40-60 kelimelik"; "SEO Alt Metin … 30+ kelimelik"; video çıktısı "MP4, H.264, 1080x1920, altyazılı, kapak görseli ile"; başarı ölçütü "ilk 2 saniyede ana mesajı anlamalı".

**Süreç (§14):** 1 Brief onayı (Pazarlama / İş Sahibi) → 2 Tasarım ilk taslak (Tasarımcı) → 3 Metin kontrolü (İçerik Ekibi) → 4 Marka kontrolü (Kurumsal İletişim) → 5 Hukuk / Teknik kontrol (İlgili uzman / danışman) → 6 Final export (Tasarımcı) → 7 Yayın (Sosyal Medya / Web Ekibi: "Tarih, saat, link, telefon ve UTM kontrol edildi mi?"). Revizyon "v01, v02, final".

**Uyum maddeleri:** SMS "KVKK, izinli iletişim ve gönderim saatleri kontrol edilmelidir"; mailing alt bilgi "Adres, izin/abonelik bilgisi"; "Doğrulanmamış rakam, abartılı iddia veya hukuki/finansal kesin sonuç vaadi kullanılmamalı"; "Korku pazarlaması yapılmamalı".

### 1.2 A sınıfı bilgiler

| Alıntı | Mevcut karşılık | Eksik |
|---|---|---|
| "Brief No [BRIEF_NO]" | `mk_brief_no` — tam | — |
| "Marka / Şirket" | `mk_brand_name` — tam | — |
| "Alt Marka / Ürün / Hizmet [Kategori > Hizmet / Ürün]" | `mk_brand_structure`, `oc_services` — tam (havuz) | — |
| "Belge Başlık Sıralaması" (17 başlık) | `mk_brief_format=full` — kısmi | explanation 9 parça sayıyor; 17 başlık, kısa özet (§17) ve İş Akış Raporu yazılı değil |
| "Kullanım Notu: … doküman tasarımı siyah-beyaz tutulur. Marka renkleri yalnızca bilgi alanlarında yazılır." | yok | kural metni (C, §5) |
| "CTA kullanılan tüm alanlarda linke ek olarak telefon numarası da belirtilir" | yok | **yeni `mk_cta_format`** |
| "Öncelik ve Deadline [Normal / Acil / Kampanya kritik]" | yok | öncelik seti — içerik planı şablonunun alanı; form alanı önerilmedi (bkz. §4 not) |
| "Durum [Taslak / İçerik onayı bekliyor / Tasarımda / Revizyonda / Yayına hazır]" | `mk_flow` + `mk_flow_published` — kısmi | ara durumlar ("Tasarımda", "Revizyonda") yok; içerik planı durum setine bağlı, form alanı önerilmedi |
| §2 platform ölçü tablosu | `mk_formats` / `mk_meta_creative` / `mk_blog_cover` — kısmi | platform başına ölçü, LinkedIn etkinlik kapağı, YouTube video/post, GMB, mailing banner yok → **yeni `mk_sizes`** |
| "Funnel Aşaması [Farkındalık > Değerlendirme > Karar > Sadakat]" | `mk_funnel=fdk` — kısmi | **Sadakat** aşaması yok |
| "Emoji Kullanımı [Yok / sınırlı / platforma göre]" | yok | **yeni `mk_emoji`** |
| "Satış Sertliği [Yumuşak farkındalık + net CTA / kampanya odaklı / doğrudan satış]" | yok | **yeni `mk_sales_tone`** (marka varsayılanı; brief içerik başına değiştirebilir) |
| "Kaçınılacak Dil: Abartılı iddia, doğrulanmamış rakam, korku pazarlaması, aşırı teknik jargon ve kesin sonuç vaadi" | `mk_banned` — kısmi (superlative, price_claim) | korku pazarlaması, teknik jargon, doğrulanmamış rakam seçenekleri yok |
| "Yerleşim Paterni: F-pattern veya Z-pattern" | yok (F/Z kılavuzu ayrı bulgu dosyasında) | çapraz başvuru |
| "İkon Stili [Outline / flat / minimal / tek renk / vurgu rengi]" | `brand_icons` — tam | — |
| "Fotoğraf / İllüstrasyon Stili" | `brand_imagery` — tam | — |
| "Logo Kullanımı [Logo kullanılacak / kullanılmayacak / sosyalde küçük / blog görselinde yok]" + §9 "Logo kullanım talimatı yoksa tasarımcı logoyu otomatik eklememeli" | yok | içerik başına (B) + kural (C) |
| "Renk Kullanımı [Marka özelindeki HEX kodları ve kullanım rolleri]" | `brand_color_*` — kısmi | koyu / açık / nötr / durum HEX yok (§3.2) |
| "Tipografi [Font ailesi, başlık-gövde ayrımı, mobil okunabilirlik notu]" | `brand_font_heading/body` — tam | — |
| 8A "Kullanılmayacak formatlar 'Kapsam dışı' … 360° üretimlerde tüm alt başlıklar doldurulur" | `mk_formats` — kısmi | anket, canlı yayın yok; diğer kanallar (SMS, podcast, basın, sunum) başka bulgularda |
| 8D.i "Slayt Sayısı [5-8 slayt önerilir]" | `mk_formats: C` ruleDetail "6–9 slayt" — **çelişki** | §4 |
| 8E "Kare Sayısı [5-7 kare]" | `mk_formats: S` ruleDetail "3 kare" — **çelişki** | §4 |
| 8D "Destek Metni [15-20 kelimelik kısa açıklama]" + §6 slogan 6-8 kelime | `mk_formats: T` "görsel üzerindeki metin en çok 12 kelimedir" — **çelişki** | §4 |
| "Storyboard Kartları - Zorunlu Alanlar" (10 alan) + §15 "Storyboard kullanılan tüm bölümlerde Storyboard Numarası, Süre, Konuşma Metni, Görsel, Kamera, Lens, Işık, Renk, Müzik ve Amaç alanları dolduruldu" | yok | **yeni `mk_storyboard`** (alan seti kararı — "Blog Alan Seti" emsali) |
| 8C "Alternatif Metin [Kısa alt text] … Başlık Meta … Alt Yazı … Açıklama Metni … SEO Alt Metin [… 30+ kelimelik …]" | `mk_visual_meta` — kısmi | "Açıklama metni" seçeneği yok; "30+ kelime alt metin" mevcut alt kuralıyla çelişir (§4) |
| 8D "İletişim Alanı [Web] \| Telefon: [TELEFON] \| [Lokasyon varsa]" | yok | **yeni `mk_contact_block`** |
| 8D.i "Dosya Teslimi: Her slayt ayrı PNG/JPG, ayrıca düzenlenebilir kaynak dosya ve gerekiyorsa PDF carousel çıktısı" | `mk_zip` — kısmi | format ve kaynak dosya yok → **`mk_export_formats`, `mk_source_file`** |
| 8H.ii "Hatırlatma Metni [Etkinlikten 1 gün önce ve yayın günü …]" | `mk_evt_plan=standard` — kısmi | hatırlatma zamanı yazılı değil (§4) |
| 8L "Format [LinkedIn Live / YouTube Live / webinar / Instagram Live]" | `mk_evt_types` — kısmi | canlı yayın türü yok (§4) |
| 8M "160 karakter ideal; gerekiyorsa kısa link …", "KVKK, izinli iletişim ve gönderim saatleri" | yok | SMS bulgu dosyasına çapraz başvuru |
| 8N "Medya İletişim [Ad Soyad / E-posta / Telefon]", "Şirket Hakkında [Kısa kurumsal tanıtım]" | `oc_tagline` — kısmi | basın iletişim kişisi — basın bülteni bulgusuna çapraz başvuru |
| 8O "Preheader … 70-100 karakterlik", "Mailing Banner 600-800 px genişlik", "Alt Bilgi [Adres, izin/abonelik bilgisi, sosyal medya linkleri]" | `mk_mail_consent: identity, unsub` — kısmi | mailing bulgusuna çapraz başvuru; banner ölçüsü `mk_sizes` tablosunda |
| §10 etiket kalıpları (ör. X Post "#[Etiket1] #[Etiket2] #[Marka]") | `mk_hashtags` kuralı "X'te en çok 2 etiket" — küçük çelişki | §4 |
| §11 "Zorunlu Kullanılacak Assetler [Logo, font, fotoğraf, ürün görseli, kurumsal kimlik dosyaları]" | `brand_guide_notes`, `oc_logo` — kısmi | varlık klasörü bağlantısı yok → **`oc_assets_url`** |
| §13 "Ana Tasarım Dosyası: Canva / Figma / PSD / AI kaynak dosya linki" | `mk_visual_source: designer` ruleDetail "kaynak dosyalar … teslim alınır" — kısmi | araç seçimi yok → **`mk_source_file`** |
| §13 "Export Formatları: PNG / JPG / MP4 / PDF - platforma göre", "Video Çıktısı: MP4, H.264, 1080x1920, altyazılı, kapak görseli ile" | yok | **`mk_export_formats`** |
| §13 "Dosya İsimlendirme: [MARKA]_[BRIEF_NO]_[FORMAT]_[PLATFORM]_[YAYIN_TARIHI]_v01" | `mk_brief_format=full` ruleDetail — kısmi | `[PLATFORM]` eksik; ayırıcı alt çizgi kararı yok → **`mk_file_naming`** |
| §13 "Revizyon Takibi: v01, v02, final" | `mk_brief_delivery` kuralı "v01, v02" — kısmi | "final" adı yok |
| §14 7 aşamalı onay, "4. Marka Kontrolü — Kurumsal İletişim", "5. Hukuk / Teknik Kontrol — İlgili uzman / danışman" | `mk_flow`, `mk_approvers` — kısmi | marka kontrolü ve teknik uzman rolü, 7 aşamalı akış seçeneği yok (§4) |
| §16A "Uzantılar: Telefon: [TELEFON] \| Site bağlantıları" | `mk_gads_assets: call, sitelinks` — tam | — |
| §16B LinkedIn "[Sektör / ünvan / şirket büyüklüğü / yetkinlik]", "[Single image / document ad / video / event ad]"; TikTok "[Spark Ads / In-feed video]" | `mk_ads_channels: linkedin, tiktok` — kısmi | ayrı bölüm yok; reklam bulgusuna çapraz başvuru |
| İş Akış Raporu "Format: Word dokümanı" | `mk_brief_delivery: word` — tam | — |

### 1.3 B sınıfı (brief alanları — form alanı değil)

Kapak / §1: brief no değeri, hazırlanma tarihi, yayın tarihi / saati, takvim haftası / kampanya dönemi, hizmet / ürün, konu, anahtar kelime, platformlar, amaç, CTA metni, CTA bağlantısı, telefon (marka varsayılanından), tek cümlelik ana fikir, iş sahibi / talep eden, tasarım sahibi, öncelik, deadline, durum.
§3–4: içerik açısı (farkındalık / eğitici / sosyal kanıt / kampanya / rehber / erken uyarı / segment), hedef kitle ve persona içgörüsü, huni aşaması, ana mesaj, destekleyici kanıt, kampanya ana fikri, kullanıcı problemi, marka çözümü, algı hedefi, karar tetikleyici.
§5–6: bu işin tonu (marka tonundan), görsel slogan, alt açıklama, 3 alternatif başlık, görsel hissi, görsel konsept, kompozisyon, görsel arama kelimeleri (TR / EN), logo kullanımı.
§8: blog meta (sayfa linki, meta title, meta description, odak kelime, slug, özet, iç link, dış kaynak), blog gövdesi (H1–H6, SSS), öne çıkan görsel metinleri (başlık, kısa açıklama, alt metin, başlık meta, alt yazı, açıklama, AI / stok promptu), tek görsel (ana başlık, destek metni, 3 fayda, vurgu alanı, dipnot), carousel slayt metinleri, story kareleri, storyboard kartlarının içeriği (SB no, süre, konuşma, görsel, kamera, lens, ışık, renk, müzik, amaç), video başlığı / süresi / kapak sloganı / açıklaması, anket soruları ve seçenekleri, etkinlik başlığı / türü / tarih / konuşmacılar / akış / hatırlatma metni, podcast başlığı / kurgusu / metni, PDF başlığı / amacı / sayfa akışı, sunum slaytları, canlı yayın başlığı / süresi / platformu / akışı, SMS metni, basın bülteni (başlık, spot, 5N1K giriş, gövde, alıntı), mailing (konu, preheader, hero, gövde, CTA, alt bilgi).
§10: platform başına caption metinleri ve etiketler.
§11: stok görsel / video / ikon arama kelimeleri, AI görsel / video promptu, referans görseller.
§16: Google Ads kampanya amacı, türü, lokasyon, anahtar kelimeler, başlıklar, açıklamalar, açılış sayfası; sosyal reklam hedef kitlesi, kreatif formatı, reklam metni.
§17 / İş Akış Raporu: kısa özet satırları, durum.

---

## 2. Şablon: Marka Kimliği Kılavuzu (alan başlıkları)

### 2.1 Özet

**Amaç:** "brief, sosyal medya içeriği, blog görseli, reklam kreatifi, mailing, SMS, video, podcast kapağı, basın bülteni, sunum, hizmet tanıtımı, fiyat teklifi ve tüm tasarım çalışmalarında ana marka referansı".
**Bölümler:** 1 Genel Marka Bilgileri · 2 Logo Kullanım Bilgileri · 3 Kurumsal Renk Paleti (3.1 Ana Renkler: HEX / RGB / CMYK / kullanım alanı; 3.2 Yardımcı Renkler) · 4 Tipografi (kullanım alanı / font / ağırlık / punto-px / satır aralığı / not) · 5 Başlık ve Metin Hiyerarşisi · 6 Görsel Dil ve Tasarım Stili · 7 Buton ve CTA · 8 Sosyal Medya Tasarım Standartları · 9 Sunum / PDF / Doküman · 10 Kullanılmaması Gerekenler · 11 Dosya Formatları ve Teslim · 12 Dosya İsimlendirme · 13 Kullanım Notu.
**Sayısal başlıklar (değerleri değil, türü önemli):** logo minimum boyut (px genişlik), logo güvenli alanı (logo yüksekliğine oran), 4 ana + 3 yardımcı renk, 6 tipografi satırı (H1, H2, H3, gövde, dipnot, CTA), uzunluk aralıkları (kelime / cümle), köşe yuvarlaklığı (px), çizgi kalınlığı (px), sosyal format başına ölçü + kenar güvenli alanı (px).
**Not:** "Font dosyası kaynaklara eklenmemeli; yalnızca font adı, lisans durumu ve kullanım alanı belirtilmelidir."

### 2.2 A sınıfı — alan alan karşılaştırma

| Şablon başlığı (alıntı) | Mevcut karşılık | Durum / eksik |
|---|---|---|
| "Marka / Şirket Adı" | `mk_brand_name` (77) | tam |
| "Ticari Unvan" | `oc_legal_name` (77) | tam |
| "Marka Kısa Tanımı [Markayı 1-2 cümle ile açıklayan tanım]" | `oc_tagline` (77) — explanation "1–2 cümle" | tam |
| "Slogan / Motto" | `mk_slogan` (77) | tam |
| "Ana Mesaj [Markanın hedef kitleye verdiği ana mesaj]" | yok (`oc_tagline` tanımdır, `mk_prod_fields: value` ürün başınadır) | **yeni `oc_key_message`** |
| "Hedef Kitle [B2B / B2C / Kurumsal / KOBİ / İnsan Kaynakları / Finans vb.]" | `business_model` (78) + `mk_b2b_size`, `mk_b2b_sectors`, `mk_b2b_roles`, `mk_audience` (49) | tam |
| "Marka Kişiliği [Kurumsal, güvenilir, yenilikçi, uzman, sade vb.]" | yok (`brand_tone` tek seçimli ses tonudur) | **yeni `brand_personality`** |
| "İletişim Tonu [Resmi / yarı resmi / bilgilendirici / satış odaklı / uzman dili]" | `brand_tone` (Formal, Friendly, Energetic, Expert, Luxury) — kısmi | "satış odaklı" ekseni ayrı karar → `mk_sales_tone`; "bilgilendirici" ≈ Expert/Friendly (seçenek eklenmesi önerilmez) |
| "Ana Logo", "Yatay Logo", "Dikey Logo", "İkon / Amblem", "Beyaz Logo", "Siyah Logo" (dosya adı sütunuyla) | `brand_logo_variants` (Primary, Stacked, Symbol, Favicon, Mono, Dark) + `oc_logo` (tek adres) — kısmi | varyant başına dosya adı / adres yok; Beyaz ve Siyah ayrı satır, formda `Mono` tek seçenek → **yeni `oc_logo_files`** |
| "Minimum Kullanım Boyutu", "Logo Güvenli Alanı" | `brand_logo_rules: MinSize, ClearSpace` — kısmi (kural var, **ölçü değeri yok**; yalnız `brand_guide_notes` serbest metni) | **yeni `brand_logo_specs`** |
| "Logo Kullanılmaması Gerekenler: Gerdirme, gölge, renk değiştirme, efekt ekleme, düşük çözünürlük." | `brand_logo_rules: NoDistort, NoEffects, SVG` | tam (düşük çözünürlük → C) |
| "Ana Renk … HEX / RGB / CMYK / Kullanım Alanı (Logo, başlık, vurgu, CTA)" | `brand_color_primary` (HEX) | HEX tam; RGB HEX'ten türer (C); **CMYK yok** |
| "İkincil Renk" | `brand_color_secondary` | tam |
| "Koyu Renk … Metin, footer, koyu zemin" | yok (`brand_neutral` yalnız karakter) | **yeni `brand_color_dark`** |
| "Açık Renk … Arka plan, kart, blok alan" | yok (`mkPlanData` zemini `brand_neutral`'dan sabit kodla üretiyor) | **yeni `brand_color_light`** |
| "Başarı / Onay Rengi", "Uyarı Rengi" | `brand_status_colors=Guide` — kısmi (kod girilemiyor) | **yeni `brand_color_success`, `brand_color_warning`** (+ hata / bilgi, alan etiketi zaten 4 rengi sayıyor) |
| "Nötr Gri … Çizgi, arka plan, pasif alan" | `brand_neutral` — kısmi (HEX yok) | **yeni `brand_color_neutral`** |
| Tipografi: "Font Ailesi" (6 satır) | `brand_font_heading`, `brand_font_body` (79) | tam |
| Tipografi: "Font Ağırlığı" (seviye başına) | `brand_type_rules: Weights` (en fazla 4) — kısmi | seviye–ağırlık eşlemesi yok |
| Tipografi: "Punto / PX", "Satır Aralığı" (H1, H2, H3, gövde, dipnot, CTA) | `brand_type_scale` (1.200–1.500), `brand_body_text` (16/17/18 px, 1.5–1.7) — kısmi | web ölçeği oranla karşılanıyor; **görsel tasarım (sosyal / baskı) ölçüleri ve "Dipnot", "CTA / Buton Yazısı" satırları yok** → **yeni `brand_type_table`** |
| "Not: Font dosyası kaynaklara eklenmemeli; yalnızca font adı, lisans durumu ve kullanım alanı" | `brand_font_source: Licensed` — kısmi | C kuralı |
| "H1 … 4-8 kelime", "H2 … 4-10 kelime", "H3 … 3-8 kelime", "Spot Metin … 1-2 cümle", "Gövde Metni … 40-70 kelime", "CTA Metni … 2-5 kelime" | yok | **yeni `mk_text_lengths` (+ özel)** |
| "Genel Görsel Stil: Minimal / kurumsal / modern / teknolojik / sade / dinamik" | `page_design_style` (yalnız site) — kısmi | pazarlama görsellerine bağlayan alan yok; `brand_personality` + `brand_imagery` ile karşılanır, ayrı alan önerilmedi |
| "Fotoğraf Kullanımı: Gerçek insan, ofis, sektör görseli, soyut görsel" | `brand_imagery` (RealPhotos, Product, Stock, Illustration, 3D, AI) — kısmi | "soyut görsel" yok (küçük; önerilmedi) |
| "İllüstrasyon Kullanımı: Flat, 3D, line art, ikon bazlı" | `brand_imagery: Illustration, 3D` — kısmi | alt stil yok → `brand_guide_notes` |
| "İkon Stili: Outline" | `brand_icons` | tam |
| "Arka Plan Kullanımı: Açık Zemin veya koyu zemin" | `color_theme` (site) — kısmi | görseller için `brand_color_dark/light` yeterli |
| "Doku / Pattern" | yok | `brand_guide_notes` (seyrek; alan önerilmedi) |
| "Köşe Yuvarlaklığı" | `brand_radius` (aralıklar) | tam |
| "Gölge Kullanımı" | `brand_shadow` | tam |
| "Çizgi Kalınlığı" | yok (`brand_icons` kuralı "çizgi kalınlığı sabittir", değer yok) | `brand_type_table`'a benzer biçimde `brand_logo_specs` yerine `brand_guide_notes`; alan önerilmedi |
| "Negatif Alan" | — | C |
| "Ana CTA Metni" | yok | **yeni `mk_cta_texts`** |
| "Buton Rengi" | `brand_color_accent` (boşsa ana renk) | tam |
| "Buton Yazı Rengi" | yok | C (kontrasttan türetilir); özel değer `brand_guide_notes` |
| "Buton Fontu" | `brand_font_heading/body` | tam (ağırlık `brand_type_table`) |
| "Buton Köşe Yapısı" | `brand_radius` | tam |
| "Buton Konumu: Sağ alt / sol alt / merkez / footer alanı" | yok | **yeni `mk_cta_position`** |
| "CTA Formatı: CTA: [CTA_METNİ]: [CTA_LINK] \| Telefon: [TELEFON_NUMARASI]" | yok | **yeni `mk_cta_format`, `mk_cta_phone`, `mk_cta_url`** |
| §8 sosyal medya: "Format / Ölçü / Güvenli Alan / Not" (Instagram post, Story/Reels, LinkedIn, Facebook, X, YouTube thumbnail, Google My Business) | `mk_formats`, `mk_meta_creative` — kısmi | platform başına ölçü, güvenli kenar ve YouTube kapak ölçüsü yok → **`mk_sizes`** |
| §9 "Sunum Ölçüsü: 16:9", "PDF Ölçüsü: A4 dikey / A4 yatay" | yok | **yeni `mk_doc_page`** (sunum oranı Sunum bulgusunda; birleştirilmeli) |
| §9 "Kapak Yapısı: Logo, başlık, kısa açıklama, tarih", "İç Sayfa Yapısı" | yok | C (sabit iskelet) |
| §9 "Footer Bilgisi: Web sitesi, telefon, sayfa numarası" | yok | **`mk_contact_block`** |
| §10 "Marka Dışı Renk: Onaysız renk kullanılmamalı" | `brand_status=New` ruleDetail "yeni renk … onay gerektirir" — kısmi | C kuralı (bütün durumlar için) |
| §10 "Aşırı Metin Kullanımı", "Okunaksız Kontrast", "Stok Görsel Uyumsuzluğu", "Efekt Yoğunluğu", "Düşük Çözünürlüklü Görsel" | `mk_formats: T` (12 kelime), `wcag`, `brand_imagery: Stock` — kısmi | C kuralları |
| §11 "Logo: SVG, PNG, PDF — Şeffaf zeminli versiyon bulunmalı" | `brand_deliverables: LogoPack` (SVG / PNG) — kısmi | PDF yok → `mk_export_formats` |
| §11 "Görsel: JPG, PNG, WEBP — Web için optimize edilmeli" | `image_format` (web) — tam (web); teslim için `mk_export_formats` | — |
| §11 "Video: MP4", "Sunum: PPTX, PDF", "Doküman: DOCX, PDF" | yok | **`mk_export_formats`** |
| §11 "Tasarım Kaynağı: AI, PSD, Figma, Canva linki — Düzenlenebilir kaynak dosya" | `brand_deliverables: Figma` — kısmi | **`mk_source_file`** |
| §12 "Logo: marka_adi_logo_versiyon_tarih", "Sosyal Medya Görseli: marka_adi_platform_konu_format_tarih", "Video: marka_adi_platform_konu_sure_tarih", "Sunum: marka_adi_konu_sunum_tarih", "PDF / Föy: marka_adi_hizmet_foy_tarih", "Reklam Görseli: marka_adi_platform_reklam_konu_tarih", "Örnek: #marka_adi_linkedin_sgk_tesvik_post_2026-07-01" | `mk_visual_meta: filename` ("tireli") — kısmi + **çelişki** | **`mk_file_naming`** |

---

## 3. Şablon: Şirket ve İletişim Bilgileri (alan başlıkları)

### 3.1 Özet
**Amaç:** "brief, sosyal medya içeriği, blog yazısı, reklam metni, mailing, SMS, basın bülteni, sunum, hizmet tanıtımı, fiyat teklifi ve tüm kurumsal iletişim dokümanlarında marka iletişim bilgisi kaynağı"; "telefon, web sitesi, CTA linki, sosyal medya adresleri ve açık adres bilgileri bu kaynak dosyadaki bilgilerle tutarlı olmalıdır".
**Bölümler:** 1 Genel Bilgiler · 2 İletişim Bilgileri · 3 Sosyal Medya Adresleri · 4 İletişim Adresi · 5 Kullanım Notu.

### 3.2 A sınıfı — alan alan karşılaştırma

| Şablon başlığı | Mevcut karşılık | Durum |
|---|---|---|
| "Marka / Şirket Adı" | `mk_brand_name` | tam |
| "Ticari Unvan" | `oc_legal_name` | tam |
| "Vergi Dairesi", "Vergi Numarası", "MERSİS No" | `oc_tax_ids` (satır başına "Ad: değer") | tam (Organization `taxID` için ülke `oc_address.country` ile eşleşmeli) |
| "Faaliyet Alanı" (uzun cümle) | `sector_detail` (00, **text**, ph "Çocuk diş hekimliği kliniği") — kısmi | alan Proje bölümünde ve tek satır; Ortak Bilgiler'de yok, pazarlama promptunun MARKA listesine girmiyor (§4) |
| "Kısa Tanım" | `oc_tagline` | tam |
| "Telefon Numarası" | `mk_contact` | **kısmi → `oc_phone`** |
| "Web Site Adresi" | `domain_name` | tam |
| "E-posta Adresi" | `mk_contact` | **kısmi → `oc_email`** |
| "WhatsApp / Mobil İletişim" | yok | **`oc_whatsapp`** |
| "Çağrı Merkezi / Destek Hattı" | yok | **`oc_support_phone`** |
| Sosyal: Facebook, Instagram, X.com, YouTube, LinkedIn, Pinterest, WhatsApp Kanal, Google My Business, TikTok, Threads | `mk_accounts` satırları: facebook, instagram, x, youtube, linkedin, pinterest, whatsapp (Kanal), google (İşletme Profili), tiktok, threads | **tam** (10/10) |
| "Adres Tipi: Genel Merkez / Şube / Bölge Müdürlüğü" | yok | **`oc_addr_type`** + **`oc_branches`** |
| "Ülke", "İl", "İlçe", "Mahalle", "Bulvar / Cadde / Sokak", "Bina Adı", "Bina No", "Kat", "İç Kapı No", "Posta Kodu" | `mk_contact` tek satır | **kısmi → `oc_address`** (bileşenli) |
| "Açık Adres" | `mk_contact` | **bileşenlerden türetilir** (`derive` / `ocAddrLine`) |
| "Latitude / Longitude" | yok | **`oc_geo`** |
| "Harita Linki" | yok | **`oc_map`** |

---

## 4. Mevcut alanlarda değişiklik önerileri

1. **`mk_contact` (77)** — etiketi "Ek İletişim Notları" yapılsın (faks, KEP gibi listede olmayanlar); explanation'daki "Telefon / E-posta / Adres" yönlendirmesi yeni alanlara bağlansın. `ocMig()` eski değeri bir kez ayrıştırsın: etiketi Telefon / Tel → `oc_phone`; WhatsApp / GSM / Mobil → `oc_whatsapp`; Destek / Çağrı → `oc_support_phone`; `@` içeren → `oc_email`; Adres → `oc_address.street` (bileşenlere bölünmeden, kullanıcı düzeltsin); `maps.` / `goo.gl` → `oc_map`; iki ondalıklı sayı çifti → `oc_geo`; kalan satırlar `mk_contact`'ta kalır. Hedef doluysa üzerine yazılmaz (mevcut `remove` / `ocMig` ilkesi). `mkPlanData` `telefon` / `eposta` / `adres`'i yeni alanlardan okusun (kanıtlanan karışma §0); `AU_CTX` ve pazarlama promptunun MARKA listesi yeni kimlikleri alsın.
2. **`mk_formats`** — çelişkiler (tek tip brief):
   - `C` ruleDetail "6–9 slayt" ↔ "Slayt Sayısı [5-8 slayt önerilir …]" → "5–8 slayt" yapılsın (ya da kılavuz değeri ayrı seçenekle).
   - `S` ruleDetail "3 kare" ↔ "Kare Sayısı [5-7 kare]", "5-7 kare story: hook, sorun, fayda, çözüm, kanıt ve CTA" → "5–7 kare; akış kanca › sorun › fayda › çözüm › kanıt › CTA".
   - `T` ruleDetail "görsel üzerindeki metin en çok 12 kelimedir" ↔ "Görsel Slogan [Maksimum 6-8 kelime …]" + "Alt Açıklama [15-20 kelimelik …]" + "Kısa Fayda Mesajları 1) 2) 3)" → başlık en çok 8 kelime, destek metni 15–20 kelime olarak yazılsın (ya da `mk_text_lengths` seçimine bağlansın).
   - Eksik seçenekler: "Anket / etkileşimli içerik" (8G: "LinkedIn/X/Instagram Story/WhatsApp anketleri ve devam postu") ve "Canlı yayın" (8L). **Dikkat:** değerler tek harf (R, C, T, S, V, M) ve içerik planı şablonunun format kodlarıyla eşleşiyor; yeni kod eklemeden önce `marketingTemplate.formatlar` ve şablonun `dogrula.mjs`'i kontrol edilmeli.
3. **`mk_funnel`** — "Funnel Aşaması [Farkındalık > Değerlendirme > Karar > Sadakat]": yeni seçenek "F / D / K / S (Farkındalık · Değerlendirme · Karar · Sadakat)" = `fdks`; scenario: tekrar satın alma / sadakat hedefi (`mk_goals: loyalty`) olan markalar; example: plan satırında "S" etiketli müşteri bülteni.
4. **`mk_brief_format=full`** — explanation'ı kılavuzun 17 başlığı + "Kopyalanabilir Kısa Brief Özeti" + "İş Akış Raporu" ile güncellensin; ruleDetail'deki dosya adı "Marka_BriefNo_FORMAT_YAYINTARİHİ_v01" → kılavuzdaki "[MARKA]_[BRIEF_NO]_[FORMAT]_[PLATFORM]_[YAYIN_TARIHI]_v01" (PLATFORM eksik); "doküman siyah-beyaz, marka renkleri yalnız bilgi alanlarında" ve "brief'in sonunda kopyalanabilir kısa özet" eklensin. Not: ruleDetail'deki "yayından en az 2 iş günü önce" kılavuzda yok (çelişki değil, kaynaksız sabit).
5. **`mk_brief_delivery`** kuralı — "sürümler v01, v02 ekiyle" → "v01, v02 … final" ("Revizyon Takibi: v01, v02, final olarak adlandırılmalı").
6. **`mk_visual_meta`** — yeni seçenek "Açıklama metni (uzun açıklama)" = `description` (8C "Açıklama Metni [Görselin ne anlattığını açıklayan kısa metin]"; scenario: CMS medya kütüphanesinde görselin bağlamını saklamak; example: WordPress medya "Açıklama" kutusu). **Çelişki:** 8C "SEO Alt Metin [Anahtar kelime içeren, 30+ kelimelik görsel alt açıklaması]" ↔ mevcut `alt` ruleDetail "kısa … anahtar kelimeyle doldurulmaz". Mevcut kural korunmalı (erişilebilirlik ve anahtar kelime doldurma riski); kılavuzun 30+ kelimelik metni "Açıklama metni"ne yönlendirilsin.
7. **`mk_visual_meta: filename`** ruleDetail "tireli" ↔ kılavuz "marka_adi_platform_konu_format_tarih" (alt çizgi). Kapsam ayrılsın: tire kuralı **sitede yayımlanan görselin** dosya adı (SEO); ekip içi **teslim dosyası** adı yeni `mk_file_naming`'e uyar.
8. **`mk_banned`** — yeni seçenekler (tek tip §5 "Kaçınılacak Dil", §9):
   - `fear` "Korku pazarlaması" — scenario: sigorta, sağlık, finans, mevzuat konularında risk anlatılırken; example: "Ceza yemeden önce…" yerine "Süreci zamanında tamamlamak için…" ("risk/fırsat farkındalığı çözüm diliyle verilmelidir").
   - `jargon` "Aşırı teknik jargon" — scenario: karar vericiye ya da geniş kitleye yazılan içerik; example: kısaltma ilk geçtiği yerde açılır.
   - `unverified_stats` "Doğrulanmamış rakam ve oran" — scenario: istatistik içeren her içerik; example: "%40 tasarruf" yalnız kaynakla yazılır. (`superlative` ve `price_claim` bunu kapsamıyor.)
   - "hukuki/finansal kesin sonuç vaadi" `superlative` ("garanti") ile kısmen örtüşüyor — explanation'a "hukuki / finansal kesin sonuç vaadi" eklenmesi yeterli.
9. **`mk_flow` / `mk_approvers` / `mk_roles`** — §14:
   - `mk_flow` yeni seçenek "Brief onayı → Taslak → Metin kontrolü → Marka kontrolü → Hukuk / teknik kontrol → Final çıktı → Yayın" = `full7`; scenario: ajans + kurum içi çok ekipli üretim; example: tasarım "Marka kontrolü" adımında kurumsal iletişimden dönmeden final çıktıya geçmez.
   - `mk_approvers` yeni: `brand_comms` "Kurumsal iletişim (marka kontrolü)" ("4. Marka Kontrolü — Kurumsal İletişim — Renk, font, logo ve görsel dil uyumlu mu?"), `expert` "Konu uzmanı / danışman (teknik ve mevzuat kontrolü)" ("5. Hukuk / Teknik Kontrol — İlgili uzman / danışman").
   - `mk_roles` yeni: `brand_comms` "Kurumsal iletişim".
10. **`mk_hashtags`** kuralı "X'te en çok 2 etiket" ↔ §10C X Post "#[Etiket1] #[Etiket2] #[Marka]" → "X'te en çok 2 konu etiketi + marka etiketi".
11. **`mk_evt_types`** yeni `live` "Canlı yayın (LinkedIn Live, YouTube Live, Instagram Live)" (8L); **`mk_evt_plan=standard`** ruleDetail'e "hatırlatma etkinlikten 1 gün önce ve yayın günü" (8H.ii).
12. **`brand_logo_variants: Mono`** explanation — şablon "Beyaz Logo" ve "Siyah Logo"yu ayrı satır sayar; "siyah ve beyaz sürümler ayrı dosya olarak hazırlanır" eklensin (yeni seçenek gerekmez; dosyalar `oc_logo_files`'ta).
13. **`brand_status_colors: Guide`** — explanation "kılavuzdaki kodlarla birebir" diyor ama kod alanı yok → yeni HEX alanları buna `showIf` ile bağlansın (§5.2).
14. **`sector_detail`** — şablonun "Faaliyet Alanı" satırı çok cümleli; tip `textarea` yapılsın ya da Ortak Bilgiler › İşletme & Pazar'ın `refs`'ine girsin ve pazarlama promptunun MARKA listesine eklensin (şu an `AU_CTX`'te var, `mkPrompt` listesinde yok).

---

## 5. Yeni alan önerileri

Genel ilke: değerler kurumdan kuruma değişir ve Claude'un ürettiği içerik / site / yapısal veriyi doğrudan değiştirir. Placeholder'lar genel örnek; hiçbirinde şablondaki şirket verisi yok.

### 5.1 Yeni Ortak Bilgiler bölümü: **İletişim & Adres** (`oc_contact`, grup Ortak Bilgiler, 77 ile 78 arasına; 77'deki `mk_contact` buraya taşınır — kimlik aynı kalır)

Gerekçe: şablon 2. ve 4. bölüm; Google LocalBusiness / Organization alanları; `au_intl_checks: nap`, `location_pages` kuralı ("NAP tutarlılığı"), `schema_types: LocalBusiness`, `mk_conversions: phone, whatsapp`, `mk_gads_assets: call, message`. `refs`: `local`, `schema`, `mk_mail`, `mk_gads`, `mk_meta`, `mk_creative`, `au_intl`.

| # | Kimlik | Tip | Etiket | Ayrıntı |
|---|---|---|---|---|
| 1 | `oc_phone` | text (yumuşak `re`: `^\+?[\d\s()-]{7,20}$`) | Ana Telefon | kural: tıklanabilir `tel:`; yapısal veride ülke koduyla (+90 …) yazılır. scenario: müşterinin aradığı ana numara; sitede, GBP'de, reklam arama öğesinde aynı. example: alt bilgide "0212 000 00 00", JSON-LD'de "+902120000000". Kanıt: "Telefon Numarası"; Google: "include the country code and area code". |
| 2 | `oc_whatsapp` | text (aynı `re`) | WhatsApp Hattı | kural: bağlantı `https://wa.me/<ülke kodlu numara>`; WhatsApp Kanal adresinden (`mk_accounts.whatsapp`) ayrıdır. scenario: müşteri mesajla teklif / randevu istiyorsa. example: "WhatsApp'tan yazın" düğmesi, Google Ads mesaj öğesi bu numarayı kullanır. Kanıt: "WhatsApp / Mobil İletişim". |
| 3 | `oc_support_phone` | text | Destek / Çağrı Merkezi Hattı | kural: boşsa ana telefon kullanılır; Organization `contactPoint` (contactType "customer service"). scenario: satış ve destek numarası ayrıysa. example: iletişim sayfasında "Destek hattı" satırı. Kanıt: "Çağrı Merkezi / Destek Hattı". |
| 4 | `oc_email` | text (`re` e-posta) | Kurumsal E-posta | kural: `mailto:`; formlardan gelen bildirimlerin göndereni değildir. Kanıt: "E-posta Adresi". |
| 5 | `oc_addr_type` | select | Adres Türü | Genel merkez=`hq` (önerilen — tek adresli işletme); Şube=`branch`; Bölge müdürlüğü=`regional`. scenario/example: hq → iletişim sayfası "Genel Merkez" başlığı; branch → adres şube sayfasında, Organization yerine o şubenin LocalBusiness kaydında; regional → bölge müdürlüğü adresi yalnız iletişim sayfasında, LocalBusiness olarak işaretlenmez (müşteri kabulü yoksa). Kanıt: "Adres Tipi: Genel Merkez / Şube / Bölge Müdürlüğü". |
| 6 | `oc_address` | **accounts** (emsal: `mk_ids` — URL olmayan etiketli kutular, satırda `re`) — alternatif: 10 ayrı text | Adres | satırlar: `country` Ülke (varsayılan "Türkiye"; yapısal veride ISO "TR"), `city` İl, `district` İlçe, `neighborhood` Mahalle, `street` Bulvar / cadde / sokak, `building` Bina adı, `number` Bina no, `floor` Kat, `door` İç kapı no, `postal` Posta kodu (`re` `^\d{5}$`). Açık adres bu satırlardan Türkçe sırayla türetilir (ör. "Mahalle, Sokak, Bina, No: x, Kat: y, İç Kapı No: z, Posta kodu İlçe / İl"); `streetAddress`, `addressLocality`=ilçe, `addressRegion`=il, `postalCode`, `addressCountry`. scenario: fiziksel adresi olan, GBP'si olan ya da mesafeli satış metninde satıcı adresi gereken her işletme. example: alt bilgi, iletişim sayfası, LocalBusiness ve mesafeli satış sözleşmesi aynı adresi gösterir. Kanıt: şablon 4. bölüm; Google "Include as many properties as possible". |
| 7 | `oc_geo` | text (`re` `^-?\d{1,2}\.\d{5,},\s*-?\d{1,3}\.\d{5,}$`) | Konum Koordinatı (enlem, boylam) | kural: LocalBusiness `geo`; en az 5 ondalık. scenario: haritada işaretin doğru binaya düşmesi. example: "41.01234, 28.81234". Kanıt: "Latitude / Longitude"; Google "precision must be at least 5 decimal places". |
| 8 | `oc_map` | url (`hosts` yumuşak: google.com, maps.app.goo.gl, goo.gl) | Harita Bağlantısı | kural: iletişim sayfasında "Yol tarifi al", e-posta ve PDF alt bilgisinde; LocalBusiness `hasMap`. Kanıt: "Harita Linki". |
| 9 | `oc_branches` | textarea | Diğer Adresler (Şubeler) | showIf `location_pages` = true **veya** `oc_addr_type` ∈ [branch, regional] (iki ayrı koşul gerekirse yalnız `location_pages`). ph: "Ad \| açık adres \| telefon \| harita bağlantısı" satırları. kural: her şube ayrı LocalBusiness ve ayrı lokasyon sayfası; NAP her yerde aynı yazım. Kanıt: "Adres Tipi: Genel Merkez / Şube / Bölge Müdürlüğü"; Google "Define each local business location as a LocalBusiness". |
| 10 | `mk_contact` (mevcut) | textarea | Ek İletişim Notları | §4.1 |

### 5.2 Kurumsal Kimlik (01 `brand`) ve Marka Görünümü (79 `oc_brand`) eklemeleri

| Kimlik | Bölüm | Tip | Etiket | Ayrıntı / kanıt |
|---|---|---|---|---|
| `brand_color_dark` | 79 | color | Koyu Renk (Metin, Alt Bilgi, Koyu Zemin) | kural: gövde metni, alt bilgi ve koyu zemin bu renk (`--color-dark`); saf siyah yerine. scenario: kılavuzda ayrı koyu ton tanımlıysa. example: alt bilgi zemini ve paragraf rengi. Boşsa `brand_neutral`'dan türetilir. Kanıt: "Koyu Renk … Metin, footer, koyu zemin". `mkPlanData` `renk`/`renkler`'e eklenir. |
| `brand_color_light` | 79 | color | Açık Renk (Zemin, Kart, Blok Alan) | kural: sayfa / kart / blok zemini (`--color-light`); `mkPlanData`'daki sabit `neut` haritasının yerine bu değer. Kanıt: "Açık Renk … Arka plan, kart, blok alan". |
| `brand_color_neutral` | 79 | color | Nötr Gri (Çizgi, Pasif Alan) | kural: kenarlık, ayırıcı, pasif düğme. Kanıt: "Nötr Gri … Çizgi, arka plan, pasif alan". |
| `brand_color_success`, `brand_color_warning`, `brand_color_error`, `brand_color_info` | 01 | color | Başarı / Uyarı / Hata / Bilgi Rengi | showIf `brand_status_colors` ∈ [Guide]. kural: mevcut Guide ruleDetail'i ("kontrast vermiyorsa koyulaştırılmış ton") geçerli. Kanıt: "Başarı / Onay Rengi", "Uyarı Rengi" (hata ve bilgi şablonda yok; alan etiketi dört rengi saydığı için isteğe bağlı, boş bırakılabilir). |
| `oc_color_print` | 79 | textarea | Baskı Renk Kodları (CMYK) | isteğe bağlı. ph: "Ana renk \| C M Y K" satırları. kural: basılı föy / PDF / fuar materyalinde HEX yerine bu kodlar; ekran rengi bunlardan türetilmez. Kanıt: renk tablosunda "CMYK" sütunu; §11 "PDF / Föy". Öncelik düşük. |
| `brand_logo_specs` | 01 | text | Logo Ölçü Değerleri | showIf `brand_logo_rules` ∈ [ClearSpace, MinSize]. ph: "Minimum boyut: … px genişlik · Koruma alanı: logo yüksekliğinin …". Kanıt: "Minimum Kullanım Boyutu", "Logo Güvenli Alanı". |
| `oc_logo_files` | 77 (`oc_logo`'nun altında) | textarea | Logo Dosyaları (Varyasyon Başına) | ph: "Ana logo \| marka-ana-logo.svg", "Sembol \| …", "Beyaz \| …", "Siyah \| …" (dosya adı ya da adres). kural: içerikte varyasyon zemine göre seçilir (koyu zemin → beyaz; tek renk baskı → siyah); listede olmayan sürüm kullanılmaz. Kanıt: şablon §2 "Ana Logo / Yatay Logo / Dikey Logo / İkon / Amblem / Beyaz Logo / Siyah Logo" + dosya adı sütunu; tek tip §11 "Zorunlu Kullanılacak Assetler [Logo …]". |
| `oc_assets_url` | 79 | url | Marka Varlıkları Klasörü | kural: brief'lerin "Zorunlu kullanılacak assetler" satırı ve tasarımcı teslimi bu klasöre bağlanır. Kanıt: tek tip §11 "Zorunlu Kullanılacak Assetler [Logo, font, fotoğraf, ürün görseli, kurumsal kimlik dosyaları]"; şablon §11 "Tasarım Kaynağı … Canva linki". |
| `brand_type_table` | 01 | textarea | Tasarım Tipografi Tablosu | ph: "Seviye \| ağırlık \| boyut \| satır aralığı" (H1, H2, H3, Gövde, Dipnot, CTA). kural: sosyal görsel, PDF ve sunumda bu tablo; web ölçeği `brand_type_scale` / `brand_body_text`'ten gelir (ikisi karıştırılmaz). scenario: kılavuzda pt/px tablosu varsa. Kanıt: şablon §4 6 satırlı tablo; tek tip §6 "Tipografi [Font ailesi, başlık-gövde ayrımı, mobil okunabilirlik notu]". |
| `brand_personality` | 01 | multiselect (en çok 3 önerilir) | Marka Kişiliği | Kurumsal=`corporate`, Güvenilir=`trustworthy`, Yenilikçi=`innovative`, Uzman=`expert`, Sade=`simple`, Modern=`modern`, Premium=`premium`, Samimi=`warm`, Veri temelli=`data_driven`, Danışmanlık odaklı=`advisory`, Teknolojik=`tech`, Dinamik=`dynamic`. Varsayılan yok. Her seçenek için scenario "markanın … algılanması istendiğinde", example "görselde … / metinde …" (ör. Veri temelli → başlıkta kaynaklı rakam, görselde gösterge kartı; Danışmanlık odaklı → "nasıl yapılır" yönlendirmesi, uzman alıntısı). Kanıt: şablon "Marka Kişiliği [Kurumsal, güvenilir, yenilikçi, uzman, sade vb.]", "Genel Görsel Stil: Minimal / kurumsal / modern / teknolojik / sade / dinamik"; tek tip §5 "Ton [Kurumsal / modern / premium / samimi / veri temelli / danışmanlık odaklı]". |
| `oc_key_message` | 77 | textarea | Ana Marka Mesajı | kural: bütün içeriklerin "ana fikri" bu mesajla çelişmez; reklam başlıkları ve hakkımızda metni bundan türetilir. scenario: markanın hedef kitleye tek vaadi varsa. example: "Randevunuzu dakikalar içinde alın, tedaviniz boyunca aynı hekimle ilerleyin." türü bir cümle (genel, şirket verisi değil). Kanıt: "Ana Mesaj [Markanın hedef kitleye verdiği ana mesaj]". |

### 5.3 Yeni pazarlama bölümü: **Mesaj & CTA Standardı** (`mk_message`, grup İçerik, 52 `mk_content`'ten sonra)

Gerekçe: CTA, uzunluk ve dil kararları blog, sosyal, mailing, SMS, reklam, PDF hepsinde ortak; 52 (10 alan) ve 55'e (8 alan) eklemek sınırı aşar. `refs`: `brand_tone`, `brand_address`, `brand_personality`, `oc_phone`, `oc_whatsapp`.

| Kimlik | Tip | Etiket | Seçenekler / ayrıntı | Kanıt |
|---|---|---|---|---|
| `mk_cta_texts` | textarea | Standart CTA Metinleri | satır başına bir metin (2–5 kelime). kural: içerikte CTA bu listeden seçilir; listede yoksa aynı uzunluk ve hitapla yazılır. ph: "Teklif alın", "Bilgi alın", "Hemen inceleyin" (genel). | "Ana CTA Metni: Teklif Al / Bilgi Al / Hemen İncele / Başvuru Yap"; "CTA Metni … 2-5 kelime" |
| `mk_cta_url` | url | Varsayılan CTA Bağlantısı | kural: brief'te bağlantı yoksa bu sayfa; UTM `mk_links` / `mk_utm`'ye göre eklenir. | şablon kullanım notu "CTA linki … tutarlı olmalıdır"; tek tip "CTA Link [CTA_LINK]" |
| `mk_cta_format` | select | CTA Biçimi | **CTA metni + bağlantı + telefon (önerilen)**=`link_phone` — scenario: telefonla satış yapan, B2B ya da randevulu işler ("CTA kullanılan tüm alanlarda linke ek olarak telefon numarası da belirtilir"); example: "Teklif alın: …/teklif \| Telefon: 0212 …" · **CTA metni + bağlantı**=`link` — scenario: yalnız çevrim içi satış / form; example: "Hemen inceleyin → …" · **CTA metni + telefon / WhatsApp**=`phone` — scenario: sitesi zayıf, telefon ağırlıklı yerel işletme; example: "Bilgi için arayın: 0 5xx …". | şablon "CTA Formatı: CTA: [CTA_METNİ]: [CTA_LINK] \| Telefon: [TELEFON_NUMARASI]"; tek tip §9 "CTA linke ek olarak telefon numarası içermeli" |
| `mk_cta_phone` | select (showIf `mk_cta_format` ∈ [link_phone, phone]) | CTA'daki Numara | Ana telefon (önerilen)=`main` · WhatsApp hattı=`whatsapp` · Destek hattı=`support`. scenario: hangi hattın satış talebi karşıladığı; example: Instagram CTA'sında WhatsApp, LinkedIn'de ana telefon. | şablon §2 üç ayrı numara; tek tip "Telefon: [TELEFON]" |
| `mk_text_lengths` | select | Metin Uzunluk Standardı | **Kılavuz standardı (önerilen)**=`std`: H1 4–8 kelime, H2 4–10, H3 3–8, spot 1–2 cümle, paragraf 40–70 kelime, CTA 2–5 kelime; görsel başlığı en çok 8 kelime, görsel destek metni 15–20 kelime · **Kurumun kendi ölçüleri**=`custom` · **Sınır yok (mecra kuralları yeter)**=`none`. scenario/example: std → blog H2'leri ve carousel başlıkları kısa ve taranabilir; custom → kurum kılavuzundaki farklı değerler; none → yalnız platform karakter sınırları. | şablon §5 tablo; tek tip §6 "Maksimum 6-8 kelime", "15-20 kelimelik", 8D.i "başlık maksimum 6-8 kelime, destek metni 1-2 kısa cümle" |
| `mk_text_lengths_custom` | textarea (showIf `mk_text_lengths`=custom) | Özel Uzunluk Ölçüleri | ph: "Seviye \| önerilen uzunluk" | aynı |
| `mk_emoji` | select | Emoji Kullanımı | Kullanılmaz=`none` (kurumsal, B2B, resmî tonda) · Sınırlı=`limited` (vurgu için birkaç emoji; başlıkta ve CTA'da yok) · Platforma göre=`platform` (Instagram / TikTok / WhatsApp'ta serbest, LinkedIn ve e-postada yok). Önerilen işaretlenmedi (kılavuz varsayılan vermiyor). | tek tip §5 "Emoji Kullanımı [Yok / sınırlı / platforma göre]" |
| `mk_sales_tone` | select | Satış Sertliği (Varsayılan) | Yumuşak farkındalık + net CTA=`soft` (bilgilendirici içerik, tek CTA sonda) · Kampanya odaklı=`campaign` (süre / teklif vurgusu, kaynaklı fiyat) · Doğrudan satış=`direct` (ilk satırda teklif). kural: brief içerik başına değiştirebilir. | tek tip §5 "Satış Sertliği [Yumuşak farkındalık + net CTA / kampanya odaklı / doğrudan satış]"; şablon "İletişim Tonu […/ satış odaklı / …]" |

### 5.4 Yeni pazarlama bölümü: **Tasarım Üretim & Teslim Standardı** (`mk_production`, grup İçerik, 55 `mk_creative`'den sonra)

| Kimlik | Tip | Etiket | Seçenekler / ayrıntı | Kanıt |
|---|---|---|---|---|
| `mk_sizes` | select | Platform Ölçü Tablosu | **Standart tablo (önerilen)**=`std` — tek tip §2'deki platform ölçüleri (Instagram / Facebook / LinkedIn / Threads / WhatsApp Kanal 1080×1350, Story / Reels / TikTok / Shorts 1080×1920, X 1200×675, GMB 1200×900, YouTube video 1920×1080, LinkedIn etkinlik kapağı 1200×627, blog 1920×1080, mailing banner 600–800 px) · **Kurumun ölçü tablosu**=`custom`. scenario: std → kılavuzu olmayan markalar; custom → kurum kılavuzunda farklı ölçü / güvenli alan varsa. example: custom'da "Facebook 1200×1200 \| kenar 60 px". | tek tip §2; şablon §8 "Format / Ölçü / Güvenli Alan / Not" |
| `mk_sizes_custom` | textarea (showIf `mk_sizes`=custom) | Özel Ölçü Tablosu | ph: "Platform \| ölçü \| kenar güvenli alanı \| not" | şablon §8 ("Kenarlardan min. … px", "Merkez güvenli alan") |
| `mk_cta_position` | select | Görselde CTA Konumu | Sağ alt (önerilen)=`bottom_right` · Sol alt=`bottom_left` · Merkez=`center` · Alt bilgi şeridi=`footer`. scenario: okuma yönü (F/Z) ve platform arayüz alanları; example: carousel son slaytında düğme sağ altta, güvenli alanın içinde. | şablon "Buton Konumu: Sağ alt / sol alt / merkez / footer alanı"; tek tip "CTA butonu alt/sağ güvenli alanda", "görselin alt veya sağ bölümünde" |
| `mk_contact_block` | multiselect | Görsel ve Doküman İletişim Alanı | Web sitesi=`web` · Telefon=`phone` · WhatsApp=`whatsapp` · Lokasyon (il / ilçe)=`location` · Sayfa numarası (PDF / sunum)=`page_no`. kural: değerler Ortak Bilgiler'den aynı yazımla. scenario/example: tek görselin altında "web \| telefon \| ilçe"; PDF alt bilgisinde web + telefon + sayfa no. | tek tip 8D "İletişim Alanı [Web] \| Telefon: [TELEFON] \| [Lokasyon varsa]"; şablon §9 "Footer Bilgisi: Web sitesi, telefon, sayfa numarası" |
| `mk_storyboard` | select | Storyboard Kartı | **Tam kart (10 alan) (önerilen)**=`full` — SB no, süre, konuşma metni, görsel, kamera, lens, ışık, renk, müzik, amaç; scenario: video, story, canlı yayın çekimi ve dış prodüksiyon; example: her sahne SB-01, SB-02 kartıyla. · **Storyboard kullanılmaz**=`none` — scenario: yalnız grafik / slayt üreten ekip. | tek tip "Storyboard Kartları - Zorunlu Alanlar"; §15 checklist maddesi |
| `mk_export_formats` | multiselect | Teslim Dosya Formatları | PNG=`png` · JPG=`jpg` · WebP=`webp` · MP4 (H.264)=`mp4` · PDF=`pdf` · PPTX=`pptx` · DOCX=`docx` · SVG (logo / ikon)=`svg`. kural: carousel slaytları ayrı ve sıra numaralı; video altyazılı ve kapak görseliyle; logo şeffaf zeminli. | şablon §11; tek tip §13 "PNG / JPG / MP4 / PDF", "MP4, H.264, 1080x1920, altyazılı, kapak görseli ile", "Her slayt ayrı PNG/JPG; sıralı dosya ismiyle" |
| `mk_source_file` | multiselect | Düzenlenebilir Kaynak Dosya | Figma=`figma` · Canva=`canva` · Adobe (PSD / AI)=`adobe` · Kaynak dosya istenmez=`none` (exclusive). kural: final çıktıyla birlikte kaynak bağlantısı teslim edilir. | şablon "Tasarım Kaynağı: AI, PSD, Figma, Canva linki — Düzenlenebilir kaynak dosya"; tek tip §13 "Ana Tasarım Dosyası" |
| `mk_file_naming` | select | Teslim Dosyası Adlandırma | **Alt çizgili şablon (önerilen)**=`underscore`: `marka_platform_konu_format_YYYY-AA-GG` (video `…_sure_…`, sunum `marka_konu_sunum_…`, föy `marka_hizmet_foy_…`, reklam `marka_platform_reklam_konu_…`, logo `marka_logo_versiyon_…`), brief'li işte `MARKA_BRIEFNO_FORMAT_PLATFORM_YAYINTARIHI_v01` · **Tireli şablon**=`hyphen` (aynı sıra, tire; sitede yayımlanan dosyayla aynı biçim isteyenler) · **Kurumun kendi şablonu**=`custom`. kural: küçük harf, Türkçe karaktersiz; sürüm v01, v02, final. | şablon §12; tek tip §13 "Dosya İsimlendirme", "Revizyon Takibi" |
| `mk_file_naming_custom` | textarea (showIf `mk_file_naming`=custom) | Özel Adlandırma Şablonu | ph: "İçerik türü \| dosya adı şablonu" | aynı |
| `mk_doc_page` | select | PDF / Doküman Sayfa Ölçüsü | A4 dikey (önerilen)=`a4p` · A4 yatay=`a4l` · İkisi (içeriğe göre)=`both`. **Sunum / Hizmet Föyü bulgularıyla birleştirilmeli** (sunum oranı orada). | şablon §9 "PDF Ölçüsü: A4 dikey / A4 yatay", "Sunum Ölçüsü: 16:9" |

(10 alan; `mk_doc_page` Sunum / Föy bölümüne giderse 9.)

---

## 6. C sınıfı ilkeler (kural metni / bölüm rehberi için, en fazla 10)

1. Brief belgesi siyah-beyaz tasarlanır; marka renkleri yalnız HEX değeri olarak bilgi alanlarında yazılır (tek tip kullanım notu, §9 son madde).
2. Her görselde, slaytta ve story karesinde tek ana mesaj; kullanıcı ana mesajı ilk 2 saniyede anlamalı (§9, §12).
3. CTA alanı küçük, silik ya da okunaksız bırakılmaz; CTA, logo ve ana başlık platform arayüzleriyle çakışmayan güvenli alanda durur (§7, §9).
4. Logo kullanım talimatı yoksa tasarımcı logoyu kendiliğinden eklemez (§9).
5. Video ve Reels'te ilk 3 saniye kanca, altyazı okunabilir; son karede CTA (§8A, §15).
6. Görseldeki ve yayındaki metin brief'teki son sürümle birebir aynı olur (§13 "Metin Kontrolü", §15).
7. Kurumsal renk ve font dışına çıkılmaz; gerekirse alternatif açıkça belirtilir; onaysız renk kullanılmaz (tek tip §7, şablon §10).
8. Düşük çözünürlüklü, piksel bozulmalı, markanın sektörüne ve tonuna uymayan stok görsel; aşırı gölge, degrade, animasyon ve efekt kullanılmaz (şablon §10, tek tip §9).
9. Açık zemine açık yazı konmaz; küçük punto, çok ince font ve yoğun metinden kaçınılır; tasarım farklı platform ölçülerine kırpılmadan uyarlanabilir olur (şablon §10, tek tip §7).
10. Font dosyası içerik paketine ya da kaynaklara eklenmez; yalnız font adı, lisans durumu ve kullanım alanı yazılır (şablon §4 not).

---

## 7. Ana asistana notlar

- Çapraz başvurular (ayrı bulgu dosyalarında olması beklenen): SMS (gönderici adı, 160 karakter, kısa link, gönderim saatleri), basın bülteni (medya iletişim kişisi), podcast, sunum (16:9), mailing (preheader 70–100, banner 600–800 px), reklam (LinkedIn / TikTok), F/Z patern, video süreleri. Bu dosyada yalnız tek tip brief'in bunlara dokunduğu yerler A tablosunda işaretlendi.
- `oc_address` için `accounts` tipi önerisi formun izinli tip listesinin dışında; emsal `mk_ids` (URL olmayan etiketli kutular + `re`). Uygulanmazsa 10 ayrı text alan gerekir.
- `mk_formats`'a yeni kod (anket, canlı yayın) eklemeden önce içerik planı şablonunun format kodları ve `dogrula.mjs` doğrulanmalı.
- Yeni renk alanları `mkPlanData`'nın `renk` / `renkler` dizisine ve design token kurallarına eklenmeli; `brand_color_light` girildiğinde sabit `neut` haritası kullanılmamalı.
