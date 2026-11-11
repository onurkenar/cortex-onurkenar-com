#!/usr/bin/env python3
"""Google Servisleri menü alanını uygulamaya bağlar (2026-11-11).

Kullanım:
    python3 -I docs/google/arayuz_ekle.py web-proje-gelistirme.html

Yaptıkları (tekrar çalıştırılabilir; her kanca yalnız eksikse eklenir, kod ve stil blokları her seferinde kaynaktan yenilenir):
  - <style id="v26-google"> ← docs/v26/v26-google.css (v26-approval stilinden önce)
  - ana betikte /*V26-GOOGLE:BEGIN*/ … /*V26-GOOGLE:END*/ ← docs/v26/v26-google.js (function mkRuleGroups(){ öncesinde)
  - AREA / LAST / AREA_LB: sub:"google" bölümleri kendi menü alanıdır ("google", etiket "Google Servisleri")
  - Pazarlama alt başlıkları: #sideGoogleBtn (SEO Denetimi'nden sonra), areaBtn, onclick
  - renderSideNav şerit etiketi, grup aria-label öneki, arama kelimeleri; renderFields kod satırı öneki
  - renderRules: Proje Kuralları'nda "Google Servisleri" başlığı, Claude promptunda GOOGLE SERVİSLERİ KURULUMU (ggPrompt)
  - talimat dosyası (phases): "Google servisleri ve ölçüm kurulumu" fazı
  - JSON: google alanları Pazarlama Kararları dosyasında (exOwn, EX_PARTS areas, googleSetup), proje dosyasında googleSetup
  - guideHtml: gg_report bölümünde ggExportBox
  - V26: modül şeridinde "Google", Özet'te modül kartı, indirme uyarısındaki alan sayısı
  - Dokümantasyon > Pazarlama: Google Servisleri paragrafı
Veri (bölümler, kararlar, rehberler) docs/google/google_ekle.py ile yazılır; bu betik veriye dokunmaz.
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-google.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-google.css", encoding="utf-8").read().strip()


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

    # stil bloğu
    s = re.sub(r'<style id="v26-google">.*?</style>\n?', "", s, flags=re.S)
    s = once(s, '<style id="v26-approval">', '<style id="v26-google">\n' + CSS + '\n</style>\n<style id="v26-approval">', "@@never@@")

    # kod bloğu
    s = re.sub(r"/\*V26-GOOGLE:BEGIN\*/.*?/\*V26-GOOGLE:END\*/\n?", "", s, flags=re.S)
    s = once(s, "function mkRuleGroups(){", "/*V26-GOOGLE:BEGIN*/\n" + JS + "\n/*V26-GOOGLE:END*/\nfunction mkRuleGroups(){", "@@never@@")

    # alan tanımı
    s = once(s,
             'AREA=s=>s&&s.sub==="audit"?"audit":(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",common:"Ortak Bilgiler"}',
             'AREA=s=>s&&(s.sub==="audit"||s.sub==="google")?s.sub:(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",google:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google Servisleri",common:"Ortak Bilgiler"}',
             's.sub==="google")?s.sub')

    # Pazarlama alt başlıkları
    s = once(s, '<button id="sideAuditBtn" type="button" class="sideSubBtn">SEO Denetimi</button>',
             '<button id="sideAuditBtn" type="button" class="sideSubBtn">SEO Denetimi</button><button id="sideGoogleBtn" type="button" class="sideSubBtn">Google Servisleri</button>',
             'id="sideGoogleBtn"')
    s = once(s, 'm=a==="marketing"||a==="audit";', 'm=a==="marketing"||a==="audit"||a==="google";', 'a==="audit"||a==="google";')
    s = once(s, 'sideAuditBtn.toggleAttribute("aria-current",a==="audit");',
             'sideAuditBtn.toggleAttribute("aria-current",a==="audit");sideGoogleBtn.classList.toggle("active",a==="google");sideGoogleBtn.toggleAttribute("aria-current",a==="google");',
             'sideGoogleBtn.classList.toggle')
    s = once(s, 'sideAuditBtn.onclick=()=>goArea("audit");', 'sideAuditBtn.onclick=()=>goArea("audit");sideGoogleBtn.onclick=()=>goArea("google");', 'sideGoogleBtn.onclick')

    # menü ve başlık metinleri
    s = once(s, '${ca==="audit"?"Pazarlama › SEO Denetimi":ca==="common"?', '${ca==="audit"?"Pazarlama › SEO Denetimi":ca==="google"?"Pazarlama › Google Servisleri":ca==="common"?', '"Pazarlama › Google Servisleri"')
    s = once(s, '(g.a==="marketing"||g.a==="audit"?"Pazarlama · ":"")', '(g.a==="marketing"||g.a==="audit"||g.a==="google"?"Pazarlama · ":"")', 'g.a==="audit"||g.a==="google"')
    s = once(s, '"pazarlama marketing"+(AU(s)?" seo denetimi audit":"")', '"pazarlama marketing"+(AU(s)?" seo denetimi audit":AREA(s)==="google"?" google servisleri kurulum":"")', '" google servisleri kurulum"')
    s = once(s, '((AREA(s)==="marketing"||AREA(s)==="audit"?"Pazarlama · ":"")', '((AREA(s)==="marketing"||AREA(s)==="audit"||AREA(s)==="google"?"Pazarlama · ":"")', 'AREA(s)==="audit"||AREA(s)==="google"?')

    # kurallar ve prompt
    s = once(s, 'mg=mkRuleGroups(),rg=g=>', 'mg=mkRuleGroups(),gg=ggRuleGroups(),rg=g=>', 'gg=ggRuleGroups(),rg=')
    s = once(s, """(mg.length?'<h2 class="areaHead">Pazarlama</h2>'+mg.map(rg).join(""):"")""",
             """(mg.length?'<h2 class="areaHead">Pazarlama</h2>'+mg.map(rg).join(""):"")+(gg.length?'<h2 class="areaHead">Google Servisleri</h2>'+gg.map(rg).join(""):"")""",
             '<h2 class="areaHead">Google Servisleri</h2>')
    s = once(s, '${mkPrompt(mg)}', '${mkPrompt(mg)}${ggPrompt(gg)}', '${ggPrompt(gg)}')

    # talimat dosyası fazı
    s = once(s, 'G:M});\n return out}',
             'G:M});\n let GG=typeof ggRuleGroups==="function"?ggRuleGroups():[];if(GG.length)out.push({t:"Google servisleri ve ölçüm kurulumu",a:"Google etiketini ya da Tag Manager\'ı, Consent Mode varsayılanlarını, ölçüm olaylarını, doğrulama kayıtlarını ve hesap bağlantılarını kurmak; Google panellerinde yapılacak ayarları kullanıcıya menü yoluyla kontrol listesi olarak vermek.",G:GG});\n return out}',
             'Google servisleri ve ölçüm kurulumu"')

    # JSON ve proje dosyası
    s = once(s, 'return a==="marketing"?"marketing":a==="audit"?"audit":"project"}return /^mk_/.test(k)?"marketing"',
             'return a==="marketing"||a==="google"?"marketing":a==="audit"?"audit":"project"}return /^(mk|gg)_/.test(k)?"marketing"',
             '/^(mk|gg)_/')
    s = once(s, 'f:"pazarlama-kararlari",areas:["marketing"],', 'f:"pazarlama-kararlari",areas:["marketing","google"],', 'areas:["marketing","google"]')
    s = once(s, 'ölçüm, yayım ve dağıtım ile iş akışı kararları; pazarlama kuralları',
             'ölçüm, yayım ve dağıtım ile iş akışı kararları ve Google servisleri kurulumu (Tag Manager, Analytics, Ads, Search Console, İşletme Profili, Merchant Center, Looker Studio); pazarlama kuralları',
             've Google servisleri kurulumu (Tag Manager')
    s = once(s, 'marketingPrompt:mkMarketingPrompt()};', 'marketingPrompt:mkMarketingPrompt(),...ggPf()};', 'mkMarketingPrompt(),...ggPf()')
    s = once(s, '...auPf(),...dsPf(),', '...auPf(),...ggPf(),...dsPf(),', '...auPf(),...ggPf(),')

    # dışa aktarım kartı
    s = once(s, '+(s.id==="au_report"?auExportBox():"")', '+(s.id==="au_report"?auExportBox():"")+(s.id==="gg_report"?ggExportBox():"")', 'ggExportBox():""')

    # V26: modül şeridi, ikon, Özet, indirme uyarısı
    s = once(s, '["audit","SEO Denetimi","goArea(\'audit\')"],', '["audit","SEO Denetimi","goArea(\'audit\')"],["google","Google","goArea(\'google\')"],', '["google","Google","goArea(\'google\')"]')
    s = once(s, ' audit:"M11 18a7', ' google:"M9 15l6-6M10 6l1-1a4 4 0 0 1 6 6l-1 1M14 18l-1 1a4 4 0 0 1-6-6l1-1",\n audit:"M11 18a7', ' google:"M9 15l6-6')
    s = once(s, 'au=ap("audit"),', 'au=ap("audit"),gg=ap("google"),', 'gg=ap("google"),')
    s = once(s, 'Denetimi planla","goArea(\'audit\')")}', 'Denetimi planla","goArea(\'audit\')")}${mod("Google Servisleri",`${gg[0]} / ${gg[1]} karar verildi.`,"Kurulumu planla","goArea(\'google\')")}', 'Kurulumu planla"')
    s = once(s, '["audit","SEO Denetimi"]]', '["audit","SEO Denetimi"],["google","Google Servisleri"]]', '["google","Google Servisleri"]]')

    # Dokümantasyon
    s = once(s, 'bir Claude oturumu için ayrı bir pazarlama promptu kopyalanır.</p></div>',
             'bir Claude oturumu için ayrı bir pazarlama promptu kopyalanır.</p><p><b>Google Servisleri</b> (Pazarlama’nın alt başlığı) Tag Manager, Google Analytics 4, Consent Mode, Search Console, Google Ads, Merchant Center, İşletme Profili ve Looker Studio’nun kurulumunu ve asgari ayarlarını karar olarak sunar; her bölümün rehberi kurulum adımlarını ve resmî belgeleri gösterir. Kararlar Proje Kuralları’nda <b>Google Servisleri</b> başlığı altında, Claude promptunda “GOOGLE SERVİSLERİ KURULUMU” bölümünde ve talimat dosyasının “Google servisleri ve ölçüm kurulumu” fazında yer alır. <b>Kurulum Planı &amp; Talimat</b> bölümünden aynı kurallar bağlam ve kimliklerle birlikte ayrı bir kurulum talimatı (.md) olarak alınır. Kimlikler Ortak Bilgiler › Hesap ve Etiket Kimlikleri’ne yazılır.</p></div>',
             '<p><b>Google Servisleri</b> (Pazarlama’nın alt başlığı)')

    open(path, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
