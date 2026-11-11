#!/usr/bin/env python3
"""Google Servisleri menüsünün kaynağı (2026-11-11). Elle yazılır; çıktı google.json → google_ekle.py.

Kullanım: python3 -I docs/google/kaynak.py docs/google/google.json

Yapı: GROUP, AGENTS (kısaltma → pozisyon ajanı), SECTIONS (bölüm → rehber + kararlar), IDS_WHEN (Ortak Bilgiler ›
Hesap ve Etiket Kimlikleri satırı → bu satırı görünür yapan servisler). Seçenek yardımcısı o(değer, etiket, açıklama,
senaryo, örnek, kural ayrıntısı). Kaynak adresleri eklenirken gerçekten açılarak doğrulanır (2026-11-11).
"""
import json
import sys

GROUP = "Google Servisleri"
AGENTS = {
    "W": "poz:pazarlama:digital_demand_generation/web-pazarlama-muduru",
    "O": "poz:pazarlama:digital_demand_generation/web-pazarlama-muduru/dijital-olcumleme-uzmani",
    "A": "poz:veri-analitik:17.05/musteri-pazarlama-ve-gelir-analitigi/pazarlama-analitigi-uzmani",
    "R": "poz:pazarlama:digital_demand_generation/performans-pazarlama-muduru/arama-motoru-reklamlari-uzmani",
    "P": "poz:pazarlama:digital_demand_generation/performans-pazarlama-muduru",
    "M": "poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru",
    "T": "poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru/teknik-seo-uzmani",
    "K": "poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani",
    "I": "poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/kidemli-kimlik-ve-erisim-uzmani",
    "V": "poz:veri-analitik:17.04/self-servis-analitik-ve-veri-gorsellestirme/self-servis-analitik-uzmani",
}


def o(value, label, explanation, scenario, example, rd=None, **kw):
    x = {"value": value, "label": label, "explanation": explanation, "scenario": scenario, "example": example}
    if rd:
        x["ruleDetail"] = rd
    x.update(kw)
    return x


def r(title, url, note):
    return {"title": title, "url": url, "note": note}


SV = lambda *v: [{"field": "gg_services", "in": list(v)}]

SECTIONS = []

# 1 — Kapsam, Hesaplar & Erişim
SECTIONS.append({
 "id": "gg_scope", "name": "Kapsam, Hesaplar & Erişim", "en": "Scope, Accounts & Access", "icon": "◎", "agents": ["W", "I"],
 "refs": ["domain_name", "mk_brand_name", "mk_ids"],
 "desc": "Projede hangi Google servislerinin kurulacağını, hesapların kimin adına açılacağını ve hesaplara kimin, hangi yetkiyle erişeceğini belirler; sonraki bölümler buradaki servis seçimine göre açılır",
 "guide": {
  "purpose": "Google servislerinin hepsi bir Google hesabına bağlıdır ve hesabın sahibi verinin, reklam geçmişinin ve faturaların da sahibidir. Bu bölüm kurulacak servisleri seçtirir, sahipliği kuruma bağlar ve erişimi en düşük yetki ilkesine göre düzenler. Seçtiğiniz servislerin bölümleri menüde açılır; Ortak Bilgiler › Hesap ve Etiket Kimlikleri'nde de o servislerin kimlik kutuları üste gelir.",
  "criteria": [
   "Her servis kurumsal bir Google hesabında açılır ve en az iki kişi sahip / yönetici yetkisine sahiptir.",
   "Bütün kullanıcılarda iki adımlı doğrulama açıktır; ajans ve serbest çalışanlar kendi hesaplarıyla, ayrı kullanıcı olarak eklenir.",
   "Kimin hangi serviste hangi yetkiye sahip olduğu yazılı bir erişim listesinde durur ve dönemsel olarak gözden geçirilir.",
   "Kurulan her servisin kimliği (ölçüm kimliği, kapsayıcı kimliği, müşteri kimliği …) Ortak Bilgiler'e yazılır."],
  "pitfalls": [
   "Hesabı ajansın ya da çalışanın kişisel Gmail adresinde açmak: kişi ayrılınca reklam geçmişi, veriler ve faturalar kurumdan kopar.",
   "Tek bir yöneticiyle çalışmak: o kişinin hesabı kilitlenirse ya da ayrılırsa hesaba kimse erişemez.",
   "Herkese en yüksek yetkiyi vermek: yanlışlıkla silinen mülk, değişen dönüşüm ya da yayımlanan hatalı etiket geri alınması zor hasar bırakır.",
   "Servisleri birbirine bağlamadan kurmak: GA4, Ads ve Search Console bağlantısı yoksa raporlar ve reklam optimizasyonu eksik veriyle çalışır."],
  "resources": []}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_services", "label": "Kurulacak Google Servisleri", "en": "Google Services to Set Up", "type": "multiselect",
  "explanation": "Bu projede kurulacak ya da düzenlenecek Google servislerini seçer. Seçtiğiniz servislerin kurulum bölümleri menüde açılır; seçilmeyenler gizli kalır ve kurallara girmez.",
  "scenario": "Ölçüm için çoğu projede Tag Manager, Analytics 4 ve Search Console seçilir; reklam veriliyorsa Google Ads, yerel işletmede İşletme Profili, e-ticarette Merchant Center eklenir.",
  "example": "Bir diş kliniği Tag Manager, Analytics 4, Search Console, Google Ads ve İşletme Profili'ni seçer; Merchant Center ve Looker Studio bölümleri menüde görünmez.",
  "rule": "Kurulacak Google servisleri: {labels}.",
  "recommend": [
   {"field": "analytics_tool", "map": {"GA4": ["ga4"], "GTM": ["gtm"], "Search Console": ["gsc"]}},
   {"field": "mk_ads_channels", "map": {"google": ["ads", "gtm", "ga4"]}},
   {"field": "gbp", "map": {"true": ["gbp"]}},
   {"field": "modules_extra", "map": {"ecommerce": ["merchant", "ga4", "gtm"]}},
   {"field": "mk_gads_types", "map": {"shopping": ["merchant"]}}],
  "options": [
   o("gtm", "Google Tag Manager", "Analitik ve reklam etiketlerini sitenin koduna dokunmadan tek panelden yöneten etiket yönetim aracıdır. Kod siteye bir kez eklenir; sonraki etiketler sürüm ve önizlemeyle yayımlanır.",
     "Birden çok ölçüm ya da reklam etiketi kullanılacaksa, pazarlama ekibi etiketleri geliştirici beklemeden yönetmek istiyorsa.",
     "Yeni bir dönüşüm etiketi Tag Manager'da hazırlanır, Önizleme'de denenir ve sürüm notuyla yayımlanır; sitenin kodu değişmez."),
   o("ga4", "Google Analytics 4", "Ziyaretçi davranışını olay bazlı ölçen analitik platformudur: trafik kaynakları, sayfa görüntülemeleri, form gönderimi ve satın alma gibi işlemler raporlanır.",
     "Hangi kanalın ziyaretçi ve dönüşüm getirdiğini görmek isteyen hemen her site.",
     "Rapor, Instagram reklamından gelen ziyaretçilerin %4'ünün iletişim formunu gönderdiğini gösterir."),
   o("gsc", "Search Console", "Sitenin Google aramadaki durumunu gösteren ücretsiz araçtır: dizine ekleme, arama sorguları, tıklama, Core Web Vitals, güvenlik ve manuel işlem bildirimleri.",
     "Google aramasından trafik bekleyen her site; yayından önce kurulması önerilir.",
     "Yayından iki gün sonra Search Console, test ortamından kalan noindex etiketi yüzünden sayfaların dizine eklenmediğini gösterir."),
   o("ads", "Google Ads", "Google Arama, YouTube, Görüntülü Reklam Ağı ve Haritalar'da reklam yayınlanan platformdur. Bu bölüm kampanya stratejisini değil hesap kurulumunu ve asgari hesap ayarlarını kapsar; kampanya kararları Pazarlama › Google Ads'tedir.",
     "Google'da ücretli reklam verilecekse ya da verilmesi planlanıyorsa.",
     "Hesap yönetici hesabı altında uzman modunda açılır, otomatik etiketleme ve dönüşüm ölçümü kurulmadan kampanya yayınlanmaz."),
   o("merchant", "Merchant Center", "Ürün bilgilerini (fiyat, stok, görsel) Google'a ileten hesaptır; ürünler Google Alışveriş'te ücretsiz listelemelerde ve Alışveriş / Performance Max reklamlarında görünür.",
     "Online ürün satan e-ticaret siteleri.",
     "Ürün feed'i her gece güncellenir; stokta kalmayan ürün ertesi gün Google Alışveriş'ten düşer."),
   o("gbp", "Google İşletme Profili", "İşletmenin Google Arama ve Haritalar'daki profilidir: adres ya da hizmet bölgesi, çalışma saatleri, telefon, fotoğraflar ve yorumlar.",
     "Müşterinin geldiği bir konumu ya da belirli bir bölgede hizmeti olan işletmeler.",
     "\"Kadıköy veteriner\" aramasında haritada işletme kartı; yol tarifi, arama ve web sitesi düğmeleriyle görünür."),
   o("looker", "Data Studio (eski adıyla Looker Studio)", "Analytics, Ads, Search Console ve diğer kaynaklardaki verileri tek raporda birleştiren ücretsiz raporlama ve gösterge paneli aracıdır. Google Nisan 2026'da Looker Studio'nun adını yeniden Data Studio yaptı; mevcut raporlar kendiliğinden taşındı.",
     "Yöneticiye ya da müşteriye düzenli, tek sayfalık performans raporu verilecekse.",
     "Her pazartesi yöneticinin e-postasına trafik, dönüşüm, reklam harcaması ve arama tıklamalarını gösteren rapor gider.")]},
 {"id": "gg_owner", "label": "Hesapların Sahipliği", "en": "Account Ownership", "type": "select",
  "explanation": "Google hesaplarının hangi hesap altında açılacağını belirler. Sahip olan hesap, verinin, reklam geçmişinin, faturaların ve kullanıcı yetkilerinin de sahibidir.",
  "scenario": "Kurumun kendi alan adlı e-postası (Google Workspace ya da başka bir e-posta sağlayıcısındaki adresle açılmış Google hesabı) her durumda önerilir.",
  "example": "Hesaplar pazarlama@ornek.com.tr adıyla açılır; ajans kendi e-postasıyla Standart / Düzenleyici kullanıcı olarak eklenir, sözleşme bitince erişimi kaldırılır.",
  "rule": "Google hesaplarının sahipliği: {label}.",
  "options": [
   o("org", "Kurumun alan adlı ortak hesabı (önerilen)", "Hesaplar kurumun kendi alan adındaki ortak bir adresle açılır (ör. dijital@ornek.com.tr); bu adres kişiye değil göreve bağlıdır.",
     "Her kurum ve işletme için.", "Pazarlama müdürü değişse de hesaplar, veriler ve faturalar kurumda kalır.",
     "Google hesapları kurumun alan adlı ortak adresiyle açılır; sahiplik kişisel ya da ajans hesabına verilmez, en az iki kurum çalışanı sahip / yönetici olur."),
   o("person", "Bir çalışanın kurumsal hesabı", "Hesaplar bir çalışanın kurumsal adresiyle açılır; çalışan ayrılınca sahipliğin devredilmesi gerekir.",
     "Tek kişilik ya da çok küçük işletmeler.", "Çalışan ayrılmadan önce sahiplik ortak adrese ya da başka bir yöneticiye devredilir.",
     "Hesaplar bir çalışanın kurumsal hesabıyla açılır; ikinci bir sahip / yönetici zorunludur ve çalışan ayrılmadan sahiplik devredilir."),
   o("agency", "Ajansın hesabı", "Hesap ajansın yönetici hesabında açılır; kurum yalnız kullanıcı olarak eklenir. Ayrılıkta veri ve reklam geçmişi kurumda kalmayabilir.",
     "Yalnız sözleşmede hesap devri açıkça yazılıysa ve kısa süreli kampanyalarda.", "Ajansla çalışma bitince Ads hesabının sahipliği kuruma devredilir; devir maddesi sözleşmede yoktur ve geçmiş veri kaybolur.",
     "Hesaplar ajans altında açılacaktır; sözleşmede hesap ve veri devri maddesi bulunur, kurum en az bir yönetici kullanıcıyla eklenir.")]},
 {"id": "gg_access", "label": "Erişim ve Güvenlik Kuralları", "en": "Access & Security Rules", "type": "multiselect",
  "explanation": "Google hesaplarına kimin, hangi yetkiyle erişeceğine ve hesapların nasıl korunacağına dair asgari kuralları belirler.",
  "scenario": "İlk üç madde her projede asgari kabul edilir; ajansla çalışılıyorsa ajans maddesi, birden çok kişinin eriştiği hesaplarda dönemsel gözden geçirme eklenir.",
  "example": "Analytics'te pazarlama uzmanı Analist, ajans Pazarlamacı, yönetici Görüntüleyici yetkisindedir; yılda dört kez liste kontrol edilir.",
  "rule": "Google hesaplarında erişim ve güvenlik kuralları: {labels}.",
  "options": [
   o("two_admins", "En az iki sahip / yönetici", "Her serviste en az iki kurum çalışanı en yüksek yetkiye sahiptir.", "Her proje.", "Bir yöneticinin hesabı kilitlenince diğeri erişimi kurtarır.",
     "Her Google servisinde en az iki kurum çalışanı sahip / yönetici yetkisine sahiptir."),
   o("2sv", "İki adımlı doğrulama zorunlu", "Hesaplara erişen bütün kullanıcılarda iki adımlı doğrulama (tercihen geçiş anahtarı ya da güvenlik anahtarı) açıktır.", "Her proje.", "Çalınan bir parola tek başına reklam hesabına girmek için yetmez.",
     "Google hesaplarına erişen bütün kullanıcılarda iki adımlı doğrulama açıktır; mümkünse geçiş anahtarı (passkey) ya da güvenlik anahtarı kullanılır."),
   o("least", "En düşük yetki", "Her kullanıcıya işini yapmaya yetecek en düşük rol verilir: rapor okuyan Görüntüleyici, kampanya yöneten Standart, etiket hazırlayan ama yayımlamayan Düzenleyici.", "Her proje.", "Raporları izleyen yönetici Analytics'te yalnız Görüntüleyici'dir; yanlışlıkla ayar değiştiremez.",
     "Kullanıcılara işlerine yetecek en düşük rol verilir (Analytics'te Görüntüleyici / Analist / Pazarlamacı, Ads'te Salt okunur / Standart, Tag Manager'da Okuma / Düzenleme / Onaylama); yönetici yetkisi yalnız sahip ve yöneticilerdedir."),
   o("agency", "Ajans ve serbest çalışan ayrı kullanıcı", "Dış ekipler kurumun hesabını paylaşmaz; kendi e-postalarıyla ayrı kullanıcı olarak eklenir ve iş bitince çıkarılır.", "Ajans, serbest çalışan ya da danışmanla çalışılıyorsa.", "Ajansla sözleşme bitince ajans kullanıcıları aynı gün kaldırılır.",
     "Ajans ve serbest çalışanlar kendi e-postalarıyla ayrı kullanıcı olarak eklenir; ortak parola paylaşılmaz, iş bitince erişimleri aynı gün kaldırılır."),
   o("review", "Üç ayda bir erişim gözden geçirme", "Bütün servislerdeki kullanıcı listesi düzenli aralıklarla kontrol edilir; ayrılanlar ve gereğinden yüksek yetkiler temizlenir.", "Birden çok kişinin ya da dış ekibin eriştiği hesaplar.", "Ocak kontrolünde altı ay önce ayrılan bir stajyerin Ads erişimi bulunup kaldırılır.",
     "Bütün Google servislerindeki kullanıcı listesi üç ayda bir gözden geçirilir; ayrılan kişiler ve gereğinden yüksek yetkiler kaldırılır."),
   o("inventory", "Hesap ve kimlik envanteri", "Hangi serviste hangi hesap, mülk, kapsayıcı ve kimliğin bulunduğu, sahibi ve yöneticileri tek bir listede tutulur.", "Her proje; özellikle birden çok site ya da marka yönetiliyorsa.", "Envanterde GA4 mülk kimliği, Tag Manager kapsayıcı kimliği ve Ads müşteri kimliği sahipleriyle birlikte yazılıdır.",
     "Google hesap ve kimlik envanteri tutulur (servis, hesap / mülk / kapsayıcı adı, kimlik, sahip, yöneticiler); kimlikler Ortak Bilgiler › Hesap ve Etiket Kimlikleri'ne de yazılır."),
   o("offboarding", "Ayrılan çalışanın erişimi aynı gün kaldırılır", "İşten ayrılma sürecine Google servislerindeki erişimin kaldırılması eklenir.", "Kurumsal ekipler.", "İK ayrılış listesinde \"Google Ads / Analytics / Tag Manager erişimini kaldır\" maddesi vardır.",
     "Çalışan ayrıldığında Google servislerindeki erişimi aynı gün kaldırılır; sahipse önce sahiplik devredilir.")]}]
SECTIONS[-1]["guide"]["resources"] = [
 r("Google Analytics: erişim ve veri kısıtlama yönetimi", "https://support.google.com/analytics/answer/9305587", "Yönetici, Düzenleyici, Pazarlamacı, Analist ve Görüntüleyici rolleri; maliyet ve gelir metriklerini gizleme kısıtlamaları."),
 r("Google Ads: hesap erişim düzeyleri", "https://support.google.com/google-ads/answer/9978556?hl=tr", "Yönetici, Standart, Salt okunur, Faturalandırma ve Yalnız e-posta erişim düzeylerinin yapabildikleri."),
 r("Google Ads: iki adımlı doğrulama", "https://support.google.com/google-ads/answer/12864186?hl=tr", "Hesapta hassas işlemler için iki adımlı doğrulamayı zorunlu kılma (Yönetici › Erişim ve güvenlik › Güvenlik)."),
 r("Tag Manager: kullanıcılar ve izinler", "https://support.google.com/tagmanager/answer/6107011?hl=tr", "Hesap ve kapsayıcı düzeyindeki izinler: Okuma, Düzenleme, Onaylama, Yayınlama."),
 r("Search Console: kullanıcılar, sahipler ve izinler", "https://support.google.com/webmasters/answer/7687615?hl=tr", "Doğrulanmış sahip, yetki verilmiş sahip, tam ve kısıtlı kullanıcı; ayrılan sahibin doğrulama jetonunu da kaldırma."),
 r("İşletme Profili: sahipler ve yöneticiler", "https://support.google.com/business/answer/3403100?hl=tr", "Birincil sahip, sahip ve yönetici rolleri; yeni kullanıcıların ilk 7 gündeki kısıtları.")]

# 2 — Onay Modu (Consent Mode v2)
SECTIONS.append({
 "id": "gg_consent", "name": "Onay Modu (Consent Mode v2)", "en": "Consent Mode v2", "icon": "◐", "agents": ["K", "O"],
 "desc": "Google etiketlerinin çerez onayına göre nasıl çalışacağını belirler: temel ya da gelişmiş mod, varsayılan onay durumları, onay penceresiyle bağlantı ve doğrulama",
 "guide": {
  "purpose": "Consent Mode, ziyaretçinin çerez tercihini Google etiketlerine dört sinyalle iletir: ad_storage (reklam çerezleri), analytics_storage (analitik çerezleri), ad_user_data (reklam amacıyla kullanıcı verisinin Google'a gönderilmesi) ve ad_personalization (kişiselleştirilmiş reklam). Google'ın AB kullanıcı onayı politikası AEA, Birleşik Krallık ve İsviçre'deki ziyaretçiler içindir; Türkiye'de ise KVKK'nın Çerez Uygulamaları Hakkında Rehberi (Temmuz 2025) analitik ve reklam çerezleri için açık rıza ister. Bu yüzden Türkiye dahil bütün ziyaretçilerde varsayılan durum \"reddedildi\"dir; etiketler onay geldikçe güncellenir. Proje bölümündeki Çerez / Onay Platformu kararı onay penceresini, bu bölüm Google tarafındaki bağlantıyı belirler.",
  "criteria": [
   "Varsayılan onay komutu her sayfada bütün Google etiketlerinden önce çalışır; Tag Manager'da \"Consent Initialization – All Pages\" tetikleyicisindedir.",
   "Dört sinyalin varsayılanı Türkiye dahil bütün bölgelerde \"denied\"dır; ziyaretçi kabul ya da reddedince aynı sayfada update komutu gönderilir.",
   "Onay penceresinde Kabul et, Reddet ve Tercihler eşit görünürlüktedir; rıza gerektiren seçenekler ilk açılışta kapalıdır ve rıza her an geri alınabilir.",
   "Tag Assistant'ta ilk Consent olayı varsayılan değerleri, sonraki olay ziyaretçinin seçimini gösterir; reddedildiğinde analitik ve reklam çerezi yazılmaz."],
  "pitfalls": [
   "Varsayılan onay komutunu Google etiketinden ya da config komutundan sonra çalıştırmak: Google bu durumda varsayılanların uygulanmayacağını belirtir.",
   "Yalnız AEA için \"denied\" tanımlayıp Türkiye'yi \"granted\" bırakmak: KVKK rehberi analitik ve reklam çerezleri için açık rıza ister.",
   "Reddet düğmesini ikinci katmana gizlemek ya da kabulü renkle öne çıkarmak.",
   "Temel modda etiketleri engelleyip bir yandan gelişmiş moddaki modellemeyi beklemek; modelleme yalnız gelişmiş modda ve belirli trafik eşiklerinde çalışır.",
   "Google dışı etiketlerin (Meta, TikTok, LinkedIn) onay ayarını unutmak: Consent Mode yalnız Google etiketlerini yönetir; diğerleri Tag Manager'da ek onay koşuluyla tetiklenir."],
  "resources": [
   r("Web sitelerinde onay modunu kurma", "https://developers.google.com/tag-platform/security/guides/consent", "Varsayılan ve güncelleme komutları, bölgeye göre varsayılan (ISO 3166-2), wait_for_update, url_passthrough, ads_data_redaction."),
   r("Onay modu hakkında (Google Ads)", "https://support.google.com/google-ads/answer/10000067?hl=tr", "Temel ve gelişmiş modun farkı; onay yokken etiketlerin davranışı."),
   r("AEA trafiği için onay modu güncellemeleri", "https://support.google.com/google-ads/answer/13695607?hl=tr", "ad_user_data ve ad_personalization sinyalleri; kendi onay penceresi ile sertifikalı CMP kullananların yapması gerekenler."),
   r("Onay modu için davranışsal modelleme (GA4)", "https://support.google.com/analytics/answer/11161109?hl=tr", "Modelleme koşulları: gelişmiş mod, günlük olay ve kullanıcı eşikleri, Karma raporlama kimliği."),
   r("Tag Manager'da onay modu desteği", "https://support.google.com/tagmanager/answer/10718549?hl=tr", "Onaya genel bakış (Consent Overview), Consent Initialization tetikleyicisi, etiket bazında ek onay ayarı."),
   r("Google AB kullanıcı onayı politikası", "https://www.google.com/about/company/user-consent-policy/", "Politikanın AEA, Birleşik Krallık ve İsviçre'deki son kullanıcılar için geçerli olduğu kapsam."),
   r("Google CMP İş Ortağı Programı", "https://cmppartnerprogram.withgoogle.com/", "Consent Mode ile bütünleşik onay yönetim platformlarının (CMP) güncel listesi."),
   r("KVKK — Çerez Uygulamaları Hakkında Rehber", "https://kvkk.gov.tr/Icerik/7353/Cerez-Uygulamalari-Hakkinda-Rehber", "Rızasız kullanılabilen zorunlu çerezler, rıza panelinin iyi uygulamaları (eşit düğmeler, ilk açılışta pasif seçenekler, geri alma); çerezle yurt dışına aktarımda KVKK m. 9.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_cm_mode", "label": "Onay Modu Türü", "en": "Consent Mode Type", "type": "select", "showIf": SV("gtm", "ga4", "ads"),
  "explanation": "Ziyaretçi onay vermeden önce Google etiketlerinin hiç yüklenmeyeceğini (temel mod) ya da çerez yazmadan yüklenip çerezsiz sinyal göndereceğini (gelişmiş mod) belirler.",
  "scenario": "Türkiye'de KVKK açısından en temkinli seçim temel moddur; gelişmiş mod daha fazla modellenmiş veri sağlar ama hukuki değerlendirme gerektirir.",
  "example": "Temel modda ziyaretçi Reddet'e basarsa Google'a hiçbir istek gitmez; gelişmiş modda çerezsiz bir sayım isteği gider ve GA4 eksik veriyi modelleyebilir.",
  "rule": "Google onay modu türü: {label}.",
  "options": [
   o("basic", "Temel mod — onaya kadar Google etiketi yüklenmez (önerilen)", "Etiketler ziyaretçi onay penceresine yanıt verene kadar hiç yüklenmez; reddedilirse Google'a hiçbir veri, onay durumu bile gitmez.",
     "Türkiye'de faaliyet gösteren ve hukuki riski en aza indirmek isteyen işletmeler; sağlık, finans, çocuk gibi hassas alanlar.",
     "Reddeden ziyaretçinin oturumu GA4'te hiç görünmez; Google yalnız genel bir modelleme uygular.",
     "Onay modu temel modda kurulur: Google etiketleri ilgili onay verilmeden yüklenmez, reddedilince Google'a istek gönderilmez; onay penceresi sinyalleri Consent Mode v2 update komutuyla iletir."),
   o("advanced", "Gelişmiş mod — etiketler yüklenir, onay yoksa çerezsiz sinyal", "Etiketler sayfayla birlikte yüklenir; onay yokken çerez yazmadan zaman damgası, tarayıcı ve yönlendiren bilgisi içeren sinyaller gönderilir. GA4 ve Ads bu sinyallerle eksik veriyi modelleyebilir.",
     "Hukuk ya da veri koruma görevlisinin değerlendirip onayladığı, reklam bütçesi yüksek ve modellenmiş dönüşüme ihtiyaç duyan projeler.",
     "Reddeden ziyaretçiler raporda tek tek görünmez ama dönüşüm sayısı modellemeyle tamamlanır.",
     "Onay modu gelişmiş modda kurulur; bu seçim hukuk / veri koruma görevlisinin yazılı değerlendirmesiyle yapılır, onay yokken çerez yazılmaz ve aydınlatma metninde çerezsiz sinyaller anlatılır."),
   o("none", "Google etiketi kullanılmayacak", "Sitede Google'ın ölçüm ya da reklam etiketi bulunmayacağı için onay modu kurulmaz.", "Yalnız Search Console ya da İşletme Profili kullanılan projeler.", "Sitede Google etiketi yoktur; çerez penceresi yalnız diğer çerezleri yönetir.",
     "Sitede Google etiketi bulunmayacağı için onay modu kurulmaz.")]},
 {"id": "gg_cm_defaults", "label": "Varsayılan Onay Ayarları", "en": "Default Consent Settings", "type": "multiselect", "showIf": SV("gtm", "ga4", "ads"),
  "explanation": "Sitede çalışacak varsayılan onay komutunun içeriğini ve sırasını belirler. Bu ayarlar kodla (ya da Tag Manager'daki onay şablonuyla) uygulanır.",
  "scenario": "İlk üç madde her kurulumda asgari kabul edilir; onay penceresi geç yükleniyorsa bekleme süresi, reklam varsa veri kırpma eklenir.",
  "example": "Sayfanın başında gtag('consent','default',{ad_storage:'denied', analytics_storage:'denied', ad_user_data:'denied', ad_personalization:'denied', wait_for_update:500}) çalışır; ziyaretçi analitiğe izin verince yalnız analytics_storage 'granted' olur.",
  "rule": "Varsayılan onay ayarları: {labels}.",
  "options": [
   o("deny_all", "Dört sinyal varsayılan olarak reddedildi", "ad_storage, analytics_storage, ad_user_data ve ad_personalization ziyaretçi seçim yapana kadar \"denied\"dır; Türkiye dahil bütün bölgelerde.", "Her kurulum.", "İlk ziyaretteki sayfa görüntülemesi analitik çerezi yazmaz.",
     "Dört onay sinyali (ad_storage, analytics_storage, ad_user_data, ad_personalization) bütün bölgelerde varsayılan olarak 'denied'dır; yalnız işlevsel ve güvenlik amaçlı depolama (functionality_storage, security_storage) 'granted' olabilir."),
   o("first", "Varsayılan komut her etiketten önce", "Varsayılan onay komutu sayfadaki bütün Google etiketlerinden, config ve event komutlarından önce çalışır.", "Her kurulum.", "Tag Manager'da onay penceresi etiketi ve varsayılan onay etiketi Consent Initialization – All Pages tetikleyicisinde çalışır.",
     "Varsayılan onay komutu her sayfada bütün Google etiketlerinden önce çalışır; Tag Manager kullanılıyorsa onay penceresi ve varsayılan onay etiketi Consent Initialization – All Pages tetikleyicisindedir."),
   o("update", "Seçim aynı sayfada güncellenir", "Ziyaretçi kabul ya da reddedince ve tercihlerini sonradan değiştirince update komutu hemen gönderilir; seçim sonraki sayfalarda da korunur.", "Her kurulum.", "Ziyaretçi analitiğe izin verdiği anda o sayfanın görüntülemesi ölçülmeye başlar.",
     "Ziyaretçi seçim yaptığında ya da tercihini değiştirdiğinde onay penceresi aynı sayfada gtag('consent','update', …) gönderir; seçim sonraki sayfalarda sayfa yüklenirken varsayılandan hemen sonra uygulanır."),
   o("wait", "Onay penceresini bekleme süresi", "Onay penceresi eşzamansız yükleniyorsa etiketlerin seçimi beklemesi için wait_for_update (ör. 500 ms) eklenir.", "Onay penceresi üçüncü taraf betikle sonradan yükleniyorsa.", "Geri dönen ve daha önce izin vermiş ziyaretçinin ilk sayfa görüntülemesi kaybolmaz.",
     "Varsayılan onay komutunda wait_for_update: 500 kullanılır."),
   o("redact", "Reklam verisini kırpma", "ad_storage reddedildiğinde reklam tıklama bilgilerinin istekten çıkarılması için ads_data_redaction: true kullanılır.", "Google Ads etiketi olan sitelerde.", "Reklamdan gelip reddeden ziyaretçinin tıklama kimliği reklam isteklerine eklenmez.",
     "ads_data_redaction: true ayarlanır; ad_storage reddedildiğinde reklam tıklama tanımlayıcıları isteklere eklenmez."),
   o("region", "Bölgeye göre ayrı varsayılan", "AEA, Birleşik Krallık ve İsviçre için ayrı (daha belirli) bir varsayılan tanımlanır; Türkiye ve diğer bölgeler de yine reddedildi başlar.", "Yurt dışından da ziyaretçi alan siteler.", "region: ['TR'] ve AEA ülkeleri için ayrı komut; daha belirli bölge önceliklidir.",
     "Varsayılan onay komutu bölgeye göre de tanımlanır (region parametresi, ISO 3166-2); hiçbir bölgede analitik ya da reklam sinyali onaysız 'granted' başlamaz."),
   o("passthrough", "Reddedilince URL'de tıklama bilgisi (url_passthrough)", "Çerez reddedilince reklam tıklama bilgisini sayfalar arasında adres satırında taşır. Kişisel veri boyutu olduğu için yalnız hukuki değerlendirmeden sonra açılır.", "Yalnız hukuk onayıyla, reklam ölçümü kritik projelerde.", "Reddeden ziyaretçinin gclid parametresi iç bağlantılara eklenir.",
     "url_passthrough yalnız hukuk / veri koruma görevlisinin yazılı onayıyla açılır ve aydınlatma metninde anlatılır.")]},
 {"id": "gg_cm_checks", "label": "Onay Doğrulama ve Uyum Kontrolleri", "en": "Consent Verification Checks", "type": "multiselect", "showIf": SV("gtm", "ga4", "ads"),
  "explanation": "Onay modunun doğru çalıştığını kanıtlamak ve KVKK'nın çerez rehberine uygun bir onay penceresi sağlamak için yayından önce ve sonra yapılacak kontrolleri belirler.",
  "scenario": "Yayından önce bütün kontroller yapılır; sonraki her etiket değişikliğinde onay testi tekrarlanır.",
  "example": "Tag Assistant'ta Reddet sonrası Consent olayında dört sinyal 'denied' görünür, tarayıcının çerezlerinde _ga yoktur.",
  "rule": "Onay doğrulama ve uyum kontrolleri: {labels}.",
  "options": [
   o("tag_assistant", "Tag Assistant ile onay testi", "Tag Assistant'ta ilk Consent olayı varsayılan değerleri, ziyaretçinin seçiminden sonraki olay güncel değerleri gösterir.", "Her kurulum.", "Kabul, Reddet ve yalnız analitik senaryoları ayrı ayrı denenir.",
     "Yayından önce Tag Assistant ile kabul, ret ve kısmi onay senaryoları denenir; ilk Consent olayı varsayılanları, sonraki olay seçimi göstermelidir."),
   o("no_cookie", "Onay öncesi çerez yok", "Tarayıcı geliştirici araçlarında ilk açılışta ve Reddet sonrasında analitik ve reklam çerezi (ör. _ga, _gcl_au) bulunmadığı kontrol edilir.", "Her kurulum.", "Uygulama › Çerezler sekmesinde Reddet sonrası yalnız onay çerezinin kendisi görünür.",
     "İlk açılışta ve Reddet sonrasında tarayıcıda analitik ve reklam çerezi (_ga, _gid, _gcl_au vb.) yazılmadığı geliştirici araçlarıyla doğrulanır."),
   o("equal", "Eşit düğmeler, varsayılan kapalı seçenekler", "Onay penceresinde Kabul et, Reddet ve Tercihler aynı renk, büyüklük ve puntodadır; rıza gerektiren kategoriler ilk açılışta kapalıdır.", "Her kurulum (KVKK çerez rehberinin iyi uygulaması).", "Üç düğme yan yana ve aynı görünümdedir; tercihler panelinde analitik ve pazarlama anahtarları kapalı gelir.",
     "Onay penceresinde Kabul et, Reddet ve Tercihler eşit görünürlüktedir; rıza gerektiren kategoriler ilk açılışta kapalıdır, rıza kullanım koşullarına iliştirilmez ve aydınlatma metnine bağlantı verilir."),
   o("withdraw", "Rızayı geri alma her sayfada", "Ziyaretçi tercihini sayfanın köşesindeki küçük bir simge ya da alt bilgideki bağlantıyla her an değiştirebilir.", "Her kurulum.", "Sol alttaki çerez simgesi tercih panelini açar; analitiği kapatınca update komutu hemen gider.",
     "Ziyaretçi rızasını her sayfadan (köşe simgesi ya da alt bilgi bağlantısı) geri alabilir; geri alma aynı sayfada update komutuyla uygulanır."),
   o("non_google", "Google dışı etiketlerde ek onay koşulu", "Meta, TikTok, LinkedIn gibi etiketler Consent Mode'u okumaz; Tag Manager'da \"ek onay gerekir\" ayarıyla ya da onay penceresinin kategorisiyle tetiklenir.", "Google dışı reklam veya analitik etiketi varsa.", "Meta Pikseli yalnız ad_storage onayı varken çalışır.",
     "Google dışı etiketler (Meta, TikTok, LinkedIn, Clarity vb.) yalnız ilgili onay varken çalışır; Tag Manager'da her biri için \"Require additional consent for tag to fire\" ayarlanır."),
   o("log", "Onay kaydı", "Ziyaretçinin onay seçimi, tarih, metin sürümü ve kategori bazında kayıt altına alınır; kayıt kişisel veri içermeyecek biçimde tutulur.", "Hukuki ispat gereken her proje.", "Onay kaydında anonim kimlik, tarih, onay metni sürümü ve seçilen kategoriler durur.",
     "Onay seçimleri tarih, onay metni sürümü ve kategori bazında kaydedilir; kayıt gereksiz kişisel veri içermez ve saklama süresi tanımlıdır.")]}]

# 3 — Google Tag Manager
SECTIONS.append({
 "id": "gg_gtm", "name": "Google Tag Manager", "en": "Google Tag Manager", "icon": "⌗", "agents": ["O"],
 "desc": "Tag Manager kapsayıcısının kurulum yöntemini, siteye yerleşimini, sürüm ve yayımlama düzenini, kullanıcı izinlerini, onay ayarlarını ve etiket düzenini belirler",
 "guide": {
  "purpose": "Tag Manager, ölçüm ve reklam etiketlerini sitenin koduna her seferinde dokunmadan yönetmeyi sağlar. Kod siteye bir kez eklenir; sonraki her değişiklik Önizleme'de denenir ve ad ile açıklaması olan bir sürüm olarak yayımlanır. Kurulum adımları: tagmanager.google.com › Hesap oluştur (hesap adı, ülke) › kapsayıcı adı olarak alan adı ve tür Web › kurulum kodunu her sayfada <head>'in mümkün olan en üstüne ekleme › Önizleme ile test › Gönder › \"Yayınla ve sürüm oluştur\". Google'ın güncel kurulum kodu tek parçadır; eski kurulumlardaki <body> içindeki noscript parçasının kaldırılması gerekmez.",
  "criteria": [
   "Her sayfada tek bir kapsayıcı kodu, <head>'in en üstünde bulunur; aynı GA4 ya da Ads etiketi hem kodda hem Tag Manager'da yoktur.",
   "Yayımlama yetkisi bir iki kişidedir; her sürümün adı ve ne değiştiğini anlatan açıklaması vardır.",
   "Onaya genel bakış (Consent Overview) açıktır ve her etiketin onay ayarı tanımlıdır.",
   "Etiket, tetikleyici ve değişken adları bir adlandırma standardına uyar; kullanılmayan etiketler temizlenir."],
  "pitfalls": [
   "Önizleme yapmadan yayımlamak: hatalı bir tetikleyici bütün sayfalarda form gönderimini dönüşüm sayabilir.",
   "Herkese Yayınla yetkisi vermek ve sürüm açıklaması yazmamak: hangi değişikliğin veriyi bozduğu bulunamaz.",
   "Onay penceresini All Pages tetikleyicisinde çalıştırmak: etiketler onaydan önce çalışır.",
   "Özel HTML etiketlerine denetimsiz üçüncü taraf betik eklemek: güvenlik ve performans riski yaratır.",
   "Test ortamını canlı kapsayıcıyla ölçmek: test verisi canlı raporlara karışır."],
  "resources": [
   r("Tag Manager hesabı ve kapsayıcı oluşturma", "https://support.google.com/tagmanager/answer/14842164?hl=tr", "Hesap, kapsayıcı ve kapsayıcı türünün seçilmesi."),
   r("Web kapsayıcısını yükleme", "https://support.google.com/tagmanager/answer/12974036?hl=tr", "Güncel tek parçalı kurulum kodu ve yerleşimi."),
   r("Kapsayıcıları önizleme ve hata ayıklama", "https://support.google.com/tagmanager/answer/6107056?hl=tr", "Tag Assistant ile hangi etiketin hangi tetikleyiciyle çalıştığını görme."),
   r("Etiketleri doğrulama ve yayınlama", "https://support.google.com/tagmanager/answer/14842769?hl=tr", "Gönder, sürüm oluşturma ve yayımlama."),
   r("Tag Manager ve iki adımlı doğrulama", "https://support.google.com/tagmanager/answer/4525539?hl=tr", "Özel JavaScript, özel HTML ve kullanıcı ayarlarında iki adımlı doğrulama istenmesi."),
   r("Sunucu taraflı etiketleme", "https://developers.google.com/tag-platform/tag-manager/server-side", "Sunucu kapsayıcısının faydaları ve mimarisi."),
   r("Cloud Run ile sunucu taraflı kurulum", "https://developers.google.com/tag-platform/tag-manager/server-side/cloud-run-setup-guide", "Canlıda en az iki örnek, önizleme sunucusu ve özel alan adı."),
   r("Google tag gateway for advertisers", "https://developers.google.com/tag-platform/tag-manager/gateway", "Google etiketinin sitenin kendi alan adından sunulması (CDN ya da sunucu taraflı etiketleme ile)."),
   r("Google tag gateway — Cloudflare ile kurulum", "https://support.google.com/tagmanager/answer/16061406?hl=tr", "Cloudflare üzerinden gateway kurulumu ve Tag Assistant ile doğrulama.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_gtm_method", "label": "Etiket Yönetimi Yapısı", "en": "Tagging Architecture", "type": "select", "showIf": SV("gtm"),
  "explanation": "Tag Manager'ın yalnız tarayıcıda (web kapsayıcısı) mı çalışacağını, yoksa ölçüm isteklerinin kendi sunucunuzdan ya da alan adınızdan mı geçeceğini belirler.",
  "scenario": "Çoğu kurumsal site ve küçük e-ticaret için web kapsayıcısı yeterlidir; reklam bütçesi yüksek, veri kontrolü ve sayfa performansı kritikse sunucu taraflı etiketleme ya da Google tag gateway değerlendirilir.",
  "example": "Web kapsayıcısında GA4 ve Ads etiketleri ziyaretçinin tarayıcısından Google'a gider; sunucu taraflı yapıda istekler önce olcum.ornek.com.tr adresindeki sunucuya gelir, orada süzülüp iletilir.",
  "rule": "Etiket yönetimi yapısı: {label}.",
  "options": [
   o("web", "Web kapsayıcısı (önerilen)", "Tag Manager kodu sitenin her sayfasına eklenir; etiketler ziyaretçinin tarayıcısında çalışır.", "Kurumsal site, blog, küçük ve orta e-ticaret.", "Pazarlama ekibi yeni bir dönüşüm etiketini panelden ekleyip yayımlar.",
     "Tag Manager web kapsayıcısı kullanılır; kurulum kodu her sayfada <head>'in mümkün olan en üstünde bir kez bulunur, kapsayıcı kimliği yapılandırmadan okunur."),
   o("server", "Web kapsayıcısı + sunucu taraflı etiketleme", "Tarayıcıdaki istekler önce kendi alt alan adınızdaki sunucu kapsayıcısına gider; veri orada süzülür ve hedeflere iletilir. Barındırma maliyeti ve bakım ister.", "Reklam bütçesi yüksek, çok sayıda reklam platformuna veri gönderen ve veri kontrolü isteyen projeler.", "olcum.ornek.com.tr adresindeki sunucu kapsayıcısı GA4 ve Ads isteklerini alır, IP adresini ve gereksiz parametreleri çıkarıp iletir.",
     "Web kapsayıcısına ek olarak sunucu taraflı Tag Manager kurulur: kendi alt alan adında, canlıda en az iki örnekle, ayrı bir önizleme sunucusuyla; sunucuda kişisel veri süzülür ve onay sinyali hedeflere iletilir."),
   o("gateway", "Web kapsayıcısı + Google tag gateway", "Google etiketi ve ölçüm istekleri sitenin kendi alan adından (CDN üzerinden) sunulur. Onay gereğini kaldırmaz; yalnız ölçümün sunulduğu yeri değiştirir.", "Sitesi Cloudflare gibi desteklenen bir CDN arkasında olan ve sunucu kapsayıcısı işletmek istemeyen projeler.", "Etiket ornek.com.tr/olcum/ yolundan yüklenir; Tag Assistant'ta gateway durumu \"Etkin\" görünür.",
     "Google tag gateway kurulur (CDN üzerinden, sitenin kendi alan adında ölçüm yolu); sitedeki bütün etiket adresleri yeni yola güncellenir, Consent Mode ayarları değişmeden kalır ve kurulum Tag Assistant ile doğrulanır.")]},
 {"id": "gg_gtm_settings", "label": "Tag Manager Asgari Ayarları", "en": "Tag Manager Minimum Settings", "type": "multiselect", "showIf": SV("gtm"),
  "explanation": "Tag Manager kapsayıcısında yapılması gereken asgari ayarları ve çalışma kurallarını belirler.",
  "scenario": "İlk beş madde her kurulumda asgari kabul edilir; test ortamı varsa Ortamlar, birden çok kişi çalışıyorsa adlandırma ve özel HTML kuralı eklenir.",
  "example": "Sürüm 14: \"GA4 – generate_lead etiketi eklendi, iletişim formu teşekkür tetikleyicisi\" açıklamasıyla, Önizleme'den sonra yayımlanır.",
  "rule": "Tag Manager asgari ayarları: {labels}.",
  "options": [
   o("snippet", "Tek kapsayıcı kodu, <head>'in en üstünde", "Kurulum kodu her sayfaya bir kez, <head>'in mümkün olan en üstüne eklenir; aynı etiket hem kodda hem kapsayıcıda bulunmaz.", "Her kurulum.", "Sayfa kaynağında GTM-XXXX yalnız bir kez geçer; ayrıca gömülü gtag kodu yoktur.",
     "Tag Manager kodu her sayfada <head>'in mümkün olan en üstünde yalnız bir kez bulunur; aynı GA4 ya da Ads etiketi hem sitenin kodunda hem kapsayıcıda yer almaz (çift sayım)."),
   o("preview", "Her değişiklik Önizleme'de denenir", "Yayından önce Tag Assistant önizlemesiyle hangi etiketin hangi tetikleyiciyle çalıştığı ya da engellendiği kontrol edilir.", "Her kurulum.", "Önizlemede form gönderiminde generate_lead etiketinin bir kez çalıştığı görülür.",
     "Her kapsayıcı değişikliği yayımlanmadan önce Önizleme (Tag Assistant) ile denenir."),
   o("versions", "Sürüm adı ve açıklaması", "Her yayın, ne değiştiğini anlatan ad ve açıklamayla sürüm olarak kaydedilir; sorun çıkınca önceki sürüme dönülür.", "Her kurulum.", "Hatalı sürüm 15'ten sonra sürüm 14 yeniden yayımlanır.",
     "Her yayın ad ve açıklamalı bir sürümdür; sorun çıkarsa önceki sürüm yeniden yayımlanır."),
   o("permissions", "Yayımlama yetkisi sınırlı, iki adımlı doğrulama açık", "Kapsayıcıda Yayınla izni bir iki kişidedir, diğerleri Düzenleme ya da Onaylama yetkisindedir; hesapta hassas işlemler için iki adımlı doğrulama zorunludur.", "Her kurulum.", "Ajans etiketi hazırlar ve onaya sunar; kurumun ölçüm uzmanı yayımlar.",
     "Kapsayıcıda Yayınla izni en fazla iki kişidedir, diğer kullanıcılar Düzenleme ya da Onaylama yetkisindedir; Yönetici › Hesap Ayarları'nda belirli işlemler için iki adımlı doğrulama zorunludur."),
   o("consent", "Onaya genel bakış açık, her etiketin onay ayarı tanımlı", "Kapsayıcı Ayarları'nda onaya genel bakış açılır; her etiket \"onay yapılandırıldı\" durumundadır.", "Onay penceresi olan her site.", "Etiketler ekranındaki onay simgesinde \"Onay yapılandırılmadı\" listesi boştur.",
     "Kapsayıcı Ayarları'nda onaya genel bakış (Consent Overview) açıktır; bütün etiketlerin onay ayarı tanımlıdır, onay yapılandırılmamış etiket yayımlanmaz."),
   o("environments", "Test ortamı için ayrı ortam ya da kapsayıcı", "Test ortamı canlıyla aynı kapsayıcıyı aynı ortamla kullanmaz; Tag Manager Ortamları (Environments) ya da ayrı bir kapsayıcı kullanılır.", "Test / hazırlık ortamı olan projeler.", "Test sitesi \"Hazırlık\" ortamının koduyla çalışır ve test GA4 mülküne veri gönderir.",
     "Test ortamı Tag Manager Ortamları ya da ayrı kapsayıcıyla çalışır; test trafiği canlı mülke ve reklam hesabına gitmez."),
   o("naming", "Adlandırma standardı", "Etiket, tetikleyici ve değişken adları \"Araç – Tür – Ayrıntı\" biçimindedir (ör. GA4 – Olay – generate_lead).", "Birden çok kişinin çalıştığı ya da çok etiketli kapsayıcılar.", "Tetikleyici: \"Form – Gönderim – İletişim\"; değişken: \"DL – form_id\".",
     "Etiket, tetikleyici ve değişken adları \"Araç – Tür – Ayrıntı\" biçimindedir; kullanılmayan etiketler ve tetikleyiciler üç ayda bir temizlenir."),
   o("custom_html", "Özel HTML etiketleri denetimli", "Özel HTML etiketleri yalnız şablon bulunmayan durumda, kod incelemesinden sonra eklenir; Topluluk Şablon Galerisi tercih edilir.", "Üçüncü taraf betik eklenen kapsayıcılar.", "Bir sohbet aracının betiği özel HTML yerine galerideki şablonuyla eklenir.",
     "Özel HTML etiketi yalnız hazır şablon yoksa ve kod incelemesinden sonra eklenir; Topluluk Şablon Galerisi'ndeki şablonlar tercih edilir.")]}]

# 4 — Google Analytics 4
SECTIONS.append({
 "id": "gg_ga4", "name": "Google Analytics 4", "en": "Google Analytics 4", "icon": "◔", "agents": ["A", "O"],
 "refs": ["domain_name", "staging_url", "mk_ids"],
 "desc": "GA4 hesap ve mülk yapısını, mülkte yapılacak asgari ayarları, ölçülecek olayları ve anahtar etkinlikleri, diğer Google ürünleriyle bağlantıları belirler",
 "guide": {
  "purpose": "GA4 olay bazlı çalışır: her sayfa görüntüleme, form gönderimi ya da satın alma bir olaydır; işletme için sonuç anlamı taşıyan olaylar \"anahtar etkinlik\" (2024'e kadar \"dönüşüm\") olarak işaretlenir. Kurulum adımları: analytics.google.com › Yönetici › Oluştur › Hesap › Mülk (ad, raporlama saat dilimi, para birimi) › Veri akışı › Web (site adresi, akış adı, gelişmiş ölçüm) › ölçüm kimliğini (G- ile başlar) Tag Manager'a ya da siteye ekleme › Gerçek zamanlı rapor ve Tag Assistant ile doğrulama. Bu bölümdeki ayarların çoğu panelde, olaylar ise sitede (dataLayer) yapılır.",
  "criteria": [
   "Mülkün saat dilimi İstanbul, para birimi TRY (ya da işletmenin raporladığı para birimi); veri saklama 14 ay.",
   "Dahili ve geliştirici trafiği filtrelenir, ödeme sağlayıcıları istenmeyen yönlendirme listesindedir.",
   "Yalnız işletme sonucunu gösteren olaylar anahtar etkinliktir; olay adları Google'ın önerilen adlarıyla (generate_lead, purchase …) aynıdır.",
   "Sayfa adreslerine, olay parametrelerine ve form alanlarına kişisel veri (e-posta, telefon, ad) yazılmaz.",
   "Google Ads ve Search Console bağlantıları kuruludur; kişiselleştirilmiş reklam ayarı onay ve hukuki değerlendirmeye göre ayarlanır."],
  "pitfalls": [
   "Veri saklamayı 2 ayda bırakmak: keşif ve huni raporlarında geçmiş veri kaybolur.",
   "Dahili trafik filtresini test etmeden \"Etkin\" yapmak: dışlanan veri geri gelmez; önce \"Test\" durumunda denenir.",
   "Ödeme sağlayıcısından dönüşü istenmeyen yönlendirmeye eklememek: satışlar ödeme sağlayıcısından gelmiş görünür.",
   "Aynı etiketi hem kodda hem Tag Manager'da kurmak ya da enhanced measurement form olaylarıyla özel form olayını birlikte saymak: olaylar iki kez sayılır.",
   "Her olayı anahtar etkinlik yapmak: reklam optimizasyonu ve raporlar anlamsızlaşır (standart mülkte en çok 30 anahtar etkinlik)."],
  "resources": [
   r("Web sitesi için Analytics kurulumu", "https://support.google.com/analytics/answer/9304153?hl=tr", "Hesap, mülk, veri akışı ve etiket kurulum adımları."),
   r("Veri saklama", "https://support.google.com/analytics/answer/7667196?hl=tr", "2 / 14 ay seçenekleri; saklamanın yalnız keşif ve huni raporlarını etkilemesi."),
   r("Dahili trafiği filtreleme", "https://support.google.com/analytics/answer/10104470?hl=tr", "IP kuralı tanımı, filtrenin Test ve Etkin durumları."),
   r("İstenmeyen yönlendirmeleri belirleme", "https://support.google.com/analytics/answer/10327750?hl=tr", "Ödeme sağlayıcısı gibi ara alan adlarını yönlendirme sayılmaktan çıkarma."),
   r("Alanlar arası ölçüm", "https://support.google.com/analytics/answer/10071811?hl=tr", "Birden çok alan adında tek oturum; _gl parametresiyle doğrulama."),
   r("Gelişmiş ölçüm etkinlikleri", "https://support.google.com/analytics/answer/9216061?hl=tr", "Kendiliğinden ölçülen kaydırma, dış bağlantı, site içi arama, video, dosya indirme ve form olayları."),
   r("Önerilen etkinlikler", "https://support.google.com/analytics/answer/9267735?hl=tr", "generate_lead, sign_up, login, purchase gibi önerilen olay adları."),
   r("GA4 e-ticaret ölçümü", "https://developers.google.com/analytics/devguides/collection/ga4/ecommerce", "view_item … purchase olayları, items dizisi, currency ve transaction_id kuralları."),
   r("Etkinlikleri anahtar etkinlik olarak işaretleme", "https://support.google.com/analytics/answer/13128484?hl=tr", "Anahtar etkinlik oluşturma ve sınırları."),
   r("Google sinyalleri", "https://support.google.com/analytics/answer/9445345?hl=tr", "Signals veri toplamayı açma, bölgeye göre sınırlama."),
   r("Raporlama kimliği", "https://support.google.com/analytics/answer/10976610?hl=tr", "Karma, Gözlemlenen ve Cihaza dayalı kimlik; modellenmiş veri için Karma."),
   r("Veri silme istekleri", "https://support.google.com/analytics/answer/9940393?hl=tr", "Yanlışlıkla toplanan kişisel verinin silinmesi."),
   r("Google Ads'i Analytics'e bağlama", "https://support.google.com/analytics/answer/9379420?hl=tr", "Bağlantı için gereken roller ve kişiselleştirilmiş reklam ayarı."),
   r("Search Console'u Analytics'e bağlama", "https://support.google.com/analytics/answer/10737381?hl=tr", "Bir web akışı ile bir Search Console mülkü arasındaki bire bir bağlantı."),
   r("BigQuery dışa aktarımı", "https://support.google.com/analytics/answer/9358801?hl=tr", "Günlük ve akış dışa aktarımı, sınırlar ve maliyet."),
   r("Analytics'te yenilikler", "https://support.google.com/analytics/answer/9164320?hl=tr", "2026 değişiklikleri: AI Asistanı kanalı, panolar, ana makine adı filtresi, Data Manager.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_ga4_structure", "label": "Mülk ve Veri Akışı Yapısı", "en": "Property & Stream Structure", "type": "select", "showIf": SV("ga4"),
  "explanation": "GA4'te kaç mülk ve veri akışı kurulacağını, test ortamının ve birden çok alan adının nasıl ölçüleceğini belirler.",
  "scenario": "Tek siteli projelerde tek mülk ve tek web akışı yeterlidir; ödeme ya da rezervasyon başka bir alan adındaysa alanlar arası ölçüm, test ortamı varsa ayrı test mülkü eklenir.",
  "example": "ornek.com.tr ve randevu.ornek-sistem.com aynı mülkte, alanlar arası ölçümle tek oturum olarak görünür; test sitesi ayrı \"Test\" mülküne veri gönderir.",
  "rule": "GA4 mülk ve veri akışı yapısı: {label}.",
  "options": [
   o("single", "Tek mülk, tek web akışı (önerilen)", "Canlı site için bir mülk ve bir web veri akışı kurulur.", "Tek alan adlı kurumsal site, blog, e-ticaret.", "Bütün sayfalar G-XXXX kimliğiyle tek akışa veri gönderir.",
     "Canlı site için tek GA4 mülkü ve tek web veri akışı kurulur; mülk adı \"Marka – Site\" biçimindedir."),
   o("staging", "Canlı mülk + ayrı test mülkü", "Test ortamı ayrı bir mülke veri gönderir; canlı raporlar test trafiğiyle kirlenmez.", "Test / hazırlık ortamı olan ve sık yayın yapan projeler.", "Yayından önce yeni olay test mülkünde DebugView ile doğrulanır.",
     "Canlı ve test ortamı ayrı GA4 mülklerine veri gönderir; ölçüm kimliği ortama göre yapılandırmadan okunur."),
   o("cross", "Birden çok alan adı tek mülkte (alanlar arası ölçüm)", "Site ile ödeme, randevu ya da kayıt sistemi farklı alan adlarındaysa aynı mülk ve alanlar arası ölçümle tek oturum korunur.", "Ödeme, rezervasyon ya da üyelik başka alan adında çalışıyorsa.", "Randevu sayfasına geçişte adres satırında _gl parametresi görünür.",
     "Bütün alan adları aynı ölçüm kimliğini kullanır ve veri akışının alan ayarlarına eklenir; geçişlerde _gl parametresinin korunduğu doğrulanır."),
   o("web_app", "Web ve uygulama akışları aynı mülkte", "Mobil uygulama da varsa web ve uygulama akışları aynı mülkte toplanır.", "Web sitesi ve mobil uygulaması olan ürünler.", "Bir kullanıcının uygulamada başlayıp sitede tamamladığı satın alma aynı mülkte görünür.",
     "Web ve mobil uygulama veri akışları aynı GA4 mülkündedir; olay adları ve parametreler iki platformda aynıdır.")]},
 {"id": "gg_ga4_settings", "label": "GA4 Asgari Ayarları", "en": "GA4 Minimum Settings", "type": "multiselect", "showIf": SV("ga4"),
  "explanation": "GA4 mülkünde ve veri akışında yapılması gereken asgari ayarları belirler. Ayarların çoğu panelde (Yönetici menüsü) yapılır.",
  "scenario": "İlk beş madde her mülkte asgari kabul edilir; ödeme sağlayıcısı, reklam ya da kişisel veri riski varsa ilgili maddeler eklenir.",
  "example": "Yönetici › Veri ayarları › Veri saklama: 14 ay; Veri akışları › Etiket ayarları › Dahili trafiği tanımla: ofis IP'si; Veri filtreleri: Dahili trafik (Etkin).",
  "rule": "GA4 asgari ayarları: {labels}.",
  "options": [
   o("tz_currency", "Saat dilimi ve para birimi", "Mülkün raporlama saat dilimi ve para birimi işletmenin raporladığı değerlerle aynıdır.", "Her mülk.", "Saat dilimi (GMT+03:00) İstanbul, para birimi Türk lirası.",
     "Mülkün raporlama saat dilimi Türkiye (İstanbul) ve para birimi işletmenin raporladığı para birimidir (genellikle TRY); e-ticaret olaylarındaki currency bununla tutarlıdır."),
   o("retention", "Veri saklama 14 ay", "Olay verisi standart mülkte en çok 14 ay saklanabilir; süre yalnız keşif ve huni raporlarını etkiler.", "Her mülk.", "Yıllık karşılaştırma keşif raporunda yapılabilir.",
     "Yönetici › Veri ayarları › Veri saklama 14 ay yapılır."),
   o("internal", "Dahili ve geliştirici trafiği filtresi", "Ofis ve ekip IP adresleri dahili trafik olarak tanımlanır; filtre önce Test durumunda denenir, sonra Etkin yapılır.", "Her mülk.", "Ekibin kendi ziyaretleri raporlara karışmaz.",
     "Ofis ve ekip IP adresleri dahili trafik olarak tanımlanır; dahili trafik ve geliştirici trafiği filtreleri önce Test durumunda doğrulanır, sonra Etkin yapılır (etkin filtrenin dışladığı veri geri gelmez)."),
   o("referrals", "İstenmeyen yönlendirmeler", "Ödeme sağlayıcısı, 3D Secure ve rezervasyon sistemi gibi ara alan adları yönlendirme sayılmaz.", "Ödeme ya da dış rezervasyon sistemi olan siteler.", "Satışlar ödeme sağlayıcısından değil reklamdan gelmiş görünür.",
     "Ödeme sağlayıcısı, 3D Secure ve dış rezervasyon / üyelik sistemlerinin alan adları veri akışının istenmeyen yönlendirmeler listesine eklenir."),
   o("enhanced", "Gelişmiş ölçüm gözden geçirildi", "Kendiliğinden ölçülen olaylar (kaydırma, dış bağlantı, site içi arama, video, dosya indirme, form) tek tek gözden geçirilir; özel olayla çakışan kapatılır.", "Her mülk.", "Form gönderimi özel generate_lead olayıyla ölçüldüğü için gelişmiş ölçümdeki form etkileşimleri kapatılır.",
     "Gelişmiş ölçüm olayları tek tek gözden geçirilir; özel olayla aynı işi ölçen gelişmiş ölçüm olayı kapatılır (çift sayım), site içi arama parametresi sitenin arama adresine göre ayarlanır."),
   o("no_pii", "Kişisel veri gönderilmez", "Sayfa adreslerine, olay parametrelerine ve kullanıcı özelliklerine e-posta, telefon, ad, T.C. kimlik numarası yazılmaz; form alanlarının değerleri ölçülmez.", "Her mülk.", "Teşekkür sayfası adresinde ?email=… yoktur; form olayında yalnız form_id gönderilir.",
     "GA4'e kişisel veri gönderilmez: sayfa adresleri, sorgu parametreleri, olay parametreleri ve kullanıcı özellikleri e-posta, telefon, ad ya da kimlik numarası içermez; yanlışlıkla toplanırsa veri silme isteğiyle temizlenir."),
   o("signals", "Google sinyalleri kapalı ya da onaya bağlı", "Google sinyalleri demografi ve cihazlar arası raporlar için Google hesabı verisini kullanır; açılacaksa reklam onayıyla ve hukuki değerlendirmeyle açılır.", "Reklam kitlesi oluşturulacaksa değerlendirilir; diğer durumlarda kapalı kalır.", "Sinyaller kapalıdır; demografi raporu kullanılmaz.",
     "Google sinyalleri varsayılan olarak kapalıdır; yalnız reklam kitlesi gerekiyorsa, ad_personalization onayına bağlı ve hukuki değerlendirmeyle açılır."),
   o("reporting_id", "Raporlama kimliği Karma", "Onay vermeyen ziyaretçiler için modellenmiş verinin raporlarda görünmesi Karma (Blended) raporlama kimliğiyle mümkündür.", "Gelişmiş onay modu kullanılan mülkler.", "Yönetici › Veri görüntüleme › Raporlama kimliği: Karma.",
     "Raporlama kimliği Karma (Blended) olarak ayarlanır."),
   o("user_data", "Kullanıcı tarafından sağlanan veri yalnız gerekiyorsa", "Kullanıcı tarafından sağlanan veri toplama (e-posta / telefonun özetlenerek gönderilmesi) yalnız gelişmiş dönüşümler için ve onayla açılır; sağlık sektöründe kullanılamaz.", "Google Ads gelişmiş dönüşümleri kurulacaksa.", "Özellik kapalıdır; yalnız Ads gelişmiş dönüşümleri kurulduğunda açılır.",
     "Kullanıcı tarafından sağlanan veri toplama yalnız Ads gelişmiş dönüşümleri gerekiyorsa, onaya bağlı ve SHA-256 özetlenmiş veriyle açılır; aksi hâlde kapalıdır."),
   o("roles", "Rol ve erişim düzeni", "Ajans ve dış kullanıcılar yalnız mülk düzeyinde ve en düşük rolle eklenir; maliyet / gelir metrikleri gerekiyorsa kısıtlanır.", "Birden çok kişinin eriştiği mülkler.", "Ajans Pazarlamacı, yönetim Görüntüleyici, ölçüm uzmanı Düzenleyici.",
     "GA4 kullanıcıları mülk düzeyinde en düşük rolle eklenir; Yönetici rolü yalnız iki sahiptedir, gerekirse gelir ve maliyet metrikleri kısıtlanır.")]},
 {"id": "gg_ga4_events", "label": "Ölçülecek Olaylar ve Anahtar Etkinlikler", "en": "Events & Key Events", "type": "multiselect", "showIf": SV("ga4"),
  "explanation": "Sitede kodla (dataLayer ya da gtag) gönderilecek olayları ve bunlardan hangilerinin anahtar etkinlik sayılacağını belirler. Olay adları Google'ın önerilen adlarıdır.",
  "scenario": "Pazarlama › Dönüşüm Olayları'nda seçilenler burada karşılığıyla önerilir; e-ticarette satın alma hunisinin bütün olayları seçilir.",
  "example": "İletişim formu başarıyla gönderilince dataLayer.push({event:'generate_lead', form_id:'iletisim'}) çalışır; GA4'te generate_lead anahtar etkinliktir.",
  "rule": "GA4'te ölçülecek olaylar: {labels}.",
  "recommend": {"field": "mk_conversions", "map": {"form": ["lead"], "phone": ["call"], "whatsapp": ["whatsapp"], "email": ["email"], "download": ["download"], "purchase": ["ecommerce"], "event_register": ["signup"]}},
  "options": [
   o("lead", "Form gönderimi — generate_lead (anahtar)", "Form sunucu tarafından başarıyla kaydedildikten sonra generate_lead olayı gönderilir; doğrulama hatasında gönderilmez.", "İletişim, teklif, randevu ya da başvuru formu olan siteler.", "Teklif formu gönderilince form_id: 'teklif' parametresiyle generate_lead çalışır.",
     "Form başarıyla kaydedilince generate_lead olayı (form_id parametresiyle, kişisel veri olmadan) gönderilir ve anahtar etkinlik olarak işaretlenir; değer biliniyorsa value ve currency eklenir."),
   o("call", "Telefon tıklaması — click_to_call (anahtar)", "tel: bağlantısına tıklama özel olayla ölçülür; GA4'ün dış bağlantı ölçümü tel: bağlantılarını saymaz.", "Telefonla dönüşüm alan işletmeler.", "Mobilde \"Hemen ara\" düğmesine dokunulunca click_to_call çalışır.",
     "tel: bağlantılarına tıklama click_to_call olayıyla (link_location parametresiyle) ölçülür ve anahtar etkinliktir; numara parametreye yazılmaz."),
   o("whatsapp", "WhatsApp tıklaması — whatsapp_click (anahtar)", "wa.me ya da api.whatsapp.com bağlantısına tıklama özel olayla ölçülür.", "WhatsApp'tan iletişim alan işletmeler.", "Sağ alttaki WhatsApp düğmesine tıklanınca whatsapp_click çalışır.",
     "WhatsApp bağlantılarına tıklama whatsapp_click olayıyla ölçülür ve anahtar etkinliktir."),
   o("email", "E-posta tıklaması — email_click", "mailto: bağlantısına tıklama ölçülür; adres parametreye yazılmaz.", "E-postayla iletişim alan siteler.", "İletişim sayfasındaki e-posta adresine tıklama ölçülür.",
     "mailto: bağlantılarına tıklama email_click olayıyla ölçülür; e-posta adresi parametreye yazılmaz."),
   o("download", "Dosya indirme — file_download", "Katalog, broşür ya da fiyat listesi indirmeleri gelişmiş ölçümle ya da özel olayla ölçülür.", "İndirilebilir doküman sunan siteler.", "Katalog PDF'i indirilince file_name parametresiyle file_download görünür.",
     "Dosya indirmeleri file_download olayıyla (file_name, file_extension) ölçülür; önemli dokümanlar anahtar etkinlik yapılabilir."),
   o("signup", "Üyelik ve giriş — sign_up / login", "Hesap oluşturma ve giriş, yöntem parametresiyle ölçülür.", "Üyelik ya da etkinlik kaydı olan siteler.", "Google ile kayıt olunca sign_up (method: 'google') çalışır.",
     "Üyelik ve giriş sign_up ve login olaylarıyla (method parametresiyle) ölçülür; sign_up anahtar etkinliktir, kullanıcı kimliği gönderilecekse yalnız takma (pseudonim) kimlik kullanılır."),
   o("ecommerce", "E-ticaret hunisi — view_item … purchase (anahtar)", "Ürün listeleme, ürün görüntüleme, sepete ekleme, ödeme başlatma, kargo / ödeme bilgisi ve satın alma olayları items dizisiyle gönderilir.", "Online satış yapan siteler.", "Ödeme tamamlanınca transaction_id, value, currency, tax, shipping ve items ile purchase çalışır.",
     "E-ticaret olayları (view_item_list, select_item, view_item, add_to_cart, remove_from_cart, view_cart, begin_checkout, add_shipping_info, add_payment_info, purchase, refund) items dizisiyle gönderilir; her öğede item_id ya da item_name, value gönderilen her olayda currency, purchase ve refund'da benzersiz transaction_id bulunur; purchase anahtar etkinliktir ve sayfa yenilenince yeniden gönderilmez."),
   o("search", "Site içi arama — search", "Site içi arama gelişmiş ölçümle ya da arama terimi parametresiyle ölçülür.", "Arama kutusu olan siteler.", "\"kombi bakımı\" araması search_term parametresiyle raporlanır.",
     "Site içi arama view_search_results ya da search olayıyla (search_term) ölçülür; aramada kişisel veri girilebileceği için terimler raporda gözden geçirilir.")]},
 {"id": "gg_ga4_links", "label": "GA4 Ürün Bağlantıları", "en": "GA4 Product Links", "type": "multiselect", "showIf": SV("ga4"),
  "explanation": "GA4 mülkünün hangi Google ürünlerine bağlanacağını belirler (Yönetici › Ürün bağlantıları).",
  "scenario": "Reklam veriliyorsa Google Ads, arama trafiği önemliyse Search Console bağlantısı asgaridir; ham veri analizi gerekiyorsa BigQuery eklenir.",
  "example": "Ads bağlantısıyla generate_lead anahtar etkinliği Ads'e dönüşüm olarak alınır; Search Console bağlantısıyla Organik arama sorguları GA4'te görünür.",
  "rule": "GA4 ürün bağlantıları: {labels}.",
  "recommend": {"field": "gg_services", "map": {"ads": ["ads"], "gsc": ["gsc"], "merchant": ["merchant"]}},
  "options": [
   o("ads", "Google Ads", "Ads tıklamaları ve maliyetleri GA4'e, anahtar etkinlikler ve kitleler Ads'e aktarılır. GA4'te Düzenleyici, Ads'te Yönetici yetkisi gerekir.", "Google Ads kullanılan her proje.", "Ads kampanyalarının maliyeti ve getirdiği formlar GA4'te birlikte görünür.",
     "GA4 Google Ads hesabına bağlanır; kişiselleştirilmiş reklam ayarı onay sinyaline ve hukuki değerlendirmeye göre ayarlanır."),
   o("gsc", "Search Console", "Organik arama sorguları ve açılış sayfaları GA4 raporlarında görünür; bir web akışı yalnız bir Search Console mülküne bağlanır.", "Organik trafik önemli olan siteler.", "Kitaplık'tan yayımlanan Search Console raporlarında sorgu ve açılış sayfası verisi görünür.",
     "GA4 web akışı Search Console mülküne bağlanır ve Search Console raporları Kitaplık'tan yayımlanır."),
   o("bigquery", "BigQuery", "Ham olay verisi BigQuery'ye günlük aktarılır; standart mülkte günlük 1 milyon olay sınırı vardır.", "Ham veriyle analiz, CRM birleştirme ya da uzun süreli saklama gerekiyorsa.", "Satış ekibinin CRM verisi ile GA4 olayları BigQuery'de birleştirilir.",
     "GA4 günlük dışa aktarımla BigQuery'ye bağlanır; veri kümesi bölgesi, saklama süresi ve erişim yetkileri tanımlanır."),
   o("merchant", "Merchant Center", "Ürün verisi ile site davranışı birlikte görünür; ücretsiz ürün listelemelerinden gelen trafik ayrı izlenir.", "Merchant Center kullanan e-ticaret siteleri.", "Ücretsiz listelemelerden gelen satışlar GA4'te ayrı görünür.",
     "GA4 Merchant Center hesabına bağlanır.")]}]

# 5 — Search Console
SECTIONS.append({
 "id": "gg_gsc", "name": "Search Console", "en": "Google Search Console", "icon": "⌕", "agents": ["T", "M"],
 "refs": ["domain_name", "staging_url", "mk_ids"],
 "desc": "Search Console mülk türünü ve doğrulama yöntemini, site haritası gönderimini, kullanıcı yetkilerini, bağlantıları ve düzenli izlenecek raporları belirler",
 "guide": {
  "purpose": "Search Console sitenin Google aramadaki durumunu gösterir: hangi sayfaların dizinde olduğu ve neden olmadığı, hangi sorgularla gösterim ve tıklama alındığı, Core Web Vitals, güvenlik sorunları ve manuel işlemler. Kurulum adımları: search.google.com/search-console › Mülk ekle › Alan (Domain) mülkü › alan adının DNS'ine TXT doğrulama kaydı (google-site-verification=…) › doğrula › Site haritaları › sitemap.xml gönder › Ayarlar › Kullanıcılar ve izinler. Alan mülkü http / https, www ve bütün alt alan adlarını tek mülkte toplar.",
  "criteria": [
   "Alan mülkü DNS TXT kaydıyla doğrulanmıştır ve doğrulama kaydı DNS'ten silinmez; yedek olarak ikinci bir doğrulama yöntemi eklenmiştir.",
   "Site haritası gönderilmiş ve \"Başarılı\" durumdadır; robots.txt'de site haritası adresi yazılıdır.",
   "En az iki doğrulanmış sahip vardır; diğer kişiler tam ya da kısıtlı kullanıcıdır.",
   "Sayfa dizine ekleme, Core Web Vitals, güvenlik ve manuel işlemler raporları düzenli izlenir."],
  "pitfalls": [
   "Yalnız URL ön eki mülkü açmak: http / https ve www verisi ayrı mülklere bölünür.",
   "Doğrulamadan sonra DNS'teki TXT kaydını silmek: doğrulama sürekli denetlenir, kayıt kalkınca yetki düşer.",
   "Ayrılan bir sahibi kullanıcılardan çıkarıp doğrulama jetonunu bırakmak: kişi yeniden doğrulayıp erişimi geri alabilir.",
   "Site haritasının dizine eklemeyi garanti ettiğini ya da kaldırma aracının kalıcı olduğunu sanmak (geçici kaldırma yaklaşık 6 ay sürer).",
   "Test ortamını dizine açık bırakmak: test sayfaları canlı sitenin yerine aramada görünebilir."],
  "resources": [
   r("Web sitesi mülkü ekleme", "https://support.google.com/webmasters/answer/34592?hl=tr", "Alan mülkü ve URL ön eki mülkünün farkı."),
   r("Site sahipliğini doğrulama", "https://support.google.com/webmasters/answer/9008080?hl=tr", "DNS TXT kaydı ve diğer doğrulama yöntemleri; kaydın silinmemesi."),
   r("Kullanıcılar, sahipler ve izinler", "https://support.google.com/webmasters/answer/7687615?hl=tr", "Sahip ve kullanıcı rolleri, sahip çıkarılırken jetonun silinmesi."),
   r("Site haritaları raporu", "https://support.google.com/webmasters/answer/7451001?hl=tr", "Site haritası gönderme ve durumları."),
   r("URL denetleme aracı", "https://support.google.com/webmasters/answer/9012289?hl=tr", "Dizindeki sürüm, canlı test ve dizine eklenme isteği."),
   r("Sayfa dizine ekleme raporu", "https://support.google.com/webmasters/answer/7440203?hl=tr", "Sayfaların neden dizine eklenmediği ve düzeltmeyi doğrulama."),
   r("Core Web Vitals raporu", "https://support.google.com/webmasters/answer/9205520?hl=tr", "LCP, INP ve CLS eşikleri; saha verisi."),
   r("Kaldırmalar aracı", "https://support.google.com/webmasters/answer/9689846?hl=tr", "Geçici kaldırma ve kalıcı kaldırma için gerekenler."),
   r("Toplu veri dışa aktarımı", "https://support.google.com/webmasters/answer/12918484?hl=tr", "Search Console verisinin BigQuery'ye günlük aktarımı."),
   r("Search Console markalı sorgu filtresi", "https://developers.google.com/search/blog/2025/11/search-console-branded-filter", "Markalı ve markasız sorguları ayıran filtre (yalnız üst düzey mülklerde).")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_gsc_property", "label": "Mülk Türü ve Doğrulama", "en": "Property Type & Verification", "type": "select", "showIf": SV("gsc"),
  "explanation": "Search Console mülkünün türünü ve sahipliğin nasıl doğrulanacağını belirler.",
  "scenario": "DNS yönetimine erişim varsa her durumda Alan mülkü önerilir; DNS'e erişilemiyorsa URL ön eki mülkü HTML etiketi ya da Tag Manager ile doğrulanır.",
  "example": "DNS'e google-site-verification=abc… TXT kaydı eklenir; mülk sc-domain:ornek.com.tr olarak görünür ve www, blog. ve https sayfaları tek mülkte toplanır.",
  "rule": "Search Console mülkü: {label}.",
  "options": [
   o("domain", "Alan mülkü — DNS TXT doğrulaması (önerilen)", "Bütün alt alan adlarını ve protokolleri kapsar; markalı sorgu filtresi gibi bazı özellikler yalnız üst düzey mülklerde çalışır.", "DNS yönetimine erişilebilen her proje.", "sc-domain:ornek.com.tr mülkü bütün sayfaları kapsar.",
     "Search Console'da Alan mülkü açılır ve DNS TXT kaydıyla doğrulanır; TXT kaydı DNS'ten silinmez ve DNS kayıt listesinde açıklamasıyla belgelenir, yedek olarak ikinci bir doğrulama yöntemi (HTML etiketi ya da Tag Manager) eklenir."),
   o("prefix", "URL ön eki mülkü", "Yalnız yazılan önekle başlayan adresleri kapsar (ör. https://www.ornek.com.tr/); HTML etiketi, dosya, Analytics ya da Tag Manager ile doğrulanabilir.", "DNS'e erişilemiyorsa ya da yalnız bir alt dizin ölçülecekse.", "https://www.ornek.com.tr/ mülkü http ve www'suz adresleri kapsamaz.",
     "Search Console'da canlı adresin URL ön eki mülkü açılır ve HTML etiketiyle doğrulanır; doğrulama etiketi bütün sayfalarda <head> içinde kalıcıdır."),
   o("both", "Alan mülkü + önemli bölümler için URL ön eki", "Genel görünüm Alan mülkünde, blog ya da dil klasörü gibi bölümler ayrı URL ön eki mülklerinde izlenir.", "Çok dilli ya da büyük sitelerde bölüm bazlı rapor isteniyorsa.", "ornek.com.tr/en/ için ayrı mülk İngilizce bölümün verisini ayrıca gösterir.",
     "Alan mülkü DNS TXT kaydıyla doğrulanır; dil klasörleri ya da büyük bölümler için ek URL ön eki mülkleri açılır.")]},
 {"id": "gg_gsc_settings", "label": "Search Console Asgari Ayarları", "en": "Search Console Minimum Settings", "type": "multiselect", "showIf": SV("gsc"),
  "explanation": "Search Console'da kurulumdan hemen sonra yapılacak ayarları ve düzenli kontrolleri belirler.",
  "scenario": "İlk dört madde her sitede asgari kabul edilir; ham veri analizi gerekiyorsa BigQuery, alan adı değişiyorsa adres değişikliği eklenir.",
  "example": "Yayın günü sitemap.xml gönderilir, GA4 bağlantısı kurulur; her ayın ilk iş günü Sayfa dizine ekleme ve Core Web Vitals raporları kontrol edilir.",
  "rule": "Search Console asgari ayarları: {labels}.",
  "options": [
   o("sitemap", "Site haritası gönderimi", "sitemap.xml Search Console'a gönderilir ve robots.txt'de yazılır; durumu \"Başarılı\" olmalıdır.", "Her site.", "Site haritası 312 adres keşfetti, durum Başarılı.",
     "sitemap.xml (ya da site haritası dizini) Search Console'a gönderilir, robots.txt'de Sitemap satırıyla yazılır ve durumu yayından sonra kontrol edilir."),
   o("users", "Sahip ve kullanıcı düzeni", "En az iki doğrulanmış sahip vardır; ajans ve ekip tam ya da kısıtlı kullanıcıdır. Ayrılan sahibin doğrulama jetonu da kaldırılır.", "Her site.", "Ajans tam kullanıcıdır; site sahibi ve kurumun BT sorumlusu doğrulanmış sahiptir.",
     "Search Console'da en az iki doğrulanmış sahip vardır, diğer kişiler tam / kısıtlı kullanıcıdır; ayrılan sahibin kullanıcı kaydıyla birlikte doğrulama jetonu da kaldırılır."),
   o("ga4", "GA4 bağlantısı", "Search Console mülkü GA4 web akışına bağlanır.", "GA4 kullanılan her site.", "GA4'te organik sorgular açılış sayfalarıyla birlikte görünür.",
     "Search Console mülkü GA4 web akışına bağlanır."),
   o("staging", "Test ortamı dizine kapalı", "Test ve hazırlık ortamı parola ya da noindex ile korunur; Search Console'a canlı mülk olarak eklenmez.", "Test ortamı olan her proje.", "test.ornek.com.tr parola korumalıdır; aramada görünmez.",
     "Test ve hazırlık ortamları parola korumalı ya da X-Robots-Tag: noindex ile dizine kapalıdır; canlıya geçişte test ortamından noindex taşınmaz."),
   o("monitor", "Aylık rapor kontrolü", "Sayfa dizine ekleme, Core Web Vitals, HTTPS, güvenlik sorunları ve manuel işlemler raporları ayda bir kontrol edilir; e-posta bildirimleri açık tutulur.", "Her site.", "Aylık kontrolde \"Tarandı – şu anda dizine eklenmedi\" sayısındaki artış fark edilir.",
     "Sayfa dizine ekleme, Core Web Vitals, HTTPS, güvenlik sorunları ve manuel işlemler raporları ayda bir kontrol edilir; Search Console e-posta bildirimleri sahiplerde açıktır."),
   o("bigquery", "BigQuery toplu veri dışa aktarımı", "Arama verisi günlük olarak BigQuery'ye aktarılır; ilk aktarım geçmiş veriyi içermez, bölüm son kullanma süresi ayarlanır.", "16 aydan uzun arama verisi saklanacaksa ya da büyük sitelerde.", "Yıllar arası sorgu karşılaştırması BigQuery'de yapılır.",
     "Search Console toplu veri dışa aktarımı BigQuery'ye açılır; veri kümesi konumu, bölüm son kullanma süresi ve erişim yetkileri tanımlanır."),
   o("migration", "Alan adı değişirse adres değişikliği", "Alan adı değişikliğinde 301 yönlendirmelerinden sonra Adres Değişikliği aracı kullanılır.", "Alan adı taşınacaksa.", "eskimarka.com'dan yenimarka.com.tr'ye geçişte araç kullanılır.",
     "Alan adı değişirse sayfa bazlı 301 yönlendirmeleri kurulduktan sonra Search Console Adres Değişikliği aracı kullanılır ve iki mülk birlikte izlenir.")]}]

# 6 — Google Ads
SECTIONS.append({
 "id": "gg_ads", "name": "Google Ads Hesap Kurulumu", "en": "Google Ads Account Setup", "icon": "◆", "agents": ["R", "P"],
 "refs": ["oc_legal_name", "oc_tax_ids", "mk_ids"],
 "desc": "Google Ads hesabının açılış biçimini, hesap düzeyindeki asgari ayarları, dönüşüm ölçümünün kaynağını, gelişmiş dönüşümleri ve diğer hesaplarla bağlantıları belirler; kampanya stratejisi Pazarlama › Google Ads'tedir",
 "guide": {
  "purpose": "Bu bölüm kampanyalardan önce yapılması gereken hesap kurulumunu kapsar. Kurulum adımları: (ajans ya da birden çok hesap varsa) önce yönetici hesabı (MCC) › reklam hesabını uzman modunda açma (Akıllı mod yalnız Akıllı kampanyalara izin verir) › saat dilimi ve para birimi (sonradan değiştirilemez) › faturalandırma profili ve vergi bilgileri › kullanıcılar ve iki adımlı doğrulama › otomatik etiketleme › GA4 bağlantısı › dönüşüm işlemleri ve gelişmiş dönüşümler › hesap düzeyi negatif anahtar kelimeler ve otomatik uygulanan önerilerin kapatılması › ilk kampanya. Türkiye'de gösterilen reklamlara Google ülkeye özgü bir düzenleyici ek ücret uygular; fatura ve vergi ayrıntıları mali müşavirle doğrulanır.",
  "criteria": [
   "Hesap kurumsal sahiplikte, yönetici hesabı altında ve uzman modunda açılmıştır; saat dilimi İstanbul, para birimi doğru seçilmiştir.",
   "Otomatik etiketleme açıktır; site adres satırındaki gclid ve benzeri parametreleri kabul eder.",
   "Her dönüşüm yalnız bir kaynaktan birincil olarak sayılır; teklif yalnız birincil dönüşümlerle çalışır.",
   "Otomatik uygulanan öneriler kapalıdır, hesap düzeyi negatif anahtar kelime listesi ve konum ayarı (Bulunma) bilinçli seçilmiştir.",
   "Dönüşüm ölçümü ve onay sinyalleri doğrulanmadan kampanya yayına alınmaz."],
  "pitfalls": [
   "Hesabı Akıllı modda açıp öyle bırakmak: Arama kampanyalarının ayrıntılı ayarlarına erişilemez.",
   "Saat dilimini ya da para birimini yanlış seçmek: değiştirilemez, yeni hesap açmak gerekir ve geçmiş veri taşınmaz.",
   "Aynı dönüşümü hem Ads etiketiyle hem GA4 içe aktarımıyla birincil saymak: dönüşümler iki kez sayılır, teklif bozulur.",
   "Arama kampanyasında Görüntülü Reklam Ağı genişletmesini ve \"Bulunma veya ilgi\" konum seçeneğini fark etmeden açık bırakmak.",
   "1 Haziran 2026'dan beri haftanın bazı günlerini kapatan reklam zamanlamalarında da aylık harcamanın günlük bütçenin 30,4 katına kadar çıkabileceğini hesaba katmamak."],
  "resources": [
   r("Yönetici hesabı oluşturma", "https://support.google.com/google-ads/answer/7459399?hl=tr", "Birden çok hesabı tek yerden yönetmek için yönetici hesabı (MCC)."),
   r("Akıllı mod", "https://support.google.com/google-ads/answer/9520605?hl=tr", "Akıllı modda yalnız Akıllı kampanyalar oluşturulabildiği."),
   r("Dil, saat dilimi ve para birimi ayarları", "https://support.google.com/google-ads/answer/9842104?hl=tr", "Saat dilimi ve para biriminin hesap açılışında kalıcı olarak belirlenmesi."),
   r("Ülkeye özgü ek ücretler", "https://support.google.com/google-ads/answer/9750227?hl=tr", "Türkiye'de gösterilen reklamlar için düzenleyici işletim maliyeti ek ücreti (1 Ocak 2027'den itibaren %2,5)."),
   r("Çok taraflı onay", "https://support.google.com/google-ads/answer/16891189?hl=tr", "Kullanıcı ve rol değişikliği gibi hassas işlemlerde ikinci yönetici onayı."),
   r("Otomatik etiketleme", "https://support.google.com/google-ads/answer/3095550?hl=tr", "gclid ile tıklama bilgisinin dönüşüm ölçümüne ve GA4'e taşınması."),
   r("Birincil ve ikincil dönüşüm işlemleri", "https://support.google.com/google-ads/answer/11461796?hl=tr", "Teklifte kullanılan ve yalnız gözlemlenen dönüşümler."),
   r("Gelişmiş dönüşüm ayarlarındaki güncellemeler", "https://support.google.com/google-ads/answer/16884284?hl=tr", "2026'da web ve potansiyel müşteri gelişmiş dönüşümlerinin tek ayarda birleşmesi; müşteri verisi şartları."),
   r("Hesap düzeyinde negatif anahtar kelimeler", "https://support.google.com/google-ads/answer/11396330?hl=tr", "Hesap düzeyi negatif liste ve sınırı."),
   r("Otomatik uygulanan önerileri yönetme", "https://support.google.com/google-ads/answer/10276359?hl=tr", "Otomatik uygulamayı kapatma."),
   r("Arama Ağı'nda Görüntülü Reklam Ağı genişletmesi", "https://support.google.com/google-ads/answer/7193800?hl=tr", "Arama kampanyasının ağ ayarları."),
   r("Gelişmiş konum seçenekleri", "https://support.google.com/google-ads/answer/1722038?hl=tr", "\"Bulunma\" ve \"Bulunma veya ilgi\" hedefleme seçenekleri."),
   r("Reklamveren doğrulaması", "https://support.google.com/adspolicy/answer/9703665?hl=tr", "Reklamveren adının ve konumunun doğrulanması; süre içinde tamamlanmazsa kısıtlama."),
   r("Reklam zamanlamasında bütçe harcama değişikliği", "https://support.google.com/google-ads/answer/16913225?hl=tr", "1 Haziran 2026'dan beri günlere göre zamanlamada da aylık 30,4 kat sınırı.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_ads_account", "label": "Hesap Açılış Biçimi", "en": "Account Setup Mode", "type": "select", "showIf": SV("ads"),
  "explanation": "Google Ads hesabının yönetici hesabı altında mı, tek başına mı açılacağını ve hangi modda kullanılacağını belirler.",
  "scenario": "Ajansla çalışılıyorsa ya da birden çok marka / hesap yönetiliyorsa yönetici hesabı; tek işletmede de uzman modu önerilir. Akıllı mod yalnız çok küçük ve basit kampanyalar içindir.",
  "example": "Kurumun yönetici hesabı altında \"Marka – TR\" reklam hesabı uzman modunda açılır; ajans kendi yönetici hesabını bu hesaba bağlama isteği gönderir.",
  "rule": "Google Ads hesap açılış biçimi: {label}.",
  "options": [
   o("mcc", "Kurumun yönetici hesabı altında, uzman modu (önerilen)", "Kurum bir yönetici hesabı (MCC) açar; reklam hesapları bunun altında uzman modunda açılır. Ajans kendi yönetici hesabıyla bağlanır, ayrılınca bağlantı kesilir.", "Ajansla çalışan, birden çok hesabı ya da markası olan işletmeler.", "Ajans değiştiğinde reklam hesabı ve geçmiş veri kurumun yönetici hesabında kalır.",
     "Reklam hesabı kurumun yönetici hesabı (MCC) altında uzman modunda açılır; ajans kendi yönetici hesabıyla bağlanır, sahiplik kurumda kalır."),
   o("expert", "Tek hesap, uzman modu", "Reklam hesabı yönetici hesabı olmadan, uzman modunda açılır.", "Tek hesabı olan ve kendi yöneten işletmeler.", "İşletme sahibi ve pazarlama uzmanı aynı hesabı Yönetici ve Standart erişimle kullanır.",
     "Reklam hesabı uzman modunda açılır (Akıllı mod kullanılmaz); kampanyasız hesap oluşturma yoluyla açılır."),
   o("smart", "Akıllı mod", "Basitleştirilmiş arayüzde yalnız Akıllı kampanyalar oluşturulabilir; ayrıntılı hedefleme ve ölçüm ayarları sınırlıdır.", "Yalnız çok küçük bütçeli, tek kampanyalı yerel işletmeler.", "Kampanya hedefi \"telefon aramaları\" seçilir; anahtar kelime ayrıntıları gösterilmez.",
     "Hesap Akıllı modda kullanılır; ayrıntılı kampanya ihtiyacı doğarsa uzman moduna geçilir.")]},
 {"id": "gg_ads_settings", "label": "Google Ads Asgari Hesap Ayarları", "en": "Google Ads Minimum Account Settings", "type": "multiselect", "showIf": SV("ads"),
  "explanation": "Google Ads hesabında kampanyalardan önce yapılması gereken asgari ayarları belirler.",
  "scenario": "İlk altı madde her hesapta asgari kabul edilir; birden çok yönetici varsa çok taraflı onay, Arama kampanyası varsa ağ ve konum ayarları eklenir.",
  "example": "Yönetici › Hesap ayarları: otomatik etiketleme açık, otomatik uygulama kapalı, negatif anahtar kelime listesi \"iş ilanı, ücretsiz, staj\"; kampanyada konum seçeneği \"Bulunma\".",
  "rule": "Google Ads asgari hesap ayarları: {labels}.",
  "options": [
   o("tz_currency", "Saat dilimi ve para birimi doğru", "Hesap açılırken seçilir ve değiştirilemez.", "Her hesap.", "(GMT+03:00) İstanbul ve Türk lirası.",
     "Hesap saat dilimi Türkiye (İstanbul) ve para birimi faturalandırmaya uygun seçilir; hesap açılmadan önce kontrol edilir çünkü sonradan değiştirilemez."),
   o("billing", "Faturalandırma ve vergi bilgileri", "Ödeme profili kurumun ticari unvanı, adresi, vergi dairesi ve numarasıyla açılır; Türkiye'deki ek ücret ve vergiler mali müşavirle doğrulanır.", "Her hesap.", "Faturalar kurumun unvanına kesilir; muhasebe her ay faturaları indirir.",
     "Ödeme profili kurumun ticari unvanı ve vergi bilgileriyle (Ortak Bilgiler › Vergi ve Sicil Bilgileri) açılır; faturalandırma rolü muhasebeye verilir, ülkeye özgü ek ücret ve vergiler mali müşavirle doğrulanır."),
   o("autotag", "Otomatik etiketleme açık", "Reklam tıklamalarına gclid eklenir; dönüşüm ölçümü ve GA4 kaynak bilgisi bununla çalışır.", "Her hesap.", "Reklamdan gelen ziyaret GA4'te \"google / cpc\" olarak ve kampanya adıyla görünür.",
     "Otomatik etiketleme açıktır; site ve yönlendirmeler gclid, gbraid, wbraid ve UTM parametrelerini silmeden kabul eder."),
   o("auto_apply_off", "Otomatik uygulanan öneriler kapalı", "Google'ın önerilerini kendiliğinden uygulaması kapatılır; öneriler tek tek değerlendirilir.", "Her hesap.", "Bütçe artırma ya da geniş eşleme önerisi kendiliğinden uygulanmaz.",
     "Otomatik uygulanan öneriler kapalıdır; öneriler haftalık incelenip elle uygulanır."),
   o("2sv_access", "Erişim düzeyleri ve iki adımlı doğrulama", "Kullanıcılar en düşük erişim düzeyiyle eklenir; hesapta hassas işlemler için iki adımlı doğrulama zorunludur.", "Her hesap.", "Ajans Standart, muhasebe Faturalandırma, yönetim Salt okunur erişimdedir.",
     "Kullanıcılar en düşük erişim düzeyiyle eklenir (Yönetici yalnız iki kurum çalışanında); Yönetici › Erişim ve güvenlik › Güvenlik'te iki adımlı doğrulama zorunludur."),
   o("negatives", "Hesap düzeyi negatif anahtar kelimeler", "İşle ilgisiz aramalar (iş ilanı, ücretsiz, nasıl yapılır gibi) hesap düzeyinde dışlanır.", "Arama, Performance Max ya da Alışveriş kampanyası olan hesaplar.", "\"diş hekimi iş ilanı\" araması reklam göstermez.",
     "Hesap düzeyinde negatif anahtar kelime listesi kurulur (iş ilanı, staj, ücretsiz, nasıl yapılır gibi niyet dışı terimler) ve aylık arama terimleri raporuyla güncellenir."),
   o("location", "Konum seçeneği: Bulunma", "Varsayılan \"Bulunma veya ilgi\" yerine yalnız hedef bölgede bulunan ya da düzenli bulunan kişilere gösterim seçilir.", "Yerel ve bölgesel hizmet veren işletmeler.", "İstanbul hedefli kampanya, İzmir'de \"İstanbul diş kliniği\" arayan kişiye gösterilmez.",
     "Kampanyalarda konum seçeneği \"Bulunma\" (hedef konumlardaki ya da düzenli olarak bulunan kişiler) seçilir; \"Bulunma veya ilgi\" yalnız turizm gibi uzaktan ilgi bekleyen işlerde kullanılır."),
   o("network", "Arama kampanyasında Görüntülü Reklam Ağı kapalı", "Arama kampanyası Görüntülü Reklam Ağı'na genişletilmez; arama ortakları bilinçli seçilir.", "Arama kampanyası olan hesaplar.", "Arama bütçesi düşük kaliteli site gösterimlerine harcanmaz.",
     "Arama kampanyalarında Görüntülü Reklam Ağı genişletmesi kapalıdır; arama ortakları performansa göre açılıp kapatılır."),
   o("multi_party", "Çok taraflı onay", "Kullanıcı ekleme / çıkarma ve rol değişikliği gibi hassas işlemler ikinci bir yöneticinin onayını ister.", "Birden çok yöneticisi olan hesaplar.", "Ajans yeni bir Yönetici eklemek isteyince kurumun ikinci yöneticisi onaylar.",
     "Çok taraflı onay açıktır; kullanıcı ve rol değişiklikleri ikinci bir yöneticinin onayıyla yapılır."),
   o("verification", "Reklamveren doğrulaması hazır", "Doğrulama bildirimi gelince süre içinde tamamlamak için ticari unvan, vergi levhası ve yetkili kimliği hazır tutulur; doğrulanan ad reklam açıklamasında görünür.", "Her hesap.", "Doğrulama bildirimi geldiği hafta belgeler yüklenir; reklamlar kısıtlanmaz.",
     "Reklamveren doğrulaması bildirimi geldiğinde süre içinde tamamlanır; ticari unvan ve belgeler Ortak Bilgiler'deki kayıtlarla aynıdır.")]},
 {"id": "gg_ads_conv", "label": "Dönüşüm Ölçümünün Kaynağı", "en": "Conversion Source", "type": "select", "showIf": SV("ads"),
  "explanation": "Google Ads'in dönüşümleri nereden alacağını belirler: Google Ads dönüşüm etiketi mi, GA4 anahtar etkinliklerinin içe aktarımı mı. Teklif stratejisi yalnız birincil dönüşümlerle çalışır.",
  "scenario": "Reklam optimizasyonu öncelikliyse Ads etiketi birincil, GA4 içe aktarımı ikincil; basit kurulumda yalnız GA4 içe aktarımı yeterlidir.",
  "example": "\"Form gönderimi – Ads etiketi\" birincil, \"generate_lead – GA4\" ikincildir; Dönüşümler sütununda form yalnız bir kez sayılır.",
  "rule": "Google Ads dönüşüm kaynağı: {label}.",
  "options": [
   o("tag", "Google Ads dönüşüm etiketi birincil, GA4 içe aktarımı ikincil (önerilen)", "Dönüşümler Tag Manager'daki Google Ads dönüşüm etiketiyle ölçülür ve birincil sayılır; GA4'ten alınan aynı olay ikincil (yalnız gözlem) olur.", "Reklam bütçesi önemli ve teklif stratejisi dönüşüme dayalı hesaplar.", "Teklif stratejisi Ads etiketinin saydığı formlara göre çalışır; GA4 verisi karşılaştırma için durur.",
     "Dönüşümler Google Ads dönüşüm etiketiyle ölçülür ve birincildir; aynı olayın GA4 içe aktarımı ikincildir; dönüşüm değeri ve sayma yöntemi (form için bir, satış için her biri) tanımlanır."),
   o("ga4", "GA4 anahtar etkinliklerinden içe aktarım", "GA4'teki anahtar etkinlikler Ads'e alınır ve birincil yapılır; ayrı Ads etiketi kurulmaz.", "Küçük hesaplar ve tek ölçüm kaynağı istenen basit kurulumlar.", "generate_lead anahtar etkinliği Ads'te birincil dönüşümdür.",
     "Dönüşümler GA4 anahtar etkinliklerinden içe aktarılır ve birincildir; ayrıca Ads dönüşüm etiketi kurulmaz."),
   o("offline", "Çevrimdışı / CRM dönüşümleri (Data Manager)", "Formdan gelen potansiyel müşterinin satışa dönüşüp dönüşmediği CRM'den Google'a geri bildirilir.", "Satış döngüsü uzun B2B, eğitim, emlak ve sağlık işletmeleri.", "CRM'de \"satış kapandı\" olan kayıtlar haftalık olarak Ads'e yüklenir; teklif nitelikli müşteriye göre çalışır.",
     "Form dönüşümleri Ads etiketiyle ölçülür; nitelikli potansiyel müşteri ve satış sonuçları CRM'den Data Manager ile (onaya ve müşteri verisi şartlarına uygun olarak) geri yüklenir.")]},
 {"id": "gg_ads_enhanced", "label": "Gelişmiş Dönüşümler", "en": "Enhanced Conversions", "type": "select", "showIf": SV("ads"),
  "explanation": "Formda girilen e-posta ya da telefonun özetlenerek (SHA-256) Google'a gönderilip dönüşüm ölçümünün güçlendirilip güçlendirilmeyeceğini belirler. Müşteri verisi şartlarının kabulü ve ziyaretçinin onayı gerekir.",
  "scenario": "Hukuki değerlendirme yapılmış ve aydınlatma metninde anlatılmış projelerde açılır; sağlık gibi hassas alanlarda kapalı kalır.",
  "example": "Teklif formu gönderilince e-posta adresi tarayıcıda küçük harfe çevrilip özetlenir ve ad_user_data onayı varsa dönüşüm isteğine eklenir.",
  "rule": "Google Ads gelişmiş dönüşümler: {label}.",
  "options": [
   o("off", "Kapalı (önerilen başlangıç)", "Yalnız çerez ve tıklama bilgisiyle ölçüm yapılır; kişisel veri özetlenerek de gönderilmez.", "Hukuki değerlendirme yapılmamış ya da hassas sektördeki projeler.", "Dönüşüm sayısı onay oranına göre bir miktar eksik görünür.",
     "Gelişmiş dönüşümler kapalıdır; açılması hukuki değerlendirme ve aydınlatma metni güncellemesi gerektirir."),
   o("on", "Açık — onaya bağlı, özetlenmiş veriyle", "Hesap düzeyinde müşteri verisi şartları kabul edilir; form verisi normalize edilip SHA-256 ile özetlenerek yalnız ad_user_data onayı varken gönderilir.", "Reklam bütçesi yüksek, hukuki değerlendirmesi yapılmış projeler.", "Onay veren ziyaretçilerin form dönüşümleri tarayıcı değişse de eşleşir.",
     "Gelişmiş dönüşümler açıktır: müşteri verisi şartları kabul edilir, e-posta / telefon belgelenen biçimde normalize edilip SHA-256 ile özetlenir ve yalnız ad_user_data onayı varken gönderilir; aydınlatma metni buna göre güncellenir.")]},
 {"id": "gg_ads_links", "label": "Google Ads Bağlantıları", "en": "Google Ads Links", "type": "multiselect", "showIf": SV("ads"),
  "explanation": "Google Ads hesabının bağlanacağı diğer Google hesaplarını belirler (Araçlar › Data Manager). GA4 bağlantısı GA4 bölümündedir.",
  "scenario": "E-ticarette Merchant Center, yerel işletmede İşletme Profili, video reklamda YouTube kanalı bağlanır.",
  "example": "İşletme Profili bağlanınca reklamlarda adres ve harita işareti (konum öğesi) gösterilebilir.",
  "rule": "Google Ads bağlantıları: {labels}.",
  "recommend": {"field": "gg_services", "map": {"merchant": ["merchant"], "gbp": ["gbp"], "gsc": ["gsc"]}},
  "options": [
   o("merchant", "Merchant Center", "Ürün verisi Alışveriş ve Performance Max kampanyalarında kullanılır; iki tarafta da yönetici yetkisi gerekir.", "Ürün reklamı verilecekse.", "Merchant Center'daki ürünler Performance Max kampanyasında listelenir.",
     "Google Ads, Merchant Center hesabına bağlanır; Ads kampanyalarının konum hedefi Merchant Center'daki hedef ülkeyle aynıdır."),
   o("gbp", "İşletme Profili (konum öğesi)", "Reklamlarda adres, mesafe ve harita bağlantısı gösterilir; yerel reklamların ön koşuludur.", "Fiziksel konumu olan işletmeler.", "Arama reklamının altında \"Kadıköy · 1,2 km\" konum bilgisi çıkar.",
     "Google Ads İşletme Profili'ne bağlanır ve konum öğesi kampanyalara eklenir."),
   o("youtube", "YouTube kanalı", "Video reklamları ve video etkileşim kitleleri için kanal bağlanır.", "Video reklam verilecekse.", "Kanalı izleyenler yeniden pazarlama kitlesine eklenir.",
     "Google Ads, kurumun YouTube kanalına bağlanır."),
   o("gsc", "Search Console", "Organik ve ücretli arama sonuçları birlikte görülür (ücretli ve organik raporu).", "Arama kampanyası olan ve organik görünürlüğü de izlenen siteler.", "Aynı sorguda organik ve reklam tıklamaları yan yana görünür.",
     "Google Ads, Search Console mülküne bağlanır.")]}]

# 7 — Merchant Center
SECTIONS.append({
 "id": "gg_mc", "name": "Merchant Center", "en": "Google Merchant Center", "icon": "▤", "agents": ["R"],
 "refs": ["domain_name", "mk_brand_name", "oc_phone", "oc_email", "mk_ids"],
 "desc": "Merchant Center'da ürün verisinin kaynağını, iş bilgileri, site doğrulama, kargo ve iade gibi asgari ayarları ve ürün verisi kurallarını belirler",
 "guide": {
  "purpose": "Merchant Center ürünlerin Google Alışveriş'te ücretsiz listelemelerde ve Alışveriş / Performance Max reklamlarında görünmesini sağlar; Türkiye ve Türk lirası desteklenir. Kurulum adımları: hesap açma (kurulumda seçilen ülke sonradan değiştirilemez) › iş bilgileri (mağaza adı, adres, müşteri desteği) › online mağaza adresini doğrulama ve sahiplenme (Search Console doğrulaması kullanılabilir) › kargo ve iade politikaları › ürün kaynağı › pazarlama yöntemleri (ücretsiz listelemeler, reklamlar) › Google Ads bağlantısı › teşhis ekranlarının izlenmesi. Content API for Shopping 18 Ağustos 2026'da kullanımdan kaldırıldı; programla gönderimde Merchant API kullanılır.",
  "criteria": [
   "Mağaza adresi doğrulanmış ve sahiplenilmiştir; mağaza adı sitedeki ve faturadaki adla aynıdır.",
   "Kargo süresi ve ücreti hesap düzeyinde, iade politikası sitedeki iade sayfasıyla tutarlı olarak girilmiştir.",
   "Her üründe zorunlu özellikler (id, title, description, link, image_link, availability, price) ve varsa brand + GTIN doğrudur.",
   "Ürün sayfalarındaki yapısal veri (Product, Offer) feed'deki fiyat ve stokla aynıdır; değişiklik aynı gün feed'e yansır.",
   "Teşhis ekranı haftalık kontrol edilir; onaylanmayan ürün sayısı izlenir."],
  "pitfalls": [
   "Yanlış ülkeyle hesap açmak: ülke sonradan değiştirilemez.",
   "Mağaza adresini sahiplenmeden feed yüklemek: ürünler onaylanmaz.",
   "Uydurma ya da yanlış GTIN girmek, tanımlayıcısı olan ürüne identifier_exists=no yazmak: ürün reddedilir.",
   "Sayfadaki fiyat ve stokla feed'i tutarsız bırakmak: ürünler askıya alınabilir.",
   "Programla gönderimde hâlâ Content API kullanmak: istekler hata verir; Merchant API'ye geçilir."],
  "resources": [
   r("Merchant Center'ı kullanmaya başlama", "https://support.google.com/merchants/answer/12159157?hl=tr", "Hesap kurulumu; ülkenin sonradan değiştirilememesi."),
   r("Online mağaza URL'sini doğrulama ve sahiplenme", "https://support.google.com/merchants/answer/11586344?hl=tr", "Doğrulama yöntemleri ve sahiplenme."),
   r("Kargo ayarları", "https://support.google.com/merchants/answer/14886954?hl=tr", "Hizmet kapsamı, teslim süresi ve kargo ücreti."),
   r("İade politikaları", "https://support.google.com/merchants/answer/14011730?hl=tr", "İade süresi, yöntemi, ücretleri ve politika adresi."),
   r("Ürün verisi spesifikasyonu", "https://support.google.com/merchants/answer/7052112?hl=tr", "Zorunlu ve önerilen ürün özellikleri."),
   r("Online mağazadan ürün ekleme", "https://support.google.com/merchants/answer/12158480?hl=tr", "Yapısal veriden otomatik ürün ve ön koşulları."),
   r("Ücretsiz listelemeler", "https://support.google.com/merchants/answer/13692890?hl=tr", "Ücretsiz ürün listelemelerinin kullanılabildiği ülkeler."),
   r("Desteklenen diller ve para birimleri", "https://support.google.com/merchants/answer/160637?hl=tr", "Türkiye ve Türk lirası desteği."),
   r("Google Ads'i Merchant Center'a bağlama", "https://support.google.com/merchants/answer/12499498?hl=tr", "Bağlantı isteği ve onayı."),
   r("Content API for Shopping kullanımdan kaldırma", "https://developers.google.com/shopping-content/guides/sunset", "Content API'nin 18 Ağustos 2026'da kaldırılması ve Merchant API'ye geçiş."),
   r("Merchant API güncellemeleri", "https://developers.google.com/merchant/api/latest-updates", "Merchant API sürümleri ve değişiklikleri.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_mc_feed", "label": "Ürün Verisi Kaynağı", "en": "Product Data Source", "type": "select", "showIf": SV("merchant"),
  "explanation": "Ürünlerin Merchant Center'a nasıl iletileceğini belirler.",
  "scenario": "Hazır e-ticaret altyapısı (Shopify, WooCommerce, ikas, Ticimax …) kullanılıyorsa platform entegrasyonu; özel yazılmış sitede Merchant API ya da zamanlanmış dosya; az ürünlü sitede yapısal veriden otomatik ürün uygundur.",
  "example": "Site her gece 03:00'te https://ornek.com.tr/feed/google.xml dosyasını üretir; Merchant Center bu dosyayı günlük çeker.",
  "rule": "Merchant Center ürün verisi kaynağı: {label}.",
  "options": [
   o("api", "Merchant API ile otomatik gönderim", "Ürün eklenince, fiyat ya da stok değişince site değişikliği Merchant API ile hemen gönderir.", "Özel yazılmış e-ticaret siteleri, sık fiyat / stok değişimi.", "Stok sıfırlanınca ürün dakikalar içinde \"stokta yok\" olur.",
     "Ürün verisi Merchant API ile gönderilir (Content API kullanılmaz); ürün, fiyat ve stok değişiklikleri olay bazlı iletilir, kimlik bilgileri gizli anahtar deposunda tutulur."),
   o("file", "Zamanlanmış feed dosyası (XML / CSV)", "Site ürün feed'ini belirli aralıklarla üretir; Merchant Center adresi zamanlanmış olarak çeker.", "Orta ölçekli kataloglar, fiyatı günde bir kez değişen ürünler.", "Feed her gece yenilenir.",
     "Site ürün feed'ini (XML ya da CSV) zamanlanmış olarak üretir ve Merchant Center günlük çeker; feed adresi herkese açık ama tahmin edilemez değildir, yalnız ürün verisi içerir."),
   o("platform", "E-ticaret platformu entegrasyonu", "Platformun Google uygulaması ya da eklentisi ürünleri kendisi gönderir.", "Hazır e-ticaret altyapısı kullanan siteler.", "Platformdaki Google kanalı açılınca ürünler eşitlenir.",
     "Ürün verisi e-ticaret platformunun resmî Google entegrasyonuyla gönderilir; eşleme (kategori, marka, GTIN) kontrol edilir."),
   o("auto", "Mağazadan otomatik ürün (yapısal veri)", "Google ürün sayfalarındaki Product yapısal verisinden ürünleri bulur; Googlebot engellenmemeli ve adres doğrulanmış olmalıdır.", "Az ürünlü, feed üretemeyen siteler.", "Ürünler \"Google tarafından bulundu\" altında listelenir.",
     "Ürün sayfalarında eksiksiz Product / Offer yapısal verisi bulunur ve Merchant Center mağazadan otomatik ürün eklemesiyle kullanılır."),
   o("sheets", "Google E-Tablolar", "Ürünler bir Google E-Tablolar dosyasında elle tutulur.", "Çok az ürünlü ya da geçici kataloglar.", "20 ürünlük tablo pazarlama ekibince güncellenir.",
     "Ürün verisi Google E-Tablolar dosyasında tutulur; fiyat ve stok değişiklikleri aynı gün tabloya işlenir.")]},
 {"id": "gg_mc_settings", "label": "Merchant Center Asgari Ayarları", "en": "Merchant Center Minimum Settings", "type": "multiselect", "showIf": SV("merchant"),
  "explanation": "Merchant Center hesabında ürünlerin onaylanması ve doğru görünmesi için yapılması gereken asgari ayarları belirler.",
  "scenario": "İlk altı madde her hesapta asgari kabul edilir; reklam verilecekse Ads bağlantısı eklenir.",
  "example": "Kargo: 1 gün hazırlık, 1–3 gün teslim, 1.000 TL üzeri ücretsiz; iade: 14 gün, ücretsiz kargo etiketiyle, politika adresi /iade-kosullari.",
  "rule": "Merchant Center asgari ayarları: {labels}.",
  "options": [
   o("business", "İş bilgileri ve doğru ülke", "Mağaza adı, işletme adresi ve müşteri desteği bilgileri girilir; ülke doğru seçilir.", "Her hesap.", "Mağaza adı Google Alışveriş'te sitedeki marka adıyla aynı görünür.",
     "Merchant Center iş bilgileri (mağaza adı, adres, müşteri desteği) Ortak Bilgiler'deki kayıtlarla aynıdır; hesap ülkesi Türkiye (ya da satış yapılan ülke) seçilir."),
   o("claim", "Mağaza adresi doğrulandı ve sahiplenildi", "Online mağaza adresi Search Console, HTML etiketi ya da Tag Manager ile doğrulanır ve sahiplenilir.", "Her hesap.", "Ayarlar › İş bilgileri › Online mağaza: Doğrulandı ve sahiplenildi.",
     "Online mağaza adresi doğrulanır ve sahiplenilir; doğrulama etiketi ya da kaydı kaldırılmaz."),
   o("shipping", "Kargo ayarları", "Kargo hizmet kapsamı, sipariş kesim saati, hazırlık ve teslim süreleri ile kargo ücreti hesap düzeyinde girilir.", "Her hesap.", "Saat 14:00'e kadar verilen sipariş aynı gün kargolanır.",
     "Kargo ayarları hesap düzeyinde girilir (kesim saati, hazırlık ve teslim süresi, ücret / ücretsiz kargo eşiği) ve sitedeki teslimat bilgisiyle aynıdır."),
   o("returns", "İade politikası", "İade süresi, yöntemi, ücreti ve politika adresi girilir; sitedeki iade sayfasıyla ve mesafeli satış mevzuatıyla tutarlıdır.", "Her hesap.", "14 gün içinde ücretsiz iade.",
     "İade politikası (süre, yöntem, ücret, politika adresi) girilir; sitedeki iade ve cayma hakkı metniyle tutarlıdır."),
   o("attributes", "Zorunlu ürün özellikleri ve tanımlayıcılar", "Her üründe id, title, description, link, image_link, availability, price; yeni üründe brand; varsa GTIN, yoksa MPN; kullanılmış üründe condition.", "Her hesap.", "Barkodu olan ürünlerde GTIN alanı doludur.",
     "Her ürün zorunlu özellikleri (id, title, description, link, image_link, availability, price) taşır; brand ve varsa GTIN doğru girilir, GTIN uydurulmaz, identifier_exists=no yalnız tanımlayıcısı gerçekten olmayan ürünlerde kullanılır."),
   o("consistency", "Sayfa, yapısal veri ve feed tutarlı", "Ürün sayfasındaki fiyat, stok ve para birimi, yapısal veri ve feed aynıdır; kampanya fiyatı sale_price ile verilir.", "Her hesap.", "İndirim başlayınca sayfa, yapısal veri ve feed aynı anda güncellenir.",
     "Ürün sayfası, Product / Offer yapısal verisi ve feed aynı fiyat, stok ve para birimini (KDV dahil TRY) gösterir; indirimler sale_price ve tarih aralığıyla verilir."),
   o("free_listings", "Ücretsiz listelemeler açık", "Ürünler ücretsiz olarak Google Alışveriş sekmesinde ve aramada listelenir.", "Her e-ticaret hesabı.", "Reklam bütçesi olmadan ürünler Alışveriş sekmesinde görünür.",
     "Pazarlama yöntemlerinde ücretsiz listelemeler açıktır."),
   o("diagnostics", "Haftalık teşhis kontrolü", "Onaylanmayan ve uyarı alan ürünler haftalık kontrol edilir.", "Her hesap.", "Görseli küçük olduğu için reddedilen 12 ürün düzeltilir.",
     "Merchant Center teşhis ekranı haftalık kontrol edilir; onaylanmayan ürünler ve hesap düzeyi sorunlar kayıt altına alınıp düzeltilir.")]}]

# 8 — Google İşletme Profili
SECTIONS.append({
 "id": "gg_gbp", "name": "Google İşletme Profili", "en": "Google Business Profile", "icon": "⌂", "agents": ["M"],
 "refs": ["mk_brand_name", "oc_address", "oc_phone", "oc_hours", "domain_name", "oc_geo"],
 "desc": "İşletme Profili'nin türünü, doğrulamasını, kategorilerini, ad-adres-telefon tutarlılığını, çalışma saatlerini, kullanıcılarını ve yorum düzenini belirler",
 "guide": {
  "purpose": "İşletme Profili işletmenin Google Arama ve Haritalar'daki kartıdır. Kurulum adımları: business.google.com/add › işletme adı (tabeladaki ad), kategori, konum ya da hizmet bölgesi, iletişim bilgileri › doğrulama (yöntemi Google belirler: video, canlı görüntülü görüşme, telefon / SMS, e-posta ya da posta kartı) › saatler, özel saatler, kategoriler, fotoğraflar › kullanıcılar › Google Ads bağlantısı. Haritada sahipsiz bir kayıt varsa yeni profil açmak yerine o kayıt sahiplenilir. Profildeki bilgiler Ortak Bilgiler'deki ad, adres, telefon ve çalışma saatleriyle birebir aynı tutulur.",
  "criteria": [
   "Profil doğrulanmıştır; işletme adı tabeladaki adla aynıdır ve anahtar kelime içermez.",
   "Ad, adres ve telefon sitedeki iletişim sayfası, yapısal veri ve diğer dizinlerle birebir aynıdır.",
   "Birincil kategori işi en özgül biçimde anlatır; çalışma saatleri ve resmî tatillerdeki özel saatler günceldir.",
   "En az iki sahip vardır; yorumlara makul sürede, kişisel veri paylaşmadan yanıt verilir."],
  "pitfalls": [
   "İşletme adına anahtar kelime, slogan ya da şehir eklemek: profil askıya alınabilir.",
   "Evden hizmet veren işletmenin adresini göstermek ya da sanal ofis adresiyle profil açmak.",
   "Aynı konum için birden çok profil açmak.",
   "Resmî tatilleri özel saat olarak girmemek: kapalı günde müşteri kapıya gelir.",
   "Yorum karşılığında indirim vermek ya da sahte yorum almak."],
  "resources": [
   r("İşletme Profili oluşturma", "https://support.google.com/business/answer/2911778?hl=tr", "Profil oluşturma ve sahipsiz kaydı sahiplenme."),
   r("İşletmenizi Google'da temsil etme yönergeleri", "https://support.google.com/business/answer/3038177?hl=tr", "Ad, adres, telefon, kategori ve yasaklı uygulamalar."),
   r("Hizmet bölgesi işletmeleri", "https://support.google.com/business/answer/9157481?hl=tr", "Adresi gizleme ve hizmet bölgesi tanımlama."),
   r("İşletmenizi doğrulama", "https://support.google.com/business/answer/7107242?hl=tr", "Doğrulama yöntemleri ve süreleri."),
   r("Video ile doğrulama", "https://support.google.com/business/answer/14271705?hl=tr", "Doğrulama videosunda gösterilmesi gerekenler."),
   r("İşletme kategorisi", "https://support.google.com/business/answer/7249669?hl=tr", "Birincil ve ek kategorilerin seçimi."),
   r("Özel çalışma saatleri", "https://support.google.com/business/answer/6303076?hl=tr", "Tatil ve özel günler için saatler."),
   r("Sahipler ve yöneticiler", "https://support.google.com/business/answer/3403100?hl=tr", "Kullanıcı rolleri ve sahiplik devri."),
   r("Yorumları yönetme", "https://support.google.com/business/answer/3474050?hl=tr", "Yorumlara yanıt ve uygunsuz yorumu bildirme."),
   r("İşletme Profili'ni Google Ads'e bağlama", "https://support.google.com/google-ads/answer/13450314?hl=tr", "Konum öğesi için bağlantı.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_gbp_type", "label": "İşletme Türü", "en": "Business Type", "type": "select", "showIf": SV("gbp"),
  "explanation": "Profilin müşterinin geldiği bir adresi mi, müşteriye gidilen bir hizmet bölgesini mi, yoksa ikisini birden mi göstereceğini belirler.",
  "scenario": "Klinik, mağaza, restoran fiziksel konumdur; tesisatçı, temizlik, nakliye hizmet bölgesidir; hem dükkânı hem yerinde hizmeti olan işletme karmadır.",
  "example": "Kombi servisi adresini gizler ve Kadıköy, Üsküdar, Ataşehir'i hizmet bölgesi olarak gösterir.",
  "rule": "İşletme Profili türü: {label}.",
  "options": [
   o("storefront", "Fiziksel konum", "Müşteri çalışma saatlerinde adreste ağırlanır; adres haritada görünür.", "Mağaza, klinik, restoran, ofis.", "Haritada işaret ve yol tarifi düğmesi çıkar.",
     "İşletme Profili fiziksel konum olarak açılır; adres Ortak Bilgiler'deki adresle birebir aynıdır."),
   o("service_area", "Hizmet bölgesi (adres gizli)", "Müşteriye gidilir; adres gizlenir, en çok 20 hizmet bölgesi tanımlanır.", "Evden ya da araçla hizmet veren işletmeler.", "Profilde adres yerine \"İstanbul Anadolu Yakası'na hizmet veriyor\" görünür.",
     "İşletme Profili hizmet bölgesi işletmesi olarak açılır; adres gizlenir, hizmet bölgeleri il / ilçe olarak tanımlanır."),
   o("hybrid", "Karma (adres + hizmet bölgesi)", "Müşteri adrese gelebilir, ayrıca bölgede yerinde hizmet verilir.", "Hem dükkânı hem yerinde hizmeti olan işletmeler.", "Adres görünür, hizmet bölgeleri de listelenir.",
     "İşletme Profili hem adres hem hizmet bölgesiyle açılır.")]},
 {"id": "gg_gbp_settings", "label": "İşletme Profili Asgari Ayarları", "en": "Business Profile Minimum Settings", "type": "multiselect", "showIf": SV("gbp"),
  "explanation": "Profilin doğrulanması, doğru görünmesi ve güncel kalması için yapılacak asgari ayarları belirler.",
  "scenario": "İlk altı madde her profilde asgari kabul edilir; reklam veriliyorsa Ads bağlantısı eklenir.",
  "example": "Birincil kategori \"Diş kliniği\", ek kategori \"Ortodontist\"; 29 Ekim için özel saat \"Kapalı\"; web sitesi bağlantısı ?utm_source=google&utm_medium=organic&utm_campaign=gbp.",
  "rule": "İşletme Profili asgari ayarları: {labels}.",
  "options": [
   o("verify", "Doğrulama tamamlandı", "Google'ın sunduğu yöntemle (çoğunlukla video) doğrulama yapılır; videoda tabela, konum ve işletmenin yöneticisi olunduğunu gösteren kanıt bulunur.", "Her profil.", "Kesintisiz videoda sokak tabelası, kapı numarası ve kasa gösterilir.",
     "Profil doğrulanır; doğrulama videosu kesintisiz çekilir, tabela, konum ve yöneticilik kanıtı gösterilir, kimlik ve kişisel bilgiler görünmez."),
   o("nap", "Ad, adres, telefon tutarlı", "İşletme adı tabeladaki adla aynıdır; adres ve telefon sitedeki, yapısal verideki ve diğer dizinlerdeki bilgilerle birebir eşleşir.", "Her profil.", "Ad \"Gülen Diş Kliniği\"dir, \"Gülen Diş Kliniği – Kadıköy İmplant\" değildir.",
     "İşletme adı tabeladaki adla aynıdır ve anahtar kelime, şehir ya da slogan içermez; adres ve telefon Ortak Bilgiler, sitedeki iletişim sayfası ve LocalBusiness yapısal verisiyle birebir aynıdır."),
   o("categories", "Birincil ve ek kategoriler", "Birincil kategori işi en özgül biçimde anlatır; birkaç ek kategori yalnız gerçekten verilen hizmetler içindir.", "Her profil.", "Birincil \"Veteriner\", ek \"Evcil hayvan bakımı\".",
     "Birincil kategori işi en özgül biçimde anlatır; ek kategoriler yalnız gerçekten sunulan hizmetler içindir ve sık değiştirilmez."),
   o("hours", "Çalışma saatleri ve özel saatler", "Normal saatler Ortak Bilgiler'deki çalışma saatleriyle aynıdır; resmî tatiller ve özel günler önceden özel saat olarak girilir.", "Müşteri kabul eden her işletme.", "Kurban Bayramı günleri önceden \"Kapalı\" girilir.",
     "Çalışma saatleri Ortak Bilgiler'deki saatlerle aynıdır; resmî tatiller ve özel günler önceden özel saat olarak girilir, 7 günden uzun kapanışta \"Geçici olarak kapalı\" kullanılır."),
   o("owners", "En az iki sahip", "Profilde iki kurum çalışanı sahip, ajans yönetici rolündedir.", "Her profil.", "Ajans yorumlara yanıt verir ama kullanıcı ekleyip çıkaramaz.",
     "Profilde en az iki kurum çalışanı sahip, ajans ve ekip yönetici rolündedir."),
   o("content", "Açıklama, fotoğraflar ve hizmetler", "Açıklama bağlantı ve fiyat içermez; dış cephe, iç mekân, ekip ve iş fotoğrafları gerçektir; hizmetler / ürünler listelenir.", "Her profil.", "İlk ay 15 gerçek fotoğraf yüklenir.",
     "Profil açıklaması bağlantı ve promosyon içermez; dış cephe, iç mekân, ekip ve iş fotoğrafları gerçek ve güncel, hizmet / ürün listesi sitedekiyle tutarlıdır."),
   o("utm", "Web sitesi bağlantısı UTM'li", "Profildeki web sitesi ve randevu bağlantılarına UTM parametresi eklenir; GA4'te profil trafiği ayrı görünür.", "GA4 kullanan her profil.", "GA4'te \"google / organic / gbp\" kaynağı görünür.",
     "Profildeki web sitesi ve randevu bağlantıları UTM parametreleriyle (utm_source=google, utm_medium=organic, utm_campaign=gbp) verilir."),
   o("reviews", "Yorum yanıt düzeni", "Yorumlara makul sürede, kibar ve kişisel veri paylaşmadan yanıt verilir; yorum karşılığında indirim ya da sahte yorum yoktur.", "Her profil.", "Olumsuz yoruma iki iş günü içinde, hasta bilgisi vermeden yanıt verilir.",
     "Yorumlara en geç iki iş günü içinde, kişisel veri ve sağlık / müşteri bilgisi paylaşmadan yanıt verilir; teşvikli ya da sahte yorum alınmaz, politikaya aykırı yorumlar bildirilir."),
   o("ads", "Google Ads konum öğesi bağlantısı", "Profil Google Ads'e bağlanır; reklamlarda adres ve mesafe gösterilir.", "Google Ads kullanan yerel işletmeler.", "Arama reklamında konum bilgisi çıkar.",
     "İşletme Profili Google Ads'e bağlanır ve konum öğesi kampanyalarda kullanılır.")]}]

# 9 — Data Studio (eski adıyla Looker Studio)
SECTIONS.append({
 "id": "gg_looker", "name": "Data Studio (Looker Studio)", "en": "Data Studio (formerly Looker Studio)", "icon": "▦", "agents": ["V", "A"],
 "desc": "Raporlama panosunun veri kaynaklarını, sahipliğini, veri erişim kimlik bilgisini, paylaşımını ve rapor düzenini belirler",
 "guide": {
  "purpose": "Data Studio (Nisan 2026'ya kadar adı Looker Studio'ydu) GA4, Google Ads, Search Console ve diğer kaynakları tek raporda birleştirir. Kurulum adımları: Oluştur › Veri kaynağı › bağlayıcı (Google Analytics, Google Ads, Search Console …) › hesap ve mülk seçimi › Bağlan › veri kimlik bilgisi (sahip ya da görüntüleyen) › Rapor oluştur › paylaşım ve zamanlanmış gönderim. Ücretsiz sürümde rapor ve veri kaynakları onları oluşturan kişinin hesabına aittir; Pro sürümde kuruluşa (Google Cloud projesine) aittir.",
  "criteria": [
   "Rapor ve veri kaynakları kurumsal bir hesapta oluşturulur; oluşturan kişi ayrılınca rapor kopmaz.",
   "Veri kimlik bilgisi bilinçli seçilmiştir: hassas veride görüntüleyenin kimlik bilgisi, geniş kitleye paylaşılan özette sahibin kimlik bilgisi.",
   "Rapor yalnız belirli kişilerle paylaşılır; herkese açık bağlantı kullanılmaz, görüntüleyenlerin indirme ve kopyalaması gerekiyorsa kapatılır.",
   "Metrik tanımları (dönüşüm, oturum, maliyet) raporda yazılıdır; veri tazeliği ve GA4 kotası bilinir."],
  "pitfalls": [
   "Raporu bir çalışanın kişisel hesabında oluşturmak: çalışan ayrılınca veri kaynakları sahipsiz kalır.",
   "Sahibin kimlik bilgisiyle oluşturulmuş hassas raporu herkese açık bağlantıyla paylaşmak: bağlantıya sahip herkes veriyi görür.",
   "Tek sayfaya çok sayıda GA4 grafiği koymak: GA4 Data API kotası aşılır ve grafikler hata verir.",
   "GA4 rapor rakamlarını keşif (exploration) raporlarıyla karşılaştırmak: Data Studio standart raporlarla tutar."],
  "resources": [
   r("Data Studio duyurusu (Google Cloud blogu)", "https://cloud.google.com/blog/products/data-analytics/looker-studio-is-data-studio", "Looker Studio'nun Data Studio olarak yeniden adlandırılması ve Pro sürümü."),
   r("Google Analytics'e bağlanma", "https://docs.cloud.google.com/looker/docs/studio/connect-to-google-analytics", "GA4 bağlayıcısı, gereken yetkiler ve sınırlar."),
   r("Veri kimlik bilgileri", "https://docs.cloud.google.com/looker/docs/studio/data-credentials-article", "Sahip, görüntüleyen ve hizmet hesabı kimlik bilgisi."),
   r("Veri tazeliğini yönetme", "https://docs.cloud.google.com/looker/docs/studio/manage-data-freshness", "Bağlayıcılara göre önbellek ve yenileme süreleri."),
   r("Roller ve izinler", "https://docs.cloud.google.com/looker/docs/studio/roles-and-permissions", "Görüntüleyen, düzenleyen ve sahip rolleri; paylaşım kısıtları."),
   r("Pro sürümü hakkında", "https://docs.cloud.google.com/looker/docs/studio/about-pro", "Kuruluş sahipliği, ekip çalışma alanları, zamanlanmış gönderim ve diğer farklar.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_ds_sources", "label": "Rapor Veri Kaynakları", "en": "Report Data Sources", "type": "multiselect", "showIf": SV("looker"),
  "explanation": "Rapor panosuna bağlanacak veri kaynaklarını belirler.",
  "scenario": "Çoğu raporda GA4 ve Search Console; reklam varsa Google Ads; hedef ya da maliyet tablosu varsa E-Tablolar eklenir.",
  "example": "Özet sayfası GA4 oturum ve anahtar etkinliklerini, Ads harcamasını ve Search Console tıklamalarını yan yana gösterir.",
  "rule": "Data Studio rapor veri kaynakları: {labels}.",
  "recommend": {"field": "gg_services", "map": {"ga4": ["ga4"], "ads": ["ads"], "gsc": ["gsc"]}},
  "options": [
   o("ga4", "Google Analytics 4", "Trafik, kaynak, sayfa ve anahtar etkinlik verisi.", "GA4 kullanılan her rapor.", "Kanallara göre oturum ve form sayısı.", "GA4 mülkü veri kaynağı olarak bağlanır."),
   o("ads", "Google Ads", "Harcama, tıklama, gösterim ve dönüşüm verisi.", "Reklam verilen projeler.", "Kampanya bazında dönüşüm başına maliyet.", "Google Ads hesabı veri kaynağı olarak bağlanır."),
   o("gsc", "Search Console", "Organik arama sorguları, gösterim, tıklama ve ortalama sıra.", "Organik trafiği izlenen siteler.", "En çok tıklanan 20 sorgu ve açılış sayfası.", "Search Console mülkü (site ve URL gösterim tablolarıyla) veri kaynağı olarak bağlanır."),
   o("sheets", "Google E-Tablolar", "Hedefler, bütçe, CRM özetleri gibi elle tutulan veriler.", "Hedef ya da çevrimdışı veri karşılaştırılacaksa.", "Aylık hedef satırı grafikte kesik çizgiyle görünür.", "Hedef ve çevrimdışı veriler Google E-Tablolar veri kaynağından alınır; tablonun sahibi kurumsal hesaptır."),
   o("bigquery", "BigQuery", "GA4 ya da Search Console ham verisi ve birleştirilmiş tablolar.", "BigQuery dışa aktarımı olan projeler.", "GA4 olayları ile CRM satışları aynı tabloda.", "BigQuery tabloları veri kaynağı olarak bağlanır; sorgu maliyeti için tarih aralığı filtresi zorunludur.")]},
 {"id": "gg_ds_settings", "label": "Rapor Sahipliği, Erişim ve Düzeni", "en": "Report Ownership, Access & Layout", "type": "multiselect", "showIf": SV("looker"),
  "explanation": "Raporun kime ait olacağını, verinin kimin yetkisiyle görüneceğini, paylaşımı ve rapor düzenini belirler.",
  "scenario": "İlk üç madde her raporda asgari kabul edilir; yönetime düzenli rapor gidecekse zamanlanmış gönderim eklenir.",
  "example": "Rapor raporlama@ornek.com.tr hesabındadır; GA4 kaynağı görüntüleyenin kimlik bilgisini kullanır; her pazartesi 09:00'da yönetime PDF gider.",
  "rule": "Data Studio rapor sahipliği, erişim ve düzeni: {labels}.",
  "options": [
   o("owner", "Rapor ve veri kaynakları kurumsal hesapta", "Rapor ve veri kaynakları kurumsal ortak hesapta oluşturulur ya da oraya devredilir; birden çok kişi düzenleyicidir.", "Her rapor.", "Raporu hazırlayan uzman ayrılınca rapor çalışmaya devam eder.",
     "Rapor ve veri kaynakları kurumsal ortak hesapta oluşturulur ya da oraya devredilir; en az iki düzenleyici vardır."),
   o("credentials", "Veri kimlik bilgisi bilinçli seçildi", "Gelir, maliyet ya da kişiye yakın veri içeren kaynaklarda görüntüleyenin kimlik bilgisi; genel özet raporlarda sahibin kimlik bilgisi kullanılır.", "Her rapor.", "Gelir sayfasını yalnız GA4'te gelir metriklerine erişimi olanlar görür.",
     "Hassas veri kaynakları görüntüleyenin kimlik bilgisiyle, genel özet kaynakları sahibin kimlik bilgisiyle çalışır; seçim veri kaynağı listesinde belgelenir."),
   o("sharing", "Kısıtlı paylaşım", "Rapor yalnız belirli kişi ve gruplarla paylaşılır; herkese açık bağlantı kullanılmaz, gerekiyorsa görüntüleyenlerin indirme ve kopyalaması kapatılır.", "Her rapor.", "Rapor yönetim grubu ve ajansla paylaşılır.",
     "Rapor yalnız belirli kişi / gruplarla paylaşılır; \"bağlantıya sahip herkes\" paylaşımı kullanılmaz, görüntüleyenlerin indirme, kopyalama ve yeniden paylaşma izinleri gerektiği kadar kapatılır."),
   o("pages", "Standart rapor sayfaları", "Özet, edinim (kanallar), dönüşüm, organik arama ve reklam sayfaları; her sayfada tarih karşılaştırması.", "Düzenli izlenen raporlar.", "Özet sayfası tek ekranda beş ana metriği önceki dönemle karşılaştırır.",
     "Rapor özet, edinim, dönüşüm, organik arama ve reklam sayfalarından oluşur; her sayfada önceki dönem karşılaştırması bulunur."),
   o("definitions", "Metrik tanımları ve veri notu", "Raporda dönüşüm, oturum ve maliyet tanımları, veri tazeliği ve onay modunun veriye etkisi yazılıdır.", "Yönetime ya da müşteriye sunulan raporlar.", "Son sayfada \"Dönüşüm = generate_lead + click_to_call\" tanımı ve \"veri 12 saatte bir yenilenir\" notu yer alır.",
     "Raporda metrik tanımları, veri tazeliği ve onay reddi nedeniyle verinin eksik olabileceği notu yer alır."),
   o("schedule", "Zamanlanmış e-posta gönderimi", "Rapor belirli aralıklarla PDF / bağlantı olarak e-postayla gönderilir.", "Yönetime düzenli rapor gidecekse.", "Her ayın ilk iş günü 09:00'da yönetime aylık rapor gider.",
     "Rapor belirlenen alıcılara zamanlanmış e-postayla gönderilir (haftalık ya da aylık)."),
   o("performance", "Kota ve hız düzeni", "Sayfa başına grafik sayısı sınırlı tutulur, GA4 veri tazeliği ihtiyaca göre ayarlanır, ağır sorgular ayrı sayfalara bölünür.", "GA4 ağırlıklı ve çok sayfalı raporlar.", "Her sayfada en çok 10 grafik bulunur.",
     "GA4 Data API kotasını aşmamak için sayfa başına grafik sayısı sınırlı tutulur ve ağır tablolar ayrı sayfalara bölünür.")]}]

# 10 — Kurulum Planı & Talimat
SECTIONS.append({
 "id": "gg_report", "name": "Kurulum Planı & Talimat", "en": "Setup Plan & Instructions", "icon": "⤓", "agents": ["W", "O"],
 "desc": "Kurulumun nasıl doğrulanacağını ve teslim edileceğini belirler; seçimlerden ayrı bir Google kurulum talimatı (.md) üretir",
 "guide": {
  "purpose": "Bu bölüm kurulumun doğrulanmasını ve teslimini planlar. Google Servisleri bölümlerindeki bütün seçimler Proje Kuralları'na \"Google Servisleri\" başlığıyla, Claude promptuna \"GOOGLE SERVİSLERİ KURULUMU\" bölümüyle ve CLAUDE-TALİMATLARI.md dosyasına \"Google servisleri ve ölçüm kurulumu\" fazıyla girer. Kurulumu ayrı bir oturumda yaptırmak isterseniz aşağıdaki karttan aynı kuralları bağlam, kimlikler ve çalışma kurallarıyla tek bir talimat dosyası olarak alabilirsiniz. Önerilen sıra: hesaplar ve erişim › onay altyapısı › Tag Manager › GA4 › Search Console › Google Ads › Merchant Center › İşletme Profili › rapor panosu › doğrulama ve teslim.",
  "criteria": [
   "Her servis kurulumdan sonra kendi aracıyla doğrulanmış ve kanıtı (ekran görüntüsü ya da değer) kayda geçmiştir.",
   "Kimlikler Ortak Bilgiler › Hesap ve Etiket Kimlikleri'ne yazılmıştır.",
   "Erişim listesi, ölçüm planı ve değişiklik kaydı teslim edilmiştir; gözden geçirme tarihi bellidir."],
  "pitfalls": [
   "Kurulumu doğrulamadan reklam kampanyası başlatmak: ilk haftaların dönüşüm verisi kaybolur.",
   "Kimlikleri ve erişim listesini yalnız ajansta bırakmak.",
   "Ölçüm planı yazmamak: hangi olayın neyi saydığı birkaç ay sonra bilinmez."],
  "resources": [
   r("Tag Assistant ile önizleme ve hata ayıklama", "https://support.google.com/tagmanager/answer/6107056?hl=tr", "Etiketlerin ve onay durumunun canlı doğrulanması."),
   r("URL denetleme aracı", "https://support.google.com/webmasters/answer/9012289?hl=tr", "Sayfanın Google tarafından nasıl görüldüğünün denetlenmesi."),
   r("Birincil ve ikincil dönüşüm işlemleri", "https://support.google.com/google-ads/answer/11461796?hl=tr", "Dönüşüm işlemlerinin durumu ve teklifte kullanımı.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "gg_verify", "label": "Kurulum Doğrulaması", "en": "Setup Verification", "type": "multiselect",
  "explanation": "Kurulumun çalıştığını kanıtlamak için yapılacak doğrulamaları belirler. Doğrulanmamış adım tamamlanmış sayılmaz.",
  "scenario": "Seçilen her servisin kendi doğrulaması yapılır; onay testi analitik ya da reklam etiketi olan her sitede şarttır.",
  "example": "Tag Assistant'ta form gönderiminde generate_lead bir kez çalışır, GA4 Gerçek zamanlı raporda görünür, Ads'te dönüşüm durumu \"Kaydediliyor\" olur.",
  "rule": "Google kurulum doğrulaması: {labels}.",
  "options": [
   o("tag_assistant", "Tag Assistant ile etiket ve onay testi", "Her dönüşüm senaryosu ve onay seçimi Tag Assistant'ta denenir.", "Etiket kurulan her site.", "Kabul / ret senaryolarında hangi etiketin çalıştığı ekran görüntüsüyle kaydedilir.",
     "Bütün dönüşüm senaryoları ve onay seçimleri Tag Assistant ile denenir; sonuçlar ekran görüntüsüyle kaydedilir."),
   o("ga4_realtime", "GA4 Gerçek zamanlı ve DebugView", "Olaylar ve parametreler DebugView'da, sayfa görüntülemeleri Gerçek zamanlı raporda görülür.", "GA4 kurulan her site.", "generate_lead olayında form_id parametresi görünür, kişisel veri görünmez.",
     "Olaylar ve parametreleri GA4 DebugView ve Gerçek zamanlı raporda doğrulanır; kişisel veri gönderilmediği kontrol edilir."),
   o("ads_status", "Ads dönüşüm durumu ve teşhis", "Dönüşüm işlemlerinin durumu, onay modu ve gelişmiş dönüşüm teşhisleri kontrol edilir.", "Ads kurulan her hesap.", "Dönüşüm işlemi 48 saat içinde \"Kaydediliyor\" durumuna geçer.",
     "Google Ads dönüşüm işlemlerinin durumu, onay modu ve (açıksa) gelişmiş dönüşüm teşhisleri kontrol edilir; birincil / ikincil ayrımı doğrulanır."),
   o("gsc_check", "Search Console doğrulaması", "Mülk doğrulaması, site haritası durumu ve ana sayfanın URL denetimi kontrol edilir.", "Search Console kurulan her site.", "Ana sayfa URL denetiminde \"Google'da\" görünür, site haritası \"Başarılı\"dır.",
     "Search Console'da mülk doğrulaması, site haritası durumu ve ana sayfa ile önemli sayfaların URL denetimi kontrol edilir."),
   o("merchant_check", "Merchant Center ürün teşhisi", "İlk feed işlendikten sonra onaylanan / reddedilen ürünler kontrol edilir.", "Merchant Center kurulan hesaplar.", "Ürünlerin %98'i onaylı, 4 ürün görsel nedeniyle düzeltilecek.",
     "İlk feed işlendikten sonra Merchant Center teşhis ekranı kontrol edilir ve reddedilen ürünler düzeltilir."),
   o("cross_browser", "Farklı tarayıcı ve cihazda deneme", "Kurulum masaüstü ve mobil, en az iki tarayıcıda ve reklam engelleyicisiz / engelleyicili denenir.", "Her kurulum.", "Safari'de çerez reddi sonrası etiketlerin çalışmadığı görülür.",
     "Kurulum masaüstü ve mobilde, en az iki tarayıcıda denenir.")]},
 {"id": "gg_handover", "label": "Teslim ve Bakım", "en": "Handover & Maintenance", "type": "multiselect",
  "explanation": "Kurulumdan sonra teslim edilecek belgeleri ve dönemsel bakımı belirler.",
  "scenario": "Erişim listesi ve kimlik tablosu her kurulumda teslim edilir; ajansla çalışılıyorsa ölçüm planı ve değişiklik kaydı da istenir.",
  "example": "Teslim klasöründe erişim listesi, kimlik tablosu, olay sözlüğü ve Tag Manager sürüm geçmişi bulunur; üç ayda bir kontrol tarihi takvimdedir.",
  "rule": "Google kurulumunun teslim ve bakımı: {labels}.",
  "options": [
   o("access_list", "Erişim listesi", "Her serviste kim, hangi rolle erişiyor; sahipler kimler.", "Her kurulum.", "Tablo: servis, kullanıcı, rol, eklenme tarihi.",
     "Her servisin kullanıcı ve rol listesi teslim edilir."),
   o("id_table", "Kimlik tablosu", "Hesap, mülk, kapsayıcı ve dönüşüm kimlikleri; Ortak Bilgiler'e de yazılır.", "Her kurulum.", "GA4 G-XXXX, mülk 123456789, GTM-XXXX, Ads 123-456-7890.",
     "Bütün Google kimlikleri tablo olarak teslim edilir ve Ortak Bilgiler › Hesap ve Etiket Kimlikleri'ne yazılır."),
   o("measurement_plan", "Ölçüm planı (olay sözlüğü)", "Her olayın adı, tetiklendiği an, parametreleri, anahtar etkinlik olup olmadığı ve Ads'te karşılığı.", "Olay ölçümü yapılan her site.", "generate_lead: form sunucuda kaydedilince; form_id; anahtar; Ads'te birincil.",
     "Ölçüm planı (olay adı, tetikleme anı, parametreler, anahtar etkinlik / Ads karşılığı) teslim edilir ve değişiklikte güncellenir."),
   o("change_log", "Değişiklik kaydı", "Tag Manager sürümleri, GA4 ve Ads ayar değişiklikleri tarihleriyle kaydedilir.", "Birden çok kişinin çalıştığı hesaplar.", "\"2026-11-20: Ads dönüşüm değeri 500 TL yapıldı\" satırı.",
     "Google servislerindeki ayar ve etiket değişiklikleri tarih, kişi ve gerekçeyle değişiklik kaydına yazılır."),
   o("quarterly", "Üç ayda bir gözden geçirme", "Erişimler, onay testi, dönüşüm durumu, Search Console raporları ve Merchant teşhisi düzenli kontrol edilir.", "Her kurulum.", "Ocak, Nisan, Temmuz ve Ekim'in ilk haftası kontrol günüdür.",
     "Google kurulumu üç ayda bir gözden geçirilir: erişimler, onay testi, dönüşüm durumları, Search Console ve Merchant Center teşhisleri.")]}]

IDS_WHEN = {"gtm": ["gtm"], "ga4": ["ga4"], "ga4_property": ["ga4"], "search_console": ["gsc"],
            "gads_customer": ["ads"], "gads_conversion": ["ads"], "merchant": ["merchant"]}


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: kaynak.py <google.json>")
    out = {"version": "1.0", "group": GROUP, "agents": AGENTS, "idsWhen": IDS_WHEN, "sections": SECTIONS}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nf = sum(len(s["fields"]) for s in SECTIONS)
    print(f"{len(SECTIONS)} bölüm, {nf} karar, {sum(len(s['guide']['resources']) for s in SECTIONS)} kaynak")


if __name__ == "__main__":
    main()
