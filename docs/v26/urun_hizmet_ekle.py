# -*- coding: utf-8 -*-
"""8.2 Ürün ve Hizmetler kayıt düzenleyicisi (2026-11-15).
Kullanım: python3 -I docs/v26/urun_hizmet_ekle.py <html>
<style id="v26-products"> ← docs/v26/v26-products.css, <script id="v26-records"> ← docs/v26/v26-records.js (kayıt alanı çekirdeği),
<script id="v26-products"> ← docs/v26/v26-products.js (ikisi de v26-mobile'dan
önce; betik v26-planfile'dan sonra olmalı — mkPlanData'yı onun üstünden sarar). Varsa yerinde yenilenir; tekrar çalıştırılabilir.
Veri (bölüm ip_products, alan ip_products type "records"): docs/icerik-planlama/plan_alani_ekle.py."""
import hashlib, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-products.js", encoding="utf-8").read().strip()
CORE = open(ROOT + "/docs/v26/v26-records.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-products.css", encoding="utf-8").read().strip()
for t in (JS, CSS, CORE):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-planfile">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce plan_dosyasi_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-products">.*?</style>\n', '<style id="v26-products">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-records">.*?</script>\n', '<script id="v26-records">\n' + CORE + "\n</script>\n", '<script id="v26-products">' if '<script id="v26-products">' in s else '<script id="v26-mobile">')
s = put(s, r'<script id="v26-products">.*?</script>\n', '<script id="v26-products">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if not s.index('<script id="v26-planfile">') < s.index('<script id="v26-records">') < s.index('<script id="v26-products">'):
    sys.exit("HATA: sıra v26-planfile → v26-records → v26-products olmalı")
open(p, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
