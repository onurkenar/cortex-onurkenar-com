#!/usr/bin/env python3
"""Sol menü numaralandırmasını ekler (2026-11-11).

Kullanım: python3 -I docs/v26/menu_numara_ekle.py web-proje-gelistirme.html
<style id="v26-nav-numbers"> ← docs/v26/v26-nav-numbers.css (v26-approval stilinden önce), <script id="v26-nav-numbers">
← docs/v26/v26-nav-numbers.js (</body> öncesi, son betik — V26'nın renderSideNav sarmalayıcısından sonra çalışmalı).
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yenilenir.
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
CSS = open(ROOT + "/docs/v26/v26-nav-numbers.css", encoding="utf-8").read().strip()
JS = open(ROOT + "/docs/v26/v26-nav-numbers.js", encoding="utf-8").read().strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: menu_numara_ekle.py <html>")
    if "</script" in JS.lower() or "<!--" in JS:
        sys.exit("HATA: kaynakta </script ya da <!-- var")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'<style id="v26-nav-numbers">.*?</style>\n?', "", s, flags=re.S)
    s = re.sub(r'<script id="v26-nav-numbers">.*?</script>\n?', "", s, flags=re.S)
    for a in ('<style id="v26-approval">', "</body>", '<script id="v26-ux-refresh-js">'):
        if s.count(a) != 1:
            sys.exit("HATA: tek olmalı: " + a)
    s = s.replace('<style id="v26-approval">', '<style id="v26-nav-numbers">\n' + CSS + '\n</style>\n<style id="v26-approval">')
    s = s.replace("</body>", '<script id="v26-nav-numbers">\n' + JS + "\n</script>\n</body>")
    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
