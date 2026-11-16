# -*- coding: utf-8 -*-
"""8.8 Etkinlikler (2026-11-15).
Kullanım: python3 -I docs/v26/etkinlik_ekle.py <html>
<style id="v26-events"> ← docs/v26/v26-events.css, <script id="v26-events"> ← docs/v26/v26-events.js (v26-mobile'dan önce; betik
v26-mailing'den sonra olmalı — window.BL (8.3) ve kayıt çekirdeği ondan önce gelir). Betikteki /*ET_STD*/[] ve /*ET_KISA*/[]
yer tutucuları docs/icerik-planlama/etkinlik-standart-plan.json'dan (şablonun standart etkinlik planı, markasız) doldurulur.
Varsa yerinde yenilenir; tekrar çalıştırılabilir. Veri (bölüm ip_events, alan ip_events_rec type "records"):
docs/icerik-planlama/plan_alani_ekle.py. Takvim bağlantısı: docs/v26/v26-calendar.js (window.ET.cal)."""
import hashlib, json, re, sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-events.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-events.css", encoding="utf-8").read().strip()
PLAN = json.load(open(ROOT + "/docs/icerik-planlama/etkinlik-standart-plan.json", encoding="utf-8"))
assert len(PLAN["plan"]) == 29 and all(0 <= i < 29 for i in PLAN["kisa"])
raw = json.dumps(PLAN["plan"], ensure_ascii=False, separators=(",", ":"))
for bad in ("KVKK Rehberi", "#KVKK", "KVKKR"):
    if bad in raw:
        sys.exit("HATA: standart planda markaya özgü ifade var: " + bad)
for a in ("/*ET_STD*/[]", "/*ET_KISA*/[]"):
    if JS.count(a) != 1:
        sys.exit("HATA: betikte tek olmalı: " + a)
JS = JS.replace("/*ET_STD*/[]", raw).replace("/*ET_KISA*/[]", json.dumps(PLAN["kisa"]))
for t in (JS, CSS):
    if "</script" in t.lower() or "<!--" in t:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
p = sys.argv[1]
s = open(p, encoding="utf-8").read()
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">', '<script id="v26-records">', '<script id="v26-mailing">'):
    if s.count(a) != 1:
        sys.exit("HATA: tek olmalı: " + a + " (önce mailing_ekle.py)")


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    return s.replace(anchor, block + anchor)


s = put(s, r'<style id="v26-events">.*?</style>\n', '<style id="v26-events">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
s = put(s, r'<script id="v26-events">.*?</script>\n', '<script id="v26-events">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')
if s.index('<script id="v26-events">') < s.index('<script id="v26-mailing">'):
    sys.exit("HATA: v26-events, v26-mailing'den sonra olmalı")
open(p, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
