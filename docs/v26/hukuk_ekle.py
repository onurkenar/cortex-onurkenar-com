# -*- coding: utf-8 -*-
"""8.13 Hukuk & İş Gücü (2026-11-15).
Kullanım: python3 -I docs/v26/hukuk_ekle.py <html>
<style id="v26-legal"> ← docs/v26/v26-legal.css, <script id="v26-legal"> ← docs/v26/v26-legal.js (v26-mobile'dan önce; betik
v26-measure'dan sonra — 8.2–8.10'un kayıtlarını okur). Varsa yerinde yenilenir; tekrar çalıştırılabilir. Veri (bölüm ip_legal, üç
alan type "records"): docs/icerik-planlama/plan_alani_ekle.py."""
import hashlib, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-legal.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-legal.css", encoding="utf-8").read().strip()
for t in (JS, CSS):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-records">', '<script id="v26-measure">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce olcum_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-legal">.*?</style>\n', '<style id="v26-legal">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-legal">.*?</script>\n', '<script id="v26-legal">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if s.index('<script id="v26-legal">') < s.index('<script id="v26-measure">'):
    sys.exit("HATA: v26-legal, v26-measure'dan sonra olmalı")
open(p, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
