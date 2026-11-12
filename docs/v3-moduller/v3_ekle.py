# -*- coding: utf-8 -*-
"""Revize Modüler V3 seçimlerini (kaynak.py → v3-moduller.json) uygulamaya yazar (2026-11-12).
Kullanım: python3 -I docs/v3-moduller/v3_ekle.py web-proje-gelistirme.html docs/v3-moduller/v3-moduller.json [--check]
--check: yalnız denetler, dosyaya yazmaz (parça yazarken kullanın).
- onay_ekle.py'nin genişletilmiş hâli: birden çok yeni bölüm (yeni "İş Modülleri" grubu dahil), var olan bölümlere alan,
  var olan alanlara seçenek (option_add), öneri haritasına ekleme (recommend_add), rehber kaynakları.
- Geri alma kaydı DATA.v3Kit.orig; her çalıştırmada önce geri alır, sonra uygular (tekrar çalıştırılabilir).
- Bölüm kodları sıradan yeniden üretilir."""
import json, sys, re, hashlib

MARK = 'const DATA='
TXT = ('value', 'label', 'explanation', 'scenario', 'example')
FK = ('id', 'label', 'en', 'type', 'explanation', 'scenario', 'example', 'rule', 'agents')
OPT_KEYS = set(TXT) | {'ruleDetail', 'exclusive'}
FIELD_KEYS = set(FK) | {'section', 'after', 'options', 'showIf', 'recommend', 'yes', 'no'}
SEC_KEYS = {'id', 'after', 'group', 'icon', 'name', 'en', 'desc', 'guide'}
NEW_GROUP = 'İş Modülleri'


def die(m):
    sys.exit('HATA: ' + m)


def undo(D):
    old = D.pop('v3Kit', None)
    if not old:
        return
    o = old.get('orig') or {}
    D['sections'] = [x for x in D['sections'] if x['id'] not in set(o.get('addedSections') or [])]
    for g in o.get('addedGuides') or []:
        D['sectionGuides'].pop(g, None)
    D['fields'] = [f for f in D['fields'] if f['id'] not in set(o.get('addedFields') or [])]
    F = {f['id']: f for f in D['fields']}
    for fid, v in o.get('optionAdded') or []:
        if fid in F:
            F[fid]['options'] = [x for x in F[fid]['options'] if x['value'] != v]
    for fid, rec in (o.get('recommendOrig') or {}).items():
        if fid in F:
            if rec is None:
                F[fid].pop('recommend', None)
            else:
                F[fid]['recommend'] = rec
    for sid, urls in (o.get('guideRes') or {}).items():
        g = D['sectionGuides'].get(sid)
        if g:
            g['resources'] = [r for r in g.get('resources') or [] if r['url'] not in set(urls)]


def chk_opt(fid, x):
    if set(x) - OPT_KEYS:
        die('seçenekte bilinmeyen anahtar: %s / %s' % (fid, sorted(set(x) - OPT_KEYS)))
    if not all(isinstance(x.get(k), str) and x[k].strip() for k in TXT):
        die('seçenekte boş: %s / %s' % (fid, x.get('value')))
    if 'ruleDetail' in x and not str(x['ruleDetail']).strip():
        die('boş ruleDetail: %s / %s' % (fid, x['value']))


def main():
    hp, sp = sys.argv[1:3]
    check = '--check' in sys.argv[3:]
    html = open(hp, encoding='utf-8').read()
    if html.count(MARK) != 1:
        die('DATA satırı bulunamadı')
    i = html.index(MARK) + len(MARK)
    D, end = json.JSONDecoder().raw_decode(html, i)
    src = json.load(open(sp, encoding='utf-8'))
    try:
        reg = json.load(open('docs/ajan-kaydi/AGENT_REGISTRY.json', encoding='utf-8'))
        POZ = {p for d in reg['definitions'] for p in d['implementations']}
    except OSError:
        die('docs/ajan-kaydi/AGENT_REGISTRY.json okunamadı (proje kökünden çalıştırın)')

    undo(D)
    F = {f['id']: f for f in D['fields']}
    sids = [x['id'] for x in D['sections']]
    groups = {x['group'] for x in D['sections'] if x.get('group')}

    # --- alan denetimi
    new = src['fields_into'] + src['fields']
    own = {}
    for f in new:
        if set(f) - FIELD_KEYS:
            die('alanda bilinmeyen anahtar: %s / %s' % (f.get('id'), sorted(set(f) - FIELD_KEYS)))
        for k in FK:
            if not f.get(k) or (isinstance(f[k], str) and not f[k].strip()):
                die('alanda boş: %s / %s' % (f.get('id'), k))
        if not re.match(r'^[a-z][a-z0-9_]*$', f['id']):
            die('alan kimliği biçimi: ' + f['id'])
        if f['id'] in F or f['id'] in own:
            die('alan kimliği çakışıyor: ' + f['id'])
        bad = [a for a in f['agents'] if a not in POZ]
        if bad:
            die('ajan kimliği şemada yok: %s → %s' % (f['id'], bad))
        if f['type'] == 'boolean':
            if '{booltext}' not in f['rule']:
                die('boolean kuralında {booltext} yok: ' + f['id'])
            for k in ('yes', 'no'):
                if not (f.get(k) or {}).get('scenario') or not (f.get(k) or {}).get('example'):
                    die('boolean %s eksik: %s' % (k, f['id']))
            if f.get('options'):
                die('boolean alanda seçenek olmaz: ' + f['id'])
        elif f['type'] in ('select', 'multiselect'):
            ph = '{labels}' if f['type'] == 'multiselect' else '{label}'
            if ph not in f['rule']:
                die('kuralda %s yok: %s' % (ph, f['id']))
            if len(f.get('options') or []) < 2:
                die('en az 2 seçenek: ' + f['id'])
            vals, labs = [], []
            for x in f['options']:
                chk_opt(f['id'], x)
                if x['value'] in vals or x['label'] in labs:
                    die('seçenek iki kez: %s / %s' % (f['id'], x['value']))
                if x.get('exclusive') and f['type'] != 'multiselect':
                    die('exclusive yalnız multiselect: ' + f['id'])
                vals.append(x['value'])
                labs.append(x['label'])
        else:
            die('desteklenmeyen tip: ' + f['id'])
        own[f['id']] = f

    # --- seçenek eklemeleri
    oadd = []
    for a in src.get('option_add') or []:
        fid, x = a['field'], a['option']
        if fid not in F or F[fid]['type'] not in ('select', 'multiselect'):
            die('option_add alanı yok / seçenekli değil: ' + fid)
        chk_opt(fid, x)
        if x.get('exclusive'):
            die('option_add exclusive olamaz: ' + fid)
        if any(o['value'] == x['value'] or o['label'] == x['label'] for o in F[fid]['options']) or (fid, x['value']) in [(p, q['value']) for p, q, _ in oadd]:
            die('option_add seçeneği zaten var: %s / %s' % (fid, x['value']))
        if a.get('after') and a['after'] not in [o['value'] for o in F[fid]['options']] + [q['value'] for p, q, _ in oadd if p == fid]:
            die('option_add after yok: %s / %s' % (fid, a['after']))
        oadd.append((fid, x, a.get('after')))

    A = dict(F)
    A.update(own)
    extra_vals = {}
    for fid, x, _ in oadd:
        extra_vals.setdefault(fid, []).append(x['value'])

    def vals_of(fid):
        if A[fid].get('type') == 'boolean':
            return [True, False]
        return [x['value'] for x in A[fid].get('options') or []] + extra_vals.get(fid, [])

    for f in new:
        for c in f.get('showIf') or []:
            if c['field'] not in A or not c.get('in') or any(v not in vals_of(c['field']) for v in c['in']):
                die('showIf hatalı: %s → %s %s' % (f['id'], c.get('field'), c.get('in')))
        R = f.get('recommend')
        for r in (R if isinstance(R, list) else [R] if R else []):
            if r['field'] not in A:
                die('öneri kaynağı yok: %s → %s' % (f['id'], r['field']))
            for k, L in r['map'].items():
                if k not in vals_of(r['field']) and not (A[r['field']].get('type') == 'boolean' and k in ('true', 'false')):
                    die('öneri kaynak değeri yok: %s → %s / %s' % (f['id'], r['field'], k))
                if any(v not in vals_of(f['id']) for v in L):
                    die('öneri hedef değeri yok: %s / %s' % (f['id'], L))

    # --- bölüm denetimi
    nsec = src['sections']
    nids = [s['id'] for s in nsec]
    for s in nsec:
        if set(s) - SEC_KEYS:
            die('bölümde bilinmeyen anahtar: %s / %s' % (s['id'], sorted(set(s) - SEC_KEYS)))
        for k in ('id', 'after', 'group', 'icon', 'name', 'en', 'desc'):
            if not str(s.get(k) or '').strip():
                die('bölümde boş: %s / %s' % (s.get('id'), k))
        if s['id'] in sids or nids.count(s['id']) > 1:
            die('bölüm kimliği çakışıyor: ' + s['id'])
        if s['group'] not in groups and s['group'] != NEW_GROUP:
            die('grup yok: ' + s['group'])
        g = s.get('guide') or {}
        if not g.get('purpose') or len(g.get('criteria') or []) < 3 or len(g.get('pitfalls') or []) < 3 or len(g.get('resources') or []) < 3:
            die('bölüm rehberi eksik (amaç, ≥3 ölçüt, ≥3 dikkat, ≥3 kaynak): ' + s['id'])
        for r in g['resources']:
            if not str(r.get('url', '')).startswith('https://') or not r.get('title') or not r.get('note'):
                die('kaynak hatalı: %s / %s' % (s['id'], r))
        if not any(f['section'] == s['id'] for f in src['fields']):
            die('bölümde alan yok: ' + s['id'])
    for f in src['fields']:
        if f.get('section') not in nids:
            die('yeni alanın bölümü yok: %s → %s' % (f['id'], f.get('section')))
    for f in src['fields_into']:
        if f.get('section') not in sids:
            die('fields_into bölümü yok: %s → %s' % (f['id'], f.get('section')))
        aft = f.get('after')
        ok = (aft in F and F[aft]['section'] == f['section']) or any(g['id'] == aft and g['section'] == f['section'] for g in src['fields_into'])
        if not ok:
            die('fields_into after hatalı: %s → %s' % (f['id'], aft))
    for sid, L in (src.get('guide_add') or {}).items():
        if sid not in sids:
            die('guide_add bölümü yok: ' + sid)
        for r in L:
            if not str(r.get('url', '')).startswith('https://') or not r.get('title') or not r.get('note'):
                die('kaynak hatalı: %s' % r)

    print('denetim tamam: %d bölüm, %d yeni alan, %d var olan bölüme alan, %d seçenek, %d rehber kaynağı' % (
        len(nsec), len(src['fields']), len(src['fields_into']), len(oadd), sum(len(v) for v in (src.get('guide_add') or {}).values())))
    if check:
        return

    def mkf(f, sec):
        x = {k: f[k] for k in FK}
        x['section'] = sec
        for k in ('options', 'showIf', 'recommend', 'yes', 'no'):
            if f.get(k) not in (None, []):
                x[k] = f[k]
        return x

    added = []
    # var olan alanlara seçenek
    for fid, x, aft in oadd:
        L = F[fid]['options']
        j = [o['value'] for o in L].index(aft) + 1 if aft else (len(L) - 1 if L and L[-1].get('exclusive') else len(L))
        L.insert(j, x)
    # öneri haritası ekleri
    rorig = {}
    for r in src.get('recommend_add') or []:
        f = F[r['field']]
        rorig[r['field']] = json.loads(json.dumps(f.get('recommend')))
        R = f.get('recommend')
        lst = R if isinstance(R, list) else [R] if R else []
        tgt = next((x for x in lst if x['field'] == r['source']), None)
        if tgt is None:
            tgt = {'field': r['source'], 'map': {}}
            lst.append(tgt)
        for k, vs in r['map'].items():
            if k not in [o['value'] for o in F[r['source']]['options']]:
                die('recommend_add kaynak değeri yok: ' + k)
            cur = tgt['map'].setdefault(k, [])
            for v in vs:
                if v not in vals_of(r['field']):
                    die('recommend_add hedef değeri yok: ' + v)
                if v not in cur:
                    cur.append(v)
        f['recommend'] = lst[0] if len(lst) == 1 else lst
    # var olan bölümlere alan (sırayla, after zinciri)
    for f in src['fields_into']:
        j = [g['id'] for g in D['fields']].index(f['after']) + 1
        D['fields'].insert(j, mkf(f, f['section']))
        added.append(f['id'])
    # rehber kaynakları
    gres = {}
    for sid, L in (src.get('guide_add') or {}).items():
        g = D['sectionGuides'].get(sid)
        if not g:
            die('rehber yok: ' + sid)
        have = {r['url'] for r in g.get('resources') or []}
        for r in L:
            if r['url'] in have:
                continue
            g.setdefault('resources', []).append({'title': r['title'], 'url': r['url'], 'note': r['note']})
            have.add(r['url'])
            gres.setdefault(sid, []).append(r['url'])
    # yeni bölümler
    for s in nsec:
        cur = [x['id'] for x in D['sections']]
        if s['after'] not in cur:
            die('bölüm after yok: %s → %s' % (s['id'], s['after']))
        D['sections'].insert(cur.index(s['after']) + 1, {'id': s['id'], 'code': '', 'name': s['name'], 'desc': s['desc'], 'en': s['en'], 'group': s['group'], 'icon': s['icon']})
        D['sectionGuides'][s['id']] = s['guide']
        pos = max(k for k, f in enumerate(D['fields']) if f['section'] == s['after']) + 1
        for f in src['fields']:
            if f['section'] == s['id']:
                D['fields'].insert(pos, mkf(f, s['id']))
                pos += 1
                added.append(f['id'])
    # grup bütünlüğü: aynı gruptaki bölümler art arda
    seen, last = set(), None
    for x in D['sections']:
        g = (x.get('area') or 'project', x.get('sub'), x.get('group'))
        if g != last:
            if g in seen:
                die('grup bölündü: %s (%s)' % (x.get('group'), x['id']))
            seen.add(g)
            last = g
    for k, x in enumerate(D['sections']):
        x['code'] = '%02d' % k
    D['v3Kit'] = {'version': src.get('version', 1), 'orig': {
        'addedSections': nids, 'addedGuides': nids, 'addedFields': added,
        'optionAdded': [[fid, x['value']] for fid, x, _ in oadd], 'recommendOrig': rorig, 'guideRes': gres}}

    out = json.dumps(D, ensure_ascii=False)
    for bad in ('</script', '<!--'):
        if bad in out:
            die('DATA içinde yasak dizi: ' + bad)
    html = html[:i] + out + html[end:]
    open(hp, 'w', encoding='utf-8').write(html)
    print('yazıldı: %d alan, %d bölüm · md5 %s · boyut %d' % (len(added), len(nids), hashlib.md5(html.encode('utf-8')).hexdigest(), len(html.encode('utf-8'))))


main()
