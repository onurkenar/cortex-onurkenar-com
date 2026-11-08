# WEB PROJECT CONFIGURATOR — MASTER DEVELOPMENT PROMPT

## 1. PROJENİN AMACI

Teknik bilgisi sınırlı veya hiç olmayan bir kullanıcının yeni bir web projesini geliştirmeye başlamadan önce gerekli teknik, mimari, tasarımsal, operasyonel ve kalite kararlarını adım adım verebilmesini sağlayan kapsamlı bir **Web Project Configurator / Project Specification Builder** geliştiriyoruz.

Bu araç klasik bir checklist değildir.

Temel mantık:

**Kullanıcı seçimi → Açıklanmış teknik karar → Bağlayıcı proje kuralı → Claude geliştirme talimatı**

Kullanıcı configurator içindeki seçenekleri işaretlediğinde sistem bu seçimleri otomatik olarak bir **Project Specification / Project Rules** dokümanına dönüştürmelidir.

Oluşturulan kurallar daha sonra Claude veya başka bir AI coding agent'a verilerek projenin bu kurallara uygun geliştirilmesi sağlanacaktır.

Dolayısıyla configurator yalnızca "hangi teknolojiyi kullanalım?" sorusuna cevap vermemeli; aynı zamanda projenin:

- mimarisini,
- teknoloji stack'ini,
- kodlama yaklaşımını,
- frontend ve backend standartlarını,
- veritabanını,
- API yapısını,
- güvenliğini,
- deployment modelini,
- tasarım dilini,
- responsive yaklaşımını,
- hareket/animasyon sistemini,
- SEO altyapısını,
- GEO/AIO yaklaşımını,
- erişilebilirliğini,
- performans hedeflerini,
- analitik altyapısını,
- test yaklaşımını,
- operasyon modelini,
- yayın kriterlerini

tanımlayan bir **Source of Truth** oluşturmalıdır.

---

# 2. HEDEF KULLANICI

Configurator yalnızca yazılımcılar için tasarlanmamalıdır.

Ana hedeflerden biri:

> Yazılım, kodlama, hosting, database, API, framework, authentication, deployment vb. teknik konuları bilmeyen bir kullanıcının seçeneklerin açıklamalarını okuyarak doğru karar verebilmesi.

Bu nedenle hiçbir seçenek yalnızca teknik terim olarak gösterilmemelidir.

Örneğin sadece:

`PostgreSQL`

yazmak yeterli değildir.

Kullanıcı şunu anlayabilmelidir:

- PostgreSQL nedir?
- Ne işe yarar?
- Hangi projelerde tercih edilir?
- Avantajı nedir?
- Dezavantajı veya dikkat edilmesi gereken konu nedir?
- Alternatiflerinden temel farkı nedir?
- Bu seçeneği seçtiğinde proje açısından ne değişir?

Aynı prensip bütün configurator boyunca geçerlidir.

---

# 3. TEMEL UX PRENSİBİ

Her karar alanı mümkün olduğunca şu yapıda olmalıdır:

### Karar Başlığı

Kararın neyi belirlediğini sade Türkçeyle açıkla.

### Seçenek kartları

Her seçenek doğrudan kendi kartı içinde açıklanmalıdır.

İki aşamalı şu yapı KULLANILMAMALIDIR:

1. Önce seçenek seç.
2. Daha sonra başka bir bölümden seçeneğin açıklamasını oku.

Bu kullanım zor ve gereksizdir.

Her seçenek kartının içinde mümkün olduğunca şu bilgiler bulunmalıdır:

**Nedir?**

Teknik olmayan kullanıcının anlayabileceği açıklama.

**Ne zaman kullanılır?**

Hangi proje tipleri için uygundur?

**Avantajı / sonucu nedir?**

Bu seçimin projeye etkisi.

**Alternatiflerinden farkı nedir?**

Gerektiğinde kısa karşılaştırma.

---

# 4. SEÇİM → PROJE KURALI MODELİ

Configurator içindeki her anlamlı seçim bir proje kuralı oluşturmalıdır.

Örneğin:

Kullanıcı:

`PostgreSQL`

seçerse:

> Projenin ana ilişkisel veritabanı PostgreSQL olacaktır.

Kullanıcı:

`Cloudflare Pages / Workers`

seçerse:

> Projenin production deployment altyapısı Cloudflare Pages / Workers üzerinde çalışacaktır.

Kullanıcı:

`WCAG 2.2 AA`

seçerse:

> Public kullanıcı arayüzleri WCAG 2.2 AA erişilebilirlik kriterlerine uygun geliştirilecektir.

Kullanıcı:

`Mobile First`

seçerse:

> Responsive tasarım ve frontend geliştirme süreci küçük ekranlardan başlayarak Mobile-First yaklaşımıyla yürütülecektir.

Her seçim sonrasında ilgili kart grubunun altında:

### BU SEÇİMDEN OLUŞAN KURAL

alanı gösterilmelidir.

Bu alan kullanıcıya yaptığı seçimin AI coding agent açısından ne anlama geldiğini göstermelidir.

---

# 5. PROJE KURALLARI AYRI BİR ALANDA OLMALI

Ana configurator ekranı ile oluşturulan proje kuralları birbirine karıştırılmamalıdır.

İki ana çalışma alanı bulunmalıdır:

### Proje Yapılandırması

Kullanıcının karar verdiği configurator.

### Proje Kuralları

Yapılan seçimlerden otomatik oluşturulan bağlayıcı specification.

Project Rules bölümünde kurallar mantıksal gruplar altında gösterilmelidir.

Ayrıca tüm specification:

- JSON olarak indirilebilmeli,
- JSON olarak içeri aktarılabilmeli,
- localStorage ile korunabilmeli,
- Claude Master Prompt olarak kopyalanabilmelidir.

---

# 6. CLAUDE MASTER PROMPT

Configurator'ın en önemli çıktılarından biri:

**Claude Promptunu Kopyala**

özelliğidir.

Bu prompt yalnızca seçimlerin listesini vermemelidir.

AI coding agent'a açık biçimde şunu söylemelidir:

> Aşağıdaki Project Specification bu proje için Source of Truth'tur.

Seçilmeyen alternatif teknolojiler AI tarafından keyfi olarak eklenmemelidir.

Claude:

1. mevcut repository'yi incelemeli,
2. mevcut mimariyi anlamalı,
3. mevcut dependency'leri kontrol etmeli,
4. mevcut veri modelini incelemeli,
5. design tokenları incelemeli,
6. configurator kurallarını bunların üzerine uygulamalıdır.

---

# 7. DEĞİŞTİRİLEMEZ GLOBAL AI CODING KURALLARI

Aşağıdaki kurallar oluşturulan Claude promptunun temel parçasıdır.

### Kural 1

Onaylanmış özellikleri, UI bileşenlerini, route'ları veya kullanıcı akışlarını açık kullanıcı onayı olmadan kaldırma.

### Kural 2

Kodlamaya başlamadan önce mevcut:

- repository,
- mimari,
- veri modeli,
- dependency'ler,
- design tokenlar,
- component yapısı

incelenmelidir.

### Kural 3

Configurator'da seçilmiş teknoloji ve servisler projenin **Source of Truth**'udur.

### Kural 4

Seçilmemiş alternatif teknoloji veya servisleri kullanıcı onayı olmadan projeye ekleme.

### Kural 5

Secret, API key, token veya credential hiçbir zaman source code içine hard-code edilmemelidir.

Environment variable veya secret manager kullanılmalıdır.

### Kural 6

Yeni dependency ancak mevcut stack problemi çözemiyorsa eklenmelidir.

### Kural 7

Değişiklikler mümkün olduğunca:

- backward compatible,
- migration-safe,
- data-safe

olmalıdır.

### Kural 8

Yeni özelliklerde:

- acceptance criteria,
- test senaryoları,
- loading state,
- empty state,
- error state,
- success state

düşünülmelidir.

### Kural 9

Public UI:

- responsive,
- mobile friendly,
- semantic,
- keyboard accessible,
- WCAG uyumlu

olmalıdır.

### Kural 10

Specification içinde **MUST** olarak işaretlenen kurallar ihlal edilemez.

---

# 8. CONFIGURATOR ANA KAPSAMI

Configurator genişletilebilir bir mimariyle aşağıdaki alanları kapsamalıdır.

## PROJECT & INFRASTRUCTURE

- Project Definition
- Project Type
- Domain & DNS
- Hosting & Deployment
- Cloudflare
- GitHub / Source Control
- Environments
- CI/CD
- Runtime
- Storage
- Backup
- Disaster Recovery

## ENGINEERING

- Technology Stack
- Programming Languages
- Architecture & Coding Approach
- Code Standards & Naming
- Frontend Architecture
- Backend Architecture
- API Standards
- Database
- ORM / Query Layer
- Database Pooling
- Authentication
- Authorization / RBAC
- Security
- Background Jobs
- File & Storage Architecture
- Internationalization
- Observability & Monitoring
- Documentation Standards
- AI Coding Rules
- Definition of Done
- Architecture Decision Log

## PRODUCT / WEB

- CMS / Admin Panel
- Public Site
- Page Design Style
- Layout Approach
- Theme
- Responsive Strategy
- Motion
- Interaction
- Advanced Visual / 3D
- Conversion-Centered Design
- Accessible / Inclusive Design
- Sustainable Web Design

## DISCOVERABILITY

- SEO
- Semantic SEO
- Local SEO
- GEO
- AIO
- Schema.org
- Structured Data
- Internal Linking
- Crawl / Index
- Content Quality
- Media SEO

## DATA & ANALYTICS

- Analytics
- Tag Management
- Search Console
- Behavior Analytics
- Consent Mode
- Attribution

## QUALITY

- Performance
- Core Web Vitals
- Lighthouse
- Accessibility
- WCAG
- W3C
- Testing
- QA
- Security Testing
- Go-Live Checklist

## PRIVACY

- KVKK
- GDPR
- CCPA
- Cookie / Consent Management

## OPERATIONS

- Deployment
- Monitoring
- Backup
- Disaster Recovery
- Smoke Tests
- Analytics Validation
- Form Validation
- Email Validation

Mimari yeni modüllerin sonradan eklenmesine uygun olmalıdır.

---

# 9. PROJECT TYPE

Project Type yalnızca birkaç genel seçenekten oluşmamalıdır.

En az aşağıdaki proje türleri desteklenmelidir:

- Kurumsal Web Sitesi
- Kişisel Web Sitesi
- Portföy Sitesi
- Blog / İçerik Sitesi
- Haber / Medya Sitesi
- Landing Page
- SaaS Platformu
- Web Uygulaması
- Müşteri Portalı
- Üyelik / Topluluk Platformu
- Marketplace
- E-Ticaret
- B2B Platformu
- Rezervasyon / Randevu Platformu
- İlan / Listeleme Platformu
- Eğitim / LMS Platformu
- Dokümantasyon / Bilgi Bankası
- Intranet / Çalışan Portalı
- Directory / Rehber Sitesi
- Etkinlik Sitesi
- Diğer

Her biri ayrıntılı olarak açıklanmalıdır.

Örneğin:

### Marketplace

Alıcılarla birden fazla satıcı veya hizmet sağlayıcıyı aynı platformda buluşturan sistemdir.

Trendyol, Airbnb veya Armut benzeri modeller buna örnektir.

Tipik olarak:

- satıcı / tedarikçi hesabı,
- ürün veya hizmet listeleme,
- talep,
- teklif,
- ödeme,
- komisyon,
- sipariş,
- değerlendirme

gibi özellikler gerektirebilir.

Tek bir şirketin kendi ürünlerini sattığı klasik e-ticaret sitesinden farklıdır.

### Kişisel Web Sitesi

Bir kişinin:

- kendisini,
- uzmanlığını,
- çalışmalarını,
- hizmetlerini,
- projelerini,
- iletişim bilgilerini

tanıttığı web sitesidir.

Danışmanlar, yöneticiler, freelancerlar, akademisyenler ve kişisel markalar için uygundur.

---

# 10. PAGE DESIGN STYLE

Configurator'da kapsamlı bir **Page Design Style** bölümü bulunmalıdır.

Bu seçim yalnızca renk paletini değil:

- grid,
- spacing,
- typography,
- cards,
- surfaces,
- imagery,
- motion,
- hierarchy

dilini belirlemelidir.

En az aşağıdaki stiller desteklenmelidir:

1. Minimalism
2. Swiss Style
3. Flat Design
4. Flat 2.0 / Semi-Flat
5. Typography-Led
6. Monochromatic
7. Corporate Modern
8. Luxury / Quiet Luxury
9. Brutalism
10. Neobrutalism
11. Constructivism
12. Bauhaus-Inspired
13. Geometric
14. Maximalism
15. Anti-Design / Experimental
16. Art Deco
17. Vintage / Analog Retro
18. Y2K
19. Synthwave / Outrun
20. Vaporwave
21. Pixel Art / 8-Bit
22. Grunge / Punk
23. Memphis
24. Psychedelic
25. Hand-Drawn / Doodle
26. Illustration-Led
27. Collage / Mixed Media
28. Organic / Biomorphic
29. Paper-Cut / Scrapbook
30. Playful / Cartoon
31. Skeuomorphism
32. Neumorphism / Soft UI
33. Glassmorphism
34. Claymorphism
35. 3D-Led
36. Futuristic / Sci-Fi
37. Cyberpunk / Terminal
38. Gradient / Mesh Gradient
39. Photography-Led
40. Cinematic

Her stil için:

- Türkçe açıklama,
- görsel karakter,
- hangi siteler için uygun olduğu,
- diğer stillerden farkı,
- **3 tasarım örneği**

gösterilmelidir.

---

# 11. TASARIM ÖRNEKLERİ

Kullanıcının sağladığı:

**Web Tasarımı: Dönüşüm ve Marka Stratejileri**

sunumu tasarım örnekleri açısından referans kaynaktır.

Sunumda gerçek ekran örnekleri bulunan stillerde configurator içinde doğrudan bu örnekler kullanılmalıdır.

Örneğin sunumda Minimalism için kişisel portfolyo, kültür/tiyatro ve finansal hizmet gibi farklı uygulamalar; Brutalism, Constructivism, Swiss Style, Editorial, Hand-Drawn, Retro, Flat Design ve Bento Grid için de üçlü örnek setleri bulunmaktadır.

Her Page Design Style kartında:

### 3 TASARIM ÖRNEĞİ

alanı bulunmalıdır.

Mümkün olduğunda gerçek screenshot kullanılmalıdır.

Sunumda gerçek screenshot olmayan bir stil için sahte web sitesi screenshot'ı üretilmemelidir.

Bunun yerine:

**Şematik Önizleme**

kullanılabilir ve bunun şematik olduğu açıkça belirtilmelidir.

---

# 12. PAGE LAYOUT APPROACH

Görsel stil ile sayfa düzeni birbirinden ayrılmalıdır.

Aşağıdaki layout seçenekleri desteklenmelidir:

- Bento Grid
- Editorial / Magazine
- Card-Based
- Modular Grid
- Asymmetric / Broken Grid
- Split-Screen
- Full-Bleed
- Masonry
- Long-Scroll
- Scrollytelling
- Dashboard / Data-Dense
- Gallery / Portfolio

Bunlar "tasarım stili" değildir.

Örneğin:

Minimalism + Bento Grid

veya:

Luxury + Full-Bleed

veya:

Corporate Modern + Modular Grid

birlikte kullanılabilir.

Bu ayrım data modelinde korunmalıdır.

---

# 13. THEME, MOTION & DESIGN APPROACH

Bu alan Page Design Style'dan ayrı tutulmalıdır.

Çünkü:

Dark Mode bir tasarım stili değildir.

Responsive bir tasarım stili değildir.

Parallax bir tasarım stili değildir.

WebGL bir tasarım stili değildir.

Bunlar tasarım yaklaşımı veya teknik uygulama biçimleridir.

## Theme

- Light Mode
- Dark Mode
- Light + Dark
- System / Auto
- Custom

## Responsive Strategy

- Mobile-First
- Desktop-First
- Adaptive
- Responsive Hybrid

## Motion & Interaction

- Micro-interactions
- Motion / UI Animation
- Kinetic Typography
- Parallax
- Scroll-Triggered Animation
- Minimum / Hareket Yok

## Advanced Visual

- WebGL
- Interactive 3D
- Canvas
- Interactive SVG
- No Advanced Graphics

## Design Approaches

- Conversion-Centered Design
- Accessible / Inclusive Design
- Sustainable Web Design

---

# 14. THEME / MOTION ÖRNEKLERİ

Theme, Motion & Design Approach bölümündeki **HER seçenek için 3 örnek önizleme** bulunmalıdır.

Örneğin:

### Micro-interactions

1. Button hover / press
2. Form success
3. Favorite / save interaction

### Parallax

1. Destination storytelling
2. Real-estate presentation
3. Product launch

### Scroll-Triggered Animation

1. Feature reveal
2. Timeline
3. Statistic counter

### Interactive 3D

1. Automobile 360°
2. Furniture model
3. Architectural model

### Accessible Design

1. Keyboard navigation
2. High contrast
3. Enlarged text / accessible typography

Bu önizlemeler kullanıcının teknik kavramı görsel olarak anlamasını sağlamalıdır.

---

# 15. TASARIM ÖRNEKLERİNİN UX'İ

Örnekler yalnızca isim olarak verilmemelidir.

Her kart içinde mümkün olduğunca küçük bir **preview thumbnail** bulunmalıdır.

Yapı:

**Seçenek adı**

Açıklama.

`Preview 1 | Preview 2 | Preview 3`

Altlarında kısa açıklamalar.

Kullanıcı karta baktığında kavramı görsel olarak anlamalıdır.

---

# 16. CMS / ADMIN PANEL

Configurator yalnızca public siteyi düşünmemelidir.

CMS/Admin Panel gerekiyorsa kapsamlı modül mimarisi tanımlanabilmelidir.

Önerilen yapı:

- Dashboard
- İçerik Yönetimi
- Hizmetler ve Paketler
- CRM
- Pazarlama
- SEO / GEO / AIO
- Analytics & Davranış
- Danışmanlar
- İnsan Kaynakları
- Hukuk
- Referanslar
- İş Ortakları
- Etkinlikler
- Rakipler
- Medya Kütüphanesi
- Entegrasyonlar
- Sistem & Ayarlar

Alt sabit menüler:

- Yardım Merkezi
- Dokümantasyon
- Çıkış Yap

Ek özellikler:

- Command Center
- AI Admin Assistant
- approval workflows
- audit logs
- system health
- security logs
- media SEO audit

---

# 17. CMS İLİŞKİ MODELİ

CMS yalnızca bağımsız içerik tablolarından oluşmamalıdır.

Özellikle şu ilişkiler düşünülmelidir:

**Service × Package × Location × Price × Form × CTA**

CRM tarafında:

- Lead
- Source
- Campaign
- Attribution
- Customer
- Offer
- Pipeline
- Conversion

ilişkileri kurulabilmelidir.

---

# 18. SEO MODÜLÜ

SEO yalnızca title ve description değildir.

Configurator aşağıdaki yapıyı desteklemelidir:

- SEO Dashboard
- SEO Health
- Page Audit
- On-Page SEO
- Technical SEO
- Keywords
- Semantic SEO
- Topic Map
- Topic Clusters
- Entities
- Internal Links
- Local SEO
- GEO
- AIO
- Structured Data
- Media SEO
- Core Web Vitals
- Crawl & Index
- Backlink / Authority
- Content Health
- Competitor SEO
- Reports

CMS editor içinde ayrıca SEO side panel düşünülebilir.

---

# 19. PUBLISHING QUALITY GATE

Public içerik yayınlanmadan önce isteğe bağlı kalite kontrol zinciri kurulabilmelidir:

SEO
→ Semantic SEO
→ Local SEO
→ GEO/AIO
→ Schema
→ W3C
→ WCAG
→ Lighthouse
→ Media SEO
→ Internal Linking
→ FAQ
→ Social Proof

Hata seviyeleri:

### Critical

Yayın engellenebilir.

### Warning

Kullanıcı onayıyla yayın yapılabilir.

### Suggestion

Bilgilendirme amaçlıdır.

---

# 20. PUBLIC SITE KALİTE STANDARDI

Public sayfalarda aşağıdaki standartlar configurator üzerinden seçilebilir veya proje standardı olarak uygulanabilir:

- SEO
- Semantic SEO
- Local SEO
- GEO
- AIO
- schema.org
- JSON-LD
- W3C
- Lighthouse
- WCAG 2.2
- Core Web Vitals
- Responsive Design
- Semantic HTML
- Internal Linking
- Crawlability
- Indexability
- E-E-A-T / trust signals

---

# 21. IMAGE STANDARDI

Görsellerde mümkün olduğunda:

- WebP
- AVIF
- responsive images
- srcset
- sizes
- lazy loading
- width
- height
- descriptive ALT

kullanılmalıdır.

ALT erişilebilirlik ve anlam açısından zorunlu kabul edilmelidir.

`title` attribute her görselde zorunlu değildir.

---

# 22. VIDEO SEO

Video kullanılan sayfalarda gerektiğinde:

- video title,
- description,
- thumbnail,
- transcript,
- captions,
- VideoObject schema

kullanılabilmelidir.

---

# 23. LINK STANDARDI

Linklerde:

- descriptive anchor text,
- gerçek `<a href="">`,
- keyboard accessibility,
- visible focus state,
- hover state

bulunmalıdır.

Her link ve butona zorunlu `title` attribute eklenmemelidir.

Tooltip yalnızca gerçekten açıklama gerektiğinde kullanılmalıdır.

Hover prefetch zorunlu değildir; performans ve kullanıcı niyetine göre uygulanmalıdır.

---

# 24. CORE WEB VITALS

İyi kullanıcı deneyimi hedefi olarak:

- LCP ≤ 2.5 s
- INP ≤ 200 ms
- CLS ≤ 0.1

değerleri desteklenmelidir.

Configurator ayrıca:

- strict,
- standard,
- monitor only

gibi performans politikalarını destekleyebilir.

---

# 25. GEO / AIO

AI arama ve answer engine görünürlüğü ayrı bir karar alanı olmalıdır.

İçerikler gerektiğinde:

- direct answer blocks,
- explicit entities,
- entity relationships,
- source-backed claims,
- citation-friendly sections,
- structured content,
- schema markup

kullanmalıdır.

Ana cevap yalnızca client-side JavaScript içinde saklanmamalıdır.

`llms.txt` gibi gelişmekte olan uygulamalar:

- Use
- Evaluate
- No

şeklinde configurable olmalıdır.

---

# 26. ACCESSIBILITY

Accessibility tasarımın sonradan eklenen bir özelliği değildir.

Seçenekler:

- WCAG 2.2 AA
- WCAG 2.2 AAA
- WCAG 2.1 AA
- özel hedef
- kapsam dışı

olabilir.

Ayrıca:

- keyboard navigation,
- focus states,
- reduced motion,
- contrast,
- semantic HTML,
- screen reader compatibility

düşünülmelidir.

---

# 27. CONFIGURATOR ARAYÜZ TASARIMI

Arayüz:

- ferah,
- profesyonel,
- sade,
- geniş whitespace kullanan,
- okunabilir,
- teknik olmayan kullanıcının korkmadan kullanabileceği

bir yapıda olmalıdır.

Ana içerik kartlarla ilerlemelidir.

Kartlar gereksiz dekoratif olmamalıdır.

Seçili kart:

- belirgin border,
- check işareti,
- yeterli contrast

ile gösterilmelidir.

---

# 28. SOL MENÜ — ÇOK ÖNEMLİ

Sol menü için kullanıcının verdiği CMS ekran görüntüsü ana referanstır.

Menü mimarisini yanlış şekilde yapay üst kategorilere bölme.

Örneğin:

`PROJECT & INFRASTRUCTURE`

`ENGINEERING`

`PRODUCT & WEB`

gibi dev kategori başlıkları altında bütün configurator'ı toplamak referans davranış değildir.

Referans mantığı:

### Ana modül

Doğrudan sol menüde görünür.

### Alt modüller

Ana modül açıldığında altında görünür.

### Gerekirse üçüncü seviye

Alt modül altında daha fazla kırılım olabilir.

Örneğin referans:

CRM

→ CRM Dashboard

→ Talepler ve Leadler

→ → Gelen Kutusu

→ → Bana Atananlar

→ → Lead Havuzu

→ → Tüm Kayıtlar

Configurator için de aynı bilgi mimarisi kullanılmalıdır.

Örneğin:

Page Design Style

→ Ana Sayfa / Site Tasarım Stili

→ Sayfa Düzeni / Layout Yaklaşımı

→ Destekleyici Layout Yaklaşımları

→ Destekleyici Tasarım Yaklaşımları

Theme, Motion & Design Approach

→ Renk / Yüzey Teması

→ Responsive Tasarım Stratejisi

→ Hareket & Etkileşim Teknikleri

→ İleri Görsel / 3D Teknolojileri

→ Conversion-Centered Design

→ Accessible / Inclusive Design

→ Sustainable Web Design

---

# 29. SOL MENÜ GÖRSEL DAVRANIŞI

Referans CMS paneline mümkün olduğunca yakın olmalıdır.

Sol menü:

- fixed,
- beyaz,
- ince sağ border,
- üstte logo/proje adı,
- altında search,
- ana menü öğeleri,
- badge/counter,
- chevron,
- açılır alt menüler,
- hiyerarşi çizgileri,
- aktif alt menü vurgusu

içermelidir.

Aktif öğe:

- açık gri background,
- koyu border veya vurgu,
- yüksek contrast

ile gösterilmelidir.

En altta sabit:

- Proje Kuralları
- Dokümantasyon

bulunabilir.

---

# 30. ÜST HEADER

Üst header sol sidebar ile çakışmamalıdır.

Sidebar genişliği layout tarafından gerçek anlamda hesaba katılmalıdır.

Header:

- configurator adı,
- kısa açıklama,
- JSON İndir,
- JSON İçe Aktar,
- Claude Promptunu Kopyala

aksiyonlarını taşıyabilir.

Header fixed kullanılacaksa content ve sidebar offsetleri doğru hesaplanmalıdır.

Önceki sürümlerde yaşanan üst üste binme problemi tekrar edilmemelidir.

---

# 31. RESPONSIVE CONFIGURATOR

Configurator'ın kendisi de responsive olmalıdır.

Desktop:

- fixed sidebar,
- geniş content area,
- iki kolon option cards.

Tablet:

- daraltılmış sidebar veya drawer.

Mobile:

- sidebar drawer/hamburger,
- tek kolon kartlar,
- touch-friendly controls.

---

# 32. DATA MODEL

Configurator data-driven geliştirilmelidir.

Hard-coded HTML tekrarları oluşturulmamalıdır.

Temel veri modeli yaklaşık olarak:

Section

→ Fields

→ Options

→ Description

→ Rule

→ Examples

şeklinde olmalıdır.

Örneğin:

```text
Section
  id
  name
  description

Field
  id
  section
  label
  explanation
  type

Option
  value
  label
  explanation
  examples
  rule
```

Yeni bir seçenek eklemek mümkün olduğunca yalnızca configuration datasını değiştirmeyi gerektirmelidir.

---

# 33. FIELD TYPES

En az:

- text
- textarea
- select/card select
- multiselect
- boolean
- URL
- number

desteklenmelidir.

Gelecekte:

- dependency selection,
- conditional fields,
- recommended option,
- incompatible option,
- required option

özellikleri eklenebilmelidir.

---

# 34. DEPENDENCY / CONDITIONAL LOGIC

Bazı kararlar diğerlerine bağlıdır.

Örneğin:

Database Engine = PostgreSQL

ise provider seçenekleri PostgreSQL destekleyen servislerden oluşmalıdır.

ORM seçenekleri kullanılan dile ve database'e göre değişebilmelidir.

Deployment platformu runtime seçeneklerini etkileyebilir.

Ancak sistem kullanıcının mevcut seçimini sessizce değiştirmemelidir.

Tercihen:

> Bu seçim nedeniyle X önerilir.

şeklinde recommendation gösterilmelidir.

Otomatik değiştirme ancak kullanıcı açıkça kabul ederse yapılmalıdır.

---

# 35. "OTHER" KULLANIMI

Her yerde kolayca `Other` kullanmak yerine gerçek seçenek listeleri mümkün olduğunca kapsamlı tutulmalıdır.

Other seçildiğinde mümkünse:

**Özel değer gir**

alanı açılmalıdır.

Girilen değer Project Rules ve JSON'a dahil edilmelidir.

---

# 36. AÇIKLAMA KALİTESİ

Generic fallback açıklama kullanılmamalıdır.

Şu tür metin kabul edilemez:

> Bu seçenek ilgili teknik kararın alternatiflerinden biridir.

Bu kullanıcıya hiçbir şey anlatmaz.

Her seçeneğin gerçek ve özgün açıklaması bulunmalıdır.

Configurator'daki bütün seçenekler audit edilerek açıklaması olmayan seçenek kalmamalıdır.

---

# 37. TASARIM PREVIEW DATA MODELİ

Her tasarım seçeneği aşağıdaki yapıyı destekleyebilmelidir:

```text
examples:
  - image
  - title
  - description
  - source
  - previewType
```

`previewType`:

- real screenshot
- schematic
- generated example

gibi değerler alabilir.

Kullanıcı gerçek örnek ile şematik örneğin farkını görebilmelidir.

---

# 38. SUNUMDAN GELEN TASARIM PRENSİPLERİ

Yüklenen tasarım sunumundaki ana prensipler configurator'ın tasarım kararlarında dikkate alınmalıdır.

Sunum özellikle şu ayrımı vurgular:

> Tasarım trendi amaç değil araçtır.

Bir trend yalnızca estetik olarak hoş olduğu için seçilmemelidir.

Seçim:

**Marka kimliği × Kullanıcı ihtiyacı × İş hedefi**

kesişiminde yapılmalıdır.

Dolayısıyla configurator ileride seçilen:

- sektör,
- proje türü,
- hedef kitle,
- marka konumlandırması

üzerinden tasarım stilleri için **Recommended** etiketi üretebilecek şekilde tasarlanmalıdır.

---

# 39. DESIGN SYSTEM MANTIĞI

Tasarım kararları tek tek bağımsız CSS değerleri olarak ele alınmamalıdır.

Seçimler mümkün olduğunda design token sistemine dönüşmelidir:

- colors
- typography
- spacing
- radius
- shadows
- container widths
- grid
- breakpoints
- motion duration
- easing
- surface hierarchy

AI coding promptunda:

> UI geliştirirken seçilen design system ve tokenları kullan; aynı kavram için rastgele yeni değerler üretme.

kuralı bulunmalıdır.

---

# 40. CONFIGURATOR'IN SON HEDEFİ

Bu sistem tamamlandığında kullanıcı yeni bir proje için configurator'ı açacak.

Adım adım kararlarını verecek.

Örneğin:

```text
Project Type:
B2B Marketplace

Deployment:
Cloudflare Pages + Workers

Database:
PostgreSQL

Provider:
Neon

Pooling:
Cloudflare Hyperdrive

Frontend:
Next.js

Language:
TypeScript

CSS:
Tailwind

Design:
Corporate Modern

Layout:
Bento + Modular Grid

Theme:
Light + Dark

Responsive:
Mobile First

Motion:
Micro-interactions

Accessibility:
WCAG 2.2 AA

SEO:
Advanced

GEO/AIO:
Enabled
```

Configurator bunları bağlayıcı kurallara çevirecek.

Ardından kullanıcı:

**Claude Promptunu Kopyala**

diyecek.

Claude'a verilen prompt:

- ne geliştirileceğini,
- hangi teknolojilerin kullanılacağını,
- hangi teknolojilerin kullanılmayacağını,
- nasıl kodlanacağını,
- hangi tasarım dilinin kullanılacağını,
- hangi kalite kriterlerinin sağlanacağını,
- hangi testlerin yapılacağını,
- neyin değiştirilmemesi gerektiğini

açıkça belirleyecek.

---

# 41. GELİŞTİRME PRENSİBİ

Bu configurator üzerinde bundan sonra yapılacak her geliştirmede:

### Önce mevcut sistemi incele.

Mevcut çalışan özellikleri kaldırma.

### Sonra yeni özelliği ekle.

Mevcut data modeline mümkün olduğunca uy.

### UI'ı bozma.

Yeni özellik mevcut görsel sisteme entegre edilmeli.

### Eski kararları koru.

Yeni versiyon oluştururken önceki kullanıcının seçimleri mümkün olduğunca migration ile korunmalıdır.

### Versiyonla.

Örneğin:

V16 → V17

şeklinde ilerle.

### Regression kontrolü yap.

Özellikle:

- sidebar,
- navigation,
- option selection,
- rule generation,
- localStorage,
- JSON export,
- JSON import,
- Claude prompt,
- responsive behavior

her değişiklikten sonra kontrol edilmelidir.

---

# 42. KRİTİK TASARIM KURALI

Bu proje için en önemli çalışma prensiplerinden biri:

> Kullanıcı bir UI yapısını veya özelliği onayladıktan sonra, yeni geliştirme yaparken bu özelliği izinsiz kaldırma veya başka bir yapıya dönüştürme.

Yeni özellik:

**mevcut sistem + geliştirme**

şeklinde uygulanmalıdır.

**mevcut sistemi yeniden yorumlama + kaldırma**

şeklinde değil.

---

# 43. SONUÇ

Geliştirdiğimiz sistem sıradan bir web proje checklist'i değildir.

Hedef:

> Bir web projesinin fikir aşamasından production'a kadar teknik, mimari, tasarımsal, SEO, güvenlik, erişilebilirlik, performans ve operasyon kararlarını kullanıcıyla birlikte tanımlayan ve bunları doğrudan AI coding agent tarafından uygulanabilir bağlayıcı proje specification'ına dönüştüren kapsamlı bir Web Project Configurator geliştirmektir.

Bu nedenle bütün geliştirmelerde şu zincir korunmalıdır:

**İnsan tarafından anlaşılabilir açıklama**

↓

**Bilinçli kullanıcı seçimi**

↓

**Makine tarafından yorumlanabilir configuration**

↓

**Bağlayıcı Project Rules**

↓

**Claude Master Development Prompt**

↓

**Specification'a uygun kod**

Configurator'ın temel ürünü aslında HTML arayüzü değil, oluşturduğu **güvenilir ve uygulanabilir Project Specification**'dır.

---

# 44. PAZARLAMA MODÜLÜ (V24)

Configurator yalnız web projesinin teknik kararlarını değil, sitenin yayına çıktıktan sonraki **pazarlama ve içerik planını** da aynı modelle tanımlar:

**Kullanıcı seçimi → Açıklanmış karar → Bağlayıcı pazarlama kuralı → Claude talimatı / içerik planı verisi**

- Pazarlama kararları sol menüde **Ajanlar**'ın altındaki **Pazarlama** başlığında, proje kararlarından ayrı bir alan olarak durur; görünüm, açıklama kalitesi (§36), koşullu mantık (§34) ve kural modeli (§4) proje kararlarıyla aynıdır.
- Kapsam: pazarlama planı ve hedefler, rakip analizi, ürün / hizmet tanıtımı, içerik stratejisi, blog standardı, sosyal medya, brief ve görsel üretimi, özel günler, mailing, etkinlikler, reklam (ortak kurallar, Google Ads, Meta Ads), ölçüm ve raporlama, iş akışı ve onay, hukuk değerlendirmesi, iş gücü ve roller, plan dosyası.
- Seçenekler tarafsız alternatiflerdir; belirli bir müşterinin planından gelen kurallar varsayılan yapılmaz.
- Sitede teknik karşılığı olan pazarlama kararları (ölçüm olayları, UTM, blog alanları, yapısal veri, KVKK onayları) proje kararlarıyla çelişmez; aynı karar iki yerde sorulmaz, mevcut karara bağlantı verilir.
- Pazarlama kuralları Claude promptunda ayrı bir bölüm olarak yer alır; ayrıca içerik üretimi için yalnız marka ve pazarlama bağlamını içeren ayrı bir prompt üretilir.
- Seçimler İçerik ve Reklam Planı Şablonu'nun veri biçimine aktarılabilir; üretilen veri şablonun kendi doğrulamasından hatasız geçmelidir.
