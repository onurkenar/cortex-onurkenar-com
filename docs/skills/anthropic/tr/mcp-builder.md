
# MCP Sunucusu Geliştirme Rehberi

## Genel Bakış

LLM'lerin iyi tasarlanmış araçlar aracılığıyla dış hizmetlerle etkileşim kurmasını sağlayan MCP (Model Context Protocol) sunucuları oluşturun. Bir MCP sunucusunun kalitesi, LLM'lerin gerçek dünyadaki görevleri ne kadar iyi yerine getirmesini sağladığıyla ölçülür.

---

# Süreç

## 🚀 Üst Düzey İş Akışı

Yüksek kaliteli bir MCP sunucusu oluşturmak dört ana aşamadan oluşur:

### Aşama 1: Derinlemesine Araştırma ve Planlama

#### 1.1 Modern MCP Tasarımını Anlayın

**API Kapsamı ve İş Akışı Araçları:**
Kapsamlı API uç noktası kapsamını, belirli işlere özel iş akışı araçlarıyla dengeleyin. İş akışı araçları belirli görevlerde daha pratik olabilir; kapsamlı kapsam ise ajanlara işlemleri birleştirme esnekliği verir. Performans istemciye göre değişir: bazı istemciler temel araçları birleştiren kod yürütmeden yararlanırken bazıları üst düzey iş akışlarıyla daha iyi çalışır. Emin olmadığınızda kapsamlı API kapsamına öncelik verin.

**Araç Adlandırma ve Bulunabilirlik:**
Açık ve tanımlayıcı araç adları, ajanların doğru araçları hızla bulmasına yardımcı olur. Tutarlı ön ekler (ör. `github_create_issue`, `github_list_repos`) ve eylem odaklı adlandırma kullanın.

**Bağlam Yönetimi:**
Ajanlar kısa araç açıklamalarından ve sonuçları filtreleyip sayfalayabilmekten yararlanır. Odaklı ve ilgili veri döndüren araçlar tasarlayın. Bazı istemciler kod yürütmeyi destekler; bu da ajanların veriyi verimli biçimde filtreleyip işlemesine yardımcı olabilir.

**Eyleme Dönüştürülebilir Hata Mesajları:**
Hata mesajları, somut öneriler ve sonraki adımlarla ajanları çözüme yönlendirmelidir.

#### 1.2 MCP Protokol Belgelerini İnceleyin

**MCP spesifikasyonunda gezinin:**

İlgili sayfaları bulmak için site haritasıyla başlayın: `https://modelcontextprotocol.io/sitemap.xml`

Ardından belirli sayfaları Markdown biçiminde almak için `.md` son ekiyle getirin (ör. `https://modelcontextprotocol.io/specification/draft.md`).

İncelenecek temel sayfalar:
- Spesifikasyona genel bakış ve mimari
- Taşıma mekanizmaları (streamable HTTP, stdio)
- Araç, kaynak (resource) ve prompt tanımları

#### 1.3 Framework Belgelerini İnceleyin

**Önerilen yığın:**
- **Dil**: TypeScript (yüksek kaliteli SDK desteği ve MCPB gibi birçok çalışma ortamıyla iyi uyumluluk. Ayrıca yapay zekâ modelleri, yaygın kullanımı, statik tiplemesi ve iyi lint araçları sayesinde TypeScript kodu üretmede başarılıdır)
- **Taşıma**: Uzak sunucular için durumsuz JSON kullanan Streamable HTTP (durumlu oturumlara ve akışlı yanıtlara kıyasla ölçeklemesi ve bakımı daha kolaydır). Yerel sunucular için stdio.

**Framework belgelerini yükleyin:**

- **MCP En İyi Uygulamaları**: [📋 En İyi Uygulamaları Görüntüle](./reference/mcp_best_practices.md) - Temel yönergeler

**TypeScript için (önerilen):**

TypeScript SDK'nın iki ana sürümü vardır. Kod yazmadan önce birini seçin:
- **v2** (`@modelcontextprotocol/server`): güncel kararlı sürüm. Yeni sunucular için bunu kullanın.
- **v1** (`@modelcontextprotocol/sdk`): yalnız hata ve güvenlik düzeltmeleri alır. Yalnızca projenin `package.json` dosyası zaten `@modelcontextprotocol/sdk` paketine bağımlıysa kullanın ya da o projeyi `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` ile taşıyın.

Proje zaten v1 kullanıyorsa kullanıcıya bir kez, bir iki cümleyle, v2'nin (`@modelcontextprotocol/server`) güncel kararlı sürüm olduğunu, v1'in yalnız hata ve güvenlik düzeltmeleri aldığını ve `npx @modelcontextprotocol/codemod@latest v1-to-v2 .` komutunun projeyi taşıdığını söyleyin. Kullanıcı taşımayı istemedikçe v1 ile devam edin.

İkisini aynı projede karıştırmayın: v1 kod örnekleri (`@modelcontextprotocol/sdk/...` içe aktarımları) v2 için geçerli değildir.

- **TypeScript SDK (v2)**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` adresini WebFetch ile yükleyin; belgelerin tam dizini `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt`
- [⚡ TypeScript Rehberi (v2)](./reference/node_mcp_server_v2.md) - TypeScript kalıpları ve örnekleri
- Yalnız v1 projeleri için: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` ve [TypeScript Rehberi (v1)](./reference/node_mcp_server.md)

**Python için:**
- **Python SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` adresini WebFetch ile yükleyin
- [🐍 Python Rehberi](./reference/python_mcp_server.md) - Python kalıpları ve örnekleri

#### 1.4 Uygulamanızı Planlayın

**API'yi Anlayın:**
Temel uç noktaları, kimlik doğrulama gereksinimlerini ve veri modellerini belirlemek için hizmetin API belgelerini inceleyin. Gerektiğinde web araması ve WebFetch kullanın.

**Araç Seçimi:**
Kapsamlı API kapsamına öncelik verin. Uygulanacak uç noktaları en yaygın işlemlerden başlayarak listeleyin.

---

### Aşama 2: Uygulama

#### 2.1 Proje Yapısını Kurun

Proje kurulumu için dile özgü rehberlere bakın:
- [⚡ TypeScript Rehberi (v2)](./reference/node_mcp_server_v2.md) - Proje yapısı, package.json, tsconfig.json (mevcut v1 projeleri için [v1](./reference/node_mcp_server.md))
- [🐍 Python Rehberi](./reference/python_mcp_server.md) - Modül düzeni, bağımlılıklar

#### 2.2 Temel Altyapıyı Uygulayın

Ortak yardımcılar oluşturun:
- Kimlik doğrulamalı API istemcisi
- Hata işleme yardımcıları
- Yanıt biçimlendirme (JSON/Markdown)
- Sayfalama desteği

#### 2.3 Araçları Uygulayın

Her araç için:

**Girdi Şeması:**
- Zod (TypeScript) ya da Pydantic (Python) kullanın
- Kısıtları ve açık açıklamaları ekleyin
- Alan açıklamalarına örnekler ekleyin

**Çıktı Şeması:**
- Yapılandırılmış veri için mümkün olduğunda `outputSchema` tanımlayın
- Araç yanıtlarında `structuredContent` kullanın (TypeScript SDK özelliği)
- İstemcilerin araç çıktılarını anlamasına ve işlemesine yardımcı olur

**Araç Açıklaması:**
- İşlevin kısa özeti
- Parametre açıklamaları
- Dönüş tipi şeması

**Uygulama:**
- G/Ç işlemleri için async/await
- Eyleme dönüştürülebilir mesajlarla düzgün hata işleme
- Uygun olduğu yerde sayfalama desteği
- Modern SDK'lar kullanırken hem metin içeriği hem yapılandırılmış veri döndürün

**Açıklamalar (annotations):**
- `readOnlyHint`: true/false
- `destructiveHint`: true/false
- `idempotentHint`: true/false
- `openWorldHint`: true/false

---

### Aşama 3: İnceleme ve Test

#### 3.1 Kod Kalitesi

Şunları gözden geçirin:
- Tekrarlanan kod olmaması (DRY ilkesi)
- Tutarlı hata işleme
- Tam tip kapsamı
- Açık araç açıklamaları

#### 3.2 Derleme ve Test

**TypeScript:**
- Derlemeyi doğrulamak için `npm run build` çalıştırın
- v2 projeleri: [v2 rehberindeki](./reference/node_mcp_server_v2.md#verify-your-server) öz denetim betiğini derlenmiş sunucuya karşı çalıştırın
- MCP Inspector ile test edin: `npx @modelcontextprotocol/inspector`

**Python:**
- Sözdizimini doğrulayın: `python -m py_compile your_server.py`
- MCP Inspector ile test edin

Ayrıntılı test yaklaşımları ve kalite kontrol listeleri için dile özgü rehberlere bakın.

---

### Aşama 4: Değerlendirmeler (eval) Oluşturun

MCP sunucunuzu uyguladıktan sonra etkinliğini sınamak için kapsamlı değerlendirmeler oluşturun.

**Değerlendirme yönergelerinin tamamı için [✅ Değerlendirme Rehberi](./reference/evaluation.md)'ni yükleyin.**

#### 4.1 Değerlendirmenin Amacını Anlayın

LLM'lerin MCP sunucunuzu gerçekçi ve karmaşık soruları yanıtlamak için etkili biçimde kullanıp kullanamadığını sınamak için değerlendirmeleri kullanın.

#### 4.2 10 Değerlendirme Sorusu Oluşturun

Etkili değerlendirmeler oluşturmak için değerlendirme rehberinde anlatılan süreci izleyin:

1. **Araç İncelemesi**: Kullanılabilir araçları listeleyin ve yeteneklerini anlayın
2. **İçerik Keşfi**: Mevcut veriyi keşfetmek için YALNIZ OKUMA işlemleri kullanın
3. **Soru Üretimi**: 10 karmaşık ve gerçekçi soru oluşturun
4. **Yanıt Doğrulama**: Yanıtları doğrulamak için her soruyu kendiniz çözün

#### 4.3 Değerlendirme Gereksinimleri

Her sorunun şu özellikleri taşıdığından emin olun:
- **Bağımsız**: Diğer sorulara bağlı değil
- **Yalnız okuma**: Yalnızca yıkıcı olmayan işlemler gerektiriyor
- **Karmaşık**: Birden çok araç çağrısı ve derinlemesine keşif gerektiriyor
- **Gerçekçi**: İnsanların önemseyeceği gerçek kullanım durumlarına dayanıyor
- **Doğrulanabilir**: Metin karşılaştırmasıyla doğrulanabilen tek ve net bir yanıtı var
- **Kararlı**: Yanıt zamanla değişmiyor

#### 4.4 Çıktı Biçimi

Bu yapıda bir XML dosyası oluşturun:

```xml
<evaluation>
  <qa_pair>
    <question>Find discussions about AI model launches with animal codenames. One model needed a specific safety designation that uses the format ASL-X. What number X was being determined for the model named after a spotted wild cat?</question>
    <answer>3</answer>
  </qa_pair>
<!-- More qa_pairs... -->
</evaluation>
```

---

# Başvuru Dosyaları

## 📚 Belge Kütüphanesi

Geliştirme sırasında bu kaynakları gerektikçe yükleyin:

### Temel MCP Belgeleri (Önce Yükleyin)
- **MCP Protokolü**: `https://modelcontextprotocol.io/sitemap.xml` adresindeki site haritasıyla başlayın, ardından belirli sayfaları `.md` son ekiyle getirin
- [📋 MCP En İyi Uygulamaları](./reference/mcp_best_practices.md) - Evrensel MCP yönergeleri; şunları içerir:
  - Sunucu ve araç adlandırma kuralları
  - Yanıt biçimi yönergeleri (JSON ve Markdown)
  - Sayfalama için en iyi uygulamalar
  - Taşıma seçimi (streamable HTTP ve stdio)
  - Güvenlik ve hata işleme standartları

### SDK Belgeleri (Aşama 1/2 Sırasında Yükleyin)
- **Python SDK**: `https://raw.githubusercontent.com/modelcontextprotocol/python-sdk/main/README.md` adresinden getirin
- **TypeScript SDK (v2)**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/main/README.md` adresinden getirin; belgelerin tam dizini `https://ts.sdk.modelcontextprotocol.io/v2/llms.txt` adresinde
- **TypeScript SDK (v1, yalnız mevcut v1 projeleri)**: `https://raw.githubusercontent.com/modelcontextprotocol/typescript-sdk/v1.x/README.md` adresinden getirin

### Dile Özgü Uygulama Rehberleri (Aşama 2 Sırasında Yükleyin)
- [🐍 Python Uygulama Rehberi](./reference/python_mcp_server.md) - Eksiksiz Python/FastMCP rehberi; şunları içerir:
  - Sunucu başlatma kalıpları
  - Pydantic model örnekleri
  - `@mcp.tool` ile araç kaydı
  - Eksiksiz çalışan örnekler
  - Kalite kontrol listesi

- [⚡ TypeScript Uygulama Rehberi (SDK v2)](./reference/node_mcp_server_v2.md) - `@modelcontextprotocol/server` için eksiksiz TypeScript rehberi; şunları içerir:
  - Proje kurulumu ve sunucu fabrikası
  - Araç tasarımı: Zod 4 şemaları, çıktı biçimleri, sayfalama, hatalar
  - stdio ve Streamable HTTP üzerinden hizmet veren eksiksiz bir örnek ve bearer kimlik doğrulaması
  - Kaynaklar (resources), prompt'lar ve bildirimler
  - Derlenmiş sunucuyu doğrulamak için bir öz denetim betiği
  - İleri düzey özellikler için SDK örneklerine bağlantılar
  - v1 → v2 karşılık tablosu, taşıma adımları ve kalite kontrol listesi

- [⚡ TypeScript Uygulama Rehberi (SDK v1)](./reference/node_mcp_server.md) - Mevcut `@modelcontextprotocol/sdk` projeleri için eşdeğer rehber

### Değerlendirme Rehberi (Aşama 4 Sırasında Yükleyin)
- [✅ Değerlendirme Rehberi](./reference/evaluation.md) - Eksiksiz değerlendirme oluşturma rehberi; şunları içerir:
  - Soru oluşturma yönergeleri
  - Yanıt doğrulama stratejileri
  - XML biçim spesifikasyonları
  - Örnek sorular ve yanıtlar
  - Sağlanan betiklerle bir değerlendirmeyi çalıştırma
