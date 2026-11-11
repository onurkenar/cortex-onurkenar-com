#!/usr/bin/env python3
"""Meta Servisleri menüsünün kaynağı (2026-11-11). Elle yazılır; çıktı meta.json → meta_ekle.py.

Kullanım: python3 -I docs/meta/kaynak.py docs/meta/meta.json

Yapı: GROUP, AGENTS (kısaltma → pozisyon ajanı), SECTIONS (bölüm → rehber + kararlar), IDS_ADD (Ortak Bilgiler › Hesap ve
Etiket Kimlikleri'ne eklenen satırlar), IDS_WHEN (satır → bu satırı görünür yapan servisler). Seçenek yardımcısı
o(değer, etiket, açıklama, senaryo, örnek, kural ayrıntısı). Kaynak adresleri 2026-11-11'de iki araştırma ajanı tarafından
açılarak doğrulandı; facebook.com/business/help sayfaları gövdeyi otomatik araçlara vermediği için yalnız başlıkları
doğrulandı. Meta'nın ücret, limit ve uygunluk kuralları sık değişir: içerik güncellenirken kaynaklar yeniden açılmalı.
"""
import json
import sys

GROUP = "Meta Servisleri"
AGENTS = {
    "S": "poz:pazarlama:social_media_marketing/kanal-yonetimi-yoneticisi",
    "IG": "poz:pazarlama:social_media_marketing/kanal-yonetimi-yoneticisi/instagram-uzmani",
    "FB": "poz:pazarlama:social_media_marketing/kanal-yonetimi-yoneticisi/facebook-uzmani",
    "WA": "poz:pazarlama:social_media_marketing/kanal-yonetimi-yoneticisi/whatsapp-uzmani",
    "PS": "poz:pazarlama:digital_demand_generation/performans-pazarlama-muduru/ucretli-sosyal-medya-uzmani",
    "O": "poz:pazarlama:digital_demand_generation/web-pazarlama-muduru/dijital-olcumleme-uzmani",
    "K": "poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani",
    "I": "poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/kidemli-kimlik-ve-erisim-uzmani",
    "API": "poz:bilgi-teknolojileri:15.05/entegrasyon-ve-api-yonetimi/api-ve-entegrasyon-uzmani",
    "MI": "poz:pazarlama:marketing_operations_crm_martech/martech-ve-entegrasyon-muduru/entegrasyon-uzmani",
    "CX": "poz:musteri-deneyimi:11.04/cok-kanalli-destek/kidemli-cok-kanalli-destek-uzmani",
}


def o(value, label, explanation, scenario, example, rd=None, **kw):
    x = {"value": value, "label": label, "explanation": explanation, "scenario": scenario, "example": example}
    if rd:
        x["ruleDetail"] = rd
    x.update(kw)
    return x


def r(title, url, note):
    return {"title": title, "url": url, "note": note}


SV = lambda *v: [{"field": "mt_services", "in": list(v)}]
ALL = ("portfolio", "page", "instagram", "whatsapp", "pixel", "ads", "catalog")
DEV = "https://developers.facebook.com/documentation/business-messaging/whatsapp/"

SECTIONS = []

# 1 — Kapsam, İşletme Portföyü & Erişim
SECTIONS.append({
 "id": "mt_scope", "name": "Kapsam, İşletme Portföyü & Erişim", "en": "Scope, Business Portfolio & Access", "icon": "◉", "agents": ["S", "I"],
 "refs": ["mk_brand_name", "oc_legal_name", "domain_name", "mk_accounts", "mk_ids"],
 "desc": "Projede hangi Meta varlıklarının kurulacağını, bu varlıkların hangi işletme portföyüne ait olacağını ve kimin, hangi yetkiyle erişeceğini belirler; sonraki bölümler buradaki seçime göre açılır",
 "guide": {
  "purpose": "Facebook Sayfası, Instagram hesabı, WhatsApp numarası, reklam hesabı, piksel (veri kümesi) ve katalog Meta'da bir işletme portföyüne (eski adıyla Business Manager; yönetim ekranı Meta Business Suite) bağlanır. Portföyün sahibi bu varlıkların, reklam geçmişinin ve faturaların da sahibidir. Bu bölüm kurulacak varlıkları seçtirir, sahipliği kuruma bağlar ve erişimi en düşük yetki ilkesine göre düzenler. Seçtiğiniz varlıkların bölümleri menüde açılır; Ortak Bilgiler › Hesap ve Etiket Kimlikleri'nde de o varlıkların kimlik kutuları üste gelir.",
  "criteria": [
   "Bütün varlıklar kurumun kendi işletme portföyündedir; ajans varlıklara kendi portföyünden iş ortağı olarak erişir.",
   "Portföyde tam kontrollü en az iki kurum çalışanı vardır ve iki faktörlü doğrulama herkes için zorunludur.",
   "Reklam, WhatsApp Cloud API ya da yüksek mesaj limiti gerekiyorsa işletme doğrulaması tamamlanmıştır; ticari unvan ve adres belgelerle birebir aynıdır.",
   "API entegrasyonları kişisel hesap jetonuyla değil, sistem kullanıcısıyla çalışır; kimin hangi varlıkta hangi yetkiye sahip olduğu yazılı bir erişim listesindedir."],
  "pitfalls": [
   "Sayfayı ya da reklam hesabını bir çalışanın kişisel profilinde veya ajansın portföyünde açmak: kişi ayrılınca ya da ajansla yollar ayrılınca varlıklar, takipçiler ve reklam geçmişi kurumdan kopar.",
   "Tek yöneticiyle çalışmak: o kişinin Facebook hesabı kilitlenirse ya da ele geçirilirse portföye kimse erişemez.",
   "Ajans çalışanlarını tek tek kişi olarak eklemek: ajans değişince kimin erişimi olduğu takip edilemez; iş ortağı erişimi tek noktadan kaldırılır.",
   "Ticari unvanı belgelerden farklı yazmak: işletme doğrulaması reddedilir, WhatsApp ve reklam limitleri düşük kalır."],
  "resources": [
   r("Meta Business Suite'te işletme portföyü oluşturma", "https://www.facebook.com/business/help/1710077379203657", "Meta Yardım Merkezi: portföyün nasıl açıldığı."),
   r("İşletme doğrulaması", "https://www.facebook.com/business/help/2058515294227817", "Meta Yardım Merkezi: işletme doğrulamasının adımları ve istenen belgeler."),
   r("Bir iş ortağına varlık erişimi verme", "https://www.facebook.com/business/help/1717412048538897", "Ajansa varlıkları kendi portföyünden yönetme yetkisi vermek."),
   r("Sistem kullanıcıları (Business Management API)", "https://developers.facebook.com/docs/business-management-apis/system-users", "Sunucu ve yazılım entegrasyonları için kişiye bağlı olmayan kullanıcılar ve jetonlar."),
   r("Sistem kullanıcısı ekleme", "https://www.facebook.com/business/help/503306463479099", "Meta Yardım Merkezi: sistem kullanıcısını portföye ekleme."),
   r("Meta Verified", "https://about.fb.com/meta-verified/", "Meta'nın işletmeler için ücretli doğrulama ve destek aboneliği; ülkeye göre uygunluk değişir.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_services", "label": "Kurulacak Meta Varlıkları", "en": "Meta Assets to Set Up", "type": "multiselect",
  "explanation": "Bu projede kurulacak ya da düzenlenecek Meta varlıklarını seçer. Seçtiğiniz varlıkların kurulum bölümleri menüde açılır; seçilmeyenler gizli kalır ve kurallara girmez.",
  "scenario": "Sosyal medyada görünür olmak isteyen çoğu işletme işletme portföyü, Facebook Sayfası ve Instagram'ı seçer; reklam verilecekse piksel ve reklam hesabı, mesajla satış ya da destek yapılacaksa WhatsApp Business, e-ticarette katalog eklenir.",
  "example": "Bir güzellik salonu işletme portföyü, Sayfa, Instagram, WhatsApp Business, piksel ve reklam hesabını seçer; katalog bölümü menüde görünmez.",
  "rule": "Kurulacak Meta varlıkları: {labels}.",
  "recommend": [
   {"field": "mk_ads_channels", "map": {"meta": ["portfolio", "page", "instagram", "pixel", "ads"]}},
   {"field": "mk_platforms", "map": {"instagram": ["portfolio", "instagram"], "facebook": ["portfolio", "page"], "threads": ["instagram"], "whatsapp": ["whatsapp"], "whatsapp_group": ["whatsapp"], "whatsapp_community": ["whatsapp"]}},
   {"field": "mk_conversions", "map": {"whatsapp": ["whatsapp"]}},
   {"field": "modules_extra", "map": {"ecommerce": ["catalog", "pixel"]}},
   {"field": "mk_meta_objectives", "map": {"catalog": ["catalog"], "messages": ["whatsapp", "page"], "website": ["pixel"], "retargeting": ["pixel"], "instant_form": ["page"]}},
   {"field": "mk_meta_prereq", "map": {"pixel": ["pixel"], "capi": ["pixel"], "domain": ["pixel"], "bm": ["portfolio"]}}],
  "options": [
   o("portfolio", "İşletme portföyü (Meta Business Suite)", "Sayfa, Instagram, WhatsApp, reklam hesabı, piksel ve katalog gibi varlıkların bağlandığı kurumsal çatı hesaptır; kişiler, ajanslar ve yetkiler buradan yönetilir.",
     "Meta'da birden çok varlık kullanacak ya da ajansla çalışacak her işletme.",
     "Kurumun portföyünde iki yönetici, bir ajans iş ortağı ve beş varlık görünür.",
     "Bütün Meta varlıkları kurumun işletme portföyünde toplanır; kişiler ve ajanslar yetkiyi portföy üzerinden alır."),
   o("page", "Facebook Sayfası", "İşletmenin Facebook'taki herkese açık profilidir; reklamların, Messenger'ın ve WhatsApp'a tıklama reklamlarının kimliği Sayfadır.",
     "Facebook'ta görünmek, Meta reklamı vermek ya da Messenger'dan mesaj almak isteyen işletmeler. Reklam verilecekse zorunludur.",
     "Sayfada logo, kapak, iletişim bilgileri, çalışma saatleri ve “WhatsApp'tan yaz” düğmesi görünür."),
   o("instagram", "Instagram profesyonel hesap", "İşletme ya da içerik üreticisi türündeki Instagram hesabıdır; istatistikler, iletişim düğmeleri, reklam ve API erişimi profesyonel hesapla gelir.",
     "Görsel içerik üreten, Instagram'dan mesaj alan ya da Instagram'da reklam verecek işletmeler.",
     "Profilde kategori, “Ara” ve “Mesaj gönder” düğmeleri ve biyografide beş bağlantı görünür."),
   o("whatsapp", "WhatsApp Business", "Müşterilerle WhatsApp üzerinden yazışmak için kurumsal hesaptır: telefondaki WhatsApp Business uygulaması ya da yazılımla bağlanan WhatsApp Cloud API.",
     "Teklif, randevu, sipariş ya da destek talepleri WhatsApp'tan gelen işletmeler; sitede “WhatsApp'tan yazın” düğmesi ya da WhatsApp'a yönlendiren reklam varsa.",
     "Müşteri sitedeki düğmeye basar, işletmenin onaylı adıyla açılan sohbete hazır mesajla yazar."),
   o("pixel", "Meta Pikseli ve Conversions API", "Sitedeki ziyaretçi işlemlerini (form, arama, satın alma) Meta'ya bildiren ölçüm altyapısıdır: tarayıcıda Piksel, sunucuda Conversions API; ikisi aynı veri kümesine (dataset) gönderir.",
     "Meta reklamlarının sitede dönüşüm getirip getirmediğini ölçmek, site ziyaretçilerine yeniden reklam göstermek ya da reklamı dönüşüme göre optimize etmek isteyen işletmeler.",
     "Randevu formu gönderilince “Lead” olayı tarayıcıdan ve sunucudan aynı olay kimliğiyle gider; Meta tek dönüşüm sayar."),
   o("ads", "Meta reklam hesabı", "Facebook, Instagram, Messenger ve WhatsApp'a tıklama reklamlarının açıldığı, ödeme yönteminin ve faturaların bağlı olduğu hesaptır.",
     "Meta'da ücretli reklam verecek işletmeler. Kampanya stratejisi Pazarlama Kararları › Meta Ads'te, hesap kurulumu burada belirlenir.",
     "Reklam hesabı kurumun portföyünde TRY para birimi ve İstanbul saat dilimiyle açılır; ajans iş ortağı erişimiyle kampanya yönetir."),
   o("catalog", "Katalog (Commerce Manager)", "Ürün ya da hizmetlerin adı, fiyatı, görseli ve bağlantısını Meta'ya veren listedir; katalog reklamları, Instagram ürün etiketleri ve WhatsApp kataloğu bunu kullanır.",
     "E-ticaret siteleri, çok sayıda hizmet ya da ürün paketi olan işletmeler, katalog satışı reklamı verecek olanlar.",
     "Sepeti terk eden ziyaretçiye, baktığı ürünün güncel fiyatlı görseli reklam olarak gösterilir.")]},
 {"id": "mt_owner", "label": "Varlıkların Sahipliği", "en": "Asset Ownership", "type": "select",
  "explanation": "Meta varlıklarının hangi işletme portföyüne ait olacağını belirler. Varlığın sahibi olan portföy, takipçileri, reklam geçmişini, ölçüm verisini ve faturaları da elinde tutar.",
  "scenario": "Yeni kurulumda kurumun kendi portföyü; varlıklar daha önce ajansın ya da bir çalışanın hesabında açıldıysa kuruma taşıma seçilir.",
  "example": "Ajansın portföyünde açılmış reklam hesabı kurumun portföyüne taşınır; ajans aynı hesabı iş ortağı erişimiyle yönetmeye devam eder.",
  "rule": "Meta varlıklarının sahipliği: {label}.",
  "options": [
   o("own", "Kurumun kendi işletme portföyü (önerilen)", "Bütün varlıklar kurumun portföyünde açılır; ajans ve serbest çalışanlar yetkiyi bu portföyden alır.",
     "Yeni kurulan ya da varlıkları zaten kurumda olan işletmeler.", "Portföy “Kurum Adı A.Ş.” adına, iki çalışan tam kontrollü yönetici.",
     "Varlıklar kurumun kendi işletme portföyünde açılır ve kalır; ajans yalnız iş ortağı erişimiyle çalışır, varlık sahipliği hiçbir zaman ajansa ya da kişisel profile geçmez."),
   o("migrate", "Ajansta ya da kişisel hesapta olan varlıklar kuruma taşınacak", "Daha önce ajansın portföyünde ya da bir çalışanın profilinde açılmış Sayfa, Instagram, reklam hesabı ve pikselin sahipliği kurumun portföyüne aktarılır.",
     "Ajans değişikliği, çalışan ayrılığı ya da “hesap ajansta kaldı” durumu.", "Ajans Sayfayı kurum portföyüne aktarır, kendisi iş ortağı erişimine geçer; eski reklam hesabının geçmişi raporlanıp saklanır.",
     "Ajansın ya da kişisel profilin sahibi olduğu varlıklar kurumun portföyüne aktarılır; aktarılamayan varlıkta (ör. sahipliği devredilemeyen reklam hesabı) kurum portföyünde yenisi açılır ve eski hesabın raporları dışa aktarılıp saklanır."),
   o("agency", "Ajansın portföyünde kalacak", "Varlıklar ajansın portföyünde açılır, kurum yalnız erişim alır. Kurumun kontrolünü zayıflattığı için önerilmez.",
     "Yalnız kısa süreli, deneme amaçlı kampanyalar; sözleşmede devir maddesi varsa.", "Kampanya bitince ajans reklam hesabını kapatır, veriler ajansta kalır.",
     "Varlıklar ajansın portföyündedir; sözleşmede devir ve veri teslimi maddesi bulunur, kurum en az bir yöneticiyle erişimi elinde tutar.")]},
 {"id": "mt_access", "label": "Erişim ve Güvenlik", "en": "Access & Security", "type": "multiselect",
  "explanation": "İşletme portföyüne kimin, hangi yetkiyle erişeceğini ve hesap güvenliğini belirler.",
  "scenario": "En az iki yönetici ve herkes için iki faktörlü doğrulama her kurulumda seçilir; ajansla çalışılıyorsa iş ortağı erişimi, yazılım entegrasyonu varsa sistem kullanıcısı eklenir.",
  "example": "Portföyde iki tam kontrollü çalışan, ajans iş ortağı olarak yalnız reklam hesabı ve pikselde; CRM entegrasyonu sistem kullanıcısının jetonuyla çalışır.",
  "rule": "Meta işletme portföyünün erişim ve güvenlik kuralları: {labels}.",
  "options": [
   o("two_admins", "En az iki tam kontrollü yönetici", "Portföyde ve her varlıkta tam kontrole sahip en az iki kurum çalışanı bulunur.", "Her kurulum.", "Genel müdür ve pazarlama müdürü tam kontrollü.",
     "İşletme portföyünde ve her varlıkta tam kontrole sahip en az iki kurum çalışanı bulunur; yönetici kurumsal e-posta adresiyle kayıtlıdır."),
   o("2fa_all", "Herkes için iki faktörlü doğrulama zorunlu", "Portföy ayarlarından iki faktörlü doğrulama bütün kişiler için zorunlu tutulur; doğrulamayı açmayan kişi varlıklara erişemez.", "Her kurulum.", "Yeni eklenen ajans çalışanı doğrulamayı açana kadar varlıkları göremez.",
     "İşletme portföyünde iki faktörlü doğrulama herkes için zorunludur; tercihen doğrulama uygulaması ya da güvenlik anahtarı kullanılır, SMS yalnız yedektir."),
   o("verify", "İşletme doğrulaması", "Meta, işletmenin gerçekliğini ticari unvan, adres ve telefon belgeleriyle doğrular. WhatsApp Cloud API'de limitlerin yükselmesi, resmî işletme hesabı başvurusu ve bazı reklam özellikleri için gerekir.", "Reklam veren, WhatsApp Cloud API kullanan ya da mavi tik isteyen işletmeler.", "Portföy ayarlarında “Doğrulandı” durumu görünür.",
     "İşletme doğrulaması ticari unvan, adres ve telefon Ortak Bilgiler'dekiyle ve resmî belgelerle birebir aynı olacak şekilde tamamlanır."),
   o("partner", "Ajansa iş ortağı erişimi", "Ajans kendi portföyüyle bağlanır, varlıklara yalnız gereken yetkiyle erişir; ajans değişince tek işlemle kaldırılır.", "Ajans ya da serbest çalışanla yürütülen hesaplar.", "Ajans yalnız reklam hesabı ve pikselde “kampanyaları yönet” yetkisiyle görünür.",
     "Ajans varlıklara kendi işletme portföyünden iş ortağı erişimiyle bağlanır; ajans çalışanları kurumun portföyüne tek tek eklenmez."),
   o("system_user", "Entegrasyonlar için sistem kullanıcısı", "Sunucu ya da CRM gibi yazılımların Meta API'lerine erişimi için kişiye bağlı olmayan kullanıcıdır; jetonu çalışan ayrılınca geçersiz olmaz.", "Conversions API, WhatsApp Cloud API, katalog ya da lead entegrasyonu olan projeler.", "Conversions API sunucusu “capi-sunucu” sistem kullanıcısının jetonuyla çalışır.",
     "API entegrasyonları kişisel kullanıcı jetonuyla değil, yalnız gereken varlık ve izinlere sahip sistem kullanıcısının jetonuyla çalışır; jeton sunucuda gizli anahtar deposunda tutulur ve düzenli yenilenir."),
   o("least", "En düşük yetki", "Her kişi ve iş ortağı yalnız ihtiyaç duyduğu varlıkta ve yetkide bulunur; tam kontrol yalnız yöneticilerde.", "Birden çok kişinin çalıştığı her portföy.", "Topluluk yöneticisi yalnız Sayfa ve Instagram'da içerik ve mesaj yetkisine sahip.",
     "Kişi ve iş ortaklarına yalnız görevleri için gereken varlıkta, gereken kısmi yetki verilir; tam kontrol yalnız yöneticilerdedir."),
   o("review", "Üç ayda bir erişim gözden geçirme", "Portföydeki kişiler, iş ortakları, sistem kullanıcıları ve bağlı uygulamalar düzenli kontrol edilir.", "Her kurulum.", "Ocak, Nisan, Temmuz ve Ekim'de erişim listesi portföyle karşılaştırılır.",
     "Portföydeki kişiler, iş ortakları, sistem kullanıcıları ve bağlı uygulamalar üç ayda bir gözden geçirilir; kullanılmayan erişim kaldırılır."),
   o("offboarding", "Ayrılan kişinin erişimi aynı gün kaldırılır", "Kurumdan ya da projeden ayrılan kişinin ve sona eren ajansın erişimi gecikmeden kaldırılır.", "Her kurulum.", "Çalışanın son gününde portföy, Sayfa ve WhatsApp erişimi kapatılır.",
     "Kurumdan ya da projeden ayrılan kişinin ve sözleşmesi biten ajansın Meta erişimi aynı gün kaldırılır; paylaşılan jeton varsa yenilenir.")]}]

# 2 — Rıza, KVKK & Ticari İleti
SECTIONS.append({
 "id": "mt_consent", "name": "Rıza, KVKK & Ticari İleti", "en": "Consent, Privacy & Commercial Messages", "icon": "⚖", "agents": ["K", "O"],
 "desc": "Meta Pikseli ve Conversions API için çerez onayını, Meta'ya giden kişisel verinin hukuki dayanağını ve WhatsApp, Instagram, Messenger üzerinden gönderilecek ticari iletilerin onay kurallarını belirler",
 "guide": {
  "purpose": "Meta Pikseli ziyaretçinin tarayıcısına reklam çerezi yazar ve davranış verisini Meta'ya gönderir; Conversions API aynı veriyi sunucudan iletir. KVKK'nın Temmuz 2025 tarihli Çerez Uygulamaları Hakkında Rehberi davranışsal reklam çerezleri için açık rıza arar. Meta'ya giden veri yurt dışına aktarım sayılır ve 6698 sayılı Kanun'un 9. maddesine göre bir dayanağa bağlanmalıdır. WhatsApp, Instagram ve Messenger'dan gönderilen kampanya mesajları da ticari ileti niteliğindedir ve önceden onay ister. Bu bölüm bu üç konuyu kurulumdan önce netleştirir.",
  "criteria": [
   "Pazarlama çerezlerine onay verilmeden Meta Pikseli hiçbir istek göndermez ve Conversions API olayı gönderilmez; onay geri çekilince gönderim durur.",
   "Aydınlatma metni ve çerez politikası Meta araçlarını, aktarılan veriyi ve yurt dışına aktarım dayanağını açıkça yazar.",
   "Meta'ya sağlık, finans gibi hassas içerik ya da düz metin kişisel veri gitmez.",
   "WhatsApp ve diğer kanallardan pazarlama mesajı yalnız önceden alınmış ve kaydı tutulan onayla gönderilir; ret talebi hemen uygulanır."],
  "pitfalls": [
   "Pikseli sayfa açılır açılmaz yükleyip onay penceresini yalnız görüntü olarak koymak: KVKK'ya göre onaydan önce çerez yazılmış olur.",
   "Conversions API'yi “sunucu taraflı olduğu için onay gerekmez” diye düşünmek: onay reddedilen ziyaretçinin olayı sunucudan da gönderilmemelidir.",
   "Yurt dışına aktarım için standart sözleşme imzalayıp Kurum'a 5 iş günü içinde bildirmeyi unutmak.",
   "Telefon numarasını müşteri “bilgi için” verdi diye ona WhatsApp'tan kampanya mesajı göndermek."],
  "resources": [
   r("KVKK — Çerez Uygulamaları Hakkında Rehber (Temmuz 2025)", "https://kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber", "Davranışsal reklam çerezleri açık rıza gerektirir (§6.2)."),
   r("KVKK — Standart Sözleşmeler", "https://www.kvkk.gov.tr/Icerik/7929/Standart-Sozlesmeler", "Yurt dışına aktarımda kullanılan dört standart sözleşme metni."),
   r("KVKK — Standart Sözleşme Bildirim Modülü duyurusu", "https://www.kvkk.gov.tr/Icerik/8043/Standart-Sozlesme-Bildirim-Modulu-Hakkinda-Kamuoyu-Duyurusu", "Standart sözleşme imzadan itibaren 5 iş günü içinde Kurum'a bildirilir."),
   r("KVKK — Standart sözleşmelerde dikkat edilecek hususlar", "https://www.kvkk.gov.tr/Icerik/8170/Yurt-Disina-Kisisel-Veri-Aktariminda-Kullanilacak-Standart-Sozlesmelerde-Dikkat-Edilmesi-Gereken-Hususlara-Iliskin-Kamuoyu-Duyurusu", "Tarafların imza tarihleri sözleşmeye yazılır (5 Şubat 2025)."),
   r("6563 sayılı Elektronik Ticaretin Düzenlenmesi Hakkında Kanun", "https://www.mevzuat.gov.tr/mevzuatmetin/1.5.6563.pdf", "Ticari elektronik iletinin tanımı (m. 2) ve önceden onay şartı (m. 6)."),
   r("Meta Pikseli — onay (consent) API'si", "https://developers.facebook.com/docs/meta-pixel/implementation/gdpr", "fbq('consent','revoke') ve fbq('consent','grant') kullanımı."),
   r("WhatsApp Business Messaging Policy", "https://whatsappbusiness.com/policy/", "WhatsApp'ta onay (opt-in), ret ve mesaj kuralları.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_cm_mode", "label": "Piksel Onay Yöntemi", "en": "Pixel Consent Method", "type": "select", "showIf": SV("pixel", "ads"),
  "explanation": "Meta Pikseli ve Conversions API'nin çerez onayına nasıl bağlanacağını belirler.",
  "scenario": "Çoğu sitede pikselin onaydan önce hiç yüklenmemesi en sade ve güvenli yoldur; piksel Etiket Yöneticisi ya da bir eklentiyle yükleniyorsa onay API'si de doğru kurulabilir.",
  "example": "Ziyaretçi çerez penceresinde “Pazarlama”yı açınca piksel yüklenir; reddederse ağ sekmesinde facebook.com'a hiçbir istek görünmez.",
  "rule": "Meta Pikseli onay yöntemi: {label}.",
  "options": [
   o("block", "Onaydan önce piksel yüklenmez (önerilen)", "Piksel kodu yalnız ziyaretçi pazarlama çerezlerine onay verdikten sonra sayfaya eklenir.", "Çerez onay aracı (CMP) kullanan her site.", "Onay verilince piksel yüklenir ve PageView gönderilir.",
     "Meta Pikseli kodu yalnız pazarlama çerezlerine onay verildikten sonra yüklenir; onaydan önce hiçbir Meta isteği gitmez, Conversions API olayı da onay bilgisi olmadan gönderilmez."),
   o("consent_api", "Piksel onay API'siyle (revoke → grant)", "Piksel yüklenir ama başlatılmadan önce fbq('consent','revoke') çağrılır; onay gelince fbq('consent','grant') ile gönderim başlar.", "Pikselin bir eklenti ya da Etiket Yöneticisi şablonuyla yüklendiği, onayın aynı sayfada değiştiği siteler.", "Çerez aracının “onay değişti” olayı fbq('consent','grant') çağırır.",
     "Meta Pikseli başlatılmadan önce fbq('consent','revoke') çağrılır, pazarlama onayı verilince fbq('consent','grant') çağrılır, onay geri çekilince yeniden revoke edilir; Conversions API olayları da aynı onay durumuna bağlıdır."),
   o("none", "Onay yönetimi yok", "Piksel onaysız çalışır. KVKK Çerez Rehberi'ne aykırıdır; önerilmez.", "Yalnız pikselin hiç kullanılmadığı ya da yalnız Türkiye dışındaki, onay şartı olmayan bir pazara yönelik özel durumlar; hukuk birimi onayıyla.", "Piksel her ziyaretçide çalışır.",
     "Meta Pikseli onay yönetimi olmadan çalışır; bu durum hukuk birimince yazılı olarak değerlendirilmiş ve gerekçesi kayda geçirilmiştir.")]},
 {"id": "mt_privacy", "label": "Kişisel Veri ve Yurt Dışına Aktarım", "en": "Personal Data & Cross-border Transfer", "type": "multiselect", "showIf": SV(*ALL),
  "explanation": "Meta araçlarıyla işlenen kişisel veri için aydınlatma, çerez politikası, yurt dışına aktarım ve hassas veri kurallarını belirler.",
  "scenario": "Piksel, reklam ya da WhatsApp kullanan her işletme aydınlatma ve çerez politikasını günceller; Meta'ya veri aktarılıyorsa aktarım dayanağı belirlenir.",
  "example": "Çerez politikasında _fbp ve _fbc çerezleri amaç ve süreyle listelenir; aydınlatma metninde “Meta Platforms'a yurt dışına aktarım” paragrafı yer alır.",
  "rule": "Meta araçlarında kişisel veri kuralları: {labels}.",
  "options": [
   o("notice", "Aydınlatma metninde Meta araçları", "Aydınlatma metni Meta Pikseli, Conversions API, reklam kitleleri ve WhatsApp yazışmalarında işlenen veriyi, amacı ve hukuki sebebi yazar.", "Meta aracı kullanan her site.", "“Reklamların ölçümü için Meta Pikseli…” paragrafı.",
     "Aydınlatma metni Meta Pikseli, Conversions API, reklam kitleleri ve WhatsApp yazışmalarında işlenen kişisel veriyi, amacını, hukuki sebebini ve alıcı grubunu açıkça yazar."),
   o("cookie_policy", "Çerez politikasında Meta çerezleri", "Çerez politikası Meta'nın çerezlerini (ör. _fbp, _fbc) amaç ve süreyle listeler; tablo gerçek taramayla güncellenir.", "Pikselli her site.", "Çerez tablosunda “_fbp — Meta — pazarlama — 90 gün” satırı.",
     "Çerez politikasındaki tablo Meta çerezlerini sağlayıcı, amaç, kategori ve süreyle listeler; tablo sitedeki gerçek çerez taramasıyla güncel tutulur."),
   o("transfer", "Yurt dışına aktarım dayanağı", "Meta'ya giden kişisel veri yurt dışına aktarımdır; 6698 m. 9'a göre dayanak belirlenir. Standart sözleşme kullanılırsa imzadan itibaren 5 iş günü içinde Kurum'a bildirilir.", "Piksel, Conversions API, müşteri listesi ya da WhatsApp Cloud API kullanan işletmeler.", "Hukuk birimi aktarım dayanağını belirler; bildirim Standart Sözleşme Bildirim Modülü'nden yapılır.",
     "Meta'ya kişisel veri aktarımı için KVKK m. 9 kapsamında dayanak belirlenir; standart sözleşme kullanılırsa imzadan itibaren 5 iş günü içinde Kurum'a bildirilir ve kayıt saklanır."),
   o("no_sensitive", "Hassas veri ve düz metin kişisel veri gönderilmez", "Sağlık, finans, din, siyasi görüş gibi hassas bilgiler ve düz metin ad, e-posta, telefon Meta'ya gitmez.", "Özellikle sağlık, finans, hukuk ve eğitim siteleri.", "Klinik sitesinde olay adı “Lead”dir; “kanser_randevu” gibi tanı belirten özel olay yoktur.",
     "Meta'ya giden olay adlarında, parametrelerde ve adreslerde sağlık, finans gibi hassas bilgi ya da düz metin kişisel veri bulunmaz; Events Manager'da veri kaynağının sektör kategorisi doğru beyan edilir."),
   o("customer_list", "Müşteri listesi kuralları", "Reklam için Meta'ya yüklenen müşteri listeleri (Özel Hedef Kitle) yalnız hukuki dayanağı olan kişilerden oluşur ve karma yapılarak yüklenir.", "Müşteri listesiyle reklam verecek işletmeler.", "Yalnız pazarlama onayı olan müşterilerin e-postaları yüklenir.",
     "Meta'ya yüklenen müşteri listeleri yalnız pazarlama onayı ya da başka geçerli dayanağı olan kişilerden oluşur; liste karma yapılarak yüklenir, ret veren kişi sonraki yüklemeden çıkarılır."),
   o("retention", "Saklama ve silme", "Conversions API logları, WhatsApp yazışmaları ve indirilen lead dosyaları için saklama süresi belirlenir.", "Sunucu taraflı olay ya da WhatsApp entegrasyonu olan projeler.", "CAPI istek logları 30 gün, WhatsApp yazışmaları sözleşme süresince saklanır.",
     "Conversions API istek logları, WhatsApp yazışmaları ve indirilen lead dosyaları için saklama süresi belirlenir; süre dolunca silinir ya da anonim hale getirilir.")]},
 {"id": "mt_msg_consent", "label": "Ticari İleti Onayı (WhatsApp, Instagram, Messenger)", "en": "Commercial Message Consent", "type": "multiselect", "showIf": SV("whatsapp", "page", "instagram"),
  "explanation": "Meta kanallarından gönderilecek kampanya ve duyuru mesajlarının onay kurallarını belirler. 6563 sayılı Kanun ticari elektronik iletiyi geniş tanımlar ve önceden onay ister; WhatsApp'ın kendi politikası da onay (opt-in) şartı koyar.",
  "scenario": "WhatsApp'tan kampanya, hatırlatma ya da duyuru gönderecek her işletme; yalnız gelen mesajlara yanıt veriliyorsa da ret ve kayıt kuralları seçilir.",
  "example": "Sitedeki formda “WhatsApp üzerinden kampanya mesajı almak istiyorum” kutusu ayrıdır ve işaretsiz gelir; onay tarihi ve metni CRM'e yazılır.",
  "rule": "Meta kanallarında ticari ileti kuralları: {labels}.",
  "options": [
   o("prior_consent", "Pazarlama mesajı için önceden onay", "Kampanya ve tanıtım mesajı yalnız kişinin önceden, ayrı bir onayla kabul ettiği kanala gönderilir.", "WhatsApp'tan pazarlama mesajı gönderecek her işletme.", "Formda işaretsiz gelen ayrı onay kutusu.",
     "WhatsApp, Instagram ve Messenger'dan kampanya ve tanıtım mesajı yalnız kişinin önceden verdiği, kanal adını içeren ayrı onayla gönderilir; onay kutusu işaretsiz gelir."),
   o("iys", "İYS ve hukuki teyit", "SMS, e-posta ve arama onayları İleti Yönetim Sistemi'ne (İYS) kaydedilir; WhatsApp gibi kanalların İYS kapsamı hukuk birimiyle teyit edilir.", "Türkiye'de tüketicilere ticari ileti gönderen işletmeler.", "Hukuk birimi WhatsApp kampanya mesajları için onay ve İYS yaklaşımını yazılı olarak belirler.",
     "Ticari ileti onayları 6563 sayılı Kanun'a göre yönetilir; SMS, e-posta ve arama onayları İYS'ye kaydedilir, WhatsApp ve diğer mesajlaşma kanallarının İYS kapsamı hukuk birimince teyit edilip yazılı hale getirilir."),
   o("record", "Onay kaydı", "Onayın tarihi, kanalı, metni ve kaynağı saklanır; istenince gösterilebilir.", "Onayla mesaj gönderen her işletme.", "CRM'de “WhatsApp pazarlama onayı: 2026-11-12, web formu, metin v3”.",
     "Her onayın tarihi, kanalı, onay metni sürümü ve kaynağı kaydedilir ve onay süresince saklanır."),
   o("optout", "Ret hemen uygulanır", "“DUR”, “İPTAL” ya da sohbet içi ret talebi aynı gün uygulanır; kişi pazarlama listelerinden çıkar.", "Her işletme.", "Kişi “artık mesaj istemiyorum” yazınca otomatik yanıt ret kaydını onaylar.",
     "Ret talebi (mesajla, engellemeyle ya da başka kanaldan) aynı gün uygulanır; kişi bütün pazarlama listelerinden ve Meta'ya yüklenen müşteri listelerinden çıkarılır."),
   o("b2b_exception", "Esnaf ve tacirlere gönderim ayrı değerlendirilir", "6563 sayılı Kanun'a göre esnaf ve tacirlere önceden onay alınmadan ileti gönderilebilir; ret hakkı yine tanınır.", "Ağırlıklı olarak işletmelere satış yapan (B2B) firmalar.", "Bayilere giden kampanya mesajında ret seçeneği bulunur.",
     "Esnaf ve tacirlere gönderilecek iletiler için 6563 sayılı Kanun'daki istisna hukuk birimince değerlendirilir; bu iletilerde de ret seçeneği bulunur."),
   o("service_split", "Hizmet ve pazarlama mesajları ayrılır", "Sipariş, randevu, kargo gibi hizmet mesajları ile kampanya mesajları ayrı şablon, ayrı onay ve ayrı ölçümle yürütülür.", "Hem hizmet hem pazarlama mesajı gönderen işletmeler.", "Randevu hatırlatması yardımcı (utility), indirim duyurusu pazarlama şablonudur.",
     "Hizmet mesajları (sipariş, randevu, teslimat, hesap) ile pazarlama mesajları ayrı şablon, ayrı onay ve ayrı raporla yürütülür; hizmet mesajına kampanya içeriği eklenmez.")]}]

# 3 — Meta Pikseli & Conversions API
SECTIONS.append({
 "id": "mt_pixel", "name": "Meta Pikseli & Conversions API", "en": "Meta Pixel & Conversions API", "icon": "◇", "agents": ["O", "API"],
 "refs": ["domain_name", "staging_url", "mk_ids"],
 "desc": "Sitedeki dönüşümlerin Meta'ya nasıl ölçüleceğini belirler: tarayıcıdaki Meta Pikseli, sunucudaki Conversions API, olay tekilleştirme, müşteri bilgisi eşleştirmesi, alan adı doğrulama ve gönderilecek standart olaylar",
 "guide": {
  "purpose": "Meta reklamları hangi reklamın form, randevu ya da satış getirdiğini sitedeki olaylardan öğrenir. Tarayıcıdaki Meta Pikseli reklam engelleyicilerden ve tarayıcı kısıtlarından etkilenir; Conversions API aynı olayları sunucudan gönderir. İkisi birlikte kurulur, aynı olay kimliğiyle tekilleştirilir ve Meta'nın Events Manager ekranında tek veri kümesinde (dataset) görünür. Bu bölüm kurulum yöntemini, asgari ayarları ve gönderilecek olayları belirler.",
  "criteria": [
   "Piksel ve Conversions API aynı veri kümesine gönderir; aynı olay tarayıcıdan ve sunucudan aynı olay adı ve olay kimliğiyle gelir, Meta tek sayar.",
   "Olay adları Meta'nın standart olaylarıdır (Lead, Contact, Schedule, Purchase …); özel olay yalnız standart karşılığı yoksa kullanılır.",
   "Müşteri bilgisi parametreleri yalnız onay varken, normalize edilip SHA-256 ile karma yapılarak gönderilir.",
   "Kurulum Test Olayları (Test Events) ekranında doğrulanır; test ortamı canlı veri kümesine veri göndermez."],
  "pitfalls": [
   "Pikseli hem kodla hem bir eklentiyle iki kez yüklemek: her olay iki kez sayılır, reklam optimizasyonu bozulur.",
   "Conversions API'yi olay kimliği olmadan kurmak: tarayıcı ve sunucu olayları tekilleşmez, dönüşümler iki kat görünür.",
   "Form adresine e-posta ya da telefonu sorgu parametresi olarak koymak: düz metin kişisel veri piksel üzerinden Meta'ya gider.",
   "Conversions API erişim jetonunu ön yüze ya da depoya yazmak: jetonla herkes veri kümesine sahte olay gönderebilir."],
  "resources": [
   r("Meta Pikseli — standart olaylar referansı", "https://developers.facebook.com/docs/meta-pixel/reference", "Lead, Contact, Schedule, Purchase gibi standart olaylar ve parametreleri."),
   r("Piksel ve sunucu olaylarının tekilleştirilmesi", "https://developers.facebook.com/documentation/ads-commerce/conversions-api/deduplicate-pixel-and-server-events", "eventID / event_id ve olay adı eşleşmesi; 48 saatlik tekilleştirme."),
   r("Conversions API — müşteri bilgisi parametreleri", "https://developers.facebook.com/docs/marketing-api/conversions-api/parameters/customer-information-parameters", "em, ph, fn … SHA-256 ve normalizasyon; fbp, fbc, IP ve tarayıcı bilgisi karma yapılmaz."),
   r("Conversions API Gateway", "https://developers.facebook.com/documentation/ads-commerce/gateway-products/conversions-api-gateway", "Kendi bulut hesabınızda kodsuz sunucu taraflı gönderim."),
   r("Alan adı doğrulama (geliştirici belgesi)", "https://developers.facebook.com/docs/sharing/domain-verification", "DNS TXT kaydı ya da HTML dosyasıyla alan adı sahipliği."),
   r("Alan adı doğrulama (Yardım Merkezi)", "https://www.facebook.com/business/help/286768115176155", "İşletme ayarlarında alan adını doğrulama adımları."),
   r("Toplu Olay Ölçümü hakkında", "https://www.facebook.com/business/help/721422165168355", "Meta'nın olay ölçümü ve önceliklendirme yaklaşımı.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_px_method", "label": "Kurulum Yöntemi", "en": "Implementation Method", "type": "select", "showIf": SV("pixel"),
  "explanation": "Meta Pikseli ve Conversions API'nin nasıl kurulacağını belirler.",
  "scenario": "Kendi kodu olan sitelerde Piksel + kendi sunucusundan Conversions API önerilir; hazır e-ticaret platformunda platformun resmî Meta entegrasyonu, kod yazmadan sunucu taraflı gönderim isteyenlerde Conversions API Gateway seçilir.",
  "example": "Form gönderilince sunucu kaydı oluşturur, aynı olay kimliğiyle hem tarayıcıya fbq('track','Lead',{},{eventID}) hem Conversions API'ye Lead gönderir.",
  "rule": "Meta ölçüm kurulum yöntemi: {label}.",
  "options": [
   o("server", "Piksel + kendi sunucumuzdan Conversions API (önerilen)", "Piksel tarayıcıda, Conversions API sitenin sunucusunda çalışır; olay kimliğini sunucu üretir.", "Kendi kodu olan ve form / sipariş kaydı sunucuda oluşan siteler.", "Sunucu Lead kaydını oluşturur, olay kimliğini sayfaya da verir.",
     "Piksel tarayıcıda, Conversions API sitenin sunucusunda kurulur; olay kimliğini sunucu üretir ve iki kanala aynı olay adı ve kimliğiyle gönderir; erişim jetonu yalnız sunucudadır."),
   o("gateway", "Piksel + Conversions API Gateway", "Meta'nın kendi bulut hesabınızda (AWS ya da Google Cloud) çalışan, piksel olaylarını kodsuz sunucu taraflı ileten aracıdır.", "Kod değişikliği istemeyen, bulut hesabı olan işletmeler.", "Gateway alt alan adında çalışır, olay kimliğini kendisi üretir.",
     "Conversions API Gateway kurumun bulut hesabında kurulur; piksel olayları Gateway üzerinden sunucu taraflı iletilir, Gateway'in bakım ve maliyet sorumlusu belirlenir."),
   o("partner", "Platformun resmî Meta entegrasyonu", "Shopify, WooCommerce, Ticimax, İdeasoft gibi platformların resmî Meta uygulaması piksel ve Conversions API'yi birlikte kurar.", "Hazır e-ticaret ya da site platformu kullananlar.", "Platformun Meta uygulamasında veri paylaşımı “En yüksek” seçilir.",
     "Piksel ve Conversions API platformun resmî Meta entegrasyonuyla kurulur; sitede ayrıca elle piksel kodu eklenmez, çift gönderim olmadığı Test Olayları'nda doğrulanır."),
   o("sgtm", "Sunucu taraflı Etiket Yöneticisi üzerinden", "Google Tag Manager'ın sunucu kapsayıcısı Meta Conversions API etiketiyle olayları iletir.", "Sunucu taraflı Tag Manager'ı zaten kullanan siteler.", "Web kapsayıcısı olayı sunucu kapsayıcısına, o da Meta'ya gönderir.",
     "Olaylar sunucu taraflı Etiket Yöneticisi kapsayıcısındaki Meta Conversions API etiketiyle gönderilir; olay kimliği web ve sunucu kapsayıcısında aynıdır."),
   o("pixel_only", "Yalnız Meta Pikseli", "Yalnız tarayıcı tarafı ölçüm. En kolayıdır ama reklam engelleyici ve tarayıcı kısıtlarında dönüşümlerin bir kısmı kaybolur.", "Küçük bütçeli, sunucu entegrasyonu yapılamayan siteler; sonradan Conversions API eklenmek üzere.", "Yalnız fbq('track','Lead').",
     "Yalnız Meta Pikseli kurulur; dönüşüm kaybı kabul edilir ve Conversions API ileride eklenecek iş olarak kayda geçirilir.")]},
 {"id": "mt_px_settings", "label": "Asgari Ölçüm Ayarları", "en": "Minimum Measurement Settings", "type": "multiselect", "showIf": SV("pixel"),
  "explanation": "Piksel ve Conversions API kurulumunda yapılacak asgari ayarları belirler.",
  "scenario": "Tekilleştirme, karma yapma, alan adı doğrulama ve Test Olayları her kurulumda seçilir; diğerleri sitenin yapısına göre eklenir.",
  "example": "Events Manager'da veri kümesi, doğrulanmış alan adı, izinli alan adları listesi ve olay eşleşme kalitesi görünür.",
  "rule": "Meta Pikseli ve Conversions API ayarları: {labels}.",
  "options": [
   o("dedup", "Olay tekilleştirme (event_id)", "Tarayıcı ve sunucu olayı aynı olay adı ve aynı olay kimliğiyle gönderilir; Meta 48 saat içinde gelen eşleri tek sayar.", "Piksel ve Conversions API birlikte kullanılıyorsa.", "eventID “lead-8f3c2” iki kanalda aynı.",
     "Her olay tarayıcıda eventID, sunucuda event_id olarak aynı benzersiz kimlik ve aynı olay adıyla gönderilir."),
   o("hashing", "Müşteri bilgisi normalize + SHA-256", "E-posta küçük harfe çevrilip boşluklar atılır; telefon yalnız rakam ve ülke koduyla yazılır; sonra SHA-256 ile karma yapılır. fbp, fbc, IP ve tarayıcı bilgisi karma yapılmaz.", "Conversions API ya da gelişmiş eşleştirme kullanılıyorsa.", "ph: 905321234567 → SHA-256.",
     "Müşteri bilgisi parametreleri (em, ph, fn, ln, ct, zp, country, external_id) Meta'nın belgelediği şekilde normalize edilip SHA-256 ile karma yapılır; fbp, fbc, client_ip_address ve client_user_agent karma yapılmadan, yalnız onay varken gönderilir."),
   o("domain", "Alan adı doğrulama", "Alan adının kuruma ait olduğu DNS TXT kaydı ya da HTML dosyasıyla doğrulanır; bağlantı önizlemelerini kimin düzenleyeceği de buna bağlıdır.", "Kendi alan adı olan her site.", "DNS'te facebook-domain-verification=… TXT kaydı.",
     "Alan adı kurumun işletme portföyünde DNS TXT kaydı ya da HTML dosyasıyla doğrulanır; kayıt silinmez."),
   o("test_events", "Test Olayları ile doğrulama", "Kurulum Events Manager'ın Test Olayları ekranında test koduyla denenir.", "Her kurulum.", "Test ekranında Lead olayı “Tarayıcı” ve “Sunucu” olarak tekilleşmiş görünür.",
     "Her olay Events Manager › Test Olayları'nda test koduyla denenir; test kodu canlıya alınmadan kaldırılır."),
   o("emq", "Olay eşleşme kalitesi izlenir", "Events Manager'daki eşleşme kalitesi ve olay kapsaması düzenli kontrol edilir.", "Conversions API kullanılan siteler.", "Lead olayında eşleşme kalitesi 6/10'dan 8/10'a çıkar.",
     "Events Manager'daki olay eşleşme kalitesi ve tarayıcı / sunucu kapsaması ayda bir kontrol edilir; düşüşte eksik parametre araştırılır."),
   o("traffic", "İzinli alan adları (trafik izinleri)", "Veri kümesine yalnız kurumun alan adlarından olay kabul edilir; başka sitelerden gelen sahte olaylar engellenir.", "Piksel kimliği kaynak kodda göründüğü için her site.", "İzin listesinde yalnız ornek.com ve alt alan adları.",
     "Veri kümesinin trafik izinlerinde yalnız kurumun alan adları izin listesindedir."),
   o("no_pii_url", "Adreste ve parametrede kişisel veri yok", "Form sonrası adreslerde, sorgu parametrelerinde ve özel parametrelerde ad, e-posta, telefon bulunmaz.", "Her site.", "Teşekkür sayfası /tesekkurler, ?email= yok.",
     "Form ve sipariş sonrası sayfa adreslerinde, sorgu parametrelerinde ve özel olay parametrelerinde kişisel veri bulunmaz."),
   o("staging_off", "Test ortamında kapalı ya da ayrı veri kümesi", "Test ortamı canlı veri kümesine olay göndermez.", "Test ortamı olan projeler.", "Test ortamında META_PIXEL_ID boş.",
     "Test ortamında piksel ve Conversions API kapalıdır ya da ayrı bir test veri kümesi kullanılır.")]},
 {"id": "mt_px_events", "label": "Gönderilecek Standart Olaylar", "en": "Standard Events to Send", "type": "multiselect", "showIf": SV("pixel"),
  "explanation": "Sitedeki hangi işlemlerin hangi Meta standart olayıyla gönderileceğini belirler. PageView piksel yüklenince kendiliğinden gönderilir.",
  "scenario": "Hizmet sitelerinde Lead ve Contact, randevulu işletmelerde Schedule, e-ticarette ViewContent, AddToCart, InitiateCheckout ve Purchase seçilir.",
  "example": "İletişim formu gönderilince Lead, WhatsApp düğmesine basılınca Contact, sipariş tamamlanınca değer ve para birimiyle Purchase gider.",
  "rule": "Meta'ya gönderilecek standart olaylar: {labels}. Olaylar işlem gerçekten tamamlanınca (form sunucuda kaydedilince, ödeme onaylanınca) gönderilir.",
  "recommend": [
   {"field": "mk_conversions", "map": {"form": ["lead"], "phone": ["contact"], "whatsapp": ["contact"], "email": ["contact"], "purchase": ["view_content", "add_to_cart", "initiate_checkout", "purchase"], "event_register": ["complete_registration"]}},
   {"field": "modules_extra", "map": {"ecommerce": ["view_content", "add_to_cart", "initiate_checkout", "purchase", "search"], "booking": ["schedule"], "lms": ["complete_registration", "purchase"]}}],
  "options": [
   o("lead", "Lead — form gönderimi", "Teklif, iletişim ya da başvuru formu başarıyla gönderilince.", "Form toplayan her site.", "Teklif formu kaydedilince Lead.", "Lead olayı form sunucuda başarıyla kaydedilince gönderilir; form türü content_name ile belirtilir."),
   o("contact", "Contact — telefon, WhatsApp, e-posta tıklaması", "Telefon, WhatsApp ya da e-posta bağlantısına tıklanınca.", "Arama ve mesajla iletişim alan işletmeler.", "WhatsApp düğmesine basılınca Contact.", "Contact olayı telefon, WhatsApp ve e-posta bağlantılarına tıklanınca gönderilir; kanal özel parametreyle ayrılır."),
   o("schedule", "Schedule — randevu", "Randevu oluşturulunca.", "Klinik, salon, danışmanlık gibi randevulu işletmeler.", "Randevu onaylanınca Schedule.", "Schedule olayı randevu kaydı oluşunca gönderilir."),
   o("complete_registration", "CompleteRegistration — kayıt", "Üyelik, etkinlik ya da eğitim kaydı tamamlanınca.", "Üyelik ya da etkinlik kaydı olan siteler.", "Webinar kaydı tamamlanınca.", "CompleteRegistration olayı kayıt tamamlanınca gönderilir."),
   o("submit_application", "SubmitApplication — başvuru", "Kredi, iş, üyelik ya da program başvurusu gönderilince.", "Başvuru alan siteler.", "Bayilik başvurusu gönderilince.", "SubmitApplication olayı başvuru kaydedilince gönderilir."),
   o("view_content", "ViewContent — ürün / hizmet sayfası", "Ürün ya da hizmet detay sayfası görüntülenince; katalogda ürün kimliğiyle.", "E-ticaret ve katalog reklamı verenler.", "Ürün sayfasında content_ids ile ViewContent.", "ViewContent olayı ürün ya da hizmet sayfasında content_ids, content_type, value ve currency ile gönderilir."),
   o("search", "Search — site içi arama", "Site içinde arama yapılınca.", "Arama kutusu olan e-ticaret ve katalog siteleri.", "“siyah çanta” araması search_string ile.", "Search olayı site içi aramada search_string ile gönderilir."),
   o("add_to_cart", "AddToCart — sepete ekleme", "Ürün sepete eklenince.", "E-ticaret.", "Sepete eklemede content_ids, value, currency.", "AddToCart olayı sepete eklemede content_ids, value ve currency ile gönderilir."),
   o("initiate_checkout", "InitiateCheckout — ödeme başlangıcı", "Ödeme adımı başlayınca.", "E-ticaret.", "Ödeme sayfası açılınca.", "InitiateCheckout olayı ödeme adımı başlayınca gönderilir."),
   o("purchase", "Purchase — satın alma", "Ödeme onaylanınca; değer ve para birimiyle.", "Online satış yapan siteler.", "Sipariş onayında value: 1250, currency: TRY.", "Purchase olayı ödeme onaylanınca value, currency ve content_ids ile, sipariş numarasından türetilen olay kimliğiyle bir kez gönderilir."),
   o("subscribe", "Subscribe — ücretli abonelik", "Ücretli abonelik başlayınca (bülten kaydı değil).", "Abonelik satan siteler.", "Aylık plan başlayınca.", "Subscribe olayı ücretli abonelik başlayınca value ve currency ile gönderilir.")]}]

# 4 — Facebook Sayfası
SECTIONS.append({
 "id": "mt_page", "name": "Facebook Sayfası", "en": "Facebook Page", "icon": "▣", "agents": ["FB", "S"],
 "refs": ["mk_brand_name", "oc_tagline", "domain_name", "oc_phone", "oc_whatsapp", "oc_address", "oc_hours", "mk_accounts"],
 "desc": "İşletmenin Facebook Sayfasının asgari profil ayarlarını, erişimini, moderasyonunu ve Messenger üzerinden gelen mesajların nasıl yanıtlanacağını belirler",
 "guide": {
  "purpose": "Facebook Sayfası işletmenin Facebook'taki kimliğidir; Meta reklamları, Messenger ve WhatsApp'a tıklama reklamları bir Sayfa adına yayınlanır. Bu bölüm Sayfanın Ortak Bilgiler'le tutarlı profilini, erişimini ve gelen mesajların yönetimini belirler.",
  "criteria": [
   "Sayfa adı, kullanıcı adı, kategori, telefon, adres, çalışma saatleri ve site adresi Ortak Bilgiler'le birebir aynıdır.",
   "Sayfa kurumun işletme portföyündedir; tam kontrollü en az iki kişi vardır.",
   "Eylem düğmesi işletmenin ana dönüşümüne (WhatsApp, arama, randevu, site) gider.",
   "Gelen mesajlar tek gelen kutusundan, tanımlı yanıt süresiyle yanıtlanır."],
  "pitfalls": [
   "Kişisel profili işletme gibi kullanmak: reklam verilemez, istatistik ve erişim yönetimi yoktur.",
   "Çalışma saatlerini ve telefonu sitede güncelleyip Sayfada unutmak.",
   "Mesajlara günlerce yanıt vermemek: müşteri kaybolur, Sayfada yanıt süresi kötü görünür.",
   "Yorumlardaki hakaret ve spam'i elle takip etmeye çalışmak: moderasyon filtreleri kurulmalıdır."],
  "resources": [
   r("İşletmeniz için Facebook Sayfası oluşturma", "https://www.facebook.com/business/help/473994396650734", "Meta Yardım Merkezi: Sayfa oluşturma adımları."),
   r("Sayfa erişimi: Facebook erişimi ve görev erişimi", "https://www.messenger.com/help/289207354498410", "Tam / kısmi kontrol ve Business Suite üzerinden görev erişimi."),
   r("Yeni Sayfa deneyimi", "https://creators.facebook.com/new-pages-experience/", "Beğeni yerine takipçi, yeni yönetim yapısı."),
   r("Messenger Platformu", "https://developers.facebook.com/docs/messenger-platform/overview", "Sayfa ve Instagram mesajlarına otomatik ya da canlı temsilciyle yanıt.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_page_settings", "label": "Asgari Sayfa Ayarları", "en": "Minimum Page Settings", "type": "multiselect", "showIf": SV("page"),
  "explanation": "Facebook Sayfasında yapılacak asgari profil ve yönetim ayarlarını belirler.",
  "scenario": "Kategori, kullanıcı adı, iletişim bilgileri, eylem düğmesi ve erişim her Sayfada seçilir; moderasyon ve bağlı hesaplar eklenir.",
  "example": "Sayfada logo, kapak, “WhatsApp'tan yaz” düğmesi, çalışma saatleri ve Instagram bağlantısı görünür.",
  "rule": "Facebook Sayfası ayarları: {labels}.",
  "options": [
   o("identity", "Ad, kullanıcı adı ve kategori", "Sayfa adı marka adıyla, kullanıcı adı diğer hesaplarla aynı; kategori işletmenin asıl işi.", "Her Sayfa.", "facebook.com/ornekklinik, kategori “Diş Hekimi”.", "Sayfa adı marka adıyla aynıdır; kullanıcı adı diğer sosyal hesaplarla tutarlıdır; kategori işletmenin asıl işini anlatır."),
   o("contact", "İletişim, adres ve çalışma saatleri", "Telefon, WhatsApp, e-posta, adres, saatler ve site adresi Ortak Bilgiler'den aynen girilir.", "Her Sayfa.", "Saatler Ortak Bilgiler'deki tabloyla aynı.", "Sayfadaki telefon, WhatsApp, e-posta, adres, çalışma saatleri ve site adresi Ortak Bilgiler'le birebir aynıdır ve değişiklikte aynı gün güncellenir."),
   o("visuals", "Profil ve kapak görseli", "Profilde logo, kapakta güncel kampanya ya da marka görseli; mobilde kırpılmayacak şekilde.", "Her Sayfa.", "Logo kare, kapak 16:9 güvenli alanla.", "Profil görseli logo, kapak görseli mobilde kırpılmayacak güvenli alanla hazırlanır."),
   o("cta", "Eylem düğmesi", "Sayfanın ana düğmesi (WhatsApp, Ara, Randevu al, Siteyi ziyaret et) işletmenin ana dönüşümüne gider.", "Her Sayfa.", "“WhatsApp'tan mesaj gönder” düğmesi.", "Sayfanın eylem düğmesi işletmenin ana dönüşümüne yönlenir; bağlantı UTM parametresiyle verilir."),
   o("about", "Hakkında ve site bağlantısı", "Kısa tanıtım ve site bağlantısı Ortak Bilgiler'deki kısa tanıtımla tutarlıdır.", "Her Sayfa.", "Hakkında: tek cümlelik tanıtım + site.", "Hakkında alanında Ortak Bilgiler'deki kısa tanıtım ve UTM'li site bağlantısı bulunur."),
   o("access", "Erişim portföyden", "Sayfa kurumun portföyündedir; tam kontrol en az iki kişide, diğerleri görev erişimiyle.", "Her Sayfa.", "İçerik ekibi yalnız içerik ve mesaj görevinde.", "Sayfa kurumun işletme portföyüne bağlıdır; tam kontrol en az iki kurum çalışanındadır, diğer kişiler yalnız görev erişimi alır."),
   o("moderation", "Moderasyon filtreleri", "Küfür filtresi ve engellenecek kelime listesi açılır; spam ve hakaret otomatik gizlenir.", "Yorum alan her Sayfa.", "Rakip adı ve küfürler içeren yorumlar gizlenir.", "Sayfada küfür filtresi ve engellenen kelime listesi açıktır; gizlenen yorumlar haftalık kontrol edilir."),
   o("linked", "Instagram ve WhatsApp bağlantısı", "Instagram hesabı ve WhatsApp numarası Sayfaya bağlanır; reklam ve tek gelen kutusu için gerekir.", "Instagram ya da WhatsApp kullanan işletmeler.", "Sayfa ayarlarında bağlı hesaplar listelenir.", "Instagram profesyonel hesabı ve WhatsApp Business numarası Sayfaya bağlanır.")]},
 {"id": "mt_page_inbox", "label": "Mesaj Yönetimi (Messenger ve Gelen Kutusu)", "en": "Messaging & Inbox", "type": "multiselect", "showIf": SV("page", "instagram"),
  "explanation": "Facebook Sayfası ve Instagram'a gelen mesajların nasıl yanıtlanacağını belirler.",
  "scenario": "Tek gelen kutusu, anında yanıt ve yanıt süresi hedefi her işletmede seçilir; yoğun mesaj alanlarda kayıtlı yanıtlar, CRM'e aktarım ve canlı temsilciye devir eklenir.",
  "example": "Business Suite gelen kutusunda Messenger ve Instagram mesajları birlikte görünür; mesai dışında otomatik yanıt çalışma saatlerini söyler.",
  "rule": "Meta mesajlarının yönetimi: {labels}.",
  "options": [
   o("inbox", "Tek gelen kutusu", "Messenger, Instagram (ve bağlıysa WhatsApp) mesajları Business Suite gelen kutusunda ya da destek yazılımında toplanır.", "Mesaj alan her işletme.", "Ekip mesajları tek ekrandan görür ve birbirine atar.", "Messenger ve Instagram mesajları tek gelen kutusunda toplanır; mesajlar kişiye atanır ve yanıtlanmamış mesaj kalmaz."),
   o("auto_reply", "Anında yanıt ve mesai dışı mesajı", "İlk mesaja otomatik karşılama, mesai dışında çalışma saatlerini bildiren yanıt.", "Her işletme.", "“Merhaba, 09:00–18:00 arasında yanıtlıyoruz.”", "İlk mesaja otomatik karşılama, mesai dışında çalışma saatlerini ve acil iletişim yolunu bildiren yanıt gönderilir."),
   o("saved", "Kayıtlı yanıtlar ve sık sorulanlar", "Fiyat, adres, randevu gibi sık sorulara onaylı hazır yanıtlar.", "Sık aynı soruyu alan işletmeler.", "“Adres ve yol tarifi” kayıtlı yanıtı.", "Sık sorulan sorular için pazarlama ve hukuk onaylı kayıtlı yanıtlar kullanılır."),
   o("sla", "Yanıt süresi hedefi", "Mesai içinde mesajlar belirlenen sürede yanıtlanır.", "Her işletme.", "Mesai içi en geç 1 saat.", "Mesai içinde mesajlar en geç belirlenen sürede (ör. 1 saat) yanıtlanır; süre aylık raporlanır."),
   o("handoff", "Otomasyondan temsilciye devir", "Bot ya da otomatik akış çözemediğinde sohbet canlı temsilciye devredilir.", "Otomatik mesaj akışı kullananlar.", "“Temsilciye bağlan” seçeneği.", "Otomatik akışta her adımda canlı temsilciye geçiş seçeneği vardır; devir sohbet geçmişiyle yapılır."),
   o("crm", "Mesajdan gelen talepler CRM'e", "Teklif ve randevu talepleri CRM'e kaynağıyla kaydedilir.", "Satış takibi yapılan işletmeler.", "CRM'de kaynak: Instagram DM.", "Mesajdan gelen teklif ve randevu talepleri CRM'e kaynak kanalıyla kaydedilir."),
   o("no_sensitive", "Mesajla hassas veri istenmez", "Kart bilgisi, T.C. kimlik numarası, sağlık bilgisi mesajla istenmez; güvenli forma yönlendirilir.", "Her işletme.", "“Ödeme için güvenli bağlantıyı kullanın.”", "Mesaj kanallarında kart bilgisi, T.C. kimlik numarası ya da sağlık bilgisi istenmez; gerekirse güvenli forma yönlendirilir.")]}]

# 5 — Instagram
SECTIONS.append({
 "id": "mt_ig", "name": "Instagram Profesyonel Hesap", "en": "Instagram Professional Account", "icon": "◍", "agents": ["IG", "S"],
 "refs": ["mk_brand_name", "oc_tagline", "domain_name", "mk_accounts"],
 "desc": "Instagram hesabının türünü, işletme portföyüne ve Facebook Sayfasına bağlantısını, asgari profil ve güvenlik ayarlarını ve sitede Instagram verisi kullanılacaksa API yöntemini belirler",
 "guide": {
  "purpose": "Instagram'da istatistik, iletişim düğmeleri, reklam ve API erişimi profesyonel hesapla gelir. Hesabın işletme portföyüne ve Facebook Sayfasına bağlanması reklamlar, ürün etiketleri ve bazı API özellikleri için gerekir. Sitede Instagram akışı gösterilecekse eski Basic Display API 4 Aralık 2024'te kapandığı için güncel Instagram API yöntemi seçilmelidir.",
  "criteria": [
   "Hesap profesyonel hesaptır ve kurumun işletme portföyündedir; şifre paylaşılmaz, erişim portföyden verilir.",
   "Kullanıcı adı, biyografi, iletişim düğmeleri ve bağlantılar Ortak Bilgiler'le tutarlıdır; bağlantılar UTM'lidir.",
   "İki faktörlü doğrulama açıktır.",
   "Sitede Instagram verisi kullanılıyorsa güncel Instagram API'si ve sistem kullanıcısı / uzun ömürlü jetonla çalışılır."],
  "pitfalls": [
   "Hesap şifresini ajansla paylaşmak: şifre değiştirilince erişim kopar, güvenlik kaydı tutulamaz.",
   "Sitede Basic Display API kullanan eski bir eklentiyle Instagram akışı göstermeye çalışmak: 4 Aralık 2024'ten beri çalışmaz.",
   "Biyografi bağlantısını UTM'siz vermek: Instagram'dan gelen ziyaretçiler analitikte “direct” görünür.",
   "Yorum filtrelerini açmamak: spam ve hakaret yorumları markayı yıpratır."],
  "resources": [
   r("Instagram Platform — genel bakış", "https://developers.facebook.com/docs/instagram-platform/overview", "Instagram Login ile ve Facebook Login ile Instagram API farkları."),
   r("Instagram Basic Display API'nin kapanması", "https://developers.facebook.com/blog/post/2024/09/04/update-on-instagram-basic-display-api", "4 Aralık 2024'te kapandı; yerine Instagram API."),
   r("Ticaret uygunluk gereklilikleri", "https://www.facebook.com/business/help/2347002662267537", "Ürün etiketleri ve alışveriş özelliklerinin uygunluk şartları."),
   r("Threads API — genel bakış", "https://developers.facebook.com/documentation/threads/overview", "Threads'te içerik yayınlama API'si (isteğe bağlı kanal).")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_ig_type", "label": "Hesap Türü", "en": "Account Type", "type": "select", "showIf": SV("instagram"),
  "explanation": "Instagram hesabının işletme mi içerik üreticisi mi olacağını belirler. İkisi de profesyonel hesaptır; işletme hesabı iletişim düğmeleri, entegrasyonlar ve API için genellikle daha uygundur.",
  "scenario": "Kurumlar, mağazalar ve hizmet işletmeleri işletme hesabı; kişisel marka, yazar ya da etkileyici (influencer) içerik üreticisi hesabı seçer.",
  "example": "Bir klinik işletme hesabıyla “Ara”, “Yol tarifi” ve “Mesaj” düğmelerini kullanır.",
  "rule": "Instagram hesap türü: {label}.",
  "options": [
   o("business", "İşletme hesabı (önerilen)", "Kurumlar için profesyonel hesap; iletişim düğmeleri, kategori, entegrasyonlar ve API erişimi.", "Kurumsal markalar, mağazalar, hizmet işletmeleri.", "Profilde kategori ve iletişim düğmeleri.",
     "Instagram hesabı işletme türünde profesyonel hesaptır."),
   o("creator", "İçerik üreticisi hesabı", "Kişisel marka ve içerik üreticileri için profesyonel hesap; bazı entegrasyonlar işletme hesabındaki kadar geniş değildir.", "Kişisel marka, uzman, yazar, etkileyici.", "Profilde “Dijital içerik üreticisi” kategorisi.",
     "Instagram hesabı içerik üreticisi türünde profesyonel hesaptır; gereken entegrasyonun bu hesap türünü desteklediği kurulumdan önce kontrol edilir.")]},
 {"id": "mt_ig_settings", "label": "Asgari Instagram Ayarları", "en": "Minimum Instagram Settings", "type": "multiselect", "showIf": SV("instagram"),
  "explanation": "Instagram profesyonel hesabında yapılacak asgari ayarları belirler.",
  "scenario": "Portföy bağlantısı, iki faktörlü doğrulama, profil ve bağlantılar her hesapta seçilir; yorum filtreleri ve Threads isteğe göre eklenir.",
  "example": "Biyografide kısa tanıtım ve UTM'li beş bağlantı, profilde “Ara” ve “WhatsApp” düğmeleri.",
  "rule": "Instagram ayarları: {labels}.",
  "options": [
   o("portfolio", "İşletme portföyüne ve Sayfaya bağlı", "Hesap kurumun portföyüne eklenir ve Facebook Sayfasına bağlanır; reklam, ürün etiketleri ve tek gelen kutusu için gerekir.", "Reklam veren ya da ekiple yönetilen hesaplar.", "Portföyde Instagram hesabı varlık olarak görünür.", "Instagram hesabı kurumun işletme portföyüne eklenir ve Facebook Sayfasına bağlanır; erişim portföyden verilir, şifre paylaşılmaz."),
   o("2fa", "İki faktörlü doğrulama", "Hesapta doğrulama uygulamasıyla iki faktörlü doğrulama açılır, yedek kodlar güvenli yerde saklanır.", "Her hesap.", "Doğrulama uygulaması açık, yedek kodlar parola kasasında.", "Instagram hesabında doğrulama uygulamasıyla iki faktörlü doğrulama açıktır; yedek kodlar kurumun parola kasasında saklanır."),
   o("profile", "Profil: ad, kategori, biyografi", "Ad ve kullanıcı adı marka adıyla, biyografi kısa tanıtımla tutarlı; kategori asıl iş.", "Her hesap.", "@ornekklinik · Diş Hekimi · tek cümle tanıtım.", "Instagram adı, kullanıcı adı, kategori ve biyografi Ortak Bilgiler'deki marka adı ve kısa tanıtımla tutarlıdır."),
   o("contact", "İletişim düğmeleri", "Telefon, e-posta, adres ve WhatsApp düğmeleri Ortak Bilgiler'deki bilgilerle.", "Müşteriyle doğrudan iletişim isteyen işletmeler.", "“Ara” ve “WhatsApp” düğmeleri.", "Profildeki iletişim düğmeleri Ortak Bilgiler'deki telefon, e-posta, adres ve WhatsApp hattıyla aynıdır."),
   o("links", "Biyografi bağlantıları UTM'li", "Biyografiye en çok beş bağlantı eklenebilir; hepsi UTM parametreli verilir.", "Her hesap.", "?utm_source=instagram&utm_medium=social&utm_campaign=bio", "Biyografi bağlantıları utm_source=instagram ve utm_medium=social parametreleriyle verilir; bağlantılar ayda bir kontrol edilir."),
   o("comments", "Yorum ve mesaj filtreleri", "Gizli kelimeler, saldırgan yorum filtresi ve istenmeyen mesaj filtreleri açılır.", "Etkileşimi yüksek ya da tartışmalı sektörlerdeki hesaplar.", "Küfür ve spam yorumlar otomatik gizlenir.", "Instagram'da gizli kelime listesi ve saldırgan yorum / mesaj filtreleri açıktır."),
   o("insights", "İstatistikler raporlanır", "Erişim, etkileşim, takipçi ve bağlantı tıklamaları aylık rapora girer.", "Her hesap.", "Aylık raporda erişim ve profil ziyaretleri.", "Instagram istatistikleri (erişim, etkileşim, takipçi, bağlantı tıklamaları) aylık pazarlama raporuna eklenir."),
   o("threads", "Threads profili", "Instagram hesabıyla Threads profili açılır; isteğe bağlı metin kanalı.", "Kısa metin paylaşımı ve topluluk etkileşimi isteyen markalar.", "Threads'te aynı kullanıcı adı.", "Threads profili Instagram hesabıyla aynı kullanıcı adıyla açılır ve Ortak Bilgiler › Sosyal Hesap Adresleri'ne yazılır.")]},
 {"id": "mt_ig_api", "label": "Sitede Instagram Verisi (API)", "en": "Instagram Data on Site (API)", "type": "select", "showIf": SV("instagram"),
  "explanation": "Sitede Instagram gönderileri gösterilecek ya da Instagram verisi bir yazılıma çekilecekse hangi API yönteminin kullanılacağını belirler.",
  "scenario": "Sitede Instagram akışı yoksa “Kullanılmayacak”; yalnız gönderi gösterilecekse Instagram Login ile API; ürün etiketleme, hashtag araması ya da iş ortaklığı reklamları gerekiyorsa Facebook Login ile API seçilir.",
  "example": "Ana sayfadaki son 6 gönderi, sunucunun günde bir kez Instagram API'den çektiği ve önbelleğe aldığı veriden çizilir.",
  "rule": "Sitede Instagram verisi: {label}.",
  "options": [
   o("none", "Kullanılmayacak", "Sitede Instagram akışı ya da entegrasyon yok; profil bağlantısı yeterli.", "Çoğu kurumsal site.", "Altbilgide yalnız Instagram simgesi.", "Sitede Instagram API kullanılmaz; yalnız profil bağlantısı verilir."),
   o("ig_login", "Instagram Login ile Instagram API", "Facebook Sayfası bağlantısı gerektirmeyen güncel yöntem; gönderi, yorum ve mesaj yönetimi.", "Sitede kendi gönderilerini gösterecek işletmeler.", "Sunucu günde bir kez son gönderileri çeker.",
     "Instagram verisi Instagram Login ile Instagram API'den sunucu tarafında çekilir ve önbelleğe alınır; jeton yalnız sunucuda tutulur ve süresi dolmadan yenilenir; Basic Display API kullanılmaz."),
   o("fb_login", "Facebook Login ile Instagram API", "Sayfaya bağlı hesap ister; ürün etiketleme, hashtag araması ve iş ortaklığı reklamları gibi ek özellikler bu yöntemle çalışır.", "Ürün etiketi, hashtag araması ya da reklam entegrasyonu gereken projeler.", "Sistem kullanıcısı jetonuyla gönderi ve ürün etiketi yönetimi.",
     "Instagram verisi Facebook Login for Business ile Instagram API'den, sistem kullanıcısı jetonuyla sunucu tarafında çekilir; Basic Display API kullanılmaz."),
   o("tool", "Üçüncü taraf araç / eklenti", "Akış bir hizmet ya da eklentiyle gösterilir.", "Kod yazmak istemeyen küçük siteler.", "Eklentinin Instagram bağlantısı yenilenir.",
     "Instagram akışı güncel Instagram API'yi kullanan bir araçla gösterilir; aracın Basic Display API'ye bağlı olmadığı ve kişisel veri işleme koşulları kurulumdan önce kontrol edilir.")]}]

# 6 — WhatsApp Business
SECTIONS.append({
 "id": "mt_wa", "name": "WhatsApp Business", "en": "WhatsApp Business", "icon": "✆", "agents": ["WA", "CX", "API"],
 "refs": ["oc_whatsapp", "mk_brand_name", "oc_hours", "oc_address", "domain_name", "mk_accounts"],
 "desc": "WhatsApp'ın uygulama mı Cloud API mi olacağını, numara ve profil ayarlarını, şablon ve mesaj kurallarını, ücretlendirmeyi ve sitedeki WhatsApp bağlantılarını belirler",
 "guide": {
  "purpose": "WhatsApp Business iki yolla kullanılır: telefondaki WhatsApp Business uygulaması ya da yazılımla bağlanan WhatsApp Business Platform (Cloud API). Cloud API'de işletmenin başlattığı mesajlar onaylı şablonla gönderilir ve mesaj başına ücretlendirilir (1 Temmuz 2025'ten beri); 1 Ekim 2026'dan beri hizmet mesajlarında da numara başına aylık 1.000 mesaj ücretsizdir, sonrası ücretlidir. Mesaj limitleri işletme portföyü düzeyindedir. Bu bölüm platformu, numara ve profil ayarlarını, mesaj kurallarını ve sitedeki bağlantıları belirler.",
  "criteria": [
   "WhatsApp numarası kuruma aittir, kişisel numara değildir; profil Ortak Bilgiler'le tutarlıdır.",
   "İşletmenin başlattığı mesajlar yalnız onaylı şablonla ve onay (opt-in) alınmış kişilere gönderilir; şablon kategorisi doğrudur.",
   "Cloud API kullanılıyorsa webhook imzası doğrulanır, jeton sunucuda tutulur, numara iki adımlı doğrulama PIN'iyle korunur.",
   "Sitedeki WhatsApp bağlantıları uluslararası biçimdedir ve tıklama dönüşüm olarak ölçülür."],
  "pitfalls": [
   "Kişisel WhatsApp numarasını işletme hattı yapmak: çalışan ayrılınca müşteri yazışmaları ve numara kurumdan gider.",
   "Kampanya içeriğini yardımcı (utility) şablon olarak göndermeye çalışmak: Meta şablonu pazarlama olarak yeniden sınıflandırır, ücret ve limit değişir.",
   "Onay almadan toplu mesaj göndermek: kullanıcılar engeller, kalite düşer, numaranın mesaj limiti kısıtlanır.",
   "1 Ekim 2026 ücret değişikliğini hesaba katmadan pencere içinde yoğun yardımcı mesaj göndermek."],
  "resources": [
   r("WhatsApp Business Platform — fiyatlandırma", DEV + "pricing", "Mesaj başına ücret, ücretsiz giriş noktası ve 2026 değişiklikleri; Türkiye ayrı pazar."),
   r("Şablon kategorileri", DEV + "templates/template-categorization", "Pazarlama, yardımcı ve kimlik doğrulama; karışık içerik pazarlama sayılır."),
   r("WhatsApp Business Messaging Policy", "https://whatsappbusiness.com/policy/", "Onay, ret ve 24 saatlik müşteri hizmet penceresi kuralları."),
   r("Mesaj limitleri", DEV + "messaging-limits", "Limitler işletme portföyü düzeyinde; kademeler ve yükselme koşulları."),
   r("Kullanıcı başına pazarlama mesajı limiti", DEV + "templates/marketing-templates/per-user-limits/", "131049 hatası ve yeniden deneme kuralı."),
   r("Görünen ad", DEV + "display-names", "Görünen adın onayı ve değiştirilme sınırı."),
   r("Resmî işletme hesabı (mavi tik)", DEV + "official-business-accounts", "Başvuru şartları: doğrulanmış portföy, iki adımlı doğrulama, onaylı görünen ad."),
   r("Telefon numaraları", DEV + "business-phone-numbers/phone-numbers", "Numara kaydı ve iki adımlı doğrulama PIN'i."),
   r("Business uygulaması kullanıcılarını Cloud API'ye bağlama (coexistence)", DEV + "embedded-signup/onboarding-business-app-users", "Aynı numarayı uygulamada ve Cloud API'de kullanma; sınırlar."),
   r("Çözüm sağlayıcılar", DEV + "solution-providers/overview/", "Çözüm ortağı ile teknoloji sağlayıcı arasındaki faturalama farkı."),
   r("Webhook uç noktası oluşturma", DEV + "webhooks/create-webhook-endpoint", "X-Hub-Signature-256 ile imza doğrulama."),
   r("On-Premises API'nin kapanması", "https://developers.facebook.com/docs/whatsapp/on-premises/sunset", "Son sürüm 23 Ekim 2025'te sona erdi; Cloud API kullanılır."),
   r("WhatsApp — sohbet bağlantısı (wa.me)", "https://faq.whatsapp.com/5913398998672934", "Numara uluslararası biçimde, ?text= ile hazır mesaj."),
   r("WhatsApp'a tıklama reklamları rehberi", "https://whatsappbusiness.com/blog/click-to-whatsapp-ad-guide/", "Facebook ve Instagram reklamından WhatsApp sohbeti açmak.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_wa_platform", "label": "WhatsApp Platformu", "en": "WhatsApp Platform", "type": "select", "showIf": SV("whatsapp"),
  "explanation": "WhatsApp'ın telefon uygulamasıyla mı, yazılımla bağlanan Cloud API ile mi, ya da ikisiyle birlikte mi kullanılacağını belirler. On-Premises API 23 Ekim 2025'te kapandığı için API seçeneği Cloud API'dir.",
  "scenario": "Az mesaj alan ve birkaç kişinin yanıtladığı işletmeler uygulamayı; CRM, otomatik bildirim, chatbot ya da çok temsilci gerekiyorsa Cloud API'yi; uygulamadaki sohbeti sürdürüp otomasyon da isteyenler birlikte kullanımı (coexistence) seçer.",
  "example": "Randevu hatırlatmaları Cloud API'den yardımcı şablonla otomatik gider; müşteri yanıtlayınca temsilci aynı sohbeti destek yazılımından sürdürür.",
  "rule": "WhatsApp platformu: {label}.",
  "options": [
   o("app", "WhatsApp Business uygulaması", "Telefonda (ve bağlı cihazlarda) çalışan ücretsiz uygulama; profil, katalog, hazır yanıtlar, etiketler.", "Günde az sayıda mesaj alan küçük işletmeler.", "İki çalışan bağlı cihazlardan yanıtlar.",
     "WhatsApp Business uygulaması kurumun numarasıyla kullanılır; uygulama kurum telefonundadır, yazışma yedeği kurumsal hesaba alınır."),
   o("coexistence", "Uygulama + Cloud API aynı numarada (coexistence)", "Aynı numara hem uygulamada hem Cloud API'de çalışır; uygulamadan gönderilenler ücretsiz, API mesajları Cloud API fiyatıyla. Bazı uygulama özellikleri (grup, kaybolan mesaj vb.) desteklenmez; hız ve bağlı cihaz sınırları vardır.", "Uygulamayı bırakmadan otomasyon ve entegrasyon eklemek isteyenler.", "Elle yazışma uygulamadan, sipariş bildirimleri API'den.",
     "Aynı numara WhatsApp Business uygulamasında ve Cloud API'de birlikte kullanılır; desteklenmeyen özellikler ve sınırlar kurulumdan önce kontrol edilir, ücretli API mesajları ayrı raporlanır."),
   o("cloud_bsp", "Cloud API — çözüm ortağı üzerinden", "Meta'nın çözüm ortağı (BSP) kurulum, gelen kutusu ve destek sağlar; faturalama ortağa göre değişir.", "Hazır gelen kutusu ve chatbot aracı isteyen işletmeler.", "Çözüm ortağının panelinde 5 temsilci aynı numaradan yanıtlar.",
     "WhatsApp Cloud API bir Meta çözüm ortağı üzerinden kullanılır; WhatsApp hesabı ve numara kurumun işletme portföyündedir, ortak değişse de numara kurumda kalır."),
   o("cloud_direct", "Cloud API — doğrudan Meta'ya bağlı", "Kurumun kendi yazılımı Cloud API'ye doğrudan bağlanır; ödeme yöntemi kurumun portföyündedir.", "Kendi yazılım ekibi olan, CRM ya da sipariş sistemiyle entegre çalışacak işletmeler.", "Sipariş sistemi kargo bildirimini yardımcı şablonla gönderir.",
     "WhatsApp Cloud API kurumun kendi yazılımından, sistem kullanıcısı jetonuyla doğrudan kullanılır; ödeme yöntemi kurumun işletme portföyündedir.")]},
 {"id": "mt_wa_settings", "label": "Numara, Profil ve Hesap Ayarları", "en": "Number, Profile & Account Settings", "type": "multiselect", "showIf": SV("whatsapp"),
  "explanation": "WhatsApp hattının numara, profil, güvenlik ve hesap ayarlarını belirler.",
  "scenario": "Kurumsal numara, profil ve iki adımlı doğrulama her kurulumda seçilir; Cloud API'de ödeme yöntemi, webhook doğrulaması ve resmî hesap başvurusu eklenir.",
  "example": "Profilde marka adı, kısa açıklama, adres, çalışma saatleri, site ve e-posta; numara iki adımlı doğrulama PIN'iyle korunur.",
  "rule": "WhatsApp hesap ayarları: {labels}.",
  "options": [
   o("number", "Kuruma ait numara", "Kişisel değil, kuruma kayıtlı bir hat; sabit hat ya da sanal numara da olabilir.", "Her kurulum.", "Hat şirket adına kayıtlı.", "WhatsApp hattı kurum adına kayıtlı bir numaradır; kişisel numara kullanılmaz ve numara Ortak Bilgiler › WhatsApp Hattı'yla aynıdır."),
   o("profile", "İşletme profili", "Ad, açıklama, kategori, adres, çalışma saatleri, site ve e-posta Ortak Bilgiler'den.", "Her kurulum.", "Profilde saatler ve site.", "WhatsApp işletme profilindeki ad, açıklama, kategori, adres, çalışma saatleri, site ve e-posta Ortak Bilgiler'le aynıdır."),
   o("display_name", "Görünen ad marka adıyla uyumlu", "Cloud API'de görünen ad Meta onayından geçer; marka adıyla tutarlı olmalı, sık değiştirilmemeli.", "Cloud API kullananlar.", "Görünen ad “Örnek Klinik”.", "WhatsApp görünen adı işletme adıyla tutarlıdır ve Meta onayından geçer; ad sık değiştirilmez."),
   o("pin", "İki adımlı doğrulama PIN'i", "Numara kaydında ve uygulamada iki adımlı doğrulama PIN'i açılır, kurumun parola kasasında saklanır.", "Her kurulum.", "PIN parola kasasında.", "WhatsApp numarasında iki adımlı doğrulama PIN'i açıktır ve kurumun parola kasasında saklanır."),
   o("oba", "Resmî işletme hesabı (mavi tik) başvurusu", "Doğrulanmış portföy, iki adımlı doğrulama ve onaylı görünen adla mavi tik başvurusu yapılır.", "Tanınırlığı olan, sahte hesap riski taşıyan markalar.", "Görünen adın yanında mavi tik.", "Şartlar sağlanınca resmî işletme hesabı (mavi tik) başvurusu yapılır; başvuru sonucu kayda geçirilir."),
   o("payment", "Ödeme yöntemi (Cloud API)", "Cloud API'de ücretli mesajlar için portföye ödeme yöntemi eklenir; 30 Eylül 2026'dan sonra ödeme yöntemi olmayan hesapların hizmet mesajları da teslim edilmez.", "Cloud API kullananlar.", "Kurumsal kart ve fatura bilgileri ekli.", "Cloud API için işletme portföyüne kurumsal ödeme yöntemi ve fatura bilgileri eklenir; aylık WhatsApp maliyeti raporlanır."),
   o("webhook", "Webhook imza doğrulaması (Cloud API)", "Gelen webhook isteklerinin X-Hub-Signature-256 imzası uygulama gizli anahtarıyla doğrulanır.", "Cloud API'yi kendi sunucusuna bağlayanlar.", "İmzası tutmayan istek 401 ile reddedilir.", "WhatsApp webhook'unda her isteğin X-Hub-Signature-256 imzası ham gövde ve uygulama gizli anahtarıyla HMAC-SHA256 olarak doğrulanır; doğrulanmayan istek işlenmez, gizli anahtar yalnız sunucudadır."),
   o("quality", "Kalite ve mesaj limiti izlenir", "Numaranın kalite durumu ve portföyün mesaj limiti düzenli izlenir; düşüşte kampanya durdurulur.", "Şablonla toplu mesaj gönderenler.", "Kalite düşünce pazarlama gönderimi durdurulur.", "WhatsApp numarasının kalite durumu ve işletme portföyünün mesaj limiti haftalık izlenir; kalite düşerse pazarlama gönderimi durdurulup neden araştırılır."),
   o("catalog", "WhatsApp kataloğu", "Ürün ya da hizmetler WhatsApp'ta katalog olarak gösterilir; Meta kataloğuyla bağlanabilir.", "Ürün ya da paket satan işletmeler.", "Sohbette katalog düğmesi.", "WhatsApp kataloğu Meta kataloğuyla bağlanır; fiyat ve stok sitedekiyle aynı tutulur.")]},
 {"id": "mt_wa_messaging", "label": "Mesaj ve Şablon Kuralları", "en": "Messaging & Template Rules", "type": "multiselect", "showIf": SV("whatsapp"),
  "explanation": "WhatsApp'ta mesaj gönderme, şablon, otomatik yanıt ve maliyet kurallarını belirler.",
  "scenario": "24 saat penceresi, şablon kategorisi ve ret kuralları Cloud API'de her kurulumda seçilir; uygulama kullananlar otomatik yanıt ve devir kurallarını seçer.",
  "example": "Müşteri yazdıktan sonraki 24 saatte serbest yanıt; sonrasında yalnız onaylı yardımcı ya da pazarlama şablonu.",
  "rule": "WhatsApp mesaj kuralları: {labels}.",
  "options": [
   o("window", "24 saatlik müşteri hizmet penceresi", "Müşterinin son mesajından sonraki 24 saat içinde şablonsuz mesaj gönderilebilir; dışında yalnız onaylı şablon.", "Cloud API kullananlar.", "25. saatte yanıt için şablon gerekir.", "Müşterinin son mesajından sonraki 24 saat içinde serbest mesaj gönderilir; pencere dışında işletme yalnız onaylı şablonla yazar."),
   o("templates", "Doğru şablon kategorisi", "Pazarlama, yardımcı (utility) ve kimlik doğrulama şablonları amaca göre seçilir; karışık içerik pazarlama sayılır.", "Şablon kullanan herkes.", "Kargo bildirimi yardımcı, indirim duyurusu pazarlama.", "Şablonlar amaca göre pazarlama, yardımcı ya da kimlik doğrulama kategorisinde açılır; yardımcı şablona pazarlama içeriği eklenmez; şablon listesi ve onay durumları kayıt altındadır."),
   o("per_user", "Kişi başına pazarlama limitine uyum", "Meta bir kişiye gidecek pazarlama mesajı sayısını sınırlayabilir; 131049 hatasında aynı mesaj hemen yeniden denenmez.", "Pazarlama şablonu gönderenler.", "Hata alınan kişiye en az 24 saat sonra yeniden denenir.", "Pazarlama şablonunda 131049 hatası alınan kişiye aynı mesaj en az 24 saat yeniden gönderilmez; hata oranı raporlanır."),
   o("cost", "Maliyet izlenir", "Mesaj başına ücretlendirme (1 Temmuz 2025) ve 1 Ekim 2026 değişikliği (hizmet mesajlarında numara başına aylık 1.000 ücretsiz, pencere içi yardımcı mesajlar ücretli) bütçeye yansıtılır.", "Cloud API kullananlar.", "Aylık raporda kategoriye göre mesaj sayısı ve maliyet.", "WhatsApp mesajları kategoriye göre sayılır ve maliyeti aylık raporlanır; Meta'nın güncel fiyat tablosu (Türkiye ayrı pazar) ve ücretsiz giriş noktası kuralları bütçeye yansıtılır."),
   o("auto", "Karşılama ve mesai dışı yanıtı", "İlk mesaja karşılama, mesai dışında çalışma saatlerini bildiren otomatik yanıt.", "Her işletme.", "“Mesainiz dışında yazdınız, 09:00'da dönüyoruz.”", "WhatsApp'ta ilk mesaja karşılama ve mesai dışında çalışma saatlerini bildiren otomatik yanıt vardır."),
   o("handoff", "Bottan temsilciye devir", "Otomatik akış her adımda temsilciye geçiş sunar.", "Chatbot kullananlar.", "“Temsilciyle görüş” düğmesi.", "WhatsApp otomatik akışında her adımda canlı temsilciye geçiş seçeneği bulunur; devir sohbet geçmişiyle yapılır."),
   o("optout", "Ret anahtar kelimeleri", "“DUR”, “İPTAL” gibi yanıtlar pazarlama listesinden otomatik çıkarır.", "Pazarlama mesajı gönderenler.", "“DUR” yazan kişi listeden çıkar ve onay mesajı alır.", "Pazarlama şablonlarında ret yolu belirtilir; “DUR” ve benzeri yanıtlar kişiyi otomatik olarak pazarlama listesinden çıkarır.")]},
 {"id": "mt_wa_site", "label": "Sitede ve Reklamda WhatsApp", "en": "WhatsApp on Site & Ads", "type": "multiselect", "showIf": SV("whatsapp"),
  "explanation": "Sitedeki WhatsApp düğmelerini, QR kodu, WhatsApp'a tıklama reklamlarını ve ölçümünü belirler.",
  "scenario": "WhatsApp'tan talep alan her sitede wa.me bağlantısı ve tıklama ölçümü seçilir; reklam veriliyorsa WhatsApp'a tıklama reklamları eklenir.",
  "example": "Sayfadaki “WhatsApp'tan yazın” düğmesi https://wa.me/905321234567?text=… adresine gider ve tıklamada GA4 ile Meta'ya olay gönderir.",
  "rule": "Sitede ve reklamda WhatsApp: {labels}.",
  "recommend": [{"field": "mk_conversions", "map": {"whatsapp": ["wa_me", "tracking"]}}],
  "options": [
   o("wa_me", "wa.me bağlantısı", "Bağlantı numarayı uluslararası biçimde (ülke kodu, başta 0, boşluk ve tire olmadan) kullanır; isteğe bağlı hazır mesaj ?text= ile.", "WhatsApp'tan talep alan her site.", "https://wa.me/905321234567?text=Merhaba%2C%20randevu", "Sitedeki WhatsApp bağlantıları https://wa.me/ ile ülke kodlu, boşluksuz numaraya verilir; hazır mesaj ?text= ile ve URL kodlamasıyla eklenir; numara Ortak Bilgiler'deki WhatsApp hattıdır."),
   o("qr", "QR kod", "Mağaza, broşür ve kartvizitlerde wa.me bağlantısının QR kodu kullanılır.", "Fiziksel mağaza ya da basılı malzeme kullananlar.", "Kasada “WhatsApp'tan sipariş” QR kodu.", "Basılı malzemelerde wa.me bağlantısının UTM bilgisi taşıyan hazır mesajlı QR kodu kullanılır."),
   o("tracking", "Tıklama dönüşüm olarak ölçülür", "WhatsApp bağlantısına tıklama analitikte ve Meta'da (Contact) olay olarak gönderilir.", "WhatsApp'ı dönüşüm sayan siteler.", "Tıklamada GA4 whatsapp_click ve Meta Contact.", "WhatsApp bağlantısına tıklama analitik aracına ve onay varsa Meta'ya Contact olayı olarak gönderilir."),
   o("ctwa", "WhatsApp'a tıklama reklamları", "Facebook ve Instagram reklamı tıklanınca WhatsApp sohbeti açılır; WhatsApp hesabı Sayfaya bağlı olmalıdır. Bu reklamlardan gelen sohbette ücretsiz giriş noktası penceresi açılır.", "Mesajla satış ya da randevu alan, reklam veren işletmeler.", "Reklamdaki “WhatsApp'tan mesaj gönder” düğmesi.", "WhatsApp'a tıklama reklamları için WhatsApp numarası Facebook Sayfasına bağlanır; reklamdan gelen sohbetler kaynaklarıyla etiketlenir ve satışa dönüşenler raporlanır."),
   o("channel", "WhatsApp Kanalı", "Tek yönlü duyuru kanalı; takipçi numaraları işletmeye görünmez.", "Duyuru ve içerik paylaşmak isteyen markalar.", "Kanal adresi Ortak Bilgiler'de.", "WhatsApp Kanalı açılırsa adresi Ortak Bilgiler › Sosyal Hesap Adresleri'ne yazılır ve içerik takvimine eklenir.")]}]

# 7 — Meta Reklam Hesabı Kurulumu
SECTIONS.append({
 "id": "mt_ads", "name": "Meta Reklam Hesabı Kurulumu", "en": "Meta Ad Account Setup", "icon": "◆", "agents": ["PS", "I"],
 "refs": ["mk_brand_name", "oc_legal_name", "oc_tax_ids", "mk_ids"],
 "desc": "Meta reklam hesabının para birimi ve saat dilimini, ödeme ve fatura ayarlarını, özel reklam kategorilerini, marka güvenliğini ve hesaba bağlanacak varlıkları belirler; kampanya stratejisi Pazarlama Kararları › Meta Ads'te kalır",
 "guide": {
  "purpose": "Reklam hesabının para birimi ve saat dilimi hesap açılırken belirlenir ve sonradan değiştirilemez; değiştirmek için yeni hesap açmak gerekir, eski hesabın geçmişi ayrı kalır. Bu bölüm hesabı doğru açtırır, fatura ve ödeme bilgilerini kurumla eşler, Meta'nın özel reklam kategorilerini ve siyasi / sosyal konulu reklam kurallarını kontrol ettirir, hesaba veri kümesini, Sayfayı, Instagram'ı, WhatsApp'ı ve katalogu bağlar. Kampanya amaçları, kitleler ve kreatif kararları Pazarlama Kararları › Meta Ads'tedir.",
  "criteria": [
   "Reklam hesabı kurumun işletme portföyündedir; para birimi ve saat dilimi muhasebe ve raporlamayla uyumludur.",
   "Fatura bilgileri ticari unvan, vergi dairesi ve vergi numarasıyla girilir; Meta faturalarındaki vergi ve ücret kalemleri muhasebeyle kontrol edilir.",
   "Reklamın konusu özel reklam kategorisine giriyorsa doğru kategori seçilir; siyasi / sosyal konulu reklam için yetkilendirme yapılır.",
   "Veri kümesi, Sayfa, Instagram hesabı, WhatsApp numarası ve katalog reklam hesabına bağlıdır."],
  "pitfalls": [
   "Hesabı USD ve yanlış saat dilimiyle açmak: raporlar ve faturalar muhasebeyle tutmaz, düzeltmek için yeni hesap gerekir.",
   "Fatura bilgilerini eksik girmek: Meta faturası muhasebeye işlenemez.",
   "Kredi, istihdam ya da konut ilanını normal reklam gibi açmak: reklam reddedilir ya da hesap kısıtlanır.",
   "Advantage+ kreatif iyileştirmelerini kontrol etmeden açık bırakmak: marka kurallarına uymayan otomatik varyasyonlar yayınlanabilir."],
  "resources": [
   r("Özel reklam kategorileri (Marketing API)", "https://developers.facebook.com/docs/marketing-api/audiences/special-ad-category", "Konut, finansal ürün ve hizmetler, istihdam, sosyal konular / seçimler / siyaset."),
   r("Özel reklam kategorisi seçme", "https://www.facebook.com/business/help/298000447747885", "Meta Yardım Merkezi: kampanyada özel kategori seçimi."),
   r("Sosyal konular, seçimler ve siyaset reklamları için yetkilendirme", "https://www.facebook.com/business/help/208949576550051", "Yetkilendirme ve “Ödeyen” beyanı."),
   r("Meta reklamları için konum ücretleri", "https://www.facebook.com/business/help/1238737454289085", "Bazı ülkelere gösterilen reklamlara eklenen ücret; faturayla kontrol edilir."),
   r("Advantage+ kreatif iyileştirmeleri (Marketing API v22)", "https://developers.facebook.com/blog/post/2025/01/17/marketing-api-v22-impacts-to-advantage-plus-creative-enhancements/", "İyileştirmeler tek tek açılır ya da kapatılır.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_ads_account", "label": "Para Birimi ve Saat Dilimi", "en": "Currency & Time Zone", "type": "select", "showIf": SV("ads"),
  "explanation": "Reklam hesabının para birimini ve saat dilimini belirler. İkisi hesap açılırken seçilir ve sonradan değiştirilemez.",
  "scenario": "Türkiye'de faturalanan ve TL ile muhasebeleşen işletmeler TRY ve İstanbul saat dilimini; döviz bütçeli ya da yurt dışı merkezli işletmeler kendi para birimini seçer.",
  "example": "Hesap TRY ve (GMT+03:00) İstanbul ile açılır; günlük bütçe ve raporlar Türkiye gününe göre çalışır.",
  "rule": "Meta reklam hesabının para birimi ve saat dilimi: {label}. Bu ayarlar sonradan değiştirilemez; değişiklik gerekirse yeni reklam hesabı açılır ve eski hesabın raporları saklanır.",
  "options": [
   o("try_ist", "TRY · İstanbul (önerilen)", "Türk lirası ve İstanbul saat dilimi.", "Türkiye'de faturalanan ve TL ile muhasebeleşen işletmeler.", "Bütçe 500 TL/gün, gün 00:00 İstanbul'da başlar.", "Reklam hesabı TRY para birimi ve İstanbul saat dilimiyle açılır."),
   o("usd_ist", "USD · İstanbul", "ABD doları ve İstanbul saat dilimi.", "Bütçesi ve muhasebesi dolar bazlı olan işletmeler.", "Bütçe 20 USD/gün.", "Reklam hesabı USD para birimi ve İstanbul saat dilimiyle açılır; kur farkı muhasebeyle önceden konuşulur."),
   o("eur_market", "EUR · hedef pazar saat dilimi", "Euro ve hedef pazarın saat dilimi.", "Avrupa'ya reklam veren, euro ile muhasebeleşen işletmeler.", "EUR ve Berlin saat dilimi.", "Reklam hesabı EUR para birimi ve hedef pazarın saat dilimiyle açılır.")]},
 {"id": "mt_ads_settings", "label": "Asgari Reklam Hesabı Ayarları", "en": "Minimum Ad Account Settings", "type": "multiselect", "showIf": SV("ads"),
  "explanation": "Reklam hesabında yapılacak asgari sahiplik, ödeme, uyum ve marka güvenliği ayarlarını belirler.",
  "scenario": "Sahiplik, roller, fatura bilgileri ve ödeme yöntemi her hesapta seçilir; reklam konusuna göre özel kategori ve siyasi reklam yetkilendirmesi, bütçe riskine göre harcama limiti eklenir.",
  "example": "Faturada ticari unvan ve vergi numarası, kurumsal kart birincil, ikinci kart yedek; hesap harcama limiti üç aylık bütçe kadar.",
  "rule": "Meta reklam hesabı ayarları: {labels}.",
  "options": [
   o("owner", "Kurumun portföyünde, rollerle", "Hesap kurumun portföyündedir; ajans iş ortağı erişimiyle, çalışanlar görevine göre rolle.", "Her hesap.", "Muhasebe yalnız fatura görüntüleme yetkisinde.", "Reklam hesabı kurumun işletme portföyündedir; ajans iş ortağı erişimiyle, çalışanlar görevine uygun rolle (yönetme, reklam, analiz, fatura) eklenir."),
   o("billing", "Fatura bilgileri ve vergi", "Ticari unvan, adres, vergi dairesi ve vergi numarası girilir; Meta faturasındaki vergi ve ücret kalemleri muhasebeyle kontrol edilir.", "Her hesap.", "Aylık Meta faturası muhasebeye iletilir.", "Reklam hesabının fatura bilgileri ticari unvan, adres, vergi dairesi ve vergi numarasıyla girilir; Meta faturaları her ay muhasebeye iletilir ve faturadaki vergi ile konum ücreti kalemleri muhasebe birimince kontrol edilir."),
   o("payment", "Ödeme yöntemi ve yedek", "Kurumsal kart ya da ön ödemeli bakiye birincil, ikinci bir yöntem yedek; kişisel kart kullanılmaz.", "Her hesap.", "Kurumsal kart + yedek kart.", "Reklam hesabında kuruma ait birincil ve yedek ödeme yöntemi tanımlıdır; kişisel kart kullanılmaz."),
   o("spend_limit", "Hesap harcama limiti", "Hesabın toplam harcamasına üst sınır konur; hatalı bütçe girişine karşı güvenlik.", "Ajansla ya da çok kişiyle yönetilen hesaplar.", "Limit üç aylık onaylı bütçe.", "Reklam hesabına onaylı bütçeyle uyumlu bir harcama limiti konur; limit bütçe onayıyla güncellenir."),
   o("special", "Özel reklam kategorisi kontrolü", "Kredi ve finansal ürün, istihdam, konut ya da sosyal konular / seçimler / siyaset reklamlarında özel kategori seçilir; hedefleme seçenekleri kısıtlanır.", "Finans, insan kaynakları, emlak, dernek ve siyasi içerikli reklamlar.", "İş ilanı kampanyası “İstihdam” kategorisinde.", "Her kampanyada reklamın özel reklam kategorisine girip girmediği kontrol edilir; giriyorsa doğru kategori ve ülke seçilir."),
   o("political", "Siyasi / sosyal konulu reklam yetkilendirmesi", "Bu tür reklamlarda kullanıcı kimliği ve Sayfa yetkilendirilir, “Ödeyen” beyanı eklenir.", "Kamu politikası, seçim ya da toplumsal konularda reklam verecek kurumlar.", "Reklamda “Ödeyen: Örnek Derneği”.", "Sosyal konular, seçimler ya da siyaset reklamı verilecekse reklamı yöneten kişiler ve Sayfa hedef ülke için yetkilendirilir ve “Ödeyen” beyanı eklenir."),
   o("brand_safety", "Marka güvenliği", "Engelleme listeleri ve envanter filtresiyle reklamın uygunsuz içeriklerin yanında görünmesi sınırlanır.", "Marka hassasiyeti yüksek işletmeler.", "Belirli yayıncılar engelleme listesinde.", "Reklam hesabında engelleme listeleri ve envanter filtresi kurum politikasına göre ayarlanır."),
   o("advantage", "Otomatik kreatif iyileştirmeleri gözden geçirilir", "Advantage+ kreatif iyileştirmeleri tek tek değerlendirilir; marka kurallarına uymayanlar kapatılır.", "Marka kılavuzu olan işletmeler.", "Metin varyasyonu kapalı, görsel kırpma açık.", "Advantage+ kreatif iyileştirmeleri her kampanyada tek tek gözden geçirilir; marka ve hukuk kurallarına uymayan otomatik varyasyonlar kapatılır."),
   o("naming", "Adlandırma ve UTM", "Kampanya, reklam seti ve reklam adları ile UTM şeması standarttır.", "Her hesap.", "2026-11_lead_istanbul_karusel", "Kampanya, reklam seti ve reklam adları ile reklam bağlantılarındaki UTM parametreleri pazarlama kararlarındaki standarda göre verilir.")]},
 {"id": "mt_ads_links", "label": "Reklam Hesabına Bağlanacaklar", "en": "Linked Assets", "type": "multiselect", "showIf": SV("ads"),
  "explanation": "Reklam hesabıyla birlikte çalışacak varlıkları ve aktarımları belirler.",
  "scenario": "Veri kümesi, Sayfa ve Instagram her reklam hesabına bağlanır; mesaj reklamlarında WhatsApp, katalog satışında katalog, anlık form kullananlarda CRM aktarımı eklenir.",
  "example": "Reklam hesabı veri kümesine, Sayfaya, Instagram'a ve WhatsApp numarasına bağlı; anlık form lead'leri CRM'e otomatik düşer.",
  "rule": "Meta reklam hesabına bağlananlar: {labels}.",
  "recommend": [{"field": "mt_services", "map": {"pixel": ["dataset"], "page": ["page_ig"], "instagram": ["page_ig"], "whatsapp": ["whatsapp"], "catalog": ["catalog"]}},
                {"field": "mk_meta_objectives", "map": {"instant_form": ["lead_crm"], "messages": ["whatsapp"], "catalog": ["catalog"]}}],
  "options": [
   o("dataset", "Veri kümesi (piksel)", "Dönüşüm ölçümü ve yeniden hedefleme için.", "Siteye trafik ya da dönüşüm reklamı verenler.", "Reklam setinde dönüşüm olayı Lead.", "Veri kümesi (piksel) reklam hesabına bağlanır; kampanyalar standart olaylarla optimize edilir."),
   o("page_ig", "Facebook Sayfası ve Instagram hesabı", "Reklamların hangi kimlikle yayınlanacağı.", "Her hesap.", "Reklamda Sayfa adı ve Instagram kullanıcı adı.", "Reklamlar kurumun Facebook Sayfası ve Instagram hesabı kimliğiyle yayınlanır."),
   o("whatsapp", "WhatsApp numarası", "WhatsApp'a tıklama reklamları için numara Sayfaya ve hesaba bağlanır.", "Mesaj reklamı verenler.", "Reklamın hedefi WhatsApp.", "WhatsApp numarası Sayfaya bağlanır ve WhatsApp'a tıklama reklamlarında kullanılır."),
   o("catalog", "Katalog", "Katalog reklamları ve ürün etiketleri için.", "E-ticaret ve katalog satışı.", "Dinamik ürün reklamı.", "Meta kataloğu reklam hesabına ve veri kümesine bağlanır; ürün kimlikleri piksel olaylarındaki content_ids ile aynıdır."),
   o("lead_crm", "Anlık form lead'leri CRM'e", "Anlık formdan gelen talepler CRM'e otomatik aktarılır; elle dosya indirmeye bırakılmaz.", "Anlık form (lead) reklamı verenler.", "Lead 5 dakika içinde CRM'de ve satışçıya atanmış.", "Anlık form talepleri resmî entegrasyon ya da sistem kullanıcısı jetonuyla CRM'e otomatik aktarılır; aktarım hatası günlük kontrol edilir."),
   o("offline", "Satış sonuçları Conversions API ile", "CRM'de satışa dönen talepler Conversions API ile Meta'ya geri bildirilir.", "Satışı sitede değil telefonda ya da mağazada kapanan işletmeler.", "CRM'de “satış” aşamasına geçen lead Meta'ya Purchase olarak gider.", "CRM'de satışa dönüşen talepler, onay ve hukuki dayanak varsa, Conversions API ile karma yapılmış müşteri bilgisiyle Meta'ya bildirilir.")]}]

# 8 — Katalog & Commerce Manager
SECTIONS.append({
 "id": "mt_catalog", "name": "Katalog & Commerce Manager", "en": "Catalog & Commerce Manager", "icon": "▤", "agents": ["MI", "PS"],
 "refs": ["domain_name", "oc_services"],
 "desc": "Meta kataloğunun hangi kaynaktan besleneceğini, ürün verisinin asgari kalite kurallarını ve katalogun reklam, Instagram ve WhatsApp'ta nasıl kullanılacağını belirler",
 "guide": {
  "purpose": "Meta kataloğu ürün ya da hizmetlerin kimlik, ad, açıklama, fiyat, stok, görsel ve bağlantı bilgisini tutar. Katalog reklamları, Instagram ürün etiketleri ve WhatsApp kataloğu bu veriyi kullanır. Ürün kimlikleri piksel olaylarındaki content_ids ile aynı olmazsa katalog reklamları doğru ürünü gösteremez. Alışveriş özelliklerinin ülkeye göre uygunluğu değişir; Türkiye'deki durum işletmenin Commerce Manager hesabında kontrol edilmelidir.",
  "criteria": [
   "Katalog otomatik ve düzenli güncellenen bir kaynaktan beslenir; fiyat ve stok sitedekiyle aynıdır.",
   "Ürün kimlikleri site, piksel (content_ids) ve katalogda aynıdır.",
   "Zorunlu alanlar eksiksiz, görseller kurallara uygundur; teşhis ekranında hata yoktur.",
   "Katalog kurumun portföyündedir ve veri kümesine bağlıdır."],
  "pitfalls": [
   "Katalogu elle yükleyip güncellememek: fiyatı değişen ürün reklamda eski fiyatla görünür.",
   "Pikselde ürün kimliği yerine ürün adı göndermek: katalog reklamları ziyaretçiye baktığı ürünü gösteremez.",
   "Görsellerde metin, logo ya da filigran yoğunluğu: ürünler reddedilebilir.",
   "Alışveriş özelliklerinin Türkiye'de açık olduğunu varsaymak: uygunluk Commerce Manager'da kontrol edilmelidir."],
  "resources": [
   r("Ticaret uygunluk gereklilikleri", "https://www.facebook.com/business/help/2347002662267537", "Alışveriş ve ürün etiketi özelliklerinin uygunluk şartları."),
   r("Meta Pikseli — standart olaylar referansı", "https://developers.facebook.com/docs/meta-pixel/reference", "ViewContent, AddToCart, Purchase olaylarında content_ids ve content_type.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_cat_source", "label": "Katalog Veri Kaynağı", "en": "Catalog Data Source", "type": "select", "showIf": SV("catalog"),
  "explanation": "Meta kataloğunun hangi kaynaktan, nasıl güncelleneceğini belirler.",
  "scenario": "Kendi kodlu e-ticaret sitesinde planlı veri feed'i; hazır platformda platformun Meta entegrasyonu; çok sık stok değişen büyük kataloglarda API seçilir.",
  "example": "Site her gece /feeds/meta.xml dosyasını üretir, Meta saatte bir çeker; stok bitince ürün “out of stock” görünür.",
  "rule": "Meta katalog veri kaynağı: {label}.",
  "options": [
   o("feed", "Planlı veri feed'i (önerilen)", "Site düzenli olarak bir ürün dosyası (XML, CSV) üretir; Meta belirlenen aralıkta çeker.", "Kendi kodlu e-ticaret siteleri.", "Günlük feed, saatlik fiyat güncellemesi.", "Katalog sitenin ürettiği planlı veri feed'inden beslenir; feed en az günde bir güncellenir, fiyat ve stok değişikliği sık ise ek güncelleme planlanır."),
   o("platform", "Platformun Meta entegrasyonu", "Hazır e-ticaret platformunun resmî Meta uygulaması katalogu eşitler.", "Shopify, WooCommerce, Ticimax, İdeasoft kullananlar.", "Platform uygulamasında katalog eşitleme açık.", "Katalog e-ticaret platformunun resmî Meta entegrasyonuyla eşitlenir; ürün kimlikleri piksel olaylarıyla aynıdır."),
   o("api", "Katalog API'si", "Ürün değişiklikleri sunucudan API ile anlık gönderilir.", "Büyük ve sık değişen kataloglar.", "Stok değişince ürün 1 dakikada güncellenir.", "Katalog sunucudan Meta katalog API'siyle, sistem kullanıcısı jetonuyla güncellenir; değişiklikler kuyrukla ve yeniden deneme mantığıyla gönderilir."),
   o("manual", "Elle (tablo ya da tek tek)", "Ürünler Commerce Manager'da elle girilir ya da tablo yüklenir.", "Birkaç hizmet paketi ya da az ürünü olan işletmeler.", "Altı hizmet paketi elle girilmiş.", "Katalog elle yönetilir; fiyat ya da içerik değiştiğinde aynı gün güncellenir ve ayda bir siteyle karşılaştırılır.")]},
 {"id": "mt_cat_settings", "label": "Katalog Kalite ve Kullanım Ayarları", "en": "Catalog Quality & Usage", "type": "multiselect", "showIf": SV("catalog"),
  "explanation": "Katalog verisinin asgari kalite kurallarını ve katalogun nerelerde kullanılacağını belirler.",
  "scenario": "Ürün kimliği eşleşmesi, zorunlu alanlar, fiyat / stok eşitliği ve teşhis takibi her katalogda seçilir; ürün setleri, Instagram ve WhatsApp kullanımı ihtiyaca göre eklenir.",
  "example": "Teşhis ekranında 0 hata; “Kış koleksiyonu” ürün seti katalog reklamında kullanılır.",
  "rule": "Meta katalog ayarları: {labels}.",
  "options": [
   o("ids", "Ürün kimlikleri pikselle aynı", "Katalogdaki id, pikselde content_ids olarak aynen gönderilir.", "Katalog reklamı verenler.", "SKU “TS-104” her yerde aynı.", "Katalogdaki ürün kimliği sitedeki ürün kimliği ve piksel olaylarındaki content_ids ile aynıdır."),
   o("fields", "Zorunlu alanlar eksiksiz", "Kimlik, ad, açıklama, uygunluk, durum, fiyat, bağlantı, görsel ve marka.", "Her katalog.", "Teşhiste eksik alan uyarısı yok.", "Katalogda kimlik, ad, açıklama, uygunluk, durum, fiyat, bağlantı, görsel ve marka alanları her üründe doludur."),
   o("price_stock", "Fiyat ve stok sitedekiyle aynı", "İndirimli fiyat ve stok bilgisi site ile katalogda aynı anda değişir.", "Her katalog.", "İndirim başlayınca sale_price feed'de.", "Katalogdaki fiyat, indirimli fiyat ve stok sitedekiyle aynıdır; tutarsızlık teşhis ekranında haftalık kontrol edilir."),
   o("images", "Görsel kuralları", "Ürün net, arka plan sade; yoğun metin, filigran ve yanıltıcı görsel kullanılmaz.", "Her katalog.", "Beyaz arka planlı kare ürün görseli.", "Katalog görsellerinde ürün net görünür; yoğun metin, filigran ve yanıltıcı görsel kullanılmaz."),
   o("sets", "Ürün setleri", "Kategori, sezon ya da kampanyaya göre ürün setleri oluşturulur.", "Katalog reklamı verenler.", "“İndirimdekiler” seti.", "Katalog reklamları için kategori ve kampanyaya göre ürün setleri oluşturulur."),
   o("diagnostics", "Teşhis ekranı izlenir", "Commerce Manager teşhis ekranındaki hata ve uyarılar düzenli düzeltilir.", "Her katalog.", "Haftalık teşhis kontrolü.", "Commerce Manager teşhis ekranı haftalık kontrol edilir; reddedilen ürünler düzeltilir."),
   o("ig_tags", "Instagram ürün etiketleri", "Uygunsa gönderilerde ürün etiketi kullanılır; Türkiye uygunluğu Commerce Manager'da kontrol edilir.", "Instagram'da ürün satan işletmeler.", "Gönderide ürün etiketi ve fiyat.", "Instagram ürün etiketleri yalnız Commerce Manager'da hesabın uygun olduğu doğrulanınca kullanılır."),
   o("wa_catalog", "WhatsApp kataloğu", "Meta kataloğu WhatsApp Business hesabına bağlanır.", "WhatsApp'tan sipariş alan işletmeler.", "Sohbette ürün kartı.", "Meta kataloğu WhatsApp Business hesabına bağlanır; WhatsApp'ta gösterilen fiyat sitedekiyle aynıdır.")]}]

# 9 — Kurulum Planı & Talimat
SECTIONS.append({
 "id": "mt_report", "name": "Kurulum Planı & Talimat", "en": "Setup Plan & Instructions", "icon": "☰", "agents": ["S", "O"],
 "desc": "Meta kurulumunun nasıl doğrulanacağını, teslimde hangi belgelerin verileceğini ve bakımını belirler; seçimlerden ayrı bir kurulum talimatı (.md) üretilir",
 "guide": {
  "purpose": "Kurulumun bittiği ancak doğrulanınca söylenebilir: onaysız ziyaretçide pikselin çalışmadığı, olayların tekilleştiği, WhatsApp şablonunun test numarasına ulaştığı, reklam önizlemesinin doğru Sayfa ve Instagram kimliğiyle göründüğü kontrol edilir. Teslimde erişim listesi, varlık ve kimlik tablosu, olay sözlüğü ve şablon listesi verilir. Aşağıdaki kart seçimlerinizden ayrı bir kurulum talimatı üretir.",
  "criteria": [
   "Her doğrulama adımı kanıtla (ekran görüntüsü, Test Olayları kaydı, ağ isteği) belgelenir.",
   "Erişim listesi ve varlık / kimlik tablosu teslim edilir; kimlikler Ortak Bilgiler'e yazılır.",
   "Olay sözlüğü ve WhatsApp şablon listesi güncel tutulur.",
   "Erişim, onay ve maliyet üç ayda bir gözden geçirilir."],
  "pitfalls": [
   "Pikseli yalnız onay verilmiş tarayıcıda denemek: onay reddinde de istek gidip gitmediği görülmez.",
   "Kurulum belgesini yalnız ajansta bırakmak: ajans değişince kimse yapıyı bilmez.",
   "WhatsApp şablonlarını gerçek müşterilerde denemek: kalite puanı düşer.",
   "Kimlikleri kaydetmemek: geliştirici, ajans ve analitik ekibi farklı varlıklara bağlanır."],
  "resources": [
   r("Piksel ve sunucu olaylarının tekilleştirilmesi", "https://developers.facebook.com/documentation/ads-commerce/conversions-api/deduplicate-pixel-and-server-events", "Doğrulamada tarayıcı ve sunucu olaylarının tek sayılması."),
   r("WhatsApp — telefon numaraları ve test", DEV + "business-phone-numbers/phone-numbers", "Numara kaydı ve iki adımlı doğrulama."),
   r("Meta Pikseli — onay (consent) API'si", "https://developers.facebook.com/docs/meta-pixel/implementation/gdpr", "Onay reddinde gönderim olmadığının denetimi.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "mt_verify", "label": "Doğrulama Adımları", "en": "Verification Steps", "type": "multiselect",
  "explanation": "Kurulum bittiğinde yapılacak kontrolleri belirler.",
  "scenario": "Onay testi ve Test Olayları pikselli her kurulumda, WhatsApp testi WhatsApp kurulumunda, reklam önizlemesi reklam hesabında seçilir.",
  "example": "Rapor: onay reddinde facebook.com isteği yok; Lead tarayıcı + sunucu tekilleşmiş; şablon test numarasına ulaştı.",
  "rule": "Meta kurulumunun doğrulanması: {labels}.",
  "options": [
   o("consent_test", "Onay reddi testi", "Çerezler reddedilince ağ sekmesinde Meta isteği olmadığı, kabul edilince başladığı denetlenir.", "Pikselli her kurulum.", "Ret: 0 istek; kabul: PageView.", "Çerezler reddedilince tarayıcı ağ sekmesinde facebook.com / connect.facebook.net isteği olmadığı, kabul edilince pikselin başladığı denetlenir ve kaydedilir."),
   o("test_events", "Test Olayları ve tekilleştirme", "Her olay Test Olayları'nda tarayıcı ve sunucu kaynaklı tek olay olarak görünür.", "Piksel ve Conversions API kurulumu.", "Lead: tarayıcı + sunucu, tekilleştirildi.", "Her standart olay Events Manager › Test Olayları'nda denenir; tarayıcı ve sunucu olayının tekilleştiği kaydedilir."),
   o("pixel_helper", "Meta Pixel Helper kontrolü", "Tarayıcı eklentisiyle sayfada tek piksel ve doğru olaylar olduğu görülür.", "Pikselli her site.", "Eklenti tek piksel kimliği gösterir.", "Meta Pixel Helper ile her sayfa türünde tek piksel kimliği ve beklenen olaylar doğrulanır."),
   o("domain_check", "Alan adı doğrulandı", "İşletme ayarlarında alan adı “Doğrulandı” durumundadır.", "Kendi alan adı olan her site.", "Durum: Doğrulandı.", "İşletme ayarlarında alan adının doğrulandığı kontrol edilir."),
   o("wa_test", "WhatsApp test mesajı", "Şablonlar ve otomatik yanıtlar test numarasında denenir; webhook imza doğrulaması çalışır.", "WhatsApp kurulumu.", "Şablon test numarasına ulaştı, webhook 200 döndü.", "WhatsApp şablonları, otomatik yanıtlar ve webhook test numarasıyla denenir; gerçek müşteri listesi testte kullanılmaz."),
   o("ads_preview", "Reklam önizlemesi", "Reklam önizlemesi doğru Sayfa, Instagram kimliği, bağlantı ve UTM'yle görünür.", "Reklam hesabı kurulumu.", "Önizlemede UTM'li bağlantı.", "İlk kampanyadan önce reklam önizlemesinde Sayfa, Instagram kimliği, bağlantı ve UTM parametreleri kontrol edilir."),
   o("devices", "Farklı tarayıcı ve cihazda deneme", "Mobil ve masaüstünde, en az iki tarayıcıda denenir.", "Her kurulum.", "Safari ve Chrome'da aynı sonuç.", "Kurulum mobil ve masaüstünde, en az iki tarayıcıda denenir.")]},
 {"id": "mt_handover", "label": "Teslim ve Bakım", "en": "Handover & Maintenance", "type": "multiselect",
  "explanation": "Kurulumdan sonra teslim edilecek belgeleri ve dönemsel bakımı belirler.",
  "scenario": "Erişim listesi ve varlık / kimlik tablosu her kurulumda teslim edilir; olay sözlüğü ve şablon listesi ilgili kurulumda eklenir.",
  "example": "Teslim klasöründe erişim listesi, varlık tablosu, olay sözlüğü, WhatsApp şablon listesi ve değişiklik kaydı bulunur.",
  "rule": "Meta kurulumunun teslim ve bakımı: {labels}.",
  "options": [
   o("access_list", "Erişim listesi", "Portföyde ve her varlıkta kim, hangi yetkiyle; iş ortakları ve sistem kullanıcıları.", "Her kurulum.", "Tablo: varlık, kişi / ortak, yetki, tarih.", "Portföy ve varlık erişim listesi (kişiler, iş ortakları, sistem kullanıcıları ve yetkileri) teslim edilir."),
   o("asset_table", "Varlık ve kimlik tablosu", "Portföy, Sayfa, Instagram, reklam hesabı, veri kümesi, katalog, WhatsApp hesap ve numara kimlikleri; Ortak Bilgiler'e de yazılır.", "Her kurulum.", "Veri kümesi 123…, WABA 102…", "Bütün Meta varlık kimlikleri tablo olarak teslim edilir ve Ortak Bilgiler › Hesap ve Etiket Kimlikleri'ne yazılır."),
   o("event_dict", "Olay sözlüğü", "Her olayın adı, tetiklendiği an, parametreleri ve reklamda kullanımı.", "Pikselli kurulum.", "Lead: form sunucuda kaydedilince; content_name.", "Olay sözlüğü (olay adı, tetikleme anı, parametreler, reklamda kullanımı) teslim edilir ve değişiklikte güncellenir."),
   o("templates", "WhatsApp şablon listesi", "Şablon adı, kategori, dil, onay durumu ve kullanım yeri.", "WhatsApp Cloud API kurulumu.", "randevu_hatirlatma · yardımcı · tr · onaylı.", "WhatsApp şablon listesi (ad, kategori, dil, onay durumu, kullanım yeri) teslim edilir ve güncel tutulur."),
   o("change_log", "Değişiklik kaydı", "Piksel, reklam hesabı, WhatsApp ve katalog ayar değişiklikleri tarih, kişi ve gerekçeyle.", "Birden çok kişinin çalıştığı hesaplar.", "“2026-12-01: Advantage+ metin varyasyonu kapatıldı.”", "Meta varlıklarındaki ayar değişiklikleri tarih, kişi ve gerekçeyle değişiklik kaydına yazılır."),
   o("quarterly", "Üç ayda bir gözden geçirme", "Erişimler, onay testi, olay eşleşme kalitesi, WhatsApp kalitesi ve maliyeti, katalog teşhisi.", "Her kurulum.", "Ocak, Nisan, Temmuz, Ekim.", "Meta kurulumu üç ayda bir gözden geçirilir: erişimler, onay testi, olay eşleşme kalitesi, WhatsApp kalite durumu ve maliyeti, katalog teşhisi ve Meta'nın kural / fiyat değişiklikleri.")]}]

IDS_ADD = [
 {"k": "meta_page", "label": "Facebook Sayfası kimliği (Page ID)", "ph": "123456789012345", "re": "^\\d{6,20}$"},
 {"k": "meta_ig", "label": "Instagram profesyonel hesap kimliği", "ph": "17841400000000000", "re": "^\\d{6,20}$"},
 {"k": "meta_catalog", "label": "Meta katalog kimliği", "ph": "1234567890123456", "re": "^\\d{6,20}$"},
 {"k": "meta_waba", "label": "WhatsApp Business hesabı (WABA) kimliği", "ph": "102345678901234", "re": "^\\d{6,20}$"},
 {"k": "meta_wa_phone", "label": "WhatsApp telefon numarası kimliği (Phone number ID)", "ph": "109876543210987", "re": "^\\d{6,20}$"},
]
IDS_WHEN = {"meta_business": ["portfolio"], "meta_pixel": ["pixel"], "meta_ad_account": ["ads"], "meta_page": ["page"],
            "meta_ig": ["instagram"], "meta_catalog": ["catalog"], "meta_waba": ["whatsapp"], "meta_wa_phone": ["whatsapp"]}


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: kaynak.py <meta.json>")
    out = {"version": "1.0", "group": GROUP, "agents": AGENTS, "idsAdd": IDS_ADD, "idsWhen": IDS_WHEN, "sections": SECTIONS}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nf = sum(len(s["fields"]) for s in SECTIONS)
    print(f"{len(SECTIONS)} bölüm, {nf} karar, {sum(len(s['guide']['resources']) for s in SECTIONS)} kaynak")


if __name__ == "__main__":
    main()
