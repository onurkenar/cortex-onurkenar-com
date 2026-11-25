# -*- coding: utf-8 -*-
"""kilavuz-alanlari.json'daki yeni bölümleri ve eksik seçenekleri uygulamaya yazar (2026-11-25).
Kullanım: python3 -I docs/pazarlama/bolum_secenek_ekle.py web-proje-gelistirme.html docs/pazarlama/kilavuz-alanlari.json [--set id1,id2]
kilavuz_ekle.py'nin 1. (bölümler), 3. (optionAdd) ve 9. (kodlar) adımlarının, yalnız eksik olanlar için olan karşılığıdır:
- sections[]: uygulamada olmayan bölüm `after`'dan sonra eklenir, rehberi sectionGuides'a yazılır, kimliği
  DATA.guideKit.added.sections'a eklenir (kilavuz_ekle.py yeniden çalışınca geri alıp yeniden ekler).
- optionAdd[]: alanda olmayan seçenek, kaynaktaki bir önceki seçenekten (ilk seçenekte spec.after'dan) sonra eklenir;
  değeri guideKit.added.options[alan]'a yazılır.
- --set id1,id2: fieldSet[] içindeki bu alanların yalnız `showIf` değeri DATA'ya yazılır (özgün değer kilavuz_ekle.py'nin
  geri alma kaydında zaten duruyor). Başka betiklerin değiştirdiği anahtarlara dokunmamak için yalnız adı verilen alanlar.
- Bölüm kodları sıradan yeniden üretilir (%02d), pazarlama gruplarının ardışık olduğu denetlenir.
Neden ayrı: kilavuz_ekle.py 2026-11-09'dan beri önceden var olan bir denetimde duruyor (alan_ekle.py ile aynı durum).
Tekrar çalıştırılabilir; var olana dokunmaz. Yeni bölümün alanları ardından alan_ekle.py ile eklenir."""
import copy, hashlib, json, sys

hp, sp = sys.argv[1:3]
SET = set(sys.argv[sys.argv.index('--set') + 1].split(',')) if '--set' in sys.argv else set()
h = open(hp, encoding='utf-8').read()
MARK = 'const DATA='
if h.count(MARK) != 1:
    sys.exit('HATA: DATA satırı bulunamadı')
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
src = json.load(open(sp, encoding='utf-8'))
A = D['guideKit']['added']
secs = D['sections']
ns = no = nf = 0
for sec in src.get('sections', []):
    sid = sec['id']
    if any(x['id'] == sid for x in secs):
        continue
    for k in ('name', 'en', 'desc', 'group', 'icon', 'after'):
        if not str(sec.get(k, '')).strip():
            sys.exit('HATA: %s: %s boş' % (sid, k))
    g = sec.get('guide') or {}
    if not g.get('purpose') or len(g.get('criteria', [])) < 3 or len(g.get('pitfalls', [])) < 3 or len(g.get('resources', [])) < 2:
        sys.exit('HATA: %s: rehber eksik' % sid)
    for r in g['resources']:
        if not str(r.get('url', '')).startswith('https://') or not r.get('title') or not r.get('note'):
            sys.exit('HATA: %s: kaynak hatalı %s' % (sid, r))
    pos = next((k for k, x in enumerate(secs) if x['id'] == sec['after']), None)
    if pos is None:
        sys.exit('HATA: %s: after bölümü yok %s' % (sid, sec['after']))
    secs.insert(pos + 1, {'id': sid, 'code': '', 'name': sec['name'], 'desc': sec['desc'], 'en': sec['en'],
                          'group': sec['group'], 'area': 'marketing', 'icon': sec['icon']})
    D['sectionGuides'][sid] = {k: g[k] for k in ('purpose', 'criteria', 'pitfalls', 'resources')}
    if sid not in A.setdefault('sections', []):
        A['sections'].append(sid)
    ns += 1
FI = {f['id']: f for f in D['fields']}
for spec in src.get('optionAdd', []):
    f = FI.get(spec['field'])
    if not f or f['type'] not in ('select', 'multiselect'):
        sys.exit('HATA: optionAdd alanı yok ya da seçenekli değil ' + spec['field'])
    ops = f.setdefault('options', [])
    prev = spec.get('after')
    for o in spec['options']:
        if not any(x['value'] == o['value'] for x in ops):
            for k in ('label', 'explanation', 'scenario', 'example'):
                if not o.get(k):
                    sys.exit('HATA: %s.%s %s eksik' % (spec['field'], o['value'], k))
            pos = len(ops) if not prev else next((k + 1 for k, x in enumerate(ops) if x['value'] == prev), None)
            if pos is None:
                sys.exit('HATA: %s after değeri yok %s' % (spec['field'], prev))
            ops.insert(pos, copy.deepcopy(o))
            lst = A.setdefault('options', {}).setdefault(spec['field'], [])
            if o['value'] not in lst:
                lst.append(o['value'])
            no += 1
        prev = o['value']
for spec in src.get('fieldSet', []):
    fid = spec['field']
    if fid not in SET or 'showIf' not in spec['set']:
        continue
    if fid not in FI:
        sys.exit('HATA: --set alanı yok ' + fid)
    v = spec['set']['showIf']
    for c in v:
        g = FI.get(c['field'])
        vals = [True, False] if g and g['type'] == 'boolean' else [o['value'] for o in (g or {}).get('options') or []]
        if not g or any(x not in vals for x in c['in']):
            sys.exit('HATA: %s showIf hatalı %s' % (fid, c))
    if FI[fid].get('showIf') != v:
        FI[fid]['showIf'] = copy.deepcopy(v)
        nf += 1
for k, x in enumerate(secs):
    x['code'] = '%02d' % k
seen, prevg = set(), None
for x in secs:
    if x.get('area') != 'marketing' or x.get('sub'):
        continue
    g = x.get('group')
    if g != prevg and g in seen:
        sys.exit('HATA: pazarlama grubu ardışık değil: %s (%s)' % (g, x['id']))
    seen.add(g)
    prevg = g
out = json.dumps(D, ensure_ascii=False)
for bad in ('</script', '<!--'):
    if bad in out:
        sys.exit('HATA: DATA içinde yasak dizi ' + bad)
h = h[:i] + out + h[end:]
open(hp, 'w', encoding='utf-8').write(h)
print('tamam: %d bölüm, %d seçenek, %d showIf · md5 %s · boyut %d' % (ns, no, nf, hashlib.md5(h.encode('utf-8')).hexdigest(), len(h.encode('utf-8'))))
