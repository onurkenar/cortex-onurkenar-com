# -*- coding: utf-8 -*-
"""İş Modülleri — 1. parça (2026-11-12, Revize Modüler V3: B20 CRM ve Satış Süreci, B2 Destek Talebi ve Bilgi Bankası,
B3 Anket, NPS ve Geri Bildirim, B4 Abonelik, Paket ve Üyelik Planları, B5 Online Danışmanlık Satışı).
Kaynak doküman: Web_Sayfasi_Projesi_Revize_Moduler_V3 — Lead ve CRM Sistemi (Faz 4), 3. Parti CRM Entegrasyon Katmanı,
Opportunity / Deal, Lead Scoring, Satış Süreç Diyagramı; Destek Talep ve Ticket Yönetimi; Anket, NPS ve Geri Bildirim;
Abonelik, Paket ve Üyelik Yönetimi; Online Danışmanlık Satışı ve Randevu Yönetimi.
Her bölümün bütün alanları Ek Modüller (modules_extra) kararında ilgili modül seçilince görünür. CRM için var olan `crm`
değeri kapıdır; diğer dört modülün seçeneği option_add ile Ek Modüller'e eklenir.
Hukuki dayanaklar 2026-11-12'de mevzuat.gov.tr'deki güncel metinden okundu: 6502 sayılı Kanun m. 48 ve m. 52,
Abonelik Sözleşmeleri Yönetmeliği m. 2, 5, 13, 22–25, Mesafeli Sözleşmeler Yönetmeliği m. 15."""

APP = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
INT = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani'
CRM_SR = 'poz:satis:08.01/crm-ve-pipeline-yonetimi/kidemli-crm-uzmani'
PIPE = 'poz:satis:08.01/crm-ve-pipeline-yonetimi/pipeline-yonetimi-uzmani'
CRM_DQ = 'poz:satis:08.01/crm-ve-pipeline-yonetimi/crm-veri-kalitesi-analisti'
ROUTE = 'poz:satis:08.01/gelir-operasyonlari/lead-yonlendirme-uzmani'
REVOPS = 'poz:satis:08.01/gelir-operasyonlari/kidemli-gelir-operasyonlari-uzmani'
SCORE = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/lead-skorlama-uzmani'
LEADM = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/lead-yonetimi-uzmani'
KVKK = 'poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani'
KVKK_LAW = 'poz:hukuk:05.06/veri-koruma-danismanligi-ekibi/kvkk-ve-gdpr-hukuk-uzmani'
SUP_SR = 'poz:musteri-deneyimi:11.04/birinci-seviye-destek/kidemli-musteri-destek-uzmani'
OMNI = 'poz:musteri-deneyimi:11.04/cok-kanalli-destek/kidemli-cok-kanalli-destek-uzmani'
ESC = 'poz:musteri-deneyimi:11.05/teknik-destek-koordinasyonu/teknik-eskalasyon-uzmani'
KB = 'poz:musteri-deneyimi:11.04/destek-bilgi-yonetimi/kidemli-bilgi-yonetimi-uzmani'
VOC = 'poz:musteri-deneyimi:11.06/musterinin-sesi/kidemli-musterinin-sesi-uzmani'
CXA = 'poz:musteri-deneyimi:11.01/musteri-deneyimi-analitigi/kidemli-musteri-deneyimi-analitigi-uzmani'
RECOVER = 'poz:musteri-deneyimi:11.03/riskli-musteri-ve-kurtarma/kidemli-musteri-kurtarma-uzmani'
PKG = 'poz:satis:08.07/fiyatlandirma-stratejisi/paket-ve-tarife-uzmani'
TAH = 'poz:finans:03.05/tahsilat-planlama-ve-takip/kidemli-tahsilat-uzmani'
EFAT = 'poz:muhasebe:invoicing_ebilling/e-fatura-ve-e-arsiv-operasyonlari-yoneticisi/e-fatura-uzmani'
RETAIN = 'poz:musteri-deneyimi:11.08/churn-onleme-ve-musteri-kurtarma/kidemli-musteri-tutundurma-uzmani'
CONTRACT = 'poz:hukuk:05.02/sozlesme-standartlari-ekibi/kidemli-sozlesme-hukuku-musaviri'
PM = 'poz:urun-arge:18.03/dijital-urun-yonetimi/urun-yoneticisi'


def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    if exclusive:
        x['exclusive'] = True
    return x


def gate(v):
    return [{'field': 'modules_extra', 'in': [v]}]


def opened(name):
    return "Seçilince İş Modülleri › %s bölümündeki kararlar açılır." % name


G_CRM, G_TK, G_SV, G_SUB, G_CS = gate('crm'), gate('ticket'), gate('survey'), gate('subscription'), gate('consulting')

# ---------------------------------------------------------------- Ek Modüller'e eklenen seçenekler
OPTION_ADD = [
    {'field': 'modules_extra', 'option': o(
        'ticket', 'Destek talebi (ticket) ve bilgi bankası',
        "Müşteri, üye ya da kurumsal kullanıcıdan gelen destek taleplerinin numaralı kayıt (ticket) olarak açıldığı, kategori ve öncelikle sınıflandırılıp ekibe atandığı, SLA süreleriyle izlenip kapatıldığı modül; yardım makaleleriyle (bilgi bankası) talepleri azaltır. " + opened('Destek Talebi ve Bilgi Bankası'),
        "Satış sonrası destek veren SaaS, e-ticaret, eğitim, rezervasyon ya da kurumsal hizmet projeleri; destek talepleri e-posta kutusunda kayboluyor, kimin neye baktığı ve ne kadar sürede yanıt verildiği bilinmiyorsa.",
        "Müşteri portalında \"Destek Taleplerim\" sayfası: #TK-2026-01482 numaralı \"Fatura adresim yanlış\" talebi \"Müşteri yanıtı bekleniyor\" durumunda; panelde destek ekibi önceliğe göre sıralı kuyruğu ve SLA sayaçlarını görür.")},
    {'field': 'modules_extra', 'option': o(
        'survey', 'Anket, NPS ve geri bildirim',
        "NPS, CSAT, CES ve genel geri bildirim anketlerinin oluşturulduğu, işlem sonrası otomatik gönderildiği, yanıtların müşteri kaydına bağlanıp düşük puanda aksiyon başlatıldığı modül. " + opened('Anket, NPS ve Geri Bildirim'),
        "Müşteri memnuniyetini düzenli ölçmek, destek / teslimat / eğitim sonrası deneyimi puanlamak ve memnun olmayan müşteriye hızla dönmek isteniyorsa.",
        "Destek talebi kapandıktan sonra müşteriye \"Sorununuz ne kadar iyi çözüldü? (1–5)\" e-postası gider; 2 puan veren müşteri için destek ekip liderine otomatik takip görevi açılır.")},
    {'field': 'modules_extra', 'option': o(
        'subscription', 'Abonelik, paket ve üyelik planları',
        "Aylık / yıllık abonelik, kademeli paket, kredi ya da seans hakkı içeren planların satıldığı, tekrarlayan tahsilatın, başarısız ödemenin, plan değişikliğinin, iptalin ve kullanım haklarının yönetildiği modül. " + opened('Abonelik, Paket ve Üyelik Planları'),
        "SaaS, ücretli üyelik, eğitim erişim paketi, bakım / destek paketi ya da düzenli teslimatlı ürün satan projeler; gelirin önemli kısmı tekrarlayan ödemeden geliyorsa.",
        "Fiyatlandırma sayfasında Başlangıç / Profesyonel / Kurumsal planları ve \"Yıllık öde, 2 ay kazan\" anahtarı; müşteri panelinde \"Planım: Profesyonel · Sonraki ödeme 14 Aralık · Planı değiştir · Aboneliği iptal et\".")},
    {'field': 'modules_extra', 'option': o(
        'consulting', 'Online danışmanlık satışı',
        "Danışmanlık hizmetinin seans ya da paket olarak satıldığı, müşterinin danışman ve uygun saat seçip ödeme yaptığı, randevuya otomatik görüntülü görüşme bağlantısı üretilip hatırlatma gönderildiği modül. " + opened('Online Danışmanlık Satışı'),
        "Psikolojik danışmanlık, diyetisyen, hukuk / mali müşavirlik ön görüşmesi, kariyer koçluğu, yazılım mentorluğu gibi uzaktan, ücretli ve randevulu hizmet satılıyorsa.",
        "\"60 dakikalık strateji görüşmesi — 2.500 TL\" sayfasında danışman ve saat seçilir, ödeme sonrası müşteriye Google Meet bağlantılı onay e-postası ve takvim daveti gider; görüşmeden 1 saat önce hatırlatma SMS'i ulaşır.")},
]

# ---------------------------------------------------------------- B20 CRM ve Satış Süreci
S_CRM = {
    'id': 'biz_crm', 'group': 'İş Modülleri', 'icon': '◎',
    'name': 'CRM ve Satış Süreci', 'en': 'CRM, Lead Management & Sales Pipeline',
    'desc': "Lead toplama, kaynak takibi, satış hunisi (pipeline) ve fırsat yönetimi, lead dağıtımı, puanlama ve mükerrer / spam kontrolü, aktivite ve teklif takibi ile dış CRM senkronunu karara bağlar",
    'guide': {
        'purpose': "CRM (müşteri ilişkileri yönetimi) modülü sitenin formlarından, telefon, WhatsApp, canlı destek, reklam formları ve diğer modüllerden (rezervasyon, eğitim, e-ticaret, danışmanlık) gelen her potansiyel müşteriyi (lead) tek bir müşteri profilinde toplar; lead'in kaynağını, satış hunisindeki aşamasını, sorumlusunu, iletişim geçmişini ve teklif durumunu izlenebilir hâle getirir. Bu bölüm lead kaynaklarını, satış aşamalarını, atama kuralını, lead kalitesi denetimlerini, aktivite / teklif kayıtlarını ve HubSpot, Salesforce gibi dış bir CRM ile senkronu belirler. Satış süreç diyagramı ve KPI'lar (Lead → MQL → SQL → fırsat → teklif → kazanıldı dönüşüm oranları, ortalama kapanış süresi, kayıp sebebi dağılımı) bu kararlardan türetilir.",
        'criteria': [
            "Her lead'in kaynağı (form, kanal, kampanya, UTM parametreleri) oluştuğu anda otomatik ve değiştirilemez biçimde kaydedilir; kaynak bilinmeden pazarlama bütçesinin getirisi ölçülemez.",
            "Lead (aday) ile fırsat (opportunity / deal) ayrı kayıtlardır: lead değerlendirilir, satışa uygun bulunan (SQL) fırsata dönüşür, fırsatın tutarı, olasılığı ve tahmini kapanış tarihi olur.",
            "Satış aşamaları panelden yönetilir; her aşama geçişi kim, ne zaman, hangi aşamadan bilgisiyle kaydedilir, \"Kaybedildi\"de kayıp sebebi zorunludur.",
            "Satış temsilcisi yalnız kendisine ya da ekibine atanmış kayıtları görür; yetki sunucuda, kayıt düzeyinde denetlenir.",
            "Ticari elektronik ileti izni, aydınlatma metni sürümü ve izin kaynağı lead kaydında ayrı alanlarda tutulur; izinsiz kişiye pazarlama iletisi gönderilmez (6563 sayılı Kanun, İYS).",
            "Dış CRM kullanılıyorsa hangi sistemin hangi alanın sahibi olduğu (tek doğru kaynak) baştan belirlenir; senkron idempotent, kuyruklu ve hatası izlenebilirdir.",
        ],
        'pitfalls': [
            "Form gönderimlerini yalnız e-postaya yönlendirmek: lead kaydı, kaynak ve takip geçmişi oluşmaz, dönüşüm ölçülemez.",
            "İçe aktarılan (CSV) listelere izin kaynağı sorgulamadan pazarlama e-postası / SMS göndermek: İYS kaydı olmayan alıcıya ticari ileti idari para cezası riski taşır.",
            "Mükerrer kontrolü yapmamak: aynı kişi üç farklı temsilciye üç ayrı lead olarak düşer, müşteri üç kez aranır.",
            "Mükerrer kayıtları otomatik ve geri alınamaz biçimde birleştirmek: farklı kişilerin verisi karışır, aktivite geçmişi kaybolur.",
            "Dış CRM ile çift yönlü senkronda çakışma kuralı tanımlamamak: iki sistem birbirinin değişikliğini sonsuz döngüde ezer.",
            "Lead puanlamayı açıklanamayan bir kara kutu yapmak: satış ekibi puana güvenmez; puanın hangi davranıştan geldiği kayıtta görünmelidir.",
        ],
        'resources': [
            {'title': "6698 sayılı Kişisel Verilerin Korunması Kanunu", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6698&MevzuatTur=1&MevzuatTertip=5', 'note': "Lead verisinin işlenme şartları, aydınlatma yükümlülüğü ve yurt dışına aktarım (m. 9) için temel kanun."},
            {'title': "6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6563&MevzuatTur=1&MevzuatTertip=5', 'note': "Ticari elektronik ileti için önceden onay ve ret hakkı kuralları."},
            {'title': "Ticari İletişim ve Ticari Elektronik İletiler Hakkında Yönetmelik", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20914&MevzuatTur=7&MevzuatTertip=5', 'note': "Onayın alınma biçimi, ispatı ve İleti Yönetim Sistemi'ne kayıt yükümlülüğü."},
            {'title': "İleti Yönetim Sistemi (İYS)", 'url': 'https://iys.org.tr/', 'note': "Ticari ileti izinlerinin kaydedildiği ve gönderim öncesi sorgulandığı resmî sistem."},
            {'title': "HubSpot — Understanding the CRM APIs", 'url': 'https://developers.hubspot.com/docs/api-reference/latest/crm/understanding-the-crm', 'note': "HubSpot nesne modeli (kişi, şirket, fırsat), ilişkiler ve CRM API'leri."},
            {'title': "Pipedrive API Reference", 'url': 'https://developers.pipedrive.com/docs/api/v1', 'note': "Pipedrive kişi, fırsat (deal), aşama ve aktivite uç noktaları."},
            {'title': "Zoho CRM V8 APIs", 'url': 'https://www.zoho.com/crm/developer/docs/api/v8/', 'note': "Zoho CRM kayıt, upsert ve toplu işlem API'leri."},
            {'title': "Microsoft Dataverse Web API (Dynamics 365)", 'url': 'https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/overview', 'note': "Dynamics 365 Sales verisine erişen Dataverse Web API'si."},
            {'title': "OWASP — Automated Threats to Web Applications", 'url': 'https://owasp.org/www-project-automated-threats-to-web-applications/', 'note': "Bot ve spam form gönderimlerinin sınıflandırılması ve savunmaları."},
        ],
    },
}

F_CRM = [
    {'id': 'crm_lead_sources', 'section': 'biz_crm', 'type': 'multiselect', 'label': 'Lead Kaynakları', 'en': 'Lead Sources & Capture', 'agents': [LEADM, APP], 'showIf': G_CRM,
     'explanation': "Potansiyel müşterinin (lead) CRM'e hangi kanallardan gireceğini belirler. Her kaynaktan gelen kayıt aynı lead modeline yazılır, kaynak ve kampanya bilgisiyle etiketlenir.",
     'scenario': "Pazarlama ve satış bütçesinin hangi kanaldan geri döndüğünü görmek, hiçbir talebin e-posta kutusunda kaybolmaması isteniyorsa; özellikle birden çok form, reklam ve iletişim kanalı varsa.",
     'example': "Google Ads'ten gelen ziyaretçi teklif formunu doldurur; CRM'de \"Kaynak: Web formu · utm_source=google · utm_campaign=kasim-kampanya · Sayfa: /kurumsal-paket\" etiketli yeni lead oluşur ve satış ekibine düşer.",
     'rule': "Lead kaynakları: {labels}. Her lead kaynak kanalı, UTM parametreleri, açılış sayfası ve oluşma zamanıyla sunucuda kaydedilir ve sonradan değiştirilemez; aydınlatma metni sürümü ve ticari ileti izni (izin metni, tarih, kanal) ayrı alanlarda tutulur, izin kutusu önceden işaretli gelmez; aynı kişiye ait yeni kayıt mevcut müşteri profiline bağlanır; form uç noktaları hız sınırı ve bot korumasıyla korunur.",
     'recommend': [{'field': 'modules_extra', 'map': {'support_ai': ['chat'], 'events': ['events'], 'booking': ['modules'], 'lms': ['modules'], 'ecommerce': ['modules'], 'consulting': ['modules']}},
                   {'field': 'mk_ads_channels', 'map': {'meta': ['ad_forms'], 'linkedin': ['ad_forms'], 'google': ['ad_forms'], 'tiktok': ['ad_forms']}}],
     'options': [
         o('web_form', 'Web formları ve açılış sayfaları (önerilen)', "İletişim, teklif, demo ve indirme (lead magnet) formları ile kampanya açılış sayfaları.", "Her proje; sitenin birincil dönüşüm noktası formsa.", "\"Teklif al\" formu gönderilince lead kaydı oluşur ve form adı kaynak olarak yazılır.",
           "Bütün formlar tek lead oluşturma servisine gönderilir; form adı, sayfa adresi ve UTM değerleri gizli alanlarla taşınır, sunucuda doğrulanır."),
         o('phone', 'Telefon', "Gelen çağrılardan temsilcinin açtığı ya da çağrı merkezi entegrasyonuyla oluşan kayıtlar.", "Satışın önemli bölümü telefonla geliyorsa.", "Temsilci çağrı sırasında panelde \"Yeni lead (telefon)\" kaydı açar, numara mevcut müşteriyle otomatik eşlenir.",
           "Telefonla gelen lead kaynak \"Telefon\" olarak, arayan numara E.164 biçiminde normalize edilerek kaydedilir; çağrı kaydı tutulacaksa aydınlatma ve rıza ayrıca yönetilir."),
         o('whatsapp', 'WhatsApp', "WhatsApp Business hattına gelen mesajlardan oluşan lead'ler.", "Müşteriler sorularını WhatsApp'tan soruyorsa.", "WhatsApp'tan fiyat soran kişi için konuşma bağlantısıyla birlikte lead kaydı açılır.",
           "WhatsApp konuşmasından lead oluşturulurken yalnız gerekli alanlar (ad, numara, ilgilendiği hizmet) aktarılır, mesaj içeriği kişisel veri olarak saklama politikasına tabidir."),
         o('chat', 'Canlı destek ve sohbet botu', "Canlı destek penceresi ya da yapay zekâ sohbet botu üzerinden toplanan iletişim bilgileri.", "Sitede canlı destek / AI sohbet modülü varsa.", "Sohbet botu ziyaretçiye e-postasını sorar, izin onayından sonra lead oluşturur ve konuşma özetini nota ekler.",
           "Sohbetten lead oluşturma ancak ziyaretçi iletişim bilgisini kendisi verip aydınlatma gösterildikten sonra yapılır; konuşma özeti lead'e not olarak eklenir."),
         o('email', 'E-posta', "Kurumsal satış adresine (ör. satis@) gelen e-postalar.", "Teklif talepleri e-postayla geliyorsa.", "satis@ adresine gelen e-posta gönderen adresine göre mevcut kişiyle eşlenir ya da yeni lead açar.",
           "Gelen e-postadan lead oluşturmada gönderen adresi doğrulanır, ekler zararlı yazılım taramasından geçer; otomatik yanıtlar ve bülten iadeleri lead açmaz."),
         o('ad_forms', 'Reklam platformu formları', "Meta Anlık Form, LinkedIn Lead Gen, Google Ads potansiyel müşteri formu gibi reklam içi formlar.", "Reklam kampanyalarında platform içi form kullanılıyorsa.", "Meta reklam formunu dolduran kişi webhook ile birkaç saniye içinde CRM'e \"Kaynak: Meta Anlık Form · Kampanya: Kasım\" olarak düşer.",
           "Reklam formu lead'leri platform webhook'u ya da resmî entegrasyonla alınır; webhook imzası doğrulanır, aynı lead kimliği ikinci kez işlenmez."),
         o('events', 'Etkinlik ve webinar kayıtları', "Etkinlik, fuar, webinar ve bilet başvuruları.", "Etkinlik pazarlaması yapılıyorsa.", "Webinar kaydı yapan kişi \"Kaynak: Etkinlik · Webinar 12 Aralık\" etiketiyle CRM'e girer, katılım durumu sonradan işlenir.",
           "Etkinlik kayıtları etkinlik kimliğiyle lead'e bağlanır; katılım / katılmama bilgisi aktivite olarak yazılır."),
         o('modules', 'Diğer modüllerden gelen kayıtlar', "Rezervasyon, eğitim (LMS), e-ticaret siparişi ve online danışmanlık başvurularının lead / müşteri kaydı olarak aktarılması.", "Projede rezervasyon, eğitim, e-ticaret ya da danışmanlık modülü varsa.", "Ücretsiz ön görüşme randevusu alan kişi CRM'de \"Kaynak: Danışmanlık randevusu\" etiketli lead olur, randevu zaman çizelgesinde görünür.",
           "Rezervasyon, eğitim, sipariş ve danışmanlık olayları ortak olay arayüzüyle CRM'e yazılır; satın alan kişi müşteri, başvuran kişi lead olarak sınıflanır."),
         o('import', 'Toplu içe aktarma (CSV / Excel)', "Fuar listesi, eski sistem ya da kartvizit listelerinin içe aktarılması.", "Eski bir sistemden geçiş ya da etkinlikte toplanan liste varsa.", "İçe aktarma ekranında 340 satırlık dosya yüklenir; 12 satır mükerrer, 5 satır geçersiz e-posta olarak raporlanır.",
           "İçe aktarmada her satır doğrulanır, mükerrer kontrolünden geçer ve izin kaynağı zorunlu alan olarak istenir; izin kaynağı olmayan kayıtlar pazarlama iletisi listelerine eklenmez."),
         o('manual', 'Panelden elle giriş', "Satış temsilcisinin yüz yüze görüşme, tavsiye ya da saha ziyaretinden sonra lead'i elle eklemesi.", "Saha satışı ve tavsiyeyle gelen müşteri varsa.", "Temsilci fuarda tanıştığı kişiyi \"Kaynak: Saha · Tavsiye eden: ABC Ltd.\" ile ekler.",
           "Elle eklenen lead'de kaynak seçimi zorunludur ve ekleyen kullanıcı kaydedilir."),
     ]},

    {'id': 'crm_pipeline', 'section': 'biz_crm', 'type': 'select', 'label': 'Satış Hunisi (Pipeline) Modeli', 'en': 'Sales Pipeline Model', 'agents': [PIPE, REVOPS, APP], 'showIf': G_CRM,
     'explanation': "Lead'in ve satış fırsatının (opportunity / deal) hangi aşamalardan geçerek kazanılacağını ya da kaybedileceğini belirler. Satış süreç diyagramı ve dönüşüm KPI'ları bu aşamalardan türetilir.",
     'scenario': "Basit hizmet satışında kısa bir huni yeter; kurumsal satışta pazarlama ve satışın devir noktası (MQL / SQL), teklif, sözleşme ve ödeme aşamaları ayrı izlenmelidir; farklı ürün hatları farklı süreçle satılıyorsa birden çok huni gerekir.",
     'example': "Panelde sürükle-bırak pano: \"Yeni (24) · Değerlendirme (11) · Teklif gönderildi (6, 412.000 TL) · Sözleşme bekleniyor (2) · Kazanıldı · Kaybedildi\"; kartı \"Kaybedildi\"ye taşıyan temsilciden kayıp sebebi istenir.",
     'rule': "Satış hunisi modeli: {label}. Lead ve fırsat (opportunity) ayrı kayıtlardır; fırsatta tutar ve para birimi, olasılık, tahmini kapanış tarihi, ürün / hizmet ve sorumlu kullanıcı tutulur; aşamalar panelden yönetilir, her aşama geçişi kullanıcı, tarih ve önceki aşamayla kaydedilir, \"Kaybedildi\"ye geçişte kayıp sebebi zorunludur; Lead → MQL → SQL → fırsat → teklif → kazanıldı dönüşüm oranları, ortalama kapanış süresi, kayıp sebebi dağılımı ve temsilci bazlı dönüşüm panelde raporlanır; 4 Göz Onay Akışı etkinse teklif ve sözleşme onayı o modül üzerinden yürür.",
     'recommend': {'field': 'business_model', 'map': {'b2c': ['simple'], 'b2b': ['standard'], 'b2b2c': ['multi'], 'b2g': ['standard'], 'nonprofit': ['simple']}},
     'options': [
         o('simple', 'Basit huni (Yeni → Görüşüldü → Teklif → Kazanıldı / Kaybedildi)', "Az aşamalı, tek huni; MQL / SQL ayrımı yoktur.", "Küçük ekip, kısa satış döngüsü, bireysel müşteri.", "Bir diyetisyen kliniğinde talep → arandı → paket önerildi → satın aldı.",
           "Tek huni ve dört-beş aşama kurulur; MQL / SQL alanları oluşturulmaz, puanlama kullanılıyorsa yalnız sıralama için kullanılır."),
         o('standard', 'Standart B2B hunisi (MQL / SQL, fırsat, teklif, sözleşme, ödeme) (önerilen)', "Yeni lead → Değerlendirme → MQL → SQL → Fırsat → İhtiyaç analizi → Teklif hazırlanıyor → Teklif gönderildi / görüntülendi → Revizyon → Sözleşme / e-İmza bekleniyor → Ödeme bekleniyor → Kazanıldı / Kaybedildi / Beklemede.", "Kurumsal satış, uzun satış döngüsü, pazarlama ve satış ekiplerinin ayrı olduğu yapılar.", "Pazarlama 60 puanı geçen lead'i MQL olarak satışa devreder; satış görüşmeden sonra SQL yapıp fırsat açar.",
           "Lead aşamaları (Yeni, Değerlendirme, MQL, SQL) ile fırsat aşamaları (İhtiyaç analizi … Kazanıldı / Kaybedildi / Beklemede) ayrı tutulur; SQL olan lead fırsata dönüştürülür ve iki kayıt birbirine bağlanır; teklif durumları gönderildi, görüntülendi, onaylandı, reddedildi, revizyon istendi, süresi doldu olarak izlenir."),
         o('multi', 'Ürün / hizmet hattına göre birden çok huni', "Her ürün hattı, iş birimi ya da müşteri tipi için ayrı aşamalı huniler.", "Bireysel ve kurumsal satışın ya da farklı hizmet gruplarının farklı süreçle yürüdüğü projeler.", "\"Bireysel eğitim\" hunisi 4 aşamalı, \"Kurumsal eğitim\" hunisi teklif ve sözleşme aşamalı ayrı panolarda izlenir.",
           "Her huninin aşamaları ayrı tanımlanır, fırsat tek bir huniye aittir; raporlar huni bazında ve toplamda verilir, huniler arası taşımada aşama eşlemesi istenir."),
     ]},

    {'id': 'crm_routing', 'section': 'biz_crm', 'type': 'select', 'label': 'Lead Atama ve Dağıtım Kuralı', 'en': 'Lead Assignment & Routing', 'agents': [ROUTE, APP], 'showIf': G_CRM,
     'explanation': "Yeni gelen lead'in hangi satış temsilcisine, ekibe ya da iş ortağına atanacağını belirler.",
     'scenario': "Tek kişilik satışta elle atama yeter; birden çok temsilci varsa eşit dağıtım ya da bölge / ürün kuralı, bayi ağı varsa iş ortağına yönlendirme, yüksek hacimde puana göre öncelik gerekir.",
     'example': "İzmir'den gelen \"Kurumsal paket\" talebi kurala göre Ege bölge ekibine atanır; temsilci 2 saat içinde dokunmazsa ekip liderine uyarı düşer.",
     'rule': "Lead atama kuralı: {label}. Atama kuralları panelden yönetilir; atama ve yeniden atama geçmişi (kim, ne zaman, gerekçe) saklanır; tanımlı süre içinde işlem görmeyen lead için ekip liderine uyarı gider; temsilci yalnız kendisine ya da ekibine atanmış lead ve fırsatları görür, bu kısıt sunucuda kayıt düzeyinde uygulanır (istemciden gelen kayıt kimliğine güvenilmez).",
     'options': [
         o('manual', 'Elle atama (havuzdan alma)', "Lead ortak havuza düşer, yönetici atar ya da temsilci kendisi üstlenir.", "1–3 kişilik satış ekibi.", "Havuzdaki lead'in üzerinde \"Üstlen\" düğmesi; üstlenen temsilcinin adı kayda yazılır.",
           "Lead'ler atanmamış havuza düşer; üstlenme işlemi tek seferlik ve yarışa karşı korumalıdır (aynı lead iki kişiye atanamaz)."),
         o('round_robin', 'Sırayla eşit dağıtım (round-robin)', "Lead'ler uygun temsilcilere sırayla dağıtılır; izinli ya da kapasitesi dolu temsilci atlanır.", "Benzer işi yapan çok sayıda temsilci varsa.", "Sabah gelen 9 lead üç temsilciye üçer üçer dağıtılır.",
           "Dağıtım sırası sunucuda atomik sayaçla tutulur; izinli / pasif temsilci atlanır, temsilci başına günlük üst sınır tanımlanabilir."),
         o('territory', 'Bölge, ürün ya da kampanyaya göre kural (önerilen)', "İl / bölge, ürün-hizmet, dil, müşteri tipi ya da kampanyaya göre önceden tanımlı kurallar.", "Bölge ya da uzmanlık bazlı satış ekipleri.", "\"Ürün = Eğitim ve Firma büyüklüğü ≥ 50\" ise Kurumsal Eğitim ekibine; diğerleri İç Satış ekibine.",
           "Kurallar öncelik sırasıyla değerlendirilir, ilk eşleşen uygulanır; hiçbir kural eşleşmezse varsayılan ekibe atanır ve bu durum raporlanır."),
         o('partner', 'İş ortağına / bayiye yönlendirme', "Belirli bölge ya da ürün lead'leri yetkili iş ortağına gönderilir.", "Bayi, distribütör ya da franchise ağıyla satış yapılıyorsa.", "Antalya'dan gelen talep yetkili bayinin portalına düşer; bayi 24 saatte dönmezse lead merkeze geri alınır.",
           "İş ortağına yalnız lead'i işlemek için gereken alanlar aktarılır (veri minimizasyonu), aktarım KVKK kapsamında aktarım olarak kaydedilir; iş ortağı yalnız kendisine yönlendirilen kayıtları görür."),
         o('score', 'Puana ve önceliğe göre', "Yüksek puanlı (sıcak) lead'ler deneyimli temsilcilere ya da hızlı yanıt kuyruğuna gider.", "Yüksek hacimli lead ve sınırlı satış kapasitesi.", "Puanı 80 üstü lead \"Sıcak\" kuyruğuna ve kıdemli temsilciye, 40 altı pazarlama besleme akışına gider.",
           "Atama, lead puanı hesaplandıktan sonra yapılır; puan eşikleri panelden yönetilir, düşük puanlı lead satışa değil pazarlama besleme akışına yönlendirilir."),
     ]},

    {'id': 'crm_scoring', 'section': 'biz_crm', 'type': 'multiselect', 'label': 'Lead Puanlama, Mükerrer ve Spam Kontrolü', 'en': 'Lead Scoring, Deduplication & Spam Filtering', 'agents': [SCORE, CRM_DQ, APP], 'showIf': G_CRM,
     'explanation': "Lead kalitesinin nasıl ölçüleceğini (puanlama, MQL / SQL eşikleri, segmentler) ve kirli verinin nasıl ayıklanacağını (mükerrer, spam, düşük kalite) belirler. Paneldeki CRM menüsünde \"Skorlama ve Segmentler\" ile \"Mükerrer Kayıtlar\" ekranlarının davranışı bu karardan gelir.",
     'scenario': "Lead sayısı arttıkça satış ekibinin hangi lead'e önce döneceğini bilmesi, aynı kişinin birden çok kayıtla görünmemesi ve bot gönderimlerinin ekibi meşgul etmemesi gerekiyorsa.",
     'example': "\"Mükerrer Kayıtlar\" ekranında aynı e-posta ve telefona sahip iki kayıt yan yana gösterilir; yetkili kullanıcı alanları seçip \"Birleştir\" der, iki kaydın aktivite geçmişi tek kayıtta toplanır.",
     'rule': "Lead kalitesi denetimleri: {labels}. Puan ve sınıflandırma kuralları panelden yönetilir ve sürümlenir; her puan değişikliği hangi kuraldan geldiğiyle kayıtta görünür; mükerrer birleştirme ve spam işaretleme geri alınabilir ve denetim kaydına yazılır; spam / düşük kalite kayıtları silinmez, işaretlenip satış kuyruğundan çıkarılır ve saklama süresi sonunda imha edilir.",
     'options': [
         o('scoring', 'Lead puanlama (sıcak / ılık / soğuk)', "Kaynak, form bilgisi (firma büyüklüğü, sektör), sayfa ziyareti, e-posta etkileşimi, etkinlik katılımı gibi kriterlere puan verilir.", "Satış ekibi lead'leri önceliklendirmekte zorlanıyorsa.", "Fiyatlandırma sayfasını 3 kez ziyaret eden ve demo formu dolduran lead 85 puanla \"Sıcak\" etiketi alır.",
           "Puan demografik ve davranışsal bileşenlerle sunucuda hesaplanır; davranış verisi yalnız çerez / izleme onayı olan ziyaretçiden toplanır; puan geçmişi kayıtta tutulur."),
         o('mql_sql', 'MQL / SQL eşikleri ve devir kuralı', "Pazarlamaya uygun lead (MQL) ve satışa uygun lead (SQL) ölçütleri ile devir kuralı.", "Pazarlama ve satış ekipleri ayrıysa.", "Puan ≥ 60 olan lead MQL olur ve satışa devredilir; temsilci ilk görüşmeden sonra SQL ya da \"uygun değil\" olarak işaretler.",
           "MQL ve SQL ölçütleri panelden tanımlanır; geçişler otomatik ya da temsilci onayıyla yapılır ve tarihleriyle kaydedilir; MQL → SQL dönüşüm oranı raporlanır."),
         o('segments', 'Etiket ve dinamik segmentler', "Sektör, bölge, ilgi alanı, aşama ve davranışa göre kendiliğinden güncellenen segmentler.", "Kampanya ve pazarlama otomasyonu segmentlerle çalışıyorsa.", "\"Son 30 günde eğitim sayfasını gezen, İstanbul'daki KOBİ'ler\" segmenti her gün kendiliğinden güncellenir.",
           "Segment koşulları sunucuda değerlendirilir; pazarlama iletisi gönderilecek segmentler izin durumu (İYS, abonelik tercihi) filtresinden geçer."),
         o('dedupe', 'Mükerrer kayıt tespiti ve onaylı birleştirme (önerilen)', "E-posta, normalize edilmiş telefon ve şirket adına göre mükerrer adayları bulunur; birleştirme yetkili onayıyla yapılır.", "Birden çok kaynaktan lead geliyorsa (neredeyse her proje).", "Aynı telefonla gelen iki kayıt \"Olası mükerrer\" rozetiyle işaretlenir.",
           "E-posta küçük harfe, telefon E.164 biçimine normalize edilip benzersizlik kontrolü yapılır; birleştirmede alan bazlı seçim yapılır, iki kaydın aktivite ve izin geçmişi korunur, birleştirme geri alınabilir."),
         o('spam', 'Bot ve spam filtresi', "Görünmez bot doğrulaması (Cloudflare Turnstile vb.), bal küpü (honeypot) alanı, hız sınırı ve tek kullanımlık e-posta alan adı kontrolü.", "Herkese açık formu olan her proje.", "Bot gönderimi panelde lead olarak görünmez, \"Engellenen gönderim\" sayacına yazılır.",
           "Bot doğrulaması sunucuda token doğrulamasıyla yapılır; başarısız gönderimler lead oluşturmaz, yalnız sayısal olarak raporlanır."),
         o('low_quality', 'Düşük kalite işaretleme', "Geçersiz telefon, anlamsız ad, rakip firma, hedef dışı ülke gibi kriterlerle lead'in düşük kalite olarak işaretlenmesi.", "Reklam kampanyaları çok sayıda niteliksiz lead getiriyorsa.", "Telefonu 10 haneden kısa ve adı \"test\" olan lead \"Düşük kalite\" etiketiyle satış kuyruğundan çıkar; kaynak kampanya raporunda ayrıca görünür.",
           "Düşük kalite kriterleri panelden yönetilir; işaretli lead satış kuyruğundan çıkar ama silinmez, kampanya kalite raporunda sayılır."),
     ]},

    {'id': 'crm_activity', 'section': 'biz_crm', 'type': 'multiselect', 'label': 'Aktivite, Teklif ve Müşteri Zaman Çizelgesi', 'en': 'Activities, Quotes & Customer Timeline', 'agents': [CRM_SR, APP], 'showIf': G_CRM,
     'explanation': "Lead ve müşteriyle yapılan iletişimin, görevlerin, tekliflerin ve diğer modüllerdeki olayların CRM'de nasıl kaydedileceğini belirler. Paneldeki CRM menüsünün \"Teklif Oluşturma\" ekranının davranışı bu karardan gelir.",
     'scenario': "Müşteriyle kimin, ne zaman, ne konuştuğu bilinmiyor, takip aramaları unutuluyor ya da teklifler Word dosyalarında kayboluyorsa.",
     'example': "Müşteri kartında zaman çizelgesi: \"12 Kas 10:14 Teklif görüntülendi · 11 Kas Teklif TKL-2026-118 gönderildi (184.000 TL + KDV) · 9 Kas Telefon görüşmesi (not) · 8 Kas Destek talebi kapandı · CSAT 5/5\".",
     'rule': "CRM aktivite ve teklif kapsamı: {labels}. Bütün aktiviteler kullanıcı, tarih, kanal ve aktivite türüyle kaydedilir ve bu alanlara göre süzülebilir; zaman çizelgesindeki kayıtlar ilgili modül kaydına bağlantı verir; kişisel veri içeren notlar yalnız yetkili rollerce görülür ve uygulama loglarına yazılmaz.",
     'recommend': {'field': 'modules_extra', 'map': {'ticket': ['module_timeline'], 'survey': ['module_timeline'], 'subscription': ['module_timeline'], 'booking': ['module_timeline'], 'lms': ['module_timeline'], 'ecommerce': ['module_timeline'], 'consulting': ['module_timeline']}},
     'options': [
         o('timeline', 'Birleşik müşteri zaman çizelgesi (önerilen)', "Lead / müşteri kartında bütün etkileşimlerin kronolojik akışı.", "Her CRM kurulumu.", "Kartta en yeni olay en üstte, türüne göre simgeli ve süzülebilir liste.",
           "Zaman çizelgesi ekleme yapılan (append-only) bir aktivite tablosundan okunur; olaylar sonradan düzenlenemez, yalnız düzeltme notu eklenir."),
         o('tasks', 'Görev ve hatırlatıcılar', "Temsilciye tarihli görev (ara, e-posta gönder, toplantı) atanması ve hatırlatma.", "Takip aramalarının unutulduğu ekipler.", "\"Perşembe 14:00 teklif sonrası takip araması\" görevi, saatinde temsilciye bildirim olarak düşer.",
           "Görevler sorumlu, son tarih ve durumla tutulur; gecikmiş görevler temsilci ve ekip liderine panelde gösterilir."),
         o('comms', 'E-posta, telefon ve toplantı kaydı', "Gönderilen / gelen e-postaların, görüşme notlarının ve toplantıların lead'e bağlanması.", "Satış iletişimi e-posta ve telefonla yürüyorsa.", "Temsilcinin CRM'den gönderdiği e-posta ve müşterinin yanıtı aynı kartta konuşma olarak görünür.",
           "CRM'den gönderilen e-postalar işlemsel e-posta sağlayıcısı üzerinden gönderilir ve kaydedilir; gelen yanıtlar konu kimliğiyle eşlenir, ekler güvenli depolamada tutulur."),
         o('quotes', 'Fırsattan teklif oluşturma', "Fırsat üzerindeki ürün / hizmet satırlarından numaralı teklif üretilmesi, paylaşılması ve durumunun izlenmesi.", "Teklifle satış yapılan B2B projeler.", "\"Teklif oluştur\" ile fırsat satırlarından PDF teklif üretilir, müşteriye güvenli bağlantıyla gönderilir; müşteri açınca durum \"Görüntülendi\" olur.",
           "Teklif tutarları sunucuda fiyat listesinden ve iskonto yetkisinden hesaplanır (istemciden gelen tutara güvenilmez); teklif sürümlenir, gönderilen sürüm değiştirilemez; durumlar gönderildi, görüntülendi, onaylandı, reddedildi, revizyon istendi, süresi doldu; paylaşım bağlantısı tahmin edilemez ve süreli."),
         o('module_timeline', 'Diğer modül olaylarının zaman çizelgesine yazılması', "Sipariş, rezervasyon, eğitim, destek talebi, anket yanıtı, abonelik ve danışmanlık olaylarının müşteri kartında görünmesi.", "Projede başka iş modülleri de varsa.", "Kartta \"Abonelik yenilendi\", \"Destek talebi açıldı\", \"NPS 9\" olayları satış görüşmelerinin yanında görünür.",
           "Modüller CRM'e ortak olay sözleşmesiyle (olay türü, kayıt kimliği, zaman, özet) yazar; ayrıntı kaynak modülde kalır, CRM yalnız özet ve bağlantı tutar."),
         o('automation', 'Durum değişikliğinde otomasyon', "Aşama, puan ya da segment değişince görev açma, e-posta gönderme ya da pazarlama akışını tetikleme.", "Satış ve pazarlama süreçleri tekrarlayan adımlar içeriyorsa.", "Teklif 5 gün görüntülenmezse temsilciye görev, 10 gün yanıtsız kalırsa müşteriye hatırlatma e-postası.",
           "Otomasyon kuralları panelden yönetilir, kuyrukla çalışır ve idempotenttir (aynı olay ikinci kez tetiklemez); pazarlama iletisi gönderen kurallar izin kontrolünden geçer."),
         o('reports', 'Satış hunisi raporları ve KPI panosu', "Dönüşüm oranları, pipeline değeri, kazanılan gelir, ortalama kapanış süresi, temsilci ve kaynak bazlı performans.", "Satış yönetimi performansı izliyorsa.", "Panoda \"Lead → MQL %32 · MQL → SQL %41 · Teklif kabul oranı %28 · Ortalama kapanış 23 gün\".",
           "KPI'lar tek tanımlı metrik sözlüğünden hesaplanır; temsilci yalnız kendi, yönetici ekibinin verisini görür; raporlar dışa aktarılırken kişisel veri sütunları yetkiye göre maskelenir."),
     ]},

    {'id': 'crm_sync', 'section': 'biz_crm', 'type': 'select', 'label': 'Dış CRM Senkronu', 'en': 'Third-Party CRM Integration', 'agents': [INT, CRM_SR, KVKK], 'showIf': G_CRM,
     'explanation': "Sitedeki CRM verisinin harici bir CRM platformuyla (HubSpot, Salesforce, Pipedrive, Zoho, Microsoft Dynamics …) senkronize edilip edilmeyeceğini belirler.",
     'scenario': "Satış ekibi zaten bir CRM kullanıyorsa ve verinin iki yerde ayrı ayrı tutulması istenmiyorsa; hiç CRM yoksa sitedeki yerleşik CRM yeterli olabilir.",
     'example': "Sitede oluşan lead 30 saniye içinde HubSpot'ta kişi olarak görünür; HubSpot'ta fırsat \"Kazanıldı\" yapılınca sitedeki müşteri kaydı da güncellenir.",
     'rule': "Dış CRM senkronu: {label}. Entegrasyon OAuth 2.0 ya da en dar kapsamlı API belirteciyle yapılır, gizli değerler yalnız sunucu tarafındaki gizli anahtar deposunda tutulur; senkron kuyruk üzerinden, dış kayıt kimliği eşlemesiyle idempotent upsert olarak çalışır; hata alan kayıtlar artan aralıklı yeniden denenir, kalıcı hatalar ayrı kuyrukta (dead-letter) panelde gösterilir; alan eşlemesi (field mapping) panelden yönetilir ve yalnız gerekli alanlar aktarılır; sunucuları yurt dışında olan CRM'e aktarımın KVKK m. 9 dayanağı hukuk birimince teyit edilir ve aydınlatma metnine yazılır.",
     'options': [
         o('none', 'Dış CRM yok — yerleşik CRM (önerilen)', "Bütün CRM işlevleri sitenin kendi yönetim panelinde çalışır.", "Henüz CRM kullanmayan ya da küçük ekipli kurumlar.", "Satış ekibi lead ve fırsatları sitenin panelindeki CRM menüsünden yönetir.",
           "Dış CRM bağlantısı kurulmaz; ileride bağlanabilmesi için kayıtlarda dış kimlik alanı ve olay kuyruğu yine hazırlanır."),
         o('hubspot', 'HubSpot', "HubSpot CRM ile kişi, şirket ve fırsat senkronu.", "Pazarlama ve satışta HubSpot kullanılıyorsa.", "Sitedeki lead HubSpot'ta kişi olarak, kaynak ve UTM özel özelliklere yazılmış olarak oluşur.",
           "HubSpot CRM API'leri (contacts, companies, deals, associations) kullanılır; eşleme e-posta ve dış kimlik özelliğiyle yapılır, API oran sınırlarına uyulur."),
         o('salesforce', 'Salesforce', "Salesforce Sales Cloud ile Lead, Contact, Account ve Opportunity senkronu.", "Kurumsal satış ekibi Salesforce kullanıyorsa.", "Web lead'i Salesforce'ta Lead nesnesi olarak açılır; dönüştürüldüğünde site kaydı fırsat kimliğiyle güncellenir.",
           "Salesforce REST API'si ve bağlı uygulama (connected app) ile OAuth kullanılır; upsert harici kimlik alanı (external ID) üzerinden yapılır."),
         o('pipedrive', 'Pipedrive', "Pipedrive ile kişi, kuruluş ve deal senkronu.", "KOBİ satış ekibi Pipedrive kullanıyorsa.", "Lead Pipedrive'da \"Leads Inbox\"a düşer; deal aşaması değişince sitedeki fırsat aşaması güncellenir.",
           "Pipedrive API'si ve webhook'ları kullanılır; aşama eşlemesi iki sistemin aşama kimlikleriyle panelde tanımlanır."),
         o('zoho', 'Zoho CRM', "Zoho CRM ile Leads, Contacts, Accounts ve Deals senkronu.", "Zoho ekosistemi kullanılıyorsa.", "Form lead'i Zoho CRM'de Leads modülüne kaynak alanıyla birlikte yazılır.",
           "Zoho CRM API'sinin upsert uç noktası ve tekrar eden kayıt kontrol alanları kullanılır; veri merkezi bölgesi (ör. EU) hesapla aynı seçilir."),
         o('dynamics', 'Microsoft Dynamics 365', "Dynamics 365 Sales ile Dataverse Web API üzerinden senkron.", "Microsoft altyapısı kullanan kurumsal yapılar.", "Lead Dynamics'te lead tablosuna yazılır, nitelendirildiğinde fırsat kimliği siteye geri döner.",
           "Dataverse Web API ve Microsoft Entra ID uygulama kaydı ile yalnız gerekli tablo izinleri verilir."),
         o('other', 'Diğer CRM (API / webhook)', "Yerli ya da sektöre özel bir CRM ile özel API / webhook entegrasyonu.", "Kurumun kendi CRM'i ya da listede olmayan bir ürün varsa.", "Lead imzalı webhook ile kurumun CRM'ine gönderilir, yanıt olarak CRM kayıt numarası alınır.",
           "Entegrasyon sözleşmesi (alanlar, kimlik eşlemesi, hata kodları, oran sınırı) yazılı olarak belirlenir; giden webhook'lar imzalanır, gelenlerin imzası doğrulanır."),
     ]},

    {'id': 'crm_sync_dir', 'section': 'biz_crm', 'type': 'select', 'label': 'Senkron Yönü ve Çakışma Kuralı', 'en': 'Sync Direction & Conflict Resolution', 'agents': [INT, CRM_DQ], 'showIf': G_CRM + [{'field': 'crm_sync', 'in': ['hubspot', 'salesforce', 'pipedrive', 'zoho', 'dynamics', 'other']}],
     'explanation': "Verinin hangi yönde aktığını ve iki sistemde aynı alan farklı değiştirildiğinde hangisinin geçerli olacağını belirler.",
     'scenario': "Satış ekibi yalnız dış CRM'de çalışıyorsa tek yön yeter; site panelinde de aşama ve not güncelleniyorsa çift yönlü senkron ve açık bir çakışma kuralı gerekir.",
     'example': "Alan sahipliği tablosu: \"Kaynak, UTM, form yanıtları → site sahibi · Aşama, tutar, sorumlu → CRM sahibi\"; CRM'de değişen aşama siteye yansır, sitedeki kaynak alanı CRM'den ezilemez.",
     'rule': "Senkron yönü ve çakışma kuralı: {label}. Senkron döngüye girmesin diye her değişiklik kaynağıyla etiketlenir ve kendi kaynağına geri yazılmaz; çakışmalar ve reddedilen güncellemeler panelde listelenir.",
     'options': [
         o('out', 'Tek yön: site → dış CRM (önerilen)', "Lead ve aktiviteler sitede oluşur ve dış CRM'e gönderilir; satış süreci dış CRM'de yürür.", "Satış ekibi tamamen dış CRM'de çalışıyorsa.", "Form lead'i CRM'e gider; CRM'deki değişiklik siteye dönmez.",
           "Yalnız site → CRM yönünde yazılır; sitedeki CRM ekranları salt okunur özet gösterir ve kayıt CRM'deki karta bağlantı verir."),
         o('two_way', 'Çift yönlü, alan sahipliğiyle', "İki sistem de yazar; her alanın sahibi tek sistemdir, sahip olmayan sistemin değişikliği yok sayılır ve raporlanır.", "Satış dış CRM'de, operasyon ve müşteri portalı sitede yürüyorsa.", "Aşama CRM'den, iletişim izni siteden gelir; iki tarafta da güncel görünür.",
           "Alan sahipliği tablosu panelde tanımlanır; \"son yazan kazanır\" kuralı kullanılmaz; aynı alanda kısa aralıkta çakışan değişiklikler insan onayına düşer."),
         o('in', 'Tek yön: dış CRM → site', "Müşteri ve aşama verisi dış CRM'de yönetilir, site yalnız okur (ör. müşteri portalında gösterim).", "CRM ana kayıt sistemi, site yalnız müşteri yüzü ise.", "CRM'de \"Kazanıldı\" olan müşteri için sitede portal hesabı açılır.",
           "Site dış CRM'deki kayıtları okur ve önbellekler; sitede değiştirilen müşteri verisi dış CRM'e API ile yazılmaz, kullanıcıya CRM'de güncelleme talebi olarak iletilir."),
     ]},
]

# ---------------------------------------------------------------- B2 Destek Talebi ve Bilgi Bankası
S_TK = {
    'id': 'biz_ticket', 'group': 'İş Modülleri', 'icon': '⚑',
    'name': 'Destek Talebi ve Bilgi Bankası', 'en': 'Support Tickets, Help Desk & Knowledge Base',
    'desc': "Destek taleplerinin hangi kanallardan açılacağını, kategori / öncelik / durum yapısını, SLA ve üst kademeye aktarma (eskalasyon) kurallarını, atamayı, bilgi bankası, müşteri portalı ve CRM bağlantısını karara bağlar",
    'guide': {
        'purpose': "Destek Talebi (ticket) modülü müşteri, üye, kurumsal kullanıcı ya da iş ortağından gelen her talebi numaralı bir kayıt olarak açar; kategori ve öncelikle sınıflandırır, doğru ekibe atar, ilk yanıt ve çözüm sürelerini (SLA) izler, gecikmede üst kademeye aktarır (eskalasyon) ve kapanışta memnuniyet ölçer. Bilgi bankası (yardım merkezi) sık sorulan sorunları makale olarak sunup talep sayısını azaltır. Bu bölüm talep kanallarını, kategori / öncelik / durum yapısını, SLA modelini, atama kuralını ve self-servis ile portal / CRM bağlantılarını belirler. Hizmet yönetimi süreçleri için ITIL ve ISO/IEC 20000 iyi uygulamaları, şikâyet yönetimi için ISO 10002 yol göstericidir.",
        'criteria': [
            "Her talep tek bir numara alır ve hangi kanaldan gelirse gelsin aynı kayıt üzerinde yürür; e-posta yanıtları yeni talep açmaz, mevcut talebe eklenir.",
            "Müşteriye görünen yanıt ile yalnız ekibin gördüğü iç not arayüzde ve veritabanında ayrıdır; iç not hiçbir kanaldan müşteriye gitmez.",
            "SLA saati talep açılınca başlar, \"müşteri yanıtı bekleniyor\"da durur, iş saati takvimi ve resmî tatillerle hesaplanır; ihlale yaklaşan talep için önceden uyarı verilir.",
            "Destek personeli yalnız kendisine ya da ekibine atanmış talepleri görür; kurumsal müşteri yalnız kendi şirketinin taleplerini görür; bu kısıt sunucuda uygulanır.",
            "Dosya ekleri tür / boyut denetiminden ve zararlı yazılım taramasından geçer, herkese açık adresle değil süreli ve yetkili bağlantıyla indirilir.",
            "Talep kayıtları için saklama süresi, arşivleme ve anonimleştirme kuralı tanımlıdır; talepte geçen kart numarası gibi hassas veriler maskelenir.",
        ],
        'pitfalls': [
            "Destek için ortak bir e-posta kutusu kullanmak: kimin baktığı, ne kadar sürede yanıtlandığı ve tekrar eden sorunlar ölçülemez.",
            "İç notun e-posta yanıtına yanlışlıkla eklenebildiği tasarım: iç değerlendirmeler ve kişisel veri müşteriye sızar.",
            "SLA'yı takvim saatiyle hesaplamak: hafta sonu açılan talep pazartesi sabahı ihlal görünür, ekip gerçek performansını göremez.",
            "Talep numarasını ardışık ve tahmin edilebilir yapıp yetkiyi yalnız arayüzde denetlemek: başka müşterinin talebi adres değiştirilerek açılabilir (IDOR).",
            "Kapanan talebi süresiz yeniden açılabilir bırakmak: aylar sonra farklı bir konu eski talebin altına yazılır, raporlar bozulur.",
            "Bilgi bankası makalelerini güncellemeden yayında tutmak: yanlış yönlendirme talep sayısını azaltmak yerine artırır.",
        ],
        'resources': [
            {'title': "PeopleCert — ITIL sertifikaları ve ITIL 4", 'url': 'https://www.peoplecert.org/browse-certifications/it-governance-and-service-management/ITIL-1', 'note': "Olay, talep ve problem yönetimi gibi hizmet yönetimi uygulamalarının resmî çerçevesi."},
            {'title': "Zendesk — Defining SLA policies", 'url': 'https://support.zendesk.com/hc/en-us/articles/4408829459866-Defining-SLA-policies', 'note': "İlk yanıt, sonraki yanıt ve çözüm süresi hedeflerinin önceliğe göre tanımlanmasına örnek."},
            {'title': "RFC 5322 — Internet Message Format", 'url': 'https://www.rfc-editor.org/rfc/rfc5322', 'note': "E-posta yanıtlarını doğru talebe eklemek için Message-ID, In-Reply-To ve References başlıkları."},
            {'title': "OWASP — File Upload Cheat Sheet", 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html', 'note': "Talep eklerinin güvenli alınması, doğrulanması ve saklanması."},
            {'title': "KVKK — Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi", 'url': 'https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi', 'note': "Kapanmış talep kayıtlarının saklama süresi sonunda imhası ve anonimleştirilmesi."},
            {'title': "KVKK — İlgili Kişiler Tarafından Yapılan Başvuruların Cevaplanması Yükümlülüğü", 'url': 'https://www.kvkk.gov.tr/Icerik/2046/Ilgili-Kisiler-Tarafindan-Yapilan-Basvurularin-Cevaplanmasi-Yukumlulugu', 'note': "Destek kanalından gelen KVKK başvurularının ayrı süreçle ve yasal sürede yanıtlanması."},
            {'title': "T.C. Ticaret Bakanlığı — Tüketicinin Korunması ve Piyasa Gözetimi Genel Müdürlüğü", 'url': 'https://tuketici.ticaret.gov.tr/', 'note': "Tüketici şikâyetleri ve tüketici hakem heyeti süreçleri hakkında resmî bilgi."},
            {'title': "W3C WAI — Forms Tutorial", 'url': 'https://www.w3.org/WAI/tutorials/forms/', 'note': "Talep açma formunun etiket, hata mesajı ve klavye erişilebilirliği."},
        ],
    },
}

F_TK = [
    {'id': 'tk_channels', 'section': 'biz_ticket', 'type': 'multiselect', 'label': 'Talep Açma Kanalları', 'en': 'Ticket Intake Channels', 'agents': [OMNI, APP], 'showIf': G_TK,
     'explanation': "Destek taleplerinin hangi kanallardan ticket kaydına dönüşeceğini belirler. Bütün kanallar aynı talep kaydına ve numaralandırmaya yazar.",
     'scenario': "Müşterilerin desteğe ulaştığı kanalların hepsi kayıt altına alınmak isteniyorsa; özellikle e-posta, WhatsApp ve canlı destek ayrı ayrı izleniyorsa.",
     'example': "Müşteri destek@ adresine yazar; #TK-2026-01482 numaralı talep açılır, otomatik yanıtta numara bildirilir; müşterinin sonraki e-postaları aynı talebe eklenir.",
     'rule': "Destek talebi açma kanalları: {labels}. Her kanal aynı talep kaydını oluşturur; talep numarası tahmin edilemeyen iç kimlikten ayrı, okunur bir numaradır; kaynak kanal, ilişkili kayıt (sipariş, rezervasyon, eğitim, abonelik) ve müşteri profiliyle birlikte saklanır; talep açılınca müşteriye numaralı alındı bildirimi gönderilir.",
     'recommend': {'field': 'modules_extra', 'map': {'portal': ['portal'], 'support_ai': ['chat'], 'ecommerce': ['system'], 'booking': ['system'], 'subscription': ['system']}},
     'options': [
         o('web_form', 'Sitedeki destek formu (önerilen)', "Kategori seçimli, ekli dosya alabilen destek formu.", "Her projede temel kanal.", "\"Destek talebi oluştur\" formunda konu seçilince ilgili yardım makaleleri önerilir.",
           "Form sunucuda doğrulanır, bot korumalıdır; giriş yapmamış kullanıcıdan gelen talep e-posta doğrulamasıyla müşteri kaydına bağlanır."),
         o('portal', 'Müşteri portalı', "Giriş yapmış kullanıcının portaldan talep açması, izlemesi ve yanıtlaması.", "Üyelik ya da müşteri portalı varsa.", "Portalda \"Taleplerim\" listesi ve talep detayında yazışma geçmişi.",
           "Portal talepleri oturumdaki kullanıcıya bağlanır; kullanıcı yalnız kendi (kurumsal hesapta yetkisi varsa şirketinin) taleplerini görür."),
         o('email', 'E-posta', "Destek adresine gelen e-postaların talebe dönüşmesi.", "Müşteriler desteğe e-postayla yazıyorsa.", "Yanıt e-postası konu satırındaki numara ve e-posta başlıklarıyla doğru talebe eklenir.",
           "Gelen e-postalar Message-ID / In-Reply-To başlıklarıyla mevcut talebe eşlenir; otomatik yanıtlar ve geri dönen iletiler döngü oluşturmaz; ekler taramadan geçer."),
         o('chat', 'Canlı destek ve sohbet botu', "Çözülemeyen canlı destek ya da bot konuşmasının talebe dönüştürülmesi.", "Canlı destek / AI sohbet modülü varsa.", "Bot \"Bunu destek ekibine iletiyorum\" der; konuşma dökümü ekli talep açılır.",
           "Sohbetten talep açılırken konuşma dökümü talebe eklenir, müşteriye talep numarası sohbette gösterilir."),
         o('whatsapp', 'WhatsApp', "WhatsApp Business hattından gelen destek mesajları.", "Müşteriler WhatsApp'ı tercih ediyorsa.", "WhatsApp'tan yazan müşteriye talep numarası iletilir, temsilci yanıtını panelden verir.",
           "WhatsApp mesajları resmî Business Platform entegrasyonuyla alınır; 24 saatlik hizmet penceresi dışındaki yanıtlar onaylı şablonla gönderilir."),
         o('phone', 'Telefon / çağrı merkezi', "Çağrı sırasında temsilcinin panelde talep açması.", "Telefon desteği veriliyorsa.", "Temsilci arayanın numarasıyla müşteri kartını açar, \"Talep oluştur\" der.",
           "Telefonla açılan talepte kanal \"Telefon\" ve açan temsilci kaydedilir; çağrı kaydı tutuluyorsa ayrı aydınlatma yapılır."),
         o('admin', 'Panelden müşteri adına', "Satış, operasyon ya da muhasebe ekibinin müşteri adına talep açması.", "İç ekipler müşteri sorunlarını desteğe aktarıyorsa.", "Muhasebe ekibi \"Fatura düzeltme\" talebini müşteri adına açar, müşteri bilgilendirilir.",
           "Müşteri adına açılan talepte açan kullanıcı ve gerekçe kaydedilir."),
         o('system', 'Sistem olaylarından otomatik', "Ödeme hatası, rezervasyon sorunu, eğitim erişim hatası gibi olayların kendiliğinden talep açması.", "Kritik işlem hatalarının proaktif ele alınması isteniyorsa.", "Abonelik tahsilatı üçüncü kez başarısız olunca müşteri için \"Ödeme sorunu\" talebi açılır.",
           "Otomatik talepler olay türü ve kayıt kimliğiyle tekilleştirilir; aynı olay için ikinci talep açılmaz."),
     ]},

    {'id': 'tk_structure', 'section': 'biz_ticket', 'type': 'multiselect', 'label': 'Kategori, Öncelik, Durum ve Yanıt Yapısı', 'en': 'Categories, Priorities, Statuses & Replies', 'agents': [SUP_SR, APP], 'showIf': G_TK,
     'explanation': "Taleplerin nasıl sınıflandırılacağını, hangi durumlardan geçeceğini ve müşteri yanıtı ile iç notun nasıl ayrılacağını belirler.",
     'scenario': "Talepler farklı konularda geliyor, farklı ekiplerce ele alınıyor ve aciliyeti değişiyorsa; müşteriye görünmemesi gereken iç değerlendirmeler yazılıyorsa.",
     'example': "Talep: \"Kategori: Ödeme › İade · Öncelik: Yüksek · Durum: İşlemde\"; altında müşteriye giden yanıt beyaz, sarı zeminli \"İç not — yalnız ekip görür\" kutusu ayrı.",
     'rule': "Talep yapısı: {labels}. Durum seti Yeni → Açık → Atandı → İşlemde → Müşteri yanıtı bekleniyor / İç ekip yanıtı bekleniyor → Çözüldü → Kapandı (+ Yeniden açıldı, İptal edildi) olarak kurulur; durum geçişleri sunucudaki izinli geçiş tablosuna göre yapılır ve kullanıcı, tarih, gerekçeyle kaydedilir; müşteri yanıtı ile iç not ayrı kayıt türüdür, iç not hiçbir bildirim ya da portal ekranında müşteriye gösterilmez.",
     'options': [
         o('categories', 'Kategori ve alt kategoriler (önerilen)', "Teknik destek, ödeme, fatura, iade, rezervasyon, eğitim, hesap erişimi gibi kategoriler ve alt kategoriler.", "Her destek kurulumu.", "\"Hesap erişimi › Şifre sıfırlama\" seçilince talep varsayılan olarak Birinci Seviye ekibe gider.",
           "Kategoriler panelden yönetilir; her kategoriye varsayılan ekip, öncelik ve SLA bağlanır."),
         o('priorities', 'Öncelik seviyeleri (düşük / normal / yüksek / kritik)', "Talebin aciliyetini gösteren dört seviye.", "SLA önceliğe göre değişiyorsa.", "\"Kritik — ödeme alınamıyor\" talebi kuyruğun en üstünde kırmızı rozetle görünür.",
           "Öncelik müşteri tarafından önerilebilir ama son kararı destek ekibi verir; kritik öncelik ekip liderine anında bildirim üretir."),
         o('auto_close', 'Çözülen talebin otomatik kapanması', "\"Çözüldü\" talebe müşteri belirli gün içinde yanıt vermezse talep kapanır.", "Açık bekleyen talep sayısı şişiyorsa.", "Çözüldü bildiriminden 5 gün sonra yanıt gelmezse talep \"Kapandı\" olur ve müşteriye bilgi gider.",
           "Otomatik kapanma süresi panelden tanımlanır; kapanan talep tanımlı süre içinde müşteri yanıtıyla yeniden açılır, süre sonunda yeni talep açılır ve eski talebe bağlanır."),
         o('merge', 'Mükerrer talep birleştirme', "Aynı müşterinin aynı konu için açtığı talepler birleştirilir.", "Müşteriler aynı konuda birden çok kanaldan yazıyorsa.", "E-posta ve WhatsApp'tan gelen iki talep tek talepte birleşir, diğeri \"Birleştirildi\" olur.",
           "Birleştirme yalnız aynı müşteri (ya da aynı kurumsal hesap) talepleri arasında ve yetkili kullanıcıca yapılır; yazışma geçmişi korunur."),
         o('canned', 'Hazır yanıt şablonları', "Kategori, dil ve kanala göre hazır yanıtlar.", "Tekrarlayan sorular çoksa.", "Temsilci \"/iade-suresi\" yazınca onaylı iade süresi yanıtı eklenir, düzenleyip gönderir.",
           "Şablonlar dil ve marka bazında yönetilir, değişkenler (ad, talep no) sunucuda doldurulur; şablon metni kaçışlanarak işlenir."),
         o('attachments', 'Güvenli dosya ekleri', "Müşteri ve ekibin ekran görüntüsü, belge ekleyebilmesi.", "Teknik destek ya da belge isteyen süreçler.", "Müşteri hata ekran görüntüsünü ekler; ek yalnız talep tarafları için süreli bağlantıyla açılır.",
           "Ekler izinli tür ve boyut listesiyle sınırlanır, zararlı yazılım taramasından geçer, özel depolamada tutulur ve süreli imzalı adresle sunulur."),
         o('masking', 'Hassas veri maskeleme', "Talep metnindeki kart numarası, T.C. kimlik numarası gibi verilerin otomatik maskelenmesi.", "Ödeme ve kimlik içeren konular destekte konuşuluyorsa.", "Müşterinin yazdığı kart numarası kayıtta \"**** **** **** 4242\" olarak görünür.",
           "Kart numarası (Luhn denetimli) ve T.C. kimlik numarası kalıpları kayıttan önce maskelenir; tam değer hiçbir yerde saklanmaz ve loglara yazılmaz."),
     ]},

    {'id': 'tk_sla', 'section': 'biz_ticket', 'type': 'select', 'label': 'SLA ve Üst Kademeye Aktarma (Eskalasyon)', 'en': 'SLA & Escalation', 'agents': [ESC, SUP_SR], 'showIf': G_TK,
     'explanation': "İlk yanıt ve çözüm sürelerinin (SLA, hizmet düzeyi hedefi) nasıl belirleneceğini ve süre aşımında talebin kime aktarılacağını belirler.",
     'scenario': "Destek hızı müşteri memnuniyetini ya da sözleşme yükümlülüğünü etkiliyorsa; kurumsal müşterilere farklı hizmet düzeyi taahhüt ediliyorsa.",
     'example': "\"Yüksek\" öncelikli talebin ilk yanıt hedefi 4 iş saati; 3 saat 12 dakikada SLA rozeti turuncuya döner, 4 saatte ekip liderine eskalasyon bildirimi gider.",
     'rule': "SLA modeli: {label}. SLA saati talep açılınca başlar, \"Müşteri yanıtı bekleniyor\"da durur, iş saati takvimi ve resmî tatillere göre hesaplanır; ihlale yaklaşan talep için önceden uyarı, ihlalde sorumlu kullanıcıya ve ekip liderine bildirim gider; SLA uyum oranı, ortalama ilk yanıt ve çözüm süresi panelde raporlanır.",
     'options': [
         o('none', 'SLA yok — yalnız sıra ve yaş takibi', "Süre hedefi tanımlanmaz, talepler açılış sırasıyla ve bekleme süresiyle izlenir.", "Çok düşük talep hacmi, tek kişilik destek.", "Kuyrukta talepler \"3 gündür açık\" bilgisiyle eskiden yeniye sıralanır.",
           "SLA sayaçları kurulmaz; açık kalma süresi raporlanır ve tanımlı günü aşan talepler listede vurgulanır."),
         o('single', 'Tek SLA (bütün talepler için)', "Bütün talepler için tek ilk yanıt ve çözüm hedefi.", "Küçük ekip, benzer talep türleri.", "Bütün taleplerde ilk yanıt 1 iş günü, çözüm 3 iş günü.",
           "Tek SLA politikası tanımlanır; hedef süreler panelden değiştirilebilir."),
         o('priority', 'Önceliğe göre SLA (önerilen)', "Her öncelik seviyesinin ayrı ilk yanıt ve çözüm hedefi vardır.", "Kritik sorunların hızlı ele alınması gereken çoğu proje.", "Kritik: 1 saat / 8 saat · Yüksek: 4 saat / 2 gün · Normal: 1 gün / 5 gün.",
           "Öncelik başına ilk yanıt ve çözüm hedefleri tanımlanır; öncelik değişirse sayaç yeni hedefe göre yeniden hesaplanır ve değişiklik kaydedilir."),
         o('contract', 'Müşteri tipi, sözleşme ya da abonelik planına göre', "Kurumsal sözleşmeli ya da premium planlı müşterilere farklı hedefler.", "Destek paketi satılan ya da kurumsal SLA taahhüdü olan projeler.", "Kurumsal plan müşterisinin kritik talebi 30 dakikada, standart planın 4 saatte yanıtlanır.",
           "SLA politikası müşteri kaydındaki sözleşme / plan alanından seçilir (öncelik ile birlikte); taahhüt edilen SLA'lar müşteri portalında görünür ve aylık uyum raporu üretilir."),
     ]},

    {'id': 'tk_assign', 'section': 'biz_ticket', 'type': 'select', 'label': 'Talep Atama Kuralı', 'en': 'Ticket Assignment', 'agents': [SUP_SR, APP], 'showIf': G_TK,
     'explanation': "Yeni talebin hangi ekip ya da destek uzmanına gideceğini belirler.",
     'scenario': "Birden çok destek uzmanı ya da ekibi (birinci seviye, teknik, muhasebe) varsa.",
     'example': "\"Ödeme › İade\" talebi kurala göre Finans Destek ekibine gider; ekip içinde en az açık talebi olan uzmana atanır.",
     'rule': "Talep atama kuralı: {label}. Atama ve yeniden atama gerekçesiyle kaydedilir; sorumlu, takip eden ve bilgilendirilecek kullanıcılar ayrı alanlardır; destek uzmanı yalnız kendisine ya da ekibine atanmış talepleri görür, hassas kategorideki talepler ek yetki ister.",
     'options': [
         o('pool', 'Ortak havuz, uzman üstlenir', "Talepler ekip kuyruğuna düşer, uzman sıradakini üstlenir.", "Küçük ve esnek destek ekibi.", "Kuyrukta \"Sıradakini al\" düğmesi en eski / en öncelikli talebi verir.",
           "Üstlenme işlemi atomiktir (aynı talep iki kişiye atanamaz); üstlenilmeden bekleyen talepler için ekip liderine uyarı gider."),
         o('round_robin', 'Sırayla / en az yüke göre dağıtım', "Talepler çevrimiçi uzmanlara sırayla ya da açık talep sayısına göre dağıtılır.", "Orta-büyük ekip, benzer yetkinlikler.", "Vardiyada olan dört uzmana talepler en az açık talebi olandan başlayarak dağıtılır.",
           "Dağıtım uzmanın vardiya / izin durumuna bakar; kapasite sınırı aşılınca talep kuyrukta kalır."),
         o('rules', 'Kategori, dil, ürün ve müşteri tipine göre kural (önerilen)', "Kurallarla doğru ekibe yönlendirme, ekip içinde dağıtım.", "Uzmanlık gerektiren farklı konular ve ekipler varsa.", "İngilizce talepler uluslararası ekibe, \"LMS erişim\" talepleri eğitim destek ekibine.",
           "Kurallar öncelik sırasıyla değerlendirilir; eşleşmeyen talep varsayılan ekibe düşer; kural değişiklikleri sürümlenir."),
         o('account_owner', 'Müşterinin sorumlu yöneticisine', "Kurumsal müşterinin talepleri atanmış müşteri yöneticisine ya da müşteri başarı uzmanına gider.", "Az sayıda büyük kurumsal müşteriye birebir hizmet veriliyorsa.", "ABC Holding'in talepleri her zaman atanmış müşteri başarı yöneticisine düşer.",
           "Sorumlu yönetici CRM'deki müşteri kaydından okunur; yönetici izindeyse vekil ya da ekip kuyruğu devreye girer."),
     ]},

    {'id': 'tk_selfservice', 'section': 'biz_ticket', 'type': 'multiselect', 'label': 'Bilgi Bankası, Portal ve Bağlantılar', 'en': 'Knowledge Base, Portal & Integrations', 'agents': [KB, APP], 'showIf': G_TK,
     'explanation': "Talepleri azaltan self-servis yapının (yardım makaleleri, öneri) ve talep modülünün müşteri portalı, CRM ve anket modülüyle bağlantılarını belirler.",
     'scenario': "Aynı sorular tekrar tekrar geliyor, müşteri taleplerini takip etmek için e-posta kutusunu karıştırıyor ya da satış ekibi müşterinin destek geçmişini görmüyorsa.",
     'example': "Talep formunda \"Faturamı nasıl indiririm?\" yazılınca üç yardım makalesi önerilir; müşteri makaleyi açıp \"Sorunum çözüldü\" derse talep açılmaz ve bu \"önlenen talep\" olarak sayılır.",
     'rule': "Destek self-servis ve bağlantıları: {labels}.",
     'recommend': {'field': 'modules_extra', 'map': {'portal': ['portal'], 'crm': ['crm'], 'survey': ['csat']}},
     'options': [
         o('kb', 'Bilgi bankası / yardım merkezi (önerilen)', "Kategorili, aranabilir yardım makaleleri ve sık sorulan sorular.", "Tekrarlayan sorular varsa.", "/yardim altında \"Hesap ve Giriş\", \"Ödeme ve Fatura\" kategorileri; her makalenin altında \"Faydalı oldu mu?\".",
           "Makaleler CMS'te taslak / yayında / arşiv durumlarıyla, son güncelleme tarihi ve sorumlusuyla yönetilir; makale HTML'i güvenli biçimde işlenir; görüntülenme ve faydalı oyu raporlanır."),
         o('deflection', 'Talep açarken makale önerisi', "Konu yazılırken ilgili makalelerin önerilmesi.", "Bilgi bankası varsa ve talep hacmi yüksekse.", "Konu alanına \"iade\" yazılınca \"İade süreci nasıl işler?\" makalesi önerilir.",
           "Öneri arama tabanlıdır; önerinin talebi önleyip önlemediği ölçülür, öneri müşterinin talep açmasını engellemez."),
         o('portal', 'Müşteri portalında takip ve yanıt', "Müşterinin taleplerini portalda görmesi, yanıtlaması, dosya eklemesi.", "Müşteri / üye portalı varsa.", "Portalda talep listesi, durum rozetleri ve yazışma geçmişi.",
           "Portal yalnız müşteriye görünen yanıtları gösterir; kurumsal hesap yöneticisi yetkisi varsa şirketin bütün taleplerini görür."),
         o('crm', 'CRM müşteri kartına bağlantı', "Talep olaylarının CRM zaman çizelgesinde, açık taleplerin müşteri kartında görünmesi.", "CRM modülü varsa.", "Satış temsilcisi müşteri kartında \"2 açık destek talebi · SLA ihlali 1\" uyarısını görür.",
           "Talep açma, durum değişikliği, çözüm ve kapanış CRM'e olay olarak yazılır; satış kullanıcıları talep içeriğinin yalnız özetini görür."),
         o('csat', 'Çözüm sonrası memnuniyet anketi', "Talep kapanınca CSAT anketinin gönderilmesi; düşük puanda talebin yeniden incelenmesi.", "Anket / NPS modülü varsa ya da destek kalitesi ölçülecekse.", "Kapanış e-postasında 1–5 yıldız; 1–2 yıldız veren müşterinin talebi ekip liderinin inceleme listesine düşer.",
           "Memnuniyet anketi Anket, NPS ve Geri Bildirim modülü üzerinden gönderilir, sonuç talep kaydına yazılır; aynı talep için tek anket gönderilir."),
         o('company', 'Kurumsal hesap görünümü', "Kurumsal müşteride yetkili kullanıcının şirketinin bütün taleplerini görmesi.", "B2B destek veriliyorsa.", "ABC Holding BT yöneticisi portalda şirketindeki 14 kullanıcının taleplerini görür.",
           "Kurumsal görünüm yalnız şirket yöneticisi rolüne açıktır; kapsam sunucuda şirket kimliğiyle sınırlanır."),
     ]},
]

# ---------------------------------------------------------------- B3 Anket, NPS ve Geri Bildirim
S_SV = {
    'id': 'biz_survey', 'group': 'İş Modülleri', 'icon': '★',
    'name': 'Anket, NPS ve Geri Bildirim', 'en': 'Surveys, NPS & Customer Feedback',
    'desc': "Anket türlerini (NPS, CSAT, CES, ürün / içerik ve etkinlik değerlendirmesi), dağıtım kanallarını, tetikleyicileri ve sıklık sınırını, düşük puanda aksiyonu ve yanıtların anonimliğini karara bağlar",
    'guide': {
        'purpose': "Anket modülü müşteri deneyimini sayıyla ölçer ve ölçümü aksiyona bağlar: NPS (tavsiye etme olasılığı, 0–10) sadakati, CSAT (memnuniyet) belirli bir etkileşimi, CES (müşteri efor skoru) işlemin ne kadar kolay olduğunu ölçer. Anketler destek kapanışı, sipariş, rezervasyon ya da eğitim tamamlama gibi olaylarla tetiklenir; yanıtlar müşteri kaydına yazılır, düşük puan destek talebine ya da müşteri yöneticisine görev olarak döner. Bu bölüm hangi anketlerin kullanılacağını, nasıl dağıtılacağını, ne sıklıkla gönderileceğini, düşük puanın nasıl ele alınacağını ve yanıtların kimlikli mi anonim mi tutulacağını belirler.",
        'criteria': [
            "NPS standart soruyla (0–10) sorulur; 9–10 tavsiye eden (promoter), 7–8 pasif, 0–6 kötüleyen (detractor) sayılır ve NPS = tavsiye eden % − kötüleyen % olarak sistemde hesaplanır.",
            "Her anketin tetikleyicisi, hedef kitlesi, kanalı ve sıklık sınırı tanımlıdır; aynı kişiye kısa aralıkla birden çok anket gitmez.",
            "Düşük puan bir aksiyona bağlanır (takip görevi, destek talebi) ve müşteriye geri dönüldüğü kaydedilir; ölçüp ses çıkarmamak güveni azaltır.",
            "Anket bağlantıları tahmin edilemez belirteçle (token) korunur, süreli ve tek yanıtlıdır; yanıt başka bir kişinin adına verilemez.",
            "Anonim olduğu söylenen ankette kimlik, IP adresi ya da kişiye özel bağlantı yanıtla eşleştirilmez; küçük gruplarda sonuçlar kimliği ele vermeyecek eşikle gösterilir.",
            "Anket davetleri kampanya içeriği taşımaz; davetin ticari elektronik ileti sayılıp sayılmayacağı ve izin gereksinimi hukuk birimince teyit edilir.",
        ],
        'pitfalls': [
            "Her işlemden sonra anket göndermek: anket yorgunluğu yanıt oranını düşürür ve marka algısını bozar.",
            "Anketi uzun tutmak: NPS / CSAT anketinde tek puan sorusu ve bir açık uçlu soru çoğu durumda yeterlidir.",
            "Puanı yüksek çıkarmak için yalnız memnun müşterilere anket göndermek ya da temsilcinin yanıtı yönlendirmesine izin vermek: ölçüm anlamını yitirir.",
            "\"Anonim\" anketin bağlantısına müşteri kimliği koymak: yanıt kişiye geri bağlanabilir, verilen söz ve KVKK ilkeleri çiğnenir.",
            "Açık uçlu yorumları ham hâlde geniş bir ekiple paylaşmak: yorumlarda telefon, sağlık bilgisi gibi kişisel veriler bulunabilir.",
            "Sonuçları yalnız ortalama olarak raporlamak: dağılım ve trend görülmeden iyileşme ya da bozulma fark edilmez.",
        ],
        'resources': [
            {'title': "Bain & Company — Measuring Your Net Promoter Score", 'url': 'https://www.netpromotersystem.com/about/measuring-your-net-promoter-score/', 'note': "NPS sorusu, tavsiye eden / pasif / kötüleyen sınıfları ve skorun hesaplanması (NPS'in geliştiricisi Bain'in resmî sayfası)."},
            {'title': "Qualtrics — Customer Effort Score (CES)", 'url': 'https://www.qualtrics.com/articles/customer-experience/customer-effort-score/', 'note': "Müşteri efor skorunun soru biçimi, ölçeği ve ne zaman kullanılacağı."},
            {'title': "KVKK — Aydınlatma Yükümlülüğü", 'url': 'https://www.kvkk.gov.tr/Icerik/2033/Aydinlatma-Yukumlulugu-', 'note': "Kimlikli anket yanıtlarını toplarken yapılacak bilgilendirme."},
            {'title': "KVKK — Kişisel Verilerin Silinmesi, Yok Edilmesi veya Anonim Hale Getirilmesi", 'url': 'https://www.kvkk.gov.tr/Icerik/2038/kisisel-verilerin-silinmesi-yok-edilmesi-veya-anonim-hale-getirilmesi', 'note': "Anket verisinin anonimleştirilmesi ve saklama süresi sonunda imhası."},
            {'title': "6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6563&MevzuatTur=1&MevzuatTertip=5', 'note': "Anket davetinin ticari elektronik ileti niteliği taşıyıp taşımadığının değerlendirilmesi."},
            {'title': "İleti Yönetim Sistemi (İYS)", 'url': 'https://iys.org.tr/', 'note': "Ticari ileti izinlerinin sorgulanması; davetler ticari içerik taşıyorsa gönderim öncesi kontrol."},
            {'title': "W3C WAI — Forms Tutorial", 'url': 'https://www.w3.org/WAI/tutorials/forms/', 'note': "Puanlama ölçekleri ve açık uçlu soruların erişilebilir form olarak kurulması."},
        ],
    },
}

F_SV = [
    {'id': 'sv_types', 'section': 'biz_survey', 'type': 'multiselect', 'label': 'Anket Türleri', 'en': 'Survey Types', 'agents': [VOC, APP], 'showIf': G_SV,
     'explanation': "Projede hangi ölçüm ve geri bildirim türlerinin kullanılacağını belirler; her tür hazır şablonla gelir, panelden çok dilli düzenlenebilir.",
     'scenario': "Genel sadakat (NPS), tekil etkileşim memnuniyeti (CSAT), işlem kolaylığı (CES) ya da içerik / etkinlik geri bildirimi ölçülmek isteniyorsa.",
     'example': "Panelde \"Anketler\" listesi: \"Çeyreklik NPS (yayında) · Destek sonrası CSAT (yayında) · Eğitim değerlendirme (taslak)\"; her anketin yanıt oranı ve skoru yanında.",
     'rule': "Kullanılacak anket türleri: {labels}. Anketler taslak / yayında / pasif / arşivlendi durumlarıyla, sürümlenerek yönetilir; yayındaki anketin soruları değiştirilince yeni sürüm açılır ve sonuçlar sürümle raporlanır; soru metinleri çok dilli tutulur.",
     'recommend': {'field': 'modules_extra', 'map': {'ticket': ['csat'], 'lms': ['event'], 'events': ['event'], 'subscription': ['nps', 'exit'], 'ecommerce': ['csat'], 'booking': ['csat'], 'consulting': ['csat']}},
     'options': [
         o('nps', 'NPS — tavsiye etme olasılığı (önerilen)', "\"Bizi bir arkadaşınıza tavsiye etme olasılığınız nedir?\" sorusu (0–10) ve isteğe bağlı \"Neden?\" sorusu.", "Genel müşteri sadakatini dönemsel izlemek için.", "Panoda \"NPS +42 · Tavsiye eden %58 · Pasif %26 · Kötüleyen %16\" ve aylık trend grafiği.",
           "NPS 0–10 ölçeğiyle sorulur; 9–10 tavsiye eden, 7–8 pasif, 0–6 kötüleyen olarak sınıflanır; skor sunucuda hesaplanır ve segment, ürün, dönem bazında raporlanır."),
         o('csat', 'CSAT — etkileşim memnuniyeti', "Belirli bir etkileşim sonrası 1–5 memnuniyet sorusu.", "Destek, teslimat, rezervasyon ya da danışmanlık sonrası.", "\"Destek deneyiminizden ne kadar memnun kaldınız? ★★★★☆\"",
           "CSAT ilgili kayda (talep, sipariş, rezervasyon) bağlanır; skor 4–5 verenlerin oranı olarak hesaplanır."),
         o('ces', 'CES — müşteri efor skoru', "\"Bu işlemi tamamlamak ne kadar kolaydı?\" sorusu (1–7 ya da 1–5).", "Ödeme, iade, başvuru gibi süreçlerin zorluğunu ölçmek için.", "İade işlemi bitince \"İadenizi oluşturmak ne kadar kolaydı?\" sorusu.",
           "CES işlem tamamlandıktan sonra tek soru olarak gösterilir; yüksek efor yanıtları süreç sahibine raporlanır."),
         o('product', 'Ürün / içerik geri bildirimi', "Sayfa, makale ya da özellik için \"Faydalı oldu mu?\" ve öneri soruları.", "Bilgi bankası, blog, dokümantasyon ya da yazılım ürünü varsa.", "Makale altında \"Bu sayfa işinize yaradı mı? Evet / Hayır\" ve \"Ne eksikti?\" kutusu.",
           "Sayfa içi geri bildirim oturum açmadan da alınabilir; bot korumalıdır, aynı tarayıcıdan tekrar oy sayılmaz, açık uçlu metin kişisel veri taramasından geçer."),
         o('event', 'Etkinlik ve eğitim değerlendirmesi', "Etkinlik, webinar ya da eğitim sonrası çok sorulu değerlendirme.", "Etkinlik ya da LMS modülü varsa.", "Eğitim tamamlanınca eğitmen, içerik ve platform için 1–5 puan ile öneri sorusu.",
           "Değerlendirme sonuçları etkinlik / eğitim ve eğitmen kaydına bağlanır; eğitmen yalnız toplu sonuçları görür."),
         o('general', 'Genel öneri ve şikâyet formu', "Herkese açık öneri, şikâyet ve teşekkür formu.", "Kurumun açık bir geri bildirim kanalı olması isteniyorsa.", "Alt bilgide \"Görüş ve önerileriniz\" bağlantısı.",
           "Şikâyet niteliğindeki geri bildirimler destek talebine dönüştürülebilir; form bot korumalıdır."),
         o('exit', 'İptal / ayrılma anketi', "Abonelik iptali ya da üyelik silme sırasında isteğe bağlı neden sorusu.", "Abonelik veya üyelik modeli varsa.", "İptal ekranında \"Neden ayrılıyorsunuz? (isteğe bağlı)\" seçenekleri.",
           "Ayrılma anketi isteğe bağlıdır ve iptali geciktirmez ya da zorlaştırmaz; yanıtlar churn nedeni raporuna yazılır."),
     ]},

    {'id': 'sv_channels', 'section': 'biz_survey', 'type': 'multiselect', 'label': 'Anket Dağıtım Kanalları', 'en': 'Survey Distribution Channels', 'agents': [VOC, APP], 'showIf': G_SV,
     'explanation': "Anketlerin müşteriye hangi kanallardan ulaştırılacağını belirler.",
     'scenario': "Yanıt oranını yükseltmek için müşterinin en çok kullandığı kanal seçilir; işlem sonrası anketlerde işlemin yapıldığı kanal genellikle en iyisidir.",
     'example': "Destek talebi kapanınca e-posta ile, rezervasyon sonrası SMS bağlantısıyla, portal kullanıcısına ise panelde açılan küçük anket kutusuyla sorulur.",
     'rule': "Anket dağıtım kanalları: {labels}. Anket bağlantıları tahmin edilemez, süreli ve tek yanıtlı belirteçle (token) üretilir; belirteç URL'de kişisel veri taşımaz ve analitik araçlarına gönderilmez; davetlerde kampanya / tanıtım içeriği bulunmaz, davetin ticari elektronik ileti sayılıp sayılmadığı ve İYS onayı gerekip gerekmediği hukuk birimince teyit edilir; gönderimler Bildirim Merkezi ya da işlemsel e-posta / SMS altyapısı üzerinden yapılır.",
     'options': [
         o('email', 'E-posta (önerilen)', "Anket sorusunun e-postaya gömülü ilk adımı ve bağlantı.", "Çoğu işlem sonrası anket.", "E-postada 0–10 düğmeleri; tıklanan puan kaydedilir, açılan sayfada \"Neden?\" sorulur.",
           "E-postadaki puan düğmeleri yalnız ön seçim kaydeder; yanıt, açılan sayfada onaylanınca kesinleşir (e-posta tarayıcılarının bağlantıyı önceden açması yanıt saymaz)."),
         o('in_app', 'Site / panel içi anket kutusu', "Giriş yapmış kullanıcıya site ya da panel içinde gösterilen küçük anket.", "Yazılım ürünü, müşteri portalı ya da üyelik sitesi varsa.", "Panelin sağ altında \"Bu ay deneyiminizi puanlar mısınız?\" kutusu; kapatılınca 30 gün gösterilmez.",
           "Kutu odak tuzağı oluşturmaz, klavyeyle kapatılabilir; kapatma tercihi kaydedilir, sıklık sınırına uyulur."),
         o('portal', 'Müşteri portalında anketlerim', "Kullanıcıya atanmış anketlerin portalda listelenmesi.", "Müşteri portalı varsa.", "Portalda \"Bekleyen anketler (1)\" rozeti.",
           "Portal anketleri oturumdaki kullanıcıya bağlıdır; yanıtlanan anket tekrar yanıtlanamaz."),
         o('sms', 'SMS bağlantısı', "Kısa mesajla gönderilen anket bağlantısı.", "Telefonla iletişim kurulan ya da e-postası olmayan müşteriler.", "\"Randevunuzu 1 dakikada puanlayın: kisa.link/abc\"",
           "SMS daveti kısa ve kampanya içeriksiz tutulur; gönderim saatleri sınırlandırılır, ret talebi işlenir."),
         o('whatsapp', 'WhatsApp', "WhatsApp onaylı şablonuyla anket daveti.", "Müşteri iletişimi WhatsApp üzerinden yürüyorsa.", "Rezervasyon sonrası WhatsApp mesajında \"Deneyiminizi puanlayın\" düğmesi.",
           "WhatsApp daveti onaylı şablonla gönderilir; şablon kategorisi ve izin durumu kontrol edilir."),
         o('qr', 'Bağlantı ve QR kod', "Fiziksel mekânda, etkinlikte ya da baskı materyalinde paylaşılan genel anket bağlantısı.", "Mağaza, klinik, etkinlik alanı gibi yüz yüze temas noktaları.", "Etkinlik çıkışında QR kodlu \"Etkinliği değerlendirin\" afişi.",
           "Genel bağlantıyla gelen yanıtlar anonim kabul edilir; tekrar yanıt ve bot gönderimine karşı hız sınırı ve bot doğrulaması uygulanır."),
     ]},

    {'id': 'sv_triggers', 'section': 'biz_survey', 'type': 'multiselect', 'label': 'Tetikleyiciler ve Sıklık Sınırı', 'en': 'Survey Triggers & Frequency Cap', 'agents': [CXA, APP], 'showIf': G_SV,
     'explanation': "Anketlerin hangi olaylarla otomatik gönderileceğini belirler. Her tetikleyici ortak bir sıklık sınırına tabidir (anket yorgunluğunu önlemek için).",
     'scenario': "Ölçümün olaydan hemen sonra ve doğru kişiye yapılması, aynı müşteriye üst üste anket gitmemesi isteniyorsa.",
     'example': "Müşteri pazartesi destek anketi aldıysa çarşamba tamamladığı siparişin anketi gönderilmez; panelde \"Sıklık sınırı nedeniyle atlandı: 37\" sayacı görünür.",
     'rule': "Anket tetikleyicileri: {labels}. Bütün tetikleyiciler ortak bir kişi başı sıklık sınırına tabidir (panelden ayarlanır; varsayılan aynı kişiye 30 günde en çok bir anket) ve en çok bir hatırlatma gönderilir; tetikleyiciler kuyrukla, olay kimliğine göre tekilleştirilerek çalışır; ret vermiş ya da iletişim tercihini kapatmış kişiye anket gönderilmez.",
     'recommend': {'field': 'modules_extra', 'map': {'ticket': ['ticket_closed'], 'ecommerce': ['purchase'], 'booking': ['service_done'], 'consulting': ['service_done'], 'lms': ['course_done'], 'events': ['course_done'], 'subscription': ['periodic', 'cancel']}},
     'options': [
         o('ticket_closed', 'Destek talebi kapandığında', "Talep \"Çözüldü / Kapandı\" olunca CSAT anketi.", "Destek talebi modülü varsa.", "Talep kapanışından 1 saat sonra CSAT e-postası.",
           "Anket talep kapanışından sonra kısa gecikmeyle gönderilir; talep yeniden açılırsa bekleyen anket iptal edilir."),
         o('purchase', 'Sipariş teslim edildiğinde', "Sipariş teslim / tamamlandığında alışveriş deneyimi anketi.", "E-ticaret modülü varsa.", "Kargo teslim edildikten 2 gün sonra \"Siparişinizi nasıl buldunuz?\".",
           "Anket teslim olayından sonra gönderilir; iade süreci açık siparişte ertelenir."),
         o('service_done', 'Rezervasyon ya da danışmanlık tamamlandığında', "Randevu / görüşme tamamlanınca deneyim anketi.", "Rezervasyon ya da online danışmanlık modülü varsa.", "Görüşme bitiminden 30 dakika sonra danışman değerlendirme anketi.",
           "Yalnız \"Tamamlandı\" durumundaki rezervasyonlar tetikler; no-show ve iptal anket üretmez."),
         o('course_done', 'Eğitim ya da etkinlik bittiğinde', "Eğitim tamamlama, sertifika ya da etkinlik katılımı sonrası değerlendirme.", "LMS ya da etkinlik modülü varsa.", "Kurs tamamlanınca sertifika ekranında değerlendirme formu.",
           "Değerlendirme katılım / tamamlama kaydıyla eşlenir; katılmayan kişiye gönderilmez."),
         o('periodic', 'Dönemsel NPS', "Belirli aralıkla (ör. üç ayda bir) müşteri tabanına ya da segmente NPS anketi.", "İlişki düzeyinde sadakat izlenecekse.", "Her çeyreğin ilk haftası aktif müşterilerin rastgele %25'ine NPS gönderilir.",
           "Dönemsel anket örneklemle ve kişi başı sıklık sınırına uyarak gönderilir; yeni müşteriye ilk 30 gün gönderilmez."),
         o('cancel', 'Abonelik iptali ya da plan değişikliği', "İptal, plan düşürme ya da yenilememe sonrası geri bildirim.", "Abonelik modülü varsa.", "Plan düşüren müşteriye \"Neden daha küçük bir plana geçtiniz?\" sorusu.",
           "İptal sonrası anket iptal işleminden ayrıdır ve isteğe bağlıdır; iptal onayı ankete bağlanmaz."),
         o('inactive', 'Uzun süredir işlem yapmayan müşteri', "Belirli süre etkileşimi olmayan müşteriye geri bildirim / churn riski anketi.", "Müşteri kaybını önleme çalışması yapılıyorsa.", "90 gündür giriş yapmayan üyeye \"Size nasıl daha iyi hizmet verebiliriz?\" anketi.",
           "Etkinsizlik eşiği panelden tanımlanır; pazarlama iletisi izni olmayan kişiye yalnız hizmet niteliğindeki anket gönderilir, nitelik hukuk birimince teyit edilir."),
     ]},

    {'id': 'sv_actions', 'section': 'biz_survey', 'type': 'multiselect', 'label': 'Düşük Puan ve Geri Bildirim Aksiyonları', 'en': 'Closed-Loop Feedback Actions', 'agents': [RECOVER, VOC], 'showIf': G_SV,
     'explanation': "Anket yanıtının hangi aksiyonu başlatacağını belirler: düşük puanda takip, yüksek puanda yorum / referans isteği, sonuçların müşteri kaydına yazılması.",
     'scenario': "Ölçümün yalnız raporda kalmayıp memnun olmayan müşteriye hızla dönülmesi (döngüyü kapatma) isteniyorsa.",
     'example': "NPS'te 3 veren müşteri için müşteri başarı yöneticisine 24 saat süreli \"Geri dön\" görevi açılır; yönetici aradıktan sonra sonucu \"Döngü kapatıldı\" notuyla girer.",
     'rule': "Anket yanıtı aksiyonları: {labels}. Aksiyon eşikleri (ör. NPS 0–6, CSAT 1–2) panelden yönetilir; açılan her aksiyonun sorumlusu, son tarihi ve sonucu kaydedilir; aksiyonlar kuyrukla ve yanıt kimliğine göre tekilleştirilerek açılır.",
     'recommend': {'field': 'modules_extra', 'map': {'ticket': ['ticket'], 'crm': ['crm_task', 'crm_profile']}},
     'options': [
         o('ticket', 'Düşük puanda destek talebi', "Kötüleyen ya da düşük CSAT yanıtı için destek talebi açılması ya da mevcut talebin yeniden açılması.", "Destek talebi modülü varsa.", "CSAT 1 veren müşterinin kapanan talebi \"Yeniden inceleme\" etiketiyle yeniden açılır.",
           "Düşük puan aynı konudaki kapalı talebi tanımlı süre içinde yeniden açar, süre geçmişse yeni talep açar ve eskisine bağlar."),
         o('crm_task', 'Müşteri yöneticisine takip görevi (önerilen)', "Düşük puanda sorumlu satış / müşteri başarı kullanıcısına görev.", "Kurumsal müşteriler ya da yüksek değerli müşteri tabanı.", "Görev: \"NPS 4 — ABC Ltd. — 24 saat içinde arayın\".",
           "Görev müşteri kaydındaki sorumluya atanır, sorumlu yoksa ekip kuyruğuna düşer; görev kapatılırken sonuç notu zorunludur."),
         o('alert', 'Yönetici uyarısı ve günlük özet', "Düşük puan ve tekrar eden olumsuz yorumlar için yöneticiye bildirim.", "Hizmet kalitesinin yakından izlendiği ekipler.", "Destek müdürüne her sabah \"Dün 3 düşük CSAT, 2'si aynı kategoriden\" özeti.",
           "Uyarılar toplu özet olarak gönderilir; kişisel veri içeren yorumlar özetlerde kısaltılır."),
         o('promoter', 'Tavsiye edenden yorum / referans isteği', "9–10 veren müşteriden değerlendirme sitesinde yorum ya da referans izni istenmesi.", "Sosyal kanıt ve referans toplanmak isteniyorsa.", "NPS 10 veren müşteriye \"Görüşünüzü sitemizde paylaşabilir miyiz?\" sorusu.",
           "Yorumun sitede ad / logo ile yayınlanması yalnız ayrıca alınan açık izinle yapılır; izin kaydı ve geri alma yolu tutulur."),
         o('crm_profile', 'Skorların CRM müşteri kartına yazılması', "NPS, CSAT, CES ve memnuniyet segmentinin müşteri kartında görünmesi.", "CRM modülü varsa.", "Müşteri kartında \"Son NPS: 9 (Tavsiye eden) · CSAT ortalaması 4,6\".",
           "Skorlar CRM'e olay olarak yazılır; anonim anket yanıtları CRM'e aktarılmaz."),
         o('close_loop', 'Müşteriye geri dönüş kaydı', "Geri bildirime verilen yanıtın ve yapılan iyileştirmenin müşteriye bildirilmesi ve kaydedilmesi.", "Müşteri deneyimi programı yürütülüyorsa.", "\"Önerinizle fatura indirme adımını kısalttık\" bilgilendirmesi ve kayıtta \"Döngü kapatıldı\" durumu.",
           "Her aksiyonun durumu açık / müşteriye dönüldü / kapatıldı olarak izlenir; döngü kapatma oranı raporlanır."),
     ]},

    {'id': 'sv_privacy', 'section': 'biz_survey', 'type': 'select', 'label': 'Yanıtların Kimliği ve KVKK', 'en': 'Response Identity & Privacy', 'agents': [KVKK, CXA], 'showIf': G_SV,
     'explanation': "Anket yanıtlarının kişiyle ilişkilendirilip ilişkilendirilmeyeceğini ve bu verinin nasıl korunacağını belirler.",
     'scenario': "Takip aksiyonu için kimlik gerekiyorsa kimlikli; çalışan ya da hassas konulu anketlerde dürüst yanıt için anonim yanıt tercih edilir.",
     'example': "Anket girişinde \"Yanıtlarınız hesabınızla ilişkilendirilecek ve size geri dönmek için kullanılacaktır — Aydınlatma metni\" notu; anonim ankette ise \"Bu anket anonimdir, yanıtınız kimliğinizle eşleştirilmez\".",
     'rule': "Anket yanıtlarının kimliği: {label}. Açık uçlu yanıtlar kart numarası, T.C. kimlik numarası ve telefon kalıpları için maskelenir; anket yanıtlarına yalnız yetkili roller erişir ve yanıtlar uygulama loglarına yazılmaz; anket verisi için saklama süresi tanımlanır, süre sonunda silinir ya da anonimleştirilir; dışa aktarımda kişisel veri sütunları yetkiye göre gizlenir.",
     'options': [
         o('identified', 'Kimlikli yanıt (aksiyon için)', "Yanıt müşteri kaydına bağlıdır; düşük puanda kişiye dönülebilir.", "İşlem sonrası CSAT, kurumsal müşteri NPS'i.", "Yanıt müşteri kartında görünür, sorumlu kişi arayabilir.",
           "Ankete başlamadan aydınlatma bilgisi gösterilir; yanıt yalnız hizmet iyileştirme ve takip amacıyla işlenir."),
         o('pseudonymous', 'Takma adlı (analiz anonim, aksiyon için kimlik yalnız yetkiliye) (önerilen)', "Raporlar ve yorum listeleri kimliksiz gösterilir; kimlik yalnız takip aksiyonu için yetkili rolde açılır.", "Hem dürüst yanıt hem de takip isteyen çoğu müşteri anketi.", "Analist yorumları kimliksiz görür; müşteri başarı yöneticisi yalnız kendisine düşen takip görevinde müşteriyi görür.",
           "Yanıt tablosunda kimlik yerine takma ad anahtarı tutulur, eşleme ayrı ve erişimi kısıtlı tabloda saklanır; kimliğin açılması denetim kaydına yazılır."),
         o('anonymous', 'Anonim yanıt', "Yanıt hiçbir biçimde kişiyle eşleştirilmez; IP ya da kişiye özel bağlantı yanıtla saklanmaz.", "Çalışan anketi, hassas konular, genel QR anketleri.", "Sonuçlar yalnız toplu ve en az 5 yanıtlı gruplarda gösterilir.",
           "Anonim ankette kişiye özel belirteç yanıt kaydına yazılmaz (yalnız tekrar yanıtı önlemek için ayrı, tek yönlü işaret tutulur); küçük gruplarda sonuçlar gizlenir; anonim yanıtlar aksiyon üretmez."),
         o('choice', 'Katılımcı seçer', "Ankette \"Size geri dönmemizi ister misiniz?\" seçeneği; seçmeyen için yanıt anonim tutulur.", "Geri dönüşü isteğe bırakmak isteyen markalar.", "Anket sonunda \"Evet, benimle iletişime geçin\" kutusu (önceden işaretli değil).",
           "İletişim izni kutusu önceden işaretli gelmez; işaretlenmezse yanıt anonim akışa yazılır, işaretlenirse kimlikli akışa."),
     ]},
]

# ---------------------------------------------------------------- B4 Abonelik, Paket ve Üyelik Planları
S_SUB = {
    'id': 'biz_subscription', 'group': 'İş Modülleri', 'icon': '⟳',
    'name': 'Abonelik, Paket ve Üyelik Planları', 'en': 'Subscriptions, Plans & Recurring Billing',
    'desc': "Plan modelini, deneme süresini, tekrarlayan tahsilat ve başarısız ödeme takibini, faturalamayı, plan değişikliği / iptal / askıya almayı, abonelik sözleşmesi ve yenileme kurallarını ve ödeme sağlayıcısını karara bağlar",
    'guide': {
        'purpose': "Abonelik modülü düzenli aralıklarla ücretlendirilen planların (aylık / yıllık abonelik, kademeli paket, kullanıcı başına, kullanım ya da kredi bazlı haklar) satışını ve yaşam döngüsünü yönetir: deneme, aktif, ödeme bekliyor, askıya alındı, iptal edildi, süresi doldu. Tekrarlayan tahsilat ödeme sağlayıcısının kart saklama (tokenizasyon) ve abonelik altyapısıyla yapılır; başarısız ödemede yeniden deneme ve bildirim akışı (dunning) çalışır; her tahsilattan sonra fatura (e-Fatura / e-Arşiv) üretilir. Tüketiciye satışta 6502 sayılı Kanun m. 52 ve Abonelik Sözleşmeleri Yönetmeliği uygulanır: belirli süreli abonelik kendiliğinden aynı süre kadar uzatılamaz, iptal yöntemi kayıt yönteminden zor olamaz, fesih talebi süresinde yerine getirilip kalan ücret iade edilir. Bu bölüm plan modelini, denemeyi, tahsilatı, değişiklik ve iptal kurallarını, yasal yükümlülükleri ve ödeme sağlayıcısını belirler.",
        'criteria': [
            "Tutar, plan, indirim ve dönem hesabı yalnız sunucuda yapılır; istemciden gelen fiyat ya da plan bilgisine güvenilmez.",
            "Kart bilgisi uygulama sunucusunda tutulmaz; ödeme sağlayıcısının saklı kart belirteci (token) kullanılır ve PCI DSS kapsamı en aza indirilir.",
            "Her tahsilat denemesi idempotency anahtarıyla bir kez yapılır; ödeme sağlayıcısından gelen bildirimler (webhook) imza doğrulamasıyla ve tekrarlara dayanıklı işlenir.",
            "Abonelik durum makinesi (deneme, aktif, ödeme bekliyor, askıda, iptal, süresi doldu) tanımlıdır ve hak erişimi yalnız bu duruma göre verilir.",
            "Tüketici aboneliği iptal edebilmek için kayıt olduğu yöntemden daha zor bir yola zorlanmaz; iptal paneldeki tek bir akışla yapılabilir ve onayı kalıcı veri saklayıcısıyla bildirilir.",
            "Plan ve fiyat değişiklikleri sürümlenir; mevcut abonelere uygulanacak değişiklik önceden bildirilir ve kayıtlıdır.",
        ],
        'pitfalls': [
            "Belirli süreli (ör. 12 aylık) aboneliği tüketicinin onayı olmadan aynı süre için kendiliğinden uzatmak: 6502 m. 52/3'e aykırıdır ve onaysız dönemin bedeli talep edilemez (Abonelik Sözleşmeleri Yönetmeliği m. 13/2).",
            "İptali yalnız telefonla ya da çok adımlı ikna ekranlarıyla mümkün kılmak: iptal yöntemi abonelik başlatma yönteminden ağır olamaz.",
            "Başarısız ödemede erişimi anında kesmek ya da sınırsız yeniden denemek: müşteri kaybı ve banka tarafında şüpheli işlem riski doğar; tanımlı bir yeniden deneme takvimi ve ek süre gerekir.",
            "Webhook'u imza doğrulamadan işlemek: sahte \"ödeme başarılı\" bildirimiyle ücretsiz erişim açılabilir.",
            "Plan yükseltmede fark hesabını istemcide yapmak ya da oranlamayı (proration) belgelememek: fatura ile tahsil edilen tutar tutmaz.",
            "Kullanım haklarını (kredi, seans) yarış durumuna açık biçimde düşmek: aynı anda iki istekle hak iki kez kullanılır.",
        ],
        'resources': [
            {'title': "6502 sayılı Tüketicinin Korunması Hakkında Kanun", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=6502&MevzuatTur=1&MevzuatTertip=5', 'note': "m. 48 mesafeli sözleşme ve cayma hakkı, m. 52 abonelik sözleşmeleri: kendiliğinden uzama yasağı, fesih hakkı, iptal yöntemi ve iade."},
            {'title': "Abonelik Sözleşmeleri Yönetmeliği", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20480&MevzuatTur=7&MevzuatTertip=5', 'note': "Sözleşmenin zorunlu içeriği (m. 6), fesih bildirimi (m. 23), fesih talebinin en geç 7 günde yerine getirilmesi (m. 24) ve 15 günde iade (m. 25)."},
            {'title': "Mesafeli Sözleşmeler Yönetmeliği", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20237&MevzuatTur=7&MevzuatTertip=5', 'note': "Ön bilgilendirme, sözleşmenin onaylanması ve cayma hakkı istisnaları (m. 15)."},
            {'title': "GİB e-Belge — e-Fatura mevzuatı", 'url': 'https://ebelge.gib.gov.tr/efaturamevzuat.html', 'note': "Abonelik tahsilatı sonrası düzenlenecek e-Fatura / e-Arşiv Fatura uygulamasının resmî kaynağı."},
            {'title': "iyzico — Abonelik", 'url': 'https://docs.iyzico.com/urunler/abonelik', 'note': "iyzico'nun ödeme planı, deneme süresi ve kayıtlı kartla tekrarlayan tahsilat ürünü."},
            {'title': "Stripe — Subscriptions overview", 'url': 'https://docs.stripe.com/billing/subscriptions/overview', 'note': "Abonelik yaşam döngüsü, durumlar ve webhook olayları için referans model."},
            {'title': "Stripe — Prorations", 'url': 'https://docs.stripe.com/billing/subscriptions/prorations', 'note': "Plan yükseltme / düşürmede oranlı fark hesabının nasıl yapıldığı."},
            {'title': "Stripe — Smart Retries", 'url': 'https://docs.stripe.com/billing/revenue-recovery/smart-retries', 'note': "Başarısız tekrarlayan ödemelerde yeniden deneme ve gelir kurtarma yaklaşımı."},
            {'title': "PCI Security Standards Council", 'url': 'https://www.pcisecuritystandards.org/', 'note': "Kart verisi güvenliği standardı (PCI DSS); kart saklamayı sağlayıcıya bırakarak kapsamı daraltma."},
        ],
    },
}

F_SUB = [
    {'id': 'sub_model', 'section': 'biz_subscription', 'type': 'multiselect', 'label': 'Plan ve Hak Modeli', 'en': 'Plan & Entitlement Model', 'agents': [PKG, APP], 'showIf': G_SUB,
     'explanation': "Satılacak abonelik, paket ve üyelik planlarının yapısını ve planın verdiği hakların (özellik erişimi, kota, kredi, seans) nasıl ölçüleceğini belirler.",
     'scenario': "SaaS, ücretli üyelik, eğitim erişimi, danışmanlık seans paketi, bakım / destek paketi ya da düzenli teslimatlı ürün satılıyorsa.",
     'example': "Fiyatlandırma sayfası: \"Başlangıç 490 TL/ay (3 kullanıcı) · Profesyonel 1.290 TL/ay (10 kullanıcı, öncelikli destek) · Kurumsal — teklif alın\"; \"Yıllık ödemede %17 indirim\" anahtarı.",
     'rule': "Abonelik plan ve hak modeli: {labels}. Planlar taslak / yayında / pasif / arşivlendi durumlarıyla ve sürümlenerek yönetilir; mevcut aboneler abone oldukları plan sürümünde kalır; fiyat, para birimi, KDV oranı ve dönem plan sürümünde tutulur; planın verdiği haklar (özellik erişimi, kota, kredi, seans, kullanıcı sayısı) tek bir hak (entitlement) tablosundan sunucuda denetlenir, arayüzdeki gizleme yetki sayılmaz; hak düşümü atomik ve idempotenttir; kullanılan, kalan ve süresi dolan haklar ile kullanım geçmişi müşteri panelinde görünür.",
     'recommend': {'field': 'project_type', 'map': {'SaaS': ['recurring', 'tiered', 'per_seat'], 'LMS': ['access', 'recurring'], 'Community': ['access', 'recurring'], 'Booking': ['credits']}},
     'options': [
         o('recurring', 'Aylık / yıllık abonelik (önerilen)', "Sabit ücretli, dönemsel yenilenen abonelik; yıllık seçenekte indirim.", "Düzenli kullanılan hizmetlerin çoğu.", "\"Aylık 490 TL ya da yıllık 4.900 TL\" seçimi.",
           "Dönem başlangıcı, sonraki tahsilat tarihi ve dönem sonu abonelik kaydında tutulur; yıllık / aylık geçişi plan değişikliği kuralına tabidir."),
         o('tiered', 'Kademeli planlar', "Özellik ve limitleri artan Başlangıç / Profesyonel / Kurumsal gibi kademeler.", "Farklı büyüklükte müşterilere hitap eden ürünler.", "Plan karşılaştırma tablosunda özellik satırları ve \"En popüler\" etiketi.",
           "Kademelerin özellik ve limitleri hak tablosunda tanımlanır; karşılaştırma tablosu aynı kaynaktan üretilir."),
         o('per_seat', 'Kullanıcı (koltuk) başına', "Ücret ve hak kurumsal hesaptaki kullanıcı sayısına göre.", "Ekip olarak kullanılan B2B yazılım.", "\"10 kullanıcı × 129 TL\"; yönetici panelinde kullanıcı ekle / çıkar.",
           "Koltuk sayısı değişikliği oranlı fark hesabıyla işlenir; koltuk üst sınırı sunucuda denetlenir, kurumsal yönetici kullanıcıları atar."),
         o('usage', 'Kullanım bazlı (ölçülen)', "Dönem sonunda ölçülen kullanım (API çağrısı, GB, mesaj sayısı) üzerinden ücret.", "Altyapı, API ya da iletişim hizmetleri.", "Faturada \"12.400 SMS × 0,18 TL\" satırı.",
           "Kullanım olayları değiştirilemez sayaç kaydına idempotent yazılır; dönem kapanışında toplanıp faturaya aktarılır; müşteri anlık kullanımını panelde görür."),
         o('credits', 'Kredi / seans / hak paketi', "Belirli sayıda kullanım hakkı (danışmanlık seansı, ders, rezervasyon, indirme) içeren paket.", "Danışmanlık, eğitim, spor salonu, ortak çalışma alanı gibi hak bazlı hizmetler.", "\"10 seanslık paket — 7 seans kaldı · Son kullanım 31 Mart\".",
           "Hak bakiyesi işlem defteri (ledger) olarak tutulur; her kullanım ve iade bir satırdır; süresi dolan ve devreden haklar kurala göre işlenir; bakiye eksiye düşemez."),
         o('access', 'Süreli üyelik / içerik erişimi', "Belirli süre boyunca içerik, eğitim ya da topluluk erişimi veren üyelik.", "Eğitim platformu, premium içerik, topluluk.", "\"Premium üyelik — bütün kurslara erişim · 14 Ekim'e kadar\".",
           "Erişim yetkisi üyelik bitiş tarihinden türetilir ve her istekte sunucuda denetlenir; süre bitince erişim kapanır, veriler saklama kuralına göre tutulur."),
         o('freemium', 'Ücretsiz plan (freemium)', "Sınırlı özellikli kalıcı ücretsiz plan ve ücretli plana yükseltme.", "Geniş kullanıcı tabanı edinip bir kısmını ücretliye dönüştürmek isteyen ürünler.", "Ücretsiz planda \"3 proje sınırına ulaştınız — Yükselt\" uyarısı.",
           "Ücretsiz plan da hak tablosunda bir plan olarak tanımlanır; sınır aşımı sunucuda engellenir ve yükseltme önerisi gösterilir."),
     ]},

    {'id': 'sub_trial', 'section': 'biz_subscription', 'type': 'select', 'label': 'Deneme Süresi', 'en': 'Free Trial', 'agents': [PKG, APP], 'showIf': G_SUB,
     'explanation': "Ücretli plana geçmeden önce ücretsiz deneme sunulup sunulmayacağını ve deneme sonunda ne olacağını belirler.",
     'scenario': "Ürünün değerini kullanarak göstermek gerekiyorsa deneme sunulur; kartlı deneme dönüşümü artırabilir ama deneme sonu bildirimi ve kolay iptal şarttır.",
     'example': "\"14 gün ücretsiz dene\" düğmesi; panelde \"Denemenizin bitmesine 3 gün kaldı — Planınızı seçin\" şeridi.",
     'rule': "Deneme süresi: {label}. Deneme başlangıç ve bitiş tarihi abonelik kaydında tutulur; aynı kişi / kurum için tekrar deneme açılması (e-posta, ödeme aracı belirteci, kurum vergi numarası eşleşmesiyle) engellenir; deneme sonunda ne olacağı kayıt sırasında açıkça gösterilir.",
     'options': [
         o('none', 'Deneme yok', "Abonelik ilk ödemeyle başlar.", "Değeri kolay anlaşılan ya da kurulum maliyeti yüksek hizmetler.", "Fiyatlandırma sayfasında yalnız \"Satın al\" düğmesi.",
           "Deneme durumları kurulmaz; ilk dönem ödemesi başarılı olunca abonelik aktifleşir."),
         o('no_card', 'Kartsız deneme (önerilen)', "Deneme kart bilgisi istenmeden başlar; sonunda ödeme yöntemi eklenmezse hesap ücretsiz plana iner ya da salt okunur olur.", "Tüketiciye satış ve sürtünmesiz deneme istenen ürünler.", "Deneme bitince \"Devam etmek için plan seçin\" ekranı; veriler 30 gün saklanır.",
           "Deneme bitiminden önce (ör. 3 gün ve 1 gün kala) bildirim gönderilir; deneme sonunda tahsilat yapılmaz, hesap tanımlı kısıtlı duruma geçer."),
         o('with_card', 'Kartlı deneme, sonunda otomatik başlangıç', "Deneme başında kart saklanır; iptal edilmezse deneme sonunda ilk tahsilat yapılır.", "B2B ürünler ya da kartlı denemenin yaygın olduğu pazarlar.", "Kayıtta \"14 gün ücretsiz — 15. gün 490 TL tahsil edilir, istediğiniz zaman iptal edebilirsiniz\" bilgisi ve onay kutusu.",
           "İlk tahsilat tarihi ve tutarı kayıt anında açıkça gösterilir ve onaylatılır; tahsilattan önce hatırlatma gönderilir; deneme içinde iptal tek adımdır ve hiçbir tahsilat yapılmaz; tüketiciye satışta bu akış hukuk birimince ön bilgilendirme ve abonelik kurallarına göre teyit edilir."),
         o('paid_intro', 'İndirimli ilk dönem', "Ücretsiz deneme yerine ilk dönemin indirimli satılması.", "Deneme kötüye kullanımının yüksek olduğu ürünler.", "\"İlk ay 49 TL, sonra 490 TL/ay\".",
           "İndirimli dönemin süresi ve sonraki normal fiyat ödeme ekranında açıkça yazılır; normal fiyata geçişten önce bildirim gönderilir."),
     ]},

    {'id': 'sub_billing', 'section': 'biz_subscription', 'type': 'multiselect', 'label': 'Tahsilat, Başarısız Ödeme ve Faturalama', 'en': 'Recurring Billing, Dunning & Invoicing', 'agents': [TAH, EFAT, APP], 'showIf': G_SUB,
     'explanation': "Tekrarlayan tahsilatın nasıl yapılacağını, başarısız ödemede hangi adımların izleneceğini (dunning) ve her tahsilattan sonra faturanın nasıl düzenleneceğini belirler.",
     'scenario': "Abonelik geliri kesintisiz toplanmak, kartı süresi dolan ya da limiti yetmeyen müşteri kaybedilmemek ve her tahsilat yasal faturaya bağlanmak isteniyorsa.",
     'example': "Tahsilat başarısız olur; müşteriye \"Ödemeniz alınamadı — kartınızı güncelleyin\" e-postası gider, sistem 1, 3 ve 5. günde yeniden dener; 7. gün hâlâ ödenmemişse abonelik \"Askıda\" olur.",
     'rule': "Tahsilat ve faturalama: {labels}. Her tahsilat denemesi abonelik ve dönem kimliğinden türetilen idempotency anahtarıyla yapılır; tahsilat tarihi, deneme sayısı, sonuç ve ödeme sağlayıcısı işlem kimliği kaydedilir; ödeme sağlayıcısı bildirimleri (webhook) imza doğrulamasıyla, tekrarlara dayanıklı işlenir ve abonelik durumu yalnız sunucuda doğrulanmış sonuca göre değişir; kart bilgisi uygulamada saklanmaz.",
     'options': [
         o('auto_charge', 'Kayıtlı kartla otomatik tahsilat (önerilen)', "Ödeme sağlayıcısında saklanan kart belirteciyle dönem başında otomatik çekim.", "Kartla ödenen abonelikler.", "Her ayın 14'ünde 490 TL otomatik tahsil edilir, makbuz e-postayla gelir.",
           "Kart saklama ve çekim ödeme sağlayıcısının abonelik / kayıtlı kart altyapısıyla yapılır; 3D Secure gerektiren durumda müşteriye doğrulama bağlantısı gönderilir."),
         o('dunning', 'Başarısız ödemede yeniden deneme ve bildirim', "Tanımlı yeniden deneme takvimi, her denemede bildirim ve kart güncelleme çağrısı.", "Otomatik tahsilat yapılan her abonelik.", "Yeniden deneme takvimi: 1., 3., 5. gün; her başarısızlıkta e-posta ve panel uyarısı.",
           "Yeniden deneme sayısı ve aralığı panelden tanımlanır; sağlayıcının kalıcı ret kodlarında (ör. çalıntı kart) yeniden deneme yapılmaz; denemeler idempotent ve kayıtlıdır."),
         o('grace', 'Ek süre ve askıya alma', "Başarısız ödemeden sonra erişimin belirli gün açık kalması, ardından aboneliğin askıya alınması.", "Müşteri kaybını azaltmak isteyen projeler.", "7 günlük ek süre boyunca hizmet çalışır; 8. gün abonelik askıya alınır, ödeme gelince otomatik açılır.",
           "Ek süre bitince abonelik \"Askıda\" durumuna geçer, haklar kurala göre kısıtlanır; ödeme alınınca yeniden aktifleşir; veriler askıda silinmez."),
         o('card_update', 'Kart güncelleme bağlantısı', "Müşterinin panelden ya da e-postadaki güvenli bağlantıdan ödeme yöntemini güncellemesi.", "Kartı süresi dolan müşteriler için.", "\"Kartınızın süresi bu ay doluyor — Güncelleyin\" bağlantısı sağlayıcının güvenli kart sayfasını açar.",
           "Kart güncelleme ödeme sağlayıcısının barındırılan sayfası ya da bileşeniyle yapılır; bağlantı süreli ve tek kullanımlıktır; kart son kullanma tarihi yaklaşınca önceden hatırlatma gönderilir."),
         o('invoice', 'Her tahsilatta e-Fatura / e-Arşiv Fatura', "Başarılı her tahsilattan sonra faturanın entegratör üzerinden otomatik düzenlenmesi.", "Türkiye'de fatura düzenleme yükümlülüğü olan bütün satışlar.", "Tahsilattan sonra müşteriye e-Arşiv Fatura PDF'i ve bağlantısı gider; kurumsal müşteriye e-Fatura olarak iletilir.",
           "Alıcı e-Fatura mükellefiyse e-Fatura, değilse e-Arşiv Fatura düzenlenir (mükellefiyet sorgusu entegratörden); fatura tahsilat kaydına bağlanır ve aynı tahsilat için ikinci fatura kesilmez; uygulanacak belge türü ve zamanlaması mali müşavirce teyit edilir."),
         o('bank_transfer', 'Havale / EFT ile kurumsal fatura', "Kurumsal müşteriye dönem başında fatura kesilip vadeli ödeme beklenmesi.", "Kartla ödeme yapmayan kurumsal müşteriler.", "Kurumsal plan için ayın 1'inde 30 gün vadeli fatura; ödeme eşleşince durum \"Ödendi\".",
           "Ödeme eşleştirme açıklama kodu ve tutarla yapılır; vadesi geçen fatura için tanımlı hatırlatma ve ek süre akışı çalışır."),
     ]},

    {'id': 'sub_changes', 'section': 'biz_subscription', 'type': 'multiselect', 'label': 'Plan Değişikliği, İptal ve Askıya Alma', 'en': 'Plan Changes, Cancellation & Pause', 'agents': [RETAIN, APP], 'showIf': G_SUB,
     'explanation': "Müşterinin plan yükseltme, düşürme, aboneliği dondurma, iptal etme ve yeniden etkinleştirme işlemlerinin nasıl işleyeceğini belirler.",
     'scenario': "Müşterilerin ihtiyaç değiştikçe plan değiştirebilmesi ve iptal edebilmesi gereken her abonelik.",
     'example': "Müşteri panelinde \"Planı değiştir\" → Profesyonel'e geçiş: \"Bugün 516 TL fark tahsil edilecek, sonraki ödemeniz 14 Aralık'ta 1.290 TL\"; \"Aboneliği iptal et\" → tek onay ekranı → \"Aboneliğiniz 14 Aralık'ta sona erecek\".",
     'rule': "Plan değişikliği ve iptal kuralları: {labels}. Fark ve iade tutarları sunucuda hesaplanır ve işlemden önce müşteriye gösterilir; her değişiklik eski plan, yeni plan, tarih ve uygulayan kullanıcıyla kaydedilir ve müşteriye kalıcı veri saklayıcısıyla (e-posta) bildirilir; iptal panelde tek bir akışla yapılabilir ve abonelik başlatma yönteminden daha ağır koşul içermez.",
     'options': [
         o('upgrade_prorate', 'Yükseltme hemen, oranlı fark (önerilen)', "Üst plana geçiş anında geçerli olur; kalan gün için fark oranlanarak tahsil edilir.", "Kademeli planlı her abonelik.", "Ayın 15'inde yükseltmede yarım ayın farkı tahsil edilir, yeni haklar hemen açılır.",
           "Oranlı fark kalan gün / dönem gün sayısıyla sunucuda hesaplanır, tahsilat başarılı olunca yeni haklar açılır; tahsilat başarısızsa plan değişmez."),
         o('downgrade_end', 'Düşürme dönem sonunda', "Alt plana geçiş mevcut dönemin sonunda uygulanır; dönem sonuna kadar mevcut haklar sürer.", "Ödenmiş dönemin iadesiyle uğraşılmak istenmiyorsa.", "\"Başlangıç planına geçişiniz 14 Aralık'ta yapılacak\" bilgisi.",
           "Düşürme planlı değişiklik olarak kaydedilir ve dönem sonunda uygulanır; yeni planın limitini aşan kullanım (ör. kullanıcı sayısı) için müşteriye önceden uyarı gösterilir."),
         o('cancel_end', 'İptal dönem sonunda geçerli', "İptal anında kaydedilir; erişim ödenmiş dönemin sonuna kadar sürer, yenileme yapılmaz.", "Aylık / belirsiz süreli abonelikler.", "\"Aboneliğiniz iptal edildi — 14 Aralık'a kadar kullanmaya devam edebilirsiniz\".",
           "İptal talebi alındığında yenileme durdurulur ve iptal onayı e-postayla gönderilir; iptal dönem sonunda hüküm doğurur, yeniden etkinleştirme dönem sonuna kadar tek tıkla yapılabilir."),
         o('cancel_now_refund', 'Hemen iptal ve kalan ücretin iadesi', "İptal hemen geçerli olur, ödenmiş ama kullanılmamış dönemin ücreti iade edilir.", "Yıllık peşin ödemeli abonelikler ya da yasal fesih durumları.", "Yıllık aboneliği 4. ayda iptal eden tüketiciye kalan 8 ayın ücreti iade edilir.",
           "Kalan dönem iadesi sunucuda hesaplanır ve ödeme sağlayıcısına idempotent iade isteğiyle gönderilir; tüketici aboneliklerinde iade, fesih bildiriminin hüküm ifade etmesinden itibaren 15 gün içinde kesinti yapılmadan tamamlanır."),
         o('pause', 'Dondurma (askıya alma)', "Müşterinin aboneliği belirli süre dondurması; tahsilat ve haklar durur.", "Mevsimsel kullanım ya da geçici ara veren müşteriler (spor salonu, eğitim).", "\"Aboneliğimi 1 ay dondur\" seçeneği; dönüş tarihi panelde görünür.",
           "Dondurma süresi üst sınırı ve yılda kaç kez yapılabileceği panelden tanımlanır; dondurma bitince abonelik kendiliğinden ve önceden bildirilerek devam eder."),
         o('reactivate', 'Yeniden etkinleştirme', "İptal edilen ya da askıya alınan aboneliğin yeniden başlatılması.", "Geri dönen müşteriler.", "\"Aboneliğinizi yeniden başlatın — verileriniz duruyor\".",
           "Yeniden etkinleştirme yeni bir ödeme onayı gerektirir; eski plan pasifse güncel plan sürümü gösterilir."),
         o('retention', 'İptal akışında isteğe bağlı neden ve teklif', "İptal ekranında tek adımlık isteğe bağlı neden sorusu ve dondurma / indirim önerisi.", "Müşteri kaybını anlamak ve azaltmak isteniyorsa.", "İptal ekranında \"Ayrılma nedeniniz (isteğe bağlı)\" ve \"Bunun yerine 1 ay dondurabilirsiniz\" bağlantısı; \"İptali onayla\" düğmesi aynı ekranda.",
           "Neden sorusu ve teklif isteğe bağlıdır; iptal onayı aynı ekranda erişilebilir kalır, ek ekran, telefon ya da temsilci görüşmesi şartı konmaz."),
     ]},

    {'id': 'sub_legal', 'section': 'biz_subscription', 'type': 'multiselect', 'label': 'Abonelik Sözleşmesi, Yenileme ve Bildirimler', 'en': 'Subscription Contract, Renewal & Notices', 'agents': [CONTRACT, KVKK, APP], 'showIf': G_SUB,
     'explanation': "Tüketiciye satılan aboneliklerde sözleşme, ön bilgilendirme, yenileme onayı, fesih ve iade yükümlülüklerinin uygulamada nasıl karşılanacağını belirler (6502 sayılı Kanun m. 48 ve 52, Abonelik Sözleşmeleri Yönetmeliği, Mesafeli Sözleşmeler Yönetmeliği).",
     'scenario': "Bireysel müşteriye (tüketici) abonelik satılıyorsa bu yükümlülükler zorunludur; yalnız kurumlara satışta sözleşme hükümleri ayrıca hukuk birimince belirlenir.",
     'example': "Ödeme adımında ön bilgilendirme formu ve abonelik sözleşmesi metni, onay kutusu; tahsilattan sonra sözleşmenin PDF'i e-postayla gelir; 12 aylık planın bitimine 30 gün kala \"Aboneliğinizi uzatmak ister misiniz?\" e-postası ve panelde \"Uzat\" düğmesi.",
     'rule': "Abonelik yasal yükümlülükleri: {labels}. Bu yükümlülüklerin projedeki uygulaması (metinler, süreler, belirli süreli / belirsiz süreli ayrımı, kurumsal müşterilere uygulanacak koşullar) yayından önce hukuk birimince teyit edilir; onaylanan metin sürümü, onay tarihi ve IP adresi her abonelik kaydında saklanır.",
     'options': [
         o('pre_info', 'Ön bilgilendirme ve sözleşme onayı (önerilen)', "Ödemeden önce ön bilgilendirme formu, abonelik / mesafeli satış sözleşmesi ve cayma hakkı bilgisinin gösterilip onaylatılması.", "Tüketiciye mesafeli abonelik satışı.", "Ödeme adımında açılır metinler ve \"Ön bilgilendirme formunu ve sözleşmeyi okudum, onaylıyorum\" kutusu (önceden işaretli değil).",
           "Metinler hukuki metin yönetiminden sürümüyle çekilir; plan adı, toplam fiyat (vergiler dahil), dönem, sonraki tahsilat tarihi ve fesih yöntemi metne değişken olarak işlenir; onay kaydı sürüm, tarih ve IP ile saklanır."),
         o('contract_copy', 'Sözleşmenin kalıcı veri saklayıcısıyla verilmesi', "Abonelik sözleşmesinin bir nüshasının e-posta / PDF olarak tüketiciye iletilmesi ve panelde erişilebilir olması.", "Tüketiciye yazılı ya da mesafeli abonelik.", "Abonelik başlayınca sözleşme PDF'i e-postayla gelir; panelde \"Sözleşmelerim\" altında indirilebilir.",
           "Onaylanan sözleşme sürümünden kişiye özel PDF üretilir, e-postayla gönderilir ve panelde süresiz değil saklama süresi boyunca indirilebilir tutulur (6502 m. 52/2)."),
         o('renewal_consent', 'Belirli süreli abonelikte açık onayla uzatma', "12 ay gibi belirli süreli aboneliklerin kendiliğinden aynı süre için uzamaması; uzatmanın tüketicinin süre bitmeden vereceği açık talep / onayla yapılması.", "Taahhütlü ya da belirli süreli (ör. yıllık) planlar satılıyorsa.", "Yıllık plan bitiminden önce \"Uzat\" e-postası; onay gelmezse plan dönem sonunda sona erer ya da tüketicinin onayladığı belirsiz süreli plana geçer.",
           "Belirli süreli abonelik sözleşmesine kendiliğinden aynı süre uzama hükmü konmaz; uzatma ancak sözleşme bitmeden tüketicinin talebi ya da onayıyla yapılır ve bu onay kaydedilir; onaysız dönem için tahsilat yapılmaz (6502 m. 52/3, Abonelik Sözleşmeleri Yönetmeliği m. 13)."),
         o('easy_cancel', 'İptalin kayıt yönteminden zor olmaması', "Abonelik çevrim içi başlatıldıysa iptalin de çevrim içi, panelde tek akışla yapılabilmesi.", "Bütün tüketici abonelikleri.", "Panelde \"Aboneliği iptal et\" bağlantısı; telefon ya da dilekçe şartı yok.",
           "İptal, abonelik başlatma yönteminden daha ağır koşul içermez ve fesih bildirimi kalıcı veri saklayıcısıyla alınır; tüketicinin fesih hakkı (belirsiz süreli ya da bir yıl ve daha uzun belirli süreli abonelikte gerekçesiz ve cezasız) uygulamada engellenmez (6502 m. 52/4, Yönetmelik m. 22–23)."),
         o('cancel_deadline', 'Fesih süresi ve iade takibi', "Fesih talebinin en geç 7 gün içinde yerine getirilmesi, feshin bildirilmesi ve kalan ücretin 15 gün içinde iadesi.", "Bütün tüketici abonelikleri.", "Panelde fesih talebi \"Alındı · 12 Kas\" → \"Sonuçlandı · 12 Kas\" → \"İade edildi · 14 Kas\".",
           "Fesih talepleri için süre sayacı tutulur; talep en geç 7 gün içinde sonuçlandırılır, fesih tüketiciye kalıcı veri saklayıcısıyla bildirilir, ödenmiş tutarın kalan kısmı 15 gün içinde kesintisiz iade edilir; süre aşımı yöneticiye uyarı üretir (Abonelik Sözleşmeleri Yönetmeliği m. 24–25)."),
         o('renewal_reminder', 'Yenileme ve fiyat değişikliği bildirimi', "Yenileme tarihinden ve fiyat değişikliğinden önce müşteriye bildirim.", "Yıllık planlar ve fiyat güncellemesi yapılan abonelikler.", "Yenilemeden 7 gün önce \"14 Aralık'ta 4.900 TL tahsil edilecek\" e-postası.",
           "Yenileme hatırlatması ve fiyat değişikliği bildirimi işlemsel bildirim olarak gönderilir; fiyat değişikliğinin mevcut abonelere uygulanma koşulları ve bildirim süresi hukuk birimince belirlenip sözleşmeye yazılır."),
     ]},

    {'id': 'sub_provider', 'section': 'biz_subscription', 'type': 'select', 'label': 'Tekrarlayan Ödeme Sağlayıcısı', 'en': 'Recurring Payment Provider', 'agents': [INT, TAH], 'showIf': G_SUB,
     'explanation': "Kart saklama ve tekrarlayan tahsilatın hangi ödeme kuruluşu üzerinden yapılacağını belirler. Projede başka bir ödeme sağlayıcısı kararı varsa aynı sağlayıcı tercih edilir.",
     'scenario': "Türkiye'de kartla abonelik tahsilatı için yerli ödeme kuruluşları, yurt dışında yerleşik şirket yapılarında uluslararası sağlayıcılar, mobil uygulama içi satışta mağaza abonelikleri öne çıkar.",
     'example': "iyzico panelinde \"Profesyonel Aylık\" ödeme planı; sitedeki abonelik kaydı iyzico abonelik referansını tutar ve ödeme bildirimlerini webhook ile alır.",
     'rule': "Tekrarlayan ödeme sağlayıcısı: {label}. Kart verisi uygulama sunucusuna gelmez (sağlayıcının barındırılan ödeme sayfası / bileşeni ve kart belirteci kullanılır); sağlayıcı API anahtarları yalnız sunucu tarafındaki gizli anahtar deposunda tutulur; sağlayıcı bildirimleri imza doğrulamasıyla işlenir; sağlayıcıdaki abonelik / ödeme durumu ile sitedeki kayıt günlük mutabakatla karşılaştırılır.",
     'options': [
         o('iyzico', 'iyzico Abonelik (önerilen)', "iyzico'nun ödeme planı, deneme süresi ve kayıtlı kartla tekrarlayan tahsilat ürünü.", "Türkiye'de kurulu, TL ile tüketiciye ya da kuruma abonelik satan projeler.", "Planlar iyzico panelinden ya da API ile tanımlanır, tahsilatlar iyzico'dan yapılır.",
           "iyzico Abonelik API'si ile ürün / ödeme planı ve abone oluşturulur; abonelik referans kodları sitede saklanır, ödeme sonuçları bildirimlerle güncellenir; ürünün ücretlendirme koşulları sağlayıcıyla teyit edilir."),
         o('paytr', 'PayTR (kart saklama ile tekrarlayan tahsilat)', "PayTR'nin kart saklama özelliğiyle dönemsel çekimi uygulamanın planlaması.", "PayTR ile çalışan projeler.", "Sistem her dönem başında saklı kart belirteciyle PayTR'ye ödeme isteği gönderir.",
           "Dönem takvimi ve yeniden deneme uygulama tarafında yönetilir; çekim saklı kart belirteciyle yapılır; tekrarlayan ödeme ve kart saklama özelliğinin hesapta açık olduğu sağlayıcıyla teyit edilir."),
         o('stripe', 'Stripe Billing', "Stripe'ın abonelik, faturalama, oranlama ve yeniden deneme altyapısı.", "Yurt dışında yerleşik şirket yapısıyla uluslararası abonelik satan projeler.", "Stripe Customer Portal üzerinden plan değişikliği ve kart güncelleme.",
           "Stripe Billing abonelik nesneleri ve webhook olayları kullanılır; Stripe hesabının şirketin kuruluş ülkesinde açılabildiği ve Türkiye'deki müşteriye fatura yükümlülüklerinin nasıl karşılanacağı önceden teyit edilir."),
         o('app_store', 'Mobil uygulama mağazası abonelikleri', "App Store / Google Play uygulama içi abonelikleri.", "Dijital içerik ya da özellik mobil uygulamada satılıyorsa.", "Uygulamada \"Premium'a geç\" mağazanın ödeme ekranını açar; web hesabı abonelik durumunu sunucu bildirimlerinden alır.",
           "Mağaza sunucu bildirimleri ve makbuz doğrulaması sunucuda yapılır; web ve mobil abonelikleri aynı hak tablosunda birleşir, aynı hak iki kanaldan iki kez satılmaz."),
         o('pos', 'Banka sanal POS + uygulamanın kendi tekrarlama motoru', "Bankanın sanal POS'u ve kart saklama hizmetiyle, dönem ve yeniden deneme mantığının tamamen uygulamada kurulması.", "Bankayla doğrudan anlaşmalı, özel komisyon şartı olan kurumlar.", "Uygulama gece görevinde vadesi gelen abonelikler için POS'a çekim isteği gönderir.",
           "Kart saklama bankanın / sağlayıcının belirteç hizmetiyle yapılır, uygulama kart verisi saklamaz; zamanlayıcı görev kilitli ve idempotent çalışır, aynı dönem iki kez çekilmez."),
     ]},
]

# ---------------------------------------------------------------- B5 Online Danışmanlık Satışı
S_CS = {
    'id': 'biz_consulting', 'group': 'İş Modülleri', 'icon': '☎',
    'name': 'Online Danışmanlık Satışı', 'en': 'Online Consulting Sales & Video Sessions',
    'desc': "Danışmanlık paket modelini, danışman ve takvim yönetimini, görüntülü görüşme entegrasyonunu, ödeme zamanı ile iptal / iade kuralını ve hatırlatma, görüşme notu ve kayıt iznini karara bağlar",
    'guide': {
        'purpose': "Online danışmanlık modülü uzaktan verilen ücretli hizmetin (seans, paket ya da abonelik) uçtan uca satışını yönetir: hizmet ve danışman seçimi, uygun tarih / saat seçimi, ödeme, randevu oluşturma, görüntülü görüşme bağlantısı üretimi, hatırlatmalar, görüşme sonrası not ve takip. Randevu ve uygunluk altyapısı Rezervasyon / Randevu modülüyle ortaktır — ikinci bir takvim motoru kurulmaz; seans paketleri ve abonelikler Abonelik modülünün hak yapısını, satış ve fatura E-Ticaret modülünü, başvurular CRM'i kullanır. Görüşme kaydı ve danışmanlık sırasında paylaşılan bilgiler (ör. sağlık, hukuk, finans) kişisel ve çoğu zaman hassas veridir; kayıt varsayılan olarak kapalı tutulur.",
        'criteria': [
            "Aynı danışman için çakışan randevu, eşzamanlı iki ödemede bile oluşamaz; uygunluk sunucuda kilit ya da benzersizlik kısıtıyla korunur.",
            "Seçilen saat ödeme sırasında kısa bir süre tutulur, ödeme tamamlanmazsa otomatik serbest bırakılır; randevu ödeme sunucuda doğrulanınca onaylanır.",
            "Görüşme bağlantısı her randevuya özeldir, yalnız müşteri, danışman ve yetkili yöneticiye gösterilir, bekleme odası / lobi açıktır ve analitik araçlarına gönderilmez.",
            "İptal, yeniden planlama ve iade kuralı satın almadan önce açıkça gösterilir ve sistemde aynı kurala göre uygulanır.",
            "Hatırlatmalar müşterinin ve danışmanın saat dilimine göre gönderilir; takvim daveti (.ics) standart biçimdedir.",
            "Görüşme notları yalnız ilgili danışman ve yetkili roller tarafından görülür; kayıt yapılacaksa önceden açık bilgilendirme ve gerekli hukuki dayanak (çoğu durumda açık rıza) alınır.",
        ],
        'pitfalls': [
            "Rezervasyon modülü varken danışmanlık için ayrı bir takvim ve uygunluk sistemi yazmak: iki sistem aynı danışmana çakışan randevu verir.",
            "Görüşme bağlantısını ödeme öncesinde ya da herkese açık sayfada göstermek: ödeme yapmayan kişi görüşmeye katılabilir.",
            "Bütün görüşmelerin kaydını varsayılan olarak açmak: hassas kişisel veri gereksiz yere işlenir ve saklanır.",
            "Saat dilimini hesaba katmamak: yurt dışındaki müşteri görüşmeye bir saat geç ya da erken katılır.",
            "İptal / iade kuralını yalnız sözleşme metnine yazıp sisteme uygulamamak: destek ekibi her iptali elle tartışır.",
            "Danışman notlarını CRM'deki herkesin görebileceği alana yazmak: danışmanlık sırrı ve kişisel veri geniş bir ekiple paylaşılır.",
        ],
        'resources': [
            {'title': "Mesafeli Sözleşmeler Yönetmeliği", 'url': 'https://www.mevzuat.gov.tr/mevzuat?MevzuatNo=20237&MevzuatTur=7&MevzuatTertip=5', 'note': "Ön bilgilendirme, cayma hakkı ve istisnaları (m. 15) — uzaktan satılan danışmanlık hizmetine uygulanışı hukuk birimince belirlenir."},
            {'title': "KVKK — Açık Rıza Alırken Dikkat Edilecek Hususlar", 'url': 'https://www.kvkk.gov.tr/Icerik/2037/Acik-Riza-Alirken-Dikkat-Edilecek-Hususlar', 'note': "Görüşme kaydı gibi işlemler için rızanın belirli, bilgilendirmeye dayalı ve özgür iradeyle alınması."},
            {'title': "KVKK — Aydınlatma Yükümlülüğü", 'url': 'https://www.kvkk.gov.tr/Icerik/2033/Aydinlatma-Yukumlulugu-', 'note': "Başvuru formu, görüşme ve not süreçlerinde yapılacak bilgilendirme."},
            {'title': "Zoom — Meetings API", 'url': 'https://developers.zoom.us/docs/api/meetings/', 'note': "Randevuya özel Zoom toplantısı oluşturma, güncelleme ve silme."},
            {'title': "Google Meet REST API overview", 'url': 'https://developers.google.com/workspace/meet/api/guides/overview', 'note': "Google Meet toplantı alanı (meeting space) oluşturma ve ayarları."},
            {'title': "Google Calendar API — Create events", 'url': 'https://developers.google.com/workspace/calendar/api/guides/create-events', 'note': "Takvim etkinliğine Meet bağlantısı (conferenceData) ekleyerek randevu oluşturma."},
            {'title': "Microsoft Graph — Create onlineMeeting", 'url': 'https://learn.microsoft.com/en-us/graph/api/application-post-onlinemeetings', 'note': "Microsoft Teams çevrim içi toplantısı oluşturma."},
            {'title': "Jitsi Meet Handbook", 'url': 'https://jitsi.github.io/handbook/', 'note': "Açık kaynak görüntülü görüşme altyapısının kurulumu ve kendi sunucuda barındırılması."},
            {'title': "RFC 5545 — iCalendar", 'url': 'https://www.rfc-editor.org/rfc/rfc5545', 'note': "Randevu davetlerinin (.ics) standart biçimi, saat dilimi ve güncelleme / iptal iletileri."},
        ],
    },
}

F_CS = [
    {'id': 'cs_packages', 'section': 'biz_consulting', 'type': 'multiselect', 'label': 'Danışmanlık Satış Modeli', 'en': 'Consulting Offer Model', 'agents': [PM, APP], 'showIf': G_CS,
     'explanation': "Danışmanlık hizmetinin hangi biçimlerde satılacağını belirler: tek seans, çoklu seans paketi, abonelik / üyelik, kurumsal paket ya da ücretsiz ön görüşme.",
     'scenario': "Hizmet tek seferlik mi, düzenli takip mi gerektiriyor; bireysel mi kurumsal mı satılıyor sorusunun yanıtına göre seçilir.",
     'example': "Hizmet sayfasında \"Tek seans 45 dk — 1.500 TL · 5 seanslık paket — 6.750 TL (%10 avantajlı) · Kurumsal ekip paketi — teklif alın · Ücretsiz 15 dk tanışma görüşmesi\".",
     'rule': "Danışmanlık satış modeli: {labels}. Her danışmanlık hizmetinde süre (ör. 30 / 45 / 60 / 90 dk), fiyat, para birimi, kapsam, teslim yöntemi ve danışman tipi tanımlanır; satış, sipariş ve fatura E-Ticaret altyapısıyla, başvurular CRM'e lead / fırsat olarak yazılır; randevu ve uygunluk Rezervasyon / Randevu modülüyle ortak altyapıda tutulur, ayrı bir takvim motoru kurulmaz.",
     'recommend': {'field': 'modules_extra', 'map': {'subscription': ['subscription'], 'crm': ['free_intro']}},
     'options': [
         o('single', 'Tek seans (önerilen)', "Belirli süreli tek görüşme satışı.", "İlk görüşme, tek seferlik danışmanlık.", "\"60 dk strateji görüşmesi — 2.500 TL\".",
           "Tek seans ürünü ödeme sonrası bir randevu hakkı üretir ve hak randevu oluşturulunca kullanılır."),
         o('bundle', 'Çoklu seans paketi', "Belirli sayıda seans içeren, son kullanım tarihli paket.", "Düzenli takip gerektiren danışmanlık (koçluk, diyet, terapi).", "Panelde \"5 seanslık paket — 3 seans kaldı · Son kullanım 30 Haziran\".",
           "Paket seansları hak defterinde tutulur; randevu oluşunca hak düşer, kurala uygun iptalde iade edilir; paket son kullanım tarihi satın almadan önce gösterilir."),
         o('subscription', 'Abonelik / üyelik', "Aylık belirli seans hakkı ya da sınırsız danışman erişimi veren abonelik.", "Abonelik modülü varsa ve sürekli danışmanlık sunuluyorsa.", "\"Aylık 2 seans + mesajla destek — 2.900 TL/ay\".",
           "Seans hakları Abonelik modülünün hak tablosundan gelir; dönem sonunda kullanılmayan hakların devri plan kuralına göre işlenir."),
         o('corporate', 'Kurumsal paket', "Bir kurumun çalışanları için toplu seans hakkı ve kurumsal faturalandırma.", "Çalışan destek programları, kurumsal eğitim / koçluk.", "ABC Holding çalışanları kurum koduyla kayıt olur, seanslar kurumun 100 seanslık havuzundan düşer.",
           "Kurumsal havuz kurum hesabına bağlanır; kurum yöneticisi yalnız toplu kullanım sayısını görür, çalışanın görüşme içeriğini ve notlarını göremez."),
         o('free_intro', 'Ücretsiz ön görüşme', "Satış öncesi kısa ücretsiz tanışma görüşmesi.", "Hizmetin değerini anlatmak ve doğru paketi önermek için.", "\"15 dk ücretsiz tanışma\" randevusu; görüşme sonrası danışman paket önerisi gönderir.",
           "Ücretsiz görüşme kişi başı sınırlıdır (aynı e-posta / telefonla tekrar alınamaz) ve CRM'de fırsat olarak açılır."),
     ]},

    {'id': 'cs_experts', 'section': 'biz_consulting', 'type': 'multiselect', 'label': 'Danışman ve Takvim Yönetimi', 'en': 'Consultant Profiles & Availability', 'agents': [PM, APP], 'showIf': G_CS,
     'explanation': "Danışman profillerinin, çalışma saatlerinin ve uygunluğun nasıl yönetileceğini belirler.",
     'scenario': "Birden çok danışman varsa, danışmanlar kişisel takvimlerini kullanıyorsa ya da farklı saat dilimlerinde hizmet veriliyorsa.",
     'example': "Danışman panelinde \"Çalışma saatlerim: Pzt–Cum 10:00–18:00 · Seans arası 15 dk · Günde en çok 6 görüşme · 20–24 Aralık izinli\"; Google Takvim'deki özel randevular sitede dolu görünür.",
     'rule': "Danışman ve takvim yönetimi: {labels}. Uygunluk sunucuda hesaplanır; aynı danışman için çakışan randevu, eşzamanlı isteklerde bile veritabanı düzeyinde kilit ya da benzersizlik kısıtıyla engellenir; bütün zamanlar UTC olarak saklanır, müşteriye ve danışmana kendi saat dilimiyle gösterilir; Rezervasyon / Randevu modülü etkinse aynı uygunluk ve randevu tabloları kullanılır.",
     'recommend': {'field': 'modules_extra', 'map': {'booking': ['calendar_sync']}},
     'options': [
         o('profiles', 'Danışman profilleri (önerilen)', "Uzmanlık alanı, unvan, biyografi, sertifikalar, konuşulan diller ve verdiği hizmetler.", "Müşterinin danışman seçtiği her yapı.", "\"Uzm. Psk. Ayşe K. · Bilişsel davranışçı terapi · Türkçe, İngilizce · 8 yıl deneyim\" kartı.",
           "Danışman profili personel kaydına bağlıdır; profil yayını onaya tabidir, sertifika belgeleri yalnız yetkililerce görülür."),
         o('availability', 'Çalışma saatleri ve istisnalar', "Haftalık çalışma saatleri, kapalı günler, izinler ve özel tarihler.", "Danışmanların farklı günlerde çalıştığı yapılar.", "İzin girilen günlerde müşteri takviminde saat seçeneği çıkmaz.",
           "Uygunluk haftalık şablon + istisna kayıtlarından hesaplanır; geçmişte kalan ve en kısa önceden rezervasyon süresinden yakın saatler sunulmaz."),
         o('buffer', 'Seans arası hazırlık süresi ve günlük sınır', "Seanslar arasında boşluk ve danışman başına günlük en çok görüşme sayısı.", "Yoğun çalışan danışmanlar.", "60 dakikalık seanstan sonra 15 dakika boşluk; günde en çok 6 görüşme.",
           "Hazırlık süresi ve günlük sınır uygunluk hesabına dahil edilir ve danışman bazında ayarlanabilir."),
         o('calendar_sync', 'Kişisel takvim senkronu (Google / Outlook)', "Danışmanın kişisel takvimindeki dolu zamanların sitede dolu görünmesi ve randevuların takvime yazılması.", "Danışmanlar dış takvim kullanıyorsa.", "Danışmanın Google Takvim'deki toplantısı sitede o saati kapatır; yeni randevu takvime eklenir.",
           "Takvim bağlantısı OAuth ile en dar kapsamla kurulur (yalnız dolu / boş bilgisi ve uygulamanın oluşturduğu etkinlikler); belirteçler şifreli saklanır, bağlantı danışman tarafından kaldırılabilir."),
         o('auto_assign', 'Otomatik danışman atama', "Müşteri danışman seçmeden hizmet ve saat seçer, sistem uygun danışmanı atar.", "Danışmanların birbirinin yerine geçebildiği hizmetler.", "\"İlk uygun danışmanla görüş\" seçeneği.",
           "Atama uygunluk, uzmanlık ve yük dengesine göre yapılır; atanan danışman randevu onayında gösterilir."),
         o('performance', 'Danışman performans raporu', "Randevu sayısı, tamamlanan görüşme, iptal ve gelmeme (no-show) oranı, gelir ve memnuniyet.", "Birden çok danışmanın yönetildiği yapılar.", "Panoda danışman bazlı \"Bu ay 42 görüşme · No-show %4 · CSAT 4,8\".",
           "Danışman yalnız kendi performansını, yönetici bütün danışmanları görür; memnuniyet sonuçları toplu gösterilir."),
     ]},

    {'id': 'cs_video', 'section': 'biz_consulting', 'type': 'select', 'label': 'Görüntülü Görüşme Altyapısı', 'en': 'Video Meeting Integration', 'agents': [INT, APP], 'showIf': G_CS,
     'explanation': "Randevular için görüşme bağlantısının hangi platformda ve nasıl üretileceğini belirler.",
     'scenario': "Kurumun ve danışmanların zaten kullandığı platform genellikle en iyi seçimdir; veri yerleşimi ve kayıt kontrolü önemliyse kendi sunucunda barındırılan çözüm düşünülür.",
     'example': "Ödeme onaylanınca randevuya özel Zoom toplantısı oluşur; bağlantı müşteri panelinde \"Görüşmeye katıl\" düğmesi olarak görüşmeden 10 dakika önce etkinleşir.",
     'rule': "Görüntülü görüşme altyapısı: {label}. Bağlantı her randevuya özel üretilir ve randevu ödeme / onayla kesinleştikten sonra gösterilir; yalnız müşteri, danışman ve yetkili yöneticiye görünür, herkese açık sayfaya, URL parametresine ve analitik araçlarına yazılmaz; bekleme odası / lobi açıktır; randevu iptal ya da yeniden planlanınca toplantı silinir / güncellenir; bağlantı oluşturma, güncelleme ve iptal işlemleri kaydedilir; platform API anahtarları yalnız sunucu tarafındaki gizli anahtar deposunda tutulur.",
     'options': [
         o('meet', 'Google Meet (Google Takvim ile) (önerilen)', "Randevu Google Takvim etkinliği olarak oluşturulur ve Meet bağlantısı eklenir.", "Google Workspace kullanan kurumlar.", "Müşteriye gelen takvim davetinde Meet bağlantısı.",
           "Google Calendar API ile etkinlik oluşturulurken conferenceData ile Meet bağlantısı istenir; etkinlik kurumun hizmet takviminde tutulur."),
         o('zoom', 'Zoom', "Randevuya özel Zoom toplantısı Zoom Meetings API ile oluşturulur.", "Danışmanlar ya da müşteriler Zoom'a alışkınsa.", "Onay e-postasında Zoom bağlantısı ve toplantı şifresi.",
           "Zoom Meetings API'si sunucudan sunucuya OAuth uygulamasıyla kullanılır; toplantıda bekleme odası ve şifre açık, katılımcı kaydı kapalı olarak oluşturulur."),
         o('teams', 'Microsoft Teams', "Microsoft Graph ile çevrim içi Teams toplantısı oluşturulur.", "Microsoft 365 kullanan kurumsal yapılar.", "Kurumsal müşteriye Teams toplantı bağlantısı gider.",
           "Microsoft Graph onlineMeeting / takvim etkinliği API'leri en dar izinle kullanılır; lobi ayarı dış katılımcıyı bekletecek biçimde yapılır."),
         o('jitsi', 'Jitsi (kendi sunucunda)', "Açık kaynak Jitsi Meet'in kurumun sunucusunda barındırılması.", "Veri yerleşimi ve kayıt kontrolü kritikse, lisans maliyeti istenmiyorsa.", "Görüşme meet.kurum.com.tr adresinde, tahmin edilemez oda adıyla açılır.",
           "Jitsi kendi sunucuda kurulur, odaya yalnız randevuya özel süreli belirteçle (JWT) girilir; oda adları tahmin edilemez; sunucu güncelleme ve kapasite planı operasyona dahil edilir."),
         o('manual', 'Danışman bağlantıyı elle ekler', "Danışman kendi kullandığı platformdan bağlantıyı randevuya elle girer.", "Az sayıda danışman, entegrasyon maliyeti istenmiyorsa.", "Danışman panelinde \"Görüşme bağlantısı ekle\" alanı; eklenince müşteriye bildirim gider.",
           "Elle girilen bağlantı adres biçimi ve izinli alan adları listesiyle doğrulanır; randevudan belirli süre önce bağlantı eklenmemişse danışmana ve yöneticiye uyarı gider."),
     ]},

    {'id': 'cs_payment', 'section': 'biz_consulting', 'type': 'select', 'label': 'Ödeme Zamanı ve İptal / İade Kuralı', 'en': 'Payment Timing & Cancellation Policy', 'agents': [CONTRACT, APP], 'showIf': G_CS,
     'explanation': "Danışmanlık bedelinin ne zaman alınacağını ve iptal, yeniden planlama ile gelmeme (no-show) durumlarında hangi kuralın uygulanacağını belirler.",
     'scenario': "Danışman zamanının boşa gitmemesi ve müşteriye adil, önceden bilinen bir iptal hakkı sunulması isteniyorsa.",
     'example': "Ödeme ekranında \"Görüşmeden 24 saat öncesine kadar ücretsiz iptal ya da bir kez yeniden planlama · Sonrasında iade yapılmaz\" notu; müşteri panelinde \"İptal et\" düğmesi süre dolunca \"Yeniden planlama talebi\"ne dönüşür.",
     'rule': "Ödeme zamanı ve iptal kuralı: {label}. Seçilen saat ödeme sırasında tanımlı süre tutulur, ödeme tamamlanmazsa otomatik serbest bırakılır; randevu, ödeme sunucuda doğrulanınca onaylanır; iptal / yeniden planlama penceresi ve iade tutarı sunucuda kurala göre hesaplanır ve satın almadan önce ön bilgilendirmede gösterilir; iadeler ödeme sağlayıcısına idempotent iade isteğiyle gönderilir; cayma hakkı ve istisnalarının (Mesafeli Sözleşmeler Yönetmeliği m. 15) danışmanlık hizmetine uygulanışı ile seçilen kuralın metni hukuk birimince teyit edilir.",
     'options': [
         o('prepay_24h', 'Randevuda tam ödeme · 24 saate kadar ücretsiz iptal (önerilen)', "Ödeme randevu alınırken yapılır; görüşmeden 24 saat öncesine kadar iptal tam iade ya da ücretsiz yeniden planlama sağlar.", "Bireysel müşteriye satılan çoğu danışmanlık.", "Görüşmeye 30 saat kala iptal eden müşteriye tam iade yapılır.",
           "İptal penceresi görüşme başlangıcından geriye hesaplanır; pencere içinde iptal tam iade ya da paket hakkının geri yüklenmesiyle sonuçlanır, pencere dışındaki iptal iade üretmez."),
         o('prepay_48h', 'Randevuda tam ödeme · 48 saate kadar iptal, sonra yalnız yeniden planlama', "Daha uzun iptal penceresi; pencere dışında iade yerine bir kez yeniden planlama hakkı.", "Hazırlık gerektiren uzun seanslar ve kurumsal danışmanlık.", "Görüşmeye 20 saat kala müşteri iade alamaz ama bir kez başka güne alabilir.",
           "Yeniden planlama hakkı sayısı randevu kaydında tutulur ve kullanıldıkça düşer."),
         o('deposit', 'Kapora ile rezervasyon, kalan görüşme sonrası', "Randevu kaporayla kesinleşir, kalan tutar görüşmeden sonra ödeme bağlantısıyla alınır.", "Uzun ya da tutarı görüşmede netleşen hizmetler.", "Kapora 500 TL; görüşme sonrası 2.000 TL'lik ödeme bağlantısı gönderilir.",
           "Kapora ve kalan tutar ayrı tahsilat kaydıdır; kalan tutar için ödeme bağlantısı süreli ve tek kullanımlıktır, vadesi geçen ödeme için hatırlatma gönderilir."),
         o('package_credit', 'Paket / abonelik hakkından düşüm', "Ücret paket ya da abonelikle önceden alınmıştır; randevu hak düşer, kurala uygun iptalde hak geri yüklenir.", "Seans paketi ya da abonelik satılıyorsa.", "Pakette 3 seans kalmışken alınan randevu bakiyeyi 2'ye düşürür; 24 saat önce iptal edilince 3'e döner.",
           "Hak düşümü ve iadesi atomik ve idempotenttir; no-show durumunda hak kural gereği yanar ve kayıtta \"no-show\" olarak işaretlenir."),
         o('invoice', 'Kurumsal fatura (görüşme sonrası)', "Kurumsal müşteriye görüşmeler sonrasında dönemsel fatura kesilir; iptal koşulları kurumsal sözleşmeye göredir.", "Kurumsal danışmanlık sözleşmeleri.", "Ay sonunda kuruma \"Kasım — 18 seans\" faturası.",
           "Kurumsal randevular sözleşme kimliğine bağlanır; iptal ve no-show kuralları sözleşmeden okunur, dönem sonunda faturalanacak seanslar raporlanır."),
     ]},

    {'id': 'cs_session', 'section': 'biz_consulting', 'type': 'multiselect', 'label': 'Hatırlatma, Görüşme Notu ve Kayıt', 'en': 'Reminders, Session Notes & Recording', 'agents': [KVKK_LAW, APP], 'showIf': G_CS,
     'explanation': "Randevu öncesi hatırlatmaları, görüşme sonrası notları ve takip adımlarını, görüşme kaydının yapılıp yapılmayacağını belirler.",
     'scenario': "Gelmeme (no-show) oranını düşürmek, görüşme sonrası takibi düzenli yapmak ve kayıt / not süreçlerinin KVKK'ya uygun olması isteniyorsa.",
     'example': "Görüşmeden 24 saat ve 1 saat önce e-posta / SMS hatırlatması; görüşme sonrası danışman panelinde \"Özel not (yalnız siz görürsünüz)\" ve \"Müşteriyle paylaşılacak özet\" alanları ayrı; kayıt seçeneği kapalı.",
     'rule': "Hatırlatma, not ve kayıt: {labels}. Hatırlatmalar müşterinin saat dilimine göre ve işlemsel bildirim olarak gönderilir; danışmanın özel notu ile müşteriyle paylaşılan özet ayrı kayıt türüdür; görüşme notları ve kayıtlar yalnız ilgili danışman ve yetkili roller tarafından görülür, şifreli depolanır, uygulama loglarına ve CRM'in genel alanlarına yazılmaz; saklama süresi sonunda silinir.",
     'options': [
         o('reminders', 'Randevu hatırlatmaları (önerilen)', "Görüşmeden önce (ör. 24 saat ve 1 saat) e-posta / SMS / anlık bildirim hatırlatması.", "Bütün randevulu hizmetler.", "\"Yarın 14:00'te Ayşe K. ile görüşmeniz var — Görüşmeye katıl\" SMS'i.",
           "Hatırlatma zamanları panelden ayarlanır; hatırlatmalar kuyrukla gönderilir, iptal ya da yeniden planlanan randevunun bekleyen hatırlatmaları silinir."),
         o('ics', 'Takvim daveti (.ics)', "Onay e-postasında takvime eklenebilir davet; değişiklik ve iptalde güncel davet.", "Müşteri ve danışmanın kendi takvimini kullandığı her durum.", "Onay e-postasındaki \"Takvime ekle\" ekiyle randevu müşterinin telefon takvimine düşer.",
           "Davet RFC 5545 biçiminde, saat dilimi bilgisi ve sabit UID ile üretilir; yeniden planlamada SEQUENCE artırılarak güncelleme, iptalde CANCEL iletisi gönderilir."),
         o('notes', 'Danışman notu ve müşteriye özet', "Görüşme sonrası danışmanın özel notu ve isteğe bağlı müşteriyle paylaşılan özet / ödev.", "Takip gerektiren danışmanlık.", "Müşteri panelinde \"Görüşme özeti ve bir sonraki adımlar\" bölümü; danışmanın özel notu müşteriye görünmez.",
           "Özel not ve paylaşılan özet ayrı alanlarda tutulur; özel not şifreli saklanır ve yalnız yazan danışman ile yetkili klinik / hizmet sorumlusu erişir; her erişim kaydedilir."),
         o('followup', 'Görüşme sonrası takip ve CRM', "Görüşme sonucu, takip görevi ve satış fırsatının CRM'e yazılması.", "Görüşmeden paket ya da hizmet satışı çıkıyorsa.", "Ücretsiz ön görüşmeden sonra danışman \"5 seanslık paket önerildi\" sonucunu girer, CRM'de fırsat açılır.",
           "CRM'e yalnız sonuç, takip tarihi ve satış bilgisi aktarılır; görüşme içeriği ve özel notlar aktarılmaz."),
         o('no_show', 'Gelmeme (no-show) işaretleme', "Görüşmeye katılmayan müşterinin işaretlenmesi ve kuralın uygulanması.", "No-show oranının izlenmesi ve iptal kuralının uygulanması isteniyorsa.", "Danışman 15 dakika bekledikten sonra \"Katılmadı\" işaretler; paket hakkı kurala göre düşer.",
           "No-show işaretleme görüşme başlangıcından sonra açılır, işaretleyen ve zaman kaydedilir; müşteriye bildirim gider ve itiraz yolu sunulur."),
         o('recording_consent', 'Görüşme kaydı yalnız açık izinle', "Görüşmenin kaydı varsayılan olarak kapalıdır; yalnız müşterinin ayrıca verdiği izinle ve belirli amaçla açılır.", "Eğitim, kalite ya da müşterinin talebiyle kayıt gerekiyorsa.", "Görüşme başında \"Bu görüşmenin kaydedilmesine izin veriyor musunuz?\" sorusu; izin yoksa kayıt düğmesi pasif.",
           "Kayıt yalnız görüşme öncesi ayrıca alınan ve geri alınabilen izinle başlatılır; izin metni, sürüm ve zaman kaydedilir; kayıt şifreli, erişimi kısıtlı depolamada tutulur ve saklama süresi sonunda silinir; görüşme kaydının hukuki dayanağı (açık rıza ya da başka bir şart, özel nitelikli veri olup olmadığı) hukuk birimince belirlenir."),
         o('no_recording', 'Görüşmeler hiç kaydedilmez', "Hiçbir görüşme kaydedilmez; platformdaki kayıt özelliği kapatılır.", "Terapi, sağlık, hukuk gibi hassas danışmanlıklar ya da kayıt ihtiyacı yoksa.", "Görüşme ekranında kayıt düğmesi bulunmaz; hizmet sayfasında \"Görüşmeler kaydedilmez\" bilgisi.",
           "Görüntülü görüşme platformunda bulut ve yerel kayıt kapatılarak toplantı oluşturulur; kayıt yapılmadığı hizmet sayfasında ve aydınlatma metninde belirtilir.", exclusive=True),
     ]},
]

PART = {
    'sections': [S_CRM, S_TK, S_SV, S_SUB, S_CS],
    'fields': F_CRM + F_TK + F_SV + F_SUB + F_CS,
    'fields_into': [],
    'option_add': OPTION_ADD,
    'guide_add': {},
}
