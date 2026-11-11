#!/usr/bin/env python3
"""Sol menüde açık olan yeri kırmızı işaretleyen stil bloğunu ekler (2026-11-11).

Kullanım: python3 -I docs/v26/aktif_kirmizi_ekle.py web-proje-gelistirme.html
<style id="v26-active-red"> ← docs/v26/v26-active-red.css; v26-approval stilinden önce (v12 / v17 / v26-done-items'tan
sonra gelmeli ki aynı özgüllükteki kuralları geçsin). Tekrar çalıştırılabilir: blok varsa kaynaktan yenilenir.
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
CSS = open(ROOT + "/docs/v26/v26-active-red.css", encoding="utf-8").read().strip()


def main():
    if len(sys.argv) != 2:
        sys.exit("kullanım: aktif_kirmizi_ekle.py <html>")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    s = re.sub(r'<style id="v26-active-red">.*?</style>\n?', "", s, flags=re.S)
    anchor = '<style id="v26-approval">'
    if s.count(anchor) != 1 or s.index('<style id="v26-done-items">') > s.index(anchor):
        sys.exit("HATA: v26-approval / v26-done-items stil bloğu beklenen yerde değil")
    s = s.replace(anchor, '<style id="v26-active-red">\n' + CSS + "\n</style>\n" + anchor)
    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
