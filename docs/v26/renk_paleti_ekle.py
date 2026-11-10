#!/usr/bin/env python3
"""Renk Paleti ve kontrast denetimi ("palette" alan tipi, oc_palette) — 2026-11-10.

Kullanım: python3 -I docs/v26/renk_paleti_ekle.py web-proje-gelistirme.html

  - PALETTE alan tanımı → docs/ortak-bilgiler/ortak-bilgiler.json (oc_brand, brand_color_info'dan sonra) ve
    DATA.fields (aynı yer; ortak_bilgiler_ekle.py'nin üreteceği biçimde: {"id","section"} | new)
  - docs/v26/v26-palette.js  → ana betikte /*V26-PALETTE:BEGIN*/ … /*V26-PALETTE:END*/ (yoksa function one(f){ öncesine)
  - docs/v26/v26-palette.css → <style id="v26-palette"> (yoksa </head> öncesine)
  - ana betik kancaları (yalnız eksikse): one, isset, ruleBase
Tekrar çalıştırılabilir: alan tanımı her çalıştırmada bu dosyadakiyle değiştirilir, bloklar kaynaktan yenilenir.
"""
import hashlib, json, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(D))
OC = os.path.join(ROOT, "docs", "ortak-bilgiler", "ortak-bilgiler.json")
AFTER = "brand_color_info"
PALETTE = {
    "id": "oc_palette",
    "new": {
        "label": "Renk Paleti",
        "en": "Color Palette",
        "type": "palette",
        "explanation": "Ana, ikincil ve vurgu renklerini, metin, zemin ve çizgi için yardımcı renkleri ve (kılavuzda tanımlıysa) durum renklerini tek yerde seçersiniz. Her rengin altında, kullanılacağı yerdeki kontrast oranı WCAG 2.2'ye göre hesaplanır; yetersiz çiftler üstteki uyarı kutusunda önerilen tonla birlikte listelenir.",
        "scenario": "Kurumsal kimlik kılavuzundaki renkler siteye, pazarlama görsellerine ve brief'lere aktarılırken; özellikle marka rengi açık bir tonsa (sarı, turuncu, açık mavi, açık yeşil) metnin ve buton yazısının okunup okunmadığını görmek için.",
        "example": "Ana renk olarak #F5A623 (turuncu) seçilirse beyaz zeminde bağlantı metni 2,0:1 çıkar ve uyarı verilir; öneri olarak metin ve bağlantıda koyulaştırılmış bir ton (ör. #9A6413), butonda ise koyu yazı gösterilir.",
        "rule": "Renk paletinin kontrastı WCAG 2.2 AA ölçütüne göre denetlenmiştir. {contrast} Kontrastı 4,5:1'in altındaki renk çiftleri normal metinde, 3:1'in altındakiler büyük metin, ikon, form kenarlığı ve odak çerçevesinde kullanılmaz; yetersiz çiftler için önerilen koyu / açık tonlar ayrı token olarak tanımlanır (ör. --color-primary-text) ve durum hiçbir zaman yalnız renkle anlatılmaz.",
        "agents": [
            "poz:bilgi-teknolojileri:15.05/kurumsal-yazilim-gelistirme/uygulama-gelistirme-uzmani",
            "poz:tasarim:19.02/marka-kimligi-tasarimi/gorsel-kimlik-uzmani",
        ],
        "palette": [
            {"title": "Ana renkler", "desc": "Markayı temsil eden renkler: butonlar, bağlantılar, aktif durumlar ve vurgu alanları.",
             "ids": ["brand_color_primary", "brand_color_secondary", "brand_color_accent"]},
            {"title": "Yardımcı renkler", "desc": "Metin, zemin ve çizgi renkleri; sayfanın okunabilirliğini en çok bunlar belirler.",
             "ids": ["brand_color_dark", "brand_color_light", "brand_color_neutral"]},
            {"title": "Durum renkleri", "desc": "Başarı, uyarı, hata ve bilgi mesajları, rozetler ve form doğrulama.",
             "ids": ["brand_color_success", "brand_color_warning", "brand_color_error", "brand_color_info"],
             "gate": {"field": "brand_status_colors",
                      "text": "Durum renkleri kurumsal kılavuzda tanımlıysa burada seçilir; şu an Kurumsal Kimlik › Durum Renkleri kararında “Kurumsal kılavuzdaki tanımlar” seçili değil.",
                      "link": "Durum Renkleri kararına git"}},
        ],
    },
}
MARK = "const DATA="


def die(m):
    sys.exit("HATA: " + m)


hp = sys.argv[1]
s = open(hp, encoding="utf-8").read()
js = open(os.path.join(D, "v26-palette.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-palette.css"), encoding="utf-8").read().strip()
for t in (js, css):
    if "</script" in t or "<!--" in t or "</style" in t:
        die("kaynakta </script, </style ya da <!-- var")

# 1) Ortak Bilgiler kaynağı
oc = json.load(open(OC, encoding="utf-8"))
sec = next((x for x in oc["sections"] if x["id"] == "oc_brand"), None) or die("ortak-bilgiler.json: oc_brand yok")
sec["fields"] = [f for f in sec["fields"] if f["id"] != PALETTE["id"]]
k = next((i for i, f in enumerate(sec["fields"]) if f["id"] == AFTER), None)
if k is None:
    die("ortak-bilgiler.json: " + AFTER + " yok")
sec["fields"].insert(k + 1, PALETTE)
open(OC, "w", encoding="utf-8").write(json.dumps(oc, ensure_ascii=False, indent=1) + "\n")

# 2) DATA
if s.count(MARK) != 1:
    die("DATA satırı bulunamadı")
i = s.index(MARK) + len(MARK)
data, end = json.JSONDecoder().raw_decode(s, i)
FI = {f["id"]: f for f in data["fields"]}
ids = [x for g in PALETTE["new"]["palette"] for x in g["ids"]]
for x in ids + [PALETTE["new"]["palette"][2]["gate"]["field"]]:
    if x not in FI:
        die("alan yok: " + x)
for x in ids:
    if FI[x]["section"] != "oc_brand" or FI[x]["type"] != "color":
        die("üye alan oc_brand'da renk alanı değil: " + x)
for k2 in ("label", "en", "type", "rule", "explanation", "scenario", "example"):
    if not PALETTE["new"][k2].strip():
        die("boş: " + k2)
if "{contrast}" not in PALETTE["new"]["rule"]:
    die("kuralda {contrast} yok")
data["fields"] = [f for f in data["fields"] if f["id"] != PALETTE["id"]]
k = [f["id"] for f in data["fields"]].index(AFTER)
data["fields"].insert(k + 1, {"id": PALETTE["id"], "section": "oc_brand"} | PALETTE["new"])
out = json.dumps(data, ensure_ascii=False)
for bad in ("</script", "<!--"):
    if bad in out:
        die("DATA içinde yasak dizi: " + bad)
s = s[:i] + out + s[end:]


def once(old, new, done):
    global s
    if done in s:
        return
    if s.count(old) != 1:
        die(f"{old[:60]!r} {s.count(old)} kez geçiyor")
    s = s.replace(old, new)


# 3) JS bloğu
B, E_ = "/*V26-PALETTE:BEGIN*/", "/*V26-PALETTE:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    once("function one(f){", blk + "function one(f){", B)

# 4) CSS bloğu
st = '<style id="v26-palette">\n' + css + "\n</style>"
if '<style id="v26-palette">' in s:
    s = re.sub(r'<style id="v26-palette">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    if s.count("</head>") != 1:
        die("</head> tek değil")
    s = s.replace("</head>", st + "\n</head>")

# 5) kancalar
once("""else if(f.type==="panels")c='<div class="pzSlot"></div>';""",
     """else if(f.type==="panels")c='<div class="pzSlot"></div>';else if(f.type==="palette")c=palInput(f);""",
     'f.type==="palette")c=palInput(f)')
once('function isset(f){let v=state[f.id];return f.type==="panels"?',
     'function isset(f){let v=state[f.id];return f.type==="palette"?palHas():f.type==="panels"?',
     'f.type==="palette"?palHas()')
once('function ruleBase(f){if(!isset(f))return"";',
     'function ruleBase(f){if(!isset(f))return"";if(f.type==="palette")return palRule(f);',
     'if(f.type==="palette")return palRule(f);')

open(hp, "w", encoding="utf-8").write(s)
b = s.encode("utf-8")
print("tamam · md5", hashlib.md5(b).hexdigest(), "· boyut", len(b))
