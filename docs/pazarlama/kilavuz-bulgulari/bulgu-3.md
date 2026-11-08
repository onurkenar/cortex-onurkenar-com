# Bulgu 3 — Reklam · F-Z Patern · Hizmet Tanıtım Sayfası

Kaynaklar (üçü de baştan sona okundu):
- `Reklam_Olusturma_Kilavuzu_Kurumsal.txt` (616 satır, 23 bölüm)
- `F_Z_Patern_Kullanim_Kilavuzu_Kurumsal.txt` (370 satır, 16 bölüm)
- `Hizmet_Tanitim_Sayfasi_Olusturma_Kilavuzu_Kurumsal.txt` (394 satır, 16 bölüm)

Mevcut alanlar `alan-envanteri.md` ile karşılaştırıldı; ayrıca uygulamadaki DATA'dan ilgili alanların `rule` / `ruleDetail` metinleri okundu (sayı çelişkileri bu metinlerden).

Kılavuzlardaki şirkete özgü veriler (telefon "444 4 908", "NetOSGB", "RasyoTax", "Rasyotek & [Marka] İş Ortaklığı" başlığı, "81 ilde standart hizmet modeli", "CFO ve yönetim kurulu" örnekleri) seçenek ya da varsayılan yapılmadı; genel alanlara çevrildi.

---

## 0. Üç kılavuzda ortak olan karar: CTA satırı (yeni Ortak Bilgiler bölümü önerisi)

Üç kılavuz da aynı CTA biçimini standart olarak koyuyor:
- Reklam §1: "CTA alanlarında linke ek olarak telefon numarası da verilmelidir. Standart format: CTA: [CTA_METNİ] | Link: [URL] | Telefon: [TELEFON]."
- Reklam §14: "Tek aksiyon içerir, link ve telefonla tamamlanır."
- F-Z §11: "CTA: Detaylı Bilgi Al | Web: [link] | Telefon: [telefon]" · §10 "Telefon CTA altında veya yanında verilmeli; görseli kalabalıklaştırmamalıdır."
- Hizmet §11: "Telefon — CTA ile birlikte verilmeli: CTA: [CTA_METNİ] | Link: [CTA_LINK] | Telefon: [TELEFON]." · §3 "Telefon — [Kurumsal telefon numarası]"

CTA fiil listeleri de üç kılavuzda tekrar ediyor: Reklam §7.1 "Danışmanlık Talep Edin, Demo Talep Edin, Etkinliğe Kaydolun, Rehberi İndirin, Teklif Alın" · Reklam §18 "Teklif Alın / Bilgi Alın / Danışmanlık Talep Edin / Demo Talep Edin" · F-Z §10 "Teklif Alın, Bilgi Alın, Kaydolun, Rehberi İndir, Danışmanlık Talep Edin" · F-Z §11 "Hemen Başvur", "Linke Tıklayın / DM Atın / Formu Doldurun" · Hizmet §3 "Teklif Alın / Danışmanlık Talep Edin / Bize Ulaşın" · Reklam §6 "WhatsApp'tan yazın".

Bunlar kurum düzeyinde bir kez verilen ve site, reklam, sosyal, mail, sunum çıktılarının hepsini değiştiren kararlar. Mevcut karşılık yalnız `mk_contact` (serbest metin iletişim, **kısmi**: hangi numaranın CTA'da kullanılacağı, CTA biçimi ve fiil seti yok) ve `conversion_centered` (yalnız boolean, **kısmi**).

**Öneri — yeni bölüm `oc_cta` "Eylem Çağrısı (CTA)" (grup: Ortak Bilgiler, `oc_accounts`'tan önce ya da `oc_identity`'den hemen sonra).** Ortak bölümler açma boolean'ı taşımadığı için gerek yok.

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `oc_cta_phone` | text | CTA Telefonu | ph: "Örn. 0850 000 00 00 ya da +90 212 000 00 00 — boş bırakılırsa İletişim Bilgileri'ndeki ilk telefon" |
| `oc_cta_parts` | multiselect | CTA Satırının Bileşenleri | Bağlantı=link (önerilen) · Telefon=phone (önerilen) · WhatsApp=whatsapp · E-posta=email |
| `oc_cta_verbs` | multiselect | Kullanılacak CTA Metinleri | Teklif Alın=quote · Bilgi Alın=info · Danışmanlık Talep Edin=consult · Demo Talep Edin=demo · Kaydolun=register · Rehberi İndirin=download · Bize Ulaşın=contact · Hemen Başvurun=apply · WhatsApp'tan Yazın=whatsapp · DM Atın=dm |
| `oc_cta_primary` | select | Ana CTA | aynı on seçenek (tek seçim) |

Seçenek ayrıntıları:
- `oc_cta_phone` — scenario: Genel santral yerine çağrı merkezi / kısa numara / satış hattı CTA'da gösterilecekse doldurulur (Hizmet §3 "Kurumsal telefon numarası"). example: Reklam ve sayfa sonundaki CTA satırı "… | Telefon: 0850 000 00 00" olur; sitede `tel:` bağlantısıdır. Kural metnine Reklam §4'ten: "Aranabilir format … +90 formatı" → numara `tel:+90…` biçiminde bağlanır, görünür metin ulusal biçimdedir.
- `oc_cta_parts`
  - link — scenario: Her CTA'nın bir hedef adresi olmalı (Reklam §3 "CTA metni + CTA linki + telefon numarası"). example: "Link: /teklif-al/?utm_…".
  - phone — scenario: Kılavuzun varsayılanı; telefonla satış yapan kurumlar. example: "CTA: Teklif Alın | Link: … | Telefon: …" tek satırda.
  - whatsapp — scenario: Hızlı teklif / randevu WhatsApp'tan alınıyorsa (Reklam §6 "Click to WhatsApp … CTA: WhatsApp'tan yazın + telefon"). example: CTA satırına "WhatsApp: wa.me/…" eklenir.
  - email — scenario: Kurumsal satın alma e-postayla ilerliyorsa (Hizmet §9 "Bilgi alın / iş ortağımız olun formu, telefon ve e-posta"). example: Ortaklık sayfası CTA'sında e-posta adresi görünür.
  - Kural metnine platform istisnası yazılmalı (bkz. §1.4 çelişki): Google Arama reklamlarında telefon metne yazılmaz, telefon öğesiyle eklenir; TikTok gönderi metninde bağlantı tıklanmaz (Reklam §8 "Caption alanında tıklanabilir link … desteklenmez; CTA butonu ayrı gelir").
- `oc_cta_verbs` / `oc_cta_primary` — her seçenek için scenario: quote = fiyatı teklifle veren hizmet (Hizmet §11 Hero CTA); info = bilgilendirme içerikleri, F-Pattern (F-Z §11); consult = danışmanlık hizmetleri, F-Z hizmet tanıtımı (F-Z §11); demo = yazılım / SaaS (Reklam §7.1); register = webinar / etkinlik (Reklam §7 Event Ads, F-Z §10); download = rehber / lead magnet (Reklam §7 Document Ads); contact = genel kurumsal sayfalar (Hizmet §3); apply = başvuru kampanyaları, Z-Pattern (F-Z §11); whatsapp = Click to WhatsApp (Reklam §6); dm = Story / Reels (F-Z §11). example: seçilmeyen fiil üretilen hiçbir içerikte CTA olarak kullanılmaz; ana CTA hero, sayfa sonu ve reklam varsayılanıdır. Kanıt: F-Z §8 "CTA — Okuma akışının son durağına yerleştirilmelidir. Link ve telefon birlikte verilebilir." · F-Z §9 "Buton metni 2-4 kelime olmalı".

Not: `oc_cta_phone` için `derive` (mk_contact'tan) önerilmez — `mk_contact` serbest çok satırlı metin; ilk telefonu ayıklamak kırılgan. Boşken kural metni "İletişim Bilgileri'ndeki telefon" der.

---

## 1. Reklam Oluşturma Kılavuzu

### 1.1 Özet
**Amaç:** Reklamların strateji, kreatif, teknik dosya, platform uyarlaması, ölçüm, yayın ve optimizasyon süreçlerini tek standarda bağlamak; "performans hedefi, hedef kitle, dönüşüm aksiyonu, medya bütçesi, teknik varlıklar ve ölçüm altyapısını birlikte" ele almak.

**Bölümler (sırasıyla):** 1 Amaç ve kullanım ilkesi · 2 Üretim iş akışı (6 aşama) · 3 Ortak brief zorunlu alanları (12 alan) · 4 Ortak teknik kreatif standartları · 5 Google Ads (+5.1 checklist) · 6 Meta (+6.1 kreatif kontrol) · 7 LinkedIn (+7.1 B2B metin standardı) · 8 TikTok (+8.1 kreatif akışı) · 9 YouTube / Google video · 10 X · 11 Pinterest · 12 Microsoft Ads · 13 Display / Native / Programmatic · 14 Reklam metni standardı · 15 UTM ve dönüşüm eventleri · 16 Landing page ve form · 17 Hukuk, KVKK, marka güvenliği · 18 A/B test · 19 Dosya isimlendirme · 20 Yayın öncesi final checklist · 21 Performans raporlama KPI'ları · 22 Platform karar matrisi · 23 Kaynak ve güncellik notu.

**Sayısal standartlar:**
- Video: MP4/MOV, H.264, AAC, 1080p; ilk 2–3 sn hook; YouTube ilk 5 sn ana vaat; TikTok 0–2 sn hook / 2–8 problem / 8–18 çözüm / 18–25 kanıt / son 3 sn CTA; bumper 6 sn; X dikey video 15 sn altı önerilir, < 60 sn loop.
- Görsel oranları: 1:1, 4:5, 1.91:1, 9:16; Meta feed 1080×1080 / 1080×1350, Reels/Story 1080×1920; LinkedIn 1200×628 / 1200×1200; X 1200×1200, 1200×628, 2064×1080; Pinterest 2:3 1000×1500 (20 MB / 32 MB); YouTube thumbnail 1280×720, < 2 MB.
- Carousel: 2–10 kart (Meta, LinkedIn), Instagram 3–8 kart önerilir, X 2–6, Pinterest 2–5.
- RSA: 15 başlığa kadar, 4 açıklama (Google ve Microsoft).
- LinkedIn video 75 KB–500 MB, 3 sn–30 dk; TikTok ≤ 10 dk, ≤ 500 MB, ≥ 516 kbps, 9:16 min 540×960; X 280 karakter; Pinterest başlık 100 karakter (ilk 40 önemli), video 4 sn–15 dk (önerilen 6–15 sn); X anket 2–4 seçenek.
- Display banner: 300×250, 728×90, 160×600, 300×600, 320×100, 970×250.
- A/B: "en az 3 görsel/video ve 3 metin varyasyonu".
- Etiket: "LinkedIn 3-6, Instagram 5-10, X 2-4, TikTok 3-6 etiket."
- Yayın sonrası "ilk 24-48 saat izleme sorumlusu".

**Süreç (§2):** Strateji (Pazarlama/Marka) → Kreatif brief (İçerik/Tasarım) → Teknik hazırlık (Tasarım/Video/Web) → Kampanya kurulumu (Performance/Medya) → QA ve yayın (Performance/Web/İçerik; önizleme, test dönüşümü, final onay) → Optimizasyon (A/B, bütçe kaydırma, kreatif yenileme; KPI, frekans, CPA, CTR izleme).

**Uyum:** Lead formlarda "KVKK/aydınlatma metni ve gizlilik linki"; Meta lead formda "KVKK onayı"; TikTok lead "KVKK/açık rıza linki gerekir"; landing formda "KVKK aydınlatma metni, açık rıza veya ticari elektronik ileti onayı gerekiyorsa formda açıkça yer almalıdır"; §17: kanıtsız başarı oranı / garanti / kesin tasarruf / "en iyi-en büyük" yasak; sağlık, finans, vergi, hukuk, İSG, KVKK, kamu destekleri iddiaları uzman kontrolü; müşteri logosu, referans, testimonial, vaka çalışmasında izin; retargeting ve lead formda KVKK + çerez + açık rıza; rakip adı / karşılaştırmalı reklam hukuk kontrolü; stok lisansı, müzik telifi, seslendirme hakkı. Onay: "İçerik, marka, hukuk/teknik, medya ve final yayın onayı".

### 1.2 A sınıfı bilgiler
| Alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|
| "Google Ads, Meta, LinkedIn, TikTok, X, Pinterest, Microsoft Ads vb." | `mk_ads_channels` | **kısmi** — X, Pinterest, Microsoft Ads, Display/Native/Programmatic seçeneği yok; `linkedin` / `tiktok` seçeneklerinin `ruleDetail`'i boş ve ayrıntı bölümleri yok |
| "CTA: [CTA_METNİ] \| Link: [URL] \| Telefon: [TELEFON]" | `mk_contact` | **kısmi** → §0 `oc_cta` |
| "Kampanya Türüne göre CTA: Danışmanlık Talep Edin, Demo Talep Edin, Etkinliğe Kaydolun, Rehberi İndirin, Teklif Alın." | yok | **yok** → `oc_cta_verbs` |
| Google: "Search … Performance Max … Display … Demand Gen … YouTube … Shopping … App Campaigns … Lead Form Assets" | `mk_gads_types` | **kısmi** — App kampanyası yok |
| "Reklam uzantıları: site bağlantısı, açıklama, telefon, konum, lead form ve fiyat/struktur snippet" | `mk_gads_assets` | **kısmi** — konum, potansiyel müşteri formu, yapılandırılmış snippet yok |
| YouTube: "Skippable In-Stream / Non-Skippable / Bumper Ads 6 sn / In-Feed / Shorts" | `mk_gads_types` youtube | **kısmi** — hangi video formatlarının üretileceği kararı yok |
| Meta: "Feed Video 4:5 veya 1:1 … Collection Ads … Click to WhatsApp" | `mk_meta_creative`, `mk_meta_objectives` | **kısmi** — 4:5/1:1 akış videosu ve koleksiyon kreatifi yok (WhatsApp `messages` ile tam) |
| Meta: "Lead form reklamlarında gizlilik politikası, KVKK/aydınlatma linki ve teşekkür ekranı" | `mk_meta_form` (consent, thanks) | **tam** |
| LinkedIn formatları: Single Image, Video, Carousel, Document, Lead Gen Forms, Event, Conversation/Message, Text/Dynamic | yok | **yok** → yeni bölüm `mk_li` |
| LinkedIn: "risk, verimlilik, uyum, raporlama, hız ve kurumsal kontrol dili" | `brand_tone` | **kısmi** — ton var, B2B mesaj ekseni yok |
| LinkedIn hedefleme "Rol, sektör, şirket ölçeği" | `mk_b2b_roles`, `mk_b2b_sectors`, `mk_b2b_size` | **tam** (kural metninde LinkedIn hedeflemesine bağlanmalı) |
| TikTok formatları: Non-Spark In-Feed, Spark, Carousel, Lead Generation, Search/Smart+ | yok | **yok** → yeni bölüm `mk_tt` |
| "Pixel, Insight Tag, TikTok Pixel, GA4 event ve dönüşüm aksiyonları aktif." | `mk_ids` (linkedin_partner, tiktok_pixel), `mk_meta_prereq` | **kısmi** — kimlik alanı var, LinkedIn/TikTok için kurulum kararı yok |
| "A/B test için en az 3 görsel/video ve 3 metin varyasyonu önerilir." | yok | **yok** → `mk_ads_variants` |
| §18 test alanları: Başlık / Görsel / Video Hook / CTA / Landing Page / Hedef Kitle | yok | **yok** → `mk_ads_tests` |
| "Video … İlk 2-3 saniye hook içermeli; altyazı önerilir." · "son ekranda CTA + link + telefon" · "Kapak/thumbnail" | `mk_meta_creative` v916 ruleDetail (yalnız Meta 9:16), `mk_formats` R (organik) | **kısmi** — kanaldan bağımsız video reklam standardı yok → `mk_ads_video` |
| UTM: "utm_medium — cpc, paid_social, display, video, retargeting · utm_campaign — Marka + hizmet + amaç + dönem · utm_content — Kreatif türü / varyasyon · utm_term — Anahtar kelime veya hedef segment" | `mk_utm` | **kısmi / farklı** — mevcut şemada reklam ortamı tek "cpc", kampanya = dönem, utm_term yok, utm_content = gönderi/mail kimliği |
| "Dönüşüm Eventleri — form_submit, phone_click, whatsapp_click, lead, purchase, webinar_register" | `mk_conversions` | **kısmi** — webinar / etkinlik kaydı yok |
| "Ölçümleme — … CRM kaynak alanı" · "Lead Quality — CRM geri bildirimiyle ölçülmelidir." | `mk_data_entry`, `modules_extra` crm | **kısmi** — lead kalitesinin ölçümü kararı yok |
| §21 KPI: Impression, Reach, CTR, CPC, CPM, CVR, CPA/CPL, ROAS, Lead Quality, Frequency | `mk_north_star`, `mk_measure_scope` (gads, meta) | **kısmi** — reklam KPI seti yok; ölçüm kapsamında LinkedIn/TikTok yok |
| "Bütçe ve Takvim — Günlük/toplam bütçe, yayın tarihleri, test süresi, optimizasyon periyodu" | `mk_gads_budget`, `mk_meta_budget`, `mk_ads_days`, `mk_ads_pacing` | **kısmi** — LinkedIn / TikTok bütçesi yok |
| "Landing Page — Kampanya ile uyumlu sayfa" | `mk_ads_landing` | **tam** |
| "Abartılı vaat, doğrulanmamış rakam ve yanıltıcı ifade kullanılmamalı." | `mk_ads_claims`, `mk_banned` | **kısmi** — `mk_banned`'de "doğrulanmamış rakam / başarı oranı / kesin tasarruf" yok |
| "müşteri logosu, referans, testimonial veya vaka çalışması kullanımında izin" | `mk_banned` client_logo | **kısmi** — yalnız "logo veya adı" |
| "Görsellerde stok lisansı, müzikte telif hakkı ve seslendirme kullanım hakkı" | `mk_banned` copyright | **kısmi** — seslendirme yok |
| "Sağlık, finans, vergi, hukuk, İSG, KVKK ve kamu destekleri … uzman kontrolünden geçmelidir." | `mk_legal_scope` regulated "(sağlık, finans, hukuk)", `mk_approvers` | **kısmi** — konu uzmanı onaylayanı yok; düzenlenmiş alan listesi dar |
| "Onay Süreci — İçerik, marka, hukuk/teknik, medya ve final yayın onayı" | `mk_flow`, `mk_approvers` | **kısmi** — teknik ve medya (reklam) onaylayanı yok |
| §2 aşama sorumluları "Tasarım / Video / Web", "Performance / Medya" | `mk_roles` | **kısmi** — web / teknik rol yok (ads var) |
| §19 "[MARKA]_[KAMPANYA]_[FORMAT]_[PLATFORM]_[BOYUT]_[VERSIYON]" · §3 "Kampanya Adı — Marka, hizmet, dönem ve amaç içeren kısa adlandırma" | `mk_brief_format` full ruleDetail ("Marka_BriefNo_FORMAT_YAYINTARİHİ_v01"), `mk_utm_campaign` | **kısmi / farklı** — kampanya, kreatif, UTM listesi, rapor adlandırma standardı yok; brief'teki şablon farklı → `mk_naming` |
| "Etiket / Hashtag — LinkedIn 3-6, Instagram 5-10, X 2-4, TikTok 3-6 etiket." | `mk_hashtags` | **kısmi / çelişkili** (bkz. 1.4) |
| §22 karar matrisi (hedef → öncelikli platform) | `mk_ads_channels` | **kısmi** — öneri (`recommend`) yok |

### 1.3 Yeni alan önerileri

**(a) Yeni bölüm `mk_li` "LinkedIn Ads"** — grup Reklam, `mk_meta`'dan sonra. `mk_gads` / `mk_meta` gibi açma boolean'ı yerine her alan `showIf: [{field:"mk_ads_channels", in:["linkedin"]}]` (mevcut reklam bölümleriyle aynı desen). Kanıt: §7 tamamı.

| Kimlik | Tip | Etiket | Seçenekler (değer) |
|---|---|---|---|
| `mk_li_formats` | multiselect | Reklam Formatları | Tek görsel=single_image (önerilen) · Video=video · Carousel=carousel · Doküman reklamı=document · Lead Gen Form=lead_form (önerilen) · Etkinlik reklamı=event · Mesaj / sohbet reklamı=message · Metin / dinamik reklam=text_dynamic |
| `mk_li_message` | multiselect | B2B Mesaj Ekseni | Risk=risk · Verimlilik=efficiency · Uyum=compliance · Raporlama=reporting · Hız=speed · Kurumsal kontrol=control |
| `mk_li_form` | multiselect | Lead Gen Form Ayarları (showIf `mk_li_formats` ∋ lead_form) | En az alan=min_fields (önerilen) · Açık izin kutusu=consent (önerilen) · Gizlilik bağlantısı=privacy (önerilen) · Teşekkür ekranında telefon / site yönlendirmesi=thanks |
| `mk_li_insight` | boolean | LinkedIn Insight Tag | yes (önerilen) / no |
| `mk_li_budget` | text | Aylık Bütçe (TL) | ph: Örn. 15000 |

Seçenek ayrıntıları (`mk_li_formats`):
- single_image — scenario: "B2B hizmet tanıtımı, lead, trafik". example: 1200×628 ya da 1200×1200 görsel; giriş metni "sorun + çözüm; CTA + link + telefon".
- video — scenario: "Thought leadership, webinar, hizmet anlatımı". example: ilk 5 sn değer önerisi, altyazılı.
- carousel — scenario: "Süreç, rehber, çoklu fayda anlatımı". example: 2–10 kare kart, her kart tek mesaj, son kart CTA.
- document — scenario: "Lead magnet, rapor, rehber, föy". example: PDF önizlemesi; başlık "indirilebilir değeri anlatmalı", lead form ile.
- lead_form — scenario: "Nitelikli B2B lead". example: LinkedIn profil verisiyle dolan kısa form, açık izin ve gizlilik linki.
- event — scenario: "Webinar, canlı yayın, eğitim". example: tarih, saat, konuşmacı ve kayıt CTA'sı görünür.
- message — scenario: "Davet, demo, segment bazlı teklif". example: "Kişiselleştirilmiş ve kısa mesaj; tek net aksiyon."
- text_dynamic — scenario: "Awareness/retargeting destek". example: masaüstü sağ alanda kısa başlık + marka + CTA.

`mk_li_message` — scenario: kurumun değer önerisi hangi karar alanına dokunuyor (§7.1 "İlk cümle CFO, İK, operasyon, satın alma veya yönetim karar alanına dokunmalıdır"). example: seçilen eksen ilk cümlede yer alır ("… riskinizi yıl bitmeden görünür kılın"). Kanıt: "Abartılı satış dili yerine risk, verimlilik, uyum, raporlama, hız ve kurumsal kontrol dili kullanılmalıdır." Not: bu alan istenirse elenebilir (sınırda A); ton yerine "hangi fayda ekseni" kararıdır.

`mk_li_insight` — yes scenario: dönüşüm ve yeniden hedefleme ölçülecekse (§20 "Pixel, Insight Tag … aktif"). example: Insight Tag çerez onayına bağlı yüklenir, kimlik `mk_ids.linkedin_partner`'dan alınır. no scenario: yalnız farkındalık / lead form (platform içi). example: siteye LinkedIn etiketi eklenmez.

`mk_li_budget` — `mk_gads_budget` / `mk_meta_budget` ile eşlik (§3 "Bütçe ve Takvim").

Hedefleme alanı önerilmedi: `mk_b2b_roles` / `mk_b2b_sectors` / `mk_b2b_size` aynı kararı veriyor; LinkedIn kural metni bunları "LinkedIn hedeflemesi" olarak yazmalı.

**(b) Yeni bölüm `mk_tt` "TikTok Ads"** — grup Reklam, `mk_li`'den sonra; alanlar `showIf: [{field:"mk_ads_channels", in:["tiktok"]}]`. Kanıt: §8.

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_tt_formats` | multiselect | Reklam Formatları | Yeni kreatifli akış reklamı (Non-Spark In-Feed)=in_feed (önerilen) · Spark Ads=spark · Carousel=carousel · Lead Generation=lead · Arama / Smart+=search_smart |
| `mk_tt_spark` | select | Spark Ads Kaynağı (showIf `mk_tt_formats` ∋ spark) | Yalnız kendi hesabımızın videoları=own · Kendi hesabımız + izinli içerik üretici / UGC videoları=creators |
| `mk_tt_pixel` | boolean | TikTok Pixel | yes (önerilen) / no |
| `mk_tt_budget` | text | Aylık Bütçe (TL) | ph: Örn. 15000 |

- in_feed — scenario: "Yeni reklam kreatifiyle trafik, lead, app, satış". example: 9:16 video, CTA butonu ayrı; metinde tıklanabilir link, @ ya da etiket yok.
- spark — scenario: "Sosyal kanıt, creator/UGC, organik etkileşim güçlendirme". example: organik video ve yorumlarıyla reklam olarak yayınlanır.
- carousel — scenario: "Ürün, fayda listesi, öncesi/sonrası". example: her kart tek mesaj, son kart CTA.
- lead — scenario: "Hızlı teklif ve kayıt". example: kısa sorular; "KVKK/açık rıza linki gerekir" (kural metnine sabit).
- search_smart — scenario: "Arama niyeti veya otomatik optimizasyon". example: kreatif ile landing page aynı vaadi taşır.
- `mk_tt_spark` own — scenario: marka kendi organik videolarını büyütür. example: yalnız marka hesabının gönderileri reklamda. creators — scenario: UGC / creator güveni kullanılacaksa. example: içerik üreticisinin yetkilendirme kodu ve yazılı kullanım izni kaydedilir (`mk_banned` no_consent ile bağlantılı).
- `mk_tt_pixel` — `mk_li_insight` ile aynı mantık, kimlik `mk_ids.tiktok_pixel`.

**(c) `mk_ads` (59) — ortak reklam kuralları; showIf mevcut desenle `mk_ads_channels` ∌ none**

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_ads_variants` | select | Kreatif Varyasyon Sayısı | En az 3 görsel/video + 3 metin=three (önerilen) · 2 varyasyon (A/B)=two · Tek kreatif=one |
| `mk_ads_tests` | multiselect | Test Edilecek Değişkenler (showIf `mk_ads_variants` ∈ three, two) | Başlık=headline · Görsel=visual · Video kancası=hook · CTA=cta · Açılış sayfası / form=landing · Hedef kitle=audience |
| `mk_ads_video` | multiselect | Video Reklam Standardı | Altyazı=subtitles (önerilen) · İlk 2–3 saniyede kanca=hook (önerilen) · Marka ve fayda ilk 5 saniyede=brand5 · Son karede CTA + bağlantı + telefon=end_cta (önerilen) · Kapak / küçük resim=cover |

- `mk_ads_variants` three — scenario: bütçe öğrenme için yeterliyse; kılavuz önerisi (§6.1). example: her reklam setinde 3 görsel/video × 3 metin. two — scenario: küçük bütçe. example: tek değişkenli A/B. one — scenario: çok küçük bütçe / tek mesajlı duyuru. example: test yapılmaz, kreatif yorgunluğu frekansla izlenir.
- `mk_ads_tests` — scenario ve example her biri §18 tablosundan: headline (problem / fayda / kampanya odaklı; CTR, CPC, Quality Score), visual (insanlı / dashboard / ürün / ikon / infografik; CTR, CVR), hook (soru / iddia / risk / fırsat / sosyal kanıt; 3 sn izlenme), cta (Teklif Alın / Bilgi Alın …; CVR, CPA, lead kalitesi), landing (kısa form / uzun form / WhatsApp / telefon; form tamamlama), audience (lookalike / remarketing / ilgi / iş unvanı / anahtar kelime; CPA, ROAS). Kural: aynı anda tek değişken test edilir (C).
- `mk_ads_video` — kanıt: §4 "İlk 2-3 saniye hook içermeli; altyazı önerilir." · §5 YouTube "İlk 5 saniye ana vaat; son ekranda CTA + link + telefon." · §9 "Thumbnail ve başlık kritik." · §20 "Video kreatiflerde ilk 3 saniye hook, altyazı, kapak görseli ve son CTA kontrol edildi." scenario (subtitles): reklamlar sessiz izlenen akışlarda gösterilecekse. example: tüm reklam videolarında yanmış (burned-in) ya da yüklenmiş altyazı.

**(d) `mk_measure` (62)**

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_ads_kpis` | multiselect | Reklam KPI Seti (showIf `mk_ads_channels` ∌ none) | Gösterim=impressions · Erişim=reach · TO (CTR)=ctr · TBM (CPC)=cpc · BGM (CPM)=cpm · Dönüşüm oranı (CVR)=cvr · Edinme / lead başı maliyet (CPA / CPL)=cpa · ROAS=roas · Lead kalitesi (CRM geri bildirimi)=lead_quality · Frekans=frequency |

Önerilen set hedefe göre (`recommend` `mk_goals`'tan): awareness → impressions, reach, cpm, frequency; leads / requests → ctr, cvr, cpa, lead_quality; sales → cvr, cpa, roas. Kanıt: §21 "Yorumlama Notu" sütunu ("Awareness kampanyalarında kritik", "E-ticaret/satış kampanyaları için", "CRM geri bildirimiyle ölçülmelidir", "Kreatif yorgunluğu ve remarketing kontrolü").

**(e) `mk_creative` (55) — adlandırma (üç kılavuzda ortak)**

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_naming` | select | Adlandırma ve Sürüm Standardı | Kurumsal şablon (MARKA_KONU_FORMAT_PLATFORM_BOYUT_vNN)=structured (önerilen) · Kısa (marka-konu-vNN)=short · Serbest=free |

- structured — scenario: birden çok kişi / ajans aynı dosyalarla çalışıyorsa. example: kreatif "Marka_Kampanya_Video_Meta_1080x1920_v01.mp4", kampanya "Marka_Hizmet_Lead_Search_YYYYAA_v01", UTM listesi "Marka_Kampanya_UTM_YYYYAA", rapor "Marka_Platform_Kampanya_Rapor_DÖNEM", hizmet sayfası içerik dosyası "Marka_Hizmet_Hizmet_Tanitim_Sayfasi_v01.docx", web görseli küçük harf tireli "marka-hizmet-adi-one-cikan-gorsel.webp"; sürüm v01, v02 … final.
- short — scenario: tek kişilik ekip. example: "marka-yaz-kampanyasi-v02.png".
- free — scenario: dosya takibi yapılmıyor. example: yalnız `mk_visual_meta` filename kuralı uygulanır.
- Kanıt: Reklam §19 tablo; Reklam §3 "Örn: …_Lead_Search_202607_v01"; Hizmet §16 tablo ve "Revizyon — v01, v02, v03, final şeklinde takip edilmelidir."
- Çakışma: `mk_brief_format` full ruleDetail'deki "Marka_BriefNo_FORMAT_YAYINTARİHİ_v01" ayrı bir şablon; `mk_naming` seçilince brief teslim dosyası da bu standarda bağlanmalı (tek kaynak). Diğer kılavuz bulgularında (tek tip brief) farklı şablon çıkarsa birleştirilmeli.

### 1.4 Mevcut alanlarda değişiklik önerileri
1. **`mk_ads_channels`** — seçenek ekle: `microsoft` "Microsoft Ads (Bing)" (ruleDetail: "Google Ads import sonrası ayarlar, URL, tracking ve uzantılar kontrol edilmeli." §12), `x` "X Ads" (ruleDetail: 280 karakter kısa metin; etiket 2–4 §10, §14), `pinterest` "Pinterest Ads" (ruleDetail: 2:3 1000×1500, başlığın ilk 40 karakteri §11), `programmatic` "Görüntülü / native / programatik reklam" (ruleDetail: HTML5 banner clickTag + yedek görsel, native'de "editoryal görünüme uygun ama yanıltıcı olmayan dil", frekans ve kreatif yorgunluğu §13). `linkedin` ve `tiktok`'a ruleDetail yaz (bölümleri yoksa en azından §7.1 ve §8.1 özeti). Ayrıca `recommend: {field:"mk_goals", map:{leads:["linkedin","google"], requests:["google","meta"], awareness:["meta","google","tiktok"], sales:["google","meta"], community:["meta","tiktok"]}}` — §22 karar matrisi ("B2B lead toplama → LinkedIn", "Geniş farkındalık → Meta / YouTube / TikTok", "E-ticaret satış → Google Shopping / PMax", "Hızlı teklif / WhatsApp → Meta"). B2B ayrımı için ikinci kaynak `business_model` b2b → linkedin.
2. **`mk_ads_landing` / `mk_ads_claims` showIf** — şu an `in: ['google','meta','linkedin','tiktok']`; yeni kanal değerleri eklenirse bu listelere de eklenmeli (aksi halde yalnız X / Microsoft seçen projede ortak kurallar gizlenir).
3. **`mk_gads_types`** — `app` "Uygulama kampanyası" ekle (§5 "App Campaigns — Uygulama yükleme veya uygulama içi aksiyon"). `search` ruleDetail "en az 8 farklı başlık … 4 açıklama" → kılavuz "15 başlığa kadar, 4 açıklama; anahtar kelime, fayda, kanıt ve CTA varyasyonları" — "en az 8, en çok 15 başlık" olarak genişletilebilir (çelişki yok). `demand_gen` ruleDetail boş → "1:1, 4:5, 1.91:1 görsel; kısa video; ilk mesaj görselde". `pmax` ruleDetail'e "Asset grupları hizmet/ürün bazında ayrılır; her asset grubu tek tema taşır."
4. **`mk_gads_assets`** — seçenek ekle: `location` "Konum", `lead_form` "Potansiyel müşteri formu" (ruleDetail: "Form alanları minimum tutulur; KVKK/aydınlatma metni ve gizlilik linki eklenir … teşekkür ekranı + telefon yönlendirmesi" §5), `snippet` "Yapılandırılmış snippet" (§5.1).
5. **Yeni alan `mk_gads_yt`** [multiselect] "YouTube Video Formatları", showIf `mk_gads_types` ∋ youtube: Atlanabilir yayın içi=skippable · Atlanamaz yayın içi=non_skippable · Bumper (6 sn)=bumper · Akış içi (In-Feed)=infeed · Shorts=shorts. Kanıt §9 tablosu; üretilecek video sürelerini ve oranlarını değiştirdiği için A. (scenario/example §9'daki "Kullanım" / "Kreatif Notu" sütunlarından: bumper "Frekans ve hatırlanma — Tek vaat + marka", shorts "İlk 1-2 sn hook, altyazı", infeed "Thumbnail ve başlık kritik".)
6. **`mk_gads_assets` call — ÇELİŞKİ (korunmalı):** mevcut ruleDetail "Telefon numarası reklam metnine yazılmaz, telefon öğesiyle eklenir" — kılavuz §5 "açıklamalar fayda + CTA + telefon içerir" diyor. Google Ads politikası başlık / açıklamada telefon numarasını kabul etmez; mevcut kural doğru. Öneri: CTA satırı kuralına (§0) "Google Arama reklamlarında telefon yalnız telefon öğesiyle" istisnası yazılsın; kılavuz düzeltilmez, uygulama platform kuralını önde tutar. Kılavuzun kendi notu da bunu destekler: "Platform teknik gereklilikleri zamanla değişebilir; final yükleme öncesi ilgili reklam panelinde güncel spec doğrulaması yapılmalıdır."
7. **`mk_meta_creative`** — seçenek ekle: `v45` "4:5 / 1:1 akış videosu" (§6 "Facebook Feed Video — 4:5 veya 1:1; MP4/MOV; altyazılı; ilk 3 sn hook"), `collection` "Koleksiyon (kapak + ürün / hizmet kartları)" (§6 "Katalog ve landing page uyumu önemli"). `carousel` ruleDetail'e "2–10 kart; Instagram'da 3–8 kart önerilir; kart 1 kanca, son kart CTA".
8. **`mk_utm`** — seçenek ekle: `ads_full` "Ayrıntılı reklam şeması (5 parametre)" ruleDetail: utm_source = platform (google, meta, linkedin, tiktok, x, pinterest, microsoft); utm_medium = cpc / paid_social / display / video / retargeting; utm_campaign = marka_hizmet_amaç_dönem; utm_content = kreatif türü ve varyasyonu (ör. video_hooka_9x16); utm_term = anahtar kelime ya da hedef segment. Mevcut `standard` organik için kalır (reklamda tek "cpc" yerine kanal ayrımı kılavuzun §15 standardı). `mk_utm_campaign` placeholder'ı "Örn. marka_hizmet_lead_202607" olabilir.
9. **`mk_conversions`** — seçenek ekle: `event_register` "Etkinlik / webinar kaydı" (§15 "webinar_register"). Lead kalitesi için `mk_ads_kpis` lead_quality yeterli.
10. **`mk_measure_scope`** — seçenek ekle: `linkedin` "LinkedIn Ads", `tiktok` "TikTok Ads" (diğer kanallar eklenirse onlar da), `crm` "CRM lead kalitesi geri bildirimi" (§21 "Lead Quality — Satışa uygun lead oranı — CRM geri bildirimiyle ölçülmelidir").
11. **`mk_flow`** — seçenek ekle: `staged` "Taslak → Revizyon → İçerik onayı → Teknik onay → Yayına hazır" (Hizmet §16 "Onay Durumu — Taslak / Revizyonda / İçerik Onayı / Teknik Onay / Yayına Hazır."; Reklam §2 "QA ve Yayın — Önizleme, test dönüşümü, final onay"). `mk_approvers` showIf'ine `staged` eklenmeli.
12. **`mk_approvers`** — seçenek ekle: `technical` "Teknik / web sorumlusu", `media` "Medya / reklam sorumlusu", `expert` "Konu uzmanı (teknik doğruluk)". Kanıt: §3 "İçerik, marka, hukuk/teknik, medya ve final yayın onayı"; §17 "teknik iddialar uzman kontrolünden geçmelidir".
13. **`mk_roles`** — seçenek ekle: `web` "Web / teknik sorumlu" (§2 "Teknik Hazırlık — Tasarım / Video / Web"; "QA ve Yayın — Performance / Web / İçerik").
14. **`mk_banned`** — seçenek ekle: `unverified_stats` "Doğrulanmamış rakam, başarı oranı veya kesin tasarruf vaadi" (§17, §4). `client_logo` etiketini "Onaysız müşteri logosu, adı, yorumu veya vaka çalışması" yap (§17 "testimonial veya vaka çalışması"). `copyright` etiketini "Telifli / lisanssız müzik, görsel veya seslendirme" yap (§17 "seslendirme kullanım hakkı").
15. **`mk_legal_scope` regulated** — etiket "(sağlık, finans, hukuk)" → "(sağlık, finans, vergi, hukuk, iş sağlığı ve güvenliği, kişisel veri, kamu destekleri)" (§17).
16. **`mk_hashtags` — ÇELİŞKİ:** rule metni "X'te en çok 2 etiket kullanılır" ve `brand_topic` "3–5 konu etiketi"; kılavuz §14 "LinkedIn 3-6, Instagram 5-10, X 2-4, TikTok 3-6 etiket." Öneri: seçenek ekle `per_platform` "Platforma göre (LinkedIn 3–6 · Instagram 5–10 · X 2–4 · TikTok 3–6)" ve rule metnindeki sabit "X'te en çok 2" ifadesini yalnız `brand_topic`'e taşı. (Sosyal medya kılavuzu bulgusunda başka sayı çıkarsa o esas alınmalı; bu kılavuzdaki sayı reklam metni tablosunda geçiyor.)

### 1.5 B sınıfı brief alanları (form alanı değil)
Kampanya adı (tekil değer; adlandırma standardı A) · platform ve reklam formatı (kampanya başına) · kampanya amacı · hedef kitle tanımı (rol, sektör, ölçek, lokasyon, ilgi, davranış, remarketing listesi, benzer kitle) · ana teklif / değer önerisi · tek ana mesaj, destek mesajı, kanıt · CTA metni + link (kampanyaya özel) · landing page adresi · bütçe ve takvim (yayın tarihleri, test süresi) · ölçüm eşleştirmesi (hangi dönüşüm etiketi) · onay kayıtları · RSA başlık / açıklama metinleri · anahtar kelime ve negatif listeler · Pinterest / X / Meta kreatif dosyaları · UTM değerleri · yayın sonrası 24–48 saat izleme sorumlusu (kişi) · rapor dönemi.

### 1.6 C sınıfı ilkeler (kurala / rehbere)
1. Her reklam amaç, kitle, mesaj, teklif, CTA, landing page ve ölçümle birlikte tasarlanır; metin, görsel ve dosya özellikleri platforma özel hazırlanır (§1).
2. Yayından önce piksel, dönüşüm, UTM, form, telefon / WhatsApp tıklaması, landing açılışı ve teşekkür sayfası test edilir; ilk 24–48 saat izlenir (§1, §20).
3. Kritik metin, logo ve CTA güvenli alanda kalır; Stories / Reels üst-alt arayüz alanına metin konmaz; her yerleşim için ayrı kırpım kontrol edilir (§4, §6.1).
4. Görselde tek ana mesaj, küçük puntolu yoğun metin yok; carousel'de her kart tek mesaj, son kart CTA (§4, §6.1).
5. Landing page reklamla aynı vaadi ve aynı CTA'yı taşır, mobilde hızlı açılır (LCP / CLS), form alanları amaca göre en azdadır (§16).
6. Lead formlarda gizlilik ve aydınlatma bağlantısı, gerekiyorsa açık rıza / ticari ileti onayı ayrı kutuda; teşekkür ekranı ölçüme bağlıdır (§5, §6.1, §16).
7. Retargeting ve lead form reklamları çerez ve rıza süreçlerine uyumludur; rakip adı / karşılaştırmalı reklam hukuk kontrolünden geçer (§17).
8. Telefon tıklanabilir ve aranabilir biçimde (ulusal kısa numara ya da +90) yazılır; TikTok metninde bağlantı / @ / etiket tıklanmaz, CTA butonu kullanılır (§4, §8).
9. Kreatif yorgunluğu frekansla izlenir; kreatif yenileme ve bütçe kaydırma optimizasyon döngüsünün parçasıdır (§2, §13, §21).
10. Platform teknik gereklilikleri değişkendir; yükleme öncesi panelde güncel spec doğrulanır (kapak notu, §23).

---

## 2. F-Z Patern Kullanım Kılavuzu

### 2.1 Özet
**Amaç:** Tasarımı "okunabilirlik, mesaj hiyerarşisi ve dönüşüm akışı" açısından yönetmek; başlık, görsel, fayda, kanıt ve CTA'yı göz hareketine göre yerleştirmek. Kapsam: mailing, sosyal medya (LinkedIn, Instagram, Facebook, X, WhatsApp Business, YouTube Community, Threads, TikTok), web / landing (hero, hizmet sayfası, blog öne çıkan görsel, banner, form blokları), sunum / PDF (kapak, satış sunumu, lead magnet, rehber, teklif föyü).

**Bölümler:** 1 Amaç ve kapsam · 2 Temel kavramlar (F, Z, F-Z hibrit) · 3 Kullanım karar matrisi · 4 F-Pattern · 5 Z-Pattern · 6 F-Z hibrit · 7 Format bazlı standartlar · 8 Tasarım alanları ve yerleşim rolleri · 9 Teknik tasarım standartları · 10 İçerik ve metin standardı · 11 CTA yerleşimi · 12 Görsel hiyerarşi ve erişilebilirlik · 13 Uygulama şablonları · 14 Hatalı kullanımlar · 15 Tasarımcı final checklist (10 madde) · 16 Brief içinde kullanım formatı.

**Sayısal standartlar:** F başlık 6–8 kelime, en çok 2 satır; alt başlık / alt açıklama 15–20 kelime; bilgilendirmede 3–5 kısa madde; görsel postlarda en çok 25–35 kelime; başlık alanı görselin %15–25'i; Z başlık 4–7 kelime; Z görsel / metin %55–70 / %30–45; fayda maddeleri en çok 3, her biri 3–5 kelime; CTA buton metni 2–4 kelime; ana mesaj ilk 2 saniyede; carousel şablonu 7 slayt (Hook / Problem / İçgörü / Fayda / Çözüm / Kanıt / CTA).

**Format → patern (§7):** Bilgilendirme bülteni F · Kampanya / webinar maili Z ya da F-Z · LinkedIn tek görsel F-Z · Instagram post Z · Carousel F + Z kapanış · Story / Reels kapak Z · Blog öne çıkan görsel merkez ya da F-Z · Landing hero F-Z · Sunum kapak Z.

**Süreç:** İçerik amacına göre patern seç (§3) → alanları rollerine göre yerleştir (§8) → teknik standartlar (§9) → metin ölçüleri (§10) → CTA son durakta (§11) → checklist (§15) → brief'e "Seçilen patern, gerekçe, okuma akışı, CTA konumu, teknik not, teslim kontrolü" yazılır (§16).

**Uyum:** Erişilebilirlik — "Renk tek başına anlam taşıyıcı olmamalı", alternatif metin, yüksek kontrast, mobilde küçük punto yok; yasal dipnot "küçük puntoda … okunabilir". KVKK / İYS maddesi yok.

### 2.2 A sınıfı bilgiler
| Alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|
| "F-Z patern talimatı aşağıdaki standart alanlarla verilmelidir: Seçilen Patern … Kullanım Gerekçesi … Okuma Akışı … CTA Konumu …" | `mk_brief_format` | **kısmi** — brief biçimi var, okuma deseni standardı (kullanılıyor mu) yok → `mk_fz` |
| "Landing Page Hero — F-Z — Sol metin/sağ görsel veya merkez başlık + sağ alt CTA" · Hizmet §12 "Okuma Akışı — F/Z paternine uygun başlık, görsel, fayda ve CTA yerleşimi planlanmalıdır." | `conversion_centered`, `page_layout_approach` (Split-Screen) | **kısmi** — sitede okuma deseni kararı yok → `reading_pattern` (03) |
| "Logo — Sol üst en güvenli alandır; sosyal görsellerde küçük kullanılmalıdır." · "Blog Öne Çıkan Görsel — … logo talimata bağlı" · checklist "Logo kullanımı brief talimatına uygun mu?" | `brand_logo_rules` (koruma alanı, min boyut…) | **kısmi** — pazarlama görsellerinde logonun yeri / kullanımı kararı yok → `mk_logo_place` |
| "İkonlar aynı stil ailesinden seçilmeli; outline veya minimal ikon tercih edilmelidir." | `brand_icons` | **tam** (Outline seçeneği var; kılavuz Outline'ı öneriyor — "(önerilen)" eklenebilir) |
| "Telefon CTA altında veya yanında verilmeli" · CTA formatları §11 | — | → §0 `oc_cta` |
| "CTA Metni — Aksiyon odaklı olmalıdır: Teklif Alın, Bilgi Alın, Kaydolun, Rehberi İndir, Danışmanlık Talep Edin." | yok | → `oc_cta_verbs` |
| "Mailing - Bilgilendirme Bülteni — F-Pattern … Mailing - Kampanya / Webinar — Z-Pattern veya F-Z" | `mk_mail_layout` (single / multi) | **kısmi** — düzen var, desen yok (kural metnine `mk_fz` açıkken eklenir; ayrı alan gerekmez) |
| "Bilgilendirme içeriklerinde 3-5 kısa madde; görsel postlarda maksimum 25-35 kelime." | `mk_formats` T ruleDetail "görsel üzerindeki metin en çok 12 kelimedir" | **çelişkili** (bkz. 2.4) |
| "Carousel — 1: Hook / 2: Problem / 3: İçgörü / 4: Fayda / 5: Çözüm / 6: Kanıt / 7: CTA" | `mk_formats` C ruleDetail "6–9 slayt … son slayt CTA" | **tam** (7 slayt aralığın içinde; şablon kural metnine eklenebilir) |

### 2.3 Yeni alan önerileri
**`mk_creative` (55):**

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_fz` | boolean | F / Z Okuma Deseni Standardı | yes (önerilen) / no |
| `mk_logo_place` | select | Görsellerde Logo Kullanımı | Sol üst köşe, küçük=top_left (önerilen) · Üst bant (logo + tarih / kategori)=top_band · Her brief'te ayrıca belirtilir=brief |

- `mk_fz` yes — scenario: Mailing, sosyal görsel, carousel, story, blog görseli ve sunumlar tek yerleşim mantığıyla üretilecekse (§1 Kapsam). example: brief'te "Seçilen patern: Z · CTA konumu: sağ alt" satırı; bülten F (sol hizalı başlık, maddeler, altta CTA), kampanya görseli Z (sol üst logo, sağ üst etiket, merkez görsel, sağ alt CTA), LinkedIn görseli F-Z. ruleDetail: §7 eşleme tablosu + §10 ölçüleri (başlık 6–8 / Z 4–7 kelime, alt açıklama 15–20, en çok 3 fayda maddesi, CTA 2–4 kelime) + §15 checklist teslim öncesi uygulanır. no — scenario: tasarım dili serbest bırakılıyorsa / tasarımcı kendi sistemini kullanıyorsa. example: brief'te patern satırı yok. Kanıt: §16 "Tasarım brieflerinde F-Z patern talimatı aşağıdaki standart alanlarla verilmelidir".
- `mk_logo_place` top_left — scenario: kılavuzun varsayılanı; sosyal ve reklam görselleri. example: her görselde sol üstte küçük logo, ana mesajdan baskın değil (§4 "Logo küçük, net ve ana mesajdan baskın olmayacak"). top_band — scenario: bülten, rapor, etkinlik görselleri tarih / kategoriyle birlikte. example: üst bantta logo + tarih (§8 "Tarih / Kategori — Üst bantta logo ile birlikte"). brief — scenario: blog öne çıkan görsellerinde logo bazen istenmiyorsa (§7 "logo talimata bağlı"). example: brief'te "Logo: yok / sol üst" satırı zorunlu. (Not: tek tip brief kılavuzu bulgusunda logo kuralı varsa birleştirilmeli.)

**`design_approach` (03) — proje alanı:**

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `reading_pattern` | boolean | F / Z Okuma Deseni (Hero ve Hizmet Sayfaları) | yes / no |

- yes — scenario: kurumsal site, hizmet ve landing sayfaları dönüşüm odaklıysa (§6 "lead toplama, hizmet tanıtımı ve karar vericiye yönelik B2B içeriklerde etkilidir"). example: hero'da solda H1 + alt açıklama + CTA, sağda ürün / ekip / dashboard görseli, altta güven unsurları (§13 "Landing Hero"); bilgi yoğun sayfalarda sol hizalı başlık ve bloklar (F). no — scenario: galeri, portföy, deneysel tasarımlar. example: yerleşim tasarım stiline bırakılır. `recommend`: `conversion_centered` true → yes; `project_type` Corporate Website / Landing Page / B2B Platform → yes.

### 2.4 Mevcut alanlarda değişiklik önerileri
1. **`mk_formats` T — ÇELİŞKİ:** ruleDetail "görsel üzerindeki metin en çok 12 kelimedir"; F-Z §4 "görsel postlarda maksimum 25-35 kelime" (F-Pattern bilgilendirme görselleri için). Z görsellerinde (Instagram post §7) kısa başlık 4–7 kelime + kısa CTA 12 kelimeye uyuyor. Öneri: ruleDetail "Tanıtım / kampanya görsellerinde (Z) en çok 12 kelime; bilgilendirme görsellerinde (F) en çok 25–35 kelime ve 3–5 kısa madde" — ya da `mk_fz` açıkken bu ayrım uygulanır. (Sosyal medya kılavuzu bulgusundaki sayı ile karşılaştırılmalı.)
2. **`brand_icons`** — `Outline` etiketine "(önerilen)" (§9 "outline veya minimal ikon tercih edilmelidir").
3. **`mk_mail_layout`** — `mk_fz` açıkken kural: tek konu (kampanya / webinar) → Z ya da F-Z, çok bölümlü bülten → F (§7). Alan değişmez, rule metnine koşullu ek.
4. **`mk_formats` C** — ruleDetail'e §13 yedi slaytlık şablon (Hook → Problem → İçgörü → Fayda → Çözüm → Kanıt → CTA) eklenebilir.

### 2.5 B sınıfı brief alanları
Seçilen patern (F / Z / F-Z) — içerik başına · kullanım gerekçesi · okuma akışı (1. başlık → 2. alt açıklama → 3. görsel / kanıt → 4. fayda → 5. CTA) · CTA konumu (alt blok / sağ alt / alt merkez / son slayt / son kare) · teknik not (güvenli alan, mobil, logo, negatif alan, kırpma) · teslim kontrolü · ana başlık, alt açıklama, fayda maddeleri, CTA metni ve linki · tarih / kategori / kampanya etiketi · ana görsel.

### 2.6 C sınıfı ilkeler
1. Patern içerik amacına göre seçilir: bilgi yoğunsa F, dikkat ve aksiyon odaklıysa Z, bilgi + aksiyon dengesinde F-Z (§3).
2. CTA okuma akışının son durağındadır; buton, link ve telefon kopuk verilmez (§8, §14).
3. Tek tasarımda tek ana mesaj; logo, başlık ve CTA aynı görsel ağırlıkta gösterilmez (§14).
4. Başlık 6–8 kelime (Z'de 4–7), en çok 2 satır; alt açıklama 15–20 kelime; en çok 3 fayda maddesi, her biri 3–5 kelime; CTA metni 2–4 kelime (§4, §5, §9, §10).
5. Ana mesaj ilk 2 saniyede anlaşılır; başlıklar düşük kontrastlı veya yoğun görsel üzerinde kaybolmaz (§12).
6. Renk tek başına anlam taşımaz; görsellere alternatif metin, web'de ayrıca SEO alt metni yazılır (§12).
7. Kritik metin ve CTA kenara yaslanmaz, platform arayüzüyle çakışmaz; tasarım farklı ölçülere kırpılmadan uyarlanabilir (§9).
8. Mobil öncelik: tek kolon, mobilde küçük punto yok, mobil önizleme zorunlu (§4, §9, §12).
9. Başlık bold, alt açıklama regular / medium; satırlar ve bloklar kısa, aralarında negatif alan (§9).
10. Yasal dipnot ve footer alt alanda küçük ama okunabilir puntoda (§8, §10).

---

## 3. Hizmet Tanıtım Sayfası Oluşturma Kılavuzu

### 3.1 Özet
**Amaç:** Hizmet sayfalarını "SEO uyumlu, dönüşüm odaklı, okunabilir ve marka standardına uygun" hazırlamak; sayfa "kullanıcıyı teklif, form, arama veya danışmanlık talebi gibi aksiyonlara yönlendiren stratejik bir satış destek varlığıdır".

**Bölümler:** 1 Amaç ve kapsam · 2 Sayfa türleri (standart detay, kısa, iş birliği ana, iş ortaklığı detay) · 3 Üretim öncesi bilgi toplama formu (12 alan) · 4 SEO ve meta standartları · 5 Görsel, video ve podcast meta alanları · 6 Standart sayfa mimarisi (16 modül) · 7 Kısa sayfa mimarisi (8 modül) · 8 İş birliği sayfası mimarisi (9 modül) · 9 İş ortaklığı detay yapısı (12 bölüm) · 10 Yazım dili ve okunabilirlik · 11 CTA, form ve dönüşüm · 12 UX, tasarım ve teknik web · 13 Schema, iç linkleme ve yayın · 14 Kopyalanabilir şablon · 15 Yayın öncesi checklist (15 madde) · 16 Dosya isimlendirme ve revizyon.

**Sayısal standartlar:** URL slug ≤ 75 karakter (ideal 30–60), küçük harf, tire, Türkçe / özel karakter yok · odak anahtar kelime ≤ 3 kelime · meta title 35–60 karakter, 285–580 px · meta description 120–160 karakter, 680–920 px · sayfa özeti 40–60 kelime · öne çıkan görsel 16:9, 1920×1080, WebP · avantajlar 3–6 (kısa sayfada 3–5) · kısa sayfada en çok 3 FAQ, ortaklık detayında 3–5 · müşteri görüşü 1–3 (ortaklık detayı) · paragraf 40–70 kelime · H başlık ≤ 64 karakter · tek H1 · ilgili blog 3–6.

**Süreç:** Bilgi toplama (§3) → SEO / meta (§4) → medya meta (§5) → mimariye göre içerik (§6–9) → dil ve hiyerarşi (§10) → CTA ve form (§11) → UX / teknik (§12) → schema, iç link, UTM (§13) → checklist (§15) → adlandırma ve onay durumu (§16: Taslak / Revizyonda / İçerik Onayı / Teknik Onay / Yayına Hazır).

**Uyum:** Form alanlarında "KVKK onay alanı"; "Form UX — … KVKK metinleri görünür olmalıdır"; sertifika / referans / rakam gibi güven unsurları gerçek olmalı; erişilebilirlik (alt metin, kontrast, klavye, form etiketleri).

### 3.2 A sınıfı bilgiler
| Alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|
| Sayfa türleri: "Standart Hizmet Detay Sayfası … Kısa Hizmet Tanıtım Sayfası … İş Birliği Ana Sayfası … İş Ortaklığı Detay Sayfası" | `mk_prod_types` (service, product, package) | **kısmi** — kayıt türü var; sayfa derinliği (standart / kısa) ve iş birliği / ortaklık sayfaları yok → `mk_prod_pages` |
| §6 modüller: Hero, hizmet anlatımı, avantajlar, video/ses/galeri, markanın öne çıkan avantajları, sertifika ve belgeler, referanslar, öne çıkan rakamlar, case study, teknik özellikler ve kapsam, fiyat/paketler, indirilebilir içerik, CTA, FAQ, diğer hizmetler, ilgili bloglar | `mk_prod_fields` (slogan, summary, value, audience, benefits, features, price_note, faq, image, proof) | **kısmi** — süreç, teknik kapsam, "neden biz", sertifika, rakamlar, vaka, medya galerisi, paket karşılaştırması, indirilebilir içerik, CTA alanları, içindekiler, diğer hizmetler yok |
| "Fiyatlandırma / Paketler — Şeffaf paket karşılaştırması; fiyat yoksa paket kapsamı ve Enterprise seçenekleri." | `mk_prod_price` (open, from, quote) | **tam** (paket karşılaştırması modül olarak `mk_prod_fields`'e) |
| "Anahtar Kelime — Maksimum 3 kelime olmalı; H1, giriş, meta title, meta description ve ilgili alt başlıklarda doğal şekilde kullanılmalıdır." | `mk_prod_keywords` | **kısmi** — "en çok 3 kelime" ve "giriş + alt başlık" kullanımı ruleDetail'de yok |
| §11 "Hero CTA … Orta Sayfa CTA … Sticky CTA … Final CTA" | `conversion_centered` | **kısmi** — CTA yerleşim kararı yok → `mk_prod_cta` |
| "Form Alanları — Ad Soyad, Şirket, Telefon, E-posta, Hizmet İlgisi, Mesaj, KVKK onay alanı." | yok (üyelik `member_signup_fields` başka iş) | **yok** → `mk_prod_form` |
| "Telefon — [Kurumsal telefon numarası]" · CTA formatı | `mk_contact` | **kısmi** → §0 |
| "Öne Çıkan Görsel — 16:9 oranında, tercihen 1920x1080 px; .webp formatında" · "Resim Dosya Adı — anahtar-kelime-hizmet-adi.webp" | `mk_prod_fields` image ruleDetail, `image_format` WebP, `mk_visual_meta` filename | **kısmi** — ölçü ve dosya adı kalıbı yok (ruleDetail ile kapanır) |
| "Alternatif Metin … Görsel Başlık … Alt Yazı … Açıklama" | `mk_visual_meta` (alt, title, caption) | **kısmi** — "Açıklama" yok |
| "Video Başlık … Video Alt Yazı … Video Açıklaması" · "Podcast Bilgileri — Başlık, kısa açıklama, konuşmacı, süre, konu özeti, transkript ve CTA" | `video_seo` (07) | **kısmi** — boolean; içerik kuralı C olarak kural metnine |
| "Sayfa İçerik Dosyası — [MARKA]_[HIZMET_ADI]_Hizmet_Tanitim_Sayfasi_v01.docx" | `mk_blog_output` (yalnız blog) | **yok** → `mk_prod_output` |
| "Onay Durumu — Taslak / Revizyonda / İçerik Onayı / Teknik Onay / Yayına Hazır." | `mk_flow` | **kısmi** → değişiklik 1.4-11 |
| "Revizyon — v01, v02, v03, final" | yok | **yok** → `mk_naming` (1.3-e) |
| "FAQ Alanı — SEO uyumlu, akordiyon formatına uygun" | `faq_required` (04) | **tam** |
| "Güven Unsurları — Referanslar, sertifikalar, rakamlar, case study ve uzmanlık göstergeleri görünür olmalıdır." | `social_proof` (04) | **kısmi** — referans / yorum var; sertifika, rakam, vaka modülleri `mk_prod_fields`'e |
| "Service Schema … FAQ Schema … Organization / LocalBusiness … Breadcrumb" | `schema_types` | **tam** |
| "İç Linkleme — Ana hizmet, alt hizmet, kategori, blog ve ilgili hizmet sayfalarına doğal link" · "İlgili Bloglar — 3-6 blog" | `internal_links`, `mk_prod_links` | **tam** (sayı C) |
| "UTM — Kampanya veya reklamdan gelen trafik için CTA linklerinde UTM standardı uygulanmalıdır." | `mk_utm` | **tam** |
| "Okuma Akışı — F/Z paternine uygun" | yok | → `reading_pattern` (2.3) |
| "Dil — Kurumsal, güven veren, sade" | `brand_tone`, `brand_address` | **tam** |
| "Sayfa Adresi — [https://siteadi.com.tr/konu-basligi]" | `oc_services` ("Ad \| sayfa adresi") | **tam** (sayfa adresi listesi ortak bilgide) |

### 3.3 Yeni alan önerileri (`mk_prod` (51), hepsi `showIf: mk_prod_on = true`)

| Kimlik | Tip | Etiket | Seçenekler |
|---|---|---|---|
| `mk_prod_pages` | multiselect | Sayfa Türleri | Standart hizmet detay sayfası=standard (önerilen) · Kısa hizmet sayfası=short · İş birliği ana sayfası=partners · İş ortaklığı detay sayfası=partner_detail |
| `mk_prod_cta` | multiselect | CTA Yerleşimi | İlk ekran (hero)=hero (önerilen) · Sayfa ortası (avantaj / kapsam sonrası)=mid (önerilen) · Sabit (sticky) buton=sticky · Sayfa sonu form ve telefon=final (önerilen) |
| `mk_prod_form` | multiselect | Teklif / İletişim Formu Alanları | Ad soyad=name · Şirket=company · Telefon=phone · E-posta=email · İlgilenilen hizmet=interest · Mesaj=message · KVKK onayı=kvkk (önerilen, zorunlu) |
| `mk_prod_output` | multiselect | Çıktı Biçimleri | Word (.docx)=docx · HTML=html · JSON (CMS'e aktarım)=json · Düz metin=text |

`mk_prod_pages`:
- standard — scenario: "Ana hizmetlerin anlatımı, SEO görünürlüğü ve lead toplama." example: Hero, anlatım, avantajlar, medya, referans, teknik kapsam, fiyat / paket, FAQ, CTA modüllü uzun sayfa (§2, §6).
- short — scenario: "Alt hizmet, kampanya veya hızlı karar gerektiren hizmetler." example: problem, çözüm, 3–5 avantaj, görsel, başarı rakamları, CTA, en çok 3 FAQ (§2, §7).
- partners — scenario: "Markanın iş birliği yaklaşımını ve tüm iş ortaklarını tanıtma." example: yaklaşım, ortak logoları / kartları, ortaklık türleri (teknoloji, entegrasyon, akademik / eğitim, istihdam), katkılar, "İş Ortağımız Olun" formu (isim, şirket, iş birliği alanı, mesaj) (§8).
- partner_detail — scenario: "Belirli bir iş ortağı veya entegrasyonu anlatma." example: "[Marka] & [Ortak] İş Ortaklığı" başlığı, ortak hizmet / entegrasyon, neden bu ortaklık, KPI destekli kazanımlar, ortaklık süreci (talep → analiz → özel çözüm → entegrasyon → kullanım), 3–5 FAQ (§9).
- Not: `cms_modules`'taki "İş Ortakları" modülüyle `recommend` bağı kurulabilir (partners / partner_detail seçilince CMS'te İş Ortakları önerilir).

`mk_prod_cta`:
- hero — scenario: her hizmet sayfası; "Sayfanın ilk ekranında ana aksiyon". example: H1 altında ana CTA butonu ve telefon (§11, §12 "Above the Fold — İlk ekranda H1, kısa fayda metni ve CTA görünmelidir").
- mid — scenario: uzun sayfalar. example: avantajlar veya teknik kapsam bloğundan sonra "karar destek CTA".
- sticky — scenario: mobil trafiği yüksek, telefonla satış yapan kurumlar. example: "Mobil ve masaüstünde görünür hızlı iletişim veya teklif butonu" ekranın altında sabit.
- final — scenario: her sayfa. example: "Sayfa sonunda form, telefon ve kısa yönlendirme metni".

`mk_prod_form` — her alan için scenario: B2B'de company + interest, B2C'de name + phone yeterli; kılavuz "Form UX — Alan sayısı minimum tutulmalı" der, varsayılan set kılavuzdaki 7 alan. example: sayfa sonu formunda seçilen alanlar ve ayrı KVKK onay kutusu; zorunlu / isteğe bağlı ayrımı etikette. kvkk — kural: aydınlatma bağlantısı form üstünde, pazarlama izni ayrı kutu (Reklam §16 ile aynı). `business_model` b2b → company, interest önerisi.

`mk_prod_output` — docx: içerik metni onaya Word ile gidiyorsa (Hizmet §16 ".docx"); html / json: CMS'e doğrudan aktarılacaksa; text: başka araçlara yapıştırılacaksa. example: her sayfa için seçilen biçimlerde dosya, adı `mk_naming`'e göre. (`mk_blog_output` ile aynı desen.)

### 3.4 Mevcut alanlarda değişiklik önerileri
1. **`mk_prod_fields`** — seçenek ekle: `process` "Nasıl çalışır (süreç adımları)" · `scope` "Teknik kapsam ve metodoloji" · `why_us` "Markanın ayrışan avantajları (Neden biz?)" · `certificates` "Sertifika ve belgeler" · `stats` "Öne çıkan rakamlar" · `cases` "Başarı hikâyeleri / vaka çalışması" · `media` "Video, ses ve görsel galeri" · `packages` "Paket karşılaştırması" · `download` "İndirilebilir içerik (broşür, rehber, kontrol listesi)" · `cta` "CTA alanları" · `toc` "İçindekiler (uzun sayfalarda)" · `related` "Diğer hizmetler". Kanıt: §6 modül tablosu 2–16, §4 "Table of Content — Uzun hizmet sayfalarında H2/H3 başlıklarına göre içindekiler", §14 şablonu ("Nasıl Çalışır?", "Teknik Kapsam", "Neden #Marka?"). ruleDetail önerileri: `benefits` "standart sayfada 3–6, kısa sayfada 3–5 avantaj"; `stats` / `certificates` / `cases` "yalnız doğrulanabilir veriyle" (mevcut `proof` kuralıyla aynı); `faq` "kısa sayfada en çok 3, ortaklık detayında 3–5 soru, akordiyon"; `summary` "40–60 kelime"; `image` "16:9, 1920×1080, WebP; dosya adı anahtar-kelime-hizmet-adi.webp; alt metin, başlık, alt yazı ve açıklama".
2. **`mk_prod_keywords`** — `set` / `main` ruleDetail'ine "odak kelime en çok 3 kelime; H1, giriş paragrafı, meta başlık, meta açıklama ve ilgili alt başlıklarda doğal geçer" (§4). Mevcut "H1, title, açıklama ve özette geçer" → "giriş" ve "alt başlık" eksik.
3. **`mk_visual_meta`** — seçenek ekle: `description` "Açıklama" (§5 "Açıklama — Görselin hizmet anlatımına nasıl destek verdiğini açıklayan kısa metin").
4. **`mk_flow`** — `staged` seçeneği (1.4-11 ile aynı).
5. **`faq_required` (04) / `schema_types` FAQPage** — rehbere not: Google FAQ zengin sonucu 7 Mayıs 2026'da kalktı (proje CLAUDE.md, SEO Denetimi notu); kılavuz "FAQPage schema ile desteklenebilir" diyor — işaretleme zararsız ama zengin sonuç beklentisi yazılmamalı.
6. **SEO ölçüleri** — `seo_level` rule'unda ve `mk_blog_fieldset` rule'unda "meta başlık ve meta açıklama SEO / Semantik bölümündeki standarda göre yazılır" deniyor, ama SEO bölümünde sayısal ölçü yok. Kılavuzun ölçüleri (title 35–60 karakter / 285–580 px, description 120–160 / 680–920 px, slug ≤ 75 ideal 30–60, H başlık ≤ 64, tek H1) `seo_level` Advanced / Standard ruleDetail'ine eklenmeli (C sınıfı — seçim değil, standart metni). Blog kılavuzu bulgusunda farklı aralık varsa ikisi uzlaştırılmalı.

### 3.5 B sınıfı brief alanları
Hizmet / ürün adı · sayfa türü (sayfa başına) · sayfa adresi · odak anahtar kelime · hedef kitle (persona, karar verici, sektör, ölçek — sayfa başına) · kullanıcı problemi · hizmetin ana faydası · sayfa CTA'sı ve CTA linki · kaynaklar (mevzuat, rapor, kurum duyurusu, iç doküman) · H1, kısa tanıtım, meta title / description, özet · avantajlar, teknik kapsam, süreç adımları, paketler · referanslar, rakamlar, sertifikalar, vaka özetleri · FAQ soru-cevapları · görsel / video / podcast meta metinleri · ilgili blog ve diğer hizmet bağlantıları · ortaklık sayfasında ortak adı, başlangıç tarihi, entegre sistemler, kazanımlar.

### 3.6 C sınıfı ilkeler
1. Sayfada tek H1; hizmet adını ve odak kelimeyi içerir; H2 ana bölümler, H3–H4 alt açıklama, FAQ ve kapsam (§10).
2. Paragraflar 40–70 kelime, H başlıkları ≤ 64 karakter; avantaj, süreç, kapsam ve paketler madde ya da tabloyla (§10).
3. Teknik terim ilk kullanımda parantez içinde açıklanır; kısaltmanın ilk kullanımında açık hali yazılır (§10).
4. İlk ekranda H1, kısa fayda metni ve CTA görünür; CTA yalnız sonda değil karar noktalarında da yer alır (§11, §12).
5. Slug küçük harf, tireli, Türkçe ve özel karaktersiz, ≤ 75 (ideal 30–60) karakter; meta title 35–60, description 120–160 karakter (§4).
6. Görseller WebP ve optimize, video gömmeleri sayfa hızını düşürmez; alt metin, kontrast, klavye ve form etiketleri denetlenir (§12).
7. Breadcrumb hem görünür hero'da hem yapısal veride; Service, Organization / LocalBusiness, gerekiyorsa FAQPage işaretlemesi (§13).
8. Hizmeti destekleyen 3–6 blog yazısı kart olarak listelenir; ana / alt hizmet ve kategori sayfalarına doğal iç bağlantı (§13).
9. Yayın öncesi 15 maddelik checklist; yayın sonrası mobil / masaüstü görünüm, form gönderimi, CTA linkleri, görsel yükleme ve meta alanları kontrol edilir (§13, §15).
10. Video ve podcast için başlık, kısa açıklama, transkript ve CTA hazırlanır (§5).

---

## 4. Toplu öneri listesi (kısa)

**Yeni bölümler**
- `oc_cta` "Eylem Çağrısı (CTA)" (Ortak Bilgiler): `oc_cta_phone` text · `oc_cta_parts` multiselect (link, phone, whatsapp, email) · `oc_cta_verbs` multiselect (quote, info, consult, demo, register, download, contact, apply, whatsapp, dm) · `oc_cta_primary` select (aynı değerler).
- `mk_li` "LinkedIn Ads" (Reklam; showIf mk_ads_channels ∋ linkedin): `mk_li_formats` (single_image, video, carousel, document, lead_form, event, message, text_dynamic) · `mk_li_message` (risk, efficiency, compliance, reporting, speed, control) · `mk_li_form` (min_fields, consent, privacy, thanks) · `mk_li_insight` boolean · `mk_li_budget` text.
- `mk_tt` "TikTok Ads" (Reklam; showIf mk_ads_channels ∋ tiktok): `mk_tt_formats` (in_feed, spark, carousel, lead, search_smart) · `mk_tt_spark` select (own, creators) · `mk_tt_pixel` boolean · `mk_tt_budget` text.

**Mevcut bölümlere yeni alanlar**
- `mk_ads`: `mk_ads_variants` select (three, two, one) · `mk_ads_tests` multiselect (headline, visual, hook, cta, landing, audience) · `mk_ads_video` multiselect (subtitles, hook, brand5, end_cta, cover).
- `mk_gads`: `mk_gads_yt` multiselect (skippable, non_skippable, bumper, infeed, shorts).
- `mk_measure`: `mk_ads_kpis` multiselect (impressions, reach, ctr, cpc, cpm, cvr, cpa, roas, lead_quality, frequency).
- `mk_creative`: `mk_naming` select (structured, short, free) · `mk_fz` boolean · `mk_logo_place` select (top_left, top_band, brief).
- `mk_prod`: `mk_prod_pages` multiselect (standard, short, partners, partner_detail) · `mk_prod_cta` multiselect (hero, mid, sticky, final) · `mk_prod_form` multiselect (name, company, phone, email, interest, message, kvkk) · `mk_prod_output` multiselect (docx, html, json, text).
- `design_approach` (03): `reading_pattern` boolean.

**Mevcut alan değişiklikleri**
- `mk_ads_channels` + microsoft, x, pinterest, programmatic; linkedin/tiktok ruleDetail; `recommend` mk_goals + business_model. `mk_ads_landing` / `mk_ads_claims` showIf listeleri yeni kanallarla güncellenmeli.
- `mk_gads_types` + app; search "8–15 başlık"; demand_gen / pmax ruleDetail.
- `mk_gads_assets` + location, lead_form, snippet. `call` ruleDetail korunur (Google telefonu metinde kabul etmez — kılavuzla çelişki, platform kuralı önde).
- `mk_meta_creative` + v45, collection; carousel 2–10 (IG 3–8).
- `mk_utm` + ads_full (5 parametreli reklam şeması).
- `mk_conversions` + event_register. `mk_measure_scope` + linkedin, tiktok, crm.
- `mk_flow` + staged (Taslak → Revizyon → İçerik onayı → Teknik onay → Yayına hazır); `mk_approvers` + technical, media, expert (showIf'e staged); `mk_roles` + web.
- `mk_banned` + unverified_stats; client_logo ve copyright etiketleri genişler. `mk_legal_scope` regulated etiketi genişler.
- `mk_hashtags` + per_platform (LinkedIn 3–6 · Instagram 5–10 · X 2–4 · TikTok 3–6) — rule'daki "X'te en çok 2" ile çelişki.
- `mk_formats` T: "en çok 12 kelime" ↔ F-Z "25–35 kelime" çelişkisi; Z / F ayrımı.
- `mk_prod_fields` + process, scope, why_us, certificates, stats, cases, media, packages, download, cta, toc, related; sayı aralıkları ruleDetail'e.
- `mk_prod_keywords` ruleDetail: odak kelime ≤ 3 kelime, giriş ve alt başlıklar.
- `mk_visual_meta` + description.
- `brand_icons` Outline "(önerilen)".
- `seo_level` ruleDetail: meta / slug / başlık ölçüleri (C; blog bulgusuyla uzlaştır).
