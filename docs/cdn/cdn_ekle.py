# -*- coding: utf-8 -*-
"""CDN & Önbellek bölümünü uygulamaya yazar (2026-11-10): Barındırma & Yayın'dan sonra yeni bölüm (rehber + kararlar).
Kullanım: python3 -I docs/cdn/cdn_ekle.py web-proje-gelistirme.html docs/cdn/cdn.json
- guvenlik_ekle.py'nin kopyasıdır; geri alma kaydı DATA.cdnKit.orig (bölüm, rehber, alanlar).
- Tekrar çalıştırılabilir: önce geri alır, sonra uygular. Bölüm kodları sıradan yeniden üretilir.
- Denetimler: kimlik çakışması, boş metin, seçenek değerleri, kural yer tutucusu, showIf ve recommend başvuruları,
  ajan kimliği biçimi, rehber adresleri https, DATA'da </script ve <!-- yok.
- Kaynak: kaynak.py → cdn.json (elle düzenlemeyin)."""
import json, sys, re, hashlib

MARK = 'const DATA='
TXT = ('value', 'label', 'explanation', 'scenario', 'example')
FK = ('id', 'label', 'en', 'type', 'explanation', 'scenario', 'example', 'rule', 'agents')


def die(m):
    sys.exit('HATA: ' + m)


def main():
    hp, sp = sys.argv[1:3]
    html = open(hp, encoding='utf-8').read()
    if html.count(MARK) != 1:
        die('DATA satırı bulunamadı')
    i = html.index(MARK) + len(MARK)
    D, end = json.JSONDecoder().raw_decode(html, i)
    src = json.load(open(sp, encoding='utf-8'))

    # 1) geri al
    old = D.pop('cdnKit', None)
    if old:
        o = old.get('orig') or {}
        D['sections'] = [x for x in D['sections'] if x['id'] not in set(o.get('addedSections') or [])]
        for g in o.get('addedGuides') or []:
            D['sectionGuides'].pop(g, None)
        D['fields'] = [f for f in D['fields'] if f['id'] not in set(o.get('addedFields') or [])]
        for sid, urls in (o.get('guideRes') or {}).items():
            g = D['sectionGuides'].get(sid)
            if g:
                g['resources'] = [r for r in g.get('resources') or [] if r['url'] not in set(urls)]

    F = {f['id']: f for f in D['fields']}
    sids = [x['id'] for x in D['sections']]
    new = src['fields_into'] + src['fields']
    own = {}
    for f in new:
        for k in FK:
            if not f.get(k) or (isinstance(f[k], str) and not f[k].strip()):
                die('alanda boş: %s / %s' % (f.get('id'), k))
        if f['id'] in F or f['id'] in own:
            die('alan kimliği çakışıyor: ' + f['id'])
        if any(not re.match(r'^poz:[a-z0-9-]+:.+', a) for a in f['agents']):
            die('ajan kimliği hatalı: ' + f['id'])
        if f['type'] == 'boolean':
            if '{booltext}' not in f['rule']:
                die('boolean kuralında {booltext} yok: ' + f['id'])
            for k in ('yes', 'no'):
                if not (f.get(k) or {}).get('scenario') or not (f.get(k) or {}).get('example'):
                    die('boolean %s eksik: %s' % (k, f['id']))
        elif f['type'] in ('select', 'multiselect'):
            ph = '{labels}' if f['type'] == 'multiselect' else '{label}'
            if ph not in f['rule']:
                die('kuralda %s yok: %s' % (ph, f['id']))
            vals = []
            for x in f['options']:
                if not all(str(x.get(k) or '').strip() for k in TXT):
                    die('seçenekte boş: %s / %s' % (f['id'], x.get('value')))
                if x['value'] in vals:
                    die('seçenek iki kez: %s / %s' % (f['id'], x['value']))
                vals.append(x['value'])
        else:
            die('desteklenmeyen tip: ' + f['id'])
        own[f['id']] = f
    A = dict(F)
    A.update(own)
    vals_of = lambda fid: [x['value'] for x in A[fid].get('options') or []]
    for f in new:
        for c in f.get('showIf') or []:
            if c['field'] not in A or any(v not in vals_of(c['field']) for v in c['in']):
                die('showIf hatalı: %s → %s' % (f['id'], c['field']))
        R = f.get('recommend')
        for r in (R if isinstance(R, list) else [R] if R else []):
            if r['field'] not in A:
                die('öneri kaynağı yok: %s → %s' % (f['id'], r['field']))
            for k, L in r['map'].items():
                if k not in vals_of(r['field']):
                    die('öneri kaynak değeri yok: %s → %s / %s' % (f['id'], r['field'], k))
                if any(v not in vals_of(f['id']) for v in L):
                    die('öneri hedef değeri yok: %s / %s' % (f['id'], L))

    def mkf(f, sec):
        x = {k: f[k] for k in FK}
        x['section'] = sec
        for k in ('options', 'showIf', 'recommend', 'yes', 'no'):
            if f.get(k) is not None and f.get(k) != []:
                x[k] = f[k]
        if f['type'] in ('select', 'multiselect'):
            x['options'] = f['options']
        return x

    added = []
    # 2) var olan bölümlere alan
    for f in src['fields_into']:
        if f['section'] not in sids or f['after'] not in F or F[f['after']]['section'] != f['section']:
            die('fields_into konumu hatalı: ' + f['id'])
        j = [g['id'] for g in D['fields']].index(f['after']) + 1
        D['fields'].insert(j, mkf(f, f['section']))
        added.append(f['id'])
    # 3) rehber kaynakları
    gres = {}
    for sid, L in (src.get('guide_add') or {}).items():
        g = D['sectionGuides'].get(sid)
        if not g:
            die('rehber yok: ' + sid)
        have = {r['url'] for r in g.get('resources') or []}
        for r in L:
            if not r['url'].startswith('https://') or not r.get('title') or not r.get('note'):
                die('kaynak hatalı: %s' % r)
            if r['url'] in have:
                continue
            g.setdefault('resources', []).append(r)
            gres.setdefault(sid, []).append(r['url'])
    # 4) yeni bölüm
    sec = src['section']
    if sec['id'] in sids or sec['after'] not in sids:
        die('bölüm id / after hatalı')
    if sec['group'] not in {x['group'] for x in D['sections']}:
        die('grup yok: ' + sec['group'])
    g = src['guide']
    if not g.get('purpose') or not g.get('criteria') or not g.get('pitfalls') or any(not r['url'].startswith('https://') for r in g['resources']):
        die('bölüm rehberi eksik')
    D['sections'].insert(sids.index(sec['after']) + 1, {'id': sec['id'], 'code': '', 'name': sec['name'], 'desc': sec['desc'], 'en': sec['en'], 'group': sec['group'], 'icon': sec['icon']})
    D['sectionGuides'][sec['id']] = g
    pos = max(k for k, f in enumerate(D['fields']) if f['section'] == sec['after']) + 1
    for f in src['fields']:
        D['fields'].insert(pos, mkf(f, sec['id']))
        pos += 1
        added.append(f['id'])
    for k, x in enumerate(D['sections']):
        x['code'] = '%02d' % k
    D['cdnKit'] = {'version': src.get('version', 1), 'orig': {'addedSections': [sec['id']], 'addedGuides': [sec['id']], 'addedFields': added, 'guideRes': gres}}

    out = json.dumps(D, ensure_ascii=False)
    for bad in ('</script', '<!--'):
        if bad in out:
            die('DATA içinde yasak dizi: ' + bad)
    html = html[:i] + out + html[end:]
    open(hp, 'w', encoding='utf-8').write(html)
    code = next(x['code'] for x in D['sections'] if x['id'] == sec['id'])
    print('tamam: %d alan, bölüm %s (%s), %d rehber kaynağı · md5 %s · boyut %d' % (len(added), sec['id'], code, sum(len(v) for v in gres.values()), hashlib.md5(html.encode('utf-8')).hexdigest(), len(html.encode('utf-8'))))


main()
