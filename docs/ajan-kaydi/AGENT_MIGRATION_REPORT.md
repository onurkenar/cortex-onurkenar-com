# Ajan Kaydı Göç (Import) Raporu

Tarih: 2026-10-30 · Kaynak: `web-proje-gelistirme.html` içindeki `DATA.departments` (23 departmanın `org` hiyerarşisi; kaynak JSON'lar `docs/organizasyon/NN-ad.json`), `DATA.agentCatalog`, `DATA.skillCatalog`, `DATA.boards` / `committees` / `workingGroups` ve `DATA.membership`.

Bütün sayılar `rgSummary()` / `rgFiles()` çıktısından ve kimlik defterinden okunmuştur; tahmin yoktur. Sayılar, kullanıcı seçimi olmayan temiz bir proje durumundan üretilmiştir.

Son üretim: `web-proje-gelistirme.html` md5 `5782e28cbaebe01c20187eb44898febf`; `8d11368c37157bfea8a8d34dcdf96d57` sürümünden (yalnız `mk_comp_*` kararlarının varsayılan ajanları değişti) üretilen dosyalar birebir aynıdır. Bu sürümde katalog ajanları ve özel ajanlar kaldırılmış; sistemde yalnız pozisyon ajanları vardır (bkz. §7).

## 1. Yöntem

1. **Kimlik defteri** — `python3 -I docs/organizasyon/ajan_kimlik_ekle.py web-proje-gelistirme.html docs/ajan-kaydi/agent-id-ledger.json <md5>`.
   - Her pozisyona `departman|pozisyon` anahtarıyla kalıcı bir `AGT-NN-NNNN` kimliği verir ve `DATA.agentIds`'e yazar.
   - Pozisyon kümesi arayüzdeki `dpPos` ile aynıdır; yönetim kurulu komite düğümleri hariçtir.
2. **Tanımlar** — Ayrı bir veri kopyası yoktur. `rgBuild()` tanımları her açılışta organizasyondan türetir. Kullanıcı farkları `state.registry.defs` içinde tutulur.
3. **Dışa aktarım** — `rgFiles()` → `AGENT_REGISTRY.json`, `SKILL_REGISTRY.json`, `AGENT_ORGANIZATION_MAP.json`.

**Idempotency kanıtı.** Betik gerçek dosyada ikinci kez çalıştırıldı. Çıktısı "0 yeni, 0 yeniden etkin, 0 emekliye ayrıldı; DATA.agentIds değişmedi" oldu; dosyanın md5'i aynı kaldı (`5ceaf9a15c6356b1482b4765835c5705`).

**Mevcut veri.** Hiçbir kayıt silinmedi. Mevcut seçimler (`state.agents`, `state.skills`, organ seçimleri, üyelikler) değişmedi. `state.registry` yalnız ilk kayıt işleminde oluşur.

## 2. Sonuç tablosu

| Ölçüt | Değer |
|---|---|
| İncelenen departman | 23 |
| Kaynak verisi bulunan departman | 23 |
| Kaynak verisi olmayan departman (`missing_source`) | 0 |
| Benzersiz pozisyon | 2.342 |
| Agent Definition | 2.343 (1 orkestratör `AGT-00-0001` + 2.342 pozisyon) |
| Agent Instance | 0 — örnekler kullanıcı tarafından şirket başına oluşturulur |
| Eşleştirilemeyen pozisyon | 0 |
| Kimlik defteri | 2.342 etkin, 0 emekli, 0 takma ad |
| Seviye dağılımı | L0 1 · L1 49 · L2 688 · L3 1.605 |
| Tanım durumu | 2.343 taslak |
| Eski katalog içeriği taşınan pozisyon | 32 (33 eski ajan; tanımda `migrated_from`) |
| Birden çok uygulayanı olan tanım | 0 — AGT-15-0069 Site Güvenilirlik Mühendisi'nde iki eski ajanın (performans-uzmani + gozlemlenebilirlik) içeriği tek pozisyon ajanında birleşti |
| Yazma yetkisiyle başlayan tanım | 18 |
| Çalıştırma yetkisiyle başlayan tanım | 12 |
| Skill ataması olan tanım | 33 |
| KPI'sı olan tanım | 204 |
| Gizli görev maddesi (`DP_DUTIES=false`) | 111 |
| Skill kategorisi | 7 (+ 181 öneri kategori, `status: "öneri"`) |
| Skill Definition | 22 (katalogdaki skill'ler, örtük sürüm 1.0.0) |
| İşlem türü | 12 (8'i her zaman insan onaylı) |
| Kurul / komite / çalışma grubu | 53 organ, 490 koltuk (rol unvanlarından 302 + ek koltuk 188, `DATA.membership.extra`) |
| Aynı departmanda tekrar eden unvan grubu | 6 |

## 3. Pozisyon türleri

| Tür | Sayı | Seviye |
|---|---|---|
| Orkestratör | 1 | L0 |
| Departman lideri | 23 | L1 |
| Departman yönetimi (aides) | 20 | L1 |
| Yönetim kurulu (düğüm) | 1 | L1 |
| Kurul üyesi | 4 | L1 |
| Ara yönetici (ofis) | 1 | L1 |
| Birim lideri | 181 | L2 |
| Ekip yöneticisi | 507 | L2 |
| Birime bağlı rol | 31 | L3 |
| Ekip rolü | 1.573 | L3 |
| Matris rol | 1 | L3 |

## 4. Departman bazında

Sütunlar: tanım sayısı · seviye dağılımı (L1 / L2 / L3) · eski katalog içeriği taşınan pozisyon (Katalog) · KPI'sı olan tanım (KPI) · gizli görev maddesi (Gizli görev).

| Kod | Departman | Tanım | L1 | L2 | L3 | Katalog | KPI | Gizli görev |
|---|---|---|---|---|---|---|---|---|
| 01 | Üst Yönetim ve Kurumsal Yönetişim | 43 | 12 | 5 | 26 | 0 | 6 | 35 |
| 02 | Muhasebe ve Mali İşler | 85 | 1 | 33 | 51 | 0 | 9 | 0 |
| 03 | Finans ve Hazine | 76 | 2 | 23 | 51 | 0 | 9 | 4 |
| 04 | İnsan Kaynakları ve Organizasyon | 45 | 1 | 20 | 24 | 0 | 12 | 0 |
| 05 | Hukuk İşleri | 108 | 3 | 32 | 73 | 0 | 9 | 7 |
| 06 | Uyum, Kurumsal Risk ve İç Kontrol | 119 | 4 | 32 | 83 | 1 | 9 | 0 |
| 07 | İç Denetim | 131 | 4 | 32 | 95 | 0 | 9 | 0 |
| 08 | Satış ve Gelir Yönetimi | 132 | 4 | 32 | 96 | 6 | 9 | 0 |
| 09 | Pazarlama ve Büyüme | 159 | 1 | 47 | 111 | 7 | 10 | 0 |
| 10 | Kurumsal İletişim ve İtibar Yönetimi | 132 | 4 | 32 | 96 | 1 | 9 | 0 |
| 11 | Müşteri Deneyimi ve Satış Sonrası Hizmetler | 105 | 1 | 32 | 72 | 2 | 9 | 5 |
| 12 | Operasyon Yönetimi | 92 | 1 | 28 | 63 | 0 | 8 | 5 |
| 13 | Üretim, Tedarik Zinciri ve Lojistik | 105 | 1 | 32 | 72 | 0 | 9 | 5 |
| 14 | Kalite Yönetimi | 105 | 1 | 32 | 72 | 0 | 9 | 5 |
| 15 | Bilgi Teknolojileri | 88 | 1 | 26 | 61 | 11 | 7 | 5 |
| 16 | Siber Güvenlik ve Bilgi Güvenliği | 105 | 1 | 32 | 72 | 1 | 9 | 5 |
| 17 | Veri, Analitik ve Yapay Zekâ | 105 | 1 | 32 | 72 | 2 | 9 | 5 |
| 18 | Ürün Yönetimi ve Ar-Ge | 105 | 1 | 32 | 72 | 0 | 9 | 5 |
| 19 | Tasarım ve Yaratıcı Hizmetler | 101 | 1 | 31 | 69 | 1 | 9 | 5 |
| 20 | İdari İşler ve Destek Hizmetleri | 101 | 1 | 31 | 69 | 0 | 9 | 5 |
| 21 | İş Sağlığı, Güvenliği, Çevre ve Sürdürülebilirlik | 105 | 1 | 32 | 72 | 0 | 9 | 5 |
| 22 | Kurumsal Güvenlik | 96 | 1 | 29 | 66 | 0 | 8 | 5 |
| 23 | Sekreterya, Yönetici Destek ve Protokol | 99 | 1 | 31 | 67 | 0 | 9 | 5 |

## 5. Hiyerarşi notları

**İnsan şeması ile yürütme hiyerarşisi 5 tanımda farklıdır.** Bunlar bilinçli istisnalardır; ikisi de tanımda ayrı alanlarda tutulur (`org_parent_agent_id`, `parent_agent_id`):

| Tanım | Şemada bağlı olduğu | Yürütmede üstü | Neden |
|---|---|---|---|
| AGT-01-0001 CEO / Genel Müdür | AGT-01-0007 Yönetim Kurulu | AGT-00-0001 Orkestratör | Kurul ve CEO aynı seviyede (L1); işi orkestratör dağıtır, kurul karar organıdır |
| AGT-01-0008 Yönetim Kurulu Başkanı | AGT-01-0007 | AGT-00-0001 | Aynı neden |
| AGT-01-0009 Yönetim Kurulu Başkan Vekili | AGT-01-0007 | AGT-00-0001 | Aynı neden |
| AGT-01-0010 Yönetim Kurulu Üyesi | AGT-01-0007 | AGT-00-0001 | Aynı neden |
| AGT-01-0011 Bağımsız Yönetim Kurulu Üyesi | AGT-01-0007 | AGT-00-0001 | Aynı neden |

**Şemada üst pozisyonu olmayan 23 tanım:** 22 departman lideri (bağlı oldukları makam şema dışında, `reportsTo`) ve 01'deki Yönetim Kurulu düğümü (Genel Kurul'a bağlı). Bunların yürütmedeki üstü orkestratördür.

**Döngü:** `rgCycles()` 0 döngü buldu.

## 6. Dikkat gerektiren kayıtlar

**Aynı departmanda aynı unvanlı farklı koltuklar.** Her biri ayrı tanım ve ayrı kimliktir; birleştirilmedi:

| Departman | Unvan | Kimlikler |
|---|---|---|
| 06 | Risk Veri Analisti | AGT-06-0024, AGT-06-0113 |
| 07 | Denetim Komitesi Raporlama Uzmanı | AGT-07-0004, AGT-07-0128 |
| 08 | Satış Geliştirme Temsilcisi | AGT-08-0026, AGT-08-0041 |
| 09 | Kanal Pazarlama Uzmanı | AGT-09-0083, AGT-09-0157 |
| 09 | Rekabet Analisti | AGT-09-0089, AGT-09-0141 |
| 09 | Pazarlama Veri Analisti | AGT-09-0124, AGT-09-0145 |

Bunlar farklı birim ya da ekiplerdeki koltuklardır. Birleştirilmeleri gerekiyorsa karar kullanıcınındır.

**Diğer kayıtlar**
- **AGT-15-0069** iki eski katalog ajanının içeriğini taşıyor. Araçlar ve skill'ler birleşik; varsayılan yetki bu birleşik araçlardan türer (yazma ve çalıştırma).
- **Görev tanımları gizli.** `DP_DUTIES=false` olduğu için 111 görev maddesi tanımlara yazılmadı; tanımlarda yalnız sayıları (`responsibilities_hidden`) var. Görev tanımları onaylanıp `DP_DUTIES` açıldığında tanımlar kendiliğinden dolar.
- **Öneri işaretli kayıtlar.** Misyon metni, öneri skill kategorileri ve varsayılan yetkiler kaynakta açıkça yazmaz; organizasyondan türetilmiş öneridir. Misyon şablonla üretilir; tanımlar taslak durumundadır.

## 7. Yeniden üretme ve geri alma

**Yeniden üretme.** Departman, skill ya da ajan kataloğu değişince sırasıyla:
1. Kimlik betiğini çalıştırın.
2. JSON dosyalarını dışa aktarın: Ajan Kaydı › Rapor ve dışa aktarım, ya da AGENT_TEST_REPORT.md §5'teki headless yöntem.
3. Betik "Olası yeniden adlandırma" yazarsa, doğru olanları defterin `aliases` alanına ekleyip yeniden çalıştırın.

**Geri alma.** Değişiklik öncesi kopyalar `_yedek/` altında:
- `web-proje-gelistirme.2026-10-30-ajan-kaydi-oncesi.html` (md5 `8c6c53ec4bc83f8c705532c67b9acd9e`)
- `CLAUDE.2026-10-30-ajan-kaydi-oncesi.md`
- `YOL-HARITASI.2026-10-30-ajan-kaydi-oncesi.md`

**Katalog ajanlarının kaldırılması (2026-10-30).** Başka bir oturum, 33 katalog ajanını kaldırıp içeriklerini pozisyon ajanlarına taşıdı. Ajan Kaydı bu modele uyarlandı ve JSON dosyaları yeniden üretildi.
- Kimlikler pozisyona bağlı olduğu için değişmedi: kimlik betiği "0 yeni, 0 emekli" verdi.
- Yazma / çalıştırma yetkisiyle başlayan tanım sayıları korundu (18 / 12).
- Uygulayan süzgeci ve ajan etiketi artık `legacy` alanına bakıyor; dışa aktarıma `migrated_from` eklendi.
- Uyarlama öncesi kopya: `_yedek/web-proje-gelistirme.2026-10-30-ajan-kaydi-legacy-oncesi.html` (md5 `3397f28c43ae098b44b727c4b9cb723e`).

**Özel ajanların kaldırılması (2026-10-30).** "Ajanlar" oturumu özel ajanları ve "özel içerikli ajan" ayrımını kaldırdı; sistemde yalnız 2.342 pozisyon ajanı kaldı. Ajan Kaydı'nda:
- "Pozisyonu olmayan özel ajan" satırı özetten ve dışa aktarım görünümünden kaldırıldı (kavram artık yok, hep 0'dı).
- Uygulayan süzgecinin seçenekleri "Eski katalog içeriği taşınan" (32) ve "Standart pozisyon ajanı" (2.310) oldu.
- Kimlikler (0 yeni / 0 emekli), yetki sayıları (18 / 12) ve `migrated_from` (33) değişmedi. JSON dosyaları yeniden üretildi.
- Uyarlama öncesi kopya: `_yedek/web-proje-gelistirme.2026-10-30-ajan-kaydi-ozel-ajan-oncesi.html` (md5 `17e4e029f9d416b2ff8506667bf7aa22`).

**İki pozisyon ajanına skill bağlanması (2026-10-30, "Ajanlar" oturumu).** AGT-11-0045 Servis Masası Temsilcisi (kvkk-kontrol, marka-sesi) ve AGT-17-0045 KPI ve Raporlama Analisti (kvkk-kontrol, olay-takibi). JSON dosyaları yeniden üretildi. Yalnız bu iki tanım değişti; skill ataması olan tanım 31 → 33, yetki sayıları ve özet aynı.

## 8. Bu mimaride uygulanamayanlar

Uygulama tek bir HTML dosyasıdır; sunucu ve veritabanı yoktur. Kullanıcı 2026-10-30'da WP-OnKe'de uygulanmasını seçti. Bu nedenle şunlar **uygulanamaz** ve yapılmadı:
- Prisma şeması ve veritabanı migration'ları;
- REST API uç noktaları;
- sunucu tarafı yetki denetimi;
- veritabanı düzeyinde tenant izolasyonu.

Karşılıkları:
- veri modeli `state.registry`'dedir;
- servis fonksiyonları `rg*`'dir;
- denetimler tarayıcıda çalışır;
- şirket izolasyonu, her servis çağrısında zorunlu şirket bağlamıyla yapılır.
