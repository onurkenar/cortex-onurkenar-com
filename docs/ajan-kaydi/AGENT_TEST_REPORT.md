# Ajan Kaydı Test Raporu

Tarih: 2026-10-30 · Test edilen dosya: `web-proje-gelistirme.html`, md5 `5a478ca797386b09189368bcc5130a8c` (katalog ajanlarının kaldırılmasından sonraki uyarlama; yazılan sürümle birebir aynı kopya). İlk sürüm `5ceaf9a15c6356b1482b4765835c5705` üzerinde de çalıştırıldı (171 PASS / 0 FAIL).

**Ortam**
- Headless Google Chrome (`--headless=new --dump-dom`).
- Test betiği, dosyanın test kopyasına eklenir (`</script></body></html>` öncesine). Kopya ayrı bir localStorage anahtarı kullanır. Kopya proje klasörünün dışında tutulur.
- Kilit `projectReady=()=>true` ile açılır.

Burada yalnız gerçekten çalıştırılan testler raporlanmıştır. Çalıştırılmayanlar §6'da ayrıca listelenmiştir.

## 0. Son uyarlama — özel ajanların kaldırılması

Dosya: md5 `0f3e1b8c6de0ade926a47052e240e697`. Uyarlama yalnız 3 metin değişikliği içerir (bkz. AGENT_MIGRATION_REPORT.md §7).

`rg_test.js` geçici klasörle birlikte silindiği için bu sürümde yeniden yazılmış iki kısa test çalıştırıldı:

| Test | Sonuç |
|---|---|
| Duman testi | 7 görünümün hepsi açılıyor. 2.343 tanım (L0 1 · L1 49 · L2 688 · L3 1.605); taşınan 32 / standart 2.310 / uygulayansız 1 (orkestratör). Yazma / çalıştırma 18 / 12, `migrated_from` 33, çoklu uygulayan 0. Analiz görevi tamamlanıyor. `needs_approval:false` yazılmış ödeme görevi yine onay bekliyor. İzleyici onay politikasını değiştiremiyor (`forbidden`). JS hatası yok |
| Değişmezlik (uyarlama öncesi `17e4e029…` ↔ sonrası) | Ajan Kaydı kullanılmamış projede prompt `9956a0d7/7392`, kurallar `5dc79f32/7589`, zip `18a77ad3/16254`, proje dosyası `a13afa94/21806`, localStorage `79797bab/635` — iki sürümde birebir aynı; kayda yalnız bakmak `state.registry` oluşturmuyor |

Bu sürümde tam test dizisi (173 test) **yeniden çalıştırılmadı**; aşağıdaki sonuçlar önceki sürüm (`5a478ca7…`) içindir.

## 1. Özet

| Test | Sonuç |
|---|---|
| Ajan Kaydı birim ve senaryo testleri (`rg_test.js`) | **173 PASS / 0 FAIL** |
| Kod incelemesi bulgularının kanıt senaryoları (bağımsız inceleme betiği) | 10 bulgunun 10'u düzeltildi; senaryolar artık engelleniyor (bkz. §3) |
| Değişmezlik karşılaştırması (`cmp.js`) | Ajan Kaydı kullanılmamış projede prompt, kurallar, zip, proje dosyası ve localStorage karması uyarlama öncesi sürümle **aynı** (bkz. §4). Kayda yalnız bakmak `state.registry` oluşturmuyor |
| Ajan araması regresyonu | İlk sürümde 41 PASS / 0 FAIL. Katalog ajanları kaldırıldıktan sonra 19 PASS / 6 FAIL; uyarlama öncesi sürümde (`3397f28c…`) de aynı — bkz. not |
| Komite / çalışma grubu kartı regresyonu | İlk sürümde 12 PASS / 0 FAIL. Katalog ajanları kaldırıldıktan sonra 8 PASS / 1 FAIL; uyarlama öncesi sürümde de aynı — bkz. not |
| Ajanlar sayfası genel testi (`agents_test2.js`) | 3 FAIL; değişiklik öncesi ve sonrası sürümlerde birebir aynı satırlar — bkz. not |
| JavaScript hatası | Bütün test çalıştırmalarında yok |
| Ekran görüntüsü | İlk sürümde: görevler ve onaylar 1440 px açık ve koyu tema; liste 520 px (yatay taşma yok, `scrollWidth` 520 = `clientWidth` 520). Uyarlama yalnız etiket metinlerini değiştirdi; ekran görüntüsü yeniden alınmadı |

**Arama ve komite testleri notu.** Bu iki test, diğer oturumun kaldırdığı Geliştirme / Ürün İçi Ajanlar sekmelerine ve katalog kimliklerine bağlı. Kırılmalar Ajan Kaydı'nın uyarlamasından önce de aynı sayıdaydı; testlerin yeni sekme yapısına uyarlanması gerekir. Durum o oturuma bildirildi.

**`agents_test2.js` notu.** Başarısız 3 satır ("kategoriler", "prompt geliştirme bloğu", "prompt ürün içi bloğu") değişiklikten önceki sürümde de birebir aynı başarısızdır. Bunlar testin eski kategori ve prompt beklentileridir; bu değişiklikten gelmez.

## 2. Ajan Kaydı testleri — gruplar

| Grup | PASS | Kapsam |
|---|---|---|
| 1 ID benzersizliği | 6 | 2.343 tanım; kimlikler ve pozisyon anahtarları tekil; biçim `AGT-NN-NNNN`; unvan değişince kimlik aynı kalır; yeniden kurulum aynı kimlikleri verir |
| 2 Pozisyon–ajan eşleştirme | 12 | Tanım sayısı = şemadaki pozisyon sayısı. Komite düğümleri tanım değil. Katalog içeriği taşınan 32 pozisyon / 33 eski ajan; eski kimlik kendi pozisyon ajanına çözülür; taşınan pozisyonun tek uygulayanı kendi ajanı. Birden çok uygulayanı olan tanım yok. AGT-15-0069'da iki eski ajanın araçları birleşik, yazma ve çalıştırma yetkisi korunuyor, `migrated_from` iki kimlik. Yetki uygulayanın araçlarından türer. Gizli görev sayısı raporlanır |
| 3 Hiyerarşi döngüsü | 8 | Döngü yok; yalnız orkestratör kök. Seviye kuralı ve istisnaları. Prompttaki örnek akış L1 → L2 → L2 → L3. Yapay döngü yakalanır |
| 4 Çapraz departman | 9 | Organlar; üç departmandan çalışma grubu üyeleri; koltuk eşlemesinden otomatik üyelik. Üyelik, ajan kartıyla aynı kayıt. Orkestratör üye olamaz. Departmanlar arası doğrudan devir reddedilir |
| 5 Skill–Agent çoktan çoğa | 6 | Bir skill birden çok ajanda, bir ajanda birden çok skill; tek kaynak (`skills`); kaldırma yalnız o ajandan |
| 6 Skill sürümleme | 17 | 1.0.0 katalog sürümü. Aynı içerikle yayın reddedilir. Sürüm artışı major / minor / patch. JSON şema doğrulaması. Etkinleştirme ve sabitleme. Sabitli sürüm kaldırılamaz. İzin eksikse yayın reddedilir. Kapsam |
| 7 Yetkisiz işlem | 12 | Yazma yetkisiz kayıt. Örnek ve şirket kısıtı. İzleyici rolü. Yetkisiz üst ajan üzerinden dolaylı yazma. Üyelik yetki vermez. Organ isteği sınırı. Çalıştırma öncesi denetim |
| 8 İnsan onayı | 11 | 8 işlem türü her zaman onaylı; düzenleyici onay veremez; ikinci karar reddedilir; politika açık / kapalı; ret görevi iptal eder; skill sürümünün onay politikası |
| 9 Tenant izolasyonu | 8 | İki şirkette ayrı örnek. Başka şirketin örneği / görevi okunamaz, çalıştırılamaz, değiştirilemez, devredilemez. Zincirde başka şirket varsa yetki boş |
| 10 Doğrulama (API karşılığı: servis fonksiyonları) | 17 | Boş / uzun alanlar, bilinmeyen değerler, sınırlar, geçersiz durum geçişi, kilitli proje, tanım değişikliğinde sürüm ve geçmiş |
| 11 Veri bütünlüğü | 8 | `DATA.departments` değişmedi. Defter = 2.342 pozisyon, eksik ya da fazla yok. Departman kodları 01–23. Dışa aktarım sayıları; haritada her ajan bir kez |
| 12 Idempotency | 10 | Örnek tekrar oluşmaz. Aynı anahtar + aynı içerik → aynı görev; aynı anahtar + farklı içerik → `conflict`. Yeniden deneme, zaman aşımı, süpürme |
| Devir ve yürütme | 6 | Beş halkalı zincir, döngü, yukarı devir reddi, takılabilir yürütücü, görev / yürütme geçmişi |
| 13 Yönetim paneli | 19 | Sekme ve sayaç; liste, arama, sayfalama ve filtreler; detay; yedi görünümün hepsi; arayüzden örnek, durum, yetki, görev ve sürüm |
| Denetim kaydı | 2 | Her değişiklik kaydedilir; zaman / kişi / işlem / hedef dolu |
| 14 İnceleme bulguları | 22 | §3'teki düzeltmelerin regresyon testleri |

## 3. Kod incelemesi bulguları ve düzeltmeleri

Modül, `kod-hata-avcisi` ajanıyla bağımsız olarak incelendi. Bulguların her biri test kopyasında çalıştırılarak kanıtlandı ve düzeltildi. Düzeltmeler 14. gruptaki testlerle korunuyor.

| # | Önem | Bulgu | Düzeltme |
|---|---|---|---|
| 1 | Kritik | Devirli görev, üst görevi açan kullanıcının rolünü alıyordu; İzleyici, yöneticinin görevinden çalıştırma görevi açabiliyordu | Rol her zaman o anki kullanıcıdır; devirde kök görevi açanın rolüyle kesişir |
| 2 | Kritik | Çalıştırma, görevin açıldığı andaki rolle denetleniyordu | Çalıştırmada o anki rol ∩ açan ∩ kök görevi açan |
| 3 | Kritik | Onay ihtiyacı yalnız görev açılırken hesaplanıyordu; kayıtta `needs_approval:false` yazınca ödeme onaysız tamamlanıyordu | Çalıştırmada yeniden hesaplanır, yalnız eklenir |
| 4 | Yüksek | Yönetim işlemlerinde rol denetimi yoktu; Düzenleyici onay politikasını ve şirket yetkilerini değiştirebiliyordu | `rgRole` ile Yönetici / Düzenleyici sınırı (AGENT_PERMISSION_MATRIX.md §3). Rol seçimi tek kullanıcılı dosyada denemedir; arayüzde ve belgelerde açıkça yazıyor |
| 5 | Yüksek | Zaman aşımından sonra eski denemenin geç yanıtı görevi tamamlıyordu | Sonuç yalnız görevin o anki denemesinden kabul edilir |
| 6 | Orta | Aynı idempotency anahtarı farklı içerikte eski görevi döndürüyordu; otomatik anahtar önceliği ve sınırları kapsamıyordu | İstek parmak izi (`fp`); farklıysa `conflict`; otomatik anahtar bütün alanları kapsar |
| 7 | Orta | Çok alanlı tanım değişikliğinde doğrulama hatası olsa da önceki alanlar kaydediliyordu | Önce bütün alanlar doğrulanır, sonra uygulanır; `rgDo` hata olunca kaydı işlem öncesine döndürür (`rgInstSet` de aynı düzende) |
| 8 | Orta | `requester:{type:"agent"}` ile devir denetimi atlanabiliyordu | Ajan talebi yalnız `parent` üzerinden |
| 9 | Düşük | Şirket değişince önceki şirketin görev ayrıntısı görünüyordu; servislerde şirket parametresi isteğe bağlıydı | Görev ayrıntısı şirkete göre süzülür; `rgTask` / `rgInstGet` / `rgDecide` şirket bağlamı olmadan reddeder |
| 10 | Düşük | Üst görevin tanımı kaynakta yoksa kodsuz hata; bilinmeyen karar rolü denetim görünümünü çökertiyordu | Kodlu `invalid` hatası; bilinmeyen rol adı olduğu gibi gösterilir |

**XSS.** İnceleme, kullanıcı verisinin kaçışsız HTML'e girdiği bir yer bulmadı. Metinler `E()` ile kaçırılır, satır içi `onclick` değerleri `rgJ` ile JSON-tırnaklanır.

## 4. Değişmezlik

Senaryo: Ajan Kaydı'nı kullanmayan bir proje. İki eski katalog kimliği (`agToggle("backend-mimar")`, `agToggle("frontend-mimar")`; artık pozisyon ajanına çözülür), bir pozisyon ajanı ve bir komite seçildi, sonra kaydın bütün görünümleri açılıp kapandı.

| Çıktı | Uyarlama öncesi (`3397f28c…`) | Sonra (`5a478ca7…`) |
|---|---|---|
| Claude promptu | `a5d7b8b3/7292` | `a5d7b8b3/7292` |
| Proje Kuralları | `cb3f661a/7489` | `cb3f661a/7489` |
| Ajan zip'i | `31f89edd/13512` | `31f89edd/13512` |
| Proje dosyası | `27f8d856/21072` | `27f8d856/21072` |
| localStorage | `79797bab/635` | `79797bab/635` |

İlk yazımda da (`8c6c53ec…` → `5ceaf9a1…`) aynı karşılaştırma birebir aynı çıkmıştı. O sürümde karma değerleri farklıydı, çünkü katalog ajanları henüz kaldırılmamıştı.

Değerler FNV-1a karması / uzunluktur.

## 5. Yeniden çalıştırma

1. Gerçek dosyanın bir kopyasını proje klasörü dışına alın.
2. `rg_test.js` içeriğini kopyada `</script></body></html>` öncesine ekleyin ve localStorage anahtarını değiştirin.
3. Şu komutla çalıştırıp `<pre id="testResult">` içeriğini okuyun:
   ```sh
   "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --disable-gpu --window-size=1440,1000 --virtual-time-budget=30000 --dump-dom file://<kopya>
   ```

JSON dışa aktarımı aynı yöntemle üretilir: test betiği `rgFiles()` çıktısını sayfaya yazar.

**Uyarı:** Test betikleri (`rg_test.js`, `cmp.js`, `export.js`, ekran görüntüsü senaryoları) oturumun geçici çalışma klasöründeydi ve o klasör 2026-10-30'da temizlendi. Bu rapordaki sonuçlar silinmeden önce alındı. Testleri yeniden çalıştırmak için betiklerin yeniden yazılıp proje içinde saklanması gerekir.

## 6. Çalıştırılmayan ya da uygulanamayan testler

| Konu | Durum |
|---|---|
| Lint / TypeScript / build | **Uygulanamaz.** Projede derleme adımı, linter veya TypeScript yok. Yalnız modülün sözdizimi `node --check` ile denetlendi; tarayıcıda çalıştırmada JS hatası yok |
| Prisma, migration, REST API, sunucu tarafı denetim, veritabanı tenant izolasyonu | **Uygulanamaz** (sunucusuz mimari, kullanıcı kararı) |
| Gerçek LLM sağlayıcısıyla yürütme | **Test edilmedi.** Bağlı sağlayıcı yok; yalnız sahte yürütücü (`mock`) ve testteki denetimli yürütücü kullanıldı |
| Çok kullanıcılı rol ayrımı | **Test edilemez.** Kimlik doğrulama yok; roller tek kullanıcının seçimidir |
| Ekran okuyucu ile erişilebilirlik | **Test edilmedi.** Yalnız `role="status"` / `role="alert"` mesajları, etiketli alanlar ve klavye ile erişilebilir düğmeler kodda kontrol edildi |
| 500 px'ten dar ekran | **Test edilmedi** (headless en az 500 px çizer). 520 px'te taşma yok |
| Büyük görev / denetim hacmi altında performans | **Ölçülmedi.** Denetim kaydı 5.000 satırla sınırlı; liste 50 satırlık sayfalarla çizilir |
