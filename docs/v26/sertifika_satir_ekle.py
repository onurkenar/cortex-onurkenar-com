"""Sertifikalar ve Belgeler satır düzenleyicisi (2026-11-15) — docs/v26/v26-certs.{js,css}.
Kullanım: python3 -I docs/v26/sertifika_satir_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kanca yalnız eksikse eklenir.
Kanca: one() — CERT_F'deki metin kararı textarea yerine satır düzenleyicisiyle (certInput) çizilir. Değer metin olarak kalır,
bu yüzden isset / ruleBase / ocVal / dışa aktarım kancası gerekmez."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-certs.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-certs.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1) JS bloğu: one()'ın hemen önünde (FI tanımlıdır)
B, E_ = "/*V26-CERTS:BEGIN*/", "/*V26-CERTS:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
# 2) CSS bloğu: v26-mobile'dan önce
st = '<style id="v26-certs">' + css + "</style>"
if '<style id="v26-certs">' in s:
    s = re.sub(r'<style id="v26-certs">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
# 3) kanca
once('else if(f.type==="textarea")c=`<textarea', 'else if(CERT_F[f.id])c=certInput(f);else if(f.type==="textarea")c=`<textarea')
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
