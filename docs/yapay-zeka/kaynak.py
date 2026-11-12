#!/usr/bin/env python3
"""Yapay Zekâ menüsünün kaynağı (2026-11-12). Elle yazılır; çıktı yapay-zeka.json → yz_ekle.py.

Kullanım: python3 -I docs/yapay-zeka/kaynak.py docs/yapay-zeka/yapay-zeka.json

Kullanıcı isteği (2026-11-12): "Yapay zekâ ile ilgili ayarlar menüsü ekleyelim (en sol menüde pazarlama vs gibi);
https://openai.com/business/businesses-in-chatgpt/ bu özellik ile ilgili yapılması gerekenleri ekleyelim, buna ek olarak
işletme / ürün / hizmetle ilgili yapılması gereken başka ayarlar varsa onları da ekle."
Kaynak adresleri 2026-11-12'de iki araştırma ajanı tarafından açılarak doğrulandı (openai.com otomatik araçlara 403 döndürdüğü
için tarayıcıda okundu). Bu alandaki ürünler çok yeni ve ülkeye göre değişiyor: Businesses in ChatGPT 10 Kasım 2026'da beta;
Türkiye'de sahiplenmenin açık olup olmadığı doğrulanamadı (metinlerde "hesabınızda kontrol edin" denir). Güncellerken kaynakları
yeniden açın. Mevcut proje kararları tekrar edilmez: robots.txt standardı (robots_policy), GEO / AIO (geo_aio), llms.txt
(llms_txt) projede; burada öneriyle bağlanır.
"""
import json
import sys

GROUP = "Yapay Zekâ"
AGENTS = {
    "M": "poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru",
    "T": "poz:pazarlama:digital_demand_generation/seo-ve-geo-muduru/teknik-seo-uzmani",
    "W": "poz:pazarlama:digital_demand_generation/web-pazarlama-muduru",
    "O": "poz:pazarlama:digital_demand_generation/web-pazarlama-muduru/dijital-olcumleme-uzmani",
    "P": "poz:pazarlama:digital_demand_generation/performans-pazarlama-muduru",
    "R": "poz:pazarlama:digital_demand_generation/performans-pazarlama-muduru/arama-motoru-reklamlari-uzmani",
    "K": "poz:uyum-risk:06.06/veri-koruma-uyum-programi/kvkk-uyum-uzmani",
    "L": "poz:hukuk:05.07/teknoloji-ve-dijital-urun-hukuku-ekibi/yapay-zeka-hukuku-uzmani",
    "AG": "poz:veri-analitik:17.06/akilli-otomasyon-ve-yapay-zeka-ajanlari/yapay-zeka-ajanlari-muhendisi",
    "GEN": "poz:veri-analitik:17.06/uretken-yapay-zeka-cozumleri/kidemli-uretken-yapay-zeka-muhendisi",
    "STR": "poz:veri-analitik:17.01/veri-ve-yapay-zeka-stratejisi/kidemli-veri-ve-yapay-zeka-stratejisi-uzmani",
    "MI": "poz:pazarlama:marketing_operations_crm_martech/martech-ve-entegrasyon-muduru/entegrasyon-uzmani",
    "I": "poz:siber-guvenlik:16.05/kimlik-ve-erisim-yonetisimi/kidemli-kimlik-ve-erisim-uzmani",
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


SV = lambda *v: [{"field": "yz_services", "in": list(v)}]
OA = "https://openai.com/"
HELP = "https://help.openai.com/"

SECTIONS = []

# 1 — Kapsam & Hazırlık
SECTIONS.append({
 "id": "yz_scope", "name": "Kapsam & Hazırlık", "en": "AI Scope & Readiness", "icon": "✦", "agents": ["M", "STR"],
 "refs": ["mk_brand_name", "oc_legal_name", "domain_name", "oc_tagline", "oc_address", "oc_phone", "oc_hours"],
 "desc": "İşletmenin, ürünlerinin ve hizmetlerinin hangi yapay zekâ platformlarında ve hangi başlıklarda ele alınacağını seçer, platform kayıtlarından önce gereken hazırlığı belirler; sonraki bölümler buradaki seçime göre açılır",
 "guide": {
  "purpose": "İnsanlar işletme, ürün ve hizmet ararken artık ChatGPT, Google AI Mode / Gemini, Microsoft Copilot, Perplexity ve Claude gibi yapay zekâ asistanlarına da soruyor. Bu asistanlar bilgiyi sitenizden, işletme profillerinden, ürün beslemelerinden ve başka kaynaklardan derliyor. Bu menü, bu platformlarda işletmenizin doğru görünmesi için yapılacakları karar olarak toplar: ChatGPT'de işletme profilinin sahiplenilmesi (Businesses in ChatGPT, 10 Kasım 2026'da beta), ChatGPT reklamları, yapay zekâ üzerinden alışveriş, diğer platformların işletme programları, yapay zekâ tarayıcılarına izinler, sitedeki yapay zekâ asistanı ve ölçüm. Proje Kararları'ndaki robots.txt, GEO / AIO ve llms.txt kararları burada tekrar edilmez, öneriyle bağlanır.",
  "criteria": [
   "İşletme adı, adres, telefon, çalışma saatleri, kategori, fiyat ve iade koşulları sitede, Ortak Bilgiler'de ve bütün platformlarda aynıdır; tek doğru kaynak Ortak Bilgiler'dir.",
   "Platform kayıtları için alan adlı kurumsal e-posta, DNS erişimi ve yetkili kişinin resmî belgeleri (vergi levhası, sicil, yetki belgesi) hazırdır.",
   "Her platformun Türkiye'de sunulup sunulmadığı kayıttan önce güncel resmî belgeden kontrol edilir.",
   "Platform hesapları kişisel değil kurumsal hesaplarla açılır; erişim ekibe ve ajansa ayrı ayrı verilir."],
  "pitfalls": [
   "Yapay zekâ platformlarında görünmek için özel bir dosya ya da işaretleme şart sanmak: Google, yapay zekâ özellikleri için normal SEO dışında ek gereklilik olmadığını söylüyor.",
   "Sitede, profilde ve beslemede farklı fiyat, saat ya da adres bırakmak: asistanlar çelişkili bilgiyi yanlış aktarır.",
   "ABD'de duyurulan bir özelliğin (ör. yapay zekâ içinde ödeme) Türkiye'de de açık olduğunu varsaymak.",
   "Arama botlarını da engelleyen genel bir yapay zekâ engeli koymak: işletme yapay zekâ yanıtlarında kaynak olarak görünmez."],
  "resources": [
   r("Businesses in ChatGPT (OpenAI)", OA + "business/businesses-in-chatgpt/", "İşletmenin ChatGPT'deki profilini sahiplenmesi, doğrulaması ve güncellemesi."),
   r("Introducing Businesses in ChatGPT", OA + "index/introducing-businesses-chatgpt/", "10 Kasım 2026 duyurusu: Business Hub, ürün beslemesi, istatistikler, Business Agent."),
   r("ChatGPT'nin sunulduğu ülkeler", HELP + "en/articles/7947663-chatgpt-supported-countries", "Türkiye listede; işletme özelliklerinin uygunluğu ayrıca kontrol edilmeli."),
   r("Google: yapay zekâ özellikleri ve web siteniz", "https://developers.google.com/search/docs/appearance/ai-features", "AI Overviews ve AI Mode için ek dosya ya da işaretleme gerekmez; profil ve Merchant Center güncel tutulur.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_services", "label": "Ele Alınacak Başlıklar", "en": "AI Topics to Cover", "type": "multiselect",
  "explanation": "Bu projede yapay zekâ ile ilgili hangi başlıkların ele alınacağını seçer. Seçtiğiniz başlıkların bölümleri menüde açılır; seçilmeyenler gizli kalır ve kurallara girmez.",
  "scenario": "Her işletme için ChatGPT'de işletme profili, yapay zekâ tarayıcıları ve ölçüm önerilir; e-ticarette alışveriş, yerel işletmede Google / Apple / Microsoft profilleri, sitede sohbet asistanı varsa asistan bölümü eklenir.",
  "example": "Bir diş kliniği ChatGPT işletme profili, Google, Apple, tarayıcı izinleri, sitedeki asistan ve ölçümü seçer; alışveriş ve reklam bölümleri menüde görünmez.",
  "rule": "Yapay zekâ görünürlüğü için ele alınan başlıklar: {labels}.",
  "recommend": [
   {"field": "geo_aio", "map": {"true": ["chatgpt_business", "crawlers", "monitoring"]}},
   {"field": "modules_extra", "map": {"ecommerce": ["shopping", "chatgpt_business"], "support_ai": ["assistant"]}},
   {"field": "gbp", "map": {"true": ["google", "apple", "microsoft"]}},
   {"field": "robots_policy", "map": {"AiSearchAllow": ["crawlers"], "AiTrainBlock": ["crawlers"]}}],
  "options": [
   o("chatgpt_business", "ChatGPT'de işletme profili (Businesses in ChatGPT)", "İşletmenin ChatGPT'deki kaydını Business Hub'da sahiplenmek, doğrulamak ve bilgilerini güncellemek. 10 Kasım 2026'da beta olarak açıldı; uygunluk ülkeye, sektöre ve doğrulamaya bağlı.",
     "Web sitesi olan her işletme; özellikle ChatGPT'den müşteri gelmesini isteyenler.", "ChatGPT'de işletme adı arandığında mavi tikli profil, doğru site, logo ve iade politikası görünür.",
     "İşletmenin ChatGPT'deki kaydı Business Hub'da sahiplenilir ve doğrulanır; uygunluk (Türkiye dahil) başvurudan önce kontrol edilir."),
   o("chatgpt_ads", "ChatGPT reklamları", "ChatGPT'nin ücretsiz ve Go planlarında yanıtın altında gösterilen reklamlar. Ads Manager self-servis kullanımında Türkiye listede.", "ChatGPT kullanıcılarına ücretli ulaşmak isteyen işletmeler.", "“İstanbul'da diş beyazlatma” sohbetinin altında kliniğin reklamı.",
     "ChatGPT reklam hesabı kurumsal hesapla açılır; reklamlar yanıtları etkilemez, hedefleme ve ölçüm kuralları bölümünde belirlenir."),
   o("shopping", "Yapay zekâ üzerinden alışveriş ve ürün beslemeleri", "Ürünlerin ChatGPT, Google AI Mode / Gemini, Copilot ve Perplexity alışveriş sonuçlarında görünmesi için ürün beslemeleri ve ödeme programları. Programların çoğu şimdilik ABD odaklı.", "E-ticaret yapan işletmeler.", "Ürün beslemesi günde bir güncellenir; ChatGPT'de ürün önerildiğinde satın alma sitede tamamlanır.",
     "Ürünlerin yapay zekâ alışveriş sonuçlarında doğru görünmesi için ürün verisi ve beslemeler hazırlanır; Türkiye'de açık olmayan programlar için hazırlık yapılır."),
   o("google", "Google AI Mode / Gemini", "Google'ın yapay zekâ özellikleri İşletme Profili, Merchant Center ve site içeriğini kullanır; ek dosya gerekmez. Kurulum Google Servisleri menüsündedir, burada yapay zekâya özgü kontroller var.", "Google'da görünen her işletme.", "AI Mode'daki yanıtta işletmenin güncel saatleri ve ürün fiyatı doğru görünür.",
     "Google AI Mode / Gemini için İşletme Profili, Merchant Center ve yapısal veri güncel ve siteyle tutarlı tutulur."),
   o("microsoft", "Microsoft Copilot ve Bing", "Bing Places for Business, Bing Webmaster Tools'taki AI Performance raporu ve IndexNow; Copilot yanıtları Bing dizinine dayanır.", "Bing ve Copilot'tan da trafik isteyen işletmeler.", "Bing Webmaster Tools'ta sitenin Copilot yanıtlarında kaç kez kaynak gösterildiği izlenir.",
     "Microsoft tarafında Bing Places kaydı, Bing Webmaster Tools ve IndexNow kurulur."),
   o("apple", "Apple Business (Haritalar, Siri, Safari)", "Apple Business ile işletmenin Apple Haritalar'daki kartı sahiplenilir; Türkiye'de marka ve konum yönetimi açık.", "Fiziksel konumu olan işletmeler.", "iPhone'da Haritalar'da işletmenin logosu, saatleri ve fotoğrafları görünür.",
     "Apple Business'ta işletmenin konum kartı sahiplenilir ve Ortak Bilgiler'le aynı bilgilerle güncellenir."),
   o("perplexity", "Perplexity", "Perplexity'nin ücretsiz satıcı programı ve arama botu. Perplexity içinden satın alma ABD'deki Pro kullanıcılarla sınırlı.", "Teknoloji ve araştırma odaklı kitleye satış yapanlar.", "Perplexity'de ürün araştırmasında işletmenin ürünleri listelenir.",
     "Perplexity için arama botuna izin verilir; satıcı programı uygunsa başvurulur."),
   o("meta_ai", "Meta Business Agent (WhatsApp / Messenger)", "Meta'nın işletmeler için WhatsApp ve Messenger'da müşteri sorularını yanıtlayan yapay zekâ ajanı; 3 Haziran 2026'da duyuruldu, kademeli açılıyor.", "WhatsApp ya da Messenger'dan çok soru alan işletmeler.", "Gece gelen “saat kaçta açıksınız?” sorusunu ajan yanıtlar, karmaşık soruyu temsilciye bırakır.",
     "Meta Business Agent kullanılacaksa yanıt kapsamı, yapay zekâ bildirimi ve temsilciye devir kuralları belirlenir."),
   o("crawlers", "Yapay zekâ tarayıcılarına izinler", "OpenAI, Anthropic, Perplexity, Apple, Meta ve Google'ın arama / yanıt botları ile model eğitimi botlarına robots.txt ve sunucu kurallarıyla verilecek izinler.", "Her site.", "OAI-SearchBot ve Claude-SearchBot'a izin, GPTBot ve ClaudeBot'a kurum kararına göre izin ya da engel.",
     "Yapay zekâ tarayıcılarının izinleri arama / yanıt ve model eğitimi ayrımıyla belirlenir."),
   o("assistant", "Sitedeki yapay zekâ asistanı", "Sitede müşterilere yanıt veren sohbet asistanının şeffaflık, kişisel veri ve doğruluk kuralları (AB Yapay Zekâ Yasası m. 50, KVKK üretken yapay zekâ rehberi).", "Sitede ya da uygulamada yapay zekâ sohbeti olan işletmeler.", "Sohbet penceresi “Yapay zekâ asistanıyla konuşuyorsunuz” diye başlar.",
     "Sitedeki yapay zekâ asistanı için şeffaflık, kişisel veri ve doğruluk kuralları uygulanır."),
   o("monitoring", "Ölçüm ve takip", "Yapay zekâ kaynaklı ziyaretlerin, ChatGPT ve Bing istatistiklerinin ve yanıt doğruluğunun düzenli izlenmesi.", "Her işletme.", "Aylık raporda chatgpt.com ve perplexity.ai'dan gelen ziyaret ve dönüşümler ayrı satırda.",
     "Yapay zekâ kaynaklı trafik, platform istatistikleri ve yanıt doğruluğu düzenli izlenir.")]},
 {"id": "yz_prep", "label": "Hazırlık", "en": "Readiness", "type": "multiselect",
  "explanation": "Platform kayıtlarından önce hazır olması gerekenleri belirler. ChatGPT'de profil yayımlamak için kimlik ve işletme belgesi doğrulaması da istenebilir.",
  "scenario": "Tek doğru kaynak ve kurumsal e-posta her işletmede; DNS erişimi ve resmî belgeler profil sahiplenilecekse seçilir.",
  "example": "Ortak Bilgiler eksiksiz, info@alanadi.com.tr çalışıyor, DNS paneline erişim var, vergi levhası ve imza sirküleri PDF olarak hazır.",
  "rule": "Yapay zekâ platformlarına hazırlık: {labels}.",
  "options": [
   o("single_source", "Tek doğru kaynak: Ortak Bilgiler", "Ad, ticari unvan, adres, telefon, saatler, kategori ve kısa tanıtım önce Ortak Bilgiler'de tamamlanır; platformlara buradan girilir.", "Her işletme.", "Saat değişince önce Ortak Bilgiler, aynı gün sitede ve profillerde güncellenir.",
     "İşletme bilgileri önce Ortak Bilgiler'de tamamlanır; bütün yapay zekâ platformlarına buradan, birebir aynı yazımla girilir."),
   o("domain_email", "Alan adlı kurumsal e-posta", "Sahiplik doğrulaması için sitenin alan adıyla aynı alan adında e-posta (ör. info@alanadi.com.tr).", "Profil sahiplenecek her işletme.", "Doğrulama kodu info@ adresine gelir.",
     "Platform kayıtları sitenin alan adıyla aynı alan adındaki kurumsal e-postayla yapılır."),
   o("dns", "DNS erişimi", "Sahiplik doğrulamasında DNS TXT kaydı eklenebilmesi için alan adı paneline erişim.", "Profil sahiplenecek ve alan adını doğrulayacak işletmeler.", "Cloudflare DNS'e doğrulama TXT kaydı eklenir.",
     "Doğrulama TXT kayıtları DNS'e eklenir, ne için eklendiği not edilir ve doğrulamadan sonra silinmez."),
   o("documents", "Yetkili kişi ve resmî belgeler", "Kimlik doğrulaması için yetkili kişinin resmî kimliği, işletme sicil bilgisi ve yetki belgesi; ad, adres ve vergi / sicil numarası resmî kayıtlarla eşleşmeli.", "Profil yayımlayacak işletmeler.", "Vergi levhası, ticaret sicil gazetesi ve imza sirküleri hazır.",
     "Platformlardaki kimlik doğrulamasını yetkili kişi yapar; ticari unvan, adres ve vergi / sicil numarası resmî kayıtlarla birebir aynıdır."),
   o("availability", "Türkiye uygunluk kontrolü", "Her platformun özelliği kayıttan önce güncel resmî belgeden kontrol edilir; açık değilse tarih notuyla bekleme listesine alınır.", "Her işletme.", "“Businesses in ChatGPT — Türkiye: henüz değil, 2027-01'de yeniden bak.”",
     "Her yapay zekâ platformu özelliğinin Türkiye'de açık olup olmadığı kayıttan önce resmî belgeden kontrol edilir; açık değilse kontrol tarihi takvime yazılır.")]}]

# 2 — ChatGPT'de İşletme
SECTIONS.append({
 "id": "yz_chatgpt", "name": "ChatGPT'de İşletme (Business Hub)", "en": "Businesses in ChatGPT", "icon": "◎", "agents": ["M", "W"],
 "refs": ["mk_brand_name", "oc_legal_name", "domain_name", "oc_tagline", "oc_address", "oc_phone", "oc_hours", "mk_accounts"],
 "desc": "İşletmenin ChatGPT'deki kaydının Business Hub'da sahiplenilmesini, doğrulanmasını, güncellenmesini ve izlenmesini belirler",
 "guide": {
  "purpose": "Businesses in ChatGPT (10 Kasım 2026, beta) işletmelerin ChatGPT'deki kayıtlarını sahiplenip doğrulamasını, bilgilerini güncellemesini ve istatistikleri görmesini sağlar. Kayıt ChatGPT'nin kenar çubuğundaki İşletme Merkezi'nden (Business Hub) bulunur; sahiplik işletme telefonu, işletme e-postası, DNS TXT kaydı ya da Shopify ile doğrulanır. Değişiklik yayımlamak, besleme bağlamak ve istatistik görmek için ayrıca kimlik doğrulaması istenir. Sahiplenilen profile mavi tik gelir; sahiplenmek daha üst sıra ya da satış garantisi vermez ve ChatGPT başka kaynakları da kullanmaya devam eder. Uygunluk ülkeye, sektöre, doğrulamaya ve bütünlük kontrollerine bağlıdır; Türkiye'deki işletmeler için durum başvurudan önce kontrol edilmelidir.",
  "criteria": [
   "Kayıt yetkili kişi tarafından sahiplenilir ve doğrulanır; kimlik doğrulamasındaki ad, adres ve vergi / sicil numarası resmî kayıtlarla eşleşir.",
   "Profildeki web sitesi, açıklama, kategori, logo, teslimat ve iade politikası sitedekiyle aynıdır.",
   "Ekip ve ajans erişimi Business Hub'dan ayrı ayrı verilir; her marka ayrı yönetilir.",
   "İstatistikler (son 28 gün: bahsedilme, site tıklaması, keşif konuları) aylık rapora girer."],
  "pitfalls": [
   "Profil güncellemesinin hemen yansıyacağını sanmak: OpenAI değişiklikleri inceleyip yayımlar, yanıtlara yansıması zaman alır.",
   "Sahiplenmenin sıralama ya da satış garantisi verdiğini düşünmek.",
   "Temsil etmediğiniz bir işletmeyi yönetmek, sahte yorum ya da hakları olmayan görsel kullanmak: politika ihlalidir.",
   "Yerel işletme kaydı bulunamayınca yeni kayıt açmaya çalışmak: yerel mağaza ve restoranlar şu anda yalnız ABD'de var olan kaydı sahiplenebiliyor."],
  "resources": [
   r("Businesses in ChatGPT", OA + "business/businesses-in-chatgpt/", "Özelliğin tanıtımı, uygunluk ve Business Hub bağlantısı."),
   r("ChatGPT'de işletmenizi kurma (Türkçe)", HELP + "tr-tr/articles/20001635-setting-up-your-business-on-chatgpt", "Sahiplenme, doğrulama yolları, kimlik doğrulaması, güncellenebilen alanlar, istatistikler."),
   r("Businesses in ChatGPT politikası", OA + "policies/businesses-in-chatgpt/", "Doğru ve güncel bilgi, sahte yorum yasağı, görsel hakları."),
   r("Business Agents politikası", OA + "policies/business-agents-policy/", "Ajan yapay zekâ olduğunu belirtir; baskı ve gereksiz kişisel veri isteği yasak."),
   r("Introducing Businesses in ChatGPT", OA + "index/introducing-businesses-chatgpt/", "Business Agent ve ürün beslemesi; ajan ABD'deki uygun işletmelere açık.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_cg_claim", "label": "Kayıt Durumu", "en": "Listing Claim", "type": "select", "showIf": SV("chatgpt_business"),
  "explanation": "ChatGPT'deki işletme kaydı için ne yapılacağını belirler.",
  "scenario": "Kayıt bulunuyorsa sahiplenilir; çevrimiçi işletmede kayıt yoksa “işletme ekle” görünebilir; Türkiye'de henüz açık değilse kontrol takvimi tutulur.",
  "example": "Business Hub'da işletme adıyla aranır, kayıt seçilir, DNS ile doğrulanır.",
  "rule": "ChatGPT işletme kaydı: {label}.",
  "options": [
   o("claim", "Var olan kaydı sahiplen ve doğrula (önerilen)", "ChatGPT kenar çubuğunda İşletme Merkezi açılır, işletme adıyla aranır, kayıt seçilip doğrulanır.", "ChatGPT'de kaydı bulunan işletmeler.", "Kayıt bulundu, doğrulama talebi gönderildi, sonuç e-postayla geldi.",
     "ChatGPT'de var olan işletme kaydı Business Hub'da sahiplenilir ve doğrulanır; doğrulama sonucu ve tarihi kayda geçirilir."),
   o("add", "Kayıt yoksa işletme ekle (çevrimiçi işletme)", "Uygun çevrimiçi işletmelerde “işletme ekle” seçeneği görünebilir; yerel mağaza ve restoranlar şimdilik yalnız ABD'de var olan kaydı sahiplenebilir.", "Kaydı bulunmayan çevrimiçi işletmeler.", "Online eğitim sitesi “işletme ekle” ile kaydını oluşturur.",
     "ChatGPT'de kayıt yoksa ve seçenek sunuluyorsa çevrimiçi işletme kaydı Ortak Bilgiler'deki bilgilerle eklenir."),
   o("wait", "Uygunluk açılana kadar izle", "Türkiye'de ya da sektörde sahiplenme açık değilse düzenli kontrol edilir; bu sırada site ve diğer kaynaklar düzeltilir.", "Sahiplenme seçeneği görünmeyen işletmeler.", "Her ayın ilk iş günü Business Hub kontrol edilir.",
     "ChatGPT'de işletme sahiplenme seçeneği açık değilse her ay kontrol edilir; bu sürede site, yapısal veri ve diğer profiller güncel tutulur.")]},
 {"id": "yz_cg_verify", "label": "Sahiplik Doğrulama Yöntemi", "en": "Ownership Verification", "type": "select", "showIf": SV("chatgpt_business"),
  "explanation": "Business Hub'da sahipliğin nasıl doğrulanacağını belirler. Ayrıca değişiklik yayımlamak için kimlik doğrulaması (resmî kimlik, işletme sicil bilgisi, yetki belgesi) istenebilir.",
  "scenario": "Alan adı kurumun elindeyse DNS TXT en kalıcı yoldur; Shopify kullananlar Shopify ile, DNS erişimi olmayanlar işletme e-postası ya da telefonuyla doğrular.",
  "example": "DNS'e OpenAI'nin verdiği TXT kaydı eklenir, doğrulama tamamlanır, kayıt silinmez.",
  "rule": "ChatGPT işletme sahipliği {label} ile doğrulanır; değişiklik yayımlamak için gereken kimlik doğrulamasını işletmenin yetkilisi yapar.",
  "options": [
   o("dns", "DNS TXT kaydı (önerilen)", "Alan adına TXT kaydı eklenir.", "Alan adı paneline erişimi olan işletmeler.", "Cloudflare'de TXT kaydı.", "Doğrulama TXT kaydı DNS'te kalıcı tutulur ve DNS değişikliklerinde korunur."),
   o("email", "İşletme e-postası", "Alan adlı kurumsal e-postaya kod gelir.", "DNS erişimi olmayan ama alan adlı e-postası olanlar.", "info@ adresine doğrulama e-postası.", "Doğrulama alan adlı kurumsal e-postayla yapılır; kişisel e-posta kullanılmaz."),
   o("phone", "İşletme telefonu (SMS / otomatik arama)", "Kayıttaki işletme telefonuna kod gönderilir.", "Telefonu kayıtta doğru görünen yerel işletmeler.", "Sabit hatta otomatik arama.", "Doğrulama kayıttaki işletme telefonuyla yapılır; telefon Ortak Bilgiler'deki ana telefonla aynıdır."),
   o("shopify", "Shopify", "Shopify mağazası bağlanarak doğrulanır.", "Shopify kullanan e-ticaret siteleri.", "Shopify'daki ChatGPT uygulamasıyla doğrulama.", "Doğrulama Shopify mağazası bağlanarak yapılır; mağaza kurumun hesabındadır.")]},
 {"id": "yz_cg_profile", "label": "Profil Bilgileri", "en": "Profile Information", "type": "multiselect", "showIf": SV("chatgpt_business"),
  "explanation": "Business Hub'da güncellenecek profil alanlarını belirler. Değişiklikler OpenAI incelemesinden sonra yayımlanır.",
  "scenario": "Web sitesi, açıklama, kategori ve logo her profilde; e-ticarette teslimat ve iade politikası eklenir.",
  "example": "Açıklama Ortak Bilgiler'deki kısa tanıtımdır; iade politikası sitedeki sayfayla aynı.",
  "rule": "ChatGPT işletme profilinde güncellenen bilgiler: {labels}. Her alan sitedeki ve Ortak Bilgiler'deki bilgiyle aynıdır.",
  "options": [
   o("website", "Web sitesi", "Sitenin canlı adresi.", "Her profil.", "https://www.alanadi.com.tr", "Profildeki web sitesi Ortak Bilgiler › Canlı Site Adresi'dir."),
   o("description", "Açıklama", "İşletmenin ne yaptığını anlatan kısa metin; abartısız, doğrulanabilir.", "Her profil.", "Ortak Bilgiler'deki kısa tanıtım.", "Profil açıklaması Ortak Bilgiler'deki kısa tanıtımdır; doğrulanamayan iddia (“en iyi”, “1 numara”) içermez."),
   o("category", "Ürün / hizmet kategorisi", "İşletmenin asıl işini anlatan kategori.", "Her profil.", "Diş hekimi · Estetik diş hekimliği.", "Profil kategorisi işletmenin asıl işini anlatır ve diğer profillerdeki kategoriyle uyumludur."),
   o("logo", "Logo ve kapak fotoğrafı", "Kurumsal logo ve hakları kurumda olan kapak fotoğrafı.", "Her profil.", "Kare logo, gerçek mekân fotoğrafı.", "Profilde kurumsal logo ve hakları kuruma ait kapak fotoğrafı kullanılır."),
   o("shipping_returns", "Teslimat ve iade politikası", "Sitedeki teslimat ve iade sayfasıyla aynı bilgi.", "Ürün satan işletmeler.", "14 gün iade, 2 iş günü kargo.", "Profildeki teslimat ve iade bilgileri sitedeki politika sayfasıyla aynıdır; değişince aynı gün güncellenir."),
   o("local", "Adres, telefon ve saatler", "Yerel işletmede ad, adres, telefon ve çalışma saatleri.", "Fiziksel konumu olan işletmeler.", "Ortak Bilgiler'deki adres ve saat tablosu.", "Profildeki ad, adres, telefon ve çalışma saatleri Ortak Bilgiler'le birebir aynıdır.")]},
 {"id": "yz_cg_ops", "label": "Yönetim, İstatistik ve Ajan", "en": "Management, Insights & Agent", "type": "multiselect", "showIf": SV("chatgpt_business"),
  "explanation": "Business Hub'ın yönetimini, istatistiklerin izlenmesini, ürün beslemesini ve Business Agent'ı belirler.",
  "scenario": "Ekip erişimi, istatistik takibi ve politika uyumu her profilde; ürün beslemesi ve Business Agent yalnız uygunsa.",
  "example": "Ajans erişimi verilir; her ay bahsedilme ve site tıklaması raporlanır; Business Agent Türkiye'de açılınca değerlendirilir.",
  "rule": "ChatGPT işletme profilinin yönetimi: {labels}.",
  "options": [
   o("team", "Ekip ve ajans erişimi", "Business Hub'da ekip arkadaşı ya da ajans erişimi verilir; her marka ayrı yönetilir.", "Birden çok kişinin yönettiği profiller.", "Ajans yalnız düzenleme yetkisiyle eklenmiş.", "Business Hub erişimi ekip ve ajansa kişi bazında verilir; ayrılan kişinin erişimi aynı gün kaldırılır."),
   o("insights", "İstatistikler aylık raporlanır", "Son 28 günün toplu verisi: bahsedilme, site tıklaması, keşif konuları; tek tek istemler paylaşılmaz.", "Her profil.", "Aylık raporda “ChatGPT'de bahsedilme: 340”.", "Business Hub istatistikleri (bahsedilme, site tıklaması, keşif konuları) aylık pazarlama raporuna eklenir."),
   o("policy", "Politika uyumu", "Yalnız temsil edilen işletme yönetilir; doğru ve güncel bilgi, sahte yorum yok, görsel hakları kurumda.", "Her profil.", "Kampanya bitince profildeki kampanya metni kaldırılır.", "Profil Businesses in ChatGPT politikasına uyar: yalnız temsil edilen işletme, doğru ve güncel bilgi, sahte yorum yok, hakları kuruma ait görseller."),
   o("feed", "Ürün beslemesi (uygunsa)", "Business Hub'dan fiyat ve stok içeren ürün beslemesi bağlanır; standart besleme şimdilik ABD odaklı.", "Ürün satan ve uygun olan işletmeler.", "Günlük besleme, sitedeki fiyatla aynı.", "Uygunsa Business Hub'a fiyat ve stok içeren ürün beslemesi bağlanır; besleme sitedeki fiyat ve stokla aynıdır."),
   o("agent", "Business Agent (uygunsa)", "ChatGPT içinde işletme adına soruları yanıtlayan ajan; şu an ABD'deki uygun e-ticaret ve çevrimiçi hizmet işletmelerine açık. Satın alma ya da rezervasyon yapmaz, siteye bağlantı verir.", "Uygunluk açıldığında çok soru alan işletmeler.", "Ajan “bu ürün hangi bedende var?” sorusunu yanıtlar ve ürün sayfasına yönlendirir.",
     "Business Agent kullanılırsa ajan işletmeyi temsil eden bir yapay zekâ olduğunu açıkça belirtir, baskı ve sahte aciliyet kullanmaz, gereksiz kişisel veri istemez, lisans gerektiren tavsiye vermez; yanıtları sitedeki bilgiyle sınırlıdır.")]}]

# 3 — ChatGPT Reklamları
SECTIONS.append({
 "id": "yz_ads", "name": "ChatGPT Reklamları", "en": "Ads in ChatGPT", "icon": "◆", "agents": ["P", "R"],
 "refs": ["mk_brand_name", "oc_legal_name", "domain_name"],
 "desc": "ChatGPT reklam hesabının kurulumunu, hedefini ve ölçümünü belirler",
 "guide": {
  "purpose": "ChatGPT reklamları ücretsiz ve Go planlarında yanıtın altında gösterilir; Plus, Pro, Business, Enterprise ve Edu'da reklam yoktur. Reklamlar yanıtları etkilemez, sağlık ve siyaset gibi hassas konularda gösterilmez. Ads Manager self-servis kullanımında reklam veren tüzel kişinin ülkesi listede olmalıdır; Türkiye listede. Satın alma gösterim, tıklama ya da dönüşüm hedeflidir; ölçüm için piksel ve Conversions API vardır. Bu bölüm hesabı, hedefi ve ölçümü belirler.",
  "criteria": [
   "Reklam hesabı kurumun tüzel kişiliğiyle açılır; fatura bilgileri ticari unvanla aynıdır.",
   "Ölçüm pikseli yalnız pazarlama çerezlerine onay verilince çalışır; dönüşümler tanımlıdır.",
   "Açılış sayfaları OpenAI'nin reklam denetim botuna (OAI-AdsBot) açıktır.",
   "Bağlantılar UTM'lidir ve reklam metni sitedeki bilgiyle tutarlıdır."],
  "pitfalls": [
   "Reklamın yanıtı etkileyeceğini ya da organik görünürlük sağlayacağını sanmak.",
   "Hassas konularda (sağlık, siyaset) reklam beklemek: bu konularda gösterilmez.",
   "Pikseli onaysız çalıştırmak.",
   "Açılış sayfasında OAI-AdsBot'u engellemek: reklam denetimi başarısız olabilir."],
  "resources": [
   r("Ads in ChatGPT", HELP + "en/articles/20001047-ads-in-chatgpt", "Reklamların hangi planlarda ve nasıl gösterildiği."),
   r("Ads Manager — ülkeler", HELP + "en/articles/20001245-ads-manager-availability", "Self-servis kullanımın açık olduğu ülkeler (Türkiye dahil)."),
   r("Ads in ChatGPT — temel bilgiler", HELP + "en/articles/20001207-ads-in-chatgpt-the-basics", "Reklam biçimi, satın alma hedefleri, teklif ve UTM."),
   r("OpenAI Ads geliştirici belgeleri", "https://developers.openai.com/ads", "Ölçüm pikseli, Conversions API ve Advertiser API.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_ads_goal", "label": "Satın Alma Hedefi", "en": "Buying Goal", "type": "select", "showIf": SV("chatgpt_ads"),
  "explanation": "ChatGPT reklamlarının neye göre satın alınacağını belirler.",
  "scenario": "Ölçüm kurulmuşsa dönüşüm; yeni markada tıklama ya da gösterim.",
  "example": "Dönüşüm hedefiyle randevu formu ölçülür; başlangıç teklifleri küçük tutulup sonuçla ayarlanır.",
  "rule": "ChatGPT reklamlarının satın alma hedefi: {label}.",
  "options": [
   o("conversions", "Dönüşüm", "Piksel ya da Conversions API ile ölçülen dönüşüme göre.", "Ölçümü kurulu siteler.", "Randevu formu dönüşüm.", "Reklamlar dönüşüm hedefiyle satın alınır; dönüşüm olayları Pazarlama › Dönüşüm Olayları'yla aynıdır."),
   o("clicks", "Tıklama", "Siteye gelen tıklamaya göre (CPC).", "Ölçümü henüz kurulmamış ya da trafik hedefli kampanyalar.", "Ürün sayfasına trafik.", "Reklamlar tıklama hedefiyle satın alınır; teklif ve bütçe haftalık gözden geçirilir."),
   o("impressions", "Gösterim", "Görünürlüğe göre (CPM).", "Yeni marka ve lansman.", "Lansman haftası.", "Reklamlar gösterim hedefiyle satın alınır; kampanya sonunda erişim raporlanır.")]},
 {"id": "yz_ads_setup", "label": "Asgari Reklam Ayarları", "en": "Minimum Ad Settings", "type": "multiselect", "showIf": SV("chatgpt_ads"),
  "explanation": "ChatGPT reklam hesabının asgari kurulum ve ölçüm ayarlarını belirler.",
  "scenario": "Kurumsal hesap, fatura, UTM ve açılış sayfası her kurulumda; piksel ölçüm yapılacaksa.",
  "example": "Hesap şirket adına, piksel onaydan sonra çalışıyor, bağlantılar utm_source=chatgpt ile.",
  "rule": "ChatGPT reklam ayarları: {labels}.",
  "options": [
   o("account", "Kurumsal hesap ve fatura", "Hesap tüzel kişi adına, fatura bilgileri ticari unvan ve vergi numarasıyla.", "Her hesap.", "Ads Manager'da şirket bilgileri.", "ChatGPT reklam hesabı kurumun tüzel kişiliği adına açılır; fatura bilgileri ticari unvan ve vergi numarasıyla girilir."),
   o("pixel", "Ölçüm pikseli / Conversions API (onaylı)", "Dönüşüm ölçümü; yalnız pazarlama çerezi onayıyla.", "Dönüşüm ölçen hesaplar.", "Onay verilince piksel yüklenir.", "OpenAI reklam pikseli yalnız pazarlama çerezlerine onay verilince çalışır; sunucu taraflı olaylar da aynı onaya bağlıdır ve kişisel veri düz metin gönderilmez."),
   o("utm", "UTM parametreleri", "Reklam bağlantıları UTM'li; yapay zekâ kaynaklı trafik analitikte ayrılır.", "Her hesap.", "?utm_source=chatgpt&utm_medium=cpc", "ChatGPT reklam bağlantıları UTM parametreleriyle verilir; analitikte ayrı kanal olarak raporlanır."),
   o("landing", "Açılış sayfası denetime açık", "Açılış sayfası OAI-AdsBot'a açık, hızlı ve reklam metniyle tutarlı.", "Her hesap.", "robots.txt OAI-AdsBot'u engellemiyor.", "Reklam açılış sayfaları OAI-AdsBot'a açıktır ve reklam metnindeki teklif sayfada aynen bulunur."),
   o("review", "Haftalık gözden geçirme", "Teklif, bütçe ve sonuçlar haftalık kontrol edilir.", "Her hesap.", "Pazartesi raporu.", "ChatGPT reklam sonuçları ve teklifleri haftalık gözden geçirilir.")]}]

# 4 — Yapay Zekâ ile Alışveriş
SECTIONS.append({
 "id": "yz_shop", "name": "Yapay Zekâ ile Alışveriş & Ürün Beslemeleri", "en": "AI Shopping & Product Feeds", "icon": "▤", "agents": ["MI", "P"],
 "refs": ["domain_name", "oc_services"],
 "desc": "Ürünlerin ChatGPT, Google AI Mode / Gemini, Copilot ve Perplexity alışveriş sonuçlarında doğru görünmesi için ürün verisini, beslemeleri ve ödeme programlarını belirler",
 "guide": {
  "purpose": "Yapay zekâ asistanları ürün önerirken ürün beslemelerini, yapısal veriyi ve satıcı bilgilerini kullanır. ChatGPT'de Shopify satıcılarının ürünleri Shopify Catalog üzerinden zaten listelenir; doğrudan ürün beslemesi onaylı ortaklara açıktır ve standart besleme şimdilik ABD odaklıdır. OpenAI Mart 2026'da Instant Checkout'u daralttı; satın alma artık satıcının sitesinde tamamlanıyor. Google'ın AI Mode / Gemini içi ödemesi (UCP) ABD, Kanada ve Avustralya'da; Copilot Checkout ABD'de; Perplexity içi satın alma ABD'deki Pro kullanıcılarla sınırlı. Türkiye'deki bir işletme için bugün yapılacak iş, ürün verisini bu beslemelere hazır ve sitedekiyle tutarlı hale getirmektir.",
  "criteria": [
   "Her ürünün sabit bir kimliği vardır; kimlik site, yapısal veri, analitik ve bütün beslemelerde aynıdır.",
   "Zorunlu alanlar (kimlik, başlık, açıklama, bağlantı, marka, satıcı adı, görsel, stok durumu, fiyat) eksiksizdir; fiyat ve stok sitedekiyle aynıdır.",
   "Ürün sayfalarındaki Product / Offer yapısal verisi sayfada görünen bilgiyle aynıdır.",
   "Satış, ödeme ve iade satıcının sitesinde, satıcının sorumluluğunda tamamlanır."],
  "pitfalls": [
   "ABD'ye özgü ödeme programlarına Türkiye'den başvurmaya çalışmak.",
   "Beslemede sitedekinden farklı fiyat ya da stok bırakmak: ürün yanlış önerilir ya da reddedilir.",
   "Yasaklı ürünleri (alkol, nikotin, kumar, reçeteli ilaç, silah) beslemeye koymak.",
   "Ürün kimliklerini sonradan değiştirmek: geçmiş veri ve eşleşmeler kopar."],
  "resources": [
   r("OpenAI ürün beslemesi şartnamesi", "https://developers.openai.com/commerce/specs/file-upload/products", "Zorunlu dokuz alan ve isteğe bağlı alanlar."),
   r("OpenAI ürün beslemesi teslimi", "https://developers.openai.com/commerce/specs/file-upload/overview", "SFTP, biçimler, en az günde bir tam snapshot."),
   r("OpenAI Commerce — başlarken", "https://developers.openai.com/commerce/guides/get-started", "Onaylı ortaklar, başvuru ve yasaklı ürünler."),
   r("ChatGPT ile alışveriş", HELP + "en/articles/11128490-shopping-with-chatgpt-search", "Shopify Catalog ve satıcı sıralamasını etkileyenler."),
   r("Powering product discovery in ChatGPT", OA + "index/powering-product-discovery-in-chatgpt/", "Mart 2026: satın alma satıcının sitesinde tamamlanır."),
   r("Google UCP ile ödeme (Merchant Center)", "https://support.google.com/merchants/answer/16837055?hl=en", "AI Mode ve Gemini'de ödeme; ABD, Kanada, Avustralya."),
   r("Microsoft Copilot Checkout", "https://about.ads.microsoft.com/en/solutions/technology/agentic-commerce", "Copilot içinde ödeme; ABD'ye satış yapan satıcılar."),
   r("Perplexity Merchant Program", "https://www.perplexity.ai/hub/blog/shop-like-a-pro", "Ücretsiz satıcı programı.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_shop_channels", "label": "Alışveriş Kanalları", "en": "AI Shopping Channels", "type": "multiselect", "showIf": SV("shopping"),
  "explanation": "Ürünlerin hangi yapay zekâ alışveriş kanallarına hazırlanacağını belirler. Ülke uygunluğu her kanal için seçenek açıklamasında yazar.",
  "scenario": "Türkiye'de satış yapan işletme için Google Merchant Center beslemesi ve Shopify (kullanılıyorsa) bugün işe yarar; diğerleri uygunluk açılınca.",
  "example": "Google Merchant Center beslemesi güncel; OpenAI beslemesi için başvuru formu takvime yazıldı.",
  "rule": "Ürünlerin hazırlandığı yapay zekâ alışveriş kanalları: {labels}.",
  "options": [
   o("google_mc", "Google Merchant Center (AI Mode / Gemini)", "Google'ın yapay zekâ özellikleri Merchant Center ürün verisini kullanır; kurulum Google Servisleri › Merchant Center'da. AI Mode içi ödeme (UCP) şimdilik ABD, Kanada, Avustralya.", "Google'da ürün gösteren işletmeler.", "Merchant Center teşhis ekranında 0 hata.",
     "Ürünler Google Merchant Center beslemesiyle güncel tutulur; AI Mode / Gemini içi ödeme yalnız uygun ülkelerde açılınca değerlendirilir."),
   o("shopify", "Shopify Catalog (ChatGPT)", "Shopify satıcılarının ürünleri Shopify Catalog üzerinden ChatGPT'de zaten listelenir; ayrıca ChatGPT uygulaması var.", "Shopify kullanan mağazalar.", "Shopify'da ChatGPT uygulaması kurulu.",
     "Shopify kullanılıyorsa ürünlerin ChatGPT'de Shopify Catalog üzerinden göründüğü kontrol edilir; ürün verisi Shopify'da güncel tutulur."),
   o("openai_feed", "OpenAI ürün beslemesi (onaylı ortak)", "Doğrudan ChatGPT'ye ürün beslemesi; onaylı ortaklara açık, standart besleme şimdilik ABD odaklı.", "Uygunluk açıldığında büyük kataloglu satıcılar.", "Başvuru formu dolduruldu, sonuç bekleniyor.",
     "OpenAI ürün beslemesi uygunsa başvurulur; besleme şartnamesindeki zorunlu alanlarla, en az günde bir tam snapshot olarak hazırlanır."),
   o("copilot", "Microsoft Merchant Center (Copilot)", "Copilot alışverişi Microsoft Merchant Center'ı kullanır; Copilot Checkout şimdilik ABD'ye satış yapan satıcılar için.", "Bing / Copilot'ta ürün göstermek isteyenler.", "Microsoft Merchant Center'a besleme bağlı.",
     "Ürünler Microsoft Merchant Center'a beslenir; Copilot içi ödeme uygun ülkelerde açılınca değerlendirilir."),
   o("perplexity", "Perplexity Merchant Program", "Ücretsiz satıcı programı; Perplexity içinden satın alma şimdilik ABD.", "Perplexity'de görünmek isteyen satıcılar.", "Program formu gönderildi.",
     "Perplexity Merchant Program uygunsa başvurulur; ürün bilgileri sitedekiyle aynıdır.")]},
 {"id": "yz_shop_data", "label": "Ürün Verisi Kuralları", "en": "Product Data Rules", "type": "multiselect", "showIf": SV("shopping"),
  "explanation": "Bütün yapay zekâ alışveriş kanallarında ortak ürün verisi kurallarını belirler.",
  "scenario": "Kimlik, zorunlu alanlar, fiyat / stok eşitliği ve yapısal veri her e-ticaret sitesinde seçilir.",
  "example": "Ürün TS-104 her yerde aynı kimlikle; fiyat ve stok saat başı eşitleniyor.",
  "rule": "Yapay zekâ alışverişi için ürün verisi kuralları: {labels}.",
  "options": [
   o("ids", "Sabit ürün kimliği", "Ürün kimliği değişmez; site, yapısal veri, analitik ve beslemelerde aynı.", "Her e-ticaret sitesi.", "SKU TS-104.", "Her ürünün sabit bir kimliği vardır; kimlik site, yapısal veri, analitik olayları ve bütün beslemelerde aynıdır ve sonradan değiştirilmez."),
   o("required", "Zorunlu alanlar eksiksiz", "Kimlik, başlık, açıklama, bağlantı, marka, satıcı adı, görsel, stok durumu, fiyat (para birimiyle).", "Her besleme.", "price: 1250.00 TRY", "Her üründe kimlik, başlık, açıklama, bağlantı, marka, satıcı adı, görsel, stok durumu ve para birimli fiyat doludur."),
   o("sync", "Fiyat ve stok eşitliği", "Beslemedeki fiyat ve stok sitedekiyle aynı; besleme en az günde bir güncellenir.", "Her besleme.", "Günlük tam besleme + fiyat değişiminde ek güncelleme.", "Beslemelerdeki fiyat, indirimli fiyat ve stok sitedekiyle aynıdır; beslemeler en az günde bir tam olarak güncellenir."),
   o("structured", "Product / Offer yapısal verisi", "Ürün sayfalarında sayfada görünen bilgiyle aynı Product ve Offer işaretlemesi.", "Her ürün sayfası.", "Sayfadaki fiyat ile JSON-LD fiyatı aynı.", "Ürün sayfalarında Product ve Offer yapısal verisi sayfada görünen ad, fiyat, stok ve görselle birebir aynıdır."),
   o("policies", "Teslimat ve iade bilgisi", "Teslimat süresi, ücret ve iade koşulları sitede açık ve beslemelerde aynı.", "Ürün satan her site.", "Ücretsiz kargo 500 TL üzeri, 14 gün iade.", "Teslimat ve iade koşulları sitede açık bir sayfadadır ve beslemelerde aynı bilgiyle verilir."),
   o("prohibited", "Yasaklı ürün kontrolü", "Platform politikalarında yasak ürünler (alkol, nikotin, kumar, reçeteli ilaç, silah …) beslemeye konmaz.", "Geniş kataloglu satıcılar.", "Yasaklı kategoriler beslemeden filtrelenir.", "Platform politikalarında yasaklı ürünler beslemelere konmaz; filtre kuralı belgelenir."),
   o("checkout_site", "Satış sitede tamamlanır", "Ödeme, sözleşme ve iade süreci satıcının sitesinde; mesafeli satış yükümlülükleri satıcıdadır.", "Her satıcı.", "Yapay zekâdan gelen kullanıcı ürün sayfasına iner, ödemeyi sitede yapar.", "Yapay zekâ kanallarından gelen satın almalar satıcının sitesinde tamamlanır; ön bilgilendirme, mesafeli satış sözleşmesi ve iade süreci sitedeki akışla aynıdır.")]}]

# 5 — Diğer Platformlar
SECTIONS.append({
 "id": "yz_platforms", "name": "Google, Microsoft, Apple, Perplexity & Meta", "en": "Other AI Platforms", "icon": "◇", "agents": ["M", "T"],
 "refs": ["mk_brand_name", "domain_name", "oc_address", "oc_phone", "oc_hours", "mk_accounts"],
 "desc": "ChatGPT dışındaki yapay zekâ platformlarında işletme ve ürün bilgilerinin doğru görünmesi için platform başına yapılacakları belirler",
 "guide": {
  "purpose": "Google AI Mode / Gemini, Microsoft Copilot, Apple'ın Siri ve Safari'si, Perplexity ve Meta'nın işletme ajanı işletme bilgisini kendi kaynaklarından alır: Google İşletme Profili ve Merchant Center, Bing Places ve Bing dizini, Apple Business, Perplexity'nin arama botu, WhatsApp / Messenger. Bu bölüm her platform için asgari işleri belirler. Google'ın kurulumu Google Servisleri menüsünde, Meta'nınki Meta Servisleri menüsündedir; burada yalnız yapay zekâya özgü kontroller var.",
  "criteria": [
   "Her platformdaki işletme kaydı kurumun hesabındadır ve Ortak Bilgiler'le aynıdır.",
   "Google için ek yapay zekâ dosyası ya da işaretlemesi aranmaz; İşletme Profili, Merchant Center ve yapısal veri güncel tutulur.",
   "Bing Webmaster Tools'ta AI Performance raporu izlenir; yeni ve değişen sayfalar IndexNow ile bildirilir.",
   "Apple Business'ta konum kartı sahiplenilmiştir (Türkiye'de marka ve konum yönetimi açık)."],
  "pitfalls": [
   "Google-Extended'ı engelleyince AI Overviews'tan çıkılacağını sanmak: Google-Extended Gemini eğitimi ve Gemini Apps'teki dayanaklandırma içindir, Arama'yı etkilemez.",
   "Applebot-Extended'ı Applebot sanmak: Applebot-Extended yalnız Apple modellerinin eğitimini kontrol eder; aramayı etkilemez.",
   "Bing Places'ı eski adresinde aramak: Ekim 2025'te bing.com/forbusiness'a taşındı.",
   "Meta Business Agent'ı yapay zekâ olduğunu belirtmeden kullanmak."],
  "resources": [
   r("Google: yapay zekâ özellikleri ve web siteniz", "https://developers.google.com/search/docs/appearance/ai-features", "Ek gereklilik yok; profil ve Merchant Center güncel tutulur."),
   r("Google'ın ortak tarayıcıları (Google-Extended)", "https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers", "Google-Extended'ın neyi kontrol ettiği."),
   r("Yeni Bing Places for Business", "https://blogs.bing.com/search/October-2025/Introducing-the-New-Bing-Places-for-Business-Built-for-Business-Owners,-Powered-by-Research", "Ekim 2025: bing.com/forbusiness."),
   r("Bing Webmaster Tools — AI Performance", "https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview", "Copilot ve Bing yapay zekâ yanıtlarında kaynak gösterilme."),
   r("IndexNow", "https://www.indexnow.org/", "Bing, Yandex, Naver, Seznam ve Yep'e anında bildirim (Google katılmıyor)."),
   r("IndexNow — belgeler", "https://www.indexnow.org/documentation", "Anahtar dosyası (<anahtar>.txt), keyLocation, toplu gönderim ve yanıt kodları."),
   r("IndexNow — sık sorulanlar", "https://www.indexnow.org/faq", "Anahtar dosyasının yeri, tekrar gönderim ve hata kodları."),
   r("Apple Business", "https://business.apple.com/", "Apple Haritalar'da konum kartı, logo, saatler, eylemler."),
   r("Apple Business — ülkelere göre özellikler", "https://support.apple.com/126603", "Türkiye: marka ve konum yönetimi, markalı e-posta."),
   r("Applebot ve Applebot-Extended", "https://support.apple.com/en-us/119829", "Applebot arama; Applebot-Extended yalnız eğitim."),
   r("Perplexity botları", "https://docs.perplexity.ai/guides/bots", "PerplexityBot ve Perplexity-User."),
   r("Meta Business Agent", "https://about.fb.com/news/2026/06/meta-business-agent/", "WhatsApp ve Messenger'da işletme ajanı (3 Haziran 2026).")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_google", "label": "Google AI Mode / Gemini", "en": "Google AI Mode / Gemini", "type": "multiselect", "showIf": SV("google"),
  "explanation": "Google'ın yapay zekâ özelliklerinde doğru görünmek için yapılacak kontrolleri belirler. Kurulum Google Servisleri menüsündedir.",
  "scenario": "Profil, Merchant Center ve yapısal veri her işletmede; snippet kontrolleri ve Google-Extended kararı bilinçli verilir.",
  "example": "İşletme Profili saatleri siteyle aynı; ürün yapısal verisi sayfadaki fiyatla aynı; Google-Extended kararı yazılı.",
  "rule": "Google AI Mode / Gemini için: {labels}.",
  "options": [
   o("profile", "İşletme Profili güncel", "Ad, adres, telefon, saatler, kategori, ürün / hizmetler.", "Yerel işletmeler.", "Bayram saatleri önceden girilir.", "Google İşletme Profili Ortak Bilgiler'le aynıdır; özel gün saatleri önceden girilir."),
   o("merchant", "Merchant Center güncel", "Ürün fiyatı, stok ve politikalar.", "Ürün satanlar.", "Teşhis ekranında 0 hata.", "Merchant Center ürün verisi siteyle aynıdır ve teşhis ekranı haftalık kontrol edilir."),
   o("structured", "Yapısal veri sayfayla aynı", "Organization / LocalBusiness / Product işaretlemesi sayfada görünen metinle aynı.", "Her site.", "JSON-LD'deki telefon sayfadakiyle aynı.", "Yapısal veri sayfada görünen bilgiyle birebir aynıdır; görünmeyen bilgi işaretlenmez."),
   o("no_extra", "Ek yapay zekâ dosyası şart değil", "Google, AI Overviews ve AI Mode için yeni makine okunur dosya ya da işaretleme gerekmediğini söylüyor.", "Her site.", "llms.txt kararı yalnız diğer platformlar için ayrı değerlendirilir.", "Google'ın yapay zekâ özellikleri için ek dosya ya da işaretleme eklenmez; standart SEO ve içerik kalitesi esastır."),
   o("snippet", "Snippet kontrolleri bilinçli", "nosnippet, data-nosnippet, max-snippet ve noindex yapay zekâ özelliklerindeki gösterimi de etkiler.", "Fiyat ya da gizli içerik gösterimini sınırlamak isteyenler.", "Kampanya kuralları bloğunda data-nosnippet.", "nosnippet, data-nosnippet, max-snippet ve noindex yalnız gerekçeli yerlerde kullanılır; yapay zekâ özelliklerindeki gösterimi de etkilediği bilinir."),
   o("extended", "Google-Extended kararı", "Gemini eğitimi ve Gemini Apps'teki dayanaklandırma için izin ya da engel; Arama'yı ve sıralamayı etkilemez.", "Her site.", "robots.txt'de Google-Extended satırı kurum kararına göre.", "Google-Extended için kurum kararı (izin / engel) robots.txt'de uygulanır; bu kararın Google Arama ve AI Overviews görünürlüğünü etkilemediği bilinir.")]},
 {"id": "yz_microsoft", "label": "Microsoft Copilot ve Bing", "en": "Microsoft Copilot & Bing", "type": "multiselect", "showIf": SV("microsoft"),
  "explanation": "Copilot ve Bing yapay zekâ yanıtları için yapılacakları belirler.",
  "scenario": "Bing Webmaster Tools, IndexNow bildirimi ve anahtar dosyası her site için; Bing Places yerel işletmeler için.",
  "example": "Bing Webmaster Tools'ta AI Performance raporu aylık okunur; yayınlanan her sayfa IndexNow ile bildirilir.",
  "rule": "Microsoft Copilot ve Bing için: {labels}.",
  "options": [
   o("places", "Bing Places kaydı", "İşletme kaydı bing.com/forbusiness üzerinden; Ortak Bilgiler'le aynı.", "Yerel işletmeler.", "Bing Places'ta doğrulanmış kayıt.", "Bing Places for Business kaydı sahiplenilir ve Ortak Bilgiler'le aynı tutulur."),
   o("bwt", "Bing Webmaster Tools + AI Performance", "Site doğrulanır, site haritası gönderilir; AI Performance raporu Copilot'ta kaynak gösterilmeyi izler.", "Her site.", "Aylık AI Performance okuma.", "Site Bing Webmaster Tools'ta doğrulanır, site haritası gönderilir; AI Performance raporu aylık izlenir."),
   o("indexnow", "IndexNow bildirimi", "Yeni, değişen, yönlendirilen ve silinen sayfalar yayın anında bildirilir; tek gönderim IndexNow'a katılan bütün arama motorlarıyla (Bing, Yandex, Naver, Seznam, Yep) paylaşılır. Google katılmıyor.", "İçeriği sık değişen siteler.", "Yayın sonrası https://api.indexnow.org/indexnow adresine değişen adresler gönderilir.",
     "Yeni, değişen, yönlendirilen (301 / 302) ve silinen (404 / 410) sayfalar yayın anında IndexNow ile bildirilir: tek adres GET ?url=…&key=…, toplu gönderim POST /indexnow (JSON: host, key, urlList; istek başına en çok 10.000 adres) tek bir uç noktaya yapılır. Değişmemiş adres tekrar gönderilmez; sitenin bütün adresleri için site haritası kullanılır. 200 / 202 başarılı, 400 biçim hatası, 403 anahtar bulunamadı ya da eşleşmedi, 422 adres başka alan adına ait ya da anahtar uyumsuz, 429 çok sık gönderim (Retry-After beklenir) olarak ele alınır ve hata kaydedilir."),
   o("indexnow_key", "IndexNow anahtar dosyası (<anahtar>.txt)", "IndexNow, siteye konan bir anahtar dosyasıyla sahipliği doğrular: anahtar 8–128 karakterdir (a-z, A-Z, 0-9, tire), sitenin köküne <anahtar>.txt adıyla, içinde yalnız anahtar olan UTF-8 metin dosyası konur. Dosya başka klasördeyse keyLocation verilir ve yalnız o klasörün altındaki adresleri kapsar. Anahtar herkese açık bir doğrulama değeridir, gizli anahtar sayılmaz.", "IndexNow kullanan her site.", "https://www.alanadi.com.tr/3f8a1c0e9b7d4e21a6c5.txt dosyası açılınca yalnız 3f8a1c0e9b7d4e21a6c5 yazar.",
     "IndexNow anahtarı 8–128 karakter (a-z, A-Z, 0-9, tire) olarak bir kez üretilir ve ortam ayarında tutulur; sitenin köküne <anahtar>.txt adıyla, içinde yalnız anahtar bulunan UTF-8 düz metin dosyası olarak yayımlanır (giriş gerektirmez, 200 döner, yönlendirme yok). Dosya kökte değilse keyLocation parametresi verilir ve dosya yalnız bulunduğu klasörün altındaki adresleri kapsar. Her alan adı / alt alan adı kendi anahtar dosyasını sunar; anahtar dosyası robots.txt, CDN kuralı ya da yayın temizliğiyle engellenmez veya silinmez; anahtar değiştirilirse eski dosya yenisi doğrulanana kadar kalır."),
   o("mmc", "Microsoft Merchant Center", "Ürünlerin Bing ve Copilot alışverişinde görünmesi için.", "Ürün satanlar.", "Microsoft Merchant Center'da besleme.", "Ürün satılıyorsa Microsoft Merchant Center'a besleme bağlanır ve siteyle eşit tutulur.")]},
 {"id": "yz_apple", "label": "Apple Business", "en": "Apple Business", "type": "multiselect", "showIf": SV("apple"),
  "explanation": "Apple Haritalar, Siri ve Safari'de işletmenin doğru görünmesi için yapılacakları belirler.",
  "scenario": "Fiziksel konumu olan işletmeler konum kartını sahiplenir; Applebot izni her sitede.",
  "example": "Apple Haritalar'da işletmenin logosu, saatleri ve randevu eylemi görünür.",
  "rule": "Apple Business için: {labels}.",
  "options": [
   o("claim", "Konum kartını sahiplen", "Apple Business'ta konum doğrulanır; Türkiye'de marka ve konum yönetimi açık.", "Fiziksel konumu olan işletmeler.", "Konum doğrulandı.", "Apple Business'ta işletmenin konum kartı sahiplenilir ve doğrulanır."),
   o("details", "Logo, saatler, fotoğraflar", "Kart bilgileri Ortak Bilgiler'le aynı.", "Her kart.", "Bayram saatleri önceden girilir.", "Apple Haritalar kartındaki logo, saatler, fotoğraflar ve iletişim bilgileri Ortak Bilgiler'le aynıdır."),
   o("actions", "Eylemler (randevu, sipariş)", "Kartta randevu ya da sipariş bağlantısı.", "Randevu ya da sipariş alan işletmeler.", "“Randevu al” düğmesi.", "Apple Haritalar kartına sitedeki randevu ya da sipariş sayfası eylem olarak eklenir."),
   o("applebot", "Applebot'a izin", "Applebot Siri, Spotlight ve Safari aramasını besler; Applebot-Extended yalnız eğitim içindir.", "Her site.", "robots.txt Applebot'u engellemiyor.", "Applebot'a izin verilir; Applebot-Extended için kurum kararı ayrıca uygulanır.")]},
 {"id": "yz_perplexity", "label": "Perplexity", "en": "Perplexity", "type": "multiselect", "showIf": SV("perplexity"),
  "explanation": "Perplexity yanıtlarında ve alışverişinde görünmek için yapılacakları belirler.",
  "scenario": "Bot izni her site; satıcı programı ürün satanlar için.",
  "example": "PerplexityBot'a izin; Merchant Program formu gönderildi.",
  "rule": "Perplexity için: {labels}.",
  "options": [
   o("bot", "PerplexityBot'a izin", "PerplexityBot siteleri Perplexity sonuçlarında gösterir ve bağlantı verir; eğitim için kullanılmaz.", "Her site.", "robots.txt'de PerplexityBot izinli.", "PerplexityBot'a robots.txt'de izin verilir."),
   o("user_fetch", "Kullanıcı istekli erişimi bilmek", "Perplexity-User kullanıcının istediği sayfayı getirir ve genellikle robots.txt'yi uygulamaz; gizli içerik yalnız erişim kontrolüyle korunur.", "Üye içeriği olan siteler.", "Üye sayfaları oturum ister.", "Gizli ya da üyeye özel içerik robots.txt'ye değil erişim kontrolüne dayanır."),
   o("merchant", "Merchant Program", "Ücretsiz satıcı programı; satın alma şimdilik ABD'deki Pro kullanıcılarla sınırlı.", "Ürün satanlar.", "Program formu gönderildi.", "Ürün satılıyorsa Perplexity Merchant Program uygunluğu kontrol edilir ve uygunsa başvurulur.")]},
 {"id": "yz_meta_ai", "label": "Meta Business Agent", "en": "Meta Business Agent", "type": "select", "showIf": SV("meta_ai"),
  "explanation": "WhatsApp ve Messenger'da müşteri sorularını yanıtlayan Meta yapay zekâ ajanının kullanılıp kullanılmayacağını belirler. Kademeli açılıyor; bazı özellikler bekleme listesinde, Türkiye uygunluğu doğrulanamadı.",
  "scenario": "Çok sayıda tekrarlayan soru alan işletmeler değerlendirir; hassas sektörlerde (sağlık, finans, hukuk) dikkatle ya da hiç kullanılmaz.",
  "example": "Ajan çalışma saatleri ve konum sorularını yanıtlar, fiyat teklifini temsilciye bırakır.",
  "rule": "Meta Business Agent: {label}.",
  "options": [
   o("use", "Kullan (kapsamı sınırlı, temsilciye devirli)", "Ajan yalnız onaylı bilgilerle yanıt verir; çözemediğini temsilciye devreder.", "Tekrarlayan soruları çok olan işletmeler.", "Saat, adres, kargo durumu soruları.",
     "Meta Business Agent yalnız onaylı bilgi kaynağıyla yanıt verir, yapay zekâ olduğunu belirtir, her adımda temsilciye geçiş sunar; yanıtlar haftalık örneklenip kontrol edilir."),
   o("waitlist", "Bekleme listesi / uygunluk kontrolü", "Türkiye'de açılınca değerlendirmek üzere izlenir.", "Henüz erişimi olmayan işletmeler.", "Ayda bir kontrol.", "Meta Business Agent'ın Türkiye'deki uygunluğu ayda bir kontrol edilir; açılınca kapsam ve kurallar belirlenip kullanılır."),
   o("no", "Kullanma", "Mesajlar yalnız insan temsilcilerle yanıtlanır.", "Hassas sektörler ya da kişisel iletişimi önemli markalar.", "Bütün mesajlar destek ekibinde.", "Meta Business Agent kullanılmaz; mesajlar insan temsilcilerle yanıtlanır.")]}]

# 6 — Yapay Zekâ Tarayıcıları
SECTIONS.append({
 "id": "yz_crawlers", "name": "Yapay Zekâ Tarayıcıları & İçerik İzinleri", "en": "AI Crawlers & Content Permissions", "icon": "⌁", "agents": ["T", "L"],
 "refs": ["domain_name"],
 "desc": "Yapay zekâ şirketlerinin arama / yanıt botlarına ve model eğitimi botlarına hangi izinlerin verileceğini, robots.txt ve sunucu / CDN kurallarıyla nasıl uygulanacağını belirler; proje kararındaki robots.txt standardıyla uyumludur",
 "guide": {
  "purpose": "Yapay zekâ şirketlerinin botları üç gruba ayrılır: arama / yanıt botları (siteyi yapay zekâ yanıtlarında kaynak olarak gösterir — OAI-SearchBot, Claude-SearchBot, PerplexityBot, Applebot, Meta-WebIndexer), model eğitimi botları (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent) ve kullanıcının istediği sayfayı getiren botlar (ChatGPT-User, Claude-User, Perplexity-User, Meta-ExternalFetcher — bazıları robots.txt'yi uygulamayabilir). Görünür olmak isteyen işletme arama / yanıt botlarına izin verir; eğitime izin kurum kararıdır. robots.txt değişiklikleri birkaç saat ile bir gün içinde yansır; CDN'in bot yönetimi robots.txt ile çelişmemelidir. Proje › SEO / Semantik › robots.txt Standardı'ndaki yapay zekâ seçenekleri bu bölümle aynı olmalıdır.",
  "criteria": [
   "Arama / yanıt botlarına robots.txt'de izin verilir ve CDN / güvenlik duvarı bu botları engellemez (OpenAI, OAI-SearchBot IP aralıklarını yayımlar).",
   "Eğitim botları için kurum kararı yazılıdır ve robots.txt'de uygulanır.",
   "Her alt alan adının kendi robots.txt'si vardır.",
   "Kural değişikliği sunucu loglarında gerçek bot istekleriyle doğrulanır."],
  "pitfalls": [
   "Bütün yapay zekâ botlarını tek kuralla engellemek: işletme yapay zekâ yanıtlarında kaynak olarak görünmez.",
   "GPTBot'u engelleyince ChatGPT aramasından çıkılacağını sanmak: arama için OAI-SearchBot belirleyicidir.",
   "robots.txt'nin gizli içeriği koruduğunu sanmak: kullanıcı istekli botlar uygulamayabilir; gizli içerik erişim kontrolüyle korunur.",
   "CDN'in “yapay zekâ botlarını engelle” ayarını robots.txt'yi kontrol etmeden açmak."],
  "resources": [
   r("OpenAI tarayıcıları", "https://developers.openai.com/api/docs/bots", "OAI-SearchBot, GPTBot, ChatGPT-User, OAI-AdsBot ve IP listeleri."),
   r("Anthropic tarayıcıları", "https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler", "ClaudeBot, Claude-SearchBot, Claude-User."),
   r("Perplexity botları", "https://docs.perplexity.ai/guides/bots", "PerplexityBot ve Perplexity-User."),
   r("Meta tarayıcıları", "https://developers.facebook.com/docs/sharing/webmasters/web-crawlers", "Meta-ExternalAgent, Meta-ExternalFetcher, Meta-WebIndexer."),
   r("Applebot", "https://support.apple.com/en-us/119829", "Applebot ve Applebot-Extended."),
   r("Google'ın ortak tarayıcıları", "https://developers.google.com/search/docs/crawling-indexing/google-common-crawlers", "Google-Extended."),
   r("Cloudflare Content Signals Policy", "https://blog.cloudflare.com/content-signals-policy/", "robots.txt'de search / ai-input / ai-train tercihleri."),
   r("llms.txt önerisi", "https://llmstxt.org/", "Resmî standart değil, öneri (2024).")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_bots_search", "label": "Arama / Yanıt Botlarına İzin", "en": "Search / Answer Bots Allowed", "type": "multiselect", "showIf": SV("crawlers"),
  "explanation": "Siteyi yapay zekâ yanıtlarında kaynak olarak gösteren botlardan hangilerine izin verileceğini belirler. Bunları engellemek o platformun yanıtlarında görünmemek demektir.",
  "scenario": "Görünür olmak isteyen işletmeler hepsine izin verir.",
  "example": "robots.txt'de OAI-SearchBot, Claude-SearchBot, PerplexityBot, Applebot ve Meta-WebIndexer için Allow: /",
  "rule": "Yapay zekâ arama / yanıt botlarından izin verilenler: {labels}. Bu botlar CDN ve güvenlik duvarında da engellenmez.",
  "recommend": [{"field": "robots_policy", "map": {"AiSearchAllow": ["oai_search", "claude_search", "perplexity", "applebot", "meta_index"]}}],
  "options": [
   o("oai_search", "OAI-SearchBot (ChatGPT arama)", "ChatGPT arama sonuçları için; engellenen site arama yanıtlarında gösterilmez. OpenAI IP aralıklarını yayımlar.", "ChatGPT'de görünmek isteyen her site.", "WAF'ta searchbot.json aralıkları açık.", "OAI-SearchBot'a robots.txt'de izin verilir ve OpenAI'nin yayımladığı IP aralıkları güvenlik duvarında engellenmez."),
   o("claude_search", "Claude-SearchBot (Claude arama)", "Claude'un arama kalitesi için dizinler; engellemek Claude yanıtlarında görünürlüğü azaltabilir.", "Claude'da görünmek isteyenler.", "Allow: /", "Claude-SearchBot'a robots.txt'de izin verilir."),
   o("perplexity", "PerplexityBot", "Perplexity sonuçlarında gösterir ve bağlantı verir; eğitim için kullanılmaz.", "Perplexity'de görünmek isteyenler.", "Allow: /", "PerplexityBot'a robots.txt'de izin verilir."),
   o("applebot", "Applebot (Siri, Spotlight, Safari)", "Apple'ın arama ve öneri özelliklerini besler.", "Apple kullanıcılarına görünmek isteyenler.", "Allow: /", "Applebot'a robots.txt'de izin verilir."),
   o("meta_index", "Meta-WebIndexer (Meta AI arama)", "Meta AI aramasının kalitesi ve kaynak gösterme için.", "Meta AI'da görünmek isteyenler.", "Allow: /", "Meta-WebIndexer'a robots.txt'de izin verilir."),
   o("bing", "Bingbot (Copilot)", "Copilot yanıtları Bing dizinine dayanır; Bingbot normal arama botudur.", "Copilot'ta görünmek isteyenler.", "Bingbot engellenmiyor.", "Bingbot engellenmez; Copilot yanıtları Bing dizinine dayanır.")]},
 {"id": "yz_bots_train", "label": "Model Eğitimi Botları", "en": "AI Training Bots", "type": "select", "showIf": SV("crawlers"),
  "explanation": "Yapay zekâ modellerinin eğitimi için içerik toplayan botlara (GPTBot, ClaudeBot, Google-Extended, Applebot-Extended, Meta-ExternalAgent) izin verilip verilmeyeceğini belirler. Bu karar arama görünürlüğünü doğrudan belirlemez; Meta-ExternalAgent ayrıca dizinleme de yaptığı için ayrı değerlendirilir.",
  "scenario": "Markasının modeller tarafından bilinmesini isteyen işletmeler izin verir; özgün içerik, araştırma ya da ücretli içerik üretenler engelleyebilir; karar hukuk birimiyle verilir.",
  "example": "Blog yazıları eğitime açık, ücretli eğitim içerikleri dizini eğitim botlarına kapalı.",
  "rule": "Yapay zekâ model eğitimi botları: {label}.",
  "recommend": [{"field": "robots_policy", "map": {"AiTrainBlock": ["block"]}}],
  "options": [
   o("allow", "İzin ver", "Eğitim botları siteyi tarayabilir.", "Marka bilinirliği öncelikli işletmeler.", "Eğitim botları için ayrı kural yok.", "Model eğitimi botlarına izin verilir; karar yıllık gözden geçirilir."),
   o("block", "Engelle", "GPTBot, ClaudeBot, Google-Extended, Applebot-Extended ve (dizinleme etkisi değerlendirilerek) Meta-ExternalAgent robots.txt'de engellenir; arama botları açık kalır.", "Özgün ve emek yoğun içerik üretenler.", "User-agent: GPTBot · Disallow: /", "Model eğitimi botları robots.txt'de engellenir; arama / yanıt botları açık kalır ve iki grup ayrı satırlarda yazılır."),
   o("partial", "İçerik türüne göre", "Herkese açık tanıtım içeriği eğitime açık, özgün / ücretli içerik dizinleri kapalı.", "Hem tanıtım hem özgün içerik üretenler.", "/blog/ açık, /egitimler/ kapalı.", "Model eğitimi botları yalnız belirlenen dizinlerde engellenir; dizin listesi robots.txt'de ve içerik politikasında aynıdır.")]},
 {"id": "yz_bots_tech", "label": "Teknik Uygulama", "en": "Technical Implementation", "type": "multiselect", "showIf": SV("crawlers"),
  "explanation": "Bot izinlerinin teknik olarak nasıl uygulanacağını ve doğrulanacağını belirler.",
  "scenario": "CDN uyumu, alt alan adları ve log doğrulaması her sitede; Content-Signal ve llms.txt isteğe bağlı.",
  "example": "Cloudflare'in bot ayarı robots.txt'yle karşılaştırıldı; loglarda OAI-SearchBot 200 dönüyor.",
  "rule": "Yapay zekâ bot izinlerinin uygulanması: {labels}.",
  "options": [
   o("cdn", "CDN / güvenlik duvarı uyumu", "CDN'in bot yönetimi ve güvenlik duvarı izin verilen botları engellemez.", "CDN kullanan siteler.", "Cloudflare AI Crawl Control ayarı robots.txt ile aynı.", "CDN ve güvenlik duvarı kuralları robots.txt'deki yapay zekâ bot kararlarıyla aynıdır; izin verilen botlar engellenmez."),
   o("subdomains", "Her alt alan adında robots.txt", "Kurallar alt alan adı başına geçerlidir.", "Alt alan adı olan siteler.", "blog. ve magaza. alt alanlarında da robots.txt.", "Her alt alan adında kendi robots.txt'si bulunur ve aynı yapay zekâ bot kararlarını uygular."),
   o("logs", "Loglarda doğrulama", "Kural değişikliğinden sonra sunucu loglarında botların isteği ve yanıt kodu kontrol edilir.", "Her site.", "OAI-SearchBot → 200, GPTBot → robots ile engelli.", "robots.txt ya da CDN değişikliğinden sonra sunucu loglarında bot istekleri ve yanıt kodları kontrol edilir; sonuç kayda geçirilir."),
   o("private", "Gizli içerik erişim kontrolüyle", "Kullanıcı istekli botlar (ChatGPT-User, Claude-User, Perplexity-User, Meta-ExternalFetcher) robots.txt'yi uygulamayabilir.", "Üye ya da ücretli içerik sunanlar.", "Üye sayfaları oturum ister.", "Gizli, üyeye özel ya da ücretli içerik robots.txt'ye değil oturum ve yetki kontrolüne dayanır."),
   o("content_signal", "Content-Signal satırı", "Cloudflare'in önerdiği robots.txt satırı: search / ai-input / ai-train tercihleri; tercih bildirir, teknik koruma değildir.", "Tercihlerini açıkça yazmak isteyen siteler.", "Content-Signal: search=yes, ai-train=no", "robots.txt'de Content-Signal satırıyla search, ai-input ve ai-train tercihleri kurum kararına göre yazılır."),
   o("llms", "llms.txt (proje kararıyla)", "llms.txt resmî standart değil, bir öneri; Google kullanmıyor. Karar Proje › AI Arama (GEO / AIO) › llms.txt'dedir.", "Belgelendirme ağırlıklı siteler.", "llms.txt kararı projede “değerlendir”.", "llms.txt yalnız proje kararı “kullan” ise yayımlanır; içeriği sitedeki sayfalarla tutarlıdır.")]}]

# 7 — Sitedeki Yapay Zekâ Asistanı
SECTIONS.append({
 "id": "yz_assistant", "name": "Sitedeki Yapay Zekâ Asistanı", "en": "On-site AI Assistant", "icon": "✎", "agents": ["AG", "L", "K"],
 "refs": ["mk_brand_name", "oc_hours", "oc_phone"],
 "desc": "Sitede ya da uygulamada müşterilere yanıt veren yapay zekâ asistanının şeffaflık, bilgi kaynağı, kişisel veri ve doğruluk kurallarını belirler",
 "guide": {
  "purpose": "AB Yapay Zekâ Yasası'nın 50. maddesi, insanlarla etkileşen yapay zekâ sistemlerinin kişiye bir yapay zekâyla konuştuğunu bildirmesini ister; bu yükümlülük 2 Ağustos 2026'dan beri uygulanır ve AB'deki kullanıcılara hizmet veren Türk işletmelerini de ilgilendirebilir. KVKK'nın 24 Kasım 2025 tarihli Üretken Yapay Zekâ ve Kişisel Verilerin Korunması Rehberi hukuki dayanak, yurt dışına aktarım, şeffaflık, ilgili kişi hakları ve güvenliği ele alır. Bu bölüm sitedeki asistanın bu çerçevede nasıl çalışacağını belirler; proje kararındaki “Canlı destek ve AI sohbet” modülüyle birlikte uygulanır.",
  "criteria": [
   "Asistan konuşmanın başında yapay zekâ olduğunu açıkça söyler; insan temsilciye geçiş her zaman mümkündür.",
   "Asistan yalnız onaylı bilgi kaynağıyla yanıt verir; fiyat, stok ve politika bilgisini uydurmaz.",
   "Gereksiz ya da hassas kişisel veri istenmez; aydınlatma metni asistanı ve model sağlayıcısını (yurt dışı aktarım dahil) kapsar.",
   "Konuşma kayıtlarının saklama süresi ve erişimi belirlidir; yanıtlar düzenli örneklenip kontrol edilir."],
  "pitfalls": [
   "Asistanı insan temsilci gibi tanıtmak.",
   "Asistana sağlık, hukuk, finans gibi lisans gerektiren tavsiye verdirmek.",
   "Konuşmalarda T.C. kimlik numarası, kart bilgisi ya da sağlık bilgisi toplamak.",
   "Model sağlayıcısına veri aktarımını aydınlatma metninde belirtmemek."],
  "resources": [
   r("AB Yapay Zekâ Yasası — Madde 50 (şeffaflık)", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-50", "İnsanlarla etkileşen yapay zekâ sistemleri kendini bildirir."),
   r("AB Yapay Zekâ Yasası — Madde 113 (yürürlük)", "https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-113", "Genel uygulama 2 Ağustos 2026."),
   r("Avrupa Komisyonu — yapay zekâ düzenleyici çerçevesi", "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai", "Şeffaflık kuralları Ağustos 2026."),
   r("KVKK — Üretken Yapay Zekâ ve Kişisel Verilerin Korunması Rehberi", "https://www.kvkk.gov.tr/Icerik/8547/uretken-yapay-zeka-ve-kisisel-verilerin-korunmasi-rehberi-15-soruda", "24 Kasım 2025; hukuki dayanak, aktarım, şeffaflık, haklar."),
   r("OpenAI Business Agents politikası", OA + "policies/business-agents-policy/", "Ajanların kendini tanıtması, baskı ve veri kuralları (örnek ilke seti).")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_as_source", "label": "Bilgi Kaynağı", "en": "Knowledge Source", "type": "select", "showIf": SV("assistant"),
  "explanation": "Asistanın hangi bilgilerle yanıt vereceğini belirler.",
  "scenario": "Çoğu işletmede yalnız site içeriği ve onaylı belgeler; e-ticarette ürün kataloğu ve sipariş durumu eklenir.",
  "example": "Asistan SSS, hizmet sayfaları ve fiyat listesinden yanıt verir; bilmediğinde temsilciye yönlendirir.",
  "rule": "Sitedeki yapay zekâ asistanının bilgi kaynağı: {label}.",
  "options": [
   o("site_only", "Yalnız site içeriği ve onaylı belgeler (önerilen)", "Asistan yalnız sitedeki sayfalar ve onaylanmış belgelerle yanıt verir.", "Hizmet işletmeleri ve kurumsal siteler.", "Kaynak: SSS, hizmetler, fiyat listesi.", "Asistan yalnız site içeriği ve onaylı belgelerle yanıt verir; kaynakta olmayan bilgi için “bilmiyorum” der ve temsilciye yönlendirir."),
   o("site_catalog", "Site + ürün kataloğu ve sipariş durumu", "Ürün, stok ve kimliği doğrulanmış kullanıcının sipariş durumu da kullanılır.", "E-ticaret siteleri.", "“Siparişim nerede?” sorusu oturumlu kullanıcıda yanıtlanır.", "Asistan site içeriği, ürün kataloğu ve yalnız kimliği doğrulanmış kullanıcının kendi sipariş bilgisiyle yanıt verir; başkasının verisine erişemez."),
   o("general", "Genel model bilgisi + site", "Model genel bilgisini de kullanır; uydurma riski daha yüksektir.", "Genel bilgi sorularının da yanıtlandığı eğitim / içerik siteleri.", "Genel kavram açıklamaları.", "Asistan genel model bilgisini kullanabilir; fiyat, politika ve işletmeye özgü bilgide yalnız site kaynaklarına dayanır ve bunu yanıtta belirtir.")]},
 {"id": "yz_as_rules", "label": "Şeffaflık, Veri ve Güvenlik Kuralları", "en": "Transparency, Data & Safety Rules", "type": "multiselect", "showIf": SV("assistant"),
  "explanation": "Sitedeki asistanın uyması gereken kuralları belirler.",
  "scenario": "Bildirim, temsilciye devir, hassas veri yasağı ve aydınlatma her asistanda seçilir.",
  "example": "Pencere “Yapay zekâ asistanı” başlığıyla açılır; kart numarası yazılırsa maskelenir; “temsilciye bağlan” her zaman görünür.",
  "rule": "Sitedeki yapay zekâ asistanının kuralları: {labels}.",
  "options": [
   o("disclose", "Yapay zekâ olduğunu bildirir", "Konuşma başında ve pencere başlığında yapay zekâ olduğu açıkça yazar (AB YZ Yasası m. 50).", "Her asistan.", "“Yapay zekâ asistanıyla konuşuyorsunuz.”", "Asistan konuşmanın başında ve pencere başlığında yapay zekâ olduğunu açıkça bildirir; kendini insan gibi tanıtmaz."),
   o("handoff", "İnsan temsilciye geçiş", "Her adımda temsilciye geçiş; mesai dışında iletişim yolu.", "Her asistan.", "“Temsilciye bağlan” düğmesi.", "Her adımda insan temsilciye geçiş sunulur; mesai dışında çalışma saatleri ve iletişim yolu bildirilir."),
   o("no_sensitive", "Gereksiz / hassas veri istenmez", "T.C. kimlik, kart, sağlık bilgisi istenmez; yazılırsa maskelenir.", "Her asistan.", "Kart numarası *** ile maskelenir.", "Asistan gereksiz ya da hassas kişisel veri istemez; kullanıcı yazarsa kayıtta maskelenir."),
   o("notice", "Aydınlatma ve yurt dışı aktarım", "Aydınlatma metni asistanı, model sağlayıcısını ve yurt dışına aktarımı (KVKK m. 9) kapsar.", "Her asistan.", "Aydınlatma metninde “sohbet asistanı” paragrafı.", "Aydınlatma metni sohbet asistanında işlenen veriyi, model sağlayıcısını ve yurt dışına aktarım dayanağını açıkça yazar."),
   o("no_advice", "Lisans gerektiren tavsiye yok", "Sağlık, hukuk, finans tavsiyesi verilmez; uzmana yönlendirilir.", "Sağlık, hukuk, finans sektörleri.", "“Bu konuda hekiminize danışın.”", "Asistan sağlık, hukuk ve finans gibi lisans gerektiren konularda tavsiye vermez, uzmana yönlendirir."),
   o("retention", "Kayıt saklama süresi", "Konuşma kayıtlarının süresi, erişimi ve silinmesi belirli.", "Her asistan.", "Kayıtlar 90 gün, sonra anonim.", "Konuşma kayıtlarının saklama süresi ve erişim yetkisi belirlidir; süre dolunca silinir ya da anonimleştirilir; model eğitimine verilmez."),
   o("quality", "Yanıt kalitesi örneklemesi", "Yanıtlar haftalık örneklenir; yanlış bilgi kaynağıyla düzeltilir.", "Her asistan.", "Haftada 30 konuşma incelenir.", "Asistan yanıtları haftalık örneklenip doğruluk açısından kontrol edilir; yanlış yanıtın kaynağı düzeltilir ve kayda geçirilir."),
   o("abuse", "Kötüye kullanım ve istem saldırısı koruması", "İstem enjeksiyonu, sistem talimatını sızdırma ve kötüye kullanım denemelerine karşı sınırlar.", "Herkese açık asistanlar.", "Hız sınırı ve araç yetkisi kısıtı.", "Asistanın araç ve veri erişimi en düşük yetkiyle sınırlıdır; istem enjeksiyonu ve kötüye kullanıma karşı hız sınırı ve girdi denetimi uygulanır.")]}]

# 8 — Ölçüm & Takip
SECTIONS.append({
 "id": "yz_monitor", "name": "Ölçüm & Takip", "en": "AI Measurement & Monitoring", "icon": "◷", "agents": ["O", "M"],
 "refs": ["domain_name", "oc_keywords"],
 "desc": "Yapay zekâ kaynaklı ziyaretlerin, platform istatistiklerinin ve yapay zekâ yanıtlarındaki bilgi doğruluğunun nasıl izleneceğini belirler",
 "guide": {
  "purpose": "Yapay zekâ asistanlarından gelen ziyaretler ve platform istatistikleri (ChatGPT Business Hub'da son 28 günün bahsedilme ve tıklama verisi, Bing Webmaster Tools'ta AI Performance) düzenli izlenmezse emeğin karşılığı görülmez. Ayrıca asistanların işletme hakkında yanlış bilgi verip vermediği belirli sorularla düzenli test edilmelidir; SEO Denetimi'ndeki AI test sorguları aynı soru setini kullanabilir.",
  "criteria": [
   "Analitikte yapay zekâ kaynaklı oturumlar (chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com …) ayrı kanal olarak raporlanır.",
   "Platform istatistikleri aylık rapora girer.",
   "Belirlenen test soruları ayda bir platformlarda sorulur; yanlış bilgi kaynağına göre düzeltilir.",
   "Değişiklikler ve sonuçlar tarihli olarak kaydedilir."],
  "pitfalls": [
   "Yapay zekâ trafiğini “referral” içinde kaybetmek.",
   "Yanıtlardaki yanlış bilgiyi platforma yazarak düzeltmeye çalışmak: kaynak (site, profil, besleme) düzeltilmeden kalıcı düzelmez.",
   "Tek bir soruyla genel sonuç çıkarmak: yanıtlar kişiye ve zamana göre değişir.",
   "Bahsedilme sayısını sıralama ya da satış garantisi sanmak."],
  "resources": [
   r("ChatGPT'de işletmenizi kurma — istatistikler (Türkçe)", HELP + "tr-tr/articles/20001635-setting-up-your-business-on-chatgpt", "Son 28 günün bahsedilme, site tıklaması ve keşif konuları."),
   r("Bing Webmaster Tools — AI Performance", "https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview", "Copilot ve Bing yapay zekâ yanıtlarında kaynak gösterilme."),
   r("ChatGPT ile web araması", HELP + "en/articles/9237897-searching-the-web-with-chatgpt", "ChatGPT aramasının kaynakları; OAI-SearchBot izni.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_monitor_set", "label": "İzleme", "en": "Monitoring", "type": "multiselect", "showIf": SV("monitoring"),
  "explanation": "Yapay zekâ görünürlüğünün nasıl izleneceğini belirler.",
  "scenario": "Ayrı kanal, platform istatistikleri ve aylık test soruları her işletmede.",
  "example": "Aylık rapor: yapay zekâ kanalından 420 oturum, 18 form; ChatGPT'de 340 bahsedilme; 10 test sorusundan 9'unda doğru bilgi.",
  "rule": "Yapay zekâ görünürlüğünün izlenmesi: {labels}.",
  "options": [
   o("channel", "Analitikte ayrı kanal", "chatgpt.com, perplexity.ai, copilot.microsoft.com, gemini.google.com, claude.ai gibi kaynaklar özel bir kanal grubunda.", "Analitik kullanan her site.", "GA4'te “Yapay zekâ” kanal grubu.", "Analitikte yapay zekâ asistanlarından gelen oturumlar yönlendiren alan adına göre ayrı bir kanal grubunda raporlanır; liste yeni platformlarla güncellenir."),
   o("hub_insights", "ChatGPT Business Hub istatistikleri", "Bahsedilme, site tıklaması, keşif konuları (son 28 gün).", "ChatGPT profilini sahiplenenler.", "Aylık raporda ChatGPT satırı.", "ChatGPT Business Hub istatistikleri aylık raporlanır."),
   o("bing_ai", "Bing AI Performance", "Copilot ve Bing yapay zekâ yanıtlarında kaynak gösterilme ve dayanak sorguları.", "Bing Webmaster Tools kullananlar.", "Aylık AI Performance özeti.", "Bing Webmaster Tools AI Performance raporu aylık okunur ve raporlanır."),
   o("prompt_tests", "Aylık test soruları", "Ortak Bilgiler › Hedef Sorgular'dan türetilen sorular ChatGPT, Gemini, Copilot, Perplexity ve Claude'da sorulur; doğruluk ve kaynak kaydedilir.", "Her işletme.", "“[şehir]'de en iyi [hizmet] hangisi?” ve “[marka] saat kaçta açık?”", "Hedef sorgulardan türetilen test soruları ayda bir başlıca yapay zekâ asistanlarında sorulur; işletmenin geçip geçmediği, bilginin doğruluğu ve gösterilen kaynak kaydedilir."),
   o("fix_flow", "Yanlış bilgi düzeltme süreci", "Yanlış bilgi görülünce kaynağı (site, profil, besleme, dış kaynak) bulunur ve orada düzeltilir.", "Her işletme.", "Eski adres bir rehber sitesinde kalmış; düzeltme talebi gönderildi.", "Yapay zekâ yanıtında yanlış bilgi görülünce kaynağı bulunur ve kaynağında düzeltilir; takip kaydı tutulur."),
   o("quarterly", "Üç ayda bir gözden geçirme", "Platform uygunlukları (Türkiye), bot kuralları, profiller ve beslemeler düzenli gözden geçirilir.", "Her işletme.", "Ocak, Nisan, Temmuz, Ekim.", "Yapay zekâ platformlarının Türkiye uygunluğu, bot kuralları, profiller ve beslemeler üç ayda bir gözden geçirilir.")]}]

# 9 — Kurulum Planı & Talimat
SECTIONS.append({
 "id": "yz_report", "name": "Kurulum Planı & Talimat", "en": "Setup Plan & Instructions", "icon": "☰", "agents": ["M", "STR"],
 "desc": "Yapay zekâ ayarlarının teslim ve bakımını belirler; seçimlerden ayrı bir talimat (.md) üretilir",
 "guide": {
  "purpose": "Platform kayıtları, bot kuralları ve beslemeler birçok kişinin elinden geçer; ne yapıldığı kayda geçmezse ajans ya da çalışan değişince bilgi kaybolur. Bu bölüm teslim edilecekleri belirler; aşağıdaki kart seçimlerinizden ayrı bir talimat üretir.",
  "criteria": [
   "Hangi platformda hangi hesabın, kimin yetkisiyle açıldığı listelenir.",
   "Doğrulama kayıtları (DNS TXT, e-posta) ve tarihleri saklanır.",
   "robots.txt ve CDN bot kurallarındaki her değişiklik tarih ve gerekçeyle kaydedilir.",
   "Test soruları ve sonuçları aylık arşivlenir."],
  "pitfalls": [
   "Doğrulama TXT kaydını “gereksiz” diye silmek: doğrulama düşer.",
   "Platform hesaplarını kişisel e-postayla açmak.",
   "Bot kuralını değiştirip kaydını tutmamak: görünürlük düşüşünün nedeni bulunamaz.",
   "Türkiye'de açılan yeni özellikleri izlememek."],
  "resources": [
   r("Businesses in ChatGPT", OA + "business/businesses-in-chatgpt/", "Business Hub ve uygunluk."),
   r("OpenAI tarayıcıları", "https://developers.openai.com/api/docs/bots", "Bot değişikliklerinin yansıma süresi ve IP listeleri.")]}})
SECTIONS[-1]["fields"] = [
 {"id": "yz_handover", "label": "Teslim ve Bakım", "en": "Handover & Maintenance", "type": "multiselect",
  "explanation": "Yapay zekâ ayarlarının teslim edilecek belgelerini ve bakımını belirler.",
  "scenario": "Platform ve erişim listesi her kurulumda; diğerleri seçilen başlıklara göre.",
  "example": "Teslim klasöründe platform listesi, doğrulama kayıtları, robots.txt değişiklik geçmişi ve aylık test sonuçları.",
  "rule": "Yapay zekâ ayarlarının teslim ve bakımı: {labels}.",
  "options": [
   o("platforms", "Platform ve erişim listesi", "Platform, hesap, sahip, erişimi olanlar, durum (açık / bekleniyor).", "Her kurulum.", "ChatGPT Business Hub — doğrulandı — 2 kişi.", "Yapay zekâ platformları listesi (hesap, sahip, erişimi olanlar, uygunluk durumu) teslim edilir."),
   o("verifications", "Doğrulama kayıtları", "DNS TXT kayıtları, doğrulama e-postaları ve tarihleri.", "Profil sahiplenen kurulumlar.", "TXT: openai-domain-verification=… (2026-11-15).", "Doğrulama kayıtları ve tarihleri teslim edilir; DNS'teki doğrulama kayıtlarının neye ait olduğu not edilir."),
   o("bot_log", "Bot kuralı değişiklik geçmişi", "robots.txt ve CDN bot kurallarındaki değişiklikler tarih ve gerekçeyle.", "Bot izinleri belirlenen kurulumlar.", "2026-11-20: GPTBot engellendi (hukuk kararı).", "robots.txt ve CDN bot kurallarındaki değişiklikler tarih, kişi ve gerekçeyle kaydedilir."),
   o("tests", "Test soruları ve sonuçlar", "Aylık test sorularının yanıtları ve doğruluk notu.", "İzleme yapılan kurulumlar.", "Kasım: 10 sorudan 9'u doğru.", "Aylık test soruları ve sonuçları arşivlenir."),
   o("review", "Üç ayda bir gözden geçirme", "Uygunluk, kurallar, profiller, beslemeler ve asistan kayıtları.", "Her kurulum.", "Ocak, Nisan, Temmuz, Ekim.", "Yapay zekâ ayarları üç ayda bir gözden geçirilir.")]}]

IDS_ADD = []
IDS_WHEN = {}


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: kaynak.py <yapay-zeka.json>")
    out = {"version": "1.0", "group": GROUP, "agents": AGENTS, "idsAdd": IDS_ADD, "idsWhen": IDS_WHEN, "sections": SECTIONS}
    json.dump(out, open(sys.argv[1], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    nf = sum(len(s["fields"]) for s in SECTIONS)
    print(f"{len(SECTIONS)} bölüm, {nf} karar, {sum(len(s['guide']['resources']) for s in SECTIONS)} kaynak")


if __name__ == "__main__":
    main()
