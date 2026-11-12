# -*- coding: utf-8 -*-
"""kilavuz-alanlari.json'daki fields[] içinden uygulamada henüz olmayan alanları DATA'ya yazar (2026-11-12).
Kullanım: python3 -I docs/pazarlama/alan_ekle.py web-proje-gelistirme.html docs/pazarlama/kilavuz-alanlari.json
kilavuz_ekle.py'nin alan adımının aynısıdır: alan `after`'dan sonra (yoksa bölümün sonuna) eklenir ve kimliği
DATA.guideKit.added.fields'e yazılır — böylece kilavuz_ekle.py yeniden çalışınca alanı geri alıp yeniden ekler.
Neden ayrı: kilavuz_ekle.py 2026-11-09'dan beri önceden var olan bir denetimde duruyor
(design_hero recommend → page_design_style "Accessible-First"; hesap_satiri_ekle.py ile aynı durum).
Var olan alana dokunmaz; tekrar çalıştırılabilir. Denetimler: zorunlu metinler, rule yer tutucusu, boolean'da
yes / no, showIf alan ve değerleri, ajan kimliklerinin pozisyon ajanı biçimi."""
import copy, hashlib, json, sys

PH = {"select": "{label}", "multiselect": "{labels}", "boolean": "{booltext}", "text": "{value}",
      "textarea": "{value}", "url": "{value}", "color": "{value}", "accounts": "{value}"}
hp, sp = sys.argv[1:3]
h = open(hp, encoding='utf-8').read()
MARK = 'const DATA='
if h.count(MARK) != 1:
    sys.exit('HATA: DATA satırı bulunamadı')
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
src = json.load(open(sp, encoding='utf-8'))
FI = {f['id']: f for f in D['fields']}
SI = {s['id'] for s in D['sections']}
added = D['guideKit']['added'].setdefault('fields', [])
n = 0
for spec in src.get('fields', []):
    fid = spec['id']
    if fid in FI:
        if fid not in added:
            added.append(fid)
        continue
    f = copy.deepcopy(spec)
    after = f.pop('after', None)
    for k in ('label', 'en', 'type', 'explanation', 'rule', 'scenario', 'example'):
        if not f.get(k):
            sys.exit('HATA: %s eksik %s' % (fid, k))
    if f['section'] not in SI:
        sys.exit('HATA: bölüm yok ' + f['section'])
    if f['type'] not in PH or PH[f['type']] not in f['rule']:
        sys.exit('HATA: %s rule yer tutucusu' % fid)
    if f['type'] == 'boolean' and not (f.get('yes') and f.get('no')):
        sys.exit('HATA: %s yes / no eksik' % fid)
    for o in f.get('options') or []:
        for k in ('label', 'explanation', 'scenario', 'example'):
            if not o.get(k):
                sys.exit('HATA: %s seçenek %s eksik' % (fid, k))
    for c in f.get('showIf') or []:
        g = FI.get(c['field'])
        if not g:
            sys.exit('HATA: showIf alanı yok ' + c['field'])
        vals = [True, False] if g['type'] == 'boolean' else [o['value'] for o in g.get('options') or []]
        if any(v not in vals for v in c['in']):
            sys.exit('HATA: showIf değeri yok %s' % c)
    for a in f.get('agents') or []:
        if not a.startswith('poz:') or a.count(':') != 2:
            sys.exit('HATA: ajan kimliği ' + a)
    L = D['fields']
    if after:
        if after not in FI or FI[after]['section'] != f['section']:
            sys.exit('HATA: %s after alanı bu bölümde değil %s' % (fid, after))
        pos = next(k for k, x in enumerate(L) if x['id'] == after) + 1
    else:
        pos = max(k for k, x in enumerate(L) if x['section'] == f['section']) + 1
    L.insert(pos, f)
    FI[fid] = f
    added.append(fid)
    n += 1
out = json.dumps(D, ensure_ascii=False)
for bad in ('</script', '<!--'):
    if bad in out:
        sys.exit('HATA: DATA içinde yasak dizi ' + bad)
h = h[:i] + out + h[end:]
open(hp, 'w', encoding='utf-8').write(h)
print('tamam: %d alan eklendi · md5 %s · boyut %d' % (n, hashlib.md5(h.encode('utf-8')).hexdigest(), len(h.encode('utf-8'))))
