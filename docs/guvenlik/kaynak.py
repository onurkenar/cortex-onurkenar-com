# -*- coding: utf-8 -*-
"""Güvenlik eklemeleri (2026-11-10, kullanıcı isteği: "Güvenlik & gizlilik bölümüne penetrasyon testleri ekle" ve
"güvenlik ile ilgili XSS, IDOR için alan ekle (uygun yere koy)").
Çalıştırınca yanına guvenlik.json yazar; uygulamaya guvenlik_ekle.py işler.
python3 -I docs/guvenlik/kaynak.py"""
import json, os

PEN = 'poz:siber-guvenlik:16.06/uygulama-ve-api-guvenlik-testleri/kidemli-sizma-testi-uzmani'
APPSEC = 'poz:siber-guvenlik:16.06/guvenli-yazilim-gelistirme-yasam-dongusu/kidemli-uygulama-guvenligi-uzmani'
VULN = 'poz:siber-guvenlik:16.08/guvenlik-acigi-ve-maruziyet-yonetimi/zafiyet-analisti'
CODE = 'poz:siber-guvenlik:16.06/devsecops-ve-kod-guvenligi/kod-guvenligi-uzmani'


def o(v, l, ex, sc, eg, rd=None):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    return x


# ---------------------------------------------------------------- Güvenlik Mühendisliği'ne yeni karar
VULN_FIELD = {
    'id': 'vuln_controls', 'section': 'security_eng', 'after': 'security_controls', 'type': 'multiselect',
    'label': 'Zafiyet Sınıfları ve Savunmaları', 'en': 'Vulnerability Classes & Defenses', 'agents': [APPSEC, CODE],
    'explanation': 'XSS, IDOR gibi en sık istismar edilen açık türlerinin her biri için kodda uygulanacak somut savunmayı belirler. "Uygulama Güvenlik Kontrolleri" genel başlıkları seçer; bu karar her açık türünün nasıl önleneceğini ve nasıl test edileceğini kurala yazar.',
    'scenario': 'Üyelik, panel, API, dosya yükleme ya da kullanıcı içeriği olan her projede; özellikle bir kullanıcının başka kullanıcının ya da organizasyonun kaydına ulaşabileceği B2B, SaaS, e-ticaret ve portal projelerinde.',
    'example': 'IDOR seçilince sipariş detayı uç noktası /api/orders/1043 isteğinde kaydın oturumdaki kullanıcıya ait olup olmadığını denetler; başkasının siparişi istendiğinde 404 döner ve bu durum otomatik testle kanıtlanır.',
    'rule': 'Aşağıdaki zafiyet sınıflarına karşı belirtilen savunmalar uygulanacak ve her biri en az bir otomatik testle kanıtlanacaktır: {labels}.',
    'options': [
        o('xss', 'XSS: kalıcı ve yansıyan (sunucu tarafı çıktı)', 'Kullanıcıdan gelen ve veritabanına kaydedilen (kalıcı) ya da adres / form üzerinden sayfaya geri yansıyan (yansıyan) içeriğin betik olarak çalışmasını önler. Savunma, verinin girişte değil, ekrana basıldığı bağlama göre kodlanmasıdır.', 'Yorum, ürün değerlendirmesi, profil, forum ya da arama sonucu gösteren her sayfada.', 'Bir yorumcunun yazdığı <script> etiketi sayfada düz metin olarak görünür, diğer ziyaretçilerin tarayıcısında çalışmaz.',
          'XSS (kalıcı / yansıyan): çıktı bağlama göre kodlanacak (HTML gövdesi, öznitelik, URL, JavaScript, CSS ayrı); şablon motorunun otomatik kaçışı kapatılmayacak; zengin metin yalnız sunucuda izin listeli bir temizleyiciyle (ör. DOMPurify / sanitize-html, izinli etiket ve öznitelik listesi) kaydedilecek; CSP nonce tabanlı script-src ile ikinci savunma kurulacak; çerezler HttpOnly olacak. Test: her girdi alanına bilinen XSS yükleri gönderilip çıktıda kaçırıldığı doğrulanacak.'),
        o('xss_dom', 'XSS: DOM tabanlı (tarayıcı tarafı)', 'Sunucuya hiç gitmeden tarayıcıdaki JavaScript\'in adres çubuğu, hash, postMessage ya da API yanıtındaki veriyi güvensiz biçimde sayfaya yazmasıyla oluşur. Sunucu tarafı kaçış bunu engellemez.', 'Tek sayfa uygulamaları (React, Vue, Svelte), arama / filtre parametrelerini sayfaya yazan ön yüzler, üçüncü taraf widget\'ları.', 'Arama sayfası ?q= değerini textContent ile yazar; innerHTML yerine kullanıldığı için <img onerror> yükü çalışmaz.',
          'DOM tabanlı XSS: kullanıcı kaynaklı veri innerHTML, outerHTML, document.write, insertAdjacentHTML, eval, new Function, setTimeout(string) ve javascript: adreslerine verilmeyecek; metin textContent ile yazılacak; çerçeve kaçış kapıları (dangerouslySetInnerHTML, v-html, {@html}) yalnız DOMPurify ile temizlenmiş içerikle kullanılacak; mümkünse CSP require-trusted-types-for \'script\' ile Trusted Types zorunlu tutulacak; postMessage alıcıları origin denetleyecek.'),
        o('idor', 'IDOR / BOLA (nesne düzeyinde yetki)', 'İstekle gelen bir kayıt kimliğinin (sipariş, fatura, belge, kullanıcı id) oturumdaki kullanıcıya veya etkin organizasyona ait olup olmadığının denetlenmemesidir. OWASP API Security Top 10\'da birinci sıradadır; kimliği tahmin edilemez (UUID) yapmak tek başına çözüm değildir.', 'Kullanıcının kendi kayıtlarını gördüğü her panel, portal ve API; özellikle çok organizasyonlu ve çok kiracılı projeler.', '/api/invoices/8812 isteğinde sorgu "WHERE id = ? AND organization_id = <oturumdaki organizasyon>" ile çalışır; başka şirketin faturası istenince 404 döner.',
          'IDOR / BOLA: istemciden gelen her nesne kimliği sunucuda sahiplik / organizasyon koşuluyla sorgulanacak (WHERE id = ? AND owner_id / organization_id = oturumdaki değer); kimlik yetki kanıtı sayılmayacak, UUID kullanımı denetimin yerine geçmeyecek; yetkisiz erişimde kaydın varlığını sızdırmamak için 404 dönülecek; liste, dışa aktarma, dosya indirme ve toplu işlem uç noktaları da aynı denetimden geçecek; her uç nokta için "ikinci kullanıcı / ikinci organizasyon" testi yazılacak.'),
        o('bfla', 'Fonksiyon düzeyinde yetki atlatma (BFLA)', 'Yalnız yöneticinin çağırması gereken bir işlemin (kullanıcı silme, rol değiştirme, iade onaylama) normal kullanıcı tarafından doğrudan API\'ye istek atılarak çalıştırılabilmesidir. Menüde düğmeyi gizlemek koruma sağlamaz.', 'Yönetim paneli, rol / izin yapısı ve ayrı yetki seviyeleri olan her projede.', 'Üye rolündeki kullanıcı DELETE /api/admin/users/15 isteğini elle gönderdiğinde 403 alır; işlem denetim kaydına yazılır.',
          'Fonksiyon düzeyinde yetki: yönetim ve yetkili işlemler sunucuda rol / izin denetiminden geçecek, varsayılan olarak reddedilecek; arayüzde gizleme yetkilendirme sayılmayacak; aynı kaynağın bütün HTTP yöntemleri (GET, POST, PUT, PATCH, DELETE) ayrı ayrı denetlenecek; yetkisiz deneme denetim kaydına yazılacak.'),
        o('mass_assignment', 'Toplu atama (mass assignment)', 'İstek gövdesindeki alanların doğrudan veritabanı modeline bağlanması sonucu kullanıcının rol, sahip, fiyat, durum, bakiye gibi kendisinin değiştirmemesi gereken alanları değiştirebilmesidir.', 'Profil güncelleme, kayıt, sipariş ve ayar formları olan her projede.', 'Profil güncelleme isteğine {"role":"admin"} eklense de yalnız ad, telefon ve dil alanları kaydedilir.',
          'Toplu atama: istek gövdesi modele doğrudan bağlanmayacak; her uç nokta izin listeli giriş modeli (DTO / şema) kullanacak; rol, sahip, organizasyon, fiyat, tutar, durum, onay ve bakiye gibi alanlar yalnız sunucu mantığıyla atanacak; bilinmeyen alanlar reddedilecek ya da yok sayılacak.'),
        o('ssrf', 'SSRF (sunucu taraflı istek sahteciliği)', 'Kullanıcının verdiği bir adresi sunucunun çağırması (bağlantı önizlemesi, webhook, görsel indirme, PDF oluşturma) üzerinden iç ağa, bulut metaveri servisine (169.254.169.254) veya yerel servislere erişilmesidir.', 'Webhook, bağlantı önizlemesi, adresten görsel / dosya içe aktarma, PDF ya da ekran görüntüsü üreten projelerde.', 'Webhook adresi olarak http://169.254.169.254/latest/meta-data/ girildiğinde istek reddedilir; yalnız https ve herkese açık adreslere izin verilir.',
          'SSRF: sunucunun çağırdığı kullanıcı kaynaklı adresler izin listesine göre denetlenecek; yalnız https; özel IP aralıkları, localhost, link-local ve bulut metaveri adresleri ad çözümlemesinden SONRA engellenecek; yönlendirmeler izlenmeyecek ya da her adımda yeniden denetlenecek; yanıt boyutu ve süresi sınırlanacak; bu istekler ayrı, yetkisi kısıtlı bir ağ çıkışından yapılacak.'),
        o('open_redirect', 'Açık yönlendirme (open redirect)', 'Girişten sonra ?next=, ?returnUrl= gibi parametrelerle kullanıcının saldırganın sitesine yönlendirilebilmesidir; oltalama ve OAuth jetonu çalmada kullanılır.', 'Giriş sonrası dönüş adresi, çıkış, ödeme dönüşü veya kampanya yönlendirmesi olan projelerde.', '/giris?next=https://kotu-site.com isteğinde kullanıcı ana sayfaya yönlendirilir; yalnız sitenin kendi yolları kabul edilir.',
          'Açık yönlendirme: yönlendirme parametreleri yalnız sitenin kendi göreli yollarını (/ ile başlayan, // ile başlamayan) ya da izin listesindeki adresleri kabul edecek; geçersiz değerde varsayılan sayfaya dönülecek; OAuth dönüş adresleri tam eşleşmeyle kayıtlı olacak.'),
        o('path_traversal', 'Dosya yolu geçişi (path traversal)', 'Dosya adı ya da yolu içeren parametrelerle (../../etc/passwd) uygulamanın izinli klasör dışındaki dosyaları okuması veya yazmasıdır.', 'Belge indirme, şablon seçme, dil dosyası yükleme veya dosya önizleme olan projelerde.', '/indir?dosya=../../.env isteği reddedilir; indirme kimlikle yapılır ve kimlik veritabanındaki dosya yoluna çevrilir.',
          'Dosya yolu geçişi: kullanıcı girdisi dosya sistemi yoluna eklenmeyecek; dosyalara kimlikle erişilip yol sunucuda eşlenecek; zorunlu durumda yol normalize edilip izinli kök klasörün içinde kaldığı doğrulanacak; arşiv açarken (zip slip) her öğenin yolu denetlenecek.'),
        o('file_upload', 'Güvensiz dosya yükleme', 'Yüklenen dosyanın sunucuda çalıştırılabilmesi, HTML / SVG olarak aynı kökende açılıp XSS\'e dönüşmesi, aşırı büyük dosyalarla hizmetin durdurulması veya zararlı yazılım dağıtılmasıdır.', 'Profil fotoğrafı, belge, CV, başvuru eki ya da medya yükleme olan her projede.', 'Yüklenen fatura.pdf.html dosyası içerik imzasıyla reddedilir; kabul edilen dosyalar rastgele adla ayrı depolama alanında saklanır ve indirme olarak sunulur.',
          'Dosya yükleme: tür uzantıyla değil içerik imzasıyla (magic bytes) ve izin listesiyle denetlenecek; boyut ve sayı sınırı olacak; dosya rastgele adla, web kökü dışında ya da ayrı bir alan adındaki depolamada saklanacak; HTML, SVG ve betik içerebilen türler satır içi sunulmayacak (Content-Disposition: attachment, X-Content-Type-Options: nosniff); görseller yeniden işlenip metaverisi silinecek; gerekiyorsa zararlı yazılım taraması yapılacak.'),
        o('clickjacking', 'Clickjacking (tıklama kaçırma)', 'Sitenin görünmez bir çerçeve içine alınıp kullanıcının farkında olmadan düğmelere tıklatılmasıdır (ödeme onayı, ayar değiştirme).', 'Oturum açılan, ödeme ya da ayar değiştirme işlemi olan her sitede.', 'Başka bir site panel sayfasını iframe içinde açmaya çalıştığında tarayıcı çerçeveyi göstermez.',
          'Clickjacking: CSP frame-ancestors \'none\' (gömülmesi gereken sayfalarda yalnız izinli kökenler) ve eski tarayıcılar için X-Frame-Options: DENY gönderilecek.'),
        o('race', 'Yarış durumu ve iş mantığı açıkları', 'Aynı isteğin aynı anda birden çok kez gönderilmesiyle kuponun iki kez kullanılması, stoktan fazla satış, bakiyenin eksiye düşmesi ya da onay adımlarının atlanması gibi mantık hatalarıdır; otomatik tarayıcılar bunları genellikle bulamaz.', 'Ödeme, kupon, puan, stok, rezervasyon, oylama veya çok adımlı onay akışı olan projelerde.', 'Aynı kupon kodu 20 eşzamanlı istekle denendiğinde yalnız biri başarılı olur; diğerleri "kupon kullanıldı" yanıtı alır.',
          'Yarış durumu ve iş mantığı: tutar, stok, kupon, bakiye ve rezervasyon işlemleri veritabanı işlemi ve satır kilidi / benzersizlik kısıtıyla atomik yapılacak; ödeme ve sipariş uç noktaları idempotency anahtarı kullanacak; çok adımlı akışlarda adım sırası sunucuda doğrulanacak; eşzamanlı istek testleri yazılacak.'),
        o('enumeration', 'Hesap ve kayıt numaralandırma', 'Giriş, kayıt ya da parola sıfırlamada farklı hata mesajlarıyla hangi e-postanın kayıtlı olduğunun anlaşılması veya sıralı kimliklerle kayıtların taranmasıdır.', 'Üyelik, parola sıfırlama, davet ya da herkese açık profil sayfası olan projelerde.', 'Parola sıfırlama formu e-posta kayıtlı olsun olmasın aynı mesajı verir: "Bu adres kayıtlıysa bağlantı gönderildi."',
          'Numaralandırma: giriş, kayıt ve parola sıfırlama yanıtları ve süreleri hesabın varlığını ele vermeyecek; bu uç noktalar IP ve hesap bazında hız sınırlı olacak; herkese açık adreslerde sıralı kimlik yerine tahmin edilemez kimlik kullanılacak (yetki denetiminin yerine geçmez).'),
    ],
    'recommend': [
        {'field': 'security_controls', 'map': {'XSS': ['xss', 'xss_dom'], 'OWASP': ['xss', 'xss_dom', 'idor', 'bfla', 'mass_assignment', 'ssrf', 'open_redirect', 'file_upload', 'clickjacking']}},
        {'field': 'member_mode', 'map': {'Open': ['xss', 'xss_dom', 'idor', 'bfla', 'mass_assignment', 'enumeration'], 'Approval': ['xss', 'xss_dom', 'idor', 'bfla', 'mass_assignment', 'enumeration'], 'Invite': ['idor', 'bfla', 'mass_assignment']}},
        {'field': 'panel_tenancy', 'map': {'multi_org': ['idor', 'bfla', 'mass_assignment'], 'multi_tenant': ['idor', 'bfla', 'mass_assignment']}},
        {'field': 'modules_extra', 'map': {'ecommerce': ['race', 'idor'], 'booking': ['race', 'idor'], 'community': ['xss', 'xss_dom', 'file_upload'], 'forum': ['xss', 'xss_dom', 'file_upload'], 'listings': ['xss', 'file_upload', 'idor'], 'career': ['file_upload', 'idor']}},
    ],
}

SEC_GUIDE_ADD = [
    {'title': 'OWASP – Cross Site Scripting Prevention Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html', 'note': 'Bağlama göre çıktı kodlama, güvenli DOM yöntemleri ve HTML temizleme kuralları.'},
    {'title': 'MDN – Trusted Types API', 'url': 'https://developer.mozilla.org/en-US/docs/Web/API/Trusted_Types_API', 'note': 'DOM tabanlı XSS\'i tarayıcı düzeyinde engelleyen CSP require-trusted-types-for yönergesi.'},
    {'title': 'OWASP – Insecure Direct Object Reference Prevention', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Insecure_Direct_Object_Reference_Prevention_Cheat_Sheet.html', 'note': 'IDOR\'un nedenleri ve her nesne erişiminde sahiplik denetimi.'},
    {'title': 'OWASP API Security Top 10 (2023)', 'url': 'https://api-security.owasp.org/editions/2023/en/0x11-t10/', 'note': 'BOLA, kimlik doğrulama, nesne özelliği düzeyinde yetki (toplu atama), fonksiyon düzeyinde yetki ve SSRF dahil en kritik API açıkları.'},
    {'title': 'OWASP – Server Side Request Forgery Prevention', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html', 'note': 'İzin listesi, ad çözümlemesi sonrası IP denetimi ve ağ katmanı önlemleri.'},
    {'title': 'OWASP – Mass Assignment Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html', 'note': 'İzin listeli giriş modelleri (DTO) ile toplu atamanın önlenmesi.'},
    {'title': 'OWASP – File Upload Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html', 'note': 'Dosya türü denetimi, depolama, adlandırma ve sunum kuralları.'},
    {'title': 'OWASP – Unvalidated Redirects and Forwards', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html', 'note': 'Açık yönlendirmenin önlenmesi.'},
]

# ---------------------------------------------------------------- Yeni bölüm: Penetrasyon (Sızma) Testi
SECTION = {'id': 'pentest', 'after': 'security_eng', 'group': 'Güvenlik & Gizlilik', 'icon': '◈',
           'name': 'Penetrasyon (Sızma) Testi', 'en': 'Penetration Testing',
           'desc': 'Sitenin ve uygulamanın gerçek bir saldırganın yöntemleriyle, yetkili ve kontrollü olarak denenmesini planlar: kapsam, yaklaşım, standart, zamanlama, testi yapan, ortam, otomatik taramalar, test kuralları, rapor içeriği, düzeltme süreleri ve canlıya çıkış kapısı.'}

GUIDE = {
    'purpose': 'Penetrasyon (sızma) testi, yazılan güvenlik kontrollerinin gerçekten çalıştığını bir saldırganın gözüyle sınar. Kod incelemesi ve otomatik taramalar bilinen kalıpları yakalar; yetki atlatma, IDOR, iş mantığı ve zincirlenmiş açıklar ise çoğunlukla ancak insan eliyle yapılan testte ortaya çıkar. Bu bölüm testin neyi, nasıl, ne zaman, kim tarafından ve hangi kurallarla yapılacağını; bulguların nasıl raporlanıp hangi sürede kapatılacağını önceden belirler.',
    'criteria': [
        'Kapsamı panellere, API\'ye, ödeme ve dosya yükleme akışlarına göre seçin; test edilmeyen her bölüm raporda “kapsam dışı” olarak açıkça yazılmalıdır.',
        'Gri kutu (test hesaplarıyla) yaklaşım çoğu proje için en verimli olanıdır: yetki ve IDOR açıkları ancak oturum açmış farklı rollerle denenince görünür.',
        'Bir standarda göre test isteyin (OWASP WSTG, ASVS, API Top 10); böylece testin neyi kapsadığı ve eksik kalan konular ölçülebilir olur.',
        'Canlıya çıkıştan önce en az bir kez, sonra büyük değişikliklerde ve yılda bir test planlayın; aradaki dönemi otomatik taramalar ve açık bildirim politikası (security.txt) doldurur.',
        'Test başlamadan yazılı yetki ve kapsam belgesi imzalanmalıdır. İzinsiz test, Türk Ceza Kanunu m. 243–244 kapsamında suç oluşturabilir.',
        'Bulgular CVSS puanıyla önceliklendirilir; kritik ve yüksek açıklar için düzeltme süresi ve yeniden test önceden kararlaştırılır.',
    ],
    'pitfalls': [
        'Yalnız otomatik tarayıcı çıktısını “sızma testi” saymak. Tarayıcılar IDOR, yetki atlatma ve iş mantığı açıklarının çoğunu bulamaz.',
        'Testi gerçek müşteri verisi bulunan canlı ortamda, kapsam ve acil durdurma kuralları olmadan yapmak.',
        'Raporu alıp düzeltme sonrası yeniden test yaptırmamak; kapatıldığı varsayılan açıkların bir kısmı yanlış ya da eksik düzeltilmiş olur.',
        'Bulguları e-posta ekinde şifresiz paylaşmak; sızma testi raporu saldırgan için hazır bir saldırı planıdır.',
        'Kapsamı yalnız ana siteyle sınırlayıp yönetim panellerini, API\'yi ve alt alan adlarını dışarıda bırakmak.',
    ],
    'resources': [
        {'title': 'OWASP Web Security Testing Guide (WSTG)', 'url': 'https://owasp.org/www-project-web-security-testing-guide/', 'note': 'Web uygulaması sızma testinin kapsamlı yöntem rehberi; test başlıkları ve adımları.'},
        {'title': 'OWASP Application Security Verification Standard (ASVS)', 'url': 'https://owasp.org/www-project-application-security-verification-standard/', 'note': 'Üç seviyeli doğrulama gereksinimleri; testin kabul ölçütü olarak kullanılır.'},
        {'title': 'OWASP API Security Top 10 (2023)', 'url': 'https://api-security.owasp.org/editions/2023/en/0x11-t10/', 'note': 'API testinde öncelikli on risk (BOLA, kimlik doğrulama, BFLA, SSRF …).'},
        {'title': 'OWASP Top 10', 'url': 'https://owasp.org/Top10/', 'note': 'Web uygulamalarında en kritik güvenlik risklerinin güncel listesi.'},
        {'title': 'NIST SP 800-115 – Technical Guide to Information Security Testing and Assessment', 'url': 'https://csrc.nist.gov/pubs/sp/800/115/final', 'note': 'Güvenlik testinin planlanması, yürütülmesi ve raporlanması için NIST rehberi.'},
        {'title': 'FIRST – CVSS v4.0', 'url': 'https://www.first.org/cvss/v4-0/', 'note': 'Bulguların önem derecesini puanlamak için kullanılan ortak sistem.'},
        {'title': 'RFC 9116 – security.txt', 'url': 'https://www.rfc-editor.org/rfc/rfc9116', 'note': 'Güvenlik araştırmacılarının açık bildirebileceği iletişim bilgisinin yayımlanma biçimi.'},
        {'title': 'ZAP (Zed Attack Proxy)', 'url': 'https://www.zaproxy.org/', 'note': 'Açık kaynak dinamik uygulama güvenliği tarayıcısı; CI hattında otomatik tarama için.'},
    ],
}

PT = [
    {'id': 'pentest_scope', 'type': 'multiselect', 'label': 'Test Kapsamı', 'en': 'Test Scope', 'agents': [PEN],
     'explanation': 'Sızma testinde hangi bölümlerin deneneceğini belirler. Seçilmeyen bölümler raporda “kapsam dışı” olarak yazılır.',
     'scenario': 'Üyelik, panel, API veya ödeme olan projelerde web uygulamasıyla birlikte kimlik doğrulama, yetkilendirme ve API mutlaka kapsama alınmalıdır.',
     'example': 'Kapsam: web uygulaması, kimlik doğrulama, yetkilendirme, API ve yönetim paneli; ödeme sağlayıcısının kendi sayfası kapsam dışı.',
     'rule': 'Sızma testinin kapsamı: {labels}. Kapsam dışı bırakılan bölümler raporda açıkça yazılacaktır.',
     'options': [
         o('web', 'Web uygulaması ve herkese açık sayfalar', 'Formlar, arama, içerik sayfaları, çerez ve güvenlik başlıkları, istemci tarafı kod.', 'Her projede.', 'İletişim formu, arama ve blog sayfaları XSS, yönlendirme ve başlık açısından denenir.', 'Herkese açık sayfalar, formlar, güvenlik başlıkları ve istemci tarafı kod test edilecek.'),
         o('auth', 'Kimlik doğrulama ve oturum yönetimi', 'Giriş, kayıt, parola sıfırlama, çok adımlı doğrulama, oturum çerezi, çıkış ve oturum süresi.', 'Üyelik veya panel girişi olan her projede.', 'Parola sıfırlama bağlantısının yeniden kullanılıp kullanılamadığı ve oturumun çıkıştan sonra geçersizleştiği denenir.', 'Giriş, kayıt, parola sıfırlama, MFA ve oturum yaşam döngüsü test edilecek.'),
         o('authz', 'Yetkilendirme: IDOR / BOLA ve yetki yükseltme', 'Farklı rol ve organizasyonlardaki test hesaplarıyla başkasının kaydına erişim ve yetkisiz işlem denemeleri.', 'Birden fazla rolü ya da organizasyonu olan her projede.', 'A şirketinin kullanıcısı B şirketinin fatura kimliğini isteyerek erişim dener.', 'Her rol ve organizasyon çifti için IDOR / BOLA ve yetki yükseltme denemeleri yapılacak.'),
         o('api', 'API uç noktaları', 'REST / GraphQL uç noktaları, belgelenmemiş uç noktalar, hız sınırı, toplu atama, CORS.', 'Ayrı API\'si, mobil uygulaması veya entegrasyonu olan projelerde.', 'Belgelenmemiş /api/v1/admin/export uç noktası normal kullanıcı jetonuyla denenir.', 'API uç noktaları (belgelenmemişler dahil) OWASP API Top 10\'a göre test edilecek.'),
         o('admin', 'Yönetim panelleri', 'Panel girişi, rol ayrımı, toplu işlemler, dışa aktarma ve ayarlar.', 'CMS, operasyon ya da süper yönetici paneli olan projelerde.', 'Editör rolüyle ayarlar uç noktası çağrılarak yetki atlatma denenir.', 'Yönetim panelleri ve panel alt alan adları kapsama dahil edilecek.'),
         o('payment', 'Ödeme, iade ve kupon akışları', 'Tutarın istemcide değiştirilmesi, kuponun tekrar kullanılması, ödeme dönüşü (callback) sahteciliği, yarış durumları.', 'E-ticaret, rezervasyon ve abonelik projelerinde.', 'Sepet tutarı istekte 1 TL yapılarak gönderilir; sunucu tutarı kendisi hesapladığı için sipariş gerçek tutarla oluşur.', 'Ödeme, iade, kupon ve ödeme dönüşü akışları tutar bütünlüğü ve yarış durumu açısından test edilecek; ödeme sağlayıcısının kendi altyapısı test edilmeyecek.'),
         o('upload', 'Dosya yükleme ve indirme', 'Zararlı içerikli dosya, tür atlatma, yol geçişi, başkasının dosyasını indirme.', 'Belge, görsel veya ek yüklenen projelerde.', 'SVG içinde betik yüklenip açıldığında çalışıp çalışmadığı denenir.', 'Dosya yükleme ve indirme uç noktaları tür, boyut, yol ve yetki açısından test edilecek.'),
         o('infra', 'Altyapı: sunucu, TLS, DNS ve e-posta', 'Açık portlar, TLS yapılandırması, alt alan adı ele geçirme, SPF / DKIM / DMARC, yönetim arayüzleri.', 'Kendi sunucusu veya birden çok alt alan adı olan projelerde.', 'Kullanılmayan bir alt alan adının boşta kalan bir hizmete yönlendiği (subdomain takeover) tespit edilir.', 'Sunucu, TLS, DNS (alt alan adı ele geçirme dahil) ve e-posta kimlik doğrulama kayıtları test edilecek.'),
         o('cloud', 'Bulut, CDN ve depolama yapılandırması', 'Herkese açık bırakılmış depolama alanları, yanlış izinler, gizli anahtar sızıntısı.', 'AWS, Azure, Google Cloud, Cloudflare R2 vb. kullanan projelerde.', 'Yüklenen belgelerin bulunduğu depolama alanının listelenebilir olup olmadığı denenir.', 'Bulut depolama, CDN ve kimlik / izin yapılandırması gözden geçirilecek.'),
         o('social', 'Sosyal mühendislik ve oltalama', 'Çalışanlara yönelik oltalama e-postası ve telefon senaryoları. Ayrı yazılı onay ve iletişim planı gerektirir.', 'Kurum içi farkındalığın ölçülmesi isteniyorsa; çoğu web projesinde kapsam dışıdır.', 'Yönetim paneli kullanıcılarına izinli bir oltalama e-postası gönderilir, tıklama oranı raporlanır.', 'Sosyal mühendislik testi yalnız ayrı yazılı onay ve bilgilendirme planıyla yapılacak.'),
     ],
     'recommend': [
         {'field': 'member_mode', 'map': {'Open': ['web', 'auth', 'authz', 'api'], 'Approval': ['web', 'auth', 'authz', 'api'], 'Invite': ['web', 'auth', 'authz']}},
         {'field': 'modules_extra', 'map': {'ecommerce': ['payment'], 'booking': ['payment'], 'lms': ['payment'], 'career': ['upload'], 'listings': ['upload'], 'portal': ['authz', 'api']}},
         {'field': 'vuln_controls', 'map': {'file_upload': ['upload'], 'idor': ['authz'], 'bfla': ['authz', 'admin']}},
     ]},
    {'id': 'pentest_approach', 'type': 'select', 'label': 'Test Yaklaşımı', 'en': 'Testing Approach', 'agents': [PEN],
     'explanation': 'Test yapanın sistem hakkında ne kadar bilgiyle başlayacağını belirler. Bilgi arttıkça test daha derin ve verimli olur.',
     'scenario': 'Çoğu proje için gri kutu en iyi maliyet / bulgu oranını verir; kritik finans ya da sağlık sistemlerinde beyaz kutu tercih edilir.',
     'example': 'Gri kutuda test ekibine her rolden birer test hesabı ve API belgesi verilir; kaynak kodu verilmez.',
     'rule': 'Sızma testi {label} yaklaşımıyla yapılacaktır.',
     'options': [
         o('black', 'Kara kutu (dış saldırgan)', 'Test ekibine yalnız adres verilir; hesap ve belge verilmez. Dış saldırganı en gerçekçi biçimde taklit eder ama oturum içi açıkları büyük ölçüde kaçırır.', 'Yalnız herkese açık bir site ya da dış saldırı yüzeyinin ölçülmesi isteniyorsa.', 'Ekip yalnız alanadi.com adresiyle başlar.', 'Test ekibine yalnız hedef adresler verilecek.'),
         o('grey', 'Gri kutu (test hesaplarıyla) (önerilen)', 'Her rolden test hesapları ve API belgesi verilir. Yetki, IDOR ve iş mantığı açıklarını bulmanın en verimli yoludur.', 'Üyelik, panel veya API olan projelerin çoğunda.', 'Müşteri, editör ve yönetici rollerinden birer test hesabı, iki ayrı test organizasyonu ve API belgesi verilir.', 'Test ekibine her rolden ve en az iki organizasyondan test hesabı ile API belgesi verilecek.'),
         o('white', 'Beyaz kutu (kaynak kodla)', 'Kaynak kod, mimari ve yapılandırma da paylaşılır; kod incelemesi ile canlı test birleştirilir. En kapsamlıdır, en çok zaman alır.', 'Finans, sağlık, kimlik doğrulama sağlayıcısı gibi yüksek riskli sistemlerde.', 'Ekip kaynak koddaki yetki ara katmanını inceleyip atlanabilen bir rotayı canlı ortamda doğrular.', 'Test ekibiyle kaynak kod, mimari ve yapılandırma gizlilik sözleşmesiyle paylaşılacak.'),
     ]},
    {'id': 'pentest_standard', 'type': 'multiselect', 'label': 'Test Standardı ve Metodoloji', 'en': 'Testing Standard', 'agents': [PEN],
     'explanation': 'Testin hangi standarda göre yapılacağını ve raporun neye göre eşleneceğini belirler. Standart, testin neyi kapsadığını ölçülebilir kılar.',
     'scenario': 'Web projelerinde OWASP WSTG ile ASVS birlikte; API ağırlıklı projelerde ayrıca OWASP API Top 10.',
     'example': 'Rapordaki her bulgu WSTG test kimliği ve ASVS gereksinim numarasıyla eşlenir.',
     'rule': 'Sızma testi şu standart ve metodolojilere göre yapılacak ve raporlanacaktır: {labels}.',
     'options': [
         o('wstg', 'OWASP Web Security Testing Guide (WSTG)', 'Web uygulaması testinin adım adım yöntem rehberi.', 'Her web projesinde.', 'Bulgu: WSTG-ATHZ-04 (IDOR).'),
         o('asvs', 'OWASP ASVS', 'Seviyeli doğrulama gereksinimleri; testin kabul ölçütü olarak kullanılır.', 'Gereksinim bazlı güvence istenen projelerde.', 'ASVS 4.1.2 gereksinimi karşılanmadı olarak işaretlenir.'),
         o('api_top10', 'OWASP API Security Top 10', 'API\'lere özgü en kritik on risk.', 'Ayrı API\'si olan projelerde.', 'Bulgu: API1:2023 Broken Object Level Authorization.'),
         o('ptes', 'PTES (Penetration Testing Execution Standard)', 'Ön görüşmeden raporlamaya kadar sızma testi sürecinin aşamaları.', 'Test sürecinin sözleşmede aşama aşama tanımlanması istenirse.', 'Ön görüşme, istihbarat toplama, tehdit modelleme, istismar ve raporlama aşamaları.'),
         o('nist115', 'NIST SP 800-115', 'Güvenlik testinin planlanması ve yürütülmesi için NIST rehberi.', 'Kamu, düzenlemeye tabi ya da uluslararası denetime giren projelerde.', 'Test planı NIST SP 800-115 aşamalarına göre hazırlanır.'),
     ],
     'recommend': {'field': 'pentest_scope', 'map': {'web': ['wstg', 'asvs'], 'api': ['api_top10'], 'authz': ['wstg']}}},
    {'id': 'pentest_asvs_level', 'type': 'select', 'label': 'ASVS Doğrulama Seviyesi', 'en': 'ASVS Verification Level', 'agents': [APPSEC],
     'showIf': [{'field': 'pentest_standard', 'in': ['asvs']}],
     'explanation': 'OWASP ASVS\'nin hangi seviyesine göre doğrulama yapılacağını belirler. Seviye yükseldikçe gereksinim sayısı ve derinliği artar.',
     'scenario': 'Kişisel veri işleyen çoğu iş uygulaması için Seviye 2; yalnız tanıtım sitelerinde Seviye 1; finans, sağlık ve kritik altyapıda Seviye 3.',
     'example': 'Seviye 2 seçilince oturum yönetimi, erişim denetimi ve kriptografi gereksinimlerinin tamamı kontrol listesine girer.',
     'rule': 'Doğrulama OWASP ASVS {label} gereksinimlerine göre yapılacaktır.',
     'options': [
         o('L1', 'Seviye 1 (temel)', 'Kara kutu testle doğrulanabilen asgari gereksinimler.', 'Kişisel veri işlemeyen, düşük riskli siteler.', 'Tanıtım sitesi ve iletişim formu.'),
         o('L2', 'Seviye 2 (standart) (önerilen)', 'Hassas veri işleyen uygulamaların çoğu için önerilen seviye.', 'Üyelik, e-ticaret, B2B portal ve SaaS uygulamaları.', 'Müşteri portalı ve yönetim paneli olan bir B2B platform.'),
         o('L3', 'Seviye 3 (yüksek güvence)', 'Kritik işlemler ve yüksek değerli veriler için en derin doğrulama.', 'Bankacılık, sağlık, kimlik doğrulama sağlayıcıları, kritik altyapı.', 'Ödeme kuruluşunun müşteri paneli.'),
     ]},
    {'id': 'pentest_schedule', 'type': 'multiselect', 'label': 'Test Zamanlaması', 'en': 'Testing Schedule', 'agents': [VULN, PEN],
     'explanation': 'Sızma testinin ve sürekli güvenlik kontrollerinin ne zaman yapılacağını belirler.',
     'scenario': 'En az canlıya çıkıştan önce bir test ve yılda bir tekrar; büyük değişikliklerde ek test; aradaki dönem için otomatik tarama ve açık bildirim politikası.',
     'example': 'Yayından iki hafta önce gri kutu test, her sürümde otomatik DAST taraması, sitede /.well-known/security.txt dosyası.',
     'rule': 'Güvenlik testleri şu zamanlarda yapılacaktır: {labels}.',
     'options': [
         o('prelaunch', 'Canlıya çıkmadan önce', 'İlk yayından önce, düzeltmeye zaman kalacak biçimde yapılan test.', 'Her yeni projede.', 'Yayın tarihinden en az iki hafta önce test, bir hafta önce yeniden test.', 'İlk canlıya çıkıştan önce, düzeltme ve yeniden test için zaman bırakılarak sızma testi yapılacak.'),
         o('major', 'Büyük sürüm ve mimari değişiklikten sonra', 'Yeni modül, ödeme, kimlik doğrulama ya da altyapı değişikliğinden sonra yapılan odaklı test.', 'Sürekli geliştirilen ürünlerde.', 'Yeni bayi portalı yayına girmeden önce yalnız o portal test edilir.', 'Kimlik doğrulama, yetki, ödeme ya da altyapıyı değiştiren büyük sürümlerden sonra odaklı test yapılacak.'),
         o('annual', 'Yılda en az bir kez', 'Düzenli tam kapsamlı test.', 'Kişisel veri işleyen ve sürekli yayında olan projelerde; birçok uyum çerçevesi bunu bekler.', 'Her yıl Mart ayında dış firma testi.', 'Yılda en az bir kez tam kapsamlı sızma testi yapılacak.'),
         o('ci_dast', 'Her sürümde otomatik tarama (DAST)', 'Test ortamına her dağıtımda otomatik dinamik güvenlik taraması; insan testinin yerine geçmez.', 'Sık yayın yapan ekiplerde.', 'Staging dağıtımından sonra ZAP taraması çalışır, yüksek bulguda hat durur.', 'Her sürümde test ortamında otomatik DAST taraması çalışacak; yüksek önemli bulgu yayını durduracak.'),
         o('vdp', 'Sürekli: açık bildirim politikası ve security.txt', 'Dışarıdan bulunan açıkların nasıl bildirileceğini ve iyi niyetli araştırmacının korunacağını açıklayan politika.', 'Herkese açık her sitede önerilir.', '/.well-known/security.txt dosyasında güvenlik e-postası ve politika adresi yer alır.', 'Açık bildirim politikası yayımlanacak ve /.well-known/security.txt (RFC 9116) dosyası eklenecek.'),
         o('bounty', 'Hata ödül programı (bug bounty)', 'Bulunan açıklar için araştırmacılara ödül verilen, kapsamı ve kuralları belirli program.', 'Olgun güvenlik süreçleri ve hızlı düzeltme kapasitesi olan büyük ürünlerde.', 'Program platformda kapsam, ödül tablosu ve kurallarla yayımlanır.', 'Kapsamı, kuralları ve ödül tablosu yazılı bir hata ödül programı yürütülecek.'),
     ]},
    {'id': 'pentest_executor', 'type': 'select', 'label': 'Testi Yapan', 'en': 'Test Performed By', 'agents': [PEN],
     'explanation': 'Sızma testini kimin yapacağını belirler. Bağımsızlık, bulguların tarafsızlığını ve denetimlerde kabul görmesini sağlar.',
     'scenario': 'Canlıya çıkış ve yıllık testlerde bağımsız dış uzman; ara dönemde iç ekip ve otomatik araçlar.',
     'example': 'Hibrit modelde her sürümde otomatik tarama ve iç inceleme yapılır, yılda bir bağımsız firma tam test yapar.',
     'rule': 'Sızma testini {label} yapacaktır.',
     'options': [
         o('external', 'Bağımsız dış firma / sertifikalı uzman', 'Geliştirme ekibinden bağımsız, deneyimli (ör. OSCP, OSWE, CREST sertifikalı) test ekibi.', 'Canlıya çıkış, yıllık test ve denetim gereken durumlarda.', 'Sözleşmeli güvenlik firması iki hafta gri kutu test yapar.', None),
         o('internal', 'Kurum içi güvenlik ekibi', 'Şirketin kendi uygulama güvenliği ekibi.', 'Güvenlik ekibi olan kurumlarda, ara dönem testlerinde.', 'İç ekip her büyük sürümde odaklı test yapar.', None),
         o('hybrid', 'Hibrit: otomatik tarama + iç inceleme + yıllık dış test', 'Sürekli otomatik tarama ve iç incelemeyi yılda en az bir bağımsız testle birleştirir.', 'Sürekli geliştirilen ürünlerin çoğunda.', 'CI\'da DAST, sürümlerde iç inceleme, yılda bir dış firma.', None),
     ]},
    {'id': 'pentest_env', 'type': 'select', 'label': 'Test Ortamı', 'en': 'Test Environment', 'agents': [PEN, VULN],
     'explanation': 'Testin hangi ortamda yapılacağını belirler. Test ortamı canlıya ne kadar benzerse bulgular o kadar gerçekçidir.',
     'scenario': 'Önerilen, canlının birebir kopyası olan ama gerçek kişisel veri içermeyen test (staging) ortamıdır.',
     'example': 'staging.alanadi.com canlıyla aynı sürüm ve yapılandırmada, sentetik verilerle test edilir.',
     'rule': 'Sızma testi {label} ortamında yapılacaktır.',
     'options': [
         o('staging', 'Canlı benzeri test ortamı (önerilen)', 'Aynı sürüm ve yapılandırma, sentetik veri; canlı sistem ve gerçek kullanıcılar etkilenmez.', 'Çoğu projede.', 'Test için ayrı veritabanı ve sahte ödeme anahtarları kullanılır.', 'Test ortamı canlıyla aynı sürüm ve yapılandırmada olacak, gerçek kişisel veri içermeyecek.'),
         o('production', 'Canlı ortam (onaylı zaman penceresiyle)', 'Gerçek yapılandırmayı test eder; kesinti ve veri riski nedeniyle onaylı zaman penceresi, yedek ve izleme gerektirir.', 'Test ortamı kurulamıyorsa veya altyapı / yapılandırma testi gerekiyorsa.', 'Gece 02:00–05:00 arasında, yedek alındıktan sonra, yıkıcı denemeler yapılmadan.', 'Canlı ortamda test yalnız onaylı zaman penceresinde, öncesinde yedek alınarak ve yıkıcı denemeler yapılmadan yürütülecek.'),
         o('both', 'İkisi birlikte', 'Uygulama açıkları test ortamında, altyapı ve yapılandırma canlıda sınanır.', 'Altyapısı ayrıca test edilmesi gereken projelerde.', 'Uygulama staging\'de, TLS ve DNS canlıda test edilir.', 'Uygulama testleri test ortamında, altyapı ve yapılandırma testleri canlıda onaylı pencerede yapılacak.'),
     ]},
    {'id': 'pentest_tools', 'type': 'multiselect', 'label': 'Otomatik Güvenlik Taramaları', 'en': 'Automated Security Scanning', 'agents': [CODE, VULN],
     'explanation': 'Sızma testleri arasındaki dönemi kapatan, geliştirme hattında (CI) çalışan otomatik taramaları belirler. İnsan eliyle yapılan testin yerine geçmez.',
     'scenario': 'Her projede en az bağımlılık ve gizli anahtar taraması; API ve panel olan projelerde DAST.',
     'example': 'Her birleştirme isteğinde Semgrep ve bağımlılık taraması, her staging dağıtımında ZAP taraması çalışır.',
     'rule': 'Geliştirme hattında şu otomatik güvenlik taramaları çalışacak, yüksek önemli bulgular birleştirmeyi ya da yayını durduracaktır: {labels}.',
     'options': [
         o('dast', 'DAST – çalışan uygulama taraması (ör. ZAP)', 'Çalışan uygulamaya dışarıdan saldırı denemeleri yapan tarayıcı.', 'Test ortamı olan projelerde.', 'Staging dağıtımından sonra ZAP temel taraması.'),
         o('sast', 'SAST – kaynak kod analizi (ör. Semgrep, CodeQL)', 'Kodda güvensiz kalıpları (innerHTML, ham SQL, sahiplik denetimi olmayan sorgu) arayan statik analiz.', 'Her projede.', 'Birleştirme isteğinde innerHTML kullanımı uyarı olarak işaretlenir.'),
         o('sca', 'Bağımlılık açığı taraması (SCA)', 'Kullanılan paketlerdeki bilinen açıkları (CVE) bulur.', 'Her projede.', 'npm audit / Dependabot yüksek önemli açıkta birleştirmeyi durdurur.'),
         o('secrets', 'Gizli anahtar taraması (ör. gitleaks)', 'Depoya yanlışlıkla eklenen API anahtarı, parola ve jetonları bulur.', 'Her projede; depo herkese açıksa zorunlu.', 'Commit öncesi kanca ve GitHub gizli bilgi koruması.'),
         o('iac', 'Konteyner ve altyapı kodu taraması', 'Docker imajları, Terraform / Kubernetes yapılandırmalarındaki açık ve yanlış ayarlar.', 'Konteyner veya altyapı kodu kullanan projelerde.', 'Trivy taraması kök kullanıcıyla çalışan imajı işaretler.'),
         o('headers', 'TLS ve güvenlik başlığı denetimi', 'TLS sürümü, sertifika, HSTS, CSP ve diğer güvenlik başlıklarının düzenli kontrolü.', 'Her canlı sitede.', 'Haftalık otomatik denetim CSP\'nin yanlışlıkla kaldırıldığını bildirir.'),
     ]},
    {'id': 'pentest_rules', 'type': 'multiselect', 'label': 'Test Kuralları (Rules of Engagement)', 'en': 'Rules of Engagement', 'agents': [PEN],
     'explanation': 'Test başlamadan kararlaştırılan, testin hukuki ve operasyonel sınırlarını çizen kurallardır.',
     'scenario': 'Her sızma testinde yazılı yetki ve kapsam belgesi zorunludur; diğer kurallar ortam ve kapsama göre seçilir.',
     'example': 'İmzalı yetki belgesinde kapsamdaki adresler, tarih aralığı, test IP\'leri, yasak denemeler ve acil durum telefonu yer alır.',
     'rule': 'Sızma testi şu kurallarla yürütülecektir: {labels}.',
     'options': [
         o('auth_doc', 'Yazılı yetki ve kapsam belgesi', 'Kapsam, tarih aralığı, test IP adresleri ve yetkili kişilerin imzasını içeren belge. İzinsiz test TCK m. 243–244 kapsamında suç oluşturabilir.', 'Her testte.', 'Test, imzalı belge ulaşmadan başlamaz.', 'Test, kapsam, tarih aralığı ve test IP adreslerini içeren imzalı yetki belgesi olmadan başlamayacak.'),
         o('accounts', 'Test hesapları ve sentetik veri', 'Her rol ve organizasyon için ayrı test hesabı; gerçek kişi verisi kullanılmaz.', 'Gri ve beyaz kutu testlerde.', 'Müşteri-A, Müşteri-B ve Yönetici test hesapları.', 'Her rol ve en az iki organizasyon için test hesabı ve sentetik veri hazırlanacak.'),
         o('no_dos', 'Hizmet engelleme ve yıkıcı deneme yasağı', 'Yük / DoS saldırısı, veri silme ve kalıcı değişiklik yapılmaz; yük testi ayrı planlanır.', 'Özellikle canlı ortamda.', 'Kayıt silme açığı bulunduğunda yalnız kendi test kaydı üzerinde kanıtlanır.', 'Hizmet engelleme, veri silme ve kalıcı değişiklik içeren denemeler yapılmayacak.'),
         o('data_safety', 'Kişisel veriye erişimde dur ve bildir', 'Test sırasında gerçek kişisel veriye ulaşılırsa test durdurulur, veri kopyalanmaz, kanıt maskelenir ve sorumluya hemen bildirilir.', 'Kişisel veri işleyen her projede.', 'IDOR ile gerçek müşteri kaydı görülünce yalnız kayıt kimliği maskelenerek raporlanır.', 'Gerçek kişisel veriye ulaşılırsa test durdurulacak, veri kopyalanmayacak, kanıt maskelenecek ve sorumluya hemen bildirilecek.'),
         o('emergency', 'Acil durdurma ve iletişim kişisi', 'Kesinti veya beklenmeyen etki olduğunda testi durduracak, iki tarafta da 7/24 ulaşılabilir kişiler.', 'Her testte.', 'Test ekibi ve proje tarafından birer nöbetçi telefon.', 'İki tarafta da ulaşılabilir acil durum kişileri ve testi durdurma yöntemi tanımlanacak.'),
         o('secure_share', 'Bulguların şifreli paylaşımı ve saklama süresi', 'Rapor ve kanıtlar şifreli kanaldan paylaşılır, saklama ve imha süresi belirlenir.', 'Her testte.', 'Rapor şifreli arşivle, parola ayrı kanaldan iletilir; test verisi 90 gün sonra imha edilir.', 'Rapor ve kanıtlar şifreli kanaldan paylaşılacak; saklama ve imha süresi belirlenecek.'),
     ]},
    {'id': 'pentest_report', 'type': 'multiselect', 'label': 'Rapor İçeriği', 'en': 'Report Contents', 'agents': [PEN, VULN],
     'explanation': 'Sızma testi raporunda bulunması gereken bölümleri belirler.',
     'scenario': 'Her raporda önem puanı, kanıt, yeniden üretim adımları ve düzeltme önerisi; yönetime sunulacaksa yönetici özeti.',
     'example': 'Bulgu: IDOR · CVSS 8.1 · /api/invoices/{id} · adım adım yeniden üretim · düzeltme: organizasyon koşullu sorgu · ASVS 4.2.1.',
     'rule': 'Sızma testi raporu şunları içerecektir: {labels}.',
     'options': [
         o('exec', 'Yönetici özeti', 'Teknik olmayan okuyucu için genel risk durumu ve öncelikli eylemler.', 'Yönetime veya müşteriye sunulacak raporlarda.', 'Bir sayfalık özet: 1 kritik, 3 yüksek bulgu ve öncelikli üç eylem.'),
         o('cvss', 'CVSS v4.0 puanı ve iş etkisi', 'Her bulgunun ortak ölçüyle önem derecesi ve projeye özgü etkisi.', 'Her raporda.', 'CVSS 8.1 (Yüksek) — müşteri faturaları başka şirketlerce görülebilir.'),
         o('repro', 'Kanıt ve adım adım yeniden üretim', 'İstek / yanıt örnekleri, ekran görüntüleri ve geliştiricinin açığı tekrar oluşturabileceği adımlar.', 'Her raporda.', 'İstek, yanıt ve hangi hesapla denendiği.'),
         o('fix', 'Düzeltme önerisi ve referans', 'Açığın nasıl kapatılacağı ve ilgili OWASP / CWE referansı.', 'Her raporda.', 'Öneri: sorguya organization_id koşulu; CWE-639.'),
         o('mapping', 'OWASP Top 10 / ASVS / WSTG eşlemesi', 'Bulguların standart maddelerle eşlenmesi; kapsanan ve eksik kalan maddelerin listesi.', 'Standarda göre yapılan testlerde.', 'API1:2023, ASVS 4.2.1, WSTG-ATHZ-04.'),
         o('retest', 'Düzeltme sonrası yeniden test sonucu', 'Her bulgunun kapatılıp kapatılmadığının yeniden test edilerek raporlanması.', 'Her testte.', 'Bulgu 3: düzeltildi (yeniden test 12 Aralık).'),
     ]},
    {'id': 'pentest_sla', 'type': 'select', 'label': 'Bulgu Düzeltme Süreleri', 'en': 'Remediation SLA', 'agents': [VULN],
     'explanation': 'Bulguların önem derecesine göre en geç ne kadar sürede kapatılacağını belirler.',
     'scenario': 'Kişisel veri veya ödeme işleyen projelerde sıkı süreler; düşük riskli tanıtım sitelerinde standart süreler.',
     'example': 'Kritik bir IDOR bulgusu 48 saat içinde kapatılır ve yeniden test edilir.',
     'rule': 'Bulgu düzeltme süreleri: {label}. Süresinde kapatılamayan bulgu için yazılı risk kabulü ve geçici önlem gerekecektir.',
     'options': [
         o('strict', 'Sıkı: Kritik 48 saat · Yüksek 7 gün · Orta 30 gün · Düşük 90 gün', 'Kişisel veri, ödeme veya kritik iş süreci olan projeler için.', 'E-ticaret, SaaS, B2B portal, sağlık ve finans.', 'Kritik bulgu hafta sonu bile 48 saat içinde kapatılır.'),
         o('standard', 'Standart: Kritik 7 gün · Yüksek 30 gün · Orta 90 gün · Düşük sonraki sürüm', 'Orta riskli projeler için yaygın düzen.', 'Kurumsal site, blog, içerik platformu.', 'Yüksek bulgu bir sonraki iki haftalık sprintte kapatılır.'),
         o('risk_based', 'Risk bazlı: her bulgu için ayrı karar ve yazılı risk kabulü', 'Süre bulgu bazında güvenlik sorumlusu ve proje sahibiyle belirlenir; kapatılmayan bulgu için yazılı risk kabulü alınır.', 'Kaynakları kısıtlı ya da özel uyum gereksinimi olan projelerde.', 'Orta bulgu için geçici WAF kuralı ve 60 günlük süre yazılı olarak kabul edilir.'),
     ]},
    {'id': 'pentest_gate', 'type': 'boolean', 'label': 'Kritik Bulguda Canlıya Çıkışı Durdur', 'en': 'Block Release on Critical Findings', 'agents': [VULN, PEN],
     'explanation': 'Kapatılmamış kritik veya yüksek önemli bir sızma testi bulgusu varken canlıya çıkışın engellenip engellenmeyeceğini belirler.',
     'scenario': 'Kişisel veri, ödeme ya da panel içeren her projede önerilir.',
     'example': 'Yeniden testte IDOR bulgusu hâlâ açıksa yayın tarihi ertelenir.',
     'rule': 'Kapatılmamış kritik veya yüksek önemli sızma testi bulgusu varken canlıya çıkış engellenmesi {booltext}.',
     'yes': {'scenario': 'Müşteri verisi, ödeme veya yönetim paneli olan bir projede yayın tarihi güvenlikten önce gelmemeliyse.', 'example': 'Canlıya Çıkış kalite kapısında “Açık kritik / yüksek bulgu yok” maddesi işaretlenmeden yayın yapılmaz.'},
     'no': {'scenario': 'Kişisel veri işlemeyen, kısa ömürlü bir tanıtım sayfasında bulgular yayından sonra kapatılabilir.', 'example': 'Orta önemli bir başlık eksikliği yayından sonraki ilk bakımda giderilir.'}},
]

for f in PT:
    f['section'] = SECTION['id']
    for x in f.get('options') or []:
        if x.get('ruleDetail') is None:
            x.pop('ruleDetail', None)
for x in VULN_FIELD['options']:
    if x.get('ruleDetail') is None:
        x.pop('ruleDetail', None)

out = {'version': 1, 'fields_into': [VULN_FIELD], 'guide_add': {'security_eng': SEC_GUIDE_ADD},
       'section': SECTION, 'guide': GUIDE, 'fields': PT}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'guvenlik.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('yazıldı:', p, '· bölüm alanı', len(PT), '· zafiyet seçenekleri', len(VULN_FIELD['options']))
