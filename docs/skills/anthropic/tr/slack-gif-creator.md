
# Slack GIF Oluşturucu

Slack için optimize edilmiş animasyonlu GIF'ler oluşturmaya yönelik yardımcı araçlar ve bilgi sunan bir araç seti.

## Slack Gereksinimleri

**Boyutlar:**
- Emoji GIF'leri: 128x128 (önerilen)
- Mesaj GIF'leri: 480x480

**Parametreler:**
- FPS: 10-30 (düşük değer daha küçük dosya boyutu demektir)
- Renkler: 48-128 (daha az renk = daha küçük dosya boyutu)
- Süre: Emoji GIF'lerini 3 saniyenin altında tutun

## Temel İş Akışı

```python
from core.gif_builder import GIFBuilder
from PIL import Image, ImageDraw

# 1. Create builder
builder = GIFBuilder(width=128, height=128, fps=10)

# 2. Generate frames
for i in range(12):
    frame = Image.new('RGB', (128, 128), (240, 248, 255))
    draw = ImageDraw.Draw(frame)

    # Draw your animation using PIL primitives
    # (circles, polygons, lines, etc.)

    builder.add_frame(frame)

# 3. Save with optimization
builder.save('output.gif', num_colors=48, optimize_for_emoji=True)
```

## Grafik Çizimi

### Kullanıcının Yüklediği Görsellerle Çalışma
Kullanıcı bir görsel yüklerse şunlardan hangisini istediğini değerlendirin:
- **Doğrudan kullanmak** (ör. "bunu canlandır", "bunu karelere böl")
- **İlham kaynağı olarak kullanmak** (ör. "buna benzer bir şey yap")

Görselleri PIL ile yükleyip üzerinde çalışın:
```python
from PIL import Image

uploaded = Image.open('file.png')
# Use directly, or just as reference for colors/style
```

### Sıfırdan Çizim
Grafikleri sıfırdan çizerken PIL ImageDraw temel öğelerini kullanın:

```python
from PIL import ImageDraw

draw = ImageDraw.Draw(frame)

# Circles/ovals
draw.ellipse([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)

# Stars, triangles, any polygon
points = [(x1, y1), (x2, y2), (x3, y3), ...]
draw.polygon(points, fill=(r, g, b), outline=(r, g, b), width=3)

# Lines
draw.line([(x1, y1), (x2, y2)], fill=(r, g, b), width=5)

# Rectangles
draw.rectangle([x1, y1, x2, y2], fill=(r, g, b), outline=(r, g, b), width=3)
```

**Kullanmayın:** Emoji fontları (platformlar arasında güvenilir değildir) ya da bu skill'de hazır grafikler bulunduğunu varsaymayın.

### Grafiklerin İyi Görünmesini Sağlama

Grafikler basit değil, özenli ve yaratıcı görünmelidir. Bunu şöyle sağlayın:

**Daha kalın çizgiler kullanın** - Dış hatlar ve çizgiler için her zaman `width=2` ya da daha yüksek bir değer verin. İnce çizgiler (width=1) kesik kesik ve amatörce görünür.

**Görsel derinlik katın**:
- Arka planlar için gradyan kullanın (`create_gradient_background`)
- Karmaşıklık için birden çok şekli katmanlayın (ör. içinde daha küçük bir yıldız olan bir yıldız)

**Şekilleri daha ilginç hâle getirin**:
- Yalnızca düz bir daire çizmeyin; parlama noktaları, halkalar ya da desenler ekleyin
- Yıldızlara ışıma eklenebilir (arkalarına daha büyük, yarı saydam kopyalarını çizin)
- Birden çok şekli birleştirin (yıldızlar + pırıltılar, daireler + halkalar)

**Renklere dikkat edin**:
- Canlı, birbirini tamamlayan renkler kullanın
- Kontrast ekleyin (açık şekillerde koyu dış hat, koyu şekillerde açık dış hat)
- Genel kompozisyonu göz önünde bulundurun

**Karmaşık şekiller için** (kalpler, kar taneleri vb.):
- Çokgen ve elips birleşimleri kullanın
- Simetri için noktaları dikkatle hesaplayın
- Ayrıntı ekleyin (bir kalpte parlama eğrisi olabilir, kar tanelerinin karmaşık dalları vardır)

Yaratıcı ve ayrıntılı olun! İyi bir Slack GIF'i yer tutucu grafik gibi değil, özenli görünmelidir.

## Kullanılabilir Yardımcı Araçlar

### GIFBuilder (`core.gif_builder`)
Kareleri birleştirir ve Slack için optimize eder:
```python
builder = GIFBuilder(width=128, height=128, fps=10)
builder.add_frame(frame)  # Add PIL Image
builder.add_frames(frames)  # Add list of frames
builder.save('out.gif', num_colors=48, optimize_for_emoji=True, remove_duplicates=True)
```

### Doğrulayıcılar (`core.validators`)
GIF'in Slack gereksinimlerini karşılayıp karşılamadığını denetler:
```python
from core.validators import validate_gif, is_slack_ready

# Detailed validation
passes, info = validate_gif('my.gif', is_emoji=True, verbose=True)

# Quick check
if is_slack_ready('my.gif'):
    print("Ready!")
```

### Yumuşatma (Easing) Fonksiyonları (`core.easing`)
Doğrusal yerine yumuşak hareket:
```python
from core.easing import interpolate

# Progress from 0.0 to 1.0
t = i / (num_frames - 1)

# Apply easing
y = interpolate(start=0, end=400, t=t, easing='ease_out')

# Available: linear, ease_in, ease_out, ease_in_out,
#           bounce_out, elastic_out, back_out
```

### Kare Yardımcıları (`core.frame_composer`)
Sık ihtiyaçlar için kolaylık fonksiyonları:
```python
from core.frame_composer import (
    create_blank_frame,         # Solid color background
    create_gradient_background,  # Vertical gradient
    draw_circle,                # Helper for circles
    draw_text,                  # Simple text rendering
    draw_star                   # 5-pointed star
)
```

## Animasyon Kavramları

### Sallanma/Titreşim
Nesnenin konumunu salınımla kaydırın:
- Kare indeksiyle `math.sin()` ya da `math.cos()` kullanın
- Doğal bir his için küçük rastgele değişimler ekleyin
- x ve/veya y konumuna uygulayın

### Nabız/Kalp Atışı
Nesnenin boyutunu ritmik olarak ölçekleyin:
- Yumuşak bir nabız için `math.sin(t * frequency * 2 * math.pi)` kullanın
- Kalp atışı için: iki hızlı atış, ardından duraklama (sinüs dalgasını ayarlayın)
- Temel boyutun 0.8 ile 1.2 katı arasında ölçekleyin

### Zıplama
Nesne düşer ve zıplar:
- Yere iniş için `easing='bounce_out'` ile `interpolate()` kullanın
- Düşüş (hızlanma) için `easing='ease_in'` kullanın
- Her karede y hızını artırarak yerçekimi uygulayın

### Dönme/Döndürme
Nesneyi merkezi etrafında döndürün:
- PIL: `image.rotate(angle, resample=Image.BICUBIC)`
- Yalpalama için: açıda doğrusal değer yerine sinüs dalgası kullanın

### Belirme/Kaybolma (Fade In/Out)
Yavaş yavaş görünme ya da kaybolma:
- RGBA görsel oluşturun, alfa kanalını ayarlayın
- Ya da `Image.blend(image1, image2, alpha)` kullanın
- Belirme: alfa 0'dan 1'e
- Kaybolma: alfa 1'den 0'a

### Kayma
Nesneyi ekran dışından yerine taşıyın:
- Başlangıç konumu: kare sınırlarının dışında
- Bitiş konumu: hedef konum
- Yumuşak duruş için `easing='ease_out'` ile `interpolate()` kullanın
- Hedefi aşıp geri dönme için: `easing='back_out'` kullanın

### Yakınlaştırma
Yakınlaştırma etkisi için ölçekleyip konumlandırın:
- Yakınlaştırma: 0.1'den 2.0'a ölçekleyin, merkezi kırpın
- Uzaklaştırma: 2.0'dan 1.0'a ölçekleyin
- Etkiyi artırmak için hareket bulanıklığı eklenebilir (PIL filtresi)

### Patlama/Parçacık Saçılması
Dışa doğru yayılan parçacıklar oluşturun:
- Rastgele açı ve hızlarla parçacıklar üretin
- Her parçacığı güncelleyin: `x += vx`, `y += vy`
- Yerçekimi ekleyin: `vy += gravity_constant`
- Parçacıkları zamanla soldurun (alfayı azaltın)

## Optimizasyon Stratejileri

Yalnızca dosya boyutunu küçültmeniz istendiğinde aşağıdaki yöntemlerden birkaçını uygulayın:

1. **Daha az kare** - Daha düşük FPS (20 yerine 10) ya da daha kısa süre
2. **Daha az renk** - 128 yerine `num_colors=48`
3. **Daha küçük boyutlar** - 480x480 yerine 128x128
4. **Yinelenenleri kaldırma** - save() içinde `remove_duplicates=True`
5. **Emoji modu** - `optimize_for_emoji=True` otomatik optimize eder

```python
# Maximum optimization for emoji
builder.save(
    'emoji.gif',
    num_colors=48,
    optimize_for_emoji=True,
    remove_duplicates=True
)
```

## Yaklaşım

Bu skill şunları sağlar:
- **Bilgi**: Slack gereksinimleri ve animasyon kavramları
- **Yardımcı araçlar**: GIFBuilder, doğrulayıcılar, yumuşatma fonksiyonları
- **Esneklik**: Animasyon mantığını PIL temel öğeleriyle kendiniz kurarsınız

Şunları SAĞLAMAZ:
- Katı animasyon şablonları ya da hazır fonksiyonlar
- Emoji fontu çizimi (platformlar arasında güvenilir değildir)
- Skill'e gömülü hazır grafik kütüphanesi

**Kullanıcı yüklemeleri hakkında not**: Bu skill hazır grafikler içermez; ancak kullanıcı bir görsel yüklerse onu PIL ile yükleyip üzerinde çalışın — doğrudan mı yoksa yalnızca ilham kaynağı olarak mı kullanılmasını istediğini isteğine göre yorumlayın.

Yaratıcı olun! Kavramları birleştirin (zıplama + dönme, nabız + kayma vb.) ve PIL'in bütün olanaklarını kullanın.

## Bağımlılıklar

```bash
pip install pillow imageio numpy
```
