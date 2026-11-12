# -*- coding: utf-8 -*-
"""V3 maddeleri A10, A13–A18 (2026-11-12): API güvenlik standartları (api_features'a 5 seçenek), SLO ve kapasite
hedefleri (performance_eng), felaket kurtarma hedefleri ve önlemleri (backup_recovery), panel / yönetici kullanıcı
yönetimi (auth), çerez izin davranışı, hukuki metin yönetimi, sürümleme ve onay kaydı, kişisel veri envanteri,
saklama-imha, ilgili kişi başvuruları ve veri ihlali (privacy). Yeni bölüm yok; alanlar var olan bölümlere eklenir.

Hukuki dayanaklar 2026-11-12'de resmî metinden okunarak doğrulandı: KVKK m. 13 (başvuruya en geç otuz gün),
Silme Yönetmeliği m. 11 (periyodik imha aralığı altı ayı geçemez; politika yükümlülüğü olmayan veri sorumlusu üç ay),
Kurul'un 24.01.2019 tarihli 2019/10 sayılı kararı (Kurul'a gecikmeksizin ve en geç 72 saat, ilgili kişilere makul en
kısa sürede, veri ihlali müdahale planı), KVKK Çerez Uygulamaları Rehberi (Temmuz 2025: kabul / ret / tercihler eşit
derecede), Mesafeli Sözleşmeler Yönetmeliği m. 7, 8, 20 (ön bilgilerin teyidi, ödeme yükümlülüğü bildirimi,
işlem bilgi ve belgelerinin üç yıl saklanması)."""


def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    if exclusive:
        x['exclusive'] = True
    return x


# --- Sorumlu pozisyon ajanları (pozisyonlar.txt'ten birebir)
API = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani'
SWE = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
SRE = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/site-guvenilirlik-muhendisi'
DEVOPS = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/kidemli-devops-muhendisi'
DR = 'poz:bilgi-teknolojileri:15.02/yedekleme-depolama-ve-felaket-kurtarma/felaket-kurtarma-uzmani'
BKP = 'poz:bilgi-teknolojileri:15.02/yedekleme-depolama-ve-felaket-kurtarma/kidemli-depolama-ve-yedekleme-uzmani'
CLOUD = 'poz:bilgi-teknolojileri:15.02/bulut-platformlari-ve-finops/kidemli-bulut-muhendisi'
IAM = 'poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/kidemli-kimlik-ve-erisim-uzmani'
ACCGOV = 'poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/erisim-yonetisimi-uzmani'
AUTHN = 'poz:siber-guvenlik:16.05/kimlik-dogrulama-ve-musteri-kimligi-guvenligi/kidemli-kimlik-dogrulama-uzmani'
IR = 'poz:siber-guvenlik:16.04/siber-olay-mudahale-ve-dijital-adli-inceleme/kidemli-olay-mudahale-uzmani'
PRIVENG = 'poz:siber-guvenlik:16.07/gizlilik-muhendisligi-ve-teknik-kontroller/kidemli-gizlilik-muhendisligi-uzmani'
KVKK = 'poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani'
INV = 'poz:uyum-risk:06.06/veri-envanteri-ve-kontroller/veri-envanteri-uzmani'
RET = 'poz:uyum-risk:06.06/veri-envanteri-ve-kontroller/saklama-ve-imha-kontrol-uzmani'
APPL = 'poz:uyum-risk:06.06/basvuru-ve-ihlal-koordinasyonu/ilgili-kisi-basvuru-koordinasyon-uzmani'
BREACH = 'poz:uyum-risk:06.06/basvuru-ve-ihlal-koordinasyonu/veri-ihlali-koordinasyon-uzmani'
LAWKVKK = 'poz:hukuk:05.06/veri-koruma-danismanligi-ekibi/kvkk-ve-gdpr-hukuk-uzmani'
LAWDOC = 'poz:hukuk:05.06/veri-sozlesmeleri-ve-aktarim-ekibi/veri-koruma-dokumantasyon-uzmani'
CONTRACT = 'poz:hukuk:05.02/sozlesme-standartlari-ekibi/sozlesme-sablonlari-uzmani'

BACKUP_ON = [{'field': 'backup_strategy', 'in': ['Managed Daily', 'Daily PITR', 'Custom']}]
CMP_ON = [{'field': 'cookie_manager', 'in': ['CookieYes', 'Cookiebot', 'Usercentrics', 'Custom', 'Other']}]
MEMBERS = ['Open', 'Approval', 'Invite']


# ============================================================ A10 — API standartlarına 5 seçenek
OPTION_ADD = [
    {'field': 'api_features', 'after': 'OpenAPI', 'option': o(
        'Token Lifecycle', 'Erişim / yenileme jetonu yaşam döngüsü',
        'Kısa ömürlü erişim jetonu (access token), daha uzun ömürlü ve tek kullanımlık yenileme jetonu (refresh token), jeton yenileme, iptal ve oturum sonlandırma kurallarının tanımlanmasıdır.',
        'API\'ye oturum açmış kullanıcılar, mobil uygulama ya da ayrı ön yüz bağlanıyorsa; özellikle jeton tabanlı (JWT, OAuth 2.0) kimlik doğrulama kullanılıyorsa.',
        'Erişim jetonu 15 dakika geçerlidir; süresi dolunca uygulama arka planda yenileme jetonuyla yenisini alır. Kullanıcı "Tüm cihazlardan çık" dediğinde bütün yenileme jetonları iptal edilir.',
        'Erişim jetonu kısa ömürlüdür (ör. 5–15 dakika) ve her istekte imza, süre, yayıncı ve hedef (iss, aud, exp) sunucuda doğrulanır; yenileme jetonu her kullanımda yenisiyle değiştirilir (rotasyon), yeniden kullanılan eski jeton bütün jeton ailesini iptal eder; çıkış, parola değişikliği ve yetki değişikliğinde ilgili jetonlar sunucu tarafında iptal edilir; tarayıcıda jetonlar localStorage\'a değil HttpOnly + Secure çerezine yazılır ve jetonlar loglara düşmez.')},
    {'field': 'api_features', 'after': 'Token Lifecycle', 'option': o(
        'API Keys', 'API anahtarı yönetimi (oluşturma, rotasyon, iptal, kapsam)',
        'Sunucudan sunucuya ya da iş ortağı entegrasyonlarında kullanılan API anahtarlarının oluşturulması, kapsamının sınırlanması, süreli yenilenmesi (rotasyon) ve iptal edilmesi sürecidir.',
        'İş ortakları, bayiler, harici sistemler ya da müşteriler API\'ye kendi anahtarlarıyla bağlanıyorsa.',
        'Panelde "Yeni API anahtarı" ile anahtar yalnız bir kez gösterilir; listede yalnız ilk 4 karakteri, son kullanım tarihi ve kapsamı görünür; "İptal et" anahtarı anında geçersiz kılar.',
        'API anahtarları yalnız bir kez gösterilir, veritabanında özet değeri (hash) olarak saklanır; her anahtarın sahibi, kapsamı, son kullanma tarihi ve son kullanım zamanı tutulur; rotasyon sırasında eski ve yeni anahtar kısa bir geçiş süresince birlikte çalışır; iptal anında geçerli olur, anahtar oluşturma / iptal işlemleri denetim kaydına yazılır ve anahtar değeri hiçbir log ya da hata mesajında yer almaz.')},
    {'field': 'api_features', 'after': 'API Keys', 'option': o(
        'Scopes', 'Uç nokta bazında yetki kapsamları (scope)',
        'Her API uç noktası (endpoint) için hangi yetki kapsamının (ör. orders:read, orders:write) gerektiğinin ayrı ayrı tanımlanması ve her istekte denetlenmesidir.',
        'Farklı rollerin, iş ortaklarının ya da uygulamaların API\'nin yalnız bir bölümüne erişmesi gerekiyorsa.',
        'Muhasebe entegrasyonunun anahtarı yalnız "invoices:read" kapsamına sahiptir; sipariş iptal uç noktasını çağırınca 403 Forbidden döner.',
        'Her uç noktanın gerektirdiği kapsam OpenAPI tanımında ve kodda açıkça yazılır; yetki denetimi varsayılan reddet ilkesiyle sunucuda, her istekte yapılır; jetona ya da anahtara yalnız işi için gereken en dar kapsam verilir; kapsam denetimi nesne düzeyindeki sahiplik denetiminin (IDOR / BOLA) yerine geçmez, ikisi birlikte uygulanır.')},
    {'field': 'api_features', 'after': 'Scopes', 'option': o(
        'Problem Details', 'Standart hata yanıtı biçimi (RFC 9457 Problem Details)',
        'API hata yanıtlarının bütün uç noktalarda aynı JSON biçiminde (type, title, status, detail, instance) dönmesidir; RFC 9457 standardıdır.',
        'API\'yi birden çok istemci (web, mobil, iş ortağı) kullanıyorsa ve hataların istemcide tutarlı işlenmesi gerekiyorsa.',
        'Geçersiz e-posta için 422 yanıtı: {"type": "https://alanadi.com/problems/validation", "title": "Doğrulama hatası", "status": 422, "errors": [{"field": "email", "message": "Geçerli bir e-posta girin"}]}.',
        'Hata yanıtları application/problem+json türünde, RFC 9457 alanlarıyla (type, title, status, detail, instance) döner; doğrulama hatalarında alan bazlı hata listesi eklenir; yanıtlarda yığın izi (stack trace), SQL, iç sunucu adı ya da kişisel veri yer almaz; her hata yanıtında loglardaki kayda bağlanan bir istek kimliği (correlation ID) bulunur.')},
    {'field': 'api_features', 'after': 'Problem Details', 'option': o(
        'Deprecation Policy', 'Sürüm kullanımdan kaldırma politikası (Deprecation / Sunset)',
        'Eski API sürümlerinin ne zaman kullanımdan kaldırılacağının duyurulması, yanıtlarda Deprecation (RFC 9745) ve Sunset (RFC 8594) başlıklarıyla bildirilmesi ve kaldırma takviminin yazılı olmasıdır.',
        'API\'yi sizin kontrolünüzde olmayan istemciler (mobil uygulamanın eski sürümleri, iş ortakları) kullanıyorsa ve sürümler zamanla değişecekse.',
        'v1 uç noktası artık "Deprecation" ve "Sunset: Wed, 30 Jun 2027 23:59:59 GMT" başlıklarıyla yanıt verir; geliştirici dokümanında v1 → v2 geçiş rehberi ve takvim yer alır.',
        'Sürümler anlamsal sürümleme (major.minor.patch) ile numaralanır, geriye uyumsuz değişiklik yalnız yeni major sürümle yapılır; kullanımdan kaldırılan sürüm Deprecation (RFC 9745) ve Sunset (RFC 8594) başlıklarıyla ve geçiş belgesine Link başlığıyla işaretlenir; kaldırma tarihi önceden duyurulur, eski sürümün kullanımı izlenir ve sunset tarihinden önce kullanıcılar bilgilendirilir.')},
]


# ============================================================ A13 — SLO ve kapasite (performance_eng)
F_PERF = [
    {'id': 'slo_targets', 'section': 'performance_eng', 'after': 'performance_controls', 'type': 'select',
     'label': 'Hizmet Seviyesi Hedefleri (SLO)', 'en': 'Service Level Objectives (SLO)', 'agents': [SRE, DEVOPS],
     'explanation': 'Sitenin ve API\'nin ölçülebilir güvenilirlik ve hız hedefleridir: çalışma süresi (uptime), kritik API uç noktalarında 95. yüzdelik yanıt süresi (p95), hata oranı ve önbellek isabet oranı. Hedefler 28 ya da 30 günlük kayan pencerede gerçek trafikten ölçülür.',
     'scenario': 'Sitenin kesintisi ya da yavaşlığı gelir, itibar ya da sözleşme kaybına yol açıyorsa; ekip "ne kadar iyi yeterince iyi" sorusuna ortak bir sayıyla yanıt vermek istiyorsa.',
     'example': 'İzleme panelinde "Sipariş API — p95: 380 ms (hedef < 500 ms), hata oranı: %0,4 (hedef < %1), çalışma süresi 30 gün: %99,96 (hedef ≥ %99,9)" satırları yeşil görünür.',
     'rule': 'Hizmet seviyesi hedefleri (SLO): {label}. Hedefler kullanıcı tarafından görülen gerçek trafikten, 30 günlük kayan pencerede ölçülür ve İzleme Kapsamı kararındaki araçlarla panoda gösterilir; ölçüm, sağlık kontrolü ve bakım trafiğini hedef hesabından ayırır. Core Web Vitals hedefleri ayrıca Performans bölümündeki karardan gelir.',
     'options': [
         o('basic', 'Temel: çalışma süresi ≥ %99,5, kritik API p95 < 1 sn, hata oranı < %2', 'Küçük kurumsal site ya da iç araç için yeterli, maliyeti düşük hedef seti; ayda yaklaşık 3,6 saat kesinti payı bırakır.', 'Tanıtım sitesi, düşük trafikli içerik sitesi, kesintinin doğrudan gelir kaybı yaratmadığı projeler.', 'Aylık raporda "Çalışma süresi %99,7 — hedef %99,5 karşılandı" yazar; tek sunucu ve günlük yedekle çalışılır.',
           'Hedefler: aylık çalışma süresi ≥ %99,5, kritik API uç noktalarında p95 < 1 saniye, 5xx hata oranı < %2; hedef aşımı haftalık raporda gösterilir.'),
         o('standard', 'Standart: çalışma süresi ≥ %99,9, kritik API p95 < 500 ms, hata oranı < %1, önbellek isabeti ≥ %80 (önerilen)', 'Proje dokümanındaki hedef seti: kritik servislerde ayda yaklaşık 43 dakika kesinti payı, hızlı API ve yüksek önbellek isabeti.', 'E-ticaret, üyelik, rezervasyon ve SaaS gibi kullanıcının işlem yaptığı projeler.', 'Ödeme ve sepet API\'lerinin p95 süresi 500 ms\'yi aşınca nöbetçi ekibe uyarı gider; önbellek isabeti %80\'in altına düşen sorgu raporda kırmızı görünür.',
           'Hedefler: kritik servislerde aylık çalışma süresi ≥ %99,9, kritik API uç noktalarında p95 < 500 ms, ortalama API hata oranı < %1, kritik sorgularda önbellek isabet oranı ≥ %80; kritik uç noktaların listesi ve her biri için hedef dokümante edilir.'),
         o('high', 'Yüksek: çalışma süresi ≥ %99,95, kritik API p95 < 300 ms, hata oranı < %0,5', 'Kesintinin doğrudan büyük gelir ya da sözleşme cezası yarattığı, yedekli altyapı gerektiren sıkı hedef seti; ayda yaklaşık 22 dakika kesinti payı.', 'Yüksek hacimli pazar yeri, ödeme altyapısı, sözleşmeyle SLA verilen kurumsal (B2B) platform.', 'Çok bölgeli kurulumda bir bölge düştüğünde trafik otomatik diğerine geçer; aylık raporda "%99,97" görünür.',
           'Hedefler: aylık çalışma süresi ≥ %99,95, kritik API uç noktalarında p95 < 300 ms, hata oranı < %0,5; bu hedefler yedekli (çok bölgeli ya da çok erişilebilirlik alanlı) altyapı, otomatik yük devretme ve nöbet düzeni olmadan taahhüt edilmez.'),
         o('measure_first', 'Önce ölç, sonra hedef koy', 'Canlı trafik ölçülmeden sayı taahhüt edilmez; ilk 4–6 hafta ölçüm yapılır, hedefler gerçek değerlere göre belirlenir.', 'Yeni ürün, trafiği tahmin edilemeyen proje ya da mevcut sistemin ölçüm altyapısı henüz kurulmamışsa.', 'Yayından sonraki altı haftalık raporda p95, hata oranı ve çalışma süresi ölçülür; hedefler bu değerlerin biraz üstüne yazılır.',
           'Yayından itibaren p95 yanıt süresi, hata oranı, çalışma süresi ve önbellek isabeti ölçülür; 4–6 haftalık veriden sonra hedefler yazılı olarak belirlenir ve bu karar güncellenir.'),
     ]},

    {'id': 'slo_practices', 'section': 'performance_eng', 'after': 'slo_targets', 'type': 'multiselect',
     'label': 'Ölçeklenebilirlik ve Kapasite Uygulamaları', 'en': 'Scalability & Capacity Practices', 'agents': [SRE, CLOUD],
     'explanation': 'Hedeflerin yoğun trafikte de tutması için uygulanacak işlerdir: hata bütçesi, otomatik ölçekleme eşikleri, yük testi, kampanya öncesi kapasite testi, SLO panosu ve uyarılar.',
     'scenario': 'Trafiğin dönemsel olarak katlandığı (kampanya, indirim günü, kayıt dönemi) ya da yatay ölçeklenebilir altyapı kullanan projeler.',
     'example': 'Büyük indirim kampanyasından iki hafta önce beklenen trafiğin 3 katıyla yük testi yapılır; rapor ve ölçekleme eşikleri depoda (repo) saklanır.',
     'rule': 'Ölçeklenebilirlik ve kapasite uygulamaları: {labels}.',
     'options': [
         o('error_budget', 'Hata bütçesi politikası', 'SLO\'nun izin verdiği kesinti / hata payıdır (ör. %99,9 hedefte ayın %0,1\'i). Bütçe tükenince yeni özellik yayını yavaşlatılır, güvenilirlik işine öncelik verilir.', 'Sık yayın yapan ve hız ile kararlılık arasında denge kurmak isteyen ekipler.', 'Ayın 20\'sinde hata bütçesinin %90\'ı harcanmışsa yalnız düzeltme ve güvenilirlik yayınları yapılır.',
           'SLO hedeflerinden aylık hata bütçesi hesaplanır ve panoda gösterilir; bütçe tükendiğinde ne yapılacağı (yayın dondurma, kök neden çalışması) yazılı politika olarak dokümante edilir.'),
         o('autoscale', 'Otomatik ölçekleme eşikleri', 'CPU, bellek, istek sayısı ya da kuyruk uzunluğuna göre sunucu / konteyner sayısının otomatik artırılıp azaltılmasıdır; en az ve en çok kopya sayısı yazılıdır.', 'Bulut ya da konteyner altyapısında çalışan, trafiği gün içinde değişen projeler.', 'CPU %70\'i 5 dakika aşınca uygulama kopyası 2\'den 6\'ya çıkar; gece trafiği düşünce 2\'ye iner.',
           'Uygulama durumsuz (stateless) tasarlanır; ölçekleme metriği, eşikler, en az / en çok kopya sayısı ve soğuma süreleri altyapı kodunda tanımlanır; veritabanı bağlantı havuzu en çok kopya sayısına göre boyutlandırılır.'),
         o('load_test', 'Yük testi ve raporu', 'Beklenen ve beklenenin üstündeki trafiğin test ortamında üretilip yanıt süresi, hata oranı ve kaynak kullanımının ölçülmesidir; sonuçlar raporlanır.', 'Canlıya çıkış öncesi ve büyük mimari değişikliklerden sonra.', 'Rapor: "500 eş zamanlı kullanıcıda p95 420 ms, 1.200 kullanıcıda veritabanı CPU %95 — darboğaz: ürün arama sorgusu".',
           'Kritik kullanıcı akışları için yük, stres ve uzun süreli dayanıklılık (soak) testleri betik olarak depoda tutulur; testler canlı veriyle değil, anonim ya da sentetik veriyle yapılır; sonuçlar ve bulunan darboğazlar raporlanır.'),
         o('campaign_test', 'Kampanya öncesi kapasite testi ve geçici kaynak artırımı', 'Bilinen yoğun dönemlerden önce beklenen trafiğe göre kapasite testi yapılması ve kaynakların geçici olarak artırılmasıdır.', 'İndirim günü, lansman, kayıt dönemi gibi önceden bilinen trafik zirveleri olan projeler.', 'Kampanya takviminde "Efsane Cuma: 3 kat trafik testi 10 gün önce, en az kopya sayısı 2 → 6, kampanya bitince geri al" maddesi vardır.',
           'Pazarlama takvimindeki yoğun dönemlerden en az bir hafta önce beklenen trafiğin en az 2 katıyla kapasite testi yapılır; geçici kaynak artırımı ve geri alma adımları önceden yazılır.'),
         o('slo_dashboard', 'SLO panosu ve uyarılar', 'SLO göstergelerinin (çalışma süresi, p95, hata oranı, önbellek isabeti) tek panoda izlenmesi ve hedef aşılmadan önce uyarı verilmesidir.', 'Canlı trafik alan bütün projeler.', 'Hata bütçesi normalin 10 katı hızla tükenmeye başlayınca nöbetçiye anlık bildirim gider.',
           'SLO göstergeleri tek panoda izlenir; uyarılar ham eşik yerine hata bütçesinin tükenme hızına göre kurulur, her uyarının sahibi ve müdahale adımı (runbook) bellidir.'),
         o('synthetic', 'Sentetik izleme (dışarıdan düzenli kontrol)', 'Kritik sayfa ve API\'lerin farklı konumlardan düzenli aralıklarla otomatik olarak çağrılıp yanıt süresi ve doğruluğunun ölçülmesidir.', 'Gece ya da düşük trafikte de kesintiyi hemen fark etmek gerekiyorsa.', 'Her dakika İstanbul ve Frankfurt\'tan ana sayfa, giriş ve sepet akışı denenir; iki konum üst üste başarısız olursa uyarı gider.',
           'Ana sayfa, giriş, arama ve ödeme gibi kritik akışlar en az iki konumdan düzenli olarak sentetik testle denetlenir; sentetik trafik analitik verisinden ayrılır.'),
         o('degradation', 'Kontrollü işlev kaybı (graceful degradation)', 'Bağımlı bir servis (arama, öneri, kargo hesaplama) çökünce sitenin tamamen durmak yerine o işlevi devre dışı bırakarak çalışmaya devam etmesidir.', 'Çok sayıda dış servise ya da mikroservise bağımlı projeler.', 'Öneri servisi yanıt vermezse ürün sayfası "Benzer ürünler" bölümü olmadan açılır; sipariş akışı etkilenmez.',
           'Dış servis çağrılarında zaman aşımı, sınırlı yeniden deneme ve devre kesici (circuit breaker) kullanılır; kritik olmayan işlevler için yedek davranış tanımlanır, kritik akış (giriş, ödeme) bağımlılıklarından yalıtılır.'),
         o('capacity_review', 'Dönemsel kapasite ve maliyet gözden geçirmesi', 'Kaynak kullanımı, büyüme eğilimi ve maliyetin belirli aralıklarla gözden geçirilip yatay / dikey ölçekleme kararlarının güncellenmesidir.', 'Büyüyen ve bulut maliyeti önemli olan projeler.', 'Üç ayda bir: "Veritabanı depolama aylık %8 büyüyor, 5 ay sonra sınır; okuma kopyası eklenecek" kararı yazılır.',
           'Kaynak kullanımı ve büyüme eğilimi en az üç ayda bir gözden geçirilir; darboğaz tahmini, ölçekleme kararı ve maliyet etkisi kayda alınır.'),
     ]},
]


# ============================================================ A14 — felaket kurtarma (backup_recovery)
F_DR = [
    {'id': 'dr_targets', 'section': 'backup_recovery', 'after': 'restore_testing', 'type': 'select',
     'label': 'Felaket Kurtarma Hedefleri (RTO / RPO)', 'en': 'Disaster Recovery Targets (RTO / RPO)', 'agents': [DR, DEVOPS], 'showIf': BACKUP_ON,
     'explanation': 'RTO (kurtarma süresi hedefi), büyük bir arızadan sonra hizmetin en geç ne kadar sürede yeniden çalışacağıdır; RPO (kurtarma noktası hedefi), en çok ne kadarlık verinin kaybedilmesinin kabul edileceğidir. Yedekleme stratejisi bu hedefleri karşılayacak biçimde seçilir.',
     'scenario': 'Veritabanı silinmesi, fidye yazılımı, bölge çapında bulut kesintisi gibi felaketlerde ne kadar bekleme ve veri kaybının kabul edilebilir olduğuna iş tarafı karar vermeliyse.',
     'example': 'RTO 4 saat / RPO 1 saat seçildiğinde, saat 14:00\'te veritabanı bozulursa site en geç 18:00\'de açılır ve en çok 13:00 sonrası girilen kayıtlar kaybolabilir.',
     'rule': 'Felaket kurtarma hedefleri: {label}. Seçilen yedekleme stratejisi ve sıklığı bu hedefleri karşılamalıdır; karşılamıyorsa uyumsuzluk kullanıcıya raporlanır. Hedefler felaket kurtarma planında yazılır ve geri yükleme testlerinde ölçülen gerçek sürelerle karşılaştırılır.',
     'recommend': {'field': 'backup_strategy', 'map': {'Managed Daily': ['rto24'], 'Daily PITR': ['rto4'], 'Custom': ['rto4']}},
     'options': [
         o('rto24', 'Temel: RTO 24 saat / RPO 24 saat', 'Günlük yedekten geri dönüş: en çok bir günlük veri kaybı ve bir iş günü içinde yeniden açılış.', 'İçeriği seyrek değişen kurumsal site, blog, tanıtım sitesi.', 'Gece 03:00 yedeği alınır; ertesi gün öğlen arıza olursa sabahtan beri yapılan içerik düzenlemeleri yeniden girilir.',
           'Günlük otomatik yedek yeterlidir; geri yükleme adımları en çok 24 saatte tamamlanacak biçimde yazılır ve test edilir.'),
         o('rto4', 'Standart: RTO 4 saat / RPO 1 saat (önerilen)', 'Zamana göre geri dönüş (PITR) ile en çok bir saatlik veri kaybı ve aynı gün içinde yeniden açılış.', 'Sipariş, üyelik, form ya da rezervasyon kaydı alan projeler.', 'Hatalı bir toplu güncelleme 10:42\'de fark edilir; veritabanı 10:40 durumuna geri döndürülür, site öğleden önce açılır.',
           'Veritabanında zamana göre geri dönüş (PITR) ya da en az saatlik yedek zorunludur; altyapı kod olarak (IaC) tanımlanır ki ortam 4 saat içinde yeniden kurulabilsin.'),
         o('rto1', 'Yüksek: RTO 1 saat / RPO 15 dakika', 'Sürekli günlük (WAL / binlog) aktarımı ve hazır bekleyen (warm standby) ortamla hızlı geri dönüş.', 'Kesintinin saat başı ciddi gelir kaybı yarattığı e-ticaret ve SaaS projeleri.', 'Ana bölge çöktüğünde ikinci bölgedeki hazır veritabanı kopyası 30 dakikada birincil yapılır, DNS yönlendirilir.',
           'Veritabanı değişiklik günlükleri en çok 15 dakikalık gecikmeyle ikinci konuma aktarılır; ikinci konumda hazır bekleyen ortam bulunur ve yük devretme adımları runbook\'ta yazılıdır.'),
         o('rto_min', 'Kesintisiz: RTO dakikalar / RPO sıfıra yakın (çok bölgeli, aktif-aktif)', 'Birden çok bölgede aynı anda çalışan, eşzamanlı çoğaltmalı yapı; en pahalı ve en karmaşık seçenektir.', 'Ödeme altyapısı, sözleşmeyle yüksek SLA verilen kritik platformlar.', 'Bir bulut bölgesi tamamen kapandığında kullanıcılar fark etmeden diğer bölgeden hizmet almaya devam eder.',
           'Uygulama ve veri en az iki bölgede çalışır; otomatik yük devretme ve veri tutarlılığı yöntemi mimari karar kaydında (ADR) gerekçelendirilir; maliyet ve karmaşıklık kullanıcı onayı olmadan üstlenilmez.'),
     ]},

    {'id': 'dr_measures', 'section': 'backup_recovery', 'after': 'dr_targets', 'type': 'multiselect',
     'label': 'Felaket Kurtarma ve Süreklilik Önlemleri', 'en': 'Disaster Recovery & Continuity Measures', 'agents': [DR, BKP, DEVOPS], 'showIf': BACKUP_ON,
     'explanation': 'Yedeklerin gerçekten işe yaraması ve hizmetin felakette sürdürülebilmesi için alınacak önlemlerdir: yazılı plan ve runbook, medya dosyaları için ayrı yedek, farklı bölgede şifreli kopya, değiştirilemez yedek, yüksek erişilebilirlik, tatbikat.',
     'scenario': 'Yedeklerin aynı hesapta / aynı bölgede durduğu, medya dosyalarının yedeklenmediği ya da geri yüklemenin hiç denenmediği durumlarda risk yüksektir.',
     'example': 'Fidye yazılımı üretim hesabını şifrelediğinde, ayrı bir hesaptaki değiştirilemez (immutable) yedekten veritabanı ve görseller geri yüklenir; adımlar runbook\'tan izlenir.',
     'rule': 'Felaket kurtarma ve süreklilik önlemleri: {labels}. Yedekleme ve geri yükleme betikleri depoda tutulur; yedeklere erişim en az yetkiyle ve üretim hesabından ayrı kimlik bilgileriyle yapılır.',
     'options': [
         o('dr_plan', 'Yazılı felaket kurtarma planı ve runbook', 'Kim, hangi sırayla, hangi komutlarla hizmeti geri getirir: iletişim listesi, karar yetkisi, adım adım geri yükleme talimatı.', 'Bütün canlı projeler; özellikle ekipte tek kişinin bildiği kurulumlar.', 'DEPLOYMENT.md\'nin yanında "FELAKET-KURTARMA.md": senaryolar, sorumlular, komutlar, doğrulama adımları.',
           'Felaket kurtarma planı ve geri yükleme runbook\'u depoda yazılı tutulur; senaryolar (veri silinmesi, bölge kesintisi, fidye yazılımı, hesabın ele geçirilmesi), sorumlular ve doğrulama adımlarını içerir, altyapı değiştikçe güncellenir.'),
         o('media_backup', 'Medya ve dosyalar için ayrı yedek', 'Veritabanı dışındaki yüklenen görseller, belgeler ve dosya deposunun (S3, R2 vb.) ayrı bir yedekleme stratejisiyle korunmasıdır.', 'Kullanıcıların ya da editörlerin dosya yüklediği projeler.', 'Nesne deposunda sürümleme açıktır ve dosyalar her gece ayrı hesaptaki bir kovaya kopyalanır.',
           'Yüklenen dosyalar ve medya, veritabanından ayrı olarak sürümleme ve düzenli kopyalama ile yedeklenir; veritabanındaki dosya kayıtları ile depodaki dosyaların tutarlılığı geri yükleme testinde denetlenir.'),
         o('offsite', 'Farklı bölgede / hesapta şifreli kopya (3-2-1)', 'Yedeklerin en az bir kopyasının üretim ortamından farklı bölgede ve farklı hesapta tutulmasıdır (3 kopya, 2 farklı ortam, 1 kopya başka yerde).', 'Bulut bölgesi kesintisine ya da hesabın ele geçirilmesine karşı korunmak isteyen projeler.', 'Avrupa bölgesindeki üretim yedekleri her gece başka bölgedeki ayrı bir yedek hesabına şifreli olarak kopyalanır.',
           'Yedeklerin en az bir kopyası farklı bölgede ve ayrı yetkilendirilmiş bir hesapta tutulur; yedekler aktarımda ve depoda şifrelenir, şifreleme anahtarları yedekle aynı yerde saklanmaz; yurt dışına kopyalama KVKK yurt dışı aktarım kurallarına göre değerlendirilir.'),
         o('immutable', 'Değiştirilemez (immutable) yedek', 'Belirli süre boyunca kimsenin, yönetici hesabının bile silemediği ya da değiştiremediği yedek kopyalarıdır (nesne kilidi / WORM).', 'Fidye yazılımı ve yetkili hesabın ele geçirilmesi riskine karşı.', 'Yedek kovasında 30 günlük nesne kilidi vardır; ele geçirilen yönetici hesabı yedekleri silmeye çalışınca işlem reddedilir.',
           'En az bir yedek kopyası belirli saklama süresince silinemez ve değiştirilemez biçimde (nesne kilidi / WORM) tutulur; yedek silme yetkisi üretim yöneticilerinden ayrıdır.'),
         o('ha', 'Yüksek erişilebilirlik ve yedekli yapı', 'Kritik bileşenlerin (uygulama, veritabanı, yük dengeleyici) birden çok kopya ve erişilebilirlik alanında çalışması; tek bir arızanın hizmeti durdurmamasıdır.', 'Yüksek SLO hedefi olan, kesintinin doğrudan gelir kaybı yarattığı projeler.', 'Veritabanının ikinci erişilebilirlik alanında eş zamanlı kopyası vardır; birincil düşerse 1–2 dakikada otomatik geçiş olur.',
           'Kritik bileşenlerde tek hata noktası bırakılmaz: uygulama en az iki kopyada, veritabanı yedek kopyalı ve otomatik yük devretmeli çalışır; bakım ve güncellemeler kesintisiz yayın yöntemleriyle yapılır.'),
         o('drill', 'Felaket kurtarma tatbikatı', 'Planın gerçek bir ortamda baştan sona denenmesi ve ölçülen sürelerin RTO / RPO hedefleriyle karşılaştırılmasıdır.', 'Plan yazılmış ama hiç denenmemişse; ekip ya da altyapı değiştiyse.', 'Yılda bir, test ortamı sıfırdan kurulup son yedekten açılır: "Ölçülen RTO 3 saat 10 dk — hedef 4 saat, karşılandı".',
           'Felaket kurtarma tatbikatı en az yılda bir yapılır (Restore Testi kararındaki sıklık tek tablo / tek veritabanı geri yüklemesini kapsar); ölçülen süreler, sorunlar ve düzeltmeler raporlanır.'),
         o('backup_monitoring', 'Yedek başarısızlık uyarısı ve bütünlük kontrolü', 'Yedekleme işi başarısız olduğunda ya da beklenen boyutun çok altında kaldığında uyarı verilmesi ve yedeklerin okunabilirliğinin otomatik denetlenmesidir.', 'Otomatik yedek alınan bütün projeler; sessizce bozulan yedekler en sık görülen sorundur.', 'Gece yedeği alınamayınca sabah 07:00\'de ekip kanalına "Yedek başarısız: orders-db" bildirimi düşer.',
           'Her yedekleme işinin sonucu izlenir; başarısızlık, gecikme ya da olağan dışı boyut değişiminde uyarı verilir; yedeklerin sağlama toplamı (checksum) ve açılabilirliği düzenli olarak otomatik denetlenir.'),
         o('backup_retention', 'Yedek saklama süresi ve kişisel verinin yedekten düşmesi', 'Yedeklerin ne kadar süre tutulacağı ve silinen / imha edilen kişisel verinin yedeklerde ne zaman ortadan kalkacağının tanımlanmasıdır.', 'Kişisel veri işleyen ve KVKK saklama-imha politikası olan projeler.', 'Günlük yedekler 30 gün, aylık yedekler 12 ay tutulur; hesabını silen üyenin verisi en geç 12 ay sonra bütün yedeklerden çıkar.',
           'Yedek saklama süreleri (günlük, haftalık, aylık) yazılı olarak belirlenir ve otomatik uygulanır; silinen kişisel verinin yedeklerde kalacağı en uzun süre saklama-imha politikasında belirtilir, geri yüklemeden sonra silinmiş kayıtlar yeniden silinir.'),
     ]},
]


# ============================================================ A15 — panel / yönetici kullanıcı yönetimi (auth)
F_AUTH = [
    {'id': 'admin_user_mgmt', 'section': 'auth', 'after': 'mfa', 'type': 'multiselect',
     'label': 'Panel Kullanıcı ve Yetki Yönetimi', 'en': 'Admin / Panel User & Access Management', 'agents': [IAM, ACCGOV, SWE],
     'explanation': 'Yönetim paneli ve iç kullanıcı hesaplarının yaşam döngüsü ve yetki yönetimi: davetle hesap açma, hesap durumları, eş zamanlı oturum ve cihaz yönetimi, şüpheli giriş tespiti, yetki değişikliklerinin denetim kaydı, dönemsel gözden geçirme, sayfa / modül bazında yetki ve ayrılan personelin erişiminin kapatılması. Ziyaretçi (üye) hesapları Üyelik & Giriş bölümünde ayrıca yönetilir.',
     'scenario': 'Panele birden çok çalışan, ajans ya da dış danışman giriyorsa; personel değişimi oluyorsa ya da denetimde "kim, ne zaman, hangi yetkiyi aldı" sorusuna yanıt verilmesi gerekiyorsa.',
     'example': 'Panelde "Kullanıcılar" ekranı: Ayşe Y. — Editör — Aktif — 2 açık oturum (Chrome / macOS, Safari / iPhone) — "Oturumları kapat"; Mehmet K. — Muhasebe — Askıda; her satırda yetki değişiklik geçmişi.',
     'rule': 'Panel ve yönetici kullanıcılarının yönetiminde şu kurallar uygulanır: {labels}. Kullanıcı ve yetki işlemleri yalnız sunucuda, yetkili rolün izniyle yapılır; kullanıcı kendi yetkisini genişletemez; yönetici hesaplarında çok adımlı doğrulama MFA kararına ve Panel & Portal Mimarisi bölümündeki zorunlu önlemlere göre uygulanır.',
     'recommend': [{'field': 'rbac', 'map': {'true': ['page_module_perm', 'authz_audit', 'periodic_review']}},
                   {'field': 'company_size', 'map': {'medium': ['invite', 'statuses', 'offboarding', 'authz_audit'], 'large': ['invite', 'statuses', 'offboarding', 'authz_audit', 'periodic_review', 'internal_external'], 'group': ['invite', 'statuses', 'offboarding', 'authz_audit', 'periodic_review', 'internal_external']}}],
     'options': [
         o('invite', 'Davetle hesap açma', 'Panel hesapları açık kayıtla değil, yetkili bir yöneticinin gönderdiği süreli ve tek kullanımlık davet bağlantısıyla açılır; rol davet sırasında belirlenir.', 'Panele yalnız belirli kişilerin girmesi gereken bütün projeler.', 'Yönetici "Kullanıcı davet et" ile e-posta ve rol seçer; bağlantı 48 saat geçerlidir, kullanılınca geçersiz olur.',
           'Panel hesapları yalnız davetle açılır; davet bağlantısı tek kullanımlık ve süreli (ör. 48 saat) olur, davet edilen rol sunucuda davetle eşleştirilir ve davet gönderme / kabul denetim kaydına yazılır.'),
         o('statuses', 'Hesap durumları: aktif, pasif, askıda, silinmiş', 'Hesabın yaşam döngüsü durumlarla yönetilir: aktif (giriş yapabilir), pasif (geçici olarak kapalı), askıda (inceleme ya da ihlal nedeniyle kilitli), silinmiş (erişim yok, kayıt saklama süresince tutulur).', 'Personel izne çıkan, geçici olarak erişimi kapatılan ya da incelemeye alınan hesapların olduğu projeler.', 'Şüpheli işlem fark edilince hesap "Askıda" yapılır; kullanıcının bütün oturumları kapanır ve giriş ekranında "Hesabınız askıya alındı" görünür.',
           'Hesap durumları aktif, pasif, askıda ve silinmiş olarak tanımlanır; aktif dışındaki her durumda giriş ve API erişimi reddedilir, durum değişikliğinde açık oturumlar ve jetonlar hemen iptal edilir; silinen hesabın kayıtları denetim kaydı ve saklama süresince anonimleştirilmeden tutulur.'),
         o('sessions', 'Eş zamanlı oturum ve cihaz yönetimi', 'Kullanıcının hangi cihazlarda açık oturumu olduğunun görülmesi, oturum geçmişi, eş zamanlı oturum sınırı ve tek tek ya da toplu oturum kapatma.', 'Panele farklı cihazlardan girilen, ortak bilgisayar kullanılan ya da hesap paylaşımının engellenmesi gereken projeler.', 'Kullanıcı profilinde "Açık oturumlar: 3 — Windows / Edge, İstanbul, 2 saat önce …" listesi ve "Diğer bütün oturumları kapat" düğmesi bulunur.',
           'Her kullanıcının açık oturumları ve oturum geçmişi (cihaz, tarayıcı, yaklaşık konum, zaman) kullanıcıya ve yetkili yöneticiye gösterilir; eş zamanlı oturum sınırı tanımlanır, tek oturum ya da bütün oturumlar sunucu tarafında kapatılabilir.'),
         o('suspicious', 'Şüpheli giriş tespiti ve oturumun sonlandırılması', 'Olağan dışı konum, yeni cihaz, kısa sürede çok sayıda başarısız deneme ya da imkânsız seyahat gibi işaretlerde ek doğrulama istenmesi, uyarı verilmesi ve gerekirse oturumun otomatik kapatılması.', 'Yönetici hesaplarının ele geçirilmesinin ciddi zarar yaratacağı projeler.', 'Aynı hesap 10 dakika arayla İstanbul ve Amsterdam\'dan girince ikinci oturum yeniden doğrulama ister, güvenlik ekibine uyarı gider.',
           'Yeni cihaz, olağan dışı konum, art arda başarısız deneme ve aynı anda uzak konumlardan oturum gibi işaretler kural tabanlı olarak değerlendirilir; şüpheli durumda yeniden doğrulama istenir, gerekirse oturum sonlandırılır, kullanıcıya ve güvenlik sorumlusuna bildirim gider; kararlar kişisel veri içermeyen biçimde loglanır.'),
         o('authz_audit', 'Yetki değişikliklerinin denetim kaydı', 'Rol atama, rol kaldırma, yetki genişletme ve hesap durumu değişikliklerinin kim, ne zaman, kime, eski ve yeni değerle kaydedilmesidir.', 'Denetime tabi kurumlar ve birden çok yöneticinin olduğu paneller.', 'Kayıt: "12.11.2026 14:05 — Ali T. (Yönetici) — Zeynep A.\'ya Finans rolü verdi — gerekçe: görev değişikliği".',
           'Kullanıcı açma, durum değişikliği, rol ve yetki değişiklikleri; yapan kişi, hedef kullanıcı, eski / yeni değer, zaman ve gerekçeyle yalnız eklenebilir (append-only) denetim kaydına yazılır; bu kayıt panelden silinemez ve düzenlenemez.'),
         o('periodic_review', 'Dönemsel yetki gözden geçirmesi', 'Kullanıcı listesinin ve verilen yetkilerin belirli aralıklarla birim yöneticilerine onaylatılması; gereksiz yetkilerin kaldırılmasıdır.', 'Personel değişiminin sık olduğu, iç / dış denetime tabi kurumlar.', 'Üç ayda bir her birim yöneticisine "Ekibinizin panel yetkileri" listesi gider; onaylanmayan yetkiler 15 gün sonra otomatik kaldırılır.',
           'Panel kullanıcıları ve yetkileri en az üç ayda bir gözden geçirilir; 90 gün kullanılmayan hesaplar pasifleştirilir, gereksiz yetkiler kaldırılır ve gözden geçirme sonucu kayda alınır.'),
         o('page_module_perm', 'Sayfa ve modül bazında yetki', 'Rol bazlı yetkinin modül (Blog, Siparişler, Kullanıcılar) ve gerektiğinde tek tek sayfa / içerik düzeyinde görüntüle, düzenle, yayınla, sil gibi izinlere ayrılmasıdır.', 'Farklı ekiplerin panelin farklı bölümlerini yönettiği projeler.', 'Ürün editörü yalnız "Ürünler" modülünü görür; "Kurumsal" sayfalarını düzenleme yetkisi yalnız kurumsal iletişim rolündedir.',
           'Yetkiler modül ve işlem düzeyinde (görüntüle, oluştur, düzenle, yayınla, sil, dışa aktar) tanımlanır; gerektiğinde sayfa / içerik düzeyinde kısıt eklenir; menüde görünmeyen modülün API\'si de sunucuda aynı yetkiyle korunur.'),
         o('internal_external', 'İç ve dış kullanıcı ayrımı', 'Çalışanlar ile ajans, danışman, bayi gibi dış kullanıcıların ayrı rol gruplarında, süreli erişimle ve daha dar yetkiyle yönetilmesidir.', 'Panele ajans, serbest çalışan ya da iş ortağı erişimi verilen projeler.', 'Ajans kullanıcısı "Dış — Pazarlama Ajansı" etiketiyle görünür; erişimi sözleşme bitiş tarihinde kendiliğinden kapanır, kullanıcı verisini dışa aktaramaz.',
           'Dış kullanıcılar ayrı rol grubunda tutulur; erişimleri bitiş tarihli verilir, kişisel veri dışa aktarma ve kullanıcı yönetimi yetkisi verilmez; dış kullanıcı erişimi ayrı raporlanır.'),
         o('offboarding', 'Ayrılan personelin erişiminin aynı gün kapatılması', 'Görevden ayrılan ya da görevi değişen kişinin panel, API anahtarı ve bağlı hesaplarının ayrılış günü kapatılmasıdır.', 'Personel değişimi olan bütün kurumlar.', 'İK "çıkış" kaydını girince kişinin panel hesabı pasifleşir, oturumları kapanır, adına açılmış API anahtarları iptal edilir.',
           'Ayrılan personelin hesabı ayrılış günü pasifleştirilir, bütün oturumları ve jetonları iptal edilir, adına oluşturulan API anahtarları ve paylaşılan gizli bilgiler yenilenir; sahip olduğu içerik ve işler başka bir kullanıcıya devredilir.'),
     ]},
]


# ============================================================ A16–A18 — gizlilik, KVKK, çerez ve hukuki metinler (privacy)
F_PRIV = [
    {'id': 'cookie_behavior', 'section': 'privacy', 'after': 'cookie_manager', 'type': 'multiselect',
     'label': 'Çerez İzin Davranışı', 'en': 'Cookie Consent Behavior', 'agents': [KVKK, PRIVENG, SWE], 'showIf': CMP_ON,
     'explanation': 'Seçilen çerez / onay platformunun nasıl davranacağını belirler: çerez kategorileri, onay gelmeden zorunlu olmayan script ve etiketlerin yüklenmemesi, Kabul Et / Reddet / Tercihler düğmelerinin eşit görünürlüğü, rıza kaydı, tercihin sonradan değiştirilmesi, çerez envanteri ve onay modlarıyla eşitleme.',
     'scenario': 'Sitede analitik, reklam, harita, video, sohbet gibi zorunlu olmayan çerez ya da üçüncü taraf script kullanılıyorsa. KVKK Çerez Uygulamaları Rehberi kabul ve reddin eşit derecede sunulmasını iyi uygulama olarak gösterir.',
     'example': 'Siteye ilk girişte alt bantta aynı renk ve boyutta "Kabul Et", "Reddet", "Tercihleri Yönet" düğmeleri çıkar; ret seçilince Google Analytics ve Meta Pikseli hiç yüklenmez, sol alttaki çerez simgesiyle tercih sonradan değiştirilebilir.',
     'rule': 'Çerez izin davranışı: {labels}. Zorunlu olmayan hiçbir çerez, script, piksel ya da etiket rıza alınmadan yüklenmez ve tetiklenmez; rıza sunucu tarafında da kayıt altına alınır. Google ve Meta onay modu ayarları Analitik › Onay Modu, Google Servisleri › Onay Modu ve Meta Servisleri › Rıza kararlarıyla uyumlu tutulur.',
     'recommend': {'field': 'cookie_manager', 'map': {'CookieYes': ['categories', 'default_deny', 'equal_buttons', 'consent_log', 'revisit'], 'Cookiebot': ['categories', 'default_deny', 'equal_buttons', 'consent_log', 'revisit'], 'Usercentrics': ['categories', 'default_deny', 'equal_buttons', 'consent_log', 'revisit'], 'Custom': ['categories', 'default_deny', 'equal_buttons', 'consent_log', 'revisit', 'inventory']}},
     'options': [
         o('categories', 'Kategori yönetimi: zorunlu, işlevsel, analitik, pazarlama', 'Çerezler amaçlarına göre kategorilere ayrılır; zorunlu kategori dışındakiler ayrı ayrı açılıp kapatılabilir ve her kategorinin açıklaması vardır.', 'Birden çok amaçla çerez kullanan bütün siteler.', '"Tercihleri Yönet" penceresinde dört satır: Zorunlu (her zaman açık), İşlevsel, Analitik, Pazarlama — her birinin altında kısa açıklama ve çerez listesi.',
           'Çerezler zorunlu, işlevsel, analitik ve pazarlama kategorilerinde tanımlanır; zorunlu çerezler pazarlama amacıyla kullanılmaz, diğer kategoriler için ayrı ayrı rıza alınır ve her kategorinin açıklaması merkezi olarak yönetilir.'),
         o('default_deny', 'Varsayılan reddet: rızadan önce zorunlu olmayan script yüklenmez', 'Ziyaretçi seçim yapmadan önce analitik, reklam ve diğer zorunlu olmayan script, piksel ve etiketler hiç yüklenmez; seçimden sonra yalnız izin verilen kategoriler çalışır.', 'Bütün projeler; KVKK açık rızası gerektiren çerezlerde rızanın önceden alınması gerekir.', 'İlk sayfa yüklemesinde ağ isteklerinde google-analytics.com ya da facebook.net görünmez; "Analitik" onaylanınca GA4 o anda yüklenir.',
           'Zorunlu olmayan script, piksel ve etiketler sayfaya doğrudan eklenmez; onay platformu ya da etiket yöneticisi üzerinden kategoriye bağlanarak yalnız ilgili rıza verilince yüklenir; rıza geri alınınca ilgili çerezler silinir ve script\'ler bir sonraki yüklemede çalışmaz.'),
         o('equal_buttons', 'Kabul Et / Reddet / Tercihleri Yönet eşit görünürlükte', 'İlk katmanda üç seçenek de aynı renk, boyut ve punto ile sunulur; ret, kabulden zor ya da gizli değildir.', 'Bütün projeler; KVKK Çerez Rehberi bunu iyi uygulama örneği olarak gösterir.', 'Bantta üç düğme yan yana ve aynı görünümdedir; "Reddet" bir alt menüye ya da küçük bir bağlantıya saklanmaz.',
           'İlk katmanda "Kabul Et", "Reddet" ve "Tercihleri Yönet" eşit renk, boyut ve vurguda sunulur; kapatma (X) düğmesi rıza sayılmaz, sayfada gezinmek rıza sayılmaz, onay kutuları önceden işaretli gelmez.'),
         o('consent_log', 'Rıza kaydı ve kanıt (zaman, metin sürümü, tercih)', 'Her rıza ya da ret kararının zamanı, kabul edilen kategoriler, gösterilen çerez politikası / aydınlatma metni sürümü ve tercih değişiklikleriyle kayıt altına alınmasıdır.', 'Rızanın ispat yükünün veri sorumlusunda olduğu bütün projeler.', 'Panelde "Rıza kayıtları" raporu: anonim ziyaretçi kimliği, 12.11.2026 10:14, Analitik: evet, Pazarlama: hayır, Çerez Politikası v3.2.',
           'Her rıza kararı için rastgele rıza kimliği, tarih-saat, kabul / ret edilen kategoriler, gösterilen metin sürümleri ve kaynak (banner, tercih paneli) sunucuda kaydedilir; IP adresi gerekiyorsa kısaltılarak tutulur; kayıtlar raporlanabilir ve saklama-imha politikasındaki süre sonunda silinir.'),
         o('revisit', 'Tercihi her an değiştirme (kalıcı bağlantı / simge)', 'Ziyaretçinin rızasını verdiği kadar kolay geri alabilmesi için alt bilgide "Çerez Tercihleri" bağlantısı ya da köşede kalıcı küçük bir simge bulunur.', 'Bütün projeler.', 'Sol alttaki çerez simgesine tıklanınca tercih paneli yeniden açılır; "Pazarlama" kapatılınca değişiklik anında uygulanır.',
           'Tercih paneli alt bilgideki bağlantıdan ve içeriği kapatmayan kalıcı bir simgeden her sayfada yeniden açılabilir; değişiklik sayfa yenilenmeden uygulanır ve kayıt altına alınır.'),
         o('inventory', 'Çerez ve script envanteri + düzenli tarama', 'Sitede kullanılan bütün çerezlerin ve üçüncü taraf script\'lerin adı, sağlayıcısı, amacı, kategorisi ve süresiyle listelenmesi ve sitenin düzenli olarak taranıp envanterin güncel tutulmasıdır.', 'Pazarlama ekibinin sık yeni etiket eklediği siteler.', 'Aylık tarama raporu: "Yeni çerez bulundu: _ttp (TikTok) — kategorisiz"; çerez politikasındaki tablo envanterden otomatik üretilir.',
           'Çerez ve script envanteri (ad, sağlayıcı, amaç, kategori, süre, birinci / üçüncü taraf) tutulur ve en az ayda bir otomatik taramayla güncellenir; kategorisi atanmamış yeni çerez ya da script yayına engel sayılır; çerez politikasındaki tablo envanterden üretilir.'),
         o('reprompt', 'Rıza süresi ve yeniden sorma', 'Verilen tercihin ne kadar süre geçerli olacağı ve ne zaman yeniden sorulacağıdır; her girişte sormak "rıza yorgunluğu" yaratır, tercih çerezin ömrüyle orantılı aralıklarla hatırlatılır.', 'Bütün projeler; çerez listesi ya da amaçları değiştiğinde ayrıca gerekir.', 'Tercih 6 ay saklanır; süre dolunca ya da çerez politikasına yeni bir pazarlama aracı eklenince banner yeniden gösterilir.',
           'Tercih makul bir süre saklanır ve bu süre sonunda ya da çerez kategorileri / amaçları / metin sürümü değiştiğinde yeniden sorulur; aynı ziyaretçiye her girişte rıza sorulmaz.'),
         o('signal_sync', 'Google ve Meta onay modlarıyla eşitleme', 'Onay platformundaki kategori kararlarının Google Consent Mode sinyallerine (ad_storage, analytics_storage, ad_user_data, ad_personalization) ve Meta Pikseli rıza durumuna aktarılmasıdır.', 'Google Analytics, Google Ads, Tag Manager ya da Meta Pikseli kullanılan siteler.', 'Ziyaretçi "Analitik: evet, Pazarlama: hayır" seçince analytics_storage granted, ad_storage ve ad_user_data denied gönderilir; Meta Pikseli hiç yüklenmez.',
           'Onay platformu kararları sayfa yüklenmeden önce varsayılan "denied" durumuyla Google onay moduna, ardından kullanıcı seçimine göre güncellemeyle aktarılır; Meta Pikseli rıza verilmeden yüklenmez; eşleme tablosu Google ve Meta Servisleri menülerindeki kararlarla aynı tutulur.'),
     ]},

    {'id': 'legal_texts', 'section': 'privacy', 'after': 'cookie_behavior', 'type': 'multiselect',
     'label': 'Yönetilecek Hukuki Metinler', 'en': 'Managed Legal Texts', 'agents': [LAWKVKK, KVKK, CONTRACT],
     'explanation': 'Sitede yayınlanacak ve yönetim panelinden merkezi olarak yönetilecek hukuki metinlerin listesidir. Metinler ilgili sayfa ve formlarda otomatik gösterilir; içerikleri hukuk biriminin onayından geçer.',
     'scenario': 'Kişisel veri toplayan form, üyelik, e-ticaret, ticari ileti ya da çerez kullanan her site. Metinlerin dağınık sayfalarda elle güncellenmesi sürüm karışıklığına yol açar.',
     'example': 'Panelde "Hukuki Metinler" modülü: Ziyaretçi Aydınlatma Metni v2.1 (yayında), Çerez Politikası v3.2, İletişim Formu Aydınlatma Metni v1.4, Mesafeli Satış Sözleşmesi v5.0; her birinin sürüm geçmişi ve yayın tarihi görünür.',
     'rule': 'Sitede ve panelde merkezi olarak yönetilecek hukuki metinler: {labels}. Metinler veritabanında sürümlü içerik olarak tutulur, ilgili sayfa, form ve ödeme adımlarında otomatik gösterilir, hukuk birimi onayı olmadan yayına alınmaz; Claude metinlerin hukuki içeriğini yazmaz, yalnız şablon ve yer tutucu üretir.',
     'recommend': [{'field': 'module_ecommerce', 'map': {'store': ['distance_sales', 'returns', 'terms']}},
                   {'field': 'member_mode', 'map': {m: ['terms', 'privacy_policy'] for m in MEMBERS}},
                   {'field': 'cookie_manager', 'map': {'CookieYes': ['cookie_policy'], 'Cookiebot': ['cookie_policy'], 'Usercentrics': ['cookie_policy'], 'Custom': ['cookie_policy'], 'Other': ['cookie_policy']}}],
     'options': [
         o('visitor_notice', 'Ziyaretçi aydınlatma metni', 'Sitenin ziyaretçilerden hangi kişisel verileri hangi amaç ve hukuki sebeple işlediğini anlatan, KVKK m. 10 kapsamındaki genel aydınlatma metni.', 'Kişisel veri işleyen her site.', 'Alt bilgide "Aydınlatma Metni" bağlantısı; sayfada veri sorumlusu, amaçlar, aktarılan taraflar ve haklar yazar.',
           'Ziyaretçi aydınlatma metni alt bilgide her sayfadan erişilebilir ve çerez banner\'ından bağlantı verilir; metin sürümlü yönetilir.'),
         o('form_notices', 'Forma özel aydınlatma metinleri', 'İletişim, teklif, başvuru, bülten gibi her formun topladığı veriye özgü kısa aydınlatma metinleri; form oluşturucuyla ilişkilendirilir.', 'Birden çok amaçla form kullanan siteler (iletişim, kariyer başvurusu, teklif isteme).', 'Kariyer başvuru formunun altında "Başvuru Formu Aydınlatma Metni" bağlantısı ve kısa özet görünür.',
           'Her form kendi aydınlatma metnine bağlanır ve form altında otomatik gösterilir; metni olmayan form yayına alınamaz.'),
         o('cookie_policy', 'Çerez politikası', 'Kullanılan çerezlerin kategori, amaç, sağlayıcı ve süreleriyle açıklandığı metin; çerez envanterinden üretilen tabloyla birlikte.', 'Çerez kullanan bütün siteler.', 'Çerez politikası sayfasında envanterden otomatik oluşan tablo ve banner\'dan doğrudan bağlantı vardır.',
           'Çerez politikası çerez envanteriyle eşlenir, tablo envanterden otomatik üretilir ve banner ile tercih panelinden erişilebilir.'),
         o('privacy_policy', 'Gizlilik politikası', 'Kurumun kişisel veri işleme, saklama, güvenlik ve paylaşım ilkelerini genel olarak anlatan metin (aydınlatma metninden ayrı, daha kapsamlı politika).', 'Üyelik, e-ticaret ya da uluslararası (GDPR) kapsamı olan projeler.', 'Alt bilgide "Gizlilik Politikası" sayfası; KVKK ve GDPR haklarının nasıl kullanılacağı anlatılır.',
           'Gizlilik politikası sürümlü yönetilir ve alt bilgiden erişilebilir; içerik aydınlatma metinleriyle çelişmeyecek biçimde hukuk biriminin onayıyla güncellenir.'),
         o('explicit_consent', 'Açık rıza metinleri', 'Kanundaki diğer işleme şartları yoksa ve açık rızaya dayanılacaksa, belirli konuya ilişkin, bilgilendirmeye dayalı ve özgür iradeyle alınan rıza metinleri; aydınlatma metninden ayrı sunulur.', 'Yurt dışına aktarım, özel nitelikli veri, profil çıkarma gibi açık rızaya dayanan işlemler varsa.', 'Formda aydınlatma metni bağlantısından ayrı, işaretsiz bir kutu: "Kişisel verilerimin … amacıyla yurt dışındaki sunuculara aktarılmasına açık rıza veriyorum."',
           'Açık rıza metinleri aydınlatma metninden ayrı sunulur, hizmet şartına bağlanmaz, her amaç için ayrı alınır ve geri alınabilir; açık rıza yalnız başka bir işleme şartı yoksa kullanılır.'),
         o('commercial_msg', 'Ticari elektronik ileti izni metni', '6563 sayılı Kanun kapsamında e-posta, SMS ve arama ile ticari ileti gönderimi için alınan onay metni; İleti Yönetim Sistemi (İYS) kaydıyla birlikte.', 'Bülten, kampanya e-postası ya da SMS gönderen projeler.', 'Kayıt formunda işaretsiz kutu: "Kampanya ve duyurulardan e-posta ve SMS ile haberdar olmak istiyorum."',
           'Ticari ileti izni ayrı ve işaretsiz bir kutuyla, kanal bazında alınır; izin kaydı İYS ile eşitlenir, ret hakkı her iletide kolayca kullanılabilir.'),
         o('dsr_form', 'İlgili kişi başvuru formu', 'KVKK m. 11\'deki hakların kullanılması için veri sorumlusuna başvuru formu ve başvuru yolları sayfası.', 'Kişisel veri işleyen bütün veri sorumluları.', '"KVKK Başvuru" sayfasında başvuru formu, KEP adresi ve posta adresi; form gönderilince başvuru numarası verilir.',
           'İlgili kişi başvuru formu ve başvuru yolları sayfası yayınlanır; form İlgili Kişi Başvuruları kararındaki süreç ve kayıt yapısına bağlanır.'),
         o('distance_sales', 'Mesafeli satış sözleşmesi ve ön bilgilendirme formu', 'Mesafeli Sözleşmeler Yönetmeliği kapsamında ürün / hizmet bazında özelleştirilebilen sözleşme ve sipariş öncesi ön bilgilendirme formu.', 'İnternetten tüketiciye satış yapan e-ticaret, abonelik, rezervasyon ve dijital ürün projeleri.', 'Ödeme adımında sipariş özetinin altında ön bilgilendirme formu ve sözleşme açılır; iki ayrı işaretsiz onay kutusu işaretlenmeden "Siparişi Onayla" etkinleşmez.',
           'Mesafeli satış sözleşmesi ve ön bilgilendirme formu ürün / hizmet türüne göre şablondan üretilir, sipariş bilgileriyle (satıcı, ürün, toplam fiyat, teslimat, cayma hakkı) doldurulur ve ödeme öncesinde gösterilir; tüketici ön bilgileri teyit etmeden ve siparişin ödeme yükümlülüğü doğurduğu açıkça bildirilmeden sipariş oluşturulmaz.'),
         o('terms', 'Kullanım koşulları / üyelik sözleşmesi', 'Sitenin ya da platformun kullanım kuralları, kullanıcı yükümlülükleri ve sorumluluk sınırları.', 'Üyelik, kullanıcı içeriği, pazar yeri ya da SaaS projeleri.', 'Kayıt formunda "Kullanım Koşulları\'nı okudum, kabul ediyorum" kutusu ve metnin sürüm numarası.',
           'Kullanım koşulları sürümlü yönetilir; kabul edilen sürüm kullanıcı kaydına bağlanır.'),
         o('returns', 'İade, iptal ve cayma politikası', 'İade, değişim, sipariş iptali ve cayma hakkının nasıl kullanılacağını anlatan politika ve cayma formu.', 'Ürün ya da hizmet satışı yapan projeler.', '"İade ve Cayma" sayfasında süreler, istisnalar, adımlar ve indirilebilir cayma formu bulunur.',
           'İade, iptal ve cayma politikası ile cayma formu yayınlanır, sözleşme ve ön bilgilendirme formuyla tutarlı tutulur; sitede cayma talebi alınıyorsa talebin ulaştığına dair teyit tüketiciye hemen iletilir.'),
     ]},

    {'id': 'legal_versioning', 'section': 'privacy', 'after': 'legal_texts', 'type': 'multiselect',
     'label': 'Hukuki Metin Sürümleme ve Onay Kaydı', 'en': 'Legal Text Versioning & Consent Records', 'agents': [SWE, KVKK, CONTRACT],
     'explanation': 'Hukuki metinlerin sürümlenmesi, kullanıcıya gösterilen sürümün ve verilen onayların kayıt altına alınması, sipariş anındaki sözleşmenin saklanması ve metin değişince yeniden onay alınmasıyla ilgili teknik kurallardır.',
     'scenario': 'Formda onay, üyelikte koşul kabulü ya da siparişte sözleşme onayı alınan projeler; ileride "kullanıcı hangi metni onayladı" sorusuna kanıtla yanıt vermek gerekir.',
     'example': 'Sipariş kaydında: "Mesafeli Satış Sözleşmesi v5.0 — onay 12.11.2026 15:32:08 — IP 85.105.x.x — PDF: siparis-10482-sozlesme.pdf"; PDF siparişle birlikte e-postayla gönderilmiştir.',
     'rule': 'Hukuki metin sürümleme ve onay kaydı: {labels}. Onay kayıtları yalnız eklenebilir biçimde tutulur, panelden düzenlenemez; onay kaydındaki kişisel veriler saklama-imha politikasındaki süre boyunca saklanır.',
     'options': [
         o('versioning', 'Metin sürümleme ve geçmiş', 'Her hukuki metnin sürüm numarası, yayın tarihi, değişiklik özeti ve önceki sürümleriyle saklanması; eski sürüm silinmez, arşivlenir.', 'Hukuki metni olan bütün projeler.', 'Çerez Politikası sayfasının altında "Sürüm 3.2 — Yürürlük: 01.10.2026 — Önceki sürümler" bağlantısı.',
           'Hukuki metinler değiştirilemez sürümler olarak saklanır; yeni sürüm yeni kayıt açar, yayındaki sürüm ve geçmiş sürümler tarih ve değişiklik özetiyle listelenir.'),
         o('shown_version', 'Kullanıcıya gösterilen sürümün kaydı', 'Bir formda, banner\'da ya da ödeme adımında kullanıcıya hangi metin sürümünün gösterildiğinin işlemle birlikte kaydedilmesidir.', 'Aydınlatma yükümlülüğünün yerine getirildiğinin ispatı gereken projeler.', 'İletişim formu kaydında "Aydınlatma Metni gösterildi: İletişim v1.4" alanı bulunur.',
           'Her form gönderimi, rıza ve sipariş kaydı, o anda gösterilen metinlerin sürüm kimliklerini içerir.'),
         o('unchecked_boxes', 'Onay kutuları ayrı, zorunlu ve önceden işaretsiz', 'Her onay (sözleşme, açık rıza, ticari ileti) ayrı kutuyla alınır; kutular önceden işaretli gelmez; yalnız işlem için gerçekten gerekli olanlar zorunludur.', 'Form, üyelik ve sipariş alan bütün projeler.', 'Ödeme sayfasında "Ön bilgilendirme formunu okudum" ve "Mesafeli satış sözleşmesini onaylıyorum" zorunlu, "Kampanya iletileri almak istiyorum" isteğe bağlı ve işaretsizdir.',
           'Onay kutuları önceden işaretli gelmez ve her amaç için ayrıdır; zorunlu onaylar sunucuda da denetlenir (istemci tarafı atlatılsa da işlem reddedilir); ticari ileti ve açık rıza hizmetin ön şartı yapılmaz.'),
         o('consent_record', 'Onay kaydı: kim, ne zaman, hangi sürüm, hangi form, IP', 'Her onayın kullanıcı / ziyaretçi kimliği, tarih-saat, metin sürümü, alındığı form ya da adım ve IP adresiyle kayıt altına alınmasıdır.', 'Onayın ispat yükünün veri sorumlusunda olduğu bütün projeler.', 'Panelde "Onay kayıtları" raporu üye ya da sipariş numarasıyla aranabilir ve dışa aktarılabilir.',
           'Her onay; kullanıcı ya da kayıt kimliği, tarih-saat (UTC), metin türü ve sürümü, kaynak form / adım, IP adresi ve kullanıcı ajanı ile yalnız eklenebilir bir tabloya yazılır; onayın geri alınması da yeni kayıt olarak eklenir.'),
         o('order_snapshot', 'Sipariş anındaki sözleşmenin siparişe bağlanması, PDF ve e-posta ile iletilmesi', 'Onaylanan sözleşme ve ön bilgilendirme formunun sipariş bilgileriyle doldurulmuş hâlinin siparişe bağlı olarak saklanması, PDF olarak indirilebilmesi ve e-postayla gönderilmesidir.', 'E-ticaret ve mesafeli satış yapan projeler.', 'Hesabım › Siparişlerim › #10482 ekranında "Sözleşmeyi indir (PDF)" düğmesi; aynı PDF sipariş onay e-postasının ekindedir.',
           'Sipariş onayında sözleşme ve ön bilgilendirme formunun doldurulmuş hâli değiştirilemez biçimde (sürüm kimliği ve içerik özeti / hash ile) siparişe bağlanır, PDF olarak üretilir, tüketiciye e-postayla gönderilir ve hesabından indirilebilir; Mesafeli Sözleşmeler Yönetmeliği\'ndeki saklama süresi (işleme ilişkin bilgi ve belgeler için üç yıl) hukuk biriminin teyidiyle uygulanır.'),
         o('reconsent', 'Metin değişince yeniden onay', 'Sözleşme ya da kullanım koşullarının esaslı değişikliğinde mevcut kullanıcılardan yeni sürüm için tekrar onay alınmasıdır; eski sürüm arşivde kalır.', 'Üyelik ve abonelik projeleri.', 'Kullanım koşulları v4 yayınlanınca üye bir sonraki girişte değişiklik özetini görür ve "Kabul ediyorum" demeden devam edemez.',
           'Esaslı değişiklik olarak işaretlenen yeni sürüm yayınlanınca ilgili kullanıcılardan bir sonraki işlemde yeniden onay istenir; yeni onay alınana kadar eski sürümün kaydı geçerli kalır; değişiklik özeti kullanıcıya gösterilir.'),
         o('form_binding', 'Form oluşturucu entegrasyonu', 'Form oluşturucuda her forma bağlanacak aydınlatma metni, onay kutuları ve zorunluluk durumu seçilir; metin formda otomatik gösterilir.', 'Panelden form oluşturulan projeler.', 'Form düzenleyicide "Hukuki metinler" sekmesi: Aydınlatma: Teklif Formu v1.2; Onay: Ticari ileti (isteğe bağlı).',
           'Form oluşturucu her forma aydınlatma metni ve onay kutularını bağlamayı zorunlu tutar; formda gösterilen metin sürümü form yanıtıyla birlikte kaydedilir.'),
         o('multilang', 'Çok dilli hukuki metin', 'Sitenin desteklediği her dil için hukuki metinlerin ayrı sürümlenmesi ve kullanıcının dilinde gösterilmesidir; çeviri hukuk onayından geçer.', 'Birden çok dilde yayın yapan ya da yurt dışına satış yapan projeler.', 'İngilizce sayfada Cookie Policy v3.2-en gösterilir; onay kaydında dil kodu da tutulur.',
           'Her dil sürümü ayrı onaylanır ve sürümlenir; kullanıcı hangi dildeki metni onayladıysa o dil ve sürüm kaydedilir; çevirisi onaylanmamış dilde Türkçe metin gösterilir.'),
     ]},

    {'id': 'privacy_inventory', 'section': 'privacy', 'after': 'legal_versioning', 'type': 'multiselect',
     'label': 'Kişisel Veri Envanteri ve Uyum Kayıtları', 'en': 'Personal Data Inventory & Compliance Records', 'agents': [INV, KVKK, LAWDOC],
     'explanation': 'Sitede ve panelde işlenen kişisel verilerin envanterinin (veri kategorisi, amaç, hukuki sebep, saklama süresi, imha yöntemi, aktarılan taraflar) oluşturulması ve bununla bağlantılı uyum kayıtlarıdır.',
     'scenario': 'Kişisel veri işleyen her proje; envanter, saklama-imha politikasının, aydınlatma metinlerinin ve ihlal değerlendirmesinin temelidir.',
     'example': 'Envanter satırı: "Sipariş — Müşteri — Kimlik, İletişim, Müşteri İşlem — Amaç: siparişin ifası — Hukuki sebep: sözleşmenin ifası (m. 5/2-c) — Saklama: 10 yıl — Alıcı: kargo firması — Yurt dışı: yok".',
     'rule': 'Kişisel veri envanteri ve uyum kayıtları: {labels}. Yeni bir form, tablo, entegrasyon ya da üçüncü taraf servis eklendiğinde envanter aynı değişiklikte güncellenir; veritabanı şemasında kişisel veri alanları işaretlenir.',
     'options': [
         o('inventory', 'Kişisel veri envanteri', 'Her veri kategorisi için işleme amacı, hukuki sebep, ilgili kişi grubu, saklama süresi, imha yöntemi, alıcılar ve güvenlik önlemlerinin listelendiği envanter.', 'Kişisel veri işleyen bütün projeler.', 'Depoda "docs/kvkk/veri-envanteri" tablosu; her form ve veritabanı tablosu bir envanter satırına bağlanır.',
           'Kişisel veri envanteri her veri kategorisi için amaç, hukuki sebep, ilgili kişi grubu, saklama süresi, imha yöntemi, alıcı grupları, yurt dışı aktarım ve güvenlik önlemlerini içerir; kod tabanındaki kişisel veri alanları envanterdeki satırlara eşlenir.'),
         o('explicit_flag', 'Açık rıza gerektiren işlemlerin ayrı işaretlenmesi', 'Envanterde hukuki sebebi açık rıza olan işlemler ayrı işaretlenir; rıza geri alınınca o işlemin durdurulacağı yer belli olur.', 'Pazarlama, profil çıkarma, yurt dışı aktarım gibi rızaya dayanan işlemler varsa.', 'Envanterde "Kişiselleştirilmiş reklam — hukuki sebep: açık rıza ⚑" satırı; rıza geri alınınca ilgili segmentten çıkarma işi tetiklenir.',
           'Açık rızaya dayanan işlemler envanterde ve kodda ayrı işaretlenir; rıza durumu işlem öncesinde sunucuda denetlenir, rıza geri alınınca işlem durdurulur.'),
         o('transfers', 'Üçüncü taraf ve yurt dışı aktarım kaydı', 'Kişisel verinin paylaşıldığı servislerin (e-posta, SMS, analitik, ödeme, barındırma, CRM) ve yurt dışına aktarımların hangi veriyle, hangi amaç ve dayanakla yapıldığının kaydıdır.', 'Bulut servisleri, yurt dışı merkezli araçlar ya da iş ortaklarıyla veri paylaşan projeler.', 'Aktarım kaydı: "E-posta servisi — ad, e-posta — bülten gönderimi — sunucu: AB — dayanak: standart sözleşme (Kurul\'a bildirildi)".',
           'Kişisel veri paylaşılan her üçüncü taraf ve yurt dışı aktarım; alıcı, veri kategorileri, amaç, konum ve hukuki dayanakla kaydedilir; yeni entegrasyon bu kayıt ve hukuk birimi değerlendirmesi olmadan canlıya alınmaz; yurt dışı aktarımda KVKK m. 9\'daki yöntemler hukuk biriminin teyidiyle uygulanır.'),
         o('verbis_check', 'VERBİS kayıt yükümlülüğü kontrolü', 'Veri sorumlusunun Veri Sorumluları Sicili\'ne (VERBİS) kayıt yükümlüsü olup olmadığının Kurul\'un istisna kararlarına göre kontrol edilmesi; yükümlüyse kaydın envanterle tutarlı tutulmasıdır.', 'Kurum ilk kez dijital hizmet başlatıyor ya da çalışan sayısı / ciro değişiyorsa.', 'Uyum kontrol listesinde "VERBİS: yükümlü — kayıt güncel (son güncelleme 02.09.2026)" satırı.',
           'Veri sorumlusunun VERBİS kayıt yükümlülüğü Kurul\'un güncel istisna kararlarına göre hukuk birimince kontrol edilir; yükümlüyse yeni işleme amaçları ve veri kategorileri sicil kaydına yansıtılır (Claude yalnız kontrol listesini hazırlar, kayıt kararını vermez).'),
         o('dpa', 'Veri işleyen sözleşmeleri', 'Veriyi veri sorumlusu adına işleyen hizmet sağlayıcılarla (barındırma, e-posta, çağrı merkezi, yazılım bakımı) güvenlik yükümlülüklerini, ihlal bildirimini ve veri iadesini düzenleyen sözleşmeler.', 'Dış hizmet sağlayıcı kullanan bütün projeler.', 'Tedarikçi listesinde her servis için "Veri işleyen sözleşmesi: imzalı / tarih" sütunu.',
           'Kişisel veriye erişen her hizmet sağlayıcıyla veri işleyen sözleşmesi bulunur; sözleşmede güvenlik önlemleri, alt işleyen kullanımı, ihlalin gecikmeksizin bildirimi ve sözleşme sonunda verinin iadesi / imhası yer alır.'),
         o('special_data', 'Özel nitelikli kişisel veriye ek önlem', 'Sağlık, biyometrik, din, ceza mahkûmiyeti gibi özel nitelikli kişisel veriler için ayrı işleme şartı ve ek güvenlik önlemleridir.', 'Sağlık, sigorta, insan kaynakları, eğitim ya da biyometrik doğrulama içeren projeler.', 'Hasta formundaki sağlık bilgileri ayrı şifrelenmiş alanda tutulur; yalnız "Sağlık Personeli" rolü görebilir, her erişim loglanır.',
           'Özel nitelikli kişisel veriler envanterde ayrıca işaretlenir; alan düzeyinde şifreleme, ayrı erişim rolü, erişim kaydı ve maskeleme uygulanır; mümkünse toplanmaz, toplanıyorsa işleme şartı hukuk biriminin teyidiyle belirlenir.'),
     ]},

    {'id': 'privacy_retention', 'section': 'privacy', 'after': 'privacy_inventory', 'type': 'select',
     'label': 'Saklama Süresi Dolan Verilerin İmhası', 'en': 'Retention & Disposal of Expired Data', 'agents': [RET, KVKK, SWE],
     'explanation': 'Saklama süresi dolan ya da işleme şartı ortadan kalkan kişisel verilerin silme, yok etme, anonimleştirme ya da arşivleme yoluyla nasıl ortadan kaldırılacağıdır. Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi Hakkında Yönetmelik\'e göre saklama ve imha politikası hazırlamış veri sorumlusu periyodik imha yapar ve periyodik imha aralığı altı ayı geçemez.',
     'scenario': 'Form başvuruları, eski siparişler, pasif üyeler, loglar ve yedekler gibi zamanla biriken kişisel verisi olan bütün projeler.',
     'example': 'Her 1 Ocak ve 1 Temmuz\'da otomatik iş çalışır: süresi dolan 1.240 iletişim formu kaydı silinir, 3 yılı dolan pasif üyelerin siparişleri anonimleştirilir; imha tutanağı panelde raporlanır.',
     'rule': 'Saklama süresi dolan kişisel veriler için yaklaşım: {label}. Her veri kategorisinin saklama süresi kişisel veri envanterinden gelir; imha işlemleri kayıt altına alınır ve imha kayıtları en az üç yıl saklanır.',
     'options': [
         o('periodic_auto', 'Saklama-imha politikası + otomatik periyodik imha (en çok 6 ayda bir) (önerilen)', 'Saklama süreleri politikada yazılır; zamanlanmış bir iş, süresi dolan kayıtları en çok altı ayda bir otomatik olarak siler ya da anonimleştirir ve tutanak üretir.', 'VERBİS kayıt yükümlüsü veri sorumluları ve düzenli kişisel veri biriktiren bütün projeler.', 'Arka plan işleri listesinde "Periyodik imha — her 6 ayda bir — son çalışma 01.07.2026 — 1.240 kayıt silindi" satırı.',
           'Kişisel veri saklama ve imha politikası hazırlanır; periyodik imha işi en çok altı ayda bir otomatik çalışır, süresi dolan kayıtları envanterdeki yönteme göre siler ya da anonimleştirir, imha tutanağı üretir; işlem idempotent ve tekrar çalıştırılabilir tasarlanır, yedeklerdeki kopyalar yedek saklama süresi dolunca düşer.'),
         o('anonymize', 'Anonimleştirerek istatistik için saklama', 'Süresi dolan kayıtlar silinmek yerine kimseyle ilişkilendirilemeyecek biçimde anonimleştirilir; toplu istatistik ve raporlama için kullanılmaya devam eder.', 'Satış, kullanım ya da talep istatistiklerinin uzun dönem korunması gereken projeler.', '3 yılı dolan siparişlerde ad, e-posta, telefon ve adres silinir; il, ürün, tutar ve tarih istatistik tablosunda kalır.',
           'Anonimleştirmede doğrudan tanımlayıcılar silinir, dolaylı tanımlayıcılar (tam tarih, posta kodu, nadir değer) genelleştirilir; takma ad (pseudonymization) anonimleştirme sayılmaz; anonim veri ile kaynak kayıt arasında geri dönüş anahtarı tutulmaz.'),
         o('archive', 'Yasal saklama süresince kısıtlı arşiv, süre sonunda imha', 'Vergi, ticaret ya da tüketici mevzuatı gereği saklanması gereken kayıtlar, işleme amacı bitince erişimi kısıtlı bir arşive taşınır; yasal süre dolunca imha edilir.', 'Fatura, sözleşme ve sipariş kaydı tutan e-ticaret ve kurumsal projeler.', 'Hesabını silen üyenin faturaları "Yasal arşiv" bölümüne taşınır; yalnız muhasebe rolü görebilir, 10 yıl sonra otomatik silinir.',
           'Yasal saklama yükümlülüğü olan kayıtlar canlı tablolardan ayrı, erişimi yalnız yetkili rollerle sınırlı ve her erişimi loglanan arşive taşınır; arşivdeki kayıtlar yalnız yasal amaçla kullanılır ve süre sonunda periyodik imhaya girer.'),
         o('manual', 'Kontrol listesiyle elle imha (küçük veri sorumlusu)', 'Saklama ve imha politikası hazırlama yükümlülüğü olmayan küçük veri sorumluları için; Yönetmelik, imha yükümlülüğünün doğduğu tarihi takip eden üç ay içinde silme / yok etme / anonimleştirme öngörür.', 'Az sayıda form kaydı olan, VERBİS yükümlüsü olmayan küçük işletme siteleri.', 'Panelde "İmha bekleyen kayıtlar" listesi; yönetici her üç ayda bir listeyi gözden geçirip "Seçilenleri kalıcı sil" der.',
           'Süresi dolan kayıtlar panelde listelenir ve yükümlülüğün doğduğu tarihten itibaren en geç üç ay içinde elle silinir; silme işlemleri kayıt altına alınır, liste boş değilse panel uyarı gösterir.'),
     ]},

    {'id': 'privacy_rights', 'section': 'privacy', 'after': 'privacy_retention', 'type': 'multiselect',
     'label': 'İlgili Kişi Başvuruları ve Haklar', 'en': 'Data Subject Requests & Rights', 'agents': [APPL, KVKK, SWE],
     'explanation': 'KVKK m. 11\'deki hakların (bilgi talep etme, düzeltme, silme, itiraz vb.) kullanılması için başvuru kanalları, kimlik doğrulama, yanıt süresi takibi ve başvuru kaydıdır. KVKK m. 13\'e göre başvurular en kısa sürede ve en geç otuz gün içinde, kural olarak ücretsiz sonuçlandırılır.',
     'scenario': 'Kişisel veri işleyen bütün projeler; üyelik ve e-ticaret projelerinde başvuru sayısı yüksek olur.',
     'example': 'Başvuru panelinde: "#KVKK-2026-0142 — Silme talebi — kimlik doğrulandı — kalan süre: 12 gün — sorumlu: Uyum Ekibi"; süre dolmadan 5 gün önce sorumluya hatırlatma gider.',
     'rule': 'İlgili kişi başvuruları: {labels}. Başvurular ve yanıtları kişisel veri içerdiği için erişimi yetkili rollerle sınırlı tutulur; hesap silme ve veri indirme gibi üye işlemleri Üyelik & Giriş bölümündeki kararlarla tutarlı uygulanır.',
     'recommend': [{'field': 'privacy_regime', 'map': {'GDPR': ['portability']}},
                   {'field': 'member_mode', 'map': {m: ['self_service'] for m in MEMBERS}}],
     'options': [
         o('channels', 'Başvuru kanalları (form, KEP, e-posta, posta)', 'İlgili kişinin başvurusunu iletebileceği yolların sitede açıkça yazılması ve dijital başvuru formunun sunulmasıdır; kanallar Kurul\'un başvuru usul ve esaslarına ilişkin düzenlemesine göre belirlenir.', 'Bütün veri sorumluları.', '"KVKK Başvuru" sayfasında: çevrim içi form, KEP adresi, kayıtlı e-posta ile başvuru ve posta adresi.',
           'Başvuru kanalları (çevrim içi form, KEP, sistemde kayıtlı e-posta adresi, yazılı başvuru) KVKK Başvuru sayfasında yazılır; bütün kanallardan gelen başvurular tek kayıt sistemine girilir. Kabul edilen kanallar hukuk biriminin teyidiyle güncel Tebliğ\'e göre belirlenir.'),
         o('identity', 'Başvuruda kimlik doğrulama', 'Başvurunun gerçekten ilgili kişiden geldiğinin, gereğinden fazla veri istemeden doğrulanmasıdır; yanlış kişiye veri vermek veri ihlalidir.', 'Bütün projeler; özellikle erişim ve silme taleplerinde.', 'Üye, hesabına girerek başvurursa ek belge istenmez; üye olmayan kişiye kayıtlı e-postasına doğrulama bağlantısı gönderilir.',
           'Başvuru sahibinin kimliği başvurunun niteliğine uygun, en az veriyle doğrulanır (oturum açmış üye, kayıtlı e-postaya doğrulama bağlantısı vb.); doğrulama için istenen belgeler yalnız bu amaçla kullanılır ve süre sonunda silinir.'),
         o('sla30', '30 gün yanıt süresi takibi', 'Her başvurunun alındığı tarih, son yanıt tarihi (en geç 30 gün) ve kalan sürenin izlenmesi, süre yaklaşınca sorumluya hatırlatma yapılmasıdır.', 'Bütün veri sorumluları; KVKK m. 13 yanıt süresini bağlayıcı olarak belirler.', 'Başvuru listesinde "kalan gün" sütunu; 5 gün kalanlar turuncu, süresi geçenler kırmızı görünür.',
           'Her başvuruya alındığı tarihten itibaren en geç 30 günlük son yanıt tarihi atanır; süre sonuna yaklaşınca sorumluya ve yöneticisine hatırlatma gider; yanıt kabul ya da gerekçeli ret olarak yazılı veya elektronik ortamda iletilir.'),
         o('rights_set', 'Erişim, düzeltme, silme ve itiraz talepleri', 'KVKK m. 11\'deki hakların her biri için işlem adımları: verinin işlenip işlenmediğini öğrenme ve bilgi talep etme, düzeltme, silme / yok etme, aktarılan üçüncü kişilere bildirim, otomatik analiz sonucuna itiraz.', 'Bütün veri sorumluları.', 'Panelde başvuru türü "Düzeltme" seçilince ilgili üye kaydı açılır; düzeltme yapılınca veri aktarılan servislere de güncelleme gönderilir.',
           'Her hak türü için panelde işlem adımı tanımlanır: kişiye ait verilerin dökümü, düzeltme, silme / anonimleştirme ve verinin aktarıldığı üçüncü kişilere bildirim; silme talebinde yasal saklama yükümlülüğü olan kayıtlar gerekçesiyle arşivde tutulur ve kişiye bildirilir.'),
         o('portability', 'Veri taşınabilirliği (GDPR kapsamındaysa)', 'GDPR m. 20 kapsamında kişinin sağladığı verileri yapılandırılmış, yaygın kullanılan ve makinece okunabilir biçimde alabilmesi; KVKK\'da ayrı bir taşınabilirlik hakkı yoktur.', 'AB\'deki kişilere hizmet veren ve GDPR kapsamına giren projeler.', 'GDPR başvurusunda kişiye profil, sipariş ve tercih verileri JSON ve CSV dosyası olarak süreli indirme bağlantısıyla verilir.',
           'GDPR kapsamındaki kişiler için kişinin sağladığı veriler makinece okunabilir biçimde (JSON / CSV) dışa aktarılır; dosya süreli ve kişiye özel bağlantıyla iletilir.'),
         o('register', 'Başvuru kaydı ve raporu', 'Bütün başvuruların tür, tarih, sonuç ve süreleriyle kayıt altına alınması ve dönemsel olarak raporlanmasıdır; Kurul incelemesinde kanıt sağlar.', 'Bütün veri sorumluları.', 'Üç aylık rapor: "42 başvuru — 30 silme, 8 erişim, 4 düzeltme — ortalama yanıt 9 gün — süresi geçen: 0".',
           'Başvurular tür, alınma ve yanıt tarihi, sonuç ve sorumlu ile kaydedilir; başvuru kayıtları en az yetkiyle erişilir ve dönemsel olarak raporlanır.'),
         o('self_service', 'Üyelerde self-servis veri indirme ve hesap silme', 'Üyenin başvuru yapmadan hesap panelinden verilerini indirebilmesi ve hesabını silebilmesidir; Üyelik & Giriş bölümündeki "Verilerimi indir", "Hesabımı sil" ve Hesap Silme kararlarıyla aynı işlemdir.', 'Üyelik sistemi olan projeler.', 'Hesabım › Gizlilik sayfasında "Verilerimi indir" ve "Hesabımı sil" düğmeleri; işlem başvuru kaydına otomatik eklenir.',
           'Self-servis veri indirme ve hesap silme işlemleri Üyelik & Giriş bölümündeki kararlara göre uygulanır ve otomatik olarak başvuru kaydına işlenir; işlem öncesi yeniden kimlik doğrulaması istenir.'),
     ]},

    {'id': 'privacy_breach', 'section': 'privacy', 'after': 'privacy_rights', 'type': 'multiselect',
     'label': 'Veri İhlali Müdahalesi ve Bildirim', 'en': 'Data Breach Response & Notification', 'agents': [BREACH, IR, LAWKVKK],
     'explanation': 'Kişisel verilerin kanuni olmayan yollarla başkalarınca elde edilmesi (veri ihlali) durumunda uygulanacak müdahale prosedürü, bildirimler ve kayıtlardır. Kurul\'un 24.01.2019 tarihli ve 2019/10 sayılı kararına göre ihlal, öğrenildiği tarihten itibaren gecikmeksizin ve en geç 72 saat içinde Kurul\'a, etkilenen kişiler belirlendikten sonra makul olan en kısa sürede ilgili kişilere bildirilir.',
     'scenario': 'Kişisel veri işleyen bütün projeler; ihlal anında kim ne yapacak sorusunun önceden yanıtlanmış olması gerekir.',
     'example': 'Hatalı bir API ayarı yüzünden müşteri adresleri dışarı açılır; olay müdahale planı devreye girer: erişim kapatılır, etki analiz edilir, 72 saat içinde Kurul\'a bildirim formu gönderilir, etkilenen 3.400 müşteriye e-posta atılır.',
     'rule': 'Veri ihlali müdahalesi ve bildirimi: {labels}. İhlal belirtisi (yetkisiz erişim, toplu dışa aktarma, sızıntı ihbarı) güvenlik izlemesinden olay müdahale sorumlusuna otomatik iletilir; inceleme sırasında kanıtlar (loglar) korunur, kişisel veri gereğinden fazla kopyalanmaz.',
     'options': [
         o('response_plan', 'Veri ihlali müdahale planı', 'İhlalde kime raporlama yapılacağı, kimin karar vereceği, bildirimlerin kim tarafından yapılacağı ve olası sonuçların nasıl değerlendirileceğini belirleyen, düzenli gözden geçirilen yazılı plan.', 'Bütün veri sorumluları; 2019/10 sayılı Kurul kararı böyle bir planın hazırlanmasını ve belirli aralıklarla gözden geçirilmesini öngörür.', 'Depoda "VERI-IHLALI-PLANI.md": iletişim listesi, ilk 1 saat / 24 saat / 72 saat adımları, karar yetkisi, şablonlar.',
           'Veri ihlali müdahale planı yazılı hazırlanır (sorumlular, iletişim zinciri, ilk müdahale, etki değerlendirmesi, bildirim kararı, iletişim şablonları) ve en az yılda bir gözden geçirilir.'),
         o('notify_board', 'Kurul\'a 72 saat içinde bildirim', 'İhlal öğrenildikten sonra gecikmeksizin ve en geç 72 saat içinde Kurul\'un Kişisel Veri İhlal Bildirim Formu ile bildirim yapılması; bilgiler aynı anda sağlanamıyorsa aşamalı olarak tamamlanır, gecikmede gerekçe açıklanır.', 'Bütün veri sorumluları; GDPR kapsamında ayrıca denetim otoritesine 72 saat kuralı vardır.', 'İhlal kaydında "Öğrenilme: 12.11.2026 09:20 — Kurul\'a bildirim son saat: 15.11.2026 09:20" sayacı görünür.',
           'İhlal kaydında öğrenilme zamanı ve 72 saatlik bildirim son saati tutulur; bildirim kararı hukuk / uyum sorumlusunca verilir, Kurul\'un bildirim formundaki bilgiler (kapsam, etkilenen kişi ve kayıt sayısı, alınan önlemler) kayıttan üretilebilir.'),
         o('notify_subjects', 'Etkilenen kişilere bildirim', 'Etkilenen kişiler belirlendikten sonra makul olan en kısa sürede, iletişim adresine ulaşılabiliyorsa doğrudan, ulaşılamıyorsa web sitesinde yayın gibi uygun yollarla bildirim yapılmasıdır.', 'İhlalden etkilenen kişilerin belirlenebildiği her durum.', 'Etkilenen müşterilere "Hesabınızla ilgili güvenlik bildirimi" e-postası: ne oldu, hangi veriler etkilendi, ne yapmalı, iletişim.',
           'Etkilenen kişiler kayıtlardan belirlenebilecek biçimde loglama yapılır; bildirim şablonu (ne oldu, hangi veriler, olası sonuçlar, alınan önlemler, kişinin yapması gerekenler, iletişim) hazır tutulur ve toplu gönderim yeteneği bulunur.'),
         o('breach_log', 'İhlal kaydı', 'Her ihlalin olguları, etkileri ve alınan önlemlerin kayıt altına alınması ve Kurul incelemesine hazır tutulmasıdır; bildirim gerekmeyen olaylar da kaydedilir.', 'Bütün veri sorumluları.', 'Panelde "Güvenlik olayları" kaydı: tarih, tür, etkilenen kayıt sayısı, kök neden, önlemler, bildirim durumu.',
           'Her ihlal ve ihlal şüphesi; zaman çizelgesi, etkilenen veri kategorileri ve kişi sayısı, kök neden, alınan önlemler ve bildirim kararlarıyla değiştirilemez bir kayda yazılır.'),
         o('processor_notice', 'Veri işleyenin gecikmeksizin bildirimi', 'Veri işleyen (barındırma, e-posta, yazılım sağlayıcısı) nezdinde yaşanan ihlalin veri sorumlusuna gecikmeksizin bildirilmesinin sözleşmeyle ve teknik olarak güvenceye alınmasıdır.', 'Dış hizmet sağlayıcı kullanan bütün projeler.', 'E-posta servis sağlayıcısının güvenlik bildirimleri doğrudan olay müdahale ekibinin ortak adresine gelir.',
           'Veri işleyen sözleşmelerinde ihlalin gecikmeksizin bildirilmesi yükümlülüğü ve iletişim noktası yazılır; sağlayıcıların güvenlik bildirim kanalları olay müdahale ekibinin izlediği adrese yönlendirilir.'),
         o('masking', 'Maskeleme ve anonimleştirme ile etkiyi azaltma', 'Kişisel verinin ekranlarda, loglarda, raporlarda ve test ortamlarında maskelenmesi ya da anonimleştirilmesi; böylece olası bir ihlalde açığa çıkan veri azalır.', 'Panelde çok sayıda kişinin kişisel veriye eriştiği ya da canlı verinin test ortamına kopyalandığı projeler.', 'Panel listesinde telefon "0532 *** ** 47" görünür; tamamı yalnız "Göster" ile ve yetkili role açılır, her gösterim loglanır; test ortamında sahte veri kullanılır.',
           'Kişisel veriler listelerde ve raporlarda varsayılan olarak maskeli gösterilir; tam değer yalnız yetkili rolle ve kayıt altına alınarak açılır; loglara kişisel veri yazılmaz; test ve geliştirme ortamlarında canlı kişisel veri yerine anonim ya da sentetik veri kullanılır.'),
         o('access_logs', 'Kişisel veriye erişim loglarının saklanması', 'Kişisel veriye kimin, ne zaman, hangi kayda eriştiğinin loglanması ve bu logların değiştirilemez biçimde belirli süre saklanmasıdır; ihlalin kapsamını belirlemenin tek yoludur.', 'Panelden kişisel veriye erişilen bütün projeler.', 'Erişim logu: "12.11.2026 11:02 — kullanici:183 — musteri:55210 — görüntüledi — IP"; loglar ayrı hesapta 2 yıl tutulur.',
           'Kişisel veriye görüntüleme, dışa aktarma ve değiştirme erişimleri kullanıcı, kayıt kimliği, işlem ve zamanla loglanır; loglar merkezi ve kurcalamaya dayanıklı biçimde saklanır, saklama süresi politikada yazılır; olağan dışı toplu erişimde uyarı verilir.'),
         o('drill', 'İhlal tatbikatı', 'Müdahale planının senaryo üzerinden (masa başı ya da teknik) denenmesi; 72 saatlik bildirim süresinin gerçekten karşılanabildiğinin görülmesidir.', 'Planı hazır olan bütün kurumlar; ekip değiştiğinde ayrıca.', 'Yılda bir masa başı tatbikat: "Müşteri listesi dışarı sızdı" senaryosunda bildirim taslağı 30 saatte hazırlandı, iki eksik adım plana eklendi.',
           'Veri ihlali müdahale planı en az yılda bir tatbikatla denenir; tatbikatta bildirim süreleri ölçülür, bulunan eksikler plana işlenir.'),
     ]},
]


# ============================================================ Rehber kaynakları (2026-11-12'de açılarak doğrulandı)
GUIDE_ADD = {
    'api_standards': [
        {'title': 'RFC 9457 — Problem Details for HTTP APIs', 'url': 'https://www.rfc-editor.org/rfc/rfc9457.html', 'note': 'API hata yanıtlarının standart JSON biçimi (type, title, status, detail, instance).'},
        {'title': 'RFC 9745 — The Deprecation HTTP Response Header Field', 'url': 'https://www.rfc-editor.org/rfc/rfc9745.html', 'note': 'Bir API kaynağının kullanımdan kaldırıldığını yanıtta bildiren Deprecation başlığı.'},
        {'title': 'RFC 8594 — The Sunset HTTP Header Field', 'url': 'https://www.rfc-editor.org/rfc/rfc8594.html', 'note': 'Eski API sürümünün hangi tarihte kapanacağını bildiren Sunset başlığı.'},
        {'title': 'RFC 9700 — Best Current Practice for OAuth 2.0 Security', 'url': 'https://www.rfc-editor.org/rfc/rfc9700.html', 'note': 'Erişim ve yenileme jetonlarının güvenli kullanımı, jeton rotasyonu ve kapsam kısıtlama için güncel en iyi uygulamalar.'},
    ],
    'auth': [
        {'title': 'OWASP — Session Management Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html', 'note': 'Oturum süresi, boşta kalma zaman aşımı, oturumun sunucuda sonlandırılması ve çoklu oturum yönetimi.'},
        {'title': 'NIST SP 800-53 Rev. 5', 'url': 'https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final', 'note': 'AC-2 Hesap yönetimi, AC-6 En az yetki, AC-12 Oturum sonlandırma ve AU denetim kaydı kontrolleri.'},
    ],
    'performance_eng': [
        {'title': 'Google SRE Kitabı — Service Level Objectives', 'url': 'https://sre.google/sre-book/service-level-objectives/', 'note': 'SLI, SLO ve SLA kavramları; hedeflerin yüzdelik değerlerle tanımlanması.'},
        {'title': 'Google SRE Çalışma Kitabı — Implementing SLOs', 'url': 'https://sre.google/workbook/implementing-slos/', 'note': 'SLO\'nun ölçümden panoya ve uyarıya kadar adım adım uygulanması.'},
        {'title': 'Google SRE Çalışma Kitabı — Error Budget Policy', 'url': 'https://sre.google/workbook/error-budget-policy/', 'note': 'Hata bütçesi tükendiğinde yayın ve öncelik kararlarını düzenleyen örnek politika.'},
        {'title': 'Grafana k6 — Load test types', 'url': 'https://grafana.com/docs/k6/latest/testing-guides/test-types/', 'note': 'Yük, stres, ani artış (spike) ve uzun süreli dayanıklılık (soak) testlerinin farkları ve ne zaman kullanılacağı.'},
    ],
    'backup_recovery': [
        {'title': 'Google Cloud — Disaster recovery planning guide', 'url': 'https://cloud.google.com/architecture/dr-scenarios-planning-guide', 'note': 'RTO / RPO tanımı, felaket kurtarma desenleri ve planın test edilmesi.'},
        {'title': 'NIST SP 800-209 — Security Guidelines for Storage Infrastructure', 'url': 'https://csrc.nist.gov/pubs/sp/800/209/final', 'note': 'Yedek ve depolama altyapısının güvenliği: değiştirilemez kopya, şifreleme, erişim ayrımı, fidye yazılımına karşı koruma.'},
    ],
    'privacy': [
        {'title': 'KVKK — Çerez Uygulamaları Hakkında Rehber (Temmuz 2025)', 'url': 'https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/fb193dbb-b159-4221-8a7b-3addc083d33f.pdf', 'note': 'Çerez kategorileri, açık rıza ve aydınlatmanın ayrılması, kabul / ret / tercihler düğmelerinin eşit sunulması, rızanın periyodik hatırlatılması.'},
        {'title': 'KVKK — Kişisel Veri İşleme Envanteri Hazırlama Rehberi', 'url': 'https://www.kvkk.gov.tr/SharedFolderServer/CMSFiles/14a17049-71da-4417-a07b-961f75a0070e.PDF', 'note': 'Envanterde bulunması gereken alanlar: amaç, hukuki sebep, saklama ve periyodik imha süresi, aktarımlar, tedbirler.'},
        {'title': 'Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi Hakkında Yönetmelik (Resmî Gazete, 28.10.2017)', 'url': 'https://www.resmigazete.gov.tr/eskiler/2017/10/20171028-10.htm', 'note': 'Saklama ve imha politikası, periyodik imha (m. 11: aralık altı ayı geçemez) ve imha kayıtları.'},
        {'title': 'KVKK — Veri İhlali Bildirimi (Kurul\'un 2019/10 sayılı kararı)', 'url': 'https://www.kvkk.gov.tr/Icerik/5362/Veri-Ihlali-Bildirimi', 'note': 'İhlalin en geç 72 saat içinde Kurul\'a, etkilenenlere makul en kısa sürede bildirimi, bildirim formu ve ihlal müdahale planı.'},
    ],
}


PART = {
    'sections': [],
    'fields': [],
    'fields_into': F_PERF + F_DR + F_AUTH + F_PRIV,
    'option_add': OPTION_ADD,
    'guide_add': GUIDE_ADD,
}
