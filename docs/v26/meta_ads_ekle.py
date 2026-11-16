# -*- coding: utf-8 -*-
"""8.10 Meta Ads (2026-11-15).
Kullanım: python3 -I docs/v26/meta_ads_ekle.py <html>
<style id="v26-meta-ads"> ← docs/v26/v26-meta-ads.css, <script id="v26-meta-ads"> ← docs/v26/v26-meta-ads.js (v26-mobile'dan önce;
betik v26-gads'ten sonra — window.BL (8.3), window.prItems (8.2), window.SP (8.4) ve kayıt çekirdeği ondan önce gelir). Dikkat:
id="v26-meta" Pazarlama › Meta Servisleri modülüdür (docs/v26/v26-meta.js → docs/meta/arayuz_ekle.py); bu betik ona dokunmaz.
Varsa yerinde yenilenir; tekrar çalıştırılabilir. Veri (bölüm ip_meta, dört alan type "records"): docs/icerik-planlama/plan_alani_ekle.py."""
import hashlib, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-meta-ads.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-meta-ads.css", encoding="utf-8").read().strip()
for t in (JS, CSS):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-records">', '<script id="v26-gads">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce google_ads_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-meta-ads">.*?</style>\n', '<style id="v26-meta-ads">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-meta-ads">.*?</script>\n', '<script id="v26-meta-ads">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if s.index('<script id="v26-meta-ads">') < s.index('<script id="v26-gads">'):
    sys.exit("HATA: v26-meta-ads, v26-gads'ten sonra olmalı")
open(p, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
