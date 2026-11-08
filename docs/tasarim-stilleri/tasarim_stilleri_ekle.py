#!/usr/bin/env python3
"""Tasarım kütüphanesi: stiller, sınıflar, yeni karar alanları, layout'lar, önizleme ve canlı örnekler.

Kullanım: python3 -I docs/tasarim-stilleri/tasarim_stilleri_ekle.py web-proje-gelistirme.html docs/tasarim-stilleri/tasarim-stilleri.json

Kaynak (tasarim-stilleri.json; V2 anahtarlarını kaynak_v2.py yazar):
- fields: aynı stil listesini taşıyan alanlar (page_design_style, secondary_design_styles).
- add[]: yeni stil seçenekleri {after, value, label, explanation, scenario, example, examples[3]}.
- rename: stil → yeni etiket (değer aynı kalır; kayıtlı seçimler bozulmaz).
- images: stil → {ids[], labels[]} | null (pptDesignImages / pptDesignLabels).
- mock: stil → {brand, kicker, title, button}; her seçenekte zorunlu. principle + principleMock: seçilemeyen ilke kaydı.
- classes[{id,name}], styleMeta: stil → {cls[], tone l|d}; her stil ve ilke için zorunlu.
- newFields[]: yeni karar alanları {after, id, label, type, cls[], explanation, rule, scenario, example,
  none / noneValue, noneLabel, noneText, noneScenario, noneExample}; seçenekleri cls'teki stillerden türer
  (metinleri stilden kopyalanır), başta "yok" seçeneği; agents page_design_style'dan.
- layouts: add[] (yeni layout seçenekleri, iki layout alanına), meta: layout → {en, pages[], responsive, a11y,
  perf, styles[], recipes[3]}, pageNames, recipeLabels.
- live: stil → {sites[], gallery[], note?}.

Çıktı DATA.designStyleKit = {version, classes, meta, mock, live, principle, layouts{meta,pageNames,recipeLabels},
fieldCls{alan: [sınıf]}, added, orig{fields{id: özgün alan}, addedFields[], images}}.
Betik her çalıştırmada önce kendi değişikliklerini geri alır (dokunduğu alanlar özgün kopyalarıyla değişir,
eklediği alanlar ve designExamples silinir, görseller geri yüklenir), sonra uygular — tekrar çalıştırılabilir.

Denetimler: alan seçenek listeleri aynı; yeni seçenekte metinler dolu, value benzersiz, after var; görsel
kimlikleri var, etiket sayısı tutuyor, aynı görsel seti iki stilde yok; her stilin mock ve meta kaydı var,
sınıflar tanımlı; layout meta'sı her layout seçeneği için var, 3 kompozisyon, hücre türleri bilinen,
önerilen stiller var; canlı adresler https; metinlerde `</script` ya da `<!--` yok.
"""
import copy
import hashlib
import json
import sys

MARK = '<script>const DATA='
LAYOUT_FIELDS = ['page_layout_approach', 'secondary_layout_approaches']
CELLS = set('nav hero head text img card cta chart stat side form tile foot list quote gal tall wide pin mason bleed layer hscroll dash zpath fpath'.split())
TXT = ('value', 'label', 'scenario', 'example', 'explanation')


def die(msg):
    sys.exit('HATA: ' + msg)


def opt(a):
    return {k: a[k] for k in TXT}


def main():
    if len(sys.argv) != 3:
        die('kullanım: tasarim_stilleri_ekle.py <html> <json>')
    html_p, src_p = sys.argv[1:]
    html = open(html_p, encoding='utf-8').read()
    if html.count(MARK) != 1:
        die('DATA satırı bulunamadı')
    i = html.index(MARK) + len(MARK)
    D, end = json.JSONDecoder().raw_decode(html, i)
    src = json.load(open(src_p, encoding='utf-8'))
    names = src.get('fields') or []
    P, L, X = D['pptDesignImages'], D['pptDesignLabels'], D['designExamples']

    # 1) önceki çalıştırmayı geri al
    kit = D.pop('designStyleKit', None)
    if kit:
        o = kit.get('orig') or {}
        D['sections'] = [x for x in D['sections'] if x['id'] not in set(o.get('addedSections') or [])]
        for g in o.get('addedGuides') or []:
            D['sectionGuides'].pop(g, None)
        D['fields'] = [f for f in D['fields'] if f['id'] not in set(o.get('addedFields') or [])]
        fo = o.get('fields') or {}
        D['fields'] = [copy.deepcopy(fo[f['id']]) if f['id'] in fo else f for f in D['fields']]
        if not fo:  # V1 kaydı: yalnız eklenen seçenekler
            added = set(kit.get('added') or [])
            for f in D['fields']:
                if f['id'] in names:
                    f['options'] = [x for x in f['options'] if x['value'] not in added]
        for v in kit.get('added') or []:
            X.pop(v, None)
        for v, old in (o.get('images') or {}).items():
            if old is None:
                P.pop(v, None)
                L.pop(v, None)
            else:
                P[v], L[v] = old[0], old[1]
    F = {f['id']: f for f in D['fields']}
    for n in names + LAYOUT_FIELDS:
        if n not in F:
            die('alan yok: ' + n)
    rec_existing = [k for k in (src.get('profiles') or {}) if k in F]
    orig_fields = {n: copy.deepcopy(F[n]) for n in names + LAYOUT_FIELDS + rec_existing}

    # 2) stiller
    vals = [o['value'] for o in F[names[0]]['options']]
    for n in names[1:]:
        if [o['value'] for o in F[n]['options']] != vals:
            die('alanların seçenekleri farklı: ' + n)
    added = []
    for a in src.get('add') or []:
        for k in ('after',) + TXT:
            if not str(a.get(k) or '').strip():
                die('yeni stilde boş alan: %s / %s' % (a.get('value'), k))
        if len(a.get('examples') or []) != 3:
            die('examples üç öğe olmalı: ' + a['value'])
        if a['value'] in vals:
            die('stil zaten var: ' + a['value'])
        if a['after'] not in vals:
            die('after bulunamadı: %s → %s' % (a['value'], a['after']))
        for n in names:
            ops = F[n]['options']
            ops.insert([x['value'] for x in ops].index(a['after']) + 1, opt(a))
        vals.insert(vals.index(a['after']) + 1, a['value'])
        X[a['value']] = list(a['examples'])
        added.append(a['value'])
    for v, lab in (src.get('rename') or {}).items():
        if v not in vals:
            die('yeniden adlandırılan stil yok: ' + v)
        for n in names:
            next(x for x in F[n]['options'] if x['value'] == v)['label'] = lab
    if len(set(vals)) != len(vals):
        die('yinelenen stil değeri')

    store, orig_img = D['pptImageStore'], {}
    for v, im in (src.get('images') or {}).items():
        if v not in vals:
            die('görsel atanan stil listede yok: ' + v)
        orig_img[v] = [P[v], L.get(v, [])] if v in P else None
        if im is None:
            P.pop(v, None)
            L.pop(v, None)
            continue
        ids, labs = im.get('ids') or [], im.get('labels') or []
        if not ids or len(ids) != len(labs) or any(k not in store for k in ids):
            die('görsel tanımı hatalı: ' + v)
        P[v], L[v] = list(ids), list(labs)
    seen = {}
    for v in vals:
        if v in P:
            key = tuple(P[v])
            if key in seen:
                die('aynı görseller iki stilde: %s, %s' % (seen[key], v))
            seen[key] = v

    cls_ids = [c['id'] for c in src.get('classes') or []]
    meta = src.get('styleMeta') or {}
    pr = src.get('principle') or {}
    mock = dict(src.get('mock') or {})
    if pr:
        mock[pr['value']] = src.get('principleMock')
        X[pr['value']] = list(pr.get('examples') or [])
        added.append(pr['value'])
    need = vals + ([pr['value']] if pr else [])
    miss = [v for v in need if v not in mock or v not in meta]
    extra = [v for v in set(mock) | set(meta) if v not in need]
    if miss or extra:
        die('mock / meta eksik %s / fazla %s' % (miss, extra))
    for v in need:
        m = mock[v]
        if not all(str(m.get(k) or '').strip() for k in ('brand', 'kicker', 'title', 'button')):
            die('mock alanı boş: ' + v)
        if not meta[v].get('cls') or any(c not in cls_ids for c in meta[v]['cls']) or meta[v].get('tone') not in ('l', 'd'):
            die('meta hatalı: ' + v)

    # 3) yeni karar alanları
    field_cls = {names[0]: ['primary-style', 'brand-style', 'visual-approach'],
                 names[1]: ['primary-style', 'brand-style', 'visual-approach']}
    added_fields = []
    base = F[names[0]]
    for nf in src.get('newFields') or []:
        for k in ('after', 'id', 'label', 'type', 'explanation', 'rule', 'scenario', 'example', 'noneLabel', 'noneText', 'noneScenario', 'noneExample'):
            if not str(nf.get(k) or '').strip():
                die('yeni alanda boş: %s / %s' % (nf.get('id'), k))
        if nf['id'] in F:
            die('alan zaten var: ' + nf['id'])
        if nf['type'] not in ('select', 'multiselect'):
            die('alan tipi: ' + nf['id'])
        nv = nf.get('none') or nf.get('noneValue')
        ops = [{'value': nv, 'label': nf['noneLabel'], 'scenario': nf['noneScenario'], 'example': nf['noneExample'], 'explanation': nf['noneText']}]
        if nf['type'] == 'multiselect':
            ops[0]['exclusive'] = True
        for v in vals:
            if set(meta[v]['cls']) & set(nf['cls']):
                ops.append(opt(next(x for x in base['options'] if x['value'] == v)))
        if len(ops) < 3:
            die('alanda seçenek az: ' + nf['id'])
        fld = {'id': nf['id'], 'section': base['section'], 'label': nf['label'], 'type': nf['type'],
               'explanation': nf['explanation'], 'options': ops, 'rule': nf['rule'],
               'scenario': nf['scenario'], 'example': nf['example'], 'agents': list(base.get('agents') or [])}
        j = [f['id'] for f in D['fields']].index(nf['after'] if nf['after'] in F else names[1])
        D['fields'].insert(j + 1, fld)
        F[fld['id']] = fld
        field_cls[fld['id']] = list(nf['cls'])
        added_fields.append(fld['id'])

    # 4) layout'lar
    lay = src.get('layouts') or {}
    lvals = [o['value'] for o in F[LAYOUT_FIELDS[0]]['options']]
    if [o['value'] for o in F[LAYOUT_FIELDS[1]]['options']] != lvals:
        die('layout alanlarının seçenekleri farklı')
    for a in lay.get('add') or []:
        for k in ('after',) + TXT:
            if not str(a.get(k) or '').strip():
                die('yeni layout\'ta boş alan: %s / %s' % (a.get('value'), k))
        if a['value'] in lvals or a['after'] not in lvals:
            die('layout değeri / after hatalı: ' + a['value'])
        for n in LAYOUT_FIELDS:
            ops = F[n]['options']
            ops.insert([x['value'] for x in ops].index(a['after']) + 1, opt(a))
        lvals.insert(lvals.index(a['after']) + 1, a['value'])
    lmeta = lay.get('meta') or {}
    if sorted(lmeta) != sorted(lvals):
        die('layout meta eksik / fazla: %s' % (set(lvals) ^ set(lmeta)))
    pages = lay.get('pageNames') or {}
    for v, m in lmeta.items():
        for k in ('en', 'responsive', 'a11y', 'perf'):
            if not str(m.get(k) or '').strip():
                die('layout meta boş: %s / %s' % (v, k))
        if any(p not in pages for p in m.get('pages') or []) or not m.get('pages'):
            die('layout sayfa türü: ' + v)
        if any(s not in vals for s in m.get('styles') or []) or not m.get('styles'):
            die('layout önerilen stil: ' + v)
        rs = m.get('recipes') or []
        if len(rs) != 3:
            die('layout kompozisyonu 3 olmalı: ' + v)
        for r in rs:
            for row in r:
                if len(row) != 3 or any(c not in CELLS for c in row[2]):
                    die('layout satırı hatalı: %s %s' % (v, row))

    # 5) tasarım parametreleri: bölüm, rehber, alanlar, token eşlemesi, stil profilinden öneriler
    added_sections, added_guides, ptok = [], [], {}
    sec = src.get('section')
    if sec:
        ids = [x['id'] for x in D['sections']]
        if sec['id'] in ids or sec['after'] not in ids:
            die('bölüm id / after hatalı: ' + sec['id'])
        D['sections'].insert(ids.index(sec['after']) + 1, {'id': sec['id'], 'code': '', 'name': sec['name'], 'desc': sec['desc'], 'en': sec['en'], 'group': sec['group'], 'icon': sec['icon']})
        added_sections.append(sec['id'])
        if src.get('guide'):
            if sec['id'] in D['sectionGuides']:
                die('rehber zaten var: ' + sec['id'])
            g = src['guide']
            if not g.get('purpose') or not g.get('criteria') or any(not str(r.get('url', '')).startswith('https://') for r in g.get('resources') or []):
                die('rehber eksik ya da adres https değil')
            D['sectionGuides'][sec['id']] = g
            added_guides.append(sec['id'])
    last = None
    for pm in src.get('params') or []:
        for k in ('id', 'label', 'en', 'explanation', 'rule', 'scenario', 'example'):
            if not str(pm.get(k) or '').strip():
                die('parametre alanında boş: %s / %s' % (pm.get('id'), k))
        if pm['id'] in F or not sec:
            die('parametre alanı zaten var ya da bölüm yok: ' + pm['id'])
        ops = []
        for o2 in pm['options']:
            if not all(str(o2.get(k) or '').strip() for k in TXT):
                die('parametre seçeneğinde boş metin: %s / %s' % (pm['id'], o2.get('value')))
            ops.append(opt(o2))
            if o2.get('tokens'):
                ptok.setdefault(pm['id'], {})[o2['value']] = o2['tokens']
        fld = {'id': pm['id'], 'section': sec['id'], 'label': pm['label'], 'en': pm['en'], 'type': 'select', 'explanation': pm['explanation'],
               'options': ops, 'rule': pm['rule'], 'scenario': pm['scenario'], 'example': pm['example'], 'agents': list(base.get('agents') or [])}
        j = [f['id'] for f in D['fields']].index(last) + 1 if last else max(i2 for i2, f in enumerate(D['fields']) if f['section'] in (names and base['section'],)) + 1
        D['fields'].insert(j, fld)
        F[fld['id']] = fld
        added_fields.append(fld['id'])
        last = fld['id']
    prof = src.get('profiles') or {}
    for fid, prf in prof.items():
        if fid not in F:
            die('profil alanı yok: ' + fid)
        ovals = [o2['value'] for o2 in F[fid]['options']]
        dflt = prf.get('_')
        if dflt not in ovals:
            die('profil varsayılanı seçeneklerde yok: %s / %s' % (fid, dflt))
        mp = {}
        for val, sts in prf.items():
            if val == '_':
                continue
            if val not in ovals:
                die('profil değeri seçeneklerde yok: %s / %s' % (fid, val))
            for st in sts:
                if st not in need:
                    die('profilde bilinmeyen stil: %s / %s' % (fid, st))
                if st in mp:
                    die('stil iki değerde: %s / %s' % (fid, st))
                mp[st] = [val]
        for st in vals:
            mp.setdefault(st, [dflt])
        rec = {'field': names[0], 'map': mp}
        old = F[fid].get('recommend')
        F[fid]['recommend'] = ([] if old is None else (old if isinstance(old, list) else [old])) + [rec] if old else rec
    lr = src.get('layoutRec') or {}
    for k in ('style', 'cls', 'type', 'sector'):
        for key, L2 in (lr.get(k) or {}).items():
            if any(x not in lvals for x in L2):
                die('layout önerisinde bilinmeyen layout: %s / %s' % (k, key))
    for k in ('b2b', 'b2c', 'conversion', 'dense', 'spacious', 'heavy', 'a11yRisk'):
        if any(x not in lvals for x in lr.get(k) or []):
            die('layout öneri listesi: ' + k)
    for k in (lr.get('style') or {}):
        if k not in vals:
            die('layout önerisinde bilinmeyen stil: ' + k)
    tp = {o2['value'] for o2 in F['project_type']['options']} if 'project_type' in F else set()
    for k in (lr.get('type') or {}):
        if k not in tp:
            die('layout önerisinde bilinmeyen site türü: ' + k)
    pg = src.get('pages') or []
    for k, _ in pg:
        if k not in pages:
            die('sayfa türü layout sayfa adlarında yok: ' + k)
    for k2, x in enumerate(D['sections']):
        x['code'] = '%02d' % k2

    live = src.get('live') or {}
    for v, x in live.items():
        if v not in vals:
            die('canlı örnek stili listede yok: ' + v)
        for s in (x.get('sites') or []) + (x.get('gallery') or []):
            if not str(s.get('name') or '').strip() or not str(s.get('url') or '').startswith('https://'):
                die('canlı örnek adı / adresi geçersiz: %s / %s' % (v, s))

    D['designStyleKit'] = {
        'version': 2, 'classes': src.get('classes') or [], 'meta': meta, 'mock': mock, 'live': live,
        'principle': pr, 'fieldCls': field_cls,
        'layouts': {'meta': lmeta, 'pageNames': pages, 'recipeLabels': lay.get('recipeLabels') or []},
        'params': [p2['id'] for p2 in src.get('params') or []], 'paramTokens': ptok, 'layoutRec': lr, 'pages': pg,
        'added': added, 'orig': {'fields': orig_fields, 'addedFields': added_fields, 'images': orig_img,
                                 'addedSections': added_sections, 'addedGuides': added_guides}}

    out = json.dumps(D, ensure_ascii=False)
    for bad in ('</script', '<!--'):
        if bad in out:
            die('DATA içinde yasak dizi: ' + bad)
    html = html[:i] + out + html[end:]
    open(html_p, 'w', encoding='utf-8').write(html)
    print('stil %d (+%d), alan +%d, layout %d, görselli stil %d, canlı %d site / %d stil, md5 %s' % (
        len(vals), len(added), len(added_fields), len(lvals), sum(1 for v in vals if v in P),
        sum(len(x.get('sites') or []) for x in live.values()), len(live), hashlib.md5(html.encode('utf-8')).hexdigest()))


if __name__ == '__main__':
    main()
