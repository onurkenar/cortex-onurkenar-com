# -*- coding: utf-8 -*-
"""Tutarlılık katmanı (2026-11-15) — çakışan / tekrar eden kararların bağlanması.
Kullanım: python3 -I docs/v26/tutarlilik_ekle.py <html>
1) DATA'ya docs/v26/tutarlilik.json'u uygular: fieldSet (etiket, en, derive), textAppend (açıklamaya cümle ekler),
   textReplace (alanın bütün metinlerinde), guideReplace (bölüm rehberinde), recommendAdd, move (alanı başka bölüme taşır, kimlik aynı kalır), refsAdd.
   Her değişen anahtarın özgün değeri ilk uygulamada DATA.consistencyKit.orig'e yazılır (geri alma kaydı).
2) <script id="v26-consistency"> ← docs/v26/v26-consistency.js ve <style id="v26-consistency"> ← v26-consistency.css
   (v26-mobile bloklarından önce; varsa yerinde yenilenir).
Bütün işlemler hedef değeri doğrudan yazar; tekrar çalıştırma aynı dosyayı verir. Diğer veri betiklerinden (Ortak Bilgiler,
kılavuz, Google, Meta, onay akışı, tasarım stilleri, SEO denetimi) SONRA çalıştırılır — onlar bu alanları kaynaklarından
yeniden yazarsa bu betik yeniden çalıştırılır."""
import copy, hashlib, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
hp = sys.argv[1]
h = open(hp, encoding='utf-8').read()
src = json.load(open(os.path.join(HERE, 'tutarlilik.json'), encoding='utf-8'))
JS = open(os.path.join(HERE, 'v26-consistency.js'), encoding='utf-8').read().strip()
CSS = open(os.path.join(HERE, 'v26-consistency.css'), encoding='utf-8').read().strip()
for t in (JS, CSS):
    if '</script' in t.lower() or '<!--' in t:
        sys.exit('HATA: kaynakta </script ya da <!-- var')

MARK = 'const DATA='
if h.count(MARK) != 1:
    sys.exit('HATA: DATA satırı bulunamadı')
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
FI = {f['id']: f for f in D['fields']}
SI = {s['id']: s for s in D['sections']}
kit = D.setdefault('consistencyKit', {})
kit['version'] = src['version']
orig = kit.setdefault('orig', {})


def need(fid):
    if fid not in FI:
        sys.exit('HATA: alan yok ' + fid)
    return FI[fid]


def keep(fid, key, val):
    o = orig.setdefault(fid, {})
    if key not in o:
        o[key] = copy.deepcopy(val) if val is not None else None


def opt_vals(f):
    return [True, False] if f['type'] == 'boolean' else [o['value'] for o in f.get('options') or []]


# 1. fieldSet
for fid, kv in src.get('fieldSet', {}).items():
    f = need(fid)
    for k, v in kv.items():
        if k == 'derive':
            s = need(v['from'])
            for a, b in v['map'].items():
                if f['type'] != 'boolean' and b not in opt_vals(f):
                    sys.exit('HATA: derive hedef değeri yok %s=%s' % (fid, b))
                sv = [str(x).lower() for x in opt_vals(s)]
                if a not in [str(x) for x in opt_vals(s)] and a not in sv:
                    sys.exit('HATA: derive kaynak değeri yok %s=%s' % (v['from'], a))
        if f.get(k) != v:
            keep(fid, k, f.get(k))
            f[k] = copy.deepcopy(v)

# 2. textAppend
for fid, kv in src.get('textAppend', {}).items():
    f = need(fid)
    for k, add in kv.items():
        cur = f.get(k) or ''
        if add.strip() not in cur:
            keep(fid, k, cur)
            f[k] = cur.rstrip() + add


# 3. textReplace (alanın bütün metin değerlerinde)
def repl(o, a, b):
    if isinstance(o, str):
        return o.replace(a, b) if a in o and b not in o else o
    if isinstance(o, list):
        return [repl(x, a, b) for x in o]
    if isinstance(o, dict):
        return {k: repl(v, a, b) for k, v in o.items()}
    return o


for r in src.get('textReplace', []):
    f = need(r['field'])
    g = repl(f, r['old'], r['new'])
    if g != f:
        for k in f:
            if g[k] != f[k]:
                keep(r['field'], k, f[k])
        f.clear()
        f.update(g)

# 3b. guideReplace (bölüm rehberinde — sectionGuides — metin değişikliği; özgün metin kit.guide'a)
kg = kit.setdefault('guide', {})
for r in src.get('guideReplace', []):
    if r['section'] not in D.get('sectionGuides', {}):
        sys.exit('HATA: rehber yok ' + r['section'])
    g = D['sectionGuides'][r['section']]
    gg = repl(g, r['old'], r['new'])
    if gg != g:
        kg.setdefault(r['section'], []).append(r['old'])
        D['sectionGuides'][r['section']] = gg
    elif r['new'] not in json.dumps(g, ensure_ascii=False):
        sys.exit('HATA: rehberde metin bulunamadı ' + r['section'])

# 4. recommendAdd
for fid, L in src.get('recommendAdd', {}).items():
    f = need(fid)
    cur = f.get('recommend')
    cur = [] if cur is None else (cur if isinstance(cur, list) else [cur])
    new = copy.deepcopy(cur)
    for r in L:
        s = need(r['field'])
        for a, bs in r['map'].items():
            if a not in opt_vals(s) or any(b not in opt_vals(f) for b in bs):
                sys.exit('HATA: recommend değerleri %s ← %s' % (fid, r['field']))
        if r not in new:
            new.append(copy.deepcopy(r))
    if new != cur:
        keep(fid, 'recommend', f.get('recommend'))
        f['recommend'] = new

# 5. move (kimlik aynı; bölüm ve sıra değişir)
L = D['fields']
for m in src.get('move', []):
    f = need(m['id'])
    if m['section'] not in SI:
        sys.exit('HATA: bölüm yok ' + m['section'])
    if need(m['after'])['section'] != m['section']:
        sys.exit('HATA: after alanı hedef bölümde değil ' + m['after'])
    k = next(k for k, x in enumerate(L) if x['id'] == m['id'])
    a = next(k for k, x in enumerate(L) if x['id'] == m['after'])
    if f['section'] == m['section'] and k == a + 1:
        continue
    if 'section' not in orig.get(m['id'], {}):
        prev = L[k - 1]['id'] if k and L[k - 1]['section'] == f['section'] else None
        keep(m['id'], 'section', f['section'])
        keep(m['id'], 'after', prev)
    L.pop(k)
    f['section'] = m['section']
    a = next(k for k, x in enumerate(L) if x['id'] == m['after'])
    L.insert(a + 1, f)

# 6. refsAdd
ar = kit.setdefault('refs', {})
for sid, ids in src.get('refsAdd', {}).items():
    if sid not in SI:
        sys.exit('HATA: bölüm yok ' + sid)
    for fid in ids:
        if SI[need(fid)['section']].get('area') != 'common':
            sys.exit('HATA: refsAdd ortak alan değil ' + fid)
        r = SI[sid].setdefault('refs', [])
        if fid not in r:
            r.append(fid)
            ar.setdefault(sid, [])
            if fid not in ar[sid]:
                ar[sid].append(fid)

# showIf / derive / recommend başvuruları hâlâ geçerli mi
for f in L:
    for c in f.get('showIf') or []:
        if c['field'] not in FI:
            sys.exit('HATA: showIf alanı yok %s → %s' % (f['id'], c['field']))

out = json.dumps(D, ensure_ascii=False)
for bad in ('</script', '<!--'):
    if bad in out:
        sys.exit('HATA: DATA içinde yasak dizi ' + bad)
h = h[:i] + out + h[end:]

# 7. JS / CSS blokları
for a in ('<style id="v26-mobile">', '<script id="v26-mobile">'):
    if h.count(a) != 1:
        sys.exit('HATA: tek olmalı: ' + a)
css = '<style id="v26-consistency">\n' + CSS + '\n</style>\n'
mm = re.search(r'<style id="v26-consistency">.*?</style>\n', h, flags=re.S)
h = h[:mm.start()] + css + h[mm.end():] if mm else h.replace('<style id="v26-mobile">', css + '<style id="v26-mobile">')
js = '<script id="v26-consistency">\n' + JS + '\n</script>\n'
mm = re.search(r'<script id="v26-consistency">.*?</script>\n', h, flags=re.S)
h = h[:mm.start()] + js + h[mm.end():] if mm else h.replace('<script id="v26-mobile">', js + '<script id="v26-mobile">')
open(hp, 'w', encoding='utf-8').write(h)
print('tamam · md5 %s · boyut %d' % (hashlib.md5(h.encode('utf-8')).hexdigest(), len(h.encode('utf-8'))))
