
# Skill Oluşturucu

Yeni skill'ler oluşturmak ve onları yinelemeli olarak iyileştirmek için bir skill.

Genel hatlarıyla bir skill oluşturma süreci şöyle ilerler:

- Skill'in ne yapmasını istediğinize ve bunu kabaca nasıl yapması gerektiğine karar verin
- Skill'in bir taslağını yazın
- Birkaç test prompt'u hazırlayın ve bunları skill'e erişimi olan bir Claude ile çalıştırın
- Kullanıcının sonuçları hem nitel hem nicel olarak değerlendirmesine yardım edin
  - Çalıştırmalar arka planda sürerken, henüz yoksa birkaç nicel değerlendirme (eval) taslağı hazırlayın (varsa olduğu gibi kullanabilir ya da değişmesi gereken bir şey olduğunu düşünüyorsanız düzenleyebilirsiniz). Sonra bunları kullanıcıya açıklayın (ya da zaten varsa, mevcut olanları açıklayın)
  - Sonuçları kullanıcının incelemesi için göstermek ve nicel metriklere de bakabilmesini sağlamak üzere `eval-viewer/generate_review.py` betiğini kullanın
- Kullanıcının sonuçlara ilişkin değerlendirmesinden gelen geri bildirime (ve nicel karşılaştırmalı ölçümlerden göze batan bariz kusurlar çıkarsa onlara) göre skill'i yeniden yazın
- Memnun kalana kadar tekrarlayın
- Test kümesini genişletin ve daha büyük ölçekte yeniden deneyin

Bu skill'i kullanırken işiniz, kullanıcının bu süreçte nerede olduğunu anlamak ve devreye girip bu aşamalarda ilerlemesine yardım etmektir. Örneğin kullanıcı "X için bir skill yapmak istiyorum" diyebilir. Ne demek istediğini netleştirmesine yardım edebilir, bir taslak yazabilir, test senaryolarını yazabilir, nasıl değerlendirmek istediğini belirleyebilir, bütün prompt'ları çalıştırabilir ve süreci tekrarlayabilirsiniz.

Öte yandan kullanıcının elinde zaten bir skill taslağı olabilir. Bu durumda doğrudan döngünün değerlendirme/yineleme kısmına geçebilirsiniz.

Elbette her zaman esnek olmalısınız; kullanıcı "Bir sürü değerlendirme çalıştırmama gerek yok, sadece benimle birlikte akışına bırak" derse onun yerine bunu yapabilirsiniz.

Ardından skill bittikten sonra (ama yine, sıra esnektir) skill'in tetiklenmesini iyileştirmek için ayrı bir betiğimizin bulunduğu skill açıklaması iyileştiricisini de çalıştırabilirsiniz.

Tamam mı? Tamam.

## Kullanıcıyla iletişim

Skill oluşturucuyu, kodlama jargonuna aşinalık düzeyi çok farklı olan kişiler kullanabilir. Duymadıysanız (nasıl duyacaksınız ki, daha çok yeni başladı), şu sıralar Claude'un gücünün tesisatçılara terminallerini açma, anne babalara ve büyükanne büyükbabalara "npm nasıl kurulur" diye Google'da arama yapma ilhamı verdiği bir akım var. Öte yandan kullanıcıların büyük kısmı muhtemelen bilgisayar konusunda oldukça yetkin.

Bu yüzden lütfen iletişiminizi nasıl ifade edeceğinizi anlamak için bağlamdaki ipuçlarına dikkat edin! Varsayılan durumda, size biraz fikir vermesi için:

- "evaluation" (değerlendirme) ve "benchmark" (karşılaştırmalı ölçüm) sınırda ama kabul edilebilir
- "JSON" ve "assertion" (doğrulama ifadesi) için, bunları açıklamadan kullanmadan önce kullanıcının bu kavramları bildiğine dair ciddi ipuçları görmek istersiniz

Emin değilseniz terimleri kısaca açıklamanızda sakınca yok; kullanıcının anlayıp anlamayacağından emin olmadığınız terimleri kısa bir tanımla açıklamaktan çekinmeyin.

---

## Bir skill oluşturma

### Amacı Yakalama

Kullanıcının amacını anlayarak başlayın. Mevcut konuşma, kullanıcının yakalamak istediği bir iş akışını zaten içeriyor olabilir (ör. "bunu bir skill'e dönüştür" der). Öyleyse yanıtları önce konuşma geçmişinden çıkarın — kullanılan araçlar, adımların sırası, kullanıcının yaptığı düzeltmeler, gözlemlenen girdi/çıktı biçimleri. Boşlukları kullanıcının doldurması gerekebilir ve bir sonraki adıma geçmeden önce onay vermelidir.

1. Bu skill Claude'un ne yapabilmesini sağlamalı?
2. Bu skill ne zaman tetiklenmeli? (hangi kullanıcı ifadeleri/bağlamlarda)
3. Beklenen çıktı biçimi nedir?
4. Skill'in çalıştığını doğrulamak için test senaryoları kuralım mı? Nesnel olarak doğrulanabilir çıktıları olan skill'ler (dosya dönüştürme, veri çıkarma, kod üretme, sabit iş akışı adımları) test senaryolarından fayda görür. Öznel çıktıları olan skill'lerin (yazım üslubu, sanat) çoğu zaman bunlara ihtiyacı olmaz. Skill türüne göre uygun varsayılanı önerin, ama kararı kullanıcıya bırakın.

### Görüşme ve Araştırma

Uç durumlar, girdi/çıktı biçimleri, örnek dosyalar, başarı ölçütleri ve bağımlılıklar hakkında proaktif olarak sorular sorun. Bu kısmı netleştirene kadar test prompt'larını yazmayı bekleyin.

Mevcut MCP'leri kontrol edin — araştırma için işe yarıyorsa (belgelerde arama, benzer skill'leri bulma, en iyi uygulamalara bakma), mümkünse alt ajanlarla paralel, değilse satır içinde araştırın. Kullanıcının yükünü azaltmak için bağlamı önceden hazırlamış olarak gelin.

### SKILL.md'yi Yazma

Kullanıcıyla yapılan görüşmeye dayanarak şu bileşenleri doldurun:

- **name**: Skill tanımlayıcısı
- **description**: Ne zaman tetikleneceği, ne yaptığı. Bu, birincil tetikleme mekanizmasıdır — hem skill'in ne yaptığını HEM DE ne zaman kullanılacağına dair belirli bağlamları içermelidir. "Ne zaman kullanılır" bilgisinin tamamı gövdeye değil buraya yazılır. Not: Şu anda Claude'un skill'leri "yetersiz tetikleme" eğilimi var — yani yararlı olacakları durumlarda kullanmamak. Buna karşı koymak için lütfen skill açıklamalarını biraz "ısrarcı" yazın. Örneğin "Anthropic'in iç verilerini göstermek için basit ve hızlı bir gösterge paneli nasıl yapılır." yerine "Anthropic'in iç verilerini göstermek için basit ve hızlı bir gösterge paneli nasıl yapılır. Kullanıcı gösterge panellerinden, veri görselleştirmeden, iç metriklerden bahsettiğinde ya da açıkça 'gösterge paneli' istemese bile herhangi bir şirket verisini göstermek istediğinde bu skill'i mutlaka kullanın." yazabilirsiniz.
- **compatibility**: Gerekli araçlar, bağımlılıklar (isteğe bağlı, nadiren gerekir)
- **skill'in geri kalanı :)**

### Skill Yazım Rehberi

#### Bir Skill'in Anatomisi

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter (name, description required)
│   └── Markdown instructions
└── Bundled Resources (optional)
    ├── scripts/    - Executable code for deterministic/repetitive tasks
    ├── references/ - Docs loaded into context as needed
    └── assets/     - Files used in output (templates, icons, fonts)
```

#### Aşamalı Açıklama

Skill'ler üç seviyeli bir yükleme sistemi kullanır:
1. **Üst veri** (name + description) - Her zaman bağlamdadır (~100 kelime)
2. **SKILL.md gövdesi** - Skill her tetiklendiğinde bağlamdadır (ideali <500 satır)
3. **Paketlenmiş kaynaklar** - Gerektikçe (sınırsız; betikler yüklenmeden çalıştırılabilir)

Bu kelime sayıları yaklaşıktır; gerekirse rahatça daha uzun yazabilirsiniz.

**Temel kalıplar:**
- SKILL.md'yi 500 satırın altında tutun; bu sınıra yaklaşıyorsanız, skill'i kullanan modelin devam etmek için bir sonraki adımda nereye gitmesi gerektiğine dair açık yönlendirmelerle birlikte ek bir hiyerarşi katmanı ekleyin.
- Referans dosyalarına SKILL.md'den, ne zaman okunmaları gerektiğine dair yönlendirmeyle açıkça atıf yapın
- Büyük referans dosyaları (>300 satır) için bir içindekiler tablosu ekleyin

**Alan bazlı düzenleme**: Bir skill birden çok alanı/çerçeveyi destekliyorsa, varyanta göre düzenleyin:
```
cloud-deploy/
├── SKILL.md (workflow + selection)
└── references/
    ├── aws.md
    ├── gcp.md
    └── azure.md
```
Claude yalnızca ilgili referans dosyasını okur.

#### Sürpriz Olmaması İlkesi

Söylemeye gerek yok ama skill'ler kötü amaçlı yazılım, istismar kodu ya da sistem güvenliğini tehlikeye atabilecek herhangi bir içerik barındırmamalıdır. Bir skill'in içeriği, anlatıldığında amacı bakımından kullanıcıyı şaşırtmamalıdır. Yanıltıcı skill'ler ya da yetkisiz erişimi, veri sızdırmayı veya diğer kötü amaçlı faaliyetleri kolaylaştırmak için tasarlanmış skill'ler oluşturma isteklerine uymayın. Yine de "XYZ rolüne bürün" gibi şeyler sorun değildir.

#### Yazım Kalıpları

Talimatlarda emir kipini tercih edin.

**Çıktı biçimlerini tanımlama** - Bunu şöyle yapabilirsiniz:
```markdown
## Report structure
ALWAYS use this exact template:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

**Örnek kalıbı** - Örnek eklemek yararlıdır. Örnekleri şöyle biçimlendirebilirsiniz (ama örneklerde "Input" ve "Output" geçiyorsa biraz farklılaştırmak isteyebilirsiniz):
```markdown
## Commit message format
**Example 1:**
Input: Added user authentication with JWT tokens
Output: feat(auth): implement JWT-based authentication
```

### Yazım Üslubu

Ağır ve bayat MUTLAKA'lar yerine, modele bir şeylerin neden önemli olduğunu açıklamaya çalışın. Zihin kuramından yararlanın ve skill'i belirli örneklere aşırı dar biçimde bağlamak yerine genel tutmaya çalışın. Önce bir taslak yazın, sonra ona taze gözlerle bakıp iyileştirin.

### Test Senaryoları

Skill taslağını yazdıktan sonra 2-3 gerçekçi test prompt'u bulun — gerçek bir kullanıcının gerçekten söyleyeceği türden şeyler. Bunları kullanıcıyla paylaşın: [tam olarak bu ifadeyi kullanmanız gerekmez] "Denemek istediğim birkaç test senaryosu şunlar. Bunlar doğru görünüyor mu, yoksa başka eklemek ister misiniz?" Sonra bunları çalıştırın.

Test senaryolarını `evals/evals.json` dosyasına kaydedin. Henüz assertion yazmayın — yalnızca prompt'ları yazın. Assertion'ların taslağını, çalıştırmalar sürerken bir sonraki adımda hazırlayacaksınız.

```json
{
  "skill_name": "example-skill",
  "evals": [
    {
      "id": 1,
      "prompt": "User's task prompt",
      "expected_output": "Description of expected result",
      "files": []
    }
  ]
}
```

Tam şema için (daha sonra ekleyeceğiniz `assertions` alanı dahil) `references/schemas.md` dosyasına bakın.

## Test senaryolarını çalıştırma ve değerlendirme

Bu bölüm kesintisiz tek bir sıradır — yarıda durmayın. `/skill-test` ya da başka herhangi bir test skill'ini KULLANMAYIN.

Sonuçları, skill dizininin kardeşi olarak `<skill-name>-workspace/` içine koyun. Çalışma alanında sonuçları yinelemeye göre (`iteration-1/`, `iteration-2/` vb.) düzenleyin ve bunun içinde her test senaryosuna bir dizin (`eval-0/`, `eval-1/` vb.) verin. Bunların hepsini baştan oluşturmayın — dizinleri ilerledikçe oluşturun.

### Adım 1: Bütün çalıştırmaları (skill'li VE temel) aynı turda başlatın

Her test senaryosu için aynı turda iki alt ajan başlatın — biri skill'le, biri skill'siz. Bu önemli: önce skill'li çalıştırmaları başlatıp temel (baseline) çalıştırmalara sonra dönmeyin. Her şeyi aynı anda başlatın ki hepsi aşağı yukarı aynı anda bitsin.

**Skill'li çalıştırma:**

```
Execute this task:
- Skill path: <path-to-skill>
- Task: <eval prompt>
- Input files: <eval files if any, or "none">
- Save outputs to: <workspace>/iteration-<N>/eval-<ID>/with_skill/outputs/
- Outputs to save: <what the user cares about — e.g., "the .docx file", "the final CSV">
```

**Temel çalıştırma** (aynı prompt, ama temelin ne olacağı bağlama bağlıdır):
- **Yeni bir skill oluşturuluyorsa**: hiç skill yok. Aynı prompt, skill yolu yok, `without_skill/outputs/` içine kaydedin.
- **Mevcut bir skill iyileştiriliyorsa**: eski sürüm. Düzenlemeden önce skill'in anlık görüntüsünü alın (`cp -r <skill-path> <workspace>/skill-snapshot/`), sonra temel alt ajanı bu anlık görüntüye yönlendirin. `old_skill/outputs/` içine kaydedin.

Her test senaryosu için bir `eval_metadata.json` yazın (assertion'lar şimdilik boş olabilir). Her değerlendirmeye, neyi test ettiğine dayanan açıklayıcı bir ad verin — yalnızca "eval-0" değil. Bu adı dizin için de kullanın. Bu yineleme yeni ya da değiştirilmiş değerlendirme prompt'ları kullanıyorsa, bu dosyaları her yeni değerlendirme dizini için oluşturun — önceki yinelemelerden aktarıldıklarını varsaymayın.

```json
{
  "eval_id": 0,
  "eval_name": "descriptive-name-here",
  "prompt": "The user's task prompt",
  "assertions": []
}
```

### Adım 2: Çalıştırmalar sürerken assertion taslaklarını hazırlayın

Yalnızca çalıştırmaların bitmesini beklemeyin — bu süreyi verimli kullanabilirsiniz. Her test senaryosu için nicel assertion taslakları hazırlayın ve bunları kullanıcıya açıklayın. `evals/evals.json` içinde zaten assertion'lar varsa, onları gözden geçirin ve neyi kontrol ettiklerini açıklayın.

İyi assertion'lar nesnel olarak doğrulanabilir ve açıklayıcı adlara sahiptir — karşılaştırmalı ölçüm görüntüleyicisinde açıkça okunmalılar ki sonuçlara göz atan biri her birinin neyi kontrol ettiğini hemen anlasın. Öznel skill'ler (yazım üslubu, tasarım kalitesi) nitel olarak daha iyi değerlendirilir — insan yargısı gerektiren şeylere zorla assertion dayatmayın.

Taslakları hazırladıktan sonra `eval_metadata.json` dosyalarını ve `evals/evals.json` dosyasını assertion'larla güncelleyin. Ayrıca kullanıcıya görüntüleyicide neler göreceğini açıklayın — hem nitel çıktıları hem nicel karşılaştırmalı ölçümü.

### Adım 3: Çalıştırmalar tamamlandıkça zamanlama verilerini kaydedin

Her alt ajan görevi tamamlandığında `total_tokens` ve `duration_ms` içeren bir bildirim alırsınız. Bu verileri hemen çalıştırma dizinindeki `timing.json` dosyasına kaydedin:

```json
{
  "total_tokens": 84852,
  "duration_ms": 23332,
  "total_duration_seconds": 23.3
}
```

Bu verileri yakalamak için tek fırsat budur — görev bildirimiyle gelir ve başka hiçbir yerde saklanmaz. Bildirimleri toplu işlemeye çalışmak yerine her birini geldiği anda işleyin.

### Adım 4: Notlandırın, birleştirin ve görüntüleyiciyi başlatın

Bütün çalıştırmalar bittiğinde:

1. **Her çalıştırmayı notlandırın** — `agents/grader.md` dosyasını okuyan ve her assertion'ı çıktılara göre değerlendiren bir notlandırıcı alt ajan başlatın (ya da satır içinde notlandırın). Sonuçları her çalıştırma dizinindeki `grading.json` dosyasına kaydedin. grading.json'daki expectations dizisi `text`, `passed` ve `evidence` alanlarını kullanmalıdır (`name`/`met`/`details` ya da başka varyantları değil) — görüntüleyici tam olarak bu alan adlarına dayanır. Programla kontrol edilebilen assertion'lar için göz kararı bakmak yerine bir betik yazıp çalıştırın — betikler daha hızlı, daha güvenilirdir ve yinelemeler arasında yeniden kullanılabilir.

2. **Karşılaştırmalı ölçümde birleştirin** — birleştirme betiğini skill-creator dizininden çalıştırın:
   ```bash
   python -m scripts.aggregate_benchmark <workspace>/iteration-N --skill-name <name>
   ```
   Bu, her yapılandırma için pass_rate, süre ve token değerlerini ortalama ± standart sapma ve farkla birlikte içeren `benchmark.json` ve `benchmark.md` dosyalarını üretir. benchmark.json'u elle üretiyorsanız, görüntüleyicinin beklediği tam şema için `references/schemas.md` dosyasına bakın.
Her with_skill sürümünü temel karşılığından önce koyun.

3. **Bir analist taraması yapın** — karşılaştırmalı ölçüm verilerini okuyun ve toplu istatistiklerin gizleyebileceği örüntüleri ortaya çıkarın. Nelere bakmanız gerektiği için `agents/analyzer.md` dosyasına ("Analyzing Benchmark Results" bölümü) bakın — skill'den bağımsız olarak her zaman geçen assertion'lar (ayırt edici olmayanlar), yüksek varyanslı değerlendirmeler (muhtemelen kararsız) ve süre/token ödünleşimleri gibi şeyler.

4. **Görüntüleyiciyi** hem nitel çıktılar hem nicel verilerle **başlatın**:
   ```bash
   nohup python <skill-creator-path>/eval-viewer/generate_review.py \
     <workspace>/iteration-N \
     --skill-name "my-skill" \
     --benchmark <workspace>/iteration-N/benchmark.json \
     > /dev/null 2>&1 &
   VIEWER_PID=$!
   ```
   2. ve sonraki yinelemeler için ayrıca `--previous-workspace <workspace>/iteration-<N-1>` verin.

   **Cowork / başsız (headless) ortamlar:** `webbrowser.open()` kullanılamıyorsa ya da ortamda ekran yoksa, sunucu başlatmak yerine bağımsız bir HTML dosyası yazmak için `--static <output_path>` kullanın. Kullanıcı "Submit All Reviews" düğmesine tıkladığında geri bildirim bir `feedback.json` dosyası olarak indirilir. İndirdikten sonra, bir sonraki yinelemenin alabilmesi için `feedback.json` dosyasını çalışma alanı dizinine kopyalayın.

Not: Görüntüleyiciyi oluşturmak için lütfen generate_review.py'yi kullanın; özel HTML yazmaya gerek yok.

5. **Kullanıcıya** şuna benzer bir şey **söyleyin**: "Sonuçları tarayıcınızda açtım. İki sekme var — 'Outputs' her test senaryosuna tıklayarak geçmenizi ve geri bildirim bırakmanızı sağlar, 'Benchmark' nicel karşılaştırmayı gösterir. İşiniz bitince buraya dönüp bana haber verin."

### Kullanıcının görüntüleyicide gördükleri

"Outputs" sekmesi her seferinde bir test senaryosu gösterir:
- **Prompt**: verilen görev
- **Output**: skill'in ürettiği dosyalar, mümkün olduğunda satır içinde görüntülenir
- **Previous Output** (2. ve sonraki yinelemeler): önceki yinelemenin çıktısını gösteren daraltılmış bölüm
- **Formal Grades** (notlandırma yapıldıysa): assertion geçti/kaldı sonuçlarını gösteren daraltılmış bölüm
- **Feedback**: yazdıkça kendiliğinden kaydedilen bir metin kutusu
- **Previous Feedback** (2. ve sonraki yinelemeler): metin kutusunun altında gösterilen, önceki seferki yorumları

"Benchmark" sekmesi istatistik özetini gösterir: her yapılandırma için geçme oranları, süre ve token kullanımı; değerlendirme bazında dökümler ve analist gözlemleriyle birlikte.

Gezinme önceki/sonraki düğmeleri ya da ok tuşlarıyla yapılır. İşleri bitince bütün geri bildirimleri `feedback.json` dosyasına kaydeden "Submit All Reviews" düğmesine tıklarlar.

### Adım 5: Geri bildirimi okuyun

Kullanıcı işinin bittiğini söylediğinde `feedback.json` dosyasını okuyun:

```json
{
  "reviews": [
    {"run_id": "eval-0-with_skill", "feedback": "the chart is missing axis labels", "timestamp": "..."},
    {"run_id": "eval-1-with_skill", "feedback": "", "timestamp": "..."},
    {"run_id": "eval-2-with_skill", "feedback": "perfect, love this", "timestamp": "..."}
  ],
  "status": "complete"
}
```

Boş geri bildirim, kullanıcının sonucu iyi bulduğu anlamına gelir. İyileştirmelerinizi kullanıcının belirli şikâyetleri olduğu test senaryolarına odaklayın.

İşiniz bitince görüntüleyici sunucusunu kapatın:

```bash
kill $VIEWER_PID 2>/dev/null
```

---

## Skill'i iyileştirme

Döngünün kalbi burasıdır. Test senaryolarını çalıştırdınız, kullanıcı sonuçları inceledi ve şimdi onun geri bildirimine göre skill'i daha iyi hâle getirmeniz gerekiyor.

### İyileştirmeler hakkında nasıl düşünülür

1. **Geri bildirimden genelleme yapın.** Burada olan şeyin büyük resmi şu: birçok farklı prompt'ta milyon kez (belki gerçekten, belki daha da fazla, kim bilir) kullanılabilecek skill'ler oluşturmaya çalışıyoruz. Burada siz ve kullanıcı yalnızca birkaç örnek üzerinde tekrar tekrar yineleme yapıyorsunuz çünkü bu daha hızlı ilerlemeye yardım ediyor. Kullanıcı bu örnekleri en ince ayrıntısına kadar biliyor ve yeni çıktıları değerlendirmesi hızlı oluyor. Ama sizin ve kullanıcının birlikte geliştirdiği skill yalnızca bu örneklerde çalışıyorsa işe yaramaz. Kılı kırk yaran, örneklere aşırı uyan değişiklikler ya da boğucu derecede kısıtlayıcı MUTLAKA'lar eklemek yerine, inatçı bir sorun varsa, farklı metaforlar kullanmayı ya da farklı çalışma kalıpları önermeyi deneyebilirsiniz. Denemesi görece ucuz ve belki harika bir şey bulursunuz.

2. **Prompt'u yalın tutun.** Hakkını vermeyen şeyleri çıkarın. Yalnızca nihai çıktıları değil, transkriptleri de okuduğunuzdan emin olun — skill'in modele verimsiz şeylerle bir sürü zaman harcattığı görünüyorsa, skill'in buna yol açan kısımlarını çıkarmayı deneyip ne olduğunu görebilirsiniz.

3. **Nedenini açıklayın.** Modelden yapmasını istediğiniz her şeyin arkasındaki **nedeni** açıklamak için gerçekten çaba gösterin. Günümüzün LLM'leri *zeki*. İyi bir zihin kuramına sahipler ve iyi bir düzenekle donatıldıklarında ezbere talimatların ötesine geçip gerçekten işleri yürütebilirler. Kullanıcıdan gelen geri bildirim kısa ya da sinirli olsa bile, görevi ve kullanıcının yazdığını neden yazdığını, gerçekte ne yazdığını anlamaya çalışın ve sonra bu anlayışı talimatlara aktarın. Kendinizi büyük harflerle HER ZAMAN ya da ASLA yazarken ya da aşırı katı yapılar kullanırken bulursanız, bu bir sarı bayraktır — mümkünse yeniden çerçeveleyin ve gerekçeyi açıklayın ki model istediğiniz şeyin neden önemli olduğunu anlasın. Bu daha insani, daha güçlü ve daha etkili bir yaklaşımdır.

4. **Test senaryoları arasında tekrarlanan işlere bakın.** Test çalıştırmalarının transkriptlerini okuyun ve alt ajanların hepsinin birbirinden bağımsız olarak benzer yardımcı betikler yazıp yazmadığını ya da bir şey için aynı çok adımlı yaklaşımı izleyip izlemediğini fark edin. 3 test senaryosunun hepsinde alt ajan bir `create_docx.py` ya da `build_chart.py` yazdıysa, bu skill'in o betiği paketlemesi gerektiğine dair güçlü bir işarettir. Betiği bir kez yazın, `scripts/` içine koyun ve skill'e onu kullanmasını söyleyin. Bu, gelecekteki her çağrıyı tekerleği yeniden icat etmekten kurtarır.

Bu görev oldukça önemli (burada yılda milyarlarca dolarlık ekonomik değer yaratmaya çalışıyoruz!) ve düşünme süreniz darboğaz değil; acele etmeyin ve konuları gerçekten iyice düşünün. Bir revizyon taslağı yazıp sonra ona yeniden bakmanızı ve iyileştirmeler yapmanızı öneririm. Kullanıcının kafasının içine girmek ve ne istediğini, neye ihtiyaç duyduğunu anlamak için gerçekten elinizden geleni yapın.

### Yineleme döngüsü

Skill'i iyileştirdikten sonra:

1. İyileştirmelerinizi skill'e uygulayın
2. Temel çalıştırmalar dahil bütün test senaryolarını yeni bir `iteration-<N+1>/` dizinine yeniden çalıştırın. Yeni bir skill oluşturuyorsanız temel her zaman `without_skill`'dir (skill yok) — bu, yinelemeler boyunca aynı kalır. Mevcut bir skill'i iyileştiriyorsanız temel olarak neyin mantıklı olduğuna kendi muhakemenizle karar verin: kullanıcının getirdiği özgün sürüm mü, yoksa önceki yineleme mi.
3. İnceleme aracını önceki yinelemeyi gösteren `--previous-workspace` ile başlatın
4. Kullanıcının incelemesini ve işinin bittiğini söylemesini bekleyin
5. Yeni geri bildirimi okuyun, yeniden iyileştirin, tekrarlayın

Şunlardan biri olana kadar devam edin:
- Kullanıcı memnun olduğunu söyler
- Geri bildirimlerin hepsi boştur (her şey iyi görünüyor)
- Anlamlı bir ilerleme kaydetmiyorsunuzdur

---

## İleri düzey: Kör karşılaştırma

Bir skill'in iki sürümü arasında daha titiz bir karşılaştırma istediğiniz durumlar için (ör. kullanıcı "yeni sürüm gerçekten daha mı iyi?" diye sorar) bir kör karşılaştırma sistemi vardır. Ayrıntılar için `agents/comparator.md` ve `agents/analyzer.md` dosyalarını okuyun. Temel fikir şu: iki çıktıyı hangisinin hangisi olduğunu söylemeden bağımsız bir ajana verin ve kaliteyi onun değerlendirmesine bırakın. Sonra kazananın neden kazandığını analiz edin.

Bu isteğe bağlıdır, alt ajan gerektirir ve çoğu kullanıcının buna ihtiyacı olmaz. İnsan inceleme döngüsü genellikle yeterlidir.

---

## Açıklama Optimizasyonu

SKILL.md frontmatter'ındaki description alanı, Claude'un bir skill'i çağırıp çağırmayacağını belirleyen birincil mekanizmadır. Bir skill'i oluşturduktan ya da iyileştirdikten sonra, daha doğru tetikleme için açıklamayı optimize etmeyi önerin.

### Adım 1: Tetikleme değerlendirme sorgularını üretin

Tetiklemesi gereken ve tetiklememesi gereken sorgulardan oluşan karışık 20 değerlendirme sorgusu oluşturun. JSON olarak kaydedin:

```json
[
  {"query": "the user prompt", "should_trigger": true},
  {"query": "another prompt", "should_trigger": false}
]
```

Sorgular gerçekçi olmalı ve bir Claude Code ya da Claude.ai kullanıcısının gerçekten yazacağı türden olmalıdır. Soyut istekler değil; somut, belirli ve bol ayrıntılı istekler. Örneğin dosya yolları, kullanıcının işi ya da durumu hakkında kişisel bağlam, sütun adları ve değerleri, şirket adları, URL'ler. Biraz arka plan hikâyesi. Bazıları küçük harfle yazılmış olabilir ya da kısaltmalar, yazım hataları veya gündelik konuşma dili içerebilir. Farklı uzunluklarda bir karışım kullanın ve net, kesin durumlar yerine uç durumlara odaklanın (kullanıcı bunları onaylama fırsatı bulacak).

Kötü: `"Format this data"`, `"Extract text from PDF"`, `"Create a chart"`

İyi: `"ok so my boss just sent me this xlsx file (its in my downloads, called something like 'Q4 sales final FINAL v2.xlsx') and she wants me to add a column that shows the profit margin as a percentage. The revenue is in column C and costs are in column D i think"`

**Tetiklemesi gereken** sorgular (8-10) için kapsamı düşünün. Aynı amacın farklı ifadelerini istersiniz — bazıları resmî, bazıları gündelik. Kullanıcının skill'in ya da dosya türünün adını açıkça anmadığı ama açıkça ona ihtiyaç duyduğu durumları da ekleyin. Birkaç alışılmadık kullanım durumu ve bu skill'in başka bir skill'le yarıştığı ama kazanması gereken durumlar da katın.

**Tetiklememesi gereken** sorgular (8-10) için en değerli olanlar kıl payı kaçanlardır — skill'le anahtar kelimeleri ya da kavramları paylaşan ama aslında farklı bir şeye ihtiyaç duyan sorgular. Komşu alanları, safça anahtar kelime eşleştirmenin tetikleyeceği ama tetiklememesi gereken belirsiz ifadeleri ve sorgunun skill'in yaptığı bir şeye değindiği ama başka bir aracın daha uygun olduğu bağlamları düşünün.

Kaçınılması gereken temel şey: tetiklememesi gereken sorguları bariz biçimde alakasız yapmayın. Bir PDF skill'i için olumsuz test olarak "Bir fibonacci fonksiyonu yaz" fazla kolaydır — hiçbir şeyi test etmez. Olumsuz durumlar gerçekten yanıltıcı olmalıdır.

### Adım 2: Kullanıcıyla gözden geçirin

Değerlendirme kümesini HTML şablonunu kullanarak kullanıcının incelemesine sunun:

1. Şablonu `assets/eval_review.html` dosyasından okuyun
2. Yer tutucuları değiştirin:
   - `__EVAL_DATA_PLACEHOLDER__` → değerlendirme öğelerinin JSON dizisi (etrafında tırnak yok — bu bir JS değişken ataması)
   - `__SKILL_NAME_PLACEHOLDER__` → skill'in adı
   - `__SKILL_DESCRIPTION_PLACEHOLDER__` → skill'in mevcut açıklaması
3. Geçici bir dosyaya yazın (ör. `/tmp/eval_review_<skill-name>.html`) ve açın: `open /tmp/eval_review_<skill-name>.html`
4. Kullanıcı sorguları düzenleyebilir, should-trigger değerini değiştirebilir, öğe ekleyip çıkarabilir, sonra "Export Eval Set" düğmesine tıklar
5. Dosya `~/Downloads/eval_set.json` konumuna iner — birden fazla sürüm olması ihtimaline karşı (ör. `eval_set (1).json`) Downloads klasöründe en yeni sürümü kontrol edin

Bu adım önemlidir — kötü değerlendirme sorguları kötü açıklamalara yol açar.

### Adım 3: Optimizasyon döngüsünü çalıştırın

Kullanıcıya şunu söyleyin: "Bu biraz zaman alacak — optimizasyon döngüsünü arka planda çalıştıracağım ve düzenli aralıklarla kontrol edeceğim."

Değerlendirme kümesini çalışma alanına kaydedin, sonra arka planda çalıştırın:

```bash
python -m scripts.run_loop \
  --eval-set <path-to-trigger-eval.json> \
  --skill-path <path-to-skill> \
  --model <model-id-powering-this-session> \
  --max-iterations 5 \
  --verbose
```

Tetikleme testinin kullanıcının gerçekte deneyimlediğiyle örtüşmesi için sistem prompt'unuzdaki model kimliğini (mevcut oturumu çalıştıran modelinkini) kullanın.

Çalışırken, kullanıcıya hangi yinelemede olunduğu ve puanların nasıl göründüğü hakkında güncel bilgi vermek için düzenli aralıklarla çıktının sonuna bakın.

Bu, bütün optimizasyon döngüsünü otomatik olarak yürütür. Değerlendirme kümesini %60 eğitim ve %40 ayrılmış test olarak böler, mevcut açıklamayı değerlendirir (güvenilir bir tetikleme oranı elde etmek için her sorguyu 3 kez çalıştırır), sonra başarısız olanlara dayanarak iyileştirme önermesi için Claude'u çağırır. Her yeni açıklamayı hem eğitim hem test kümesinde yeniden değerlendirir ve 5 kereye kadar yineler. Bittiğinde, yineleme başına sonuçları gösteren bir HTML raporunu tarayıcıda açar ve `best_description` içeren JSON döndürür — aşırı uyumu önlemek için eğitim puanına göre değil test puanına göre seçilir.

### Skill tetiklemesi nasıl çalışır

Tetikleme mekanizmasını anlamak daha iyi değerlendirme sorguları tasarlamaya yardım eder. Skill'ler Claude'un `available_skills` listesinde adları + açıklamalarıyla görünür ve Claude bir skill'e başvurup başvurmayacağına bu açıklamaya bakarak karar verir. Bilinmesi gereken önemli şey şu: Claude skill'lere yalnızca kendi başına kolayca halledemeyeceği görevler için başvurur — "bu PDF'i oku" gibi basit, tek adımlı sorgular, açıklama mükemmel eşleşse bile skill'i tetiklemeyebilir, çünkü Claude bunları temel araçlarla doğrudan halledebilir. Karmaşık, çok adımlı ya da uzmanlık gerektiren sorgular, açıklama eşleştiğinde skill'leri güvenilir biçimde tetikler.

Bu, değerlendirme sorgularınızın, Claude'un bir skill'e başvurmaktan gerçekten fayda göreceği kadar dolu olması gerektiği anlamına gelir. "X dosyasını oku" gibi basit sorgular kötü test senaryolarıdır — açıklamanın kalitesi ne olursa olsun skill'leri tetiklemezler.

### Adım 4: Sonucu uygulayın

JSON çıktısındaki `best_description` değerini alın ve skill'in SKILL.md frontmatter'ını güncelleyin. Kullanıcıya öncesini/sonrasını gösterin ve puanları bildirin.

---

### Paketleme ve Sunma (yalnızca `present_files` aracı varsa)

`present_files` aracına erişiminiz olup olmadığını kontrol edin. Yoksa bu adımı atlayın. Varsa skill'i paketleyin ve .skill dosyasını kullanıcıya sunun:

```bash
python -m scripts.package_skill <path/to/skill-folder>
```

Paketledikten sonra, kurabilmesi için kullanıcıyı oluşan `.skill` dosyasının yoluna yönlendirin.

---

## Claude.ai'ya özgü talimatlar

Claude.ai'da temel iş akışı aynıdır (taslak → test → inceleme → iyileştirme → tekrar), ama Claude.ai'da alt ajan olmadığı için bazı işleyişler değişir. Uyarlamanız gerekenler şunlar:

**Test senaryolarını çalıştırma**: Alt ajan olmaması paralel çalıştırma olmadığı anlamına gelir. Her test senaryosu için skill'in SKILL.md dosyasını okuyun, sonra test prompt'unu kendiniz gerçekleştirmek için talimatlarını izleyin. Senaryoları birer birer yapın. Bu, bağımsız alt ajanlardan daha az titizdir (skill'i siz yazdınız ve onu siz çalıştırıyorsunuz, yani bütün bağlam sizde), ama yararlı bir sağlamlık kontrolüdür — ve insan inceleme adımı bunu telafi eder. Temel çalıştırmaları atlayın — skill'i yalnızca görevi istendiği gibi tamamlamak için kullanın.

**Sonuçları inceleme**: Tarayıcı açamıyorsanız (ör. Claude.ai'ın sanal makinesinde ekran yoksa ya da uzak bir sunucudaysanız), tarayıcıdaki inceleme aracını tamamen atlayın. Bunun yerine sonuçları doğrudan konuşmada sunun. Her test senaryosu için prompt'u ve çıktıyı gösterin. Çıktı kullanıcının görmesi gereken bir dosyaysa (.docx ya da .xlsx gibi), dosya sistemine kaydedin ve indirip inceleyebilmesi için nerede olduğunu söyleyin. Geri bildirimi satır içinde isteyin: "Nasıl görünüyor? Değiştirmek istediğiniz bir şey var mı?"

**Karşılaştırmalı ölçüm**: Nicel karşılaştırmalı ölçümü atlayın — alt ajanlar olmadan anlamlı olmayan temel karşılaştırmalarına dayanır. Kullanıcıdan gelen nitel geri bildirime odaklanın.

**Yineleme döngüsü**: Öncekiyle aynı — skill'i iyileştirin, test senaryolarını yeniden çalıştırın, geri bildirim isteyin — yalnızca araya tarayıcıdaki inceleme aracı girmeden. Bir dosya sisteminiz varsa sonuçları yine yineleme dizinlerinde düzenleyebilirsiniz.

**Açıklama optimizasyonu**: Bu bölüm yalnızca Claude Code'da bulunan `claude` CLI aracını (özellikle `claude -p`) gerektirir. Claude.ai'daysanız atlayın.

**Kör karşılaştırma**: Alt ajan gerektirir. Atlayın.

**Paketleme**: `package_skill.py` betiği Python ve dosya sistemi olan her yerde çalışır. Claude.ai'da betiği çalıştırabilirsiniz ve kullanıcı oluşan `.skill` dosyasını indirebilir.

**Mevcut bir skill'i güncelleme**: Kullanıcı yeni bir skill oluşturmanızı değil, mevcut bir skill'i güncellemenizi istiyor olabilir. Bu durumda:
- **Özgün adı koruyun.** Skill'in dizin adını ve `name` frontmatter alanını not edin -- bunları değiştirmeden kullanın. Ör. kurulu skill `research-helper` ise çıktı `research-helper.skill` olmalı (`research-helper-v2` değil).
- **Düzenlemeden önce yazılabilir bir konuma kopyalayın.** Kurulu skill yolu salt okunur olabilir. `/tmp/skill-name/` konumuna kopyalayın, orada düzenleyin ve kopyadan paketleyin.
- **Elle paketliyorsanız önce `/tmp/` içinde hazırlayın**, sonra çıktı dizinine kopyalayın -- izinler nedeniyle doğrudan yazmalar başarısız olabilir.

---

## Cowork'e Özgü Talimatlar

Cowork'teyseniz bilmeniz gereken başlıca şeyler şunlar:

- Alt ajanlarınız var, yani ana iş akışı (test senaryolarını paralel başlatma, temel çalıştırmaları yürütme, notlandırma vb.) tamamen çalışır. (Yine de zaman aşımlarıyla ciddi sorunlar yaşarsanız test prompt'larını paralel yerine sırayla çalıştırmanızda sakınca yoktur.)
- Tarayıcınız ya da ekranınız yok; bu yüzden değerlendirme görüntüleyicisini oluştururken sunucu başlatmak yerine bağımsız bir HTML dosyası yazmak için `--static <output_path>` kullanın. Sonra kullanıcının HTML'i tarayıcısında açmak için tıklayabileceği bir bağlantı sunun.
- Her nedense Cowork kurulumu, Claude'u testleri çalıştırdıktan sonra değerlendirme görüntüleyicisini oluşturmaktan soğutuyor gibi görünüyor; o yüzden bir kez daha yineleyelim: Cowork'te de Claude Code'da da testleri çalıştırdıktan sonra, skill'i kendiniz revize edip düzeltmeye çalışmadan önce, insanın örneklere bakabilmesi için değerlendirme görüntüleyicisini her zaman `generate_review.py` ile (kendi özel HTML kodunuzu yazarak değil) oluşturmalısınız. Şimdiden kusura bakmayın ama burada büyük harflere geçeceğim: GİRDİLERİ KENDİNİZ DEĞERLENDİRMEDEN *ÖNCE* DEĞERLENDİRME GÖRÜNTÜLEYİCİSİNİ OLUŞTURUN. Bunları bir an önce insanın önüne koymak istersiniz!
- Geri bildirim farklı çalışır: çalışan bir sunucu olmadığı için görüntüleyicinin "Submit All Reviews" düğmesi `feedback.json` dosyasını bir dosya olarak indirir. Sonra onu oradan okuyabilirsiniz (önce erişim istemeniz gerekebilir).
- Paketleme çalışır — `package_skill.py` yalnızca Python ve bir dosya sistemi ister.
- Açıklama optimizasyonu (`run_loop.py` / `run_eval.py`) tarayıcı değil, alt süreç üzerinden `claude -p` kullandığı için Cowork'te sorunsuz çalışmalıdır; ama lütfen skill'i tamamen bitirene ve kullanıcı skill'in iyi durumda olduğunu kabul edene kadar bunu bekletin.
- **Mevcut bir skill'i güncelleme**: Kullanıcı yeni bir skill oluşturmanızı değil, mevcut bir skill'i güncellemenizi istiyor olabilir. Yukarıdaki Claude.ai bölümündeki güncelleme yönergelerini izleyin.

---

## Referans dosyaları

agents/ dizini, uzmanlaşmış alt ajanlar için talimatlar içerir. İlgili alt ajanı başlatmanız gerektiğinde bunları okuyun.

- `agents/grader.md` — Assertion'ların çıktılara göre nasıl değerlendirileceği
- `agents/comparator.md` — İki çıktı arasında kör A/B karşılaştırmasının nasıl yapılacağı
- `agents/analyzer.md` — Bir sürümün diğerini neden geçtiğinin nasıl analiz edileceği

references/ dizininde ek belgeler bulunur:
- `references/schemas.md` — evals.json, grading.json vb. için JSON yapıları

---

Buradaki temel döngüyü vurgu için bir kez daha tekrarlıyorum:

- Skill'in neyle ilgili olduğunu belirleyin
- Skill'in taslağını yazın ya da düzenleyin
- Skill'e erişimi olan Claude'u test prompt'ları üzerinde çalıştırın
- Kullanıcıyla birlikte çıktıları değerlendirin:
  - benchmark.json oluşturun ve kullanıcının incelemesine yardım etmek için `eval-viewer/generate_review.py` çalıştırın
  - Nicel değerlendirmeleri çalıştırın
- Siz ve kullanıcı memnun kalana kadar tekrarlayın
- Nihai skill'i paketleyin ve kullanıcıya teslim edin.

Unutmadığınızdan emin olmak için, varsa TodoList'inize adımları ekleyin. Cowork'teyseniz, bunun gerçekleştiğinden emin olmak için TodoList'inize özellikle "Değerlendirmelerin JSON'unu oluştur ve insanın test senaryolarını inceleyebilmesi için `eval-viewer/generate_review.py` çalıştır" maddesini ekleyin.

Bol şans!
