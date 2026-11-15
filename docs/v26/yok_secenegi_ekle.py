"""Serbest metin kararlarında "yok" seçeneği (2026-11-15) — docs/v26/v26-none.{js,css}.
Kullanım: python3 -I docs/v26/yok_secenegi_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kancalar yalnız eksikse eklenir.
Kancalar: isset (işaretliyse verilmiş), ruleBase (NONE_F kuralı), ocVal (Ortak Bilgiler kartında etiket),
one() (metin kutusunun altında işaret kutusu)."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-none.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-none.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

B, E_ = "/*V26-NONE:BEGIN*/", "/*V26-NONE:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
st = '<style id="v26-none">' + css + "</style>"
if '<style id="v26-none">' in s:
    s = re.sub(r'<style id="v26-none">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
once('function isset(f){let v=state[f.id];', 'function isset(f){if(typeof noneOn==="function"&&noneOn(f))return true;let v=state[f.id];')
once('function ruleBase(f){if(!isset(f))return"";', 'function ruleBase(f){if(!isset(f))return"";if(typeof noneOn==="function"&&noneOn(f))return noneRule(f);')
once("function ocVal(f){if(!isset(f))return '<span class=\"ocEmpty\">Girilmedi</span>';",
     "function ocVal(f){if(!isset(f))return '<span class=\"ocEmpty\">Girilmedi</span>';if(typeof noneOn===\"function\"&&noneOn(f))return E(NONE_F[f.id].label);")
once('${c}${other}', '${c}${noneBox(f)}${other}')
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
