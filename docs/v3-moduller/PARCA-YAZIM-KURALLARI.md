# Parça yazım kuralları (V3 modülleri)

WP-OnKe tek dosyalık bir "web projesi yapılandırıcısı"dır: kullanıcı karar kartlarından seçim yapar, araç her seçimi
Claude'a verilecek **bağlayıcı proje kuralına** çevirir. Sen kod yazmıyorsun; yeni **karar alanlarının verisini**
Python dosyası olarak yazıyorsun. Dosya `docs/v3-moduller/parca_<ad>.py`, içinde tek bir `PART` sözlüğü.

**Uygulama dosyasına (`web-proje-gelistirme.html`) asla yazma.** Yalnız kendi parça dosyanı yaz.

## PART biçimi

```python
# -*- coding: utf-8 -*-
"""Kısa açıklama (hangi V3 maddeleri)."""

def o(v, l, ex, sc, eg, rd=None, exclusive=False):
    x = {'value': v, 'label': l, 'explanation': ex, 'scenario': sc, 'example': eg}
    if rd: x['ruleDetail'] = rd
    if exclusive: x['exclusive'] = True
    return x

PART = {
  'sections': [ {...} ],      # yeni bölümler (yalnız sana verilen bölüm kimlikleri)
  'fields': [ {...} ],        # yeni bölümlerin alanları, ekranda görünecek sırayla; her alanda 'section'
  'fields_into': [ {...} ],   # VAR OLAN bölümlere eklenen alanlar; her alanda 'section' + 'after' (var olan ya da senin önceki alanın)
  'option_add': [ {'field': 'api_features', 'after': 'OpenAPI', 'option': o(...)} ],  # var olan alana seçenek
  'guide_add': { 'var_olan_bolum_id': [ {'title','url','note'} ] },                  # var olan bölüm rehberine kaynak
}
```

### Bölüm (`sections`)
`{'id', 'group', 'icon', 'name', 'en', 'desc', 'guide'}` — `after` YAZMA (kaynak.py atar).
- `group`: sana söylenen grup adı (ör. `'İş Modülleri'`, `'Teknik Mimari'`).
- `icon`: tek bir sembol karakteri (◈ ⇄ ◍ ▥ ✉ ☎ ★ ◎ ⚑ ⌘ ✦ ⟳ ⧉ vb.; emoji değil).
- `name` Türkçe bölüm adı, `en` İngilizce karşılığı (yalnız aramada kullanılır), `desc` bölümün tek cümlelik açıklaması.
- `guide`: `{'purpose': paragraf, 'criteria': [6 madde], 'pitfalls': [6 madde], 'resources': [5–9 kaynak]}`.
  Kaynak `{'title', 'url' (https), 'note' (ne işe yaradığı, Türkçe tek cümle)}`. **Her adresi gerçekten aç**
  (`curl -sL -o /dev/null -w '%{http_code}' -A 'Mozilla/5.0' <url>` → 200 ya da sayfayı WebFetch ile oku). Açılmayanı koyma.
  Resmî kaynakları tercih et: W3C, MDN, OWASP, NIST, RFC Editor, IETF, KVKK (kvkk.gov.tr), mevzuat.gov.tr, Ticaret Bakanlığı,
  İYS (iys.org.tr), sağlayıcının kendi resmî dokümanı, Google / Apple / Android geliştirici belgeleri.

### Alan
Zorunlu anahtarlar: `id, label, en, type, explanation, scenario, example, rule, agents` (+ yeni bölümde `section`,
var olan bölümde `section` ve `after`). İsteğe bağlı: `options`, `showIf`, `recommend`, `yes`, `no`.
- `id`: küçük harf + alt çizgi, sana verilen önekle (ör. `tk_…`). Var olan kimliklerle çakışmasın (`alanlar.txt`'e bak).
- `type`: `select` (tek seçim), `multiselect` (çoklu), `boolean` (Evet / Hayır).
- `label` Türkçe karar adı; `en` İngilizce adı.
- `explanation`: kararın ne olduğu (1–3 cümle). `scenario`: bu karar ne zaman önemli. `example`: sitede / panelde nasıl görünür, somut örnek.
- `rule`: Proje Kuralları'na ve Claude promptuna giren cümle. select'te `{label}`, multiselect'te `{labels}`, boolean'da
  `{booltext}` yer tutucusu **zorunlu**. Örnek: `'Destek talebi kanalları: {labels}.'`. Bağlayıcı, uygulanabilir yaz.
- `agents`: 1–3 sorumlu pozisyon ajanı kimliği — **yalnız `pozisyonlar.txt`'teki `poz:…` kimlikleri** (ilk sütun, birebir).
  İşi fiilen yapacak pozisyonu seç (yazılım işi → 15 Bilgi Teknolojileri, güvenlik → 16, KVKK → 06.06 / 05.06, satış → 08,
  müşteri deneyimi / destek → ilgili departman, pazarlama → 09 …). `grep -i '<anahtar kelime>' pozisyonlar.txt`.
- `options` (select / multiselect): 3–10 seçenek, her biri `o(value, label, explanation, scenario, example, ruleDetail)`.
  - `value`: kısa, ASCII, alan içinde tekil (ör. `'email'`, `'sla_strict'`). `label` Türkçe, alan içinde tekil.
    Önerilen seçeneğin etiketine ` (önerilen)` ekle (en çok bir tane, select'te).
  - `ruleDetail`: seçilince kuralın sonuna eklenen **uygulama talimatı** (Claude'un kodda ne yapacağı, 1–3 cümle). Seçeneklerin
    çoğunda yaz; "yok / kullanılmaz" seçeneklerinde de ne yapılmayacağını yaz.
  - "Yok / kullanılmayacak" anlamındaki multiselect seçeneğine `exclusive=True` (tek başına kalır).
- `boolean`: `yes` ve `no` = `{'scenario', 'example'}` zorunlu; `options` yazma.
- `showIf`: `[{'field': 'alan_id', 'in': [değerler]}]` — alan yalnız koşul sağlanınca görünür. Değerler kaynak alanın
  `value`'ları (boolean'da `True` / `False`). Kendi bölümündeki kapı alanına ya da var olan alana bağlanabilir.
- `recommend`: `{'field': kaynak_alan, 'map': {kaynak_değer: [bu alanın değerleri]}}` ya da bunların listesi —
  kullanıcıya "Öneriyi uygula" notu çıkarır. Yalnız anlamlı eşleşmelerde kullan.

## Dil ve içerik
- Bütün metin **Türkçe**, sade ve somut; teknik terim gerekiyorsa ilk geçişte parantezle açıkla (ör. "tekil oturum açma (SSO)").
- Türkiye bağlamını gözet: KVKK, 6563 sayılı Kanun ve İYS, Mesafeli Sözleşmeler Yönetmeliği, e-Fatura / e-Arşiv, TL.
  Hukuki iddiada emin değilsen genel yaz ("hukuk biriminin teyidiyle"); tarih / sayı uydurma.
- Bir seçeneğin `scenario`'su "ne zaman bu seçilir", `example`'ı "sitede ya da panelde somut olarak ne görülür".
- Var olan kararları **tekrar etme** (`alanlar.txt`'e bak). Örtüşüyorsa kuralda o karara atıf yap.
- Kurallar sunucu otoritesi, en az yetki, kişisel verinin loglara sızmaması, idempotency gibi güvenli varsayılanları içersin.

## Denetim
Yazdıktan sonra proje kökünde:
```sh
cd /Users/onurkenar/Downloads/Projeler/WP-OnKe
python3 -I docs/v3-moduller/kaynak.py && python3 -I docs/v3-moduller/v3_ekle.py web-proje-gelistirme.html docs/v3-moduller/v3-moduller.json --check
```
"denetim tamam" görene kadar düzelt. `--check` dosyaya yazmaz. (Diğer parçalar da aynı anda yazılıyor olabilir; onların
hatası çıkarsa kendi parçanı ayrı denetlemek için onların dosyasına dokunma — hatanın senin parçana ait olup olmadığına bak.)

Başvuru dosyaları (salt okunur):
- `/private/tmp/claude-501/-Users-onurkenar-Downloads-Projeler-WP-OnKe/0fc3d49a-adff-4edf-b91f-c3ea9d5f1248/scratchpad/v3/alanlar.txt` — var olan bütün bölümler, alanlar, değerler.
- `…/scratchpad/v3/pozisyonlar.txt` — geçerli ajan kimlikleri.
- `…/scratchpad/v3/ornek-alanlar.json` — var olan üç alanın tam verisi (biçim örneği).
- `…/scratchpad/doc/v3.txt` — kaynak doküman (Web_Sayfasi_Projesi_Revize_Moduler_V3.docx'in metni); ilgili başlıkları oku.
- `docs/onay-akisi/kaynak.py`, `docs/cdn/kaynak.py` — aynı biçimde yazılmış iki tamamlanmış örnek (kalite çıtası bunlar).
