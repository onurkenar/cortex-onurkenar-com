# -*- coding: utf-8 -*-
"""Panel & Portal Mimarisi kaynak verisi (2026-11-08, kullanıcının "Web Project Configurator — Panel & Portal
Architecture" yönergesi). Çalıştırınca yanına panel-portal.json yazar; uygulamaya panel_portal_ekle.py işler.

python3 -I docs/panel-portal/kaynak.py   →   docs/panel-portal/panel-portal.json
"""
import json, os

SWE = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
OPS = 'poz:bilgi-teknolojileri:15.05/devops-sre-ve-yayin-yonetimi/kidemli-devops-muhendisi'
SEC = 'poz:siber-guvenlik:16.06/devsecops-ve-kod-guvenligi/kod-guvenligi-uzmani'
DBA = 'poz:bilgi-teknolojileri:15.02/veritabani-yonetimi/kidemli-veritabani-yoneticisi'
API = 'poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani'

SECTION = {
    'id': 'panels', 'after': 'architecture', 'group': 'Teknik Mimari', 'icon': '▣',
    'name': 'Panel & Portal Mimarisi', 'en': 'Panel & Portal Architecture',
    'desc': 'Projede hangi yönetim panellerinin ve kullanıcı portallarının olacağını, her birinin adresini, hangi uygulamadan sunulacağını, kimlik doğrulama ve yetki yapısını, modüllerini, veri izolasyonunu ve dağıtımını belirler.',
}

GUIDE = {
    'purpose': 'Bir web projesinde herkese açık sitenin yanında çoğu zaman bir veya birkaç kapalı alan bulunur: içerik yönetimi, operasyon, müşteri portalı, tedarikçi ya da bayi paneli, çalışan portalı… Bu bölüm her panelin kimin için olduğunu, hangi adresten açılacağını, hangi uygulama tarafından sunulacağını, kimlerin hangi modüllere hangi yetkiyle erişeceğini ve verinin nasıl ayrılacağını baştan netleştirir. Kararlar netleşmeden yazılan panellerde adres çakışmaları, birbirine sızan oturumlar ve yalnız menüyü gizleyerek yapılan “yetkilendirme” en sık görülen sorunlardır.',
    'criteria': [
        'Önce paneli kullanacak kişileri yazın: platform yöneticisi, editör, müşteri, tedarikçi, bayi, çalışan, denetçi. Her kullanıcı grubunun ayrı bir panele mi, yoksa aynı panelde farklı bir role mi ihtiyacı olduğunu buna göre seçin.',
        'Adres yaklaşımı (alt alan adı, alt dizin, ayrı alan adı) ile uygulama sınırını ayrı düşünün. admin.alanadi.com adresi ayrı bir uygulama olmak zorunda değildir; aynı uygulama ana makine adına (host) göre yönlendirme yapabilir.',
        'Yazılım mimarisi (monolith, modüler monolith, microservices) ile dağıtım topolojisi (kaç dağıtım birimi, nerede çalıştığı) farklı kararlardır. Tek kod tabanı birden fazla birim olarak dağıtılabilir; ayrı ön yüz uygulamaları tek bir API’yi paylaşabilir.',
        'Bir kullanıcının birden fazla organizasyona üye olup olmayacağını ve her organizasyonda farklı rol taşıyıp taşımayacağını erken belirleyin; bu karar veritabanı modelini (kullanıcı, organizasyon, üyelik, rol, izin) doğrudan değiştirir.',
        'Rol bazlı yetki (RBAC) çoğu proje için yeterli başlangıçtır. Kayıt sahibi, bölge, tutar sınırı gibi koşullar gerekiyorsa RBAC’ın üstüne nitelik bazlı (ABAC) kurallar eklenir.',
        'Yönetim panellerinde çok adımlı doğrulama, kısa oturum, denetim kaydı ve arama motorlarından gizleme (noindex) varsayılan olmalıdır.',
    ],
    'pitfalls': [
        'Menüde bir bağlantıyı gizlemeyi yetkilendirme sanmak. Gizlenen sayfa adresi bilinerek açılabilir; her istek sunucuda rol, izin ve organizasyon bağlamıyla denetlenmelidir.',
        'İstekle gelen kayıt kimliğinin (sipariş, fatura, belge id) kullanıcının organizasyonuna ait olup olmadığını kontrol etmemek. Bu açık (IDOR / BOLA) en sık rastlanan API güvenlik açığıdır.',
        'Alt alan adları arasında oturum paylaşmak için çerezi üst alan adına (Domain=.alanadi.com) yazmak. Bütün alt alan adları bu çereze erişir; tek bir zayıf alt alan adı yönetim oturumunu ele geçirebilir.',
        'Alt alan adlarının “aynı site” (same-site) sayıldığını unutmak. SameSite çerez ayarı kardeş alt alan adından gelen sahte isteğe karşı tek başına koruma sağlamaz; CSRF jetonu gerekir.',
        'Yönetim panelini herkese açık siteyle aynı kökende (alt dizinde) tutup kullanıcı içeriği (yorum, forum, profil) yayınlamak. Herkese açık sayfadaki bir XSS açığı aynı kökendeki yönetim paneline ulaşabilir.',
        'Panel adreslerini /api, /auth, /static, www gibi altyapının kullandığı yollarla çakıştırmak.',
    ],
    'resources': [
        {'title': 'OWASP – Authorization Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html', 'note': 'Varsayılan olarak reddetme, her istekte yetki denetimi, en az yetki ve RBAC / ABAC tercihlerini anlatan resmî OWASP rehberi.'},
        {'title': 'OWASP API Security – Broken Object Level Authorization', 'url': 'https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization/', 'note': 'Kayıt kimliği üzerinden başka kullanıcının veya organizasyonun verisine erişme açığı (IDOR / BOLA) ve önlemleri.'},
        {'title': 'OWASP – Session Management Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html', 'note': 'Oturum çerezi özellikleri (Secure, HttpOnly, SameSite, Domain, Path), oturum süresi ve yenileme kuralları.'},
        {'title': 'OWASP – Cross-Site Request Forgery Prevention', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html', 'note': 'CSRF jetonu, imzalı çift gönderim çerezi ve alt alan adlarından gelen saldırılara karşı önlemler.'},
        {'title': 'MDN – Set-Cookie', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Set-Cookie', 'note': 'Domain, Path, __Host- ve __Secure- önekleri ile SameSite değerlerinin tarayıcıdaki davranışı.'},
        {'title': 'MDN – Cross-Origin Resource Sharing (CORS)', 'url': 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS', 'note': 'Farklı kökendeki panelin API’ye kimlik bilgisiyle istek atabilmesi için gereken başlıklar.'},
        {'title': 'web.dev – Same-site ve same-origin', 'url': 'https://web.dev/articles/same-site-same-origin', 'note': 'Alt alan adlarının neden aynı site sayıldığını ve bunun çerez güvenliğine etkisini açıklar.'},
        {'title': 'NIST – Role Based Access Control', 'url': 'https://csrc.nist.gov/projects/role-based-access-control', 'note': 'RBAC modelinin temel kavramları: kullanıcı, rol, izin, oturum ve rol hiyerarşisi.'},
        {'title': 'NIST SP 800-162 – ABAC rehberi', 'url': 'https://csrc.nist.gov/pubs/sp/800/162/upd2/final', 'note': 'Nitelik bazlı erişim denetiminin (ABAC) tanımı ve RBAC’ın üstüne nasıl genişletileceği.'},
        {'title': 'Microsoft – Çok kiracılı çözümlerde kiracı modelleri', 'url': 'https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/considerations/tenancy-models', 'note': 'Ortak şema, kiracı başına şema ve kiracı başına veritabanı modellerinin maliyet, izolasyon ve işletim karşılaştırması.'},
        {'title': 'OpenID Connect Core 1.0', 'url': 'https://openid.net/specs/openid-connect-core-1_0.html', 'note': 'Farklı alan adlarındaki paneller arasında tek oturum açma (SSO) için kullanılan standart kimlik protokolü.'},
    ],
}


def o(value, label, explanation, scenario, example, rd=None):
    x = {'value': value, 'label': label, 'explanation': explanation, 'scenario': scenario, 'example': example}
    if rd:
        x['ruleDetail'] = rd
    return x


SITE_SMALL = ['Corporate Website', 'Personal Website', 'Portfolio', 'Blog', 'News Media', 'Landing Page', 'Knowledge Base', 'Event', 'Nonprofit', 'Directory']

FIELDS = [
    {'id': 'panel_inventory', 'label': 'Panel ve Portal Envanteri', 'en': 'Panel & Portal Inventory', 'type': 'panels', 'agents': [SWE, SEC], 'options': [],
     'explanation': 'Projede kurulacak yönetim panellerini ve kullanıcı portallarını tanımlar: her panelin adresi, sunan uygulaması, kimlik doğrulaması, rolleri ve izinleri, modülleri, veri kapsamı, arayüzü, güvenlik önlemleri ve dağıtımı. Şablondan ekleyebilir, önerilen başlangıç mimarisini uygulayabilir ya da özel panel oluşturabilirsiniz.',
     'scenario': 'Sitenin herkese açık sayfaları dışında oturum açılarak kullanılan her alan için bir panel tanımlanır: içerik yönetimi, operasyon, müşteri, tedarikçi, bayi, çalışan veya çalışma alanı.',
     'example': 'Bir B2B pazar yerinde müşteri portalı portal.alanadi.com, tedarikçi portalı supplier.alanadi.com, yönetim paneli admin.alanadi.com adresinden açılır; üçü aynı uygulamadan sunulabilir.',
     'rule': 'Projedeki yönetim panelleri ve kullanıcı portalları Panel & Portal Envanteri’nde tanımlanmıştır; adresler, sunan uygulamalar, roller, izinler, modüller ve veri kapsamı PANEL VE PORTAL MİMARİSİ bölümüne göre uygulanacak, envanterde olmayan panel açık onay olmadan eklenmeyecektir.'},
    {'id': 'panel_url_strategy', 'label': 'Panel Adres (URL) Yaklaşımı', 'en': 'Panel URL Strategy', 'type': 'select', 'agents': [SWE, OPS],
     'explanation': 'Panellerin herkese açık siteye göre hangi adres yapısıyla açılacağının genel kuralıdır. Yeni eklenen paneller bu yaklaşımla başlar; Hibrit seçilirse her panelin adresi ayrı belirlenir.',
     'scenario': 'Tek bir içerik yönetim paneli olan kurumsal sitede alt dizin, birden çok portalı olan pazar yeri veya SaaS platformunda hibrit yapı en sık tercih edilir.',
     'example': 'Alt dizinde içerik paneli alanadi.com/admin adresinden, hibrit yapıda müşteri portalı portal.alanadi.com, yönetim paneli admin.alanadi.com adresinden açılır.',
     'rule': 'Panellerin genel adres yaklaşımı {label} olacaktır. Panel bazlı adresler Panel & Portal envanterindeki URL tanımlarına uyacak, yeni panel adresi açık onay olmadan eklenmeyecektir.',
     'options': [
         o('subdomain', 'Alt alan adı (admin.alanadi.com)', 'Her panel kendi alt alan adında açılır. Paneller tarayıcı açısından ayrı köken (origin) olur; çerezler ve depolama birbirinden ayrılır, panel başına ayrı güvenlik başlığı ve önbellek kuralı kolaylaşır. DNS kaydı ve sertifika yönetimi gerektirir.',
           'Müşteri, tedarikçi ve yönetim panelleri ayrı kitlelere hizmet veriyorsa ve panellerin birbirinden yalıtılması isteniyorsa.',
           'portal.alanadi.com müşteri portalı, admin.alanadi.com yönetim paneli; ikisi aynı uygulamadan ana makine adına göre yönlendirilebilir.',
           'Her panel ayrı köken olarak ele alınacak; oturum çerezi varsayılan olarak yalnız kendi ana makinesine (host-only) yazılacak, alt alan adları aynı site sayıldığı için CSRF jetonu zorunlu olacaktır.'),
         o('subdirectory', 'Alt dizin (alanadi.com/admin)', 'Panel, herkese açık siteyle aynı alan adında bir yol altında açılır. Kurulumu en kolay yöntemdir; aynı köken olduğu için çerez ve depolama paylaşılır, Path ayarı güvenlik sınırı değildir.',
           'Tek bir yönetim paneli olan kurumsal site, blog veya kampanya sitesinde.',
           'alanadi.com/admin içerik paneli, alanadi.com/hesabim üye paneli.',
           'Paneller herkese açık siteyle aynı kökende olduğu için panel rotalarında katı CSP, ayrı çerez adı, CSRF jetonu, no-store önbellek ve X-Robots-Tag: noindex uygulanacaktır.'),
         o('separate_domain', 'Ayrı alan adı (baskaalanadi.com)', 'Panel tamamen farklı bir alan adında açılır. Herkese açık siteden en güçlü ayrımı sağlar (farklı site); ortak oturum ancak OpenID Connect gibi yönlendirmeli bir protokolle kurulabilir.',
           'Bayi veya tedarikçi portalı ayrı bir marka altında sunulacaksa ya da yönetim paneli kurumsal ağ alan adında tutulacaksa.',
           'Bayi portalı bayi-markasi.com, yönetim paneli yonetim.sirket-ic.com adresinden açılır.',
           'Ayrı alan adındaki paneller farklı site sayılacak; paneller arası oturum yalnız OpenID Connect / SAML yönlendirmesiyle kurulacak, çerez paylaşılmayacaktır.'),
         o('hybrid', 'Hibrit (panel bazlı)', 'Her panelin adres yapısı ayrı seçilir: örneğin üye paneli alt dizinde, yönetim paneli alt alan adında, bayi portalı ayrı alan adında. Esnektir; her panel için çerez, CORS ve CSRF kuralları ayrı tanımlanmalıdır.',
           'Pazar yeri, B2B platform, SaaS veya e-ticaret gibi birden fazla kitleye panel sunan projelerde.',
           'alanadi.com/hesabim üye paneli, admin.alanadi.com yönetim paneli, supplier.alanadi.com tedarikçi portalı.',
           'Her panelin adres türü envanterde ayrı tanımlanacak; panel başına çerez kapsamı, CORS izin listesi ve CSRF kuralı o panelin adres türüne göre uygulanacaktır.'),
     ],
     'recommend': {'field': 'project_type', 'map': dict([(t, ['subdirectory']) for t in SITE_SMALL] + [
         ('SaaS', ['hybrid']), ('Web App', ['hybrid']), ('Portal', ['subdomain']), ('Community', ['subdirectory']), ('Marketplace', ['hybrid']),
         ('E-commerce', ['hybrid']), ('B2B Platform', ['hybrid']), ('Booking', ['hybrid']), ('Classifieds', ['hybrid']), ('LMS', ['hybrid']),
         ('Intranet', ['subdomain']), ('Government', ['hybrid'])])}},

    {'id': 'panel_app_topology', 'label': 'Panel Uygulama Topolojisi', 'en': 'Panel Application Topology', 'type': 'select', 'agents': [SWE],
     'explanation': 'Panellerin kaç uygulama tarafından sunulacağını belirler. Yazılım mimarisinden (Mimari & Kodlama Yaklaşımı › Uygulama Mimarisi) ayrıdır: modüler monolith bir arka uç, birden çok ön yüz uygulamasına hizmet verebilir.',
     'scenario': 'Az sayıda panelde tek uygulama; farklı ekiplerin farklı panelleri geliştirdiği ya da panellerin teknoloji ihtiyacının ayrıştığı projelerde ayrı ön yüz uygulamaları uygundur.',
     'example': 'Tek uygulamada /admin ve portal.alanadi.com aynı kod tabanından sunulur; ayrı ön yüz yapısında yönetim paneli ve müşteri portalı ayrı uygulamalardır, ikisi aynı API’yi kullanır.',
     'rule': 'Panel uygulama topolojisi {label} olacaktır. Bu karar yazılım mimarisinden ayrı tutulacak; bir panelin hangi uygulamadan sunulduğu envanterdeki “Uygulama” alanına uyacaktır.',
     'options': [
         o('single_app', 'Tek uygulama, panel başına rota grubu', 'Bütün paneller aynı uygulamanın içinde ayrı rota grupları (ve gerekirse ana makine adına göre yönlendirme) olarak yer alır. Kod paylaşımı ve yayın en basittir; panel sınırları modül ve yetki katmanıyla korunmalıdır.',
           'Ekip küçük, panel sayısı birkaç taneyse ve paneller aynı teknolojiyle yazılacaksa.',
           'Tek bir Next.js / Laravel uygulamasında /admin, /hesabim ve portal.alanadi.com rotaları birlikte durur.',
           'Paneller tek uygulamada ayrı rota grupları olarak geliştirilecek; panel rotaları ortak yetki ara katmanından (middleware) geçecek, paneller arası doğrudan modül bağımlılığı kurulmayacaktır.'),
         o('separate_frontends', 'Ayrı ön yüz uygulamaları + ortak API', 'Her panel (veya panel grubu) ayrı bir ön yüz uygulamasıdır; iş kuralları ve veri erişimi tek bir ortak API / arka uçta durur. Panel arayüzleri bağımsız yayınlanır, yetki kuralları tek yerde kalır.',
           'Yönetim paneli ile müşteri portalının arayüz ihtiyaçları ve yayın takvimleri farklıysa.',
           'admin uygulaması ve portal uygulaması ayrı depolarda veya monorepo paketlerinde; ikisi api.alanadi.com’u çağırır.',
           'Panel ön yüzleri ayrı uygulamalar olacak, yetki ve iş kuralları yalnız ortak API’de uygulanacak; ön yüzlerde yetki kararı verilmeyecektir.'),
         o('per_panel', 'Panel başına bağımsız uygulama', 'Her panel kendi ön yüzü ve arka ucuyla ayrı bir uygulamadır. En güçlü ayrımı sağlar; ortak kimlik, veri tutarlılığı ve izleme için ek altyapı (kimlik sağlayıcı, olay akışı, API ağ geçidi) gerekir.',
           'Paneller ayrı ekiplerce yönetiliyor, farklı ölçeklenme ve uyum gereksinimleri varsa.',
           'Satıcı paneli ve operasyon paneli ayrı servisler olarak çalışır, ortak kimlik sağlayıcıyla oturum açar.',
           'Her panel bağımsız uygulama olarak kurulacak; ortak kimlik sağlayıcı, servisler arası yetki jetonu ve merkezi denetim kaydı zorunlu olacaktır.'),
         o('hybrid', 'Hibrit', 'Bazı paneller aynı uygulamada, bazıları ayrı uygulamada sunulur. Örneğin içerik paneli ve üye paneli ana uygulamada, çalışma alanı uygulaması ayrı bir ön yüzde.',
           'Projenin bir kısmı basit, bir kısmı bağımsız ölçeklenmesi gereken bir ürünse.',
           'alanadi.com ve /admin ana uygulamada; app.alanadi.com ayrı SaaS ön yüzü.',
           'Hangi panelin hangi uygulamadan sunulduğu envanterde açıkça yazılacak; uygulamalar arası ortak kod paylaşılan paketlerle yönetilecektir.'),
     ],
     'recommend': {'field': 'architecture_style', 'map': {'Monolith': ['single_app'], 'Modular Monolith': ['single_app'], 'Microservices': ['separate_frontends'], 'Serverless': ['separate_frontends'], 'Event Driven': ['separate_frontends']}}},

    {'id': 'panel_deploy_topology', 'label': 'Panel Dağıtım Topolojisi', 'en': 'Panel Deployment Topology', 'type': 'select', 'agents': [OPS],
     'explanation': 'Panellerin kaç dağıtım birimi olarak yayına alınacağını belirler. Uygulama topolojisinden ayrıdır: tek kod tabanı birden çok birim olarak dağıtılabilir, ayrı uygulamalar aynı birimde çalışabilir.',
     'scenario': 'Yönetim paneli herkese açık siteden ayrı yayınlanmak, ayrı ölçeklenmek veya ayrı ağda (iç ağ, erişim kontrollü) çalıştırılmak isteniyorsa ayrı dağıtım birimi seçilir.',
     'example': 'Tek birimde site ve paneller tek seferde yayına alınır; ayrı birimlerde yönetim paneli yalnız şirket ağından veya Cloudflare Access arkasından erişilebilen ayrı bir dağıtımdır.',
     'rule': 'Panellerin dağıtım topolojisi {label} olacaktır. Panel bazlı dağıtım sınırı envanterdeki “Dağıtım sınırı” alanına uyacaktır.',
     'options': [
         o('single_unit', 'Tek dağıtım birimi', 'Site ve bütün paneller tek seferde, aynı ortamda yayına alınır. En basit işletimdir; bir paneldeki hata tüm sistemi etkileyebilir.', 'Küçük ve orta projelerde.', 'Bir Cloudflare Workers projesi hem siteyi hem /admin panelini sunar.', 'Site ve paneller tek dağıtım birimi olarak yayınlanacak; panel rotaları için ayrı önbellek ve güvenlik başlığı kuralları tanımlanacaktır.'),
         o('per_app', 'Uygulama başına ayrı dağıtım', 'Her uygulama kendi dağıtım birimidir; ayrı yayın, ayrı ölçek, ayrı erişim kuralı uygulanabilir.', 'Ayrı ön yüz uygulamaları veya bağımsız paneller seçildiyse.', 'Müşteri portalı ve yönetim paneli ayrı projeler olarak yayınlanır; yönetim paneli erişim kontrollü ağın arkasındadır.', 'Her uygulama ayrı dağıtım birimi olacak; birimler arası ortak yapılandırma ve gizli anahtarlar merkezi olarak yönetilecektir.'),
         o('hybrid', 'Hibrit', 'Bazı paneller ana uygulamayla birlikte, bazıları ayrı birim olarak yayınlanır.', 'Yalnız yönetim panelinin ayrı ağda tutulması isteniyorsa.', 'Site ve üye paneli birlikte; admin.alanadi.com ayrı birim.', 'Ayrı yayınlanacak paneller envanterde “Ayrı dağıtım” olarak işaretlenecektir.'),
     ],
     'recommend': {'field': 'panel_app_topology', 'map': {'single_app': ['single_unit'], 'separate_frontends': ['per_app'], 'per_panel': ['per_app'], 'hybrid': ['hybrid']}}},

    {'id': 'panel_identity', 'label': 'Paneller Arası Kimlik Doğrulama', 'en': 'Cross-Panel Authentication', 'type': 'select', 'agents': [SWE, SEC],
     'explanation': 'Bir kullanıcının birden çok panele aynı hesapla mı girdiğini ve oturumun paneller arasında nasıl taşındığını belirler. Kimlik doğrulama altyapısı (Kimlik Doğrulama & Güvenlik › Kimlik Doğrulama Yöntemi) ayrı bir karardır.',
     'scenario': 'Aynı kişi hem müşteri portalını hem destek panelini kullanıyorsa ortak kimlik; dış kullanıcılarla çalışanların kimliği tamamen ayrı tutulmak isteniyorsa ayrı kimlik seçilir.',
     'example': 'Ortak kimlikte kullanıcı portal.alanadi.com’a giriş yaptıktan sonra support.alanadi.com’a geçtiğinde parola sorulmadan kimlik sağlayıcı üzerinden oturum açılır; her panelin kendi oturum çerezi vardır.',
     'rule': 'Paneller arası kimlik doğrulama {label} olacaktır. Bir kullanıcının panel erişimi hesabın değil, üyeliğinin (organizasyon + rol) özelliği olarak sunucuda denetlenecektir.',
     'options': [
         o('shared_idp', 'Ortak kimlik sağlayıcı, panel başına oturum (SSO)', 'Tek kullanıcı deposu ve tek giriş sayfası (kimlik sağlayıcı) vardır; her panel kendi oturum çerezini OpenID Connect benzeri bir akışla alır. Oturumlar birbirinden ayrı sonlandırılabilir.', 'Alt alan adı veya ayrı alan adı kullanan, birden çok paneli olan projelerde önerilir.', 'auth.alanadi.com giriş sayfası; admin ve portal kendi çerezlerini alır.', 'Tek kullanıcı deposu ve ortak giriş akışı kullanılacak; her panel kendi oturumunu kendi ana makinesine yazacak, oturum çerezi üst alan adına yazılmayacaktır.'),
         o('shared_session', 'Ortak oturum (tek çerez)', 'Bütün paneller aynı oturum çerezini kullanır. Alt dizin yapısında doğaldır; alt alan adlarında çerezin üst alan adına yazılmasını gerektirir ve bütün alt alan adlarını aynı güven düzeyine bağlar.', 'Paneller aynı alan adında alt dizinlerdeyse.', 'alanadi.com/hesabim ve alanadi.com/admin aynı oturumla açılır; admin yetkisi rolden gelir.', 'Paneller tek oturumu paylaşacak; yönetim paneline girişte ek doğrulama (step-up) istenecek, oturum çerezi alt alan adlarına açılmayacaktır.'),
         o('separate', 'Panel başına ayrı kimlik', 'Her panelin kendi kullanıcı deposu ve giriş sayfası vardır. En güçlü ayrımı sağlar; aynı kişi için birden çok hesap ve parola oluşur.', 'Çalışanlar ile dış kullanıcıların hiçbir ortak hesap paylaşmaması gerektiğinde.', 'Yönetim paneli kurumsal hesapla, müşteri portalı müşteri hesabıyla girilir.', 'Her panel kendi kullanıcı deposunu kullanacak; paneller arası hesap eşleştirmesi yapılmayacaktır.'),
         o('hybrid', 'Hibrit (iç paneller kurumsal SSO, dış portallar ortak kimlik)', 'Çalışan panelleri kurumsal kimlik sağlayıcıyla (Microsoft Entra, Google Workspace, Okta), dış portallar projenin kendi kullanıcı deposuyla açılır.', 'Hem çalışan hem müşteri / tedarikçi panelleri olan projelerde.', 'admin.alanadi.com kurumsal SSO, portal.alanadi.com e-posta + parola veya passkey ile açılır.', 'Kurum içi paneller kurumsal kimlik sağlayıcıya, dış portallar proje kullanıcı deposuna bağlanacak; iki kimlik türü aynı tabloda karıştırılmayacaktır.'),
     ],
     'recommend': {'field': 'panel_url_strategy', 'map': {'subdomain': ['shared_idp'], 'subdirectory': ['shared_session'], 'separate_domain': ['shared_idp'], 'hybrid': ['shared_idp']}}},

    {'id': 'panel_tenancy', 'label': 'Organizasyon ve Kiracı Modeli', 'en': 'Organization / Tenancy Model', 'type': 'select', 'agents': [SWE, DBA],
     'explanation': 'Kullanıcıların sisteme doğrudan mı, yoksa bir organizasyon (şirket, bayi, tedarikçi, çalışma alanı) üzerinden mi bağlandığını belirler. Kullanıcı, organizasyon, üyelik ve rol ayrı varlıklar olarak modellenir.',
     'scenario': 'Kurumsal sitede tek kurum; B2B platformda bir kullanıcının birden çok müşteri şirketine üye olabildiği çok organizasyonlu yapı; SaaS ürününde çalışma alanı başına yalıtılmış veri.',
     'example': 'Çok organizasyonlu yapıda Ayşe Hanım A Ltd.’de “Satın alma yöneticisi”, B A.Ş.’de “Görüntüleyici” rolündedir; portalda organizasyon değiştirince yetkileri de değişir.',
     'rule': 'Organizasyon ve kiracı modeli {label} olacaktır. Kullanıcı, organizasyon, üyelik (kullanıcı + organizasyon + rol), rol ve izin ayrı tablolarda modellenecek; her sorgu etkin organizasyon bağlamıyla filtrelenecektir.',
     'options': [
         o('single_org', 'Tek kurum', 'Bütün kullanıcılar tek kuruma aittir; roller doğrudan kullanıcıya verilir. Organizasyon tablosu yine tutulur ama tek kayıttır.', 'Kurumsal site, kurum içi panel veya tek işletmeli e-ticaret.', 'Editör ve yönetici rolleri doğrudan kullanıcılara atanır.', None),
         o('multi_org', 'Çok organizasyonlu (kullanıcı birden çok organizasyona üye)', 'Müşteri, tedarikçi veya bayi şirketleri organizasyon olarak tutulur; kullanıcı birden çok organizasyona farklı rollerle üye olabilir, panelde etkin organizasyonu seçer.', 'B2B platform, pazar yeri, bayi ve tedarikçi portalları.', 'Bir muhasebeci üç müşteri şirketinin portalına aynı hesapla girer.', 'Etkin organizasyon her istekte sunucuda doğrulanacak; kullanıcının o organizasyondaki üyeliği ve rolü yoksa istek reddedilecektir.'),
         o('multi_tenant', 'Çok kiracılı (çalışma alanı başına yalıtılmış veri)', 'Her müşteri bir kiracı / çalışma alanıdır; veri kiracı kimliğiyle yalıtılır, kiracılar birbirinin verisini hiçbir koşulda görmez. Kullanıcı birden çok çalışma alanına üye olabilir.', 'SaaS ürünleri.', 'app.alanadi.com/acme ve app.alanadi.com/globex ayrı çalışma alanlarıdır.', 'Her kayıt kiracı kimliği taşıyacak; kiracı kimliği istemciden değil oturumdaki üyelikten alınacak, kiracılar arası sorgu yalnız denetim kaydıyla platform yöneticisine açık olacaktır.'),
     ],
     'recommend': {'field': 'project_type', 'map': dict([(t, ['single_org']) for t in SITE_SMALL + ['E-commerce', 'Community', 'Booking', 'Classifieds', 'Intranet', 'Government', 'LMS']] + [
         ('SaaS', ['multi_tenant']), ('Web App', ['multi_tenant']), ('Portal', ['multi_org']), ('Marketplace', ['multi_org']), ('B2B Platform', ['multi_org'])])}},

    {'id': 'panel_data_isolation', 'label': 'Veri İzolasyon Yöntemi', 'en': 'Data Isolation Method', 'type': 'select', 'agents': [DBA, SEC],
     'showIf': [{'field': 'panel_tenancy', 'in': ['multi_org', 'multi_tenant']}],
     'explanation': 'Organizasyonların veya kiracıların verisinin veritabanında nasıl ayrılacağını belirler. Yalıtım güçlendikçe maliyet ve işletim yükü artar.',
     'scenario': 'Çoğu B2B ve SaaS ürünü ortak şema + organizasyon kimliği + satır düzeyi güvenlikle başlar; sözleşmesi ayrı veritabanı isteyen büyük müşteriler için hibrit modele geçilir.',
     'example': 'Ortak şemada siparişler tablosunun her satırında organization_id vardır ve PostgreSQL satır düzeyi güvenlik politikası başka organizasyonun satırını döndürmez.',
     'rule': 'Organizasyon / kiracı verisi {label} yöntemiyle yalıtılacaktır.',
     'options': [
         o('row_level', 'Ortak şema + organizasyon kimliği + satır düzeyi güvenlik', 'Bütün kiracılar aynı tabloları kullanır; her satır organization_id / tenant_id taşır. Uygulama filtresine ek olarak veritabanı satır düzeyi güvenliği (RLS) önerilir.', 'Başlangıç ve orta ölçek; en düşük maliyet.', 'orders(id, organization_id, …) + RLS politikası.', 'Organizasyon kimliği taşıyan her tabloda bileşik indeks ve mümkünse satır düzeyi güvenlik politikası kullanılacak; organizasyon filtresi olmayan sorgu kod incelemesinde reddedilecektir.'),
         o('schema_per_tenant', 'Kiracı başına şema', 'Her kiracının aynı veritabanında ayrı şeması vardır. Yalıtım güçlenir; migration her şemaya uygulanmalıdır.', 'Kiracı sayısı yüzlerle sınırlıysa ve daha güçlü ayrım isteniyorsa.', 'tenant_acme.orders, tenant_globex.orders.', 'Migration’lar bütün kiracı şemalarına aynı sürümle uygulanacak; şema seçimi istemciden gelen değere göre yapılmayacaktır.'),
         o('db_per_tenant', 'Kiracı başına veritabanı', 'Her kiracı ayrı veritabanındadır. En güçlü yalıtım ve kiracı bazlı yedek / bölge seçimi; işletim maliyeti en yüksektir.', 'Düzenlemeye tabi sektörler veya sözleşmeyle ayrı veri isteyen kurumsal müşteriler.', 'Her kurumsal müşteri için ayrı veritabanı ve ayrı yedek takvimi.', 'Kiracı → veritabanı eşlemesi sunucu tarafında tutulacak; bağlantı bilgileri gizli anahtar yöneticisinde saklanacaktır.'),
         o('hybrid', 'Hibrit (varsayılan ortak şema, büyük kiracıya ayrı veritabanı)', 'Kiracıların çoğu ortak şemada, ayrı yalıtım isteyenler kendi veritabanında tutulur.', 'Büyüyen SaaS ürünlerinde.', 'Standart planlar ortak şemada, kurumsal plan ayrı veritabanında.', 'Kiracının yalıtım türü kiracı kaydında tutulacak; veri erişim katmanı her iki türü aynı arayüzle sunacaktır.'),
     ],
     'recommend': {'field': 'panel_tenancy', 'map': {'multi_org': ['row_level'], 'multi_tenant': ['row_level']}}},

    {'id': 'panel_authz', 'label': 'Panel Yetkilendirme Modeli', 'en': 'Panel Authorization Model', 'type': 'select', 'agents': [SWE, SEC],
     'explanation': 'Panellerdeki erişim kararlarının hangi modelle verileceğini belirler. Temel model rol bazlı yetkidir (RBAC); gerekirse nitelik bazlı (ABAC) kurallarla genişletilir. Kararlar her zaman sunucuda uygulanır.',
     'scenario': 'Küçük bir içerik panelinde genel roller; B2B portalında organizasyon bağlamında roller; tutar sınırı, bölge veya kayıt sahibi koşulu gereken operasyonlarda RBAC + ABAC.',
     'example': 'RBAC + ABAC’ta “Satın alma uzmanı” teklif onaylayabilir; ancak 250.000 TL üstü teklif için “Satın alma müdürü” rolü ve aynı organizasyon koşulu aranır.',
     'rule': 'Panel yetkilendirmesi {label} ile yapılacaktır. Yetki kararları varsayılan olarak reddeder, her istekte sunucuda kullanıcı + etkin organizasyon + rol + izin ile verilir; menü veya düğme gizlemek yetkilendirme yerine geçmez.',
     'options': [
         o('rbac_global', 'RBAC – genel roller', 'Roller doğrudan kullanıcıya verilir ve bütün sistemde geçerlidir.', 'Tek kurumlu projeler, içerik panelleri.', 'Editör bütün içerikleri düzenler, yönetici ayarları da değiştirir.', None),
         o('rbac_org', 'RBAC – organizasyon bağlamında roller', 'Rol, kullanıcı ile organizasyon arasındaki üyeliğe bağlıdır; aynı kullanıcı farklı organizasyonlarda farklı rol taşır. Platform rolleri (süper yönetici) organizasyon rollerinden ayrı tutulur.', 'Çok organizasyonlu ve çok kiracılı projeler.', 'Kullanıcı A Ltd.’de yönetici, B A.Ş.’de görüntüleyicidir.', 'İzin denetimi her zaman (kullanıcı, etkin organizasyon, izin) üçlüsüyle yapılacak; platform rolleri organizasyon verisine yalnız denetim kaydıyla erişecektir.'),
         o('rbac_abac', 'RBAC + ABAC kuralları', 'Rol bazlı izinlerin üstüne kayıt sahibi, durum, tutar, bölge, saat gibi niteliklere bağlı kurallar eklenir. Kurallar merkezi bir politika katmanında tutulur.', 'Onay akışları, tutar sınırları veya kayıt sahibine göre erişim gereken projeler.', 'Satış temsilcisi yalnız kendi müşterilerini, bölge müdürü kendi bölgesindekileri görür.', 'ABAC kuralları dağınık if blokları yerine merkezi politika katmanında tanımlanacak ve birim testleriyle doğrulanacaktır.'),
     ],
     'recommend': {'field': 'panel_tenancy', 'map': {'single_org': ['rbac_global'], 'multi_org': ['rbac_org'], 'multi_tenant': ['rbac_org']}}},

    {'id': 'panel_session', 'label': 'Oturum ve Çerez Stratejisi', 'en': 'Session & Cookie Strategy', 'type': 'select', 'agents': [SEC, SWE],
     'explanation': 'Panel oturumunun tarayıcıda nasıl tutulacağını ve çerezin hangi kapsamda yazılacağını belirler. Adres yaklaşımıyla birlikte düşünülmelidir: alt alan adları aynı site sayılır, alt dizinler aynı köken paylaşır.',
     'scenario': 'Çoğu panel için sunucu tarafı oturum + host-only çerez en güvenli başlangıçtır; mobil uygulama ve üçüncü taraf istemciler için ayrıca API jetonu verilir.',
     'example': 'admin.alanadi.com, __Host-admin_session adlı, Secure, HttpOnly, SameSite=Lax, Path=/ çerezini yalnız kendi ana makinesine yazar.',
     'rule': 'Panel oturumları {label} ile yönetilecektir. Oturum çerezleri Secure ve HttpOnly olacak, oturum kimliği girişte ve yetki yükseltmede yenilenecek, oturum jetonları localStorage’da tutulmayacaktır.',
     'options': [
         o('host_only', 'Sunucu tarafı oturum + host-only çerez (__Host-)', 'Oturum sunucuda tutulur; tarayıcıya yalnız oturum kimliği, Domain özelliği olmadan (yalnız kendi ana makinesi) ve __Host- önekiyle yazılır.', 'Önerilen varsayılan; her adres yaklaşımında çalışır.', 'Set-Cookie: __Host-portal_sid=…; Secure; HttpOnly; SameSite=Lax; Path=/', 'Oturum çerezleri __Host- önekiyle, Domain özelliği olmadan yazılacaktır.'),
         o('parent_domain', 'Üst alan adında paylaşılan çerez', 'Çerez Domain=.alanadi.com ile bütün alt alan adlarına açılır; paneller arası tek oturum kolaylaşır ama bütün alt alan adları aynı güven düzeyine bağlanır.', 'Yalnız bütün alt alan adları aynı ekip tarafından yönetiliyor ve kullanıcı içeriği barındırmıyorsa.', 'Set-Cookie: sid=…; Domain=.alanadi.com; Secure; HttpOnly', 'Üst alan adına yazılan çerez yalnız kimlik sağlayıcı oturumu için kullanılacak; yönetim yetkisi taşıyan oturum her zaman host-only olacak, alt alan adlarının listesi güvenlik incelemesinden geçecektir.'),
         o('bff', 'BFF (Backend for Frontend) + HttpOnly çerez', 'Her panelin kendi sunucu katmanı vardır; tarayıcı yalnız HttpOnly oturum çerezi taşır, API jetonları sunucuda kalır.', 'Ayrı ön yüz uygulamaları ve harici kimlik sağlayıcı kullanan projelerde.', 'portal ön yüzü kendi BFF’ine istek atar, BFF api.alanadi.com’a jetonla gider.', 'Erişim ve yenileme jetonları tarayıcıya verilmeyecek, BFF katmanında tutulacaktır.'),
         o('bearer', 'API jetonu (Bearer) – yalnız uygulama dışı istemciler', 'Kısa ömürlü erişim jetonu + yenileme jetonu. Mobil uygulama ve üçüncü taraf entegrasyonlar içindir; tarayıcı panelleri için önerilmez.', 'Geliştirici / API portalı ve mobil istemciler.', 'Authorization: Bearer … başlığıyla API çağrısı.', 'Tarayıcı panelleri çerezli oturum kullanacak; Bearer jetonları yalnız mobil ve entegrasyon istemcilerine, kapsamı sınırlı ve kısa ömürlü olarak verilecektir.'),
     ],
     'recommend': {'field': 'panel_identity', 'map': {'shared_idp': ['host_only'], 'shared_session': ['host_only'], 'separate': ['host_only'], 'hybrid': ['host_only']}}},

    {'id': 'panel_api_access', 'label': 'Panel API Erişim Modeli', 'en': 'Panel API Access Model', 'type': 'select', 'agents': [API, SEC],
     'explanation': 'Panellerin iş verisine hangi API yoluyla eriştiğini belirler. Aynı kökendeki API çerezle sorunsuz çalışır; farklı kökendeki API için CORS izin listesi ve CSRF koruması gerekir.',
     'scenario': 'Tek uygulamada aynı köken; ayrı ön yüz uygulamalarında BFF veya merkezi API.',
     'example': 'Merkezi API’de api.alanadi.com yalnız portal.alanadi.com ve admin.alanadi.com kökenlerine Access-Control-Allow-Credentials ile yanıt verir.',
     'rule': 'Paneller iş verisine {label} ile erişecektir. API yanıtları panelin rolüne göre değil, istekteki kullanıcının izinlerine göre süzülecektir.',
     'options': [
         o('same_origin', 'Aynı köken API (panel kendi /api yolunu kullanır)', 'Her panel kendi kökenindeki /api yoluna istek atar; CORS gerekmez.', 'Tek uygulama ve alt dizin yapısı.', 'alanadi.com/admin → alanadi.com/api/admin/…', 'CORS açılmayacak; durum değiştiren isteklerde CSRF jetonu doğrulanacaktır.'),
         o('bff', 'Panel başına BFF', 'Her panel ön yüzünün yanında kendi sunucu katmanı vardır; BFF iç API’ye sunucudan gider.', 'Ayrı ön yüz uygulamaları.', 'portal.alanadi.com/api (BFF) → iç servis.', 'İç API’ler internete açılmayacak, yalnız BFF katmanından erişilecektir.'),
         o('central_api', 'Merkezi API (api.alanadi.com) + CORS izin listesi', 'Bütün paneller tek API’yi çağırır; API yalnız envanterdeki panel kökenlerine izin verir.', 'Birden çok ön yüz ve mobil istemci aynı API’yi kullanıyorsa.', 'Access-Control-Allow-Origin: https://portal.alanadi.com', 'CORS izin listesi envanterdeki panel kökenlerinden üretilecek; joker karakter (*) kimlik bilgili isteklerde kullanılmayacaktır.'),
         o('gateway', 'API ağ geçidi + jeton', 'İstekler API ağ geçidinden geçer; kimlik doğrulama, hız sınırı ve yönlendirme ağ geçidinde yapılır.', 'Panel başına bağımsız uygulamalar ve microservices.', 'gateway.alanadi.com → orders-service, billing-service.', 'Ağ geçidi kimliği doğrular; yetki kararı yine servislerde kullanıcı + organizasyon bağlamıyla verilir.'),
     ],
     'recommend': {'field': 'panel_app_topology', 'map': {'single_app': ['same_origin'], 'separate_frontends': ['central_api'], 'per_panel': ['gateway'], 'hybrid': ['central_api']}}},

    {'id': 'panel_admin_hardening', 'label': 'Yönetim Panellerinde Zorunlu Önlemler', 'en': 'Admin Panel Hardening', 'type': 'multiselect', 'agents': [SEC, OPS],
     'explanation': 'Yönetim, operasyon, finans ve denetim gibi yetkili panellerin hepsinde zorunlu olacak güvenlik önlemleridir. Panel bazlı ek önlemler envanterdeki Güvenlik sekmesinde seçilir.',
     'scenario': 'Her projede en az çok adımlı doğrulama, denetim kaydı, hız sınırı ve noindex önerilir; kurum içi paneller için ağ düzeyinde erişim kontrolü eklenir.',
     'example': 'admin.alanadi.com Cloudflare Access arkasındadır, girişte passkey ister, kritik işlemde parolayı yeniden sorar ve her değişikliği denetim kaydına yazar.',
     'rule': 'Yönetim panellerinde zorunlu önlemler: {labels}.',
     'options': [
         o('mfa', 'Çok adımlı doğrulama zorunlu', 'Yetkili panellere girişte ikinci adım (passkey, TOTP) zorunludur.', 'Her yönetim panelinde.', 'Girişten sonra authenticator kodu istenir.'),
         o('step_up', 'Kritik işlemde yeniden doğrulama', 'Rol değiştirme, ödeme iadesi, toplu silme, dışa aktarma gibi işlemlerde kimlik yeniden doğrulanır.', 'Finans ve kullanıcı yönetimi olan panellerde.', 'İade onayından önce passkey yeniden istenir.'),
         o('zero_trust', 'Ağ düzeyinde erişim kontrolü (Zero Trust / VPN)', 'Panel adresi yalnız kurumsal kimlikle doğrulanmış cihazlara veya VPN’e açılır.', 'Kurum içi yönetim ve operasyon panellerinde.', 'Cloudflare Access veya kurumsal VPN arkasında.'),
         o('ip_allowlist', 'IP izin listesi', 'Panel yalnız belirli IP aralıklarından erişilebilir.', 'Sabit ofis IP’si olan ekiplerde.', 'Yalnız ofis ve VPN çıkış IP’leri.'),
         o('audit', 'Denetim kaydı', 'Kim, ne zaman, hangi kaydı, hangi organizasyonda değiştirdi bilgisi değiştirilemez biçimde tutulur.', 'Her yönetim panelinde.', 'Rol değişikliği: kim, eski rol, yeni rol, zaman, IP.'),
         o('rate_limit', 'Giriş ve API hız sınırı', 'Başarısız giriş ve API çağrıları kullanıcı ve IP bazında sınırlandırılır.', 'Her panelde.', '5 başarısız denemeden sonra artan bekleme süresi.'),
         o('short_session', 'Kısa oturum ve boşta kalma zaman aşımı', 'Yetkili oturumlar kısa sürer, boşta kalınca kapanır.', 'Finans, kullanıcı yönetimi ve denetim panellerinde.', '15 dakika boşta kalınca oturum kapanır.'),
         o('noindex', 'Arama motorlarından gizleme (noindex)', 'Panel sayfaları X-Robots-Tag: noindex ile işaretlenir, site haritasına girmez. robots.txt tek başına koruma değildir.', 'Her panelde.', 'X-Robots-Tag: noindex, nofollow'),
         o('csp', 'Katı içerik güvenliği politikası (CSP)', 'Panel sayfalarında yalnız izinli kaynaklardan betik çalışır; satır içi betik nonce ile.', 'Her yönetim panelinde; alt dizin yapısında özellikle.', "Content-Security-Policy: script-src 'self' 'nonce-…'; frame-ancestors 'none'"),
     ]},
]

for f in FIELDS:
    if f['type'] == 'multiselect':
        for x in f['options']:
            x.setdefault('ruleDetail', None)
            if x['ruleDetail'] is None:
                del x['ruleDetail']

CATS = [
    {'id': 'admin', 'name': 'Platform yönetimi'},
    {'id': 'customer', 'name': 'Müşteri ve üye'},
    {'id': 'business', 'name': 'İş ortakları ve tedarik'},
    {'id': 'internal', 'name': 'Kurum içi'},
    {'id': 'specialist', 'name': 'Uzman ve operasyon araçları'},
    {'id': 'custom', 'name': 'Özel paneller'},
]

MODULES = [
    ('dashboard', 'Gösterge paneli', 'Panelin açılış ekranı: özet sayılar, görevler, uyarılar.', 0),
    ('profile', 'Profil', 'Kullanıcının kendi bilgileri, parola / passkey, oturumlar.', 0),
    ('org', 'Organizasyon yönetimi', 'Organizasyon bilgileri, şubeler, fatura bilgileri.', 1),
    ('users', 'Kullanıcı yönetimi', 'Kullanıcı davet etme, devre dışı bırakma, üyelik ve rol atama.', 1),
    ('roles', 'Rol ve izin yönetimi', 'Rollerin ve rollere bağlı izinlerin tanımlanması.', 1),
    ('tenants', 'Kiracılar / çalışma alanları', 'Kiracı veya çalışma alanı kayıtları, planları, durumu.', 1),
    ('content', 'İçerik ve sayfalar', 'Sayfa, yazı, menü ve bileşen içeriklerinin yönetimi.', 0),
    ('media', 'Medya kütüphanesi', 'Görsel, video ve belge dosyalarının yönetimi.', 0),
    ('forms', 'Form başvuruları', 'İletişim, teklif ve başvuru formlarından gelen kayıtlar.', 1),
    ('seo', 'SEO ayarları', 'Başlık, açıklama, yönlendirme ve site haritası ayarları.', 0),
    ('products', 'Ürün yönetimi', 'Ürün, hizmet, fiyat ve katalog kayıtları.', 0),
    ('inventory', 'Stok', 'Depo, stok seviyesi ve hareketleri.', 0),
    ('orders', 'Siparişler', 'Sipariş kayıtları, durumları ve sevkiyat.', 1),
    ('requests', 'Talepler', 'Teklif isteği, iade, izin, değişiklik gibi talep kayıtları.', 1),
    ('offers', 'Teklifler', 'Hazırlanan ve alınan teklifler, onay akışı.', 1),
    ('invoices', 'Faturalar', 'Fatura, e-fatura ve fatura belgeleri.', 1),
    ('payments', 'Ödemeler', 'Tahsilat, iade, hakediş ve ödeme hareketleri.', 1),
    ('subscriptions', 'Abonelik ve planlar', 'Plan, abonelik, kullanım ve yenileme kayıtları.', 1),
    ('documents', 'Belgeler', 'Sözleşme, katalog, teknik doküman ve paylaşılan dosyalar.', 1),
    ('customers', 'Müşteri kayıtları', 'Müşteri kartları, iletişim geçmişi.', 1),
    ('leads', 'Potansiyel müşteriler', 'Lead kayıtları, nitelendirme ve atama.', 1),
    ('campaigns', 'Kampanyalar', 'Kampanya, kupon ve indirim kurgusu.', 0),
    ('courses', 'Kurslar ve dersler', 'Kurs, ders, ödev ve öğrenci ilerlemesi.', 0),
    ('notifications', 'Bildirimler', 'E-posta, SMS ve panel içi bildirim tercihleri ve geçmişi.', 0),
    ('messages', 'Mesajlar', 'Kullanıcılar ve ekipler arası yazışmalar.', 1),
    ('tickets', 'Destek talepleri', 'Destek kayıtları, SLA ve çözüm süreci.', 1),
    ('knowledge', 'Bilgi bankası', 'Yardım makaleleri ve sık sorulan sorular.', 0),
    ('reports', 'Raporlar', 'Hazır raporlar ve dışa aktarma.', 1),
    ('analytics', 'Analitik', 'Kullanım, dönüşüm ve performans göstergeleri.', 0),
    ('api_keys', 'API anahtarları', 'API anahtarı oluşturma, kapsam ve iptal.', 1),
    ('webhooks', "Webhook'lar", 'Olay bildirimleri, imza anahtarları ve teslim kayıtları.', 1),
    ('integrations', 'Entegrasyonlar', 'Üçüncü taraf servis bağlantıları ve ayarları.', 1),
    ('compliance', 'Uyum ve politika kayıtları', 'Politika onayları, KVKK talepleri, kontrol kanıtları.', 1),
    ('settings', 'Ayarlar', 'Panel ve organizasyon ayarları.', 1),
    ('audit', 'Denetim kayıtları', 'Kim, ne zaman, neyi değiştirdi kayıtları (salt okunur).', 1),
]
MIDS = [m[0] for m in MODULES]


def R(id, name, scope, m=(), w=(), r=(), all=None):
    return {'id': id, 'name': name, 'scope': scope, 'm': list(m), 'w': list(w), 'r': list(r), 'all': all}


T = []


def tpl(id, name, en, cat, mode, slug, audience, desc, modules, roles, mfa='optional', scope='org', risk='standard', idp='shared'):
    T.append({'id': id, 'name': name, 'en': en, 'cat': cat, 'mode': mode, 'slug': slug, 'audience': audience, 'desc': desc,
              'modules': modules, 'roles': roles, 'mfa': mfa, 'scope': scope, 'risk': risk, 'idp': idp})


tpl('super_admin', 'Süper Yönetici Paneli', 'Super Admin', 'admin', 'subdomain', 'admin', 'Platform sahibi ve sistem yöneticileri',
    'Bütün organizasyonları, kullanıcıları, planları ve sistem ayarlarını yöneten en yetkili panel.',
    ['dashboard', 'tenants', 'org', 'users', 'roles', 'subscriptions', 'integrations', 'settings', 'reports', 'audit', 'notifications'],
    [R('super_admin', 'Süper yönetici', 'platform', all='m'),
     R('sys_admin', 'Sistem yöneticisi', 'platform', m=['org', 'users', 'integrations', 'settings', 'notifications'], w=['tenants', 'subscriptions'], r=['dashboard', 'roles', 'reports', 'audit']),
     R('support_agent', 'Destek görevlisi', 'platform', w=['users'], r=['dashboard', 'tenants', 'org', 'subscriptions']),
     R('audit_viewer', 'Denetim görüntüleyici', 'platform', r=['dashboard', 'reports', 'audit'])],
    mfa='required', scope='platform', risk='high', idp='internal')
tpl('cms_admin', 'İçerik Yönetim Paneli (CMS)', 'CMS Admin', 'admin', 'subdirectory', 'admin', 'Editörler, içerik yazarları ve site yöneticisi',
    'Sayfa, yazı, medya, menü ve SEO ayarlarının yönetildiği panel.',
    ['dashboard', 'content', 'media', 'forms', 'seo', 'users', 'settings', 'audit'],
    [R('site_admin', 'Site yöneticisi', 'org', all='m'),
     R('editor', 'Editör', 'org', m=['content', 'media'], w=['seo', 'forms'], r=['dashboard']),
     R('author', 'Yazar', 'own', w=['content', 'media'], r=['dashboard']),
     R('viewer', 'Görüntüleyici', 'org', r=['dashboard', 'content', 'media'])],
    mfa='required', scope='org', risk='high', idp='internal')
tpl('backoffice', 'Operasyon Paneli (Backoffice)', 'Backoffice / Operations', 'admin', 'subdomain', 'backoffice', 'Operasyon, sipariş ve müşteri hizmetleri ekipleri',
    'Sipariş, talep, müşteri, belge ve günlük operasyon işlerinin yürütüldüğü kurum içi panel.',
    ['dashboard', 'orders', 'requests', 'customers', 'products', 'inventory', 'documents', 'tickets', 'reports', 'notifications', 'audit'],
    [R('ops_manager', 'Operasyon müdürü', 'platform', all='m'),
     R('ops_specialist', 'Operasyon uzmanı', 'platform', w=['orders', 'requests', 'customers', 'documents', 'tickets', 'inventory'], r=['dashboard', 'products', 'reports', 'notifications']),
     R('ops_viewer', 'Görüntüleyici', 'platform', r=['dashboard', 'orders', 'requests', 'customers', 'reports'])],
    mfa='required', scope='platform', risk='high', idp='internal')
tpl('customer_portal', 'Müşteri Portalı', 'Customer Portal', 'customer', 'subdomain', 'portal', 'Müşteri şirketlerin kullanıcıları',
    'Müşterinin siparişlerini, taleplerini, tekliflerini, faturalarını ve belgelerini takip ettiği portal.',
    ['dashboard', 'profile', 'org', 'users', 'orders', 'requests', 'offers', 'invoices', 'payments', 'documents', 'messages', 'tickets', 'notifications'],
    [R('customer_admin', 'Müşteri hesap yöneticisi', 'org', m=['org', 'users', 'requests', 'offers'], w=['messages', 'tickets', 'payments'], r=['dashboard', 'profile', 'orders', 'invoices', 'documents', 'notifications']),
     R('customer_user', 'Müşteri kullanıcısı', 'org', w=['requests', 'messages', 'tickets', 'profile'], r=['dashboard', 'orders', 'offers', 'documents', 'notifications']),
     R('customer_finance', 'Müşteri finans kullanıcısı', 'org', w=['payments'], r=['dashboard', 'invoices', 'orders', 'documents'])])
tpl('supplier_portal', 'Tedarikçi Portalı', 'Supplier Portal', 'business', 'subdomain', 'supplier', 'Tedarikçi şirketlerin kullanıcıları',
    'Tedarikçinin teklif isteklerini yanıtladığı, siparişleri, faturaları ve belgeleri yönettiği portal.',
    ['dashboard', 'profile', 'org', 'users', 'products', 'requests', 'offers', 'orders', 'invoices', 'payments', 'documents', 'messages', 'notifications'],
    [R('supplier_admin', 'Tedarikçi yöneticisi', 'org', m=['org', 'users', 'products', 'offers'], w=['documents', 'messages', 'invoices'], r=['dashboard', 'requests', 'orders', 'payments', 'notifications']),
     R('supplier_sales', 'Satış temsilcisi', 'org', w=['offers', 'messages', 'products'], r=['dashboard', 'requests', 'orders', 'documents']),
     R('supplier_finance', 'Finans kullanıcısı', 'org', w=['invoices'], r=['dashboard', 'orders', 'payments', 'documents'])])
tpl('seller_portal', 'Satıcı / Mağaza Paneli', 'Seller / Merchant Portal', 'business', 'subdomain', 'seller', 'Pazar yerindeki satıcılar ve mağaza ekipleri',
    'Satıcının ürünlerini, stoklarını, siparişlerini, kampanyalarını ve hakedişlerini yönettiği panel.',
    ['dashboard', 'org', 'users', 'products', 'inventory', 'orders', 'campaigns', 'payments', 'invoices', 'messages', 'tickets', 'reports'],
    [R('store_owner', 'Mağaza sahibi', 'org', all='m'),
     R('catalog_manager', 'Katalog yöneticisi', 'org', m=['products', 'inventory'], w=['campaigns'], r=['dashboard', 'orders', 'reports']),
     R('order_operator', 'Sipariş operatörü', 'org', w=['orders', 'messages', 'tickets'], r=['dashboard', 'products', 'inventory']),
     R('store_finance', 'Mağaza finans', 'org', r=['dashboard', 'payments', 'invoices', 'reports'])])
tpl('partner_portal', 'İş Ortağı Portalı', 'Partner Portal', 'business', 'subdomain', 'partner', 'Çözüm ve satış ortakları',
    'İş ortaklarının müşteri yönlendirdiği, teklif ve satış materyallerine ulaştığı, komisyonlarını izlediği portal.',
    ['dashboard', 'org', 'users', 'leads', 'customers', 'offers', 'documents', 'payments', 'reports', 'messages'],
    [R('partner_admin', 'İş ortağı yöneticisi', 'org', m=['org', 'users', 'leads'], w=['offers', 'customers', 'messages'], r=['dashboard', 'documents', 'payments', 'reports']),
     R('partner_user', 'İş ortağı kullanıcısı', 'org', w=['leads', 'messages'], r=['dashboard', 'customers', 'documents', 'offers'])])
tpl('dealer_portal', 'Bayi Portalı', 'Dealer / Reseller Portal', 'business', 'subdomain', 'dealer', 'Bayi ve yeniden satıcı ekipleri',
    'Bayinin fiyat listelerine, stoklara, sipariş, teklif, fatura ve kampanya bilgilerine ulaştığı portal.',
    ['dashboard', 'org', 'users', 'products', 'orders', 'offers', 'invoices', 'payments', 'campaigns', 'documents', 'tickets', 'reports'],
    [R('dealer_admin', 'Bayi yöneticisi', 'org', m=['org', 'users', 'orders', 'offers'], w=['tickets', 'payments'], r=['dashboard', 'products', 'invoices', 'campaigns', 'documents', 'reports']),
     R('dealer_sales', 'Bayi satış', 'org', w=['orders', 'offers', 'tickets'], r=['dashboard', 'products', 'campaigns', 'documents']),
     R('dealer_finance', 'Bayi finans', 'org', w=['payments'], r=['dashboard', 'invoices', 'orders', 'reports'])])
tpl('member_dashboard', 'Üye / Kullanıcı Paneli', 'Member / User Dashboard', 'customer', 'subdirectory', 'hesabim', 'Bireysel üyeler ve son kullanıcılar',
    'Üyenin profilini, siparişlerini, bildirimlerini, mesajlarını ve hesap güvenliğini yönettiği panel.',
    ['dashboard', 'profile', 'orders', 'documents', 'messages', 'notifications', 'settings'],
    [R('member', 'Üye', 'own', w=['profile', 'messages', 'notifications', 'settings'], r=['dashboard', 'orders', 'documents'])], scope='own')
tpl('org_admin', 'Organizasyon / Şirket Yöneticisi', 'Organization / Company Admin', 'customer', 'subdirectory', 'company', 'Müşteri veya kurum tarafındaki şirket yöneticileri',
    'Bir şirketin kendi kullanıcılarını, rollerini, fatura bilgilerini ve ayarlarını yönettiği panel.',
    ['dashboard', 'org', 'users', 'roles', 'subscriptions', 'invoices', 'settings', 'audit'],
    [R('org_owner', 'Şirket sahibi', 'org', all='m'),
     R('org_admin', 'Şirket yöneticisi', 'org', m=['users'], w=['org', 'settings'], r=['dashboard', 'roles', 'subscriptions', 'invoices', 'audit'])], mfa='required')
tpl('employee_portal', 'Çalışan Portalı', 'Employee / Staff Portal', 'internal', 'subdomain', 'staff', 'Şirket çalışanları',
    'Çalışanların duyurulara, belgelere, izin ve talep süreçlerine ulaştığı kurum içi portal.',
    ['dashboard', 'profile', 'documents', 'requests', 'messages', 'notifications', 'knowledge', 'reports'],
    [R('employee', 'Çalışan', 'own', w=['profile', 'requests', 'messages'], r=['dashboard', 'documents', 'knowledge', 'notifications']),
     R('team_manager', 'Ekip yöneticisi', 'org', m=['requests'], w=['messages'], r=['dashboard', 'documents', 'reports', 'knowledge']),
     R('hr_specialist', 'İK uzmanı', 'org', m=['documents', 'requests', 'knowledge'], w=['notifications'], r=['dashboard', 'reports'])], mfa='required', risk='high', idp='internal')
tpl('billing', 'Faturalama ve Finans Paneli', 'Billing / Finance', 'internal', 'subdomain', 'billing', 'Finans ve muhasebe ekipleri',
    'Fatura, tahsilat, iade, abonelik ve finans raporlarının yönetildiği panel.',
    ['dashboard', 'invoices', 'payments', 'subscriptions', 'customers', 'documents', 'reports', 'audit'],
    [R('finance_manager', 'Finans müdürü', 'platform', all='m'),
     R('accountant', 'Muhasebe uzmanı', 'platform', w=['invoices', 'payments', 'documents'], r=['dashboard', 'subscriptions', 'customers', 'reports']),
     R('finance_viewer', 'Finans görüntüleyici', 'platform', r=['dashboard', 'invoices', 'payments', 'reports'])], mfa='required', scope='platform', risk='high', idp='internal')
tpl('crm', 'CRM / Satış Paneli', 'CRM / Sales', 'internal', 'subdomain', 'crm', 'Satış ve müşteri ilişkileri ekipleri',
    'Potansiyel müşteri, müşteri, teklif ve satış fırsatlarının yönetildiği panel.',
    ['dashboard', 'leads', 'customers', 'offers', 'orders', 'campaigns', 'messages', 'documents', 'reports'],
    [R('sales_manager', 'Satış müdürü', 'platform', all='m'),
     R('sales_rep', 'Satış temsilcisi', 'own', w=['leads', 'customers', 'offers', 'messages', 'documents'], r=['dashboard', 'orders', 'campaigns']),
     R('sales_viewer', 'Görüntüleyici', 'platform', r=['dashboard', 'leads', 'customers', 'reports'])], mfa='required', scope='platform', idp='internal')
tpl('helpdesk', 'Destek Masası', 'Helpdesk / Support', 'specialist', 'subdomain', 'support', 'Müşteri destek ekipleri',
    'Destek taleplerinin karşılandığı, SLA’ların izlendiği ve bilgi bankasının yönetildiği panel.',
    ['dashboard', 'tickets', 'customers', 'messages', 'knowledge', 'reports', 'notifications'],
    [R('support_manager', 'Destek yöneticisi', 'platform', all='m'),
     R('support_agent', 'Destek uzmanı', 'platform', w=['tickets', 'messages'], r=['dashboard', 'customers', 'knowledge']),
     R('kb_editor', 'Bilgi bankası editörü', 'platform', m=['knowledge'], r=['dashboard', 'tickets'])], mfa='required', scope='platform', idp='internal')
tpl('marketing', 'Pazarlama Paneli', 'Marketing', 'specialist', 'subdomain', 'marketing', 'Pazarlama ve içerik ekipleri',
    'Kampanya, içerik, form, potansiyel müşteri ve pazarlama analitiğinin yönetildiği panel.',
    ['dashboard', 'campaigns', 'content', 'media', 'leads', 'forms', 'analytics', 'reports', 'integrations'],
    [R('marketing_manager', 'Pazarlama müdürü', 'platform', all='m'),
     R('marketing_specialist', 'Pazarlama uzmanı', 'platform', w=['campaigns', 'content', 'media', 'forms'], r=['dashboard', 'leads', 'analytics', 'reports']),
     R('content_editor', 'İçerik editörü', 'platform', w=['content', 'media'], r=['dashboard', 'campaigns'])], mfa='required', scope='platform', idp='internal')
tpl('analytics', 'Analitik ve Raporlama Paneli', 'Analytics / Reporting', 'specialist', 'subdomain', 'analytics', 'Analistler ve yöneticiler',
    'Kullanım, satış, operasyon ve finans göstergelerinin raporlandığı panel; veri değiştirmez.',
    ['dashboard', 'analytics', 'reports', 'audit'],
    [R('analyst', 'Analist', 'platform', w=['reports'], r=['dashboard', 'analytics', 'audit']),
     R('executive_viewer', 'Yönetici görüntüleyici', 'platform', r=['dashboard', 'analytics', 'reports'])], mfa='required', scope='platform', idp='internal')
tpl('lms_instructor', 'Eğitmen Paneli (LMS)', 'LMS / Instructor', 'specialist', 'subdomain', 'instructor', 'Eğitmenler ve eğitim koordinatörleri',
    'Eğitmenlerin kurs, ders, ödev ve öğrenci ilerlemesini yönettiği panel.',
    ['dashboard', 'courses', 'media', 'messages', 'documents', 'reports', 'payments'],
    [R('instructor', 'Eğitmen', 'own', m=['courses'], w=['media', 'messages', 'documents'], r=['dashboard', 'reports', 'payments']),
     R('teaching_assistant', 'Eğitmen asistanı', 'own', w=['messages'], r=['dashboard', 'courses', 'documents']),
     R('edu_coordinator', 'Eğitim koordinatörü', 'org', all='m')])
tpl('developer', 'Geliştirici / API Portalı', 'Developer / API', 'specialist', 'subdomain', 'developers', 'Entegrasyon yapan geliştiriciler',
    'API anahtarları, webhook’lar, kullanım bilgileri ve API dokümantasyonunun sunulduğu portal.',
    ['dashboard', 'api_keys', 'webhooks', 'documents', 'analytics', 'tickets', 'settings'],
    [R('dev_admin', 'Geliştirici hesap yöneticisi', 'org', all='m'),
     R('developer', 'Geliştirici', 'org', w=['webhooks', 'tickets'], r=['dashboard', 'api_keys', 'documents', 'analytics'])], mfa='required')
tpl('auditor', 'Denetçi / Uyum Paneli', 'Auditor / Compliance', 'internal', 'subdomain', 'compliance', 'İç denetim, uyum ve dış denetçiler',
    'Denetim kayıtları, politika onayları, uyum kanıtları ve raporların salt okunur incelendiği panel.',
    ['dashboard', 'audit', 'compliance', 'reports', 'documents'],
    [R('auditor', 'Denetçi', 'platform', r=['dashboard', 'audit', 'compliance', 'reports', 'documents']),
     R('compliance_officer', 'Uyum sorumlusu', 'platform', m=['compliance'], w=['documents'], r=['dashboard', 'audit', 'reports'])], mfa='required', scope='platform', risk='high', idp='internal')
tpl('tenant_admin', 'Kiracı / Çalışma Alanı Yöneticisi', 'Tenant / Workspace Admin', 'customer', 'subdomain', 'app', 'SaaS müşterisinin çalışma alanı yöneticileri ve üyeleri',
    'SaaS müşterisinin çalışma alanı, kullanıcıları, rolleri, planı, entegrasyonları ve API anahtarlarını yönettiği alan.',
    ['dashboard', 'users', 'roles', 'subscriptions', 'invoices', 'integrations', 'api_keys', 'settings', 'audit', 'notifications'],
    [R('workspace_owner', 'Çalışma alanı sahibi', 'org', all='m'),
     R('workspace_admin', 'Çalışma alanı yöneticisi', 'org', m=['users', 'integrations', 'settings'], w=['api_keys', 'notifications'], r=['dashboard', 'roles', 'subscriptions', 'invoices', 'audit']),
     R('workspace_member', 'Üye', 'org', w=['notifications'], r=['dashboard']),
     R('workspace_guest', 'Misafir', 'own', r=['dashboard'])], mfa='optional')
tpl('custom', 'Özel Panel', 'Custom Panel', 'custom', 'subdomain', 'panel', 'Kullanıcının tanımladığı kitle',
    'Şablonlarda karşılığı olmayan, kullanıcının adını, kitlesini, modüllerini ve rollerini kendisinin belirlediği panel.',
    ['dashboard', 'profile', 'settings'],
    [R('panel_admin', 'Panel yöneticisi', 'org', all='m'), R('panel_user', 'Panel kullanıcısı', 'org', r=['dashboard', 'profile'])])

for t in T:
    for m in t['modules']:
        assert m in MIDS, (t['id'], m)
    for r in t['roles']:
        for k in ('m', 'w', 'r'):
            for m in r[k]:
                assert m in t['modules'], (t['id'], r['id'], m)

SCEN = [
    {'id': 'corporate_cms', 'name': 'Kurumsal web sitesi + CMS', 'types': SITE_SMALL,
     'why': 'Tek bir yönetim paneli yeterli; aynı alan adında alt dizin kurulumu ve bakımı en kolay seçenektir.',
     'panels': [['cms_admin', 'subdirectory', 'admin']], 'fields': {'panel_url_strategy': 'subdirectory', 'panel_tenancy': 'single_org'}},
    {'id': 'b2b_marketplace', 'name': 'B2B pazar yeri', 'types': ['Marketplace', 'B2B Platform'],
     'why': 'Müşteri, tedarikçi ve platform yönetimi ayrı kitlelerdir; ayrı alt alan adları oturum ve güvenlik başlıklarını ayırır. Aynı uygulamadan ana makine adına göre sunulabilir.',
     'panels': [['customer_portal', 'subdomain', 'portal'], ['supplier_portal', 'subdomain', 'supplier'], ['super_admin', 'subdomain', 'admin'], ['backoffice', 'subdomain', 'backoffice']],
     'fields': {'panel_url_strategy': 'hybrid', 'panel_tenancy': 'multi_org'}},
    {'id': 'saas', 'name': 'Çok kiracılı SaaS', 'types': ['SaaS', 'Web App'],
     'why': 'Müşteri çalışma alanları app alt alan adında, platform yönetimi ayrı alt alan adında; çalışma alanı verisi kiracı kimliğiyle yalıtılır.',
     'panels': [['tenant_admin', 'subdomain', 'app'], ['super_admin', 'subdomain', 'admin'], ['billing', 'subdomain', 'billing']],
     'fields': {'panel_url_strategy': 'hybrid', 'panel_tenancy': 'multi_tenant'}},
    {'id': 'ecommerce', 'name': 'E-ticaret', 'types': ['E-commerce'],
     'why': 'Üye hesabı sitenin içinde alt dizinde kalır (sepet ve oturum aynı kökende), yönetim ve operasyon ayrı alt alan adında yalıtılır.',
     'panels': [['member_dashboard', 'subdirectory', 'hesabim'], ['cms_admin', 'subdomain', 'admin'], ['backoffice', 'subdomain', 'backoffice']],
     'fields': {'panel_url_strategy': 'hybrid', 'panel_tenancy': 'single_org'}},
    {'id': 'member_portal', 'name': 'Üyelik / müşteri portalı', 'types': ['Portal', 'Community', 'Classifieds'],
     'why': 'Üye paneli kullanıcıların ana alanıdır; yönetim paneli üye içeriklerinden ayrı kökende tutulur.',
     'panels': [['member_dashboard', 'subdirectory', 'hesabim'], ['cms_admin', 'subdomain', 'admin']],
     'fields': {'panel_url_strategy': 'hybrid'}},
    {'id': 'booking', 'name': 'Rezervasyon platformu', 'types': ['Booking'],
     'why': 'Müşteri rezervasyonlarını kendi hesabından, personel takvimini ayrı panelden yönetir.',
     'panels': [['member_dashboard', 'subdirectory', 'hesabim'], ['employee_portal', 'subdomain', 'staff'], ['cms_admin', 'subdomain', 'admin']],
     'fields': {'panel_url_strategy': 'hybrid'}},
    {'id': 'lms', 'name': 'Eğitim platformu (LMS)', 'types': ['LMS'],
     'why': 'Öğrenci paneli sitenin içinde, eğitmen paneli ve yönetim ayrı alt alan adlarında.',
     'panels': [['member_dashboard', 'subdirectory', 'hesabim'], ['lms_instructor', 'subdomain', 'instructor'], ['cms_admin', 'subdomain', 'admin']],
     'fields': {'panel_url_strategy': 'hybrid'}},
    {'id': 'intranet', 'name': 'Kurum içi portal', 'types': ['Intranet'],
     'why': 'Çalışan portalı kurumsal SSO ile açılır; yönetim paneli erişim kontrollü ağın arkasında tutulur.',
     'panels': [['employee_portal', 'subdomain', 'intranet'], ['super_admin', 'subdomain', 'admin']],
     'fields': {'panel_url_strategy': 'subdomain', 'panel_identity': 'hybrid'}},
    {'id': 'government', 'name': 'Kamu / belediye portalı', 'types': ['Government'],
     'why': 'Vatandaş işlemleri sitenin içinde, içerik ve başvuru operasyonları ayrı panellerde.',
     'panels': [['member_dashboard', 'subdirectory', 'e-hizmet'], ['cms_admin', 'subdomain', 'admin'], ['backoffice', 'subdomain', 'backoffice'], ['auditor', 'subdomain', 'compliance']],
     'fields': {'panel_url_strategy': 'hybrid'}},
]
EXTRA = [
    {'module': 'crm', 'panel': ['crm', 'subdomain', 'crm'], 'why': 'Ek Modüller’de CRM seçildi.'},
    {'module': 'support_ai', 'panel': ['helpdesk', 'subdomain', 'support'], 'why': 'Ek Modüller’de canlı destek seçildi.'},
    {'module': 'lms', 'panel': ['lms_instructor', 'subdomain', 'instructor'], 'why': 'Ek Modüller’de eğitim (LMS) seçildi.'},
    {'module': 'portal', 'panel': ['customer_portal', 'subdomain', 'portal'], 'why': 'Ek Modüller’de müşteri portalı seçildi.'},
    {'module': 'listings', 'panel': ['member_dashboard', 'subdirectory', 'hesabim'], 'why': 'İlan veren üyelerin ilanlarını yönetmesi için.'},
]

RESERVED_PATHS = ['api', 'auth', 'login', 'logout', 'signin', 'signup', 'register', 'oauth', 'callback', 'sso', '.well-known', 'static', 'assets', 'public', 'cdn',
                  '_next', '_nuxt', '_astro', 'build', 'dist', 'health', 'healthz', 'status', 'metrics', 'robots.txt', 'sitemap.xml', 'favicon.ico', 'manifest.json',
                  'sw.js', 'feed', 'rss', 'graphql', 'webhooks', 'uploads', 'media', 'wp-json', 'wp-content', 'wp-includes', 'cdn-cgi']
RESERVED_SUBS = ['www', 'mail', 'email', 'smtp', 'imap', 'pop', 'pop3', 'mx', 'ns1', 'ns2', 'ftp', 'sftp', 'cdn', 'static', 'assets', 'autodiscover', 'autoconfig',
                 'localhost', 'staging', 'dev', 'test', 'preview', 'api']

LEVELS = [['r', 'Görüntüle'], ['w', 'Düzenle'], ['m', 'Yönet']]

out = {
    'version': 1,
    'section': SECTION, 'guide': GUIDE, 'fields': FIELDS,
    'kit': {
        'categories': CATS,
        'modules': [{'id': a, 'name': b, 'desc': c, 'sensitive': bool(d)} for a, b, c, d in MODULES],
        'templates': T, 'scenarios': SCEN, 'extra': EXTRA,
        'reserved': {'paths': RESERVED_PATHS, 'subdomains': RESERVED_SUBS},
        'levels': LEVELS,
    },
}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'panel-portal.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('yazıldı:', p, len(T), 'şablon', len(MODULES), 'modül', len(FIELDS), 'karar', len(SCEN), 'senaryo')
