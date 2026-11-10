# -*- coding: utf-8 -*-
"""4 Göz Onay Akışı arayüzü (akış diyagramı, durum göstergeleri, anahtar) — tekrar çalıştırılabilir (2026-11-10).
Kullanım: python3 -I docs/v26/onay_arayuz_ekle.py web-proje-gelistirme.html
<style id="v26-approval"> head sonuna, <script id="v26-approval"> body sonuna; varsa içerikleri kaynaktan yenilenir.
Kararlar ve kurallar ayrı: docs/onay-akisi/onay_ekle.py (önce o çalıştırılır)."""
import sys, os, hashlib

D = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
h = open(hp, encoding='utf-8').read()
css = open(os.path.join(D, 'v26-approval.css'), encoding='utf-8').read()
js = open(os.path.join(D, 'v26-approval.js'), encoding='utf-8').read()
for bad in ('</script', '<!--'):
    assert bad not in js and bad not in css, bad


def block(tag, body):
    global h
    op, cl = '<%s id="v26-approval">\n' % tag, '</%s>' % tag
    if op in h:
        i = h.index(op) + len(op)
        h = h[:i] + body + h[h.index(cl, i):]
    elif tag == 'style':
        assert h.count('</head>') == 1
        k = h.index('</head>')
        h = h[:k] + op + body + cl + '\n' + h[k:]
    else:
        k = h.rindex('</body>')
        h = h[:k] + op + body + cl + '\n' + h[k:]


block('style', css)
block('script', js)
open(hp, 'w', encoding='utf-8').write(h)
print('tamam · md5', hashlib.md5(h.encode('utf-8')).hexdigest(), '· boyut', len(h.encode('utf-8')))
