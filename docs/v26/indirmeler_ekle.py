#!/usr/bin/env python3
"""Dashboard › İndirmeler bölümünü ekler (2026-11-12).

Kullanım: python3 -I docs/v26/indirmeler_ekle.py web-proje-gelistirme.html
<style id="v26-downloads"> ← docs/v26/v26-downloads.css (v26-approval stilinden önce), <script id="v26-downloads"> ←
docs/v26/v26-downloads.js (</body> öncesi; bütün üretici fonksiyonlardan sonra). Bloklar varsa yerinde yenilenir (sıra
korunur, tekrar çalıştırmada dosya aynı kalır). DATA'ya dokunmaz.
"""
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CSS = open(os.path.join(HERE, "v26-downloads.css"), encoding="utf-8").read().strip()
JS = open(os.path.join(HERE, "v26-downloads.js"), encoding="utf-8").read().strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: indirmeler_ekle.py <html>")
    if "</script" in JS.lower() or "<!--" in JS:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    for a in ('<style id="v26-approval">', "</body>", 'id="overviewPage"'):
        if a != 'id="overviewPage"' and s.count(a) != 1:
            sys.exit("HATA: tek olmalı: " + a)
    css = '<style id="v26-downloads">\n' + CSS + "\n</style>\n"
    m = re.search(r'<style id="v26-downloads">.*?</style>\n', s, flags=re.S)
    s = s[:m.start()] + css + s[m.end():] if m else s.replace('<style id="v26-approval">', css + '<style id="v26-approval">')
    js = '<script id="v26-downloads">\n' + JS + "\n</script>\n"
    m = re.search(r'<script id="v26-downloads">.*?</script>\n', s, flags=re.S)
    s = s[:m.start()] + js + s[m.end():] if m else s.replace("</body>", js + "</body>")
    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
