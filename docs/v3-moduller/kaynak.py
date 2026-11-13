# -*- coding: utf-8 -*-
"""Revize Modüler V3 dokümanından seçilen maddeler (2026-11-12, kullanıcı kararı: A3, A5, A10, A13–A18,
B2–B9, B11, B20, C1, C2, C8). Parçalar (parca_*.py, her biri PART sözlüğü tanımlar) burada birleşir ve
yanına v3-moduller.json yazılır; uygulamaya v3_ekle.py işler.
python3 -I docs/v3-moduller/kaynak.py

Yeni menü grubu: "İş Modülleri" (İçerik & Yönetim'den sonra). Bölüm sırası ORDER'dadır; parçalar bölümlere
'after' yazmaz, burada atanır (eksik parça varsa bir önceki mevcut bölüme bağlanır)."""
import json, os, runpy, glob

HERE = os.path.dirname(os.path.abspath(__file__))
GROUP = 'İş Modülleri'

# (bölüm, bağlandığı var olan bölüm) — aynı zincirde sırayla
ORDER = [
    ('mobile_app', 'frontend_arch'),          # C1 Teknik Mimari
    ('biz_crm', 'i18n'),                      # B20 — İş Modülleri grubu buradan başlar
    ('biz_ticket', 'biz_crm'),                # B2
    ('biz_survey', 'biz_ticket'),             # B3
    ('biz_subscription', 'biz_survey'),       # B4
    ('biz_consulting', 'biz_subscription'),   # B5
    ('biz_einvoice', 'biz_consulting'),       # E-Fatura / E-Arşiv (2026-11-13, kullanıcı isteği)
    ('biz_certificates', 'biz_einvoice'),     # B11
    ('biz_notify', 'biz_certificates'),       # B6
    ('biz_mailing', 'biz_notify'),            # B7
    ('biz_social', 'biz_mailing'),            # B8
    ('biz_automation', 'biz_social'),         # B9
]

# Proje Türü → yeni Ek Modüller önerisi (var olan öneri haritasına eklenir)
REC_ADD = {
    'SaaS': ['subscription', 'ticket', 'notify', 'einvoice'],
    'Web App': ['notify'],
    'Portal': ['ticket', 'notify'],
    'Community': ['notify'],
    'E-commerce': ['notify', 'mailing', 'einvoice'],
    'Marketplace': ['ticket', 'notify', 'einvoice'],
    'B2B Platform': ['ticket', 'einvoice'],
    'Booking': ['notify'],
    'LMS': ['certificates', 'notify'],
    'Knowledge Base': ['ticket'],
}


def main():
    parts = sorted(glob.glob(os.path.join(HERE, 'parca_*.py')))
    out = {'version': 1, 'group': GROUP, 'sections': [], 'fields': [], 'fields_into': [], 'option_add': [],
           'guide_add': {}, 'recommend_add': [{'field': 'modules_extra', 'source': 'project_type', 'map': REC_ADD}],
           'parts': []}
    secs = {}
    for p in parts:
        P = runpy.run_path(p)['PART']
        out['parts'].append(os.path.basename(p))
        for s in P.get('sections') or []:
            secs[s['id']] = s
        out['fields'] += P.get('fields') or []
        out['fields_into'] += P.get('fields_into') or []
        out['option_add'] += P.get('option_add') or []
        for k, v in (P.get('guide_add') or {}).items():
            out['guide_add'].setdefault(k, []).extend(v)
    known = {a for a, _ in ORDER}
    for sid in secs:
        if sid not in known:
            raise SystemExit('ORDER içinde olmayan bölüm: ' + sid)
    present = set(secs)
    for sid, after in ORDER:
        if sid not in present:
            continue
        a = after
        while a in known and a not in present:          # eksik parça: zincirde geri git
            a = dict(ORDER)[a]
        s = dict(secs[sid])
        s['after'] = a
        out['sections'].append(s)
    # İş Modülleri bölümlerinin kapısı Ek Modüller'e eklenen seçeneklerdir; seçeneği gelmemiş modülün önerisini düş
    have = {x['option']['value'] for x in out['option_add'] if x['field'] == 'modules_extra'} | {'crm'}
    m = out['recommend_add'][0]['map']
    for k in list(m):
        m[k] = [v for v in m[k] if v in have]
        if not m[k]:
            del m[k]
    json.dump(out, open(os.path.join(HERE, 'v3-moduller.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('tamam: %d parça, %d bölüm, %d alan + %d var olan bölüme, %d seçenek' % (
        len(parts), len(out['sections']), len(out['fields']), len(out['fields_into']), len(out['option_add'])))


main()
