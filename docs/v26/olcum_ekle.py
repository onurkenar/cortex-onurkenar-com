# -*- coding: utf-8 -*-
"""8.12 Ölçüm (2026-11-15).
Kullanım: python3 -I docs/v26/olcum_ekle.py <html>
<style id="v26-measure"> ← docs/v26/v26-measure.css, <script id="v26-measure"> ← docs/v26/v26-measure.js (v26-mobile'dan önce;
betik v26-rivals'tan sonra). Varsa yerinde yenilenir; tekrar çalıştırılabilir. Veri (bölüm ip_measure, dört alan type "records"):
docs/icerik-planlama/plan_alani_ekle.py. Takvim bağlantısı: docs/v26/v26-calendar.js (window.OLC.cal)."""
import hashlib, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-measure.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-measure.css", encoding="utf-8").read().strip()
for t in (JS, CSS):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-records">', '<script id="v26-rivals">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce rakip_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-measure">.*?</style>\n', '<style id="v26-measure">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-measure">.*?</script>\n', '<script id="v26-measure">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if s.index('<script id="v26-measure">') < s.index('<script id="v26-rivals">'):
    sys.exit("HATA: v26-measure, v26-rivals'tan sonra olmalı")
open(p, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
