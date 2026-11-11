#!/usr/bin/env python3
"""Meta Servisleri menü alanını uygulamaya bağlar (2026-11-11). docs/google/arayuz_ekle.py'den SONRA çalışır
(kancalar Google eklemesinden sonraki metinlere yazılır).

Kullanım:
    python3 -I docs/meta/arayuz_ekle.py web-proje-gelistirme.html

Yaptıkları (tekrar çalıştırılabilir; her kanca yalnız eksikse eklenir, kod ve stil blokları her seferinde kaynaktan yenilenir):
  - <style id="v26-meta"> ← docs/v26/v26-meta.css (v26-approval stilinden önce)
  - ana betikte /*V26-META:BEGIN*/ … /*V26-META:END*/ ← docs/v26/v26-meta.js (function mkRuleGroups(){ öncesinde)
  - AREA / LAST / AREA_LB: sub:"meta" bölümleri kendi menü alanıdır ("meta", etiket "Meta Servisleri")
  - Pazarlama alt başlıkları: #sideMetaBtn (Google Servisleri'nden sonra), areaBtn, onclick
  - renderSideNav şerit etiketi, grup aria-label öneki, arama kelimeleri; renderFields kod satırı öneki
  - renderRules: Proje Kuralları'nda "Meta Servisleri" başlığı, Claude promptunda META SERVİSLERİ KURULUMU (mtPrompt)
  - talimat dosyası (phases): "Meta servisleri kurulumu" fazı
  - JSON: meta alanları Pazarlama Kararları dosyasında (exOwn, EX_PARTS areas, metaSetup), proje dosyasında metaSetup
  - guideHtml: mt_report bölümünde mtExportBox
  - V26: modül şeridinde "Meta", Özet'te modül kartı, indirme uyarısındaki alan sayısı
  - Dokümantasyon > Pazarlama: Meta Servisleri paragrafı
Veri (bölümler, kararlar, rehberler, kimlik satırları) docs/meta/meta_ekle.py ile yazılır; bu betik veriye dokunmaz.
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-meta.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-meta.css", encoding="utf-8").read().strip()


def fail(m):
    sys.exit("HATA: " + m)


def once(s, old, new, done_marker):
    """old tam 1 kez geçmeli; done_marker varsa zaten uygulanmış sayılır."""
    if done_marker in s:
        return s
    n = s.count(old)
    if n != 1:
        fail(f"{n} eşleşme: {old[:90]!r}")
    return s.replace(old, new)


def main():
    if len(sys.argv) != 2:
        fail("kullanım: arayuz_ekle.py <html>")
    path = sys.argv[1]
    s = open(path, encoding="utf-8").read()
    for t in (JS, CSS):
        if "</script" in t.lower() or "<!--" in t:
            fail("kaynakta </script ya da <!-- var")
    if 'id="sideGoogleBtn"' not in s:
        fail("önce docs/google/arayuz_ekle.py çalıştırılmalı")

    # stil ve kod blokları
    s = re.sub(r'<style id="v26-meta">.*?</style>\n?', "", s, flags=re.S)
    s = once(s, '<style id="v26-approval">', '<style id="v26-meta">\n' + CSS + '\n</style>\n<style id="v26-approval">', "@@never@@")
    s = re.sub(r"/\*V26-META:BEGIN\*/.*?/\*V26-META:END\*/\n?", "", s, flags=re.S)
    s = once(s, "function mkRuleGroups(){", "/*V26-META:BEGIN*/\n" + JS + "\n/*V26-META:END*/\nfunction mkRuleGroups(){", "@@never@@")

    # alan tanımı
    s = once(s,
             'AREA=s=>s&&(s.sub==="audit"||s.sub==="google")?s.sub:(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",google:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google Servisleri",common:"Ortak Bilgiler"}',
             'AREA=s=>s&&(s.sub==="audit"||s.sub==="google"||s.sub==="meta")?s.sub:(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",google:"",meta:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google Servisleri",meta:"Meta Servisleri",common:"Ortak Bilgiler"}',
             's.sub==="meta"')

    # Pazarlama alt başlıkları
    s = once(s, '<button id="sideGoogleBtn" type="button" class="sideSubBtn">Google Servisleri</button>',
             '<button id="sideGoogleBtn" type="button" class="sideSubBtn">Google Servisleri</button><button id="sideMetaBtn" type="button" class="sideSubBtn">Meta Servisleri</button>',
             'id="sideMetaBtn"')
    s = once(s, 'm=a==="marketing"||a==="audit"||a==="google";', 'm=a==="marketing"||a==="audit"||a==="google"||a==="meta";', 'a==="google"||a==="meta"')
    s = once(s, 'sideGoogleBtn.toggleAttribute("aria-current",a==="google");',
             'sideGoogleBtn.toggleAttribute("aria-current",a==="google");sideMetaBtn.classList.toggle("active",a==="meta");sideMetaBtn.toggleAttribute("aria-current",a==="meta");',
             'sideMetaBtn.classList.toggle')
    s = once(s, 'sideGoogleBtn.onclick=()=>goArea("google");', 'sideGoogleBtn.onclick=()=>goArea("google");sideMetaBtn.onclick=()=>goArea("meta");', 'sideMetaBtn.onclick')

    # menü ve başlık metinleri
    s = once(s, 'ca==="google"?"Pazarlama › Google Servisleri":', 'ca==="google"?"Pazarlama › Google Servisleri":ca==="meta"?"Pazarlama › Meta Servisleri":', '"Pazarlama › Meta Servisleri"')
    s = once(s, '(g.a==="marketing"||g.a==="audit"||g.a==="google"?"Pazarlama · ":"")', '(g.a==="marketing"||g.a==="audit"||g.a==="google"||g.a==="meta"?"Pazarlama · ":"")', 'g.a==="google"||g.a==="meta"')
    s = once(s, 'AREA(s)==="google"?" google servisleri kurulum":""', 'AREA(s)==="google"?" google servisleri kurulum":AREA(s)==="meta"?" meta servisleri facebook instagram whatsapp kurulum":""', '" meta servisleri facebook instagram whatsapp kurulum"')
    s = once(s, '((AREA(s)==="marketing"||AREA(s)==="audit"||AREA(s)==="google"?"Pazarlama · ":"")', '((AREA(s)==="marketing"||AREA(s)==="audit"||AREA(s)==="google"||AREA(s)==="meta"?"Pazarlama · ":"")', 'AREA(s)==="google"||AREA(s)==="meta"')

    # kurallar ve prompt
    s = once(s, 'gg=ggRuleGroups(),rg=g=>', 'gg=ggRuleGroups(),mt=mtRuleGroups(),rg=g=>', 'gg=ggRuleGroups(),mt=mtRuleGroups(),')
    s = once(s, """(gg.length?'<h2 class="areaHead">Google Servisleri</h2>'+gg.map(rg).join(""):"")""",
             """(gg.length?'<h2 class="areaHead">Google Servisleri</h2>'+gg.map(rg).join(""):"")+(mt.length?'<h2 class="areaHead">Meta Servisleri</h2>'+mt.map(rg).join(""):"")""",
             '<h2 class="areaHead">Meta Servisleri</h2>')
    s = once(s, '${ggPrompt(gg)}', '${ggPrompt(gg)}${mtPrompt(mt)}', '${mtPrompt(mt)}')

    # talimat dosyası fazı
    s = once(s, 'G:GG});\n return out}',
             'G:GG});\n let MT=typeof mtRuleGroups==="function"?mtRuleGroups():[];if(MT.length)out.push({t:"Meta servisleri kurulumu",a:"Meta Pikseli ve Conversions API\'yi onay altyapısıyla birlikte kurmak, alan adı doğrulama kaydını, WhatsApp bağlantılarını ve webhook\'larını, katalog feed\'ini uygulamak; işletme portföyü, Sayfa, Instagram, WhatsApp ve reklam hesabı panellerinde yapılacak ayarları kullanıcıya menü yoluyla kontrol listesi olarak vermek.",G:MT});\n return out}',
             'Meta servisleri kurulumu"')

    # JSON ve proje dosyası
    s = once(s, 'return a==="marketing"||a==="google"?"marketing":a==="audit"?"audit":"project"}return /^(mk|gg)_/.test(k)?"marketing"',
             'return a==="marketing"||a==="google"||a==="meta"?"marketing":a==="audit"?"audit":"project"}return /^(mk|gg|mt)_/.test(k)?"marketing"',
             '/^(mk|gg|mt')
    s = once(s, 'areas:["marketing","google"],', 'areas:["marketing","google","meta"],', 'areas:["marketing","google","meta"')
    s = once(s, 'İşletme Profili, Merchant Center, Looker Studio); pazarlama kuralları',
             'İşletme Profili, Merchant Center, Looker Studio) ile Meta servisleri kurulumu (işletme portföyü, Facebook Sayfası, Instagram, WhatsApp Business, Meta Pikseli ve Conversions API, reklam hesabı, katalog); pazarlama kuralları',
             'ile Meta servisleri kurulumu (işletme portföyü')
    s = once(s, 'mkMarketingPrompt(),...ggPf()};', 'mkMarketingPrompt(),...ggPf(),...mtPf()};', 'mkMarketingPrompt(),...ggPf(),...mtPf()')
    s = once(s, '...auPf(),...ggPf(),', '...auPf(),...ggPf(),...mtPf(),', '...auPf(),...ggPf(),...mtPf(),')

    # dışa aktarım kartı
    s = once(s, '+(s.id==="gg_report"?ggExportBox():"")', '+(s.id==="gg_report"?ggExportBox():"")+(s.id==="mt_report"?mtExportBox():"")', 'mtExportBox():""')

    # V26: modül şeridi, ikon, Özet, indirme uyarısı
    s = once(s, '["google","Google","goArea(\'google\')"],', '["google","Google","goArea(\'google\')"],["meta","Meta","goArea(\'meta\')"],', '["meta","Meta","goArea(\'meta\')"]')
    s = once(s, ' google:"M9 15l6-6', ' meta:"M7 8c-2.2 0-4 1.8-4 4s1.8 4 4 4c2.5 0 3.5-2 5-4s2.5-4 5-4c2.2 0 4 1.8 4 4s-1.8 4-4 4c-2.5 0-3.5-2-5-4S9.5 8 7 8Z",\n google:"M9 15l6-6', ' meta:"M7 8c')
    s = once(s, 'gg=ap("google"),', 'gg=ap("google"),mt=ap("meta"),', 'mt=ap("meta"),')
    s = once(s, '"Kurulumu planla","goArea(\'google\')")}', '"Kurulumu planla","goArea(\'google\')")}${mod("Meta Servisleri",`${mt[0]} / ${mt[1]} karar verildi.`,"Kurulumu planla","goArea(\'meta\')")}', 'goArea(\'meta\')")}')
    s = once(s, '["google","Google Servisleri"]]', '["google","Google Servisleri"],["meta","Meta Servisleri"]]', '["meta","Meta Servisleri"]')

    # Dokümantasyon
    s = once(s, 'Kimlikler Ortak Bilgiler › Hesap ve Etiket Kimlikleri’ne yazılır.</p></div>',
             'Kimlikler Ortak Bilgiler › Hesap ve Etiket Kimlikleri’ne yazılır.</p><p><b>Meta Servisleri</b> (Pazarlama’nın alt başlığı) işletme portföyü (Meta Business Suite), Facebook Sayfası, Instagram, WhatsApp Business, Meta Pikseli ve Conversions API, reklam hesabı ve katalogun kurulumunu ve asgari ayarlarını karar olarak sunar; KVKK, çerez onayı ve ticari ileti onayı ayrı bir bölümdedir. Kararlar Proje Kuralları’nda <b>Meta Servisleri</b> başlığı altında, Claude promptunda “META SERVİSLERİ KURULUMU” bölümünde ve talimat dosyasının “Meta servisleri kurulumu” fazında yer alır; <b>Kurulum Planı &amp; Talimat</b> bölümünden ayrı bir kurulum talimatı (.md) olarak da alınır. Kampanya stratejisi Pazarlama Kararları › Meta Ads’te kalır.</p></div>',
             '<p><b>Meta Servisleri</b> (Pazarlama’nın alt başlığı)')

    open(path, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
