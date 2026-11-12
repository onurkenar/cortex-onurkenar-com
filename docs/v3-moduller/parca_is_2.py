# -*- coding: utf-8 -*-
"""V3 İş Modülleri — parça 2: B11 Kurum Sertifikaları, B6 Bildirim Merkezi, B7 E-posta Aboneliği ve Toplu Gönderim,
B8 Sosyal Medya Paylaşım Modülü, B9 Pazarlama Otomasyonu ve Müşteri Yolculukları (2026-11-12).
Kaynak doküman: Web_Sayfasi_Projesi_Revize_Moduler_V3 (Sertifika Yönetimi, Bildirim Merkezi ve Çok Kanallı Mesajlaşma,
Mailing Abonelik ve 3. Parti E-Posta Gönderim, Mikro Sosyal Medya Paylaşım, Pazarlama Otomasyonu ve Journey Builder).
Kaynak adresleri 2026-11-12'de açılarak doğrulandı (developers.facebook.com curl'e 400 döndürdüğü için WebFetch ile okundu).
Bu dosya yalnız PART tanımlar; birleştirme docs/v3-moduller/kaynak.py'dedir."""

# --- sorumlu pozisyon ajanları (pozisyonlar.txt'ten birebir)
APP = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
INT = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani'
KINT = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/kidemli-entegrasyon-muhendisi'
SRE = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/site-guvenilirlik-muhendisi'
KVKK = 'poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani'
CERT = 'poz:kalite:14.02/standartlar-ve-sertifikasyon/sertifikasyon-uzmani'
DOCC = 'poz:kalite:14.01/dokuman-ve-kayit-kontrolu/dokuman-kontrol-uzmani'
TSEO = 'poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru/teknik-seo-uzmani'
EMAIL = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/e-posta-pazarlama-uzmani'
AUTO = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/pazarlama-otomasyonu-uzmani'
CRM = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/crm-uzmani'
MTECH = 'poz:pazarlama:marketing_operations_crm_martech/martech-ve-entegrasyon-muduru/entegrasyon-uzmani'
SOCIAL = 'poz:pazarlama:social_media_marketing/kanal-yonetimi-yoneticisi'
ABT = 'poz:pazarlama:growth_conversion/cro-ve-deney-yonetimi-muduru/a-b-test-uzmani'

ON_CERT = [{'field': 'modules_extra', 'in': ['certificates']}]
ON_NT = [{'field': 'modules_extra', 'in': ['notify']}]
ON_ML = [{'field': 'modules_extra', 'in': ['mailing']}]
ON_SP = [{'field': 'modules_extra', 'in': ['social_publish']}]
ON_MO = [{'field': 'modules_extra', 'in': ['automation']}]

# --- ortak kaynaklar (birden çok rehberde)
R_6563 = {'title': '6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun', 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6563&MevzuatTur=1&MevzuatTertip=5',
          'note': 'Ticari elektronik iletinin ancak alıcının önceden onayıyla gönderilebileceği (m. 6) ve ret hakkı (m. 8).'}
R_YON = {'title': 'Ticari İletişim ve Ticari Elektronik İletiler Hakkında Yönetmelik', 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20914&MevzuatTur=7&MevzuatTertip=5',
         'note': 'Onay gerektirmeyen bilgilendirme iletileri (m. 6), İYS\'ye kaydedilmeyen onayın geçersizliği (m. 7), retten sonra üç iş günü içinde durdurma (m. 10) ve kayıtların üç yıl saklanması.'}
R_IYS = {'title': 'İleti Yönetim Sistemi (İYS)', 'url': 'https://iys.org.tr/',
         'note': 'Ticari elektronik ileti onay ve retlerinin kaydedildiği ve sorgulandığı ulusal sistem.'}
R_GSND = {'title': 'Google — Email sender guidelines', 'url': 'https://support.google.com/a/answer/81126',
          'note': 'Gmail\'e günde 5.000 ve üzeri ileti gönderenler için SPF, DKIM, DMARC, tek tıkla abonelikten çıkış ve %0,3 spam oranı sınırı.'}


def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    if exclusive:
        x['exclusive'] = True
    return x


# =====================================================================================================
# B11 — Kurum Sertifikaları
# =====================================================================================================
SEC_CERT = {
    'id': 'biz_certificates', 'group': 'İş Modülleri', 'icon': '✪',
    'name': 'Kurum Sertifikaları', 'en': 'Company Certifications (ISO, TSE, CE, Halal, Accreditation)',
    'desc': 'Kurumun kendi kalite ve uygunluk belgelerinin (ISO 9001, ISO/IEC 27001, TSE, CE, helal, akreditasyon …) sitede nasıl gösterileceğini, geçerlilik tarihlerinin nasıl izleneceğini, belgelerin nasıl doğrulanacağını ve hangi şirket, hizmet, ürün ya da tesisle eşleşeceğini belirler; eğitim (LMS) katılımcı sertifikalarından ayrıdır.',
    'guide': {
        'purpose': 'Sertifikalar ziyaretçi için güven unsurudur ama yalnız geçerliyse: süresi dolmuş, kapsamı yanlış gösterilen ya da doğrulanamayan bir belge güveni artırmak yerine hukuki ve itibari risk yaratır. Bu bölüm kurum belgelerini tek merkezde, veren kuruluş, belge numarası, kapsam ve geçerlilik tarihleriyle yönetmeyi; süresi yaklaşanı hatırlatmayı, süresi dolanı yayından otomatik kaldırmayı ve her belgeyi veren kuruluşun sorgu sayfasına bağlamayı sağlar. Öğrencilere verilen eğitim sertifikaları bu modülün değil, Eğitim (LMS) modülündeki "Sertifika" özelliğinin konusudur.',
        'criteria': [
            'Her sertifika kaydında veren kuruluş, belge numarası, standart / kapsam metni, başlangıç ve bitiş tarihi ve belge dosyası zorunludur; eksik kayıt yayına alınmaz.',
            'Geçerlilik süresi sunucuda hesaplanır: bitiş tarihi geçen belge herkese açık sayfalardan kendiliğinden kalkar, yönetim panelinde "Süresi doldu" olarak görünür.',
            'Belge, akreditasyon kapsamı ve kapsamı dışındaki hizmet / tesis açıkça ayrılır; sertifika rozeti yalnız kapsamdaki hizmet ya da üründe gösterilir.',
            'Akreditasyonlu belgeler için akreditasyon kurumu (ör. TÜRKAK) ya da IAF CertSearch gibi resmî sorgu kaynağına bağlantı verilir.',
            'Yapısal veride kurum belgeleri schema.org Certification tipiyle (hasCertification) işaretlenir; işaretleme sayfada görünen bilgiyle birebir aynıdır.',
            'Sertifika ekleme, değiştirme, yayından kaldırma ve dosya indirme işlemleri denetim kaydına yazılır.',
        ],
        'pitfalls': [
            'Süresi dolmuş sertifikanın logosunu sitede bırakmak: ziyaretçi yanıltılır, belgelendirme kuruluşu logonun kaldırılmasını isteyebilir.',
            'Yalnız bir tesis ya da hizmet için alınmış belgeyi bütün kuruma aitmiş gibi göstermek (kapsam dışı kullanım).',
            'Akreditasyonsuz bir kuruluştan alınmış belgeyi akreditasyonlu gibi sunmak; doğrulama bağlantısı vermemek.',
            'Belge PDF\'ini kişisel veri (imza, T.C. kimlik numarası, çalışan bilgisi) içeren hâliyle herkese açık indirmeye koymak.',
            'Kurum belgelerini kişilerin eğitim sertifikası için tasarlanmış EducationalOccupationalCredential tipiyle işaretlemek ya da yapısal verinin zengin sonuç getireceğini varsaymak.',
            'Yenileme sürecini tek kişinin takvimine bırakmak: hatırlatma ve görev ataması olmadan belge sessizce düşer.',
        ],
        'resources': [
            {'title': 'schema.org — Certification', 'url': 'https://schema.org/Certification', 'note': 'Veren kuruluş (issuedBy), belge numarası (certificationIdentification), geçerlilik (validFrom, expires), durum (certificationStatus) ve denetim tarihi alanları.'},
            {'title': 'schema.org — hasCertification', 'url': 'https://schema.org/hasCertification', 'note': 'Sertifikayı Organization, Service, Product, Place ya da Person kaydına bağlayan özellik.'},
            {'title': 'schema.org — hasCredential', 'url': 'https://schema.org/hasCredential', 'note': 'Kişi ve kurum yeterlilikleri için genel özellik; kurum kalite belgelerinde Certification daha uygundur.'},
            {'title': 'Google — Merchant listing structured data', 'url': 'https://developers.google.com/search/docs/appearance/structured-data/merchant-listing', 'note': 'Google\'ın hasCertification\'ı yalnız belirli ürün etiketleri (AB enerji etiketi, araç CO2 sınıfı) için okuduğunu gösterir; ISO belgeleri için zengin sonuç yoktur.'},
            {'title': 'TÜRKAK — Türk Akreditasyon Kurumu', 'url': 'https://www.turkak.org.tr/', 'note': 'Türkiye\'de akredite belgelendirme kuruluşlarının ve kapsamlarının sorgulandığı resmî kurum.'},
            {'title': 'IAF CertSearch', 'url': 'https://www.iafcertsearch.org/', 'note': 'Akreditasyonlu yönetim sistemi belgelerinin uluslararası doğrulama veritabanı.'},
            {'title': 'Avrupa Komisyonu — CE marking', 'url': 'https://single-market-economy.ec.europa.eu/single-market/ce-marking_en', 'note': 'CE işaretinin ne anlama geldiği; bir kurum belgesi değil, ürün uygunluk beyanı olduğu.'},
            {'title': 'Helal Akreditasyon Kurumu (HAK)', 'url': 'https://hak.gov.tr/', 'note': 'Helal belgelendirme kuruluşlarının akreditasyonu ve sorgulanması.'},
        ],
    },
}

F_CERT = [
    {'id': 'cert_display', 'section': 'biz_certificates', 'type': 'multiselect', 'label': 'Sertifikaların Sitede Gösterimi', 'en': 'Certificate Display & Structured Data',
     'agents': [TSEO, APP, CERT], 'showIf': ON_CERT,
     'explanation': 'Kurum belgelerinin herkese açık sitede nerede ve nasıl görüneceğini, detay sayfası, indirme ve yapısal veri kullanılıp kullanılmayacağını belirler. Öğrencilere verilen eğitim sertifikaları bu kararın değil, Eğitim Özellikleri kararındaki "Sertifika" seçeneğinin konusudur.',
     'scenario': 'Kalite, bilgi güvenliği ya da ürün uygunluk belgesi satın alma kararında rol oynuyorsa (kurumsal satış, kamu ihalesi, gıda, sağlık, yazılım hizmeti).',
     'example': 'Hizmetler sayfasında "ISO/IEC 27001" rozeti görünür; rozete tıklayınca belge numarası, kapsam, geçerlilik tarihi ve veren kuruluşun sorgu bağlantısı olan detay sayfası açılır.',
     'rule': 'Kurum sertifikaları sitede şu biçimlerde gösterilir: {labels}. Yalnız geçerli ve yayın onayı verilmiş belgeler gösterilir; sayfada veren kuruluş, belge numarası, kapsam ve bitiş tarihi görünür, belge kapsamı dışındaki hizmet ya da üründe rozet çıkmaz.',
     'options': [
         o('page', 'Sertifikalar sayfası (önerilen)', 'Bütün geçerli belgelerin kategoriye göre listelendiği tek sayfa.', 'Birden çok belgesi olan her kurum.', '/sertifikalar sayfasında Kalite, Bilgi Güvenliği ve Ürün Uygunluğu başlıkları altında kartlar.',
           'Sertifikalar sayfası yalnız geçerli belgeleri kategoriye göre listeler; her kartta logo, belge adı, veren kuruluş, belge numarası ve bitiş tarihi bulunur.'),
         o('badge', 'Hizmet / ürün sayfasında rozet', 'İlgili belge, kapsamına giren hizmet ya da ürün sayfasında küçük rozet olarak görünür.', 'Belgenin belirli bir hizmet ya da ürünü kapsadığı durumlar.', 'Bulut barındırma hizmeti sayfasında ISO/IEC 27001 rozeti; danışmanlık sayfasında yok.',
           'Rozet yalnız sertifikanın eşleştiği varlıkta gösterilir ve detay sayfasına bağlanır; rozet görseli alternatif metin taşır.'),
         o('footer', 'Alt bilgide seçili logolar', 'Sitenin alt bilgisinde öne çıkarılmış birkaç belge logosu.', 'Belgenin kurumun tamamını kapsadığı ve marka güveni için sürekli görünmesi istendiği durumlar.', 'Her sayfanın altında ISO 9001 ve TSE logoları, Sertifikalar sayfasına bağlantılı.',
           'Alt bilgide yalnız kurumun tamamını kapsayan, "öne çıkar" işaretli en çok birkaç geçerli belge gösterilir; logo kullanım kuralları belgelendirme kuruluşunun yönergesine uyar.'),
         o('detail', 'Belge başına detay sayfası', 'Her sertifika için kapsam metni, tarihler ve doğrulama bağlantısı olan ayrı sayfa.', 'Kurumsal alıcıların belge ayrıntısını sorduğu, ihale ve tedarikçi değerlendirmesi yapılan sektörler.', '/sertifikalar/iso-27001 sayfasında kapsam: “İstanbul veri merkezi ve yönetilen hizmetler”.',
           'Her belgenin detay sayfası canonical adres taşır; süresi dolan belgenin sayfası 410 ya da arşiv notuyla döner, arama motorlarına noindex verilir.'),
         o('download', 'Belge dosyasını indirme', 'Belge PDF\'inin ya da görselinin herkese açık indirilmesi.', 'Müşterilerin tedarikçi dosyası için belge kopyası istediği durumlar.', 'Detay sayfasında "Belgeyi indir (PDF, 240 KB)" bağlantısı.',
           'Herkese açık indirilen belge kişisel veri (imza, kimlik numarası, çalışan adı) içermeyen sürümdür; indirme sayısı kişisel veri tutmadan sayılır, gizli belgeler yalnız yetkili kullanıcıya imzalı ve süreli bağlantıyla verilir.'),
         o('schema', 'Yapısal veri (schema.org Certification)', 'Belgelerin Organization, Service ya da Product kaydına hasCertification ile bağlanması.', 'Arama motorlarının ve yapay zekâ asistanlarının kurum belgelerini doğru okuması istendiğinde.', 'Detay sayfasının JSON-LD\'sinde Certification: issuedBy, certificationIdentification, validFrom, expires.',
           'Kurum belgeleri schema.org Certification tipiyle (issuedBy, certificationIdentification, validFrom, expires, certificationStatus) işaretlenir ve hasCertification ile ilgili varlığa bağlanır; EducationalOccupationalCredential kullanılmaz, işaretleme sayfada görünen bilgiyle aynıdır ve zengin sonuç vaat edilmez.'),
     ]},

    {'id': 'cert_validity', 'section': 'biz_certificates', 'type': 'multiselect', 'label': 'Geçerlilik Takibi ve Doğrulama', 'en': 'Validity Tracking & Verification',
     'agents': [CERT, APP], 'showIf': ON_CERT,
     'explanation': 'Sertifikaların bitiş tarihinin nasıl izleneceğini, süresi yaklaşınca kime hatırlatılacağını, süresi dolanın ne olacağını ve belgenin veren kuruluş üzerinden nasıl doğrulanacağını belirler.',
     'scenario': 'Belgeler yıllık gözetim denetimi ve üç yıllık yenileme döngüsüne tabiyse ya da birden çok belge farklı tarihlerde sona eriyorsa.',
     'example': 'ISO 9001 belgesinin bitişine 90 gün kala kalite sorumlusuna "yenileme denetimi planla" görevi açılır; bitiş günü geçince rozet siteden kalkar ve panelde kırmızı "Süresi doldu" etiketi çıkar.',
     'rule': 'Sertifika geçerlilik ve doğrulama kuralları: {labels}. Geçerlilik her istekte sunucu saatine göre hesaplanır; arayüzdeki tarih bilgisine güvenilmez.',
     'options': [
         o('reminder', 'Bitişten önce hatırlatma (önerilen)', 'Bitiş tarihinden belirli gün önce sorumluya hatırlatma gönderilir.', 'Her kurum.', 'Bitişe 90, 30 ve 7 gün kala kalite sorumlusuna e-posta ve panel bildirimi.',
           'Bitiş tarihinden 90, 30 ve 7 gün önce belge sorumlusuna ve yedeğine hatırlatma gönderilir; hatırlatma zamanlanmış iş olarak çalışır ve aynı eşik için bir kez gönderilir.'),
         o('auto_expire', 'Süresi dolan otomatik yayından kalkar (önerilen)', 'Bitiş tarihi geçen belge herkese açık bütün alanlardan kendiliğinden kaldırılır.', 'Sitede belge rozeti ya da logosu kullanan her kurum.', 'Gece çalışan iş süresi dolan ISO 14001 belgesini "Süresi doldu" durumuna alır, rozetler kaybolur.',
           'Bitiş tarihi geçen belge "Süresi doldu" durumuna alınır ve sayfa, rozet, alt bilgi ve yapısal veriden kalkar; yeniden yayın yalnız yeni tarihlerle yapılır.'),
         o('renewal_task', 'Yenileme görevi ve geçmişi', 'Yenileme süreci sorumluya görev olarak atanır; önceki belge sürümleri geçmişte saklanır.', 'Birden çok belgesi ve belge sorumlusu olan kurumlar.', 'Görev: "ISO 27001 yeniden belgelendirme denetimi — sorumlu: Bilgi Güvenliği Müdürü, son tarih 15 Mart".',
           'Yenileme sorumluya görev olarak atanır; yeni belge yüklenince eski sürüm silinmez, geçmişte tarih ve yükleyenle saklanır.'),
         o('verify_link', 'Veren kuruluşta doğrulama bağlantısı', 'Belge numarasıyla veren belgelendirme kuruluşunun sorgu sayfasına bağlantı verilir.', 'Ziyaretçinin ya da kurumsal alıcının belgeyi bağımsız doğrulaması istendiğinde.', 'Detay sayfasında "Belgeyi doğrula" → belgelendirme kuruluşunun sorgu sayfası, belge no: TR-1234.',
           'Her belgede veren kuruluşun resmî doğrulama adresi ve belge numarası tutulur; bağlantı yalnız https ve izinli alan adlarına verilir, yeni sekmede rel="noopener" ile açılır.'),
         o('accreditation', 'Akreditasyon kontrolü (TÜRKAK / IAF)', 'Belgeyi veren kuruluşun akreditasyonu ve akreditasyon kapsamı kayda yazılır ve kontrol edilir.', 'Kamu ihalesi, kurumsal tedarikçi değerlendirmesi ya da regüle sektörler.', 'Kayıtta "Akreditasyon: TÜRKAK, kapsam: ISO/IEC 27001" ve IAF CertSearch bağlantısı.',
           'Akreditasyonlu belgelerde akreditasyon kurumu ve kapsamı kaydedilir; akreditasyonsuz belge "akredite" ibaresiyle gösterilmez.'),
         o('audit_log', 'Denetim kaydı ve dosya erişim yetkisi', 'Belge ekleme, değiştirme, yayından kaldırma ve indirme işlemleri kayda yazılır; belge dosyaları yetkiye göre açılır.', 'Kalite yönetim sistemi denetimine giren kurumlar.', 'Kayıt: "12.03 — Kalite Uzmanı, ISO 9001 bitiş tarihini değiştirdi (eski: 2026-05-01)".',
           'Sertifika kayıtlarındaki her değişiklik kim, ne zaman, hangi alan, eski ve yeni değerle denetim kaydına yazılır; dosyalar özel depolamada tutulur ve yetkiye göre imzalı bağlantıyla verilir.'),
     ]},

    {'id': 'cert_entities', 'section': 'biz_certificates', 'type': 'multiselect', 'label': 'Sertifikanın Bağlandığı Varlıklar', 'en': 'Certificate-to-Entity Mapping',
     'agents': [DOCC, APP], 'showIf': ON_CERT,
     'explanation': 'Bir sertifikanın hangi kayıtlarla ilişkilendirilebileceğini belirler. Aynı belge birden çok varlığa bağlanabilir; rozet ve yapısal veri bu eşlemeye göre çıkar.',
     'scenario': 'Grup şirketi, birden çok marka ya da tesis varsa ya da belge yalnız belirli hizmet veya ürünleri kapsıyorsa.',
     'example': 'ISO 22000 belgesi yalnız "Ankara üretim tesisi" ve o tesiste üretilen ürünlerle eşleşir; İzmir tesisinin ürün sayfalarında rozet çıkmaz.',
     'rule': 'Sertifikalar şu varlıklarla eşleştirilebilir: {labels}. Eşleme belge kapsamına uygun yapılır; kapsam dışı varlıkla eşleme yapılmaz ve rozet yalnız eşlenen varlıkta gösterilir.',
     'options': [
         o('company', 'Şirket / tüzel kişi (önerilen)', 'Belgenin hangi şirkete ait olduğu.', 'Her kurum; grup yapısında zorunlu.', 'Belge sahibi: “Örnek Teknoloji A.Ş.”.',
           'Her sertifika bir tüzel kişiye bağlıdır; grup şirketlerinde belge başka şirketin sayfasında gösterilmez.'),
         o('brand', 'Marka', 'Belgenin hangi marka altında gösterileceği.', 'Birden çok markası olan şirketler.', 'Aynı şirketin iki markasından yalnız birinin sitesinde helal belgesi görünür.',
           'Çok markalı yapıda sertifika yalnız eşlendiği markanın sayfalarında gösterilir.'),
         o('service', 'Hizmet', 'Belgenin kapsadığı hizmetler.', 'Hizmet bazlı belgelendirme (ör. bilgi güvenliği yalnız barındırma hizmetinde).', 'Yönetilen güvenlik hizmeti sayfasında ISO/IEC 27001 rozeti.',
           'Hizmet eşlemesi Service kaydının yapısal verisine hasCertification olarak da yazılır.'),
         o('product', 'Ürün', 'Belgenin ya da uygunluk işaretinin kapsadığı ürünler.', 'CE, TSE, helal ya da ürün belgesi olan üreticiler ve satıcılar.', 'Ürün sayfasında “CE — uygunluk beyanı” bağlantısı.',
           'Ürün eşlemesinde CE gibi ürün uygunluk işaretleri kurum belgesi olarak değil, ürünün uygunluk bilgisi olarak gösterilir.'),
         o('facility', 'Tesis / lokasyon', 'Belgenin geçerli olduğu fabrika, ofis, şube ya da veri merkezi.', 'Belge kapsamı adres bazında sınırlıysa.', 'Konum sayfasında “Bu tesis ISO 14001 kapsamındadır”.',
           'Tesis eşlemesi şube / konum sayfasında gösterilir; kapsam dışı tesislerde belge gösterilmez.'),
         o('partner', 'İş ortağı / tedarikçi', 'İş ortaklarının ve tedarikçilerin belgelerinin kurum içinde izlenmesi.', 'Tedarikçi kalitesinin izlendiği, yetkili servis ya da bayi ağı olan kurumlar.', 'Panelde tedarikçi kartında “ISO 9001 — bitiş 2027-02-10”.',
           'İş ortağı ve tedarikçi belgeleri varsayılan olarak yalnız panelde görünür; herkese açık gösterim ayrıca onay ister.'),
     ]},
]

# =====================================================================================================
# B6 — Bildirim Merkezi
# =====================================================================================================
SEC_NT = {
    'id': 'biz_notify', 'group': 'İş Modülleri', 'icon': '◔',
    'name': 'Bildirim Merkezi', 'en': 'Notification Center & Multichannel Messaging',
    'desc': 'Sistemin ürettiği bütün bildirimlerin (e-posta, SMS, WhatsApp, mobil ve web anlık bildirim, uygulama içi bildirim) tek merkezden, kanal önceliği, izin kontrolü, şablon, kuyruk ve teslim takibiyle gönderilmesini yapılandırır.',
    'guide': {
        'purpose': 'Bildirimler farklı modüllerde ayrı ayrı yazıldığında aynı kişiye aynı anda üç kanaldan mesaj gider, pazarlama iletisi izinsiz kişiye ulaşır, başarısız gönderim fark edilmez ve kim neyi ne zaman aldı sorusu yanıtsız kalır. Bildirim Merkezi bütün modüllerin olay üretip merkeze bıraktığı, merkezin ise kategoriye (güvenlik, işlemsel, hizmet, pazarlama) göre izin, tercih, sessiz saat ve sıklık kurallarını uygulayıp uygun kanaldan gönderdiği ortak altyapıdır. İşlemsel e-posta sağlayıcısı ve gönderici alan adı Sunucu & Altyapı › E-posta & Bildirimler bölümünde, WhatsApp Business hesabının kurulumu Meta Servisleri menüsünde seçilir; bu bölüm onları kullanır.',
        'criteria': [
            'Her bildirim bir kategoriye bağlıdır; pazarlama kategorisindeki ileti gönderimden hemen önce İYS ve kullanıcı tercihi kontrol edilmeden kuyruğa alınmaz.',
            'Güvenlik ve hesap bildirimleri (şifre sıfırlama, yeni cihazdan giriş, MFA) tercih merkezinden kapatılamaz ve sessiz saatlere takılmaz.',
            'Gönderimler kuyrukta, olay kimliğine bağlı idempotency anahtarıyla işlenir; yeniden deneme aynı bildirimi iki kez göndermez.',
            'Teslim durumu (kuyrukta, gönderildi, teslim edildi, başarısız, iade) sağlayıcı webhook\'larından imza doğrulanarak güncellenir.',
            'Şablonlar kanal ve dil başına yönetilir, sürümlenir; değişken eksikse ileti gönderilmez, hata kaydı açılır.',
            'Gönderim kaydında ileti içeriği değil, şablon sürümü, alıcı kimliği (maskeli adres), kanal, durum ve hata kodu tutulur; kayıtlar belirlenen sürede anonimleştirilir.',
        ],
        'pitfalls': [
            'İşlemsel bir iletiye (sipariş onayı, randevu hatırlatma) kampanya ya da ürün önerisi eklemek: ileti ticari elektronik ileti sayılır ve önceden onay ister.',
            'Bildirimleri istek sırasında doğrudan sağlayıcıya göndermek: sağlayıcı yavaşladığında sayfa yanıtı gecikir, hata olunca bildirim kaybolur.',
            'Web anlık bildirim iznini sayfa açılır açılmaz istemek: kullanıcı reddeder ve tarayıcı bir daha sormaz; izin yalnız kullanıcı eylemiyle istenir.',
            'iOS\'ta web anlık bildirimin her sitede çalıştığını varsaymak: yalnız ana ekrana eklenmiş web uygulamalarında (iOS / iPadOS 16.4 ve sonrası) çalışır.',
            'Kişisel veriyi (sağlık, finans ayrıntısı, tek kullanımlık kod) kilit ekranında görünen bildirim metnine koymak.',
            'Retten sonra ileti göndermeye devam etmek: ret bütün kanallara ve bağlı sistemlere (CRM, e-posta servis sağlayıcısı) senkron edilmezse ihlal oluşur.',
        ],
        'resources': [
            {'title': 'MDN — Push API', 'url': 'https://developer.mozilla.org/en-US/docs/Web/API/Push_API', 'note': 'Service worker ile tarayıcıya anlık bildirim abonelik ve alma modeli.'},
            {'title': 'MDN — Notifications API', 'url': 'https://developer.mozilla.org/en-US/docs/Web/API/Notifications_API', 'note': 'Bildirim izni isteme ve sistem bildirimi gösterme.'},
            {'title': 'web.dev — Push notifications overview', 'url': 'https://web.dev/articles/push-notifications-overview', 'note': 'Web anlık bildirim mimarisi, izin akışı ve iyi uygulamalar.'},
            {'title': 'RFC 8292 — VAPID', 'url': 'https://www.rfc-editor.org/rfc/rfc8292', 'note': 'Uygulama sunucusunun web push hizmetine kendini tanıttığı anahtar çifti.'},
            {'title': 'WebKit — Web Push for Web Apps on iOS and iPadOS', 'url': 'https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/', 'note': 'iOS / iPadOS 16.4 ile ana ekrana eklenen web uygulamalarına gelen web push desteği.'},
            {'title': 'Firebase Cloud Messaging', 'url': 'https://firebase.google.com/docs/cloud-messaging', 'note': 'Android, iOS ve web için mobil anlık bildirim gönderim altyapısı.'},
            {'title': 'Apple — User Notifications', 'url': 'https://developer.apple.com/documentation/usernotifications', 'note': 'iOS uygulamalarında bildirim izni ve Apple Push Notification service (APNs).'},
            R_YON,
            R_IYS,
        ],
    },
}

F_NT = [
    {'id': 'nt_channels', 'section': 'biz_notify', 'type': 'multiselect', 'label': 'Bildirim Kanalları', 'en': 'Notification Channels',
     'agents': [INT, APP], 'showIf': ON_NT,
     'explanation': 'Bildirim Merkezi\'nin hangi kanallardan gönderim yapacağını belirler. E-posta için Sunucu & Altyapı › İşlemsel E-posta kararındaki sağlayıcı ve Gönderici Alan Adı kullanılır; WhatsApp hesabı Meta Servisleri › WhatsApp Business bölümünde kurulur.',
     'scenario': 'Kullanıcıya zamanında ulaşmanın iş sonucu doğrudan etkilediği (randevu, sipariş, ödeme, destek talebi) ya da ekip içi iş bildirimlerinin gerektiği projeler.',
     'example': 'Randevudan 24 saat önce uygulama içi bildirim ve e-posta, 2 saat önce SMS gönderilir; panelde zil simgesinde okunmamış bildirim sayısı görünür.',
     'rule': 'Bildirim Merkezi kanalları: {labels}. Her kanal ayrı bir sağlayıcı bağdaştırıcısıyla (adapter) eklenir, panelden açılıp kapatılabilir; sağlayıcı anahtarları gizli değişken yönetiminde tutulur, koda ve loglara yazılmaz.',
     'recommend': [{'field': 'mt_services', 'map': {'whatsapp': ['whatsapp']}}],
     'options': [
         o('in_app', 'Uygulama içi bildirim merkezi (önerilen)', 'Kullanıcı ve yönetim panelinde zil simgesi, okunmuş / okunmamış listesi ve ilgili kayda bağlantı.', 'Üyelik, portal ya da yönetim paneli olan her proje.', 'Panelin sağ üstünde “3” rozetli zil; tıklayınca “Teklifiniz onaylandı → teklifi görüntüle”.',
           'Uygulama içi bildirimler kullanıcıya özel saklanır, yalnız sahibine listelenir (sahiplik sunucuda denetlenir), okundu bilgisi tutulur ve bağlantılar ilgili kayda yönlendirir.'),
         o('email', 'E-posta', 'İşlemsel e-posta sağlayıcısı üzerinden gönderim.', 'Kayıt, sipariş, fatura, şifre sıfırlama ve uzun içerikli bildirimler.', 'Sipariş onayı e-postası, sipariş numarası ve takip bağlantısıyla.',
           'E-postalar İşlemsel E-posta kararındaki sağlayıcı ve doğrulanmış gönderici alan adıyla gönderilir; pazarlama e-postaları ayrı alt alan adı ve E-posta Aboneliği modülü kurallarıyla gider.'),
         o('sms', 'SMS', 'Kısa mesaj sağlayıcısı üzerinden gönderim.', 'Tek kullanımlık kod, randevu hatırlatma ve acil durum bildirimi.', '“Randevunuz yarın 10:30’da. İptal için: …”',
           'SMS gönderiminde karakter sınırı ve Türkçe karakter kodlaması şablonda denetlenir; ticari SMS\'te başlıkta ya da içerikte MERSİS numarası ve ret yolu bulunur.'),
         o('whatsapp', 'WhatsApp Business', 'WhatsApp Business Platform (Cloud API ya da çözüm ortağı) üzerinden onaylı şablonlarla gönderim.', 'Müşterinin WhatsApp\'ı tercih ettiği randevu, kargo ve destek bildirimleri.', 'Onaylı “kargo yolda” şablonu, takip bağlantısıyla.',
           'WhatsApp iletileri Meta Servisleri › WhatsApp Business kararlarındaki hesap ve şablon kurallarıyla, yalnız onaylı şablon kategorisine uygun içerikle gönderilir.'),
         o('mobile_push', 'Mobil anlık bildirim (FCM / APNs)', 'Mobil uygulamaya Firebase Cloud Messaging ya da Apple Push Notification service ile bildirim.', 'Mobil uygulaması olan projeler.', 'Telefon kilit ekranında “Siparişiniz teslim edildi”; dokununca uygulamada sipariş detayı açılır.',
           'Cihaz belirteçleri (token) kullanıcıya bağlı saklanır, geçersiz döndüğünde silinir; bildirim metninde hassas kişisel veri bulunmaz, derin bağlantı (deep link) yalnız uygulama içi izinli yollara gider.'),
         o('web_push', 'Web anlık bildirim (Push API)', 'Tarayıcıya service worker ve VAPID anahtarıyla bildirim.', 'Sık dönen kullanıcısı olan web uygulamaları, haber ve topluluk siteleri.', 'Kullanıcı “Yanıt gelince haber ver” düğmesine basınca tarayıcı izin sorar; yanıt geldiğinde masaüstü bildirimi çıkar.',
           'İzin yalnız kullanıcının bir eylemiyle istenir, sayfa açılışında istenmez; abonelikler VAPID ile imzalanır, süresi dolan abonelik (404 / 410) silinir; iOS\'ta yalnız ana ekrana eklenmiş web uygulamasında çalıştığı kullanıcıya açıklanır.'),
         o('team_chat', 'Ekip içi kanal (Slack / Microsoft Teams)', 'Yönetici ve ekip bildirimlerinin kurumsal sohbet aracına iletilmesi.', 'Yeni talep, ödeme hatası, sistem uyarısı gibi ekip içi bildirimler.', '#satis kanalına “Yeni teklif talebi: 120.000 TL — CRM kaydına git”.',
           'Ekip kanallarına yalnız iç bildirimler gider; müşteri kişisel verisi mesajda yazmaz, kayda bağlantı verilir ve bağlantı yetki kontrolüyle açılır.'),
     ]},

    {'id': 'nt_categories', 'section': 'biz_notify', 'type': 'multiselect', 'label': 'Bildirim Kategorileri ve İzin Kuralları', 'en': 'Notification Categories & Consent Rules',
     'agents': [KVKK, APP], 'showIf': ON_NT,
     'explanation': 'Bildirimlerin hangi kategorilere ayrılacağını ve her kategoride hangi izin kuralının uygulanacağını belirler. Ticari elektronik ileti (pazarlama) önceden onay ve İYS kaydı ister; hizmet ve işlemsel bildirimler onay gerektirmez ama tanıtım içeremez.',
     'scenario': 'Aynı altyapıdan hem işlemsel hem pazarlama iletisi gönderilecekse; izin ve ret kurallarının karışmaması için her projede.',
     'example': 'Abonelik yenileme hatırlatması "Hizmet" kategorisindedir ve İYS kontrolüne girmez; "%20 indirim" duyurusu "Pazarlama" kategorisindedir, İYS\'de onayı olmayan kişiye gitmez.',
     'rule': 'Bildirim kategorileri: {labels}. Her şablon tek bir kategoriye bağlıdır ve kategorinin izin kuralı gönderimden hemen önce sunucuda uygulanır; işlemsel ya da hizmet şablonuna tanıtım içeriği eklenemez.',
     'options': [
         o('security', 'Güvenlik ve hesap (önerilen)', 'Şifre sıfırlama, giriş doğrulama kodu, yeni cihazdan giriş, e-posta değişikliği.', 'Üyelik olan her proje.', '“Hesabınıza yeni bir cihazdan giriş yapıldı. Siz değilseniz şifrenizi değiştirin.”',
           'Güvenlik bildirimleri tercih merkezinden kapatılamaz, sıklık sınırı ve sessiz saatlerden muaftır; kodlar tek kullanımlık ve kısa ömürlüdür, loglara yazılmaz.'),
         o('transactional', 'İşlemsel (önerilen)', 'Sipariş, ödeme, randevu, teslimat, destek talebi gibi kullanıcının başlattığı işlemin bildirimi.', 'İşlem ya da kayıt alan her proje.', '“Siparişiniz kargoya verildi — takip no: …”',
           'İşlemsel bildirimler kullanıcının işlemiyle tetiklenir ve onay gerektirmez; içerikte ürün ya da kampanya tanıtımı yapılmaz.'),
         o('service', 'Hizmet bilgilendirme', 'Devam eden abonelik, üyelik, bakım, değişiklik ve yasal bilgilendirme iletileri.', 'Abonelik, SaaS, portal ve üyelik projeleri.', '“Planınız 7 gün sonra yenilenecek.” ya da “Gizlilik politikamız güncellendi.”',
           'Hizmet bilgilendirmeleri Ticari İletişim Yönetmeliği\'nin onay gerektirmeyen durumları kapsamında gönderilir ve İYS kontrolüne girmez; mal ya da hizmet tanıtımı içerirse pazarlama kategorisine geçer.'),
         o('marketing', 'Pazarlama (ticari elektronik ileti)', 'Kampanya, indirim, bülten, ürün önerisi gibi tanıtım amaçlı iletiler.', 'E-posta, SMS ya da WhatsApp ile tanıtım yapılacaksa.', 'İYS\'de e-posta onayı olan kullanıcıya bülten gider; onayı olmayana gitmez.',
           'Pazarlama iletisi yalnız önceden onayı olan ve İYS\'de onayı kayıtlı alıcıya, onayın verildiği kanaldan gönderilir; gönderimden hemen önce İYS ve yerel tercih kontrol edilir, ret en geç üç iş günü içinde, mümkünse anında uygulanır; tacir ve esnafa onaysız gönderimde bile İYS ret kontrolü yapılır.'),
         o('internal', 'Ekip içi iş bildirimleri', 'Yeni talep, onay bekleyen işlem, görev ataması gibi çalışanlara giden bildirimler.', 'Yönetim paneli ve iş akışı olan projeler.', '“Onayınızı bekleyen 2 iade var.”',
           'Ekip bildirimleri rol ve sorumluluk alanına göre hedeflenir; yalnız kaydı görme yetkisi olan kişiye gider.'),
         o('system', 'Sistem ve operasyon uyarıları', 'Ödeme sağlayıcısı hatası, kuyruk birikmesi, sertifika süresi, entegrasyon kopması.', 'Canlı operasyonu izlenen her proje.', '“E-posta sağlayıcısı son 15 dakikada %12 hata döndü.”',
           'Sistem uyarıları operasyon ekibine, eşik ve tekrar bastırma kurallarıyla gider; kullanıcıya gösterilmez.'),
     ]},

    {'id': 'nt_delivery', 'section': 'biz_notify', 'type': 'multiselect', 'label': 'Gönderim Altyapısı (Kuyruk, Yeniden Deneme, Teslim Takibi)', 'en': 'Delivery Infrastructure',
     'agents': [KINT, SRE], 'showIf': ON_NT,
     'explanation': 'Bildirimlerin nasıl kuyruğa alınacağını, başarısız gönderimin nasıl yeniden deneneceğini, sağlayıcı ya da kanal çalışmazsa ne olacağını ve teslim durumunun nasıl izleneceğini belirler. Genel arka plan işi altyapısı Sunucu & Altyapı › Arka Plan İşleri kararındadır; bu karar bildirime özgü kuralları ekler.',
     'scenario': 'Günde yüzlerce bildirimin üzerinde gönderim yapılacaksa, sağlayıcı kesintisi iş kaybına yol açıyorsa ya da teslim kanıtı gerekiyorsa.',
     'example': 'SMS sağlayıcısı 503 döndürünce bildirim 1, 5 ve 30 dakika sonra yeniden denenir; üçüncü denemede yedek sağlayıcıya geçer; panelde "yeniden denenecek" sayacı görünür.',
     'rule': 'Bildirim gönderim altyapısı: {labels}. Gönderimler istek içinde değil, kuyruktan işlenir; her bildirim olay kimliğinden türeyen idempotency anahtarı taşır ve aynı olay için ikinci kez gönderilmez.',
     'recommend': [{'field': 'background_jobs', 'map': {'Queue': ['queue_retry'], 'Retry': ['queue_retry'], 'Dead Letter': ['queue_retry'], 'Webhook': ['webhooks']}}],
     'options': [
         o('queue_retry', 'Kuyruk, üstel geri çekilmeli yeniden deneme ve hatalı iş kuyruğu (önerilen)', 'Bildirimler kuyruğa alınır; geçici hatada artan aralıklarla yeniden denenir, sınır aşılınca ayrı hata kuyruğuna düşer.', 'Her proje.', 'Panelde kuyruk ekranı: bekleyen 12, işleniyor 3, başarısız 1 (yeniden dene düğmesi).',
           'Geçici hatalarda (zaman aşımı, 429, 5xx) üstel geri çekilme ve rastgele sapmayla kanal başına tanımlı sayıda yeniden denenir; kalıcı hatalarda (geçersiz numara, 4xx) yeniden denenmez; sınırı aşan iş hatalı iş kuyruğuna alınır ve uyarı üretir.'),
         o('priority', 'Öncelikli kuyruk', 'Güvenlik kodu ve kritik işlemsel bildirimler toplu gönderimlerden ayrı, öncelikli kuyrukta işlenir.', 'Toplu pazarlama gönderimiyle tek kullanımlık kodun aynı altyapıyı paylaştığı projeler.', '50.000 kişilik bülten gönderilirken şifre sıfırlama kodu saniyeler içinde ulaşır.',
           'Güvenlik ve işlemsel bildirimler ayrı ve öncelikli kuyrukta işlenir; toplu gönderim bu kuyruğu bekletemez.'),
         o('fallback', 'Kanal önceliği ve yedek kanal', 'Bildirim türüne göre kanal sırası tanımlanır; ulaşılamazsa sıradaki kanal denenir.', 'Kritik randevu ve ödeme bildirimleri.', 'Push teslim edilmezse 15 dakika sonra SMS gönderilir.',
           'Kanal sırası bildirim türü ve kullanıcı tercihine göre belirlenir; yedek kanala geçişte izin kuralları yeniden uygulanır, aynı bildirim iki kanaldan ancak tanımlı ise gider.'),
         o('provider_failover', 'Yedek sağlayıcı', 'Aynı kanal için ikinci sağlayıcı tanımlanır; birincisi hata verirse gönderim ona geçer.', 'SMS ya da e-posta kesintisinin doğrudan iş kaybı olduğu projeler.', 'SMS sağlayıcısı A kesintideyken iletiler B üzerinden gider; panelde geçiş kaydı.',
           'Sağlayıcı başına sağlık durumu izlenir; hata oranı eşiği aşılınca gönderim yedek sağlayıcıya geçer ve geçiş kayda yazılır.'),
         o('webhooks', 'Teslim durumu webhook\'ları', 'Sağlayıcıdan gelen teslim edildi, açıldı, iade, şikâyet olayları gönderim kaydına işlenir.', 'Teslim kanıtı ya da iade yönetimi gereken projeler.', 'Gönderim kaydında “teslim edildi 10:42:05”.',
           'Webhook istekleri sağlayıcının imzasıyla doğrulanır, olay kimliğiyle tekilleştirilir, hızlı yanıtlanıp kuyrukta işlenir; doğrulanamayan istek reddedilir.'),
         o('throttle', 'Hız sınırı ve parça parça gönderim', 'Sağlayıcının saniye / dakika sınırına göre gönderim hızı ayarlanır, toplu gönderim parçalara bölünür.', 'Toplu gönderim ya da düşük kotalı sağlayıcı kullanan projeler.', '10.000 SMS dakikada 500\'lük parçalarla gönderilir.',
           'Gönderim hızı sağlayıcı ve kanal başına sınırlanır; 429 yanıtında sağlayıcının bildirdiği bekleme süresine uyulur.'),
         o('send_log', 'Gönderim kaydı ve saklama', 'Her gönderimin kanal, şablon sürümü, durum, hata kodu ve sağlayıcı bilgisiyle kaydı.', 'Her proje; ticari ileti kayıtları mevzuat gereği saklanır.', 'Panelde kullanıcının bildirim geçmişi: tarih, kanal, şablon, durum.',
           'Gönderim kaydında ileti gövdesi ve tek kullanımlık kod tutulmaz, alıcı adresi maskelenir; ticari elektronik ileti kayıtları üç yıl saklanır, diğer kayıtlar saklama süresi sonunda anonimleştirilir.'),
     ]},

    {'id': 'nt_prefs', 'section': 'biz_notify', 'type': 'multiselect', 'label': 'Tercih Merkezi ve Baskı Kontrolü', 'en': 'Preference Center & Pressure Control',
     'agents': [KVKK, APP], 'showIf': ON_NT,
     'explanation': 'Kullanıcının hangi bildirimi hangi kanaldan alacağını kendisinin seçebileceği tercih merkezini ve aşırı bildirimi önleyen sessiz saat, sıklık sınırı ve tekrar engeli kurallarını belirler.',
     'scenario': 'Kullanıcıya birden çok kanaldan ve birden çok modülden bildirim gidiyorsa.',
     'example': 'Kullanıcı panelde "Kampanyalar: e-posta açık, SMS kapalı" seçer; gece 22:00–08:00 arasında yalnız güvenlik bildirimleri gelir.',
     'rule': 'Tercih ve baskı kontrolü: {labels}. Tercih ve ret değişiklikleri anında uygulanır ve kayda (kim, ne zaman, hangi kanal, kaynak) yazılır.',
     'options': [
         o('pref_center', 'Kategori × kanal tercih merkezi (önerilen)', 'Kullanıcı panelinde her kategori için kanal bazında aç / kapat.', 'Üyelik ya da portal olan her proje.', 'Tablo: Kampanyalar (E-posta ✓, SMS ✗, Push ✓), Hizmet bildirimleri (zorunlu).',
           'Tercih merkezi kategori × kanal bazında çalışır; güvenlik bildirimleri kapatılamaz ve bu açıkça yazılır; üye olmayan alıcı için imzalı, süreli bağlantıyla giriş gerektirmeden açılır.'),
         o('unsub_sync', 'Ret ve çıkış senkronu', 'Ret, bütün kanallara, CRM\'e, e-posta servis sağlayıcısına ve İYS\'ye yayılır.', 'Birden çok sistemin aynı kişiye ileti gönderebildiği projeler.', 'SMS\'teki ret bağlantısıyla çıkan kişi CRM\'de ve e-posta servis sağlayıcısında da “SMS: ret” olur.',
           'Ret bildirimi alındığı anda ilgili kanal için pazarlama gönderimi durur; ret CRM, e-posta servis sağlayıcısı ve İYS ile senkronlanır, yasal üst sınır üç iş günüdür.'),
         o('quiet_hours', 'Sessiz saatler', 'Belirli saatlerde (ör. 22:00–08:00) kritik olmayan bildirim gönderilmez, sonraya ertelenir.', 'SMS ve push gönderen her proje.', 'Gece 23:10\'da oluşan kampanya bildirimi sabah 09:00\'da gönderilir.',
           'Sessiz saatler alıcının saat dilimine göre uygulanır; kritik olmayan bildirimler pencere sonuna ertelenir, güvenlik ve kritik işlemsel bildirimler muaftır.'),
         o('freq_cap', 'Sıklık sınırı', 'Bir kişiye belirli sürede gönderilebilecek en çok bildirim sayısı (kanal ve kategori bazında).', 'Birden çok modülün ve otomasyonun aynı kişiye ileti gönderebildiği projeler.', 'Pazarlama: kişi başı haftada en çok 3 e-posta, 1 SMS.',
           'Sıklık sınırı kişi, kanal ve kategori bazında sunucuda sayılır; sınırı aşan pazarlama bildirimi düşürülür ya da ertelenir, güvenlik ve işlemsel bildirimler sayılmaz.'),
         o('dedupe', 'Tekrar engeli', 'Aynı içerikli bildirimin kısa sürede ikinci kez gönderilmesi engellenir.', 'Olayların birden çok kez tetiklenebildiği entegrasyonlar.', 'Ödeme sağlayıcısı aynı webhook\'u iki kez gönderse de kullanıcı tek “ödeme alındı” bildirimi alır.',
           'Aynı kullanıcıya aynı şablon ve aynı kayıt için tanımlı süre içinde ikinci bildirim gönderilmez.'),
         o('digest', 'Özet bildirim', 'Sık oluşan düşük öncelikli bildirimler tek özet iletide birleştirilir.', 'Topluluk, forum ve iş akışı bildirimleri.', 'Günde bir kez: “Takip ettiğiniz konularda 14 yeni yanıt”.',
           'Düşük öncelikli bildirimler kullanıcının seçtiği sıklıkta tek özet iletide toplanır; özet de kategori izin kuralına tabidir.'),
     ]},

    {'id': 'nt_templates', 'section': 'biz_notify', 'type': 'multiselect', 'label': 'Şablon Yönetimi', 'en': 'Template Management',
     'agents': [APP, EMAIL], 'showIf': ON_NT,
     'explanation': 'E-posta, SMS, WhatsApp, push ve uygulama içi bildirim şablonlarının nasıl hazırlanacağını, dil ve marka başına nasıl yönetileceğini, sürümleneceğini ve onaylanacağını belirler.',
     'scenario': 'Birden çok dil, marka ya da kanal varsa; şablonu geliştirici olmadan değiştirmek isteniyorsa.',
     'example': '"Randevu hatırlatma" şablonunun Türkçe ve İngilizce, e-posta ve SMS sürümleri; değişken: {ad}, {randevu_tarihi}; "Test gönderimi" düğmesi.',
     'rule': 'Bildirim şablonları: {labels}. Şablon değişkenleri kanala göre kaçışlanarak doldurulur (e-postada HTML, SMS\'te düz metin); zorunlu değişkeni eksik ileti gönderilmez.',
     'options': [
         o('central', 'Merkezi şablonlar, kanal ve dil başına (önerilen)', 'Her bildirim türünün kanal ve dil sürümleri tek yerde yönetilir.', 'Her proje.', 'Şablon listesi: Sipariş onayı → E-posta (TR, EN), SMS (TR), Push (TR, EN).',
           'Şablonlar bildirim türü × kanal × dil olarak saklanır; eksik dil sürümünde varsayılan dile düşülür ve bu durum kayda yazılır.'),
         o('versioning', 'Sürümleme ve onay', 'Şablon değişikliği yeni sürüm açar; kritik şablonlar yayından önce onaylanır.', 'Hukuki ya da finansal metin içeren bildirimler.', 'Fatura e-postası şablonu v4 → v5, finans onayından sonra etkin.',
           'Her şablon değişikliği yeni sürüm olarak saklanır; gönderim kaydı kullanılan sürümü tutar; kritik şablonlar onay akışından geçmeden etkinleşmez.'),
         o('preview_test', 'Önizleme ve test gönderimi', 'Örnek veriyle önizleme ve yalnız iç alıcılara test gönderimi.', 'Şablonu teknik olmayan ekiplerin düzenlediği projeler.', '“Test gönder” → yalnız tanımlı iç adreslere gider.',
           'Test gönderimi yalnız izinli iç alıcı listesine yapılır; gerçek müşteri verisi yerine örnek veri kullanılır.'),
         o('brand', 'Kurumsal kimlik ve yasal alt bilgi', 'Logo, renk, yazı tipi ve yasal alt bilgi (unvan, MERSİS, adres, ret yolu) şablona otomatik eklenir.', 'Birden çok marka ya da kurumsal kimlik kuralı olan projeler.', 'E-posta alt bilgisi: unvan, MERSİS no, adres, “E-posta tercihlerinizi yönetin”.',
           'Marka öğeleri Kurumsal Kimlik ve Ortak Bilgiler kararlarından alınır; pazarlama şablonlarında unvan, MERSİS numarası ve ret yolu zorunludur.'),
         o('limits', 'Kanal sınırı denetimi', 'SMS karakter / parça sayısı, push başlık ve metin uzunluğu, WhatsApp şablon kuralları kaydetmeden önce denetlenir.', 'SMS ve push kullanan projeler.', 'Uyarı: “Bu SMS Türkçe karakterler nedeniyle 3 parçaya bölünecek.”',
           'Şablon kaydedilirken kanalın uzunluk ve biçim sınırları denetlenir, aşımda uyarı verilir.'),
     ]},
]

# =====================================================================================================
# B7 — E-posta Aboneliği ve Toplu Gönderim
# =====================================================================================================
SEC_ML = {
    'id': 'biz_mailing', 'group': 'İş Modülleri', 'icon': '✉',
    'name': 'E-posta Aboneliği ve Toplu Gönderim', 'en': 'Email Subscriptions & Bulk Sending (ESP Integration)',
    'desc': 'E-posta aboneliklerinin, listelerin, abonelik kategorilerinin, abonelikten çıkışın, gönderilmeyecekler listesinin ve toplu gönderimin teknik altyapısını, e-posta servis sağlayıcısı (ESP) entegrasyonu ve alan adı kimlik doğrulamasıyla birlikte yapılandırır.',
    'guide': {
        'purpose': 'Toplu e-postanın içeriği, sıklığı ve izin metni Pazarlama › Mailing bölümünde belirlenir; bu bölüm onları çalıştıran sistemi kurar: hangi e-posta servis sağlayıcısının kullanılacağı, abonelik ve onayın nasıl kaydedileceği, İYS ile nasıl eşleneceği, tek tıkla abonelikten çıkışın ve gönderilmeyecekler listesinin nasıl çalışacağı ve alan adının SPF, DKIM, DMARC ile nasıl doğrulanacağı. Gmail ve Yahoo toplu gönderenlerden kimlik doğrulama, tek tıkla çıkış ve düşük şikâyet oranı ister; bunlar yoksa iletiler gelen kutusuna ulaşmaz.',
        'criteria': [
            'Pazarlama e-postası yalnız İYS\'de onayı kayıtlı, gönderilmeyecekler listesinde olmayan ve ilgili kategoriye abone kişiye gönderilir; kontrol gönderimden hemen önce sunucuda yapılır.',
            'Her pazarlama e-postasında RFC 8058\'e uygun List-Unsubscribe ve List-Unsubscribe-Post başlıkları ile gövdede görünür abonelikten çıkma bağlantısı bulunur.',
            'Gönderici alan adı SPF ve DKIM ile doğrulanır, DMARC kaydı yayımlanır ve From alan adı SPF ya da DKIM alan adıyla hizalanır.',
            'Hard bounce, şikâyet ve abonelikten çıkış olayları servis sağlayıcısının webhook\'larıyla alınır ve merkezi gönderilmeyecekler listesine işlenir.',
            'Çift onaylı abonelikte doğrulama bağlantısı tahmin edilemez, süreli ve tek kullanımlıktır; doğrulanmamış kayıt gönderim listesine girmez.',
            'Onay kayıtları (onay metni sürümü, tarih, kaynak, IP) onayın geçerliliği sona erdikten sonra üç yıl saklanır.',
        ],
        'pitfalls': [
            'Pazarlama ve işlemsel e-postayı aynı alan adı ve IP itibarıyla göndermek: kampanya şikâyetleri şifre sıfırlama e-postasının da spama düşmesine yol açar.',
            'Abonelikten çıkışı yalnız servis sağlayıcısında bırakmak: CRM ya da otomasyon aynı kişiye başka yoldan ileti göndermeye devam eder.',
            'Satın alınmış ya da başka kaynaktan aktarılmış listeye onay kontrolü yapmadan gönderim: hem 6563 ihlali hem itibar kaybı.',
            'Tek tıkla çıkış adresinin GET isteğinde aboneliği iptal etmesi: e-posta güvenlik tarayıcıları bağlantıyı açıp kullanıcıyı istemeden çıkarır.',
            'DMARC kaydını doğrudan reject ile başlatmak: raporlar izlenmeden yapılan sıkılaştırma meşru iletileri de engeller.',
            'Webhook isteklerini imza doğrulamadan işlemek: sahte istekle herhangi bir adres gönderilmeyecekler listesine eklenebilir ya da çıkarılabilir.',
        ],
        'resources': [
            {'title': 'RFC 8058 — One-Click Unsubscribe', 'url': 'https://www.rfc-editor.org/rfc/rfc8058', 'note': 'List-Unsubscribe-Post: List-Unsubscribe=One-Click başlığı, HTTPS POST ile çıkış ve başlıkların DKIM imzasında yer alması.'},
            {'title': 'RFC 2369 — List-Unsubscribe ve liste başlıkları', 'url': 'https://www.rfc-editor.org/rfc/rfc2369', 'note': 'E-posta listelerinde abonelikten çıkma başlığının tanımı.'},
            R_GSND,
            {'title': 'Yahoo — Sender best practices', 'url': 'https://senders.yahooinc.com/best-practices/', 'note': 'Toplu gönderenler için SPF, DKIM, DMARC, RFC 8058 tek tıkla çıkış ve çıkışın 2 gün içinde uygulanması.'},
            {'title': 'RFC 9989 — DMARC', 'url': 'https://www.rfc-editor.org/rfc/rfc9989', 'note': 'RFC 7489\'un yerini alan güncel DMARC belirtimi; hizalama ve politika.'},
            {'title': 'RFC 6376 — DKIM', 'url': 'https://www.rfc-editor.org/rfc/rfc6376', 'note': 'E-posta alan adı imzası.'},
            {'title': 'RFC 7208 — SPF', 'url': 'https://www.rfc-editor.org/rfc/rfc7208', 'note': 'Alan adı adına gönderim yetkisi olan sunucuların bildirimi.'},
            R_YON,
            R_IYS,
        ],
    },
}

F_ML = [
    {'id': 'ml_esp', 'section': 'biz_mailing', 'type': 'select', 'label': 'E-posta Servis Sağlayıcısı (ESP)', 'en': 'Email Service Provider',
     'agents': [MTECH, INT], 'showIf': ON_ML,
     'explanation': 'Toplu ve pazarlama e-postalarının hangi servis sağlayıcısı üzerinden gönderileceğini belirler. İşlemsel e-posta sağlayıcısı Sunucu & Altyapı › İşlemsel E-posta kararındadır; aynı sağlayıcı kullanılsa da pazarlama gönderimi ayrı alt alan adı ve ayrı akışla yapılır.',
     'scenario': 'Bülten, kampanya ya da otomasyon e-postası gönderilecekse. Pazarlama ekibinin Pazarlama › Mailing › Gönderim Aracı kararında seçtiği araçla uyumlu olmalıdır.',
     'example': 'Pazarlama ekibi Brevo\'yu kullanır; site abonelik formu Brevo\'daki listeye API ile yazar, çıkış ve iade olayları webhook ile siteye döner.',
     'rule': 'Toplu ve pazarlama e-postası sağlayıcısı: {label}. Sağlayıcı bir bağdaştırıcı (adapter) arkasında kullanılır; API anahtarı gizli değişken yönetiminde tutulur, liste ve şablon kimlikleri veritabanında eşlenir.',
     'recommend': [{'field': 'mk_mail_tool', 'map': {'mailchimp': ['mailchimp'], 'brevo': ['brevo'], 'euromsg': ['euromsg'], 'hubspot': ['platform'], 'klaviyo': ['platform'], 'own': ['own']}}],
     'options': [
         o('brevo', 'Brevo', 'Liste, kampanya, işlemsel e-posta ve otomasyon sunan Avrupa merkezli servis.', 'Küçük ve orta ölçekte bülten + otomasyon.', 'Site formu Brevo listesine yazar; kampanya Brevo\'dan gönderilir.',
           'Brevo listeleri ve kişileri API ile eşlenir; abonelik, çıkış, iade ve şikâyet olayları webhook ile alınır.'),
         o('mailchimp', 'Mailchimp', 'Kitle (audience), segment ve kampanya yönetimi sunan pazarlama platformu.', 'Pazarlama ekibinin Mailchimp\'te çalıştığı durumlar.', 'Abonelik formu Mailchimp kitlesine etiketle eklenir.',
           'Mailchimp kitle ve etiketleri API ile eşlenir; çift onay kullanılıyorsa kitle ayarında açılır, durum değişiklikleri webhook ile alınır.'),
         o('mailgun', 'Mailgun', 'Geliştirici odaklı, API ile yüksek hacimli gönderim servisi.', 'Kampanya arayüzü sistemin kendi panelinde olacaksa.', 'Toplu gönderim sitenin panelinden hazırlanır, Mailgun API\'siyle parça parça gönderilir.',
           'Mailgun ayrı gönderim alt alan adıyla kullanılır; olaylar imzalı webhook ile alınır, liste ve çıkış yönetimi sistemde tutulur.'),
         o('ses', 'Amazon SES', 'AWS üzerinde düşük maliyetli yüksek hacimli gönderim.', 'AWS altyapısı kullanan, kampanya arayüzünü kendisi yöneten projeler.', 'Gönderim SES üzerinden, iade ve şikâyet bildirimleri SNS ile kuyruğa düşer.',
           'SES yapılandırma kümesiyle (configuration set) kullanılır; iade ve şikâyet bildirimleri işlenip gönderilmeyecekler listesine yazılır.'),
         o('sendgrid', 'SendGrid', 'İşlemsel ve pazarlama gönderimi sunan servis.', 'İşlemsel e-postası da SendGrid\'de olan projeler (ayrı alt kullanıcı / alt alan adıyla).', 'Pazarlama gönderimi ayrı IP havuzu ve news. alt alan adıyla.',
           'Pazarlama ve işlemsel gönderim ayrı alt alan adı ve ayrı API anahtarıyla yapılır; olay webhook\'ları imza doğrulamasıyla işlenir.'),
         o('euromsg', 'EuroMsg (Relateddigital)', 'Türkiye merkezli e-posta ve SMS gönderim platformu.', 'Türkiye\'de yerel destek ve İYS entegrasyonu aranan kurumlar.', 'E-posta ve SMS aynı platformdan, İYS senkronuyla.',
           'Platformun İYS entegrasyonu kullanılsa da onay ve ret durumu sistemde de tutulur ve gönderimden önce kontrol edilir.'),
         o('platform', 'Pazarlama platformunun kendi gönderimi (HubSpot, Klaviyo …)', 'Gönderim, CRM / otomasyon platformunun yerleşik e-posta altyapısıyla yapılır.', 'Pazarlama ekibinin HubSpot ya da Klaviyo gibi bir platformda çalıştığı durumlar.', 'Site formları HubSpot\'a yazar, bülten HubSpot\'tan gider.',
           'Platform ana kayıt olur; site abonelik ve çıkış olaylarını API ile platforma yazar, platformdan gelen değişiklikleri webhook ile alır.'),
         o('own', 'Kendi gönderim altyapımız (önerilmez)', 'Kendi SMTP sunucusu ve IP\'leriyle toplu gönderim.', 'Mevzuat ya da sözleşme gereği verinin dışarı çıkamadığı istisnai durumlar.', 'Kendi posta sunucusu, kendi IP havuzu.',
           'Kendi altyapıda IP ısıtma, iade işleme, geri bildirim döngüleri ve itibar izleme ayrıca kurulur; bu yük kabul edilmeden toplu gönderim yapılmaz.'),
     ]},

    {'id': 'ml_subscription', 'section': 'biz_mailing', 'type': 'multiselect', 'label': 'Abonelik, Onay ve İYS', 'en': 'Subscription, Consent & IYS Sync',
     'agents': [KVKK, EMAIL, APP], 'showIf': ON_ML,
     'explanation': 'Kişinin listeye nasıl abone olacağını, onayın nasıl kanıtlanacağını, abonelik kategorilerini ve İleti Yönetim Sistemi (İYS) ile eşlemeyi belirler. Pazarlama tarafındaki izin kuralları Pazarlama › Mailing › İzin, Uyum ve Teslim Edilebilirlik kararındadır; bu karar onları uygulayan sistemi kurar.',
     'scenario': 'Sitede bülten ya da kampanya aboneliği toplanacaksa.',
     'example': 'Kullanıcı blogdaki formda "Haftalık bülten" ve "Etkinlik duyuruları"nı işaretler; doğrulama e-postasındaki bağlantıya tıklayınca abonelik etkinleşir ve onay İYS\'ye kaydedilir.',
     'rule': 'E-posta aboneliği kuralları: {labels}. Abonelik onay kutusu önceden işaretli gelmez, aydınlatma metninden ayrıdır; onay kaydında onay metninin sürümü, tarih-saat, kaynak sayfa ve IP tutulur.',
     'options': [
         o('categories', 'Abonelik kategorileri (önerilen)', 'Bülten, kampanya, etkinlik, ürün güncellemesi gibi ayrı abonelik konuları.', 'Birden çok e-posta türü gönderen projeler.', 'Tercih merkezinde: Bülten ✓, Kampanyalar ✗, Etkinlikler ✓.',
           'Her kategori için amaç, yasal dayanak ve kullanıcıya gösterilen açıklama tanımlanır; gönderim kategori bazında kontrol edilir.'),
         o('double_optin', 'Çift onay (double opt-in) (önerilen)', 'Abonelik, e-postadaki doğrulama bağlantısına tıklanınca etkinleşir.', 'Herkese açık abonelik formu olan her proje.', '“Aboneliğinizi onaylayın” e-postası; bağlantı 48 saat geçerli.',
           'Doğrulama belirteci rastgele, süreli ve tek kullanımlıktır; doğrulanmamış kayıt "beklemede" kalır ve gönderim listesine girmez, doğrulama tarihi, IP ve kullanıcı aracısı kaydedilir.'),
         o('iys_sync', 'İYS çift yönlü senkron', 'Sitede alınan onay ve retler İYS\'ye yazılır; İYS\'deki ret ve onay değişiklikleri sisteme alınır.', 'Türkiye\'de ticari elektronik ileti gönderen her işletme.', 'Kullanıcı İYS üzerinden ret verir; ertesi gönderimden önce sistemde de ret görünür.',
           'Onaylar İYS\'ye kaydedilir, İYS\'ye kaydedilmeyen onayla gönderim yapılmaz; İYS\'deki retler düzenli olarak ve gönderim öncesinde sorgulanır.'),
         o('pref_center', 'E-posta tercih merkezi', 'Kullanıcının kategori bazında abone olup çıkabildiği sayfa.', 'Birden çok kategori olan projeler.', 'E-postadaki “Tercihlerinizi yönetin” bağlantısı giriş gerektirmeden tercih sayfasını açar.',
           'Tercih sayfası imzalı ve süreli bağlantıyla giriş gerektirmeden açılır, yalnız o adresin tercihlerini gösterir; değişiklik kayda yazılır.'),
         o('form_protection', 'Form koruması', 'Abonelik formunda bot koruması, hız sınırı ve sahte kayıt engeli.', 'Herkese açık her abonelik formu.', 'Aynı IP\'den dakikada 5\'ten fazla abonelik denemesi engellenir.',
           'Abonelik formu bot koruması ve IP / e-posta başına hız sınırıyla korunur; aynı adres için tekrarlanan doğrulama e-postası sınırlanır.'),
         o('crm_sync', 'CRM ile eşleme', 'Abonelik durumu, kategoriler ve kaynak bilgisi CRM kişi kaydında görünür.', 'CRM modülü olan projeler.', 'CRM kişi kartında: “Bülten aboneliği — kaynak: blog formu, 12.03.2026”.',
           'Abonelik durumu CRM ile çift yönlü eşlenir; çakışmada en son ret kaydı geçerlidir.'),
     ]},

    {'id': 'ml_unsub', 'section': 'biz_mailing', 'type': 'multiselect', 'label': 'Abonelikten Çıkış ve Gönderilmeyecekler Listesi', 'en': 'Unsubscribe & Suppression List',
     'agents': [EMAIL, INT], 'showIf': ON_ML,
     'explanation': 'Abonelikten çıkışın nasıl çalışacağını ve gönderilmemesi gereken adreslerin (çıkan, kalıcı iade veren, şikâyet eden) tutulduğu merkezi listeyi belirler.',
     'scenario': 'Toplu e-posta gönderen her proje; Gmail ve Yahoo\'ya toplu gönderimde tek tıkla çıkış zorunludur.',
     'example': 'Gmail\'deki "Abonelikten çık" düğmesi List-Unsubscribe-Post başlığıyla sisteme POST gönderir; adres anında gönderilmeyecekler listesine eklenir ve servis sağlayıcısında da çıkar.',
     'rule': 'Abonelikten çıkış ve gönderilmeyecekler listesi: {labels}. Her toplu gönderimden hemen önce alıcı listesi gönderilmeyecekler listesine karşı süzülür.',
     'options': [
         o('one_click', 'Tek tıkla çıkış (RFC 8058) (önerilen)', 'İletide List-Unsubscribe (HTTPS adres) ve List-Unsubscribe-Post: List-Unsubscribe=One-Click başlıkları.', 'Pazarlama e-postası gönderen her proje.', 'Gmail ve Yahoo arayüzündeki “Abonelikten çık” düğmesi doğrudan çalışır.',
           'List-Unsubscribe başlığı alıcıya ve listeye özel, imzalı HTTPS adres içerir; çıkış yalnız POST isteğiyle yapılır (GET aboneliği iptal etmez), iki başlık DKIM imzasına dahildir.'),
         o('visible_link', 'Gövdede görünür çıkış bağlantısı', 'Her pazarlama e-postasının altında açıkça görünen “Abonelikten çık” bağlantısı.', 'Her pazarlama e-postası.', 'Alt bilgide: “Bu e-postaları almak istemiyorsanız abonelikten çıkın.”',
           'Gövdedeki çıkış bağlantısı tek adımda çıkış yapar ya da tercih merkezini açar; kullanıcıdan giriş ya da gerekçe istenmez.'),
         o('all_marketing', 'Tek işlemle bütün pazarlama e-postalarından çıkış', 'Kategori seçmek yerine bütün pazarlama e-postalarından birden çıkma seçeneği.', 'Birden çok kategori olan projeler.', 'Tercih sayfasında “Hiçbir pazarlama e-postası almak istemiyorum”.',
           'Bütün pazarlama kategorilerinden çıkış tek işlemle yapılır; işlemsel ve güvenlik e-postaları etkilenmez ve bu açıkça yazılır.'),
         o('suppression', 'Merkezi gönderilmeyecekler listesi', 'Çıkan, kalıcı iade veren ve şikâyet eden adreslerin gerekçe, tarih ve kaynakla tutulduğu liste.', 'Her toplu gönderim.', 'Listede: adres (maskeli), sebep: şikâyet, tarih, kaynak: sağlayıcı webhook.',
           'Gönderilmeyecekler listesi sistemde tutulur ve servis sağlayıcısıyla senkronlanır; adres karma değeriyle (hash) aranabilir, listeden çıkarma yalnız yeni açık onayla yapılır.'),
         o('bounce', 'İade (bounce) işleme', 'Kalıcı iade veren adres hemen, geçici iade veren adres eşik aşılınca gönderimden çıkarılır.', 'Liste temizliğinin teslim edilebilirliği etkilediği her proje.', '3 ardışık geçici iadeden sonra adres 30 gün askıya alınır.',
           'Kalıcı iade (hard bounce) adresi anında gönderilmeyecekler listesine eklenir; geçici iade (soft bounce) sayılır, tanımlı eşikte adres askıya alınır.'),
         o('complaint', 'Şikâyet işleme', 'Alıcının "spam" olarak işaretlemesi (geri bildirim döngüsü) gelince pazarlama gönderimi durur.', 'Toplu gönderim yapan her proje.', 'Şikâyet eden kişiye bir daha kampanya gitmez, CRM\'de “şikâyet” etiketi görünür.',
           'Şikâyet olayı alınan adrese pazarlama e-postası gönderimi kalıcı olarak durdurulur ve olay CRM\'e işlenir.'),
         o('webhooks', 'Servis sağlayıcısı olay webhook\'ları', 'Teslim, açılma, tıklama, iade, şikâyet ve çıkış olaylarının sisteme alınması.', 'Servis sağlayıcısı kullanan her proje.', 'Olay: “unsubscribed — kampanya: Mart bülteni” sisteme işlendi.',
           'Webhook istekleri sağlayıcı imzasıyla doğrulanır, olay kimliğiyle tekilleştirilir ve kuyrukta işlenir; çıkış olayı aboneliği, iade ve şikâyet olayı gönderilmeyecekler listesini günceller.'),
     ]},

    {'id': 'ml_deliverability', 'section': 'biz_mailing', 'type': 'multiselect', 'label': 'Alan Adı Kimlik Doğrulama ve Teslim Edilebilirlik', 'en': 'Domain Authentication & Deliverability',
     'agents': [SRE, EMAIL], 'showIf': ON_ML,
     'explanation': 'Pazarlama e-postalarının gönderildiği alan adının SPF, DKIM ve DMARC ile nasıl doğrulanacağını ve gönderim itibarının nasıl korunacağını belirler. Ana gönderici alan adı Sunucu & Altyapı › Gönderici Alan Adı kararındadır.',
     'scenario': 'Toplu gönderim yapan her proje; Gmail\'e günde 5.000 ve üzeri ileti gönderenler için SPF, DKIM ve DMARC birlikte zorunludur.',
     'example': 'Bülten news.ornek.com alt alan adından gider; DNS\'te SPF ve DKIM kayıtları, _dmarc kaydı p=none ile başlar, raporlar iki hafta izlendikten sonra quarantine\'e geçilir.',
     'rule': 'Pazarlama e-postası kimlik doğrulama ve teslim edilebilirlik kuralları: {labels}. Kimlik doğrulaması tamamlanmamış alan adından toplu gönderim yapılmaz.',
     'options': [
         o('spf_dkim', 'SPF ve DKIM (önerilen)', 'Gönderim sunucularının SPF kaydı ve iletilerin DKIM imzası.', 'Her toplu gönderim.', 'DNS\'te sağlayıcının DKIM CNAME kayıtları ve SPF include.',
           'Gönderici alan adında SPF ve DKIM birlikte kurulur; DKIM anahtarı en az 2048 bit olur ve dönemsel olarak yenilenir.'),
         o('dmarc', 'DMARC politikası ve hizalama (önerilen)', 'DMARC kaydı yayımlanır; From alan adı SPF ya da DKIM alan adıyla hizalanır.', 'Her toplu gönderim.', '_dmarc.ornek.com: v=DMARC1; p=none; rua=mailto:… → izlemeden sonra p=quarantine.',
           'DMARC kaydı p=none ve rapor adresiyle başlar, raporlar izlenip meşru kaynaklar hizalandıktan sonra quarantine ya da reject\'e geçilir; From alan adı DKIM ya da SPF alan adıyla hizalıdır.'),
         o('subdomain', 'Pazarlama için ayrı alt alan adı', 'Pazarlama gönderimi işlemsel e-postadan ayrı bir alt alan adından yapılır.', 'Hem işlemsel hem pazarlama e-postası gönderen projeler.', 'İşlemsel: mail.ornek.com, pazarlama: news.ornek.com.',
           'Pazarlama e-postası ayrı alt alan adından gönderilir; böylece kampanya şikâyetleri işlemsel e-posta itibarını etkilemez.'),
         o('postmaster', 'Spam oranı ve itibar izleme', 'Google Postmaster Tools ve sağlayıcı raporlarıyla şikâyet oranı ve itibar izlenir.', 'Gmail\'e düzenli toplu gönderim yapan projeler.', 'Panelde haftalık: şikâyet oranı %0,04, iade oranı %0,8.',
           'Şikâyet oranı %0,1 altında tutulur, %0,3\'e yaklaşırsa toplu gönderim durdurulup liste ve içerik incelenir; iade ve şikâyet oranları gönderim başına raporlanır.'),
         o('warmup', 'Kademeli ısıtma', 'Yeni alan adı ya da IP\'de gönderim hacmi günler içinde kademeli artırılır.', 'Yeni alan adı, yeni sağlayıcı ya da yeni ayrılmış IP.', 'İlk hafta en etkileşimli 2.000 aboneye, sonraki hafta 10.000\'e.',
           'Yeni alan adı ya da IP\'de gönderim en etkileşimli abonelerden başlayarak kademeli artırılır; hata ve şikâyet oranı yükselirse artış durdurulur.'),
         o('hygiene', 'Etkileşimsiz abone temizliği', 'Uzun süre etkileşim olmayan aboneler yeniden onaya çağrılır ya da listeden çıkarılır.', 'Eski ve büyük listeler.', '12 ay hiç açmayan abonelere “Bülteni almaya devam etmek istiyor musunuz?” e-postası.',
           'Tanımlı süre etkileşimsiz aboneler yeniden onay kampanyasına alınır, yanıt vermeyenler pazarlama gönderiminden çıkarılır.'),
     ]},

    {'id': 'ml_bulk', 'section': 'biz_mailing', 'type': 'multiselect', 'label': 'Toplu Gönderim Kontrolleri', 'en': 'Bulk Send Controls',
     'agents': [APP, EMAIL], 'showIf': ON_ML,
     'explanation': 'Toplu gönderim başlamadan önce ve gönderim sırasında hangi kontrollerin zorunlu olacağını belirler. Konu ve içerik A/B testleri Pazarlama › Mailing › A/B Testi kararındadır.',
     'scenario': 'Panelden kampanya gönderimi yapılan her proje.',
     'example': 'Gönder düğmesine basılınca sistem "12.430 alıcı → 11.982 uygun (İYS reddi 301, gönderilmeyecekler 147)" özetini gösterir; pazarlama müdürü onaylayınca gönderim 20:00\'de parça parça başlar.',
     'rule': 'Toplu gönderim kontrolleri: {labels}. Gönderim durumu Taslak → Onay Bekliyor → Zamanlandı → Gönderiliyor → Gönderildi / Başarısız akışıyla yönetilir; gönderim işi idempotent çalışır, yeniden başlatılınca aynı alıcıya ikinci kez göndermez.',
     'options': [
         o('preflight', 'Gönderim öncesi uygunluk özeti (önerilen)', 'İzin, İYS, gönderilmeyecekler listesi ve doğrulanmış alan adı kontrolünün sonucu gönderimden önce gösterilir.', 'Her toplu gönderim.', '“11.982 uygun, 448 hariç (nedenleriyle)”.',
           'Gönderim öncesi alıcılar onay, İYS, gönderilmeyecekler listesi ve kategori aboneliğine göre süzülür; hariç tutulanların sayısı nedenleriyle gösterilir, alan adı doğrulanmamışsa gönderim başlatılamaz.'),
         o('approval', 'Gönderim onayı', 'Toplu gönderim, hazırlayandan farklı yetkili bir kişi onaylamadan başlamaz.', 'Kurum adına geniş kitleye giden her kampanya.', 'Uzman hazırlar, pazarlama müdürü onaylar.',
           'Toplu gönderim hazırlayandan farklı yetkili kişinin onayıyla başlar; onaydan sonra içerik ya da alıcı listesi değişirse yeniden onay gerekir.'),
         o('test_send', 'Zorunlu test gönderimi', 'Gerçek gönderimden önce iç alıcılara test gönderimi.', 'Her kampanya.', 'Test e-postası farklı istemcilerde (Gmail, Outlook, mobil) kontrol edilir.',
           'Gerçek gönderimden önce en az bir test gönderimi iç alıcılara yapılır ve kayda geçer.'),
         o('schedule', 'Zamanlama ve saat dilimi', 'Gönderim ileri tarih ve saate planlanır, alıcının saat dilimi dikkate alınır.', 'Farklı saat dilimlerine gönderim ya da sabah / akşam ritmi olan bültenler.', 'Perşembe 10:00 (alıcının yerel saati).',
           'Zamanlanmış gönderim sunucu saatine göre çalışır, saat dilimi açıkça saklanır; zamanlanmış gönderim başlamadan önce iptal edilebilir.'),
         o('throttle', 'Parça parça gönderim', 'Gönderim sağlayıcı sınırına ve ısıtma planına göre parçalara bölünür.', 'Büyük listeler.', '100.000 alıcı saatte 20.000\'lik dilimlerle.',
           'Toplu gönderim parçalara bölünür, sağlayıcının hız sınırına uyulur; hata oranı eşiği aşılırsa gönderim kendiliğinden duraklar.'),
     ]},
]

# =====================================================================================================
# B8 — Sosyal Medya Paylaşım Modülü
# =====================================================================================================
SEC_SP = {
    'id': 'biz_social', 'group': 'İş Modülleri', 'icon': '⧉',
    'name': 'Sosyal Medya Paylaşım Modülü', 'en': 'Social Media Publishing Module',
    'desc': 'Kurumsal sosyal medya hesaplarının panele resmî API\'lerle bağlanmasını, gönderilerin hazırlanmasını, planlanmasını, onaylanmasını ve zamanı gelince otomatik yayınlanmasını; bağlantı sağlığını, platform sınırlarını ve hataları yapılandırır.',
    'guide': {
        'purpose': 'Hangi mecralarda, hangi formatta ve hangi sıklıkta paylaşım yapılacağı Pazarlama › Sosyal Medya bölümünde, Meta hesaplarının kurulumu Meta Servisleri menüsünde belirlenir. Bu bölüm, sitedeki içeriklerden (blog, ürün, etkinlik) gönderi taslağı üreten, onaydan geçen gönderiyi platformun resmî yayın API\'siyle zamanında paylaşan ve sonucunu izleyen teknik modülü kurar. Her platformun yayın API\'si farklı izin, hesap türü ve sınır koşullarına bağlıdır: Instagram\'da yalnız profesyonel hesaplar, LinkedIn şirket sayfasında yalnız sayfa rolü olan yöneticiler paylaşım yapabilir; TikTok\'ta denetimden geçmemiş uygulamanın gönderileri yalnız özel görünür.',
        'criteria': [
            'Her platform ayrı bir kanal bağdaştırıcısıdır; yalnız platformun resmî yayın API\'si kullanılır, tarayıcı otomasyonu ya da şifre saklama ile paylaşım yapılmaz.',
            'Hesap bağlama yalnız yetkili yönetici tarafından OAuth ile yapılır; istenen izin kapsamı kullanıcıya gösterilir ve en az yetki ilkesine göre seçilir.',
            'Erişim ve yenileme belirteçleri şifreli saklanır, loglara ve arayüze yazılmaz; süre sonu ve bağlantı kopması panelde uyarı olarak görünür.',
            'Onay gerektiren gönderi onaylanmadan yayın kuyruğuna girmez; yayın işi idempotent çalışır, yeniden deneme aynı gönderiyi iki kez paylaşmaz.',
            'Gönderi metni ve medyası kaydedilirken platformun karakter, dosya türü, boyut ve süre sınırlarına göre doğrulanır.',
            'Gönderi bağlantıları UTM standardına göre etiketlenir; yayın sonucu (gönderi kimliği, bağlantı, hata) kayda yazılır.',
        ],
        'pitfalls': [
            'Kişisel hesap şifresini sistemde saklayıp otomasyonla paylaşım yapmak: platform kurallarına aykırıdır, hesap kapatılabilir ve şifre sızıntısı riski doğar.',
            'Instagram kişisel hesabının ya da yetkisi olmayan LinkedIn kullanıcısının API ile paylaşım yapabileceğini varsaymak.',
            'Platform uygulama incelemesi (App Review / audit) süresini plana koymamak: denetimden geçmeyen TikTok istemcisinin gönderileri yalnız özel görünür.',
            'Yapay zekâ ile üretilen gönderiyi insan onayı olmadan yayınlamak.',
            'Hız sınırı (429) hatasında hemen yeniden denemek: kota daha hızlı tükenir; bekleme süresine uyulmalıdır.',
            'API sürüm sonu tarihlerini izlememek: LinkedIn gibi sürümlü API\'lerde eski sürüm kapanınca paylaşım sessizce durur.',
        ],
        'resources': [
            {'title': 'Meta — Instagram Content Publishing', 'url': 'https://developers.facebook.com/docs/instagram-platform/content-publishing', 'note': 'Yalnız Instagram profesyonel hesapları; tek görsel (JPEG), video, Reels, carousel ve Story yayını; 24 saatlik gönderi sınırı.'},
            {'title': 'Meta — Pages API: Posts', 'url': 'https://developers.facebook.com/docs/pages-api/posts', 'note': 'Facebook Sayfası\'na gönderi için pages_manage_posts izni ve sayfa erişim belirteci; zamanlama 10 dakika ile 30 gün arası.'},
            {'title': 'Meta — Threads API: Posts', 'url': 'https://developers.facebook.com/docs/threads/posts', 'note': 'threads_content_publish izni, iki adımlı yayın ve 24 saatte 250 gönderi sınırı.'},
            {'title': 'LinkedIn — Posts API', 'url': 'https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api', 'note': 'Şirket sayfası adına paylaşım için w_organization_social ve sayfa rolü (Administrator, Content Admin); sürüm başlığı ve sürüm sonu tarihleri.'},
            {'title': 'LinkedIn — Share on LinkedIn', 'url': 'https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin', 'note': 'Kişisel profil adına paylaşım için w_member_social izni.'},
            {'title': 'TikTok — Content Posting API', 'url': 'https://developers.tiktok.com/doc/content-posting-api-get-started', 'note': 'video.publish izni; denetimden geçmemiş istemcinin gönderileri yalnız özel görünür; fotoğraf gönderisi desteği.'},
            {'title': 'X — Create Post', 'url': 'https://docs.x.com/x-api/posts/create-post', 'note': 'OAuth 2.0 kullanıcı bağlamı ve tweet.write izniyle gönderi oluşturma.'},
            {'title': 'YouTube Data API — videos.insert', 'url': 'https://developers.google.com/youtube/v3/docs/videos/insert', 'note': 'Video yükleme, gizlilik durumu, zamanlı yayın (publishAt) ve kota.'},
            {'title': 'Google Business Profile — Posts', 'url': 'https://developers.google.com/my-business/content/posts-data', 'note': 'Etkinlik, teklif ve eylem çağrılı işletme gönderileri; ürün gönderisinin API ile oluşturulamadığı.'},
        ],
    },
}

F_SP = [
    {'id': 'sp_platforms', 'section': 'biz_social', 'type': 'multiselect', 'label': 'API ile Paylaşım Yapılacak Platformlar', 'en': 'Publishing Platforms (Official APIs)',
     'agents': [SOCIAL, INT], 'showIf': ON_SP,
     'explanation': 'Panelden otomatik paylaşım yapılacak platformları belirler. Yalnız platformun resmî yayın API\'sinin izin verdiği hesap türleri ve formatlar desteklenir; mecra stratejisi Pazarlama › Sosyal Medya › Mecralar kararındadır.',
     'scenario': 'Pazarlama ekibi her gün birden çok platformda paylaşım yapıyor ve gönderileri siteden / panelden planlamak istiyorsa.',
     'example': 'Blog yazısı yayımlanınca LinkedIn şirket sayfası, Facebook Sayfası ve Instagram için ayrı metin ve görselli üç taslak oluşur; onaydan sonra her biri planlanan saatte paylaşılır.',
     'rule': 'Sosyal medya paylaşım platformları: {labels}. Her platform resmî yayın API\'siyle ve ayrı bir bağdaştırıcıyla bağlanır; platformun desteklemediği format panelde pasif gösterilir, desteklenmeyen hesap türü bağlanmaz.',
     'recommend': [{'field': 'mk_platforms', 'map': {'instagram': ['instagram'], 'facebook': ['facebook_page'], 'linkedin': ['linkedin_org'], 'x': ['x'], 'youtube': ['youtube'], 'tiktok': ['tiktok'], 'threads': ['threads'], 'google': ['gbp']}}],
     'options': [
         o('facebook_page', 'Facebook Sayfası', 'Pages API ile Sayfa adına metin, bağlantı, görsel ve video gönderisi.', 'Facebook Sayfası olan işletmeler.', 'Gönderi panelde planlanır, Facebook\'ta Sayfa adına yayımlanır.',
           'Facebook Sayfası\'na sayfa erişim belirteci ve pages_manage_posts izniyle gönderilir; platformun yerel zamanlaması kullanılırsa yayın zamanı istekten 10 dakika ile 30 gün sonrası arasında olmalıdır.'),
         o('instagram', 'Instagram (yalnız profesyonel hesap)', 'Instagram profesyonel hesabına tek görsel, video, Reels, carousel ve Story yayını.', 'İşletme ya da içerik üreticisi hesabı olan markalar.', 'Carousel gönderi: 6 görsel, açıklama ve etiketler; planlanan saatte yayınlanır.',
           'Yalnız Instagram profesyonel hesapları bağlanır; görseller JPEG olarak, medya herkese açık erişilebilir geçici adresten verilir; 24 saatlik API gönderi sınırı izlenir, carousel tek gönderi sayılır.'),
         o('linkedin_org', 'LinkedIn şirket sayfası', 'Posts API ile şirket sayfası adına gönderi.', 'Kurumsal (B2B) iletişim yapan şirketler.', 'Şirket sayfasında duyuru, belge (PDF) ya da görsel gönderisi.',
           'LinkedIn şirket sayfası w_organization_social izniyle, sayfada Administrator ya da Content Admin rolü olan kullanıcının bağlantısıyla paylaşılır; istekler Linkedin-Version başlığı taşır ve kullanılan API sürümünün sona erme tarihi izlenir.'),
         o('linkedin_member', 'LinkedIn kişisel profil', 'Share on LinkedIn ile yetkilendiren kişinin kendi profilinde paylaşım.', 'Yöneticilerin ya da uzmanların kendi profillerinden kurumsal içerik paylaştığı durumlar.', 'Genel müdür kendi hesabını bağlar; onaylanan gönderi onun profilinde yayınlanır.',
           'Kişisel profil yalnız sahibinin kendi OAuth onayıyla (w_member_social) bağlanır; kişi bağlantıyı istediği an kaldırabilir ve onun adına yalnız onun onayladığı gönderi yayınlanır.'),
         o('x', 'X', 'X API ile gönderi oluşturma.', 'X\'te düzenli paylaşım yapan markalar.', 'Etkinlik duyurusu, bağlantı ve görselle.',
           'X gönderileri OAuth 2.0 kullanıcı bağlamı ve tweet.write izniyle oluşturulur; API kullanımının ücretli olduğu ve erişim düzeyine bağlı sınırlar bütçe ve plana yazılır.'),
         o('tiktok', 'TikTok', 'Content Posting API ile video ve fotoğraf gönderisi.', 'Kısa video üreten markalar.', 'Ürün tanıtım videosu planlanır, TikTok\'ta yayınlanır.',
           'TikTok gönderileri video.publish izniyle yapılır; uygulama TikTok denetiminden geçene kadar gönderiler yalnız özel görünür, bu süre canlıya çıkış planına yazılır.'),
         o('youtube', 'YouTube', 'YouTube Data API ile video yükleme ve zamanlı yayın.', 'Video içerik üreten kurumlar.', 'Video özel olarak yüklenir, publishAt ile belirlenen saatte herkese açılır.',
           'YouTube\'a videos.insert ile yüklenir; günlük kota izlenir, zamanlı yayın publishAt ile yapılır ve yapay zekâ ile üretilmiş gerçekçi içerik ilgili alanla beyan edilir.'),
         o('threads', 'Threads', 'Threads API ile metin, görsel, video ve carousel gönderisi.', 'Threads\'te paylaşım yapan markalar.', 'Kısa duyuru metni ve görsel.',
           'Threads gönderileri threads_content_publish izniyle, iki adımlı (kapsayıcı oluştur → yayınla) akışla yapılır; 24 saatlik gönderi sınırı izlenir.'),
         o('gbp', 'Google İşletme Profili gönderileri', 'Google Business Profile API ile etkinlik, teklif ve eylem çağrılı gönderi.', 'Yerel işletmeler ve şubeli markalar.', 'Şube profilinde “Yeni yıl indirimi — Teklif” gönderisi, “Rezervasyon yap” düğmesiyle.',
           'İşletme Profili gönderileri konum başına localPosts uç noktasıyla yapılır; ürün gönderisi API ile oluşturulamadığı için bu tür panelde pasif gösterilir.'),
     ]},

    {'id': 'sp_connection', 'section': 'biz_social', 'type': 'multiselect', 'label': 'Hesap Bağlantısı ve Belirteç Güvenliği', 'en': 'Account Connection & Token Security',
     'agents': [KINT, APP], 'showIf': ON_SP,
     'explanation': 'Sosyal medya hesaplarının panele nasıl bağlanacağını, erişim belirteçlerinin (token) nasıl saklanıp yenileneceğini ve bağlantı sağlığının nasıl izleneceğini belirler.',
     'scenario': 'Panelden en az bir sosyal hesap bağlanacaksa; birden çok marka ya da şube hesabı varsa özellikle.',
     'example': 'Hesaplar ekranında "Instagram — @marka — Bağlı — belirteç 12 gün sonra yenilenmeli" satırı ve "Yeniden yetkilendir" düğmesi.',
     'rule': 'Sosyal hesap bağlantı kuralları: {labels}. Sosyal medya şifreleri hiçbir koşulda istenmez ve saklanmaz; bağlantı yalnız platformun resmî OAuth akışıyla kurulur.',
     'options': [
         o('oauth_scope', 'Resmî OAuth ve en az izin (önerilen)', 'Bağlantı platformun OAuth akışıyla kurulur; yalnız gereken izinler istenir ve kullanıcıya gösterilir.', 'Her bağlantı.', '“Bu bağlantı yalnız Sayfanıza gönderi yayınlama ve gönderi istatistiklerini okuma izni ister.”',
           'OAuth akışında state parametresi ve PKCE (destekleyen platformda) kullanılır; istenen izinler en az yetkiyle sınırlanır ve bağlantı ekranında listelenir.'),
         o('token_vault', 'Şifreli belirteç saklama', 'Erişim ve yenileme belirteçleri uygulama veritabanında şifreli, anahtarı ayrı yönetilerek saklanır.', 'Her bağlantı.', 'Veritabanında belirteç alanı şifreli; arayüzde yalnız “bağlı” durumu görünür.',
           'Belirteçler alan düzeyinde şifrelenir, şifreleme anahtarı gizli değişken / anahtar yönetiminde tutulur; belirteç loglara, hata mesajlarına ve arayüze yazılmaz.'),
         o('refresh_health', 'Yenileme ve bağlantı sağlığı', 'Belirteç süre sonu izlenir, otomatik yenilenir; kopan bağlantı panelde uyarı olur.', 'Uzun süre kullanılacak her bağlantı.', 'Panel: “LinkedIn bağlantısı 5 gün içinde sona erecek — yeniden yetkilendirin.”',
           'Belirteçler süresi dolmadan yenilenir; yenilenemeyen bağlantı "yeniden yetkilendirme gerekli" durumuna alınır, o hesaba planlanmış gönderiler yayından önce sorumluya bildirilir.'),
         o('admin_only', 'Yalnız yetkili yönetici bağlar', 'Hesap bağlama ve kaldırma ayrı bir izindir; bağlayan kişi ve tarih kaydedilir.', 'Birden çok kullanıcının panelde çalıştığı projeler.', 'Uzman gönderi hazırlayabilir ama hesap bağlayamaz; bağlantıyı sosyal medya yöneticisi kurar.',
           'Hesap bağlama, kaldırma, gönderi oluşturma, onaylama ve yayınlama ayrı yetkilerdir; kullanıcı yalnız yetkili olduğu marka ve hesaplar için işlem yapar.'),
         o('review_status', 'Uygulama incelemesi takibi', 'Platformların uygulama incelemesi / denetim durumu ve izin onayları izlenir.', 'Meta, TikTok, LinkedIn gibi izin onayı isteyen platformlar.', 'Panel: “TikTok — denetim bekleniyor, gönderiler yalnız özel görünür.”',
           'Her platform için uygulama incelemesi, onaylanan izinler ve kısıtlar kayıtta tutulur ve panelde gösterilir; inceleme tamamlanmadan canlı paylaşım planlanmaz.'),
         o('revoke', 'Bağlantı kaldırmada belirteç iptali', 'Bağlantı kaldırılınca belirteç platformda iptal edilir ve sistemden silinir.', 'Her bağlantı; çalışan ayrıldığında özellikle.', 'Çalışan ayrılınca kişisel LinkedIn bağlantısı kaldırılır, belirteç silinir.',
           'Bağlantı kaldırılınca belirteç platformun iptal uç noktasıyla (varsa) geçersiz kılınır ve veritabanından silinir; işlem kayda yazılır.'),
     ]},

    {'id': 'sp_publishing', 'section': 'biz_social', 'type': 'multiselect', 'label': 'Gönderi Hazırlama, Onay ve Yayın', 'en': 'Post Composition, Approval & Publishing',
     'agents': [SOCIAL, APP], 'showIf': ON_SP,
     'explanation': 'Gönderilerin hangi kaynaklardan üretileceğini, nasıl doğrulanıp onaylanacağını, takvimde nasıl planlanacağını, yayın hatasında ne olacağını ve performansın nasıl izleneceğini belirler.',
     'scenario': 'Sosyal medya paylaşımının panelden planlanıp birden çok kişinin onayından geçtiği projeler.',
     'example': 'Etkinlik sayfası yayımlanınca "Sosyal gönderi oluştur" düğmesi başlık, görsel ve UTM\'li bağlantıyla taslak üretir; takvimde Salı 10:00\'a yerleşir, pazarlama müdürü onaylayınca yayın kuyruğuna girer.',
     'rule': 'Sosyal medya gönderi kuralları: {labels}. Gönderi durumu Taslak → Onay Bekliyor → Zamanlandı → Yayınlandı / Başarısız / İptal akışıyla yönetilir.',
     'options': [
         o('sources', 'Site içeriklerinden taslak (önerilen)', 'Blog, ürün, etkinlik ve duyurulardan başlık, görsel ve bağlantıyla gönderi taslağı.', 'İçerik yayımlayan her site.', 'Blog yazısının kartında “Sosyal gönderi oluştur”.',
           'İçerik kaydından üretilen taslak kaynağına bağlı tutulur; kaynak içerik yayından kalkarsa planlanmış gönderi beklemeye alınır.'),
         o('validate', 'Platforma göre metin ve medya doğrulaması', 'Platform başına ayrı metin ve medya; karakter, oran, boyut, süre sınırları kayıtta denetlenir.', 'Birden çok platforma aynı içerik gönderiliyorsa.', '“X için metin sınırı aşıldı” ve “Instagram görseli JPEG olmalı” uyarıları.',
           'Her platform için metin, medya ve alternatif metin ayrı tutulur; platform sınırına uymayan gönderi kaydedilir ama zamanlanamaz.'),
         o('calendar', 'Takvim ve zamanlama', 'Gönderiler gün / hafta / ay takviminde, marka, platform, kampanya ve duruma göre süzülerek planlanır.', 'Düzenli paylaşım yapan ekipler.', 'Haftalık takvimde 9 gönderi; sürükleyerek saat değiştirme.',
           'Yayın zamanı markanın saat dilimiyle saklanır ve sunucuda zamanlanmış işle tetiklenir; yayından önce sorumluya hatırlatma gider.'),
         o('approval', 'Onaysız yayın yok', 'Gönderi, yetkili onaylayıcı onaylamadan yayın kuyruğuna girmez.', 'Kurum adına yayın yapan, regüle sektörde çalışan projeler.', 'Uzman hazırlar, kurumsal iletişim sorumlusu onaylar; hukuk onayı gereken kampanyada ikinci onay.',
           'Onay gerektiren hesaplarda gönderi hazırlayandan farklı yetkili kişinin onayıyla zamanlanır; onaydan sonra metin ya da medya değişirse onay düşer (İş Akışları ve Onay Mekanizmaları modülü varsa onun kurallarıyla).'),
         o('ai_draft', 'Yapay zekâ taslağı insan onayıyla', 'Yapay zekâ metin önerisi üretir; insan onayı olmadan yayınlanmaz.', 'Yapay zekâ ile metin varyasyonu üretilen projeler.', '“Öneri üret” → 3 metin varyasyonu; editör birini seçip düzenler.',
           'Yapay zekâ çıktısı yalnız taslak olarak kaydedilir; marka tonu ve yasaklı ifade kuralları uygulanır, kaynak içerik, çıktı, tarih ve kullanıcı kayda yazılır, insan onayı olmadan yayınlanmaz.'),
         o('utm', 'Otomatik UTM', 'Gönderideki site bağlantılarına UTM etiketleri otomatik eklenir.', 'Sosyal medyadan gelen trafiğin ölçüldüğü her proje.', 'Bağlantı: …?utm_source=linkedin&utm_medium=social&utm_campaign=bahar-2026.',
           'Bağlantılar Pazarlama › UTM Standardı kararındaki şemaya göre etiketlenir; kişisel veri UTM\'ye yazılmaz.'),
         o('retry', 'Hata yönetimi ve idempotent yayın', 'Yayın hatası kayda yazılır, geçici hatada beklenip yeniden denenir, sorumluya bildirilir.', 'Her otomatik yayın.', '“Instagram: medya işleniyor (bekle 60 sn)” → ikinci denemede yayınlandı.',
           'Yayın işi gönderi kimliğine bağlı idempotency anahtarıyla çalışır; 429 ve geçici hatalarda platformun bildirdiği bekleme süresine uyulur, kalıcı hatada gönderi "Başarısız" olur ve sorumluya bildirilir; platformun hata yanıtı kullanıcıya anlaşılır mesajla gösterilir.'),
         o('metrics', 'Performans verisi', 'Erişim, etkileşim ve tıklama verileri platformların izin verdiği ölçüde çekilir.', 'Sosyal medya raporlaması yapılan projeler.', 'Gönderi kartında: gösterim 4.210, etkileşim 186, tıklama 52.',
           'Performans verisi yalnız platform API\'sinin sunduğu metriklerle ve izin kapsamı içinde, sınırlı sıklıkta çekilir; gönderiden gelen talepler UTM ile CRM\'e bağlanır.'),
     ]},
]

# =====================================================================================================
# B9 — Pazarlama Otomasyonu ve Müşteri Yolculukları
# =====================================================================================================
SEC_MO = {
    'id': 'biz_automation', 'group': 'İş Modülleri', 'icon': '∞',
    'name': 'Pazarlama Otomasyonu ve Müşteri Yolculukları', 'en': 'Marketing Automation & Customer Journeys',
    'desc': 'Kullanıcı davranışı ve kayıt değişikliklerine göre çalışan otomatik akışların (müşteri yolculuğu / journey) aracını, tetikleyicilerini, aksiyonlarını, izin ve baskı korumalarını, sürümlemesini ve ölçümünü yapılandırır.',
    'guide': {
        'purpose': 'Pazarlama otomasyonu doğru kişiye doğru zamanda doğru mesajı göndermeyi sağlar; yanlış kurulduğunda ise onaysız kişiye ileti gönderen, aynı kişiyi beş akıştan birden bombardımana tutan ve kimsenin fark etmediği hatalarla çalışan bir makineye dönüşür. Bu bölüm akışın hangi araçta çalışacağını, hangi olaylarla tetikleneceğini, hangi aksiyonları yapabileceğini ve her adımda uygulanacak korumaları (izin kontrolü, çıkışta akıştan çıkma, sıklık sınırı, sessiz saat, sürümleme, onay) belirler. Mesajlar Bildirim Merkezi ve E-posta Aboneliği modülleri seçiliyse onların üzerinden gider; bülten ve kampanya içeriği Pazarlama menüsündedir.',
        'criteria': [
            'Her mesaj adımı gönderimden hemen önce kişinin güncel iznini, İYS durumunu ve gönderilmeyecekler listesini yeniden kontrol eder; akışa girerken alınan izin yeterli sayılmaz.',
            'Kişi abonelikten çıkınca ya da hedef eylemi yapınca (ör. sepeti tamamlayınca) ilgili akıştan kendiliğinden çıkar.',
            'Akışlar arası sıklık sınırı ve öncelik kuralı vardır; aynı kişi aynı gün birden çok akıştan pazarlama iletisi almaz.',
            'Etkin akıştaki değişiklik yeni sürüm açar; akıştaki kişiler girdikleri sürümle devam eder, değişiklik kayda yazılır.',
            'Harici sistemlere çağrı (webhook) yapan adımlar yalnız izinli adres listesine, zaman aşımı ve imzayla gider.',
            'Her akışın giriş, tamamlanma, çıkış, dönüşüm ve hata sayıları raporlanır; mümkünse kontrol grubuyla gerçek etki ölçülür.',
        ],
        'pitfalls': [
            'İzni akışa girişte bir kez kontrol edip üç gün sonraki e-postada yeniden kontrol etmemek: arada ret veren kişiye ileti gider.',
            'Sepet terki ya da sayfa ziyareti gibi davranış tetikleyicilerini analitik / çerez izni olmayan kişilerde kullanmak.',
            'Akışlar arası çakışmayı yönetmemek: hoş geldin, sepet terki ve kampanya akışları aynı gün aynı kişiye ayrı ayrı yazar.',
            'Etkin akışı yerinde düzenlemek: akışın ortasındaki kişiler var olmayan adıma takılır ya da adımı iki kez yaşar.',
            'Otomasyon hatalarını izlememek: başarısız webhook ya da şablon hatası haftalarca fark edilmez.',
            'Kontrol grubu olmadan "otomasyon şu kadar satış getirdi" demek: akış olmasa da gerçekleşecek satışlar otomasyona yazılır.',
        ],
        'resources': [
            R_6563,
            R_YON,
            R_IYS,
            R_GSND,
            {'title': 'OWASP — Server-Side Request Forgery Prevention Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html', 'note': 'Kullanıcının tanımladığı webhook / harici API adreslerine sunucudan istek atarken izinli adres listesi ve iç ağ engeli.'},
            {'title': 'HubSpot — Create workflows', 'url': 'https://knowledge.hubspot.com/workflows/create-workflows', 'note': 'Tetikleyici, gecikme, dallanma ve aksiyonlarla iş akışı kurma; hazır platform kullanılacaksa başvuru.'},
            {'title': 'n8n Docs', 'url': 'https://docs.n8n.io/', 'note': 'Kendi sunucusunda çalıştırılabilen iş akışı otomasyon aracı; teknik entegrasyon akışları için.'},
        ],
    },
}

F_MO = [
    {'id': 'mo_engine', 'section': 'biz_automation', 'type': 'select', 'label': 'Otomasyon Aracı', 'en': 'Automation Engine',
     'agents': [AUTO, KINT], 'showIf': ON_MO,
     'explanation': 'Müşteri yolculuklarının hangi araçta tasarlanıp çalıştırılacağını belirler: sistemin içinde yerleşik bir akış motoru, hazır bir pazarlama otomasyonu platformu ya da teknik iş akışı aracı.',
     'scenario': 'Form, sepet, kayıt, randevu ya da teklif gibi olaylara göre otomatik ileti ve görev oluşturulacaksa.',
     'example': 'HubSpot seçilirse site formları ve sipariş olayları HubSpot\'a gönderilir, akışlar orada kurulur; yerleşik motor seçilirse panelde sürükle-bırak akış düzenleyici olur.',
     'rule': 'Pazarlama otomasyonu aracı: {label}. Sistem olayları (form, kayıt, sipariş, randevu …) şemalı ve sürümlü olay olarak yayımlanır; araç bu olayları tüketir, kişisel veri yalnız gereken alanlarla aktarılır.',
     'recommend': [{'field': 'mk_mail_tool', 'map': {'hubspot': ['hubspot'], 'brevo': ['brevo'], 'klaviyo': ['klaviyo'], 'own': ['builtin']}}],
     'options': [
         o('builtin', 'Yerleşik akış motoru', 'Akışlar sistemin kendi panelinde tasarlanır ve kendi kuyruk altyapısında çalışır.', 'Veri dışarı çıkmamalı ya da akışlar ürünün parçası olacaksa (SaaS, portal).', 'Panelde sürükle-bırak akış: Tetik → Koşul → 1 gün bekle → E-posta → Görev.',
           'Akış tanımları veritabanında sürümlü saklanır; adımlar zamanlanmış işlerle çalışır, her kişi-adım çalışması idempotent ve kayıtlıdır.'),
         o('hubspot', 'HubSpot', 'CRM ile birleşik pazarlama otomasyonu platformu.', 'CRM ve satış ekibi HubSpot\'ta çalışıyorsa.', 'Form gönderimi HubSpot iş akışını başlatır; satış temsilcisine görev açılır.',
           'Site olayları ve kişi alanları HubSpot API\'siyle aktarılır; izin ve abonelik durumu iki yönlü eşlenir.'),
         o('brevo', 'Brevo Automation', 'E-posta / SMS gönderimiyle birleşik otomasyon.', 'Küçük ve orta ölçekli e-ticaret ve hizmet işletmeleri.', 'Kayıt sonrası 3 e-postalık hoş geldin akışı.',
           'Olaylar Brevo\'ya kişi özniteliği ve olay olarak gönderilir; çıkış ve iade olayları webhook ile sisteme döner.'),
         o('klaviyo', 'Klaviyo', 'E-ticaret odaklı otomasyon ve segmentasyon platformu.', 'Sepet terki, tekrar satın alma gibi e-ticaret akışları ağırlıktaysa.', 'Sepet terkinden 1 saat sonra hatırlatma e-postası.',
           'Sipariş ve ürün görüntüleme olayları Klaviyo\'ya yalnız gerekli alanlarla ve izin durumuna göre gönderilir.'),
         o('customerio', 'Customer.io', 'Ürün olaylarına dayalı mesajlaşma ve yolculuk platformu.', 'SaaS ve uygulama içi davranışa göre iletişim.', 'Deneme süresinin 10. gününde özellik kullanılmadıysa yönlendirme e-postası.',
           'Ürün olayları kişi kimliğiyle gönderilir; kişisel veri en aza indirilir, silme talepleri platforma da iletilir.'),
         o('n8n', 'n8n (teknik iş akışları)', 'Kendi sunucusunda da çalışabilen genel amaçlı iş akışı otomasyon aracı.', 'Pazarlama dışı entegrasyon akışları ya da veri dışarı çıkmaması gereken durumlar.', 'Yeni teklif → Slack bildirimi → CRM görevi → Google Sheets satırı.',
           'n8n kendi sunucusunda çalıştırılırsa erişimi kimlik doğrulama ve ağ kısıtıyla korunur; kimlik bilgileri n8n kimlik bilgisi deposunda tutulur, iş akışları sürüm kontrolüne alınır.'),
     ]},

    {'id': 'mo_triggers', 'section': 'biz_automation', 'type': 'multiselect', 'label': 'Tetikleyiciler', 'en': 'Journey Triggers',
     'agents': [AUTO, APP], 'showIf': ON_MO,
     'explanation': 'Müşteri yolculuğunu başlatacak olayları belirler. Davranış tetikleyicileri (sayfa ziyareti, sepet terki) analitik / çerez izniyle sınırlıdır.',
     'scenario': 'Hangi anların otomatik iletişime değer olduğu belli olduğunda; modül seçimlerine göre öneri gelir.',
     'example': 'Sepete ürün ekleyip 1 saat içinde ödeme yapmayan, e-posta izni olan üyeye "Sepetinizde ürün kaldı" e-postası gider.',
     'rule': 'Otomasyon tetikleyicileri: {labels}. Tetikleyici olaylar sunucuda doğrulanmış kaynaklardan üretilir; tarayıcıdan gelen olaylar tek başına para, yetki ya da durum değiştiren aksiyon başlatmaz.',
     'recommend': [{'field': 'modules_extra', 'map': {'ecommerce': ['cart_abandon', 'purchase'], 'booking': ['booking'], 'crm': ['form_submit', 'lead_score', 'inactivity'], 'lms': ['signup', 'booking'], 'events': ['booking']}}],
     'options': [
         o('form_submit', 'Form gönderimi (önerilen)', 'İletişim, teklif ya da içerik indirme formu gönderildiğinde.', 'Talep toplayan her site.', '“Formunuz bize ulaştı” e-postası + satış temsilcisine görev.',
           'Form tetikleyicisi yalnız sunucuda doğrulanmış ve bot kontrolünden geçmiş gönderimde çalışır.'),
         o('signup', 'Kayıt / üyelik', 'Yeni üye, deneme başlangıcı ya da e-posta doğrulaması tamamlandığında.', 'Üyelik, SaaS ve eğitim platformları.', 'Hoş geldin akışı: 0. gün, 2. gün, 7. gün.',
           'Kayıt akışında ilk ileti işlemsel / hizmet niteliğindedir; sonraki tanıtım iletileri yalnız pazarlama izni varsa gider.'),
         o('cart_abandon', 'Sepet terki', 'Sepete ürün eklenip belirli süre içinde ödeme yapılmadığında.', 'E-ticaret.', 'Sepet terkinden 1 saat sonra hatırlatma, 24 saat sonra ikinci hatırlatma.',
           'Sepet terki yalnız oturum açmış ya da e-postası bilinen ve pazarlama izni olan kişide tetiklenir; ödeme tamamlanınca akış durur.'),
         o('purchase', 'Satın alma / sipariş durumu', 'Sipariş tamamlandığında, teslim edildiğinde ya da tekrar satın alma zamanı geldiğinde.', 'E-ticaret ve abonelik.', 'Teslimattan 7 gün sonra değerlendirme isteği.',
           'Sipariş tetikleyicileri sipariş durum değişikliği olayından üretilir; iade ya da iptalde ilgili akış durur.'),
         o('booking', 'Randevu, etkinlik ya da eğitim', 'Randevu / rezervasyon, etkinlik kaydı, eğitim kaydı ya da tamamlama.', 'Rezervasyon, etkinlik ve LMS projeleri.', 'Eğitimi tamamlayana ileri seviye eğitim önerisi.',
           'Randevu ve eğitim tetikleyicileri ilgili modülün olayından üretilir; iptal ve gelmeme (no-show) ayrı olaylar olarak işlenir.'),
         o('lead_score', 'Puan eşiği ve durum değişikliği', 'Potansiyel müşteri puanı eşiği geçtiğinde ya da satış aşaması değiştiğinde.', 'CRM ve lead puanlaması olan B2B projeler.', 'Puan 60\'ı geçince kişi satışa devredilir.',
           'Puan ve aşama tetikleyicileri CRM\'deki değişiklik olayından üretilir; aynı eşik için akış bir kez başlar.'),
         o('inactivity', 'Hareketsizlik', 'Belirli süre giriş, satın alma ya da etkileşim olmadığında.', 'Abonelik, SaaS ve sadakat programları.', '60 gün giriş yapmayan kullanıcıya “Sizi özledik” e-postası.',
           'Hareketsizlik zamanlanmış işle hesaplanır; pazarlama izni yoksa yalnız hizmet niteliğindeki bilgilendirme gider.'),
         o('page_visit', 'Sayfa ziyareti (izinli)', 'Belirli ürün ya da fiyat sayfasının ziyareti.', 'İlgi sinyaline göre takip yapılan B2B ve e-ticaret.', 'Fiyat sayfasını 3 kez ziyaret eden kişi “sıcak” segmente alınır.',
           'Sayfa ziyareti tetikleyicisi yalnız analitik / pazarlama çerezine onay vermiş ve kimliği bilinen kişide çalışır; onay geri çekilince davranış verisi akışlarda kullanılmaz.'),
         o('date', 'Tarih', 'Doğum günü, yenileme tarihi, sözleşme bitişi gibi kayıtlı tarihler.', 'Abonelik, sigorta, sözleşmeli hizmetler.', 'Sözleşme bitişinden 30 gün önce yenileme hatırlatması.',
           'Tarih tetikleyicileri alıcının saat diliminde, günde bir kez çalışan zamanlanmış işle üretilir.'),
     ]},

    {'id': 'mo_actions', 'section': 'biz_automation', 'type': 'multiselect', 'label': 'Otomatik Aksiyonlar', 'en': 'Automated Actions',
     'agents': [AUTO, INT], 'showIf': ON_MO,
     'explanation': 'Akış adımlarında hangi aksiyonların yapılabileceğini belirler: ileti gönderme, CRM görevi, puan ve segment değişikliği, satışa devir, harici sisteme çağrı.',
     'scenario': 'Otomasyonun yalnız ileti göndermeyip ekip işlerini de tetikleyeceği durumlar.',
     'example': 'Teklif 5 gün yanıtsız kalınca müşteriye hatırlatma e-postası gider, satış temsilcisine "takip ara" görevi açılır, kişinin puanı 10 düşer.',
     'rule': 'Otomasyon aksiyonları: {labels}. Her aksiyon çalışması kişi, akış sürümü, adım ve sonuçla kayda yazılır ve CRM zaman çizelgesinde görünür.',
     'options': [
         o('send_message', 'İleti gönderimi (önerilen)', 'E-posta, SMS, WhatsApp, push ya da uygulama içi bildirim gönderimi.', 'Her akış.', '2. gün: “Kurulumu tamamlamak için 3 adım” e-postası.',
           'İletiler Bildirim Merkezi (seçiliyse) ve E-posta Aboneliği modülü kurallarıyla gönderilir; her gönderimden hemen önce kanal izni, İYS, gönderilmeyecekler listesi ve sıklık sınırı yeniden kontrol edilir.'),
         o('crm_task', 'CRM görevi ve atama', 'Satış ya da destek temsilcisine görev açılır, kayıt sahibine atanır.', 'CRM kullanan projeler.', '“Yeni lead — 24 saat içinde ara” görevi bölge temsilcisine.',
           'Görevler kayıt sahibine ya da tanımlı atama kuralına göre açılır; aynı adım için ikinci görev açılmaz.'),
         o('score_segment', 'Puan ve segment güncelleme', 'Potansiyel müşteri puanı, yaşam döngüsü aşaması ya da segment üyeliği değiştirilir.', 'Lead puanlaması ve segmentasyon yapılan projeler.', 'Webinar\'a katılan kişinin puanı +15, segment: “ilgili”.',
           'Puan ve segment değişiklikleri gerekçeli olarak kaydedilir; otomasyon kişinin izin durumunu ve kullanıcı rolünü değiştiremez.'),
         o('handoff', 'Satışa devir', 'Eşik geçilince kişi satış ekibine devredilir, otomatik pazarlama iletileri durur.', 'B2B ve yüksek tutarlı satış.', 'Puan 60 → satış temsilcisine devir; pazarlama akışlarından çıkış.',
           'Satışa devredilen kişi pazarlama akışlarından çıkarılır ya da ileti sıklığı düşürülür; devir sahibi ve zamanı kaydedilir.'),
         o('webhook', 'Harici sisteme çağrı (webhook)', 'Akış adımında harici bir API\'ye veri gönderilir.', 'ERP, muhasebe, destek ya da reklam platformu entegrasyonları.', 'Dönüşüm olayı reklam platformunun sunucu API\'sine gönderilir.',
           'Webhook adresleri yönetici onaylı izinli listeden seçilir (serbest URL yok), iç ağ adreslerine istek engellenir; istekler imzalı, zaman aşımlı ve idempotency anahtarlıdır, yalnız gerekli alanlar gönderilir.'),
         o('internal_alert', 'Ekip içi uyarı', 'Belirli durumlarda yöneticiye ya da ekibe uyarı.', 'Lead\'in süresinde işlenmediği, düşük memnuniyet puanı geldiği durumlar.', '“Lead 24 saattir işlenmedi” uyarısı satış müdürüne.',
           'Ekip uyarıları Bildirim Merkezi\'nin ekip içi kategorisiyle ve tekrar bastırma kuralıyla gönderilir.'),
     ]},

    {'id': 'mo_guardrails', 'section': 'biz_automation', 'type': 'multiselect', 'label': 'İzin ve Baskı Korumaları', 'en': 'Consent & Pressure Guardrails',
     'agents': [KVKK, AUTO], 'showIf': ON_MO,
     'explanation': 'Otomasyonun onaysız kişiye ileti göndermesini, aynı kişiyi aşırı mesajla rahatsız etmesini ve hatalı akışın kontrolsüz çalışmasını önleyen korumaları belirler.',
     'scenario': 'Pazarlama iletisi gönderen her otomasyon.',
     'example': 'Kullanıcı SMS\'teki ret bağlantısına basınca bütün akışlarda SMS adımları onun için atlanır; aynı gün iki akış e-posta göndermek isterse yalnız öncelikli olan gider.',
     'rule': 'Otomasyon korumaları: {labels}. Onaysız kişiye pazarlama iletisi hiçbir akıştan gönderilmez; bu kontrol akış aracında değil, gönderim noktasında sunucuda yapılır.',
     'options': [
         o('consent_gate', 'Her adımda izin kontrolü (önerilen)', 'Mesaj adımı, gönderimden hemen önce güncel izni ve İYS durumunu yeniden kontrol eder.', 'Her akış.', 'Akışa girdikten sonra ret veren kişinin 3. gün e-postası atlanır.',
           'Her mesaj adımı gönderimden hemen önce kanal iznini, İYS durumunu ve gönderilmeyecekler listesini kontrol eder; izin yoksa adım atlanır ve nedeni kaydedilir.'),
         o('exit_rules', 'Çıkış kuralları', 'Abonelikten çıkış, hedef eylemin gerçekleşmesi ya da müşteri olma durumunda kişi akıştan çıkar.', 'Her akış.', 'Sepeti tamamlayan kişi sepet terki akışından çıkar.',
           'Her akışta hedef eylem ve çıkış koşulları tanımlıdır; abonelikten çıkış bütün pazarlama akışlarından çıkarır.'),
         o('freq_cap', 'Akışlar arası sıklık sınırı ve öncelik', 'Bir kişiye bütün akışlardan gidebilecek ileti sayısı sınırlanır; çakışmada öncelikli akış kazanır.', 'Birden çok etkin akışı olan projeler.', 'Kişi başı günde en çok 1, haftada en çok 3 pazarlama iletisi; işlemsel akışlar sayılmaz.',
           'Sıklık sınırı akışlar arası ve kanal bazında sunucuda sayılır; çakışmada akış önceliği uygulanır, düşük öncelikli ileti ertelenir ya da atlanır.'),
         o('quiet_hours', 'Sessiz saatler ve gönderim penceresi', 'İletiler alıcının saat diliminde belirlenen saatler dışında gönderilmez.', 'SMS, push ve WhatsApp adımları olan akışlar.', 'Gece 02:00\'de tetiklenen adım sabah 09:00\'da çalışır.',
           'Mesaj adımları alıcının saat diliminde tanımlı gönderim penceresine ertelenir; resmî tatil ve hafta sonu kuralı tanımlanabilir.'),
         o('versioning', 'Sürümleme', 'Etkin akıştaki değişiklik yeni sürüm açar; içindeki kişiler eski sürümle devam eder.', 'Sık değiştirilen akışlar.', 'Hoş geldin akışı v3 → v4; v3\'teki 214 kişi v3 ile tamamlar.',
           'Etkin akış yerinde düzenlenmez, yeni sürüm açılır; kişi hangi sürümle girdiyse onunla devam eder, sürüm değişikliği kayda yazılır.'),
         o('approval', 'Yayına alma onayı ve test', 'Akış, test kişileriyle denendikten ve yetkili onayladıktan sonra etkinleşir.', 'Kurum adına geniş kitleye iletişim yapan akışlar.', 'Akış önce iç test listesiyle çalıştırılır; pazarlama müdürü onaylayınca etkin olur.',
           'Akış önce test kişileriyle (gerçek alıcıya ileti göndermeden) denenir; hazırlayandan farklı yetkili kişinin onayıyla etkinleşir.'),
         o('kill_switch', 'Acil durdurma ve hata uyarısı', 'Hatalı akış tek düğmeyle durdurulur; hata oranı eşiği aşılınca akış kendiliğinden duraklar.', 'Her akış.', 'Şablon hatası %5\'i geçince akış duraklar, sorumluya uyarı gider.',
           'Her akış tek işlemle durdurulabilir; hata oranı eşiği aşıldığında akış kendiliğinden duraklar ve sorumluya uyarı gider.'),
     ]},

    {'id': 'mo_measure', 'section': 'biz_automation', 'type': 'multiselect', 'label': 'Deney ve Raporlama', 'en': 'Experiments & Reporting',
     'agents': [ABT, AUTO], 'showIf': ON_MO,
     'explanation': 'Akışların etkisinin nasıl ölçüleceğini belirler: A/B testleri, kontrol grubu, akış raporları ve dönüşüm ilişkilendirmesi. E-posta konu satırı testleri Pazarlama › Mailing › A/B Testi kararındadır.',
     'scenario': 'Otomasyonun satışa ya da elde tutmaya katkısının kanıtlanması gerekiyorsa.',
     'example': 'Sepet terki akışında kişilerin %10\'u kontrol grubuna alınır; 30 günde akıştaki grup %18, kontrol grubu %12 satın alma oranına ulaşır.',
     'rule': 'Otomasyon ölçümü: {labels}. Raporlar kişisel veri yerine toplulaştırılmış sayılarla gösterilir.',
     'options': [
         o('journey_report', 'Akış raporları (önerilen)', 'Giriş, adım bazında ilerleme, tamamlanma, çıkış, dönüşüm ve hata sayıları.', 'Her akış.', 'Akış ekranında huni: 1.240 giriş → 980 ilk e-posta → 310 tıklama → 96 satın alma.',
           'Her akış için adım bazında sayılar ve hata oranı raporlanır; rapor akış sürümüne göre ayrılır.'),
         o('ab_test', 'A/B testi', 'Konu, içerik, kanal ya da zamanlama varyasyonları rastgele gruplara verilir.', 'Yeterli hacmi olan akışlar.', 'Hatırlatma 1 saat sonra mı 4 saat sonra mı?',
           'Testin başarı ölçütü ve örneklem büyüklüğü baştan belirlenir; kazanan, ölçüt istatistiksel olarak ayrışınca seçilir, ara sonuca bakıp erken bitirilmez.'),
         o('holdout', 'Kontrol grubu', 'Kişilerin bir bölümü akışa alınmaz; akışın gerçek etkisi kontrol grubuyla karşılaştırılır.', 'Otomasyonun gelir katkısının raporlandığı projeler.', 'Kişilerin %10\'u kontrol grubunda.',
           'Kontrol grubu rastgele ve kalıcı atanır; akışın etkisi kontrol grubuna göre artış (uplift) olarak raporlanır.'),
         o('attribution', 'Dönüşüm ilişkilendirme', 'Akıştan gelen tıklama ve dönüşümler UTM ve CRM kaydıyla ilişkilendirilir.', 'Satış ya da lead hedefi olan akışlar.', 'Akış kaynaklı 42 lead, 11 satış fırsatı.',
           'Akış iletilerindeki bağlantılar UTM standardıyla etiketlenir; dönüşüm penceresi baştan tanımlanır ve raporda yazılır.'),
     ]},
]

# =====================================================================================================
# Ek Modüller'e yeni seçenekler (kapı)
# =====================================================================================================
OPT = [
    {'field': 'modules_extra', 'option': o('certificates', 'Kurum sertifikaları (kalite / uygunluk belgeleri)',
        'Kurumun ISO, TSE, CE, helal, akreditasyon gibi belgelerinin sitede gösterilmesi, geçerlilik tarihlerinin izlenmesi ve doğrulanması. Seçilince İş Modülleri › Kurum Sertifikaları bölümündeki kararlar açılır. Eğitim katılımcılarına verilen sertifikalar bu modül değil, Eğitim (LMS) modülünün konusudur.',
        'Kalite, bilgi güvenliği ya da ürün uygunluk belgesi müşterinin satın alma kararında rol oynuyorsa (kurumsal satış, ihale, gıda, sağlık, yazılım hizmeti).',
        'Sitede Sertifikalar sayfası, hizmet sayfalarında ISO rozetleri; süresi dolan belge kendiliğinden yayından kalkar.')},
    {'field': 'modules_extra', 'option': o('notify', 'Bildirim merkezi (çok kanallı bildirim)',
        'E-posta, SMS, WhatsApp, mobil ve web anlık bildirim ile uygulama içi bildirimlerin tek merkezden, izin ve tercih kurallarıyla gönderilmesi. Seçilince İş Modülleri › Bildirim Merkezi bölümündeki kararlar açılır.',
        'Sipariş, randevu, ödeme, destek talebi gibi olaylarda kullanıcıya birden çok kanaldan ulaşılacaksa ya da birden çok modül bildirim üretiyorsa.',
        'Panelde zil simgesi ve bildirim listesi; kullanıcı ayarlarında kanal × kategori tercih tablosu.')},
    {'field': 'modules_extra', 'option': o('mailing', 'E-posta aboneliği ve toplu gönderim',
        'Bülten / kampanya aboneliği, abonelik kategorileri, çift onay, İYS senkronu, tek tıkla çıkış, gönderilmeyecekler listesi ve e-posta servis sağlayıcısı entegrasyonu. Seçilince İş Modülleri › E-posta Aboneliği ve Toplu Gönderim bölümündeki kararlar açılır.',
        'Sitede bülten aboneliği toplanacak ya da panelden toplu e-posta gönderilecekse.',
        'Blogda abonelik formu, doğrulama e-postası, e-postalarda “Tercihlerinizi yönetin” bağlantısı.')},
    {'field': 'modules_extra', 'option': o('social_publish', 'Sosyal medya paylaşım modülü',
        'Kurumsal sosyal medya hesaplarının resmî API\'lerle panele bağlanması, gönderilerin planlanması, onaylanması ve otomatik yayınlanması. Seçilince İş Modülleri › Sosyal Medya Paylaşım Modülü bölümündeki kararlar açılır.',
        'Pazarlama ekibi birden çok platformda düzenli paylaşım yapıyor ve gönderileri site içeriklerinden üretip panelden planlamak istiyorsa.',
        'Blog yazısının kartında “Sosyal gönderi oluştur”; haftalık paylaşım takvimi ve onay kuyruğu.')},
    {'field': 'modules_extra', 'option': o('automation', 'Pazarlama otomasyonu ve müşteri yolculukları',
        'Form, kayıt, sepet, randevu, puan ve hareketsizlik gibi olaylara göre otomatik ileti, görev ve segment aksiyonları çalıştıran akışlar. Seçilince İş Modülleri › Pazarlama Otomasyonu ve Müşteri Yolculukları bölümündeki kararlar açılır.',
        'Hoş geldin, sepet terki, teklif takibi, yeniden kazanım gibi tekrarlayan iletişimlerin elle değil otomatik yapılması isteniyorsa.',
        'Panelde akış düzenleyici: Form gönderildi → 1 gün bekle → izin varsa e-posta → satış temsilcisine görev.')},
]

PART = {
    'sections': [SEC_CERT, SEC_NT, SEC_ML, SEC_SP, SEC_MO],
    'fields': F_CERT + F_NT + F_ML + F_SP + F_MO,
    'fields_into': [],
    'option_add': OPT,
    'guide_add': {},
}
