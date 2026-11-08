# Ajan Kaydı — Mimari ve Tasarım Kararları

Bu doküman `web-proje-gelistirme.html` içindeki **Ajan Kaydı** (Agent Registry) ve skill yönetimi altyapısını anlatır. Arayüzde yeri: Ajanlar sayfası → **Ajan Kaydı** sekmesi. Kod: `function rgBuild` ile başlayan `rg*` fonksiyonları (`renderAgents`'tan hemen önce); stil bloğu `v25-agent-registry`; kimlik betiği `docs/organizasyon/ajan_kimlik_ekle.py`.

## 1. Kapsam ve mimari kısıt

Uygulama tek bir HTML dosyasıdır; sunucu, veritabanı ve API yoktur. Görev tanımındaki Prisma / PostgreSQL / migration / REST API / sunucu tarafı doğrulama maddeleri bu mimaride **uygulanamaz**; kullanıcı 2026-10-30'da altyapının WP-OnKe'de, mevcut mimariye uygun kurulmasını seçti. Bunun sonuçları:

| Görev tanımındaki öğe | WP-OnKe karşılığı |
|---|---|
| Prisma şeması, PostgreSQL ilişkileri | `DATA` (salt okunur kaynak) + `state.registry` (kullanıcı verisi); ilişkiler kimliklerle kurulur |
| Migration | `ajan_kimlik_ekle.py` (kimlik defteri, idempotent) — veri taşınmaz, tanımlar kaynaktan türetilir |
| API katmanı | Tarayıcı içi servis fonksiyonları (`rgDefSet`, `rgInstCreate`, `rgTaskCreate` …); her biri girdiyi doğrular, hatayı kodla (`err.code`) fırlatır |
| Sunucu tarafı yetki denetimi | Her servis fonksiyonunda aynı denetim; arayüz yalnız bu fonksiyonları çağırır. **Tarayıcıdaki kodu değiştirebilen biri denetimi atlayabilir** — gerçek güvenlik sınırı değildir |
| Tenant izolasyonu | Her kayıt bir şirkete (`company`) bağlıdır; servisler şirket bağlamı dışındaki kayda erişimi reddeder. Tek kullanıcılı, yerel bir araçtır |
| Kullanıcı / rol modeli | Oturumdaki rol (Yönetici / Düzenleyici / İzleyici) kullanıcının seçimidir; kimlik doğrulama yoktur. Dosya tek kullanıcılıdır: rol seçimi işlemleri o rolle denemek içindir ve herkes rolünü değiştirebilir. Gerçek rol ayrımı sunucuda kimlik doğrulama gerektirir |

Altyapı ileride gerçek bir sunucuya taşınacaksa veri modeli (§3) ve kurallar (§5–7) aynen kullanılabilir; dışa aktarılan JSON dosyaları bu taşımanın girdisidir.

## 2. Temel ilke: ikinci bir organizasyon yok

- Departman, birim, ekip ve pozisyonun tek kaynağı `DATA.departments`'tır (kullanıcının `docs/organizasyon/*.json` dosyalarından `departman_ekle.py` ile üretilir). Ajan Kaydı bunları **okur**, kopyalamaz.
- Ajan tanımları her açılışta organizasyondan türetilir. Kullanıcı değişiklikleri yalnız fark olarak `state.registry.defs[agent_id]` içinde tutulur.
- Ajanın uygulayıcısı mevcut ajan sistemidir: pozisyonun ajanı (`pagBase`). 2026-10-30'dan beri sistemde yalnız pozisyon ajanları vardır; kullanıcının oluşturduğu özel ajanlar kaldırıldı. 2026-10-30'da 33 katalog ajanının (20 geliştirme + 13 ürün içi) içeriği bulundukları 32 pozisyonun ajanına taşındı (`DATA.positionAgents`, ajanda `legacy`). Eski kimlikler (`backend-mimar` …) `agId()` ile pozisyon ajanına çözülür; dışa aktarılan tanımda `migrated_from` alanı taşınan eski kimlikleri listeler.
- Skill bağlantısı da mevcut sistemdedir: uygulayıcı ajanın `skills` dizisi (`skLink`). Kayıt yalnız sürüm sabitlemesini ekler.
- Kurul / komite / çalışma grubu üyeliği de mevcut sistemdedir: `agMemb()`. Bu fonksiyon `DATA.membership` koltuk eşlemesini ve `state.agents[id].memb` elle değişikliklerini birleştirir. Kayıt bu modeli okur ve oraya yazar.

## 3. Mantıksal varlıklar ve nerede tutuldukları

| Varlık | Kaynak / depo | Not |
|---|---|---|
| AgentDefinition | `rgDefs()` ← `DATA.departments` + `DATA.agentIds` + `state.registry.defs` | 1 orkestratör + her pozisyon için 1 tanım |
| AgentInstance | `state.registry.instances["INS-<şirket>-<agent_id>"]` | Şirket başına tanım başına en çok 1 örnek |
| AgentHierarchy | Tanımda `parent_agent_id` (yürütme) ve `org_parent_agent_id` (insan şeması) | `rgKids`, `rgAncestors`, `rgCycles` |
| SkillDefinition | `skAll()` (katalog + özel skill) → `rgSk()` | `SKL-<KOD>` |
| SkillVersion | Katalog skill'inde örtük 1.0.0 + `state.registry.skills[kod].versions[]` | İçerik parmak izi (FNV-1a) ile değişiklik tespiti |
| AgentSkillAssignment | Uygulayıcı ajanın `skills` dizisi + `state.registry.pins[agent_id][kod]` | Sabitleme yoksa en son etkin sürüm |
| AgentToolAssignment | Uygulayıcı ajanların `tools` birleşimi (`d.tools`) | Araç → yetki eşlemesi `RG_TOOL_PERM` |
| AgentTask | `state.registry.tasks["TSK-…"]` | Durum makinesi §6 |
| AgentExecution | `task.executions[]` | Deneme başına bir kayıt |
| AgentApproval | `state.registry.approvals["APR-…"]` | Yalnız insan karar verir |
| AgentAuditLog | `state.registry.audit[]` | Her değişiklik; en çok 5.000 kayıt, düşen sayısı `auditDropped` |
| Şirket (tenant) | `state.registry.companies[]` | Varsayılan: proje adıyla tek şirket |

`state.registry` yalnız ilk değişiklikte oluşur. Ajan Kaydı'na yalnız bakmak hiçbir şey yazmaz. Kayıt kullanılmamış bir projede Claude promptu, kurallar, zip, proje dosyası ve localStorage öncekiyle birebir aynıdır (test: AGENT_TEST_REPORT.md).

## 4. Kimlik (Agent ID)

- Biçim: `AGT-<departman kodu>-<4 haneli sıra>`, örneğin `AGT-09-0024`. Orkestratör `AGT-00-0001`.
- Kimlikler `docs/ajan-kaydi/agent-id-ledger.json` defterinde tutulur ve `DATA.agentIds`'e işlenir. Arayüz kimliği hesaplamaz, defterden okur.
- Neden defter: pozisyon kimlikleri bazı departmanlarda unvandan türer. Unvan değişince pozisyon kimliği değişebilir, ama Agent ID değişmemelidir.
- Unvan değişip pozisyon kimliği aynı kalırsa: Agent ID aynı kalır, yalnız ad güncellenir.
- Pozisyon kimliği de değişirse: betik eskisini emekliye ayırır, yenisine geçici kimlik verir ve "olası yeniden adlandırma" diye yazar. Defterin `aliases` alanına `"departman|eski": "departman|yeni"` eklenip betik yeniden çalıştırılınca yeni pozisyon eski kimliği alır. Geçici kimlik `replaced_id` olarak not edilir.
- Numaralar bir daha verilmez; emekli kayıt silinmez.
- Departman kodu ilk atamadaki sıradır ve defterde sabittir.
- `agent_code` (örn. `09-TEKNIK-SEO-UZMANI`) rol kodudur. Aynı departmanda aynı unvanlı farklı koltuklar bu kodu paylaşır.

## 5. Yürütme hiyerarşisi (L0–L3)

| Seviye | Tür | Hangi pozisyonlar |
|---|---|---|
| L0 | Orkestratör | Ana asistan (Claude Code ana oturumu) |
| L1 | Departman | Departman lideri, ara yönetici (ofis), yönetim pozisyonları (aides), yönetim kurulu ve kurul rolleri |
| L2 | Birim / ekip | Birim lideri, ekip yöneticisi |
| L3 | Uzman | Ekip rolleri, birime bağlı roller, matris roller |

Yürütme üstü, insan şemasındaki üst zincirde (`up`) seviyesi daha küçük olan ilk pozisyondur. İki istisna vardır:
- ekip yöneticisi birim liderine bağlanır;
- ara yönetici ve yönetim pozisyonları departman liderine bağlanır.

Departman liderleri, kurul ve kurul rolleri yürütmede orkestratöre bağlıdır. Böylece insan şemasıyla yürütme hiyerarşisi ayrışır: lider insan şemasında CEO'ya raporlar, yürütmede ise işi orkestratörden alır. İkisi farklıysa Organizasyon görünümünde "insan hiyerarşisi farklı" yazar.

Örnek akış: `AGT-09-0001` Pazarlama ve Büyüme Direktörü (L1) → `AGT-09-0016` Dijital Pazarlama ve Talep Yaratma Direktörü (L2, birim) → `AGT-09-0022` SEO ve GEO Müdürü (L2, ekip) → `AGT-09-0024` Teknik SEO Uzmanı (L3).

## 6. Görev yaşam döngüsü

```
pending → assigned → running → awaiting_approval → completed
                        │  ↘ completed (onay gerekmiyorsa)
                        ├→ assigned (hata/zaman aşımı, deneme hakkı varsa)
                        └→ failed
pending / assigned / awaiting_approval → cancelled ;  assigned → failed (çalıştırma öncesi denetim)
```

- **Idempotency:** Her görev, isteğin bütün alanlarından (ajan, başlık, girdi, açıklama, beklenen çıktı, skill ve sürüm, işlem türü, üst görev, talep eden, öncelik, deneme sayısı, zaman aşımı, yürütücü) bir parmak izi (`fp`) saklar.
  - Açık `idem` anahtarı aynı içerikle gelirse aynı görevi döndürür. Farklı içerikle gelirse `conflict` hatası verir; çağıran yanlış görevin açıldığını sanmaz.
  - Anahtar verilmezse parmak izi otomatik anahtar olur. Otomatik anahtarlı başarısız ya da iptal edilmiş görev yeniden açılabilir.
- **Talep eden:** Kullanıcı ya da kurul / komite / çalışma grubu olabilir. Ajan talebi yalnız bir üst görevden devirle (`parent`) açılır; dışarıdan "ajan istedi" denerek devir zinciri ve hiyerarşi denetimi atlanamaz.
- **Yeniden deneme ve zaman aşımı:** `max_attempts` 1–5 arası olabilir (varsayılan 2), `timeout_ms` 100–600.000 arası (varsayılan 30.000). `rgSweep` askıda kalan çalışmaları işler; örneğin yürütme sırasında sayfa yenilendiyse. Zaman aşımından sonra eski denemenin yanıtı gelirse sonuç kullanılmaz: yalnız görevin o anki denemesi görevi tamamlayabilir.
- **Devir ve döngü önleme:** Görev yalnız yürütme hiyerarşisinde alttaki ajana devredilebilir. Orkestratör her departmana devredebilir; departmanlar arası doğrudan devir yoktur. Zincirde aynı ajan iki kez olamaz ve zincir en çok 5 ajan olabilir (L0→L1→L2→L2→L3).
- **Çalıştırma öncesi denetim:** Görev çalıştırılmadan hemen önce yetki yeniden denetlenir. Kullanılan rol, o anki kullanıcının rolü, görevi açanın rolü ve (devirde) kök görevi açanın rolünün kesişimidir. İnsan onayı ihtiyacı da yeniden hesaplanır (`t.needs_approval || rgNeeds(…)`): proje dosyasında değer değiştirilse ya da politika sonradan sıkılaştırılsa da onay atlanamaz.
- **Yürütme arayüzü:** `RG_ADAPTERS[ad].run(ctx)` → `{ok, output}` ya da `{ok:false, error}` (Promise olabilir). Gerçek bir LLM sağlayıcısı bağlı değildir. Yalnız test edilebilir **sahte yürütücü** (`mock`) vardır: girdide `#hata` hata, `#bekle` zaman aşımı üretir. Yeni bir sağlayıcı, aynı imzayla `RG_ADAPTERS`'e eklenerek takılır.

## 7. Kurul, komite ve çalışma grupları

- Organlar kendi modelleriyle kalır (`DATA.boards`, `DATA.committees`, `DATA.workingGroups`).
- Üyelik ajan tarafındaki modeldir. Kayıt ekranında ya da ajan kartında elle eklenen ve çıkarılan üyeler aynı kayda yazılır.
- Organ, üye ajandan yalnız **analiz / rapor** ve **karar taslağı** isteyebilir. Etkin yetki read / analyze / propose ile sınırlanır.
- Karar taslağı her zaman insan onayına gider: karar hazırlama ajanda, karar onayı insandadır.
- Üyelik ajana yetki vermez (test edildi).

## 8. Skill altyapısı

- Skill içeriği (açıklama, talimat, araçlar) Skill Kütüphanesi'nde düzenlenir. Ajan Kaydı bu içeriği **sürüm** olarak yayınlar. Sürüm artışı major, minor veya patch olabilir; her sürüm taslak olarak başlar ve etkinleştirilir ya da kullanımdan kaldırılır.
- Sürüm alanları: girdi ve çıktı şeması (JSON Schema alt kümesi: kökte `type: object`, `properties`, `required`), gereken izinler (araçların gerektirdiği izinler zorunlu), kalite ölçütleri, onay politikası (`human_required` / `policy` / `none`).
- Kapsam: tek departmandaki pozisyonlara bağlı skill varsayılan olarak departmana özeldir, diğerleri geneldir. Kapsam değiştirilebilir.
- Atama kuralı: skill sürümünün gerektirdiği izinler ajanın yetkisini aşamaz.
- Sabitlenmiş sürüm kullanımdan kaldırılamaz.
- Görevde kullanılan sürüm etkin olmalıdır.
- Bu fazda skill talimatları yazılmadı. `SKILL_REGISTRY.json`'daki `suggested_categories` alanı (birim başına bir kategori) yalnız **öneri** envanteridir.

## 9. Sonraki faz

1. Pozisyonlar için uzmanlık skill'lerinin yazılması: önerilen kategorilerden başlanır; her skill önce taslak sürüm, inceleme, sonra etkin.
2. Gerçek yürütücü: `RG_ADAPTERS`'e bir sağlayıcı (ör. Claude API) eklemek. Anahtar yönetimi ve dış çağrı gerektirdiği için ayrı güvenlik incelemesi gerekir.
3. Sunucuya taşıma gerekirse: `AGENT_REGISTRY.json` / `SKILL_REGISTRY.json` / `AGENT_ORGANIZATION_MAP.json` dosyaları başlangıç verisidir. Yetki denetimleri sunucuda yeniden uygulanmalıdır.
4. Görev tanımları kullanıcı tarafından yeniden yazılınca `DP_DUTIES=true`; tanımların `responsibilities` alanı o zaman dolar.
