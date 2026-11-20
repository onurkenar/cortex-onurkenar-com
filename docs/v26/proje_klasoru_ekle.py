# -*- coding: utf-8 -*-
"""Proje dosyasının klasörü (2026-11-20) — docs/v26/v26-project-dir.{js,css}.
Kullanım: python3 -I docs/v26/proje_klasoru_ekle.py web-proje-gelistirme.html
<style id="v26-project-dir"> v26-mobile stilinden önce, <script id="v26-project-dir"> v26-area-dash betiğinden önce (o en son betik kalır).
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir. Ana betiğe ve DATA'ya dokunmaz."""
import hashlib, os, re, sys

H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-project-dir.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-project-dir.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t and "</style" not in t


def put(tag, body, anchor):
    global s
    blk = '<%s id="v26-project-dir">\n%s\n</%s>\n' % (tag, body, tag)
    pat = re.compile(r'<%s id="v26-project-dir">.*?</%s>\n' % (tag, tag), re.S)
    if pat.search(s):
        s = pat.sub(lambda m: blk, s, count=1)
    else:
        assert s.count(anchor) == 1, (anchor, s.count(anchor))
        s = s.replace(anchor, blk + anchor)


put("style", css, '<style id="v26-mobile">')
put("script", js, '<script id="v26-area-dash">')
open(H, "w", encoding="utf-8").write(s)
print("tamam · md5 %s · boyut %d" % (hashlib.md5(s.encode("utf-8")).hexdigest(), len(s.encode("utf-8"))))
