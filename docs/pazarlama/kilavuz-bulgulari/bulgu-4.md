# Bulgu 4 — Video (kısa), Uzun Formatlı Video, Podcast

Okunan dosyalar (tamamı, satır satır): `Video_Olusturma_Kilavuzu_Kurumsal.txt` (599 satır, 24 bölüm), `Uzun_Formatli_Video_Olusturma_Kilavuzu_Kurumsal.txt` (499 satır, 18 bölüm + kaynak notu), `Podcast_Olusturma_Kilavuzu_Kurumsal.txt` (416 satır, 22 bölüm). Envanter: `alan-envanteri.md` (00–82, tamamı). Ayrıca DATA'dan şu alanların seçenek metinleri okundu: `video_seo`, `mk_formats`, `mk_platforms`, `mk_caption`, `mk_visual_meta`, `mk_visual_source`, `mk_banned`, `mk_brief_format`, `mk_roles`, `mk_ai_content`, `image_format`, `marketingTemplate.formatlar` / `mecralar`.

Önemli bulgu (mevcut durum): `mk_formats` içindeki **V "Uzun video"** seçeneğinin `ruleDetail`'i boş; `marketingTemplate.formatlar`'da yalnız R, C, T, S var (V ve M yok). Yani uzun video bugün planda yalnız bir etiket; ölçü, süre, altyazı, teslim kuralı üretilmiyor. Podcast için formda hiçbir şey yok (`mk_accounts` yer tutucusundaki "Spotify | …" örneği dışında).

---

## 0. Karar: Video için tek bölüm mü, iki bölüm mü?

**Öneri: tek bölüm — "Video Üretimi" (`mk_video`, grup İçerik, `mk_creative`'ten hemen sonra). Podcast ayrı bölüm — "Podcast" (`mk_podcast`, grup Kanallar, `mk_mail`'den sonra).**

Gerekçe:
1. İki video kılavuzunun ortak standartları aynı: altyazı / SRT, seslendirme, logo–intro–outro–alt bant, güvenli alan, müzik lisansı, yapay zekâ video kuralı, export (MP4/H.264/AAC 48 kHz), dosya adlandırma, çok aşamalı onay. Ayrı bölüm açılırsa ~10 alanın 7'si iki kez sorulur ve iki bölümde farklı cevap verilip çelişki çıkabilir.
2. Uzun formatlı kılavuzun kendisi tek dokümanda iki sürümü yönetiyor: "Versiyon Yapısı — Kısa versiyon ve uzun versiyon olmak üzere iki ayrı üretim standardı içerir." Kısa video kılavuzunun karar matrisi de 15–60 dk webinar'ı kapsıyor ("Webinar / Canlı Yayın Kaydı 16:9 yatay 15-60 dk"). Yani kılavuzların kendi ayrımı "video türü"dür, "bölüm" değil.
3. Kısa ile uzun arasındaki gerçek farklar (süre, bölümleme, storyboard yoğunluğu, bölüm zaman kodları, ara özet) tür seçeneklerinin `ruleDetail`'i ve bir "Senaryo ve Storyboard Çıktısı" kararıyla karşılanabiliyor; ayrı bölüm gerektirmiyor.
4. Kısa sosyal videonun **mecraya özgü** kuralları (Reels 1080×1920, kanca, UI alanları, paylaşım metni, etiket) zaten `mk_social` › `mk_formats` R'de. `mk_video` bunları tekrar etmez; **üretim** standardını (senaryo, ses, altyazı, marka öğeleri, teslim, onay) verir. Sınır: "nerede ve hangi metinle paylaşılır" → `mk_social`; "nasıl üretilir ve teslim edilir" → `mk_video`.
5. Podcast ayrı bir kanal: kendi dağıtım altyapısı (RSS → Spotify / Apple Podcasts), kendi seri kimliği (seri adı, açıklama, kategori, kapak), kendi yayın ritmi ve ses-teknik standardı var. `mk_mail` / `mk_events` gibi kendi açma boolean'ıyla Kanallar grubunda durmalı.

---

## 1. VİDEO OLUŞTURMA KILAVUZU (kısa / genel video)

### 1.1 Özet
- **Amaç:** "strateji, senaryo, storyboard, çekim, yapay zekâ video üretimi, seslendirme, altyazı, kurgu, teknik export ve kalite kontrol süreçlerini standartlaştırmak"; çıktı "marka kimliğine uygun, teknik olarak doğru, platforma uyumlu, erişilebilir ve yayınlanabilir".
- **Ana bölümler (sırayla):** 1 Amaç ve kapsam (6 video türü) · 2 Video türü karar matrisi · 3 Platform teknik standartları + YouTube SDR bitrate tablosu · 4 Video genel bilgileri formu · 5 Strateji ve senaryo standardı (akış + metin kuralları) · 6 Bölüm / Part / Sahne yapısı · 7 Sahne kartı şablonu · 8 Görsel anlatım · 9 Kamera, lens, kadraj · 10 Işık ve renk · 11 Güvenli alan, logo, alt bant, ekran yazısı · 12 Kapak görseli · 13 AI video üretim standardı + negatif prompt · 14 Seslendirme + ElevenLabs prompt örneği · 15 SRT ve altyazı · 16 Storyboard kartı · 17 Post-prodüksiyon · 18 Export, teslim, dosya isimlendirme · 19 Video SEO ve metadata · 20 Kalite kontrol listesi · 21 Revizyon ve final onay · 22 Revizyon takip tablosu · 23 Kullanılmaması gerekenler · 24 Kaynaklar.
- **Sayısal standartlar:**
  - Türler: sosyal 9:16 15–59 sn; genel tanıtım 16:9 60–299 sn; eğitim/LMS 16:9 30–180 sn/modül; ürün/hizmet 9:16 veya 16:9 30–90 sn; webinar 16:9 15–60 dk; AI sahnesi 3–8 sn/sahne.
  - Senaryo akışı: Hook 0–3 sn · Problem 3–10 sn · İçgörü 10–20 sn · Çözüm 20–35 sn · Fayda/Kanıt 35–45 sn · CTA son 3–8 sn.
  - Başlık en çok 6 kelime (Video SEO'da "4-6 kelime"), kısa video açıklaması "en fazla 20 kelimelik özetle başlayabilir", kapak sloganı en çok 6 kelime.
  - Platform: YouTube MP4/H.264/AAC-LC–Opus/48 kHz, 1920×1080 veya 3840×2160 master; Shorts / Reels 1080×1920; LinkedIn organik 3 sn–10 dk, 75 KB–5 GB, 10–60 FPS; LinkedIn reklam 3 sn–30 dk, 30 FPS önerilir, "15-30 sn arası reklam versiyonu ayrıca hazırlanmalıdır"; TikTok min 540×960, ≤500 MB, ≥516 kbps, 10 dk'ya kadar; X kısa sürüm 30–60 sn; LMS MP4/H.264/1920×1080/25-30-60 FPS/AAC. YouTube bitrate: 1080p 8 / 12 Mbps, 4K 35–45 / 53–68 Mbps vb.
  - Güvenli alan: kenarlardan en az %5; alt %20 altyazı alanı; intro en çok 2–3 sn.
  - Seslendirme: Türkçe 2,2–2,6 kelime/sn; WAV önerilir.
  - Altyazı: satır 35–42 karakter, en çok 1–2 satır, blok 1–5 sn, `.srt`.
  - Export: final MP4/H.264; sosyal kesit 9:16 1080×1920 altyazılı + kapak; yatay 16:9 1920×1080/3840×2160; kare 1:1 1080×1080; feed 4:5 1080×1350.
  - Sahne numarası X.Y.Z.W (Video.Bölüm.Part.Sahne); dosya adı `VideoX_BolumY_PartZ_SahneW_V1.mp4`, final `VideoX_Final_TR_16x9_V1.mp4`.
- **Süreç (onay, §21):** Brief onayı (Pazarlama / İş sahibi) → Senaryo onayı (İçerik ekibi) → Storyboard onayı (Tasarım / Prodüksiyon) → Ses onayı (İçerik / Marka) → Kurgu ilk taslak (Video editör) → Teknik kontrol (Video / Dijital ekip) → Hukuki / uzman kontrol (İlgili danışman) → Final onay (İş sahibi / Marka). Revizyon takibi: V1/V2/V3/Final, tarih, talep eden, alan (metin / görsel / ses / müzik / altyazı / storyboard / prompt / export), durum.
- **Uyum maddeleri:** "Hukuki, teknik, KVKK, İSG, SGK, vergi veya mevzuat içeriğinde yanlış yönlendirme var mı?"; "hukuki/finansal kesin sonuç vaadinden kaçınılmalıdır"; "Lisanslı, telif problemi olmayan … fon müziği"; "Abartılı vaat, doğrulanmamış rakam, korku pazarlaması … kullanılmamalıdır"; AI içinde logo / metin üretmeme.

### 1.2 A sınıfı bilgiler — mevcut karşılık
| # | Kılavuzdan alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|---|
| 1 | "Sosyal Medya Videosu 9:16 dikey 15-59 sn … Genel Tanıtım Videosu 16:9 yatay 60-299 sn … Eğitim / LMS Videosu … Ürün / Hizmet Videosu … Webinar / Canlı Yayın Kaydı 16:9 yatay 15-60 dk" | `mk_formats` (R, V) | **Kısmi** — yalnız "Reels / kısa video" ve "Uzun video" var; tanıtım, ürün, eğitim, webinar, motion ayrımı ve süreleri yok; V'nin kuralı boş. |
| 2 | "Platforma göre 9:16, 16:9, 1:1 ve 4:5 varyasyonları hazırlanır." / "Sosyal Kesit 9:16 … Kare Versiyon 1:1 … Feed Dikey 4:5" | `mk_meta_creative` (yalnız Meta reklamı) | **Kısmi** — organik video teslim paketinde hangi sürümlerin hazırlanacağı yok. |
| 3 | "1920x1080 veya 3840x2160 master üretin." / "Master Video Proje ihtiyacına göre ProRes veya yüksek bitrate MP4" | yok | **Yok** |
| 4 | "Konuşma metni … tek anlatıcı, uzman anlatımı veya diyalog formatında hazırlanabilir." / "Ses Türü Kadın / erkek / genç / orta yaş / olgun / kurumsal lider tonu" / "Ses Tonu Kurumsal, sakin, anlaşılır, güven veren" | `brand_tone` (01) yalnız yazılı ses tonu | **Kısmi** — seslendirme kaynağı (uzman / profesyonel / AI) ve marka sesi profili yok. |
| 5 | "Telaffuz KVKK, GDPR, SGK, İSG gibi kısaltmaların okunuşu belirtilmelidir." | yok | **Yok** (kurum özelindeki kısaltma ve ürün adlarının okunuşu; Ortak Bilgiler'e uygun) |
| 6 | "Üretim Araçları Kling, Google Veo, Runway, Seedance …" / "AI video içinde okunabilir metin, logo veya marka işareti ürettirilmemelidir." | `mk_visual_source` ai (etiket kuralı) | **Kısmi** — video sahnelerinde yapay zekâ kullanılıp kullanılmayacağı ve kapsamı (B-roll / tamamı) yok; AI video kuralları yok. |
| 7 | "SRT Dili Türkçe veya hedef yayın dili" / "Transkript Erişilebilirlik ve SEO için konuşma metni veya transkript hazırlanmalıdır." | `video_seo` (07, yalnız sitedeki video), `mk_formats` R ruleDetail ("altyazı zorunludur") | **Kısmi** — sosyal kısa video dışındaki videolar için altyazı politikası, SRT dosyası, gömülü sürüm, çok dilli altyazı yok. |
| 8 | "Logo Alanı Sağ üst veya sol üst güvenli alan" / "Intro Maksimum 2-3 saniye" / "Outro CTA, web adresi, telefon ve logo ile tamamlanır." / "Alt Bant Konuşmacı adı, görev, bölüm başlığı" | `brand_logo_rules` (01, genel logo kuralı) | **Kısmi** — videoya özgü marka öğeleri (intro, outro, alt bant, köşe logosu) yok. |
| 9 | "Kapak Görseli JPG / PNG / WEBP, platform boyutuna göre" / "Kapak Sloganı … maksimum 6 kelimelik" | `video_seo` (site), `mk_blog_cover` (yalnız blog) | **Kısmi** — video kapağı teslim kuralı yok. |
| 10 | "Uzun YouTube videolarında 00:00 formatında bölüm zamanları eklenmelidir." | `video_seo` example ("dakika işaretli bölümler") | **Kısmi** — yalnız site videosunda, sosyal/YouTube planında yok. |
| 11 | "Brief Onayı … Senaryo Onayı … Storyboard Onayı … Ses Onayı … Kurgu İlk Taslak … Teknik Kontrol … Hukuki / Uzman Kontrol … Final Onay" | `mk_flow` (Taslak → [Hukuk] → Onay → Yayın), `mk_approvers` | **Kısmi** — video üretimine özgü ara onay aşamaları yok. |
| 12 | "Abartılı vaat, doğrulanmamış rakam, korku pazarlaması veya hukuki/finansal kesin sonuç vaadi kullanılmamalıdır." | `mk_banned` (superlative, price_claim) | **Kısmi** — "korku pazarlaması" ve "kesin sonuç vaadi" seçeneği yok. |
| 13 | "Müzik Lisanslı, telif problemi olmayan, marka tonuna uygun fon müziği kullanılır." | `mk_banned` copyright | **Tam** (telif yasağı); markaya özel müzik/jingle kararı yeni alanda seçenek olarak. |
| 14 | "Video Dili Türkçe veya hedef pazara göre farklı dil" | `mk_languages` (78) | **Tam** |
| 15 | "Platform Kullanımı LMS / Web / YouTube / Instagram / LinkedIn / TikTok / WhatsApp / X" | `mk_platforms`, `module_lms` | **Tam** (web/LMS proje kararlarından) |
| 16 | "CTA [CTA metni] \| [CTA linki] \| Telefon: [telefon]" | `mk_contact`, `domain_name` | **Tam** (telefon ve adres Ortak Bilgiler'den; biçim C) |
| 17 | "Video Dosyası VideoX_BolumY_PartZ_SahneW_V1.mp4" | `mk_brief_format` full ruleDetail (`Marka_BriefNo_FORMAT_YAYINTARİHİ_v01`) | **Kısmi / çelişki** — bkz. §5 madde 11. |

### 1.3 B sınıfı brief alanları (form alanı değil)
Video numarası / kampanya kodu, video başlığı, video amacı, hedef kitle (persona), video türü (bu video için), ana mesaj, konuşma metni, toplam süre hesabı (kelime, okuma, ön/son boşluk), bu videonun formatı (9:16 / 16:9 / 1:1 / 4:5), görsel dil (bu video için: "Kurumsal, modern, gerçekçi …"), platform kullanımı, CTA metni ve linki, teslim formatı (bu video için); bölüm / part / sahne kartları (no, başlık, amaç, konuşma metni, süre, sahne türü, duygu, ana mesaj, teknik hassasiyet, karakter devamlılığı); storyboard kartı (frame no, kare açıklaması, kamera açısı / hareketi, kompozisyon, ekran yazısı, seslendirme, süre, geçiş, grafik notu, post-prodüksiyon notu, onay durumu); kamera / lens / ışık seçimleri; master prompt, sahne promptları, referans görseller; kapak sloganı ve görsel konsept; video SEO başlığı, açıklaması, etiketler, bölüm zamanları; revizyon kaydı (versiyon, tarih, talep eden, açıklama, alan, durum); hazırlayan / kontrol eden / onaylayan / tarih.

### 1.4 C sınıfı ilkeler (en fazla 10)
1. İlk 3 saniyede kanca; akış Hook (0–3 sn) → Problem (3–10) → İçgörü (10–20) → Çözüm (20–35) → Fayda/Kanıt (35–45) → CTA (son 3–8 sn).
2. Her sahne tek ana mesaj taşır ("Her sahnede birden fazla ana mesaj verilmemelidir"); seslendirme hızı Türkçe 2,2–2,6 kelime/sn; süre kelime + okuma + ön/son boşlukla hesaplanır.
3. Altyazı: satır 35–42 karakter, en çok 2 satır, blok 1–5 sn, konuşmadan önce görünmez, cümle anlam bütünlüğüyle bölünür, UI bindirmeleriyle çakışmaz.
4. Güvenli alan: kenarlardan en az %5; alt %20 altyazı; TikTok'ta "altyazılar sağ ve alt UI alanlarından uzak"; CTA, yüz, logo, altyazı merkez güvenli alanda.
5. AI video: okunabilir metin, logo, rastgele sembol ürettirilmez; ekran yazısı, logo, alt bant, CTA ve altyazı post-prodüksiyonda eklenir; master prompt + sahne promptu + negatif prompt standardı; karakter ve kamera sabitleme; prompt dili araç performansına göre (Kling, Veo, Runway, Seedance için İngilizce tercih edilebilir).
6. Teknik: MP4 / H.264 / AAC 48 kHz; "Kare hızı çekilen kare hızıyla aynı olmalıdır"; bitrate YouTube SDR tablosuna göre.
7. Ses: dip ses, yankı, patlama, clipping yok; müzik anlatımı bastırmaz; ses efekti düşük yoğunlukta; tüm sahnelerde aynı LUT / renk düzenleme ve aynı beyaz dengesi.
8. Video SEO metadata: başlık anahtar kelimeyle başlar, 4–6 kelime; açıklama özetle başlar, CTA ve linkle biter; uzun YouTube videosunda 00:00 bölüm zamanları; transkript hazırlanır.
9. Teknik terimler anlaşılır açıklanır; hukuki / finansal kesin sonuç vaadi, doğrulanmamış rakam ve korku pazarlaması kullanılmaz; mevzuat içeriği uzman kontrolünden geçer.
10. Kaçınılacak görseller: kalabalık arka plan, okunamayan ekran, abartılı mimik, fake logo, watermark, karikatürize stil, bozuk yüz/el, titrek kamera.

---

## 2. UZUN FORMATLI VİDEO OLUŞTURMA KILAVUZU

### 2.1 Özet
- **Amaç:** "uzun formatlı video içeriklerinin strateji, senaryo, bölümleme, storyboard, çekim, kurgu, export, yayın ve kalite kontrol süreçlerini standartlaştırmak"; kapsam "5 dakikanın üzerindeki eğitim, tanıtım, uzman görüşü, belgesel, webinar, panel, LMS dersi, ürün/hizmet demo ve YouTube/Vimeo/Web yayınlı kurumsal videolar".
- **Ana bölümler (sırayla):** 1 Amaç ve kapsam · 2 Kullanım senaryoları ve video türleri (eğitim, bilgilendirme, reklam/tanıtım, belgesel/hikâye, webinar/panel) · 3 Kısa ve uzun versiyon karar matrisi · 4 Prodüksiyon öncesi bilgi toplama (zorunlu alanlar) · 5 Hiyerarşi: Bölüm, Konu, Sahne, Storyboard · 6 Kısa versiyon standardı · 7 Uzun versiyon standardı · 8 Senaryo, konuşma metni, anlatım · 9 Storyboard ve sahne planı · 10 Teknik format ve export · 11 Görsel tasarım, marka, ekran yerleşimi · 12 Kamera, ışık, ses, çekim · 13 Kurgu, altyazı, erişilebilirlik · 14 Platform bazlı yayın (öncesi + sonrası kontrol) · 15 Dosya isimlendirme, klasör, versiyonlama · 16 Kalite kontrol, onay, revizyon · 17 Kopyalanabilir brief şablonları (kısa + uzun) · 18 Final checklist · Kaynak notu.
- **Sayısal standartlar:**
  - Kısa sürüm 5–12 dk (Giriş + 2–4 ana bölüm + kapanış); uzun sürüm 12–45+ dk (giriş + çoklu bölüm + konu blokları + özetler + kapanış).
  - Hiyerarşi: Video X.0 · Bölüm X.Y (kısa 1–4 dk / uzun 3–8 dk) · Konu X.Y.Z (30 sn–3 dk) · Sahne X.Y.Z.W (8–20 sn; eğitimde 8 sn) · Storyboard X.Y.Z.W.N (2–5 sn; detaylı üretimde 2 sn).
  - Kısa sürüm akışı: Giriş/Hook 20–45 sn ("İlk 5 saniyede konu netleşmeli"), Ana bölüm 1 ve 2 1–3 dk, Kanıt/Örnek 1–2 dk, Kapanış/CTA 20–45 sn; "15-30 sn sosyal medya kesitleri üretilebilir".
  - Uzun sürüm: Açılış 45–90 sn, Bölüm girişi 15–30 sn, Ana anlatım blokları 3–8 dk ("Her 2-4 dakikada görsel değişim"), Ara özet 20–40 sn (2–3 madde), Uygulama/Vaka 2–6 dk, Final özet ve CTA 45–90 sn.
  - Metin: cümle ≤6 kelime (istisna 9); 8 sn sahnede 16–18 kelime (en çok 20); 6 kelimelik cümle normal 2,5 sn / rahat 3 sn / vurgulu 3,5–4 sn.
  - Teknik: master MOV/MP4 4K/1080p yüksek bitrate, "altyazısız ve altyazılı iki çıktı"; Web/LMS MP4 H.264 1920×1080 25/30 fps AAC 48 kHz; Vimeo kare piksel 1:1; LinkedIn 3 sn–30 dk, 360–1920 px; sosyal kesit 9:16 1080×1920 15–60 sn; minimum 1920×1080; arşivde ProRes/DNxHR; thumbnail YouTube 1280×720.
  - Ekran: kenarlardan en az %5; bölüm başlık kartı 3–6 kelime; kurgu ritmi 20–40 sn'de görsel destek veya kadraj değişimi.
  - Çekim: 4K çekim önerilir; lens konuşma 35–50 mm, portre 50–85 mm, mekân 24–35 mm; yaka veya shotgun mikrofon; ekran kaydı min 1080p.
- **Süreç:** prodüksiyon öncesi zorunlu bilgi ("Eksik alanlar “[Netleştirilmeli]” olarak işaretlenmeli; kritik bilgi eksikse üretime başlanmamalıdır") → senaryo onayı (İçerik sahibi / Pazarlama) → storyboard onayı (Pazarlama / Tasarım / Video editör) → ham çekim kontrolü (Video ekibi) → ilk kurgu (Pazarlama / İçerik sahibi) → final kurgu (Pazarlama / Yayın sorumlusu) → yayın sonrası (Pazarlama / Raporlama: analytics, yorum, CTA tıklaması, kesit önerileri).
- **Uyum:** senaryoda "hukuki hassasiyet kontrol edilir"; ham çekimde "veri gizliliği"; ekran kaydında "kişisel/veri gizliliği kontrol edilmeli"; "Önceden kaydedilmiş sesli video içeriklerinde senkronize altyazı sağlanmalıdır" (WCAG'a atıf); "Platform teknik gereklilikleri yayın tarihinden önce güncel resmi kaynaklardan tekrar kontrol edilmelidir."

### 2.2 A sınıfı bilgiler — mevcut karşılık
| # | Kılavuzdan alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|---|
| 1 | "Kısa Versiyon 5-12 dakika … Uzun Versiyon 12-45+ dakika" | `mk_formats` V "Uzun video" | **Kısmi** — sürüm ayrımı ve süre aralığı yok; V'nin kuralı boş, şablonda V formatı tanımsız. |
| 2 | "Kurumsal Eğitim … Bilgilendirme … Reklam / Tanıtım … Belgesel / Hikaye Anlatımı … Webinar / Panel Kaydı" | `mk_formats` V; `mk_evt_after` recording_share (webinar kaydı paylaşımı) | **Kısmi** — tür seçimi yok. |
| 3 | "Storyboard Yoğunluğu — Daha sade; kritik sahnelerde detaylı storyboard. / Her bölüm/konu/sahne için ayrıntılı storyboard ve prodüksiyon notu." | `mk_brief_format` (tasarım brief'i) | **Kısmi** — video senaryosunun hangi derinlikte (sahne kartı / storyboard) üretileceği kararı yok. Claude'un video çıktısını doğrudan değiştirir. |
| 4 | "Master Arşiv MOV veya MP4; 4K/1080p; yüksek bitrate; temiz ses; altyazısız ve altyazılı iki çıktı." | yok | **Yok** |
| 5 | "Altyazı SRT ve gömülü altyazılı versiyon hazırlanmalıdır." | `video_seo` (site) | **Kısmi** (bkz. 1.2 #7) |
| 6 | "Logo Intro/outroda net; video içinde tercihen sağ üst veya alt bantta düşük yoğunluklu kullanılır." / "CTA Ekranı … web sitesi, telefon ve varsa QR/link" / "Başlık Kartı Bölüm girişlerinde 3-6 kelimelik başlık" | `brand_logo_rules` | **Kısmi** (bkz. 1.2 #8) |
| 7 | "Thumbnail YouTube için 1280x720, yüksek kontrast, kısa başlık" | yok | **Yok** (teslim paketinde) |
| 8 | "Ana videodan 15-60 sn dikey/karesel teaser çıkarılır." | `mk_derive` (blogdan türetme) | **Kısmi** — videodan sosyal kesit türetme yok. |
| 9 | "YouTube … İzlenme süresi, CTR, izleyici tutma … LMS / Akademi … Tamamlama oranı … izleme bırakma noktası" | `mk_measure_scope` (social, post, followers, blog, gads, meta) | **Kısmi** — video metrikleri yok. |
| 10 | "Final onay ve yayın sonrası raporlama sorumlusu belirlendi mi?" / onay sahipleri "Pazarlama / Tasarım / Video editör … Yayın sorumlusu … Raporlama" | `mk_roles` (video = "Video editörü"), `mk_flow` | **Kısmi** — `video` rolünün senaryosu yalnız kısa video; prodüksiyon (çekim / ses) rolü yok. |
| 11 | "Final Export marka_konu_platform_sure_v01.mp4" / "Altyazı marka_konu_tr_srt_v01.srt" | `mk_brief_format` adlandırması | **Kısmi / çelişki** — bkz. §5 madde 11. |

### 2.3 B sınıfı brief alanları
Marka / şirket (bu video için), video başlığı, hedef kitle, video türü, ana mesaj, toplam süre ve esneklik aralığı, platform, kaynak metin (blog, sunum, mevzuat, ürün dokümanı, röportaj notu), CTA; bölüm sayısı, konu başlıkları, sahne listesi, storyboard satırları (no, süre, konuşma metni, görsel, kamera, lens, ışık, renk, müzik/ses, amaç); konuşmacı / anlatıcı (ad, unvan, rol); görsel kaynaklar (B-roll, ekran kaydı, grafik, arşiv); teknik çıktılar listesi (bu video için); final checklist cevapları.

### 2.4 C sınıfı ilkeler (en fazla 10)
1. Hiyerarşi Video > Bölüm > Konu > Sahne > Storyboard; her seviye kendi süresi, başlığı ve mesajıyla; numaralama X.Y.Z.W.N.
2. Cümle en çok 6 kelime (istisna 9); 8 sn sahnede 16–18, en çok 20 kelime.
3. Uzun sürümde her ana bölümden önce 15–30 sn giriş, bölüm sonlarında 20–40 sn ara özet (2–3 madde), her 2–4 dk görsel değişim; konuşma 20–40 sn'den uzun desteksiz kalmaz.
4. Kapanış her zaman özet + CTA + iletişim bilgisi (web, telefon; varsa QR) birlikte; CTA görsel olarak da verilir.
5. Kısa sürümde her bölüm tek ana fikir; görsel yoğunluk yüksek, metin yoğunluğu düşük; karmaşık veride tablo yerine infografik.
6. Çekim ve export aynı fps (25 veya 30); minimum 1920×1080; master yüksek kaliteyle saklanır, platform kopyaları ayrı export edilir.
7. Prodüksiyon öncesi zorunlu bilgi eksikse "[Netleştirilmeli]" yazılır; kritik bilgi eksikse üretime başlanmaz.
8. Ekran kaydında imleç görünür, kişisel ve gizli veri gösterilmez; ham çekim veri gizliliği açısından kontrol edilir.
9. Anlatıcı sesi müzikten önceliklidir; terimler, unvanlar, marka adları, web adresi ve CTA yazımı kontrol edilir.
10. Platform teknik gereklilikleri yayından önce güncel resmî kaynaklardan yeniden kontrol edilir.

---

## 3. PODCAST OLUŞTURMA KILAVUZU

### 3.1 Özet
- **Amaç:** "ses içeriğini yalnızca yayınlanacak bir kayıt olarak değil, marka uzmanlığını, güven algısını ve dönüşüm hedefini destekleyen sürdürülebilir bir içerik varlığı olarak ele almak"; "fikir aşamasından yayın sonrası performans ölçümüne kadar tek standart".
- **Ana bölümler (sırayla):** Kapak bilgisi + CTA standardı · 1 Amaç ve kapsam (kurumsal podcast, kısa sosyal ses, video podcast, webinar sonrası podcast, röportaj, lead magnet ses) · 2 İçerik stratejisi · 3 Format türleri · 4 Bölüm akışı ve senaryo · 5 Kopyalanabilir metin formatı · 6 Teknik ses kayıt standardı · 7 Kayıt ortamı ve ekipman · 8 Kurgu ve post-prodüksiyon · 9 Kapak görseli ve görsel kimlik · 10 Metadata ve RSS · 11 Platform yayın standartları · 12 Podcast SEO · 13 Transkript, altyazı, erişilebilirlik · 14 CTA, telefon, lead yönlendirme · 15 Sosyal medya uyarlama · 16 Dosya isimlendirme · 17 Yayın akışı (10 adım) · 18 Performans ve KPI · 19 Hukuki, KVKK, telif · 20 Brief şablonu · 21 Yayın öncesi checklist · 22 Kaynaklar.
- **Sayısal standartlar:**
  - Formatlar: Tek anlatıcı 1–8 dk; Sunucu + uzman 3–15 dk; İki uzman sohbeti 10–30 dk; Müşteri/vaka 5–15 dk; Webinar kesiti 5–20 dk; Kısa sosyal 30–90 sn.
  - Bölüm akışı (6 dk şablon): Açılış 0:00–0:15 · Hook 0:15–0:30 · Problem 0:30–1:30 · Uzman yanıtı 1:30–4:00 · Çözüm 4:00–5:00 · Özet 5:00–5:30 · CTA 5:30–6:00.
  - Ses: kayıt WAV 48 kHz 24-bit; yayın MP3 128 kbps+ veya AAC-LC; stereo ≈ -16 LUFS, mono ≈ -19 LUFS; tepe -1 dBTP altı; gürültü tabanı ≈ -60 dB; mikrofon 15–20 cm; Spotify en çok 12 saat, kurumsal içerik genellikle 5–30 dk; intro 5–10 sn, outro 5–15 sn.
  - Kapak: 1:1, 3000×3000 önerilir (Apple 1400–3000), PNG/JPG, transparan değil; %10 güvenli boşluk; sosyal kesit kapağı 1080×1920 / 1080×1080 / 1080×1350.
  - SEO: bölüm başlığı 60–80 karakter; açıklama 150–300 kelime; özet metin 40–60 kelime; konuşma hızı 130–160 kelime/dk.
  - Sosyal uyarlama: Reels/Shorts/TikTok 1080×1920 15–60 sn (ilk 2 sn hook); LinkedIn 30–90 sn; Instagram post 1080×1350; carousel 1080×1350 5–7 slayt; YouTube Community 1080×1080; mailing 600–800 px; WhatsApp kanal 60–90 sn.
  - Dosya adı: `[MARKA]_[PODCAST]_[EP_NO]_[KONU]_[YYYYMMDD]_MASTER.wav` / `_PUBLISH.mp3` / `_TRANSCRIPT.docx` / `_SUBTITLE.srt` / `_COVER_3000x3000.jpg` / `[PLATFORM]_CUT01.mp4`.
- **Süreç (§17):** konu-kitle-amaç-CTA-platform netleşir → senaryo ve uzman onayı → kayıt hazırlığı → kayıt (ayrı kanal) → kurgu, temizlik, loudness, export → kapak, açıklama, transkript, kesitler → RSS/hosting yükleme, metadata kontrolü → Apple, Spotify, YouTube, web, sosyal dağıtım → yayın sonrası link/oynatıcı/CTA kontrolü → performans raporu.
- **Uyum (§19):** konuşmacı onayı (kayıt, yayın, kesit, yeniden paylaşım), müzik ve görsel lisansı, "İsim, ses, görüntü, kurum bilgisi ve iletişim verileri KVKK kapsamında değerlendirilmelidir", hassas iddialar uzman kontrolü, "Sponsorlu içerikler açıkça belirtilmeli; reklam ve editoryal içerik ayrımı korunmalıdır", explicit işareti doğru.

### 3.2 A sınıfı bilgiler — mevcut karşılık
| # | Kılavuzdan alıntı | Mevcut karşılık | Durum / eksik |
|---|---|---|---|
| 1 | "Kurumsal Podcast Marka veya uzman tarafından düzenli yayınlanan ses serileri." | yok | **Yok** (bölüm yok) |
| 2 | "Show Title Podcastin seri adı. Kısa, akılda kalıcı ve marka ile ilişkili olmalıdır." | yok | **Yok** |
| 3 | "Show Description Serinin ne anlattığını ve kimler için olduğunu açıklayan kısa metin." | yok | **Yok** |
| 4 | "Category Platform kategori eşleşmesi doğru seçilmelidir." | yok | **Yok** |
| 5 | "Author / Sahip Marka, kurum veya içerik sahibi bilgisi." / "Language Birincil yayın dili." | `mk_brand_name`, `oc_legal_name`, `mk_languages` | **Tam** (Ortak Bilgiler'den türer) |
| 6 | Format tablosu "Tek Anlatıcı … Sunucu + Uzman … İki Uzman Sohbeti … Müşteri / Vaka Hikayesi … Webinar Kesiti … Kısa Sosyal Podcast" | yok | **Yok** |
| 7 | "Video Podcast Ses içeriğinin video çekimiyle birlikte YouTube, LinkedIn veya sosyal platformlara uyarlanması." / "YouTube / YouTube Music Video podcast, statik kapak + ses, Shorts kesiti veya tam bölüm video formatında" | yok | **Yok** |
| 8 | "Yayın Platformu Spotify, Apple Podcasts, YouTube, LinkedIn, web blog, WhatsApp Business veya mailing dağıtımı önceden belirlenmelidir." | `mk_platforms` (youtube, linkedin, whatsapp), `mk_mail_on` | **Kısmi** — Spotify, Apple Podcasts ve web bölüm sayfası yok; podcast'e özgü dağıtım listesi yok. |
| 9 | "Seri sürdürülebilirliği için takipçi veya abonelik artışı." + "düzenli yayınlanan" | yok | **Yok** (yayın sıklığı) |
| 10 | "Intro 5-10 sn, outro 5-15 sn aralığında tutulmalıdır. Marka jingle kullanılıyorsa lisanslı olmalıdır." | yok | **Yok** (jingle kararı) |
| 11 | "Tam transkript blog sayfasına eklenirse …" / "Özet Metin Bölümün 40-60 kelimelik kısa özeti" / "Bölüm Notları Kaynaklar, linkler, ilgili hizmet sayfaları" / sosyal uyarlama tablosu | yok | **Yok** (bölüm çıktı paketi) |
| 12 | "RSS feed kullanılıyorsa feed herkese açık, şifresiz ve RSS 2.0 uyumlu olmalıdır." | `mk_accounts` diger ("Spotify \| …" örneği) | **Kısmi** — Spotify / Apple Podcasts / RSS satırı yok. |
| 13 | KPI tablosu "İndirme … Dinlenme … Tamamlama Oranı … Dinleyici Kaybı … CTR … Lead / Form … Abonelik / Takip" | `mk_measure_scope` | **Kısmi** — podcast metrikleri yok. |
| 14 | "Reklam / Sponsorluk Sponsorlu içerikler açıkça belirtilmeli" | `mk_legal_scope` | **Kısmi** — sponsorlu / iş birliği içerik seçeneği yok. |
| 15 | "Konuşmacı Onayı Kayıt, yayın, kesit kullanımı ve yeniden paylaşım için konuşmacı izni alınmalıdır." | `mk_visual_meta` consent (görsel için) | **Kısmi** — ses kaydı / konuk izni kapsanmıyor (kural metnine eklenmeli, C). |
| 16 | "CTA Standardı CTA: [CTA_METNİ] \| Link: [CTA_LINK] \| Telefon: [TELEFON_NUMARASI]" | `mk_contact`, `domain_name` | **Tam** (veri Ortak Bilgiler'de; biçim C) |

### 3.3 B sınıfı brief alanları
Bölüm başlığı, bölüm no (EP-XX), marka (çok markalı yapıda), konu, anahtar kelime, hedef kitle (bu bölüm), format (bu bölüm), süre, konuşmacılar (sunucu / uzman / konuk), ana mesaj, CTA metni ve linki, bu bölümün dağıtım kanalları, bölüm açıklaması, bölüm notları, transkript, GUID, pubDate, enclosure (URL, MIME, boyut), explicit işareti (bölüm bazında), bölüm kapağı başlığı, sosyal kesit seçimi ve captionları; yayın sonrası KPI değerleri.

### 3.4 C sınıfı ilkeler (en fazla 10)
1. Strateji teknikten önce: her bölüm tek ana problem / soru etrafında, tek cümlelik ana mesaj ve tek CTA ile kurulur; doğaçlamada bile giriş, ana mesaj, süre ve CTA önceden belirlenir.
2. Bölüm akışı: Açılış (marka/seri adı, konu, vaat) → Hook → Problem → Uzman yanıtı → Çözüm ("doğrudan satış baskısı kurmadan") → Özet → CTA.
3. Ses tekniği: kayıt WAV 48 kHz 24-bit; yayın MP3 128 kbps+ / AAC-LC; stereo ≈ -16 LUFS, mono ≈ -19 LUFS; tepe < -1 dBTP; master ve yayın dosyası ayrı export; gürültü azaltma ölçülü ("metalik ses oluşmamalıdır").
4. Kapak: 1:1, 3000×3000 (1400–3000 kabul), PNG/JPG, transparan değil; logo, başlık, yüz merkezde, kenarlarda %10 boşluk; başlık mobilde okunur.
5. Metadata: RSS 2.0, herkese açık, şifresiz, UTF-8; her bölümde sabit ve benzersiz GUID; pubDate RFC 2822; enclosure URL, MIME ve boyut doğru; explicit doğru işaretlenir.
6. Keşfedilebilirlik: bölüm başlığı 60–80 karakter, konu ve anahtar kelimeyi doğal içerir; açıklama 150–300 kelime (özet, maddeler, konuk, CTA linki, telefon); web sayfasında yapısal veri görünür içerikle birebir.
7. CTA sözlü okunur, açıklamada yazılı yer alır, sosyal uyarlamada tekrarlanır; biçim "CTA: … | Link: … | Telefon: …".
8. Konuşma hızı 130–160 kelime/dk; teknik terimler ve kısaltmalar ilk kullanımda açılır; video podcast ve sosyal kesitlerde altyazı zorunlu.
9. İzin ve uyum: konuşmacı izni (kayıt, yayın, kesit, yeniden paylaşım), lisanslı müzik / jingle / görsel, isim-ses-görüntü KVKK kapsamında, hukuki / finansal / sağlık iddiaları uzman kontrolü, sponsorlu içerik açıkça belirtilir.
10. Kayıt: sessiz, yankısız oda; kapalı kulaklık; uzaktan kayıtta her konuşmacı ayrı kanal ve lokal kayıt; kritik kayıtta yedek; yayın sonrası link, oynatıcı, kapak ve CTA çalışırlığı kontrol edilir.

---

## 4. YENİ ALAN ÖNERİLERİ

### 4.1 Yeni bölüm: **Video Üretimi** (`mk_video`) — grup **İçerik**, `mk_creative`'ten sonra (kodlar yeniden numaralanır)

Önerilen öneri bağlantısı: `mk_video_on` için `recommend: {field: "mk_formats", map: {R: [true], V: [true]}}` (boolean hedef desteklenmiyorsa `rehber`de not). Tüm alanlar `showIf: [{field:"mk_video_on", in:[true]}]`.

**1. `mk_video_on` [boolean] "Video Üretimi"**
- yes — scenario: Marka sosyal medyada Reels / Shorts, sitede tanıtım ya da eğitim videosu, YouTube'da uzun içerik yayınlayacaksa ("her video çıktısının marka kimliğine uygun, teknik olarak doğru, platforma uyumlu, erişilebilir ve yayınlanabilir kalitede üretilmesini sağlamak"). example: Her video brief'i senaryo, sahne kartı, altyazı ve teslim paketiyle gelir; kapanışta CTA, web adresi ve telefon görünür.
- no — scenario: Marka hiç video üretmiyor ya da video yalnız sitedeki dekoratif arka plan ise. example: Planda video formatı olmaz; video kuralları prompta yazılmaz.

**2. `mk_video_types` [multiselect] "Video Türleri"** (Kılavuz §2 karar matrisi + uzun kılavuz §2–3)
| Etiket | Değer | scenario (ne zaman doğru) | example (içerikte nasıl görünür) |
|---|---|---|---|
| Sosyal medya kısa videosu (9:16 · 15–59 sn) | `social` | Reels, Shorts, TikTok, LinkedIn mobil akışta erişim hedefleniyorsa ("İlk 3 saniyede güçlü hook gerekir"). | 30 sn dikey video ilk 3 sn'de soruyla açılır, altyazılıdır, son 3–8 sn'de CTA. |
| Genel tanıtım videosu (16:9 · 60–299 sn) | `promo` | Web, YouTube, landing page ve sunumda marka ya da hizmet anlatılacaksa ("Giriş, problem, çözüm, kanıt ve CTA akışı kurulmalıdır"). | Ana sayfadaki 2 dakikalık yatay video problemle başlar, kanıtla devam eder, CTA ile biter. |
| Ürün / hizmet videosu (9:16 veya 16:9 · 30–90 sn) | `product` | Tek bir hizmetin faydası ve kullanım senaryosu sosyal, web ya da reklamda anlatılacaksa ("Fayda, kullanım senaryosu ve CTA net olmalıdır"). | Hizmet sayfasındaki 60 sn'lik video üç fayda ve tek CTA gösterir. |
| Eğitim / LMS videosu (16:9 · modül başına 30–180 sn) | `training` | Akademi, e-öğrenme ya da müşteri eğitimi yapılıyorsa ("Altyazı, ses kontrolü ve bölümleme kritik önemdedir"). | Her modül videosu bir öğrenme kazanımıyla başlar, SRT altyazısıyla LMS'e yüklenir. |
| Webinar / canlı yayın kaydı (16:9 · 15–60 dk) | `webinar` | Webinar, panel ya da canlı yayınlar kalıcı içeriğe dönüştürülecekse ("Bölüm işaretleri, kapak, açıklama ve kısa kesitler hazırlanmalıdır"). | YouTube'daki kayıt 00:00 bölüm zamanlarıyla yayımlanır; en iyi üç an dikey kesit olur. |
| Motion graphics / infografik video | `motion` | Veri, süreç, mevzuat ya da kontrol listesi görsel anlatılacaksa (kapsam: "Veri, süreç, kontrol listesi, mevzuat ve teknik konuların görsel anlatımı"). | Beş adımlı süreç ikon ve oklarla animasyonlu anlatılır, ekran yazıları post-prodüksiyonda eklenir. |
| Belgesel / marka hikâyesi / vaka | `story` | Marka hikâyesi, başarı hikâyesi ya da vaka anlatılacaksa ("Röportaj, B-roll, gerçek mekan ve anlatıcı sesi birlikte planlanmalı"). | Müşteri röportajı, sahadan B-roll ve anlatıcı sesiyle 8 dakikalık vaka filmi. |
| Uzun format — kısa sürüm (16:9 · 5–12 dk) | `long_short` | Tek konu hızlı ve odaklı anlatılacaksa: satış sunumu, kısa eğitim, YouTube açıklayıcı video ("Giriş + 2-4 ana bölüm + kapanış"). | 9 dakikalık video: 30 sn giriş, üç ana bölüm, 1 dk vaka, 30 sn CTA. |
| Uzun format — uzun sürüm (16:9 · 12–45+ dk) | `long_full` | Konu modüler ve kapsamlı anlatılacaksa: LMS, kurumsal eğitim, ürün demo ("Giriş + çoklu bölüm + konu blokları + özetler + kapanış"). | 30 dakikalık eğitimde her bölüm 15–30 sn başlık kartıyla açılır, sonunda 2–3 maddelik ara özet bulunur. |
- ruleDetail önerisi: her seçenekte kendi süresi, oranı ve akışı (yukarıdaki alıntılar); `long_full`'da "Her 2-4 dakikada görsel değişim", ara özet 20–40 sn; `long_short`'ta "Kısa versiyonlardan ayrıca 15-30 sn sosyal medya kesitleri üretilebilir."
- recommend önerisi: `mk_formats` R → `social`; V → `long_short`; `module_lms` (courses/corporate) → `training`; `mk_evt_types` webinar → `webinar`.

**3. `mk_video_script` [select] "Senaryo ve Storyboard Çıktısı"** (uzun kılavuz §3, §5, §9; kısa kılavuz §6–7, §16)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Senaryo + sahne kartları; storyboard yalnız kritik sahnelerde | `scenes` | Kısa sürüm, sosyal ve tanıtım videoları; ekip küçük, revizyon riski düşük ("Daha sade; kritik sahnelerde detaylı storyboard"). | Video 1.1.1.1 … numaralı sahne kartlarıyla gelir; yalnız açılış ve CTA sahnesinde storyboard karesi vardır. |
| Senaryo + sahne kartları + tam storyboard (2–5 sn kareler) | `full` | Uzun sürüm, dış çekim ekibi, ajans ya da AI video üretimi ("Her bölüm/konu/sahne için ayrıntılı storyboard ve prodüksiyon notu"). | 8 sn'lik her sahne 16–18 kelime metin taşır; 2 sn'lik storyboard karelerinde kamera, lens, ışık, renk, müzik ve amaç yazılıdır. |
- recommend: `mk_video_types` `long_full` / `story` → `full`; diğerleri → `scenes`.
- Kanıt: "Sahne … Video üretiminin en küçük operasyonel birimidir." (bu yüzden "yalnız konuşma metni" seçeneği önerilmedi).

**4. `mk_video_captions` [multiselect] "Altyazı ve Metin Dökümü"**
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Ayrı SRT dosyası (önerilen) | `srt` | Konuşma içeren her video; YouTube, LMS ve web oynatıcısında açılıp kapanabilen altyazı ("Konuşma içeren videolarda SRT hazırlanmalı"). | Her videoyla `…_TR_V1.srt` teslim edilir; satırlar 35–42 karakter, en çok iki satır. |
| Altyazı gömülü sürüm (önerilen) | `burned` | Sesi kapalı izlenen sosyal akış videoları ("Kısa, altyazılı ve hızlı açılışlı kurgu gerekir"; "SRT ve gömülü altyazılı versiyon hazırlanmalıdır"). | Reels sürümünde altyazı görüntünün içinde, alt güvenli alanda yer alır. |
| Tam metin dökümü (transkript) (önerilen) | `transcript` | Video sitede yayımlanacak ya da arama görünürlüğü önemliyse ("Erişilebilirlik ve SEO için konuşma metni veya transkript hazırlanmalıdır"). | Video sayfasının altında konuşmanın tam metni bulunur. |
| Hedef dillerde ek altyazı | `multi` | Ortak Bilgiler › Diller'de birden çok dil varsa ("SRT Dili Türkçe veya hedef yayın dili"). | Türkçe videoya İngilizce `…_EN_V1.srt` eklenir. |
- "Altyazı yok" seçeneği önerilmez: kılavuz (WCAG atfıyla) "Önceden kaydedilmiş sesli video içeriklerinde senkronize altyazı sağlanmalıdır".
- recommend: `mk_languages` 2+ dil → `multi`; `video_seo` true → `transcript`.

**5. `mk_video_deliver` [multiselect] "Teslim Paketi"** (kısa kılavuz §18, uzun kılavuz §10; temel çıktı her zaman MP4 / H.264 / AAC 48 kHz 1080p — kural metni)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| 4K master (3840×2160) | `master_4k` | Büyük ekran, premium kullanım ya da sonradan kadraj düzeltme gerekiyorsa ("premium veya büyük ekran kullanımında 3840x2160"). | Final 1080p yayınlanır, 4K master arşivlenir. |
| Arşiv master (ProRes / yüksek bitrate; altyazısız + altyazılı) | `archive` | Videodan sonradan yeni kesit ve dil sürümü üretilecekse ("altyazısız ve altyazılı iki çıktı"). | Arşivde temiz sesli, altyazısız ProRes master ve altyazılı MP4 birlikte durur. |
| Dikey sosyal kesit (9:16 · 1080×1920) (önerilen) | `v916` | Yatay videonun sosyal akışta da kullanılacağı her durumda ("Sosyal Kesit 9:16, 1080x1920, altyazılı, kapak görseli ile"). | 5 dakikalık videodan 3 adet 15–60 sn dikey kesit çıkar. |
| Kare sürüm (1:1 · 1080×1080) | `sq` | Kare akış yüzeyleri (LinkedIn, Facebook) kullanılıyorsa ("Kare Versiyon 1:1, 1080x1080"). | LinkedIn gönderisinde kare sürüm. |
| Feed dikey sürüm (4:5 · 1080×1350) | `p45` | Instagram / Facebook akışında daha geniş mobil alan isteniyorsa ("Feed için 4:5 güçlü mobil alan sağlar"). | Akış gönderisinde 4:5 sürüm. |
| 15–30 sn reklam kesiti | `ad_cut` | Video ücretli tanıtımda da kullanılacaksa ("15-30 sn arası reklam versiyonu ayrıca hazırlanmalıdır"). | LinkedIn ve Meta reklamında kullanılan 20 sn'lik kesit. |
| Kapak görseli / küçük resim (önerilen) | `cover` | Her yayımlanan video ("İzlemeyi tetikleyen, maksimum 6 kelimelik başlık"; "YouTube için 1280x720"). | YouTube'da 1280×720 kapak; büyük, en çok 6 kelimelik başlık ve küçük logo. |
| Bölüm zaman kodları (00:00) | `chapters` | 5 dakikayı aşan YouTube / web videoları ("Uzun YouTube videolarında 00:00 formatında bölüm zamanları eklenmelidir"). | Açıklamada "00:00 Giriş · 01:20 Problem · 04:10 Çözüm". |
| Ayrı ses dosyası (WAV) | `voice` | Seslendirme ayrı kaydediliyor ya da podcast'e dönüştürülecekse ("Ses Dosyası WAV / MP3, sahne veya video numarasıyla"). | `…_Voice_V1.wav` teslim edilir. |
| Kaynak proje dosyası | `project` | Video ajans / serbest çalışan tarafından yapılıyor ve sonradan düzenlenecekse ("Kaynak Proje Premiere Pro / After Effects / CapCut / Figma / Canva linki"). | Teslimde kurgu proje bağlantısı da verilir. |
- recommend: `mk_video_types` `long_full`/`long_short`/`webinar` → `chapters`, `v916`; `mk_ads_channels` ≠ none → `ad_cut`.

**6. `mk_video_voice` [multiselect] "Seslendirme"** (kısa kılavuz §14; uzun kılavuz §12)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Uzman / çalışan kendi sesiyle anlatır | `speaker` | Uzman anlatımı, webinar, kurumsal eğitim; güven için gerçek kişi gerekiyorsa ("Konuşma metni … tek anlatıcı, uzman anlatımı …"; "Yaka mikrofonu veya shotgun mikrofon"). | Uzman kameraya orta planda konuşur; alt bantta adı ve unvanı yazar. |
| Profesyonel seslendirme | `pro` | Tanıtım ve motion videolarında "broadcast-ready" ses isteniyorsa ("Voice-over net ve broadcast-ready seviyede olmalıdır"). | Tanıtım videosunda stüdyo kaydı WAV seslendirme. |
| Yapay zekâ seslendirme (etiketli) | `ai` | Sık üretilen eğitim ve bilgi videolarında hız gerekiyorsa ("ElevenLabs / AI Seslendirme Prompt Örneği"). | Seslendirme marka ses profiliyle üretilir; yapay zekâ etiketi `mk_visual_source` ai kuralına göre eklenir. |

**7. `mk_video_voice_profile` [text] "Seslendirme Sesi ve Tonu"** — showIf `mk_video_voice` in [pro, ai]
- placeholder: "Örn. Orta yaş kadın sesi; kurumsal, sakin, güven veren; orta hız (2,2–2,6 kelime/sn)"
- scenario: Farklı videolarda aynı marka sesinin duyulması isteniyorsa. example: Bütün eğitim videolarında aynı ses türü ve ton kullanılır; yeni seslendirme bu tanımla istenir.
- Kanıt: "Ses Türü Kadın / erkek / genç / orta yaş / olgun / kurumsal lider tonu" · "Ses Tonu Kurumsal, sakin, anlaşılır, güven veren, bilgilendirici" · "Okuma Hızı … yaklaşık 2,2-2,6 kelime / saniye".

**8. `mk_video_ai` [select] "Yapay Zekâ ile Video"** (kısa kılavuz §1, §2, §13, §23)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kullanılmaz (gerçek çekim, ekran kaydı, motion) | `none` | Gerçek ekip, mekân ve müşteriyle güven kurulması gerekiyorsa ya da düzenlenmiş sektörde. | Bütün sahneler kamera çekimi veya ekran kaydıdır. |
| Yalnız B-roll ve metaforik sahnelerde | `broll` | Çekimi zor kavram ve arka plan sahneleri için ("AI Video Sahnesi … 3-8 sn / sahne … B-roll, metaforik sahne, açıklayıcı video"). | Uzman konuşması gerçek çekim, "veri güvenliği" kavramı 5 sn'lik AI sahnesi. |
| Sahnelerin tamamı yapay zekâ ile | `full` | Açıklayıcı ve kavramsal videolarda çekim bütçesi yoksa ("Yapay zekâ destekli video: Kling, Veo, Runway, Seedance ve benzeri araçlarla sahne üretimi"). | Her sahne master prompt ve sahne promptuyla üretilir; logo ve yazılar kurguda eklenir. |
- ruleDetail (broll, full): "AI video içinde okunabilir metin, logo veya marka işareti ürettirilmez; ekran yazısı, logo, alt bant, CTA ve altyazı post-prodüksiyonda eklenir. Master prompt + sahne promptu + negatif prompt standardı uygulanır; karakter ve kamera sabitlenir; prompt dili araca göre (Kling, Veo, Runway, Seedance için İngilizce). Üretilen video `mk_visual_source` ai kuralına göre etiketlenir."
- recommend: `mk_visual_source` ai yoksa → `none` (ya da bilgi notu: AI görsel kaynağı kapalıyken `broll`/`full` seçilirse uyarı).

**9. `mk_video_brand` [multiselect] "Videoda Marka Öğeleri"** (kısa kılavuz §11, §17; uzun kılavuz §11; podcast §8 jingle)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kısa marka girişi (intro, en çok 2–3 sn) | `intro` | Tanıtım, eğitim ve uzun videolarda ("Intro Maksimum 2-3 saniye; marka girişi hızlı ve sade olmalıdır"). | İlk 2 sn'de logo animasyonu, ardından doğrudan konu. |
| Kapanış ekranı: CTA + web adresi + telefon + logo (önerilen) | `outro` | CTA içeren her video ("Outro CTA, web adresi, telefon ve logo ile tamamlanır"; "Kapanış ekranında web sitesi, telefon ve CTA birlikte verilmelidir"). | Son 5 sn: "Ücretsiz ön görüşme" + site adresi + telefon + logo. |
| Köşede sabit küçük logo (sağ üst) | `logo_corner` | Video paylaşıldığında markanın tanınması isteniyorsa ("Logo Alanı Sağ üst veya sol üst güvenli alan"; "tercihen sağ üst"). | Video boyunca sağ üstte düşük yoğunluklu logo. |
| Alt bant (konuşmacı adı, unvan, bölüm adı) | `lower_third` | Konuşmacılı ve bölümlü videolarda ("Alt Bant Konuşmacı adı, görev, bölüm başlığı veya kısa vurgu metni"). | "Ayşe Yılmaz · Uyum Uzmanı" alt bandı alt güvenli alanda. |
| Bölüm başlık kartı (3–6 kelime) | `title_card` | Uzun formatlı ve eğitim videolarında ("Bölüm girişlerinde 3-6 kelimelik başlık, sade arka plan ve güçlü kontrast"). | "2. Bölüm · Riskleri Tanıyın" kartı. |
| Kapanışta QR kod | `qr` | Video ekranda, fuarda ya da sunumda oynatılacaksa ("varsa QR/link yönlendirmesi"). | Kapanış ekranında form sayfasına giden QR. |
| Marka müziği / jingle (lisanslı) | `jingle` | Seri içeriklerde tanınırlık isteniyorsa ("Marka jingle kullanılıyorsa lisanslı olmalıdır"; "marka tonuna uygun fon müziği"). | Her videonun intro ve outrosunda aynı 3 sn'lik ses imzası. |

**10. `mk_video_approval` [multiselect] "Video Onay Aşamaları"** (kısa kılavuz §21; uzun kılavuz §16) — genel `mk_flow`'un video için ara aşamaları
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Brief onayı (pazarlama / iş sahibi) | `brief` | Ajans ya da dış ekip çalışıyorsa ("Amaç, hedef kitle, CTA, platform ve format net mi?"). | Brief onaylanmadan senaryo yazılmaz. |
| Senaryo onayı (önerilen) | `script` | Her video ("Konuşma metni, süre, başlık ve ana mesaj doğru mu?"). | Konuşma metni süre hesabıyla onaya gider. |
| Storyboard onayı | `storyboard` | Tam storyboard üretilen videolarda ("Sahne akışı, kamera, görsel ve geçiş net mi?"). | Çekimden önce storyboard PDF'i onaylanır. |
| Ses onayı | `voice` | Profesyonel ya da AI seslendirmede ("Ton, telaffuz, vurgu ve okuma hızı uygun mu?"). | Seslendirme kurguya girmeden dinlenip onaylanır. |
| İlk kurgu onayı (önerilen) | `rough_cut` | Her video ("Akış, ritim, altyazı, ekran metinleri ve müzik dengesi uygun mu?"). | V1 kurgu yorumlanır, V2 hazırlanır. |
| Teknik kontrol | `technical` | Birden çok platforma export varsa ("Export, çözünürlük, FPS, dosya adı ve platform uyumu doğru mu?"). | Her platform kopyası teknik listeyle kontrol edilir. |
| Hukuki / uzman kontrolü | `legal` | Mevzuat, finans, sağlık, KVKK, İSG içerikli videolarda ("Mevzuat, finans, KVKK, İSG veya teknik iddialarda risk var mı?"). | Vergi konulu video mali müşavir görüşünden geçer. |
| Final onay (önerilen) | `final` | Her video ("Yayına hazır mı, revizyon gerekiyor mu?"). | Yayın tarihinden önce iş sahibi final sürümü onaylar. |
- recommend: `mk_legal_on` true veya `sector_regulations` ≠ None → `legal`; `mk_video_script` full → `storyboard`; `mk_video_voice` pro/ai → `voice`.

(Alan sayısı: 10. Dosya adlandırma alan olarak önerilmedi; §5 madde 11'deki çelişki tek kural metniyle çözülmeli.)

### 4.2 Yeni bölüm: **Podcast** (`mk_podcast`) — grup **Kanallar**, `mk_mail`'den sonra

Tüm alanlar `showIf: [{field:"mk_pod_on", in:[true]}]`.

**1. `mk_pod_on` [boolean] "Podcast Yayını"**
- yes — scenario: Marka uzmanlığını düzenli bir ses serisiyle anlatmak, güven algısı ve lead üretmek istiyorsa ("marka uzmanlığını, güven algısını ve dönüşüm hedefini destekleyen sürdürülebilir bir içerik varlığı"). example: Seri Spotify, Apple Podcasts ve YouTube'da yayımlanır; her bölümün web sayfasında transkript ve CTA bulunur.
- no — scenario: Düzenli ses içeriği üretecek konuşmacı ya da prodüksiyon kapasitesi yoksa. example: Podcast kuralları ve çıktıları prompta yazılmaz.

**2. `mk_pod_name` [text] "Podcast (Seri) Adı"** — ph: "Örn. Uzman Notları". Kanıt: "Show Title Podcastin seri adı. Kısa, akılda kalıcı ve marka ile ilişkili olmalıdır." scenario: Seri tek bir adla bütün platformlarda tanınmalıysa. example: Açılışta "Merhaba, [Seri adı]'na hoş geldiniz" okunur; RSS `title` alanı bu addır.

**3. `mk_pod_desc` [textarea] "Seri Açıklaması"** — ph: "Örn. KOBİ'ler için mevzuat ve finans konularında 10 dakikalık uzman sohbetleri." Kanıt: "Show Description Serinin ne anlattığını ve kimler için olduğunu açıklayan kısa metin." scenario/example: platform mağaza sayfasında ve web seri sayfasında aynı metin görünür.

**4. `mk_pod_category` [text] "Platform Kategorisi"** — ph: "Örn. İş Dünyası › Yönetim". Kanıt: "Category Platform kategori eşleşmesi doğru seçilmelidir." scenario: Seri Apple / Spotify'da doğru listede çıksın diye bir kez belirlenir. example: RSS'te kategori etiketi bu değerle yazılır. (Platform kategori listesi kılavuzda yok; liste uydurmamak için metin alanı önerildi.)

**5. `mk_pod_formats` [multiselect] "Bölüm Formatları"** (§3)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Tek anlatıcı (1–8 dk) | `solo` | "Bilgilendirme, mevzuat, kısa uzman görüşü" | Giriş > Problem > Açıklama > Çözüm > CTA akışlı 5 dakikalık bölüm. |
| Sunucu + uzman (3–15 dk) (önerilen değil; kılavuzun 6 dk şablonu bu formatta) | `host_expert` | "Kurumsal güven, soru-cevap, danışmanlık perspektifi" | Sunucu sorar, uzman kısa ve net yanıtlar verir. |
| İki uzman sohbeti (10–30 dk) | `duo` | "Derin konu analizi, sektör içgörüsü, panel hissi" | Gündem > tartışma > örnek > özet > CTA. |
| Müşteri / vaka hikâyesi (5–15 dk) | `case` | "Sosyal kanıt ve başarı hikayesi" | Önce > sorun > çözüm > sonuç > öneri. |
| Webinar kesiti (5–20 dk) | `webinar` | "Canlı yayından yeniden içerik üretimi" | Webinarın en değerli bölümleri seçilir, intro/outro eklenir. |
| Kısa sosyal podcast (30–90 sn) | `short` | "WhatsApp, LinkedIn, Reels/Shorts için hızlı tüketim" | Hook > tek içgörü > CTA. |
- Not: kılavuz bir format önermiyor; "(önerilen)" konmamalı. Kopyalanabilir metin şablonu (§5) "[Sunucu]" / "[Uzman]" rolleriyle yazıldığı için `host_expert` varsayılan olarak düşünülebilir — kullanıcıya sorulmalı.
- recommend: `mk_evt_types` webinar → `webinar`.

**6. `mk_pod_media` [select] "Yayın Biçimi"** (§1, §11)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Yalnız ses | `audio` | Konuşmacılar kamera önünde olmak istemiyor ya da prodüksiyon basitse. | Bölüm yalnız Spotify / Apple'da ses olarak yayımlanır. |
| Ses + statik kapaklı YouTube videosu | `static` | YouTube'da da bulunmak isteniyor ama çekim yapılmıyorsa ("statik kapak + ses"). | YouTube'da bölüm kapağı üzerinde ses oynar; bölüm zaman kodları açıklamada. |
| Video podcast (kamera çekimi) | `video` | YouTube, LinkedIn ve sosyal kesit üretimi hedefleniyorsa ("Ses içeriğinin video çekimiyle birlikte YouTube, LinkedIn veya sosyal platformlara uyarlanması"). | İki kameralı stüdyo çekimi; kesitler altyazılı Reels olur. |
- ruleDetail (video): "Video podcast ve sosyal kesitlerde altyazı zorunlu kabul edilmelidir."; `mk_video_on` önerilir.

**7. `mk_pod_freq` [select] "Yayın Sıklığı"** — Haftalık=`weekly`, 2 haftada bir=`biweekly`, Aylık=`monthly`. Kanıt: "Marka veya uzman tarafından düzenli yayınlanan ses serileri." / "Seri sürdürülebilirliği için takipçi veya abonelik artışı." Kılavuz sayı vermiyor → "(önerilen)" yok. scenario: weekly — iki ve üzeri sabit konuşmacı ve hazır konu havuzu varsa; biweekly — tek uzmanla sürdürülebilir ritim; monthly — konuk ağırlıklı, hazırlığı uzun seriler. example: Takvimde her bölümün kayıt, kurgu ve yayın günü bu ritimle planlanır.

**8. `mk_pod_platforms` [multiselect] "Dağıtım Kanalları"** (§2, §11, §20)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Spotify | `spotify` | Geniş dinleyici; RSS ile dağıtım ("128 kbps+ MP3 veya AAC-LC önerilir"). | Bölüm RSS'ten Spotify'a düşer. |
| Apple Podcasts | `apple` | iOS dinleyicisi ("RSS feed; gerekli etiketler, en az bir bölüm ve artwork içermelidir"). | 3000×3000 kapakla listelenir. |
| YouTube / YouTube Music | `youtube` | Video ya da statik kapaklı yayın. | Başlık, açıklama, zaman kodu ve thumbnail ayrıca hazırlanır. |
| Web sitesi (bölüm sayfası) | `web` | Arama görünürlüğü ve dönüşüm ("Ses oynatıcı embed edilmeli; bölüm özeti, transkript, kaynaklar ve CTA yer almalıdır"). | `/podcast/bolum-12/` sayfasında oynatıcı + transkript + CTA. |
| LinkedIn | `linkedin` | B2B karar verici ("kısa video kesit, audio quote post veya doküman carousel"). | Bölümden 60 sn'lik uzman kesiti. |
| WhatsApp Kanal | `whatsapp` | ("60-90 saniyelik kısa ses veya podcast link duyurusu … telefon bilgisi görünür") | Kanalda 60 sn ses + bölüm linki. |
| E-posta bülteni | `mail` | Abonelere bölüm duyurusu ("Podcast başlığı, kısa özet, CTA butonu ve telefon"). | Bültende podcast kutusu. |
- recommend: `mk_platforms` youtube / linkedin / whatsapp → aynı değerler; `mk_mail_on` true → `mail`.

**9. `mk_pod_assets` [multiselect] "Bölüm Çıktıları"** (§8, §9, §12, §13, §15)
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Tam transkript (önerilen) | `transcript` | ("Tam bölüm için transkript arşivlenmelidir"; blog sayfasına eklenirse SEO ve erişilebilirlik) | Konuşmacı adlarıyla ayrıştırılmış metin. |
| 40–60 kelimelik kısa özet (önerilen) | `summary` | Platform açıklaması ve sosyal metin için ("Bölümün 40-60 kelimelik kısa özeti hazırlanmalıdır"). | Bölüm kartındaki özet paragraf. |
| Bölüm notları ve kaynaklar | `notes` | ("Kaynaklar, linkler, ilgili hizmet sayfaları ve içerik yönlendirmeleri eklenmelidir") | Açıklamada ilgili hizmet sayfası bağlantıları. |
| Bölüm kapağı (1:1 · 3000×3000) | `episode_art` | Her bölüme ayrı görsel isteniyorsa ("Episode Art … 3000x3000 px tercih edilmeli"). | Bölüm başlıklı kare kapak. |
| Altyazı dosyası (SRT / VTT) | `subtitles` | Video podcast ve kesitler varsa ("Video podcast, Shorts, Reels ve sosyal medya kesitleri için altyazı dosyası"). | Kesitlerle `_SUBTITLE.srt`. |
| Sosyal kesitler (15–60 sn dikey) | `cuts` | Sosyal mecralarda da duyurulacaksa ("1080x1920 px, 15-60 sn … İlk 2 saniye hook, altyazı"). | Bölüm başına 2–3 dikey kesit. |
| Alıntı görseli / carousel | `quote` | Instagram / LinkedIn görsel paylaşımı ("Bölümden ana fikir, alıntı veya 3 maddelik özet"; carousel 5–7 slayt). | Uzmanın bir cümlesi 1080×1350 görselde. |

**10. `mk_pod_jingle` [boolean] "Marka Jingle'ı (Intro / Outro Müziği)"**
- yes — scenario: Seri tanınır bir ses imzasıyla açılıp kapanacaksa. example: 5–10 sn intro ve 5–15 sn outro aynı lisanslı müzikle. 
- no — scenario: Sade, konuşma odaklı bölümler. example: Bölüm doğrudan sözlü açılışla başlar.
- Kanıt: "Intro 5-10 sn, outro 5-15 sn aralığında tutulmalıdır. Marka jingle kullanılıyorsa lisanslı olmalıdır."

### 4.3 Ortak Bilgiler'e tek alan (isteğe bağlı ama önerilir)

**`oc_pronounce` [textarea] "Okunuş ve Kısaltma Listesi"** — bölüm `oc_identity` (77), `mk_contact`'tan sonra.
- ph: "Örn. KVKK | ka-ve-ka-ka (ilk kullanımda: Kişisel Verilerin Korunması Kanunu)\nMarka adı | okunuşu"
- scenario: Seslendirme, podcast ve AI ses üretiminde marka adı, ürün adları ve kısaltmaların her seferinde aynı okunması isteniyorsa. example: Seslendirme prompt'una ve podcast metnine "KVKK: ilk kullanımda açık hali, sonra ka-ve-ka-ka" satırı eklenir.
- Kanıt: video "Telaffuz KVKK, GDPR, SGK, İSG gibi kısaltmaların okunuşu belirtilmelidir."; podcast "kısaltmalar ilk kullanımda açık haliyle yazılmalıdır"; ses onayı "Ton, telaffuz, vurgu ve okuma hızı uygun mu?". Ortak bölümde durursa video kapalıyken podcast'te de kullanılabilir (iki bölüme aynı alan konamıyor). `refs`: `mk_video`, `mk_podcast`.

---

## 5. MEVCUT ALANLARDA DEĞİŞİKLİK ÖNERİLERİ

1. **`mk_formats` → seçenek V "Uzun video": `ruleDetail` boş.** Öneri: "Uzun video 16:9 1920×1080 (premiumda 3840×2160) üretilir; kısa sürüm 5–12 dk, uzun sürüm 12–45+ dk; açıklamada 00:00 bölüm zamanları, SRT altyazı ve kapak görseli bulunur; video üretim kuralları Video Üretimi bölümüne göre." Kanıt: uzun kılavuz §3, §10; kısa kılavuz §19. Ayrıca `marketingTemplate.formatlar`'da V yok — plan dosyasında format kartı boş kalıyor. V için `{olcu: "1920×1080 (16:9)", sure: "5–12 dk kısa sürüm · 12–45+ dk uzun sürüm; bölüm zaman kodları", plat: ["YouTube","LinkedIn video","Web / LMS"]}` eklenebilir — **ama** bu nesne içerik planı şablonundan kopyalanmış; şablon (`dogrula.mjs`) V'yi kabul ediyor mu önce doğrulanmalı.
2. **`mk_formats` → R "Reels / kısa video" süre farkı.** Şablondaki `R.sure` "15–45 saniye", kılavuz "Sosyal Medya Videosu … 15-59 sn", X için "30-60 sn", uzun kılavuzda sosyal kesit "15-60 sn". Öneri: `ruleDetail`'e "15–59 sn (ideal 15–45 sn)" yazmak; ayrıca "TikTok'ta altyazı sağ ve alt UI alanlarından uzak tutulur" eklemek (kılavuz: "altyazılar sağ ve alt UI alanlarından uzak tutulmalıdır"; mevcut metin yalnız üst ve alt kenarı söylüyor).
3. **`mk_caption` ↔ video açıklaması.** Kılavuz: "Sosyal medya video açıklaması anahtar kelime ile başlamalı ve CTA cümlesi ile bitmelidir." Mevcut `structured` seçeneği "Her metin ilk satırda kanca ile başlar". Çelişki değil ama birleştirilmeli: `structured` ruleDetail'ine "video paylaşımlarında kanca cümlesi odak anahtar kelimeyi içerir" eklenebilir.
4. **`mk_platforms` → youtube `ruleDetail`.** Şu an "Shorts … 100 karakter; uzun videolarda açıklama ilgili sayfaya bağlantı verir". Ekle: "uzun videolarda açıklamada 00:00 bölüm zamanları, başlık anahtar kelimeyle başlar (4–6 kelime), kapak 1280×720." Kanıt: kısa §19, uzun §10, §14.
5. **`mk_banned` → iki eksik seçenek.**
   - `fear` "Korku pazarlaması (abartılı risk ve tehdit dili)" — scenario: güvenlik, sağlık, hukuk ve finans gibi riskin satış argümanı yapılabildiği sektörler; example: "Bu hatayı yaparsanız şirketiniz kapanır" yerine "Bu kontrol, cezai riski azaltır". Kanıt: "Abartılı vaat, doğrulanmamış rakam, korku pazarlaması … kullanılmamalıdır."
   - `outcome_promise` "Kesin sonuç vaadi (hukuki, finansal, sağlık)" — scenario: danışmanlık, finans, sağlık, hukuk hizmetleri; example: "Davanızı kazandırırız" / "%100 vergi tasarrufu" yazılmaz. Kanıt: "hukuki/finansal kesin sonuç vaadinden kaçınılmalıdır."
6. **`mk_measure_scope` → iki seçenek.**
   - `video` "Video metrikleri (izlenme süresi, izleyici tutma, CTR, tamamlama)" — Kanıt: uzun §14 "İzlenme süresi, CTR, izleyici tutma, yorumlar, link tıklamaları"; LMS "Tamamlama oranı … izleme bırakma noktası". showIf/recommend: `mk_video_on`.
   - `podcast` "Podcast metrikleri (indirme, dinlenme, tamamlama, dinleyici kaybı, takipçi)" — Kanıt: podcast §18. showIf/recommend: `mk_pod_on`.
7. **`mk_accounts` → yeni satırlar.** `spotify` (Spotify podcast sayfası), `apple_podcasts` (Apple Podcasts sayfası), `podcast_rss` (RSS akışı adresi; `re` ile yumuşak URL denetimi), `when: mk_pod_on`. Kanıt: §10 "RSS feed … herkese açık, şifresiz ve RSS 2.0 uyumlu", §11 Apple / Spotify. Şu an Spotify yalnız "diğer" satırında örnek olarak geçiyor.
8. **`mk_roles` → `video` seçeneğinin senaryosu ve yeni rol.** `video` "Video editörü" senaryosu yalnız kısa video diyor; uzun format ve webinar kurgusunu da kapsamalı (kılavuz: "Kurgu İlk Taslak — Video Editör"). Yeni rol önerisi: `producer` "Prodüksiyon (çekim, ses kaydı, kurgu)" — Kanıt: "Storyboard Onayı — Tasarım / Prodüksiyon"; podcast "Hedef Kullanıcı … prodüksiyon … ve ajans ekipleri"; "Ham Çekim Kontrolü — Video ekibi".
9. **`mk_legal_scope` → yeni seçenek** `sponsored` "Sponsorlu / iş birliği içerikleri" — Kanıt: "Sponsorlu içerikler açıkça belirtilmeli; reklam ve editoryal içerik ayrımı korunmalıdır." (Ayrıca `recorded` "Konuk / konuşmacı ses ve görüntü kaydı içeren içerikler" düşünülebilir — Kanıt: "Kayıt, yayın, kesit kullanımı ve yeniden paylaşım için konuşmacı izni alınmalıdır.")
10. **`mk_visual_meta` → consent `ruleDetail`'i genişletilmeli:** şu an "görsel" diyor; "video ve ses kaydındaki konuşmacı / konuk için de kayıt, yayın, kesit ve yeniden paylaşım izni alınır" eklenmeli (podcast §19, uzun §16 "veri gizliliği").
11. **Dosya adlandırma çelişkisi.** Üç ayrı biçim var: `mk_brief_format` full → `Marka_BriefNo_FORMAT_YAYINTARİHİ_v01`; kısa video kılavuzu → `VideoX_BolumY_PartZ_SahneW_V1.mp4` / `VideoX_Final_TR_16x9_V1.mp4`; uzun kılavuz → `marka_konu_platform_sure_v01.mp4`, altyazı `marka_konu_tr_srt_v01.srt`; podcast → `[MARKA]_[PODCAST]_[EP_NO]_[KONU]_[YYYYMMDD]_…`. Alan eklemeden tek kural öneriyorum: final dosyalar brief adlandırmasını izler (marka + brief no + format/platform + dil + sürüm); sahne düzeyindeki ara dosyalar sahne kodunu (`…_SahneW_…`) ekler. Kullanıcıya hangi biçimin esas olacağı sorulmalı (kılavuzlar kendi aralarında tutarsız).
12. **`video_seo` (07)** — site videoları için **tam** karşılık (title, description, thumbnail, transcript/caption, VideoObject). Değişiklik gerekmiyor; yalnız `mk_video_captions` `transcript` önerisi bu alandan beslenebilir. Podcast web sayfası için `schema_types`'ta podcast türü yok; kılavuz "Schema/structured data kullanılıyorsa sayfa içeriğiyle birebir uyumlu olmalıdır … Google Rich Results Test ile kontrol" diyor — eklemeden önce Google'ın güncel desteği doğrulanmalı (uydurmamak için öneri olarak bırakıldı).
13. **`mk_derive`** blog → paylaşım türetmeyi kapsıyor; kılavuzlar videodan ("Ana videodan 15-60 sn dikey/karesel teaser") ve webinardan podcast'e ("Webinar Sonrası Podcast") türetmeyi tarif ediyor. Alan değil; `mk_video_deliver` `v916` ve `mk_pod_formats` `webinar` ile karşılanıyor — `mk_derive` rehberine bir cümle eklenebilir.

---

## 6. Kısa kontrol: alan sayısı ve sınır
- `mk_video`: 10 alan (on + 9). `mk_podcast`: 10 alan (on + 9). Ortak Bilgiler: 1 (`oc_pronounce`).
- Bölüm sınırı: `mk_social` = paylaşım (mecra, format etiketi, metin, etiket, saat); `mk_video` = üretim ve teslim; `mk_creative` = brief biçimi, görsel kaynak ve yasaklar (AI etiketi ve rıza buradan devralınır); `video_seo` = sitedeki video sayfası teknik SEO'su.
- Hiçbir seçenekte şirket adı, telefon ya da renk yok; Rasyotek'e atıflar (kaynak notları) genel kurallara çevrildi.
