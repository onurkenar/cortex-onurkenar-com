#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tasarim-stilleri.json'a Faz 5 verisini yazar: Tasarım Parametreleri bölümü, 10 parametre alanı (token eşlemeli),
stil profilleri (parametre önerileri), layout öneri kuralları ve sayfa türleri (kullanıcı yönergesi 2026-11-07, Faz 5–6).

Kullanım: python3 -I docs/tasarim-stilleri/kaynak_v3.py docs/tasarim-stilleri/tasarim-stilleri.json
Tekrar çalıştırılabilir: params, section, guide, profiles, existingRec, layoutRec, pages anahtarlarını üzerine yazar.
"""
import json
import sys

SECTION = {"after": "design_style", "id": "design_params", "name": "Tasarım Parametreleri", "en": "Design Parameters",
           "group": "Tasarım & Arayüz", "icon": "▥",
           "desc": "Seçilen stil ve düzeni ölçülebilir kurallara çevirir: boşluk yoğunluğu, ızgara, yüzey, görsel işleme, hizalama, açılış kompozisyonu, bölüm ritmi, kapsayıcı genişliği, etkileşim yoğunluğu ve gezinme. Köşe yuvarlaklığı ve gölge Kurumsal Kimlik'te, renk modu ve hareket teknikleri Tema, Hareket & Tasarım'da kalır. Bu kararlardan tasarım token'ları, JSON yapılandırması ve Claude için tasarım şartnamesi üretilir."}
GUIDE = {"purpose": "Bu bölüm tasarım stilini geliştiricinin uygulayabileceği somut değerlere çevirir. Burada verilen kararlar CSS değişkenlerine (design token), bileşen ve responsive kurallarına dönüşür; böylece aynı stil her sayfada aynı boşluk, ızgara, yüzey ve hareket kurallarıyla uygulanır.",
         "criteria": ["Her parametrenin altında, seçtiğiniz ana stile göre bir öneri görünür; öneri yalnız “Öneriyi uygula” ile uygulanır, kendiliğinden değişmez.",
                      "Yoğunluk ve kapsayıcı genişliği içerik miktarına göre seçin: çok bilgi gösteren paneller sıkı ve geniş, marka ve hikâye sayfaları ferah ve dar ölçüyle daha iyi okunur.",
                      "Etkileşim yoğunluğu arttıkça performans ve erişilebilirlik yükü artar; hareket azaltma tercihi her seçimde geçerlidir.",
                      "Köşe yuvarlaklığı, gölge, renk ve font zaten Kurumsal Kimlik ve Ortak Bilgiler'de seçiliyse burada tekrar seçilmez; tasarım çıktısı onları oradan okur.",
                      "Kararlar tamamlandığında bölümün başındaki “Tasarım çıktısı” kartından JSON yapılandırmasını ve CSS token'larını indirebilir, şartnameyi kopyalayabilirsiniz."],
         "pitfalls": ["Aynı sayfada farklı yoğunluk ve köşe kuralları kullanmak tutarsız görünür; istisnaları sayfa bazlı layout'la sınırlayın.",
                      "Glass ya da katmanlı yüzeylerde metin kontrastı her arka planda yeniden denetlenmelidir.",
                      "Tam genişlik kapsayıcıda metin satırları çok uzar; metin blokları her durumda 60–75 karakterle sınırlanmalıdır.",
                      "Alt gezinme çubuğu yalnız mobilde ve en çok beş hedefle kullanılmalıdır."],
         "resources": [{"title": "W3C — WCAG 2.2", "url": "https://www.w3.org/TR/WCAG22/", "note": "Kontrast, odak görünürlüğü, hedef boyutu ve hareket ölçütleri."},
                       {"title": "Design Tokens Community Group — Format Module", "url": "https://www.designtokens.org/tr/drafts/format/", "note": "Tasarım token'larının paylaşılabilir JSON biçimi (taslak)."},
                       {"title": "MDN — prefers-reduced-motion", "url": "https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/At-rules/@media/prefers-reduced-motion", "note": "Hareket azaltma tercihine uyum."}]}

def O(v, l, x, s, e, t=None):
    o = {"value": v, "label": l, "explanation": x, "scenario": s, "example": e}
    if t:
        o["tokens"] = t
    return o

PARAMS = [
 {"id": "design_density", "label": "Görsel Yoğunluk", "en": "Visual Density", "after": None,
  "explanation": "Bileşenler ve bölümler arasındaki boşluk miktarını belirler; 8 noktalı boşluk ölçeğinin temel birimine dönüşür.",
  "rule": "Arayüzün görsel yoğunluğu {label} olacaktır; bileşen içi ve bölümler arası boşluklar bu ölçekteki token'larla verilecek, rastgele değer kullanılmayacaktır.",
  "scenario": "Ana stil seçildikten sonra; özellikle hem pazarlama sayfası hem panel içeren projelerde.",
  "example": "Ferah seçilen bir mimarlık sitesinde bölümler arasında 128 px boşluk; sıkı seçilen bir yönetim panelinde 48 px boşluk ve yoğun tablolar.",
  "options": [O("Ultra Spacious", "Ultra Spacious — Çok ferah", "Çok geniş boşluk, az öğe; içerik nefes alır. Artısı: premium ve sakin. Eksisi: kaydırma uzar, bilgi yoğun sayfalara uymaz.", "Lüks marka, sanat ve mimarlık portfolyosu.", "Bir saat markasında ürün fotoğrafı ekranın ortasında yalnız durur, çevresinde geniş boşluk vardır.", {"space": 12, "section": 160, "lh": 1.75}),
              O("Spacious", "Spacious — Ferah", "Bol boşluk, rahat okuma. Artısı: odaklı ve modern. Eksisi: ekran başına daha az bilgi.", "Kurumsal tanıtım, hizmet ve marka siteleri.", "Bir danışmanlık sitesinde her hizmet bloğu arasında geniş boşluk vardır.", {"space": 10, "section": 128, "lh": 1.7}),
              O("Balanced", "Balanced — Dengeli", "Genel amaçlı orta yoğunluk. Artısı: çoğu sayfaya uyar. Eksisi: ayırt edici değildir.", "Belirgin bir ihtiyaç yoksa varsayılan seçim.", "Bir e-ticaret sitesinde kartlar arası 24 px, bölümler arası 96 px boşluk.", {"space": 8, "section": 96, "lh": 1.6}),
              O("Compact", "Compact — Sıkı", "Daha az boşluk, daha çok içerik. Artısı: verimli tarama. Eksisi: dikkat dağılabilir; dokunma hedefleri yine 24 px'in altına inmez.", "SaaS ürün sayfaları, kataloglar, dokümantasyon.", "Bir yazılım dokümantasyonunda kenar menüsü ve içerik sık ama düzenli yerleşir.", {"space": 6, "section": 72, "lh": 1.55}),
              O("Dense", "Dense — Yoğun", "En sık yerleşim; tablolar ve paneller. Artısı: tek ekranda çok veri. Eksisi: pazarlama sayfalarında yorucu.", "Yönetim paneli, analitik ve veri ağırlıklı ekranlar.", "Bir analitik panelinde 16 gösterge tek ekrana sığar.", {"space": 4, "section": 48, "lh": 1.5})]},
 {"id": "design_grid", "label": "Izgara Sistemi", "en": "Grid System",
  "explanation": "Masaüstündeki sütun sayısını belirler; tablet ve mobil sütunları bundan türetilir (tablet en çok 8, mobil 4).",
  "rule": "Sayfa ızgarası {label} olacaktır; tablet ve mobilde sütun sayısı tasarım yapılandırmasındaki değerlere iner ve bileşenler sütun sınırlarına hizalanır.",
  "scenario": "Layout seçildikten sonra; özellikle modüler, bento ve panel düzenlerinde.",
  "example": "12 sütunlu ızgarada açılış görseli 7, metin 5 sütun kaplar; mobilde ikisi 4 sütunun tamamına yayılır.",
  "options": [O("Grid 4", "4 Columns — 4 sütun", "Basit, tek amaçlı sayfalar. Artısı: sade. Eksisi: karmaşık düzen kurulamaz.", "Tek sayfalık tanıtım, açılış sayfası.", "Bir etkinlik sayfası 4 sütunlu ızgarada iki büyük blokla kurulur.", {"cols": [4, 4, 4]}),
              O("Grid 8", "8 Columns — 8 sütun", "Orta karmaşıklık; mobil öncelikli tasarımlara uygun.", "Mobil uygulama tanıtımı, kişisel site.", "Bir uygulama tanıtımında özellikler 8 sütunda ikişerli dizilir.", {"cols": [8, 8, 4]}),
              O("Grid 12", "12 Columns — 12 sütun", "Web'in standart ızgarası; 2, 3, 4 ve 6'lı bölünmelere izin verir.", "Kurumsal, e-ticaret ve içerik siteleri; varsayılan.", "Bir kurumsal sitede hizmet kartları 3'lü, referanslar 4'lü dizilir.", {"cols": [12, 8, 4]}),
              O("Grid 16", "16 Columns — 16 sütun", "İnce bölünmeler; geniş ekran panelleri. Eksisi: tasarım ve bakım zorlaşır.", "Analitik panel, veri yoğun yönetim ekranı.", "Bir veri panelinde göstergeler 4, grafikler 8 sütun kaplar.", {"cols": [16, 8, 4]}),
              O("Grid Fluid", "Fluid — Akışkan ızgara", "Sabit sütun yerine içeriğe göre kendiliğinden kırılan ızgara (auto-fit / minmax).", "Galeri, kart koleksiyonu, deneysel düzenler.", "Bir galeride kartlar en az 280 px genişlikte ekrana sığdığı kadar dizilir.", {"cols": ["fluid", "fluid", "fluid"]})]},
 {"id": "design_surface_treatment", "label": "Yüzey İşleme", "en": "Surface Treatment",
  "explanation": "Kart ve panellerin genel yüzey karakteri. Yüzey / Derinlik Efekti kararındaki stil efektini (ör. cam) hangi yüzeylere uygulayacağınızın temelidir.",
  "rule": "Bileşen yüzeyleri {label} karakterde olacaktır; yüzey token'ları (zemin, kenarlık, yükseklik) bütün kart, panel ve açılır menülerde aynı kullanılacaktır.",
  "scenario": "Ana stil ve yüzey efekti seçildikten sonra.",
  "example": "Elevated seçilen bir SaaS sitesinde kartlar beyaz zeminden hafif gölgeyle ayrılır; Flat seçilen bir kamu sitesinde ince kenarlıkla ayrılır.",
  "options": [O("Flat", "Flat — Düz", "Gölgesiz, kenarlık ya da renkle ayrılan yüzeyler.", "Kamu, kurumsal ve yüksek erişilebilirlik hedefli siteler.", "Kartlar açık gri zeminde ince kenarlıklıdır.", {"elev": "none"}),
              O("Elevated", "Elevated — Yükseltilmiş", "Hafif gölgeyle zeminden ayrılan katmanlar.", "SaaS, uygulama ve e-ticaret arayüzleri.", "Ürün kartı fareyle üzerine gelince biraz yükselir.", {"elev": "soft"}),
              O("Glass", "Glass — Cam", "Yarı saydam, arka planı bulanıklaştıran yüzeyler; yedek düz yüzey şart.", "Yapay zekâ, fintech ve uygulama tanıtımları.", "Gezinme çubuğu kaydırırken arkadaki içeriği buzlu cam gibi gösterir.", {"elev": "glass"}),
              O("Textured", "Textured — Dokulu", "Kâğıt, tahıl ya da desen dokulu yüzeyler.", "El yapımı ürün, sürdürülebilir marka, kültür sitesi.", "Bloklar hafif kâğıt dokulu krem zeminde durur.", {"elev": "texture"}),
              O("Layered", "Layered — Katmanlı", "Üst üste binen, derinlik hissi veren yüzeyler.", "Editoryal, kreatif ajans, lansman sayfası.", "Metin kartı fotoğrafın köşesine taşar.", {"elev": "layered"})]},
 {"id": "design_image_treatment", "label": "Görsel İşleme", "en": "Image Treatment",
  "explanation": "Fotoğraf ve görsellerin sitede nasıl işleneceği; görsel dilin tutarlılığını sağlar.",
  "rule": "Görseller {label} işlemeyle sunulacaktır; işleme CSS ya da üretim aşamasında tutarlı uygulanacak, ürün renklerinin doğru görünmesi gereken yerlerde bozulmayacaktır.",
  "scenario": "Medya yaklaşımı ve marka renkleri belirlendikten sonra.",
  "example": "Duotone seçilen bir konferans sitesinde bütün konuşmacı fotoğrafları lacivert-pembe çift tona çevrilir.",
  "options": [O("Natural", "Natural — Doğal", "Görseller gerçek renkleriyle; yalnız ışık ve kırpım düzeltmesi.", "Ürün, yemek, turizm ve sağlık siteleri.", "Restoran fotoğrafları gerçek renkleriyle gösterilir.", {"img": "none"}),
              O("Duotone", "Duotone — Çift ton", "İki marka rengine indirgenmiş görseller.", "Kampanya, konferans, farklı kaynaklı fotoğraflar.", "Konuşmacı portreleri iki renkte tek kimliğe kavuşur.", {"img": "duotone"}),
              O("Monochrome", "Monochrome — Tek renk", "Siyah-beyaz ya da tek tonlu görseller.", "Mimarlık, hukuk, editoryal ve lüks siteler.", "Ekip fotoğrafları siyah-beyaz sunulur.", {"img": "grayscale(1)"}),
              O("Cinematic", "Cinematic — Sinematik", "Geniş en-boy oranı, koyu ve kontrastlı renk düzeltmesi.", "Otomotiv, film, destinasyon ve prestij lansmanı.", "Açılış görseli 21:9 oranında, koyu tonlu bir sahnedir.", {"img": "contrast(1.1) saturate(.9)"}),
              O("Illustrated", "Illustrated — İllüstrasyon", "Fotoğraf yerine illüstrasyon ya da ikon ağırlıklı görsel dil.", "Eğitim, SaaS anlatımı, çocuk ve topluluk siteleri.", "Her özellik kartında küçük bir çizim yer alır.", {"img": "none"})]},
 {"id": "design_alignment", "label": "İçerik Hizalaması", "en": "Content Alignment",
  "explanation": "Başlık, metin ve blokların genel hizalama kuralı.",
  "rule": "İçerik hizalaması {label} olacaktır; uzun metin her durumda sola hizalı kalacak, ortalanmış metin kısa başlık ve açıklamalarla sınırlanacaktır.",
  "scenario": "Layout ve açılış kompozisyonu seçilirken.",
  "example": "Asimetrik seçilen bir ajans sitesinde başlık sola, görsel sağa taşar; ritim her bölümde değişir.",
  "options": [O("Left", "Left — Sola hizalı", "Okunabilirliği en yüksek, taranması kolay hizalama.", "Kurumsal, içerik ve dokümantasyon siteleri.", "Bütün başlıklar ve paragraflar sol kenardan başlar.", None),
              O("Center", "Center — Ortalanmış", "Kısa mesajlar ve açılışlar için simetrik düzen.", "Açılış sayfası, lansman ve etkinlik.", "Açılış başlığı ve düğme ekranın ortasındadır.", None),
              O("Asymmetric", "Asymmetric — Asimetrik", "Dengeli ama simetrik olmayan, dinamik kompozisyon.", "Kreatif ajans, moda ve kültür siteleri.", "Görsel sayfanın üçte ikisini kaplar, metin dar sütunda kalır.", None),
              O("Mixed", "Mixed — Karışık", "Açılış ortada, içerik solda gibi bölüme göre değişen hizalama.", "Çoğu pazarlama sitesi.", "Açılış ortalanmış, hizmet listeleri sola hizalıdır.", None)]},
 {"id": "design_hero", "label": "Açılış (Hero) Kompozisyonu", "en": "Hero Composition",
  "explanation": "Ana sayfanın ilk ekranının kuruluşu; ilk izlenimi ve LCP performansını belirler.",
  "rule": "Ana sayfa açılışı {label} kompozisyonunda olacaktır; ilk ekranda tek bir ana mesaj ve tek bir birincil eylem bulunacak, açılış görseli ya da videosu öncelikli ve optimize yüklenecektir.",
  "scenario": "Ana sayfa tasarlanırken; sayfa bazlı layout'la birlikte.",
  "example": "Split seçilen bir SaaS sitesinde solda başlık ve düğme, sağda ürün ekranı durur.",
  "options": [O("Hero Centered", "Centered — Ortalanmış", "Tek mesaj ve eylem ortada.", "Ürün, uygulama ve etkinlik.", "Ortada büyük başlık, altında tek düğme.", None),
              O("Hero Split", "Split — İkiye bölünmüş", "Metin ve görsel yan yana.", "SaaS, kurumsal ve hizmet siteleri.", "Solda değer önerisi, sağda ürün görseli.", None),
              O("Hero Full-Bleed", "Full-Bleed — Tam genişlik görsel", "Ekranı kaplayan görsel üzerinde metin.", "Turizm, mimarlık, restoran.", "Otel fotoğrafı ekranı kaplar, başlık sol altta durur.", None),
              O("Hero Video", "Video — Video açılış", "Sessiz, kısa ve durdurulabilir arka plan videosu.", "Otomotiv, etkinlik ve marka lansmanı.", "Sessiz döngü videonun üzerinde başlık ve ‘Videoyu durdur’ düğmesi.", None),
              O("Hero Editorial", "Editorial — Editoryal", "Dergi kapağı gibi büyük tipografi ve kırpılmış görsel.", "Yayın, moda ve kültür kurumları.", "Dev başlık görselin üzerine taşar, yanında sayı etiketi.", None)]},
 {"id": "design_rhythm", "label": "Bölüm Ritmi", "en": "Section Rhythm",
  "explanation": "Sayfa boyunca bölümlerin yerleşim ve zemin değişim düzeni.",
  "rule": "Bölüm ritmi {label} olacaktır; bölümler arası boşluk yoğunluk token'ından gelecek ve ritim kırılmaları bilinçli olarak kullanılacaktır.",
  "scenario": "Uzun sayfalar ve ana sayfa kurgusunda.",
  "example": "Alternating seçilen bir hizmet sayfasında görsel-metin blokları sırayla sağa ve sola yerleşir.",
  "options": [O("Uniform", "Uniform — Tekdüze", "Her bölüm aynı yapı ve zeminde; öngörülebilir.", "Kurumsal, kamu ve dokümantasyon.", "Bütün bölümler beyaz zeminde aynı ızgarada.", None),
              O("Alternating", "Alternating — Dönüşümlü", "Görsel-metin yönü ve zemin rengi sırayla değişir.", "Hizmet ve ürün tanıtımı.", "Bir bölüm açık griyle, sonraki beyazla; görseller sırayla sağ ve sol.", None),
              O("Dynamic", "Dynamic — Dinamik", "Her bölüm kendine özgü kompozisyonla; sürpriz ve hareket.", "Kreatif ajans, kampanya, lansman.", "Bir bölüm tam ekran görsel, sonraki asimetrik kolaj, sonraki dev sayılar.", None)]},
 {"id": "design_container", "label": "Kapsayıcı Genişliği", "en": "Container Width",
  "explanation": "İçeriğin masaüstünde yayılabileceği en büyük genişlik.",
  "rule": "İçerik kapsayıcısı {label} olacaktır; metin blokları her durumda 60–75 karakterlik satır uzunluğuyla sınırlanacaktır.",
  "scenario": "Ekran genişliği ve içerik türüne göre.",
  "example": "Standart seçilen bir sitede içerik 1200 px'te ortalanır; Full seçilen bir galeride görseller kenardan kenara yayılır.",
  "options": [O("Narrow", "Narrow — Dar (960 px)", "Okuma odaklı, dar ölçü.", "Blog, makale, kişisel site.", "Makale 960 px genişlikte ortalanır.", {"max": "960px"}),
              O("Standard", "Standard — Standart (1200 px)", "Çoğu site için dengeli genişlik.", "Kurumsal, e-ticaret ve hizmet siteleri.", "İçerik 1200 px genişlikte ortalanır.", {"max": "1200px"}),
              O("Wide", "Wide — Geniş (1440 px)", "Geniş ekranlarda daha çok içerik.", "Panel, katalog ve veri ağırlıklı siteler.", "Ürün ızgarası 1440 px'e kadar genişler.", {"max": "1440px"}),
              O("Full", "Full — Tam genişlik", "Kenardan kenara; metin blokları yine sınırlı.", "Fotoğraf, galeri ve sinematik siteler.", "Görseller ekranın tamamını kaplar, metin 720 px'te kalır.", {"max": "100%"})]},
 {"id": "design_interaction_intensity", "label": "Etkileşim Yoğunluğu", "en": "Interaction Intensity",
  "explanation": "Geçiş, hover ve kaydırma animasyonlarının ne kadar belirgin olacağı. Hangi tekniklerin kullanılacağı Tema, Hareket & Tasarım bölümündeki Hareket & Etkileşim Teknikleri kararındadır.",
  "rule": "Etkileşim yoğunluğu {label} olacaktır; animasyon süreleri hareket token'larından gelecek, prefers-reduced-motion tercihinde hareketler durdurulacak ya da yalnız opaklık geçişine inecektir.",
  "scenario": "Ana stil ve hareket teknikleri seçildikten sonra.",
  "example": "Subtle seçilen bir fintech sitesinde düğmeler 150 ms'de renk değiştirir; Expressive seçilen bir lansmanda bölümler kaydırmayla sahnelenir.",
  "options": [O("Static", "Static — Durağan", "Yalnız odak ve durum değişimleri; animasyon yok.", "Kamu, sağlık ve yüksek erişilebilirlik hedefli siteler.", "Düğme durumları anında değişir.", {"dur": "0ms"}),
              O("Subtle", "Subtle — Hafif", "Kısa, fark edilmeyen geçişler.", "Kurumsal, fintech ve çoğu site; varsayılan.", "Kart üzerine gelince 150 ms'de hafifçe yükselir.", {"dur": "150ms"}),
              O("Moderate", "Moderate — Orta", "Belirgin ama ölçülü animasyonlar.", "SaaS, e-ticaret, uygulama tanıtımı.", "Bölümler kaydırınca hafifçe belirir.", {"dur": "250ms"}),
              O("Expressive", "Expressive — Belirgin", "Anlatının parçası olan, sahne kuran hareketler.", "Lansman, kreatif ajans, deneyim siteleri.", "Başlıklar harf harf belirir, görseller paralaksla kayar.", {"dur": "400ms"})]},
 {"id": "design_navigation", "label": "Gezinme Kalıbı", "en": "Navigation Pattern",
  "explanation": "Ana menünün biçimi; site haritasının derinliğine ve cihaz kullanımına göre seçilir.",
  "rule": "Ana gezinme {label} kalıbında olacaktır; menü klavyeyle tam kullanılabilecek, mobilde erişilebilir bir çekmece ya da alt çubuğa dönüşecek ve ‘içeriğe atla’ bağlantısı bulunacaktır.",
  "scenario": "Site haritası belirlendikten sonra.",
  "example": "Mega Menu seçilen bir sanayi sitesinde ‘Ürünler’ menüsü ürün gruplarını görselli sütunlarla açar.",
  "options": [O("Top Nav", "Top Nav — Üst menü", "Yatay üst menü; mobilde çekmece.", "Çoğu site; 5–7 ana başlık.", "Logo solda, 6 başlık sağda.", None),
              O("Mega Menu", "Mega Menu — Geniş açılır menü", "Çok sütunlu, görselli alt menüler.", "Çok ürünlü kurumsal ve e-ticaret siteleri.", "Ürünler menüsü kategorileri dört sütunda açar.", None),
              O("Sidebar", "Sidebar — Kenar menü", "Sol kenarda sabit menü.", "Dokümantasyon, panel ve uygulamalar.", "Solda sabit başlık ağacı.", None),
              O("Bottom Nav", "Bottom Nav — Alt çubuk (mobil)", "Mobilde başparmakla erişilen alt sekme çubuğu; en çok 5 hedef.", "Uygulama benzeri mobil öncelikli siteler.", "Mobilde Ana sayfa, Ara, Sepet, Hesabım sekmeleri altta.", None),
              O("Hybrid", "Hybrid — Karma", "Masaüstünde üst menü + bağlam kenar menüsü, mobilde alt çubuk.", "SaaS, portal ve hesap içeren siteler.", "Üstte ana menü, hesap sayfalarında solda alt menü.", None)]},
]

# Stil profilleri: parametre → değer → stiller. Listede olmayan stil varsayılanı alır.
PROF = {
 "design_density": {"_": "Balanced", "Ultra Spacious": ["Luxury", "Japandi", "Art Direction-Led"], "Spacious": ["Minimalism", "Scandinavian", "Editorial Magazine", "Cinematic", "Photography-Led", "Eco Sustainable", "Typography-Led", "Immersive", "Kinetic Type"], "Compact": ["Material Design", "SaaS Product-Led", "Fintech Trust", "Swiss Style", "Brutalism", "Flat 2.0", "Dark-First"], "Dense": ["Data Viz-Led", "Industrial", "Cyberpunk"]},
 "design_grid": {"_": "Grid 12", "Grid 16": ["Data Viz-Led", "Industrial"], "Grid 8": ["Playful", "Claymorphism", "Neo-Memphis"], "Grid Fluid": ["Organic", "Liquid Fluid", "Anti-Design", "Immersive", "Collage", "Maximalism", "Psychedelic"]},
 "design_surface_treatment": {"_": "Flat", "Elevated": ["Material Design", "SaaS Product-Led", "Flat 2.0", "Corporate Modern", "Fintech Trust", "Claymorphism", "Neumorphism", "Playful", "Dark-First"], "Glass": ["Glassmorphism", "Liquid Glass", "AI-Native", "Web3 Digital Native", "Futuristic"], "Textured": ["Vintage", "Grunge", "Eco Sustainable", "Hand-Drawn", "Skeuomorphism", "Japandi", "Organic"], "Layered": ["Art Direction-Led", "Collage", "Paper-Cut", "3D-Led", "Immersive", "Liquid Fluid", "Maximalism"]},
 "design_image_treatment": {"_": "Natural", "Duotone": ["Duotone", "Constructivism"], "Monochrome": ["Monochromatic", "Brutalism", "Swiss Style", "Typography-Led"], "Cinematic": ["Cinematic", "Immersive", "Luxury", "Dark-First", "Art Direction-Led"], "Illustrated": ["Illustration-Led", "Hand-Drawn", "Playful", "Isometric", "Memphis", "Neo-Memphis", "Pixel Art", "Paper-Cut", "Flat Design", "Claymorphism"]},
 "design_alignment": {"_": "Mixed", "Left": ["Swiss Style", "Corporate Modern", "Fintech Trust", "Data Viz-Led", "Industrial", "Editorial Magazine", "Material Design", "Dark-First"], "Center": ["Minimalism", "Luxury", "Immersive", "Kinetic Type", "AI-Native", "Art Deco", "Cinematic"], "Asymmetric": ["Art Direction-Led", "Constructivism", "Anti-Design", "Brutalism", "Neobrutalism", "Collage", "Japandi", "Maximalism"]},
 "design_hero": {"_": "Hero Split", "Hero Centered": ["Minimalism", "AI-Native", "Kinetic Type", "Art Deco", "Typography-Led", "Accessible-First"], "Hero Full-Bleed": ["Photography-Led", "Luxury", "Eco Sustainable", "Liquid Fluid", "Duotone"], "Hero Video": ["Cinematic", "3D-Led", "Immersive"], "Hero Editorial": ["Editorial Magazine", "Art Direction-Led", "Swiss Style", "Japandi", "Collage", "Brutalism", "Constructivism"]},
 "design_rhythm": {"_": "Alternating", "Uniform": ["Swiss Style", "Corporate Modern", "Material Design", "Industrial", "Data Viz-Led", "Fintech Trust", "Minimalism", "Dark-First"], "Dynamic": ["Maximalism", "Anti-Design", "Art Direction-Led", "Immersive", "Collage", "Memphis", "Y2K", "Psychedelic", "Kinetic Type", "Neobrutalism", "Liquid Fluid"]},
 "design_container": {"_": "Standard", "Narrow": ["Editorial Magazine", "Japandi", "Typography-Led"], "Wide": ["Data Viz-Led", "Material Design", "Industrial", "SaaS Product-Led", "Dark-First"], "Full": ["Photography-Led", "Cinematic", "Immersive", "Art Direction-Led", "Kinetic Type", "Liquid Fluid"]},
 "design_interaction_intensity": {"_": "Subtle", "Static": ["Brutalism", "Swiss Style"], "Moderate": ["SaaS Product-Led", "Material Design", "Glassmorphism", "Liquid Glass", "Playful", "Claymorphism", "AI-Native", "Web3 Digital Native", "Neobrutalism", "Neo-Memphis", "Y2K"], "Expressive": ["Kinetic Type", "Immersive", "Liquid Fluid", "Psychedelic", "Synthwave", "Maximalism", "3D-Led", "Cyberpunk", "Cinematic", "Anti-Design"]},
 "design_navigation": {"_": "Top Nav", "Mega Menu": ["Corporate Modern", "Industrial"], "Sidebar": ["Data Viz-Led", "Dark-First"], "Hybrid": ["SaaS Product-Led", "AI-Native", "Material Design", "Fintech Trust"]},
 "brand_radius": {"_": "Small", "None": ["Brutalism", "Swiss Style", "Constructivism", "Industrial", "Art Deco", "Editorial Magazine", "Bauhaus", "Pixel Art", "Cyberpunk", "Futuristic", "Grunge", "Typography-Led", "Art Direction-Led", "Luxury", "Duotone", "Kinetic Type"], "Medium": ["SaaS Product-Led", "Material Design", "Flat 2.0", "Scandinavian", "Eco Sustainable", "AI-Native", "Dark-First", "Web3 Digital Native", "Neo-Memphis", "Illustration-Led"], "Large": ["Glassmorphism", "Claymorphism", "Neumorphism", "Liquid Glass", "Liquid Fluid", "Playful", "Organic"], "Pill": ["Y2K"]},
 "brand_shadow": {"_": "Soft", "Flat": ["Flat Design", "Swiss Style", "Brutalism", "Minimalism", "Typography-Led", "Editorial Magazine", "Bauhaus", "Constructivism", "Pixel Art", "Monochromatic", "Duotone", "Industrial", "Japandi", "Art Deco", "Luxury", "Accessible-First"], "Layered": ["3D-Led", "Glassmorphism", "Liquid Glass", "Skeuomorphism", "Paper-Cut", "Immersive", "Collage", "Art Direction-Led"]},
}

# Layout öneri kuralları (kural tabanlı, ağırlıkları açık; ölçülmüş kullanıcı performansı değildir)
STYLE_LAY = {"Corporate Modern": ["Modular Grid", "Split Screen"], "Swiss Style": ["Modular Grid", "Editorial"], "Luxury": ["Full Bleed", "Editorial"],
             "SaaS Product-Led": ["Bento Grid", "Long Scroll"], "Minimalism": ["Centered Hero", "Modular Grid"], "Neobrutalism": ["Asymmetric Grid", "Card Based"],
             "Photography-Led": ["Gallery", "Full Bleed"], "Cinematic": ["Scrollytelling", "Full Bleed"], "Data Viz-Led": ["Dashboard", "Modular Grid"], "AI-Native": ["Bento Grid", "Split Screen"]}
CLASS_LAY = {"primary-style": ["Modular Grid", "Card Based"], "brand-style": ["Modular Grid", "Split Screen"], "visual-approach": ["Editorial", "Asymmetric Grid"],
             "surface-effect": ["Bento Grid", "Card Based"], "media-approach": ["Full Bleed", "Gallery"], "theme-approach": ["Bento Grid", "Modular Grid"],
             "interaction-approach": ["Scrollytelling", "Long Scroll"]}
TYPE_LAY = {"Corporate Website": ["Modular Grid", "Split Screen", "Sticky Sections"], "Personal Website": ["Centered Hero", "Editorial"], "Portfolio": ["Gallery", "Masonry", "Horizontal Scroll"],
            "Blog": ["F-Pattern", "Editorial", "Card Based"], "News Media": ["Editorial", "F-Pattern", "Modular Grid"], "Landing Page": ["Centered Hero", "Z-Pattern", "Long Scroll"],
            "SaaS": ["Bento Grid", "Long Scroll", "Sticky Sections"], "Web App": ["Dashboard", "Sidebar Navigation", "Configurator Workspace"], "Portal": ["Sidebar Navigation", "Dashboard", "Card Based"],
            "Community": ["Card Based", "Masonry"], "Marketplace": ["Card Based", "Modular Grid"], "E-commerce": ["Card Based", "Modular Grid", "Configurator Workspace"],
            "B2B Platform": ["Modular Grid", "Dashboard", "Split Screen"], "Booking": ["Split Screen", "Card Based", "Configurator Workspace"], "Classifieds": ["Card Based", "F-Pattern"],
            "LMS": ["Sidebar Navigation", "Card Based", "Dashboard"], "Knowledge Base": ["Sidebar Navigation", "F-Pattern"], "Intranet": ["Dashboard", "Sidebar Navigation"],
            "Directory": ["Card Based", "F-Pattern"], "Event": ["Centered Hero", "Full Bleed", "Long Scroll"], "Nonprofit": ["Long Scroll", "Full Bleed", "Scrollytelling"],
            "Government": ["Modular Grid", "F-Pattern", "Sidebar Navigation"]}
SECTOR_LAY = {"finance": ["Modular Grid", "Split Screen"], "professional": ["Modular Grid", "Split Screen"], "tourism": ["Full Bleed", "Gallery"], "food": ["Full Bleed", "Gallery"],
              "beauty": ["Full Bleed", "Layered"], "media": ["Editorial", "Masonry"], "tech": ["Bento Grid", "Long Scroll"], "education": ["Card Based", "Sidebar Navigation"],
              "public": ["Modular Grid", "F-Pattern"], "ngo": ["Long Scroll", "Scrollytelling"], "manufacturing": ["Modular Grid", "Full Bleed"], "construction": ["Full Bleed", "Gallery"],
              "automotive": ["Full Bleed", "Configurator Workspace"], "energy": ["Modular Grid", "Scrollytelling"], "logistics": ["Modular Grid", "Split Screen"],
              "retail": ["Card Based", "Gallery"], "health": ["Modular Grid", "Centered Hero"]}
LAYREC = {"weights": {"main": 40, "mainAlt": 30, "mainRef": 15, "secondary": 10, "type": 20, "sector": 10, "audience": 5, "conversion": 10, "density": 10, "page": 50, "pageMiss": -20, "perf": -10, "a11y": -10, "base": 20},
          "style": STYLE_LAY, "cls": CLASS_LAY, "type": TYPE_LAY, "sector": SECTOR_LAY,
          "b2b": ["Modular Grid", "Split Screen", "Sticky Sections"], "b2c": ["Card Based", "Full Bleed", "Long Scroll"],
          "conversion": ["Centered Hero", "Z-Pattern", "Split Screen", "Long Scroll", "Sticky Sections"],
          "dense": ["Dashboard", "Modular Grid", "Card Based", "Sidebar Navigation", "F-Pattern"], "spacious": ["Centered Hero", "Full Bleed", "Editorial", "Z-Pattern"],
          "heavy": ["Horizontal Scroll", "Scrollytelling", "Layered", "Masonry", "Gallery", "Configurator Workspace"],
          "a11yRisk": ["Horizontal Scroll", "Scrollytelling", "Layered", "Masonry", "Asymmetric Grid"]}
PAGES = [["home", "Ana sayfa"], ["product", "Hizmet / Ürün"], ["about", "Hakkımızda"], ["blog", "Blog listeleme"], ["post", "Blog detay"], ["contact", "İletişim"],
         ["landing", "Landing Page"], ["dashboard", "Dashboard"], ["auth", "Üyelik / Giriş"], ["custom", "Özel sayfa"]]


def main():
    p = sys.argv[1]
    src = json.load(open(p, encoding='utf-8'))
    src['section'] = SECTION
    src['guide'] = GUIDE
    src['params'] = PARAMS
    src['profiles'] = PROF
    src['layoutRec'] = LAYREC
    src['pages'] = PAGES
    json.dump(src, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('parametre', len(PARAMS), 'profil', len(PROF), 'sayfa', len(PAGES))


if __name__ == '__main__':
    main()
