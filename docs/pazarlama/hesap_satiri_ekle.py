# -*- coding: utf-8 -*-
"""kilavuz-alanlari.json'daki accountsAdd satırlarını uygulamaya yazar (2026-11-11).
Kullanım: python3 -I docs/pazarlama/hesap_satiri_ekle.py web-proje-gelistirme.html docs/pazarlama/kilavuz-alanlari.json
kilavuz_ekle.py'nin 5. adımının (accounts satırları) aynısıdır: satır `after`'dan sonra eklenir ve kimliği
DATA.guideKit.added.accounts[alan]'a yazılır — böylece kilavuz_ekle.py yeniden çalışınca satırı geri alıp yeniden ekler.
Neden ayrı: kilavuz_ekle.py 2026-11-09'dan beri önceden var olan bir denetimde duruyor
(design_hero recommend → page_design_style "Accessible-First"; CLAUDE.md'deki not). Tekrar çalıştırılabilir:
var olan satıra dokunmaz."""
import copy, hashlib, json, sys

hp, sp = sys.argv[1:3]
h = open(hp, encoding='utf-8').read()
MARK = 'const DATA='
if h.count(MARK) != 1:
    sys.exit('HATA: DATA satırı bulunamadı')
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
src = json.load(open(sp, encoding='utf-8'))
FI = {f['id']: f for f in D['fields']}
acc = D['guideKit']['added'].setdefault('accounts', {})
n = 0
for spec in src.get('accountsAdd', []):
    fid = spec['field']
    f = FI.get(fid)
    if not f or f['type'] != 'accounts':
        sys.exit('HATA: accounts alanı değil ' + fid)
    rows = f.setdefault('accounts', [])
    prev = spec.get('after')
    for r in spec['rows']:
        if not r.get('k') or not r.get('label') or not r.get('ph'):
            sys.exit('HATA: satır hatalı %s' % r)
        for c in r.get('when') or []:
            if c['field'] not in FI:
                sys.exit('HATA: when alanı yok %s' % c['field'])
            vals = [o['value'] for o in FI[c['field']].get('options') or []] if FI[c['field']]['type'] != 'boolean' else [True, False]
            if any(v not in vals for v in c['in']):
                sys.exit('HATA: when değeri yok %s' % c)
        if not any(x['k'] == r['k'] for x in rows):
            pos = len(rows) if not prev else next((k + 1 for k, x in enumerate(rows) if x['k'] == prev), None)
            if pos is None:
                sys.exit('HATA: after yok %s' % prev)
            rows.insert(pos, copy.deepcopy(r))
            n += 1
        if r['k'] not in acc.setdefault(fid, []):
            acc[fid].append(r['k'])
        prev = r['k']
out = json.dumps(D, ensure_ascii=False)
for bad in ('</script', '<!--'):
    if bad in out:
        sys.exit('HATA: DATA içinde yasak dizi ' + bad)
h = h[:i] + out + h[end:]
open(hp, 'w', encoding='utf-8').write(h)
print('tamam: %d satır eklendi · md5 %s · boyut %d' % (n, hashlib.md5(h.encode('utf-8')).hexdigest(), len(h.encode('utf-8'))))
