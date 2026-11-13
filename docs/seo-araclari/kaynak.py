# -*- coding: utf-8 -*-
"""Pazarlama › SEO Araçları (2026-11-13, kullanıcı isteği: "3. Pazarlama menüsü altına Semrush, Ahrefs (ve varsa benzer
programlar) ile ilgili maddeleri ekleyelim"). Veri burada yazılır; yanına seo-araclari.json üretilir, uygulamaya
seo_araclari_ekle.py işler:
  python3 -I docs/seo-araclari/kaynak.py
  python3 -I docs/seo-araclari/seo_araclari_ekle.py web-proje-gelistirme.html docs/seo-araclari/seo-araclari.json

Kaynak adresleri ve araç bilgileri 2026-11-13'te sağlayıcıların resmî sayfaları açılarak doğrulandı (iki araştırma ajanı +
curl). Fiyat yazılmaz (sık değişir); plan adı yalnız özelliğin bir plana bağlı olduğu yerde anılır ve "planınızda kontrol
edin" notuyla verilir. Kişisel ya da şirkete özgü değer yazılmaz."""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
GROUP = 'SEO Araçları'

# --- sorumlu pozisyon ajanları (docs/ajan-kaydi/AGENT_REGISTRY.json'da denetlenir)
P = 'poz:pazarlama:'
SEO = P + 'digital_demand_generation/seo-ve-geo-muduru'
SEOY = SEO + '/seo-yoneticisi'
TSEO = SEO + '/teknik-seo-uzmani'
ISEO = SEO + '/icerik-seo-uzmani'
AIV = SEO + '/ai-arama-gorunurlugu-uzmani'
OLC = P + 'digital_demand_generation/web-pazarlama-muduru/dijital-olcumleme-uzmani'
REK = P + 'market_research_analytics/rekabet-ve-sektor-istihbarati-muduru/rekabet-analisti'
MT = P + 'marketing_operations_crm_martech/martech-ve-entegrasyon-muduru/pazarlama-teknolojileri-uzmani'
BI = P + 'marketing_operations_crm_martech/pazarlama-verisi-ve-raporlama-muduru/bi-ve-dashboard-uzmani'
TED = P + 'marketing_operations_crm_martech/butce-ve-tedarikci-yonetimi-muduru/tedarikci-yonetimi-uzmani'
DEVOPS = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/kidemli-devops-muhendisi'


def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    if exclusive:
        x['exclusive'] = True
    return x


def R(t, u, n):
    return {'title': t, 'url': u, 'note': n}


TOOLS = ['ahrefs', 'awt', 'semrush', 'seranking', 'similarweb', 'moz', 'sistrix', 'majestic', 'screamingfrog', 'ubersuggest', 'mangools', 'serpstat']
SUITE = ['ahrefs', 'awt', 'semrush', 'seranking', 'moz', 'sistrix', 'ubersuggest', 'mangools', 'serpstat']   # proje kurulan paketler
GATE = [{'field': 'mk_st_tools', 'in': TOOLS}]
GATE_SUITE = [{'field': 'mk_st_tools', 'in': SUITE}]
GATE_CRAWL = [{'field': 'mk_st_tools', 'in': ['ahrefs', 'awt', 'semrush', 'seranking', 'moz', 'sistrix', 'ubersuggest', 'serpstat', 'screamingfrog']}]
GATE_RANK = [{'field': 'mk_st_tools', 'in': ['ahrefs', 'semrush', 'seranking', 'moz', 'sistrix', 'ubersuggest', 'mangools', 'serpstat']}]
GATE_RES = [{'field': 'mk_st_tools', 'in': [t for t in TOOLS if t != 'screamingfrog']}]

sections, fields = [], []

# ============================================================== 1. Araç seçimi & hesaplar
sections.append({
    'id': 'mk_st_scope', 'after': 'mk_measure', 'area': 'marketing', 'group': GROUP, 'icon': '⌕',
    'name': 'Araç Seçimi & Hesap Yönetimi', 'en': 'SEO Tools: Selection & Accounts',
    'desc': 'Ahrefs, Semrush ve benzeri SEO araçlarından hangilerinin kullanılacağı, hesapların kime ait olacağı ve erişim kuralları.',
    'refs': ['mk_brand_name', 'domain_name'],
    'guide': {
        'purpose': 'SEO araçları (Ahrefs, Semrush, SE Ranking, Similarweb, Moz, Sistrix, Majestic, Screaming Frog) anahtar kelime, rakip, backlink, sıralama ve teknik tarama verisi sağlar. Bu bölüm hangi aracın ne için kullanılacağını, hesabın şirkete ait olmasını ve erişimin kontrollü verilmesini kararlaştırır. Araçların trafik, hacim ve backlink sayıları kendi veri tabanlarına dayanan tahminlerdir; sitenin gerçek verisi Google Search Console ve GA4\'tedir (5. Google menüsü).',
        'criteria': [
            'Her aracın kullanım amacı yazılıdır (teknik tarama, sıralama takibi, rakip, backlink); aynı iş için iki ücretli araç alınmaz.',
            'Hesaplar şirket adına, kurumsal e-posta ile açılır; plan sahibi ve yenileme tarihi kayıtlıdır.',
            'Her kullanıcı kendi koltuğuyla girer; ortak şifre yoktur, iki adımlı doğrulama açıktır.',
            'Ayrılan çalışanın ve biten ajans sözleşmesinin erişimi aynı gün kaldırılır.',
            'API / MCP birim kotası izlenir; aylık kullanım sınırı belirlenmiştir.',
            'Raporlarda aracın verisi "tahmin" etiketiyle, Search Console verisinden ayrı verilir.',
        ],
        'pitfalls': [
            'Ajansın ya da serbest çalışanın kişisel hesabında kurulan proje, iş bitince geçmiş verisiyle birlikte kaybolur.',
            'Aracın "organik trafik" tahmini sitenin gerçek trafiği sanılıp hedef ve bütçe buna göre konur.',
            'Ücretsiz Ahrefs Webmaster Tools ve Search Console yeterliyken ücretli plan alınır.',
            'Koltuk sayısı ortak şifreyle aşılır; sağlayıcının kullanım koşulları çiğnenir ve hesap kilitlenebilir.',
            'API / MCP anahtarı koda, dokümana ya da sohbet geçmişine yazılır.',
            'Plan yenileme tarihi takip edilmez; sıralama geçmişi ve proje ayarları plan düşünce kaybolur.',
        ],
        'resources': [],   # aşağıda RES ile doldurulur
    }})

fields.append({
    'id': 'mk_st_tools', 'section': 'mk_st_scope', 'label': 'Kullanılacak SEO Araçları', 'en': 'SEO Tools', 'type': 'multiselect',
    'explanation': 'Projede kullanılacak SEO araçları. Seçtiğiniz araçlara göre bu gruptaki proje kurulumu, tarama, sıralama takibi, analiz ve raporlama kararları açılır.',
    'scenario': 'Rakip, anahtar kelime ve backlink verisi ya da düzenli teknik tarama gerekiyorsa en az bir araç seçin; yalnız kendi sitenizin verisi yetiyorsa Search Console ile ücretsiz Ahrefs Webmaster Tools çoğu zaman yeterlidir.',
    'example': 'Bir hizmet firması rakip ve anahtar kelime için Semrush, kendi sitesinin teknik taraması için ücretsiz Ahrefs Webmaster Tools seçer; panelde iki aracın görev ayrımı yazılıdır.',
    'rule': 'Kullanılacak SEO araçları: {labels}. Her aracın kullanım amacı (teknik tarama, sıralama, rakip, backlink, pazar) yazılıdır; aynı iş için iki ücretli araç kullanılmaz. Araçların trafik, arama hacmi, zorluk ve backlink sayıları sağlayıcının tahminidir; Google Search Console ve GA4 verisinin yerine geçmez ve raporlarda kaynağıyla birlikte verilir.',
    'agents': [SEO, TED],
    'recommend': [
        {'field': 'mk_comp_method', 'map': {'tool': ['semrush', 'similarweb']}},
        {'field': 'au_access', 'map': {'links': ['ahrefs', 'semrush'], 'crawl': ['screamingfrog']}},
    ],
    'options': [
        o('ahrefs', 'Ahrefs', 'Backlink veri tabanı güçlü, Site Explorer, Keywords Explorer, Site Audit, Rank Tracker ve Brand Radar (yapay zekâ görünürlüğü) içeren ücretli SEO paketi.',
          'Backlink ve rakip içerik analizi öncelikliyse, içerik ve bağlantı fırsatı düzenli aranacaksa.',
          'SEO ekibi rakiplerin en çok bağlantı alan sayfalarını Ahrefs\'te çıkarır, içerik planına üç yeni konu ekler.',
          'Ahrefs projesi şirket hesabında açılır; site Search Console bağlantısıyla doğrulanır (doğrulanmış proje ücretsiz ek tarama ve Site Explorer kredisi alır). Ahrefs\'in tahmini trafik ve hacim verisi "Ahrefs tahmini" etiketiyle raporlanır.'),
        o('awt', 'Ahrefs Webmaster Tools (ücretsiz)', 'Ahrefs\'in doğrulanmış site sahiplerine ücretsiz sunduğu sürüm: Site Audit (aylık proje başına 5.000 tarama kredisi), kendi siteniz için Site Explorer ve Web Analytics.',
          'Bütçe sınırlıysa ya da yalnız kendi sitenizin teknik taraması ve backlink görünümü gerekiyorsa; rakip verisi gerekmiyorsa.',
          'Küçük bir klinik sitesi Search Console bağlantısıyla Ahrefs Webmaster Tools\'u açar; her pazartesi otomatik tarama raporu e-postayla gelir.',
          'Ahrefs Webmaster Tools yalnız doğrulanmış site için kullanılır (Search Console bağlantısı, DNS TXT, HTML dosyası ya da meta etiket); rakip analizi bu sürümde yapılmaz, gerekirse ücretli araç ayrıca kararlaştırılır.'),
        o('semrush', 'Semrush', 'Anahtar kelime ve rakip araştırması, Site Audit, Position Tracking, Backlink Audit, yerel SEO ve AI Visibility Toolkit içeren ücretli pazarlama paketi; Google Ads ve İşletme Profili bağlantıları var.',
          'Anahtar kelime, reklam ve rakip araştırması birlikte yapılacaksa; günlük sıralama takibi ve yerel SEO gerekiyorsa.',
          'Pazarlama ekibi Semrush Keyword Gap ile üç rakibin sıralanıp kendisinin sıralanmadığı 120 sorguyu bulur, içerik takvimine işler.',
          'Semrush projesi şirket hesabında açılır; proje alan adı araç kurulduktan sonra değiştirilemediği için alan adı (www dahil) Ortak Bilgiler › Canlı Site Adresi\'yle aynı yazılır. Semrush\'ın trafik ve hacim verisi "Semrush tahmini" etiketiyle raporlanır.'),
        o('seranking', 'SE Ranking', 'Sıralama takibi, site denetimi, anahtar kelime ve rakip araştırması sunan, daha düşük bütçeli SEO paketi.',
          'Ahrefs ya da Semrush bütçesi yoksa, ajans olarak çok sayıda müşteri projesi yönetilecekse.',
          'Bir ajans 15 müşterinin anahtar kelimelerini SE Ranking\'de izler, her müşteriye aylık beyaz etiketli rapor gönderir.',
          'SE Ranking projesi şirket ya da ajans hesabında, müşteriye erişim verilecek şekilde açılır; tahmini veriler kaynağıyla raporlanır.'),
        o('similarweb', 'Similarweb', 'Sitelerin trafik kaynakları, ziyaretçi davranışı ve pazar payı tahminlerini veren pazar istihbaratı aracı; teknik SEO aracı değildir.',
          'Rakiplerin trafik kanallarını (organik, ücretli, sosyal, yönlendirme) ve pazar payını karşılaştırmak gerekiyorsa.',
          'Pazarlama müdürü üç rakibin trafiğinin yüzde kaçının sosyal medyadan geldiğini Similarweb\'de görür, kanal bütçesini gözden geçirir.',
          'Similarweb verisi panel ve modellerden türetilmiş tahmindir; yalnız rakip ve pazar karşılaştırmasında kullanılır, sitenin kendi trafiği için GA4 esas alınır.'),
        o('moz', 'Moz Pro', 'Anahtar kelime araştırması, site taraması (rogerbot), sıralama takibi ve Domain Authority metriği sunan SEO paketi. Moz Local yalnız ABD, Birleşik Krallık ve Kanada\'da çalışır; Türkiye\'deki işletme listelemesi için kullanılamaz.',
          'Ekip Moz metriklerine (Domain Authority) ve bağlantı veri tabanına alışkınsa.',
          'SEO uzmanı bağlantı fırsatlarını Moz\'un Domain Authority değerine göre sıralar.',
          'Moz projesi şirket hesabında açılır; Domain Authority Moz\'a özgü bir tahmindir, Google sıralama faktörü olarak sunulmaz.'),
        o('sistrix', 'Sistrix', 'Ülke bazlı görünürlük endeksi (Türkiye dahil 40 ülke; google.com.tr için mobil ve masaüstü günlük), sıralama takibi ve site denetimi (Optimizer) sunan SEO aracı.',
          'Görünürlüğün haftalık endeksle izlenmesi ve Google güncellemelerinin etkisinin görülmesi isteniyorsa.',
          'SEO yöneticisi bir Google çekirdek güncellemesinden sonra Sistrix görünürlük endeksindeki düşüşü raporlar.',
          'Sistrix görünürlük endeksi aracın kendi anahtar kelime kümesine dayanan bir göstergedir; trafikle karıştırılmaz.'),
        o('majestic', 'Majestic', 'Yalnız backlink verisine odaklanan araç; Trust Flow ve Citation Flow metrikleri.',
          'Backlink profili ve bağlantı kalitesi derinlemesine incelenecekse, ana pakete ek veri gerekiyorsa.',
          'Bir e-ticaret sitesi bağlantı kampanyası öncesi aday sitelerin Trust Flow değerini Majestic\'te kontrol eder.',
          'Majestic metrikleri Majestic\'e özgüdür; bağlantı kararında tek başına kullanılmaz, sayfanın konusu ve trafiğiyle birlikte değerlendirilir.'),
        o('screamingfrog', 'Screaming Frog SEO Spider', 'Bilgisayara kurulan masaüstü tarayıcı; siteyi tarayıp başlık, meta, yönlendirme, kırık bağlantı, canonical ve yapısal veri sorunlarını listeler. Ücretsiz sürüm taramada en çok 500 adresle ve sınırlı ayarla çalışır; Search Console, GA4 ve PageSpeed bağlantıları lisanslı sürümdedir.',
          'Yayın öncesi ya da büyük değişiklik sonrası ayrıntılı teknik tarama gerekiyorsa; hazırlık (staging) sitesi taranacaksa.',
          'Teknik SEO uzmanı yayından önce hazırlık sitesini Screaming Frog ile tarar, 34 kırık iç bağlantıyı yazılım ekibine iletir.',
          'Screaming Frog taraması sunucuyu yormayacak hızda yapılır; hazırlık sitesi taranırken kimlik bilgileri araca girilir, dışa aktarılan tarama dosyaları kişisel veri içeriyorsa paylaşılmaz.'),
        o('ubersuggest', 'Ubersuggest', 'Anahtar kelime araştırması, site denetimi, sıralama takibi ve yapay zekâ görünürlüğü sunan, sınırlı ücretsiz kullanımı olan düşük bütçeli araç.',
          'Küçük işletme ya da başlangıç bütçesinde temel anahtar kelime ve sıralama verisi gerekiyorsa.',
          'Bir kuaför salonu Ubersuggest\'te hizmet sorgularının hacmine bakıp blog konularını seçer.',
          'Ubersuggest verisi tahmindir; Türkçe sorgularda hacim Search Console ve Google Ads Anahtar Kelime Planlayıcı ile karşılaştırılır.'),
        o('mangools', 'Mangools (KWFinder, SERPWatcher)', 'Anahtar kelime (KWFinder), SERP analizi, sıralama takibi (SERPWatcher), backlink (LinkMiner) ve yapay zekâ arama takibi araçlarından oluşan paket; sınırlı ücretsiz hesap var.',
          'Kullanımı kolay, anahtar kelime odaklı bir araç isteniyorsa.',
          'İçerik uzmanı KWFinder\'da düşük zorluklu uzun kuyruk sorguları bulur.',
          'Mangools verisi tahmindir; sıralama takibi SERPWatcher\'da hedef konum ve cihazla kurulur.'),
        o('serpstat', 'Serpstat', 'Anahtar kelime, site analizi, sıralama takibi, site denetimi ve backlink araçları sunan SEO paketi.',
          'Ahrefs / Semrush\'a göre daha düşük bütçeyle geniş araç seti isteniyorsa.',
          'Bir ajans Serpstat\'ta müşterinin rakip sorgularını çıkarır ve denetim raporu hazırlar.',
          'Serpstat verisi tahmindir; projeler şirket ya da ajans hesabında, devredilebilir şekilde açılır.'),
        o('none', 'Harici SEO aracı kullanılmayacak', 'Yalnız Google Search Console, GA4 ve Bing Webmaster Tools kullanılır.',
          'Küçük ve yeni bir sitede ya da bütçe yokken; ölçüm Google ve Bing araçlarıyla yapılır.',
          'Yeni açılan bir kafe sitesi yalnız Search Console ve İşletme Profili istatistiklerini izler.',
          'Harici SEO aracı kullanılmaz; anahtar kelime ve sıralama verisi Search Console\'dan, teknik denetim 4. SEO Denetimi menüsündeki süreçle yapılır.', exclusive=True),
    ]})

fields.append({
    'id': 'mk_st_primary', 'section': 'mk_st_scope', 'label': 'Raporlamada Esas Alınacak Araç', 'en': 'Primary SEO Tool', 'type': 'select',
    'explanation': 'Sıralama, görünürlük ve rakip karşılaştırmasında tek doğru kaynak sayılacak araç. Farklı araçlar aynı sorgu için farklı sıra ve hacim gösterir; raporlar tek araca dayanır.',
    'scenario': 'Birden çok araç seçildiyse mutlaka belirleyin; aksi hâlde aylık raporlarda sayılar kaynağa göre değişir.',
    'example': 'Semrush esas alınır; Ahrefs Webmaster Tools yalnız teknik tarama için kullanılır. Aylık raporda sıralama grafiği Semrush\'tan gelir.',
    'rule': 'Raporlamada esas alınacak SEO aracı: {label}. Sıralama, görünürlük ve rakip karşılaştırması bu araçtan alınır; başka araçlardan gelen sayı raporda aracın adıyla ayrıca belirtilir, iki aracın sayısı aynı grafikte karıştırılmaz.',
    'agents': [SEOY, OLC],
    'showIf': GATE_SUITE,
    'options': [
        o('ahrefs', 'Ahrefs', 'Sıralama ve görünürlük Ahrefs Rank Tracker ve Site Explorer\'dan alınır.', 'Ahrefs ana araçsa.', 'Aylık raporun sıralama ve backlink grafikleri Ahrefs\'ten dışa aktarılır.'),
        o('semrush', 'Semrush', 'Sıralama ve görünürlük Semrush Position Tracking ve Domain Overview\'dan alınır.', 'Semrush ana araçsa.', 'Aylık raporun görünürlük yüzdesi Semrush Position Tracking\'den gelir.'),
        o('seranking', 'SE Ranking', 'Sıralama SE Ranking\'den alınır.', 'SE Ranking ana araçsa.', 'Müşteri raporu SE Ranking\'in rapor oluşturucusundan çıkar.'),
        o('moz', 'Moz Pro', 'Sıralama Moz Pro\'dan alınır.', 'Moz ana araçsa.', 'Rapordaki sıralama tablosu Moz Pro kampanyasından gelir.'),
        o('sistrix', 'Sistrix', 'Görünürlük Sistrix endeksinden alınır.', 'Sistrix ana araçsa.', 'Rapordaki görünürlük eğrisi Sistrix\'ten gelir.'),
        o('other', 'Seçilen diğer araç (Ubersuggest, Mangools, Serpstat)', 'Sıralama seçilen diğer araçtan alınır; araç adı raporda yazılır.', 'Ana araç Ubersuggest, Mangools ya da Serpstat ise.', 'Rapordaki sıralama tablosu Serpstat\'tan gelir ve başlıkta araç adı yazılır.'),
        o('gsc', 'Search Console (araçlar yardımcı)', 'Ortalama konum ve tıklama Search Console\'dan; araçlar yalnız rakip ve fırsat için.', 'Gerçek veriye dayanmak isteniyorsa ya da yalnız ücretsiz Ahrefs Webmaster Tools varsa.', 'Raporun ana grafiği Search Console tıklamasıdır; araç verisi ekte "tahmin" olarak durur.'),
    ]})

fields.append({
    'id': 'mk_st_owner', 'section': 'mk_st_scope', 'label': 'Hesap Sahipliği', 'en': 'Account Ownership', 'type': 'select',
    'explanation': 'SEO aracı hesabının ve projelerin kime ait olacağı. Sıralama geçmişi, tarama geçmişi ve proje ayarları hesabın sahibinde kalır.',
    'scenario': 'Ajans ya da serbest çalışanla çalışılıyorsa özellikle önemlidir; iş bitince geçmiş verinin şirkette kalması gerekir.',
    'example': 'Hesap şirketin pazarlama@ adresine açılır, ajansın uzmanları kullanıcı olarak eklenir; sözleşme bitince yalnız kullanıcıları kaldırılır.',
    'rule': 'SEO aracı hesap sahipliği: {label}.',
    'agents': [TED, SEO],
    'showIf': GATE,
    'options': [
        o('company', 'Şirket hesabı, kurumsal e-posta (önerilen)', 'Hesap şirket adına ve kişiye bağlı olmayan kurumsal e-postayla açılır; faturayı şirket öder.', 'Her durumda önerilir.', 'Hesabın sahibi pazarlama@ortak adresi; çalışanlar ve ajans kullanıcı olarak girer.',
          'Hesap şirket adına, kişiye bağlı olmayan kurumsal e-postayla açılır; fatura şirkettedir, sahip (Owner) yetkisi en az iki yöneticide tanımlıdır.'),
        o('agency', 'Ajans hesabı, şirkete erişim verilir', 'Ajans kendi hesabında proje açar, şirkete görüntüleme ya da düzenleme erişimi verir.', 'Ajans aracı zaten kullanıyorsa ve şirket ayrı lisans almayacaksa.', 'Ajans Semrush projesini şirketin kullanıcısıyla paylaşır; aylık raporlar ortak projeden çıkar.',
          'Ajans hesabındaki projeye şirkete paylaşım verilir; sözleşmede sözleşme bitiminde proje verisinin (sıralama geçmişi, anahtar kelime listesi, tarama raporları) dışa aktarılıp şirkete teslim edileceği yazılır.'),
        o('personal', 'Kişisel hesap (önerilmez)', 'Bir çalışanın ya da serbest çalışanın kişisel hesabı kullanılır.', 'Yalnız kısa süreli denemede.', 'Uzman kendi hesabında deneme projesi açar; iki hafta sonra şirket hesabına taşınır.',
          'Kişisel hesap yalnız deneme için kullanılır; kalıcı proje şirket hesabına taşınır, kişisel hesapta şirket verisi bırakılmaz.'),
    ]})

fields.append({
    'id': 'mk_st_access', 'section': 'mk_st_scope', 'label': 'Erişim, Koltuk ve Kota Kuralları', 'en': 'Access, Seats & Quotas', 'type': 'multiselect',
    'explanation': 'SEO araçlarına kimin, hangi rolle eriştiği ve API / MCP birim kotasının nasıl kontrol edildiği.',
    'scenario': 'Aracı birden çok kişi ya da ajans kullanıyorsa; API veya Claude bağlantısı (MCP) kullanılacaksa.',
    'example': 'Herkes kendi koltuğuyla girer, iki adımlı doğrulama zorunludur; her üç ayda bir kullanıcı listesi gözden geçirilir.',
    'rule': 'SEO aracı erişim kuralları: {labels}.',
    'agents': [MT, TED],
    'showIf': GATE,
    'options': [
        o('seats', 'Herkes kendi koltuğuyla girer, ortak şifre yok', 'Her kullanıcıya ayrı koltuk açılır.', 'Her ekipte.', 'Ajansın iki uzmanı için iki ayrı kullanıcı eklenir.',
          'Her kullanıcı kendi koltuğuyla girer; ortak şifre kullanılmaz (sağlayıcıların kullanım koşulları da hesap paylaşımını sınırlar).'),
        o('roles', 'En az yetkili rol', 'Rapor okuyanlar görüntüleme, proje kuranlar düzenleme rolü alır; sahip / yönetici rolü sınırlı tutulur.', 'Birden çok kullanıcı varsa.', 'Yönetim kurulu üyesi yalnız görüntüleme paylaşımıyla raporu görür.',
          'Kullanıcılar en az yetkili rolle eklenir (Ahrefs: Owner / Admin / Member, Semrush: Owner / Admin / User / Guest ve görüntüleme paylaşımı); sahip rolü en az iki yöneticidedir.'),
        o('mfa', 'İki adımlı doğrulama zorunlu', 'Hesaplarda iki adımlı doğrulama (2FA) açılır; destekleniyorsa kurumsal tekil oturum (SSO).', 'Her ekipte.', 'Ahrefs çalışma alanında yönetici 2FA\'yı herkes için zorunlu yapar.',
          'Bütün kullanıcılarda iki adımlı doğrulama açılır; plan destekliyorsa SAML SSO ile kurumsal kimlikten girilir.'),
        o('offboard', 'Ayrılanın erişimi aynı gün kaldırılır', 'Çalışan ayrıldığında ya da ajans sözleşmesi bittiğinde kullanıcısı silinir.', 'Her ekipte.', 'Sözleşmesi biten ajansın kullanıcıları son gün kaldırılır, API anahtarları yenilenir.',
          'Ayrılan çalışanın ve sözleşmesi biten ajansın erişimi aynı gün kaldırılır; onların oluşturduğu API / MCP anahtarları iptal edilip yenilenir.'),
        o('review', 'Üç ayda bir erişim gözden geçirmesi', 'Kullanıcı listesi, roller ve API anahtarları üç ayda bir kontrol edilir.', 'Birden çok kullanıcı ya da ajans varsa.', 'Her çeyrek başında kullanıcı listesi dışa aktarılıp onaylanır.',
          'Kullanıcılar, roller ve API / MCP anahtarları üç ayda bir gözden geçirilir; kullanılmayan koltuk ve anahtar kapatılır.'),
        o('billing', 'Plan, yenileme tarihi ve sahibi kayıtlı', 'Planın adı, yenileme tarihi ve faturadan sorumlu kişi kayıtlıdır.', 'Ücretli araç varsa.', 'Satın alma takviminde Semrush yenilemesinden 30 gün önce hatırlatma vardır.',
          'Araç planı, yenileme tarihi ve sorumlusu kayıtlıdır; yenilemeden önce kullanım gözden geçirilir. Plan düşürülürse kaybolacak proje ve sıralama geçmişi önceden dışa aktarılır.'),
        o('quota', 'API / MCP birim kotası izlenir', 'API ve MCP sorguları plan birimlerinden düşer; aylık üst sınır konur.', 'API ya da Claude bağlantısı (MCP) kullanılacaksa.', 'Ahrefs MCP anahtarına aylık birim sınırı konur; sınırın %80\'inde uyarı gelir.',
          'API ve MCP kullanımı plan birimlerinden düşer; anahtar başına aylık birim sınırı belirlenir, büyük raporlardan önce tahmini birim kontrol edilir.'),
    ]})

# ============================================================== 2. Proje kurulumu & doğrulama
sections.append({
    'id': 'mk_st_setup', 'after': 'mk_st_scope', 'area': 'marketing', 'group': GROUP, 'icon': '⊕',
    'name': 'Proje Kurulumu & Doğrulama', 'en': 'SEO Tools: Project Setup & Verification',
    'desc': 'SEO aracında projenin hangi alan adı kapsamıyla açılacağı, site sahipliğinin nasıl doğrulanacağı ve hangi Google hizmetlerine bağlanacağı.',
    'refs': ['domain_name', 'staging_url', 'mk_ids'],
    'guide': {
        'purpose': 'SEO aracında proje, sitenin aracın içindeki karşılığıdır: tarama, sıralama takibi ve raporlar projeye bağlıdır. Kapsam (alan adı, alt alan adları, klasör) yanlış seçilirse tarama eksik ya da fazla yapılır, sıralama yanlış adresle eşleşir. Ahrefs\'te site sahipliğinin doğrulanması ücretsiz ek kredi ve robots.txt\'yi aşma gibi seçenekler açar; Semrush\'ta proje için doğrulama gerekmez, yalnız engellenen sayfaları taramak için doğrulama dosyası kullanılır.',
        'criteria': [
            'Proje alan adı Ortak Bilgiler › Canlı Site Adresi\'yle (www dahil) aynıdır.',
            'Kapsam bilinçli seçilmiştir: blog ya da mağaza alt alan adındaysa kapsamdadır, hazırlık sitesi ayrıdır.',
            'Ahrefs projesi Search Console bağlantısıyla doğrulanmıştır.',
            'Search Console bağlantısı yalnız gereken mülke ve okuma amacıyla verilmiştir.',
            'Dil ya da ülke klasörleri ayrı izlenecekse ayrı proje veya etiketle ayrılmıştır.',
            'Bağlantılar ve doğrulama yöntemi devir belgesinde yazılıdır.',
        ],
        'pitfalls': [
            'Semrush\'ta araç kurulduktan sonra proje alan adı değiştirilemez; www / www\'suz yanlış yazım projenin baştan açılmasını gerektirir.',
            'Ahrefs\'te proje kapsamı Search Console mülküyle uyuşmazsa Search Console verisi gelmez.',
            'Hazırlık (staging) sitesi canlı projeye karışır, raporlar ikiye bölünür.',
            'Doğrulama için eklenen HTML dosyası ya da meta etiket bir sonraki yayında silinir, doğrulama düşer.',
            'Search Console\'a "sahip" yetkisi gereğinden fazla kişiye verilir.',
            'Proje ajansın hesabında doğrulanır; sözleşme bitince doğrulama ve geçmiş kaybolur.',
        ],
        'resources': [],
    }})

fields.append({
    'id': 'mk_st_domain', 'section': 'mk_st_setup', 'label': 'Proje Kapsamı', 'en': 'Project Scope', 'type': 'select',
    'explanation': 'SEO aracındaki projenin hangi adresleri kapsayacağı. Ahrefs\'te kapsam "tam adres / klasör / alan adı / alan adı ve alt alan adları"; Semrush\'ta Site Audit varsayılan olarak bütün alt alan adlarını tarar, Position Tracking alan adı, alt alan adı, klasör ya da tek adres izler.',
    'scenario': 'Blog, mağaza, destek merkezi ya da dil sürümleri ayrı alt alan adında veya klasördeyse doğru seçim raporların doğruluğunu belirler.',
    'example': 'Blog blog.ornek.com\'da olduğu için proje "alan adı ve alt alan adları" kapsamıyla açılır; hazırlık sitesi tarama dışı bırakılır.',
    'rule': 'SEO aracı proje kapsamı: {label}. Proje alan adı Ortak Bilgiler › Canlı Site Adresi\'yle (www ve https dahil) aynı yazılır; hazırlık (staging) sitesi canlı projeye dahil edilmez.',
    'agents': [TSEO],
    'showIf': GATE_SUITE,
    'options': [
        o('subdomains', 'Alan adı ve bütün alt alan adları (önerilen)', 'Ana alan adı ve blog., magaza., destek. gibi bütün alt alan adları.', 'Sitenin parçaları farklı alt alan adlarındaysa.', 'ornek.com, www.ornek.com ve blog.ornek.com aynı projede.',
          'Proje alan adı ve bütün alt alan adlarını kapsar; hazırlık ve iç sistem alt alan adları (staging., panel., api.) tarama hariç listesine eklenir.'),
        o('domain', 'Yalnız ana alan adı', 'Yalnız www\'lu ya da www\'suz tek ana adres.', 'Site tek alan adında ve alt alan adı yoksa.', 'Proje yalnız www.ornek.com\'u kapsar.',
          'Proje yalnız ana alan adını kapsar; alt alan adı açılırsa kapsam yeniden değerlendirilir.'),
        o('folders', 'Dil / ülke klasörleri ayrı proje veya etiket', 'ornek.com/en/, ornek.com/de/ gibi klasörler ayrı izlenir.', 'Çok dilli ya da çok ülkeli sitede her pazarın performansı ayrı ölçülecekse.', '/en/ klasörü ayrı Ahrefs projesi, Semrush\'ta ayrı Position Tracking kampanyası olur.',
          'Her dil / ülke klasörü ayrı proje ya da ayrı sıralama takibi kampanyasıyla, kendi ülke ve dil ayarlarıyla izlenir; ana proje bütün siteyi taramaya devam eder.'),
        o('folder', 'Tek bölüm (klasör)', 'Projenin yalnız bir bölümü, ör. /blog/.', 'Yalnız belirli bir bölümden sorumluysanız (ör. içerik ajansı).', 'İçerik ajansının projesi yalnız ornek.com/blog/ adreslerini izler.',
          'Proje yalnız belirtilen klasörü kapsar; site geneli teknik denetim ayrıca sitenin sahibinde yapılır.'),
    ]})

fields.append({
    'id': 'mk_st_verify', 'section': 'mk_st_setup', 'label': 'Site Sahipliği Doğrulama', 'en': 'Ownership Verification', 'type': 'select',
    'explanation': 'Ahrefs (ve Ahrefs Webmaster Tools) siteyi doğrulamanızı ister; doğrulanmış projede ücretsiz ek tarama ve Site Explorer kredisi, robots.txt\'yi yok sayma ve daha hızlı tarama açılır. Yöntemler: Search Console bağlantısı, DNS TXT kaydı, kök dizine HTML dosyası, ana sayfaya meta etiket. Semrush projesi doğrulama istemez.',
    'scenario': 'Ahrefs ya da Ahrefs Webmaster Tools seçildiyse; Semrush\'ta yalnız güvenlik duvarının arkasındaki sayfalar taranacaksa doğrulama dosyası gerekir.',
    'example': 'Search Console\'da sahip yetkisi olan pazarlama yöneticisi Ahrefs\'te "GSC\'den içe aktar" der; site ve 16 aylık Search Console verisi tek adımda gelir.',
    'rule': 'SEO aracında site sahipliği doğrulama yöntemi: {label}.',
    'agents': [TSEO, DEVOPS],
    'showIf': [{'field': 'mk_st_tools', 'in': ['ahrefs', 'awt', 'semrush']}],
    'options': [
        o('gsc', 'Search Console bağlantısı (önerilen)', 'Search Console mülkü araca bağlanır; site doğrulanır ve Search Console verisi içe aktarılır.', 'Search Console mülkü varsa (5. Google menüsü).', 'Ahrefs\'te "Import from GSC" ile proje açılır.',
          'Doğrulama Search Console bağlantısıyla yapılır; bağlantıyı Search Console\'da sahip yetkisi olan şirket hesabı kurar, proje kapsamı Search Console mülküyle aynıdır.'),
        o('dns', 'DNS TXT kaydı', 'Aracın verdiği TXT kaydı alan adının DNS\'ine eklenir.', 'Search Console bağlantısı kurulamıyorsa ve DNS yönetimi elinizdeyse.', 'DNS panelinde "ahrefs-site-verification=…" TXT kaydı durur.',
          'Doğrulama DNS TXT kaydıyla yapılır; kayıt DNS değişiklik listesine "SEO aracı doğrulaması, silmeyin" notuyla yazılır.'),
        o('file', 'HTML dosyası / meta etiket', 'Kök dizine doğrulama dosyası ya da ana sayfaya meta etiket eklenir.', 'DNS erişimi yoksa.', 'Sitenin kökünde aracın verdiği .html dosyası durur.',
          'Doğrulama dosyası ya da meta etiket kaynak koda (ya da CMS ayarına) kalıcı olarak eklenir ve yayın sürecinde silinmez; şablon değişikliğinde kontrol edilir.'),
        o('none', 'Doğrulama yapılmayacak', 'Proje doğrulanmadan kullanılır.', 'Yalnız Semrush kullanılıyorsa (doğrulama gerekmez) ya da kısa denemede.', 'Semrush projesi doğrulamasız açılır.',
          'Site doğrulanmaz; Ahrefs\'te doğrulanmamış site dakikada en çok 30 adresle taranır ve robots.txt aşılamaz — bu sınırlar kabul edilir.'),
    ]})

fields.append({
    'id': 'mk_st_integrations', 'section': 'mk_st_setup', 'label': 'Bağlanacak Hizmetler', 'en': 'Integrations', 'type': 'multiselect',
    'explanation': 'SEO aracına bağlanacak Google hizmetleri ve bildirim kanalları. Semrush resmî olarak Google Analytics, Search Console, Google Ads, İşletme Profili ve Looker Studio ile bağlanır; Ahrefs Search Console ve Looker Studio ile.',
    'scenario': 'Araçtaki tahminleri gerçek veriyle karşılaştırmak ve raporları tek panelde toplamak istiyorsanız.',
    'example': 'Semrush\'ın Organic Traffic Insights raporu Search Console ve GA4\'ü bağlayarak gerçek tıklamayı aracın sıralamasıyla yan yana gösterir.',
    'rule': 'SEO aracına bağlanacak hizmetler: {labels}. Bağlantılar şirket hesabıyla, yalnız gereken mülke ve okuma amacıyla kurulur; bağlantıyı kuran kişi ve tarih devir belgesine yazılır.',
    'agents': [OLC, MT],
    'showIf': GATE_SUITE,
    'options': [
        o('gsc', 'Google Search Console', 'Gerçek tıklama, gösterim ve sorgu verisi araca gelir.', 'Search Console mülkü varsa — çoğu sitede önerilir.', 'Ahrefs projesinde Search Console sekmesi 16 aylık veriyi gösterir.',
          'Search Console araca okuma amacıyla bağlanır; araç raporlarında Search Console verisi "gerçek veri" olarak tahminlerden ayrı gösterilir.'),
        o('ga4', 'Google Analytics 4', 'Organik trafiğin oturum, etkileşim ve dönüşüm verisi araca gelir (Semrush Organic Traffic Insights).', 'Semrush kullanılıyorsa ve organik trafiğin dönüşümü sayfa bazında görülecekse.', 'Semrush\'ta hangi açılış sayfasının dönüşüm getirdiği sorguyla birlikte görünür.',
          'GA4 araca yalnız okuma yetkili bir kullanıcıyla bağlanır; bağlantı GA4\'te kullanıcı listesinde görünür ve erişim gözden geçirmesine dahildir.'),
        o('gbp', 'Google İşletme Profili', 'Yerel SEO için İşletme Profili araca bağlanır (Semrush yerel araçları).', 'Fiziksel işletme ve yerel arama önemliyse.', 'Semrush\'ta İşletme Profili yorumları ve yerel sıralama haritası izlenir.',
          'İşletme Profili yerel SEO aracına bağlanır; profil bilgisi Ortak Bilgiler\'deki ad, adres, telefon ve çalışma saatleriyle aynı tutulur.'),
        o('looker', 'Looker Studio (Data Studio) bağlayıcısı', 'Aracın verisi Looker Studio raporuna resmî bağlayıcıyla çekilir (planınızda olup olmadığını kontrol edin).', 'Raporlar Looker Studio\'da toplanıyorsa (5. Google › Data Studio).', 'Aylık SEO raporunda Search Console ve Semrush Position Tracking grafikleri aynı sayfada.',
          'Araç verisi Looker Studio\'ya sağlayıcının resmî bağlayıcısıyla çekilir; rapor sayfasında her grafiğin kaynağı yazılır.'),
        o('alerts', 'E-posta / ekip sohbeti bildirimleri', 'Sıralama düşüşü, yeni / kayıp backlink ve tarama hatası bildirimleri.', 'Sorunları rapor dönemini beklemeden görmek istiyorsanız.', 'Ahrefs kayıp backlink bildirimini haftalık e-postayla gönderir.',
          'Önemli değişiklikler (ilk 10\'dan düşen hedef sorgu, kayıp önemli backlink, tarama sağlık puanında düşüş) için bildirim kurulur; bildirim kişisel değil ekip adresine gider.'),
    ]})

# ============================================================== 3. Site denetimi (tarama)
sections.append({
    'id': 'mk_st_audit', 'after': 'mk_st_setup', 'area': 'marketing', 'group': GROUP, 'icon': '⟲',
    'name': 'Site Denetimi (Tarama) Ayarları', 'en': 'SEO Tools: Site Audit Crawl Settings',
    'desc': 'SEO aracının siteyi düzenli tarayıp teknik sorunları bulması için tarayıcı izinleri, tarama ayarları, sıklık ve bulguların iş akışı.',
    'refs': ['domain_name', 'staging_url'],
    'guide': {
        'purpose': 'SEO araçlarının Site Audit özelliği siteyi kendi tarayıcısıyla gezip kırık bağlantı, yönlendirme zinciri, eksik başlık, canonical ve hız sorunlarını listeler. Tarayıcı güvenlik duvarına (WAF) ya da CDN\'e takılırsa rapor boş veya yanlış çıkar; çok hızlı tarama sunucuyu yorar. Bu bölüm tarayıcıya hangi izinlerin verileceğini, taramanın nasıl ve ne sıklıkla yapılacağını ve bulguların kimin işine dönüşeceğini belirler. Yayına alınmış sitenin kapsamlı denetimi 4. SEO Denetimi menüsündeki süreçtir; burada aracın otomatik düzenli taraması kurulur.',
        'criteria': [
            'Aracın tarayıcısı WAF / CDN\'de kullanıcı aracısı ve resmî IP listesiyle izinlidir; bütün botlar için genel izin açılmamıştır.',
            'Tarama hızı sunucuyu yormayacak düzeydedir; yoğun saatler dışında zamanlanmıştır.',
            'JavaScript ile çizilen içerik varsa JavaScript işleme açıktır.',
            'Parametreli, filtreli ve sonsuz sayfalama adresleri hariç tutulmuştur.',
            'Kritik ve yüksek bulgular iş kaydına dönüşür, düzeltme sonrası yeniden taramayla doğrulanır.',
            'Tarama raporunun sağlık puanı eğilimi aylık izlenir.',
        ],
        'pitfalls': [
            'Cloudflare ya da başka bir WAF tarayıcıyı engeller; rapor "403" ve boş sayfalarla dolar.',
            'Tarayıcıyı geçirmek için bütün botlara izin açılır; kötü niyetli botlar da geçer.',
            'Cloudflare ücretsiz planda Bot Fight Mode açıkken atlama kuralı tarayıcıyı geçirmez; rapor yine boş çıkar.',
            'Tarayıcı yalnız kullanıcı aracısı adıyla izin alır; bu ad taklit edilebildiği için IP ya da doğrulanmış bot listesiyle eşleştirilmez.',
            'Hazırlık sitesi taranırken kimlik bilgileri paylaşımlı belgeye yazılır.',
            'Aracın her uyarısı hata sanılır; önemsiz uyarılarla ekip yorulur.',
            'Yalnız araç taraması yapılır, Search Console\'daki dizine ekleme raporu kontrol edilmez.',
        ],
        'resources': [],
    }})

fields.append({
    'id': 'mk_st_crawl', 'section': 'mk_st_audit', 'label': 'Tarama Ayarları', 'en': 'Crawl Settings', 'type': 'multiselect',
    'explanation': 'SEO aracının tarayıcısına verilecek izinler ve tarama ayarları. Tarayıcılar: Ahrefs Site Audit için AhrefsSiteAudit, Semrush Site Audit için SiteAuditBot; ikisi de robots.txt\'ye uyar.',
    'scenario': 'Aracın düzenli taraması kurulacaksa; sitede WAF / CDN, JavaScript ile çizilen içerik ya da parola korumalı hazırlık sitesi varsa.',
    'example': 'Cloudflare\'de "AhrefsSiteAudit" ve Ahrefs IP listesi için kural açılır; tarama gece 02:00\'de, sunucuyu yormayan hızda yapılır.',
    'rule': 'SEO aracı tarama ayarları: {labels}.',
    'agents': [TSEO, DEVOPS],
    'showIf': GATE_CRAWL,
    'options': [
        o('allowlist', 'Tarayıcı WAF / CDN\'de izinli (IP ve kullanıcı aracısıyla)', 'Aracın tarayıcısı güvenlik duvarında yalnız resmî IP listesi ya da doğrulanmış bot listesiyle eşleşerek geçer.', 'Sitede Cloudflare, Sucuri gibi WAF / CDN varsa — çoğu sitede.', 'Cloudflare\'de Ahrefs doğrulanmış iyi bot olarak geçer; Semrush Site Audit için 85.208.98.128/25 ağı 80 ve 443 portlarında izinlidir.',
          'Aracın tarayıcısı WAF / CDN\'de yalnız sağlayıcının resmî IP listesi ya da doğrulanmış bot listesiyle eşleşince izinlidir (kullanıcı aracısı adı tek başına yeterli sayılmaz, taklit edilebilir); bütün botlara genel izin açılmaz. Tarayıcı adları: Ahrefs AhrefsSiteAudit, Semrush SiteAuditBot, Moz rogerbot, Sistrix "SISTRIX Crawler"; Ahrefs IP listesi api.ahrefs.com\'daki JSON\'dan, Semrush Site Audit ağı Semrush yardım sayfasından güncel alınır. Cloudflare\'de atlama (Skip) kuralı ücretsiz plandaki Bot Fight Mode\'u atlamaz; bu durumda Bot Fight Mode ayarı ayrıca değerlendirilir.'),
        o('speed', 'Sunucuyu yormayan tarama hızı, gece saatinde', 'Tarama hızı düşük tutulur, trafiğin az olduğu saatte çalışır.', 'Paylaşımlı barındırma ya da yoğun trafikli sitede.', 'Semrush\'ta "2 saniyede 1 adres", Ahrefs\'te düşük hız ve 02:00 zamanlaması.',
          'Tarama hızı sunucu kapasitesine göre sınırlanır ve trafiğin en az olduğu saatte zamanlanır; tarama sırasında sunucu yanıt süresi izlenir, yükselirse hız düşürülür.'),
        o('js', 'JavaScript işleme açık', 'Sayfalar tarayıcıda olduğu gibi JavaScript çalıştırılarak taranır.', 'İçerik ya da bağlantılar JavaScript ile çiziliyorsa (SPA, istemci tarafı render).', 'Ahrefs\'te "Execute JavaScript" açılır; menü bağlantıları raporda görünür.',
          'JavaScript ile çizilen içerik için taramada JavaScript işleme açılır; JavaScript\'li ve JavaScript\'siz sonuç farkı (yalnız JavaScript ile görünen bağlantı ve içerik) ayrıca raporlanır.'),
        o('exclude', 'Parametreli ve sonsuz adresler hariç', 'Filtre, sıralama, oturum ve izleme parametreli adresler ile sonsuz sayfalama taramadan çıkarılır.', 'E-ticaret, filtreli liste ya da takvim sayfası varsa.', '?sort=, ?utm_ ve /etiket/ adresleri hariç tutma kuralıyla taranmaz.',
          'Filtre, sıralama, oturum ve izleme (utm_) parametreli adresler ile sonsuz sayfalama taramadan hariç tutulur; tarama kredisi ana sayfalara harcanır.'),
        o('sitemap', 'Site haritası başlangıç kaynağı', 'Tarama site haritasından da başlar; haritada olup bağlantı almayan sayfalar bulunur.', 'Site haritası varsa.', 'Rapor "haritada var, iç bağlantı yok" sayfalarını listeler.',
          'Tarama hem ana sayfadan hem site haritasından başlar; haritada olup iç bağlantı almayan ve bağlantı alıp haritada olmayan sayfalar raporlanır.'),
        o('mobile', 'Mobil kullanıcı aracısı', 'Tarama mobil tarayıcı kimliğiyle yapılır (Google mobil öncelikli dizine ekleme yapar).', 'Her sitede önerilir.', 'Semrush\'ta SiteAuditBot Mobile varsayılandır.',
          'Tarama mobil kullanıcı aracısıyla yapılır; masaüstü ile içerik farkı varsa ayrıca masaüstü taraması karşılaştırılır.'),
        o('staging', 'Hazırlık sitesi kimlik bilgisiyle ayrı taranır', 'Parola korumalı hazırlık sitesi yayından önce ayrı projede taranır.', 'Yayın öncesi kontrol yapılacaksa.', 'Hazırlık sitesi HTTP kimlik doğrulamasıyla taranır, canlı projeye karışmaz.',
          'Hazırlık sitesi ayrı projede, HTTP kimlik doğrulaması ya da aracın doğrulama dosyasıyla taranır; kimlik bilgileri yalnız aracın ayarında ve parola yöneticisinde durur, belgeye yazılmaz. Hazırlık sitesi arama motorlarına kapalı kalır (noindex / kimlik doğrulama).'),
    ]})

fields.append({
    'id': 'mk_st_audit_freq', 'section': 'mk_st_audit', 'label': 'Otomatik Tarama Sıklığı', 'en': 'Audit Frequency', 'type': 'select',
    'explanation': 'Aracın siteyi ne sıklıkla otomatik tarayacağı. Semrush haftalık (gün seçilir), günlük ya da tek seferlik zamanlama sunar; Ahrefs gün, saat ve saat dilimiyle zamanlanır.',
    'scenario': 'Sık içerik yayımlanan ya da sık kod yayını yapılan sitede daha sık tarama gerekir.',
    'example': 'Tarama her pazartesi 02:00\'de çalışır; SEO uzmanı salı sabahı sağlık puanını kontrol eder.',
    'rule': 'SEO aracının otomatik tarama sıklığı: {label}. Her taramadan sonra sağlık puanı ve yeni çıkan kritik / yüksek bulgular kontrol edilir.',
    'agents': [TSEO],
    'showIf': GATE_CRAWL,
    'options': [
        o('weekly', 'Haftalık (önerilen)', 'Her hafta belirli gün ve saatte.', 'Çoğu kurumsal ve içerik sitesinde.', 'Her pazartesi 02:00.', 'Tarama haftada bir, trafiğin az olduğu saatte çalışır.'),
        o('daily', 'Günlük', 'Her gün.', 'Çok sık yayın yapılan büyük e-ticaret ya da haber sitesinde (tarama kredisini kontrol edin).', 'Her gece 03:00.', 'Tarama her gün çalışır; tarama kredisi tüketimi aylık izlenir.'),
        o('monthly', 'Aylık', 'Ayda bir.', 'Az değişen küçük sitede.', 'Her ayın ilk pazartesi.', 'Tarama ayda bir çalışır; büyük değişiklikten sonra ayrıca elle başlatılır.'),
        o('release', 'Her yayından sonra', 'Kod ya da şablon yayınından sonra elle ya da otomasyonla başlatılır.', 'Sık kod yayını yapılıyorsa, haftalık taramaya ek olarak.', 'Yayın hattı bittikten sonra Site Audit yeniden başlatılır.', 'Her kod / şablon yayınından sonra tarama başlatılır ve önceki taramayla karşılaştırılır.'),
    ]})

fields.append({
    'id': 'mk_st_audit_flow', 'section': 'mk_st_audit', 'label': 'Tarama Bulgularının İş Akışı', 'en': 'Audit Issue Workflow', 'type': 'multiselect',
    'explanation': 'Tarama raporundaki bulguların nasıl önceliklendirileceği, kime iş olarak verileceği ve nasıl kapatılacağı.',
    'scenario': 'Tarama raporu düzenli çıkıyorsa; bulguların raporda kalıp düzeltilmemesini önlemek için.',
    'example': 'Kritik bulgu iş takip sistemine "SEO-teknik" etiketiyle açılır, düzeltmeden sonra yeniden taramayla kapanır.',
    'rule': 'SEO aracı tarama bulguları: {labels}.',
    'agents': [TSEO, SEOY],
    'showIf': GATE_CRAWL,
    'options': [
        o('prioritize', 'Etkiye göre önceliklendirme', 'Bulgular etkilenen sayfa sayısı ve sayfanın önemine göre sıralanır.', 'Her durumda.', 'Ana hizmet sayfasındaki canonical hatası, 3 eski blog yazısındaki eksik alt metinden önce gelir.',
          'Bulgular etkilenen sayfa sayısı, sayfanın trafik / dönüşüm önemi ve dizine ekleme etkisine göre kritik / yüksek / orta / düşük olarak sınıflanır.'),
        o('ticket', 'Kritik ve yüksek bulgular iş kaydına', 'Kritik ve yüksek bulgu sorumlu ekibe iş kaydı olarak açılır.', 'Yazılım ekibi ayrıysa.', 'İş kaydında bulgu, örnek adresler ve aracın rapor bağlantısı var.',
          'Kritik ve yüksek bulgular sorumlusu ve hedef tarihiyle iş kaydı olarak açılır; kayıtta örnek adresler ve beklenen düzeltme yazılır.'),
        o('verify', 'Düzeltme yeniden taramayla doğrulanır', 'İş, aracın yeniden taramasında bulgu kaybolunca kapanır.', 'Her durumda.', 'Yönlendirme zinciri düzeltildikten sonra yeniden tarama yapılır, bulgu kapanır.',
          'Bir bulgu ancak yeniden taramada (ya da ilgili adres yeniden kontrol edilerek) kaybolduğu görülünce kapatılır.'),
        o('ignore', 'Bilinçli kabul edilen uyarılar not ile gizlenir', 'Bilerek bırakılan uyarılar (ör. kasıtlı noindex) gerekçesiyle gizlenir.', 'Aynı uyarılar her raporda ekibi yoruyorsa.', 'Arama sonuçları sayfasının noindex uyarısı "kasıtlı" notuyla gizlenir.',
          'Bilerek kabul edilen uyarılar gerekçesiyle not edilip gizlenir; gerekçe yılda bir gözden geçirilir.'),
        o('gsc', 'Search Console dizine ekleme raporuyla karşılaştırma', 'Aracın bulguları Search Console\'un dizine ekleme ve Core Web Vitals raporlarıyla karşılaştırılır.', 'Search Console bağlıysa.', 'Araç "noindex" diyor, Search Console da "noindex ile hariç tutuldu" diyor; bulgu doğrulanır.',
          'Aracın bulguları Search Console\'un sayfa dizine ekleme ve Core Web Vitals raporlarıyla karşılaştırılır; Google\'ın raporu esas alınır.'),
    ]})

# ============================================================== 4. Sıralama takibi
sections.append({
    'id': 'mk_st_rank', 'after': 'mk_st_audit', 'area': 'marketing', 'group': GROUP, 'icon': '↗',
    'name': 'Sıralama Takibi', 'en': 'SEO Tools: Rank Tracking',
    'desc': 'Hedef sorguların arama sonuçlarındaki sırasının hangi konum, cihaz ve rakiplerle izleneceği; yapay zekâ aramasında görünürlük takibi.',
    'refs': ['oc_keywords', 'oc_competitors', 'oc_services', 'operating_region', 'mk_geo_detail', 'mk_languages', 'mk_device'],
    'guide': {
        'purpose': 'Sıralama takibi (Ahrefs Rank Tracker, Semrush Position Tracking ve benzerleri) seçilen sorguların seçilen konum ve cihazda kaçıncı sırada çıktığını düzenli ölçer. Anahtar kelime listesi Ortak Bilgiler › Hedef Sorgular\'dan, rakipler Ortak Bilgiler › Rakipler\'den gelir; böylece içerik planı, reklam ve rapor aynı listeyi kullanır. Yapay zekâ aramasında (AI Overviews, AI Mode, ChatGPT, Perplexity, Gemini) markanın görünürlüğü de ayrı araçlarla izlenebilir.',
        'criteria': [
            'İzlenen sorgular Ortak Bilgiler › Hedef Sorgular ile aynıdır; her sorgunun hedef sayfası tanımlıdır.',
            'Konum, dil ve cihaz hedef pazarla uyumludur (yerel işletmede il / ilçe düzeyi).',
            'Rakipler Ortak Bilgiler › Rakipler\'den gelir.',
            'Sorgular marka / marka dışı, hizmet ve sayfa türü etiketleriyle gruplanmıştır.',
            'SERP özellikleri (öne çıkan snippet, yerel paket, AI Overviews) ayrıca izlenir.',
            'Sıralama raporu Search Console\'daki ortalama konumla karşılaştırılarak yorumlanır.',
        ],
        'pitfalls': [
            'Semrush\'ta kampanyanın konum ve cihazı sonradan değiştirilemez; yanlış konumla açılan kampanya baştan kurulur.',
            'Yalnız masaüstü izlenir; kullanıcıların çoğu mobildedir.',
            'Ülke düzeyinde izlenen yerel işletme, il düzeyindeki gerçek sıralamasını görmez.',
            'Marka adıyla yapılan sorgular ortalamayı şişirir; marka dışı sorgular ayrıca raporlanmaz.',
            'Ahrefs Rank Tracker varsayılan olarak haftalık güncellenir; günlük dalgalanma beklentisi yanlış yorumlanır.',
            'Bir sorgunun sırası, hedef sayfa yerine başka bir sayfayla (kanibalizasyon) elde edilir ve fark edilmez.',
        ],
        'resources': [],
    }})

fields.append({
    'id': 'mk_st_kw_source', 'section': 'mk_st_rank', 'label': 'İzlenecek Sorguların Kaynağı', 'en': 'Tracked Keywords Source', 'type': 'select',
    'explanation': 'Sıralama takibine girecek anahtar kelime listesinin nereden geleceği.',
    'scenario': 'Sıralama takibi kurulacaksa; içerik, reklam ve raporun aynı sorgu listesini kullanması için.',
    'example': 'Ortak Bilgiler › Hedef Sorgular\'daki 40 sorgu hedef sayfalarıyla birlikte Semrush Position Tracking\'e aktarılır.',
    'rule': 'Sıralama takibinde izlenecek sorguların kaynağı: {label}.',
    'agents': [SEOY, ISEO],
    'showIf': GATE_RANK,
    'options': [
        o('common', 'Ortak Bilgiler › Hedef Sorgular (önerilen)', 'Hedef sorgular ve hedef sayfaları Ortak Bilgiler\'den alınır; araçta yeni sorgu bulunursa önce oraya eklenir.', 'Her durumda önerilir.', 'Yeni bir hizmet sorgusu önce Ortak Bilgiler\'e eklenir, sonra takip listesine girer.',
          'İzlenen sorgular Ortak Bilgiler › Hedef Sorgular\'daki liste ve hedef sayfalarıdır; araçta bulunan yeni sorgu önce o listeye eklenir, sonra takibe alınır.'),
        o('tool', 'Aracın önerileri + onay', 'Aracın önerdiği sorgulardan SEO yöneticisinin onayladıkları eklenir.', 'Hedef sorgu listesi henüz yoksa.', 'Araç 200 sorgu önerir, yönetici 60\'ını onaylar.',
          'Aracın önerdiği sorgulardan yalnız SEO yöneticisinin onayladıkları takibe alınır ve Ortak Bilgiler › Hedef Sorgular\'a da yazılır.'),
        o('gsc', 'Search Console sorguları', 'Search Console\'da gösterim alan sorgulardan seçilir.', 'Site bir süredir yayındaysa ve gerçek sorgu verisi varsa.', 'Son 3 ayda en çok gösterim alan 50 marka dışı sorgu takibe alınır.',
          'Takip listesi Search Console\'da gösterim alan marka dışı sorgulardan seçilir ve üç ayda bir yenilenir; liste Ortak Bilgiler › Hedef Sorgular\'a da yazılır.'),
    ]})

fields.append({
    'id': 'mk_st_rank_set', 'section': 'mk_st_rank', 'label': 'Sıralama Takibi Ayarları', 'en': 'Rank Tracking Settings', 'type': 'multiselect',
    'explanation': 'Sıralamanın hangi konum, cihaz ve rakiplerle, hangi gruplamayla izleneceği.',
    'scenario': 'Sıralama takibi kurulurken; konum ve cihaz ayarı bazı araçlarda sonradan değiştirilemez.',
    'example': 'İzmir il düzeyinde, mobil ve masaüstü ayrı; Ortak Bilgiler\'deki 5 rakip eklenir, sorgular hizmet etiketleriyle gruplanır.',
    'rule': 'Sıralama takibi ayarları: {labels}.',
    'agents': [SEOY, REK],
    'showIf': GATE_RANK,
    'options': [
        o('location', 'Konum hedef pazara göre (il / ilçe düzeyi)', 'Konum Ortak Bilgiler › Hizmet Coğrafyası ve Hizmet Bölgesi Ayrıntısı\'na göre seçilir; yerel işletmede il ya da ilçe.', 'Her durumda; yerel işletmede özellikle.', 'Bornova\'daki klinik "İzmir" yerine ilçe ya da posta kodu düzeyinde izlenir.',
          'Konum Ortak Bilgiler › Hizmet Coğrafyası ve Hizmet Bölgesi Ayrıntısı\'na göre seçilir (ülke / il / ilçe / posta kodu); dil Ortak Bilgiler › Diller\'e göredir. Kampanya açılmadan önce konum doğrulanır (Semrush\'ta sonradan değiştirilemez).'),
        o('devices', 'Mobil ve masaüstü ayrı', 'Sıralama mobil ve masaüstünde ayrı izlenir.', 'Her sitede önerilir.', 'Raporda mobil ve masaüstü sırası ayrı sütunlarda.',
          'Sıralama mobil ve masaüstü için ayrı izlenir; Ortak Bilgiler › Kitlenin Cihaz Kullanımı\'nda ağırlıklı olan cihaz raporda önce verilir.'),
        o('competitors', 'Rakipler Ortak Bilgiler\'den', 'Ortak Bilgiler › Rakipler\'deki rakip siteler takibe eklenir.', 'Rakip listesi varsa.', 'Raporda her sorguda 5 rakibin sırası yan yana.',
          'Ortak Bilgiler › Rakipler\'deki rakip alan adları sıralama takibine eklenir (Ahrefs en çok 10, Semrush en çok 20 rakip).'),
        o('tags', 'Etiketlerle gruplama', 'Sorgular marka / marka dışı, hizmet ve sayfa türüne göre etiketlenir.', 'Raporun hizmet ya da sayfa grubu bazında okunması isteniyorsa.', '"Hizmet: implant", "marka dışı" etiketli sorguların ortalama sırası ayrı izlenir.',
          'Sorgular marka / marka dışı, hizmet (Ortak Bilgiler › Ürün / Hizmetler) ve sayfa türü etiketleriyle gruplanır; raporda marka dışı ortalama ayrı verilir.'),
        o('target', 'Her sorgunun hedef sayfası', 'Her sorguya hedeflenen sayfa atanır; başka sayfa sıralanırsa uyarı verilir.', 'Birbirine yakın sayfalar (kanibalizasyon riski) varsa.', '"implant fiyatları" sorgusunda blog yazısı yerine hizmet sayfası hedeflenir.',
          'Her sorgunun hedef sayfası tanımlanır; sıralanan sayfa hedeften farklıysa (kanibalizasyon) bulgu olarak raporlanır.'),
        o('serp', 'SERP özellikleri ve AI Overviews', 'Öne çıkan snippet, yerel paket, video, "Diğer sorular" ve AI Overviews\'da görünüp görünmediği izlenir.', 'Arama sonuçlarında zengin özellikler yoğunsa.', 'Raporda "AI Overviews\'da kaynak olarak gösterildi" sütunu.',
          'SERP özellikleri (öne çıkan snippet, yerel paket, video, AI Overviews) izlenir; sitenin bu alanlarda görünüp görünmediği sorgu bazında raporlanır.'),
        o('local', 'Yerel paket (harita) takibi', 'Google haritalı yerel sonuçlarında işletmenin sırası işletme adıyla izlenir.', 'Fiziksel işletme ve İşletme Profili varsa.', 'Semrush\'ta yerel paket sırası işletme adıyla izlenir.',
          'Yerel paket (haritalı sonuç) sırası işletme adıyla izlenir; ad Google İşletme Profili\'ndeki adla aynı yazılır.'),
    ]})

fields.append({
    'id': 'mk_st_rank_freq', 'section': 'mk_st_rank', 'label': 'Sıralama Güncelleme Sıklığı', 'en': 'Rank Update Frequency', 'type': 'select',
    'explanation': 'Sıralamanın ne sıklıkla ölçüleceği. Ahrefs Rank Tracker varsayılan olarak haftalık güncellenir; Semrush Position Tracking günlük günceller (uzun süre hareketsiz kampanyada haftalığa düşebilir). Güncelleme sıklığı plana bağlıdır.',
    'scenario': 'Kampanya, site taşıma ya da Google güncellemesi dönemlerinde günlük ölçüm; normal dönemde haftalık çoğu zaman yeterlidir.',
    'example': 'Site taşıma sonrası 4 hafta günlük, sonra haftalık izlenir.',
    'rule': 'Sıralama güncelleme sıklığı: {label}. Raporlarda tek günlük dalgalanma değil, en az iki haftalık eğilim yorumlanır.',
    'agents': [SEOY],
    'showIf': GATE_RANK,
    'options': [
        o('weekly', 'Haftalık (önerilen)', 'Sıralama haftada bir ölçülür.', 'Normal dönemde çoğu sitede.', 'Her pazartesi güncel sıralama.', 'Sıralama haftalık ölçülür.'),
        o('daily', 'Günlük', 'Sıralama her gün ölçülür (planınızda olup olmadığını kontrol edin).', 'Yoğun rekabetli sorgu, kampanya ya da site taşıma döneminde.', 'Taşıma sonrası her sabah sıralama değişimi kontrol edilir.', 'Sıralama günlük ölçülür; günlük ölçüm planın birim / kredi tüketimine göre gerekli sorgularla sınırlanır.'),
        o('mixed', 'Kritik dönemde günlük, sonra haftalık', 'Taşıma, yeniden tasarım ya da Google güncellemesinde günlük; sonrasında haftalık.', 'Site taşıma ya da büyük değişiklik planlanıyorsa.', 'Yeni tasarım yayınından sonra 4 hafta günlük ölçüm.', 'Site taşıma, yeniden tasarım ya da Google çekirdek güncellemesinden sonraki 4 hafta günlük, sonra haftalık ölçülür.'),
    ]})

fields.append({
    'id': 'mk_st_ai_vis', 'section': 'mk_st_rank', 'label': 'Yapay Zekâ Aramasında Görünürlük Takibi', 'en': 'AI Search Visibility Tracking', 'type': 'multiselect',
    'explanation': 'Markanın yapay zekâ aramalarında (Google AI Overviews ve AI Mode, ChatGPT, Perplexity, Gemini, Copilot) ne sıklıkla anıldığının ve kaynak gösterildiğinin izlenmesi. Ahrefs Brand Radar (ek paket) ve Semrush AI Visibility Toolkit bu iş içindir. Sitenin yapay zekâ ayarları 7. Yapay Zekâ menüsündedir.',
    'scenario': 'Yapay zekâ aramasından gelen görünürlük işiniz için önemliyse ve 7. Yapay Zekâ menüsünde izleme kararı verdiyseniz.',
    'example': 'Semrush AI Visibility Toolkit\'te 30 müşteri sorusu (prompt) günlük izlenir; markanın anılma oranı ve rakiplerle karşılaştırması aylık raporda.',
    'rule': 'Yapay zekâ aramasında görünürlük takibi: {labels}. Bu ölçümler aracın seçtiği soru örneklemine dayanan tahmindir; sitenin yapay zekâ ayarları 7. Yapay Zekâ menüsündeki kararlara göre yapılır.',
    'agents': [AIV, SEO],
    'showIf': [{'field': 'mk_st_tools', 'in': ['ahrefs', 'semrush']}],
    'options': [
        o('brandradar', 'Ahrefs Brand Radar', 'AI Overviews, AI Mode, ChatGPT, Perplexity, Gemini ve Copilot\'ta markanın anılmasını izler; yapay zekâ endeksleri ücretli ek paket gerektirir.', 'Ahrefs kullanılıyorsa ve yapay zekâ görünürlüğü önemliyse.', 'Brand Radar\'da markanın ChatGPT\'de anılma payı rakiplerle karşılaştırılır.',
          'Ahrefs Brand Radar ile markanın ve rakiplerin yapay zekâ yanıtlarındaki anılma payı izlenir; özel soru (prompt) listesi Ortak Bilgiler › Hedef Sorgular\'dan türetilir.'),
        o('semrushai', 'Semrush AI Visibility Toolkit', 'ChatGPT, Gemini, AI Mode, AI Overviews ve Perplexity\'de görünürlük puanı, rakip ve soru araştırması; izlenen sorular günlük güncellenir.', 'Semrush kullanılıyorsa ve yapay zekâ görünürlüğü önemliyse.', 'Görünürlük puanı (0–100) ve markayı anmayan sorular listesi aylık raporda.',
          'Semrush AI Visibility Toolkit ile markanın görünürlük puanı, anıldığı / anılmadığı sorular ve kaynak gösterilen sayfalar izlenir.'),
        o('aio', 'Yalnız AI Overviews (SERP özelliği olarak)', 'Sıralama takibinde AI Overviews\'da kaynak olarak görünme izlenir; ek paket alınmaz.', 'Bütçe sınırlıysa.', 'Position Tracking\'de AI Overviews sütunu.',
          'Yapay zekâ görünürlüğü yalnız sıralama takibindeki AI Overviews SERP özelliğiyle izlenir.'),
        o('none', 'Yapay zekâ görünürlüğü izlenmeyecek', 'Ayrı yapay zekâ görünürlük takibi yapılmaz.', 'Henüz öncelik değilse.', 'Rapor yalnız klasik sıralamayı içerir.', 'Yapay zekâ görünürlüğü SEO araçlarıyla izlenmez.', exclusive=True),
    ]})

# ============================================================== 5. Anahtar kelime, rakip & backlink
sections.append({
    'id': 'mk_st_research', 'after': 'mk_st_rank', 'area': 'marketing', 'group': GROUP, 'icon': '⧉',
    'name': 'Anahtar Kelime, Rakip & Backlink Analizi', 'en': 'SEO Tools: Keyword, Competitor & Backlink Analysis',
    'desc': 'SEO araçlarıyla yapılacak anahtar kelime araştırması, rakip karşılaştırması ve backlink izleme / temizleme kuralları.',
    'refs': ['oc_keywords', 'oc_competitors', 'oc_services'],
    'guide': {
        'purpose': 'SEO araçlarının asıl gücü kendi siteniz dışındaki veridir: hangi sorguların arandığı, rakiplerin hangi sorgu ve sayfalarla trafik aldığı, hangi sitelerin kime bağlantı verdiği. Bu bölüm araştırmanın nasıl yapılacağını, sonuçların Ortak Bilgiler › Hedef Sorgular ve içerik planına nasıl işleneceğini ve backlink profilinin nasıl izlenip Google\'ın kurallarına uygun yönetileceğini belirler. Google, bağlantı reddetme (disavow) aracının yalnız çok sayıda spam / yapay bağlantı manuel işleme yol açmış ya da açması muhtemelse kullanılmasını, yanlış kullanımın siteye zarar verebileceğini söyler.',
        'criteria': [
            'Anahtar kelime araştırması arama niyetine göre gruplanır ve Ortak Bilgiler › Hedef Sorgular\'a hedef sayfasıyla işlenir.',
            'Rakip analizi Ortak Bilgiler › Rakipler listesiyle yapılır; sonuç Pazarlama › Rakip Analizi tablosuna aktarılır.',
            'Trafik ve hacim sayıları "tahmin" olarak raporlanır.',
            'Yeni ve kayıp backlinkler düzenli izlenir; önemli kayıp bağlantı için yeniden kazanım denenir.',
            'Bağlantı reddetme yalnız Google\'ın tarif ettiği durumda, gerekçesi yazılarak kullanılır.',
            'Bağlantı satın alma, bağlantı ağı ve otomatik bağlantı programı kullanılmaz (Google spam politikaları).',
        ],
        'pitfalls': [
            'Aracın "toksik" puanı tek başına kanıt sayılıp düzinelerce bağlantı reddedilir; iyi bağlantılar da gider.',
            'Arama hacmi yüksek ama niyeti uymayan sorgular için sayfa yazılır.',
            'Rakip trafik tahmini kesin sayı gibi sunulur.',
            'Rakibin bağlantı verdiği her site, kalite ve konu uyumu bakılmadan hedeflenir.',
            'Anahtar kelime listesi araçta kalır; içerik ve reklam ekibi başka listeyle çalışır.',
            'Türkçe sorgularda araç hacmi düşük ya da eksik görünür; Search Console ve Google Ads Anahtar Kelime Planlayıcı ile karşılaştırılmaz.',
        ],
        'resources': [],
    }})

fields.append({
    'id': 'mk_st_kw', 'section': 'mk_st_research', 'label': 'Anahtar Kelime Araştırması', 'en': 'Keyword Research', 'type': 'multiselect',
    'explanation': 'SEO araçlarıyla yapılacak anahtar kelime araştırmasının kapsamı ve sonuçların nereye işleneceği.',
    'scenario': 'Yeni içerik planlanırken, yeni hizmet eklenirken ya da üç ayda bir fırsat taramasında.',
    'example': 'Keyword Gap ile rakiplerin sıralandığı, sitenin sıralanmadığı 80 sorgu bulunur; niyete göre gruplanıp içerik takvimine ve Hedef Sorgular\'a eklenir.',
    'rule': 'SEO araçlarıyla anahtar kelime araştırması: {labels}. Sonuçlar Ortak Bilgiler › Hedef Sorgular\'a hedef sayfasıyla işlenir; araçtaki hacim ve zorluk değerleri tahmindir.',
    'agents': [ISEO, SEOY],
    'showIf': GATE_RES,
    'options': [
        o('intent', 'Arama niyetine göre gruplama', 'Sorgular bilgi, karşılaştırma, satın alma ve marka niyetine göre gruplanır.', 'Her araştırmada.', '"implant nedir" bilgi, "implant fiyatları" satın alma niyetine ayrılır.',
          'Sorgular arama niyetine (bilgi / karşılaştırma / işlem / marka) göre gruplanır; her grup uygun sayfa türüyle eşleştirilir.'),
        o('gap', 'Rakip boşluğu (Keyword / Content Gap)', 'Rakiplerin sıralandığı, sitenin sıralanmadığı sorgular çıkarılır.', 'Rakip listesi varsa.', 'Üç rakibin ortak sıralandığı 120 sorgu fırsat listesine girer.',
          'Rakip boşluğu analizi Ortak Bilgiler › Rakipler\'deki rakiplerle yapılır; fırsat listesi önceliklendirilip içerik planına aktarılır.'),
        o('clusters', 'Konu kümeleri', 'Sorgular ana konu ve alt başlıklara kümelenir; bir ana sayfa + destek içerikler planlanır.', 'İçerik stratejisi kuruluyorsa.', '"Diş beyazlatma" ana sayfası ve 6 destek yazısı aynı kümede.',
          'Sorgular konu kümelerine ayrılır; her küme için bir ana sayfa ve iç bağlantılı destek içerikler planlanır (Pazarlama › İçerik Stratejisi).'),
        o('questions', 'Soru sorguları ve "Diğer sorular"', 'Kitlenin sorduğu sorular SSS ve blog için toplanır.', 'SSS, blog ya da yapay zekâ görünürlüğü önemliyse.', 'Hizmet sayfasına en çok aranan 8 soru SSS olarak eklenir.',
          'Soru biçimindeki sorgular toplanır; SSS bölümleri ve blog yazıları bu sorulara doğrudan yanıt verecek şekilde planlanır.'),
        o('local', 'Yerel varyantlar', '"İl / ilçe + hizmet" sorguları ayrıca araştırılır.', 'Yerel işletmede.', '"Bornova diş kliniği" ve "İzmir implant" ayrı sorgular olarak listelenir.',
          'Hizmet bölgesindeki il / ilçe + hizmet sorguları (Ortak Bilgiler › Hizmet Bölgesi Ayrıntısı) ayrıca araştırılır.'),
        o('crosscheck', 'Search Console ve Anahtar Kelime Planlayıcı ile karşılaştırma', 'Aracın hacmi Google Ads Anahtar Kelime Planlayıcı ve Search Console gösterimiyle karşılaştırılır.', 'Türkçe ve düşük hacimli sorgularda özellikle.', 'Aracın 0 gösterdiği sorgu Search Console\'da ayda 300 gösterim alıyor.',
          'Türkçe ve düşük hacimli sorgularda aracın hacmi Search Console gösterimi ve Google Ads Anahtar Kelime Planlayıcı ile karşılaştırılır; karar tek araç verisine dayanmaz.'),
    ]})

fields.append({
    'id': 'mk_st_comp', 'section': 'mk_st_research', 'label': 'Rakip Analizi (Araçla)', 'en': 'Competitor Analysis with Tools', 'type': 'multiselect',
    'explanation': 'SEO araçlarıyla rakiplerin hangi açıdan inceleneceği. Sonuçlar Pazarlama › Rakip Analizi tablosuna işlenir.',
    'scenario': 'Pazarlama › Rakip Analizi\'nde ücretli araç yöntemi seçildiyse ya da çeyreklik rakip incelemesinde.',
    'example': 'Her çeyrek rakiplerin en çok trafik alan 20 sayfası, yeni kazandıkları bağlantılar ve organik görünürlük eğilimi tabloya işlenir.',
    'rule': 'Araçla rakip analizi: {labels}. Rakipler Ortak Bilgiler › Rakipler listesinden alınır; sonuçlar Pazarlama › Rakip Analizi tablosuna kaynağı ve tarihiyle işlenir, trafik sayıları tahmin olarak belirtilir.',
    'agents': [REK, SEOY],
    'showIf': GATE_RES,
    'options': [
        o('visibility', 'Organik görünürlük ve trafik eğilimi', 'Rakiplerin tahmini organik trafiği ve görünürlük eğilimi.', 'Her rakip incelemesinde.', 'Bir rakibin görünürlüğü son çeyrekte %30 arttı; sebebi araştırılır.',
          'Rakiplerin organik görünürlük ve tahmini trafik eğilimi çeyreklik karşılaştırılır; büyük değişimin sebebi (yeni bölüm, güncelleme, bağlantı) araştırılır.'),
        o('pages', 'En iyi sayfalar ve içerikler', 'Rakiplerin en çok trafik / bağlantı alan sayfaları.', 'İçerik planlanırken.', 'Rakibin en çok bağlantı alan "fiyat hesaplayıcı" sayfası içerik fikri olur.',
          'Rakiplerin en çok trafik ve bağlantı alan sayfaları çıkarılır; içerik planına kopya değil daha iyi ve özgün karşılıklar olarak aktarılır.'),
        o('links', 'Bağlantı boşluğu (Link Intersect / Backlink Gap)', 'Rakiplere bağlantı verip size vermeyen siteler.', 'Bağlantı kazanımı yapılacaksa.', 'Üç rakibe bağlantı veren sektör derneği sitesi fırsat listesine girer.',
          'Rakiplere bağlantı verip siteye vermeyen siteler listelenir; konu uyumu ve kalitesi kontrol edilerek bağlantı fırsatı olarak değerlendirilir.'),
        o('paid', 'Ücretli arama sorguları ve reklam metinleri', 'Rakiplerin Google Ads\'te teklif verdiği sorgular ve reklam metinleri.', 'Google Ads kullanılıyorsa (Pazarlama › Google Ads).', 'Rakibin marka adınıza reklam verdiği görülür.',
          'Rakiplerin ücretli arama sorguları ve reklam metinleri incelenir; bulgular Pazarlama › Google Ads kararlarına girdi olur.'),
        o('market', 'Trafik kanalları ve pazar payı', 'Rakiplerin trafik kanalları (organik, ücretli, sosyal, yönlendirme) ve pazar payı (Similarweb, Semrush Traffic Analytics).', 'Kanal bütçesi planlanırken.', 'Rakiplerin trafiğinin %40\'ı sosyalden geliyor.',
          'Rakiplerin trafik kanalı dağılımı ve pazar payı tahmini çeyreklik izlenir; kanal bütçe kararlarında tek veri olarak kullanılmaz.'),
    ]})

fields.append({
    'id': 'mk_st_links', 'section': 'mk_st_research', 'label': 'Backlink İzleme ve Temizleme', 'en': 'Backlink Monitoring & Cleanup', 'type': 'multiselect',
    'explanation': 'Siteye gelen bağlantıların (backlink) nasıl izleneceği ve sorunlu bağlantılarla nasıl başa çıkılacağı. Google bağlantı reddetme (disavow) aracının yalnız çok sayıda spam / yapay bağlantı manuel işleme yol açmışsa ya da açması muhtemelse kullanılmasını söyler.',
    'scenario': 'Bağlantı kazanımı yapılıyorsa, olumsuz SEO şüphesi varsa ya da Search Console\'da manuel işlem bildirimi geldiyse.',
    'example': 'Kayıp önemli bağlantı bildirimi gelir; sayfa taşındığı için bağlantı kopmuştur, eski adres yönlendirilir ve bağlantı geri kazanılır.',
    'rule': 'Backlink izleme ve temizleme: {labels}. Bağlantı satın alınmaz, bağlantı ağı ve otomatik bağlantı programı kullanılmaz (Google spam politikaları).',
    'agents': [SEOY, TSEO],
    'showIf': [{'field': 'mk_st_tools', 'in': ['ahrefs', 'awt', 'semrush', 'seranking', 'moz', 'majestic', 'mangools', 'serpstat']}],
    'options': [
        o('monitor', 'Yeni ve kayıp bağlantı bildirimleri', 'Yeni ve kayıp bağlantılar için e-posta bildirimi; aylık gözden geçirme.', 'Her sitede önerilir.', 'Ahrefs "yeni / kayıp backlink" bildirimi haftalık gelir.',
          'Yeni ve kayıp bağlantılar için bildirim kurulur ve ayda bir gözden geçirilir.'),
        o('reclaim', 'Kayıp ve kırık bağlantının geri kazanımı', 'Taşınan / silinen sayfaya gelen bağlantılar yönlendirmeyle ya da site sahibine yazılarak kurtarılır.', 'Site taşıma ya da adres değişikliği yapıldıysa.', 'Eski kampanya sayfasına gelen 25 bağlantı 301 ile yeni sayfaya yönlendirilir.',
          'Bağlantı alan ama 404 veren sayfalar 301 ile en uygun sayfaya yönlendirilir; önemli kayıp bağlantılar için site sahibiyle iletişime geçilir.'),
        o('mentions', 'Bağlantısız marka anmaları', 'Markayı anıp bağlantı vermeyen sayfalar bulunur.', 'Basın ve medya ilişkisi varsa (Pazarlama › Basın Bülteni).', 'Haberde marka adı geçiyor ama bağlantı yok; editöre yazılır.',
          'Markayı anıp bağlantı vermeyen sayfalar düzenli bulunur; uygun olanlarda kibarca bağlantı istenir.'),
        o('review', 'Şüpheli bağlantı incelemesi (kanıtla)', 'Spam görünen bağlantılar elle incelenir; aracın "toksik" puanı tek başına kanıt sayılmaz.', 'Ani şüpheli bağlantı artışı ya da olumsuz SEO şüphesi varsa.', 'Bir gecede gelen 2.000 bahis sitesi bağlantısı elle incelenir.',
          'Şüpheli bağlantılar elle incelenir; aracın toksik puanı tek başına karar gerekçesi değildir. Önce bağlantının kaldırılması site sahibinden istenir.'),
        o('disavow', 'Bağlantı reddetme yalnız Google\'ın tarif ettiği durumda', 'Disavow dosyası yalnız çok sayıda spam / yapay bağlantı manuel işleme yol açmışsa ya da açması muhtemelse, gerekçesiyle gönderilir.', 'Search Console\'da bağlantı kaynaklı manuel işlem varsa ya da geçmişte bağlantı satın alındıysa.', 'Eski ajansın aldığı ücretli bağlantılar kaldırılamayınca alan adı düzeyinde reddedilir.',
          'Bağlantı reddetme (disavow) yalnız Google\'ın tarif ettiği durumda — çok sayıda spam, yapay ya da düşük kaliteli bağlantı manuel işleme yol açmış ya da açması muhtemelse — ve kaldırma denendikten sonra kullanılır; dosya alan adı düzeyinde, gerekçesi ve tarihiyle saklanır. Disavow aracı Search Console\'da URL ön ekli mülkle çalışır.'),
    ]})

# ============================================================== 6. Raporlama & Claude bağlantısı
sections.append({
    'id': 'mk_st_report', 'after': 'mk_st_research', 'area': 'marketing', 'group': GROUP, 'icon': '▤',
    'name': 'Raporlama & Claude Bağlantısı (MCP / API)', 'en': 'SEO Tools: Reporting, MCP & API',
    'desc': 'SEO aracı verisinin nasıl raporlanacağı ve Claude\'un araç verisine MCP ya da API ile nasıl, hangi sınırlarla erişeceği.',
    'refs': ['mk_ids'],
    'guide': {
        'purpose': 'SEO araçlarının verisi, Search Console ve GA4\'ün gerçek verisiyle birlikte ve kaynakları ayrılarak raporlanmalıdır. Ahrefs ve Semrush resmî MCP sunucuları sunar; Claude bu sunucularla araç verisini doğrudan sorgulayabilir (Ajanlar › MCP Bağlantıları). MCP ve API sorguları planınızın API birimlerinden düşer; anahtarlar gizli değerdir. Bu bölüm rapor içeriğini ve Claude bağlantısının sınırlarını belirler. Rapor ritmi Pazarlama › Ölçüm & Raporlama\'daki karardır.',
        'criteria': [
            'Raporlarda her sayının kaynağı (Search Console, GA4, araç adı) yazılıdır; tahminler etiketlidir.',
            'Rapor sıralama, görünürlük, teknik sağlık, backlink ve yapılan işleri birlikte verir.',
            'Önemli değişikliklerin (yayın, taşıma, Google güncellemesi) tarihi raporda not edilir.',
            'Claude\'un MCP / API erişimi yalnız okuma amaçlıdır; anahtar gizli değer olarak saklanır.',
            'MCP / API anahtarına aylık birim sınırı konmuştur.',
            'Araçtan dışa aktarılan veri kişisel veri içermez; içeriyorsa paylaşılmaz.',
        ],
        'pitfalls': [
            'API anahtarı koda, .mcp.json dosyasına açık metin olarak ya da sohbet geçmişine yazılır.',
            'Claude büyük bir backlink sorgusunu çalıştırır, aylık birimin tamamı bir günde biter.',
            'Araç tahmini ile Search Console verisi aynı grafikte toplanır.',
            'Rapor sayı listesine döner; ne yapıldığı ve sıradaki adım yazılmaz.',
            'Looker Studio bağlayıcısı planda olmadığı halde rapor ona göre tasarlanır.',
            'Ahrefs MCP adresinde özel betik / köprü kullanılır; sağlayıcı buna izin vermez.',
        ],
        'resources': [],
    }})

fields.append({
    'id': 'mk_st_report_set', 'section': 'mk_st_report', 'label': 'SEO Raporu İçeriği', 'en': 'SEO Report Content', 'type': 'multiselect',
    'explanation': 'SEO aracı verisiyle hazırlanan raporda nelerin yer alacağı. Rapor ritmi Pazarlama › Ölçüm & Raporlama\'daki karara göredir.',
    'scenario': 'Yönetime ya da müşteriye düzenli SEO raporu verilecekse.',
    'example': 'Aylık rapor: Search Console tıklaması, marka dışı sorguların ortalama sırası, tarama sağlık puanı, yeni / kayıp bağlantılar, yapılan işler ve gelecek ayın planı.',
    'rule': 'SEO raporu içeriği: {labels}. Raporun ritmi Pazarlama › Ölçüm & Raporlama kararına göredir; her sayının kaynağı yazılır, araç verisi "tahmin" etiketiyle gerçek veriden ayrı gösterilir.',
    'agents': [OLC, BI],
    'showIf': GATE,
    'options': [
        o('real', 'Gerçek veri önce: Search Console ve GA4', 'Raporun ana göstergeleri Search Console tıklama / gösterim ve GA4 organik dönüşümüdür.', 'Her raporda önerilir.', 'Raporun ilk sayfası Search Console tıklama eğrisi.',
          'Raporun ana göstergeleri Search Console tıklama, gösterim, ortalama konum ve GA4 organik oturum / dönüşümdür; araç verisi bunları tamamlar.'),
        o('rank', 'Sıralama ve görünürlük', 'Hedef sorguların sırası, marka dışı ortalama, ilk 3 / ilk 10\'daki sorgu sayısı.', 'Sıralama takibi kuruluysa.', 'İlk 10\'daki marka dışı sorgu sayısı 18\'den 26\'ya çıktı.',
          'Hedef sorguların sırası, marka dışı ortalama ve ilk 3 / ilk 10\'daki sorgu sayısı önceki dönemle karşılaştırılır.'),
        o('health', 'Teknik sağlık', 'Tarama sağlık puanı, kritik bulgular ve kapananlar.', 'Site taraması kuruluysa.', 'Sağlık puanı 82 → 91; 14 kritik bulgudan 12\'si kapandı.',
          'Tarama sağlık puanı, açık kritik / yüksek bulgu sayısı ve dönemde kapatılan bulgular raporlanır.'),
        o('links', 'Backlink özeti', 'Yeni, kayıp ve önemli bağlantılar.', 'Backlink izleniyorsa.', 'Bu ay 12 yeni bağlantı, 3 kayıp; 1 sektör dergisi bağlantısı kazanıldı.',
          'Yeni, kayıp ve dikkate değer bağlantılar ve yeniden kazanım çalışmaları raporlanır.'),
        o('annotations', 'Değişiklik notları', 'Yayın, taşıma, içerik güncellemesi ve Google güncellemesi tarihleri grafik üstünde not edilir.', 'Her raporda önerilir.', 'Sıralama düşüşünün yanında "çekirdek güncelleme" notu.',
          'Kod yayını, site taşıma, büyük içerik güncellemesi ve Google güncellemesi tarihleri raporda not edilir; değişimler bu tarihlerle birlikte yorumlanır.'),
        o('actions', 'Yapılanlar ve sıradaki adımlar', 'Dönemde yapılan işler ve gelecek dönemin öncelikleri.', 'Her raporda önerilir.', 'Rapor "bu ay yapılanlar" ve "gelecek ay 5 öncelik" ile biter.',
          'Rapor dönemde yapılan işleri ve gelecek dönemin önceliklendirilmiş adımlarını içerir.'),
        o('looker', 'Looker Studio panosu', 'Rapor Looker Studio\'da canlı pano olarak tutulur (bağlayıcı planınızda olmalı).', 'Rapor çok kişiye düzenli gidiyorsa.', 'Yönetim panosunda SEO sekmesi her sabah güncellenir.',
          'SEO raporu Looker Studio panosu olarak tutulur; pano görüntüleme paylaşımıyla, kişisel veri içermeden paylaşılır.'),
    ]})

fields.append({
    'id': 'mk_st_mcp', 'section': 'mk_st_report', 'label': 'Claude\'un Araç Verisine Erişimi (MCP / API)', 'en': 'Claude Access via MCP / API', 'type': 'multiselect',
    'explanation': 'Claude\'un SEO aracı verisini doğrudan sorgulayıp sorgulamayacağı ve kuralları. Ahrefs MCP (https://api.ahrefs.com/mcp/mcp) ve Semrush MCP (https://mcp.semrush.com/v2/mcp) resmî sunuculardır, OAuth ile bağlanır; sorgular planın API birimlerinden düşer ve planınızda API erişimi olmalıdır. Bağlantıyı eklemek için Ajanlar › MCP Bağlantıları\'nda Ahrefs / Semrush kartını projeye ekleyin.',
    'scenario': 'Claude\'un anahtar kelime, rakip ya da backlink analizi yapmasını, rapor taslağı hazırlamasını istiyorsanız.',
    'example': 'Claude Semrush MCP ile hedef sorguların hacmini çeker, niyete göre gruplayıp içerik planı taslağı hazırlar; birim sınırı aşılmadan durur.',
    'rule': 'Claude\'un SEO aracı verisine erişimi: {labels}.',
    'agents': [MT, SEO],
    'showIf': [{'field': 'mk_st_tools', 'in': [t for t in TOOLS if t not in ('awt', 'majestic')]}],
    'options': [
        o('ahrefs_mcp', 'Ahrefs MCP', 'Claude Ahrefs verisini resmî MCP sunucusuyla sorgular (OAuth; planınızda API erişimi olmalı).', 'Ahrefs kullanılıyorsa.', 'Claude "rakiplerin son 30 günde kazandığı bağlantılar" sorgusunu Ahrefs MCP\'den çeker.',
          'Ahrefs verisine Claude resmî MCP sunucusuyla (https://api.ahrefs.com/mcp/mcp, OAuth) erişir; sunucu Ajanlar › MCP Bağlantıları\'ndan projeye eklenir. MCP adresi yalnız Claude bağlantısı için kullanılır, özel betik ya da köprü kurulmaz.'),
        o('semrush_mcp', 'Semrush MCP', 'Claude Semrush verisini resmî MCP sunucusuyla sorgular (OAuth; planınızda API birimi olmalı).', 'Semrush kullanılıyorsa.', 'Claude Semrush MCP ile 50 sorgunun hacmini ve zorluğunu çeker.',
          'Semrush verisine Claude resmî MCP sunucusuyla (https://mcp.semrush.com/v2/mcp, OAuth) erişir; sunucu Ajanlar › MCP Bağlantıları\'ndan projeye eklenir.'),
        o('similarweb_mcp', 'Similarweb MCP', 'Claude Similarweb trafik ve pazar verisini resmî MCP sunucusuyla sorgular (planınızda API erişimi olmalı).', 'Similarweb kullanılıyorsa.', 'Claude üç rakibin trafik kanal dağılımını Similarweb MCP\'den çeker.',
          'Similarweb verisine Claude resmî MCP sunucusuyla (https://mcp.similarweb.com/) erişir; sunucu Ajanlar › MCP Bağlantıları\'ndan projeye eklenir, plan API erişimi içermelidir.'),
        o('other_mcp', 'Diğer araçların resmî MCP sunucusu', 'SE Ranking, Moz (beta), Sistrix, Screaming Frog (lisanslı, bilgisayarda yerel), Ubersuggest, Mangools (beta) ve Serpstat resmî MCP sunucusu sunar.', 'Bu araçlardan biri kullanılıyorsa.', 'Claude SE Ranking MCP ile sıralama verisini okur.',
          'Seçilen diğer aracın yalnız sağlayıcının kendi yayımladığı resmî MCP sunucusu kullanılır (topluluk yapımı sunucular kullanılmaz); adres ve kimlik doğrulama sağlayıcının güncel belgesinden alınır, beta sunucular üretim raporunda tek kaynak yapılmaz.'),
        o('readonly', 'Yalnız okuma ve analiz', 'Claude araç verisini okur, analiz eder ve öneri hazırlar; araçta ayar değiştirmez.', 'MCP / API kullanılıyorsa her durumda.', 'Claude sıralama verisini yorumlar, kampanya ayarına dokunmaz.',
          'Claude araç verisini yalnız okur ve analiz eder; proje, kampanya ya da tarama ayarlarını değiştirmez, değişiklik önerisini kullanıcıya sunar.'),
        o('budget', 'Birim bütçesi ve büyük sorguda onay', 'Aylık birim sınırı vardır; büyük sorgudan önce tahmini birim kullanıcıya bildirilir.', 'MCP / API kullanılıyorsa her durumda.', 'Claude 10.000 satırlık backlink dışa aktarımından önce tahmini birimi sorar.',
          'MCP / API anahtarına aylık birim sınırı konur; büyük sorgulardan (çok satırlı dışa aktarım, toplu analiz) önce tahmini birim kullanıcıya bildirilip onay alınır.'),
        o('secrets', 'Anahtar gizli değer olarak saklanır', 'API / MCP anahtarı yalnız ortam değişkeni ya da gizli değer deposundadır.', 'API anahtarıyla bağlanılıyorsa.', '.mcp.json\'da anahtar yerine ${SEMRUSH_API_KEY} yazılı.',
          'API / MCP anahtarı koda, .mcp.json\'a açık metin olarak, belgeye ya da sohbete yazılmaz; yalnız ortam değişkeni ya da gizli değer deposunda tutulur (.mcp.json\'da ${DEGISKEN}).'),
        o('none', 'Claude araç verisine bağlanmayacak', 'Araç verisi elle dışa aktarılır, Claude\'a dosya olarak verilir.', 'API erişimi yoksa ya da bütçe sınırlıysa.', 'Aylık CSV dışa aktarımı Claude\'a yüklenir.',
          'Claude SEO aracına doğrudan bağlanmaz; gerekli veri elle dışa aktarılır, kişisel veri içermediği kontrol edilerek verilir.', exclusive=True),
    ]})

# ============================================================== kaynaklar (2026-11-13 doğrulandı)
RES = {
    'mk_st_scope': [
        R('Ahrefs Webmaster Tools', 'https://ahrefs.com/webmaster-tools', 'Ücretsiz sürümün kapsamı ve sınırları (Site Audit, Site Explorer, Web Analytics).'),
        R('Ahrefs — Kullanıcı ekleme ve roller', 'https://help.ahrefs.com/en/articles/411099-how-do-i-add-and-manage-users-to-my-account-s-workspace', 'Çalışma alanına kullanıcı ekleme ve Owner / Admin / Member rolleri.'),
        R('Ahrefs — İki adımlı doğrulama', 'https://help.ahrefs.com/en/articles/8755828-two-factor-authentication-2fa', 'Kimlik doğrulayıcı uygulama ya da güvenlik anahtarıyla 2FA ve zorunlu kılma.'),
        R('Semrush — Abonelikler ve ücretsiz hesap', 'https://www.semrush.com/kb/1011-subscriptions', 'Planlar ve ücretsiz hesabın sınırları.'),
        R('Semrush — Kullanıcı yönetimi', 'https://www.semrush.com/kb/1409-user-management', 'Owner / Admin / User / Guest rolleri, koltuk ve paylaşım.'),
        R('Semrush — SAML SSO', 'https://www.semrush.com/kb/1609-saml-sso', 'Kurumsal tekil oturum açma kurulumu.'),
    ],
    'mk_st_setup': [
        R('Ahrefs — Proje ekleme', 'https://help.ahrefs.com/en/articles/1433362-how-to-add-a-project-in-your-dashboard', 'Search Console\'dan içe aktarma ya da elle proje açma adımları.'),
        R('Ahrefs — Site sahipliği doğrulama', 'https://help.ahrefs.com/en/articles/1431155-how-do-i-verify-ownership-of-my-website', 'Search Console, DNS TXT, HTML dosyası ve meta etiket yöntemleri.'),
        R('Ahrefs — Proje kapsamı modları', 'https://help.ahrefs.com/en/articles/2834076-how-to-define-the-scope-of-project-using-different-modes', 'Tam adres, klasör, alan adı ve alt alan adları kapsamları.'),
        R('Ahrefs — Doğrulanmış proje', 'https://help.ahrefs.com/en/articles/4321336-what-is-a-verified-project', 'Doğrulanmış projenin ücretsiz ek kredileri ve Search Console bağlantısı.'),
        R('Semrush — Proje yönetimi', 'https://www.semrush.com/kb/243-managing-a-project', 'Proje oluşturma, paylaşım ve alan adının sonradan değiştirilememesi.'),
        R('Semrush — Entegrasyonlar', 'https://www.semrush.com/kb/931-integrations', 'Google Analytics, Search Console, Ads, İşletme Profili ve Looker Studio bağlantıları.'),
        R('Semrush — Organic Traffic Insights Google bağlantısı', 'https://www.semrush.com/kb/939-organic-traffic-insights-google-connection', 'Search Console ve Analytics verisini Semrush\'a bağlama.'),
        R('Ahrefs — Looker Studio bağlayıcıları', 'https://help.ahrefs.com/en/articles/9229306-how-can-i-use-ahrefs-with-looker-studio', 'Site Audit, Site Explorer ve Rank Tracker bağlayıcıları ve plan şartı.'),
    ],
    'mk_st_audit': [
        R('Ahrefs Site Audit tarayıcısı', 'https://ahrefs.com/robot/site-audit', 'AhrefsSiteAudit kullanıcı aracısı, robots.txt davranışı ve IP listeleri.'),
        R('Ahrefs — IP aralıkları ve izin listesi', 'https://help.ahrefs.com/en/articles/78658-what-is-the-list-of-your-ip-ranges', 'Cloudflare ve diğer WAF\'larda Ahrefs tarayıcısına izin verme.'),
        R('Ahrefs — Site Audit ayarları', 'https://help.ahrefs.com/en/articles/9082329-how-should-i-configure-my-site-audit-settings', 'Zamanlama, hız, JavaScript, robots.txt, parametre ve kimlik doğrulama ayarları.'),
        R('Semrush botları', 'https://www.semrush.com/bot/', 'SiteAuditBot ve diğer Semrush tarayıcılarının adları ve davranışı.'),
        R('Semrush — Site Audit yapılandırma', 'https://www.semrush.com/kb/539-configuring-site-audit', 'Kullanıcı aracısı, hız, JavaScript, hariç tutma, kimlik doğrulama ve zamanlama.'),
        R('Semrush — Site Audit sorun giderme', 'https://www.semrush.com/kb/681-site-audit-troubleshooting', 'Site Audit IP ağı ve CDN / güvenlik duvarında izin verme.'),
    ],
    'mk_st_rank': [
        R('Ahrefs Rank Tracker', 'https://ahrefs.com/rank-tracker', 'Konum, cihaz, rakip, SERP özellikleri ve AI Overviews takibi.'),
        R('Ahrefs — Sıralama güncelleme sıklığı', 'https://help.ahrefs.com/en/articles/604245-how-frequently-do-my-tracked-keywords-get-updated', 'İzlenen sorguların güncellenme sıklığı.'),
        R('Semrush — Position Tracking yapılandırma', 'https://www.semrush.com/kb/548-configuring-position-tracking', 'Arama motoru, cihaz, konum ayarları ve sonradan değiştirilemeyenler.'),
        R('Semrush — Position Tracking', 'https://www.semrush.com/kb/32-position-tracking', 'Güncelleme sıklığı, rakipler, etiketler ve SERP özellikleri.'),
        R('Ahrefs Brand Radar', 'https://help.ahrefs.com/en/articles/11064852-what-is-brand-radar-and-how-to-use-it', 'Yapay zekâ aramasında marka görünürlüğü takibi ve kapsadığı platformlar.'),
        R('Semrush — AI Visibility özellikleri', 'https://www.semrush.com/kb/1626-ai-visibility-features', 'AI Visibility Toolkit\'in izlediği platformlar ve plan farkları.'),
        R('Semrush — AI Visibility Toolkit başlangıç', 'https://www.semrush.com/kb/1496-getting-started-with-ai-visibility-toolkit', 'Görünürlük puanı, rakip ve soru araştırması raporları.'),
    ],
    'mk_st_research': [
        R('Google — Bağlantıları reddetme (disavow)', 'https://support.google.com/webmasters/answer/2648487', 'Disavow aracının ne zaman kullanılacağı ve yanlış kullanım riski.'),
        R('Semrush — Backlink Audit', 'https://www.semrush.com/kb/295-backlink-audit-tool', 'Bağlantı denetimi, toksik sinyaller, kaldırma talebi ve reddetme listesi.'),
        R('Semrush — Bağlantı reddetme dosyası', 'https://www.semrush.com/kb/764-disavowing-your-backlinks', 'Google biçiminde disavow dosyası dışa aktarma ve dikkat edilecekler.'),
        R('Ahrefs — Backlink bildirimleri', 'https://ahrefs.com/academy/how-to-use-ahrefs/alerts/backlinks', 'Yeni ve kayıp backlink e-posta bildirimleri.'),
    ],
    'mk_st_report': [
        R('Ahrefs MCP — Giriş', 'https://docs.ahrefs.com/mcp/docs/introduction.md', 'Ahrefs MCP adresi, kimlik doğrulama, birim kullanımı ve kısıtlar.'),
        R('Ahrefs MCP — Başlangıç', 'https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp', 'Ahrefs MCP\'yi Claude\'a bağlama adımları.'),
        R('Ahrefs API', 'https://ahrefs.com/seo-api', 'API erişiminin planlara göre durumu ve birim maliyeti.'),
        R('Semrush MCP', 'https://developer.semrush.com/api/introduction/semrush-mcp', 'Semrush MCP adresi, OAuth / API anahtarı ve API birimleri.'),
        R('Semrush — Looker Studio bağlayıcısı', 'https://www.semrush.com/features/google-looker-studio-connector/', 'Domain Analytics, Position Tracking ve Site Audit bağlayıcıları.'),
    ],
}
EXTRA_RES = {   # benzer araçlar ve genel kaynaklar (2026-11-13 doğrulandı)
    'mk_st_scope': [
        R('Similarweb — Planlar', 'https://www.similarweb.com/corp/pricing/', 'Ücretsiz örnek veri ile ücretli planların kapsamı.'),
        R('SE Ranking — Planlar', 'https://seranking.com/pricing.html', 'Deneme süresi ve Search Console / GA4 entegrasyonunun yer aldığı planlar.'),
        R('Moz Pro — Planlar', 'https://moz.com/products/pro/pricing', 'Moz Pro planları ve ücretsiz topluluk hesabı.'),
        R('Moz Local — Kapsanan ülkeler', 'https://moz.com/products/local/pricing', 'Moz Local\'in yalnız ABD, Birleşik Krallık ve Kanada\'da çalıştığı.'),
        R('Screaming Frog SEO Spider', 'https://www.screamingfrog.co.uk/seo-spider/', 'Masaüstü tarayıcı; ücretsiz sürümün 500 adres sınırı.'),
        R('Mangools MCP ve ücretsiz hesap', 'https://mangools.com/mcp', 'Mangools araçları, ücretsiz hesap sınırları ve MCP sunucusu.'),
    ],
    'mk_st_setup': [
        R('Google — Site sahipliğini doğrulama', 'https://support.google.com/webmasters/answer/9008080', 'Search Console doğrulama yöntemleri (HTML dosyası, meta etiket, DNS, Analytics etiketi).'),
    ],
    'mk_st_audit': [
        R('Moz — rogerbot', 'https://moz.com/help/moz-procedures/crawlers/rogerbot', 'Moz Pro site taraması tarayıcısı.'),
        R('Sistrix — Tarama hataları ve tarayıcı', 'https://www.sistrix.com/tutorials/crawling-errors-in-the-onpage-projects/', 'SISTRIX Crawler kullanıcı aracısı ve tarama sorunları.'),
        R('Screaming Frog — Yapılandırma', 'https://www.screamingfrog.co.uk/seo-spider/user-guide/configuration/', 'Kullanıcı aracısı, hız, JavaScript ve hariç tutma ayarları.'),
        R('Cloudflare — Doğrulanmış botlar', 'https://developers.cloudflare.com/bots/concepts/bot/verified-bots/', 'Doğrulanmış iyi botların tanınması.'),
        R('Cloudflare — WAF atlama (Skip) kuralı', 'https://developers.cloudflare.com/waf/custom-rules/skip/', 'Belirli trafiğin yönetilen kuralları atlaması; Bot Fight Mode istisnası.'),
        R('Google — robots.txt\'ye giriş', 'https://developers.google.com/search/docs/crawling-indexing/robots/intro', 'robots.txt\'nin ne işe yaradığı ve sınırları.'),
    ],
    'mk_st_rank': [
        R('Sistrix — Görünürlük endeksi hesaplaması', 'https://www.sistrix.com/visibility-index/calculation', 'Ülke endeksleri (Türkiye dahil) ve ölçüm yöntemi.'),
    ],
    'mk_st_research': [
        R('Majestic — MJ12bot', 'https://mj12bot.com/', 'Majestic bağlantı tarayıcısı ve robots.txt ile engelleme.'),
        R('Moz — dotbot', 'https://moz.com/help/moz-procedures/crawlers/dotbot', 'Moz bağlantı endeksi tarayıcısı.'),
    ],
    'mk_st_report': [
        R('Similarweb — Claude MCP entegrasyonu', 'https://developers.similarweb.com/docs/claude-mcp-integration.md', 'Similarweb MCP sunucusunu Claude\'a bağlama.'),
        R('SE Ranking — MCP', 'https://seranking.com/api/integrations/mcp/', 'SE Ranking MCP adresi ve kimlik doğrulama.'),
        R('Moz — MCP sunucuları', 'https://moz.com/api/docs/guides/mcp-servers', 'Moz MCP sunucuları (beta).'),
        R('Sistrix — MCP', 'https://www.sistrix.com/ask-sistrix/ai-basics/mcp/', 'Sistrix MCP, kimlik doğrulama ve kullanım kotası.'),
        R('Screaming Frog — MCP sunucusu', 'https://www.screamingfrog.co.uk/guides/mcp-server/', 'Uygulamaya gömülü yerel MCP sunucusu (lisanslı sürüm).'),
        R('Ubersuggest — Claude bağlayıcısı', 'https://claude.com/marketplace/connectors/ubersuggest-by-neil-patel', 'Anthropic dizinindeki Ubersuggest bağlayıcısı.'),
        R('Serpstat — MCP sunucusu', 'https://github.com/SerpstatGlobal/serpstat-mcp-server-js', 'Serpstat\'ın resmî yerel MCP sunucusu.'),
    ],
}


def main():
    for s in sections:
        s['guide']['resources'] = RES.get(s['id'], []) + EXTRA_RES.get(s['id'], [])
    out = {'version': 1, 'group': GROUP, 'sections': sections, 'fields': fields, 'fields_into': [], 'option_add': [],
           'guide_add': {}, 'recommend_add': []}
    json.dump(out, open(os.path.join(HERE, 'seo-araclari.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('tamam: %d bölüm, %d alan, %d kaynak' % (len(sections), len(fields), sum(len(s['guide']['resources']) for s in sections)))


main()
