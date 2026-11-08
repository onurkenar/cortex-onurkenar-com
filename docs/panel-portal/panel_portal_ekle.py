# -*- coding: utf-8 -*-
"""Panel & Portal Mimarisi bölümünü, kararlarını, rehberini ve DATA.panelKit'i uygulamaya yazar.

Kullanım: python3 -I docs/panel-portal/panel_portal_ekle.py web-proje-gelistirme.html docs/panel-portal/panel-portal.json

- Tekrar çalıştırılabilir: önce DATA.panelKit.orig'e göre önceki çalıştırmayı geri alır (eklenen bölüm, rehber, alanlar).
- Bölüm kodları sıradan yeniden üretilir (00…).
- Alan tipleri: select, multiselect ve panels (panel_inventory: envanterin alt menü kaydı; seçeneksiz, isset = en az bir panel).
- Denetimler: bölüm / alan kimliği çakışması, boş metin, seçenek değerleri, showIf ve recommend başvuruları
  (kaynak alan ve değerleri, hedef değerleri), ajan kimliği biçimi, rehber adresleri https, şablon modül / rol tutarlılığı,
  senaryo şablon ve adres türleri, DATA içinde </script ve <!-- olmaması.
- Kaynak: kaynak.py → panel-portal.json (elle düzenlemeyin; kaynak.py'yi değiştirip yeniden üretin).
- Sıra: tasarım / SEO / Ortak Bilgiler / kılavuz betiklerinden sonra da önce de çalışabilir; hepsi kodları yeniden üretir.
"""
import json, sys, re, hashlib

MARK = 'const DATA='
TXT = ('value', 'label', 'explanation', 'scenario', 'example')
MODES = ('subdomain', 'subdirectory', 'separate_domain')


def die(m):
    sys.exit('HATA: ' + m)


def main():
    if len(sys.argv) != 3:
        die('kullanım: panel_portal_ekle.py <html> <json>')
    hp, sp = sys.argv[1:]
    html = open(hp, encoding='utf-8').read()
    if html.count(MARK) != 1:
        die('DATA satırı bulunamadı')
    i = html.index(MARK) + len(MARK)
    D, end = json.JSONDecoder().raw_decode(html, i)
    src = json.load(open(sp, encoding='utf-8'))

    # 1) geri al
    old = D.pop('panelKit', None)
    if old:
        o = old.get('orig') or {}
        D['sections'] = [x for x in D['sections'] if x['id'] not in set(o.get('addedSections') or [])]
        for g in o.get('addedGuides') or []:
            D['sectionGuides'].pop(g, None)
        D['fields'] = [f for f in D['fields'] if f['id'] not in set(o.get('addedFields') or [])]

    F = {f['id']: f for f in D['fields']}
    sid = {x['id'] for x in D['sections']}
    sec = src['section']
    if sec['id'] in sid:
        die('bölüm zaten var: ' + sec['id'])
    if sec['after'] not in sid:
        die('after bölümü yok: ' + sec['after'])
    groups = {x['group'] for x in D['sections']}
    if sec['group'] not in groups:
        die('menü grubu yok: ' + sec['group'])
    for k in ('name', 'en', 'desc', 'icon'):
        if not str(sec.get(k) or '').strip():
            die('bölümde boş: ' + k)

    # 2) alanlar
    new = []
    own = {}
    for f in src['fields']:
        for k in ('id', 'label', 'en', 'type', 'explanation', 'scenario', 'example', 'rule'):
            if not str(f.get(k) or '').strip():
                die('alanda boş: %s / %s' % (f.get('id'), k))
        if f['id'] in F or f['id'] in own:
            die('alan kimliği çakışıyor: ' + f['id'])
        if not f['id'].startswith('panel_'):
            die('alan kimliği panel_ ile başlamalı: ' + f['id'])
        if f['type'] not in ('select', 'multiselect', 'panels'):
            die('desteklenmeyen tip: ' + f['id'])
        if f['type'] == 'panels':  # envanter alanı: seçeneksiz, kural metni yer tutucusuz (arayüz ve çıktı v26-panel-portal betiğinde)
            if f.get('options') or '{' in f['rule']:
                die('panels alanında seçenek ya da yer tutucu olmamalı: ' + f['id'])
            if not re.match(r'^poz:[a-z0-9-]+:.+', (f.get('agents') or [''])[0]):
                die('ajan kimliği hatalı: ' + f['id'])
            own[f['id']] = f
            continue
        vals = []
        for x in f['options']:
            if not all(str(x.get(k) or '').strip() for k in TXT):
                die('seçenekte boş metin: %s / %s' % (f['id'], x.get('value')))
            if x['value'] in vals:
                die('seçenek değeri iki kez: %s / %s' % (f['id'], x['value']))
            vals.append(x['value'])
        ph = '{labels}' if f['type'] == 'multiselect' else '{label}'
        if ph not in f['rule']:
            die('kural metninde %s yok: %s' % (ph, f['id']))
        if not f.get('agents') or any(not re.match(r'^poz:[a-z0-9-]+:.+', a) for a in f['agents']):
            die('ajan kimliği hatalı: ' + f['id'])
        own[f['id']] = f
    allf = dict(F)
    allf.update(own)

    def vals_of(fid):
        return [x['value'] for x in allf[fid].get('options') or []]
    for f in src['fields']:
        for c in f.get('showIf') or []:
            if c['field'] not in allf:
                die('showIf alanı yok: %s → %s' % (f['id'], c['field']))
            bad = [v for v in c['in'] if v not in vals_of(c['field'])]
            if bad:
                die('showIf değeri yok: %s → %s %s' % (f['id'], c['field'], bad))
        recs = f.get('recommend')
        for r in (recs if isinstance(recs, list) else [recs] if recs else []):
            if r['field'] not in allf:
                die('öneri kaynağı yok: %s → %s' % (f['id'], r['field']))
            sv = vals_of(r['field'])
            for k, L in r['map'].items():
                if allf[r['field']]['type'] != 'boolean' and k not in sv:
                    die('öneri kaynak değeri yok: %s → %s / %s' % (f['id'], r['field'], k))
                if any(v not in vals_of(f['id']) for v in L):
                    die('öneri hedef değeri yok: %s / %s' % (f['id'], L))

    # 3) rehber
    g = src['guide']
    if not g.get('purpose') or not g.get('criteria') or not g.get('pitfalls'):
        die('rehber eksik')
    for r in g.get('resources') or []:
        if not str(r.get('url', '')).startswith('https://') or not r.get('title') or not r.get('note'):
            die('rehber kaynağı hatalı: %s' % r)
    if sec['id'] in D['sectionGuides']:
        die('rehber zaten var')

    # 4) kit denetimi
    kit = src['kit']
    mids = [m['id'] for m in kit['modules']]
    if len(set(mids)) != len(mids):
        die('modül kimliği iki kez')
    cats = [c['id'] for c in kit['categories']]
    tids = []
    for t in kit['templates']:
        for k in ('id', 'name', 'en', 'cat', 'mode', 'slug', 'audience', 'desc'):
            if not str(t.get(k) or '').strip():
                die('şablonda boş: %s / %s' % (t.get('id'), k))
        if t['id'] in tids:
            die('şablon iki kez: ' + t['id'])
        tids.append(t['id'])
        if t['cat'] not in cats or t['mode'] not in MODES:
            die('şablon kategori / adres türü: ' + t['id'])
        if not re.match(r'^[a-z0-9](?:[a-z0-9-]*[a-z0-9])?$', t['slug']):
            die('şablon slug geçersiz: ' + t['id'])
        if any(m not in mids for m in t['modules']):
            die('şablonda bilinmeyen modül: ' + t['id'])
        if not t['roles']:
            die('şablonda rol yok: ' + t['id'])
        for r in t['roles']:
            if r['scope'] not in ('platform', 'org', 'own'):
                die('rol kapsamı: %s / %s' % (t['id'], r['id']))
            for k in ('m', 'w', 'r'):
                if any(m not in t['modules'] for m in r[k]):
                    die('rol izni şablon modülünde değil: %s / %s' % (t['id'], r['id']))
    if len(kit['templates']) != 21:
        die('21 panel şablonu bekleniyordu')
    ptypes = vals_of('project_type') if 'project_type' in allf else []
    for s in kit['scenarios']:
        for ty in s['types']:
            if ty not in ptypes:
                die('senaryoda bilinmeyen proje türü: %s / %s' % (s['id'], ty))
        for tp, mode, slug in s['panels']:
            if tp not in tids or mode not in MODES:
                die('senaryo paneli: %s / %s' % (s['id'], tp))
        for fid, v in (s.get('fields') or {}).items():
            if fid not in own or v not in vals_of(fid):
                die('senaryo alanı: %s / %s' % (s['id'], fid))
    mex = vals_of('modules_extra') if 'modules_extra' in allf else []
    for x in kit['extra']:
        if x['module'] not in mex or x['panel'][0] not in tids:
            die('ek öneri: %s' % x)

    # 5) yaz
    ids = [x['id'] for x in D['sections']]
    D['sections'].insert(ids.index(sec['after']) + 1, {'id': sec['id'], 'code': '', 'name': sec['name'], 'desc': sec['desc'], 'en': sec['en'], 'group': sec['group'], 'icon': sec['icon']})
    D['sectionGuides'][sec['id']] = g
    pos = max(k for k, f in enumerate(D['fields']) if f['section'] == sec['after']) + 1
    added = []
    for f in src['fields']:
        fld = {k: f[k] for k in ('id', 'label', 'en', 'type', 'explanation', 'scenario', 'example', 'rule', 'agents')}
        fld['section'] = sec['id']
        fld['options'] = f['options']
        for k in ('showIf', 'recommend'):
            if f.get(k):
                fld[k] = f[k]
        D['fields'].insert(pos, fld)
        pos += 1
        added.append(f['id'])
    for k, x in enumerate(D['sections']):
        x['code'] = '%02d' % k
    D['panelKit'] = dict(kit, version=src.get('version', 1), section=sec['id'],
                         orig={'addedSections': [sec['id']], 'addedGuides': [sec['id']], 'addedFields': added})

    out = json.dumps(D, ensure_ascii=False)
    for bad in ('</script', '<!--'):
        if bad in out:
            die('DATA içinde yasak dizi: ' + bad)
    html = html[:i] + out + html[end:]
    open(hp, 'w', encoding='utf-8').write(html)
    code = next(x['code'] for x in D['sections'] if x['id'] == sec['id'])
    print('tamam: bölüm %s (%s), %d karar, %d şablon, %d modül · md5 %s' % (sec['id'], code, len(added), len(kit['templates']), len(mids), hashlib.md5(html.encode('utf-8')).hexdigest()))


main()
