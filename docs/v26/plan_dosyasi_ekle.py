# -*- coding: utf-8 -*-
"""Plan Dosyası düzeltmeleri (2026-11-15).
Kullanım: python3 -I docs/v26/plan_dosyasi_ekle.py <html> [<icerik_planlama klasörü>]
1) <script id="v26-planfile"> ← docs/v26/v26-planfile.js (v26-mobile betiğinden önce; varsa yerinde yenilenir).
2) DATA.marketingTemplate.surum → SURUM. Klasör verilirse önce şablonun kaynak/surum.json sürümü okunur ve
   kaynak/veri.bos.json ile gömülü iskelet (marketingTemplate.bos) karşılaştırılır; fark varsa betik durur (iskelet
   elle güncellenmeli). Özgün sürüm DATA.planfileKit.orig'e yazılır. Tekrar çalıştırılabilir."""
import hashlib, json, os, re, sys

SURUM = "1.50.0"
HERE = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
tpl = sys.argv[2] if len(sys.argv) > 2 else None
JS = open(os.path.join(HERE, "v26-planfile.js"), encoding="utf-8").read().strip()
if "</script" in JS.lower() or "<!--" in JS:
    sys.exit("HATA: kaynakta </script ya da <!-- var")
h = open(hp, encoding="utf-8").read()
MARK = "const DATA="
if h.count(MARK) != 1:
    sys.exit("HATA: DATA satırı bulunamadı")
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
M = D.get("marketingTemplate")
if not isinstance(M, dict) or "bos" not in M:
    sys.exit("HATA: marketingTemplate yok")
if tpl:
    sv = json.load(open(os.path.join(tpl, "kaynak", "surum.json"), encoding="utf-8")).get("surum")
    bos = json.load(open(os.path.join(tpl, "kaynak", "veri.bos.json"), encoding="utf-8"))
    if bos != M["bos"]:
        fark = sorted(k for k in set(bos) | set(M["bos"]) if bos.get(k) != M["bos"].get(k))
        sys.exit("HATA: şablon iskeleti gömülü iskeletten farklı: " + ", ".join(fark))
    if sv != SURUM:
        sys.exit("HATA: şablon sürümü %s, betikteki SURUM %s — betiği güncelleyin" % (sv, SURUM))
kit = D.setdefault("planfileKit", {})
kit.setdefault("orig", {}).setdefault("surum", M.get("surum"))
M["surum"] = SURUM
out = json.dumps(D, ensure_ascii=False)
for bad in ("</script", "<!--"):
    if bad in out:
        sys.exit("HATA: DATA içinde yasak dizi " + bad)
h = h[:i] + out + h[end:]
a = '<script id="v26-mobile">'
if h.count(a) != 1:
    sys.exit("HATA: tek olmalı: " + a)
js = '<script id="v26-planfile">\n' + JS + "\n</script>\n"
m = re.search(r'<script id="v26-planfile">.*?</script>\n', h, flags=re.S)
h = h[:m.start()] + js + h[m.end():] if m else h.replace(a, js + a)
open(hp, "w", encoding="utf-8").write(h)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(h.encode("utf-8")).hexdigest(), len(h.encode("utf-8"))))
