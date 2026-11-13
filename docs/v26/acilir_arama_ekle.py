"""Açılır listelerde arama (2026-11-13) — docs/v26/v26-select-search.{js,css}.
Kullanım: python3 -I docs/v26/acilir_arama_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir; yoksa stil v26-mobile stilinden önce,
betik </body>'den hemen önce (son betik) eklenir. Ana betiğe ve veriye dokunmaz."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-select-search.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-select-search.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t
st = '<style id="v26-select-search">' + css + "</style>"
sc = '<script id="v26-select-search">\n' + js + "\n</script>"
if '<style id="v26-select-search">' in s:
    s = re.sub(r'<style id="v26-select-search">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'; assert s.count(a) == 1; s = s.replace(a, st + a)
if '<script id="v26-select-search">' in s:
    s = re.sub(r'<script id="v26-select-search">.*?</script>', lambda m: sc, s, count=1, flags=re.S)
else:
    assert s.rstrip().endswith("</body></html>")
    i = s.rindex("</body>"); s = s[:i] + sc + "\n" + s[i:]
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
