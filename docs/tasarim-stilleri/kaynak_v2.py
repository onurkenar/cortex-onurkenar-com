#!/usr/bin/env python3
"""tasarim-stilleri.json'a V2 tasarım kütüphanesi verisini yazar (kullanıcı yönergesi 2026-11-07, Faz 2).

Kullanım: python3 -I docs/tasarim-stilleri/kaynak_v2.py docs/tasarim-stilleri/tasarim-stilleri.json
Tekrar çalıştırılabilir: yalnız aşağıdaki anahtarları üzerine yazar (add listesine yeni stilleri ekler,
var olanları değiştirmez; rename, classes, styleMeta, principle, newFields, layouts anahtarlarını yazar).
"""
import json
import sys

# ---- 8 sınıf (yönerge §3) ----
CLASSES = [
    ["primary-style", "Temel tasarım dili"],
    ["brand-style", "Marka / sektör yaklaşımı"],
    ["visual-approach", "Görsel iletişim yaklaşımı"],
    ["surface-effect", "Yüzey / derinlik efekti"],
    ["media-approach", "Medya sunum yaklaşımı"],
    ["theme-approach", "Tema yaklaşımı"],
    ["interaction-approach", "Etkileşim yaklaşımı"],
    ["design-principle", "Genel tasarım ilkesi"],
]

# ---- çakışan 6 stil yönergedeki adı alır (değer aynı kalır, kayıtlar bozulmaz) ----
RENAME = {
    "Japandi": "Japanese Minimalism / Wabi-Sabi — Japon Minimalizmi",
    "Scandinavian": "Scandinavian / Nordic — İskandinav Tasarım",
    "Isometric": "Isometric Illustration — İzometrik İllüstrasyon",
    "Duotone": "Duotone / Color Blocking — Çift Ton / Renk Blokları",
    "Retro-Futurism": "Retro Futurism — Retro Fütürizm",
    "Editorial Magazine": "Premium Editorial — Premium Dergi Tasarımı",
}

# ---- 14 yeni stil (yönerge §3, 41–60'tan çakışmayanlar) ----
NEW = [
 {"after":"Corporate Modern","value":"SaaS Product-Led","label":"SaaS / Product-Led — Ürün Odaklı SaaS",
  "explanation":"Ürünün kendisini (ekran görüntüsü, canlı demo, özellik kartları) satış aracı yapar: net değer önerisi, ürün arayüzü ön planda, fiyatlandırma ve deneme çağrısı her bölümde erişilebilir. Artısı: ziyaretçi ürünü görerek karar verir, dönüşüm yolu kısadır. Eksisi: ürün ekranları güncel tutulmazsa güven kaybı olur; özellik listesi kalabalıklaşmaya eğilimlidir.",
  "scenario":"Abonelikli yazılım, web uygulaması veya geliştirici aracı satan; ücretsiz deneme ya da demo talebiyle büyüyen şirketler için.",
  "example":"Bir proje yönetim aracının ana sayfasında başlığın altında ürünün gerçek panosunun ekran görüntüsü durur; aşağıda özellikler kısa kartlarda, her kartta küçük bir arayüz parçası ve sağ üstte sabit ‘Ücretsiz dene’ düğmesi vardır.",
  "examples":["Proje yönetim aracı","Geliştirici platformu","B2B web uygulaması"],
  "mock":["flowly","Ürün","İşini tek ekrandan yönet","Ücretsiz dene"]},
 {"after":"SaaS Product-Led","value":"Fintech Trust","label":"Fintech / Trust-Driven — Güven Odaklı Finans",
  "explanation":"Para ve kişisel veriyle ilgili kararlarda güveni öne koyar: sakin lacivert-yeşil paletler, net rakamlar, güvenlik ve lisans rozetleri, şeffaf ücret tabloları ve sade, öngörülebilir arayüz. Artısı: kullanıcının risk algısını düşürür, düzenleyici gerekliliklerle uyumludur. Eksisi: sektörde sık kullanıldığı için ayırt edicilik azdır; güven öğeleri gerçek belgeye dayanmalıdır.",
  "scenario":"Ödeme hizmeti, dijital banka, yatırım uygulaması, sigorta veya muhasebe yazılımı gibi kullanıcıdan finansal güven bekleyen işler için.",
  "example":"Bir ödeme kuruluşunun ana sayfasında lacivert zeminde ‘Ödemelerin güvende’ başlığı, yanında kart ve işlem özetini gösteren sade bir uygulama ekranı, altında lisans numarası, şifreleme ve 7/24 destek rozetleri yer alır.",
  "examples":["Dijital banka","Ödeme kuruluşu","Yatırım uygulaması"],
  "mock":["paynet","Finans","Paran güvende","Hesap aç"]},
 {"after":"Fintech Trust","value":"Web3 Digital Native","label":"Web3 / Digital Native — Dijital Yerli",
  "explanation":"Blokzincir, topluluk ve dijital varlık ürünlerinin dilini kullanır: koyu zemin, neon vurgular, holografik geçişler, cüzdan bağlama ve topluluk metrikleri. Artısı: hedef kitle tarafından hemen tanınır, teknolojik ve topluluk odaklı görünür. Eksisi: spekülatif ve güvensiz algılanabilir; finansal iddialar, riskler ve hukuki bilgilendirme açıkça yazılmalıdır.",
  "scenario":"Blokzincir altyapısı, dijital koleksiyon, merkeziyetsiz uygulama ya da kripto eğitim topluluğu gibi dijital yerli bir kitleye hitap eden projeler için.",
  "example":"Bir dijital koleksiyon platformunun sitesinde koyu mor zeminde parlayan holografik kartlar döner; sağ üstte ‘Cüzdanı bağla’ düğmesi, altında topluluk üye sayısı ve son işlemler akışı yer alır.",
  "examples":["Dijital koleksiyon","Blokzincir altyapısı","Topluluk platformu"],
  "mock":["chainly","Web3","Topluluk sahibi olsun","Cüzdanı bağla"]},
 {"after":"Web3 Digital Native","value":"AI-Native","label":"AI-Native / Generative — Yapay Zekâ Yerlisi",
  "explanation":"Yapay zekâ ürünlerinin dilini kullanır: sohbet ya da komut kutusu ilk ekranda, üretken degrade ve parçacık efektleri, örnek istemler ve canlı çıktı önizlemesi. Artısı: ürünün nasıl çalıştığını ilk saniyede gösterir. Eksisi: tür hızla kalıplaştı, birbirine benzeyen sitelerden ayrışmak zordur; yetenekler abartılmamalı, örnek çıktılar gerçek olmalıdır.",
  "scenario":"Yapay zekâ asistanı, içerik üretim aracı, model ya da API sağlayıcısı, yapay zekâ destekli SaaS ürünü için.",
  "example":"Bir yazı asistanının ana sayfasında ortada büyük bir komut kutusu ve ‘Bir blog yazısı taslağı çıkar’ gibi örnek istem çipleri vardır; arkada yavaşça dönen mor-mavi bir degrade küre ışık saçar.",
  "examples":["Yapay zekâ asistanı","Model / API sağlayıcı","Üretken içerik aracı"],
  "mock":["nova.ai","Yapay zekâ","Sor, üret, gönder","Dene"]},
 {"after":"AI-Native","value":"Eco Sustainable","label":"Eco / Sustainable — Ekolojik / Sürdürülebilir",
  "explanation":"Sürdürülebilirliği hem görselde hem teknikte uygular: doğal toprak ve yaprak tonları, geri dönüştürülmüş kâğıt dokusu, ölçülü görsel kullanımı ve düşük karbonlu (hafif, az veri harcayan) sayfa yapısı. Artısı: değer önerisiyle tutarlı, hızlı ve güven verici bir site çıkar. Eksisi: yeşil iddialar belgeyle desteklenmezse aklama (greenwashing) olarak algılanır.",
  "scenario":"Organik gıda, sürdürülebilir moda, yenilenebilir enerji, sivil toplum veya karbon raporlaması yapan kurumlar için.",
  "example":"Bir organik çiftliğin sitesinde krem kâğıt dokulu zeminde yaprak yeşili başlıklar, az sayıda ama iyi sıkıştırılmış fotoğraf ve alt bilgide sayfa başına karbon salımı göstergesi bulunur.",
  "examples":["Organik gıda","Yenilenebilir enerji","Sürdürülebilir moda"],
  "mock":["yeşil","Sürdürülebilir","Doğaya saygıyla","Ürünler"]},
 {"after":"Typography-Led","value":"Art Direction-Led","label":"Art Direction-Led — Sanat Yönetimi Odaklı",
  "explanation":"Her sayfayı ya da kampanyayı özel bir sanat yönetimiyle kurgular: özel fotoğraf çekimi, cesur kırpımlar, sayfaya özgü tipografi ve kompozisyon. Şablon değil, editoryal bir dergi kapağı gibi düşünülür. Artısı: güçlü ve unutulmaz bir marka izlenimi bırakır. Eksisi: her yeni içerik için tasarım emeği ister; ölçeklenmesi ve tutarlılığı zordur.",
  "scenario":"Moda markası, kreatif ajans, kültür kurumu ya da lansman kampanyası gibi görsel anlatının ürünün kendisi kadar önemli olduğu projeler için.",
  "example":"Bir moda markasının sezon sayfasında model fotoğrafı ekranı çapraz keser, başlık fotoğrafın üzerine dev ve dikey yazılmıştır; her koleksiyon sayfasının kendine ait bir renk ve kompozisyonu vardır.",
  "examples":["Moda kampanyası","Kreatif ajans","Kültür kurumu"],
  "mock":["ATELIER 9","Sezon 26","Işığın biçimi","Koleksiyon"]},
 {"after":"Monochromatic","value":"Dark-First","label":"Dark-First Design — Önce Koyu Tasarım",
  "explanation":"Arayüzü baştan koyu zemin için tasarlar: derin gri yüzeyler, katmanlarla ayrılan paneller, kontrollü parlak vurgular; açık tema varsa sonradan türetilir. Artısı: yoğun ekran kullanımında göz yorgunluğunu azaltabilir, teknik ve premium görünür. Eksisi: uzun metinlerde okunabilirlik, kontrast ve görsel sunumu dikkat ister; saf siyah ve saf beyaz yan yana kullanılmamalıdır.",
  "scenario":"Geliştirici aracı, yaratıcı yazılım, oyun, medya oynatıcı veya uzun süre açık kalan bir izleme paneli için.",
  "example":"Bir video düzenleme uygulamasının sitesinde koyu grafit zeminde hafif açık tonlu paneller birbirinden ayrılır; tek vurgu rengi olan elektrik mavisi yalnız ‘İndir’ düğmesinde ve etkin sekmede görünür.",
  "examples":["Geliştirici aracı","Yaratıcı yazılım","İzleme paneli"],
  "mock":["umbra","Yazılım","Gece de net","İndir"]},
 {"after":"Memphis","value":"Neo-Memphis","label":"Neo-Memphis — Yeni Memphis",
  "explanation":"1980'lerin Memphis akımını güncel dijital ürünlere uyarlar: yumuşatılmış pastel paletler, soyut geometrik süsler, dalgalı çizgiler, ince kontur ve bol beyaz alan. Klasik Memphis'ten daha sakin ve kurumsala uygundur. Artısı: eğlenceli ama düzenli, yaratıcı ve modern görünür. Eksisi: süsler içeriği bastırırsa ciddiyet kaybolur; dekoratif öğeler ekran okuyuculardan gizlenmelidir.",
  "scenario":"Eğitim teknolojisi, yaratıcı topluluk, etkinlik platformu ya da genç kitleye hitap eden bir SaaS ürünü için.",
  "example":"Bir çevrim içi kurs platformunun ana sayfasında kırık beyaz zeminde pastel sarı yarım daire, ince siyah dalga çizgisi ve lila noktalı bir üçgen başlığın çevresinde dağınık durur; kartlar sade ve hizalıdır.",
  "examples":["Eğitim teknolojisi","Etkinlik platformu","Yaratıcı topluluk"],
  "mock":["blip","Eğitim","Öğrenmek renkli","Kursları gör"]},
 {"after":"Cyberpunk","value":"Industrial","label":"Industrial / Utilitarian — Endüstriyel / İşlevsel",
  "explanation":"İşlevi süsün önüne koyar: teknik çizim estetiği, ızgara çizgileri, uyarı sarısı ve siyahı, etiket ve seri numarası tipografisi, sık ama düzenli bilgi yerleşimi. Artısı: dürüst, sağlam ve teknik bir güven verir; karmaşık ürün bilgisini düzenli sunar. Eksisi: soğuk algılanabilir; yoğun bilgi küçük ekranda dikkatli sadeleştirilmelidir.",
  "scenario":"Makine üreticisi, endüstriyel ekipman, mühendislik firması, donanım girişimi ya da teknik ürün kataloğu için.",
  "example":"Bir sanayi robotu üreticisinin sitesinde açık gri ızgara zeminde ürünün teknik çizimi durur; ölçüler ince çizgilerle işaretlidir, başlık ‘MODEL RX-40’ gibi etiket yazısıyla yazılmış, ‘Teknik föy’ düğmesi sarı-siyah çerçevelidir.",
  "examples":["Makine üreticisi","Donanım girişimi","Teknik katalog"],
  "mock":["RX-40","Endüstri","Dayanıklı. Hassas.","Teknik föy"]},
 {"after":"Photography-Led","value":"Data Viz-Led","label":"Data Visualization-Led — Veri Görselleştirme Odaklı",
  "explanation":"Mesajı grafikler, haritalar ve canlı göstergelerle anlatır; sayılar ve eğilimler sayfanın ana görselidir. Artısı: soyut bir değeri somut ve ölçülebilir kılar, güvenilir ve analitik görünür. Eksisi: grafikler erişilebilir tablo ve metin alternatifi olmadan anlaşılmaz; veri kaynağı ve tarihi açıkça yazılmalıdır.",
  "scenario":"Analitik platformu, araştırma kurumu, kamu verisi portalı, finansal rapor ya da etki raporu yayımlayan kurum için.",
  "example":"Bir iklim araştırma kurumunun ana sayfasında ilk ekranda Türkiye haritası üzerinde sıcaklık değişimi renkleri, yanında ‘+1,4 °C’ büyük rakamı ve altında kaynak ile güncelleme tarihi bulunur.",
  "examples":["Analitik platformu","Araştırma raporu","Kamu veri portalı"],
  "mock":["metrik","Analitik","Veri konuşsun","Raporu aç"]},
 {"after":"Cinematic","value":"Immersive","label":"Immersive / Experiential — Sürükleyici / Deneyimsel",
  "explanation":"Siteyi gezilecek bir deneyime çevirir: tam ekran sahneler, kaydırmayla ilerleyen anlatı, ses, 3B ya da WebGL ortamları ve ziyaretçinin keşfettiği etkileşimler. Artısı: güçlü duygusal etki ve paylaşılabilirlik yaratır. Eksisi: performans, erişilebilirlik ve SEO maliyeti yüksektir; hareket azaltma tercihi ve sade bir alternatif yol şarttır.",
  "scenario":"Ürün lansmanı, müze ya da sergi, oyun tanıtımı, marka kampanyası veya ödül odaklı ajans portfolyosu için.",
  "example":"Bir otomobil lansmanında ziyaretçi kaydırdıkça kamera aracın etrafında döner, farlar yanar ve motor sesi duyulur; sağ üstte ‘Sesi kapat’ ve ‘Sade görünüm’ düğmeleri her zaman erişilebilirdir.",
  "examples":["Ürün lansmanı","Sanal sergi","Oyun tanıtımı"],
  "mock":["ORBIT","Deneyim","İçine gir","Keşfet"]},
 {"after":"Immersive","value":"Kinetic Type","label":"Kinetic Typography — Hareketli Tipografi",
  "explanation":"Yazının kendisini hareket ettirerek anlatır: kayan, büyüyen, harf harf beliren ya da kaydırmaya tepki veren başlıklar. Artısı: az görselle güçlü ve akılda kalıcı bir ilk izlenim yaratır. Eksisi: okunabilirliği ve dikkat süresini zorlayabilir; hareket kısa tutulmalı, hareket azaltma tercihinde durmalı ve metin her zaman seçilebilir olmalıdır.",
  "scenario":"Kreatif ajans, etkinlik ya da konferans, müzik lansmanı veya güçlü bir manifestosu olan marka için.",
  "example":"Bir tasarım konferansının sitesinde ‘DÜŞÜN · YAP · PAYLAŞ’ kelimeleri ekranı yatay şeritler halinde zıt yönlere kayarak geçer; kaydırma hızlandıkça şeritler de hızlanır, imleç üzerine gelince yavaşlar.",
  "examples":["Konferans sitesi","Kreatif ajans","Müzik lansmanı"],
  "mock":["MOTION","Konferans","DÜŞÜN · YAP","Bilet al"]},
 {"after":"Liquid Glass","value":"Liquid Fluid","label":"Liquid / Fluid Design — Akışkan Tasarım",
  "explanation":"Sıvı gibi akan biçimler, organik morph geçişleri, imlece tepki veren dalgalar ve yumuşak, kesintisiz bölüm geçişleri kullanır. Artısı: canlı, modern ve dokunsal bir his verir; markaya hareket kimliği kazandırır. Eksisi: animasyonlar işlemciyi yorabilir; hareket azaltma tercihinde durağan sürüm gösterilmelidir.",
  "scenario":"Kozmetik ve içecek markası, yaratıcı teknoloji ürünü, müzik platformu ya da canlı bir marka kimliği isteyen lansman için.",
  "example":"Bir içecek markasının sitesinde şişenin arkasında yavaşça şekil değiştiren turuncu-pembe sıvı bir damla durur; fare yaklaştıkça damla dalgalanır, bölümler birbirine dalga biçimli kenarlarla geçer.",
  "examples":["İçecek markası","Kozmetik","Yaratıcı teknoloji"],
  "mock":["flow","Lansman","Akışa bırak","Keşfet"]},
]

# Erişilebilirlik ilkesi: seçenek değildir, bütün seçimlerde geçerli kalite standardı (yönerge §3)
PRINCIPLE = {"value": "Accessible-First", "label": "Accessible-First / Inclusive — Önce Erişilebilirlik",
  "explanation": "Bir stil seçeneği değil, bütün tasarım kararlarında geçerli kalite standardıdır: WCAG 2.2 AA kontrastı, klavyeyle tam gezinme, görünür odak, hareket azaltma tercihine uyum, yalnız renge dayanmayan durumlar, yeterli dokunma alanı ve okunabilir tipografi. Hangi stil seçilirse seçilsin bu kurallar stilin önündedir.",
  "examples": ["Kamu hizmeti", "Sağlık", "Eğitim"],
  "mock": ["erişim", "Herkes için", "Herkes kullanabilsin", "Başla"]}

# ---- 62 kaydın sınıfları ve önizleme tonu (l = açık, d = koyu zeminli) ----
P, B, V, S, M, T, I = "primary-style", "brand-style", "visual-approach", "surface-effect", "media-approach", "theme-approach", "interaction-approach"
META = {
 "Minimalism": ([P], "l"), "Scandinavian": ([P], "l"), "Japandi": ([P], "l"), "Swiss Style": ([P], "l"),
 "Flat Design": ([P], "l"), "Flat 2.0": ([P], "l"), "Material Design": ([P], "l"), "Typography-Led": ([V], "l"),
 "Art Direction-Led": ([V, M], "l"), "Editorial Magazine": ([B, V], "l"), "Monochromatic": ([V, T], "d"),
 "Dark-First": ([T], "d"), "Corporate Modern": ([B], "l"), "SaaS Product-Led": ([B], "l"), "Fintech Trust": ([B], "d"),
 "Web3 Digital Native": ([B], "d"), "AI-Native": ([B], "d"), "Eco Sustainable": ([B], "l"), "Luxury": ([B], "d"),
 "Brutalism": ([P], "l"), "Neobrutalism": ([P], "l"), "Constructivism": ([P], "l"), "Bauhaus": ([P], "l"),
 "Geometric": ([P, V], "d"), "Maximalism": ([P], "l"), "Anti-Design": ([P], "l"), "Art Deco": ([P], "d"),
 "Vintage": ([P], "l"), "Y2K": ([P], "l"), "Synthwave": ([P], "d"), "Vaporwave": ([P], "l"),
 "Retro-Futurism": ([P], "l"), "Pixel Art": ([P, V], "d"), "Grunge": ([P], "d"), "Memphis": ([P], "l"),
 "Neo-Memphis": ([P], "l"), "Psychedelic": ([P], "l"), "Hand-Drawn": ([V], "l"), "Illustration-Led": ([V, M], "l"),
 "Collage": ([V, M], "l"), "Organic": ([P], "l"), "Paper-Cut": ([V], "l"), "Playful": ([P], "l"),
 "Skeuomorphism": ([S], "d"), "Neumorphism": ([S], "l"), "Glassmorphism": ([S], "d"), "Liquid Glass": ([S], "l"),
 "Liquid Fluid": ([I, S], "l"), "Claymorphism": ([S], "l"), "3D-Led": ([M], "d"), "Isometric": ([V, M], "l"),
 "Futuristic": ([P], "d"), "Cyberpunk": ([P, T], "d"), "Industrial": ([P], "l"), "Gradient": ([V, T], "d"),
 "Duotone": ([V, M], "d"), "Photography-Led": ([M], "d"), "Data Viz-Led": ([M], "l"), "Cinematic": ([M], "d"),
 "Immersive": ([I, M], "d"), "Kinetic Type": ([I], "l"),
 "Accessible-First": (["design-principle"], "l"),
}

# ---- yeni karar alanları (yönerge §3 seçim kuralları) ----
AG = "poz:15:yazilim_gelistirme_ve_muhendislik/on_yuz_gelistirme/kullanici_arayuzu_gelistirici"
NEW_FIELDS = [
 {"after": "secondary_design_styles", "id": "design_surface", "label": "Yüzey / Derinlik Efekti", "type": "select", "cls": [S], "none": "None Surface",
  "explanation": "Kart, panel ve düğmelerin yüzeyine uygulanacak derinlik efektini ayrı bir karar olarak seçin. Ana tasarım dili sitenin karakterini, yüzey efekti ise bileşenlerin dokusunu belirler; efekt yalnız uygun bileşenlerde kullanılır, metin kontrastını düşürmemelidir.",
  "rule": "Bileşen yüzeylerinde {label} efekti kullanılacaktır. Efekt kart, panel ve vurgu alanlarıyla sınırlı kalacak; metin kontrastı WCAG 2.2 AA'nın altına düşmeyecek, şeffaflığı azalt ve hareket azaltma tercihlerinde sade yedek yüzey gösterilecektir.",
  "scenario": "Ana stil sade (ör. Minimalizm, Kurumsal) ama ürün kartlarında ya da uygulama tanıtımında daha dokunsal, katmanlı bir his isteniyorsa.",
  "example": "Minimalist bir fintech sitesinde sayfanın geneli düz kalır; yalnız ‘Kart özetin’ paneli renkli arka plan üzerinde buzlu cam (Glassmorphism) yüzeyle öne çıkar.",
  "noneLabel": "Yüzey efekti yok — düz yüzeyler",
  "noneText": "Bileşenler ana stilin kendi yüzeyini kullanır; ek cam, kabartma ya da kil efekti uygulanmaz.",
  "noneScenario": "Performans, erişilebilirlik ya da sadelik önceliklidir; ana stil zaten yeterli derinlik veriyordur.",
  "noneExample": "Kurumsal bir sitede kartlar ince kenarlıklı ve gölgesiz düz yüzeylerdir."},
 {"after": "design_surface", "id": "design_media", "label": "Medya Sunum Yaklaşımı", "type": "select", "cls": [M], "none": "None Media",
  "explanation": "Sitenin görsel anlatımında hangi medya türünün öne çıkacağını seçin: fotoğraf, sinematik video, 3B, illüstrasyon ya da veri görselleştirme. Bu karar çekim, illüstrasyon ve veri hazırlığı bütçesini doğrudan etkiler.",
  "rule": "Sitenin medya sunum yaklaşımı {label} olacaktır. Görseller WebP / AVIF, uygun boyut ve tembel yükleme ile sunulacak; her görselin anlamlı alternatif metni, videoların altyazısı ve durdurma kontrolü, grafiklerin metin ya da tablo alternatifi olacaktır.",
  "scenario": "Ürün, mekân ya da veri, sitenin en güçlü ikna aracıysa ve içerik üretimi buna göre planlanacaksa.",
  "example": "Bir butik otelde medya yaklaşımı Fotoğraf Odaklı seçilir: her oda sayfası ekran genişliğinde gerçek çekimle açılır, metinler kısa tutulur.",
  "noneLabel": "Belirgin bir medya yaklaşımı yok",
  "noneText": "Görseller içeriği destekleyen ikincil öğelerdir; ana anlatım metin ve arayüzle kurulur.",
  "noneScenario": "Bilgi ve metin ağırlıklı kurumsal ya da hizmet siteleri için.",
  "noneExample": "Bir hukuk bürosunun sitesinde yalnız ekip portreleri ve küçük ikonlar kullanılır."},
 {"after": "design_media", "id": "design_theme_interaction", "label": "Tema ve Etkileşim Yaklaşımı", "type": "multiselect", "cls": [T, I],
  "explanation": "Sitenin tema karakterini (önce koyu, tek renk, degrade) ve etkileşim dilini (hareketli tipografi, sürükleyici deneyim, akışkan geçişler) ayrı bir karar olarak seçin. Renk modu (açık / koyu / sisteme göre) Tema, Hareket & Tasarım bölümündeki Renk / Yüzey Teması kararında kalır.",
  "rule": "Tema ve etkileşim yaklaşımı olarak şunlar uygulanacaktır: {labels}. Hareketler prefers-reduced-motion tercihinde durdurulacak ya da sadeleştirilecek, etkileşimler klavyeyle de kullanılabilecek ve içeriğe erişimi engellemeyecektir.",
  "scenario": "Marka güçlü bir atmosfer ya da hareket kimliği istiyorsa; teknik kitleye koyu tema öncelikli bir ürün sunuluyorsa.",
  "example": "Bir yaratıcı yazılım sitesi Dark-First ve Hareketli Tipografi'yi birlikte seçer: koyu zeminde başlıklar kaydırmayla harf harf belirir.",
  "noneValue": "None Theme Interaction", "noneLabel": "Ek tema / etkileşim yaklaşımı yok",
  "noneText": "Ana stilin ve Tema, Hareket & Tasarım bölümündeki kararların ötesinde ek bir yaklaşım uygulanmaz.",
  "noneScenario": "Sade, hızlı ve öngörülebilir bir arayüz öncelikliyse.",
  "noneExample": "Bir belediye hizmet portalı açık temada, yalnız standart odak ve geçiş efektleriyle çalışır."},
]

# ---- layout'lar: 8 yeni + 20'sinin ayrıntıları ----
# r: üç kompozisyon (row listesi). Satır: [ağırlık, "sütunlar", [hücreler]]; hücre türleri:
# nav hero head text img card cta chart stat side form tile foot list quote gal tall wide pin
LAY_NEW = [
 {"after": "Split Screen", "value": "Centered Hero", "label": "Centered Hero Layout — Ortalanmış Açılış",
  "explanation": "İlk ekranda ortalanmış tek bir güçlü başlık, kısa açıklama ve bir ana çağrı; altında bölümler sakin bir ritimle sıralanır. Artısı: mesaj ve eylem net, tasarımı ve uygulaması kolaydır. Eksisi: çok yaygın olduğu için ayırt edici değildir; uzun içerikte tekdüzeleşebilir.",
  "scenario": "Tek ve net bir değer önerisi olan ürün, uygulama, etkinlik ya da açılış sayfası için.",
  "example": "Bir not uygulamasının sitesi beyaz zeminde ortalanmış ‘Düşüncelerini tek yerde topla’ başlığı ve tek bir ‘Ücretsiz başla’ düğmesiyle açılır; hemen altında ürün ekranı durur."},
 {"after": "Centered Hero", "value": "Z-Pattern", "label": "Z-Pattern Layout — Z Okuma Düzeni",
  "explanation": "Göz sol üstten sağ üste, çaprazla sol alta ve sağ alta gider; logo, menü, açılış mesajı ve çağrı bu dört köşeye yerleştirilir. Bağımsız bir düzen olarak da, diğer düzenlerle birlikte kullanılan bir kompozisyon ilkesi olarak da seçilebilir. Artısı: az içerikli sayfalarda dikkati çağrıya taşır. Eksisi: metin yoğun sayfalarda işlemez.",
  "scenario": "Az metinli açılış sayfaları, kampanya sayfaları ve tek eylem hedefli tanıtımlar için.",
  "example": "Bir kampanya sayfasında logo sol üstte, ‘Hemen kaydol’ sağ üstte; çaprazda ürün görseli, sağ altta büyük ‘%20 indirimle başla’ düğmesi durur."},
 {"after": "Z-Pattern", "value": "F-Pattern", "label": "F-Pattern Layout — F Okuma Düzeni",
  "explanation": "Ziyaretçi metin yoğun sayfalarda önce üst satırları yatay, sonra sol kenarı dikey tarar; önemli başlıklar ve anahtar kelimeler satır başlarına yerleştirilir. Kompozisyon ilkesi olarak blog, liste ve dokümantasyon düzenleriyle birlikte kullanılır. Artısı: taranabilirliği artırır. Eksisi: yalnız metin ağırlıklı sayfalarda anlamlıdır.",
  "scenario": "Blog, haber, arama sonuçları, dokümantasyon ve ürün listeleri gibi taranan sayfalar için.",
  "example": "Bir bilgi bankası makalesinde her paragraf kalın bir anahtar ifadeyle başlar, ara başlıklar sola hizalıdır ve sağ kenarda sabit içindekiler listesi yer alır."},
 {"after": "Card Based", "value": "Sidebar Navigation", "label": "Sidebar / Sticky Navigation — Kenar Çubuğu Menüsü",
  "explanation": "Ana gezinme ya da sayfa içi menü sol veya sağ kenarda sabit durur; içerik yanında kaydırılır. Artısı: çok sayfalı ve derin yapılarda konumu ve geçişi kolaylaştırır. Eksisi: yatay alan harcar, mobilde çekmeceye dönüşmelidir; sabit menü klavye odağını kapatmamalıdır.",
  "scenario": "Dokümantasyon, bilgi bankası, yönetim paneli, uzun hizmet katalogları ve kurumsal intranet için.",
  "example": "Bir yazılım dokümantasyonunda solda sabit başlık ağacı, ortada makale, sağda o sayfanın içindekiler listesi durur; mobilde sol menü ☰ ile açılır."},
 {"after": "Masonry", "value": "Horizontal Scroll", "label": "Horizontal Scroll — Yatay Kaydırma",
  "explanation": "İçerik bölümleri ya da kartlar yatay bir şeritte ilerler; dikey kaydırma bir bölümü yatayda gezdirebilir. Artısı: galeri, zaman çizelgesi ve ürün koleksiyonlarında farklı ve akıcı bir anlatı kurar. Eksisi: keşfedilebilirlik ve klavye erişimi zordur; görünür oklar, ilerleme göstergesi ve dikey yedek gerekir.",
  "scenario": "Portfolyo, zaman çizelgesi, ürün koleksiyonu ya da hikâye anlatan kampanya bölümleri için.",
  "example": "Bir mimarlık ofisinin proje bölümünde kartlar yatay dizilir, sonuncusu kenardan taşarak devam ettiğini gösterir; altta ilerleme çubuğu ve ‹ › düğmeleri vardır."},
 {"after": "Full Bleed", "value": "Layered", "label": "Layered / Overlapping — Katmanlı / Üst Üste",
  "explanation": "Görseller, metin kutuları ve kartlar birbirinin üzerine taşarak derinlik ve hareket hissi yaratır. Artısı: düz ızgaraya göre daha editoryal ve dinamik görünür. Eksisi: üst üste binen alanlar küçük ekranda çakışabilir; metin hiçbir zaman görselin karmaşık bölümüne binmemelidir.",
  "scenario": "Moda, mimarlık, kreatif ajans ve hikâye anlatan marka sayfaları için.",
  "example": "Bir iç mimarlık sitesinde büyük salon fotoğrafının sağ alt köşesine beyaz bir metin kartı taşar, kartın altına da ikinci küçük bir detay fotoğrafı kayar."},
 {"after": "Scrollytelling", "value": "Sticky Sections", "label": "Sticky Section Layout — Sabitlenen Bölümler",
  "explanation": "Bir sütun (başlık, görsel ya da gösterge) sabit kalırken diğer sütundaki içerik kaydırılır; adımlar ilerledikçe sabit alan güncellenir. Artısı: süreç, özellik ve karşılaştırmaları bağlamı kaybetmeden anlatır. Eksisi: kısa ekranlarda sabit alan içeriği sıkıştırabilir; mobilde normal akışa dönmelidir.",
  "scenario": "Ürün özellik turu, hizmet süreci, adım adım rehber ve fiyat karşılaştırmaları için.",
  "example": "Bir SaaS özellik sayfasında solda ‘Nasıl çalışır?’ başlığı ve ürün ekranı sabit kalır; sağda dört adım kaydırıldıkça soldaki ekran ilgili adıma geçer."},
 {"after": "Dashboard", "value": "Configurator Workspace", "label": "Configurator / Workspace Layout — Yapılandırıcı / Çalışma Alanı",
  "explanation": "Ekran araç panelleri, ortada çalışma alanı ya da canlı önizleme ve kenarda özet / sepetten oluşur; kullanıcı seçim yaptıkça önizleme anında değişir. Artısı: karmaşık ürün seçimini ve özelleştirmeyi somutlaştırır. Eksisi: küçük ekranda panellerin sırası ve adımları yeniden tasarlanmalıdır; durum değişiklikleri ekran okuyucuya duyurulmalıdır.",
  "scenario": "Ürün yapılandırıcı (mobilya, araç, baskı), fiyat hesaplayıcı, tasarım aracı ve çok adımlı teklif oluşturma ekranları için.",
  "example": "Bir mutfak dolabı yapılandırıcısında solda malzeme ve renk seçenekleri, ortada canlı 3B dolap, sağda seçilenlerin listesi ve toplam fiyat yer alır."},
]
L = {  # value: [en, pages, responsive, a11y, perf, styles, recipes(3)]
 "Bento Grid": ["Bento Grid", ["home", "product", "landing"], "Masaüstünde farklı boyutlu hücreler; tablette 2, mobilde tek sütun, büyük hücreler başta.", "Hücre sırası DOM'da mantıklı olmalı; görsel sıra ile okuma sırası ayrışmamalı.", "Çok hücreli yapı orta düzey; hücrelerdeki görseller tembel yüklenmeli.", ["SaaS Product-Led", "AI-Native", "Material Design"],
   [[[1, "1fr", ["nav"]], [3, "2fr 1fr 1fr", ["hero", "stat", "img"]], [3, "1fr 1fr 2fr", ["img", "card", "chart"]]],
    [[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [4, "1fr 1fr 1fr", ["tall", "card", "img"]], [2, "1fr 2fr", ["stat", "wide"]]],
    [[1, "1fr", ["nav"]], [4, "1fr 1fr", ["hero", "img"]], [3, "1fr 1fr 1fr 1fr", ["card", "card", "stat", "card"]]]]],
 "Editorial": ["Editorial", ["blog", "post", "about"], "Çok sütunlu metin tablette 2, mobilde tek sütuna iner; büyük görseller tam genişliğe geçer.", "Uzun metinde satır uzunluğu 60–75 karakter; başlık hiyerarşisi atlanmamalı.", "Büyük görseller için duyarlı boyutlar (srcset) şart.", ["Editorial Magazine", "Swiss Style", "Luxury"],
   [[[1, "1fr", ["nav"]], [3, "1.4fr 1fr", ["img", "head"]], [3, "1fr 1fr 1fr", ["text", "text", "quote"]]],
    [[1, "1fr", ["nav"]], [2, "1fr", ["head"]], [4, "1fr 2fr 1fr", ["text", "img", "text"]]],
    [[1, "1fr", ["nav"]], [4, "1fr 1fr", ["head", "tall"]], [2, "1fr 1fr 1fr", ["list", "list", "list"]]]]],
 "Card Based": ["Card-Based", ["home", "product", "blog"], "Kart ızgarası 3–4 sütundan tablette 2, mobilde 1 sütuna iner.", "Kartın tamamı tıklanabilirse tek bağlantı olmalı; iç içe bağlantıdan kaçınılmalı.", "Kart görselleri sabit oranla ayrılmalı (kayma olmasın).", ["Material Design", "Neobrutalism", "Flat 2.0"],
   [[[1, "1fr", ["nav"]], [2, "1fr", ["head"]], [4, "1fr 1fr 1fr", ["card", "card", "card"]], [4, "1fr 1fr 1fr", ["card", "card", "card"]]],
    [[1, "1fr", ["nav"]], [3, "1fr", ["hero"]], [4, "1fr 1fr 1fr 1fr", ["card", "card", "card", "card"]]],
    [[1, "1fr", ["nav"]], [5, "1fr 3fr", ["side", "gal"]]]]],
 "Modular Grid": ["Modular Grid", ["home", "product", "about"], "12 sütunlu ızgara tablette 8, mobilde 4 sütuna; modüller sırayla alt alta.", "Modüller arası boşluk ve başlık sırası tutarlı olmalı.", "Hafif; modüller bağımsız yüklenebilir.", ["Swiss Style", "Corporate Modern", "Industrial"],
   [[[1, "1fr", ["nav"]], [3, "1fr 1fr", ["hero", "img"]], [3, "1fr 1fr 1fr", ["card", "card", "card"]]],
    [[1, "1fr", ["nav"]], [2, "1fr 1fr 1fr 1fr", ["stat", "stat", "stat", "stat"]], [4, "2fr 1fr", ["chart", "list"]]],
    [[1, "1fr", ["nav"]], [3, "1fr 2fr", ["head", "text"]], [3, "1fr 1fr 1fr", ["img", "img", "img"]]]]],
 "Asymmetric Grid": ["Asymmetric Grid", ["home", "about", "landing"], "Asimetri masaüstünde; mobilde öğeler tek sütunda, öncelik sırasıyla.", "Görsel sıra ile DOM sırası tutarlı kalmalı; odak sırası atlamamalı.", "Orta; büyük görsellere dikkat.", ["Neobrutalism", "Constructivism", "Art Direction-Led"],
   [[[1, "1fr", ["nav"]], [4, "2fr 1fr", ["hero", "tall"]], [2, "1fr 2fr", ["card", "wide"]]],
    [[1, "1fr", ["nav"]], [3, "1fr 3fr", ["text", "img"]], [3, "3fr 1fr", ["img", "quote"]]],
    [[1, "1fr", ["nav"]], [5, "1.5fr 1fr 2fr", ["tall", "head", "img"]]]]],
 "Split Screen": ["Split-Screen", ["home", "landing", "auth", "contact"], "İki yarı masaüstünde yan yana; mobilde üst üste, görsel kısalır.", "İki yarıdaki eylemler aynı ağırlıkta ise hangisinin birincil olduğu açık olmalı.", "Hafif.", ["Corporate Modern", "AI-Native", "Fintech Trust"],
   [[[1, "1fr", ["nav"]], [6, "1fr 1fr", ["hero", "img"]]],
    [[6, "1fr 1fr", ["img", "form"]]],
    [[1, "1fr", ["nav"]], [3, "1fr 1fr", ["card", "card"]], [3, "1fr 1fr", ["img", "text"]]]]],
 "Centered Hero": ["Centered Hero Layout", ["home", "landing", "product", "contact"], "Başlık ve çağrı tüm ekranlarda ortada; mobilde yazı boyutu küçülür, görsel altta.", "Ortalanmış uzun paragraflar okunmaz; açıklama kısa tutulmalı.", "Çok hafif; açılış görseli LCP öğesi olur, öncelikli yüklenmeli.", ["Minimalism", "SaaS Product-Led", "AI-Native"],
   [[[1, "1fr", ["nav"]], [3, "1fr", ["hero"]], [3, "1fr", ["img"]]],
    [[1, "1fr", ["nav"]], [4, "1fr", ["hero"]], [2, "1fr 1fr 1fr", ["stat", "stat", "stat"]]],
    [[1, "1fr", ["nav"]], [3, "1fr", ["hero"]], [3, "1fr 1fr 1fr", ["card", "card", "card"]]]]],
 "Z-Pattern": ["Z-Pattern Layout", ["landing", "home"], "Masaüstünde dört köşe; mobilde sıra logo → mesaj → görsel → çağrı.", "Görsel desen için içerik sırası bozulmamalı.", "Hafif.", ["Minimalism", "Corporate Modern", "Flat Design"],
   [[[1, "1fr", ["nav"]], [3, "1fr 1fr", ["head", "img"]], [3, "1fr 1fr", ["img", "cta"]], [0, "", ["zpath"]]],
    [[1, "1fr", ["nav"]], [4, "1fr 1fr", ["hero", "img"]], [2, "1fr 1fr", ["text", "cta"]], [0, "", ["zpath"]]],
    [[1, "1fr", ["nav"]], [3, "1fr 1fr", ["img", "head"]], [3, "1fr 1fr", ["cta", "img"]], [0, "", ["zpath"]]]]],
 "F-Pattern": ["F-Pattern Layout", ["blog", "post", "listing"], "Satır başları her ekranda sola hizalı kalır; yan sütun mobilde alta iner.", "Anahtar bilgiler satır başında olmalı; yalnız görsel desenle anlam verilmemeli.", "Hafif.", ["Swiss Style", "Editorial Magazine", "Corporate Modern"],
   [[[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [5, "3fr 1fr", ["list", "side"]], [0, "", ["fpath"]]],
    [[1, "1fr", ["nav"]], [6, "3fr 1fr", ["text", "list"]], [0, "", ["fpath"]]],
    [[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [5, "1fr 3fr", ["side", "list"]], [0, "", ["fpath"]]]]],
 "Sidebar Navigation": ["Sidebar / Sticky Navigation", ["docs", "dashboard", "service"], "Kenar çubuğu tablette daralır, mobilde çekmeceye (☰) dönüşür.", "Sabit menü odak sırasında önce gelmeli; ‘içeriğe atla’ bağlantısı şart.", "Hafif; menü ağacı uzunsa tembel çizilmeli.", ["Material Design", "Industrial", "Dark-First"],
   [[[6, "1fr 4fr", ["side", "text"]]],
    [[6, "1fr 3fr 1fr", ["side", "text", "list"]]],
    [[1, "1fr", ["nav"]], [5, "1fr 4fr", ["side", "gal"]]]]],
 "Card Based ": None,
 "Masonry": ["Masonry", ["blog", "gallery", "listing"], "Sütun sayısı 4 → 2 → 1; öğeler kendi yüksekliğinde akar.", "Okuma sırası sütun sırası mı satır sırası mı açık olmalı; klavye sırası tutarlı kalmalı.", "Çok görselli; tembel yükleme ve ayrılmış oranlar şart.", ["Photography-Led", "Collage", "Illustration-Led"],
   [[[1, "1fr", ["nav"]], [6, "1fr", ["mason"]]], [[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [5, "1fr", ["mason"]]], [[1, "1fr", ["nav"]], [6, "1fr 3fr", ["side", "mason"]]]]],
 "Horizontal Scroll": ["Horizontal Scroll", ["portfolio", "landing", "product"], "Masaüstünde yatay şerit; mobilde dokunmayla kaydırılan şerit ya da dikey liste.", "Görünür ‹ › düğmeleri, ilerleme göstergesi ve klavyeyle kaydırma şart.", "Şeritteki görseller görünür olunca yüklenmeli.", ["Art Direction-Led", "Photography-Led", "Immersive"],
   [[[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [5, "", ["hscroll"]]], [[1, "1fr", ["nav"]], [6, "", ["hscroll"]]], [[1, "1fr", ["nav"]], [3, "1fr", ["hero"]], [3, "", ["hscroll"]]]]],
 "Full Bleed": ["Full-Bleed", ["home", "landing", "about"], "Görseller tüm ekranlarda kenardan kenara; metin güvenli alanda kalır.", "Görsel üzerindeki metin için yeterli kontrast katmanı gerekir.", "Büyük görseller: AVIF / WebP, duyarlı boyut, LCP önceliği.", ["Photography-Led", "Cinematic", "Luxury"],
   [[[6, "1fr", ["bleed"]], [2, "1fr 1fr 1fr", ["card", "card", "card"]]], [[1, "1fr", ["nav"]], [4, "1fr", ["bleed"]], [2, "1fr", ["text"]]], [[3, "1fr", ["bleed"]], [3, "1fr", ["bleed"]]]]],
 "Layered": ["Layered / Overlapping", ["home", "about", "service"], "Taşmalar masaüstünde; mobilde katmanlar alt alta, taşma kaldırılır.", "Metin görselin karmaşık bölümüne binmemeli; kontrast her katmanda denetlenmeli.", "Orta.", ["Art Direction-Led", "Luxury", "Collage"],
   [[[1, "1fr", ["nav"]], [6, "1fr", ["layer"]]], [[1, "1fr", ["nav"]], [4, "1fr", ["layer"]], [2, "1fr 1fr", ["card", "card"]]], [[6, "1fr", ["layer"]]]]],
 "Long Scroll": ["Long-Scroll", ["landing", "product", "home"], "Bölümler tüm ekranlarda alt alta; mobilde bölüm içi sütunlar tek sütuna iner.", "Uzun sayfada sayfa içi menü ve ‘başa dön’ gerekir.", "Bölümler tembel yüklenmeli; toplam sayfa ağırlığı izlenmeli.", ["SaaS Product-Led", "Eco Sustainable", "Playful"],
   [[[1, "1fr", ["nav"]], [2, "1fr", ["hero"]], [2, "1fr 1fr", ["text", "img"]], [2, "1fr 1fr 1fr", ["card", "card", "card"]], [1, "1fr", ["cta"]]],
    [[1, "1fr", ["nav"]], [2, "1fr 1fr", ["img", "text"]], [2, "1fr 1fr", ["text", "img"]], [1, "1fr", ["cta"]], [1, "1fr", ["foot"]]],
    [[1, "1fr", ["nav"]], [2, "1fr", ["hero"]], [2, "1fr 1fr 1fr", ["stat", "stat", "stat"]], [2, "1fr", ["quote"]], [1, "1fr", ["cta"]]]]],
 "Scrollytelling": ["Scrollytelling", ["landing", "about", "report"], "Masaüstünde sabit görsel + kayan adımlar; mobilde adım ve görsel sırayla.", "Hareket azaltma tercihinde adımlar statik gösterilmeli; içerik hareketsiz de okunabilmeli.", "Animasyonlar ağır olabilir; yalnız transform / opacity kullanılmalı.", ["Cinematic", "Data Viz-Led", "Immersive"],
   [[[1, "1fr", ["nav"]], [6, "1fr 1fr", ["pin", "list"]]], [[6, "1fr 1fr", ["list", "pin"]]], [[1, "1fr", ["nav"]], [3, "1fr", ["bleed"]], [3, "1fr 1fr", ["pin", "text"]]]]],
 "Sticky Sections": ["Sticky Section Layout", ["product", "service", "landing"], "Masaüstünde bir sütun sabit; mobilde sabitleme kalkar, normal akış.", "Sabit alan kısa ekranda içeriği kapatmamalı; odaklanan öğe görünür kalmalı.", "Hafif (position: sticky).", ["SaaS Product-Led", "Corporate Modern", "Swiss Style"],
   [[[1, "1fr", ["nav"]], [6, "1fr 1fr", ["pin", "list"]]], [[1, "1fr", ["nav"]], [6, "2fr 1fr", ["list", "pin"]]], [[1, "1fr", ["nav"]], [2, "1fr", ["head"]], [4, "1fr 2fr", ["pin", "card"]]]]],
 "Dashboard": ["Dashboard", ["dashboard", "account"], "Kenar menü mobilde alta ya da çekmeceye; grafikler tek sütun, tablolar yatay kaydırılır.", "Grafiklerin tablo / metin karşılığı ve canlı bölge duyuruları gerekir.", "Veri istekleri ve grafik kütüphanesi ağırlığı izlenmeli.", ["Data Viz-Led", "Dark-First", "Material Design"],
   [[[6, "1fr 5fr", ["side", "dash"]]], [[1, "1fr", ["nav"]], [2, "1fr 1fr 1fr 1fr", ["stat", "stat", "stat", "stat"]], [4, "2fr 1fr", ["chart", "list"]]], [[6, "1fr 4fr", ["side", "chart"]]]]],
 "Configurator Workspace": ["Configurator / Workspace Layout", ["product", "custom"], "Masaüstünde üç panel; tablette özet alta; mobilde adım adım akış + sabit alt özet.", "Seçim değişiklikleri ekran okuyucuya duyurulmalı (aria-live); her kontrol klavyeyle kullanılmalı.", "Canlı önizleme (özellikle 3B) ağır olabilir; düşük güçte statik görsel yedek.", ["SaaS Product-Led", "Industrial", "3D-Led"],
   [[[1, "1fr", ["nav"]], [6, "1fr 3fr 1fr", ["form", "img", "list"]]], [[6, "1fr 2fr", ["form", "img"]]], [[1, "1fr", ["nav"]], [5, "3fr 1fr", ["img", "form"]], [1, "1fr", ["cta"]]]]],
 "Gallery": ["Gallery", ["portfolio", "product", "home"], "Galeri ızgarası 4 → 2 → 1; tam ekran görüntüleyici mobilde kaydırmalı.", "Her görselin alternatif metni; görüntüleyicide odak tuzağı ve Escape.", "Çok görselli: tembel yükleme, küçük önizlemeler, AVIF / WebP.", ["Photography-Led", "Minimalism", "Art Direction-Led"],
   [[[1, "1fr", ["nav"]], [6, "1fr", ["gal"]]], [[1, "1fr", ["nav"]], [4, "1fr", ["bleed"]], [2, "1fr 1fr 1fr 1fr", ["tile", "tile", "tile", "tile"]]], [[1, "1fr", ["nav"]], [1, "1fr", ["head"]], [5, "1fr", ["gal"]]]]],
}
L.pop("Card Based ")
REC_LABELS = [["Ana sayfa", "home"], ["İçerik / hizmet sayfası", "product"], ["Alternatif kurgu", "alt"]]
PAGE_NAMES = {"home": "Ana sayfa", "product": "Hizmet / Ürün", "about": "Hakkımızda", "blog": "Blog listeleme", "post": "Blog detay",
              "contact": "İletişim", "landing": "Landing Page", "dashboard": "Dashboard", "auth": "Üyelik / Giriş", "custom": "Özel sayfa",
              "listing": "Liste / arama", "docs": "Dokümantasyon", "service": "Hizmet", "portfolio": "Portfolyo", "gallery": "Galeri",
              "report": "Rapor", "account": "Hesabım"}


def main():
    p = sys.argv[1]
    src = json.load(open(p, encoding='utf-8'))
    src['classes'] = [{"id": a, "name": b} for a, b in CLASSES]
    src['rename'] = RENAME
    have = {a['value'] for a in src['add']}
    for n in NEW:
        if n['value'] in have:
            continue
        m = n.pop('mock')
        src['add'].append(n)
        src['mock'][n['value']] = {"brand": m[0], "kicker": m[1], "title": m[2], "button": m[3]}
    pm = PRINCIPLE['mock']
    src['principle'] = {k: v for k, v in PRINCIPLE.items() if k != 'mock'}
    src['principleMock'] = {"brand": pm[0], "kicker": pm[1], "title": pm[2], "button": pm[3]}
    src['styleMeta'] = {k: {"cls": c, "tone": t} for k, (c, t) in META.items()}
    src['newFields'] = NEW_FIELDS
    src['layouts'] = {"add": LAY_NEW, "pageNames": PAGE_NAMES, "recipeLabels": REC_LABELS,
                      "meta": {k: {"en": v[0], "pages": v[1], "responsive": v[2], "a11y": v[3], "perf": v[4], "styles": v[5], "recipes": v[6]} for k, v in L.items()}}
    json.dump(src, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('stil ek', len(src['add']), 'meta', len(src['styleMeta']), 'layout meta', len(L))


if __name__ == '__main__':
    main()
