# Erişilebilirlik Modülü · İşleyiş Dokümanı

**Kapsam:** Ziyaretçi Erişilebilirlik Asistanı (tüm herkese açık sayfalar) + Erişilebilirlik Merkezi (`/admin/erisilebilirlik`) + tarayıcı tabanlı tarama motoru + CMS içerik kontrolleri
**Sürüm:** v1 · 8 Kasım 2026
**Hedef ölçüt seti:** WCAG 2.2 A ve AA
**İlgili belgeler:** [`docs/ACCESSIBILITY-SCANNING.md`](ACCESSIBILITY-SCANNING.md) (tarama runbook'u) · [`docs/pazarlama-modulu.md`](pazarlama-modulu.md) (aynı biçimde yazılmış kardeş doküman)

> **Ekran görüntüleri hakkında.** Tüm görüntüler 8 Kasım 2026'da **yerel test ortamında** alındı:
> `npm run dev` (port 5959) + yerel, geçici bir PostgreSQL veritabanı (`okcom_docs`) + bu veritabanında
> oluşturulan bir test yöneticisi. Canlı veritabanına dokunulmadı. Yönetim ekranlarındaki veriler gerçek bir
> taramanın (`npm run a11y:scan`) sonucudur; ayrıca belge için **örnek kayıtlar** eklendi: 3 manuel denetim
> kaydı, 2 ziyaretçi bildirimi, 1 "İnceleniyor" ve 1 "Gerekçeli İstisna" durumundaki sorun. Bu yüzden
> ekranlarda adres olarak `http://localhost:5959` görünür. Next.js'in geliştirme göstergesi çekimlerde gizlendi.
>
> **Alan adı yer tutucusu.** Metinde sitenin alan adı `anadomain.com` olarak yazıldı; kullanılacağı ortamın
> gerçek alan adıyla değiştirilecek. Kodda bu değer bugün `src/modules/accessibility/domain/audit.ts`
> (`PRODUCTION_ORIGINS`, `DEFAULT_SCAN_CONFIG.baseUrl`) ve `.github/workflows/accessibility.yml` içinde
> tanımlıdır. Ekran görüntülerindeki adresler ise çekildikleri ortamın gerçek değerleridir.

---

## İçindekiler

1. [Temel ilkeler](#1-temel-ilkeler)
2. [Modülün parçaları](#2-modülün-parçaları)
3. [Ziyaretçi paneli](#3-ziyaretçi-paneli)
4. [Hızlı ayar kartları](#4-hızlı-ayar-kartları)
5. [Profiller](#5-profiller)
6. [Ayrıntılı bölümler](#6-ayrıntılı-bölümler)
7. [Görünüm modları ve sayfa üstü araçlar](#7-görünüm-modları-ve-sayfa-üstü-araçlar)
8. [Ses, komut ve gezinme](#8-ses-komut-ve-gezinme)
9. [Kalıcılık, performans ve gizlilik](#9-kalıcılık-performans-ve-gizlilik)
10. [Kaynak kod erişilebilirliği](#10-kaynak-kod-erişilebilirliği)
11. [Erişilebilirlik Merkezi (yönetim)](#11-erişilebilirlik-merkezi-yönetim)
12. [Tarama motoru](#12-tarama-motoru)
13. [İzleme, bildirim, CI ve saklama](#13-izleme-bildirim-ci-ve-saklama)
14. [CMS içerik, medya ve belge iş akışı](#14-cms-içerik-medya-ve-belge-iş-akışı)
15. [Veri modeli](#15-veri-modeli)
16. [Güvenlik](#16-güvenlik)
17. [Dosya yapısı ve testler](#17-dosya-yapısı-ve-testler)
18. [Bilinen sınırlar ve açık kararlar](#18-bilinen-sınırlar-ve-açık-kararlar)
19. [UserWay ile karşılaştırma](#19-userway-ile-karşılaştırma)

---

## 1. Temel ilkeler

| İlke | Uygulama |
|---|---|
| **Vendor yok** | UserWay, accessiBe, EqualWeb vb. ürünlerin script'i, aboneliği, kodu, logosu veya rengi kullanılmaz. İşlevler projenin kendi mimarisiyle (Next.js + Drizzle + Cloudflare Workers) yazıldı. |
| **Önce kaynak kod** | Widget kapalıyken de site erişilebilir olmalı. Taramanın bulduğu sorunlar kaynak kodda düzeltildi; panel bir "örtü" (overlay) olarak sorun gizlemez. |
| **Sertifika değil** | Panel, otomatik puan veya rapor hiçbir yerde "uyumlu", "%100 erişilebilir", "sertifikalı" demez. Puanın adı her yerde **"Otomatik kontrol sonucu"**dur. |
| **Tıbbi iddia yok** | Mavi filtre, disleksi fontu ve profiller için sağlık faydası veya güvenlik garantisi yazılmaz (testle sabitlendi). |
| **Kişiyi etiketlemeyen dil** | Profil adları "… desteği" biçimindedir; "engelli modu", "âmâ" gibi ifadeler kullanılmaz. |
| **Gizlilik** | Ziyaretçinin ayarları ve profil seçimi yalnız kendi tarayıcısında kalır; sunucuya, analitiğe veya dataLayer'a gitmez. |
| **Tasarım sadakati** | Panel sitenin kurumsal siyah-beyaz paletini, Urbanist yazı tipini, 20px kart yarıçapını ve tek easing'ini kullanır. Resmî palet değiştirilmedi. |

---

## 2. Modülün parçaları

```
Erişilebilirlik modülü
├── Ziyaretçi Asistanı (public)
│   ├── Başlatıcı düğme + footer bağlantısı + Alt+Shift+A
│   ├── Panel: Hızlı ayarlar · Profiller · Metin · Görünüm · Okuma ve gezinme · Panel ayarları · Yardım
│   ├── Sayfa üstü araçlar: okuma kılavuzu, odak maskesi, büyüteç, sade okuma, açıklama balonları …
│   └── İlk boyama öncesi script (tema parlaması olmasın diye)
├── Kaynak kod düzeltmeleri (kontrast, odak örtülmesi, yeniden akış, metin büyütme)
├── Erişilebilirlik Merkezi (admin · 11 bölüm)
├── Tarama motoru (Playwright + axe-core · CLI / kuyruk runner / CI kapısı)
├── CMS entegrasyonu (yayın öncesi kontrol, medya ALT/dekoratif, belge envanteri)
└── Veri: 13 tablo (a11y_*) · drizzle/0022_accessibility.sql
```

---

## 3. Ziyaretçi paneli

### 3.1 Açma yolları

Panel üç yoldan açılır:

1. **Başlatıcı düğme** — varsayılan sağ alt köşede. Aktif ayar sayısını rozet olarak gösterir; ekran okuyucu "Erişilebilirlik ayarları, 3 ayar etkin" diye okur.
2. **Footer bağlantısı** — "Erişilebilirlik" (Çerez Tercihlerim'in yanında). Ziyaretçi düğmeyi gizlediğinde paneli geri açmanın yolu budur.
3. **Klavye kısayolu** — `Alt + Shift + A`. Panel ayarlarından kapatılabilir. Başka hiçbir tarayıcı/ekran okuyucu kısayolunu engellemez. (UserWay'in kullandığı `Ctrl+U` tarayıcılarda "kaynağı görüntüle" olduğu için bilinçli olarak seçilmedi.)

![Sayfanın sağ alt köşesinde siyah daire içinde insan figürü simgeli erişilebilirlik düğmesi](erisilebilirlik-modulu/01-baslatici.png)

![Footer'daki yasal bağlantılar şeridi: Gizlilik, KVKK, Çerez Politikası, Çerez Tercihlerim ve Erişilebilirlik](erisilebilirlik-modulu/29-footer-baglantisi.png)

### 3.2 Panel düzeni

![Ana sayfa üzerinde açık erişilebilirlik paneli: başlık, araç çubuğu, Profiller ve Hızlı ayarlar bölümleri](erisilebilirlik-modulu/02-panel-genel.png)

Panelin üstünden aşağıya:

| Alan | İçerik |
|---|---|
| Başlık | "OK" logosu, "Erişilebilirlik Asistanı", kısa açıklama, kapat düğmesi. Başlık/logo gizlenebilir; gizlense de diyaloğun erişilebilir adı korunur. |
| Durum | "Etkin ayar yok" / "8 ayar etkin". Depolama kullanılamıyorsa "ayarlar yalnız bu oturum boyunca geçerli" uyarısı. |
| Araç çubuğu | **Geri al** (son değişiklik; kart tıklaması ve yazılı komut tek adımdır) · **Tümünü sıfırla** · **Tüm bölümleri genişlet/daralt** · **TR/EN** dil seçimi · **XL Büyük panel**. |
| Bölümler | Profiller · Hızlı ayarlar (varsayılan açık) · Metin · Görünüm · Okuma ve gezinme · Panel ayarları · Yardım. Her biri akordeon. |

**Diyalog davranışı.** Panel **modal değildir** (`role="dialog"`, `aria-modal` yok, odak tuzağı yok): ziyaretçi bir ayarı açıp sonucunu sayfada deneyebilmeli. Açılışta odak panel başlığına gider; `Esc` paneli kapatır ve odağı açan öğeye (yoksa başlatıcıya, o da gizliyse footer bağlantısına) döndürür. Tüm değişiklikler tek bir `aria-live` bölgesinden duyurulur.

**Boyut.** Normal 400px, büyük panel 520px. Ziyaretçi yazıyı büyüttüğünde panel de en fazla 1.5 katına kadar genişler. 640px altında panel tam genişlikte "alt sayfa" olur.

![Mobil (390px) görünümde ekranın altından açılan panel](erisilebilirlik-modulu/28-mobil-panel.png)

**Panel dili.** TR/EN yalnız panelin kendi arayüz dilidir; site içeriği çevrilmez. Panel kökü `lang="en"` alır, sayfa `lang="tr"` kalır.

![İngilizce panel: Accessibility Assistant başlığı ve Quick settings kartları](erisilebilirlik-modulu/30-panel-ingilizce.png)

---

## 4. Hızlı ayar kartları

![Hızlı ayarlar bölümünde üç sütunlu ikonlu kart ızgarası; her kartta sol üstte "i" düğmesi ve altta "Kapalı" durumu](erisilebilirlik-modulu/03-hizli-ayarlar.png)

Kartlar **yeni bir ayar sistemi değildir**: her kart mevcut ayar anahtarlarına bir "adım listesi" uygular. Kart, kaydırıcı ve sesli/yazılı komut aynı depoyu değiştirir ve birbirini her zaman doğru gösterir.

**Davranış:** kapalı → 1. adım → 2. adım → … → son adım → kapalı. Bir değer ayrıntılı bölümden adım dışı bir değere getirilirse (ör. yazı %130) kart **"Özel"** yazar; sonraki tık 1. adıma döner.

**Durum renkle sınırlı değil:** her kartta durum metni ("Kapalı", "%140", "OpenDyslexic"), adım çubukları ve açıkken onay işareti bulunur; ekran okuyucuya `aria-pressed` ile bildirilir. Kart sütun genişliği `em` cinsindendir: yazı büyüdüğünde veya disleksi fontu/geniş aralık açıldığında sütun sayısı azalır, etiketler hece ortasından bölünmez.

![Büyük metin %140, akıllı kontrast ve disleksi profili açıkken kartlar: iki sütun, etkin kartlarda onay işareti](erisilebilirlik-modulu/11-kartlar-etkin.png)

**"i" bilgi düğmesi.** Her kartın sol üstünde ayrı bir düğmedir (kartın içinde değil — düğme içinde düğme geçersiz HTML olurdu). "Büyük metin hakkında bilgi" diye okunur, `aria-expanded` taşır. Açılan kutu kartların bulunduğu alan genişliğindedir (en fazla 20em) ve dışına taşmaz. `Esc` yalnız kutuyu kapatır ve odağı "i"ye döndürür; dışarı tıklamak veya odağın başka yere geçmesi de kapatır. Kutuyu açmak hiçbir ayarı değiştirmez.

![Büyük metin kartının altında açılmış bilgi kutusu: başlık, açıklama ve "Bilgiyi kapat" düğmesi](erisilebilirlik-modulu/12-bilgi-dugmesi.png)

### Kart listesi (varsayılan sıra)

İlk 15 kart UserWay'deki tanıdık düzeni izler, sonraki 13 kart bu sitenin ek özellikleridir. Sıra ve görünürlük **Asistan Ayarları** ekranından yönetilir (§11.10).

| # | Kart | Adımlar | Bağlı özellik |
|---|---|---|---|
| 1 | Sayfayı oku | Okumayı başlat / durdur (eylem) | `tts` |
| 2 | Kontrast + | Yüksek kontrast açık → koyu | `contrast` |
| 3 | Akıllı kontrast | Açık | `contrast` |
| 4 | Bağlantıları vurgula | Açık | `highlight` |
| 5 | Büyük metin | %120 → %140 → %160 → %180 → %200 | `fontScale` |
| 6 | Metin boşluğu | Hafif → Orta → Geniş (harf + kelime aralığı) | `spacing` |
| 7 | Animasyonları durdur | Açık | `stopAnimations` |
| 8 | Resimleri gizle | Açık | `hideImages` |
| 9 | Disleksi dostu | OpenDyslexic → Okunaklı (Atkinson Hyperlegible) | `fontFamily` |
| 10 | İmleç | Büyük siyah → Büyük beyaz → Çok büyük | `cursor` |
| 11 | İpuçları | Açık | `tooltips` |
| 12 | Sayfa yapısı | Başlık/bölge/bağlantı listesini açar (eylem) | `structure` |
| 13 | Satır yüksekliği | 1.6 → 1.8 → 2.0 | `spacing` |
| 14 | Metin hizalama | Sola → Ortaya → Sağa → İki yana | `textAlign` |
| 15 | Doygunluk | Düşük → Yüksek → Gri | `colorFilters` |
| 16 | Başlıkları vurgula | Açık | `highlight` |
| 17 | Okuma kılavuzu | Açık | `readingGuide` |
| 18 | Odak maskesi | Açık | `focusMask` |
| 19 | Metin büyüteci | Balon → Alt şerit → Büyüteç görünümü | `magnifier` |
| 20 | Sade okuma | Açık | `readerMode` |
| 21 | Koyu tema | Koyu → Sistem | `theme` |
| 22 | Renk ayırt etme | Yeşil → Kırmızı → Mavi-sarı → Tek renk + desen | `colorPalette` |
| 23 | Mavi ışık filtresi | %30 → %60 | `blueFilter` |
| 24 | Sesi kapat | Açık | `muteMedia` |
| 25 | Büyük kontroller | Açık (en az 44×44 px hedef) | `largeTargets` |
| 26 | Klavye odağı | Açık (kalın iki tonlu çerçeve) | `focusVisible` |
| 27 | Yakınlaştır | %120 → %150 | `pageZoom` |
| 28 | Renkleri ters çevir | Açık | `colorFilters` |

---

## 5. Profiller

![Profiller bölümü: iki sütunlu ikonlu profil kartları](erisilebilirlik-modulu/04-profiller.png)

Profil yalnız bir **ayar kısayoludur** — bir tanı değildir, kaydedilmez, analitiğe gitmez. Her kartın altındaki "Değiştirdiği ayarlar" alanı profili açmadan önce neyi değiştireceğini gösterir.

![Motor beceri desteği profilinin "Değiştirdiği ayarlar" alanı açık: Büyük kontroller, Görünür klavye odağı, Animasyonları durdur, Açıklama balonları](erisilebilirlik-modulu/05-profil-ayrinti.png)

| Profil | Değiştirdiği ayarlar |
|---|---|
| Motor beceri desteği | Büyük kontroller · Görünür klavye odağı · Animasyonları durdur · Açıklama balonları |
| Ekran okuyucu ile kullanım desteği | Animasyonları durdur · Medyayı sustur · Görünür odak · Başlıkları belirginleştir (ekran okuyucunun kendi ayarlarına dokunmaz) |
| Renk ayırt etme desteği | Renk paleti (yeşil ayırt etme) · Bağlantıları belirginleştir · Akıllı kontrast |
| Disleksi ve okuma desteği | Disleksi fontu · Satır aralığı 1.8 · Harf aralığı 0.06em · Kelime aralığı 0.15em · Sola hizalı · Okuma kılavuzu |
| Az görenler için görünüm | Yazı %150 · Akıllı kontrast · Bağlantıları belirginleştir · Büyük imleç · Görünür odak |
| Bilişsel ve öğrenme desteği | Okunaklı font · Başlık ve bağlantı vurgusu · Animasyonları durdur · Açıklama balonları · Terim işaretleri |
| Hareket ve yanıp sönme hassasiyeti | Animasyonları durdur · Medyayı sustur · Doygunluk %80 |
| Odaklanma desteği | Odak maskesi · Animasyonları durdur · Başlıkları belirginleştir |
| Kolay kullanım | Büyük kontroller · Yazı %120 · Okunaklı font · Sade okuma · Görünür odak |

**Birleşim kuralı:** `etkin = varsayılan ⊕ yönetici varsayılanı ⊕ profiller (açılma sırasıyla) ⊕ elle yapılan ayarlar`
- İki profil aynı ayarı farklı değere çekerse sonra açılan kazanır.
- Elle yapılan değişiklik her zaman profilin üstündedir; ayrıntılı bölümde "Profilden: Disleksi" rozeti ayarın kaynağını gösterir.
- Profil kapatılınca yalnız o profilin katkısı düşer; elle yapılan ayarlar kalır.
- Yönetici bir özelliği kapattıysa profil o ayarı açamaz.

---

## 6. Ayrıntılı bölümler

Kartların ince ayarıdır. Her kontrolde etiket, açıklama, görünür değer, kaynak rozeti ve **ayrı sıfırlama** düğmesi vardır. Sayısal ayarlarda azalt/artır düğmeleri + kaydırıcı + değer; seçimlerde radyo grubu; açık/kapalı ayarlarda anahtar (switch) kullanılır.

### 6.1 Metin

![Metin bölümü: yazı boyutu, yakınlaştırılmış görünüm, satır/kelime/harf aralığı, hizalama, yazı tipi kontrolleri](erisilebilirlik-modulu/06-bolum-metin.png)

| Ayar | Aralık / seçenekler |
|---|---|
| Yazı boyutu | %100–%200, %10 adım. Tasarımın ölçülen taban değerinden hesaplanır; **birikmez** (her açılışta mevcut boyutun üstüne eklenmez). Tarayıcı yakınlaştırması engellenmez. |
| Yakınlaştırılmış görünüm | %100–%200 sayfa zoom'u; içerik yeniden akar. Panel ve başlatıcı etkilenmez. |
| Satır aralığı | Tasarım (varsayılan) veya 1.2–2.4 |
| Kelime aralığı | 0–0.5em |
| Harf aralığı | 0–0.3em |
| Metin hizalama | Varsayılan / sola / ortaya / sağa / iki yana |
| Yazı tipi | Sitenin fontu · Okunaklı (Atkinson Hyperlegible) · Disleksi okuma fontu (OpenDyslexic). İkisi de OFL lisanslıdır, yalnız seçilince indirilir; Türkçe karakterler (ğ ş ı İ ç ö ü) üç tarayıcıda ölçüldü. İkonlar etkilenmez. |
| Sade okuma görünümü | Bkz. §7.2 |
| Başlıkları / bağlantıları belirginleştir | Çerçeve ve alt çizgi — renge dayanmaz |
| Metin büyüteci | Kapalı / Balon / Alt şerit / Büyüteç görünümü |

### 6.2 Görünüm

![Görünüm bölümü: tema, kontrast, ters çevirme, gri tonlama, doygunluk, renk paleti, mavi filtre kontrolleri](erisilebilirlik-modulu/07-bolum-gorunum.png)

| Ayar | Ayrıntı |
|---|---|
| Tema | Sitenin teması / Açık / Koyu / Sistem |
| Kontrast | Varsayılan / Akıllı (soluk metin ve kenarlıkları koyulaştırır) / Yüksek kontrast açık / Yüksek kontrast koyu |
| Renkleri ters çevir · Gri tonlama · Doygunluk (%0–200) | Filtre zinciri |
| Renk ayırt etme desteği | Kırmızı / yeşil / mavi-sarı ayırt etme paletleri (Okabe–Ito, Paul Tol) ve tek renk + desen |
| Mavi ışık filtresi | Yoğunluk %0–100; zamanlama: kapalı / her zaman / saat aralığında / gün batımından doğumuna. "Bir sağlık önerisi değildir." |
| Görselleri gizle | Yerleşim korunur; anlamlı görsellerin ALT metni görselin yerinde gösterilir |
| Animasyonları durdur | CSS animasyonları, geçişler, kaydırma efektleri, otomatik oynayan video, SVG ve betik animasyonları |
| Site medyasını sustur | Önceki ses durumu saklanır, kapatınca geri yüklenir |
| Büyük imleç | Büyük / çok büyük · siyah / beyaz |
| Okuma kılavuzu · Odak maskesi | Bkz. §7.2 |
| Görünür klavye odağı | Kalın, iki tonlu odak çerçevesi |
| Büyük kontroller | Düğme ve bağlantılarda en az 44×44 px tıklama alanı |

**Teknik not — renkler.** Tema ve kontrast modları yalnız **semantik renk token'larını** yeniden eşler; resmî kurumsal palet (`--black`, `--gray-*`, `--white`, alert renkleri) değişmez. Koyu tema, resmî paletin tersine eşlenmesidir. Renk ayırt etme paletleri "Extended UI Palette" kapsamında etiketlenmiş, yalnız ziyaretçi tercihi açıkken devreye giren token'lardır.

**Teknik not — filtreler.** Filtreler `<body>`'ye uygulanmaz (sabit/yapışkan öğelerin konumunu bozar ve paneli de filtrelerdi). Bunun yerine panelin **altında** duran tam ekran bir `backdrop-filter` katmanı kullanılır; panel ve başlatıcı filtrelenmez.

### 6.3 Okuma ve gezinme

![Okuma ve gezinme bölümü: Ana içeriğe geç, açıklama balonları, terimleri işaretle, sesli okuma kontrolleri ve sesli komut](erisilebilirlik-modulu/08-bolum-okuma-gezinme.png)

İçerik: Ana içeriğe geç · Açıklama balonları · Terimleri işaretle · Sesli okuma (§8.1) · Sesli komut (§8.2) · Yazılı komut (§8.3) · Sayfa yapısı (§8.4) · Terim sözlüğü.

### 6.4 Panel ayarları

![Panel ayarları: panel dili, panel boyutu, düğme konumu, boyutu ve simgesi, düğmeyi gizle, başlığı gizle, kısayol](erisilebilirlik-modulu/09-bolum-panel-ayarlari.png)

| Ayar | Seçenekler |
|---|---|
| Panel dili | Türkçe / English |
| Panel boyutu | Normal / Büyük |
| Düğme konumu | Sağ alt / Sol alt / Sağ orta / Sol orta |
| Düğme boyutu | Normal (48px) / Büyük (60px) |
| Düğme simgesi | İnsan figürü / Göz / Ayar çubukları / Harf |
| Düğmeyi gizle | Gizlenince footer bağlantısı ve kısayol duyurulur |
| Panel başlığını ve logosunu gizle | Erişilebilir ad korunur |
| Alt+Shift+A kısayolu | Açık / kapalı |

Panel tercihleri "Tümünü sıfırla" ile silinmez (dil ve düğme konumu korunur).

### 6.5 Yardım

![Yardım bölümü: sık sorulan sorular, klavye kısayolları, erişilebilirlik açıklaması ve sorun bildirme formu](erisilebilirlik-modulu/10-bolum-yardim.png)

- **Sık sorulan sorular** (native `<details>`).
- **Klavye kısayolları** tablosu (Alt+Shift+A, Esc, Tab/Shift+Tab) ve "tarayıcı/ekran okuyucu kısayolları engellenmez" notu.
- **Erişilebilirlik açıklaması** — yöneticinin yazdığı metin; boşsa kod içindeki güvenli varsayılan metin. Gözden geçirme tarihi gösterilir.
- **Sorun bildir** formu — kategori (içerik, klavye, ekran okuyucu, kontrast, medya, form, asistan, diğer), mesaj (zorunlu, en az 10 karakter), isteğe bağlı e-posta. Yalnız sayfa yolu gönderilir; ayarlar ve profiller gönderilmez. Hatalar ilgili alana bağlanır ve özet odak alır. Bildirim kapalıysa ve destek adresi doğrulanmışsa `mailto:` bağlantısı gösterilir.

---

## 7. Görünüm modları ve sayfa üstü araçlar

### 7.1 Görünüm modları (panel kapalı, sayfa üzerinde)

| | |
|---|---|
| ![Koyu tema: siyah zemin, beyaz metin](erisilebilirlik-modulu/15-mod-koyu-tema.png) | ![Yüksek kontrast koyu](erisilebilirlik-modulu/16-mod-yuksek-kontrast-koyu.png) |
| Koyu tema | Yüksek kontrast (koyu) |
| ![Yüksek kontrast açık](erisilebilirlik-modulu/17-mod-yuksek-kontrast-acik.png) | ![Disleksi fontu ve geniş satır/harf/kelime aralığı](erisilebilirlik-modulu/18-mod-disleksi-araliklar.png) |
| Yüksek kontrast (açık) | Disleksi fontu + aralıklar |
| ![Metin yüzde iki yüz büyütülmüş ana sayfa](erisilebilirlik-modulu/19-mod-metin-200.png) | ![Gri tonlamalı sayfa](erisilebilirlik-modulu/20-mod-gri-tonlama.png) |
| Metin %200 | Gri tonlama |
| ![Sıcak renkli mavi ışık filtresi katmanı](erisilebilirlik-modulu/21-mod-mavi-filtre.png) | ![Bağlantılar altı çizili ve çerçeveli, başlıklar çerçeveli](erisilebilirlik-modulu/22-mod-baglanti-baslik-vurgu.png) |
| Mavi ışık filtresi %60 | Bağlantı ve başlık vurgusu |
| ![Görseller gizli, yerleşim korunmuş](erisilebilirlik-modulu/23-mod-gorselleri-gizle.png) | |
| Görselleri gizle | |

**İlk boyama öncesi uygulama.** Ziyaretçinin seçtiği tema ve yazı boyutu, React yüklenmeden önce çalışan küçük bir inline script ile `<html>` niteliklerine yazılır. Böylece sayfa her yüklemede önce varsayılan görünümle açılıp sonra "sıçramaz" (tema parlaması yok). Script `/admin` yollarında çalışmaz; depolama yoksa sessizce çıkar.

### 7.2 Sayfa üstü araçlar

| | |
|---|---|
| ![Fare imlecini izleyen yatay okuma kılavuzu çizgisi](erisilebilirlik-modulu/24-okuma-kilavuzu.png) | ![İmlecin çevresindeki bant dışında karartılmış ekran](erisilebilirlik-modulu/25-odak-maskesi.png) |
| **Okuma kılavuzu** — imleci ve klavye odağını izler; tıklamayı engellemez. | **Odak maskesi** — imleç çevresindeki 120px bant dışını karartır. |
| ![İmlecin altındaki paragrafın büyütülmüş hâlini gösteren siyah balon](erisilebilirlik-modulu/26-metin-buyuteci.png) | ![Sade okuma görünümü: tek sütunlu temiz metin ve "Sade okumadan çık" düğmesi](erisilebilirlik-modulu/27-sade-okuma.png) |
| **Metin büyüteci (balon)** — fare ve klavye odağında çalışır; `Esc` kapatır, imleç balona geçebilir (WCAG 1.4.13). Alt şerit ve mercek modları da vardır; mercek büyük sayfalarda (8.000+ düğüm) kendiliğinden balona düşer. | **Sade okuma** — `<main>` içeriği düz veriye çevrilip tek sütunda yeniden kurulur (`innerHTML` kopyalanmaz). Modal katmandır: odak içeri alınır, alttaki sayfa `inert` olur, `Esc` çıkar ve odak eski yerine döner. |

Diğer araçlar:
- **Açıklama balonları** — `title`, `aria-label`, `abbr` taşıyan öğelerde fare ve klavye odağında açıklama; `Esc` kapatır.
- **Terim işaretleri** — yöneticinin sözlüğündeki terimler CSS Custom Highlight API ile işaretlenir; DOM değişmez. API'yi desteklemeyen tarayıcıda panel not gösterir.
- **Görsel ALT etiketleri** — "Görselleri gizle" açıkken anlamlı görsellerin ALT metni görselin kutusuna oturur; dekoratif (`alt=""`) görsellerde etiket yoktur.
- **Medya kontrolü** — susturma ve durdurma yalnız asistanın kendi değiştirdiklerini geri yükler; YouTube gibi gömülü oynatıcılar tarayıcı güvenliği nedeniyle etkilenmez (panelde yazıyor).

---

## 8. Ses, komut ve gezinme

### 8.1 Sesli okuma

Tarayıcının kendi konuşma motorunu (`speechSynthesis`) kullanır. **Bir ekran okuyucunun yerine geçmez** — bu not panelde her zaman görünür.
- Ana içeriği oku / seçili metni oku · Duraklat / Devam / Durdur
- Okuma dili (Türkçe / English), ses seçimi, hız (0.5–2×), ses seviyesi
- Uzun metin cümle parçalarına bölünür (Chrome'un ~15 sn kesme sorunu)
- Türkçe ses yoksa açıklayıcı uyarı; API yoksa işletim sisteminin ekran okuyucusuna yönlendirme
- Otomatik başlamaz; sayfa değişince durur

### 8.2 Sesli komut (isteğe bağlı)

- Mikrofon **yalnız düğmeye basınca, tek komut için** açılır; sürekli dinleme yoktur.
- İlk kullanımda açıklama gösterilir: bazı tarayıcılar (ör. Chrome) sesi tanıma için kendi sunucularına gönderir. Kullanıcı onaylamadan mikrofon açılmaz.
- Desteklenmeyen tarayıcıda (ör. Firefox) yazılı komuta yönlendirme.
- Komutlar yalnız panel ayarlarını ve okuma/gezinme eylemlerini çalıştırır; **form göndermez, veri silmez, bağlantı açmaz.**

### 8.3 Yazılı (doğal dil) komut

![Yazılı komut alanında "yazıları büyüt ve hareketleri azalt" ve altında anlaşılan değişikliklerin önizlemesi: Yazı boyutu %120, Animasyonları durdur Açık](erisilebilirlik-modulu/13-yazili-komut.png)

- "Yazıları büyüt ve hareketleri azalt", "mavi filtreyi aç", "disleksi profilini aç", "sonraki başlık" gibi cümleler **yerel, deterministik kurallarla** çözülür (ağ ve model yok).
- Önce **önizleme** gösterilir; "Uygula" denince tüm değişiklikler tek geri alma adımı olarak uygulanır.
- Çıktı yalnız izinli komut şemasındaki biçimlerden oluşabilir (ayar değiştir, profil aç/kapa, gezinme eylemi). "Formu gönder", "hesabımı sil" gibi girdiler hiçbir komut üretmez (testle sabit).
- Projede AI altyapısı olmadığı için yalnız yerel çözücü çalışır; ileride takılabilecek bir adaptör arayüzü (`CommandInterpreter`) hazırdır ve onun çıktısı da aynı şema süzgecinden geçmek zorundadır.

### 8.4 Sayfa yapısı

![Sayfa yapısı aracı: Başlıklar (36), Bölgeler (28), Bağlantılar (54) sekmeleri ve seviyeye göre girintili başlık listesi](erisilebilirlik-modulu/14-sayfa-yapisi.png)

Başlıklar (seviyeye göre girintili), bölgeler (landmark) ve bağlantılar sekmeleri. Bir öğe seçilince sayfada oraya kaydırılır ve odaklanılır; geçici `tabindex` odak ayrılınca kaldırılır. Sekmeler ok tuşlarıyla gezilir.

---

## 9. Kalıcılık, performans ve gizlilik

| Konu | Davranış |
|---|---|
| Kayıt | `localStorage` · anahtar `ok-a11y` · sürümlü biçim. Bozuk veya eski sürüm kayıt sessizce varsayılana düşer. |
| Depolama yoksa | Gizli pencere, engellenmiş site verisi: ayarlar oturum boyunca bellekte çalışır; panel bunu söyler. |
| Sayfa geçişleri | Durum modül düzeyindeki depodadır; istemci tarafı gezinmede kaybolmaz. Başka sekmedeki değişiklik bu sekmeye de yansır. |
| İlk yük | Başlatıcı ve ilk boyama script'i ilk pakette; **panel ve araçlar yalnız panel açıldığında yüklenir** (Ekim 2026'da ilk JS paketinden ayrıldı). |
| /admin | Ziyaretçi ayarları yönetim panelinde uygulanmaz; asistan orada çizilmez. |
| Gizlilik | Hiçbir ayar, profil veya komut sunucuya gönderilmez. Güneş konumu filtresi için konum yalnız açık izinle alınır, gün doğumu/batımı tarayıcıda hesaplanır, konum saklanmaz. |
| Yönetici yapılandırması | Kök layout bir kez okur (`loadAssistantConfig`); veritabanı/tablo yoksa kod varsayılanlarına düşer, public sayfa bu yüzden hata vermez. |

---

## 10. Kaynak kod erişilebilirliği

Panel kapalıyken de sitenin erişilebilir olması için tarama bulgularına göre yapılan düzeltmeler:

| Sorun (WCAG) | Düzeltme |
|---|---|
| Okunur metin olarak kullanılan açık gri (#A3A3A3, beyaz zeminde 2.52:1) — 1.4.3 | Projede zaten tanımlı erişilebilir token'lara geçildi (`text-muted` 4.74:1, gri zeminde `text-muted-on-secondary` 4.54:1). Resmî palet değişmedi. |
| Klavye odağının çerez paneli / yapışkan header altında kalması — 2.4.11 | `FocusGuard`: odak öğesini header ile çerez paneli arasındaki serbest banda kaydırır (yumuşak kaydırma bittikten sonra). Çerez panelinin gerçek yüksekliği ölçülüp ayrılan alt şeride yazılır. Panel açıkken yapışkan "İçindekiler" rayları kendi içinde kaydırılabilir olur. |
| 320 CSS px'te yatay taşma — 1.4.10 | Proje detayındaki uzun araç adları ve Türkçe kelimeler için `overflow-wrap:anywhere`. |
| Metin büyütme / aralıkta taşma — 1.4.4, 1.4.12 | Yalnız ziyaretçi bu ayarları açtığında uzun kelimeler kırılabilir; sabit yükseklikli kapsül düğmeler büyür. Tasarımın kendi sabit font boyutları (41 yer) yazı ölçeğine bağlandı; varsayılan görünüm birebir aynı. |
| Yönetim tablolarında yatay sayfa taşması | Tablo kaydırma kapsayıcısı konumlu hâle getirildi; hücrelerdeki `sr-only` metinler kapsayıcıdan kaçıp sayfayı genişletiyordu (Taramalar ekranında 1440px pencerede 1894px). *Bu belge hazırlanırken bulundu ve düzeltildi.* |

Son tam tarama sonucu (yerel, 8 kritik sayfa × 4 görünüm × 6 durum): **otomatik ihlal 0**, manuel kontrol gerektiren 34 bulgu. Firefox ve WebKit'te ana sayfa ve iletişim sayfası da 0 ihlal.

---

## 11. Erişilebilirlik Merkezi (yönetim)

Adres: `/admin/erisilebilirlik` · sol menüde "Erişilebilirlik Merkezi". Her ekran oturum ve rol kontrolü yapar; veritabanı veya tablolar yoksa çökmez, kurulum notu gösterir.

| # | Bölüm | Adres |
|---|---|---|
| 1 | Genel Bakış | `/admin/erisilebilirlik` |
| 2 | Taramalar (+ iş detayı) | `/taramalar`, `/taramalar/[id]` |
| 3 | Sorunlar (+ sorun detayı) | `/sorunlar`, `/sorunlar/[id]` |
| 4 | Kalite & SEO | `/kalite-seo` |
| 5 | İçerik & Medya | `/icerik-medya` |
| 6 | Belgeler | `/belgeler` |
| 7 | Manuel Denetim | `/manuel-denetim` |
| 8 | Ziyaretçi Bildirimleri | `/bildirimler` |
| 9 | Raporlar (+ yazdırılabilir rapor, dışa aktarma) | `/raporlar`, `/raporlar/yazdir`, `/raporlar/export` |
| 10 | Asistan Ayarları | `/asistan` |
| 11 | Tarama Ayarları | `/ayarlar` |

### 11.1 Genel Bakış

![Genel Bakış: kritik/ciddi/orta/düşük açık sorun kartları, manuel kontrol ve istisna sayıları, son tarama özeti ve otomatik kontrol sonucu](erisilebilirlik-modulu/40-admin-genel-bakis.png)

- Önem derecesine göre **açık** erişilebilirlik ihlalleri; "manuel kontrol gerekli" ayrı sayılır ve başarısızlık sayılmaz; gerekçeli istisnalar (süresi geçenler vurgulanır).
- Son tarama: taranan / başarılı / başarısız / taranamayan sayfalar; yeni / çözülmüş görünen / yeniden açılan bulgular.
- **Otomatik kontrol sonucu**: yöntem sürümü (`a11y-auto-v1`) ve açıklamasıyla; site ortalamasının yanında **en kötü sayfa** ve **puan dağılımı** — ortalama tek başına gösterilmez. Taranamayan sayfa başarılı sayılmaz.
- Zaman içindeki değişim (son 12 tarama; grafik + aynı verinin tablosu), bileşene ve sayfa türüne göre öncelik tabloları.

**Puan yöntemi (`a11y-auto-v1`).** Yalnız başarıyla taranan sayfalar ve yalnız başarısız erişilebilirlik bulguları hesaba girer. Sayfa puanı = 100 − Σ(ağırlık × etkilenen öğe, kural başına en fazla 3); ağırlıklar kritik 10, ciddi 5, orta 2, düşük 1. Manuel kontrol bulguları, SEO/kalite bulguları ve taranamayan sayfalar puana girmez. **Bu değer bir uygunluk yüzdesi değildir.**

### 11.2 Taramalar

![Taramalar: "Taramayı panel değil, runner çalıştırır" bilgisi, zamanlanmış tarama durumu ve yeni tarama formu](erisilebilirlik-modulu/41-admin-taramalar.png)

- Panel tarayıcı **çalıştırmaz** (Cloudflare Worker'ın HTTP isteği içinde tarayıcı açılmaz); yalnız tarama isteğini kuyruğa yazar. Kuyruğu yerelde `npm run a11y:worker -- --once` veya CI işler. Ekran bunu açıkça yazar; 15 dakikadan uzun bekleyen işte uyarı çıkar.
- Yeni tarama: kapsam (tek sayfa / seçili sayfalar / sitemap sınırlı), taban adres (yalnız izinli kökler), görünüm varyantları, etkileşim durumları, eşzamanlılık / zaman aşımı / yeniden deneme sınırları. Kuyrukta en fazla 5 iş bekleyebilir.
- İş listesi: durum, tetikleyici, ilerleme, süre, hata · iptal · "Tekrar dene". Çalışan iş varken ekran görünürken 10 sn'de bir yenilenir (`prefers-reduced-motion`'da duraklatılmış başlar, kullanıcı durdurabilir).
- Zamanlanmış tarama "kurulu" gibi gösterilmez: ayar değeri ve son zamanlanmış işin tarihi (yoksa "Henüz zamanlanmış tarama kaydı yok") yazar.

![Tarama iş detayı: başlık, özet sayılar ve sayfa sonuçları](erisilebilirlik-modulu/42-admin-tarama-detayi.png)

![Motor kaydı: axe-core sürümü, Playwright ve tarayıcı sürümü, çalıştırılan etiketler, kural sayısı ve test sınırları notu](erisilebilirlik-modulu/42b-admin-motor-kaydi.png)

Motor kaydı her işle saklanır: axe-core ve Playwright sürümü, tarayıcı adı ve sürümü, çalıştırılan etiketler (`wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice`), kural sayısı ve kural listesi (her kuralın etiketleriyle), puan yöntemi sürümü, viewport'lar ve "otomatik testler WCAG ölçütlerinin bir kısmını doğrular" notu. Varyantlar (varsayılan, metin %200 …) ayrı özetlenir.

### 11.3 Sorunlar

![Sorun Kaydı: filtreler ve sorun tablosu](erisilebilirlik-modulu/43-admin-sorunlar.png)

- **Filtreler** (JS gerektirmeyen GET formu): durum, önem, tür (erişilebilirlik / kalite / SEO), sonuç tipi (ihlal / manuel kontrol), WCAG ölçütü, sayfa türü, bileşen, baseline.
- **Bileşene göre grupla**: aynı ortak bileşenden gelen sorunlar tek grupta.
- Sütunlar: önem, kural, WCAG, bileşen, sayfa sayısı, durum, ilk/son görülme, tekrar test.

![Sorunlar bileşene göre gruplanmış](erisilebilirlik-modulu/44-admin-sorunlar-bilesen.png)

![Sorun detayı: önem, Gerekçeli İstisna durumu, kural, WCAG 1.4.4, bileşen, ilk/son görülme, tekrar test; istisna gerekçesi, sorumlu ve yeniden değerlendirme tarihi; açıklama, düzeltme önerisi, örnek seçici ve temizlenmiş HTML örneği](erisilebilirlik-modulu/45-admin-sorun-detayi.png)

**Kararlı bulgu kimliği.** Kimlik = tür + sonuç tipi + kural + bileşen (URL içermez). Header'daki aynı sorun 30 sayfada tek sorun olarak görünür; etkilediği adresler "geçiş" kayıtlarında listelenir. Seçicideki kararsız parçalar (React kimlikleri, `nth-child`) atılır, böylece içerik değişince kimlik oynamaz.

**Durumlar ve geçişler**

| Durum | Elle geçilebilen | Not |
|---|---|---|
| Yeni | İnceleniyor, Düzeltildi, Gerekçeli İstisna | |
| İnceleniyor | Yeni, Düzeltildi, Gerekçeli İstisna | |
| Düzeltildi | İnceleniyor | Tekrar görülürse tarama **Yeniden Açıldı** yapar |
| Yeniden Açıldı | İnceleniyor, Düzeltildi, Gerekçeli İstisna | Yalnız tarama atar |
| Gerekçeli İstisna | İnceleniyor | Süresi dolup tekrar görülürse yeniden açılır |

- **İstisna** için gerekçe (en az 20 karakter), sorumlu ve yeniden değerlendirme tarihi zorunludur; tarih en fazla 365 gün sonrası olabilir — süresiz sessiz muafiyet yoktur.
- Taranan sayfada daha önce görülüp bu kez görülmeyen sorun **otomatik "Düzeltildi" yapılmaz**; "tekrar test: geçti" yazılır ve yönetici onaylar.
- **Baseline** işareti (gerekçe zorunlu) CI kapısının yalnız yeni sorunlarda düşmesini sağlar; baseline sorunları raporlarda görünür kalır.
- Detayda: tüm adresler, örnek seçici, **temizlenmiş** HTML örneği (her zaman metin olarak gösterilir, asla HTML olarak çizilmez), açıklama, Türkçe düzeltme önerisi, kural belgesi bağlantısı, not, olay geçmişi.

### 11.4 Kalite & SEO

![Kalite ve SEO Kontrolleri ekranı](erisilebilirlik-modulu/46-admin-kalite-seo.png)

Kırık dahili bağlantı, eksik görsel, eksik/tekrarlı title ve meta description, canonical yok/tutarsız, robots/noindex, `<html lang>` tutarsızlığı, başlık hiyerarşisi ve belirsiz bağlantı metni ("tıkla", "buraya", "devamı"). Bu kontroller mevcut SEO modülünün içinde yaşar (`src/lib/seo/page-checks.ts`) — ikinci bir sistem kurulmadı. **Erişilebilirlik puanına girmez**; hiçbir metadata, canonical, sitemap veya schema otomatik değiştirilmez. Site "Çok Yakında" modundayken noindex beklenen durum olarak bilgi notu düşer.

### 11.5 İçerik & Medya

![İçerik ve Medya İncelemesi: görsel ALT durumu kartları ve içerik kayıtları tablosu](erisilebilirlik-modulu/47-admin-icerik-medya.png)

- **Görseller**: toplam, ALT eksik (dekoratif olmayan + ALT boş), dekoratif, ALT'ı gözden geçirilmemiş; her satırdan medya kütüphanesindeki kayda bağlantı.
- **İçerik kayıtları** (tüm içerik türleri): son kontrol, kritik/ciddi bulgu sayısı, dil, inceleme durumu, video/ses durumu (altyazı / transkript / sesli betimleme). "Kontrolü çalıştır" (tek kayıt) ve "Tümünü kontrol et" (15'er kayıt, sayfalı). Kontroller içerik veya SEO metnini değiştirmez.

### 11.6 Belgeler

![Belge Envanteri ekranı](erisilebilirlik-modulu/48-admin-belgeler.png)

PDF/DOCX envanteri (medya kütüphanesi + içerik gövdelerindeki bağlantılar). Yönetici eylemiyle, tek belge ve en fazla 10 MB olarak otomatik **gözlemler**: PDF'te başlık, dil, etiketli PDF göstergesi (`/MarkInfo`, `/StructTreeRoot`), metin katmanı, sayfa sayısı, şifreleme; DOCX'te başlık, dil, başlık stilleri, açıklamasız görseller. Okuma sırası her zaman "manuel inceleme gerekli". Durumlar: bekliyor / inceleniyor / kabul edilebilir / düzeltme gerekli / HTML alternatif. Ekranda: **"Otomatik gözlem belge uygunluğunu kanıtlamaz."**

### 11.7 Manuel Denetim

![Manuel Denetim Kayıtları: yeni kayıt formu (WCAG 2.2 ölçütü, başlık, yöntem, sonuç, tarih, kapsam, not, kanıt) ve kayıt tablosu](erisilebilirlik-modulu/49-admin-manuel-denetim.png)

WCAG 2.2 A/AA ölçütü (31 A + 24 AA; 4.1.1 2.2'de kaldırıldığı için yok), başlık, yöntem (klavye, VoiceOver, NVDA, JAWS, TalkBack, zoom, uzman, diğer), sonuç (geçti / kısmen / kaldı / uygulanamaz / test edilmedi), kapsam, not (kaldı/kısmen için zorunlu), kanıt bağlantısı. Denetleyen **oturumdaki kullanıcıdan** alınır. Bu kayıtlar ACR kanıt tablosunda ve açıklama taslağında "manuel sonuç" olarak görünür. Değişiklik geçmişi tutulur.

### 11.8 Ziyaretçi Bildirimleri

![Ziyaretçi Bildirimleri: kategori, sayfa, mesaj, maskelenmiş e-posta ve durum sütunları](erisilebilirlik-modulu/50-admin-ziyaretci-bildirimleri.png)

Panelin "Sorun bildir" formundan gelen kayıtlar. E-posta adresleri **varsayılan olarak maskelenir** (açmak için `?eposta=goster`). Durum: yeni / işleniyor / kapandı. Silme iki adımlı onayla yapılır; değişiklik geçmişine mesaj veya e-posta kopyalanmaz. Kayıt alındığında, bildirim alıcıları tanımlı ve Mailgun yapılandırılmışsa yöneticiye düz metin e-posta gider (ziyaretçinin e-postası içinde yer almaz).

### 11.9 Raporlar

![Raporlar ve Açıklama: rapor kaynağı seçimi, JSON/CSV dışa aktarma düğmeleri, PDF notu ve erişilebilirlik açıklaması taslağı](erisilebilirlik-modulu/51-admin-raporlar.png)

- **Dışa aktarma**: JSON (tam rapor), CSV (sorunlar / sayfalar / motor kaydı ve test sınırları). Tarih, URL, sürüm, kural seti ve test sınırlarını içerir; **ziyaretçi bildirimleri, kişi adları, notlar, istisna sorumlusu dışa aktarılmaz**. CSV formül enjeksiyonuna karşı kaçışlıdır. Yanıt `private, no-store`.
- **PDF**: projede PDF üretim altyapısı yok; erişilebilir **yazdırılabilir HTML rapor** + tarayıcının "Yazdır → PDF olarak kaydet" komutu.

![Yazdırılabilir rapor görünümü: tek başlık, özet ve başlıklı tablolar](erisilebilirlik-modulu/52-admin-yazdirilabilir-rapor.png)

- **Erişilebilirlik açıklaması taslağı**: yalnız doğrulanmış kayıtlardan üretilir (son tarama tarihi, kapsamı ve motoru; manuel denetim sonuçları; bilinen açık sorunlar ve gerekçeli istisnalar; iletişim yolu). **"Uyumludur" hükmü kurmaz.** Yönetici düzenleyip "metni gözden geçirdim" onayıyla kaydeder; panelin Yardım bölümünde gösterilir.

![Erişilebilirlik açıklaması taslağı: Türkçe ve İngilizce metin alanları ve gözden geçirme onayı](erisilebilirlik-modulu/51b-admin-aciklama-taslagi.png)

- **ACR/VPAT kanıt tablosu**: her WCAG 2.2 A/AA ölçütü için otomatik kural kapsamı (motor kaydındaki kural→ölçüt eşlemesi), son otomatik sonuç, manuel denetim sonucu ve kanıt. ACR hükmünü ("Destekler / Kısmen destekler") **otomatik vermez**; sütun "Uzman değerlendirmesi gerekli" der. Üstte: "Bu tablo resmî bir ACR/VPAT veya sertifika değildir."

![ACR/VPAT kanıt tablosunun ilk bölümü](erisilebilirlik-modulu/51c-admin-acr-kanit-tablosu.png)

### 11.10 Asistan Ayarları

![Ziyaretçi Asistanı Ayarları: panel aç/kapa, düğme tonu ve özellik listesi](erisilebilirlik-modulu/53-admin-asistan-ayarlari.png)

| Alan | İçerik |
|---|---|
| Panel | Asistanı tamamen aç/kapa (kaynak kod erişilebilirliği etkilenmez) |
| Düğme tonu | Koyu / Açık / Bilgi mavisi — yalnız resmî palet |
| Özellikler | 28 özellik grubu ayrı ayrı aç/kapa. Kapatılan özellik panelde gizlenir **ve** profil veya eski kayıtlı ayar onu açamaz. |
| Profiller ve sıralama | Aç/kapa + Yukarı/Aşağı (sürükle-bırak yok; klavyeyle erişilebilir, yeni sıra duyurulur) |
| Hızlı ayar kartları ve sıralama | Aynı desen; bağlı özelliği kapalı kartın yanında "(özellik kapalı — panelde görünmez)" notu |
| Panel varsayılanları | Dil, düğme konumu/boyutu/simgesi, panel boyutu |
| Destek iletişimi | Destek e-postası + "doğrulandı" onayı — doğrulanmamış adres public'te gösterilmez |
| Erişilebilirlik açıklaması | TR/EN + gözden geçirme tarihi |
| Terim sözlüğü | Terim + tanım + dil; elle girilir, otomatik üretilmez (en fazla 300 terim) |
| Ziyaretçi varsayılanları | Yeni ziyaretçiye uygulanacak ayarlar — "çoğunlukla boş bırakılması önerilir" uyarılı açılır alanda |

Kayıt sürüm kontrollüdür: başka sekmede değiştirilmişse "sayfayı yenileyin" uyarısıyla yazmaz.

![Özellikler alanı: özellik grupları onay kutuları](erisilebilirlik-modulu/53b-admin-ozellikler.png)

![Hızlı ayar kartları ve sıralama: 28 kart, her satırda aç/kapa onay kutusu ve Yukarı/Aşağı düğmeleri](erisilebilirlik-modulu/53c-admin-kart-siralama.png)

### 11.11 Tarama Ayarları

![Tarama, İzleme ve Bildirim Ayarları formu](erisilebilirlik-modulu/54-admin-tarama-ayarlari.png)

| Alan | Varsayılan |
|---|---|
| Taban adres | `https://anadomain.com` (yalnız izinli kökler) |
| En fazla sayfa / eşzamanlılık / sayfa zaman aşımı / yeniden deneme | 40 / 2 / 30 sn / 1 (üst sınırlar 200 / 4 / 120 sn / 3) |
| Varyantlar | Varsayılan, metin %200, yüksek kontrast (koyu), 320 px yeniden akış |
| Etkileşim durumları | İlk yükleme, mobil menü, arama katmanı, çerez paneli, form hata durumu, erişilebilirlik paneli |
| Sıklık | Kapalı / günlük / haftalık — "CI kurulu değilse zamanlanmış tarama ÇALIŞMAZ" uyarısı |
| Kritik yollar | `/`, `/blog`, `/projeler`, `/hizmetler`, `/iletisim`, `/hakkimda` |
| CI kapısı | Yeni kritik/ciddi regresyonda başarısız ol: açık |
| Bildirimler | Alıcılar (en fazla 10) · yeni kritik/ciddi · yeniden açılan · haftalık özet (varsayılan kapalı) |
| Saklama süresi | 180 gün (30–730) |

![CMS yayın kontrolleri: yayın öncesi uyarı ve kritik hatada yayını engelleme seçenekleri](erisilebilirlik-modulu/54b-admin-cms-yayin-kontrolu.png)

---

## 12. Tarama motoru

Gerçek tarayıcıda (Playwright) axe-core 4.13 çalıştırır. Yalnız Node/CLI'da çalışır; uygulama koduna (Worker) girmez.

### 12.1 Komutlar

```bash
# Tek seferlik tarama (DB'siz; yalnız dosya raporu)
DATABASE_URL= npm run a11y:scan -- --base http://localhost:5959 --critical --no-db --out ./a11y-reports/deneme

# Kapsam seçenekleri
npm run a11y:scan -- --url https://anadomain.com/blog
npm run a11y:scan -- --paths /,/iletisim
npm run a11y:scan -- --sitemap
npm run a11y:scan -- --critical --browser firefox    # chromium (varsayılan) | firefox | webkit

# Panelden kuyruğa yazılan işleri işle
npm run a11y:worker -- --once          # veya --loop --interval 30

# CI kapısı (baseline dışı yeni kritik/ciddi ihlal → çıkış kodu 1)
npm run a11y:gate
npm run a11y:gate -- --update-baseline --reason "…" --review-at 2027-02-01

# Saklama politikası (varsayılan kuru çalışma; silmek için --apply)
npm run a11y:retention -- --apply
```

Ayrıntılı runbook: [`docs/ACCESSIBILITY-SCANNING.md`](ACCESSIBILITY-SCANNING.md).

### 12.2 Ne taranır

| Boyut | Değerler |
|---|---|
| **Varyantlar** (ayrı raporlanır) | Varsayılan · Metin %200 · Yüksek kontrast koyu · Yüksek kontrast açık · Koyu tema · 320 CSS px yeniden akış |
| **Etkileşim durumları** | İlk yükleme · Mobil menü açık · Arama katmanı açık · Çerez paneli açık · Form hata durumu (form boş gönderilir; tüm POST istekleri iptal edilir, gerçek veri **asla** gönderilmez) · Erişilebilirlik paneli açık |
| **axe etiketleri** | `wcag2a, wcag2aa, wcag21a, wcag21aa, wcag22aa, best-practice` |
| **Özel kurallar** | Klavye odağı görünürlüğü (2.4.7) · odağın sabit katman altında kalması (2.4.11) · pozitif tabindex (2.4.3) · 320 px yatay taşma (1.4.10) · %200 metinde kırpılma (1.4.4, manuel) · altyazısız video / transkriptsiz gömülü video (1.2.x, manuel) · otomatik oynayan medya (1.4.2) |
| **Kalite / SEO** | §11.4 |

Sonuçlar üç gruba ayrılır: **ihlal** (başarısız, puana girer), **manuel kontrol gerekli** (axe'ın "incomplete" sonucu — başarısızlık değil), **kalite/SEO** (puana girmez). Sayfa durumları: geçti / başarısız / hata / atlandı.

### 12.3 Sınırlar ve kuyruk

- Eşzamanlılık 1–4, en fazla 200 sayfa, sayfa zaman aşımı, ağ hatasında yeniden deneme, toplam iş süresi tavanı.
- Panelden iptal (`cancelling`) sayfalar arasında okunur; kalan sayfalar atlanır. CLI'da Ctrl+C temiz kapanış yapar.
- Runner işi atomik olarak alır (kilit + heartbeat); 2 dakika heartbeat vermeyen iş "runner kayboldu" ile başarısız sayılır.
- Raporlar: `report.json`, `issues.csv`, `pages.csv` ve erişilebilir `report.html`. `a11y-reports/` dizini git'e girmez.

---

## 13. İzleme, bildirim, CI ve saklama

| Konu | Davranış |
|---|---|
| **Bildirim tetikleyicileri** | Yeni kritik/ciddi sorun · yeniden açılan sorun · isteğe bağlı haftalık özet (değişiklik olmasa da) |
| **Birleştirme** | Bir taramadaki tüm yeni sorunlar **tek e-posta**. Aynı sorun kümesi ikinci kez gönderilmez (`a11y_notifications` tekilleştirme). Tavan: saatte 2, günde 3 e-posta. |
| **Kanal** | Mevcut Mailgun altyapısı. Slack/webhook altyapısı olmadığı için eklenmedi. Mailgun yapılandırılmamışsa bildirim "atlandı" olur; tarama düşmez. |
| **E-posta içeriği** | Sayılar + en fazla 10 sorun başlığı + panel bağlantısı. HTML örneği ve seçici e-postaya girmez. |
| **CI** | `.github/workflows/accessibility.yml` — PR, `main`'e push, günlük cron, elle tetikleme, deploy sonrası (`repository_dispatch: post-deploy`, `deployment_status`). Secret'lar: `A11Y_DATABASE_URL`, `MAILGUN_API_KEY`, `MAILGUN_DOMAIN`, `MAILGUN_FROM_EMAIL`. **Secret'lar tanımlanmadan iş akışı çalışmaz** — bu belgede kurulum durumu doğrulanmadı. |
| **CI kapısı** | Kritik sayfalar taranır; baseline dışında yeni kritik/ciddi ihlal varsa ve ayar açıksa CI düşer. Baseline DB'de veya repoda `a11y-baseline.json` olarak tutulur; her girdinin gerekçesi ve yeniden değerlendirme tarihi vardır, süresi geçmiş girdi kapıyı düşürür. |
| **Saklama** | Sayfa satırları ve geçiş kayıtları: 180 gün (ayarlanabilir; iş özetleri kalır). Ziyaretçi bildirimleri (e-posta dahil): 365 gün. Bildirim kayıtları: 365 gün. Silme varsayılan olarak kuru çalışmadır; `--apply` gerekir. |

---

## 14. CMS içerik, medya ve belge iş akışı

**Yayın öncesi kontrol.** İçerik editöründe gövde, sunucuda yayın kapısıyla aynı kodla ölçülür (900 ms gecikmeyle). Kontroller:

| Bulgu | Önem |
|---|---|
| Anlamlı görselde ALT yok · Boş bağlantı metni | **Kritik** |
| Başlık seviyesi atlama · gövdede h1 · boş başlık | Ciddi / orta |
| Anlaşılmaz bağlantı metni ("tıkla", "buraya", "devamı", "read more") · metni URL olan bağlantı | Orta |
| `th`'siz tablo · sahte liste ("• " ile başlayan paragraflar) · uzun tümü büyük harf · `tr` dışı dil | Orta / düşük |
| Dekoratif işaretli ama ALT dolu görsel · ALT doğrulanamadı | Düşük |
| Video gömmesi | Manuel kontrol |

- **Uyarı** (`warnBeforePublish`, varsayılan açık): bulgular editörde erişilebilir bir listede gösterilir.
- **Engel** (`blockOnCritical`, varsayılan kapalı): durum "Yayında"ya geçerken **yeni** kritik bulgu varsa yayın sunucu tarafında reddedilir. Kayıt zaten yayındaysa canlı gövdenin bulguları taban alınır.
- **Taslak kaydetme hiçbir koşulda engellenmez.**
- Ayar okunamazsa engelleme yapılmaz, yalnız uyarı döner (fail-open). Bunun nedeni, kapının bir içerik kalitesi kontrolü olması (güvenlik sınırı değil) ve migration'ın içerik yayınlamanın ön koşulu olmamasıdır.

**Medya kütüphanesi.** Görsel düzenleme formuna "Dekoratif görsel (ALT boş bırakılır)" ve "ALT metni gözden geçirildi" işaretleri eklendi. Dekoratif işaretliyken ALT doluysa uyarı ve "ALT'ı temizle" düğmesi çıkar (ALT otomatik silinmez); dekoratif değil ve ALT boşsa "Eksik" uyarısı çıkar. İşaretler ayrı tabloda tutulur; tablo yoksa bu alanlar gizlenir, kütüphanenin mevcut işlevi bozulmaz.

![Medya kütüphanesi ekranı](erisilebilirlik-modulu/55-cms-medya-kutuphanesi.png)

**AI.** Projede AI altyapısı yok; ALT, açıklama veya sadeleştirme taslağı üreten bir özellik eklenmedi. Orijinal içerik ve SEO metinleri hiçbir kontrol tarafından değiştirilmez.

---

## 15. Veri modeli

Migration: `drizzle/0022_accessibility.sql` — **yalnız yeni tablolar**; mevcut hiçbir tabloya kolon eklenmedi (ör. görselin dekoratif işareti `media_assets`'e değil ayrı tabloya yazılır). Tablolar yokken kod 42P01 hatasını "kurulum durumu" olarak yorumlar.

| Tablo | İçerik |
|---|---|
| `a11y_settings` | Tek satır: asistan yapılandırması, tarama yapılandırması, CMS kapısı, sürüm |
| `a11y_change_log` | Ayar / sorun / manuel denetim / belge / medya / içerik değişiklik geçmişi |
| `a11y_scan_jobs` | Tarama işleri: durum, tetikleyici, kapsam, sınırlar, motor kaydı, ilerleme, özet, puan, revision, kilit/heartbeat |
| `a11y_scan_pages` | İş × adres × varyant × durum sonuçları, SEO gözlemleri |
| `a11y_issues` | Kararlı kimlikli sorunlar: kural, WCAG, önem, bileşen, durum, istisna alanları, baseline, tekrar test |
| `a11y_issue_occurrences` | Sorunun görüldüğü adres/varyant/durum/seçici ve temizlenmiş HTML |
| `a11y_issue_events` | Durum değişiklikleri, not, kanıt |
| `a11y_manual_audits` | Manuel denetim kayıtları |
| `a11y_documents` | PDF/DOCX envanteri ve inceleme |
| `a11y_media_reviews` | Görsel dekoratif / ALT gözden geçirildi işaretleri |
| `a11y_content_reviews` | İçerik dili, inceleme durumu, son kontrol, video/ses durumu |
| `a11y_feedback` | Ziyaretçi bildirimleri (e-posta isteğe bağlı; IP saklanmaz) |
| `a11y_notifications` | Bildirim tekilleştirme kaydı |

---

## 16. Güvenlik

| Alan | Önlem |
|---|---|
| Yetki | Her Server Action ve Route Handler ilk satırda oturum + rol kontrolü yapar; layout kontrolüne güvenilmez. Kimlik/rol istemciden alınmaz. Oturumsuz çağrıda 13 eylemin hiçbiri DB bağlantısı açmaz (testli). |
| IDOR / girdi | Kimlikler biçim kontrolünden geçer, kaydın varlığı satır kilidiyle doğrulanır; tüm sorgular parametrik; LIKE kaçışlı. |
| SSRF | Taranabilen kökler sabit izin listesindedir (`anadomain.com`, `www.anadomain.com`, `localhost:5959`); ek geliştirme kökü yalnız ortam değişkeniyle açıkça verilir. Kullanıcı bilgili adres, `javascript:`/`file:`, özel IP (10.x, 169.254.x …) reddedilir; izinli kök dışına yönlendirme ve belge gezinmesi tarayıcıda engellenir; kimlik bilgisi taşıyabilecek sorgu parametreleri temizlenir. |
| Rapor gizliliği | HTML örneklerinde form değerleri, gizli alanlar, token/anahtar nitelikleri, URL sorgu parametreleri, e-posta ve telefon maskelenir. Raporlar varsayılan olarak özeldir (`no-store`, oturum zorunlu). |
| Public bildirim ucu | Honeypot, zaman kontrolü, hız sınırı (anahtar IP'nin SHA-256 özeti; IP saklanmaz), alan doğrulama, yalnız site içi yol, spam puanı. |
| Komutlar | Sesli/yazılı komut şeması form gönderme, veri silme ve bağlantı açmayı içermez. |

---

## 17. Dosya yapısı ve testler

```
src/modules/accessibility/
├── domain/        settings, profiles, state, dom, bootstrap, config, i18n, commands,
│                  tiles, audit, wcag, feedback, content-checks, document-inspect
├── client/        store, tts, execute, sun, sun-location, page-dom, media-control,
│                  reader-extract, glossary-match
├── server/        settings-repository, public-config, auth, db-guard, ingest, notifications,
│                  retention, jobs/issues/manual-audit/feedback/review repository'leri,
│                  reports, statement, documents, content-gate, actions/*
└── scanner/       engine, states, variants, custom-rules, crawl, report, runner, gate, rule-text
src/components/public/a11y/       assistant, launcher, panel, controls, icons, tile-icons,
                                  sections/*, tools/*
src/components/public/layout/focus-guard.tsx
src/components/admin/a11y/        sayfa kabuğu, navigasyon, formlar, tablolar, content/*
src/app/(admin)/admin/(protected)/erisilebilirlik/   13 sayfa + export route
src/lib/seo/page-checks.ts
src/styles/a11y.css
scripts/a11y-scan.ts
.github/workflows/accessibility.yml
drizzle/0022_accessibility.sql
```

**Testler** (`tests/`): `a11y-core`, `a11y-tiles`, `a11y-commands`, `a11y-css-tokens`, `a11y-sun`, `a11y-glossary`, `a11y-audit-domain`, `a11y-ingest`, `a11y-gate`, `a11y-notify`, `a11y-scanner-utils`, `a11y-scan-db`, `a11y-admin-actions`, `a11y-feedback`, `a11y-repositories`, `a11y-content-checks`, `a11y-cms-gate`, `a11y-documents`, `seo-page-checks`. DB testleri yerel PostgreSQL'de geçici veritabanı açar ve siler.

---

## 18. Bilinen sınırlar ve açık kararlar

**Sınırlar**
- Yakınlaştırılmış görünüm %200'de masaüstünde yatay kaydırma oluşturur (CSS `zoom` medya sorgularını yeniden değerlendirmez). Tarayıcının kendi yakınlaştırması etkilenmez.
- 320 px ve %200 metin **aynı anda** açıkken /blog kartlarında taşma kalır; WCAG bu birleşimi zorunlu tutmaz, ikisi ayrı ayrı temizdir.
- Bileşenlerde doğrudan yazılmış bazı renkler (dekoratif diyagram, gradyanlar) temadan etkilenmez.
- Sesli okuma ve mikrofonla sesli komut gerçek ses/mikrofonla doğrulanmadı; GIF/SVG dondurma sitede örnek olmadığı için tarayıcıda denenmedi.
- Sade okuma görünümünde yan yana duran iki öğenin metni boşluksuz birleşebilir (ör. "GMT+3Pazarlama" — §7.2 görüntüsünde görülüyor).
- HTML örneği temizleyicisi SVG `viewBox` sayılarını telefon numarası sanıp maskeleyebilir (gizlilik yönünde zararsız aşırı maskeleme; §11.3 görüntüsünde `viewBox="[telefon]"`).
- Odak örtülme ölçümü zamanlamaya duyarlıdır; Firefox'ta Tab yürüyüşü bağlantıları atlayabilir.
- İçerik şemasında video alanı yok; altyazı/transkript durumu elle işaretlenir.
- Gerçek Safari/VoiceOver, NVDA, TalkBack denemeleri yapılmadı — sonuçları "Manuel Denetim" ekranına kaydedilmeli.

**Açık kararlar**
- CI secret'ları ve isteğe bağlı `a11y-baseline.json` (kurulum durumu bu belgede doğrulanmadı).
- Medya yüklemenin PDF/DOCX kabul etmesi (bugün yalnız görsel kabul ediliyor; belge envanterinin medya kaynağı bu yüzden boş).
- Asistan Ayarları'nda erişilebilirlik açıklamasının ve terim sözlüğünün doldurulması.

---

## 19. UserWay ile karşılaştırma

**UserWay'de olup burada olmayan / farklı olanlar**

| UserWay | Bu sitede |
|---|---|
| Çok dilli panel | Yalnız TR/EN (sözlüğe çeviri eklenerek genişletilebilir) |
| `Ctrl+U` kısayolu | `Alt+Shift+A` (Ctrl+U tarayıcının "kaynağı görüntüle" kısayolu) |
| "Kontrast +" ters çevirme ve koyu kontrastı tek kartta döndürür | Ayrı kartlar: Kontrast +, Koyu tema, Renkleri ters çevir |
| "İmleç" kartı okuma maskesi/kılavuzunu da içerir | Ayrı kartlar: İmleç, Okuma kılavuzu, Odak maskesi |
| "Âmâ", "Motor engelli", "Nöbet ve Epileptik" profil adları | Kişiyi etiketlemeyen, tıbbi iddia içermeyen adlar |
| Ücretli sürümde AI ile otomatik kod düzeltme / ALT üretimi | Yok — sorunlar kaynak kodda düzeltildi; AI altyapısı yok |
| Bulut yönetim paneli ("Yönet") | Kendi Erişilebilirlik Merkezi |

**Burada olup UserWay ekranlarında görünmeyenler**

Geri alma ve tek tek sıfırlama · kaynak rozeti · kaydırıcıyla ince ayar · koyu/sistem teması · renk ayırt etme paletleri · zamanlanabilir mavi ışık filtresi (gün batımına göre) · metin büyüteci (balon/şerit/mercek) · sade okuma · başlık vurgusu · büyük kontroller · güçlendirilmiş klavye odağı · sayfa yakınlaştırma · medya susturma · sesli ve önizlemeli yazılı komut · terim sözlüğü · panel içinden sorun bildirme · erişilebilirlik açıklaması · "Odaklanma" ve "Kolay kullanım" profilleri · gizlenen düğmeyi footer'dan geri açma · gerçek tarayıcı taraması, sorun kaydı, CI kapısı ve CMS yayın kontrolleri.
