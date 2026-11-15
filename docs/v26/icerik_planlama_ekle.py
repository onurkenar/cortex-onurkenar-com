#!/usr/bin/env python3
"""İçerik Planlama menüsünü (yer tutucu sayfa) ekler (2026-11-15).

Kullanım: python3 -I docs/v26/icerik_planlama_ekle.py web-proje-gelistirme.html
<style id="v26-content-plan"> ← docs/v26/v26-content-plan.css (v26-mobile stilinden önce), <script id="v26-content-plan"> ← docs/v26/v26-content-plan.js
(v26-mobile betiğinden önce, v26-todo betiğinden sonra — showPage sarmalayıcısı onunkini sarar). Bloklar varsa yerinde
yenilenir (sıra korunur, tekrar çalıştırmada dosya aynı kalır). DATA'ya dokunmaz.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "v26-content-plan.css"), encoding="utf-8").read().strip()
JS = open(os.path.join(HERE, "v26-content-plan.js"), encoding="utf-8").read().strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: icerik_planlama_ekle.py <html>")
    if "</script" in JS.lower() or "<!--" in JS:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    for a in ('<style id="v26-mobile">', '<script id="v26-mobile">'):
        if s.count(a) != 1:
            sys.exit("HATA: tek olmalı: " + a)
    css = '<style id="v26-content-plan">\n' + CSS + "\n</style>\n"
    m = re.search(r'<style id="v26-content-plan">.*?</style>\n', s, flags=re.S)
    s = s[:m.start()] + css + s[m.end():] if m else s.replace('<style id="v26-mobile">', css + '<style id="v26-mobile">')
    js = '<script id="v26-content-plan">\n' + JS + "\n</script>\n"
    m = re.search(r'<script id="v26-content-plan">.*?</script>\n', s, flags=re.S)
    s = s[:m.start()] + js + s[m.end():] if m else s.replace('<script id="v26-mobile">', js + '<script id="v26-mobile">')
    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
