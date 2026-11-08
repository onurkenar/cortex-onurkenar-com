
# Web Artifact Oluşturucu

Güçlü frontend claude.ai artifact'leri oluşturmak için şu adımları izle:
1. Frontend deposunu `scripts/init-artifact.sh` ile başlat
2. Üretilen kodu düzenleyerek artifact'ini geliştir
3. Tüm kodu `scripts/bundle-artifact.sh` ile tek bir HTML dosyasında paketle
4. Artifact'i kullanıcıya göster
5. (İsteğe bağlı) Artifact'i test et

**Teknoloji yığını**: React 18 + TypeScript + Vite + Parcel (paketleme) + Tailwind CSS + shadcn/ui

## Tasarım ve Stil Yönergeleri

ÇOK ÖNEMLİ: Sıklıkla "AI slop" (yapay zekâ çöplüğü) olarak anılan şeyden kaçınmak için aşırı ortalanmış yerleşimler, mor gradyanlar, her yerde aynı yuvarlatılmış köşeler ve Inter fontu kullanmaktan kaçın.

## Hızlı Başlangıç

### Adım 1: Projeyi Başlat

Yeni bir React projesi oluşturmak için başlatma betiğini çalıştır:
```bash
bash scripts/init-artifact.sh <project-name>
cd <project-name>
```

Bu, şunlarla tamamen yapılandırılmış bir proje oluşturur:
- ✅ React + TypeScript (Vite ile)
- ✅ shadcn/ui tema sistemiyle Tailwind CSS 3.4.1
- ✅ Yol takma adları (`@/`) yapılandırılmış
- ✅ 40+ shadcn/ui bileşeni önceden kurulu
- ✅ Tüm Radix UI bağımlılıkları dahil
- ✅ Paketleme için Parcel yapılandırılmış (.parcelrc ile)
- ✅ Node 18+ uyumluluğu (Vite sürümünü otomatik algılar ve sabitler)

### Adım 2: Artifact'ini Geliştir

Artifact'i oluşturmak için üretilen dosyaları düzenle. Rehberlik için aşağıdaki **Yaygın Geliştirme Görevleri** bölümüne bak.

### Adım 3: Tek Bir HTML Dosyasında Paketle

React uygulamasını tek bir HTML artifact'inde paketlemek için:
```bash
bash scripts/bundle-artifact.sh
```

Bu, `bundle.html` dosyasını oluşturur — tüm JavaScript, CSS ve bağımlılıkları satır içine alınmış, kendi kendine yeten bir artifact. Bu dosya Claude konuşmalarında doğrudan bir artifact olarak paylaşılabilir.

**Gereksinimler**: Projenin kök dizininde bir `index.html` bulunmalıdır.

**Betiğin yaptıkları**:
- Paketleme bağımlılıklarını kurar (parcel, @parcel/config-default, parcel-resolver-tspaths, html-inline)
- Yol takma adı desteğiyle `.parcelrc` yapılandırmasını oluşturur
- Parcel ile derler (kaynak haritaları olmadan)
- html-inline kullanarak tüm varlıkları tek bir HTML dosyasının içine alır

### Adım 4: Artifact'i Kullanıcıyla Paylaş

Son olarak, paketlenmiş HTML dosyasını kullanıcının bir artifact olarak görüntüleyebilmesi için konuşmada kullanıcıyla paylaş.

### Adım 5: Artifact'i Test Etme/Görselleştirme (İsteğe Bağlı)

Not: Bu tamamen isteğe bağlı bir adımdır. Yalnızca gerekliyse ya da istenirse uygula.

Artifact'i test etmek/görselleştirmek için mevcut araçları kullan (diğer Skill'ler ya da Playwright veya Puppeteer gibi yerleşik araçlar dahil). Genel olarak, artifact'i baştan test etmekten kaçın; çünkü bu, istek ile bitmiş artifact'in görülebildiği an arasına gecikme ekler. İstenirse ya da sorun çıkarsa, artifact'i sunduktan sonra test et.

## Başvuru

- **shadcn/ui bileşenleri**: https://ui.shadcn.com/docs/components