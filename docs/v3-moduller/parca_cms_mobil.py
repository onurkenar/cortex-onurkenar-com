# -*- coding: utf-8 -*-
"""V3 maddeleri A3 (içerik modeli, URL / slug, sürümleme ve yayın), A5 (form standardı), C1 (Mobil Uygulama — yeni bölüm),
C2 (pop-up ve duyuru şeridi), C8 (metrik sözlüğü). Kaynak: Web_Sayfasi_Projesi_Revize_Moduler_V3 — Mobile, Veri ve
Uygulama Mimarisi, İçerik Yönetim Motoru, URL ve Routing, Form Builder, Sayfa Oluşturucu, Dashboard › Metrik Sözlüğü,
Mobil Uygulama / Public Mobil Deneyim, Pop-up & Banner Yönetimi, Yayın ve İçerik Akışı.
Kaynak adresleri 2026-11-12'de açılarak doğrulandı (curl 200 + sayfa başlığı)."""

# --- ajanlar (pozisyonlar.txt, birebir)
SWE = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
APPDEV = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/uygulama-gelistirme-uzmani'
API = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani'
REL = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/yayin-yonetimi-uzmani'
APPSEC = 'poz:siber-guvenlik:16.06/guvenli-yazilim-gelistirme-yasam-dongusu/kidemli-uygulama-guvenligi-uzmani'
CIAM = 'poz:siber-guvenlik:16.05/kimlik-dogrulama-ve-musteri-kimligi-guvenligi/ciam-guvenligi-uzmani'
TSEO = 'poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru/teknik-seo-uzmani'
EDITOR = 'poz:pazarlama:content_marketing/editoryal-yonetim-muduru/kidemli-editor'
KVKK = 'poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani'
CRM = 'poz:pazarlama:marketing_operations_crm_martech/crm-ve-lead-yonetimi-muduru/crm-uzmani'
CRO = 'poz:pazarlama:growth_conversion/cro-ve-deney-yonetimi-muduru'
A11Y = 'poz:urun-arge:18.05/servis-tasarimi-ve-erisilebilirlik/dijital-erisilebilirlik-uzmani'
PM = 'poz:urun-arge:18.03/dijital-urun-yonetimi/urun-yoneticisi'
MKA = 'poz:veri-analitik:17.05/musteri-pazarlama-ve-gelir-analitigi/pazarlama-analitigi-uzmani'
KPI = 'poz:veri-analitik:17.04/kurumsal-raporlama-ve-kpi-yonetimi/kpi-ve-raporlama-analisti'
ATTR = 'poz:pazarlama:marketing_operations_crm_martech/pazarlama-verisi-ve-raporlama-muduru/atif-analitigi-uzmani'
MEAS = 'poz:pazarlama:digital_demand_generation/web-pazarlama-muduru/dijital-olcumleme-uzmani'

CMS_ON = [{'field': 'cms_mode', 'in': ['Custom Admin', 'Headless CMS', 'WordPress', 'Other']}]
MOB_ALL = ['pwa', 'react_native', 'flutter', 'native', 'wrapper']
MOB_ON = [{'field': 'mobile_app', 'in': MOB_ALL}]
MOB_STORE = [{'field': 'mobile_app', 'in': ['react_native', 'flutter', 'native', 'wrapper']}]


def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    if exclusive:
        x['exclusive'] = True
    return x


# =====================================================================================================
# A3 — İçerik modeli (cms bölümü)
# =====================================================================================================
CMS_CONTENT_RULES = {
    'id': 'cms_content_rules', 'section': 'cms', 'after': 'cms_modules', 'type': 'multiselect',
    'label': 'İçerik Modeli ve URL Kuralları', 'en': 'Content Model, Page Tree & URL Rules', 'agents': [SWE, TSEO],
    'showIf': CMS_ON,
    'explanation': 'Panelde oluşturulan sayfa ve içeriklerin nasıl bir ağaçta durduğunu, adreslerinin (URL ve slug) nasıl üretildiğini, adres değişince ne olduğunu ve içerikler arasındaki ilişkilerin nasıl kurulduğunu belirler. Slug, adresin içeriğe özgü son parçasıdır (ör. /hizmetler/web-tasarim içindeki "web-tasarim").',
    'scenario': 'Panelden sayfa, hizmet, blog ya da ürün eklenecekse; adreslerin elle değil kuralla üretilmesi, değişen adreslerin arama motoru trafiğini kaybettirmemesi ve içeriklerin birbirine bağlanması isteniyorsa.',
    'example': 'Editör "Kurumsal Web Tasarım" sayfasını "Hizmetler" altına ekler; adres kendiliğinden /hizmetler/kurumsal-web-tasarim olur, sayfada "Ana sayfa › Hizmetler › Kurumsal Web Tasarım" yolu çıkar; slug sonradan değiştirilirse eski adres yeni adrese 301 ile yönlenir.',
    'rule': 'İçerik modeli ve URL kuralları: {labels}. Adres üretimi, yönlendirme ve ilişki kuralları sunucuda uygulanır (istemciden gelen adres ya da ebeveyn bilgisine güvenilmez); aynı dilde iki içerik aynı adresi alamaz (veritabanında benzersiz kısıt), yönetim paneli ve önizleme adresleri dizine kapalıdır.',
    'recommend': [
        {'field': 'locales', 'map': {'Multi Language': ['i18n_links'], 'Locale Ready': ['i18n_links']}},
        {'field': 'schema_types', 'map': {'BreadcrumbList': ['breadcrumb']}},
        {'field': 'internal_links', 'map': {'true': ['relations']}},
    ],
    'options': [
        o('page_tree', 'Çok seviyeli sayfa ağacı ve ebeveyn sayfa seçimi', 'Sayfalar iç içe (ebeveyn → alt sayfa) yönetilir; panelde ağaç görünümünde sürükle-bırak ile taşınır.',
          'Hizmet, çözüm ya da kurumsal bilgi sayfalarının alt başlıklara ayrıldığı siteler.', 'Panelde "Kurumsal › Hakkımızda › Yönetim Kurulu" ağacı görünür, sayfa sürüklenerek başka ebeveyne taşınır.',
          'Sayfa kaydında ebeveyn alanı (parent_id) tutulur; döngü (sayfanın kendi alt sayfasını ebeveyn seçmesi) sunucuda engellenir, derinlik en çok 4 seviyeyle sınırlanır. WordPress\'te sayfa hiyerarşisi yerleşiktir; özel içerik türlerinde "hierarchical" ayarı açılmalıdır.'),
        o('parent_url', 'URL\'nin ebeveyn sayfaya göre oluşması', 'Alt sayfanın adresi ebeveyninin adres yolunu içerir (/hizmetler/web-tasarim/e-ticaret).',
          'Site yapısının adreslerden de okunması isteniyorsa; çok seviyeli hizmet / ürün ağaçlarında.', 'Ebeveyni "Hizmetler" olan sayfanın adresi kendiliğinden /hizmetler/… ile başlar.',
          'Adres yolu ebeveyn zincirinden sunucuda türetilir ve kayıtta saklanır; ebeveyn değişince bütün alt sayfaların adresleri yeniden üretilir ve her eski adres için 301 yönlendirmesi oluşturulur. WordPress\'te sayfalar için yerleşiktir.'),
        o('auto_slug', 'Otomatik slug ve elle düzeltme', 'Slug başlıktan otomatik üretilir (Türkçe harfler Latin karşılığına çevrilir, küçük harf, tire); editör gerekirse elle düzeltir.',
          'Her projede; özellikle editörlerin adres kuralını bilmediği ekiplerde.', '"Şirket İçi Eğitim Programları" başlığından sirket-ici-egitim-programlari slug\'ı önerilir, editör egitim-programlari olarak kısaltabilir.',
          'Slug ç→c, ğ→g, ı→i, ö→o, ş→s, ü→u dönüşümüyle, yalnız a-z, 0-9 ve tire içerecek biçimde sunucuda normalize edilir; elle girilen slug da aynı normalizasyondan geçer, çakışmada -2 eki önerilir. Yayınlanmış içeriğin slug\'ı değişirse uyarı gösterilir. WordPress slug\'ı yerleşik üretir; Türkçe karakter dönüşümü yayından önce test edilir.'),
        o('slug_redirect', 'Slug / adres değişince otomatik 301 yönlendirme', 'Yayınlanmış bir içeriğin adresi değişince eski adres kalıcı (301) yönlendirmeyle yeni adrese bağlanır; yönlendirmeler ve 404 kayıtları panelde listelenir.',
          'Yayında olan, arama motorunda dizine eklenmiş ya da dışarıdan bağlantı almış her site.', 'Editör /blog/kvkk-rehberi adresini /blog/kvkk-uyum-rehberi yapar; eski adres 301 ile yeniye gider, panelin "Yönlendirmeler" ekranında satır olarak görünür.',
          'Yayınlanmış içeriğin adresi değişince 301 kaydı otomatik eklenir; yönlendirme zinciri (A→B→C) tek adıma indirilir, döngü engellenir, silinen içerik için 410 ya da en yakın içeriğe 301 kararı panelde verilir; 404 alan adresler sayaçla listelenir. WordPress\'te eski slug yönlendirmesi yalnız yazılarda ve sınırlıdır; kalıcı yönlendirme listesi için SEO eklentisinin yönlendirme modülü (bkz. SEO Eklentisi kararı) ya da yönlendirme eklentisi kullanılır.'),
        o('breadcrumb', 'Ağaçtan otomatik içerik yolu (breadcrumb)', 'Sayfanın üstündeki "Ana sayfa › Hizmetler › …" yolu sayfa ağacından otomatik üretilir ve yapısal veriyle işaretlenir.',
          'İki seviyeden derin yapılı, hizmet / kategori / blog içeren siteler.', 'Ürün sayfasında "Ana sayfa › Ürünler › Kurumsal Yazılım › CRM" yolu görünür; her adım bağlantıdır.',
          'İçerik yolu sayfa ağacından sunucuda üretilir, görünen yol ile BreadcrumbList yapısal verisi aynı kaynaktan çıkar (bkz. Schema Türleri); son öğe bağlantısız, <nav aria-label> içinde sıralı listedir. WordPress çekirdeğinde yoktur; SEO eklentisinin ya da temanın içerik yolu özelliği kullanılır.'),
        o('relations', 'İçerik ilişkileri ve otomatik ilişkili içerik', 'Sayfa, blog, hizmet, ürün, referans ve medya birbirine bağlanır; ilişkili içerikler sayfada otomatik gösterilir.',
          'İç bağlantının ve içerikler arası gezinmenin önemli olduğu, hizmet + blog + referans içeren siteler.', 'Hizmet sayfasının altında o hizmetle ilişkilendirilmiş 3 blog yazısı ve 2 referans projesi kendiliğinden listelenir.',
          'İçerik ilişkileri ayrı ilişki tablosunda (kaynak, hedef, ilişki türü, sıra) tutulur; yayında olmayan ya da başka dildeki içerik ilişkide gösterilmez, silinen içeriğin ilişkileri temizlenir. Otomatik öneri önce elle bağlananları, sonra aynı kategori / etiketi gösterir. WordPress\'te ilişki alanı yerleşik değildir; özel alan eklentisi ya da tema kodu gerekir.'),
        o('required_fields', 'İçerik tipine göre zorunlu alanlar', 'Her içerik tipinin (hizmet, blog, ürün, referans …) yayına çıkmak için doldurulması gereken alanları ayrı tanımlanır.',
          'Birden çok editörün içerik girdiği, eksik içeriğin yayına çıkmaması gereken projeler.', 'Hizmet sayfası öne çıkan görsel, kısa açıklama, CTA ve SEO başlığı girilmeden "Yayınla" düğmesi etkin olmaz; eksik alanlar listelenir.',
          'Zorunlu alan kuralları içerik tipi şemasında tanımlanır ve yayın isteğinde sunucuda doğrulanır; taslak eksik alanlarla kaydedilebilir, yayın engellenir. WordPress çekirdeğinde yoktur; özel alan eklentisi ve yayın öncesi doğrulama kancası gerekir.'),
        o('taxonomy', 'Kategori ve etiket sınıflandırması', 'İçerikler kategori (hiyerarşik) ve etiket (serbest) ile sınıflandırılır, listeleme ve filtrelemede kullanılır.',
          'Blog, haber, bilgi bankası, ürün ve referans listeleri olan siteler.', 'Blogda "Kategori: Dijital Pazarlama", "Etiket: SEO, GA4" görünür; kategori sayfası filtreli liste verir.',
          'Kategori ve etiketler dil bazında tutulur; tek içerikli ya da boş etiket sayfaları noindex olur, aynı anlamdaki etiketler birleştirilir (birleştirmede eski adres 301). WordPress\'te kategori, etiket ve özel taksonomi yerleşiktir.'),
        o('i18n_links', 'Dil sürümlerinin birbirine bağlanması', 'Bir içeriğin Türkçe ve İngilizce gibi sürümleri tek kayıt grubunda bağlanır; her dilin kendi slug\'ı olur.',
          'Çok dilli sitelerde (bkz. Dil Yapısı); dil değiştiricinin aynı içeriğin karşılığına gitmesi isteniyorsa.', 'Türkçe /hizmetler/web-tasarim sayfasındaki dil seçicisi /en/services/web-design sayfasına gider; karşılığı yoksa dilin ana sayfasına.',
          'Dil sürümleri ortak çeviri grubu kimliğiyle bağlanır; hreflang etiketleri ve dil seçici bu gruptan üretilir (bkz. Yerelleştirme Kuralları), karşılığı olmayan dil için hreflang yazılmaz. WordPress çekirdeğinde çok dillilik yoktur; çok dilli eklenti kullanılır.'),
        o('multi_brand', 'Marka / şirket bazlı içerik', 'İçerikler hangi marka ya da şirkete ait olduğuna göre etiketlenir; aynı içerik birden çok markada kullanılabilir.',
          'Holding, çok markalı ya da beyaz etiketli (white-label) yapılar.', 'Aynı KVKK sayfası iki marka sitesinde kullanılır, kampanya sayfası yalnız bir markanın sitesinde görünür.',
          'İçerik ile marka arasında çoka-çok ilişki tutulur; listeleme sorguları etkin markaya göre süzülür, bir markanın editörü yalnız kendi markasının içeriğini düzenler (yetki sunucuda denetlenir). Aynı içerik birden çok alan adında yayındaysa canonical tek adresi gösterir. WordPress\'te çoklu site (multisite) ya da taksonomi ile kurulur.'),
    ],
}

CMS_PUBLISHING = {
    'id': 'cms_publishing', 'section': 'cms', 'after': 'cms_content_rules', 'type': 'multiselect',
    'label': 'Sürümleme, Zamanlama ve Yayın Takibi', 'en': 'Versioning, Scheduling & Publishing Lifecycle', 'agents': [SWE, EDITOR],
    'showIf': CMS_ON,
    'explanation': 'İçeriklerin sürüm geçmişinin, ileri tarihli yayının, arşivlemenin, yayın öncesi kontrollerin ve yayın sonrası performans takibinin panelde nasıl çalışacağını belirler. İçerik onay akışı bu karar değil, İş Akışları ve Onay Mekanizmaları ile Pazarlama › İş Akışı & Onay kararlarıdır.',
    'scenario': 'Birden çok kişinin içerik düzenlediği, kampanya sayfalarının belirli tarihte açılıp kapandığı ya da yanlış bir değişikliğin hızla geri alınması gereken projeler.',
    'example': 'Editör kampanya sayfasını 1 Aralık 09:00\'da yayına, 31 Aralık 23:59\'da yayından kalkacak biçimde planlar; dün yapılan hatalı değişiklik "Sürümler" sekmesinden tek tıkla geri alınır.',
    'rule': 'İçerik sürümleme, zamanlama ve yayın takibi: {labels}. Yayın, geri alma ve zamanlama işlemleri sunucuda yetki denetimiyle yapılır ve kim / ne zaman / ne yaptı bilgisiyle kaydedilir; zamanlanmış işler idempotent çalışır (aynı içerik iki kez yayına alınmaz).',
    'recommend': [
        {'field': 'seo_gate', 'map': {'true': ['seo_checklist']}},
        {'field': 'approval_enabled', 'map': {'true': ['revisions', 'field_audit']}},
    ],
    'options': [
        o('revisions', 'Sürüm geçmişi, karşılaştırma ve geri alma', 'Her kayıt yeni bir sürüm oluşturur; iki sürüm yan yana karşılaştırılır, eski sürüme dönülebilir.',
          'Her CMS projesi; özellikle birden çok editörlü ekipler.', '"Sürümler" sekmesinde 12 sürüm listelenir, ikisi seçilince değişen paragraflar renkli görünür, "Bu sürüme dön" yeni bir sürüm olarak geri yükler.',
          'Her kayıtta içeriğin tam sürümü saklanır; geri alma yeni sürüm oluşturur (geçmiş silinmez), sürüm sayısı ya da süresi sınırlanır (ör. son 50 sürüm). WordPress\'te revizyonlar yerleşiktir; sayısı WP_POST_REVISIONS ile sınırlanır, özel alanların revizyona girmesi ayrıca ayarlanır.'),
        o('field_audit', 'Alan bazında değişiklik kaydı', 'Hangi alanın kim tarafından, ne zaman, hangi değerden hangi değere değiştirildiği ayrı ayrı kaydedilir.',
          'Fiyat, iletişim, hukuki metin gibi hassas alanların izlenmesi gereken projeler; denetime tabi kurumlar.', 'Ürün kaydında "Fiyat: 1.200 → 1.450 TL · Ayşe Y. · 12.11.2026 14:32" satırı görünür.',
          'Değişiklik kaydı yalnız eklenebilir (append-only) tabloda tutulur; parola, token ve kişisel veri içeren alanların değeri kayda yazılmaz, yalnız "değişti" işaretlenir. WordPress\'te yerleşik değildir; etkinlik kaydı (activity log) eklentisi gerekir.'),
        o('schedule', 'İleri tarihli yayın ve otomatik yayından kaldırma', 'İçerik belirlenen tarih-saatte kendiliğinden yayına girer ve istenirse belirlenen tarihte yayından kalkar.',
          'Kampanya, duyuru, etkinlik ve süreli teklif sayfaları.', 'Black Friday sayfası 28 Kasım 00:00\'da açılır, 1 Aralık 00:00\'da kapanır ve adresi ana kampanya sayfasına yönlenir.',
          'Zamanlama sunucu saatine değil Türkiye saat dilimine (Europe/Istanbul) göre girilir, UTC saklanır; zamanlanmış işi arka plan işi çalıştırır (bkz. Arka Plan İşleri), kaçan iş bir sonraki çalışmada telafi edilir. Yayından kalkan sayfa için yönlendirme ya da 410 kararı zorunludur. WordPress\'te ileri tarihli yayın yerleşiktir ama WP-Cron ziyaretle tetiklendiği için sunucu cron\'una bağlanır; otomatik yayından kaldırma eklenti ister.'),
        o('calendar', 'Yayın takvimi', 'Planlanan ve yayınlanan içerikler takvim görünümünde izlenir; tarih sürükle-bırakla değiştirilir.',
          'Düzenli blog, haber ve kampanya yayını yapan ekipler.', 'Panelde aylık takvimde 14 Kasım "Blog: KVKK rehberi (planlandı)", 18 Kasım "Kampanya sayfası (taslak)" görünür.',
          'Takvim yalnız kullanıcının yetkili olduğu içerikleri gösterir; takvimde tarih değiştirmek zamanlama kuralından ve yetki denetiminden geçer. WordPress\'te yerleşik değildir; editoryal takvim eklentisi kullanılır.'),
        o('archive', 'Arşivleme (silmeden yayından kaldırma)', 'Eskiyen içerik silinmez, arşive alınır; gerekirse geri yayına çıkar.',
          'Haber, kampanya, iş ilanı ve etkinlik gibi süreli içerikler.', 'Biten etkinlik sayfası "Arşiv" durumuna geçer, sitede "Bu etkinlik sona erdi" notuyla görünür ya da yayından kalkar.',
          'Arşivlenen içerik için üç seçenekten biri seçilir: notla yayında kalır, en yakın içeriğe 301 ya da 410; silme yalnız yetkili rolle ve onaylı yapılır, saklama süresi dolan kişisel veri içeren içerik imha politikasına göre silinir. WordPress\'te "Taslak" / "Özel" durumlarıyla ya da arşiv durumu ekleyen eklentiyle yapılır.'),
        o('seo_checklist', 'Yayın öncesi içerik SEO kontrol listesi', 'Yayınla düğmesine basılınca içeriğin SEO başlığı, açıklaması, H1, görsel alt metni, iç bağlantısı ve canonical\'ı denetlenir.',
          'SEO\'dan trafik bekleyen her içerik sitesi (bkz. Yayın Öncesi SEO Kalite Kapısı).', 'Yayınla\'ya basınca "Meta açıklama 180 karakter — en çok 160 önerilir; 2 görselde alt metin yok" uyarıları çıkar.',
          'Kontrol listesi içerik tipine göre tanımlanır ve yayın isteğinde sunucuda çalışır; kritik maddeler (noindex açık kalması, boş başlık, kopya slug) yayını engeller, diğerleri uyarıdır. WordPress\'te SEO eklentisinin içerik analizi kullanılır.'),
        o('preview', 'Paylaşılabilir süreli önizleme bağlantısı', 'Yayınlanmamış içerik, giriş yapmamış birine süreli ve tek kullanımlık bağlantıyla gösterilebilir.',
          'Müşteri, yönetici ya da hukuk biriminin taslağı panel hesabı olmadan görmesi gerekiyorsa.', 'Editör "Önizleme bağlantısı oluştur" der; 48 saat geçerli bağlantı e-postayla gönderilir, süresi dolunca açılmaz.',
          'Önizleme bağlantısı tahmin edilemez belirteçle (token) üretilir, süresi ve iptali panelden yönetilir; önizleme yanıtları noindex ve önbelleğe alınmaz (Cache-Control: private, no-store). WordPress\'te önizleme yalnız giriş yapmış kullanıcıya açıktır; paylaşılabilir önizleme eklenti ister.'),
        o('editorial_meta', 'İçerik künyesi: sorumlu, hedef ve tarihler', 'Her içerikte içerik sorumlusu, onay sorumlusu, içerik hedefi (trafik, lead, bilgilendirme, güven, satış desteği), hedef anahtar kelime, CTA, hedef yayın ve revizyon tarihi alanları bulunur.',
          'İçerik üretimi plana bağlı ve ölçülen ekipler.', 'Blog taslağının yan panelinde "Sorumlu: Mehmet K. · Hedef: lead · Anahtar kelime: KVKK uyum danışmanlığı · Revizyon: 12.05.2027" görünür.',
          'Künye alanları içerik tipinde tanımlanır; revizyon tarihi gelen içerik sorumluya görev / bildirim olarak düşer. Onay akışının kendisi İş Akışları ve Onay Mekanizmaları kararına göre kurulur.'),
        o('review_cycle', '7 / 30 / 90 gün içerik performans kontrolü', 'Yayınlanan içeriğin 7., 30. ve 90. günde trafik, dönüşüm ve arama performansı hedefle karşılaştırılır; düşük performansta güncelleme görevi açılır.',
          'Blog, rehber ve kampanya içeriklerinin geri dönüşünün izlendiği projeler.', 'Yayının 30. gününde "Hedef 500 oturum, gerçekleşen 180 — güncelleme görevi oluşturuldu" bildirimi gelir.',
          'Kontrol günleri arka plan işiyle tetiklenir, veri analitik ve Search Console kaynaklarından okunur (kişisel veri değil, toplam metrik); sonuç içerik kaydına yazılır ve sorumluya görev açılır. Metrik tanımları Pazarlama › Metrik Sözlüğü ile aynıdır.'),
        o('edit_lock', 'Eşzamanlı düzenleme kilidi', 'Bir içeriği biri düzenlerken başkası açarsa uyarı görür; üzerine yazma engellenir.',
          'Birden çok editörün aynı içeriğe dokunabildiği ekipler.', '"Bu sayfayı şu anda Ayşe Y. düzenliyor (3 dk önce)" uyarısı çıkar; "Devral" yalnız yetkiliye açıktır.',
          'Kayıtta sürüm numarasıyla iyimser kilit (optimistic locking) uygulanır: eski sürüm üzerinden gelen kayıt reddedilir ve fark gösterilir; düzenleme kilidi süreli tutulur. WordPress\'te yazı kilitleme yerleşiktir.'),
    ],
}

# =====================================================================================================
# A5 — Form standardı (cms bölümü)
# =====================================================================================================
FORM_STANDARD = {
    'id': 'form_standard', 'section': 'cms', 'after': 'cms_publishing', 'type': 'multiselect',
    'label': 'Form Oluşturucu ve Form Standardı', 'en': 'Form Builder & Form Standard', 'agents': [SWE, CRM, KVKK],
    'explanation': 'Sitedeki iletişim, teklif, başvuru, randevu ve bülten formlarının nasıl kurulacağını, doğrulanacağını, hangi onayları toplayacağını ve gönderimlerin nereye aktarılacağını belirler. Bot koruması Kimlik Doğrulama & Güvenlik › Bot Koruması, dosya yükleme kuralları Dosya & Depolama › Dosya Yükleme Standardı kararlarındadır; bu karar onlara form düzeyinde bağlanır.',
    'scenario': 'Sitede lead, teklif, başvuru ya da bülten formu varsa; formlar pazarlama, CRM ve KVKK süreçlerinin giriş kapısıysa.',
    'example': 'Teklif formunda "Firma türü: Kurumsal" seçilince vergi numarası alanı açılır; KVKK aydınlatma bağlantısı ve işaretsiz pazarlama izni kutusu görünür; gönderim CRM\'de "Kaynak: /hizmetler/seo · UTM: google/cpc · Mobil" bilgisiyle lead olur ve kullanıcı teşekkür sayfasına gider.',
    'rule': 'Form standardı: {labels}. Bütün form doğrulamaları sunucuda da yapılır (istemci doğrulaması yalnız kullanıcı kolaylığıdır); gönderimler idempotent işlenir (çift tıklamada tek kayıt), form içeriği ve kişisel veri uygulama loglarına yazılmaz, hata mesajları alanla ilişkilendirilir (aria-describedby).',
    'recommend': [
        {'field': 'modules_extra', 'map': {'crm': ['crm_source'], 'career': ['upload'], 'booking': ['builder']}},
        {'field': 'turnstile_security', 'map': {'Cloudflare Turnstile': ['spam'], 'reCAPTCHA': ['spam'], 'hCaptcha': ['spam']}},
    ],
    'options': [
        o('builder', 'Panelden form oluşturucu (çok dilli, sürümlü)', 'Formlar kod yazmadan panelde oluşturulur: alan ekleme, sürükle-bırak sıralama, metin / seçim / onay kutusu / tarih / dosya gibi alan türleri, dil bazında etiketler; formun her değişikliği yeni sürümdür.',
          'Pazarlama ekibinin sık form açtığı, rezervasyon ve eğitim başvurusu gibi farklı formların gerektiği projeler (CMS gerekir).', 'Pazarlama uzmanı "Webinar Kayıt" formunu panelde 5 alanla oluşturur, sayfaya blok olarak ekler; formda değişiklik yapınca "Sürüm 3" olur.',
          'Form tanımı sürümlü saklanır ve her gönderim, gönderildiği form sürümünün kimliğiyle kaydedilir; yayındaki formun alanı silinirse eski gönderimler kaybolmaz. Alan türleri beyaz listeyle sınırlıdır (form oluşturucudan HTML / betik eklenemez). CMS kullanılmıyorsa formlar kodda tanımlanır, aynı sürüm kuralı geçerlidir.'),
        o('conditional', 'Koşullu alanlar', 'Bir alanın cevabına göre başka alanlar görünür ya da gizlenir.',
          'Bireysel / kurumsal ayrımı, hizmet türüne göre değişen sorular.', '"Kurumsal" seçilince firma adı ve vergi numarası açılır, "Bireysel" seçilince gizlenir.',
          'Koşul kuralları form tanımında tutulur ve sunucuda da değerlendirilir: gizli alan zorunlu sayılmaz, gizli alana gelen değer kaydedilmez. Gizlenen alan ekran okuyucudan da kaldırılır, görünür olunca odak sırası korunur.'),
        o('validation', 'Alan bazlı doğrulama ve regex', 'Her alan için zorunluluk, uzunluk, biçim (e-posta, telefon, VKN, IBAN) ve özel düzenli ifade (regex) kuralı tanımlanır.',
          'Her form; özellikle teklif, başvuru ve ödeme öncesi formlar.', 'Telefon alanına "0532 123 45 67" yazılınca kabul edilir, "123" yazılınca alanın altında "Geçerli bir cep telefonu girin" çıkar.',
          'Doğrulama kuralları tek tanımdan hem istemcide hem sunucuda çalışır; regex kuralları zaman aşımıyla ve felaket geri izleme (ReDoS) riskine karşı denetlenerek uygulanır, telefon E.164 biçiminde saklanır. Hata mesajı alan yanında ve formun başında özet olarak verilir.'),
        o('consent', 'Forma özel aydınlatma metni ve onay kayıtları', 'Her forma o formun amacına uygun aydınlatma metni bağlanır; açık rıza ve ticari ileti izni ayrı, önceden işaretlenmemiş kutularla alınır ve kaydedilir.',
          'Kişisel veri toplayan her form (KVKK); pazarlama izni de alınıyorsa 6563 sayılı Kanun ve İYS.', 'Formun altında "Aydınlatma Metni" bağlantısı ve işaretsiz "Kampanyalardan e-posta ve SMS ile haberdar olmak istiyorum" kutusu durur; kutu işaretlenmeden form gönderilebilir.',
          'Aydınlatma metni bilgilendirmedir, onay kutusu değildir; açık rıza ve ticari ileti izni hizmet şartına bağlanmaz, ayrı ve önceden işaretsiz kutularla alınır. Her onay; metnin sürümü, tarih-saat, kanal, form kimliği ve IP ile kayda alınır; ticari ileti izni İYS\'ye bildirilir (bkz. Kayıtta Onay ve Bilgilendirme Metinleri). Metinler hukuk biriminin onayıyla yayınlanır.'),
        o('double_optin', 'Çift onay (double opt-in)', 'Bülten ya da pazarlama izni veren kişiye doğrulama e-postası gider; bağlantıya tıklayınca izin etkinleşir.',
          'Bülten ve pazarlama listesi toplayan formlar; yanlış ya da başkasına ait e-posta riskinin olduğu durumlar.', 'Bülten formunu dolduran kişiye "Aboneliğinizi onaylayın" e-postası gider; onaylanmayan adres 7 gün sonra silinir.',
          'Doğrulama bağlantısı tek kullanımlık ve süreli belirteçle üretilir; onaylanmamış adrese pazarlama iletisi gönderilmez, onay tarih-saati izin kaydına eklenir, süresi dolan onaysız kayıt silinir.'),
        o('crm_source', 'CRM alan eşlemesi ve kaynak kaydı (sayfa, UTM, cihaz)', 'Form alanları CRM alanlarına eşlenir; her gönderimle kaynak sayfa, yönlendiren, UTM parametreleri ve cihaz türü kaydedilir.',
          'Formların lead olarak CRM\'e aktığı, pazarlama kanallarının dönüşümünün ölçüldüğü projeler.', 'CRM\'de lead kartında "Form: Teklif · Sayfa: /hizmetler/seo · utm_source=google · utm_medium=cpc · Cihaz: mobil" görünür.',
          'Alan eşlemesi panelde tanımlanır ve sürümlenir; CRM\'e aktarım kuyrukla, yeniden denemeyle ve idempotency anahtarıyla yapılır (aktarım hatasında gönderim kaybolmaz). UTM ve kaynak bilgisi yalnız çerez / onay kurallarına uygun biçimde okunur; IP ve cihaz bilgisi ayrıntısı en az veri ilkesiyle sınırlanır.'),
        o('spam', 'Spam puanı ve bot koruması eşiği', 'Gönderimlere bot doğrulaması, gizli tuzak alan (honeypot), doldurma süresi ve hız sınırına göre spam puanı verilir; eşiği aşan gönderim karantinaya alınır.',
          'Herkese açık her form; özellikle spam ve sahte lead alan siteler.', 'Panelde "Karantina (12)" sekmesi görünür; 3 saniyede doldurulmuş ve tuzak alanı dolu gönderim CRM\'e gitmez.',
          'Bot doğrulaması Bot Koruması kararındaki sağlayıcıyla yapılır ve doğrulama belirteci sunucuda sağlayıcıya sorulur; IP ve form başına hız sınırı uygulanır, eşik panelden ayarlanır. Karantinadaki gönderim belirli süre sonra silinir, yanlış pozitif elle onaylanabilir.'),
        o('upload', 'Dosya yükleme alanı güvenliği', 'Formdaki dosya alanı (CV, belge, görsel) tür, boyut ve zararlı yazılım denetiminden geçer, özel depoda tutulur.',
          'Kariyer başvurusu, teklif ekleri, şikâyet / destek formları.', 'CV alanı yalnız PDF ve DOCX, en çok 5 MB kabul eder; yüklenen dosyaya yalnız İK rolü süreli bağlantıyla erişir.',
          'Dosya alanları Dosya Yükleme Standardı kararına uyar: MIME ve içerik imzası sunucuda denetlenir, dosya adı yeniden üretilir, dosyalar herkese açık olmayan depoda tutulur ve süreli imzalı bağlantıyla verilir, saklama süresi sonunda silinir.'),
        o('after_submit', 'Gönderim sonrası teşekkür sayfası, bildirim ve dönüşüm olayı', 'Gönderim sonrası kullanıcı teşekkür sayfasına ya da belirlenen sayfaya yönlenir, ekibe e-posta bildirimi, kullanıcıya "talebiniz alındı" e-postası gider ve dönüşüm olayı tetiklenir.',
          'Dönüşümün ölçüldüğü ve talebin hızla karşılanması gereken formlar.', 'Teklif formundan sonra /tesekkurler?form=teklif sayfası açılır; satış ekibine "Yeni teklif talebi" e-postası, kullanıcıya numaralı alındı e-postası gider.',
          'Yönlendirme adresi yalnız site içi beyaz listeden seçilir (açık yönlendirme yok); dönüşüm olayı yalnız sunucu gönderimi başarıyla kaydettikten sonra tetiklenir (bkz. Dönüşüm Olayları). Ekip bildirim e-postasında kişisel verinin tamamı yerine panel bağlantısı verilir; teşekkür sayfası noindex olur.'),
        o('abandon', 'Form terk ve alan bazlı hata ölçümü', 'Formun görüntülenme, doldurmaya başlama, gönderme ve terk oranları ile en çok hata veren / terk edilen alan ölçülür.',
          'Dönüşüm oranı iyileştirilmek istenen uzun ya da kritik formlar (CRO).', 'Raporda "Teklif formu: 1.000 görüntüleme, 340 başlama, 120 gönderim; en çok terk: Telefon alanı" görünür.',
          'Olaylar form_view, form_start, form_error (alan adıyla), form_submit olarak ve analitik onayına bağlı gönderilir; olaylara alan değeri ya da kişisel veri yazılmaz, yalnız alan adı ve hata türü yazılır.'),
    ],
}

FORM_STORAGE = {
    'id': 'form_storage', 'section': 'cms', 'after': 'form_standard', 'type': 'select',
    'label': 'Form Gönderimlerinin Saklanması', 'en': 'Form Submission Storage & Retention', 'agents': [SWE, KVKK],
    'explanation': 'Form gönderimlerinin nerede tutulacağını ve ne kadar süre saklanacağını belirler. Saklama yeri, kişisel verinin güvenliğini, silinmesini ve ilgili kişi başvurularının yanıtlanmasını doğrudan etkiler.',
    'scenario': 'Kişisel veri içeren her form için; özellikle gönderimlerin yalnız e-postaya düştüğü ya da üçüncü taraf form servisine gittiği projelerde.',
    'example': 'Gönderimler panelde "Form Gönderimleri" ekranında listelenir, CRM\'e aktarılır ve 2 yıl sonra kendiliğinden anonimleştirilir.',
    'rule': 'Form gönderimlerinin saklanması: {label}. Gönderimler saklama ve imha politikasındaki süre dolunca silinir ya da anonimleştirilir; gönderimlere erişim rol bazlıdır, dışa aktarma kayıt altına alınır ve gönderim verisi uygulama loglarına yazılmaz.',
    'recommend': {'field': 'modules_extra', 'map': {'crm': ['crm']}},
    'options': [
        o('db_panel', 'Panel veritabanında (önerilen)', 'Gönderimler projenin kendi veritabanında tutulur, panelde listelenir; e-posta yalnız bildirimdir.',
          'Çoğu proje; gönderimlerin kaybolmaması, aranması ve KVKK başvurularında bulunması gerekiyorsa.', 'Panelde "Form Gönderimleri" ekranında filtreleme, durum (yeni, ilgilenildi) ve dışa aktarma vardır.',
          'Gönderimler veritabanında şifreli bağlantı ve rol bazlı erişimle tutulur; hassas alanlar (T.C. kimlik no, sağlık bilgisi) alan düzeyinde şifrelenir, saklama süresi form başına tanımlanır ve arka plan işiyle uygulanır.'),
        o('crm', 'CRM\'e aktarılır (panelde kısa süreli kopya)', 'Gönderim CRM\'e lead olarak aktarılır; panelde yalnız aktarım başarılı olana kadar ya da kısa süre kopya tutulur.',
          'CRM\'in tek müşteri kaydı olduğu, satış ekibinin CRM\'de çalıştığı projeler.', 'Gönderim 30 saniye içinde CRM\'de lead olur; panelde "Aktarıldı" durumu ve CRM kaydına bağlantı görünür.',
          'Aktarım kuyrukla ve yeniden denemeyle yapılır; aktarılamayan gönderim panelde hata kuyruğunda kalır ve uyarı üretir, başarılı aktarımdan sonra panel kopyası tanımlı sürede silinir. CRM bir veri işleyense sözleşme ve yurt dışı aktarım durumu hukuk birimiyle teyit edilir.'),
        o('email_only', 'Yalnız e-posta (veritabanına kaydedilmez)', 'Gönderim yalnız belirlenen adrese e-postayla iletilir, sitede kayıt tutulmaz.',
          'Kişisel veri azlığı olan çok küçük siteler; yalnız geçici çözüm olarak.', 'Gönderim info@ adresine gelir; panelde form gönderimi ekranı yoktur.',
          'E-posta teslim edilemezse gönderim kaybolmamalıdır: gönderim başarısızsa kullanıcıya hata gösterilir ve işlem yeniden denenebilir. E-posta kutularındaki gönderimler de saklama süresine tabidir ve silinmesi süreç olarak tanımlanır; hassas veri (T.C. kimlik no, sağlık) bu yöntemle toplanmaz.'),
        o('external', 'Harici form servisinde', 'Form ve gönderimler üçüncü taraf bir form / pazarlama servisinde tutulur; sitede gömülü form kullanılır.',
          'Pazarlama otomasyonu platformunun formlarının kullanıldığı projeler.', 'Sayfadaki form pazarlama platformunun gömülü formudur; gönderimler o platformun panelinde görünür.',
          'Servis veri işleyen olarak sözleşmeye bağlanır, sunucuların konumu ve yurt dışı aktarım dayanağı hukuk birimiyle teyit edilir; gömülü form çerez / onay kurallarına uyar, servis betiği onaydan önce yüklenmez ve Content-Security-Policy\'de yalnız o alan adına izin verilir.'),
    ],
}

# =====================================================================================================
# C2 — Pop-up ve duyuru şeridi (public bölümü)
# =====================================================================================================
POPUP_POLICY = {
    'id': 'popup_policy', 'section': 'public', 'after': 'social_proof', 'type': 'select',
    'label': 'Pop-up ve Duyuru Şeridi Politikası', 'en': 'Pop-up & Banner Policy', 'agents': [CRO, APPDEV],
    'explanation': 'Sitede kampanya, bülten ya da duyuru için açılır pencere (pop-up) ya da sayfanın üstünde / altında duran duyuru şeridi (banner) kullanılıp kullanılmayacağını belirler. Çerez onay bandı bu karar değildir; Gizlilik / KVKK › Çerez / Onay Platformu kararındadır.',
    'scenario': 'Kampanya duyurusu, bülten aboneliği ya da çıkış anında teklif gösterilmek isteniyorsa; aynı zamanda erişilebilirlik ve arama görünürlüğü korunmak isteniyorsa.',
    'example': 'Sayfanın üstünde "Kasım boyunca kurulumda %20 indirim — Detaylar" şeridi görünür; kapatılınca o kampanya süresince tekrar çıkmaz.',
    'rule': 'Pop-up ve duyuru şeridi politikası: {label}.',
    'recommend': {'field': 'conversion_centered', 'map': {'true': ['rules']}},
    'options': [
        o('none', 'Pop-up kullanılmaz', 'Sitede açılır pencere ya da kampanya şeridi yoktur; duyurular sayfa içeriğinde verilir.',
          'Kurumsal, kamu, sağlık ya da güven odaklı siteler; sade deneyimin öncelikli olduğu projeler.', 'Kampanya bilgisi ana sayfadaki bir içerik bloğunda durur; hiçbir katman içeriğin üstüne açılmaz.',
          'Pop-up, modal kampanya penceresi ya da kampanya şeridi bileşeni eklenmez; pazarlama mesajları sayfa içi bloklarla verilir.'),
        o('banner', 'Yalnız duyuru şeridi (banner)', 'Sayfanın üstünde ya da altında ince, kapatılabilir bir şerit kullanılır; içeriği kapatan pencere açılmaz.',
          'Kampanya ve önemli duyuruları görünür kılmak, ama ziyaretçiyi bölmemek isteniyorsa.', 'Üstte "Bayram tatilinde siparişler 3 gün geç kargolanır" şeridi ve × düğmesi görünür.',
          'Şerit içeriği aşağı iterse bu, sayfa yüklenirken yer ayrılarak yapılır (düzen kayması yok); yapışkan şerit klavye odağındaki öğeyi örtmez, kapatma düğmesi erişilebilir adlıdır ve kapatma tercihi yalnız işlevsel olarak saklanır.'),
        o('rules', 'Kurallı pop-up (+ duyuru şeridi)', 'Kampanya ya da bülten pop-up\'ı belirli tetikleyici, sıklık ve erişilebilirlik kurallarıyla kullanılır; duyuru şeridi de kullanılabilir.',
          'Lead toplama ve dönüşümün öncelikli olduğu e-ticaret, eğitim ve kampanya siteleri (bkz. Dönüşüm Odaklı Tasarım).', 'Ziyaretçi sayfanın %60\'ını okuduktan sonra küçük bir bülten penceresi açılır; kapatılınca 14 gün tekrar çıkmaz.',
          'Pop-up\'lar yalnız Pop-up Kuralları kararındaki tetikleyici, sıklık ve erişilebilirlik kurallarıyla çalışır; kurallar sunucudan gelen yapılandırmadan okunur, kampanya bitince kendiliğinden kapanır.'),
    ],
}

POPUP_RULES = {
    'id': 'popup_rules', 'section': 'public', 'after': 'popup_policy', 'type': 'multiselect',
    'label': 'Pop-up ve Şerit Kuralları', 'en': 'Pop-up & Banner Rules', 'agents': [CRO, A11Y, APPDEV],
    'showIf': [{'field': 'popup_policy', 'in': ['banner', 'rules']}],
    'explanation': 'Pop-up ve duyuru şeridinin ne zaman, ne sıklıkla ve hangi erişilebilirlik / gizlilik kurallarıyla gösterileceğini belirler. Tetikleyici ve sıklık kuralları pop-up içindir; erişilebilirlik, düzen ve çerez kuralları şerit için de geçerlidir.',
    'scenario': 'Pop-up ya da şerit kullanılacaksa; arama görünürlüğü, erişilebilirlik ve kullanıcı güveni korunmak isteniyorsa.',
    'example': 'Bülten penceresi yalnız masaüstünde çıkış niyetinde açılır, Escape ile kapanır, odağı açan öğeye geri verir; mobilde yalnız alt şerit olarak görünür ve çerez bandıyla aynı anda açılmaz.',
    'rule': 'Pop-up ve şerit kuralları: {labels}.',
    'options': [
        o('triggers', 'Tetikleyiciler: çıkış niyeti, kaydırma, süre', 'Pop-up sayfa açılır açılmaz değil, çıkış niyeti (fare tarayıcı üst çubuğuna gidince), sayfanın belirli bir yüzdesinin okunması ya da belirli süre sonra açılır.',
          'Pop-up\'ın ziyaretçiyi içeriğe ulaşmadan bölmemesi isteniyorsa.', 'Blog yazısının %50\'si okununca "Benzer rehberler için bültene katılın" penceresi açılır.',
          'Pop-up ilk sayfa yüklemesinde açılmaz; tetikleyiciler (çıkış niyeti yalnız masaüstünde, kaydırma yüzdesi, süre) kampanya başına tanımlanır, ödeme / sepet / form sayfalarında pop-up çıkmaz.'),
        o('frequency', 'Gösterim sıklığı sınırı', 'Aynı ziyaretçiye aynı pop-up belirli süre içinde en çok bir kez gösterilir; kapatılan ya da dönüşen pop-up tekrar çıkmaz.',
          'Her pop-up kullanımı.', 'Kapatılan bülten penceresi 14 gün, abone olunduktan sonra hiç gösterilmez.',
          'Sıklık bilgisi işlevsel yerel depoda (kişisel veri olmadan) tutulur; oturum başına en çok bir pop-up gösterilir, abonelik / dönüşüm sonrası o kampanya tamamen kapanır.'),
        o('no_mobile_interstitial', 'Mobilde içeriği kapatan tam ekran pop-up yok', 'Mobilde ana içeriği örten tam ekran ya da büyük kampanya penceresi kullanılmaz; küçük şerit ya da alt bant tercih edilir.',
          'Mobil trafiği olan her site; Google içeriği örten katmanların arama performansını düşürebileceğini belirtir.', 'Mobilde kampanya, ekranın altında 64 px yüksekliğinde kapatılabilir bant olarak görünür.',
          'Mobilde (dar görüntü alanında) pop-up ana içeriği örtmez; kampanya ekran yüksekliğinin küçük bir kısmını kaplayan kapatılabilir bant olarak gösterilir. Yasal zorunluluk katmanları (çerez onayı, yaş doğrulaması) bu kuralın dışındadır.'),
        o('a11y', 'Kolay kapatma ve klavye / ekran okuyucu erişilebilirliği', 'Pop-up erişilebilir modal iletişim kutusu (dialog) kurallarına uyar: odak içeride tutulur, Escape ile kapanır, kapanınca odak açan öğeye döner.',
          'Her pop-up; WCAG uyumu hedeflenen her site.', 'Pencere açılınca odak başlığa gelir, Tab pencere içinde döner, Escape ve görünür × düğmesi kapatır.',
          'Pop-up role="dialog" ve aria-modal="true", erişilebilir adla (aria-labelledby) kurulur; açıkken arka plan etkisizdir (inert), odak içeride döner, Escape ve en az 24×24 px kapatma düğmesi çalışır, kapanınca odak tetikleyen öğeye geri verilir; hareket animasyonu "azaltılmış hareket" tercihine uyar.'),
        o('layout', 'Düzen kayması yok ve odaklanan öğe örtülmez', 'Şerit ya da pop-up sayfa düzenini kaydırmaz, yapışkan öğeler klavyeyle odaklanan öğenin üstünü kapatmaz.',
          'Duyuru şeridi ya da yapışkan alt bant kullanan her site.', 'Şeridin yeri sayfa yüklenirken ayrılır; Tab ile gezerken odaklanan bağlantı yapışkan bandın altında kalmaz.',
          'Şerit için yer sayfa çiziminde ayrılır (CLS üretmez); yapışkan şerit / bant varken scroll-padding ayarlanır ve odaklanan öğe örtülmez (WCAG 2.2 — 2.4.11).'),
        o('consent_order', 'Çerez onayıyla çakışmama', 'Çerez onay bandı açıkken pop-up açılmaz; iki katman aynı anda ekranı kaplamaz.',
          'Çerez onay platformu kullanan bütün siteler.', 'Ziyaretçi önce çerez tercihini yapar; kampanya penceresi ancak sonra, tetikleyicisi gerçekleşirse açılır.',
          'Pop-up yalnız çerez onay katmanı kapandıktan sonra çalışır; pop-up\'ın ölçüm ve sıklık betikleri onay kategorilerine bağlıdır, onay yoksa yalnız işlevsel sıklık bilgisi kullanılır.'),
        o('schedule', 'Kampanya bazlı zamanlama ve hedefleme', 'Pop-up ve şeritler kampanyaya bağlı başlangıç / bitiş tarihi, sayfa ve dil hedeflemesiyle yönetilir.',
          'Dönemsel kampanya, özel gün ve duyuru yapan siteler.', 'Panelde "Kasım İndirimi şeridi: 1–30 Kasım, yalnız /hizmetler/* sayfaları, TR" tanımlanır; 1 Aralık\'ta kendiliğinden kalkar.',
          'Kampanya kayıtları başlangıç / bitiş (Europe/Istanbul), hedef sayfa deseni, dil ve cihaz alanlarıyla panelden yönetilir; biten kampanya kendiliğinden kapanır, aynı anda tek kampanya pop-up\'ı gösterilir.'),
        o('measure', 'Performans ölçümü', 'Gösterim, kapatma, tıklama ve dönüşüm ölçülür; gerekirse varyantlar karşılaştırılır.',
          'Pop-up\'ın dönüşüme katkısının kanıtlanması gerekiyorsa.', 'Raporda "Bülten pop-up: 4.200 gösterim, 3.100 kapatma, 160 abonelik (%3,8)" görünür.',
          'popup_view, popup_close, popup_click, popup_convert olayları kampanya kimliğiyle ve analitik onayına bağlı gönderilir; olaylara kişisel veri yazılmaz.'),
        o('kvkk_form', 'Form içeriyorsa aydınlatma ve ayrı izin', 'Pop-up içinde e-posta ya da telefon toplanıyorsa aydınlatma bağlantısı ve işaretsiz ayrı pazarlama izni kutusu bulunur.',
          'Bülten, indirim kodu ya da lead toplayan pop-up\'lar.', 'Pencerede e-posta alanı, "Aydınlatma Metni" bağlantısı ve işaretsiz "Kampanya e-postası almak istiyorum" kutusu vardır.',
          'Pop-up formları Form Standardı kararına uyar: aydınlatma bağlantısı, önceden işaretsiz ayrı ticari ileti izni, onay kaydı ve sunucu doğrulaması; indirim kodu izin şartına bağlanacaksa hukuk biriminin teyidi alınır.'),
    ],
}

# =====================================================================================================
# C8 — Metrik sözlüğü (mk_measure bölümü)
# =====================================================================================================
MK_METRIC_DICT = {
    'id': 'mk_metric_dict', 'section': 'mk_measure', 'after': 'mk_ads_kpis', 'type': 'multiselect',
    'label': 'Metrik Sözlüğü', 'en': 'Metric Dictionary (Definitions, Sources & Formulas)', 'agents': [KPI, MKA, ATTR],
    'explanation': 'Raporlarda ve yönetim panelinde kullanılan her metriğin (lead, MQL, SQL, fırsat, dönüşüm oranı, atıf …) tek ve yazılı bir tanımının, veri kaynağının, formülünün ve güncellenme sıklığının olmasını sağlar. Böylece pazarlama, satış ve yönetim aynı sayıyı aynı anlamda konuşur.',
    'scenario': 'Raporlar birden çok kaynaktan (analitik, reklam platformları, CRM) besleniyorsa; ekipler aynı metrik için farklı sayılar görüyorsa ya da dashboard kuruluyorsa.',
    'example': 'Dashboard\'daki "MQL" kutusunun yanındaki ⓘ işaretine gelince "Lead skoru ≥ 60 ve hedef sektörde · Kaynak: CRM · Günde bir güncellenir · Son güncelleme 06:00" açıklaması görünür.',
    'rule': 'Metrik sözlüğü: {labels}. Her metriğin tanımı, veri kaynağı, formülü, güncellenme sıklığı ve sahibi tek bir sözlükte tutulur; raporlar, dashboard ve Looker / Data Studio raporları bu tanımlardan hesaplanır, aynı metrik farklı yerde farklı formülle hesaplanmaz.',
    'options': [
        o('funnel_defs', 'Huni tanımları: lead, MQL, SQL, fırsat, müşteri', 'Lead, pazarlamaya uygun lead (MQL), satışa uygun lead (SQL), fırsat (opportunity / deal) ve müşterinin hangi koşulla oluştuğu yazılı tanımlanır.',
          'Pazarlama ve satışın aynı huniyi izlediği, lead\'in satışa devredildiği her işletme.', 'Sözlükte "SQL: satış temsilcisinin ilk görüşmeden sonra bütçe ve ihtiyacı doğruladığı MQL" tanımı durur.',
          'Huni aşamaları CRM durum alanlarına birebir eşlenir; aşama geçişi tarih-saatle kaydedilir, geriye dönük tanım değişikliği yapılırsa eski dönemler eski tanımla raporlanır ve not düşülür.'),
        o('conversion_rate', 'Dönüşüm oranı tanımları', 'Her dönüşüm oranının payı, paydası ve birimi (oturum, kullanıcı, lead) belirlenir.',
          'Farklı araçların farklı dönüşüm oranı gösterdiği durumlar.', '"Form dönüşüm oranı = form_submit yapan tekil kullanıcı / formu görüntüleyen tekil kullanıcı (son 28 gün)".',
          'Her oran pay / payda / birim / dönem olarak tanımlanır; oturum ve kullanıcı bazlı oranlar aynı başlık altında karıştırılmaz, paydası sıfır olan dönemde oran "veri yok" gösterilir.'),
        o('attribution', 'Atıf (attribution) modeli ve dönüşüm penceresi', 'Dönüşümün hangi kanala yazılacağı (son tıklama, veri odaklı vb.) ve geriye dönük kaç günlük pencere kullanılacağı tanımlanır.',
          'Birden çok reklam ve organik kanalın aynı dönüşüme katkı verdiği projeler.', 'Sözlükte "Kanal raporu: GA4 veri odaklı atıf, 30 günlük tıklama penceresi; reklam platformlarının kendi raporları ayrı gösterilir" yazar.',
          'Raporun kullandığı atıf modeli ve penceresi metrikle birlikte gösterilir; reklam platformlarının kendi atfıyla analitik atfı toplanıp tek sayı yapılmaz, model değişikliği tarihli not olarak kaydedilir.'),
        o('source', 'Her metriğin veri kaynağı', 'Her metriğin hangi sistemden geldiği (GA4, Search Console, reklam platformu, CRM, ödeme sistemi) belirtilir.',
          'Birden çok sistemden beslenen her rapor.', '"Gelir: ödeme sistemi (iadeler düşülmüş) — GA4 purchase geliri değil" notu.',
          'Her metrikte birincil kaynak tek sistemdir; aynı metrik ikinci bir kaynaktan gösterilecekse ayrı adla ("GA4 geliri") gösterilir.'),
        o('formula', 'Hesaplama formülü ve filtreler', 'Formül, hariç tutulanlar (iç trafik, test siparişleri, bot, iadeler) ve para birimi / vergi durumu yazılır.',
          'Sayıların denetlenebilir olması gereken yönetim raporları.', '"ROAS = (KDV hariç, iade düşülmüş gelir) / reklam harcaması; iç IP ve test siparişleri hariç".',
          'Formüller sözlükte metin ve sorgu / hesap tanımı olarak tutulur ve sürümlenir; iç trafik ve test verisi filtreleri bütün raporlarda aynıdır, para birimi ve KDV durumu her parasal metrikte belirtilir.'),
        o('refresh', 'Güncellenme sıklığı ve veri tazeliği', 'Her metriğin ne sıklıkla güncellendiği ve kaynağın doğal gecikmesi (ör. Search Console verisinin birkaç gün geriden gelmesi) belirtilir.',
          'Gerçek zamanlı sanılan ama günlük güncellenen göstergelerin olduğu dashboard\'lar.', 'Kutunun altında "Günlük · Son güncelleme: bugün 06:00 · Kaynak gecikmesi: 2–3 gün" yazar.',
          'Her metrikte güncellenme sıklığı ve son başarılı güncelleme zamanı gösterilir; kaynağın doğal gecikmesi içindeki günler "kesinleşmedi" olarak işaretlenir.'),
        o('latency_alert', 'Veri gecikmesi ve entegrasyon hatası uyarısı', 'Bir kaynaktan beklenen sürede veri gelmezse ya da entegrasyon hata verirse ilgili metrikte ve sorumluya uyarı çıkar.',
          'Otomatik veri aktarımı (API, bağlayıcı) kullanan her rapor.', 'Dashboard\'da "Google Ads verisi 26 saattir güncellenmedi — bağlantı hatası" uyarısı ve sarı işaret görünür.',
          'Her kaynak için en geç güncellenme eşiği tanımlanır; eşik aşılınca metrik bayat olarak işaretlenir, sorumluya bildirim gider ve eksik dönem sıfır değer gibi gösterilmez.'),
        o('single_source', 'Tek doğru kaynak (single source of truth)', 'Her metrik tek yerde hesaplanır; diğer raporlar hesaplamayı tekrar etmez, bu hesaplanmış değeri kullanır.',
          'Pazarlama, satış ve yönetimin farklı araçlarda rapor aldığı kurumlar.', 'Aylık yönetim raporundaki ve dashboard\'daki "Yeni müşteri" sayısı aynı tablodan gelir, birebir tutar.',
          'Metrikler ortak hesaplama katmanında (görünüm / tablo / anlamsal katman) üretilir; dashboard, dışa aktarma ve raporlar bu katmandan okur, elle düzeltilmiş tablo kaynak olarak kullanılmaz.'),
        o('visible_def', 'Tanımın dashboard\'da görünmesi', 'Her metrik kutusunda tanım, kaynak ve son güncelleme bilgisine bir dokunuşla ulaşılır.',
          'Raporu farklı ekiplerin okuduğu, tanımın unutulabildiği durumlar.', 'Grafik başlığının yanındaki ⓘ tıklanınca tanım, formül ve kaynak açılır.',
          'Tanım bilgisi sözlükten okunur (elle kopyalanmaz); bilgi açıklaması klavye ve ekran okuyucuyla erişilebilir.'),
        o('owner_version', 'Metrik sahibi ve tanım değişiklik geçmişi', 'Her metriğin bir sahibi vardır; tanım değişiklikleri tarih, gerekçe ve onaylayanla kaydedilir.',
          'Tanımların zamanla değiştiği ve geçmiş dönemlerin karşılaştırıldığı kurumlar.', 'Sözlükte "MQL tanımı 1 Mart 2027\'de değişti (skor eşiği 50 → 60) · Onaylayan: Pazarlama Müdürü" satırı durur.',
          'Tanım değişikliği sahibinin onayıyla yapılır ve sürümlenir; raporlarda tanım değişikliği tarihi işaretlenir, eski ve yeni tanımla hesaplanan dönemler karşılaştırılırken uyarı gösterilir.'),
    ],
}

# =====================================================================================================
# C1 — Mobil Uygulama (yeni bölüm)
# =====================================================================================================
SECTION = {
    'id': 'mobile_app', 'group': 'Teknik Mimari', 'icon': '▯',
    'name': 'Mobil Uygulama', 'en': 'Mobile App (PWA, React Native, Flutter, Native)',
    'desc': 'Projenin responsive web dışında bir mobil uygulaması olup olmayacağını; varsa teknolojisini, kullanıcı kitlesini, özelliklerini, güvenlik, mağaza yayını ve ölçüm kurallarını belirler',
    'guide': {
        'purpose': 'Mobil uygulama, web platformuyla aynı iş mantığını ve aynı API\'yi kullanan tamamlayıcı bir kanaldır: yöneticiler ve satış ekipleri için dashboard, lead takibi ve bildirim; müşteriler ve ziyaretçiler için içerik, form, portal işlemleri ve anlık bildirim sunabilir. Bu bölüm önce mobil uygulamaya gerçekten ihtiyaç olup olmadığını ve hangi teknolojiyle yapılacağını, sonra kimin için olduğunu, hangi özellikleri içereceğini, cihazda veriyi nasıl koruyacağını, mağazalara nasıl yayınlanacağını ve nasıl ölçüleceğini karara bağlar. Mobil uygulama ayrı bir veri kaynağı değildir; bütün veri merkezi API\'den gelir, yetki sunucuda denetlenir.',
        'criteria': [
            'Önce responsive web ve PWA (yüklenebilir web uygulaması) ile ihtiyacın karşılanıp karşılanmadığına bakılır; mağaza varlığı, arka planda çalışma, cihaz özelliklerine derin erişim ya da güçlü çevrimdışı çalışma gerekiyorsa yerel / çapraz platform uygulama seçilir.',
            'Uygulama yalnız merkezi API üzerinden çalışır; web ve mobil aynı iş kurallarını, aynı yetki denetimini ve aynı veri modelini kullanır, iş mantığı uygulamaya kopyalanmaz.',
            'Hedef kitle (yönetici / ekip, müşteri, ziyaretçi, saha ekibi) ayrı ayrı belirlenir; her kitlenin ekranları ve yetkileri ayrıdır, ekip uygulaması herkese açık mağazada olsa da yalnız yetkili hesapla açılır.',
            'Cihazda saklanan token ve hassas veri işletim sisteminin güvenli deposunda (iOS Keychain, Android Keystore) tutulur; güvenlik gereksinimleri OWASP MASVS\'e göre doğrulanır.',
            'Paylaşılan her içeriğin bir web adresi vardır; derin bağlantılar (Universal Links / App Links) doğrulanmış alan adıyla kurulur, uygulama yüklü değilse aynı adres web sayfasını açar.',
            'Mağaza gizlilik beyanları (App Store gizlilik etiketi, Google Play Veri güvenliği bölümü), gizlilik politikası ve uygulama içinden hesap silme yayından önce hazırdır; analitik ve bildirim izinleri kullanıcı onayına bağlıdır.',
        ],
        'pitfalls': [
            'Web sitesini olduğu gibi sarmalayıp mağazaya koymak: Apple, yeniden paketlenmiş web sitesi niteliğindeki uygulamaları "asgari işlevsellik" kuralıyla reddedebilir.',
            'API anahtarı, gizli değer ya da yetki kararını uygulama paketine koymak: paket açılıp incelenebilir; gizli değer ve yetki kararı sunucuda kalmalıdır.',
            'Token\'ları düz yerel depoda (AsyncStorage, SharedPreferences, localStorage) saklamak; cihaz kaybında oturum ele geçirilebilir.',
            'Eski uygulama sürümlerini düşünmeden API değiştirmek: kullanıcılar güncellemeyi geciktirir, eski sürüm bozulur; API sürümlenmeli ve asgari sürüm kontrolü kurulmalıdır.',
            'Anlık bildirimi pazarlama için izinsiz kullanmak ya da bildirime kişisel / gizli bilgi yazmak: mağaza kurallarına ve kişisel veri mevzuatına aykırıdır, bildirim kilit ekranında görünür.',
            'Artık kapatılmış hizmetlere dayanmak (ör. Firebase Dynamic Links 25 Ağustos 2025\'te kapandı); derin bağlantılar kurumun kendi alan adıyla App Links / Universal Links olarak kurulmalıdır.',
        ],
        'resources': [
            {'title': 'web.dev — Progressive Web Apps', 'url': 'https://web.dev/explore/progressive-web-apps', 'note': 'PWA\'nın ne olduğu, yüklenebilirlik, çevrimdışı çalışma ve service worker rehberi.'},
            {'title': 'MDN — Web application manifest', 'url': 'https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest', 'note': 'PWA\'nın ad, simge, başlangıç adresi ve görüntü modunu tanımlayan manifest dosyasının alanları.'},
            {'title': 'Apple — App Store Review Guidelines', 'url': 'https://developer.apple.com/app-store/review/guidelines/', 'note': 'Asgari işlevsellik (4.2), anlık bildirim (4.5.4), hesap silme ve gizlilik kuralları dahil App Store inceleme kuralları.'},
            {'title': 'Google Play — Data safety bölümü', 'url': 'https://support.google.com/googleplay/android-developer/answer/10787469', 'note': 'Google Play mağaza sayfasındaki Veri güvenliği beyanının nasıl doldurulacağı.'},
            {'title': 'OWASP MASVS', 'url': 'https://mas.owasp.org/MASVS/', 'note': 'Mobil uygulama güvenlik doğrulama standardı: depolama, kripto, kimlik doğrulama, ağ, platform, kod, dayanıklılık ve gizlilik.'},
            {'title': 'Android — Deep links ve App Links', 'url': 'https://developer.android.com/training/app-links', 'note': 'Derin bağlantı türleri ve alan adı doğrulamalı Android App Links kurulumu.'},
            {'title': 'Apple — Supporting universal links in your app', 'url': 'https://developer.apple.com/documentation/xcode/supporting-universal-links-in-your-app', 'note': 'iOS Universal Links için ilişkili alan adı (apple-app-site-association) kurulumu.'},
            {'title': 'React Native — Resmî dokümantasyon', 'url': 'https://reactnative.dev/docs/getting-started', 'note': 'JavaScript / TypeScript ile iOS ve Android uygulaması geliştirme.'},
            {'title': 'Flutter — Resmî dokümantasyon', 'url': 'https://docs.flutter.dev/', 'note': 'Dart ile tek kod tabanından iOS ve Android uygulaması geliştirme.'},
        ],
    },
}

MOBILE_FIELDS = [
    {'id': 'mobile_app', 'section': 'mobile_app', 'type': 'select', 'label': 'Mobil Uygulama Yaklaşımı', 'en': 'Mobile App Approach', 'agents': [SWE, PM],
     'explanation': 'Projenin responsive web dışında bir mobil uygulaması olup olmayacağını ve varsa hangi teknolojiyle yapılacağını belirler. "Mobil uygulama yok" seçilirse bu bölümdeki diğer kararlar gizlenir ve projeye mobil uygulama kuralı eklenmez.',
     'scenario': 'Yönetici / ekip için hızlı erişim (lead, dashboard, bildirim), müşteri için uygulama içi portal ya da mağaza varlığı isteniyorsa; çoğu tanıtım sitesinde responsive web yeterlidir.',
     'example': 'React Native seçilirse satış ekibi telefondan lead listesini görür, lead\'e not ekler ve yeni lead atandığında anlık bildirim alır; uygulama App Store ve Google Play\'dedir.',
     'rule': 'Mobil uygulama yaklaşımı: {label}. Mobil uygulama ayrı veri kaynağı değildir: bütün veri ve iş kuralları merkezi API\'den gelir, yetki her istekte sunucuda denetlenir, mobil için ayrı ve sürümlü API uç noktaları gerekiyorsa API Standartları\'na göre sürümlenir.',
     'options': [
         o('none', 'Mobil uygulama yok (yalnız responsive web)', 'Mobil kullanıcılar siteyi tarayıcıdan kullanır; ayrı uygulama geliştirilmez.',
           'Tanıtım, kurumsal ve içerik siteleri; mobil uygulamaya özgü bir ihtiyaç (bildirim, çevrimdışı, cihaz özelliği) yoksa.', 'Telefonda site responsive açılır; mağazada uygulama yoktur.',
           'Mobil uygulama, mağaza hesabı ve mobil SDK eklenmez; mobil deneyim responsive web ve performans kurallarıyla sağlanır.'),
         o('pwa', 'PWA (yüklenebilir web uygulaması)', 'Web sitesi manifest ve service worker ile ana ekrana eklenebilir, uygulama gibi tam ekran açılır, sınırlı çevrimdışı çalışır ve web anlık bildirimi alabilir.',
           'Uygulama hissi ve ana ekran simgesi istenen ama mağaza zorunluluğu olmayan, bütçesi sınırlı projeler; müşteri portalı ve ekip panelleri.', 'Kullanıcı tarayıcıda "Ana ekrana ekle" der; site kendi simgesiyle, adres çubuğu olmadan açılır.',
           'Web uygulaması manifest (ad, simgeler, start_url, display) ve service worker ile yüklenebilir yapılır; çevrimdışı önbellek yalnız herkese açık ve kişisel olmayan içerikle sınırlıdır, oturumlu sayfalar önbelleğe alınmaz. Mağaza yayını kararları uygulanmaz; iOS\'ta web anlık bildirimi yalnız ana ekrana eklenmiş web uygulamasında çalışır.'),
         o('react_native', 'React Native', 'JavaScript / TypeScript ile iOS ve Android için tek kod tabanından yerel bileşenli uygulama.',
           'Web ekibinin TypeScript / React bildiği, web ile tip ve doğrulama kodunun paylaşılmak istendiği projeler.', 'Uygulama App Store ve Google Play\'de yayınlanır; web ile aynı API şeması ve doğrulama kuralları kullanılır.',
           'Uygulama React Native + TypeScript ile, web ile ortak tip tanımları ve API istemcisi paylaşılarak geliştirilir; iş kuralı istemciye kopyalanmaz.'),
         o('flutter', 'Flutter', 'Dart ile iOS ve Android için tek kod tabanından, kendi çizim motoruyla uygulama.',
           'Mobil ağırlıklı, özel tasarımlı arayüzü olan ve web kod paylaşımının önemli olmadığı projeler.', 'Uygulama iki mağazada aynı görünümle yayınlanır; tasarım token\'ları uygulama temasına aktarılır.',
           'Uygulama Flutter (Dart) ile geliştirilir; API istemcisi API şemasından (OpenAPI) üretilir, tasarım token\'ları web ile aynı kaynaktan tema olarak aktarılır.'),
         o('native', 'Yerel (Swift + Kotlin)', 'iOS için Swift, Android için Kotlin ile iki ayrı yerel uygulama.',
           'Cihaz özelliklerine derin erişim, en yüksek performans ya da platforma özgü deneyim gereken, iki ayrı mobil ekibi olan projeler.', 'iOS ve Android uygulamaları ayrı ekiplerce geliştirilir, aynı API\'yi kullanır.',
           'iOS Swift / SwiftUI, Android Kotlin / Jetpack Compose ile geliştirilir; iki platform aynı API sözleşmesine ve aynı özellik listesine bağlıdır, sürüm farkları takip edilir.'),
         o('wrapper', 'Capacitor ya da benzeri sarmalayıcı', 'Var olan web uygulaması yerel bir kabuk içinde paketlenir; eklentilerle kamera, bildirim gibi cihaz özelliklerine erişilir.',
           'Web uygulaması hazır olan ve mağazada bulunması gereken, cihaz özelliği ihtiyacı sınırlı projeler.', 'Müşteri portalı Capacitor ile paketlenip mağazaya konur; anlık bildirim ve kamera eklentiyle çalışır.',
           'Web uygulaması Capacitor (ya da eşdeğeri) ile paketlenir; uygulama yeniden paketlenmiş web sitesinden öte işlev sunmalıdır (yerel bildirim, çevrimdışı, cihaz özellikleri), aksi hâlde mağaza incelemesinde reddedilebilir. Uzaktan web adresi yüklemek yerine uygulama varlıkları pakete gömülür.'),
     ]},

    {'id': 'mobile_audience', 'section': 'mobile_app', 'type': 'multiselect', 'label': 'Mobil Uygulamanın Kullanıcıları', 'en': 'Mobile App Audience & Use Cases', 'agents': [PM, SWE], 'showIf': MOB_ON,
     'explanation': 'Mobil uygulamanın kimin için olduğunu ve her kitlenin hangi işleri yapacağını belirler. Her kitlenin ekranları, yetkileri ve bildirimleri ayrıdır.',
     'scenario': 'Ekip uygulaması ile müşteri uygulamasının ayrı mı tek mi olacağına, hangi modüllerin mobilde açılacağına karar verirken.',
     'example': 'Yönetici dashboard\'u ve lead bildirimlerini görür; müşteri aynı uygulamada siparişlerini, rezervasyonlarını ve destek taleplerini izler.',
     'rule': 'Mobil uygulama kullanıcıları ve kullanım senaryoları: {labels}. Her kitle yalnız kendi rolünün yetkili olduğu veriyi görür; ekip ve müşteri ekranları aynı uygulamadaysa rol ayrımı sunucuda yapılır, istemcide gizlemek yetki sayılmaz.',
     'recommend': {'field': 'modules_extra', 'map': {'crm': ['sales'], 'portal': ['customer'], 'ecommerce': ['customer'], 'booking': ['customer'], 'lms': ['learner'], 'community': ['public']}},
     'options': [
         o('admin', 'Yönetici: dashboard, rapor ve onaylar', 'Yöneticiler temel performans metriklerini, uyarıları ve bekleyen onayları mobilde görür.',
           'Yöneticilerin masa başında olmadan durumu izlemesi isteniyorsa.', 'Genel müdür sabah telefonundan dünkü lead, satış ve trafik özetini görür, bekleyen indirimi onaylar.',
           'Mobil dashboard web dashboard\'uyla aynı metrik tanımlarını kullanır (bkz. Metrik Sözlüğü); grafikler küçük ekrana uyarlanır, onay işlemleri webdekiyle aynı yetki ve onay kurallarından geçer.'),
         o('sales', 'Satış ekibi: lead ve CRM işlemleri', 'Satış ekibi lead listesini, detayını görür; durum günceller, not ekler, atama yapar, hızlı arama / e-posta / WhatsApp aksiyonu alır.',
           'Sahada ya da hareket hâlinde çalışan satış ekipleri.', 'Temsilci yeni atanan lead\'in bildirimine dokunur, lead kartı açılır, "Ara" ile müşteriyi arar ve görüşme notunu girer.',
           'Lead ve CRM ekranları CRM API\'sini kullanır; temsilci yalnız kendine ya da ekibine atanmış kayıtları görür, kişisel veri cihazda yalnız çevrimdışı kararı izin veriyorsa ve şifreli tutulur.'),
         o('field', 'Saha ekibi: görev, randevu ve konum', 'Saha personeli günlük görevlerini, randevularını ve rotasını görür; işi fotoğraf / imza ile kapatır.',
           'Servis, kurulum, bakım ya da saha satışı yapan işletmeler.', 'Teknisyen günün 5 servis randevusunu harita üzerinde görür, işi bitirince fotoğraf ekleyip "Tamamlandı" der.',
           'Görev ve randevu verisi çevrimdışı çalışabilecek biçimde senkronize edilir; konum yalnız görev sırasında ve kullanıcının izniyle alınır.'),
         o('customer', 'Müşteri: portal, sipariş, rezervasyon, destek', 'Müşteri siparişlerini, rezervasyonlarını, aboneliğini, faturalarını ve destek taleplerini görür, işlem yapar.',
           'Müşteri portalı, e-ticaret, rezervasyon ya da abonelik modülü olan projeler.', 'Müşteri rezervasyonunu uygulamadan erteler, açık destek talebine dosya ekleyerek yanıt verir.',
           'Müşteri ekranları müşteri portalıyla aynı API ve yetki kurallarını kullanır (her istekte sahiplik denetimi); uygulamadaki işlemler CRM müşteri zaman çizelgesine yazılır.'),
         o('learner', 'Öğrenci / katılımcı: eğitim ve sertifika', 'Kullanıcı eğitimlerini izler, sınav çözer, ödev gönderir, sertifikasını görür.',
           'Eğitim (LMS) modülü olan projeler.', 'Katılımcı dersi telefondan izler, kaldığı yer webde de aynı görünür.',
           'Eğitim ilerlemesi web ile aynı kayıttan okunur ve yazılır; korumalı video içerikleri süreli imzalı bağlantıyla verilir.'),
         o('public', 'Ziyaretçi: içerik, form ve kampanyalar', 'Hizmet, ürün, blog ve kampanya içerikleri uygulamada okunur; form doldurulur, lead oluşturulur.',
           'Uygulamanın içerik ve lead kanalı olarak da kullanılacağı projeler.', 'Ziyaretçi uygulamada blog yazısını okur, "Teklif al" formunu doldurur; lead CRM\'e "Kaynak: mobil uygulama" ile düşer.',
           'İçerik CMS API\'sinden gelir, her içerik web canonical adresiyle ilişkilidir; uygulama içi formlar Form Standardı kurallarına uyar ve kaynak olarak uygulama sürümü kaydedilir.'),
     ]},

    {'id': 'mobile_features', 'section': 'mobile_app', 'type': 'multiselect', 'label': 'Mobil Uygulama Özellikleri', 'en': 'Mobile App Features', 'agents': [APPDEV, API], 'showIf': MOB_ON,
     'explanation': 'Mobil uygulamada bulunacak cihaz ve etkileşim özelliklerini belirler: anlık bildirim, bildirim merkezi, çevrimdışı çalışma, derin bağlantılar, biyometrik giriş, kamera, konum ve tema.',
     'scenario': 'Uygulamanın web\'den farkını oluşturan özellikler seçilirken; her özellik ayrı izin, gizlilik beyanı ve test yükü getirir.',
     'example': 'Lead atanınca telefon bildirimi gelir, dokununca lead kartı açılır; paylaşılan blog bağlantısı uygulama yüklüyse uygulamada, değilse webde açılır.',
     'rule': 'Mobil uygulama özellikleri: {labels}. Her cihaz izni (bildirim, kamera, konum) yalnız ilgili özellik ilk kullanıldığında ve gerekçesi gösterilerek istenir; izin reddedilirse uygulama temel işlevini sürdürür.',
     'options': [
         o('push', 'Anlık bildirim (push)', 'Uygulamaya sunucudan anlık bildirim gönderilir; bildirimler kullanıcı segmentine, duruma ve kampanyaya göre hedeflenir.',
           'Lead ataması, sipariş / randevu durumu, destek yanıtı, hatırlatma ve izinli kampanya bildirimleri.', '"Size yeni bir lead atandı: ABC Ltd." bildirimine dokununca lead detayı açılır.',
           'Bildirimler sunucudan bildirim servisiyle (APNs, Firebase Cloud Messaging, web push) gönderilir; cihaz belirteçleri kullanıcıya bağlı tutulur, çıkışta silinir. İşlem bildirimleri ile pazarlama bildirimleri ayrı izin kategorisidir; pazarlama bildirimi yalnız açık onayla gönderilir, uygulamada kapatılabilir (6563 sayılı Kanun kapsamı hukuk birimiyle teyit edilir). Bildirim metnine gizli / hassas kişisel veri yazılmaz.'),
         o('inbox', 'Uygulama içi bildirim merkezi', 'Gelen bildirimler uygulama içinde listelenir, okundu / okunmadı durumu tutulur, her bildirim ilgili kayda yönlendirir.',
           'Bildirimlerin kaçırılmaması ve geçmişe dönük görülmesi gerekiyorsa.', 'Zil simgesinde "3" rozeti; listede "Teklifiniz görüntülendi", "Destek talebiniz yanıtlandı" satırları.',
           'Bildirim merkezi sunucudaki bildirim kayıtlarından okunur (cihazda yalnız önbellek); her bildirimin hedef kaydı açılırken yetki yeniden denetlenir.'),
         o('offline', 'Çevrimdışı çalışma ve senkronizasyon', 'Bağlantı yokken temel ekranlar önbellekten açılır, yapılan değişiklikler kuyruğa alınır ve bağlantı gelince gönderilir.',
           'Saha ekipleri, zayıf bağlantılı ortamlar.', 'Bodrum kattaki teknisyen işi "Tamamlandı" yapar; bağlantı gelince kayıt sunucuya gider, çakışma varsa uyarı çıkar.',
           'Çevrimdışı veri cihazda şifreli tutulur ve kapsamı en az veriyle sınırlanır; kuyruktaki her işlem idempotency anahtarıyla gönderilir, sunucuda sürüm karşılaştırmasıyla çakışma tespit edilir ve kullanıcıya gösterilir (sessiz üzerine yazma yok).'),
         o('deep_links', 'Derin bağlantı: Universal Links ve App Links', 'Web adresine tıklanınca uygulama yüklüyse ilgili ekran açılır, değilse aynı adres web sayfasını açar.',
           'Paylaşılan içerik, e-posta / SMS bağlantıları ve bildirimlerin doğrudan ilgili ekrana gitmesi isteniyorsa.', 'E-postadaki /siparis/12345 bağlantısı uygulamada sipariş ekranını, uygulama yoksa web sayfasını açar.',
           'Derin bağlantılar kurumun kendi alan adıyla, alan adı doğrulamalı iOS Universal Links (apple-app-site-association) ve Android App Links (assetlinks.json) olarak kurulur; özel URL şeması yalnız yedek olarak kullanılır. Derin bağlantı parametreleri doğrulanır, açılan kayıtta yetki yeniden denetlenir.'),
         o('canonical_share', 'Paylaşılan içeriğin web canonical adresine bağlanması', 'Uygulamada paylaşılan her içerik web\'deki canonical adresiyle paylaşılır; uygulamadaki içerik ile web sayfası eşleşir.',
           'Uygulamada içerik (blog, ürün, hizmet) gösterilen projeler.', 'Ürün ekranındaki "Paylaş" düğmesi https://ornek.com/urunler/crm adresini paylaşır.',
           'Her mobil içerik kaydı web canonical adresini taşır; paylaşımlar bu adresle yapılır, paylaşılan adres Open Graph etiketleriyle web\'de doğru önizleme verir. Uygulamadaki içerik web sayfasıyla eşleştiği için arama motorları içeriği web adresinden dizine ekler.'),
         o('biometric', 'Biyometrik giriş ve kilit', 'Parmak izi ya da yüz tanıma ile uygulama kilidi açılır ya da hassas işlem onaylanır.',
           'Ekip uygulamaları ve kişisel / finansal veri gösteren müşteri uygulamaları.', 'Uygulama açılırken Face ID ister; onay işleminden önce parmak izi doğrulanır.',
           'Biyometrik doğrulama işletim sisteminin yerel API\'siyle yapılır, biyometrik veri uygulamaya ya da sunucuya hiç gelmez; biyometri cihazdaki güvenli depodaki anahtarı açar, sunucu oturumu yerine geçmez.'),
         o('camera_files', 'Kamera ve dosya ekleme', 'Uygulamadan fotoğraf çekilip ya da dosya seçilip forma, destek talebine veya göreve eklenir.',
           'Destek, saha işi, belge yükleme ve başvuru senaryoları.', 'Müşteri destek talebine telefonundan arıza fotoğrafı ekler.',
           'Yüklenen dosyalar Dosya Yükleme Standardı\'na uyar (sunucuda tür / boyut denetimi, özel depo); fotoğraflardan konum (EXIF) bilgisi yüklemeden önce silinir.'),
         o('location', 'Konum', 'Uygulama kullanıcının konumunu yakındaki şube, saha görevi ya da rota için kullanır.',
           'Şube bulucu, saha ekibi ve teslimat senaryoları.', '"Size en yakın şube: Kadıköy (1,2 km)" kartı görünür.',
           'Konum yalnız ön planda ve ilgili özellik kullanılırken, açık izinle alınır; arka plan konumu yalnız saha görevi gibi zorunlu durumda ve ayrıca gerekçelendirilerek istenir, konum geçmişi saklama süresine tabidir.'),
         o('theming', 'Çoklu dil ve marka / tema desteği', 'Uygulama web ile aynı dilleri ve kurumsal tema kurallarını (renk, yazı tipi, logo) destekler; çok markalı yapıda markaya göre tema değişir.',
           'Çok dilli ya da çok markalı (white-label) projeler.', 'Uygulama cihaz dili İngilizceyse İngilizce açılır; ikinci markanın uygulamasında aynı kod farklı logo ve renkle çalışır.',
           'Metinler çeviri anahtarlarıyla, tema web ile aynı tasarım token\'larından üretilir; tema değişikliği erişilebilirlik kontrastını bozmaz, sistem yazı boyutu büyütme ve koyu mod desteklenir.'),
     ]},

    {'id': 'mobile_security', 'section': 'mobile_app', 'type': 'multiselect', 'label': 'Mobil Uygulama Güvenliği', 'en': 'Mobile App Security (OWASP MASVS)', 'agents': [APPSEC, CIAM], 'showIf': MOB_ON,
     'explanation': 'Mobil uygulamada oturumun, cihazda saklanan verinin ve API erişiminin nasıl korunacağını belirler. Uygulama paketi kullanıcının cihazındadır ve incelenebilir; bu yüzden güvenlik kararı sunucuda verilir, cihaz tarafı ek koruma sağlar.',
     'scenario': 'Kişisel, finansal ya da kurumsal veri gösteren her mobil uygulamada; özellikle ekip ve müşteri uygulamalarında.',
     'example': 'Token Keychain / Keystore\'da tutulur; kullanıcı panelden "Bütün cihazlarda oturumu kapat" deyince telefondaki oturum da sona erer.',
     'rule': 'Mobil uygulama güvenliği: {labels}. Uygulama paketine API anahtarı, gizli değer ya da yetki kararı konmaz; yetki her istekte sunucuda denetlenir, uygulama içi loglara token ve kişisel veri yazılmaz.',
     'options': [
         o('secure_storage', 'Token\'ların güvenli depoda saklanması (Keychain / Keystore)', 'Oturum belirteçleri ve hassas veriler iOS Keychain ve Android Keystore destekli güvenli depoda tutulur.',
           'Oturum açılan her mobil uygulama.', 'Telefon başkasının eline geçse bile token düz dosyadan okunamaz.',
           'Token ve hassas veri yalnız işletim sisteminin güvenli deposunda tutulur; AsyncStorage, SharedPreferences gibi düz depolar kullanılmaz. PWA\'da token JavaScript\'in okuyamadığı HttpOnly + Secure çerezde tutulur.'),
         o('token_flow', 'Kısa ömürlü erişim belirteci ve PKCE', 'Erişim belirteci kısa ömürlüdür, yenileme belirteci her kullanımda değişir; tarayıcı tabanlı giriş PKCE ile yapılır.',
           'Oturum açılan her mobil uygulama; tekil oturum açma (SSO) ya da sosyal giriş varsa özellikle.', 'Erişim belirteci 15 dakikada yenilenir; çalınan eski yenileme belirteci kullanılınca bütün oturum düşer.',
           'Erişim belirteci kısa ömürlü, yenileme belirteci döndürmeli (rotation) ve yeniden kullanım tespitlidir; OAuth girişleri sistem tarayıcısında PKCE ile yapılır (gömülü web görünümünde parola alınmaz).'),
         o('session_control', 'Uzaktan oturum kapatma ve anormallikte zorunlu çıkış', 'Kullanıcı ya da yönetici cihaz oturumlarını görür ve kapatır; şüpheli durumda (parola değişimi, rol kaldırma, anormal konum) oturum sunucudan sonlandırılır.',
           'Ekip uygulamaları ve hassas veri gösteren müşteri uygulamaları.', 'İşten ayrılan çalışanın rolü kaldırılınca telefonundaki uygulama bir sonraki istekte giriş ekranına döner.',
           'Cihaz oturumları sunucuda listelenir ve iptal edilebilir; parola değişimi, rol / yetki kaldırma ve anormal kullanım oturumları sonlandırır, kullanıcı yeni cihaz girişinde bilgilendirilir.'),
         o('action_log', 'Uygulama içi işlem kaydı', 'Mobilden yapılan kritik işlemler (durum değişikliği, onay, dışa aktarma) kim, ne zaman, hangi cihaz / sürüm bilgisiyle kaydedilir.',
           'Ekip uygulamaları; denetim gerektiren işlemler.', 'Lead durum değişikliği kaydında "Mobil · iOS · v2.3.1" bilgisi görünür.',
           'İşlem kaydı sunucuda, web işlemleriyle aynı denetim kaydına kanal ve uygulama sürümüyle yazılır; kayıtta kişisel veri ayrıntısı en az tutulur.'),
         o('no_secrets', 'Uygulama paketinde gizli değer yok', 'API anahtarı, istemci gizli anahtarı ya da üçüncü taraf parolası uygulama paketine konmaz.',
           'Her mobil uygulama.', 'Harita ve ödeme anahtarları yalnız sunucuda; uygulama sunucudan kısa ömürlü, kısıtlı belirteç alır.',
           'Gizli değer gerektiren üçüncü taraf çağrıları sunucu üzerinden yapılır; istemcide bulunması zorunlu anahtarlar (ör. harita) paket adı / imza ile kısıtlanır ve kota sınırlanır. Derleme hattında gizli değer taraması yapılır.'),
         o('pinning', 'Sertifika sabitleme (certificate pinning)', 'Uygulama yalnız beklenen sunucu sertifikasına / genel anahtarına bağlanır; araya giren sahte sertifikalı bağlantı reddedilir.',
           'Finans, sağlık gibi yüksek riskli uygulamalar.', 'Kullanıcının cihazına sahte kök sertifika yüklense bile uygulama API trafiği okunamaz.',
           'Sabitleme genel anahtar düzeyinde ve en az bir yedek anahtarla yapılır; sertifika yenileme planı sabitlemeyle birlikte yönetilir (yanlış sabitleme uygulamayı kilitler). PWA\'da uygulanmaz.'),
         o('root_detect', 'Jailbreak / root ve kurcalama tespiti', 'Uygulama kırılmış (jailbreak / root) cihazı, hata ayıklayıcıyı ya da değiştirilmiş paketi tespit eder ve riskli işlemleri kısıtlar.',
           'Ödeme, finans ya da yüksek değerli işlem yapan uygulamalar.', 'Root\'lu cihazda uygulama uyarı gösterir, ödeme ve onay işlemlerini kapatır.',
           'Tespit sonucu sunucuya bildirilir ve risk değerlendirmesinde kullanılır, tek başına güvenlik sınırı sayılmaz; platformun bütünlük doğrulama servisleri (Play Integrity, App Attest) kullanılabilir. PWA\'da uygulanmaz.'),
         o('screen_protect', 'Hassas ekranlarda görüntü koruması', 'Hassas ekranlarda ekran görüntüsü engellenir ya da uygulama arka plana alınınca içerik bulanıklaştırılır.',
           'Kişisel, finansal ya da sağlık verisi gösteren ekranlar.', 'Uygulama değiştiricide müşteri bilgileri yerine bulanık görüntü görünür.',
           'Hassas ekranlarda Android\'de ekran görüntüsü koruması, iOS\'ta arka plana geçişte içerik gizleme uygulanır; kapsam ekran listesiyle belirlenir.'),
         o('masvs', 'OWASP MASVS ile doğrulama', 'Uygulamanın güvenliği OWASP Mobil Uygulama Güvenliği Doğrulama Standardı (MASVS) kontrollerine göre test edilir.',
           'Mağazada yayınlanan her uygulama; özellikle kişisel veri işleyenler.', 'Yayın öncesi raporda depolama, ağ, kimlik doğrulama ve gizlilik kontrollerinin sonucu yer alır.',
           'Yayından önce ve büyük sürümlerde MASVS kontrol grupları (STORAGE, CRYPTO, AUTH, NETWORK, PLATFORM, CODE, RESILIENCE, PRIVACY) OWASP MASTG yöntemleriyle test edilir; kritik bulgu kapanmadan yayın yapılmaz (bkz. Penetrasyon Testi).'),
     ]},

    {'id': 'mobile_release', 'section': 'mobile_app', 'type': 'multiselect', 'label': 'Mağaza Yayını ve Sürüm Yönetimi', 'en': 'App Store Release & Version Management', 'agents': [REL, APPDEV], 'showIf': MOB_STORE,
     'explanation': 'Uygulamanın App Store ve Google Play\'e nasıl yayınlanacağını, test dağıtımını, sürüm güncellemelerini, hata izlemesini ve mağaza gizlilik beyanlarını belirler. PWA mağazadan dağıtılmadığı için bu karar PWA\'da görünmez; PWA web yayın akışıyla güncellenir.',
     'scenario': 'Mağazada yayınlanacak her uygulama; özellikle API değişikliklerinin eski sürümleri bozmaması gerekiyorsa.',
     'example': 'Yeni sürüm önce TestFlight ve Google Play iç testte ekibe dağıtılır, sonra %10 kullanıcıya açılır; çok eski sürümdeki kullanıcıya "Lütfen güncelleyin" ekranı çıkar.',
     'rule': 'Mağaza yayını ve sürüm yönetimi: {labels}. Mağaza hesapları kurum adına açılır ve kurum tarafından yönetilir; imzalama anahtarları güvenli depoda tutulur, kişisel geliştirici hesabına bağlanmaz.',
     'options': [
         o('stores', 'App Store ve Google Play yayını', 'Uygulama iki mağazada, kurum adına açılmış geliştirici hesaplarıyla yayınlanır.',
           'Mağazada bulunması gereken her yerel / çapraz platform uygulama.', 'Mağaza sayfasında geliştirici adı olarak şirketin ticari unvanı görünür.',
           'Geliştirici hesapları kurum adına (kurumsal hesap) açılır, erişim en az yetkiyle ve iki adımlı doğrulamayla verilir; mağaza açıklamaları, ekran görüntüleri ve destek adresi Ortak Bilgiler\'den gelir.'),
         o('beta', 'Test dağıtımı (TestFlight / Play iç test)', 'Her sürüm mağazaya çıkmadan önce test kanallarında ekip ve seçili kullanıcılara dağıtılır.',
           'Her mağaza uygulaması.', 'Satış ekibi yeni sürümü TestFlight\'tan yükleyip bir hafta dener, sonra mağazaya gönderilir.',
           'Sürümler önce iç test, sonra kapalı test kanalından geçer; test sürümleri canlı olmayan API ortamına bağlanır ya da açıkça işaretlenir.'),
         o('staged_rollout', 'Kademeli dağıtım', 'Yeni sürüm önce kullanıcıların küçük bir yüzdesine açılır, sorun yoksa genişletilir.',
           'Kullanıcı sayısı yüksek uygulamalar.', 'Sürüm %10 → %50 → %100 açılır; çökme oranı artarsa dağıtım durdurulur.',
           'Kademeli dağıtım mağazaların aşamalı yayın özelliğiyle yapılır; çökme ve hata oranı eşiği aşılırsa dağıtım durdurulur.'),
         o('force_update', 'Zorunlu güncelleme (asgari sürüm kontrolü)', 'Uygulama açılışta sunucudan asgari desteklenen sürümü sorar; altındaysa güncellemeye yönlendirir.',
           'API değişikliği ya da güvenlik düzeltmesi sonrası eski sürümün kullanılmaması gereken durumlar.', 'v1.x kullanıcısı "Bu sürüm artık desteklenmiyor — Güncelle" ekranını görür, düğme mağaza sayfasını açar.',
           'Asgari ve önerilen sürüm sunucu yapılandırmasından okunur; API eski sürümleri en az tanımlı destek süresi boyunca sürümlü uç noktalarla destekler, zorunlu güncelleme yalnız güvenlik ya da uyumsuz değişiklikte kullanılır.'),
         o('ota', 'OTA (kablosuz) güncelleme', 'Uygulamanın JavaScript ve varlık katmanı mağaza incelemesi olmadan güncellenir (React Native / Capacitor ile).',
           'Hızlı hata düzeltmesi gereken React Native ya da Capacitor uygulamaları; yerel (Swift / Kotlin) ve Flutter uygulamada genelde uygulanmaz.', 'Fiyat ekranındaki yazım hatası mağaza beklemeden aynı gün düzeltilir.',
           'OTA güncellemeleri imzalı ve kanal bazlı (test / canlı) yayınlanır, geri alınabilir; yalnız hata düzeltmesi ve küçük değişiklik için kullanılır, uygulamanın temel işlevini değiştiren güncelleme mağaza sürümüyle yapılır (mağaza kuralları).'),
         o('crash', 'Çökme ve hata izleme (crash reporting)', 'Uygulama çökmeleri, hatalar ve performans (açılış süresi, ekran geçişi) izlenir; sürüm bazında raporlanır.',
           'Her mağaza uygulaması.', 'Panelde "v2.3.1: çökmesiz kullanıcı %99,6 · en sık hata: sipariş ekranı" görünür.',
           'Çökme raporları kaynak eşlemesiyle (sembol / source map) okunur; raporlara kişisel veri, token ve form içeriği yazılmaz, kullanıcı kimliği yerine takma kimlik kullanılır. Eşik aşımında uyarı Gözlemlenebilirlik kararındaki kanala gider.'),
         o('privacy_labels', 'Mağaza gizlilik beyanları', 'App Store gizlilik etiketi (App Privacy) ve Google Play Veri güvenliği bölümü, uygulamanın ve SDK\'larının gerçekten topladığı veriye göre doldurulur.',
           'Mağazaya yayınlanan her uygulama (mağaza zorunluluğu).', 'Mağaza sayfasında "Toplanan veriler: iletişim bilgileri, kullanım verisi; izleme amacıyla kullanılmaz" görünür.',
           'Beyanlar uygulama ve üçüncü taraf SDK\'ların veri envanterinden çıkarılır, KVKK aydınlatma metniyle tutarlıdır ve her sürümde yeni SDK / izin eklenince güncellenir; uygulama içinde ve mağazada gizlilik politikası bağlantısı bulunur.'),
         o('account_deletion', 'Uygulama içinden hesap silme', 'Uygulamada hesap oluşturulabiliyorsa hesap silme de uygulama içinden başlatılabilir.',
           'Uygulama içinde hesap açılan her uygulama (App Store ve Google Play kuralı).', 'Ayarlar › Hesap › "Hesabımı sil" adımı silme talebini başlatır ve sonucunu bildirir.',
           'Hesap silme uygulama içinden ve web\'den başlatılabilir, Üyelik › Hesap Silme kararıyla aynı süreçten geçer; yasal saklama yükümlülüğü olan veriler ayrıştırılarak saklanır, kullanıcı bilgilendirilir.'),
     ]},

    {'id': 'mobile_analytics', 'section': 'mobile_app', 'type': 'multiselect', 'label': 'Mobil Ölçüm ve Kullanıcı Yolculuğu', 'en': 'Mobile Analytics & User Journey', 'agents': [MKA, MEAS], 'showIf': MOB_ON,
     'explanation': 'Mobil uygulamadaki kullanıcı davranışının, bildirim performansının ve web–uygulama yolculuğunun nasıl ölçüleceğini ve kişisel veri / onay kurallarını belirler.',
     'scenario': 'Uygulamanın kullanımının, bildirimlerin ve uygulamadan gelen lead\'lerin raporlanması isteniyorsa.',
     'example': 'Raporda web ve uygulamadan gelen form gönderimleri aynı "generate_lead" olayıyla, kanala göre ayrılarak görünür; push bildiriminin açılma ve dönüşüm oranı ayrı raporlanır.',
     'rule': 'Mobil ölçüm ve kullanıcı yolculuğu: {labels}. Mobil analitik olayları web ile aynı adlandırmayı ve Metrik Sözlüğü tanımlarını kullanır; olaylara kişisel veri yazılmaz.',
     'recommend': {'field': 'analytics_tool', 'map': {'GA4': ['shared_events']}},
     'options': [
         o('shared_events', 'Web ile ortak olay adları', 'Uygulamadaki olaylar web ile aynı adlarla (ör. generate_lead, purchase, sign_up) ve aynı parametrelerle gönderilir.',
           'Web ve uygulamanın birlikte raporlanacağı her proje.', 'GA4\'te web ve uygulama veri akışları aynı mülkte, aynı olay adlarıyla görünür.',
           'Olay sözlüğü web ile ortaktır; uygulama akışı ayrı veri akışı olarak aynı analitik mülkte tutulur, platform parametresiyle ayrılır.'),
         o('consent_gate', 'Onay öncesi analitik yok', 'Analitik ve pazarlama SDK\'ları kullanıcı onay vermeden veri göndermez; iOS\'ta uygulamalar arası izleme varsa ayrıca izin istenir.',
           'Analitik ya da reklam SDK\'sı kullanan her uygulama.', 'İlk açılışta tercih ekranı çıkar; "Reddet" seçilirse analitik SDK veri toplamaz.',
           'SDK\'lar onay alınana kadar veri toplamayacak biçimde başlatılır; onay tercihleri web\'deki kategorilerle aynıdır ve değiştirilebilir. Başka şirketlerin uygulama / siteleriyle izleme yapılıyorsa iOS\'ta App Tracking Transparency izni istenir; izleme yoksa istenmez.'),
         o('push_metrics', 'Bildirim performansı', 'Gönderilen, teslim edilen, açılan ve dönüşüme yol açan bildirimler kampanya ve şablon bazında ölçülür.',
           'Anlık bildirim kullanan uygulamalar.', '"Sipariş hatırlatma bildirimi: 2.000 gönderim, %18 açılma, 64 sipariş".',
           'Bildirim kimliği ve kampanya kimliği açılış olayına eklenir; bildirim ölçümü onay kurallarına tabidir, kapatma (abonelikten çıkma) oranı izlenir.'),
         o('crm_link', 'CRM zaman çizelgesine aktarım', 'Giriş yapmış kullanıcının uygulamadaki önemli işlemleri (form, teklif görüntüleme, rezervasyon) CRM müşteri zaman çizelgesine yazılır.',
           'CRM kullanan ve müşteri yolculuğunun tek yerde izlenmesi istenen projeler.', 'CRM\'de müşterinin zaman çizelgesinde "Mobil: teklif görüntülendi · 12.11.2026" satırı görünür.',
           'Aktarım sunucu tarafında, kullanıcı kimliğiyle ve yalnız iş amacı tanımlı olaylar için yapılır; aydınlatma metninde belirtilir, analitik takma kimliği ile CRM kimliği yalnız sunucuda eşleştirilir.'),
         o('journey', 'Web–uygulama yolculuk eşleştirmesi', 'Kullanıcının web\'de başlayıp uygulamada (ya da tersi) tamamladığı yolculuk, oturum açtıktan sonra aynı kullanıcı olarak eşleştirilir.',
           'Kullanıcıların iki kanalı birlikte kullandığı portal, e-ticaret ve eğitim projeleri.', 'Webde sepete eklenen ürün uygulamada satın alınır; rapor bunu tek yolculuk olarak gösterir.',
           'Eşleştirme yalnız oturum açmış kullanıcıda, kişisel veri yerine takma kullanıcı kimliğiyle ve onay kapsamında yapılır; derin bağlantılarda kampanya parametreleri (UTM) korunur.'),
         o('store_metrics', 'Mağaza ve sürüm metrikleri', 'Mağaza sayfası görüntüleme, yükleme, kaldırma, puan ve yorumlar ile sürüm bazında aktif kullanıcı izlenir.',
           'Mağaza üzerinden kullanıcı kazanan uygulamalar.', 'Aylık raporda "Yükleme 1.240, kaldırma 180, ortalama puan 4,6; aktif kullanıcıların %92\'si son iki sürümde".',
           'Mağaza metrikleri App Store Connect ve Play Console\'dan okunur; sürüm dağılımı zorunlu güncelleme kararlarında kullanılır.'),
     ]},
]

# =====================================================================================================
PART = {
    'sections': [SECTION],
    'fields': MOBILE_FIELDS,
    'fields_into': [CMS_CONTENT_RULES, CMS_PUBLISHING, FORM_STANDARD, FORM_STORAGE, POPUP_POLICY, POPUP_RULES, MK_METRIC_DICT],
    'guide_add': {
        'cms': [
            {'title': 'Google Search Central — URL yapısı', 'url': 'https://developers.google.com/search/docs/crawling-indexing/url-structure', 'note': 'Okunabilir, kelimeleri tireyle ayrılmış ve parametre karmaşası olmayan adres yapısı önerileri.'},
            {'title': 'Google Search Central — Yönlendirmeler ve Google Arama', 'url': 'https://developers.google.com/search/docs/crawling-indexing/301-redirects', 'note': 'Adres değişince kalıcı (301) yönlendirmenin nasıl kurulacağı ve arama görünürlüğüne etkisi.'},
            {'title': 'Google Search Central — İçerik yolu (BreadcrumbList) işaretlemesi', 'url': 'https://developers.google.com/search/docs/appearance/structured-data/breadcrumb', 'note': 'Sayfa ağacından üretilen içerik yolunun yapısal veriyle işaretlenmesi.'},
            {'title': 'W3C WAI — Forms Tutorial', 'url': 'https://www.w3.org/WAI/tutorials/forms/', 'note': 'Erişilebilir form etiketleri, gruplama, talimatlar, doğrulama ve hata bildirimi.'},
        ],
        'public': [
            {'title': 'Google Search Central — Avoid intrusive interstitials and dialogs', 'url': 'https://developers.google.com/search/docs/appearance/avoid-intrusive-interstitials', 'note': 'İçeriği örten pop-up ve katmanların kullanıcıya ve arama performansına etkisi, kabul edilebilir kullanımlar.'},
            {'title': 'W3C ARIA APG — Dialog (Modal) Pattern', 'url': 'https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/', 'note': 'Erişilebilir modal pencerede odak yönetimi, Escape ile kapatma ve klavye etkileşimi.'},
            {'title': 'W3C — Understanding SC 2.4.11 Focus Not Obscured (Minimum)', 'url': 'https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html', 'note': 'Yapışkan şerit ve bantların klavyeyle odaklanan öğeyi örtmemesi kuralı (WCAG 2.2).'},
        ],
        'mk_measure': [
            {'title': 'Google Analytics — Temel etkinlikler (key events)', 'url': 'https://support.google.com/analytics/answer/9267568', 'note': 'GA4\'te dönüşüm sayılan olayların tanımlanması.'},
            {'title': 'Google Analytics — Atıf (attribution) ile çalışmaya başlama', 'url': 'https://support.google.com/analytics/answer/10596866', 'note': 'GA4 atıf modelleri ve dönüşüm pencerelerinin metrik tanımına etkisi.'},
            {'title': 'Google Analytics — Boyutlar ve metrikler', 'url': 'https://support.google.com/analytics/answer/9143382', 'note': 'GA4 metriklerinin resmî tanımları; metrik sözlüğünde kaynak tanım olarak kullanılır.'},
        ],
    },
}
