
# Belge Ortak Yazım İş Akışı

Bu skill, kullanıcılara ortak belge oluşturma sürecinde rehberlik etmek için yapılandırılmış bir iş akışı sunar. Kullanıcıları üç aşamadan geçiren etkin bir rehber gibi davran: Bağlam Toplama, İyileştirme ve Yapı, Okur Testi.

## Bu İş Akışı Ne Zaman Önerilir

**Tetikleme koşulları:**
- Kullanıcı belge yazmaktan söz eder: "bir belge yaz", "bir öneri taslağı hazırla", "bir spesifikasyon oluştur", "yazıya dök"
- Kullanıcı belirli belge türlerinden söz eder: "PRD", "tasarım belgesi", "karar belgesi", "RFC"
- Kullanıcı kapsamlı bir yazma işine başlıyor gibi görünür

**İlk öneri:**
Kullanıcıya belgeyi birlikte yazmak için yapılandırılmış bir iş akışı öner. Üç aşamayı açıkla:

1. **Bağlam Toplama**: Kullanıcı ilgili bütün bağlamı verir, Claude ise netleştirici sorular sorar
2. **İyileştirme ve Yapı**: Her bölüm beyin fırtınası ve düzenlemeyle yinelemeli olarak oluşturulur
3. **Okur Testi**: Başkaları okumadan önce kör noktaları yakalamak için belge yeni (bağlamsız) bir Claude ile test edilir

Bu yaklaşımın, belgenin başkaları tarafından okunduğunda (onu Claude'a yapıştırdıkları durum dahil) iyi işlemesini sağlamaya yardımcı olduğunu açıkla. Bu iş akışını denemek mi yoksa serbest çalışmak mı istediklerini sor.

Kullanıcı reddederse serbest çalış. Kabul ederse 1. Aşama'ya geç.

## 1. Aşama: Bağlam Toplama

**Amaç:** Kullanıcının bildikleriyle Claude'un bildikleri arasındaki farkı kapatmak; böylece sonrasında akıllıca rehberlik edebilmek.

### İlk Sorular

Kullanıcıdan belgeyle ilgili üst bağlamı isteyerek başla:

1. Bu ne tür bir belge? (ör. teknik spesifikasyon, karar belgesi, öneri)
2. Birincil hedef kitle kim?
3. Biri bunu okuduğunda istenen etki ne?
4. İzlenecek bir şablon ya da belirli bir biçim var mı?
5. Bilinmesi gereken başka kısıtlar ya da bağlam var mı?

Kısaltmalarla yanıt verebileceklerini ya da bilgiyi kendileri için en kolay hangi biçimde aktarabiliyorlarsa öyle dökebileceklerini belirt.

**Kullanıcı bir şablon verirse ya da bir belge türünden söz ederse:**
- Paylaşabilecekleri bir şablon belgesi olup olmadığını sor
- Paylaşılan bir belgenin bağlantısını verirlerse uygun entegrasyonu kullanarak getir
- Bir dosya verirlerse oku

**Kullanıcı mevcut, paylaşılan bir belgeyi düzenlemekten söz ederse:**
- Güncel durumu okumak için uygun entegrasyonu kullan
- Alternatif metni (alt-text) olmayan görselleri kontrol et
- Alternatif metni olmayan görseller varsa, başkaları belgeyi anlamak için Claude'u kullandığında Claude'un bu görselleri göremeyeceğini açıkla. Alternatif metin üretilmesini isteyip istemediklerini sor. İsterlerse açıklayıcı alternatif metin üretmek için her görseli sohbete yapıştırmalarını iste.

### Bilgi Dökümü

İlk sorular yanıtlandıktan sonra kullanıcıyı elindeki bütün bağlamı dökmeye teşvik et. Şu tür bilgileri iste:
- Proje/sorun hakkında arka plan
- İlgili ekip tartışmaları ya da paylaşılan belgeler
- Alternatif çözümlerin neden kullanılmadığı
- Kurumsal bağlam (ekip dinamikleri, geçmiş olaylar, kurum içi politika)
- Zaman baskıları ya da kısıtlar
- Teknik mimari ya da bağımlılıklar
- Paydaş kaygıları

Düzenleme konusunda endişelenmemelerini, her şeyi olduğu gibi aktarmalarını öğütle. Bağlam vermek için birden çok yol sun:
- Bilinç akışı biçiminde bilgi dökümü
- Okunacak ekip kanallarını ya da yazışma dizilerini gösterme
- Paylaşılan belgelere bağlantı verme

**Entegrasyonlar mevcutsa** (ör. Slack, Teams, Google Drive, SharePoint ya da diğer MCP sunucuları), bunların bağlamı doğrudan çekmek için kullanılabileceğini belirt.

**Hiçbir entegrasyon algılanmadıysa ve Claude.ai ya da Claude uygulamasındaysan:** Mesajlaşma uygulamalarından ve belge depolama hizmetlerinden bağlamı doğrudan çekebilmek için Claude ayarlarında bağlayıcıları (connector) etkinleştirebileceklerini öner.

İlk dökümü yaptıktan sonra netleştirici sorular sorulacağını belirt.

**Bağlam toplama sırasında:**

- Kullanıcı ekip kanallarından ya da paylaşılan belgelerden söz ederse:
  - Entegrasyonlar mevcutsa: İçeriğin şimdi okunacağını belirt, sonra uygun entegrasyonu kullan
  - Entegrasyonlar mevcut değilse: Erişim olmadığını açıkla. Claude ayarlarında bağlayıcıları etkinleştirmelerini ya da ilgili içeriği doğrudan yapıştırmalarını öner.

- Kullanıcı bilinmeyen varlıklardan/projelerden söz ederse:
  - Daha fazla bilgi edinmek için bağlı araçlarda arama yapılıp yapılmayacağını sor
  - Aramadan önce kullanıcının onayını bekle

- Kullanıcı bağlam verdikçe nelerin öğrenildiğini ve nelerin hâlâ belirsiz olduğunu takip et

**Netleştirici sorular sorma:**

Kullanıcı ilk dökümü bitirdiğini belirttiğinde (ya da yeterince bağlam verildikten sonra), anladığından emin olmak için netleştirici sorular sor:

Bağlamdaki boşluklara dayanarak 5-10 numaralı soru üret.

Yanıt verirken kısaltma kullanabileceklerini (ör. "1: evet, 2: #kanal'a bak, 3: hayır, çünkü geriye dönük uyumluluk"), daha fazla belgeye bağlantı verebileceklerini, okunacak kanalları gösterebileceklerini ya da bilgi dökmeye devam edebileceklerini belirt. Kendileri için hangisi en verimliyse.

**Çıkış koşulu:**
Sorular konunun anlaşıldığını gösterdiğinde — temel konuların açıklanmasına gerek kalmadan uç durumlar ve ödünleşimler sorulabildiğinde — yeterli bağlam toplanmış demektir.

**Geçiş:**
Bu aşamada vermek istedikleri başka bağlam olup olmadığını ya da belgenin taslağını yazmaya geçme zamanının gelip gelmediğini sor.

Kullanıcı daha fazlasını eklemek isterse izin ver. Hazır olduğunda 2. Aşama'ya geç.

## 2. Aşama: İyileştirme ve Yapı

**Amaç:** Belgeyi beyin fırtınası, ayıklama ve yinelemeli iyileştirmeyle bölüm bölüm oluşturmak.

**Kullanıcıya talimatlar:**
Belgenin bölüm bölüm oluşturulacağını açıkla. Her bölüm için:
1. Neyin dahil edileceğine dair netleştirici sorular sorulacak
2. 5-20 seçenek için beyin fırtınası yapılacak
3. Kullanıcı neyin tutulacağını/çıkarılacağını/birleştirileceğini belirtecek
4. Bölümün taslağı yazılacak
5. Bölüm nokta atışı düzenlemelerle iyileştirilecek

En çok bilinmeyeni olan bölümle (genellikle çekirdek karar/öneri) başla, sonra diğerlerine geç.

**Bölüm sırası:**

Belge yapısı netse:
Hangi bölümle başlamak istediklerini sor.

En çok bilinmeyeni olan bölümle başlamayı öner. Karar belgelerinde bu genellikle çekirdek öneridir. Spesifikasyonlarda genellikle teknik yaklaşımdır. Özet bölümleri en sona bırakmak en iyisidir.

Kullanıcı hangi bölümlere ihtiyaç duyduğunu bilmiyorsa:
Belge türüne ve şablona göre, o belge türüne uygun 3-5 bölüm öner.

Bu yapının uygun olup olmadığını ya da değiştirmek isteyip istemediklerini sor.

**Yapı üzerinde anlaşıldığında:**

Bütün bölümler için yer tutucu metin içeren ilk belge yapısını oluştur.

**Artifact'lere erişim varsa:**
Bir artifact oluşturmak için `create_file` kullan. Bu, hem Claude'a hem kullanıcıya üzerinde çalışılacak bir iskelet sağlar.

Bütün bölümler için yer tutucular içeren ilk yapının oluşturulacağını belirt.

Bütün bölüm başlıklarını ve "[Yazılacak]" ya da "[İçerik buraya]" gibi kısa yer tutucu metinleri içeren artifact'i oluştur.

İskeletin bağlantısını ver ve her bölümü doldurma zamanının geldiğini belirt.

**Artifact'lere erişim yoksa:**
Çalışma dizininde bir Markdown dosyası oluştur. Uygun bir ad ver (ör. `decision-doc.md`, `technical-spec.md`).

Bütün bölümler için yer tutucular içeren ilk yapının oluşturulacağını belirt.

Bütün bölüm başlıklarını ve yer tutucu metinleri içeren dosyayı oluştur.

Dosyanın oluşturulduğunu adıyla birlikte doğrula ve her bölümü doldurma zamanının geldiğini belirt.

**Her bölüm için:**

### 1. Adım: Netleştirici Sorular

[BÖLÜM ADI] bölümü üzerinde çalışmaya başlanacağını duyur. Neyin dahil edilmesi gerektiğine dair 5-10 netleştirici soru sor:

Bağlama ve bölümün amacına dayanarak 5-10 belirli soru üret.

Kısaltmalarla yanıt verebileceklerini ya da yalnızca neyin ele alınmasının önemli olduğunu belirtebileceklerini söyle.

### 2. Adım: Beyin Fırtınası

[BÖLÜM ADI] bölümü için, bölümün karmaşıklığına göre dahil edilebilecek [5-20] şey için beyin fırtınası yap. Şunları ara:
- Paylaşılmış ama unutulmuş olabilecek bağlam
- Henüz söz edilmemiş bakış açıları ya da dikkate alınacak noktalar

Bölümün karmaşıklığına göre 5-20 numaralı seçenek üret. Sonunda, ek seçenek isterlerse daha fazla beyin fırtınası yapmayı öner.

### 3. Adım: Ayıklama

Hangi maddelerin tutulacağını, çıkarılacağını ya da birleştirileceğini sor. Sonraki bölümler için önceliklerini öğrenmeye yardımcı olması amacıyla kısa gerekçeler iste.

Örnekler ver:
- "1,4,7,9'u tut"
- "3'ü çıkar (1'in tekrarı)"
- "6'yı çıkar (hedef kitle bunu zaten biliyor)"
- "11 ile 12'yi birleştir"

**Kullanıcı numaralı seçim yerine serbest geri bildirim verirse** (ör. "iyi görünüyor" ya da "çoğunu beğendim ama..."), tercihlerini çıkar ve devam et. Neyin tutulmasını/çıkarılmasını/değiştirilmesini istediklerini ayrıştır ve uygula.

### 4. Adım: Eksik Kontrolü

Seçtiklerine dayanarak [BÖLÜM ADI] bölümü için eksik önemli bir şey olup olmadığını sor.

### 5. Adım: Taslak Yazma

Bu bölümün yer tutucu metnini gerçek taslak içerikle değiştirmek için `str_replace` kullan.

[BÖLÜM ADI] bölümünün seçtiklerine dayanarak şimdi yazılacağını duyur.

**Artifact kullanılıyorsa:**
Taslağı yazdıktan sonra artifact'in bağlantısını ver.

Baştan sona okumalarını ve neyin değişmesi gerektiğini belirtmelerini iste. Net olmanın sonraki bölümler için öğrenmeye yardımcı olduğunu not et.

**Dosya kullanılıyorsa (artifact yok):**
Taslağı yazdıktan sonra tamamlandığını doğrula.

[BÖLÜM ADI] bölümünün taslağının [dosya adı] dosyasında yazıldığını bildir. Baştan sona okumalarını ve neyin değişmesi gerektiğini belirtmelerini iste. Net olmanın sonraki bölümler için öğrenmeye yardımcı olduğunu not et.

**Kullanıcı için temel talimat (ilk bölümün taslağı yazılırken ekle):**
Bir not ver: Belgeyi doğrudan düzenlemek yerine neyin değişmesi gerektiğini belirtmelerini iste. Bu, sonraki bölümler için üsluplarının öğrenilmesine yardımcı olur. Örneğin: "X maddesini çıkar — Y zaten kapsıyor" ya da "Üçüncü paragrafı daha kısa yap".

### 6. Adım: Yinelemeli İyileştirme

Kullanıcı geri bildirim verdikçe:
- Düzenlemeleri yapmak için `str_replace` kullan (belgenin tamamını asla yeniden yazdırma)
- **Artifact kullanılıyorsa:** Her düzenlemeden sonra artifact'in bağlantısını ver
- **Dosya kullanılıyorsa:** Yalnızca düzenlemelerin tamamlandığını doğrula
- Kullanıcı belgeyi doğrudan düzenleyip okumanı isterse: yaptığı değişiklikleri zihninde not et ve sonraki bölümler için aklında tut (bunlar tercihlerini gösterir)

**Kullanıcı bölümden memnun kalana kadar yinelemeye devam et.**

### Kalite Kontrolü

Kayda değer değişiklik olmayan art arda 3 yinelemeden sonra, önemli bir bilgiyi kaybetmeden çıkarılabilecek bir şey olup olmadığını sor.

Bölüm bittiğinde [BÖLÜM ADI] bölümünün tamamlandığını doğrula. Sonraki bölüme geçmeye hazır olup olmadıklarını sor.

**Bütün bölümler için tekrarla.**

### Tamamlanmaya Yakın

Tamamlanmaya yaklaşırken (bölümlerin %80'i ya da fazlası bittiğinde), belgenin tamamını yeniden okuyup şunları kontrol etme niyetini duyur:
- Bölümler arasında akış ve tutarlılık
- Tekrarlar ya da çelişkiler
- "Laf kalabalığı" (slop) ya da genel geçer dolgu gibi hissettiren her şey
- Her cümlenin bir ağırlık taşıyıp taşımadığı

Belgenin tamamını oku ve geri bildirim ver.

**Bütün bölümler yazılıp iyileştirildiğinde:**
Bütün bölümlerin taslağının yazıldığını duyur. Belgenin tamamını bir kez daha gözden geçirme niyetini belirt.

Genel tutarlılık, akış ve eksiksizlik açısından gözden geçir.

Varsa son önerilerini sun.

Okur Testi'ne geçmeye hazır olup olmadıklarını ya da iyileştirmek istedikleri başka bir şey olup olmadığını sor.

## 3. Aşama: Okur Testi

**Amaç:** Belgenin okurlar için işe yaradığını doğrulamak amacıyla onu yeni bir Claude ile (bağlam sızıntısı olmadan) test etmek.

**Kullanıcıya talimatlar:**
Belgenin okurlar için gerçekten işe yarayıp yaramadığını görmek üzere şimdi test yapılacağını açıkla. Bu, kör noktaları yakalar — yazarlara anlamlı gelen ama başkalarının kafasını karıştırabilecek şeyleri.

### Test Yaklaşımı

**Alt ajanlara erişim varsa (ör. Claude Code'da):**

Testi kullanıcıyı dahil etmeden doğrudan yap.

### 1. Adım: Okur Sorularını Tahmin Et

Okurların bu belgeyi bulmaya çalışırken hangi soruları sorabileceğini tahmin etme niyetini duyur.

Okurların gerçekçi olarak sorabileceği 5-10 soru üret.

### 2. Adım: Alt Ajanla Test Et

Bu soruların yeni bir Claude örneğiyle (bu sohbetten hiçbir bağlam taşımadan) test edileceğini duyur.

Her soru için yalnızca belge içeriği ve soruyla bir alt ajan çağır.

Okur Claude'un her soruda neyi doğru, neyi yanlış yaptığını özetle.

### 3. Adım: Ek Kontrolleri Çalıştır

Ek kontroller yapılacağını duyur.

Belirsizlik, yanlış varsayımlar ve çelişkileri kontrol etmesi için bir alt ajan çağır.

Bulunan sorunları özetle.

### 4. Adım: Raporla ve Düzelt

Sorun bulunursa:
Okur Claude'un belirli konularda zorlandığını bildir.

Belirli sorunları listele.

Bu boşlukları düzeltme niyetini belirt.

Sorunlu bölümler için iyileştirme aşamasına geri dön.

---

**Alt ajanlara erişim yoksa (ör. claude.ai web arayüzü):**

Testi kullanıcının elle yapması gerekecek.

### 1. Adım: Okur Sorularını Tahmin Et

İnsanların bu belgeyi bulmaya çalışırken hangi soruları sorabileceğini sor. Claude.ai'a ne yazarlardı?

Okurların gerçekçi olarak sorabileceği 5-10 soru üret.

### 2. Adım: Testi Hazırla

Test talimatlarını ver:
1. Yeni bir Claude sohbeti aç: https://claude.ai
2. Belge içeriğini yapıştır ya da paylaş (bağlayıcıları etkin, paylaşılan bir belge platformu kullanılıyorsa bağlantıyı ver)
3. Okur Claude'a üretilen soruları sor

Her soru için Okur Claude'dan şunları vermesini iste:
- Yanıt
- Belirsiz ya da anlaşılmaz bir şey olup olmadığı
- Belgenin hangi bilgi/bağlamın zaten bilindiğini varsaydığı

Okur Claude'un doğru yanıt verip vermediğini ya da bir şeyi yanlış yorumlayıp yorumlamadığını kontrol et.

### 3. Adım: Ek Kontroller

Okur Claude'a şunları da sor:
- "Bu belgede okurlar için belirsiz ya da anlaşılmaz olabilecek ne var?"
- "Bu belge okurların hangi bilgi ya da bağlama zaten sahip olduğunu varsayıyor?"
- "Belgede iç çelişkiler ya da tutarsızlıklar var mı?"

### 4. Adım: Sonuçlara Göre Yinele

Okur Claude'un neyi yanlış yaptığını ya da nerede zorlandığını sor. Bu boşlukları düzeltme niyetini belirt.

Sorunlu bölümler için iyileştirme aşamasına geri dön.

---

### Çıkış Koşulu (İki Yaklaşım İçin de)

Okur Claude soruları tutarlı biçimde doğru yanıtladığında ve yeni boşluk ya da belirsizlik ortaya çıkarmadığında belge hazırdır.

## Son Gözden Geçirme

Okur Testi geçildiğinde:
Belgenin Okur Claude testini geçtiğini duyur. Tamamlamadan önce:

1. Son bir okumayı kendilerinin yapmasını öner — belgenin sahibi onlardır ve kalitesinden onlar sorumludur
2. Olguları, bağlantıları ya da teknik ayrıntıları bir kez daha kontrol etmelerini öner
3. Belgenin istedikleri etkiyi sağlayıp sağlamadığını doğrulamalarını iste

Bir gözden geçirme daha isteyip istemediklerini ya da işin bitip bitmediğini sor.

**Kullanıcı son gözden geçirme isterse yap. İstemezse:**
Belgenin tamamlandığını duyur. Birkaç son ipucu ver:
- Okurların belgenin nasıl geliştirildiğini görebilmesi için bu sohbetin bağlantısını bir ekte vermeyi düşün
- Ana belgeyi şişirmeden derinlik sağlamak için ekleri kullan
- Gerçek okurlardan geri bildirim geldikçe belgeyi güncelle

## Etkili Rehberlik İçin İpuçları

**Üslup:**
- Doğrudan ve yöntemli ol
- Kullanıcının davranışını etkilediğinde gerekçeyi kısaca açıkla
- Yaklaşımı "satmaya" çalışma — yalnızca uygula

**Sapmaları Ele Alma:**
- Kullanıcı bir aşamayı atlamak isterse: Bunu atlayıp serbest yazmak isteyip istemediklerini sor
- Kullanıcı bunalmış görünüyorsa: Bunun beklenenden uzun sürdüğünü kabul et. Daha hızlı ilerlemenin yollarını öner
- Süreci ayarlama yetkisini her zaman kullanıcıya bırak

**Bağlam Yönetimi:**
- Süreç boyunca, söz edilen bir konuda bağlam eksikse proaktif olarak sor
- Boşlukların birikmesine izin verme — ortaya çıktıkça ele al

**Artifact Yönetimi:**
- Bölümlerin tamamını taslak olarak yazmak için `create_file` kullan
- Bütün düzenlemeler için `str_replace` kullan
- Her değişiklikten sonra artifact bağlantısını ver
- Beyin fırtınası listeleri için asla artifact kullanma — onlar yalnızca sohbettir

**Hızdan Önce Kalite:**
- Aşamalarda acele etme
- Her yineleme anlamlı iyileştirmeler getirmeli
- Amaç, okurlar için gerçekten işe yarayan bir belgedir
