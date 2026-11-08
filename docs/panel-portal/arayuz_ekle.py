# -*- coding: utf-8 -*-
"""Panel & Portal Mimarisi arayüzünü HTML'e işler — tekrar çalıştırılabilir.
Kullanım: python3 -I docs/panel-portal/arayuz_ekle.py web-proje-gelistirme.html
Önce panel_portal_ekle.py çalıştırılmış olmalı (DATA.panelKit). Kaynaklar: docs/v26/v26-panel-portal.{css,js}.
- <style id="v26-panel-portal"> ve <script id="v26-panel-portal"> yoksa eklenir, varsa içerikleri kaynaktan yenilenir.
- Ana betik kancaları (kurallar, prompt, proje dosyası / JSON, talimat dosyası fazı, alan tipi `panels`, isset) yalnız eksikse eklenir.
- Dokümantasyon maddesi yoksa eklenir, varsa güncel metinle değiştirilir.
2026-11-08: envanter bölüm başlığından çıkarılıp sol menüde kendi alt başlığı olan `panel_inventory` alanına taşındı (kullanıcı isteği)."""
import sys, os, re, hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
hp = sys.argv[1]
h = open(hp, encoding='utf-8').read()
css = open(os.path.join(ROOT, 'docs/v26/v26-panel-portal.css'), encoding='utf-8').read()
js = open(os.path.join(ROOT, 'docs/v26/v26-panel-portal.js'), encoding='utf-8').read()
assert '"panelKit"' in h, 'önce panel_portal_ekle.py'
for bad in ('</script', '<!--'):
    assert bad not in js and bad not in css, bad


def hook(old, new, n=1):
    """old → new; new zaten varsa dokunma."""
    global h
    if h.count(new) == n and new not in old:
        return
    c = h.count(old)
    assert c == n, (old[:90], c)
    h = h.replace(old, new)


def block(tag, body, after_open, after_close):
    global h
    op = '<%s id="v26-panel-portal">\n' % tag
    cl = '</%s>' % tag
    if op in h:
        i = h.index(op) + len(op)
        j = h.index(cl, i)
        h = h[:i] + body + h[j:]
    elif tag == 'style':
        i = h.index(after_open)
        j = h.index(after_close, i) + len(after_close)
        h = h[:j] + '\n' + op + body + cl + h[j:]
    else:
        k = h.rindex('</body>')
        h = h[:k] + op + body + cl + '\n' + h[k:]


# 1) stil ve betik blokları
block('style', css, '<style id="v26-prompt-md">', '</style>')
block('script', js, None, None)

# 2) ana betik kancaları (sonraki betikte tanımlanır; açılışta henüz yoksa boş döner)
hook('ruleGroups.insertAdjacentHTML("beforeend",dsRuleGroups()+agRuleGroups());',
     'ruleGroups.insertAdjacentHTML("beforeend",dsRuleGroups()+(typeof pzRuleGroups==="function"?pzRuleGroups():"")+agRuleGroups());')
hook('${dsPrompt()}${agPrompt()}', '${dsPrompt()}${typeof pzPrompt==="function"?pzPrompt():""}${agPrompt()}')
hook('...dsPf(),claudePrompt', '...dsPf(),...(typeof pzPf==="function"?pzPf():{}),claudePrompt', 2)
# envanter alanı (type "panels"): kutu betikte .pzSlot içine çizilir; en az bir panel varsa dolu sayılır
hook('else if(f.type==="accounts")c=accInput(f);else if(f.type==="textarea")',
     'else if(f.type==="accounts")c=accInput(f);else if(f.type==="panels")c=\'<div class="pzSlot"></div>\';else if(f.type==="textarea")')
hook('function isset(f){let v=state[f.id];return f.type==="accounts"?accList(f).length>0:',
     'function isset(f){let v=state[f.id];return f.type==="panels"?(typeof pzActive==="function"&&pzActive()):f.type==="accounts"?accList(f).length>0:')

# 3) Claude talimat dosyası: panel mimarisi ilk fazda
hook('{t:"Proje temeli ve mimari",g:["Başlangıç","Teknik Mimari","Sunucu & Altyapı"],a:"Projenin kapsamını, teknoloji yığınını, veri modelini, ortamları ve altyapıyı kararlara göre kurmak ya da hizalamak."}',
     '{t:"Proje temeli ve mimari",g:["Başlangıç","Teknik Mimari","Sunucu & Altyapı"],a:"Projenin kapsamını, teknoloji yığınını, veri modelini, panel ve portal mimarisini, ortamları ve altyapıyı kararlara göre kurmak ya da hizalamak.",pz:true}')
hook('let ds=p.ds&&typeof dsActive==="function"&&dsActive();if(G.length||ds)out.push({t:p.t,a:p.a,G,ds})',
     'let ds=p.ds&&typeof dsActive==="function"&&dsActive(),pz=p.pz&&typeof pzActive==="function"&&pzActive();if(G.length||ds||pz)out.push({t:p.t,a:p.a,G,ds,pz})')
hook('${p.ds?" + tasarım şartnamesi":""}|', '${p.ds?" + tasarım şartnamesi":""}${p.pz?" + panel mimarisi":""}|') if '${p.ds?" + tasarım şartnamesi":""}|' in h else None
hook('${p.ds?" + tasarım şartnamesi":""} |', '${p.ds?" + tasarım şartnamesi":""}${p.pz?" + panel mimarisi":""} |') if '${p.ds?" + tasarım şartnamesi":""} |' in h else None
hook('${p.ds?(p.G.length?"\\n\\n":"")+dsMd():""}', '${p.ds?(p.G.length?"\\n\\n":"")+dsMd():""}${p.pz?"\\n\\n"+pzMd():""}')
assert '${p.pz?" + panel mimarisi":""}' in h, 'faz listesi kancası'

# 4) Dokümantasyon
DOC = ('<li><b>Panel &amp; Portal Mimarisi:</b> Teknik Mimari grubundaki bölümün ilk alt başlığı <b>Panel ve Portal Envanteri</b>dir (sol menüde kararlar gibi açılır; '
       'önceki / sonraki gezinmesine, ilerlemeye ve yeşil tamamlandı işaretine katılır — en az bir panel eklenince tamamlanmış sayılır). Envanterde 21 şablon '
       '(süper yönetici, CMS, operasyon, müşteri, tedarikçi, satıcı, iş ortağı, bayi, üye, şirket yöneticisi, çalışan, finans, CRM, destek, pazarlama, analitik, eğitmen, '
       'geliştirici / API, denetçi, çalışma alanı ve özel panel) ve sınırsız özel panel bulunur. Her panelin adresi (alt alan adı, alt dizin, ayrı alan adı; tam adres önizlemesi, slug '
       'doğrulama, rezerve yol ve çakışma uyarıları), sunan uygulaması, dağıtım sınırı, kimlik doğrulama kapsamı, rolleri ve izin matrisi, modülleri (özel modül eklenebilir), '
       'veri izolasyonu, arayüzü, güvenlik önlemleri ve dağıtımı ayrı sekmelerde düzenlenir. Proje türüne göre başlangıç mimarisi önerilir (yalnız “Öneriyi uygula” ile). '
       'Bölümün diğer on kararı adres yaklaşımı, uygulama ve dağıtım topolojisi, kimlik, organizasyon modeli, veri izolasyonu, yetkilendirme, oturum, API erişimi ve yönetim panellerindeki zorunlu önlemlerdir. '
       'İlk panel eklenince envanter Claude promptuna (PANEL VE PORTAL MİMARİSİ), Proje Kuralları’na, talimat dosyasının ilk fazına ve proje dosyasına '
       '(<code>panelArchitecture</code>, JSON) yazılır.</li>')
m = re.search(r'<li><b>Panel &amp; Portal Mimarisi:</b>.*?</li>', h)
if m:
    h = h[:m.start()] + DOC + h[m.end():]
else:
    a = h.index('<li><b>Tasarım Parametreleri ve teknik çıktı:</b>')
    b = h.index('</li>', a) + len('</li>')
    h = h[:b] + DOC + h[b:]

open(hp, 'w', encoding='utf-8').write(h)
print('tamam · md5', hashlib.md5(h.encode('utf-8')).hexdigest(), '· boyut', len(h.encode('utf-8')))
