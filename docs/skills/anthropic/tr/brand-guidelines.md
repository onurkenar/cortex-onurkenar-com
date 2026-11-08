
# Anthropic Marka Stili

## Genel Bakış

Anthropic'in resmî marka kimliğine ve stil kaynaklarına erişmek için bu skill'i kullanın.

**Anahtar kelimeler**: markalama, kurumsal kimlik, görsel kimlik, son işlem, stil uygulama, marka renkleri, tipografi, Anthropic markası, görsel biçimlendirme, görsel tasarım

## Marka Kuralları

### Renkler

**Ana Renkler:**

- Koyu: `#141413` - Birincil metin ve koyu arka planlar
- Açık: `#faf9f5` - Açık arka planlar ve koyu zemin üzerindeki metin
- Orta Gri: `#b0aea5` - İkincil öğeler
- Açık Gri: `#e8e6dc` - Belirgin olmayan arka planlar

**Vurgu Renkleri:**

- Turuncu: `#d97757` - Birincil vurgu
- Mavi: `#6a9bcc` - İkincil vurgu
- Yeşil: `#788c5d` - Üçüncül vurgu

### Tipografi

- **Başlıklar**: Poppins (Arial yedeğiyle)
- **Gövde Metni**: Lora (Georgia yedeğiyle)
- **Not**: En iyi sonuç için yazı tipleri ortamınızda önceden kurulu olmalıdır

## Özellikler

### Akıllı Yazı Tipi Uygulaması

- Başlıklara (24pt ve üzeri) Poppins yazı tipini uygular
- Gövde metnine Lora yazı tipini uygular
- Özel yazı tipleri yoksa kendiliğinden Arial/Georgia'ya geri döner
- Bütün sistemlerde okunabilirliği korur

### Metin Stili

- Başlıklar (24pt+): Poppins yazı tipi
- Gövde metni: Lora yazı tipi
- Arka plana göre akıllı renk seçimi
- Metin hiyerarşisini ve biçimlendirmeyi korur

### Şekil ve Vurgu Renkleri

- Metin dışı şekillerde vurgu renkleri kullanılır
- Turuncu, mavi ve yeşil vurgular sırayla döndürülür
- Markanın dışına çıkmadan görsel ilgiyi canlı tutar

## Teknik Ayrıntılar

### Yazı Tipi Yönetimi

- Varsa sistemde kurulu Poppins ve Lora yazı tiplerini kullanır
- Arial'a (başlıklar) ve Georgia'ya (gövde) otomatik geri dönüş sağlar
- Yazı tipi kurulumu gerekmez - mevcut sistem yazı tipleriyle çalışır
- En iyi sonuç için Poppins ve Lora yazı tiplerini ortamınıza önceden kurun

### Renk Uygulaması

- Markayla tam eşleşme için RGB renk değerlerini kullanır
- python-pptx'in RGBColor sınıfıyla uygulanır
- Farklı sistemlerde renk doğruluğunu korur
