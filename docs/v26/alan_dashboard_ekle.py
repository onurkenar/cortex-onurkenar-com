# -*- coding: utf-8 -*-
"""Ana menü dashboard'ları (2026-11-15, kullanıcı isteği: "her ana menünün kendi dashboardı olsun").
Kullanım: python3 -I docs/v26/alan_dashboard_ekle.py web-proje-gelistirme.html
<style id="v26-area-dash"> (</head> öncesi) ve <script id="v26-area-dash"> (</body> öncesi, en son betik — goArea, showPage,
renderSideNav ve renderProgress'i en dıştan sarmalar) ← docs/v26/v26-area-dash.{css,js}. Tekrar çalıştırılabilir: bloklar yerinde yenilenir."""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-area-dash.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-area-dash.css", encoding="utf-8").read().strip()


def put(s, tag, body, anchor):
    block = f'<{tag} id="v26-area-dash">\n{body}\n</{tag}>'
    m = re.search(rf'<{tag} id="v26-area-dash">.*?</{tag}>', s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    if s.count(anchor) != 1:
        sys.exit("HATA: bağlantı noktası tek değil: " + anchor)
    return s.replace(anchor, block + "\n" + anchor)


p = sys.argv[1]
s = open(p, encoding="utf-8").read()
s = put(s, "style", CSS, "</head>")
s = put(s, "script", JS, "</body></html>")
open(p, "w", encoding="utf-8").write(s)
print("tamam:", p)
