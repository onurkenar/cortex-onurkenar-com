#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Metin kararlarında yumuşak biçim denetimi betiğini ekler (2026-11-23).

Kullanım: python3 -I docs/v26/metin_denetim_ekle.py web-proje-gelistirme.html
<script id="v26-textcheck"> ← docs/v26/v26-textcheck.js; v26-mobile betiğinden önce (renderFields / refreshField'i
saran diğer bloklardan sonra). Tekrar çalıştırılabilir: blok varsa kaynaktan yerinde yenilenir.
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-textcheck.js", encoding="utf-8").read().strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: metin_denetim_ekle.py <html>")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    if "</script" in JS.lower() or "<!--" in JS:
        sys.exit("HATA: betikte yasak dizi")
    block = '<script id="v26-textcheck">\n' + JS + "\n</script>\n"
    m = re.search(r'<script id="v26-textcheck">.*?</script>\n', s, flags=re.S)
    if m:
        s = s[:m.start()] + block + s[m.end():]
    else:
        anchor = '<script id="v26-mobile">'
        if s.count(anchor) != 1 or s.index('<script id="v26-consistency">') > s.index(anchor):
            sys.exit("HATA: v26-mobile / v26-consistency betiği beklenen yerde değil")
        s = s.replace(anchor, block + anchor)
    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
