# MASTER PROMPT — Evrensel Web Erişilebilirlik Modülü

## 1. Rol ve amaç

Kıdemli Full-Stack Yazılım Mimarı, UI/UX Uzmanı, Erişilebilirlik Mühendisi ve Yazılım Test Mühendisi olarak hareket et.

Mevcut web projesine **bağımsız, modüler, genişletilebilir ve üretime hazır bir Erişilebilirlik Modülü** geliştir.

Modül üç temel sistemden oluşmalıdır:

1. **Ziyaretçi Erişilebilirlik Asistanı:** Herkese açık sayfalarda kullanıcıların erişilebilirlik tercihlerini yönetebileceği etkileşimli panel.
2. **Erişilebilirlik Merkezi:** Yöneticilerin modülü, denetimleri, sorunları, içerikleri ve raporları yönetebileceği 11 bölümlü yönetim sistemi.
3. **Erişilebilirlik Denetim Altyapısı:** Gerçek tarayıcı testleri, WCAG kontrolleri, CMS yayın denetimleri, CI/CD ve bildirim mekanizmaları.

**Temel hedef:** WCAG 2.2 A/AA gereksinimlerini destekleyen, mevcut projenin tasarımını ve mimarisini koruyan, üçüncü taraf erişilebilirlik widget servislerine bağımlı olmayan bir sistem oluşturmak.

Modülün varlığı, web sitesinin tamamen erişilebilir olduğu anlamına gelmez. Kaynak koddaki erişilebilirlik problemleri ayrıca düzeltilmelidir.

---

## 2. Mimari ve entegrasyon kuralları

Geliştirmeye başlamadan önce mevcut projeyi analiz et:

- Framework, programlama dili ve paket yöneticisi
- Frontend ve backend mimarisi
- Veritabanı ve ORM
- Authentication, authorization ve kullanıcı rolleri
- Mevcut CMS yapısı
- Admin paneli ve navigasyon mimarisi
- Tasarım sistemi, renk token'ları, tipografi, bileşenler
- Deployment ve CI/CD altyapısı
- E-posta ve bildirim servisleri
- Mevcut SEO, medya ve belge yönetimi

**Uyarlama prensipleri:**

- Mevcut teknoloji yığınını kullan.
- Yeni framework, veritabanı veya kimlik doğrulama sistemi kurma.
- Var olan tasarım sistemini ve onaylanmış özellikleri koru.
- Gereksiz bağımlılık veya ücretli servis ekleme.
- Modülü mevcut projeden mantıksal olarak ayrılmış bileşenler, servisler ve veri erişim katmanları halinde geliştir.
- Admin yolu varsayılan olarak `/admin/erisilebilirlik` olsun; mevcut yönetim panelinin URL yapısına uyarlanabilsin.
- Veritabanı tabloları `a11y_` öneki taşısın.
- Modül kurulmamış veya veritabanı migration'ları uygulanmamış olduğunda mevcut site çalışmaya devam etsin.
- Gerçek kullanıcı verilerini koru; üretim ortamında sıfırlama veya yıkıcı migration yapma.
- Modül, diğer projelere taşınabilecek bir yapılandırma ve entegrasyon arayüzüne sahip olsun.

## 3. Ziyaretçi Erişilebilirlik Asistanı

### 3.1. Paneli açma

Üç erişim yöntemi uygula:

1. Ekranda konumlandırılabilir erişilebilirlik başlatıcı düğmesi.
2. Footer içinde **Erişilebilirlik** bağlantısı.
3. `Alt + Shift + A` klavye kısayolu.

Başlatıcı varsayılan olarak sağ altta bulunsun ve etkin ayar sayısını göstersin.

Başlatıcı kullanıcı tarafından gizlenebilse bile footer bağlantısından erişim sürdürülebilsin.

### 3.2. Panel davranışı

Panel aşağıdaki bölümlerden oluşsun:

- Profiller
- Hızlı Ayarlar
- Metin
- Görünüm
- Okuma ve Gezinme
- Panel Ayarları
- Yardım

Bölümler erişilebilir akordeon yapısında olsun. Profiller ve Hızlı Ayarlar başlangıçta açık olsun.

Üst araç çubuğunda şu işlevler bulunsun:

- Son işlemi geri al
- Tüm erişilebilirlik ayarlarını sıfırla
- Bütün bölümleri genişlet/daralt
- Türkçe/İngilizce seçimi
- Normal/büyük panel seçimi
- Etkin ayar sayısı

**Odak yönetimi:**

- Panel `role="dialog"` kullansın ancak modal olmasın.
- Panel açıldığında odak erişilebilir panel başlığına taşınsın.
- `Esc` paneli kapatsın.
- Kapanışta odak açan öğeye geri dönsün.
- Panel açıkken kullanıcı sayfayla etkileşime devam edebilsin.
- Odak tuzağı kurulmasın.
- Değişiklikler ortak bir `aria-live` alanından duyurulsun.

**Boyutlandırma:**

- Normal panel: yaklaşık 400 px
- Büyük panel: yaklaşık 520 px
- Metin büyüdüğünde uyarlanabilir genişlik
- 640 px altındaki ekranlarda tam genişlikli alt panel
- Küçük ekranlarda taşma ve işlev kaybı olmamalı

Panel dili yalnız asistan arayüzüne uygulanmalı; sitenin içerik dilini değiştirmemeli.

---

## 4. Hızlı Ayarlar — 28 özellik

Her hızlı ayar kartı gerçek bir erişilebilirlik özelliğine bağlı çalışmalıdır.

Kartlar ayrı bir ayar deposu oluşturmasın. Kart, ayrıntılı kontrol, profil ve komutlar aynı merkezi durum yönetimini kullansın.

Çok aşamalı kartlar her tıklamada bir sonraki adıma geçsin; son adımdan sonra kapansın.

Ayrıntılı ayarda kart adımlarından farklı değer seçilmişse kartta **Özel** durumu gösterilsin.

Her kartta:

- Özellik adı ve simgesi
- Mevcut durum/değer
- Çok aşamalı özelliklerde adım göstergesi
- Etkinlik göstergesi
- `aria-pressed`
- Ayrı erişilebilir bilgi düğmesi
- Özelliği açıklayan bilgi alanı

bulunsun.

### Uygulanacak 28 hızlı ayar

| No | Özellik | Davranış |
|---|---|---|
| 1 | Sayfayı Oku | Sesli okumayı başlat/durdur |
| 2 | Kontrast + | Yüksek kontrast açık/koyu |
| 3 | Akıllı Kontrast | Düşük kontrastlı metinleri ve kenarlıkları iyileştir |
| 4 | Bağlantıları Vurgula | Alt çizgi ve görsel çerçeve |
| 5 | Büyük Metin | %120, %140, %160, %180, %200 |
| 6 | Metin Boşluğu | Hafif, orta, geniş |
| 7 | Animasyonları Durdur | Animasyon/geçiş/hareket azaltma |
| 8 | Resimleri Gizle | Görselleri gizle, anlamlı ALT metnini koru |
| 9 | Disleksi Dostu | OpenDyslexic / Atkinson Hyperlegible |
| 10 | İmleç | Büyük siyah, büyük beyaz, çok büyük |
| 11 | İpuçları | Açıklama balonları |
| 12 | Sayfa Yapısı | Başlıklar, bölgeler ve bağlantılar |
| 13 | Satır Yüksekliği | 1.6, 1.8, 2.0 |
| 14 | Metin Hizalama | Sol, orta, sağ, iki yana |
| 15 | Doygunluk | Düşük, yüksek, gri |
| 16 | Başlıkları Vurgula | Görsel belirginleştirme |
| 17 | Okuma Kılavuzu | İmleç/odak takip çizgisi |
| 18 | Odak Maskesi | Okunan bölge dışını karart |
| 19 | Metin Büyüteci | Balon, alt şerit, mercek |
| 20 | Sade Okuma | Tek sütunlu okuma modu |
| 21 | Koyu Tema | Koyu/sistem |
| 22 | Renk Ayırt Etme | Yeşil, kırmızı, mavi-sarı, tek renk/desen |
| 23 | Mavi Işık Filtresi | %30, %60 |
| 24 | Sesi Kapat | Site medyasını sustur |
| 25 | Büyük Kontroller | En az 44×44 px etkileşim hedefi |
| 26 | Klavye Odağı | İki tonlu güçlü odak çerçevesi |
| 27 | Yakınlaştır | %120, %150 |
| 28 | Renkleri Ters Çevir | Renk inversiyonu |

Kart görünürlüğü, varsayılan sıralaması ve etkinliği yönetim panelinden değiştirilebilsin.

Bilgi düğmeleri kartın eylemini tetiklemesin. Bilgi kutuları klavye, `Esc` ve odak yönetimiyle çalışsın.

---

## 5. Erişilebilirlik Profilleri — 9 profil

Aşağıdaki profilleri geliştir:

### 5.1. Motor Beceri Desteği
- Büyük kontroller
- Görünür klavye odağı
- Animasyonları durdur
- Açıklama balonları

### 5.2. Ekran Okuyucu ile Kullanım Desteği
- Animasyonları durdur
- Medyayı sustur
- Görünür odak
- Başlıkları belirginleştir

### 5.3. Renk Ayırt Etme Desteği
- Yeşil ayırt etme paleti
- Bağlantı vurgusu
- Akıllı kontrast

### 5.4. Disleksi ve Okuma Desteği
- OpenDyslexic
- Satır aralığı 1.8
- Harf aralığı 0.06em
- Kelime aralığı 0.15em
- Sola hizalama
- Okuma kılavuzu

### 5.5. Az Görenler İçin Görünüm
- Metin %150
- Akıllı kontrast
- Bağlantı vurgusu
- Büyük imleç
- Görünür odak

### 5.6. Bilişsel ve Öğrenme Desteği
- Okunaklı yazı tipi
- Başlık/bağlantı vurgusu
- Animasyonları durdur
- Açıklama balonları
- Terim işaretleri

### 5.7. Hareket ve Yanıp Sönme Hassasiyeti
- Animasyonları durdur
- Medyayı sustur
- Doygunluk %80

### 5.8. Odaklanma Desteği
- Odak maskesi
- Animasyonları durdur
- Başlık vurgusu

### 5.9. Kolay Kullanım
- Büyük kontroller
- Metin %120
- Okunaklı yazı tipi
- Sade okuma
- Görünür odak

**Profil kuralları:**

- Birden fazla profil aynı anda etkinleştirilebilsin.
- Son açılan profil, çakışan profil ayarlarında öncelikli olsun.
- Kullanıcının elle değiştirdiği ayarlar profil ayarlarından üstün olsun.
- Profil kapatılınca yalnız kendi katkısı kaldırılsın.
- Yönetici tarafından kapatılmış özellik profil tarafından açılamasın.
- Her profil etkinleştirilmeden önce hangi ayarları değiştireceğini göstersin.
- Ayarın hangi profilden geldiği arayüzde belirtilebilsin.
- Profil seçimleri sunucuya veya analitik servislere gönderilmesin.

Durum birleştirme sırası:

`Sistem varsayılanları → Yönetici varsayılanları → Profiller → Kullanıcının manuel tercihleri`

Profil adları tıbbi tanı veya garanti içermesin.

---

## 6. Ayrıntılı Erişilebilirlik Kontrolleri

### 6.1. Metin

Şu kontrolleri oluştur:

- Yazı boyutu: %100–200, %10 adımlarla
- Sayfa yakınlaştırma: %100–200
- Satır aralığı: varsayılan veya 1.2–2.4
- Kelime aralığı: 0–0.5em
- Harf aralığı: 0–0.3em
- Metin hizalama: varsayılan, sol, orta, sağ, iki yana
- Font: site fontu, Atkinson Hyperlegible, OpenDyslexic
- Sade okuma
- Başlık vurgulama
- Bağlantı vurgulama
- Metin büyüteci

Yazı ölçeği birikimli uygulanmamalı; her zaman başlangıç font değerine göre hesaplanmalı.

Font dosyalarını yalnız ilgili özellik etkinleşince yükle. Türkçe karakterleri destekle. İkon fontlarına müdahale etme.

### 6.2. Görünüm

- Site teması / açık / koyu / sistem
- Akıllı kontrast
- Yüksek kontrast açık/koyu
- Renkleri ters çevirme
- Gri tonlama
- Doygunluk %0–200
- Renk ayırt etme paletleri
- Mavi ışık filtresi %0–100
- Görselleri gizleme
- Animasyonları durdurma
- Medyayı susturma
- İmleç boyutu ve rengi
- Okuma kılavuzu
- Odak maskesi
- Büyük kontroller
- Görünür klavye odağı

Mavi ışık filtresi şu zamanlama seçeneklerine sahip olsun:

- Kapalı
- Her zaman
- Belirli saat aralığı
- Gün batımından gün doğumuna

Konum yalnız kullanıcıdan izin alındığında kullanılsın, tarayıcıda işlensin ve kaydedilmesin.

**Görünüm mimarisi:** Kurumsal renk değişkenlerini kalıcı değiştirme. Semantik tasarım token'ları üzerinden geçici görünüm modları uygula. Panel ve başlatıcı görsel filtrelerden etkilenmesin. Sabit/yapışkan bileşenlerin konumunu bozan genel `body` filtrelerinden kaçın.

### 6.3. Okuma ve gezinme

Aşağıdaki araçları geliştir:

**Okuma kılavuzu:** Fare imlecini ve klavye odağını takip etsin. Kullanıcının tıklamalarını engellemesin.

**Odak maskesi:** Odak çevresindeki yaklaşık 120 px bant dışını karartsın.

**Metin büyüteci:** Balon, alt şerit ve mercek modları. Fare ve klavyeyle çalışsın. `Esc` ile kapansın. Büyük DOM yapılarında performans için daha hafif moda geçebilsin.

**Sade okuma:** Ana içerikten güvenli metin/başlık yapısı çıkarıp tek sütunlu okuma görünümü oluştursun. Kaynak HTML'yi doğrudan kopyalayarak çalışmasın. Modal odak yönetimi ve çıkışta odak iadesi uygulasın.

**Açıklama balonları:** `title`, `aria-label` ve `abbr` açıklamalarını fare ve klavye odağında erişilebilir şekilde göstersin.

**Terim sözlüğü:** Yönetici tarafından girilen terimleri tanımlarıyla sun. Mümkünse DOM'u değiştirmeyen CSS Custom Highlight API kullan. Desteklenmeyen tarayıcıda özelliğin sınırını açıkça belirt.

**Ana içeriğe geç:** Çalışır bir skip link kullan.

**Görselleri gizle:** Sayfa düzenini koru, anlamlı görsellerin ALT metinlerini göster; dekoratif görsellerin ALT metnini gösterme.

---

## 7. Sesli Okuma ve Komut Sistemi

### 7.1. Sesli okuma

Tarayıcının Web Speech API `speechSynthesis` yeteneğini kullan.

Özellikler:

- Ana içeriği oku
- Seçili metni oku
- Başlat, duraklat, devam et, durdur
- Türkçe/İngilizce konuşma dili
- Ses seçimi
- Konuşma hızı 0.5–2×
- Ses seviyesi
- Uzun metinleri cümle gruplarına bölme
- Sayfa değişiminde okumayı durdurma
- Kullanıcı talebi olmadan otomatik konuşma başlatmama

Ses veya API bulunmadığında açıklayıcı mesaj göster.

Sesli okuma özelliğini ekran okuyucunun yerine geçen bir teknoloji olarak tanıtma.

### 7.2. Sesli komut

- Mikrofon yalnız kullanıcı düğmeye bastığında açılsın.
- Tek komutluk dinleme gerçekleşsin.
- Sürekli dinleme yapılmasın.
- İlk kullanımda tarayıcıların ses verisini harici sunuculara gönderebileceği açıklansın.
- Kullanıcı izni olmadan mikrofon kullanılmasın.
- Tarayıcı desteklemiyorsa yazılı komut gösterilsin.

İzin verilen eylemler yalnız erişilebilirlik ayarları ve güvenli sayfa gezinmesi olsun.

### 7.3. Yazılı doğal dil komutları

Örnek komutlar:

- "Yazıları büyüt."
- "Hareketleri azalt."
- "Koyu temayı aç."
- "Disleksi profilini etkinleştir."
- "Mavi filtreyi aç."
- "Sonraki başlığa geç."
- "Sayfayı oku."

Komutlar ilk aşamada **yerel ve deterministik bir komut çözücü** tarafından yorumlansın.

İşleyiş:

1. Komutu analiz et.
2. İzin verilen eylemleri belirle.
3. Yapılacak değişiklikleri kullanıcıya önizle.
4. Onay alınca uygula.
5. Tüm komutu tek geri alma işlemi olarak kaydet.

Komut motoru hiçbir koşulda form gönderme, hesap silme, veri değiştirme veya bağlantı açma yetkisine sahip olmasın.

Gelecekte AI entegrasyonuna uygun bir `CommandInterpreter` arayüzü tasarla; mevcut projede AI altyapısı yoksa yeni AI servisi ekleme.

### 7.4. Sayfa yapısı gezgini

Üç sekme oluştur:

- Başlıklar: H1–H6 hiyerarşik listesi
- Bölgeler: `header`, `main`, `nav`, `aside`, `footer` ve ARIA landmark'ları
- Bağlantılar: sayfadaki erişilebilir bağlantılar

Öğe seçildiğinde ilgili konuma kaydır ve odağı taşı.

Geçici `tabindex` değerlerini işlem tamamlandığında kaldır.

Sekmeler ok tuşlarıyla çalışsın.

---

## 8. Panel Özelleştirme

Ziyaretçi aşağıdaki seçenekleri değiştirebilsin:

- Panel dili: TR/EN
- Panel boyutu: normal/büyük
- Başlatıcı konumu: sağ alt, sol alt, sağ orta, sol orta
- Başlatıcı boyutu: 48/60 px
- Simge: insan figürü, göz, ayar çubukları, harf
- Başlatıcıyı gizle/göster
- Panel başlığı ve logosunu gizle/göster
- Klavye kısayolunu aç/kapat

Panel başlığı görsel olarak gizlense de erişilebilir adı korunmalı.

**Tümünü sıfırla**, erişilebilirlik değişikliklerini sıfırlamalı; panel dili ve başlatıcı konumu gibi panel tercihlerini korumalı.

---

## 9. Kalıcılık, Gizlilik ve Performans

### 9.1. Durum saklama

- Kullanıcı tercihlerini sürümlü `localStorage` yapısında sakla.
- Kullanıcı profilleri ve ayarları sunucuda saklama.
- Depolama engelliyse bellek üzerinden oturumluk kullanım sağla.
- Bozuk veya eski kayıtları güvenli varsayılanlara döndür.
- Sekmeler arasında tercih değişikliklerini eşitle.
- SPA navigasyonlarında durumu koru.
- İlk boyamadan önce tema ve yazı boyutunu uygula; görünüm sıçramasını önle.
- Yönetim paneli sayfalarında ziyaretçi görünüm ayarlarını uygulama.

### 9.2. Gizlilik

Aşağıdaki bilgileri analitik, veri katmanı veya sunucuya gönderme:

- Etkin erişilebilirlik profilleri
- Görünüm ve okuma tercihleri
- Sesli/yazılı komut içerikleri
- Mavi filtre için kullanılan konum bilgisi

### 9.3. Performans

- Başlatıcı ve kritik başlangıç kodunu küçük tut.
- Panelin ayrıntılı bileşenlerini ve araçlarını isteğe bağlı yükle.
- Gereksiz DOM değişikliklerinden kaçın.
- Ağır efektlerde bellek/CPU sınırları uygula.
- Mevcut Core Web Vitals ve SEO performansını koru.
- Depolama, mikrofon, konuşma veya konum API'si desteklenmediğinde site çalışmaya devam etsin.

---

## 10. Yönetim Paneli — Erişilebilirlik Merkezi

Mevcut admin paneline **Erişilebilirlik Merkezi** modülü ekle.

11 ana bölüm oluştur.

### 10.1. Genel Bakış

Gösterge panelinde:

- Kritik, ciddi, orta, düşük açık sorunlar
- Manuel kontrol bekleyen bulgular
- Gerekçeli istisnalar ve süresi geçenler
- Son tarama tarihi
- Taranan, başarılı, başarısız, taranamayan sayfalar
- Yeni, yeniden açılan ve çözülmüş görünen sorunlar
- Otomatik kontrol sonucu
- En düşük puanlı sayfa
- Sayfa bazlı puan dağılımı
- Son 12 taramanın eğilimi
- Sayfa türü ve bileşene göre sorun dağılımı

**Otomatik puan yöntemi:**

`Sayfa Puanı = 100 − Σ(Önem Ağırlığı × Etkilenen Öğe Sayısı)`

Önem ağırlıkları:

- Kritik: 10
- Ciddi: 5
- Orta: 2
- Düşük: 1

Her kural için etkilenen öğe sayısını en fazla 3 olarak hesapla.

Yalnız başarılı şekilde taranmış sayfalardaki gerçek erişilebilirlik ihlalleri hesaba girsin.

Manuel kontroller, kalite/SEO bulguları ve taranamayan sayfalar puana dahil edilmesin.

Puan yöntemini `a11y-auto-v1` olarak sürümlendir.

**Bu puanı erişilebilirlik uyumluluk yüzdesi olarak sunma.**

### 10.2. Taramalar

- Tek sayfa, seçili sayfalar veya sitemap kapsamı
- Tarayıcı ve varyant seçimi
- Etkileşim durumları
- Maksimum sayfa, concurrency, timeout ve retry
- Kuyruk, ilerleme ve durum takibi
- Tarama iptali ve yeniden deneme
- Tarama detayları ve motor sürümleri
- Zamanlanmış tarama bilgisi
- Kuyruk işini işleyen bağımsız runner

Tarama işlemini HTTP isteği içinde çalıştırma.

Kullanıcının başlattığı işleri kuyruğa ekle; Node/CLI veya uyumlu bağımsız runner üzerinden işle.

En fazla 5 bekleyen iş kuralı uygula.

Çalışan taramalar için 10 saniyelik arayüz yenileme desteği sağla; kullanıcı durdurabilsin ve hareket azaltma tercihini dikkate alsın.

### 10.3. Sorunlar

Şu filtreleri geliştir:

- Durum
- Önem derecesi
- Erişilebilirlik / kalite / SEO
- İhlal / manuel kontrol
- WCAG ölçütü
- Sayfa türü
- Bileşen
- Baseline

Aynı bileşene ait birden fazla sayfadaki bulguları kararlı kimliklerle birleştir.

**Sorun durumları:**

- Yeni
- İnceleniyor
- Düzeltildi
- Yeniden Açıldı
- Gerekçeli İstisna

Durum geçişlerini ve olay geçmişini kaydet.

Gerekçeli istisna için:

- En az 20 karakter açıklama
- Sorumlu
- Yeniden değerlendirme tarihi
- En fazla 365 günlük geçerlilik

zorunlu olsun.

Sorun yeniden görülürse uygun durumda yeniden açılsın.

Bir taramada görünmeyen sorun doğrudan otomatik kapatılmasın; tekrar test sonucu kaydedilip yönetici onayı beklensin.

Detay ekranı; kural, WCAG ölçütü, sayfalar, bileşen, güvenli HTML örneği, seçici, düzeltme önerisi, olay geçmişi ve kanıtları göstersin.

### 10.4. Kalite & SEO

Aşağıdaki kontrolleri yap:

- Kırık dahili bağlantılar
- Eksik görseller
- Eksik/tekrarlanan title
- Eksik/tekrarlanan meta description
- Canonical eksikliği veya tutarsızlığı
- Robots/noindex
- HTML dil niteliği
- Başlık hiyerarşisi
- Belirsiz bağlantı metinleri

Mevcut SEO kontrol altyapısı varsa onu yeniden kullan.

Bu bulgular erişilebilirlik puanına dahil edilmesin.

SEO meta verilerini, schema ve sitemap içeriğini kendiliğinden değiştirme.

### 10.5. İçerik & Medya

- Toplam görsel sayısı
- ALT eksik görseller
- Dekoratif görseller
- ALT gözden geçirme durumları
- İçerik inceleme listesi
- İçerik dili
- Kritik/ciddi içerik hataları
- Video altyazı durumu
- Transkript durumu
- Sesli betimleme durumu
- Tek içerik kontrolü
- Sayfalı toplu kontrol (15 kayıtlık gruplar)

Kontroller orijinal içerikleri ve SEO metinlerini otomatik değiştirmesin.

### 10.6. Belgeler

PDF ve DOCX belge envanteri oluştur.

Medya kütüphanesini ve içeriklerdeki belge bağlantılarını tarayarak kayıt üret.

**PDF gözlemleri:**
- Başlık
- Dil
- Etiketli PDF göstergesi
- Yapı ağacı
- Metin katmanı
- Sayfa sayısı
- Şifreleme

**DOCX gözlemleri:**
- Belge başlığı
- Dil
- Başlık stilleri
- Alternatif metinsiz görseller

Dosya başına varsayılan 10 MB sınırı uygula.

Belge durumları:

- Bekliyor
- İnceleniyor
- Kabul edilebilir
- Düzeltme gerekli
- HTML alternatif

Okuma sırası ve belge uygunluğu için manuel inceleme gerekliliğini belirt.

### 10.7. Manuel Denetim

WCAG 2.2 A/AA ölçütlerine göre manuel test kayıt sistemi geliştir.

Alanlar:

- WCAG ölçütü
- Başlık
- Denetim yöntemi
- Sonuç
- Kapsam
- Not
- Kanıt bağlantısı
- Test tarihi
- Denetleyen kullanıcı

Yöntemler:

- Klavye
- VoiceOver
- NVDA
- JAWS
- TalkBack
- Zoom
- Uzman
- Diğer

Sonuçlar:

- Geçti
- Kısmen geçti
- Kaldı
- Uygulanamaz
- Test edilmedi

Kısmen geçti/kaldı sonuçlarında not zorunlu olsun.

Denetleyen kimliğini aktif oturumdan al.

Geçmiş değişikliklerini sakla.

### 10.8. Ziyaretçi Bildirimleri

Ziyaretçilerin erişilebilirlik sorunlarını bildirebildiği sistemi yönet.

Form kategorileri:

- İçerik
- Klavye
- Ekran okuyucu
- Kontrast
- Medya
- Form
- Asistan
- Diğer

Zorunlu mesaj en az 10 karakter olsun. E-posta isteğe bağlı olsun.

Yalnız site içi sayfa yolu iletilsin.

Yönetim ekranında e-postaları varsayılan olarak maskele.

Durumlar:

- Yeni
- İşleniyor
- Kapandı

Silme işlemi iki aşamalı onay gerektirsin.

Yetkili yöneticilere, mevcut e-posta altyapısı üzerinden bildirim gönderilebilsin.

### 10.9. Raporlar

Geliştir:

- JSON raporu
- CSV dışa aktarma
- Erişilebilir yazdırılabilir HTML raporu
- PDF olarak kaydetmeye uygun yazdırma görünümü
- Erişilebilirlik açıklaması taslağı
- WCAG 2.2 A/AA kanıt matrisi
- ACR/VPAT hazırlık tablosu

Raporlarda:

- Tarama tarihi
- URL ve kapsam
- Motor ve kural seti sürümü
- Test sonuçları
- Otomatik testlerin sınırları
- Açık sorunlar
- Manuel denetim kanıtları

bulunsun.

Kişisel ziyaretçi bildirimlerini ve hassas notları rapora dahil etme.

CSV formül enjeksiyonuna karşı koruma uygula.

ACR/VPAT değerlendirmesinde otomatik uygunluk hükmü üretme; uzman değerlendirmesi gerektiren alanları açıkça belirt.

Erişilebilirlik açıklaması yönetici gözden geçirme onayıyla yayımlansın.

### 10.10. Asistan Ayarları

Yönetici aşağıdakileri değiştirebilsin:

- Asistanı aç/kapat
- Başlatıcı renk tonu
- 28 özelliği ayrı aç/kapat
- Profil görünürlüğü ve sırası
- Hızlı ayar kartları ve sıralaması
- Panel varsayılan dili
- Başlatıcı konumu, boyutu, simgesi
- Panel varsayılan boyutu
- Destek e-postası
- E-posta doğrulama durumu
- TR/EN erişilebilirlik açıklaması
- Açıklamanın gözden geçirme tarihi
- Terim sözlüğü (en fazla 300 kayıt)
- Yeni ziyaretçi varsayılanları

Özellik yönetici tarafından kapatıldığında eski kayıtlı kullanıcı tercihi veya profil üzerinden yeniden etkinleşemesin.

Kart/profil sıralaması klavyeyle yapılabilsin; yalnız sürükle-bırak yöntemine bağımlı olmasın.

Eşzamanlı yönetici değişiklikleri için sürüm kontrolü uygula.

### 10.11. Tarama Ayarları

Varsayılan değerler:

- Maksimum sayfa: 40, üst sınır 200
- Eşzamanlı tarama: 2, üst sınır 4
- Sayfa zaman aşımı: 30 saniye, üst sınır 120
- Yeniden deneme: 1, üst sınır 3
- Sıklık: kapalı/günlük/haftalık
- Saklama: 180 gün, ayarlanabilir 30–730
- Kritik/ciddi regresyonlarda CI başarısızlığı
- Bildirim alıcıları: en fazla 10
- Yeni ve yeniden açılan sorun bildirimleri
- İsteğe bağlı haftalık özet

Kritik URL'leri proje yöneticisi yapılandırabilsin.

CMS yayın öncesi uyarı ve kritik bulguda yayın engelleme ayarları burada yer alsın.

Gerçek zamanlayıcı/runner bağlı değilken zamanlanmış taramayı çalışıyormuş gibi gösterme.

---

## 11. Otomatik Erişilebilirlik Tarama Motoru

Gerçek tarayıcı otomasyonu için **Playwright + axe-core** kullan. Sürümleri bağımlılık yönetiminde sabitle ve tarama kayıtlarında sakla.

### Tarama kapsamı

Tarayıcılar:

- Chromium
- Firefox
- WebKit

WCAG etiketleri:

- `wcag2a`
- `wcag2aa`
- `wcag21a`
- `wcag21aa`
- `wcag22aa`
- `best-practice`

### Görünüm varyantları

- Varsayılan
- Metin %200
- Yüksek kontrast açık
- Yüksek kontrast koyu
- Koyu tema
- 320 CSS px yeniden akış

### Etkileşim durumları

- İlk yükleme
- Mobil menü açık
- Arama katmanı açık
- Çerez paneli açık
- Form hata durumu
- Erişilebilirlik paneli açık

Form hata testi gerçek veri göndermemeli; ilgili POST işlemleri engellenmeli.

### Özel kontroller

- Klavye odağı görünürlüğü
- Odak örtülmesi
- Pozitif `tabindex`
- 320 px yatay taşma
- %200 metin büyütmede kırpılma
- Metin aralığı değişiklikleri
- Altyazısız video
- Transkriptsiz medya
- Otomatik oynayan ses/video
- Başlık ve landmark yapısı
- Erişilemeyen kontroller

Otomatik doğrulanamayan kontrolleri manuel denetim olarak sınıflandır.

Sonuç sınıfları:

1. İhlal
2. Manuel kontrol gerekli
3. Kalite/SEO

Bunları birbirine karıştırma.

### Tarama işleyicisi

- CLI üzerinden çalışabilsin.
- Kuyruk üzerinden çalışabilsin.
- CI/CD içinde çalışabilsin.
- İş kilidi ve heartbeat kullansın.
- İptal ve yeniden deneme desteklesin.
- Uzun süredir heartbeat vermeyen işi başarısız olarak işaretlesin.
- Sayfa/adres sınırlarına uysun.
- Sonuçları veritabanına kaydetsin.

Rapor formatları:

- `report.json`
- `issues.csv`
- `pages.csv`
- `report.html`

Tarama raporlarını varsayılan olarak Git deposu dışında tut.

---

## 12. CI/CD ve Bildirimler

Mevcut CI/CD platformuna entegre et.

Tetikleyiciler:

- Pull Request
- Ana dala push
- Günlük zamanlanmış denetim
- Manuel tetikleme
- Deployment sonrası kontrol

**CI kapısı:**

Yeni kritik/ciddi erişilebilirlik regresyonu tespit edildiğinde yapılandırmaya bağlı olarak pipeline başarısız olsun.

Baseline sistemi oluştur:

- Bilinen sorun kimliği
- Gerekçe
- Yeniden değerlendirme tarihi
- Süre aşımı kontrolü

Baseline içindeki sorunlar raporlardan gizlenmesin.

Bildirimler:

- Yeni kritik/ciddi sorunlar
- Yeniden açılan sorunlar
- İsteğe bağlı haftalık özet

Aynı taramada oluşan sorunları mümkünse tek e-postada birleştir.

Tekilleştirme uygula ve saatte en fazla 2, günde en fazla 3 e-posta sınırı kullan.

Mevcut e-posta sağlayıcısını kullan; özellikle Mailgun veya başka bir sağlayıcıyı zorunlu tutma.

E-posta servisi yapılandırılmamışsa tarama başarısız olmasın; bildirim atlandı olarak kaydedilsin.

---

## 13. CMS Yayın Öncesi Erişilebilirlik Kontrolleri

Mevcut içerik yönetim sistemine yayın öncesi kontrol entegre et.

Kontrol listesi:

- Anlamlı görselde ALT eksikliği
- Boş bağlantı metni
- Başlık seviyesi atlama
- İçerik gövdesinde fazladan H1
- Boş başlıklar
- Belirsiz bağlantı metni
- URL'den oluşan bağlantı metni
- Başlık hücresiz tablolar
- Sahte liste kullanımı
- Uzun tamamı büyük harf metinler
- Yanlış veya eksik dil işaretlemeleri
- Dekoratif görsel/ALT çelişkisi
- Video, altyazı ve transkript kontrolü

İçerik düzenleyicisinde yaklaşık 900 ms debounce ile uyarıları göster.

Yayın kuralları:

- `warnBeforePublish`: varsayılan açık
- `blockOnCritical`: varsayılan kapalı

Kritik hata engeli yalnız sunucu tarafında gerçek yayın işleminde uygulanmalı.

**Taslak kaydetme hiçbir zaman engellenmemeli.**

Mevcut yayımlanmış içerikte yeni kritik hata olup olmadığı önceki yayımlanmış sürümle karşılaştırılabilsin.

Kontrol servisi yapılandırılmamışsa sistem güvenli biçimde uyarı moduna düşsün; CMS çalışmaya devam etsin.

### Medya kütüphanesi

Her görsel için:

- ALT metni
- Dekoratif görsel işareti
- ALT gözden geçirildi işareti

oluştur.

Dekoratif görsel ALT doluysa temizleme öner; otomatik silme.

Anlamlı görselde ALT yoksa eksik olarak işaretle.

İlgili işaretleri gerekiyorsa ayrı veri tablosunda sakla.

---

## 14. Veri Modeli

Mevcut veritabanı/ORM ile aşağıdaki 13 mantıksal tabloyu oluştur.

| Tablo | Sorumluluk |
|---|---|
| `a11y_settings` | Asistan, tarama, CMS ve sürüm ayarları |
| `a11y_change_log` | Yönetim değişiklik geçmişi |
| `a11y_scan_jobs` | Tarama işleri, durum, kilit, ilerleme |
| `a11y_scan_pages` | Sayfa/varyant/durum sonuçları |
| `a11y_issues` | Kararlı kimlikli sorunlar |
| `a11y_issue_occurrences` | Sorunların görüldüğü konumlar |
| `a11y_issue_events` | Durum değişimleri, notlar, kanıtlar |
| `a11y_manual_audits` | Manuel denetim sonuçları |
| `a11y_documents` | PDF/DOCX envanteri |
| `a11y_media_reviews` | ALT/dekoratif incelemeler |
| `a11y_content_reviews` | CMS içerik incelemeleri |
| `a11y_feedback` | Ziyaretçi sorun bildirimleri |
| `a11y_notifications` | Bildirim geçmişi ve tekilleştirme |

Tablolarda gerektiği yerde:

- UUID/kimlik
- Zaman damgaları
- Durum
- Sürüm
- Yetkili kullanıcı
- Denetim geçmişi
- Gerekçe ve kanıt
- İndeksler
- İlişkisel bütünlük

uygula.

Migration'ları geri alınabilir ve mevcut şemaya zarar vermeyecek biçimde tasarla.

Eksik tablo veya migration durumunda modül uygun kurulum uyarısı versin.

---

## 15. Güvenlik ve KVKK

### Yetkilendirme

- Yönetim işlemlerinde sunucu taraflı oturum doğrulaması.
- Her API/Server Action için rol ve izin kontrolü.
- İstemciden gelen rol/kimlik bilgilerine güvenmeme.
- IDOR önleme.
- Parametrik sorgular.
- Sıkı veri doğrulama.
- Güvenli eşzamanlı güncelleme.

### SSRF güvenliği

Tarama motoru keyfî adresleri taramasın.

- İzinli domain/kök listesi
- Özel IP ve localhost erişim kısıtları
- Geliştirme ortamı için açıkça tanımlanmış istisnalar
- Zararlı URL şemalarını engelleme
- Kimlik bilgisi içeren URL'leri reddetme
- Redirect hedeflerini doğrulama
- Tarayıcı navigasyonunu izinli origin'lerle sınırlandırma

### Veri güvenliği

- Tarama raporlarında form değerleri ve gizli alanları maskele.
- Token, e-posta, telefon ve hassas sorgu parametrelerini temizle.
- HTML örneklerini metin olarak göster; çalıştırma.
- Raporları yetkili erişime kapat.
- `Cache-Control: private, no-store` kullan.
- Ziyaretçi bildirimlerinde honeypot, hız sınırı ve spam kontrolü uygula.
- Mümkün olan yerde IP yerine geri döndürülemez kısa süreli kontrol anahtarı kullan; ham IP saklama.
- İlgisiz kişisel veri toplama.

**Saklama politikası:**

- Tarama sayfaları ve geçiş kayıtları: varsayılan 180 gün
- Ziyaretçi bildirimleri: 365 gün
- Bildirim kayıtları: 365 gün
- Temizlik işlemi varsayılan dry-run
- Gerçek silme yalnız açık uygulama komutuyla

---

## 16. Kaynak Kod Erişilebilirliği

Erişilebilirlik widget'ının kapalı olduğu durumda da site mümkün olduğunca erişilebilir olmalıdır.

Mevcut bileşenleri denetle ve şu sorunları kaynak kod seviyesinde düzelt:

- Yetersiz kontrast
- Klavye odağının görünmemesi
- Yapışkan header/çerez paneli altında kalan odak
- 320 CSS px yatay taşma
- %200 metin büyütmede içerik kaybı
- Metin aralığı değişikliklerinde taşma
- Sabit yükseklikli kontrollerin kırpılması
- Eksik label
- Hatalı ARIA
- Geçersiz iç içe etkileşimli öğeler
- Klavye ile erişilemeyen işlevler
- Erişilebilir olmayan hata mesajları
- Eksik semantik bölgeler

Mevcut görsel tasarımı varsayılan durumda koru.

Widget, kaynak kod sorunlarının üzerini örten bir çözüm olarak kullanılmamalıdır.

---

## 17. Test Stratejisi

### Birim testleri

- Ayar ve profil birleşim mantığı
- 28 hızlı ayar adımları
- Geri alma/sıfırlama
- Yerel komut çözücü
- Depolama ve sürüm geçişi
- Terim sözlüğü
- CMS içerik kuralları
- Sorun kimliği üretimi
- CI baseline
- Bildirim tekilleştirme
- Veri erişimi ve yetki kontrolleri

### Entegrasyon testleri

- Ziyaretçi paneli ve footer
- Admin ayarlarının ziyaretçi paneline yansıması
- Profil ile manuel ayar önceliği
- Tarama kuyruğu ve runner
- Tarama sonucu ve sorun kaydı
- CMS yayın kontrolü
- Medya/ALT yönetimi
- Belge envanteri
- Rapor dışa aktarma
- Bildirim gönderimi
- Migration eksikliği durumları

### E2E ve erişilebilirlik testleri

- Masaüstü ve mobil
- Chromium, Firefox, WebKit
- Klavyeyle tam kullanım
- Tab/Shift+Tab
- Esc ve odak iadesi
- Ekran okuyucu denemeleri
- %200 metin
- 320 px yeniden akış
- Yüksek kontrast
- Koyu tema
- Görsel filtreler
- Sade okuma
- Metin büyüteci
- Kullanıcı tercihleri ve sayfa geçişleri
- Türkçe/İngilizce panel
- Dinamik içerik ve formlar

Gerçek cihazlarda VoiceOver, NVDA, JAWS ve TalkBack testlerini mümkün olduğunda yap; yapılamayanları **test edilmedi** olarak raporla.

Otomatik testlerin sıfır ihlal üretmesini eksiksiz WCAG uyumu veya sertifikasyon olarak sunma.

---

## 18. Kullanıcı Arayüzü ve Deneyim Kuralları

- Mevcut projenin UI/UX tasarım sistemi kullanılsın.
- Referans görsel veya üçüncü taraf widget kopyalanmasın.
- Erişilebilirlik modülü kendi içinde de erişilebilir olsun.
- Semantik HTML öncelikli olsun.
- ARIA yalnız gerekli yerde kullanılsın.
- Kontrollerin durumları yalnız renkle anlatılmasın.
- `prefers-reduced-motion` desteklensin.
- Bilgilendirme, hata ve başarı mesajları erişilebilir olsun.
- Dokunmatik kontroller yeterli etkileşim alanına sahip olsun.
- Küçük ekranlarda metin kırpılmasın.
- Yönetim ekranlarında tablo, filtre ve formlar klavyeyle kullanılabilsin.
- Sürükle-bırak işlemleri için klavye alternatifi bulunsun.
- Kullanıcının tarayıcı yakınlaştırması ve ekran okuyucu kısayolları engellenmesin.

Erişilebilirlik tercihlerinin sağlık veya tıbbi güvenlik yararı garanti ettiği yönünde açıklama kullanma.

---

## 19. Geliştirme Aşamaları

İşlemleri aşağıdaki sırayla yürüt:

**Faz 1 — Analiz**
- Proje mimarisini incele.
- Kullanılabilecek mevcut altyapıları belirle.
- Gereksinim matrisi oluştur.
- Modülün entegrasyon noktalarını tespit et.

**Faz 2 — Temel Mimari**
- Modül klasör yapısını oluştur.
- Durum yönetimini geliştir.
- Ayar ve profil veri yapılarını oluştur.
- Migration'ları hazırla.
- API ve yetki modelini oluştur.

**Faz 3 — Ziyaretçi Asistanı**
- Başlatıcı ve panel
- 28 hızlı ayar
- 9 profil
- Ayrıntılı kontroller
- Okuma/gezinme
- Sesli ve yazılı komut
- Saklama ve tercih senkronizasyonu

**Faz 4 — Yönetim Merkezi**
- 11 yönetim ekranı
- Yönetim ayarları
- Sorun yaşam döngüsü
- Manuel denetimler
- Ziyaretçi bildirimleri
- Raporlama

**Faz 5 — Denetim Motoru**
- Playwright/axe-core
- CLI ve runner
- Kuyruk ve veritabanı kayıtları
- Varyant ve etkileşim testleri
- CI gate ve bildirimler

**Faz 6 — CMS Entegrasyonu**
- İçerik kontrolleri
- Yayın öncesi uyarı/engel
- Medya ALT kontrolleri
- Belge envanteri

**Faz 7 — Doğrulama**
- Birim ve entegrasyon testleri
- E2E testleri
- Güvenlik kontrolleri
- Performans ölçümü
- Manuel erişilebilirlik denetimi
- Regresyon düzeltmeleri

Her faz sonunda uygulanan özellikleri doğrula. Bir sonraki faza geçerken çalışan özellikleri bozma.

---

## 20. Tamamlanma ve Kabul Kriterleri

Modül aşağıdaki koşullar sağlandığında tamamlanmış kabul edilebilir:

1. 28 hızlı ayar gerçek işlevleriyle çalışıyor.
2. 9 erişilebilirlik profili ve birleşim kuralları çalışıyor.
3. Ziyaretçi paneli mobil/masaüstü ve klavyeyle kullanılabiliyor.
4. Sesli okuma, yazılı komut ve desteklenen ortamlarda sesli komut çalışıyor.
5. Panel tercihleri güvenli biçimde kalıcı hale geliyor.
6. 11 yönetim bölümü gerçek veri ve işlemlerle çalışıyor.
7. Playwright + axe-core tarama motoru ve kuyruk sistemi çalışıyor.
8. Tarama bulgularının durum ve geçmiş yönetimi çalışıyor.
9. CMS yayın kontrolleri, medya ve belge incelemeleri çalışıyor.
10. JSON/CSV/HTML raporları üretiliyor.
11. CI regresyon kapısı ve yapılandırılmış bildirim mekanizması çalışıyor.
12. 13 tabloluk veri modeli mevcut mimariye entegre edilmiş.
13. Yetkilendirme, SSRF, gizlilik ve veri maskeleme testleri uygulanmış.
14. Mevcut site fonksiyonları ve tasarım sistemi korunmuş.
15. Widget kapalıyken de tespit edilen temel kaynak kod erişilebilirlik sorunları düzeltilmiş.
16. Otomatik test sınırları ve manuel değerlendirme ihtiyaçları raporlanmış.

**Göstermelik veya işlevsiz hiçbir kontrol oluşturma.** Bir işlev teknik olarak gerçekleştirilemiyorsa nedenini, kısıtını ve uygulanabilir alternatifini belirt; tamamlandı olarak işaretleme.

### Nihai teslimat

Geliştirme sonunda aşağıdaki çıktıları sun:

- Modül mimarisi ve klasör yapısı
- Tamamlanan özellik matrisi
- Veritabanı migration'ları
- API ve entegrasyon açıklamaları
- Yönetim rolleri ve izinleri
- Tarama/CI çalıştırma talimatları
- Test sonuçları ve kapsamı
- Bilinen kısıtlar
- Açık kalan işler
- Başka bir projeye entegrasyon yönergesi

**Son talimat:** Bu teknik şartnamedeki özellikleri mevcut projenin mimarisine uyarlayarak gerçek, test edilebilir, modüler ve üretime hazır biçimde geliştir. Onaylanmış mevcut bileşenleri kaldırma veya ilgisiz alanları değiştirme. Uygulanmamış bir özelliği tamamlanmış olarak raporlama.
