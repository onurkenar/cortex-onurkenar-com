# Ajan Yetki ve Onay Matrisi

Kaynak: `web-proje-gelistirme.html` içindeki `RG_PERMS`, `RG_TOOL_PERM`, `RG_ROLES`, `RG_BODY_CAPS`, `RG_OPS` ve denetim fonksiyonları `rgEff` / `rgGate` / `rgNeeds` / `rgDecide`. Denetimler tarayıcıda çalışır (bkz. AGENT_ARCHITECTURE.md §1).

## 1. Yetki seviyeleri

| Kod | Ad | Anlamı |
|---|---|---|
| `read` | Görüntüleme | Veriyi görüntüleme |
| `analyze` | Analiz | Veriyi analiz etme |
| `propose` | Öneri | Öneri ve karar taslağı oluşturma |
| `write` | Yazma | Kayıt oluşturma veya değiştirme |
| `execute` | Çalıştırma | İzin verilen işlemleri çalıştırma |
| `approve` | Onay | Tanımlı onay mekanizmasında karar verme. Ajanlara verilse de hiçbir onay kaydını ajan karara bağlayamaz; onay kaydını yalnız insan kullanıcı kapatır |

## 2. Tanımın varsayılan yetkisi

Varsayılan yetki, pozisyonu uygulayan ajanın araçlarından türetilir:

| Araç | Gerektirdiği yetki |
|---|---|
| Read, Grep, Glob | read |
| WebSearch, WebFetch | analyze |
| Edit, Write | write |
| Bash | execute |

- Her tanımda `read`, `analyze` ve `propose` açıktır; `approve` kapalıdır.
- Yalnız Read/Grep/Glob araçlı pozisyon ajanları okuma, analiz ve öneri yetkisiyle başlar.
- Kaynak verilerde 18 tanım yazma, 12 tanım çalıştırma yetkisiyle başlar. Bunların hepsi, Edit/Write/Bash araçlı eski katalog ajanlarının içeriği (araçlarıyla birlikte) taşınan pozisyonlardır.
- Bütün tanımlar **taslak** başlar ve "Yazma ve çalıştırma işlemlerinde insan onayı gerekir" ayarı açıktır.

## 3. Etkin yetki

```
etkin = tanım yetkisi
      ∩ örnek kısıtı           (örnek tanımı yalnız daraltabilir; aşan değer reddedilir)
      ∩ şirketin izin verdiği   (şirket ayarı)
      ∩ kullanıcı rolü         (o anki kullanıcı ∩ görevi açan ∩ devirde kök görevi açan; çalıştırmada yeniden)
      ∩ {read, analyze, propose}   (istek bir kurul / komite / çalışma grubundan geliyorsa)
      ∩ devir zincirindeki her ajanın etkin yetkisi   (başka şirketten bir ajan varsa: boş küme)
```

| Rol | İzin verdiği yetkiler |
|---|---|
| Yönetici | read, analyze, propose, write, execute, approve |
| Düzenleyici | read, analyze, propose, write, execute |
| İzleyici | read, analyze |

Yönetim işlemleri de role bağlıdır (`rgRole`):

| İşlem | En az rol |
|---|---|
| Tanımın durumu, yetkileri ve insan onayı ayarı | Yönetici |
| Tanımın misyonu, girdileri, çıktıları ve sorumlusu | Düzenleyici |
| Şirket ekleme ve şirket yetkileri | Yönetici |
| Örnek oluşturma ve örnek sorumlusu | Düzenleyici |
| Örnek durumu; örnekte daraltılmış yetkiyi geri açma | Yönetici |
| Örnekte yetki daraltma | Düzenleyici |
| Skill sürümü yayınlama (taslak) | Düzenleyici |
| Skill sürüm durumu, kapsamı, ataması ve sabitleme | Yönetici |
| Kurul / komite / çalışma grubu üyeliği | Düzenleyici |
| İnsan onayı verme / reddetme | Yönetici (onay yetkisi) |

> **Sınır:** Uygulama tek bir HTML dosyasıdır ve kimlik doğrulama yoktur. Oturumdaki rol kullanıcının seçimidir ve her kullanıcı rolünü değiştirebilir. Bu denetimler istemcide çalışır; amaçları kuralları o rolle denemek ve hatalı işlemi engellemektir. Gerçek rol ayrımı ancak sunucu tarafında kimlik doğrulama ile sağlanır.

Ek kurallar:
- Skill sürümünün gerektirdiği izinler etkin yetkiyi aşamaz.
- Skill'in istediği her araç ajana atanmış olmalı ve aracın yetkisi etkin yetkide bulunmalıdır.
- Görev çalıştırılmadan hemen önce bütün denetimler o anki rolle yeniden yapılır. Görev oluşturulduktan sonra yetki daraltıldıysa ya da görevi daha düşük yetkili bir rol çalıştırıyorsa görev başarısız olur.
- İnsan onayı ihtiyacı çalıştırmada yeniden hesaplanır ve yalnız eklenebilir: kayıtta `needs_approval:false` yazmak ya da politikayı görev açıldıktan sonra sıkılaştırmak onayı atlatmaz.

## 4. İşlem türleri ve insan onayı

| İşlem | Gereken yetki | İnsan onayı |
|---|---|---|
| Analiz ve rapor | analyze | Gerekmez |
| Öneri ve karar taslağı | propose | Gerekmez; kurul / komite isteğinde **her zaman** |
| Kayıt oluşturma veya değiştirme | write | Tanımın politikasına bağlı (varsayılan: gerekir) |
| İzin verilen iç işlemi çalıştırma | execute | Tanımın politikasına bağlı (varsayılan: gerekir) |
| Ödeme ve finansal taahhüt | execute | **Her zaman** |
| Personel özlük verisini değiştirme | write | **Her zaman** |
| İşe alım, işten çıkarma ve ücret kararı | write | **Her zaman** |
| Sözleşme onayı | write | **Her zaman** |
| Müşterilere dış iletişim gönderimi | execute | **Her zaman** |
| Reklam bütçesi ve kampanya değişikliği | execute | **Her zaman** |
| Üretim ortamı değişikliği | execute | **Her zaman** |
| Veri silme ve yüksek riskli toplu işlem | execute | **Her zaman** |

Skill sürümünün onay politikası da onayı zorunlu kılabilir:
- `human_required`: varsayılandır, her zaman onay ister;
- `policy`: tanımın ayarına uyar;
- `none`: kendisi onay istemez.

Onay, işlem türünün ya da tanımın gerektirdiği onayı **kaldıramaz**; yalnız ekleyebilir.

## 5. Onay kuralları

- Onay gerektiren görev, yürütücü çıktıyı ürettikten sonra `awaiting_approval` durumunda durur ve bir onay kaydı açılır.
- Karar yalnız oturumdaki rolü onay yetkisi taşıyan **insan** kullanıcıdan gelir (`rgDecide`). Ajan, kurul, komite ya da çalışma grubu adına karar verecek bir yol yoktur.
- Onay görevi tamamlar, ret görevi iptal eder. Karara bağlanmış kayıt yeniden karara bağlanamaz.
- Karar veren kişi, rolü, zamanı ve notu kaydedilir.

## 6. Dolaylı yetki yükseltmeye karşı

| Yol | Engel |
|---|---|
| Yetkisiz ajan, yetkili alt ajana iş devreder | Zincirdeki her ajanın etkin yetkisiyle kesişim alınır |
| Departmanlar arası doğrudan devir | Yalnız yürütme hiyerarşisinde alttaki ajana devir; departmanlar arası devri orkestratör yapar |
| Komite üyeliği üzerinden işlem | Üyelik yetki vermez; organ istekleri analiz / öneri ile sınırlı; karar taslağı insan onayına gider |
| Başka şirketin ajanı / görevi | Şirket bağlamı dışındaki kayda erişim reddedilir; zincirde başka şirket varsa etkin yetki boş |
| Örnekte tanımdan fazla yetki | Reddedilir; örnek yalnız daraltır |
| Skill üzerinden yetki | Skill sürümünün izinleri ve araçları etkin yetkiyi aşamaz |
| Görev açıldıktan sonra yetki kısılması | Çalıştırma öncesi yeniden denetim; görev başarısız olur |
| Yüksek rolün açtığı görevi düşük rolün çalıştırması / devretmesi | Rol, o anki kullanıcı ∩ açan ∩ kök görevi açan |
| Kayıtta onay bayrağını değiştirme | Onay ihtiyacı çalıştırmada yeniden hesaplanır |
| Sahte "ajan istedi" talebi | Ajan talebi yalnız üst görevden devirle açılır |
| Aynı idempotency anahtarıyla farklı iş | Parmak izi farklıysa `conflict` |
| Hatalı çok alanlı değişiklikte yarım kalan yetki | Önce bütün alanlar doğrulanır; hata olursa hiçbir şey yazılmaz ve kayıt işlem öncesine döner |
