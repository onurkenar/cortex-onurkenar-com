# -*- coding: utf-8 -*-
"""İş Akışları ve Onay Mekanizmaları — 4 Göz Onay Akışı modülü (2026-11-10, kullanıcının
"Modül: 4 Göz Onay Akışı (Four-Eyes Approval Workflow)" yönergesi).
Çalıştırınca yanına onay-akisi.json yazar; uygulamaya onay_ekle.py işler.
python3 -I docs/onay-akisi/kaynak.py"""
import json, os

APP = 'poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/kidemli-yazilim-muhendisi'
SOD = 'poz:uyum-risk:06.03/gorevler-ayriligi-ve-yetki-kontrolleri/gorevler-ayriligi-uzmani'
ICK = 'poz:uyum-risk:06.03/kontrol-tasarimi-ve-test/kidemli-ic-kontrol-uzmani'
IAM = 'poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/kidemli-kimlik-ve-erisim-uzmani'
PROC = 'poz:operasyon:12.06/surec-tasarimi-ve-standardizasyon/surec-analisti'
ON = [{'field': 'approval_enabled', 'in': [True]}]


def o(v, l, ex, sc, eg, rd=None):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd:
        x['ruleDetail'] = rd
    return x


SECTION = {'id': 'approvals', 'after': 'panels', 'group': 'Teknik Mimari', 'icon': '⇄',
           'name': 'İş Akışları ve Onay Mekanizmaları', 'en': 'Workflows & Approval Mechanisms (Four-Eyes, Maker-Checker)',
           'desc': 'Kritik işlemlerin bir kişi hazırlayıp başka bir kişi onaylamadan tamamlanmamasını sağlayan 4 Göz Onay Akışı modülünü (maker-checker) yapılandırır: onaya tabi işlemler, roller ve görevler ayrılığı, onay seviyeleri, dinamik kurallar, bildirimler, yeniden onay, denetim kaydı ve yönetim raporları'}

GUIDE = {
    'purpose': '4 Göz Onay Akışı (four-eyes, maker-checker), para, yetki, fiyat, kişisel veri ya da yayın gibi kritik bir işlemin tek kişinin kararıyla gerçekleşmesini engeller: bir kişi işlemi hazırlar (Hazırlayan / Maker), farklı bir yetkili kişi inceleyip onaylar (Onaylayan / Checker). Böylece hata, suistimal ve yetkisiz değişiklik riski azalır, her adım denetlenebilir hâle gelir. Bu bölüm modülün projede kullanılıp kullanılmayacağını ve kullanılacaksa hangi işlemlerde, hangi rollerle, kaç onayla, hangi kurallarla çalışacağını karara bağlar. Modül isteğe bağlıdır; etkinleştirilmezse projeye kural, tablo ya da bağımlılık eklenmez.',
    'criteria': [
        'Para hareketi (ödeme, iade, fiyat, indirim), yetki değişikliği (rol atama, admin ekleme), kişisel veri işlemi (toplu dışa aktarma, silme) ya da kurum adına yayın varsa 4 göz onayı güçlü biçimde önerilir.',
        'Onaylayan, hazırlayandan bağımsız olmalıdır: aynı kişi kendi işlemini hiçbir yoldan (ikinci hesap, vekâlet, süper admin) onaylayamaz; bu kural arayüzde değil sunucuda zorunlu tutulur.',
        'Onay seviyesi riske göre seçilir: rutin işlemde 4 göz (bir onay), yüksek tutar ya da yüksek riskte 6 göz (iki bağımsız onay) ya da sıralı çok aşamalı onay.',
        'Onay kuralları (işlem türü, rol, departman, tutar, risk) koda gömülmez; yönetim panelinden değiştirilebilir, sürümlenir ve kuralın kendisi de onayla değişir.',
        'Onaydan sonra kritik alanlarda yapılan her değişiklik işlemi yeniden onaya düşürür; onaylanan sürüm değiştirilemez biçimde saklanır.',
        'Her adım kim, ne zaman, ne yaptı, neden ve hangi sürüm üzerinde sorularını yanıtlayan, değiştirilemez bir denetim kaydına yazılır.',
    ],
    'pitfalls': [
        'Kendi işlemini onaylama engelinin yalnız arayüzde (düğmeyi gizleyerek) yapılması: API\'ye doğrudan istek atan kullanıcı kendi işlemini onaylayabilir.',
        'Süper admin ya da "sistem" kullanıcısını onaydan muaf tutmak: görevler ayrılığı en yetkili hesapta delinir.',
        'Onaydan sonra kaydın sessizce düzenlenebilmesi: onaylanan tutar ya da içerik, onaylayanın görmediği bir değere dönüşür.',
        'Denetim kaydını uygulamanın düzenleyebildiği sıradan bir tabloda tutmak: kayıt silinebilir ya da değiştirilebilir, denetimde delil değeri kalmaz.',
        'Hatırlatma ve eskalasyon olmadan onay istemek: talepler kimsenin önünde birikir, iş durur ve kullanıcılar onayı atlatmanın yolunu arar.',
        'Her işlemi onaya bağlamak: düşük riskli işlemlerde gereksiz bekleme ve "körü körüne onay" alışkanlığı oluşur; kapsam riske göre seçilmelidir.',
    ],
    'resources': [
        {'title': 'NIST — Separation of Duty (görevler ayrılığı) tanımı', 'url': 'https://csrc.nist.gov/glossary/term/separation_of_duty', 'note': 'Kritik bir işlemin tek kişi tarafından baştan sona yürütülmemesi ilkesi.'},
        {'title': 'NIST — Two-person control (iki kişi denetimi) tanımı', 'url': 'https://csrc.nist.gov/glossary/term/two_person_control', 'note': '4 göz ilkesinin resmî karşılığı: işlem için en az iki yetkili kişinin birlikte bulunması.'},
        {'title': 'NIST SP 800-53 Rev. 5', 'url': 'https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final', 'note': 'AC-5 Görevler ayrılığı, AC-6 En az yetki, AU-9 Denetim kaydının korunması, AU-10 İnkâr edilemezlik kontrolleri.'},
        {'title': 'NIST — Role-Based Access Control (RBAC)', 'url': 'https://csrc.nist.gov/projects/role-based-access-control', 'note': 'Rol tabanlı yetkilendirme ve statik / dinamik görevler ayrılığı kısıtları.'},
        {'title': 'OWASP — Authorization Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html', 'note': 'Yetki denetiminin sunucuda, her istekte ve varsayılan reddet ilkesiyle yapılması.'},
        {'title': 'OWASP — Logging Cheat Sheet', 'url': 'https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html', 'note': 'Denetim kaydında hangi alanların tutulacağı, kayıtların kurcalamaya karşı korunması.'},
        {'title': 'NIST SP 800-92 — Log yönetimi rehberi', 'url': 'https://csrc.nist.gov/pubs/sp/800/92/final', 'note': 'Kayıtların toplanması, saklanması, korunması ve incelenmesi.'},
        {'title': 'OWASP ASVS', 'url': 'https://asvs.owasp.org/', 'note': 'İş mantığı, erişim denetimi ve kayıt gereksinimlerinin doğrulama standardı.'},
        {'title': 'OMG — BPMN 2.0.2', 'url': 'https://www.omg.org/spec/BPMN/2.0.2/About-BPMN', 'note': 'Çok aşamalı onay süreçlerini iş akışı motoruyla modellemek için standart gösterim.'},
    ],
}

F = [
    {'id': 'approval_enabled', 'type': 'boolean', 'label': '4 Göz Onay Akışı', 'en': 'Four-Eyes Approval Workflow (Maker-Checker)', 'agents': [ICK, APP],
     'explanation': 'Kritik işlemlerin bir kişi tarafından hazırlanıp başka bir yetkili kişi tarafından onaylanmadan tamamlanmamasını sağlayan isteğe bağlı modüldür. Etkinleştirilince bu bölümdeki ayarlar açılır; etkinleştirilmezse projeye hiçbir onay kuralı, tablosu ya da bağımlılığı eklenmez.',
     'scenario': 'Ödeme, iade, fiyat ya da indirim değişikliği, rol ve yetki ataması, toplu kişisel veri işlemi ya da kurum adına yayın gibi tek kişinin kararıyla yapılmaması gereken işlemler varsa.',
     'example': 'Muhasebe personeli 25.000 TL\'lik bir iadeyi hazırlar; iade, finans yöneticisi onaylayana kadar "Onay Bekliyor" durumunda kalır ve ödeme sağlayıcısına gönderilmez.',
     'rule': 'Dört göz onay akışı (maker-checker) modülü {booltext}.',
     'yes': {'scenario': 'Para, yetki, fiyat, kişisel veri ya da yayın gibi kritik işlemlerin ikinci bir kişi tarafından denetlenmesi gerekiyorsa; iç denetim, bağımsız denetim ya da mevzuat görevler ayrılığı istiyorsa.',
             'example': 'Yönetim panelinde "Onay Bekleyenler" ekranı açılır; kritik işlem kaydedildiğinde hazırlayana "Onaya gönderildi" bildirimi, onaylayana onay talebi gider.'},
     'no': {'scenario': 'Tek kişinin yönettiği küçük bir site, onaya tabi kritik işlemi olmayan tanıtım sitesi ya da onayın başka bir sistemde (ERP, ödeme sağlayıcısı paneli) yapıldığı projeler.',
            'example': 'Panelde onay ekranı ve onay tabloları yoktur; kritik işlemler yetkili rol tarafından doğrudan yapılır ve yalnız genel denetim kaydına yazılır.'}},

    {'id': 'approval_scope', 'type': 'multiselect', 'label': 'Onaya Tabi İşlemler', 'en': 'Approval Scope', 'agents': [ICK, PROC], 'showIf': ON,
     'explanation': 'Hangi işlem türlerinin tamamlanmadan önce ikinci bir kişinin onayını gerektireceğini belirler. Seçilen işlemler Taslak → Onay Bekliyor → Onaylandı / Revizyon İstendi / Reddedildi → Tamamlandı akışından geçer.',
     'scenario': 'Kapsam riske göre seçilir: para, yetki, kişisel veri ve kurum adına dışarıya giden içerik öncelikli adaylardır; düşük riskli rutin işlemleri onaya bağlamak gereksiz bekleme yaratır.',
     'example': 'Bir e-ticaret sitesinde fiyat ve indirim değişiklikleri, iadeler ve yeni yönetici ataması onaya tabidir; ürün açıklaması düzeltmesi değildir.',
     'rule': 'Onaya tabi işlem türleri: {labels}. Bu işlemler Taslak → Onay Bekliyor → Onaylandı / Revizyon İstendi / Reddedildi → Tamamlandı durum makinesinden geçer; durum geçişleri yalnız sunucuda, izin verilen geçiş tablosuna göre yapılır, "Onaylandı" olmayan işlem hiçbir yan etki (ödeme, yayın, yetki verme, dış sisteme gönderme) üretmez.',
     'recommend': [{'field': 'modules_extra', 'map': {'ecommerce': ['price', 'refund', 'order_cancel'], 'booking': ['refund', 'price'], 'crm': ['contract'], 'lms': ['content_publish'], 'portal': ['role_change'], 'listings': ['content_publish'], 'career': ['content_publish']}},
                   {'field': 'panel_authz', 'map': {'rbac_global': ['role_change', 'settings'], 'rbac_org': ['role_change', 'settings'], 'rbac_abac': ['role_change', 'settings']}}],
     'options': [
         o('content_publish', 'İçerik yayını', 'Sayfa, haber, duyuru, ilan ya da ders içeriğinin yayına alınması.', 'Kurum adına yayın yapan, yanlış içeriğin itibar ya da hukuki risk yarattığı siteler.', 'Editör duyuruyu hazırlar, kurumsal iletişim sorumlusu onaylayınca yayına girer.',
           'İçerik yayını onaylanmadan herkese açık hâle gelmez; taslak önizleme yalnız yetkililere açıktır.'),
         o('price', 'Fiyat, indirim ve kampanya değişikliği', 'Ürün / hizmet fiyatı, indirim oranı, kupon ve kampanya koşullarının değiştirilmesi.', 'E-ticaret, rezervasyon ve abonelik siteleri.', '%40 indirim kuponu, kategori yöneticisi onaylamadan kullanıma açılmaz.',
           'Fiyat, indirim ve kupon değişiklikleri onaylanana kadar müşteriye yansımaz; zamanlanmış kampanya da onaydan sonra çalışır.'),
         o('refund', 'Ödeme ve iade', 'İade, kısmi iade, manuel tahsilat, ödeme iptali ve tedarikçi ödemesi.', 'Para hareketi olan her proje.', 'Belirlenen tutarın üzerindeki iade, finans onayı olmadan ödeme sağlayıcısına gönderilmez.',
           'İade ve ödeme işlemleri onaydan sonra ödeme sağlayıcısına gönderilir; aynı işlem idempotency anahtarıyla bir kez çalışır.'),
         o('order_cancel', 'Sipariş iptali ve değişikliği', 'Onaylanmış siparişin iptali, tutar ya da ürün değişikliği.', 'Kurumsal (B2B) satış, yüksek tutarlı sipariş alan mağazalar.', 'Kargoya verilmemiş 120.000 TL\'lik kurumsal siparişin iptali satış müdürü onayıyla yapılır.',
           'Onaylanmış siparişin iptali ve tutar değişikliği onaya tabidir; stok ve fatura etkileri onaydan sonra uygulanır.'),
         o('role_change', 'Kullanıcı, rol ve yetki değişikliği', 'Yeni yönetici ekleme, rol atama / kaldırma, yetki genişletme.', 'Yönetim paneli ya da çok rollü portalı olan her proje.', 'Bir kullanıcıya "Finans Yöneticisi" rolü verilmesi, bilgi güvenliği sorumlusu onaylayınca etkinleşir.',
           'Rol ve yetki atamaları onaylanmadan etkinleşmez; kişi kendine rol veremez, yetki genişletme ayrıca kayda alınır.'),
         o('bulk_data', 'Toplu veri işlemi (dışa aktarma, silme, içe aktarma)', 'Kişisel veri içeren toplu dışa aktarma, toplu silme ve toplu içe aktarma.', 'Üye, müşteri ya da hasta verisi tutan projeler.', '5.000 üyelik listenin dışa aktarılması veri sorumlusu onayından sonra indirilebilir.',
           'Toplu dışa aktarma, silme ve içe aktarma onaydan sonra çalışır; dışa aktarım dosyası süreli ve kişiye özel bağlantıyla verilir.'),
         o('settings', 'Sistem ayarı ve entegrasyon', 'Ödeme, e-posta, API anahtarı, güvenlik ve entegrasyon ayarlarının değiştirilmesi.', 'Ayarları panelden yönetilen projeler.', 'Ödeme sağlayıcısı API anahtarının değiştirilmesi ikinci bir yöneticinin onayıyla yapılır.',
           'Ödeme, e-posta, güvenlik ve entegrasyon ayarlarındaki değişiklikler onaydan sonra uygulanır; gizli değerler onay ekranında maskelenir.'),
         o('contract', 'Sözleşme, teklif ve belge', 'Teklif, sözleşme, fatura düzeltmesi ve resmî belge.', 'CRM, teklif ya da belge yönetimi olan projeler.', 'Satış temsilcisinin hazırladığı %25 iskontolu teklif, satış müdürü onaylayınca müşteriye gönderilir.',
           'Teklif, sözleşme ve belge onaylanmadan müşteriye gönderilmez; gönderilen sürüm onaylanan sürümle aynıdır.'),
         o('personal_data', 'Kişisel veri talebi (KVKK / GDPR)', 'İlgili kişi başvurusu yanıtı, veri düzeltme, silme ve anonimleştirme.', 'KVKK / GDPR kapsamında başvuru alan projeler.', 'Silme talebinin yanıtı veri koruma sorumlusu onayından sonra gönderilir.',
           'Kişisel veri talepleri ve yanıtları onaydan sonra uygulanır; yasal yanıt süresi SLA olarak izlenir.'),
     ]},

    {'id': 'approval_levels', 'type': 'select', 'label': 'Onay Seviyesi (4 Göz / 6 Göz / Çok Aşamalı)', 'en': 'Approval Levels', 'agents': [ICK, APP], 'showIf': ON,
     'explanation': 'Bir işlemin tamamlanması için kaç bağımsız onay gerektiğini belirler. 4 göz bir hazırlayan + bir onaylayan, 6 göz bir hazırlayan + iki bağımsız onaylayan demektir; çok aşamalı onayda işlem sırayla farklı makamlardan geçer.',
     'scenario': 'Rutin kritik işlemlerde 4 göz yeterlidir; yüksek tutar, yetki ya da itibar riski olan işlemlerde 6 göz ya da çok aşamalı onay, karışık riskli projelerde kurala göre seviye seçilir.',
     'example': 'Kurala göre seçimde 10.000 TL altı iade tek onayla, üzeri finans müdürü + CFO olmak üzere iki onayla tamamlanır.',
     'rule': 'Onay seviyesi: {label}. Hazırlayan (maker) kendi işlemini hiçbir seviyede onaylayamaz; aynı kişi aynı işlemde birden çok onay veremez; bu kurallar arayüzde değil sunucuda, her istekte denetlenir.',
     'recommend': {'field': 'company_size', 'map': {'solo': ['four'], 'micro': ['four'], 'small': ['four'], 'medium': ['four'], 'large': ['dynamic'], 'group': ['dynamic']}},
     'options': [
         o('four', '4 Göz — bir onaylayan (önerilen)', 'Bir kişi hazırlar, farklı bir yetkili kişi onaylar.', 'Çoğu kritik işlem; küçük ve orta ölçekli ekipler.', 'Editör hazırlar, yayın sorumlusu onaylar.',
           'Her onaya tabi işlem için hazırlayandan farklı en az bir onaylayan gerekir.'),
         o('six', '6 Göz — iki bağımsız onaylayan', 'Bir kişi hazırlar, iki farklı yetkili kişi onaylar; iki onaylayan da hazırlayandan ve birbirinden farklıdır.', 'Yüksek tutarlı ödeme, admin yetkisi verme, toplu kişisel veri dışa aktarma.', 'Yeni süper admin ataması bilgi güvenliği yöneticisi ve BT direktörünün ikisi de onaylayınca etkinleşir.',
           'İşlem için hazırlayandan ve birbirinden farklı iki onay gerekir; iki onay aynı kişiden ya da aynı hesabın vekilinden gelemez.'),
         o('multi', 'Çok aşamalı onay', 'İşlem tanımlı aşamalardan sırayla geçer (ör. ekip yöneticisi → ilgili birim → üst yönetim); her aşamanın onaylayan rolü ayrıdır.', 'Bütçe, sözleşme, satın alma ve kurumsal yayın gibi birden çok birimi ilgilendiren işlemler.', 'Satın alma talebi önce birim müdürü, sonra satın alma, sonra finans tarafından onaylanır.',
           'Onay aşamaları ve her aşamanın onaylayan rolü tanımlanır; bir aşamada reddedilen ya da revizyon istenen işlem sonraki aşamaya geçmez.'),
         o('dynamic', 'Kurala göre (risk ve tutara göre değişen)', 'Gereken onay sayısı ve onaylayan rolü, dinamik onay kurallarına göre işlem başına belirlenir.', 'Farklı risk düzeyinde çok sayıda işlem türü olan orta ve büyük ölçekli projeler.', '5.000 TL altı iade 4 göz, 5.000–50.000 TL 6 göz, üzeri çok aşamalı onaydan geçer.',
           'Gereken onay sayısı ve onaylayan rolleri her işlemde kural tablosundan belirlenir; eşleşen kural yoksa en sıkı varsayılan kural uygulanır.'),
     ]},

    {'id': 'approval_stage_mode', 'type': 'select', 'label': 'Birden Çok Onayın Sırası', 'en': 'Multi-Approval Order', 'agents': [PROC], 'showIf': ON + [{'field': 'approval_levels', 'in': ['six', 'multi', 'dynamic']}],
     'explanation': 'Birden çok onay gerektiğinde onayların sırayla mı, aynı anda mı toplanacağını belirler.',
     'scenario': 'Sonraki onaylayanın öncekinin kararını görmesi gerekiyorsa sıralı, hız önemliyse ve onaylayanlar eşit düzeydeyse paralel seçilir.',
     'example': 'Paralel onayda iki yönetici talebi aynı anda alır; ikisi de onaylayınca işlem tamamlanır, biri reddederse işlem reddedilir.',
     'rule': 'Birden çok onay gerektiğinde onay sırası: {label}.',
     'options': [
         o('sequential', 'Sıralı', 'Onaylar tanımlı sırayla toplanır; bir aşama onaylamadan sonraki aşamaya talep gitmez.', 'Hiyerarşik onay, bütçe ve sözleşme.', 'Birim müdürü onaylayınca talep finans müdürüne düşer.',
           'Onaylar tanımlı sırayla toplanır; önceki aşama tamamlanmadan sonraki onaylayana talep gönderilmez.'),
         o('parallel', 'Paralel', 'Talep bütün onaylayanlara aynı anda gider; gereken onay sayısı tamamlanınca işlem onaylanır, tek red işlemi reddeder.', 'Eşit düzeyli iki bağımsız onaylayan (6 göz).', 'İki güvenlik yöneticisi talebi aynı anda görür.',
           'Talep bütün onaylayanlara aynı anda gönderilir; gereken onay sayısı tamamlanınca işlem onaylanır, bir red ya da revizyon talebi işlemi durdurur.'),
         o('mixed', 'Karma (aşama içinde paralel, aşamalar arası sıralı)', 'Aşamalar sırayla ilerler; bir aşama içinde birden çok onaylayan paralel çalışır.', 'Büyük kurumlarda çok birimli onay süreçleri.', 'Önce hukuk ve finans aynı anda, ikisi de onaylayınca genel müdür onaylar.',
           'Aşamalar sırayla ilerler, aşama içindeki onaylar paralel toplanır; aşama, tanımlı onay sayısı tamamlanınca kapanır.'),
     ]},

    {'id': 'approval_roles', 'type': 'multiselect', 'label': 'Roller ve Görevler Ayrılığı (SoD)', 'en': 'Roles & Segregation of Duties', 'agents': [SOD, IAM], 'showIf': ON,
     'explanation': 'Hazırlayan (Maker) ve Onaylayan (Checker) rollerinin nasıl tanımlanacağını ve görevler ayrılığının (Segregation of Duties) hangi ek kurallarla korunacağını belirler. Kullanıcının kendi işlemini onaylayamaması her durumda zorunludur.',
     'scenario': 'Bütün projelerde temel kural zorunludur; vekâlet, aynı birim kısıtı ve süper admin kuralı ekip büyüklüğüne ve denetim gereksinimine göre seçilir.',
     'example': 'Finans uzmanı iade hazırlayabilir ama onaylayamaz; finans yöneticisi onaylayabilir ama kendi hazırladığı iadeyi onaylayamaz; izindeyken yerine tanımlanan vekil 7 gün süreyle onay verebilir.',
     'rule': 'Hazırlayan (Maker) ve Onaylayan (Checker) RBAC\'de ayrı izinlerle tanımlanır ("hazırla" ve "onayla" izinleri ayrıdır); kullanıcı kendi oluşturduğu ya da son değiştirdiği işlemi onaylayamaz; ek görevler ayrılığı kuralları: {labels}.',
     'options': [
         o('no_admin_bypass', 'Süper admin de onaydan muaf değil', 'En yetkili hesap da kendi işlemini onaylayamaz; onay akışını atlatan gizli yol yoktur.', 'Bütün projeler; özellikle küçük ekiplerde yöneticinin her şeyi yapabildiği durumlar.', 'Sistem yöneticisi kendine yönetici rolü verirse işlem başka bir yöneticinin onayını bekler.',
           'Süper admin ve sistem hesapları dahil hiçbir hesap onay akışını atlayamaz; acil durum yolu ("break-glass") varsa ayrı kayda alınır ve sonradan onaylanır.'),
         o('same_unit', 'Onaylayan farklı birimden ya da üst makamdan', 'Onaylayanın hazırlayanla aynı ekipten olmaması ya da hiyerarşide üstte olması istenir.', 'Suistimal riskinin ekip içi iş birliğiyle artabileceği finans ve satın alma işlemleri.', 'Satış temsilcisinin teklifini başka bir satış temsilcisi değil, satış müdürü onaylar.',
           'Onaylayan, hazırlayanın bağlı olduğu birim yöneticisi ya da farklı bir birimden yetkili olur; aynı düzeydeki ekip arkadaşı onaylayamaz.'),
         o('delegation', 'Süreli vekâlet (delegasyon)', 'Onaylayan izindeyken yetkisini süreli olarak başka bir yetkiliye devredebilir; vekil, devredenin hazırladığı işlemi onaylayamaz.', 'Onaylayanların izne çıktığı, işlerin beklememesi gereken ekipler.', 'Finans müdürü 1–7 Ağustos arası onay yetkisini yardımcısına devreder; devir kaydı denetimde görünür.',
           'Onay yetkisi başlangıç ve bitiş tarihli olarak devredilebilir; vekâlet kendine, hazırlayana ya da zincirleme devredilemez, her vekâletli onay "vekâleten" olarak kaydedilir.'),
         o('conflict_matrix', 'Çakışan rol matrisi', 'Aynı kişide birlikte bulunmaması gereken rol çiftleri tanımlanır (ör. "ödeme hazırla" + "ödeme onayla", "tedarikçi ekle" + "tedarikçiye ödeme yap").', 'İç denetim ya da bağımsız denetime tabi kurumlar.', 'Bir kullanıcıya hem tedarikçi tanımlama hem ödeme onaylama rolü verilmek istenince sistem engeller.',
           'Çakışan rol çiftleri matris olarak tanımlanır; aynı kullanıcıya çakışan roller atanamaz, mevcut çakışmalar raporlanır.'),
         o('reapprove_roles', 'Rol atamaları da onaya tabi', 'Hazırlayan ve onaylayan rollerinin kendisinin verilmesi de 4 göz onayından geçer; kimse kendine onay yetkisi veremez.', 'Rol yönetiminin panelden yapıldığı projeler.', 'Yeni "Onaylayan" rolü ataması bilgi güvenliği sorumlusunun onayından sonra etkinleşir.',
           'Hazırlayan / onaylayan rollerinin atanması ve kaldırılması da onaya tabidir; kullanıcı kendi rolünü değiştiremez.'),
         o('periodic_review', 'Dönemsel yetki gözden geçirmesi', 'Onay yetkisi olan kullanıcı listesi belirli aralıklarla (ör. üç ayda bir) yöneticilere gözden geçirtilir.', 'Personel değişiminin sık olduğu ve denetime tabi kurumlar.', 'Üç ayda bir, ayrılan personelin onay yetkisinin kapatılıp kapatılmadığı listeyle doğrulanır.',
           'Onay yetkisi olan kullanıcılar dönemsel olarak gözden geçirilir; kullanılmayan ya da ayrılan personelin yetkisi kapatılır ve gözden geçirme kayda alınır.'),
     ]},

    {'id': 'approval_rules', 'type': 'multiselect', 'label': 'Dinamik Onay Kuralları', 'en': 'Dynamic Approval Rules', 'agents': [ICK, APP], 'showIf': ON,
     'explanation': 'Bir işlemin kimin onayına, kaç onaya ve hangi aşamalara gideceğini belirleyen kuralların hangi ölçütlere göre yapılandırılabileceğini seçer. Kurallar yönetim panelinden düzenlenir, koda gömülmez.',
     'scenario': 'İşlem türleri ve riskleri çeşitliyse; aynı işlemin tutara ya da riske göre farklı onay gerektirdiği durumlarda.',
     'example': 'Kural: "İade + tutar > 10.000 TL → Finans Müdürü + CFO (6 göz)"; "Fiyat değişikliği + indirim > %30 → Kategori Müdürü + Ticari Direktör".',
     'rule': 'Onay kuralları şu ölçütlerle yapılandırılabilir: {labels}. Kurallar yönetim panelinden düzenlenen bir kural tablosunda tutulur (koşul → gereken onay sayısı, onaylayan rolleri, aşamalar, süre); kural değişikliği de 4 göz onayıyla yapılır ve sürümlenir, her işlem hangi kural sürümüyle değerlendirildiğini saklar; eşleşen kural yoksa en sıkı varsayılan kural uygulanır.',
     'options': [
         o('type', 'İşlem türü', 'Kural işlem türüne göre seçilir (iade, fiyat, rol, yayın …).', 'Bütün kural tabloları.', '"Rol değişikliği" her zaman 6 göz.', 'Kural koşullarında işlem türü kullanılır.'),
         o('role', 'Hazırlayanın rolü', 'Hazırlayanın rolüne göre farklı onay istenir.', 'Kıdemli ve kıdemsiz personelin aynı işlemi yapabildiği ekipler.', 'Stajyerin hazırladığı içerik iki onay, editörünki bir onay gerektirir.', 'Kural koşullarında hazırlayanın rolü kullanılır.'),
         o('department', 'Departman / birim', 'İşlemin ait olduğu departmana göre onaylayan belirlenir.', 'Çok birimli kurumlar.', 'Pazarlama bütçesi pazarlama direktörüne, BT bütçesi BT direktörüne gider.', 'Kural koşullarında departman / birim kullanılır; onaylayan birimin yöneticisinden çözülür.'),
         o('amount', 'Tutar eşiği', 'İşlemin tutarına göre onay sayısı ve onaylayan değişir.', 'Ödeme, iade, satın alma, indirim.', '0–5.000 TL tek onay, 5.000–50.000 TL iki onay, üzeri çok aşamalı.', 'Kural koşullarında tutar eşikleri kullanılır; tutar para birimiyle birlikte değerlendirilir, eşik kuralları kur farkını hesaba katar.'),
         o('risk', 'Risk seviyesi', 'İşleme atanan ya da hesaplanan risk seviyesine (düşük / orta / yüksek / kritik) göre onay belirlenir.', 'Risk puanı hesaplanan işlemler (ör. yeni tedarikçiye ilk ödeme).', 'Kritik risk seviyesindeki işlem her zaman 6 göz ve bilgi güvenliği onayı ister.', 'Kural koşullarında risk seviyesi kullanılır; risk seviyesi sunucuda hesaplanır, hazırlayan tarafından değiştirilemez.'),
         o('time', 'Zaman ve bağlam', 'Mesai dışı, tatil günü ya da olağan dışı konumdan yapılan işlemler için ek onay istenir.', 'Suistimal ya da hesap ele geçirme riskinin yüksek olduğu finansal işlemler.', 'Gece 02:00\'de hazırlanan büyük ödeme ek onay gerektirir.', 'Kural koşullarında zaman ve bağlam (mesai dışı, olağan dışı konum / cihaz) kullanılır.'),
     ]},

    {'id': 'approval_extra_states', 'type': 'multiselect', 'label': 'Ek Durumlar', 'en': 'Additional States', 'agents': [PROC], 'showIf': ON,
     'explanation': 'Temel akışa (Taslak → Onay Bekliyor → Onaylandı / Revizyon İstendi / Reddedildi → Tamamlandı) eklenecek isteğe bağlı durumları seçer.',
     'scenario': 'Talebin geri çekilmesi, süre aşımı ya da iptal gibi durumların ayrı izlenmesi gerekiyorsa.',
     'example': 'Hazırlayan, onaylanmadan önce fark ettiği hatalı talebi "Geri çekildi" durumuna alır ve düzeltip yeniden gönderir.',
     'rule': 'Temel durumlara ek olarak şu durumlar kullanılır: {labels}.',
     'options': [
         o('withdrawn', 'Geri çekildi', 'Hazırlayan, karar verilmeden önce talebini geri çekebilir.', 'Hazırlayanın hatayı onaydan önce fark edebildiği işlemler.', 'Yanlış tutarlı iade talebi geri çekilip düzeltilir.', 'Hazırlayan karar verilmemiş talebini geri çekebilir; geri çekilen talep Taslak\'a döner ve kayıtta görünür.'),
         o('expired', 'Süresi doldu', 'Belirlenen sürede karara bağlanmayan talep otomatik olarak süresi dolmuş sayılır.', 'Zamana duyarlı işlemler (kampanya, rezervasyon).', '48 saatte onaylanmayan kampanya talebi düşer.', 'Belirlenen sürede karar verilmeyen talep "Süresi doldu" durumuna alınır ve hazırlayana bildirilir; süresi dolan talep yan etki üretmez.'),
         o('cancelled', 'İptal edildi', 'Onaylanmış ama henüz tamamlanmamış işlemin yetkili tarafından iptali.', 'Onay ile uygulama arasında zaman olan işlemler.', 'Onaylanan ama ertesi gün çalışacak toplu e-posta gönderimi iptal edilir.', 'Onaylanmış ama tamamlanmamış işlem yetkili tarafından gerekçeyle iptal edilebilir.'),
         o('on_hold', 'Bilgi bekleniyor (askıda)', 'Onaylayan, karar vermeden önce hazırlayandan ek bilgi ister; süre sayacı durur.', 'Belge ya da açıklama gerektiren işlemler.', 'Finans, iade için fatura kopyası ister; talep belge gelene kadar askıda kalır.', 'Onaylayan ek bilgi isteyebilir; talep "Bilgi bekleniyor" durumunda kalır ve SLA süresi durur.'),
         o('failed', 'Uygulama hatası', 'Onaylanan işlemin uygulanması (ödeme, yayın, entegrasyon) başarısız olursa ayrı durumda izlenir.', 'Dış sisteme giden işlemler.', 'Onaylanan iade ödeme sağlayıcısında hata verirse "Uygulama hatası" olarak işaretlenir.', 'Onaylanan işlemin uygulanması başarısız olursa "Uygulama hatası" durumuna alınır; yeniden deneme yeni onay gerektirmez ama kayda alınır.'),
     ]},

    {'id': 'approval_notify', 'type': 'multiselect', 'label': 'Onay Bildirimleri', 'en': 'Approval Notifications', 'agents': [APP, PROC], 'showIf': ON,
     'explanation': 'Onay sürecinin hangi olaylarında kime bildirim gideceğini belirler.',
     'scenario': 'Onaylayanların talepleri kaçırmaması ve hazırlayanın sonucu zamanında öğrenmesi için en az talep ve sonuç bildirimleri önerilir.',
     'example': 'Onay talebi onaylayana gider; 24 saat içinde karar verilmezse hatırlatma, 48 saatte üst yöneticiye eskalasyon gönderilir.',
     'rule': 'Onay bildirimleri: {labels}. Bildirimler kişisel veri ve gizli değer içermez, ayrıntı için panele bağlantı verir.',
     'options': [
         o('request', 'Yeni onay talebi (onaylayana)', 'Talep onaya gönderildiğinde onaylayana bildirim.', 'Bütün projeler.', '"3 yeni onay talebiniz var" bildirimi.', 'Onaya gönderilen her talep onaylayana bildirilir.'),
         o('reminder', 'Hatırlatma', 'Belirli süre karar verilmeyen talep için onaylayana hatırlatma.', 'Onaylayanların yoğun olduğu ekipler.', '24 saattir bekleyen talep için hatırlatma.', 'Karar verilmeyen talepler için belirlenen aralıkla hatırlatma gönderilir.'),
         o('escalation', 'Gecikme ve eskalasyon', 'Süre (SLA) aşılınca üst yöneticiye ya da yedek onaylayana bildirim.', 'Bekleyen işin para ya da müşteri kaybına yol açtığı durumlar.', '48 saatte karar verilmeyen iade finans direktörüne eskale edilir.', 'Onay süresi aşılan talepler üst yöneticiye ya da yedek onaylayana eskale edilir ve gecikme panelde işaretlenir.'),
         o('result', 'Sonuç (hazırlayana)', 'Onay, red ya da revizyon talebi sonucu hazırlayana bildirilir; red ve revizyonda gerekçe zorunludur.', 'Bütün projeler.', '"İade talebiniz revizyon için geri gönderildi: fatura numarası eksik."', 'Onay, red ve revizyon sonucu hazırlayana bildirilir; red ve revizyonda onaylayanın gerekçesi zorunludur.'),
         o('completed', 'Tamamlandı ve uygulama hatası', 'İşlem tamamlandığında ya da uygulamada hata olduğunda ilgililere bildirim.', 'Dış sisteme giden işlemler.', 'İade ödeme sağlayıcısına iletildiğinde hazırlayan ve onaylayan bilgilendirilir.', 'İşlem tamamlandığında ve uygulama hatasında hazırlayana ve onaylayana bildirim gider.'),
         o('digest', 'Günlük özet', 'Onaylayanlara bekleyen talepleri özetleyen günlük e-posta.', 'Çok sayıda düşük öncelikli talep alan onaylayanlar.', 'Her sabah 09:00\'da "Onayınızı bekleyen 12 talep" özeti.', 'Onaylayanlara bekleyen talepleri listeleyen günlük özet gönderilir.'),
     ]},

    {'id': 'approval_channels', 'type': 'multiselect', 'label': 'Bildirim Kanalları', 'en': 'Notification Channels', 'agents': [APP], 'showIf': ON,
     'explanation': 'Onay bildirimlerinin hangi kanallardan gönderileceğini belirler.',
     'scenario': 'Panel içi bildirim neredeyse her zaman, e-posta çoğu projede seçilir; anlık mesajlaşma ekip bu araçları kullanıyorsa eklenir.',
     'example': 'Onay talebi panelde zil simgesinde ve e-postada görünür; kritik talepler ayrıca ekibin Slack kanalına düşer.',
     'rule': 'Onay bildirim kanalları: {labels}.',
     'options': [
         o('in_app', 'Panel içi bildirim', 'Yönetim panelinde bildirim merkezi ve sayaç.', 'Bütün projeler.', 'Zil simgesinde "Onay bekleyen: 4".', 'Panel içinde okunmamış sayaçlı bildirim merkezi bulunur.'),
         o('email', 'E-posta', 'İşlemsel e-posta ile bildirim; e-postadan doğrudan onay verilmez, panele bağlantı verilir.', 'Bütün projeler.', '"Onayınızı bekleyen talep" e-postası, panele giden bağlantıyla.', 'Bildirim e-postası panele bağlantı içerir; onay e-postadaki bir bağlantıyla verilemez, panelde oturum ve gerekirse yeniden doğrulama ister.'),
         o('push', 'Mobil / tarayıcı anlık bildirimi', 'Mobil uygulama ya da tarayıcı bildirimi.', 'Onaylayanların sahada ya da mobilde çalıştığı ekipler.', 'Onaylayanın telefonuna anlık bildirim gelir.', 'Anlık bildirimde yalnız talep türü ve panele bağlantı gösterilir.'),
         o('chat', 'Slack / Microsoft Teams', 'Ekip mesajlaşma kanalına webhook ile bildirim.', 'Bu araçları kullanan ekipler.', '#onaylar kanalına "Yeni iade talebi" mesajı.', 'Slack / Teams bildirimleri webhook ile gönderilir; mesaj kişisel veri ve tutar ayrıntısı içermez, onay panelde verilir.'),
         o('sms', 'SMS (yalnız kritik)', 'Kritik ve süreye duyarlı talepler için SMS.', 'Gecikmesi ciddi kayıp yaratan işlemler.', 'Kritik risk seviyesindeki ödeme talebi için onaylayana SMS.', 'SMS yalnız kritik ve süreye duyarlı taleplerde gönderilir.'),
     ]},

    {'id': 'approval_sla', 'type': 'select', 'label': 'Onay Süresi (SLA)', 'en': 'Approval SLA', 'agents': [PROC], 'showIf': ON,
     'explanation': 'Bir onay talebinin en geç ne kadar sürede karara bağlanması gerektiğini belirler; hatırlatma, eskalasyon ve gecikme raporları bu süreye göre çalışır.',
     'scenario': 'Müşteriyi bekleten işlemlerde (iade, sipariş) kısa, iç süreçlerde (yayın, ayar) daha uzun süre seçilir.',
     'example': '1 iş günü seçilince 8 iş saati içinde karar verilmeyen talep geç kalmış sayılır ve eskale edilir.',
     'rule': 'Onay süresi (SLA): {label}; süre iş saatleri ve tatil takvimine göre hesaplanır, "Bilgi bekleniyor" durumunda durur.',
     'options': [
         o('4h', '4 iş saati', 'Talep en geç 4 iş saatinde karara bağlanır.', 'Müşteriyi bekleten iade ve sipariş işlemleri.', 'Sabah gelen iade talebi öğleden sonra sonuçlanır.'),
         o('1d', '1 iş günü (önerilen)', 'Talep en geç bir iş gününde karara bağlanır.', 'Çoğu iç onay süreci.', 'Bugün gönderilen fiyat değişikliği yarın aynı saate kadar onaylanır.'),
         o('3d', '3 iş günü', 'Talep en geç üç iş gününde karara bağlanır.', 'Sözleşme, bütçe gibi inceleme gerektiren işlemler.', 'Sözleşme taslağı hukuk incelemesiyle üç gün içinde sonuçlanır.'),
         o('rule', 'Kurala göre', 'Süre, dinamik onay kuralında işlem türü ve riske göre tanımlanır.', 'Farklı aciliyette çok sayıda işlem türü.', 'Kritik ödeme 2 saat, içerik yayını 2 gün.',
           'Süre her onay kuralında ayrı tanımlanır; kuralda süre yoksa 1 iş günü uygulanır.'),
     ]},

    {'id': 'approval_versioning', 'type': 'multiselect', 'label': 'Sürüm Kontrolü ve Yeniden Onay', 'en': 'Versioning & Re-Approval', 'agents': [APP, ICK], 'showIf': ON,
     'explanation': 'Onaylanan kaydın sonradan değiştirilmesine karşı korumayı belirler. Onay sonrası kritik alanlardaki değişikliğin yeniden onay istemesi her durumda zorunludur.',
     'scenario': 'Onaylanan tutarın, içeriğin ya da yetkinin onaylayanın görmediği bir değere dönüşmemesi için bütün projelerde.',
     'example': 'Onaylanan kampanyanın indirim oranı %20\'den %35\'e çıkarılınca kampanya yeniden "Onay Bekliyor" durumuna düşer ve yayından kalkar.',
     'rule': 'Onaydan sonra kritik alanlarda yapılan her değişiklik kaydı yeniden "Onay Bekliyor" durumuna alır ve yeni onay ister (kritik alanlar işlem türü başına tanımlanır); ek olarak: {labels}.',
     'options': [
         o('snapshot', 'Onaylanan sürümün kopyası ve özeti', 'Onay anındaki kaydın tam kopyası ve içerik özeti (hash) saklanır; uygulanan veri onaylanan sürümle karşılaştırılır.', 'Para ve sözleşme işlemleri.', 'Ödeme gönderilmeden önce tutarın onaylanan sürümle aynı olduğu doğrulanır.',
           'Onay anındaki kaydın değiştirilemez kopyası ve içerik özeti saklanır; işlem uygulanırken veri bu özetle karşılaştırılır, farklıysa uygulanmaz.'),
         o('diff', 'Onaylayana değişiklik farkı', 'Onaylayan, önceki onaylı sürüm ile yeni sürüm arasındaki farkı alan alan görür.', 'Güncellenen kayıtların yeniden onaylandığı işlemler.', 'Fiyat 1.200 TL → 990 TL, indirim %10 → %25 olarak vurgulanır.',
           'Onay ekranında önceki onaylı sürüm ile yeni sürüm arasındaki fark alan alan gösterilir.'),
         o('lock', 'Onay beklerken kilit', 'Onay bekleyen kayıt hazırlayan dahil kimse tarafından değiştirilemez; değişiklik için talep geri çekilir.', 'Onay sürecinde içeriğin değişmemesi gereken işlemler.', 'Onay bekleyen teklifte düzenle düğmesi kapalıdır; "Geri çek ve düzenle" seçeneği vardır.',
           'Onay bekleyen kayıt düzenlemeye kilitlenir; değişiklik için talep geri çekilir ve yeni sürüm yeniden onaya gönderilir.'),
         o('noncritical_info', 'Kritik olmayan değişiklikte bilgilendirme', 'Kritik olmayan alanlardaki değişiklik yeniden onay istemez ama onaylayana bildirilir ve kayda alınır.', 'Açıklama, etiket gibi ikincil alanları olan kayıtlar.', 'Onaylı ürünün açıklamasındaki yazım düzeltmesi onay istemez, onaylayana bilgi gider.',
           'Kritik olmayan alan değişiklikleri yeniden onay istemez; onaylayana bildirilir ve sürüm geçmişine yazılır.'),
         o('optimistic', 'Eşzamanlı değişiklik koruması', 'Onaylayan kararı verirken kayıt değişmişse onay reddedilir (sürüm numarası / ETag denetimi).', 'Birden çok kişinin aynı kayıtla çalıştığı ekipler.', 'Onaylayan eski sürümü onaylamaya çalışırsa "Kayıt değişti, yeniden inceleyin" uyarısı alır.',
           'Onay isteği kaydın sürüm numarasını taşır; kayıt bu arada değiştiyse onay reddedilir ve onaylayan güncel sürümü yeniden inceler.'),
     ]},

    {'id': 'approval_audit', 'type': 'multiselect', 'label': 'Denetim Kaydı (Audit Log)', 'en': 'Audit Log', 'agents': [ICK, IAM], 'showIf': ON,
     'explanation': 'Onay sürecindeki her adımın nasıl kayda alınacağını ve kaydın nasıl korunacağını belirler. Kullanıcı, tarih-saat, işlem, açıklama ve sürüm bilgisi her durumda kaydedilir.',
     'scenario': 'Bütün onay akışlarında; iç denetim, bağımsız denetim ya da mevzuat incelemesi olan kurumlarda ek korumalar seçilir.',
     'example': 'Denetçi, bir iadenin kim tarafından hazırlandığını, kimin hangi gerekçeyle hangi sürümü onayladığını ve ödemenin ne zaman gönderildiğini tek ekranda görür.',
     'rule': 'Onay sürecinin her adımı (oluşturma, gönderme, onay, red, revizyon, geri çekme, yeniden onay, uygulama) kullanıcı, tarih-saat (UTC ve saat dilimiyle), işlem, açıklama / gerekçe, kayıt kimliği ve sürüm bilgisiyle değiştirilemez denetim kaydına yazılır; uygulama bu kayıtları güncelleyemez ve silemez; ek olarak: {labels}.',
     'options': [
         o('append_only', 'Yalnız ekleme (append-only) veritabanı izni', 'Denetim tablosuna uygulama kullanıcısının yalnız ekleme izni vardır; güncelleme ve silme izni veritabanı düzeyinde kapalıdır.', 'Bütün projeler.', 'Uygulamada bir hata olsa bile denetim kaydı değiştirilemez.',
           'Denetim tablosunda uygulamanın veritabanı kullanıcısına yalnız INSERT ve SELECT izni verilir; UPDATE / DELETE izni yoktur.'),
         o('hash_chain', 'Kayıt zinciri ile kurcalama tespiti', 'Her kayıt bir öncekinin özetini (hash) taşır; aradan kayıt silinmesi ya da değiştirilmesi tespit edilir.', 'Denetim kaydının delil değeri taşıması gereken kurumlar.', 'Gece çalışan doğrulama işi zincirdeki kopukluğu yakalayıp uyarı verir.',
           'Her denetim kaydı bir önceki kaydın özetini içerir (hash zinciri); zincir düzenli olarak doğrulanır, kopukluk uyarı üretir.'),
         o('context', 'IP, cihaz ve oturum bilgisi', 'Kayda isteğin IP adresi, tarayıcı / cihaz bilgisi ve oturum kimliği eklenir.', 'Hesap ele geçirme riskinin önemli olduğu finansal işlemler.', 'Onayın şirket ağından mı yurt dışından mı verildiği görülür.',
           'Denetim kaydına IP adresi, cihaz / tarayıcı bilgisi ve oturum kimliği eklenir; bu bilgiler kişisel veri olarak saklama politikasına tabidir.'),
         o('separate_store', 'Ayrı ve değiştirilemez depolama', 'Kayıtlar ayrıca uygulama veritabanı dışındaki değiştirilemez bir depoya (WORM nesne depolama, log servisi) kopyalanır.', 'Bağımsız denetime ve mevzuata tabi kurumlar.', 'Kayıtlar her gece nesne kilitli (object lock) depolamaya aktarılır.',
           'Denetim kayıtları uygulama veritabanının dışında, nesne kilitli (WORM) depolamaya ya da merkezi log sistemine düzenli olarak kopyalanır.'),
         o('retention', 'Saklama süresi ve imha', 'Kayıtların ne kadar saklanacağı mevzuat ve kurum politikasıyla belirlenir; süre dolunca imha edilir ya da anonimleştirilir.', 'Kişisel veri içeren kayıtlar.', 'Onay kayıtları 10 yıl saklanır; IP adresleri 2 yıl sonra anonimleştirilir.',
           'Denetim kayıtlarının saklama süresi kişisel veri saklama ve imha politikasında tanımlanır; süre dolan kişisel veri alanları anonimleştirilir.'),
         o('export', 'Denetçi için dışa aktarma', 'Kayıtlar tarih, işlem türü ve kullanıcıya göre süzülüp CSV / PDF olarak dışa aktarılır; dışa aktarma da kayda alınır.', 'İç ve bağımsız denetim yapılan kurumlar.', 'Denetçi 2026 yılı iade onaylarını CSV olarak indirir.',
           'Denetim kayıtları süzülerek CSV / PDF olarak dışa aktarılabilir; dışa aktarma işlemi de denetim kaydına yazılır.'),
     ]},

    {'id': 'approval_dashboard', 'type': 'multiselect', 'label': 'Onay Yönetim Paneli ve Raporlar', 'en': 'Approval Dashboard & Reports', 'agents': [PROC, APP], 'showIf': ON,
     'explanation': 'Yönetim panelinde onay süreci için hangi listelerin ve raporların bulunacağını belirler.',
     'scenario': 'Bekleyen onaylar her projede gerekir; süre ve darboğaz raporları onay hacmi yüksek ya da süreç iyileştirmesi hedeflenen projelerde seçilir.',
     'example': 'Panelde "Onayımı bekleyenler: 7", "Ortalama onay süresi: 5,2 saat", "En çok bekleyen aşama: Finans" kartları görünür.',
     'rule': 'Onay yönetim panelinde şu listeler ve raporlar bulunur: {labels}. Raporlar yalnız yetkili rollere görünür ve kullanıcının yetki alanıyla sınırlıdır.',
     'options': [
         o('pending', 'Bekleyen onaylar', 'Onayımı bekleyenler ve (yetkiliye) bütün bekleyen talepler; süreye göre sıralı, gecikenler işaretli.', 'Bütün projeler.', '"Onayımı bekleyenler" listesinde 48 saati geçen talepler kırmızı.', 'Bekleyen onaylar kişiye ve role göre listelenir; geciken talepler işaretlenir.'),
         o('completed', 'Tamamlanan işlemler', 'Onaylanıp tamamlanan işlemlerin listesi ve ayrıntısı.', 'Bütün projeler.', 'Bu ay tamamlanan 124 işlem.', 'Tamamlanan işlemler süzülebilir liste olarak gösterilir.'),
         o('rejected', 'Reddedilen ve revizyon istenen talepler', 'Red ve revizyon talepleri, gerekçeleriyle.', 'Süreç kalitesinin izlendiği ekipler.', 'Reddedilen 9 talep ve en sık red gerekçesi "belge eksik".', 'Reddedilen ve revizyon istenen talepler gerekçeleriyle listelenir.'),
         o('durations', 'Onay süreleri', 'Ortalama, ortanca ve en uzun onay süreleri; SLA uyum oranı.', 'SLA izlenen süreçler.', 'İade onayında ortanca süre 3,1 saat, SLA uyumu %94.', 'Onay süreleri (ortalama, ortanca, en uzun) ve SLA uyum oranı raporlanır.'),
         o('bottlenecks', 'Darboğaz analizi', 'Taleplerin en uzun beklediği aşama, onaylayan ve işlem türü.', 'Çok aşamalı onay süreçleri.', 'Bekleme süresinin %60\'ı finans aşamasında.', 'Bekleme süresi aşama, onaylayan ve işlem türüne göre ayrıştırılarak darboğazlar raporlanır.'),
         o('workload', 'Onaylayan iş yükü', 'Onaylayan başına bekleyen ve sonuçlanan talep sayısı.', 'Onay yükünün dengelenmesi gereken ekipler.', 'Bir yöneticide 40 talep birikmişken diğerinde 3.', 'Onaylayan başına iş yükü raporlanır.'),
         o('sod_report', 'Görevler ayrılığı ihlal denemeleri', 'Kendi işlemini onaylama, çakışan rol ataması gibi engellenen denemelerin raporu.', 'İç denetime tabi kurumlar.', 'Bu ay engellenen 2 "kendi işlemini onaylama" denemesi.', 'Engellenen görevler ayrılığı ihlal denemeleri raporlanır ve güvenlik sorumlusuna bildirilir.'),
     ]},

    {'id': 'approval_ui', 'type': 'multiselect', 'label': 'Onay Arayüzü Bileşenleri', 'en': 'Approval UI Components', 'agents': [APP], 'showIf': ON,
     'explanation': 'Projedeki onay ekranlarında hangi arayüz bileşenlerinin bulunacağını belirler. Bileşenler projenin mevcut tasarım sistemiyle (renk, tipografi, bileşen kitaplığı) uyumlu yapılır.',
     'scenario': 'Durum rozetleri ve onay geçmişi her projede; toplu onay yalnız düşük riskli ve yüksek hacimli işlemlerde düşünülür.',
     'example': 'İade kaydının üstünde "Onay Bekliyor" rozeti, sağda adım adım onay geçmişi zaman çizelgesi ve "Onayla / Revizyon iste / Reddet" düğmeleri bulunur.',
     'rule': 'Onay arayüzünde şu bileşenler bulunur: {labels}. Durumlar yalnız renkle değil, metin ve simgeyle de gösterilir; onay düğmeleri yalnız yetkili kullanıcıya görünür ve yetki sunucuda yeniden denetlenir.',
     'options': [
         o('badges', 'Durum rozetleri', 'Her kayıtta durumu gösteren rozet (Taslak, Onay Bekliyor, Onaylandı, Revizyon İstendi, Reddedildi, Tamamlandı).', 'Bütün projeler.', 'Listede her satırda renkli ve simgeli durum rozeti.', 'Kayıt listelerinde ve ayrıntı ekranında simgeli durum rozetleri gösterilir.'),
         o('timeline', 'Onay geçmişi zaman çizelgesi', 'Kaydın kim tarafından, ne zaman, hangi gerekçeyle hangi duruma geçtiğini gösteren zaman çizelgesi.', 'Bütün projeler.', '"Ayşe Y. hazırladı · 10.11 09:12 → Mehmet K. revizyon istedi: fatura eksik · 10.11 11:40".', 'Kayıt ayrıntısında onay geçmişi zaman çizelgesi gösterilir.'),
         o('flow_diagram', 'Akış diyagramı ve aşama göstergesi', 'Kaydın akıştaki yerini ve kalan aşamaları gösteren adım göstergesi.', 'Çok aşamalı onay süreçleri.', '"Aşama 2 / 3 — Finans onayı bekleniyor".', 'Çok aşamalı onayda kaydın bulunduğu aşama ve kalan aşamalar adım göstergesiyle gösterilir.'),
         o('reason_required', 'Red ve revizyonda zorunlu gerekçe', 'Reddetme ve revizyon isteme gerekçe yazılmadan yapılamaz.', 'Bütün projeler.', '"Reddet" penceresinde gerekçe alanı doldurulmadan düğme etkinleşmez.', 'Red ve revizyon isteme gerekçe alanı doldurulmadan yapılamaz; gerekçe hazırlayana gösterilir ve kayda alınır.'),
         o('reauth', 'Onayda yeniden doğrulama', 'Yüksek riskli onaylarda parola ya da iki adımlı doğrulama yeniden istenir.', 'Para ve yetki işlemleri.', '50.000 TL üstü ödemeyi onaylarken iki adımlı doğrulama kodu istenir.', 'Yüksek riskli onaylarda yeniden kimlik doğrulama (parola ya da iki adımlı doğrulama) istenir.'),
         o('bulk', 'Toplu onay (yalnız düşük risk)', 'Aynı türden düşük riskli talepler toplu onaylanabilir; yüksek riskli ve 6 gözlü talepler toplu onaylanamaz.', 'Yüksek hacimli, düşük riskli içerik ya da küçük tutarlı işlemler.', 'Moderatör 30 yorum yayın talebini tek seferde onaylar.', 'Toplu onay yalnız düşük riskli işlem türlerinde açıktır; her kayıt için ayrı onay kaydı oluşturulur.'),
     ]},

    {'id': 'approval_arch', 'type': 'select', 'label': 'Onay Modülü Mimarisi', 'en': 'Approval Module Architecture', 'agents': [APP], 'showIf': ON,
     'explanation': 'Onay modülünün projede nasıl kurulacağını belirler. Modül bağımsız ve yeniden kullanılabilir olmalı; etkin değilse yüklenmemeli, tablo oluşturmamalı ve bağımlılık eklememelidir.',
     'scenario': 'Çoğu projede uygulama içinde bağımsız bir modül yeterlidir; çok sayıda karmaşık, uzun süren süreç varsa iş akışı motoru değerlendirilir.',
     'example': 'Onay modülü "approvals" klasöründe kendi tabloları, servisleri ve arayüz bileşenleriyle durur; iade, fiyat ve rol modülleri ona yalnız "onaya gönder" arayüzüyle bağlanır.',
     'rule': 'Onay modülü mimarisi: {label}. Modül bağımsızdır: onaya tabi kayıtlar modüle ortak bir arayüzle (ör. onaylanabilir kayıt sözleşmesi: tür, kimlik, kritik alanlar, uygula / geri al) bağlanır, modül diğer modüllerin iç yapısını bilmez; modül kapalıyken yüklenmez, tablo oluşturmaz ve bağımlılık eklemez.',
     'options': [
         o('module', 'Uygulama içinde bağımsız modül (önerilen)', 'Kendi tabloları (talep, adım, kural, kural sürümü, denetim kaydı), servisleri ve arayüz bileşenleriyle uygulama içinde ayrı bir modül.', 'Çoğu web projesi.', 'Yeni bir işlem türünü onaya bağlamak için yalnız o türün sözleşmesi yazılır.',
           'Modül uygulama içinde ayrı klasör / paket olarak kurulur (tablolar: onay talebi, onay adımı, onay kuralı ve sürümü, denetim kaydı); olay tabanlı arayüzle diğer modüllere bağlanır, başka projelere taşınabilir.'),
         o('engine', 'İş akışı motoru (BPMN / durable workflow)', 'Camunda, Flowable ya da Temporal gibi bir iş akışı motoru üzerinde, süreçler modellenerek çalıştırılır.', 'Çok sayıda, uzun süren ve sık değişen çok aşamalı süreç.', 'Satın alma süreci BPMN diyagramı olarak modellenir ve motor tarafından yürütülür.',
           'Onay süreçleri bir iş akışı motorunda (BPMN ya da durable workflow) modellenir; uygulama motora yalnız ortak arayüzle bağlanır, motor kapalıyken modül devre dışı kalır.'),
         o('platform', 'CMS / platformun hazır iş akışı özelliği', 'Kullanılan CMS ya da platformun yerleşik onay / editoryal iş akışı özelliği kullanılır.', 'Onay ihtiyacı yalnız içerik yayınıyla sınırlı, hazır CMS kullanan projeler.', 'Headless CMS\'in yayın onayı (workflow) özelliği açılır.',
           'Platformun yerleşik onay özelliği kullanılır; bu bölümdeki görevler ayrılığı, yeniden onay ve denetim kaydı gereksinimlerini karşılamadığı noktalar ek geliştirmeyle tamamlanır.'),
     ]},
]

for f in F:
    f['section'] = SECTION['id']
    for x in f.get('options') or []:
        if x.get('ruleDetail') is None:
            x.pop('ruleDetail', None)

out = {'version': 1, 'fields_into': [], 'guide_add': {}, 'section': SECTION, 'guide': GUIDE, 'fields': F}
p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'onay-akisi.json')
json.dump(out, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('yazıldı:', p, '· alan', len(F), '· seçenek', sum(len(f.get('options') or []) for f in F))
