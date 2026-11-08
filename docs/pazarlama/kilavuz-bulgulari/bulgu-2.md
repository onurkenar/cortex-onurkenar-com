# Bulgu 2 — Mailing, SMS, Basın Bülteni kılavuzları → form alanı analizi

Okunan dosyalar (tamamı): `Mailing_Icerik_Olusturma_Kilavuzu_Kurumsal.txt` (507 satır, 16 bölüm), `SMS_Icerigi_Olusturma_Kilavuzu_Kurumsal.txt` (323 satır, 16 bölüm), `Basin_Bulteni_Olusturma_Kilavuzu_Kurumsal.txt` (353 satır, 16 bölüm), `alan-envanteri.md` (tamamı).
Ek doğrulama (salt okuma): uygulamadaki `DATA.fields` içinden `mk_mail_*`, `mk_utm`, `mk_measure_scope`, `mk_evt_channels`, `mk_legal_scope`, `mk_roles`, `mk_approvers`, `schema_types`, `sender_domain`, `mk_mail_tool` kural metinleri (`rule` / `ruleDetail`) okundu — aşağıdaki "tam / kısmi" kararları envanterdeki etiketlere değil, bu kural metinlerine de dayanır.

Önemli tespit: mevcut `mk_mail_*` kural metinleri kılavuzun uyum ve teknik kısmının çoğunu zaten karşılıyor (List-Unsubscribe → `mk_mail_consent.unsub`; SPF / DKIM / DMARC → `sender_domain` kuralı ve `mk_mail_tool` ruleDetail; tek ana CTA ve bölüm başına `utm_content` → `mk_mail_layout`; görseller kapalıyken anlaşılırlık ve alt metin → `mk_mail_formats`; mobilde tek sütun → `mk_mail_layout` kuralı; işlemsel e-postaların tanıtım içermemesi → `mail_provider` (27) kuralı). Eksik olan asıl şey **şablonun ölçü / gönderen / CTA kararları** ile **SMS ve basın bülteni kanallarının tamamı**.

---

## 1. Mailing İçerik Oluşturma Kılavuzu

### 1.1 Özet
- **Amaç:** "Mailing içeriklerinin strateji, metin, tasarım, teknik uyum, gönderim ve raporlama süreçlerinde ortak standartla hazırlanması." Temel çıktı: "Kopyalanabilir metin, tasarım briefi, teknik ölçü, CTA, UTM, test ve yayın checklisti."
- **Bölümler (sırayla):** 1 Amaç ve Kapsam · 2 Mailing Türleri (9 tür) · 3 Brief Alanları · 4 Teknik Tasarım Standartları · 5 HTML / Kodlama ve İstemci Uyumu · 6 Görsel, Dosya ve Performans · 7 Konu Başlığı, Önizleme, Gönderen · 8 İçerik Mimarisi · 9 CTA, Link, Telefon, UTM · 10 KVKK, İYS, İzin · 11 Teslim Edilebilirlik · 12 Türlere Göre Üretim (12.1–12.8) · 13 Metin Şablonları · 14 Test, Yayın, Raporlama · 15 Final Checklist · 16 Kaynak Notları.
- **Mailing türleri:** Haftalık / aylık bülten · Hizmet tanıtım · Kampanya · Etkinlik / webinar · Lead magnet · Blog derleme · Yeniden pazarlama · Kurumsal duyuru · Transactional / bilgilendirme.
- **Sayısal standartlar:**
  - Gövde genişliği 600–800 px; "önerilen çalışma genişliği 600, 640 veya 660 px".
  - Mobil 320–480 px tek kolon; üst güvenli alan ilk 400–600 px (logo, başlık, değer önerisi, CTA).
  - Hero 600–800 × 180–350 px; hero görsel 600×250, 640×300, 660×320 px; kart görseli 300×180, 320×200, 600×338 px; tam genişlik görsel 600–1200 px (retina 2x).
  - CTA butonu en az 44 px yükseklik; CTA metni 2–4 kelime; birincil CTA tek.
  - Gövde metni en az 14 px, ideal 15–16 px, mobilde 16 px; başlık 22–32 px; satır yüksekliği 1.4–1.6; bloklar arası 16–32 px.
  - Logo 120–220 px, PNG.
  - Görsel ağırlığı ideal 100–300 KB, en çok 1 MB; RGB; JPG / PNG / GIF.
  - Konu başlığı 35–55 karakter (ilk 35 kritik); önizleme 70–120 karakter.
  - Giriş paragrafı 2–3 cümle; ana içerik 3–5 fayda / kart; bültende 3–5 içerik kartı.
  - Raporlama 24 saat, 48 saat, 7 gün.
- **Süreç (Bölüm 14):** içerik onayı → tasarım onayı → teknik test (Gmail, Outlook, Apple Mail, mobil, dark mode, plain text) → link testi → spam testi → liste kontrolü → gönderim (tarih, saat dilimi, frekans) → raporlama.
- **Uyum:** İYS kayıt ve izin doğrulaması; her ticari iletide ret / abonelikten çıkma; ret sonrası ticari gönderim yok; transactional mailde tanıtım dili yok; segmentasyon ve kişiselleştirme KVKK'ya uygun; footer'da gönderen kimliği; SPF, DKIM, DMARC, List-Unsubscribe; bounce ve liste hijyeni; gönderim ısıtma; "tereddütlü durumlarda hukuk veya KVKK ekibinden onay".

### 1.2 A sınıfı bilgiler (kurum düzeyinde bir kez verilen kararlar)

| # | Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|---|
| M1 | "Haftalık / Aylık Bülten … Hizmet Tanıtım Mailingi … Kampanya … Etkinlik / Webinar … Lead Magnet … Blog Derleme … Yeniden Pazarlama … Kurumsal Duyuru … Transactional / Bilgilendirme" | `mk_mail_types` — kısmi | Lead magnet, yeniden pazarlama, kurumsal duyuru seçenekleri yok. Transactional proje tarafında `mail_provider` (27) kuralında var — pazarlama türüne eklenmemeli. |
| M2 | "Kurumsal mailinglerde önerilen çalışma genişliği 600, 640 veya 660 px." | yok | Şablon genişliği kararı yok. |
| M3 | "Kritik kampanya ve CTA maillerinde tek kolon tercih edilir. Bültenlerde 2 kolon kullanılabilir ancak mobilde stack olmalıdır." | `mk_mail_layout` — tam | (Kural metni mobilde tek sütunu zaten söylüyor; "çok bölümlü" seçeneğine "masaüstünde en fazla 2 kolon" eklenebilir — §1.4.) |
| M4 | "Web-safe fontlar tercih edilmeli: Arial, Helvetica, Georgia, Times New Roman. Özel font varsa fallback tanımlanmalıdır." | yok (`brand_font_body` site fontu) | Mailde marka fontu mu, web-safe mi kararı yok. |
| M5 | "HTML mail ile birlikte sade metin versiyonu hazırlanmalı" | `mk_mail_formats` — kısmi | HTML + düz metin birlikte "önerilen" işaretli değil; PDF ek kılavuzda yok (bkz. §1.4). |
| M6 | "Gönderen Adı: Marka veya güvenilir kişi/marka kombinasyonu kullanılmalı." | yok | Gönderen adı biçimi kararı yok. |
| M7 | "Gönderen E-Posta: Kurumsal alan adı kullanılmalı. no-reply adresi yerine yanıt alınabilir adres tercih edilebilir." / "Takip ve müşteri yanıtları için aktif bir reply-to adresi tanımlanmalıdır." | `sender_domain` (27) alan adı için kısmi; `mk_mail_consent.identity` kısmi | Yanıtlanabilir (no-reply olmayan) adres kuralı yok. |
| M8 | "Emoji Kullanımı: Kurumsal B2B mailinglerde sınırlı kullanılmalı veya kullanılmamalıdır. Kampanya tonuna göre karar verilmelidir." | yok | Emoji politikası kararı yok. |
| M9 | "A/B Test: Konu başlığı, önizleme metni, CTA ve hero başlık için varyasyon testleri planlanabilir." | yok | A/B test edilecek öğeler kararı yok. |
| M10 | "CTA Bloku: Buton + kısa destek cümlesi + telefon." / "CTA alanında telefon numarası ayrı satırda veya destek cümlesinde verilmelidir." / her türde "CTA Standardı … \| Telefon: [TELEFON]" | yok | CTA bloğunda telefon olup olmayacağı kararı yok. |
| M11 | "UTM Source: newsletter, mailing, email …" / "UTM Medium: email" / "UTM Content: buton, hero, blog-card-1, footer gibi tıklama alanını ayırt etmek için" | `mk_utm.standard` — kısmi | E-postada `utm_source` değeri tanımsız ("kaynak = mecra"); `utm_content` kuralı "gönderi veya mail kimliği" diyor, kılavuz "tıklama alanı" diyor (§1.4). |
| M12 | "Ticari gönderimlerde İYS kayıt ve izin durumu … doğrulanmalıdır." / "Her ticari iletide kolay erişilebilir ret veya abonelikten çıkma" / "List-Unsubscribe" | `mk_mail_consent` (iys, unsub) — tam | — |
| M13 | "Bounce Yönetimi: Hard bounce adresleri listeden çıkarılmalı …" / "Liste Hijyeni: Pasif, hatalı veya izinsiz kayıtlar düzenli temizlenmelidir." / "Gönderim Isıtma: Yeni alan adı veya IP ile yüksek hacimli gönderim yapılacaksa kademeli artırma planı" | yok | `mk_mail_consent`'te seçenek olarak yok. |
| M14 | "SPF … DKIM … DMARC" | `sender_domain` (27) kuralı + `mk_mail_tool` ruleDetail — tam | — |
| M15 | "Gönderim Sıklığı: Segment ve içerik değerine göre planlanmalı" | `mk_mail_freq` — tam | — |
| M16 | "Footer: Şirket bilgisi, adres, telefon, web, sosyal ikonlar, yasal metin ve abonelikten çıkma bağlantısı." | `mk_mail_consent.identity` — kısmi | Kural var; ama veriler Ortak Bilgiler'den gelmiyor: `mk_mail` bölümünde `refs` yok (§1.4). |
| M17 | "24 saat, 48 saat ve 7 gün sonrası açılma, tıklama, dönüşüm, bounce, unsubscribe ve şikâyet metrikleri raporlanır." | `mk_measure_scope` — yok | E-posta metrikleri seçeneği yok. |
| M18 | "Bu kılavuz … KVKK, İYS, marka kimliği …" / "Kullanım: Pazarlama, Kurumsal İletişim, Tasarım, CRM ve Ajans Ekipleri" | `mk_roles` — kısmi | CRM / e-posta uzmanı rolü yok. |

### 1.3 Yeni alan önerileri — `mk_mail` (grup: Kanallar)

Mevcut bölümde 7 alan var. Önerilen 4 öncelikli alan (P1) ile bölüm 11 alana çıkar; P2 iki alan isteğe bağlıdır (eklenirse 13 — sınırın üstünde, ana asistan karar versin).

#### P1-a `mk_mail_width` [select] — "Şablon Genişliği" · showIf `mk_mail_on = true`
| Etiket | Değer | Ne zaman doğru (scenario) | Nasıl görünür (example) |
|---|---|---|---|
| 600 px (önerilen aralıkta) | `w600` | Çok bölümlü bülten ve geniş istemci uyumu gerektiğinde; kılavuzun önerdiği üç genişlikten en dar olanı. | Mail masaüstünde 600 px ortalanmış sütunda açılır; hero 600×250 px. |
| 640 px (önerilen aralıkta) | `w640` | Tek konulu tanıtım / kampanya maillerinde biraz daha geniş hero istendiğinde. | Hero 640×300 px, gövde 640 px. |
| 660 px (önerilen aralıkta) | `w660` | Görsel ağırlıklı kampanya ve etkinlik maillerinde. | Hero 660×320 px, gövde 660 px. |
| Geniş (700–800 px) | `wide` | Yalnız masaüstünde okunan kurumsal duyurularda; kılavuz 800 px'e kadar izin verir. | Gövde 700–800 px; mobilde tek sütuna düşer. |

Kılavuz üç genişliği eşit önerir; tek "(önerilen)" yok. Rule önerisi: "Mail şablonu {label} genişliğinde hazırlanır; hero görseli bu genişlikte (retina için 2x) üretilir; mobilde tek sütuna iner."
Kanıt: "Ana Gövde Genişliği: 600-800 px aralığı. Kurumsal mailinglerde önerilen çalışma genişliği 600, 640 veya 660 px." / "Hero Görsel: 600x250, 640x300 veya 660x320 px".

#### P1-b `mk_mail_from` [select] — "Gönderen Adı" · showIf `mk_mail_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Marka adı | `brand` | Kurumsal duyuru, bülten ve kampanyalarda alıcının markayı tanıması yeterliyse. | Gelen kutusunda gönderen: "Örnek Firma". |
| Kişi + marka | `person_brand` | Yeniden pazarlama, danışmanlık / B2B tanıtım maillerinde kişisel ton istendiğinde ("kısa ve kişisel ton kullanılabilir"). | Gönderen: "Ayşe Yılmaz · Örnek Firma". |

Kanıt: "Gönderen Adı: Marka veya güvenilir kişi/marka kombinasyonu kullanılmalı. Tanınmayan gönderici adı kullanılmamalıdır." Marka adı `mk_brand_name`'den alınır (Ortak Bilgiler).

#### P1-c `mk_mail_cta` [select] — "CTA Bloku" · showIf `mk_mail_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Buton + destek cümlesi + telefon (önerilen) | `button_phone` | Teklif, danışmanlık, etkinlik kaydı gibi telefonla da dönüşüm alınan maillerde; kılavuzun tüm tür şablonları bu yapıdadır. | "Teklif Alın" butonu, altında tek cümle ve "Telefon: 0212 …" satırı. |
| Yalnız buton | `button` | Dönüşümün yalnız sitede / formda ölçüldüğü e-ticaret ve içerik maillerinde. | Tek "Yazıyı Okuyun" butonu, telefon yok. |

Rule önerisi: "CTA metni 2–4 kelimelik eylem ifadesidir; birincil CTA tektir; telefon ayrı satırda Ortak Bilgiler'deki iletişim numarasıyla verilir." Kanıt: "CTA Bloku: Buton + kısa destek cümlesi + telefon." / "CTA Formatı: CTA: [CTA_METNİ] | Link: [CTA_LINK] | Telefon: [TELEFON_NUMARASI]" / "CTA Metni: 2-4 kelimelik aksiyon odaklı ifade".

#### P1-d `mk_mail_font` [select] — "Mail Yazı Tipi" · showIf `mk_mail_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Web-safe font (Arial, Helvetica, Georgia, Times New Roman) (önerilen) | `websafe` | Outlook dahil her istemcide aynı görünmesi gerektiğinde; kılavuzun varsayılanı. | Mail Arial ile açılır; her istemcide aynı. |
| Marka fontu + web-safe yedek | `brand_fallback` | Marka fontu (Ortak Bilgiler › Metin Fontu) mailde de taşınmak isteniyorsa; desteklemeyen istemcide yedeğe düşer. | Apple Mail'de marka fontu, Outlook'ta Arial görünür. |

Öneri bağlantısı: `recommend` gerekmez; `brand_fallback` seçiliyse kural `brand_font_body` değerini yazar. Kanıt: "Font Kullanımı: Web-safe fontlar tercih edilmeli … Özel font varsa fallback tanımlanmalıdır." / "Outlook render farklılıkları için … özel font … sınırlı kullanılmalıdır."

#### P2-a `mk_mail_emoji` [select] — "Emoji Kullanımı" · showIf `mk_mail_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kullanılmaz | `none` | Kurumsal B2B maillerinde. | Konu satırı ve gövde emojisiz. |
| Yalnız kampanya tonuna uygun maillerde sınırlı | `limited` | B2C kampanya maillerinde tona uyuyorsa. | Kampanya mailinin konu satırında tek emoji; bülten ve duyurularda yok. |
| Serbest | `free` | Genç / eğlence odaklı B2C markada. | Konu ve gövdede emoji kullanılabilir. |

`recommend: {field: "business_model", map: {b2b: ["none","limited"], b2g: ["none"]}}`. Kanıt: "Emoji Kullanımı: Kurumsal B2B mailinglerde sınırlı kullanılmalı veya kullanılmamalıdır. Kampanya tonuna göre karar verilmelidir." Not: SMS kılavuzu da emojiyi ayrı karara bağlıyor (§2.3 `mk_sms_charset`); ana asistan kanallar arası tek bir "Emoji Politikası" alanını `mk_creative`'e koymayı da düşünebilir.

#### P2-b `mk_mail_ab` [multiselect] — "A/B Testi" · showIf `mk_mail_on = true`
Seçenekler: Konu başlığı=`subject` · Önizleme metni=`preheader` · CTA metni=`cta` · Hero başlığı=`hero` · A/B testi yapılmaz=`none` (`exclusive: true`).
- subject — scenario: açılma oranı düşükse; example: listenin %20'sine iki konu satırı, kazanan kalana gider.
- preheader — scenario: konu satırı sabit kampanyada; example: iki önizleme metni denenir.
- cta — scenario: tıklama düşükse; example: "Teklif Alın" ↔ "Fiyatı Görün".
- hero — scenario: kampanya mesajı yeniyse; example: iki farklı hero başlığı.
- none — scenario: liste küçük ya da ESP desteklemiyorsa; example: tek sürüm gönderilir.
Kanıt: "A/B Test: Konu başlığı, önizleme metni, CTA ve hero başlık için varyasyon testleri planlanabilir."

### 1.4 Mevcut alanlarda değişiklik önerileri (Mailing)
1. **`mk_mail_types` seçenek ekle:** `lead_magnet` "Lead magnet (rehber / rapor indirme)" (ruleDetail: "CTA 'Dokümanı İndir'; doküman kapağı görselle gösterilir", kanıt 12.5; `mk_lead_magnet` true iken önerilebilir), `retargeting` "Yeniden pazarlama (önceki temasa hatırlatma)" (kanıt 12.6 "Hatırlatma > fayda > sosyal kanıt > kolay aksiyon"; ruleDetail: yalnız izinli alıcıya), `announcement` "Kurumsal duyuru" (kanıt 12.7 "Duyuru başlığı > açıklama > etki > detay linki"). Transactional'ı **ekleme**: `mail_provider` kuralı işlemsel maili zaten ayırıyor.
2. **Tür başına içerik akışı ruleDetail'leri** (kılavuz 12.x, mevcut ruleDetail'lerin sonuna): newsletter "Logo > kısa giriş > 3-5 içerik kartı > ana CTA > footer"; product "Hero > problem > çözüm > 3 fayda > güven kanıtı > CTA"; campaign "Kanca > kampanya değeri > şartlar > CTA > son tarih"; event "Etkinlik başlığı > tarih/saat > konuşmacı > kazanımlar > kayıt CTA".
3. **`mk_mail_formats`:** HTML ve Düz metin etiketine "(önerilen)" ekle ya da açıklamada birlikte seçilmesini öner — "HTML mail ile birlikte sade metin versiyonu hazırlanmalı". PDF ek kılavuzda geçmiyor; basın bülteni kılavuzu da "Ağır dosya yerine … link kullanılmalıdır" diyor — PDF ek seçeneği kalsın ama önerilmesin.
4. **`mk_mail_consent` seçenek ekle** (etiket "İzin, Uyum ve Teslim Edilebilirlik" olabilir): `reply_to` "Yanıtlanabilir gönderen adresi (no-reply yok)" (kanıt M7), `hygiene` "Bounce ve liste hijyeni" (ruleDetail: "hard bounce adresleri listeden çıkarılır, soft bounce izlenir; pasif ve izinsiz kayıtlar düzenli temizlenir", kanıt M13), `warmup` "Yeni alan adı / IP için kademeli ısıtma" (kanıt M13).
5. **`mk_mail_layout.multi` ruleDetail'ine ekle:** "masaüstünde en fazla 2 kolon, mobilde alt alta" (kanıt M3).
6. **`mk_mail` bölümüne `refs` ekle** (Ortak Bilgiler kartı): `mk_brand_name`, `oc_legal_name`, `mk_contact`, `oc_logo`, `domain_name`, `mk_accounts`, `brand_color_accent`, `brand_font_body` — kanıt "Footer: Şirket bilgisi, adres, telefon, web, sosyal ikonlar, yasal metin".
7. **`mk_utm.standard` ruleDetail düzelt:** e-postada `utm_source=newsletter` (bülten) / `mailing` (diğer), `utm_medium=email`, `utm_campaign` = kampanya adı + tarih ya da brief no, `utm_content` = tıklama alanı (`hero`, `button`, `blog-card-1`, `footer`). Mevcut metin "utm_content gönderi veya mail kimliğini taşıyacak" diyor; e-posta için kılavuzla çelişiyor. Kanıt: "UTM Source: newsletter, mailing, email …" / "UTM Campaign: kampanya adı, tarih veya brief no ile standartlaştırılmalıdır." / "UTM Content: buton, hero, blog-card-1, footer gibi tıklama alanını ayırt etmek için".
8. **`mk_measure_scope` seçenek ekle:** `email` "E-posta metrikleri (açılma, tıklama, dönüşüm, bounce, abonelikten çıkma, şikâyet)" — ruleDetail: "her gönderim için 24 saat, 48 saat ve 7 gün sonra ölçülür". Kanıt M17.
9. **`mk_roles` seçenek ekle:** `crm` "CRM / e-posta pazarlama uzmanı" (kanıt M18; SMS kılavuzu da "Pazarlama, CRM … ekipleri").

### 1.5 B sınıfı brief alanları (form alanı değil)
Mailing No / Kampanya Kodu · Marka / Şirket · Mailing Türü · Hedef Kitle / Segment · Gönderim Amacı · Ana Mesaj · Teklif / Fayda · CTA · CTA Linki · Telefon (yalnız bu mailde farklıysa) · Gönderim Tarihi / Saati · Liste / Segment (ESP / CRM liste adı) · UTM Parametreleri · Onay Durumu (İYS / izinli alıcı / işlem bildirimi) · konu başlığı ve önizleme metni · hero başlık / açıklama · fayda maddeleri · etkinlik bilgileri (tarih, saat, format, konuşmacı) · içerik kartları (blog başlığı, özet, link).
Bunun için ayrı "Mail Brief Alan Seti" alanı önermiyorum: `mk_brief_format` (55) brief biçimini zaten seçtiriyor; ana asistan istersen `mk_brief_format`'ın kural metnine "mailing brief'i kılavuzdaki 14 alanı içerir" eklenebilir.

### 1.6 C sınıfı ilkeler (kural / rehber metnine)
1. Konu başlığı 35–55 karakter, kritik mesaj ilk 35 karakterde; önizleme metni 70–120 karakter ve konuyu tekrar etmez; tamamı büyük harf ve spam tetikleyici ifade yok.
2. İlk 400–600 px'te logo, ana başlık, değer önerisi ve CTA görünür; mail tek büyük görselden oluşmaz, başlık / CTA / kritik bilgi canlı metindir.
3. Tablo tabanlı HTML, kritik CSS inline, dış CSS yok; Outlook için arka plan görseli, border-radius ve gelişmiş CSS sınırlı.
4. Gövde metni 15–16 px (mobilde 16), başlık 22–32 px, satır yüksekliği 1.4–1.6, bloklar arası 16–32 px; CTA butonu en az 44 px yüksek.
5. Mail görselleri sitenin görsel formatından bağımsız olarak JPG / PNG / GIF, RGB, tek görsel ideal 100–300 KB (en çok 1 MB); dosya adı küçük harf, tireli, Türkçe karaktersiz; base64 görsel yok (Gmail kırpması).
6. Logo mailde PNG, 120–220 px; şeffaf logo varsa dark mode için alternatif sürüm (`brand_logo_variants` Dark).
7. Animasyonlu GIF'te mesaj ilk karede anlaşılır (Outlook ilk kareyi gösterir).
8. Tüm linkler HTTPS ve UTM'li; CTA, logo, görsel, telefon ve çıkış linki gönderim öncesi test edilir.
9. Kişiselleştirme alanları (ad, şirket, sektör) hatalı / boş veri riskine karşı test edilir.
10. Gönderim öncesi Gmail, Outlook, Apple Mail, mobil ve dark mode testi; test gönderimi ilgili ekiplerce onaylanır; işlemsel mailde tanıtım dili kullanılmaz.

---

## 2. SMS İçeriği Oluşturma Kılavuzu

### 2.1 Özet
- **Amaç:** "SMS kampanyalarının kurumsal dil, teknik limitler, izin yönetimi, CTA ve ölçüm standartlarına uygun üretilmesini sağlamak." Kapsam: ticari SMS, bilgilendirme, etkinlik hatırlatma, kampanya, lead toplama, OTP / işlem bildirimi, müşteri ilişkileri, servis duyuruları.
- **Bölümler:** 1 Amaç · 2 Strateji (tek ana fikir, tek aksiyon) · 3 Türler (7 tür) · 4 Hukuki Uyum, İYS, KVKK · 5 Teknik Standartlar · 6 Gönderici Adı · 7 Yazım Standardı · 8 CTA, Telefon, Link · 9 Segmentasyon ve Kişiselleştirme · 10 Şablonlar (8 şablon) · 11 Zamanlama ve Frekans · 12 A/B Test · 13 Ölçümleme · 14 Yayın Öncesi Kontrol · 15 Arşiv, Dosya Adı, Versiyon · 16 Kaynaklar (iys.org.tr, ticaret.gov.tr, Twilio, Netgsm).
- **Sayısal standartlar:** GSM-7 tek parça 160 karakter, çok parçalıda parça başı ~153; UCS-2 (emoji / GSM-7 dışı karakter) tek parça 70, çok parçalıda ~67; ideal ticari SMS 120–155 karakter; ana değer ilk 8–12 kelimede; kanca 25–45, fayda 40–70, CTA 15–35 karakter; alfanumerik gönderici adı 11 karakter; gönderim saati 10:00–17:00; tarih / saat biçimi "24.06.2026 / 14:00"; A/B'de 100–120 ↔ 140–155 karakter.
- **Süreç:** strateji (amaç, segment, ana mesaj, aksiyon, kanal devamı) → metin (kanca + fayda + CTA + link / telefon + ret notu) → teknik kontrol (karakter, parça, Türkçe karakter, emoji) → uyum (İYS izin / ret) → test SMS (kritik kampanyada zorunlu) → onay kaydı (kişi, tarih, versiyon) → gönderim → ölçüm → arşiv (`[MARKA]_[KAMPANYA]_[SMS_TURU]_[TARIH]_v01`).
- **Uyum:** İYS izin ve ret kontrolü, izin yoksa ticari SMS yok; önceden onay; ret hakkı açık ve sağlayıcı / İYS ile uyumlu; KVKK — gereksiz / hassas kişisel veri, tam kimlik, üçüncü kişi bilgisi yok; amaç sınırlılığı; gönderim listesi, izin durumu, metin, tarih, kampanya ID ve rapor arşivlenir; OTP'de pazarlama cümlesi yok; resmî kurum izlenimi veren / manipülatif aciliyet dili yok; "Bu kılavuz hukuki görüş yerine geçmez".

### 2.2 A sınıfı bilgiler

| # | Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|---|
| S1 | "Ticari SMS, bilgilendirme SMS'i, etkinlik hatırlatma, kampanya, lead toplama, OTP/işlem bildirimi, müşteri ilişkileri ve servis duyuruları." | yok | SMS bölümü yok. |
| S2 | "Gönderici adı: Kısa, marka ile ilişkili … Alfanumerik sender ID uygulamalarında 11 karakter sınırı yaygındır." | yok | — |
| S3 | "Emoji kullanımı: Kurumsal SMS'lerde önerilmez." / "Türkçe karakter … Unicode veya özel Türkçe kodlama doğurabilir. Kritik kampanyalarda SMS sayacıyla test edilmelidir." | yok | Karakter / kodlama politikası yok. |
| S4 | "Ticari ve kampanya SMS'lerinde ideal uzunluk 120-155 karakterdir." | yok | Hedef uzunluk / parça kararı yok. |
| S5 | "Standart CTA Formatı: CTA: [CTA_METNI]: [KISA_LINK] \| Telefon: [TELEFON_NUMARASI]" / "Çift CTA: Hem form hem telefon üzerinden dönüşüm alınmak istendiğinde." | yok | CTA yapısı kararı yok. |
| S6 | "Kısaltılmış link güven problemi yaratıyorsa marka domainli kısa link kullanılmalıdır." | yok | Kısa link kararı yok. |
| S7 | "B2B içeriklerde hafta içi mesai saatleri tercih edilmelidir." / "Genel kurumsal kullanımda 10:00-17:00 aralığı daha güvenli kabul edilir." | yok | Gönderim saati penceresi yok. |
| S8 | "Frekans: … Kampanya frekans sınırı önceden belirlenmelidir." / "ilk duyuru + hatırlatma + son gün modeli" | yok | Frekans sınırı yok. |
| S9 | "İYS izin kontrolü … Ret hakkı … KVKK uyumu … Kayıt ve denetim" | `member_consents.Marketing` (31) yalnız kayıt formunda; `mk_mail_consent` yalnız e-posta | SMS için izin / uyum kararı yok. |
| S10 | "Telefon ekleme / Link konumu / Gönderim zamanı … Her testte tek değişken izole edilmelidir." | yok | A/B — C sınıfı ilke olarak kalsın (alan önermiyorum). |
| S11 | "Teslim oranı … Tıklama oranı … Arama oranı … Ret oranı … Segment maliyeti … Dönüşüm başı maliyet" | `mk_measure_scope` — yok | SMS metrikleri seçeneği yok. |
| S12 | "Onay kaydı: Pazarlama, hukuk/KVKK, ilgili iş birimi veya kampanya sahibi onayı kayıt altına alınmalıdır." | `mk_flow`, `mk_flow_log`, `mk_approvers` — tam | — |
| S13 | "Mevzuat yorumu gerektiren gönderimlerde hukuk/KVKK veya ilgili danışman kontrolü alınmalıdır." | `mk_legal_scope` — kısmi | "Ticari elektronik iletiler (e-posta, SMS)" kapsamı yok. |
| S14 | "Etkinlik SMS'i … Hatırlatma SMS'i" | `mk_evt_channels` — kısmi | Etkinlik duyuru kanallarında SMS yok. |
| S15 | "OTP / Doğrulama SMS'i … Kod görünür olmalı; pazarlama cümlesi eklenmemelidir." | `member_login_methods.PhoneOTP`, `member_2fa_methods.SMS`, `member_password_reset.Code` (31) — kısmi | SMS metin kuralı yok. |
| S16 | "Dosya adı: [MARKA]_[KAMPANYA]_[SMS_TURU]_[TARIH]_v01" | yok | C sınıfı say (ya da kanallar arası "dosya adlandırma" alanı — ana asistan diğer kılavuzlarla birleştirsin). |

### 2.3 Yeni bölüm: `mk_sms` — "SMS" (grup: **Kanallar**, `mk_mail`'den hemen sonra; kodlar yeniden numaralanır)

Bölüm açıklaması önerisi: "Ticari ve bilgilendirme SMS'lerinin gönderici adı, karakter, CTA, gönderim saati, frekans ve İYS kurallarını belirler." `refs`: `mk_brand_name`, `mk_contact`, `domain_name`, `business_model`. Toplam 10 alan.

#### `mk_sms_on` [boolean] — "SMS Pazarlaması"
- yes — scenario: kampanya, hatırlatma veya etkinlik duyurusu SMS'le gönderilecekse; example: İYS izinli müşterilere "[MARKA]: … Detay: [KISA_LINK] | Tel: [TELEFON]" biçiminde SMS gider.
- no — scenario: SMS kanalı kullanılmıyorsa; example: SMS kuralları promptta yer almaz (OTP / işlem SMS'leri proje kararlarındaki üyelik kurallarıyla yönetilir).
Kanıt: "SMS; düşük dikkat süresi, sınırlı karakter alanı ve doğrudan erişim gücü nedeniyle içerik disiplini en yüksek kanallardan biridir."

#### `mk_sms_types` [multiselect] — "SMS Türleri" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Ticari / kampanya | `campaign` | Teklif, kampanya, hizmet tanıtımı. | "[MARKA]: [HIZMET] için avantajlı teklifinizi alın. Detay: [KISA_LINK] \| Tel: [TELEFON]" |
| Bilgilendirme | `info` | Mevzuat, hizmet, operasyon duyurusu; satış dili azaltılır. | "[MARKA]: [KONU] hakkında yeni bilgilendirme yayında. İnceleyin: [KISA_LINK]" |
| Etkinlik duyurusu | `event` | Webinar, eğitim, lansman; tarih, saat, kayıt linki zorunlu. | "[MARKA]: [ETKINLIK_ADI] [TARIH] [SAAT] tarihinde. Kayıt: [KISA_LINK]" |
| Hatırlatma (randevu, etkinlik, son başvuru, ödeme) | `reminder` | Zaman bilgisi ilk satırda. | "[MARKA]: [TARIH] [SAAT] randevunuzu hatırlatırız. Değişiklik için: [TELEFON]" |
| OTP / doğrulama | `otp` | Tek kullanımlık şifre; pazarlama cümlesi yok. | "[MARKA] doğrulama kodunuz: [KOD]. Güvenliğiniz için bu kodu kimseyle paylaşmayın." |
| Servis / işlem bildirimi | `service` | Sipariş, kayıt, başvuru, destek talebi durumu. | "[MARKA]: başvurunuz alındı, sonraki adım: …" |
| Müşteri ilişkileri / anket | `survey` | Memnuniyet, geri bildirim; kibar ve kısa. | "[MARKA]: Deneyiminizi 1 dakikada değerlendirin. Anket: [KISA_LINK]" |
ruleDetail önerisi: `otp` ve `service` — "İYS izni gerektirmeyen işlem iletisidir; tanıtım ve kampanya cümlesi eklenmez" (kanıt: "OTP … pazarlama cümlesi eklenmemelidir", "Bilgilendirme veya işlem temelli SMS'lerde de kişisel veri minimizasyonu"). Kanıt tablo: Bölüm 3 ve 10.

#### `mk_sms_sender` [text] — "Gönderici Adı (SMS Başlığı)" · showIf `mk_sms_on = true`
ph: "Örn. ORNEKFIRMA (en çok 11 karakter)". Yumuşak doğrulama: 11 karakteri aşarsa uyarı (`re` / not). scenario: sağlayıcıda kayıtlı alfanumerik başlık; example: alıcının telefonunda gönderen "ORNEKFIRMA" görünür. Kanıt: "Gönderici adı: Kısa, marka ile ilişkili, kolay tanınan ve sağlayıcı/operatör kurallarıyla uyumlu olmalıdır. Alfanumerik sender ID uygulamalarında 11 karakter sınırı yaygındır." / "Netgsm … 11 karakter sınırı".

#### `mk_sms_charset` [select] — "Karakter ve Emoji Politikası" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Türkçe karakterli, emojisiz (sağlayıcı sayacıyla test) | `tr_noemoji` | Metnin doğru Türkçeyle okunması öncelikliyse; parça sayısı her gönderimde sayaçla kontrol edilir. | "Randevunuzu hatırlatırız" — ğ, ş, ı korunur; sayaç 1 ya da 2 parça gösterir. |
| Türkçe karakter yerine Latin harf (GSM-7, tek parça 160) | `latin` | Maliyet ve tek parça önceliklidir; yüksek hacimli kampanyada. | "Randevunuzu hatirlatiriz" — 160 karaktere kadar tek SMS. |
| Emoji serbest (UCS-2, tek parça 70) | `emoji` | Kılavuz kurumsal SMS'te önermez; yalnız B2C eğlence markasında bilinçli tercih. | Mesaj 70 karakteri geçince parçalanır. |
Kılavuz emojiyi açıkça önermiyor ("Kurumsal SMS'lerde önerilmez"); ilk iki seçenek arasında tercih belirtmiyor → "(önerilen)" yalnız emojisiz seçeneklerin ikisine birden "kılavuza uygun" notu olarak verilebilir. Kanıt: Bölüm 5 tablosu.

#### `mk_sms_length` [select] — "Hedef Uzunluk" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Tek parça, 120–155 karakter (önerilen) | `single` | Ticari ve kampanya SMS'lerinin varsayılanı. | Kanca + fayda + CTA + link tek SMS'e sığar. |
| Kısa, 100–120 karakter | `short` | Hatırlatma ve OTP gibi tek bilgi taşıyan mesajlarda; A/B testinde kısa sürüm. | "[MARKA]: 24.06.2026 14:00 randevunuz. Değişiklik: [TELEFON]" |
| En çok 2 parça | `two` | Bilgilendirme gibi açıklama gerektiren mesajlarda; maliyet iki katı. | GSM-7'de en çok 306, UCS-2'de 134 karakter. |
Kanıt: "Maksimum önerilen uzunluk: Ticari ve kampanya SMS'lerinde ideal uzunluk 120-155 karakterdir." / "GSM-7 çok parçalı mesajlarda bölüm başına yaklaşık 153 karakter; UCS-2 … yaklaşık 67" / A/B "100-120 karakterlik kısa metin vs. 140-155".

#### `mk_sms_cta` [select] — "CTA Yapısı" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kısa link + telefon (önerilen) | `dual` | Hem form hem telefondan dönüşüm alınacaksa; kılavuzun standart formatı. | "Teklif: [KISA_LINK] \| Tel: [TELEFON]" |
| Yalnız kısa link | `link` | Dönüşüm sitede / formda; blog, kayıt sayfası. | "Detay: [KISA_LINK]" |
| Yalnız telefon | `phone` | Teklif, randevu, çağrı merkezi yönlendirmesi. | "Bilgi: [TELEFON]" |
Kanıt: "Standart CTA Formatı: CTA: [CTA_METNI]: [KISA_LINK] | Telefon: [TELEFON_NUMARASI]" / Bölüm 8 tablo (Web, Telefon, Çift CTA).

#### `mk_sms_link` [select] — "Kısa Link" · showIf `mk_sms_on = true` ve `mk_sms_cta in [dual, link]`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Marka alan adlı kısa link (önerilen) | `brand_domain` | Güven ve tanınırlık; kılavuzun tercihi. | "ornk.co/kampanya" ya da "ornekfirma.com/k/..." |
| Genel kısaltma servisi | `shortener` | Marka kısa alan adı yoksa; güven riski kabul edilir. | "bit.ly/..." |
| Tam sayfa adresi | `full` | Adres zaten kısaysa. | "ornekfirma.com/teklif" |
ruleDetail (hepsine): "Link takip parametresi (UTM) taşır ve gönderim öncesi test edilir." Kanıt: "Link kullanımı: Kısa, güvenilir, marka ile ilişkili ve takip parametresi içeren link tercih edilmelidir. Kısaltılmış link güven problemi yaratıyorsa marka domainli kısa link kullanılmalıdır." / "Güven unsuru: Link domaini, telefon numarası ve marka adı aynı kurumsal evrende görünmelidir."

#### `mk_sms_hours` [select] — "Gönderim Zamanı" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Hafta içi 10:00–17:00 | `weekday` | B2B içerikler. | Pazartesi–Cuma 10:00–17:00 arası gönderilir. |
| Her gün 10:00–17:00 (önerilen genel kurumsal) | `daily` | B2C kampanyalarda genel güvenli pencere. | Cumartesi 11:00'de kampanya SMS'i. |
| Sektöre özel pencere | `custom` | B2C'de sektör ve izin politikası farklı saat gerektiriyorsa (saat proje notuna yazılır). | Restoran: 11:00–12:00 öğle kampanyası. |
Tüm seçeneklere ruleDetail: "Acil işlem bildirimleri ve OTP bu pencereye bağlı değildir." `recommend: {field: "business_model", map: {b2b: ["weekday"], b2g: ["weekday"], b2c: ["daily","custom"], b2b2c: ["daily"]}}`. Kanıt: "Gönderim günü: B2B içeriklerde hafta içi mesai saatleri tercih edilmelidir. B2C kampanyalarda sektör ve izin politikasına göre planlama yapılmalıdır." / "Gönderim saati: Genel kurumsal kullanımda 10:00-17:00 aralığı daha güvenli kabul edilir. Acil işlem bildirimleri bunun dışında olabilir."

#### `mk_sms_freq` [select] — "Frekans Sınırı" · showIf `mk_sms_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kampanya başına ilk duyuru + hatırlatma + son gün | `campaign3` | Son tarihli kampanya, etkinlik, başvuru. | Aynı kampanyada en çok üç SMS; davranışa göre güncellenmiş metin. |
| Haftada en çok 1 ticari SMS | `w1` | Düzenli kampanya yapan B2C markası. | Aynı alıcıya haftada tek ticari SMS. |
| Ayda en çok 2 ticari SMS | `m2` | B2B ya da düşük frekanslı iletişim. | Ayda iki SMS. |
Uyarı: kılavuz yalnız "frekans sınırı önceden belirlenmelidir" diyor, **sayısal değer vermiyor**; `w1` / `m2` değerleri kılavuzdan değil, seçenek olabilmek için önerildi (ana asistan isterse `text` alanına çevirebilir). `campaign3` doğrudan kılavuzdandır. Kanıt: "Frekans: Aynı segmente kısa aralıklarla tekrar gönderim yapılmamalıdır. Kampanya frekans sınırı önceden belirlenmelidir." / "ilk duyuru + hatırlatma + son gün modeli" / "Tekrarlı gönderim: … davranışa göre güncellenmiş metin kullanılmalıdır."

#### `mk_sms_consent` [multiselect] — "İzin ve Uyum" · showIf `mk_sms_on = true` · `jump` → `privacy_regime`
| Etiket | Değer | ruleDetail (kılavuzdan) |
|---|---|---|
| İYS izin ve ret sorgusu (önerilen) | `iys` | "Ticari SMS gönderimi öncesinde alıcının ilgili kanaldaki izin ve ret durumu kontrol edilmelidir. İzin yoksa ticari içerikli SMS gönderilmemelidir." |
| Ret mekanizması her ticari SMS'te (önerilen) | `optout` | "Ret yöntemi SMS sağlayıcısı ve İYS süreçleriyle uyumlu belirlenmelidir." |
| Kişisel veri en aza indirilir | `minimal` | "SMS içeriğinde gereksiz kişisel veri, hassas veri, tam kimlik bilgisi veya üçüncü kişilerin bilgisi kullanılmamalıdır." |
| Gönderim kaydı ve arşiv | `archive` | "Gönderim listesi, izin durumu, metin versiyonu, tarih/saat, kampanya ID ve rapor çıktıları arşivlenmelidir." |
| Kritik kampanyada test SMS zorunlu | `test` | "Kritik kampanyalarda test gönderimi zorunludur." |
scenario / example her seçenek için kılavuz cümlesinden: ör. `iys` — scenario: her ticari SMS; example: izni olmayan numara listeden otomatik düşer. Kural sonu: "Bu kurallar hukuki görüş yerine geçmez; mevzuat yorumu gereken gönderimde hukuk / KVKK görüşü alınır."

(İsteğe bağlı 11. alan: `mk_sms_tool` [text] "SMS Sağlayıcısı" — kılavuz yalnız Netgsm ve Twilio'yu kaynak olarak anıyor; sağlayıcı listesi uydurmamak için `select` yerine `text`. Bölüm sınırı nedeniyle P2.)

### 2.4 Mevcut alanlarda değişiklik önerileri (SMS)
1. **`mk_evt_channels`** seçenek ekle: `sms` "SMS" — ruleDetail: "Etkinlik SMS'inde tarih, saat ve kayıt linki bulunur; hatırlatma ilk satırda zamanı verir; SMS bölümündeki izin ve saat kurallarına uyar." Kanıt: "Etkinlik SMS'i … Tarih, saat, kayıt linki ve kısa değer vaadi zorunludur." / "Hatırlatma SMS'i … Zaman bilgisi ilk satırda verilmeli". `showIf` gerekirse `mk_sms_on`.
2. **`mk_measure_scope`** seçenek ekle: `sms` "SMS metrikleri (teslim, tıklama, arama, form, ret, parça maliyeti)" — ruleDetail: "dönüşüm başı maliyet = toplam kampanya maliyeti / nitelikli dönüşüm". Kanıt: Bölüm 13 KPI tablosu.
3. **`mk_utm.standard`** ruleDetail'ine SMS ekle: "SMS bağlantılarında `utm_medium=sms`". (Kılavuz "takip parametresi" ve "UTM" diyor ama değeri yazmıyor — `sms` değeri çıkarımdır.) Kanıt: "Tıklama oranı: Kısa link veya UTM üzerinden ölçülen tıklama oranı."
4. **`mk_legal_scope`** seçenek ekle: `commercial_msg` "Ticari elektronik iletiler (e-posta, SMS)" — ruleDetail: "İzin, ret ve içerik niteliği tereddütlü gönderimler gönderimden önce hukuk / KVKK görüşüne gider." Kanıt (SMS): "Mevzuat yorumu gerektiren gönderimlerde hukuk/KVKK veya ilgili danışman kontrolü alınmalıdır."; (Mailing): "tereddütlü durumlarda hukuk veya KVKK ekibinden onay alınmalıdır."
5. **`member_login_methods.PhoneOTP`, `member_2fa_methods.SMS`, `member_password_reset.Code`** (31, proje) ruleDetail ekle: "SMS kodu metni yalnız marka adı, kod ve 'bu kodu kimseyle paylaşmayın' uyarısı içerir; pazarlama cümlesi eklenmez." Kanıt: "OTP / Doğrulama SMS'i … Kod görünür olmalı; pazarlama cümlesi eklenmemelidir. Güvenlik uyarısı kısa tutulmalıdır." ve şablon "[MARKA] doğrulama kodunuz: [KOD]. Güvenliğiniz için bu kodu kimseyle paylaşmayın."
6. **`mk_roles`** — `crm` önerisi (§1.4-9) SMS için de geçerli ("Pazarlama, CRM, içerik …").

### 2.5 B sınıfı brief alanları
Ana amaç (lead / hatırlatma / bilgilendirme / satış / randevu / etkinlik / doğrulama) · hedef segment (müşteri tipi, hizmet ilgisi, lokasyon, davranış) · ana mesaj · tek aksiyon · kanal devamı (web sayfası, form, çağrı merkezi, WhatsApp, kayıt sayfası, müşteri paneli) · kişiselleştirme değişkenleri (ad, şirket, randevu tarihi, başvuru no) · kampanya ID / adı · kısa link · telefon (farklıysa) · gönderim tarihi / saati · A/B test değişkeni · onay veren kişi, tarih, versiyon.

### 2.6 C sınıfı ilkeler
1. Her SMS tek konu ve tek CTA içerir; ana değer ilk 8–12 kelimede.
2. Metin yapısı: kanca (25–45 karakter) + fayda (40–70) + CTA (15–35) + link / telefon + gerekiyorsa ret notu; mesaj "[MARKA]:" ile başlar (şablonların tamamı).
3. Karakter sayısı ve parça adedi her gönderimde sağlayıcı sayacıyla hesaplanır; satır sonları karaktere dahildir, çok satır yalnız okunabilirlik için.
4. Tamamı büyük harf yok (yalnız marka adı / kısa vurgu); aşırı ünlem, baskı dili, kesin sonuç vaadi, manipülatif aciliyet yok.
5. Resmî kurum izlenimi veren ya da kampanyayı olduğundan farklı gösteren ifade yok.
6. Tarih / saat biçimi "24.06.2026 / 14:00"; kısaltma anlam kaybı yaratmaz.
7. Link domaini, telefon ve marka adı aynı kurumsal evrende görünür (gönderici adı = SMS içindeki marka adı = web / çağrı merkezi dili).
8. Kişiselleştirme değişkenleri boş değişken riskine karşı test edilir; tüm hizmetler tek SMS'e sıkıştırılmaz.
9. A/B testinde tek değişken (kanca, CTA, link konumu, telefon ekleme, saat, uzunluk) izole edilir.
10. Arşiv: dosya adı `[MARKA]_[KAMPANYA]_[SMS_TURU]_[TARIH]_v01`, versiyonlar v01 / v02 / final; arşivde metin, segment, tarih, gönderici adı, link, telefon, izin notu, rapor.

---

## 3. Basın Bülteni Oluşturma Kılavuzu

### 3.1 Özet
- **Amaç:** "Haber değeri net, dili sade, verisi doğrulanmış, kaynağı belli ve aksiyonu açık bir kurumsal içerik üretmek." Çıktılar: "Basın bülteni metni, medya kit dosyaları, e-posta pitch metni, web haber metni ve sosyal medya uyarlamaları".
- **Bölümler:** 1 Amaç ve Kapsam (üretim, medya dağıtımı, dijital PR, teknik kontrol) · 2 Türler (6 tür) · 3 Bilgi Toplama Formu · 4 İçerik Mimarisi (ters piramit) + 4.1 iskelet · 5 Yazım Dili · 6 Teknik Format · 7 Görsel / Video / Medya Asset · 8 SEO ve Dijital PR · 9 E-posta Pitch ve Dağıtım + 9.1 şablon · 10 Hukuki, KVKK, Marka · 11 Yayınlama Süreci (8 adım) · 12 Dosya İsimlendirme · 13 Performans Ölçümü · 14 Final Checklist · 15 Kalite Standardı · 16 Kısa Brief Özeti.
- **Türler:** Kurumsal duyuru · Ürün / hizmet lansmanı · Etkinlik / webinar · Araştırma / rapor · İş birliği / ortaklık · Kriz / açıklama.
- **Sayısal standartlar:** başlık 55–90 karakter; spot 120–220 karakter; giriş 40–70 kelime; gövde 3–6 paragraf, paragraf ortalama 50–80 kelimeyi aşmaz; alıntı 25–60 kelime; boilerplate 70–120 kelime; Word A4 dikey, 2–2,5 cm kenar, Aptos / Arial / Calibri 10–11 punto; PDF seçilebilir metin, 5 MB altı; ana görsel 1200×675 / 1920×1080 px (16:9); basın fotoğrafı en az 2000 px, 300 dpi; video MP4 / H.264 / 1080p, kısa sürüm 30–60 sn; URL slug 30–75 karakter; meta title 35–60; meta description 120–160; OG 1200×630 / 1200×675; pitch konu başlığı 45–75 karakter; ilk 2 cümlede önem; takip 24–48 saat sonra.
- **Süreç (Bölüm 11):** brief → taslak → içerik, marka, hukuk / teknik, yönetim onayları → medya kit ve asset → pitch metni ve medya listesi → yayın tarihi, saat, ambargo, takip planı → gönderim + web haber sayfası + sosyal uyarlamalar → yansıma ve geri dönüş takibi.
- **Uyum:** kişisel veri (ad, fotoğraf, unvan, müşteri bilgisi, alıntı) izinleri; telif; finansal iddialar onaylı veriyle; müşteri / iş ortağı adı için yazılı onay; kriz riski (rakibi hedef alan, regülasyon riski taşıyan ifade çıkarılır); ambargo tarih-saat-saat dilimi üst bilgide; süperlatifler yalnız doğrulanabiliyorsa; kriz bülteninde "tek sözcü, hukuki kontrol".

### 3.2 A sınıfı bilgiler

| # | Kılavuzdan alıntı | Mevcut karşılık | Eksik |
|---|---|---|---|
| P1 | "Kurumsal Duyuru … Ürün / Hizmet Lansmanı … Etkinlik / Webinar … Araştırma / Rapor … İş Birliği / Ortaklık … Kriz / Açıklama Bülteni" | yok | Basın bülteni bölümü yok. |
| P2 | "Basın İletişim: Ad, unvan, e-posta, telefon — Medyanın hızlı teyit alabileceği net iletişim alanı." | `mk_contact` (77) — kısmi | Genel iletişim var; basın iletişim kişisi (ad, unvan) ayrı tanımlı değil. |
| P3 | "Boilerplate: 70-120 kelime. Şirket hakkında standart, güncel ve onaylı kurumsal bilgi." | `oc_tagline` (77) — kısmi | Kısa tanıtım var; 70–120 kelimelik onaylı "Kurum hakkında" metni yok. |
| P4 | "Kriz / Açıklama Bülteni … Net pozisyon, doğrulanmış bilgi, tek sözcü, hukuki kontrol" / "Sözcü / Alıntı Sahibi: [Ad soyad, unvan, kurum]" / "Sözcü portresi … Ad-soyad, unvan ve kullanım izni bilgisi eklenmelidir." | yok | Onaylı sözcü listesi yok (her bültenin alıntı sahibi B; kimlerin sözcü olabileceği A). |
| P5 | "Çıktı Formatı: Basın bülteni metni, medya kit dosyaları, e-posta pitch metni, web haber metni ve sosyal medya uyarlamaları" / "web newsroom süreçleri" | yok | Hangi çıktıların üretileceği kararı yok. |
| P6 | "Medya kiti: Logo, fotoğraf, görsel, video, infografik, rapor, sözcü biyografisi ve basın iletişim bilgisi linkle paylaşılmalıdır." | `brand_deliverables.LogoPack` (01) — kısmi | Medya kiti bileşenleri kararı yok. |
| P7 | "Web yayınında uygun ise NewsArticle veya Article yapılandırılmış veri değerlendirilmelidir." | `schema_types` — kısmi | `NewsArticle` seçeneği yok. |
| P8 | "Onay Sahipleri: [İçerik / marka / hukuk / yönetim / teknik onay]" / "İçerik, marka, hukuk/teknik ve yönetim onayları alınır." | `mk_flow`, `mk_approvers` — kısmi | Kurumsal iletişim rolü yok; diğerleri `marketing_manager`, `owner`, `legal`, `product_owner` ile yaklaşık karşılanıyor. |
| P9 | "Finansal iddia … onaylı veriyle desteklenmelidir." / "Kriz riski: … regülasyon riski taşıyan ifadeler çıkarılmalıdır." | `mk_legal_scope` — kısmi | Basın bülteni / kamuoyu açıklaması kapsamı yok. |
| P10 | "Süperlatif: 'En iyi', 'tek', 'ilk', 'lider' gibi ifadeler yalnızca doğrulanabiliyorsa" / "Müşteri adı … yazılı onay" / "Telif" | `mk_banned` (superlative, client_logo, copyright), `mk_legal_scope.personal_data` — tam | — |
| P11 | "Medya yansıması … Dijital etki … SEO etkisi (Backlink …) … Niteliksel çıktı" | `mk_measure_scope` — yok | PR / basın yansıması metriği yok. |
| P12 | "Hedef Kullanıcı: … basın ilişkileri sorumluları" | `mk_roles` — yok | Kurumsal iletişim / basın sorumlusu rolü yok. |
| P13 | "Ton: Kurumsal, sade, güven veren, akıcı ve medya tarafından doğrudan kullanılabilir" | `brand_tone` (01) — tam (bülten tonu C ilkesi olarak sabit) | — |

### 3.3 Yeni bölüm: `mk_pr` — "Basın Bülteni & Medya İlişkileri" (grup: **Kanallar**, `mk_events`'ten sonra önerilir)

Bölüm açıklaması önerisi: "Haber değeri taşıyan gelişmelerin basın bülteni, medya pitch'i, web haber sayfası ve medya kitiyle duyurulma standardını belirler." `refs`: `mk_brand_name`, `oc_legal_name`, `oc_boilerplate` (yeni, §3.4), `mk_contact`, `domain_name`, `oc_logo`, `mk_accounts`. Toplam 6 alan.

#### `mk_pr_on` [boolean] — "Basın Bülteni"
- yes — scenario: kurum lansman, atama, yatırım, rapor gibi gelişmeleri medyaya duyuracaksa; example: her duyuru başlık + spot + dateline + giriş + gövde + alıntı + boilerplate + basın iletişim iskeletiyle hazırlanır.
- no — scenario: medya ilişkisi yürütülmüyorsa; example: basın bülteni kuralları prompta girmez.
Kanıt: Bölüm 1 "Basın bülteni; kurumun haber değeri taşıyan gelişmesini medya, iş ortakları, müşteriler … için resmi, güvenilir ve kolay işlenebilir biçimde duyuran stratejik iletişim dokümanıdır."

#### `mk_pr_types` [multiselect] — "Bülten Türleri" · showIf `mk_pr_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Kurumsal duyuru | `corporate` | Yönetim ataması, yatırım, yeni ofis, marka yeniliği. | Lider görüşü ve kurumsal arka planla atama haberi. |
| Ürün / hizmet lansmanı | `launch` | Yeni ürün, hizmet, platform. | Sorun → çözüm → fayda → hedef kitle → CTA. |
| Etkinlik / webinar | `event` | Etkinlik, panel, eğitim, fuar katılımı. | Tarih, saat, konuşmacı, kayıt linki. |
| Araştırma / rapor | `research` | Sektör verisi, anket, rapor yayını. | Metodoloji, veri, grafik, uzman yorumu, kaynak linki. |
| İş birliği / ortaklık | `partnership` | Stratejik iş birliği, sponsorluk. | Taraflar, ortak hedef, her iki taraftan alıntı. |
| Kriz / açıklama | `crisis` | Kamuoyu bilgilendirme, düzeltme, resmi açıklama. | Net pozisyon, tek sözcü; yayından önce hukuk kontrolü. |
ruleDetail: `crisis` — "Kriz bülteninde yalnız onaylı tek sözcü konuşur, bilgi doğrulanmış olur ve hukuk onayı olmadan gönderilmez"; `research` — "metodoloji ve kaynak linki zorunlu". `crisis` seçilince `mk_legal_scope`'a `press` önerisi (`recommend`). Kanıt: Bölüm 2 tablosu.

#### `mk_pr_contact` [textarea] — "Basın İletişim Kişisi" · showIf `mk_pr_on = true`
ph: "Örn. Ad Soyad | Kurumsal İletişim Müdürü | basin@ornekfirma.com | 0212 000 00 00". scenario: her bültenin sonunda medyanın teyit için ulaşacağı kişi; example: "Basın İletişim: Ad Soyad | Unvan | E-posta | Telefon | Web". Not: kişinin adı ve kurumsal iletişim bilgisi bültende yayımlanacağı için kişiye bilgi verilmesi (KVKK) açıklamada belirtilir. Kanıt: "Basın İletişim: Ad, unvan, e-posta, telefon" / iskelet "[Ad Soyad] | [Unvan] | [E-posta] | [Telefon] | [Web]" / checklist "Basın iletişim e-posta ve telefon bilgileri eklendi mi?"

#### `mk_pr_spokes` [textarea] — "Onaylı Sözcüler" · showIf `mk_pr_on = true`
ph: "Örn. Ad Soyad | Genel Müdür | kurumsal duyurular, kriz\nAd Soyad | Ar-Ge Direktörü | ürün lansmanı, rapor". scenario: alıntıların yalnız yetkili kişilerden alınması; kriz bülteninde tek sözcü; example: Claude alıntıyı listedeki uygun sözcüye atar, listede olmayan kişi adına alıntı yazmaz. Kanıt: "Kriz / Açıklama Bülteni … tek sözcü" / "Sözcü / Alıntı Sahibi: [Ad soyad, unvan, kurum]" / "Alıntı sahibi, unvanı ve kurum adı doğru mu?" / "Yapay, uzun veya reklam kokan alıntılar yerine karar verici içgörü sunan kısa alıntılar".

#### `mk_pr_outputs` [multiselect] — "Bülten Çıktıları" · showIf `mk_pr_on = true`
| Etiket | Değer | scenario | example |
|---|---|---|---|
| Bülten metni (DOCX) (önerilen) | `docx` | Medyaya düzenlenebilir dosya. | A4, dikey, 2–2,5 cm kenar, 10–11 punto. |
| PDF (seçilebilir metin) | `pdf` | Final, değişmez sürüm. | 5 MB altı, taranmış değil. |
| E-posta pitch metni (önerilen) | `pitch` | Gazetecilere doğrudan gönderim. | 45–75 karakter konu; bülten metni e-posta gövdesinde. |
| Web haber / basın odası sayfası | `newsroom` | Sitede haber / basın sayfası varsa. | 55–90 karakter başlık, 30–75 karakter slug, meta, OG görseli, NewsArticle schema. |
| Sosyal medya uyarlamaları | `social` | Bülten sosyal kanallarda da duyurulacaksa. | LinkedIn / X için kısa uyarlama. |
| Medya kiti | `mediakit` | Görsel ve ek dokümanlar linkle paylaşılacaksa. | Pitch'te "Görsel ve ek dokümanlara buradan ulaşabilirsiniz: [Medya Kit Linki]". |
ruleDetail `pitch`: "Bülten metni yalnız ek olarak değil, e-posta gövdesinde de yer alır; ağır dosya eklenmez; 24–48 saat sonra tek nazik takip yapılabilir." `newsroom`: proje `schema_types`'a `NewsArticle` önerisi (§3.4-2). Kanıt: kapak "Çıktı Formatı", Bölüm 6, 8, 9.

#### `mk_pr_mediakit` [multiselect] — "Medya Kiti İçeriği" · showIf `mk_pr_on = true` ve `mk_pr_outputs` içinde `mediakit`
| Etiket | Değer | ruleDetail (kılavuz) |
|---|---|---|
| Logo (SVG / AI / EPS, şeffaf PNG) | `logo` | "Şeffaf zeminli versiyon medya kit içinde yer almalıdır." |
| Basın fotoğrafları | `photos` | "En az 2000 px genişlik, 300 dpi tercih edilir"; telif / kullanım izni notu. |
| Sözcü portresi ve biyografisi | `spokes` | "Dikey ve yatay alternatif … Ad-soyad, unvan ve kullanım izni bilgisi eklenmelidir." |
| Video | `video` | "MP4 / H.264 / 1080p; kısa versiyon 30-60 sn"; link ile, e-posta eki değil. |
| İnfografik ve rapor | `docs` | Araştırma bültenlerinde kaynak dokümanla. |
| Basın iletişim bilgisi | `contact` | `mk_pr_contact`'tan. |
scenario / example: ör. `photos` — scenario: medya baskıda da kullanacaksa; example: medya kiti klasöründe `[MARKA]_[KONU]_Gorsel_01_1920x1080.jpg`. Kanıt: Bölüm 6 "Medya kiti" satırı ve Bölüm 7 tablosu.

### 3.4 Mevcut alanlarda değişiklik / Ortak Bilgiler önerileri (Basın bülteni)
1. **Yeni Ortak Bilgiler alanı `oc_boilerplate`** [textarea] — "Kurum Hakkında (Boilerplate)", bölüm `oc_identity` (77), `oc_tagline`'dan sonra; `words: 95` (70–120 kelime önerisi, sayaç). ph: "Örn. Örnek Firma, 2010'dan bu yana … (70–120 kelime, güncel ve onaylı metin)". scenario: basın bülteninin sonundaki standart kurum paragrafı ve diğer kurumsal belgelerde tekrar kullanılan onaylı tanıtım; example: her bülten "Örnek Firma Hakkında" başlıklı aynı paragrafla biter. Ortak Bilgiler'e koyma gerekçesi: "standart, güncel ve onaylı kurumsal bilgi" — kanaldan bağımsız, birden çok içerik türünde aynen kullanılır. Kanıt: "Boilerplate: 70-120 kelime. Şirket hakkında standart, güncel ve onaylı kurumsal bilgi." / checklist "Boilerplate güncel ve onaylı mı?"
2. **`schema_types`** seçenek ekle: `NewsArticle` — ruleDetail: "Basın / haber sayfalarında kullanılır". Kanıt P7. (`mk_pr_outputs.newsroom` seçiliyse `recommend` ile önerilir.)
3. **`mk_legal_scope`** seçenek ekle: `press` "Basın bültenleri ve kamuoyu açıklamaları" — ruleDetail: "Finansal iddia (gelir, büyüme, pazar payı, yatırım) onaylı veriyle desteklenir; rakibi hedef alan ya da regülasyon riski taşıyan ifade çıkarılır; kriz bülteni hukuk onayı olmadan gönderilmez." Kanıt: Bölüm 10 ve Bölüm 2 (kriz).
4. **`mk_measure_scope`** seçenek ekle: `pr` "Basın yansımaları (yayınlanan haber, link kullanımı, backlink, UTM trafiği, röportaj talebi)". Kanıt: Bölüm 13 tablosu.
5. **`mk_roles`** seçenek ekle: `pr` "Kurumsal iletişim / basın sorumlusu". Kanıt: "Hedef Kullanıcı: Pazarlama, kurumsal iletişim, … basın ilişkileri sorumluları".
6. **`mk_approvers`** seçenek ekle: `corp_comm` "Kurumsal iletişim sorumlusu" (isteğe bağlı; diğer onay sahipleri mevcut seçeneklerle karşılanıyor). Kanıt P8.
7. **`mk_contact`** (77) — değişiklik yok; ama ana asistan, üç kılavuzda da CTA'da tek bir telefon istendiği için (Mailing "Telefon: [TELEFON]", SMS "Tel: [TELEFON]", Basın "Telefon: [Basın iletişim veya kurum telefonu]") `oc_identity`'ye **`oc_cta_phone` [text] "CTA'larda Kullanılacak Telefon"** eklemeyi değerlendirebilir (mk_contact birden çok numara içerebiliyor; Claude'un hangisini CTA'ya yazacağı belirsiz). Diğer kılavuz analizleriyle (ör. Şirket ve İletişim Bilgileri dosyası) birleştirilmeli — DEVİR: ana asistan.

### 3.5 B sınıfı brief alanları
Kurum / marka · bülten konusu · bülten türü · haber değeri · hedef medya (ekonomi, İK, teknoloji, sağlık, yerel, sektörel) · hedef kitle · yayın tarihi ve saati (saat dilimi) · ambargo durumu (embargolu / anında / planlı) · sözcü / alıntı sahibi (onaylı listeden) · CTA ve link · telefon · onay sahipleri ve onay durumu (taslak / revize / onaylandı / yayına hazır) · ana mesaj · medya kit linki · dateline şehri (varsayılan: `mk_contact` adresindeki şehir) · medya / dağıtım listesi · gazeteci kişiselleştirmesi.

### 3.6 C sınıfı ilkeler
1. Ters piramit: en önemli bilgi ilk paragrafta; giriş (40–70 kelime) kim, ne, ne zaman, nerede, neden, nasıl sorularını yanıtlar.
2. Başlık 55–90 karakter, haber değerini doğrudan verir, reklam dili içermez; spot 120–220 karakter.
3. Dateline "Şehir, GG Ay YYYY –" biçiminde ilk paragraftan önce; ambargo varsa üst bilgide tarih, saat, saat dilimi.
4. Gövde 3–6 paragraf, her paragraf tek fikir, ortalama 50–80 kelimeyi aşmaz; alıntı 25–60 kelime, karar verici içgörüsü, reklam kokmaz.
5. Haber dili nesnel ve doğrulanabilir; her rakam, oran, ödül, müşteri sayısı, pazar iddiası kaynak ve onay ister; süperlatif yalnız doğrulanabiliyorsa.
6. Teknik terim ilk kullanımda kısa açıklamayla, kısaltma ilk kullanımda açık hâliyle.
7. Web haber sayfası: slug 30–75 karakter küçük harf tireli, meta title 35–60, meta description 120–160, OG görseli 1200×630 / 1200×675, linkler UTM'li ve ilgili açılış sayfasına.
8. Görseller yüksek çözünürlüklü, telifi temiz, alt metinli (1 cümle); ana görsel 16:9 (1200×675 / 1920×1080).
9. Pitch kısa, kişiselleştirilmiş; ilk 2 cümlede neden önemli olduğu; bülten gövdede, ağır dosya yerine medya kit linki.
10. Dosya adları: `[MARKA]_[KONU]_BasinBulteni_[YYYYMMDD]_v01.docx` / `_final.pdf`, medya kit `[MARKA]_[KONU]_MediaKit_[YYYYMMDD]`; taslak, revize, final ayrı versiyonlanır.

---

## 4. Kanallar arası notlar (ana asistan için)
- **Emoji politikası** Mailing (P2 `mk_mail_emoji`) ve SMS'te (`mk_sms_charset` içinde) ayrı ele alındı; sosyal medya kılavuzunu analiz eden ajan da önerirse `mk_creative`'e tek bir kanallar arası alan düşünülebilir.
- **Dosya adlandırma / versiyonlama** üç kılavuzda da var (SMS §15, Basın §12, Mailing §6 "küçük harf ve tireli dosya adı"); C sınıfı tuttum. Diğer kılavuzlar da tanımlıyorsa tek bir `mk_file_naming` alanı (ör. `mk_planfile`'da) değerlendirilebilir — `mk_prefix` zaten seri no öneki taşıyor.
- **CTA telefonu** için `oc_cta_phone` önerisi §3.4-7'de.
- **Transactional e-posta ve OTP SMS** pazarlama dışı; proje bölümlerinde (`mail_provider`, `member_*`) kural metniyle ele alınmalı, pazarlama bölümüne tür olarak eklenmemeli (SMS'te `otp` / `service` seçenekleri yalnız "pazarlama cümlesi yok" kuralını taşımak için var — istenirse çıkarılabilir).
- Ölçüm: `mk_measure_scope`'a üç seçenek (`email`, `sms`, `pr`); `mk_utm.standard` ruleDetail'inde e-posta ve SMS değerleri.
