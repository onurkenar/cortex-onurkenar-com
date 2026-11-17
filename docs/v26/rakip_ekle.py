# -*- coding: utf-8 -*-
"""8.11 Rakip Aksiyonları & Adaylar (2026-11-15) + Ortak Bilgiler › Rakip Listesi satır düzenleyicisi (2026-11-16).
Kullanım: python3 -I docs/v26/rakip_ekle.py <html> [docs/ortak-bilgiler/ortak-bilgiler.json]
<style id="v26-rivals"> ← docs/v26/v26-rivals.css, <script id="v26-rivals"> ← docs/v26/v26-rivals.js (v26-mobile'dan önce; betik
v26-meta-ads'ten sonra — 8.10'un rakip Meta reklam kaydını okur). Varsa yerinde yenilenir; tekrar çalıştırılabilir.
Rakip Listesi (2026-11-16, kullanıcı isteği: Rakip Kayıtları 1.7.1 Rakip Listesi'nde birleşir): ana betikte
/*V26-RIVLIST:BEGIN*/…END*/ ← docs/v26/v26-rivlist.js (function one(f){ öncesinde), kanca one() — RIV_F'deki metin kararı
(oc_competitors) satır düzenleyicisiyle (rivInput) çizilir, SVC kancasının önüne; ayrıntılar window.RVD (v26-rivals.js).
oc_competitors açıklaması ve örneği DATA'da (ve verilirse ortak-bilgiler.json'da) güncellenir.
Veri (bölüm ip_rivals, iki alan type "records" — ip_rv_list 2026-11-16'da kalktı): docs/icerik-planlama/plan_alani_ekle.py."""
import hashlib, json, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-rivals.js", encoding="utf-8").read().strip()
RL = open(ROOT + "/docs/v26/v26-rivlist.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-rivals.css", encoding="utf-8").read().strip()
for t in (JS, CSS, RL):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
OJ = sys.argv[2] if len(sys.argv) > 2 else ""
s = open(p, encoding="utf-8").read()
OLD_EXPL = "Her satıra bir rakip yazın: “Ad | site adresi | tür”. Tür isteğe bağlıdır: Doğrudan (aynı müşteriye aynı ihtiyaç için satış yapan), Dolaylı (aynı ihtiyacı başka yolla karşılayan) ya da İkame. Adres yoksa yalnız adı yazabilirsiniz."
EXPL = "Her rakibi ayrı satıra girin: marka adı, web sitesi ve tür; yeni rakip için “Rakip ekle”. Tür isteğe bağlıdır: Doğrudan (aynı müşteriye aynı ihtiyaç için satış yapan), Dolaylı (aynı ihtiyacı başka yolla karşılayan) ya da İkame. Web sitesi yoksa yalnız adı yazabilirsiniz. Pazarlama › Rakip Analizi açıkken her rakibin altındaki “Ayrıntılar”da profil, ürün, mesaj, kanallar, ölçek, şube, fiyat ve reklam bilgileri girilir."
OLD_EX = "“Örnek Diş Kliniği | https://www.ornekdis.com | Doğrudan” satırı içerik planında RK-01 kimlikli rakip olarak görünür, SEO denetiminde de bu sitenin hizmet sayfaları sizinkilerle karşılaştırılır."
EXAMPLE = "Marka adı “Örnek Diş Kliniği”, web sitesi https://www.ornekdis.com, türü Doğrudan olan satır içerik planında RK-01 kimlikli rakip olur; Ayrıntılar'a girilen fiyat ve şube bilgileri planın Rakipler sekmesine aktarılır, SEO denetiminde de bu sitenin hizmet sayfaları sizinkilerle karşılaştırılır."


def once(a, b):
    global s
    if b in s:
        return
    if s.count(a) != 1:
        sys.exit("HATA: %d kez: %s" % (s.count(a), a[:80]))
    s = s.replace(a, b)


B, E_ = "/*V26-RIVLIST:BEGIN*/", "/*V26-RIVLIST:END*/"
blk = B + "\n" + RL + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    if s.count(a) != 1:
        sys.exit("HATA: one() bulunamadı")
    s = s.replace(a, "\n" + blk + a[1:])
once("else if(SVC_F[f.id])c=svcInput(f);", "else if(RIV_F[f.id])c=rivInput(f);else if(SVC_F[f.id])c=svcInput(f);")
once(json.dumps(OLD_EXPL, ensure_ascii=False), json.dumps(EXPL, ensure_ascii=False))
once(json.dumps(OLD_EX, ensure_ascii=False), json.dumps(EXAMPLE, ensure_ascii=False))
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-records">', '<script id="v26-meta-ads">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce meta_ads_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-rivals">.*?</style>\n', '<style id="v26-rivals">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-rivals">.*?</script>\n', '<script id="v26-rivals">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if s.index('<script id="v26-rivals">') < s.index('<script id="v26-meta-ads">'):
    sys.exit("HATA: v26-rivals, v26-meta-ads'ten sonra olmalı")
open(p, "w", encoding="utf-8").write(s)
if OJ:
    raw = open(OJ, encoding="utf-8").read()
    n = 0
    for o, x in ((OLD_EXPL, EXPL), (OLD_EX, EXAMPLE)):
        jo, jx = json.dumps(o, ensure_ascii=False), json.dumps(x, ensure_ascii=False)
        if jx in raw:
            continue
        if raw.count(jo) != 1:
            sys.exit("HATA: json'da %d kez: %s" % (raw.count(jo), o[:60]))
        raw = raw.replace(jo, jx)
        n += 1
    json.loads(raw)
    open(OJ, "w", encoding="utf-8").write(raw)
    print("json:", n, "metin")
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
