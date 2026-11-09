#!/usr/bin/env python3
"""Çalışma saatleri ("hours" alan tipi), Vergi ve Sicil ile Konum Koordinatı göçlerini uygulamaya yazar (2026-11-09).

Kullanım: python3 -I docs/v26/calisma_saatleri_ekle.py web-proje-gelistirme.html

  - docs/v26/v26-hours.js  → ana betikte /*V26-HOURS:BEGIN*/ … /*V26-HOURS:END*/ arasına (yoksa function one(f){ öncesine)
  - docs/v26/v26-hours.css → <style id="v26-hours"> (yoksa </head> öncesine)
  - ana betik kancaları (yalnız eksikse): isset, ruleBase, ocVal, one, accInput (noOther), ocMig sonu
Tekrar çalıştırılabilir; DATA'ya dokunmaz (alan tanımları docs/ortak-bilgiler/ortak-bilgiler.json'da).
"""
import hashlib, os, re, sys

D = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
s = open(hp, encoding="utf-8").read()
js = open(os.path.join(D, "v26-hours.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-hours.css"), encoding="utf-8").read().strip()
for t in (js, css):
    if "</script" in t or "<!--" in t or "</style" in t:
        sys.exit("HATA: kaynakta </script, </style ya da <!-- var")

def once(old, new, done):
    global s
    if done in s:
        return
    if s.count(old) != 1:
        sys.exit(f"HATA: {old[:60]!r} {s.count(old)} kez geçiyor")
    s = s.replace(old, new)

B, E_ = "/*V26-HOURS:BEGIN*/", "/*V26-HOURS:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    once("function one(f){", blk + "function one(f){", B)

st = '<style id="v26-hours">\n' + css + "\n</style>"
if '<style id="v26-hours">' in s:
    s = re.sub(r'<style id="v26-hours">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    once("</head>", st + "</head>", '<style id="v26-hours">')

once('f.type==="accounts"?accList(f).length>0:', 'f.type==="hours"?hrHas(f):f.type==="accounts"?accList(f).length>0:', 'f.type==="hours"?hrHas(f)')
once('let v=f.type==="accounts"?accText(f):state[f.id],', 'let v=f.type==="accounts"?accText(f):f.type==="hours"?hrText(f,1):state[f.id],', 'f.type==="hours"?hrText(f,1)')
once('if(f.type==="accounts")return li(accList(f)', 'if(f.type==="hours")return li(hrLines(f),9);if(f.type==="accounts")return li(accList(f)', 'return li(hrLines(f),9)')
once('else if(f.type==="accounts")c=accInput(f);', 'else if(f.type==="accounts")c=accInput(f);else if(f.type==="hours")c=hrInput(f);', 'c=hrInput(f)')
once('${accGroups(f,g,src)}<label class="accRow accOther"', '${accGroups(f,g,src)}${f.noOther?"":`<label class="accRow accOther"', 'f.noOther?"":')
once('oninput="setAcc(\'${f.id}\',\'diger\',this)">${E(v.diger||"")}</textarea></label></div>`}', 'oninput="setAcc(\'${f.id}\',\'diger\',this)">${E(v.diger||"")}</textarea></label>`}</div>`}', '</textarea></label>`}</div>`}')
once("ocCtMig(st,has)}", "ocCtMig(st,has);ocHrMig(st);ocTaxMig(st);ocGeoMig(st)}", "ocHrMig(st);ocTaxMig(st);ocGeoMig(st)")

open(hp, "w", encoding="utf-8").write(s)
print("md5", hashlib.md5(s.encode("utf-8")).hexdigest())
