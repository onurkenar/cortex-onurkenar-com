KVKK, GDPR, Yasal Belgeler ve Çerez Yönetim Sistemi — Geliştirme Promptu
Mevcut web uygulamasına kapsamlı bir KVKK / GDPR / Yasal Belgeler / Cookie Consent Management Platform (CMP) modülü geliştir.
Sistem yalnızca çerez banner'ı göstermemeli; web sitesini analiz ederek çerezleri, takip teknolojilerini, kişisel veri işleme noktalarını ve yasal belge ihtiyaçlarını tespit etmeli, gerekli belgeleri taslak olarak oluşturmalı, izinleri ve veri aktarımını kontrol etmeli, tüm süreçleri CMS üzerinden yönetmelidir.
Temel ilkeler:
* Mevcut mimari, UI/UX, tasarım sistemi, yetkilendirme altyapısı ve onaylı özellikler korunsun.
* Gerçek veritabanı, API, CMS, tarama motoru ve ziyaretçi arayüzü geliştirilsin.
* Privacy by Design, Privacy by Default, KVKK, uygulanabilir GDPR hükümleri ve WCAG 2.2 AA esas alınsın.
* Geçerli açık rıza olmadan rızaya bağlı veri işleme ve üçüncü taraf veri aktarımı gerçekleşmesin.
* Sahte tarama, uydurma çerez, hayali hukuki bilgi veya çalışmayan otomasyon oluşturulmasın.
* Otomatik içerik oluşturma ile hukuki onay/yayınlama birbirinden ayrı yönetilsin.

1. CMS — Ayarlar → Yasal (KVKK)
Tüm sistemi aşağıdaki alt modüllerle tek bir yönetim alanında oluştur:
1. Genel Bakış
2. Yasal Belgeler
3. Yasal Uygunluk Taraması
4. Eksik Belge Önerileri
5. Veri Sorumlusu / Şirket Bilgileri
6. Çerez Yönetimi
7. Çerez Kategorileri
8. Çerez Envanteri
9. Servisler / Sağlayıcılar
10. Script / Tracker Yönetimi
11. Çerez Tarama Sonuçları
12. Ziyaretçi Tercihleri ve Rıza Kayıtları
13. Banner ve Tercih Merkezi
14. Consent Mode ve Entegrasyonlar
15. Bölgesel Kurallar
16. Veri Sahibi Başvuruları
17. Raporlama ve Analitik
18. Yayınlama ve Versiyonlar
19. Audit Log
20. Ayarlar
Mevcut CMS tasarım sistemini ve RBAC yapısını kullan.

2. Yasal Belge Yönetimi
KVKK Aydınlatma Metni, Gizlilik Politikası, Çerez Politikası, Kullanım Koşulları, Üyelik ve İşletme Üyelik Sözleşmeleri, Açık Rıza, Ticari Elektronik İleti, Veri Sahibi Başvuru Metni, Mesafeli Satış Sözleşmesi, Ön Bilgilendirme Formu, Topluluk Kuralları, İçerik/Yorum Politikası ve diğer özel belge türlerini destekle.
Her belgede:
* Başlık, slug, tür, açıklama ve WYSIWYG içerik
* Belge versiyonu, durumu ve geçerlilik tarihleri
* Oluşturan, düzenleyen, inceleyen ve onaylayan
* SEO title, description, index/noindex
* İlgili mevzuat ve resmi kaynak referansları
* İlgili sayfa, form ve kullanıcı işlemleri
* Değişiklik geçmişi, karşılaştırma ve geri alma
bulunsun.
Belge iş akışı: Taslak → İncelemede → Onaylandı → Yayında → Arşivlendi.
Eski versiyonları silme. Onaylı geçmiş belge içeriklerini sonradan değiştirilemez şekilde sakla.
Public sayfalar:
* /yasal
* /yasal/[slug]
Yalnızca yayındaki belgeleri göster; mevcut tasarım sistemi, SEO ve erişilebilirlik standartlarına uy.

3. Otomatik Web Sitesi Yasal Uygunluk Taraması — YENİ
CMS'ye Web Sitesini Tara / Yasal Belgeleri Analiz Et özelliği ekle.
Sistem web sitesini ve uygulama yapısını analiz ederek hangi yasal belgelerin gerektiğini belirlemeye yardımcı olsun.
3.1. Tarama kapsamı
Erişim yetkisi bulunan public ve authenticated sayfaları, route'ları, formları, API veri akışlarını, scriptleri ve servis entegrasyonlarını incele.
Özellikle:
* Üyelik, giriş, profil ve hesap yönetimi
* Kullanıcı veya işletme kayıtları
* İletişim, başvuru, teklif ve talep formları
* Newsletter, e-posta ve SMS izinleri
* Ödeme, abonelik, satış ve sipariş akışları
* Ürün, hizmet ve e-ticaret sayfaları
* Kullanıcı yorumları ve içerik paylaşımı
* Dosya ve görsel yükleme
* Konum, kamera, mikrofon veya bildirim izinleri
* Yapay zekâ ve üçüncü taraf API entegrasyonları
* Analitik, reklam, davranış analizi ve takip servisleri
* Kişisel veri toplama, saklama, işleme ve aktarım süreçleri
* Mevcut yasal belgeler, bağlantılar ve onay kutuları
* Footer, üyelik ekranları ve diğer yasal bilgilendirme alanları
taransın.
Yalnızca HTML metnine güvenme; mümkünse uygulama kodu, API sözleşmeleri, konfigürasyon ve gerçek veri akışlarını da incele. Yetkisiz veya erişilemeyen alanları ayrıca raporla.
3.2. Eksik yasal belgeleri tespit et
Sistemde bulunan belgeleri, taramada belirlenen ihtiyaçlarla karşılaştır.
Örneğin:

| Tespit | Önerilen belge |
|---|---|
| Kişisel veri toplama | KVKK Aydınlatma Metni |
| İsteğe bağlı çerez/tracker | Çerez Politikası ve tercih mekanizması |
| Kullanıcı üyeliği | Üyelik Sözleşmesi |
| İşletme üyeliği | İşletme Üyelik Sözleşmesi |
| Pazarlama iletişimi | Ticari Elektronik İleti İzni |
| Online satış | Mesafeli Satış Sözleşmesi / Ön Bilgilendirme |
| Kullanıcı yorumları | İçerik ve Yorum Politikası |
| Veri sahibi başvurusu | Veri Sahibi Başvuru Metni |

Bunlar örnek eşleştirmelerdir. Gerçek gerekliliği faaliyet, veri işleme amacı, hukuki dayanak ve uygulanabilir mevzuata göre değerlendir.
3.3. Eksik belge taslaklarını otomatik oluştur
Eksik belge tespit edildiğinde:
1. İlgili sayfa, form, veri işleme faaliyeti ve kanıtları belirle.
2. Belge gerekliliğini değerlendir.
3. İlgili resmi mevzuat ve kurum kaynaklarını incele.
4. Mevcut şirket/veri sorumlusu bilgilerini kullan.
5. Eksik bilgileri placeholder olarak bırak.
6. Belgeyi mevcut CMS formatında taslak oluştur.
7. Kaynakları, hukuki dayanakları, tarama tarihini ve inceleme notlarını kaydet.
8. Yasal Belgeler → Taslaklar bölümüne ekle.
9. Yetkili yöneticiye inceleme ve onay bildirimi oluştur.
Hiçbir belge otomatik olarak yayınlanmasın.
3.4. Yasal uygunluk raporu
Tarama sonunda:
* Mevcut belgeler
* Eksik belgeler
* Güncellenmesi önerilen belgeler
* Eksik aydınlatma veya izin noktaları
* Olası uygunsuz çerez/tracker kullanımları
* Hukuki inceleme gerektiren alanlar
* Resmi kaynak referansları
* Öncelik/risk seviyeleri
* Önerilen düzeltmeler
gösterilsin.
Risk seviyeleri otomatik kesin hukuki hüküm olarak sunulmasın; bulguların doğrulama ve inceleme durumu açıkça belirtilsin.

4. Otomatik Çerez Tarama ve Envanter — GELİŞTİRİLDİ
Web sitesindeki çerezler, depolama teknolojileri, üçüncü taraf scriptler ve izleme çağrıları gerçek tarayıcı tabanlı taramayla tespit edilsin.
Tarama aşağıdaki senaryolarda yapılsın:
* İlk ziyaret / rıza yok
* Tümünü Reddet
* Tümünü Kabul Et
* Kategori bazlı kısmi izinler
* Oturum açmış / anonim kullanıcı (güvenli test ortamında)
* Farklı sayfalar, cihaz boyutları ve gerekli kullanıcı etkileşimleri
Çerez adı, sağlayıcı, domain, path, amaç, kategori, süre, session/persistent, first/third-party, bağlı servis, ilk/son tespit ve rıza gereksinimi kaydedilsin.
Cookies, localStorage, sessionStorage, IndexedDB, tracking pixel, script ve mümkün olan diğer izleme teknolojilerini envantere dahil et.
Tarama sonuçlarını sınıflandır, değişiklikleri önceki taramayla karşılaştır ve bilinmeyen tracker'ları işaretle.
Tarama gerçek verilerden oluşmalı; doğrulanamayan bilgi otomatik kesinleştirilmemeli.

5. Çerez Envanterini Yasal Metne Otomatik Ekleme — YENİ
Sistemin temel özelliklerinden biri, taranan çerezlerin Çerez Politikası belgesine otomatik tablo halinde aktarılmasıdır.
5.1. Dinamik çerez tablosu
Onaylı çerez envanterini kaynak alarak Çerez Politikası içinde aşağıdaki yapıda tablo oluştur:

| Çerez Adı | Sağlayıcı | Amaç | Kategori | Süre | Tür |
|---|---|---|---|---|---|
| Tespit edilen değer | Tespit edilen değer | Doğrulanmış açıklama | Kategori | Süre | 1./3. taraf |

Tabloyu Zorunlu, İşlevsel, Analitik ve Pazarlama kategorilerine göre grupla.
Gerekli durumlarda domain, veri aktarımı ve servis gizlilik politikası bilgilerini de göster.
Tablo gerçek tarama sonuçlarına ve yönetici tarafından onaylanmış envantere dayanmalı. Örnek/hayali çerezler production belgesine eklenmemeli.
5.2. Otomatik senkronizasyon
Her yeni taramada mevcut envanterle karşılaştır:
* Yeni çerez
* Silinen/kaybolan çerez
* Süresi değişen çerez
* Sağlayıcısı veya domaini değişen çerez
* Kategorisi değişen çerez
* Yeni üçüncü taraf servis
* Bilinmeyen/izin öncesi çalışan tracker
Değişiklik varsa Çerez Politikası için otomatik yeni taslak versiyon oluştur veya mevcut taslağı güncelle.
Yayındaki onaylı belgeyi otomatik değiştirme.
İş akışı:
Siteyi Tara → Envanteri Güncelleme Önerisi → İncele/Sınıflandır → Onaylı Envanter → Politika Taslağını Güncelle → Hukuki İnceleme → Yayınla
İlgili metin güncellendiğinde onaylı yeni sürüm ve yürürlük tarihi kaydedilsin. Önceki politika versiyonu korunsun.
5.3. Çerez Politikası bileşeni
Yasal belge editörüne Dinamik Çerez Tablosu bileşeni ekle.
Bileşen:
* Onaylı envanterden otomatik veri alsın.
* Kategori bazlı tablo oluştursun.
* Responsive ve erişilebilir olsun.
* Kaynak tarama, envanter ve belge versiyonlarıyla ilişkilendirilsin.
* Yayındaki sürüm için onaylı veri anlık görüntüsünü korusun.
* Envanter değişikliklerinde güncelleme uyarısı üretsin.
Aynı bileşeni tercih merkezi içindeki çerez detayları için de kullan.

6. Çerez Banner'ı ve Sürekli Sol Alt İkon
İlk ziyarette üç eşit öncelikli buton göster:
* Tümünü Kabul Et
* Tümünü Reddet
* Tercihleri Yönet
Butonlar aynı yükseklik, renk, padding, font, radius, kontrast, erişilebilirlik ve görsel ağırlığa sahip olsun. Manipülatif tasarım kullanılmasın.
Web sitesinin sol alt köşesinde, bütün sayfalarda sürekli erişilebilir bir çerez ikonu yer alsın.
İkon tercih merkezini açsın; kullanıcı önceki rızasını görüntüleyebilsin, değiştirebilsin veya geri çekebilsin.
Varsayılan konum sol alt olsun. Boyut, görünüm ve konum CMS'den yönetilebilsin. Mobil navigasyon/CTA alanlarını engellemesin.

7. Rıza Yönetimi — Default Deny
Kullanıcının geçerli rızası olmadan rıza gerektiren hiçbir çerez, tracker, profil oluşturma, analitik veya reklam işlemi çalışmasın.
Varsayılan durum:
```js
{
  necessary: true,
  functional: false,
  analytics: false,
  marketing: false
}
```
* GA4, Google Ads, Meta Pixel/CAPI, TikTok Pixel, Hotjar, Clarity ve benzeri servisler ilgili rıza olmadan başlatılmasın.
* Üçüncü taraf script, iframe, pixel, SDK ve ağ çağrıları gerekli rıza öncesi engellensin.
* İstemci ve sunucu tarafında aynı consent politikası uygulansın.
* Consent Mode v2 denied başlangıç durumu kullansın; sadece sinyal göndermekle yetinilmesin, ilgili etiketler de engellensin.
* Kısmi izinlerde yalnızca izin verilen servisler çalışsın.
* Rıza geri çekildiğinde sonraki veri aktarımı durdurulsun; teknik olarak mümkün olan tanımlayıcılar temizlensin.
* Temel güvenlik, oturum ve hizmet sunumu için gerekli, uygun hukuki dayanağa sahip işlemler ayrı yönetilsin ve pazarlama amacıyla kullanılmasın.
* Çerez tercihleri hiçbir zaman ticari elektronik ileti izni yerine geçmesin.

8. Tercih Merkezi ve Servis Modeli
Zorunlu, İşlevsel, Analitik ve Pazarlama kategorilerini dinamik yönet.
Kategori → Servis/Sağlayıcı → Çerez → Amaç/Süre/Domain/Politika seviyesinde detay göster.
Her servisin amacı, veri aktarımı, hukuki dayanağı, izin gereksinimi ve script bağımlılıklarını tanımla.
Rıza gerektiren üçüncü taraf embedded içerikleri izin öncesi placeholder ile değiştir.

9. Yasal Metinlerde Resmi Kaynak Doğrulaması — GELİŞTİRİLDİ
Yasal belge oluşturma ve güncelleme motoru resmi kurum ve mevzuat kaynaklarını öncelikli referans olarak kullansın.
Türkiye resmi kaynakları
1. KVKK — https://www.kvkk.gov.tr/
2. KVKK Çerez Uygulamaları Hakkında Rehber — https://www.kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber
3. KVKK Rehberler — https://www.kvkk.gov.tr/Icerik/2030/rehberler
4. KVKK Aydınlatma Yükümlülüğü — https://www.kvkk.gov.tr/Icerik/2033/Aydinlatma-Yukumlulugu-
5. KVKK Aydınlatma Yükümlülüğü Rehberi — https://www.kvkk.gov.tr/Icerik/5395/Aydinlatma-Yukumlulugunun-Yerine-Getirilmesi-Rehberi-Kurum-Internet-Sayfasinda-Yayinlanmistir-
6. Resmî Gazete — https://www.resmigazete.gov.tr/
7. Mevzuat Bilgi Sistemi — https://www.mevzuat.gov.tr/
8. Ticaret Bakanlığı — https://ticaret.gov.tr/
9. ETBİS — https://etbis.ticaret.gov.tr/
10. BTK — https://www.btk.gov.tr/
11. İleti Yönetim Sistemi — https://iys.org.tr/
12. Türk Patent ve Marka Kurumu — https://www.turkpatent.gov.tr/
13. Türkiye İnsan Hakları ve Eşitlik Kurumu — https://www.tihek.gov.tr/
Uluslararası resmi kaynaklar
1. EDPB — https://www.edpb.europa.eu/
2. EUR-Lex — https://eur-lex.europa.eu/
3. European Commission Data Protection — https://commission.europa.eu/law/law-topic/data-protection_en
4. ICO — https://ico.org.uk/
5. CNIL — https://www.cnil.fr/en
6. AEPD — https://www.aepd.es/
7. CPPA — https://cppa.ca.gov/
Kaynak kullanım kuralları
* Güncel ve yürürlükteki mevzuat esas alınsın.
* Önce uygulanabilir ülke/bölge ve faaliyet kapsamı belirlensin.
* Türkiye merkezli faaliyetler için ilgili Türk mevzuatı önceliklendirilsin; diğer düzenlemeler yalnızca uygulanabildiği ölçüde kullanılsın.
* Her yasal belge taslağında ilgili resmi kaynak bağlantıları ve kontrol tarihleri tutulsun.
* Kaynak erişilemezse veya doğrulanamazsa durum raporlansın.
* Resmi mevzuat ve rehber ile ürün/UX referansı birbirinden ayrı tutulsun.
* Mevzuat değişikliği taraması yapılabilsin; değişiklik tespitinde etkilenen belgeler için güncelleme önerisi oluşturulsun.
* Kaynaktaki değişikliğin gerçekten uygulanabilir olduğu doğrulanmadan otomatik hukuki hüküm verilmesin.
* AI tarafından üretilen hukuki metinler taslak niteliğinde olsun; yetkili hukuk incelemesi olmadan otomatik yayına alınmasın.

10. Merkezi Şirket Bilgileri ve Form İzinleri
Şirket unvanı, adres, iletişim, MERSİS, KEP ve diğer gerekli bilgileri merkezi yapılandırmadan al.
Belgelerde güvenli değişkenler kullan; eksik verileri uydurma.
Formlarda aydınlatma, açık rıza, sözleşme kabulü ve ticari ileti izinlerini ayrı yönet. Her kabulü belge ID/versiyonuyla ilişkilendir.

11. Rıza Kayıtları, Denetim ve Versiyonlama
Her rıza aksiyonunda kategori/servis tercihleri, zaman, ilgili politika versiyonu ve işlem türü kaydedilsin.
Gereksiz kişisel veri ve açık IP saklama.
Rıza geçmişini overwrite etme. Eski belge ve consent versiyonlarını koru.
Önemli politika değişikliklerinde yeniden rıza değerlendirmesi yap.
Yönetici işlemleri audit log ile izlensin.

12. Bölgesel Kurallar ve Veri Sahibi Başvuruları
Türkiye/KVKK, AB/AEA/GDPR, Birleşik Krallık ve gerektiğinde diğer bölgeler için yapılandırılabilir policy engine kullan.
Veri sahibi başvurularında güvenli başvuru, kimlik doğrulama, durum yönetimi, sorumlu atama, yasal süre takibi ve sonuçlandırma iş akışları oluştur.

13. Dashboard ve Bildirimler
Genel Bakış ekranında:
* Son site/çerez taraması
* Tespit edilen çerez ve servis sayıları
* Yeni/bilinmeyen tracker'lar
* Rıza öncesi veri aktarımı bulguları
* Eksik yasal belgeler
* Otomatik oluşturulan belge taslakları
* Güncellenmesi gereken belgeler
* Çerez Politikası ile envanter tutarlılığı
* Hukuki inceleme bekleyen belgeler
* Kabul/ret/özel tercih oranları
* Yayın ve audit geçmişi
göster.
Yeni çerez, eksik belge, kaynak değişikliği veya önemli risk tespit edildiğinde CMS içinde uyarı oluştur.

14. Güvenlik ve Merkezi API
Data minimization, least privilege, RBAC, server-side validation, CSRF/XSS koruması, log bütünlüğü ve güvenli cookie özelliklerini uygula.
Mevcut veritabanı ve servis mimarisini kullanarak belge, versiyon, rıza, çerez, servis, tarama, hukuki analiz, kaynak referansı ve audit kayıtlarını modelle.
Uygulama genelinde merkezi consent API kullan:
getConsentState()
hasConsent(categoryOrService)
updateConsent(preferences)
withdrawConsent()
subscribeToConsentChanges(callback)
İstemci tarafı rıza durumu tek başına sunucu tarafı doğrulamanın yerine geçmesin.

15. Dil Yönetimi ve Çok Dilli İçerikler — YENİ
CMS üzerinden Dil Yönetimi ve Çeviriler özelliği ekle.
* Varsayılan dil Türkçe (tr-TR) olsun; İngilizce (en) ve diğer diller CMS üzerinden eklenebilsin, etkinleştirilebilsin veya pasifleştirilebilsin.
* Mevcut projenin dil/i18n altyapısı varsa onu kullan; ikinci bir dil yönetim sistemi oluşturma.
* Ziyaretçinin seçtiği dil öncelikli olsun. Desteklenmeyen dilde varsayılan dile dönüş sağlansın.
* Çerez banner'ı, sol alt çerez ikonu, tercih merkezi, butonlar, çerez kategorileri, servis açıklamaları, çerez tabloları ve yasal belgeler aktif dillerde görüntülenebilsin.
* Her yasal belge için dil bazlı başlık, içerik, slug, SEO metadata, versiyon ve yayın durumu yönetilsin.
* Belgelerin çevirileri ana belgeye bağlı olsun; her dil için ayrı taslak, inceleme, onay ve yayın süreci bulunsun.
* Mevcut belge güncellendiğinde diğer dil versiyonlarında Çeviri Güncellemesi Gerekiyor uyarısı oluşsun.
* Eksik çeviriler otomatik taslak olarak oluşturulabilsin; hukuki inceleme ve yetkili onayı olmadan yayınlanmasın.
* Otomatik çerez tablosunun sütun başlıkları, kategori adları ve amaç açıklamaları seçilen dilde gösterilsin. Teknik çerez adları, domainler ve süre değerleri değiştirilmesin.
* Genel site taramasıyla oluşturulan eksik yasal belge taslakları, aktif diller için çeviri taslaklarıyla ilişkilendirilebilsin.
* Public yasal sayfalarda dil seçimi, dil bazlı URL, hreflang, canonical ve SEO metadata mevcut routing mimarisine uygun yönetilsin.
* Çeviri durumları Eksik → Taslak → İncelemede → Onaylandı → Yayında → Güncelleme Gerekli olarak takip edilsin.
* Ziyaretçi dil değiştirdiğinde mevcut çerez izinleri silinmesin veya değiştirilmesin.
* Dil seçimi ile uygulanacak hukuki bölge birbirinden bağımsız olsun. İngilizce görüntüleme otomatik olarak GDPR uygulanacağı anlamına gelmesin.
* Her aktif dil için banner, tercih merkezi, yasal belgeler, çerez tabloları, form izinleri, SEO ve WCAG erişilebilirlik testleri yapılsın.

16. Önceliklendirilmiş Geliştirme Fazları ve Bağımlılıklar
Geliştirmeyi güvenlik, teknik bağımlılıklar ve işlevsel önceliğe göre yürüt. P0 = Kritik, P1 = Yüksek, P2 = Gelişmiş. Bağımlılıkları tamamlanmayan fazlara geçme. Bağımsız işleri mümkünse paralel geliştir.
Faz 00 — Mevcut Sistem Analizi [P0]
Bağımlılık: Yok.
Repository, framework, routing, veritabanı, ORM, CMS, RBAC, i18n, analytics, tracker'lar, formlar, mevcut yasal belgeler ve veri akışlarını incele.
Çıktı: Mimari analiz, risk haritası, mevcut/eksik özellikler, teknik geliştirme planı.
Faz 01 — Temel Altyapı ve Veri Modeli [P0]
Bağımlılık: Faz 00.
Belge, versiyon, consent, kategori, servis, çerez, tarama, audit ve dil yönetimi veri modellerini oluştur. Mevcut RBAC ve güvenlik altyapısıyla bütünleştir. Merkezi yapılandırma, versiyonlama ve güvenli migration mekanizmalarını hazırla.
Çıktı: Veritabanı, temel API'ler, RBAC, migration ve ortak servis altyapısı.
Faz 02 — Consent Engine ve Default Deny [P0]
Bağımlılık: Faz 01.
Merkezi rıza motorunu oluştur. Zorunlu olmayan tüm kategoriler varsayılan kapalı olsun. İstemci ve sunucu tarafında rıza kontrolü, tercih kaydetme, geri çekme ve merkezi consent API işlevlerini geliştir.
Çıktı: Test edilebilir merkezi Consent Engine ve güvenli varsayılan izin yönetimi.
Faz 03 — Script Blocking ve Consent Mode [P0]
Bağımlılık: Faz 02.
Script registry, üçüncü taraf servis engelleme, GTM/GA4/Meta/TikTok entegrasyon kontrolleri, iframe/SDK engelleme, Google Consent Mode v2 ve sunucu tarafı aktarım kontrolünü uygula.
Rıza öncesinde isteğe bağlı üçüncü taraf veri aktarımı olmadığını gerçek ağ testleriyle doğrula.
Çıktı: Aktif veri aktarım kontrolü ve rızaya bağlı servis çalıştırma altyapısı.
Faz 04 — Banner, Tercih Merkezi ve Sol Alt Çerez İkonu [P0]
Bağımlılık: Faz 02 ve 03.
Eşit görsel öncelikli Kabul/Ret/Tercih butonlarını, kategori ve servis bazlı tercih merkezini, tüm sayfalarda sürekli görünen sol alt çerez ikonunu geliştir.
Mobil, klavye ve WCAG 2.2 AA erişilebilirlik gereksinimlerini uygula.
Çıktı: Gerçek Consent Engine'e bağlı, çalışan ve erişilebilir ziyaretçi arayüzü.
Faz 05 — Yasal Belge Yönetimi [P1]
Bağımlılık: Faz 01. Faz 02–04 ile paralel geliştirilebilir.
CMS yasal belge CRUD, WYSIWYG, şirket bilgileri, belge versiyonları, taslak/onay/yayın iş akışı ve /yasal, /yasal/[slug] sayfalarını oluştur.
Aydınlatma, açık rıza, sözleşme ve ticari ileti izinlerini ayrı modelle; formlarla ilişkilendir.
Çıktı: Çalışan belge yönetim sistemi ve public yasal sayfalar.
Faz 06 — Çerez Envanteri ve Gerçek Tarama Motoru [P1]
Bağımlılık: Faz 02–03 ve Faz 05'in ilgili veri/yönetim bileşenleri.
Gerçek browser taraması, çerez/storage envanteri, servis/sağlayıcı eşleştirmesi, bilinmeyen tracker tespiti ve farklı rıza senaryolarında network analizi geliştir.
Tarama sonuçlarını Review → Classify → Approve sürecine bağla.
Çıktı: Denetlenebilir gerçek tarama sonuçları ve onaylı çerez envanteri.
Faz 07 — Otomatik Çerez Politikası Senkronizasyonu [P1]
Bağımlılık: Faz 05 ve 06.
Onaylı çerez envanterini Çerez Politikası'na kategori bazlı dinamik tablolarla aktar.
Çerez değişikliklerinde yeni politika taslağı ve inceleme uyarısı üret. Geçmiş belge versiyonlarını ve yayımlanan tablo anlık görüntülerini koru.
Çıktı: Çerez envanteriyle entegre, kontrollü belge güncelleme otomasyonu.
Faz 08 — Genel Site Yasal Uygunluk Taraması [P2]
Bağımlılık: Faz 05–07.
Sayfaları, formları, üyelik, ödeme, kullanıcı içerikleri ve veri işleme süreçlerini analiz et.
Eksik belgeleri tespit et; 20 resmi kaynak listesinden uygulanabilir ve güncel kaynakları doğrulayarak hukuki referanslı belge taslakları oluştur.
Hukuki onay olmadan yayınlama yapma.
Çıktı: Eksik belge analizi, risk/kanıt raporu ve otomatik yasal belge taslakları.
Faz 09 — Dil Yönetimi ve Çok Dilli İçerikler [P2]
Bağımlılık: Faz 04–05 ve Faz 07–08'in ilgili belge/otomasyon işlevleri.
CMS dil yönetimi, çeviri versiyonları, aktif diller, dil bazlı yasal belgeler, banner, tercih merkezi ve otomatik çerez tablolarının çevirilerini geliştir.
Eksik çeviriler için taslak ve onay akışı uygula. Dil seçimini hukuki bölge ve rıza tercihlerinden bağımsız yönet.
Çıktı: Çok dilli CMP, yasal belgeler, çerez tabloları ve çeviri yönetimi.
Not: Faz 01'de i18n uyumlu veri modeli hazırlanmalı; Faz 09'a kadar tek dilli sabit içeriklerle teknik borç oluşturulmamalı.
Faz 10 — Audit, Dashboard, Bölgesel Kurallar ve Yönetişim [P1–P2]
Bağımlılık: Faz 01 ve ilgili modülün tamamlanması.
Consent/audit kayıtlarını, belge ve yapılandırma versiyonlarını, dashboard metriklerini, bildirimleri, bölgesel policy engine'i ve veri sahibi başvuru iş akışlarını tamamla.
Önemli: Temel consent log ve audit altyapısı Faz 01–03'ten itibaren çalışmalı. Faz 10 yalnızca gelişmiş raporlama ve yönetişim işlevlerinin tamamlanmasıdır.
Çıktı: Merkezi denetim, raporlama, bölgesel yönetim ve başvuru süreçleri.
Faz 11 — Entegrasyon, E2E ve Production Kabul Testleri [P0]
Bağımlılık: Yayına alınacak tüm fazların tamamlanması.
Rıza öncesi gerçek network testleri, kabul/ret/kısmi izin/geri çekme, çerez tarama, otomatik belge taslağı, dil değiştirme, CMS yetkileri, belge versiyonları, responsive, erişilebilirlik, güvenlik, migration, build, lint ve typecheck kontrollerini gerçekleştir.
Çıktı: Test raporu, açık riskler, deployment checklist ve production kabul sonucu.
Faz Geçiş Kuralları
1. Faz 02–03 doğrulanmadan CMP'nin güvenli olduğu iddia edilmesin.
2. Faz 03 tamamlanmadan banner tek başına production çözümü sayılmasın.
3. Faz 05 ve 06 tamamlanmadan çerez politika otomasyonu başlatılmasın.
4. Faz 07 tamamlanmadan taramaya dayalı yasal metin güncellemesi yayınlanmasın.
5. Faz 08, gerçek site bulguları ve doğrulanmış resmi kaynaklar üzerinden çalışsın.
6. Faz 09, mevcut proje dil altyapısıyla uyumlu olsun.
7. Her faz kendi unit/integration testlerinden geçsin; Faz 11'de uçtan uca kabul testleri tekrarlansın.
8. Bağımsız işler paralel geliştirilebilir; onay ve bağımlılık kontrolleri atlanamaz.
9. Tamamlanan her faz sonunda değişen dosyalar, migration'lar, testler, riskler ve sonraki fazın hazır olma durumu raporlansın.
10. Eksik, sahte veya test edilmemiş işlevler tamamlanmış olarak işaretlenmesin.

17. Kabul Kriterleri
Geliştirme ancak aşağıdakiler doğrulandığında tamamlanmış sayılabilir:
1. CMS ve /yasal sayfaları çalışıyor.
2. Yasal belgeler oluşturuluyor, versiyonlanıyor ve onaylanarak yayınlanıyor.
3. Site taraması gerçek çerez ve tracker sonuçları üretiyor.
4. Tespit edilen ve onaylanan çerezler Çerez Politikası'na otomatik tablo halinde ekleniyor.
5. Yeni çerezler bulunduğunda belge güncelleme taslağı oluşuyor.
6. Genel site analizi eksik yasal belgeleri tespit edebiliyor.
7. Eksik belgeler resmi kaynak referanslı taslak olarak oluşturuluyor.
8. Otomatik taslaklar yetkili onayı olmadan yayınlanmıyor.
9. Sol alt çerez ikonu tüm sayfalarda erişilebilir.
10. Kabul/Ret/Tercih butonları görsel açıdan eşit.
11. Rıza öncesi isteğe bağlı üçüncü taraf veri aktarımı gerçekleşmiyor.
12. Kısmi izin, ret ve geri çekme senaryoları çalışıyor.
13. Consent Mode ve script engelleme birlikte çalışıyor.
14. Çerez envanteri, politika sürümü ve rıza kayıtları tutarlı.
15. Form izinleri ve hukuki belge versiyonları ilişkilendiriliyor.
16. Audit log, RBAC ve güvenlik kontrolleri çalışıyor.
17. Mobil, klavye ve ekran okuyucu testleri başarılı.
18. Tarama, mevzuat kontrolü ve entegrasyon sınırlamaları açıkça raporlanıyor.
19. Production build, migration, typecheck, lint ve E2E testleri başarılı.
20. Mevcut web uygulaması özellikleri bozulmamış.
Teslimat: Yapılan geliştirmeler, dosyalar, migration'lar, yeni ayarlar, gerçek tarama çıktıları, oluşturulan belge taslakları, resmi kaynaklar, test sonuçları, sınırlamalar ve deployment checklist raporlansın.
Kesin kurallar: Uydurma veri üretme. Rakip ürün adlarına veya kopyalanmış arayüzlerine yer verme. Hukuki uygunluğu otomatik garanti etme. Kullanıcının rızasını varsayma. Reddetmeyi zorlaştırma. Onaylı belgeleri sessizce değiştirme. Teknik olarak doğrulanmamış işlevleri tamamlandı olarak raporlama.
