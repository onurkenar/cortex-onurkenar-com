"""Referanslar satır düzenleyicisi (2026-11-15) — docs/v26/v26-refs.{js,css}.
Kullanım: python3 -I docs/v26/referans_satir_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kanca yalnız eksikse eklenir.
Kanca: one() — REF_F'deki metin kararı textarea yerine satır düzenleyicisiyle (refInput) çizilir. Değer metin olarak kalır,
bu yüzden isset / ruleBase / ocVal / dışa aktarım kancası gerekmez. Alan açıklaması ve kuralı DATA'dadır
(docs/ortak-bilgiler/kanit_ayir_ekle.py › FIELDS)."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-refs.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-refs.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

B, E_ = "/*V26-REFS:BEGIN*/", "/*V26-REFS:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
st = '<style id="v26-refs">' + css + "</style>"
if '<style id="v26-refs">' in s:
    s = re.sub(r'<style id="v26-refs">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
once('else if(CERT_F[f.id])c=certInput(f);', 'else if(REF_F[f.id])c=refInput(f);else if(CERT_F[f.id])c=certInput(f);')
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
