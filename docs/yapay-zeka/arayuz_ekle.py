#!/usr/bin/env python3
"""Yapay Zekâ menü alanını uygulamaya bağlar (2026-11-12). docs/google/arayuz_ekle.py ve docs/meta/arayuz_ekle.py'den SONRA
çalışır (kancalar onların metnine yazılır; "uygulandı" işaretleri önektir, önceki betikleri bozmaz).

Kullanım:
    python3 -I docs/yapay-zeka/arayuz_ekle.py web-proje-gelistirme.html

Yaptıkları (tekrar çalıştırılabilir): <style id="v26-ai"> ← docs/v26/v26-ai.css; ana betikte /*V26-AI:BEGIN*/…END*/ ←
docs/v26/v26-ai.js; AREA / LAST / AREA_LB'ye "ai" ("Yapay Zekâ"); Pazarlama alt başlıklarına #sideAiBtn; şerit etiketi,
arama kelimeleri, kod satırı; Proje Kuralları'nda "Yapay Zekâ" başlığı ve Claude promptunda YAPAY ZEKÂ GÖRÜNÜRLÜĞÜ VE AYARLARI;
talimat dosyasında "Yapay zekâ görünürlüğü ve ayarları" fazı; JSON'da Pazarlama Kararları (yz_ → marketing, aiSetup), proje
dosyasında aiSetup; yz_report bölümünde yzExportBox; V26 modül şeridinde "Yapay Zekâ", Özet kartı, indirme uyarısı;
Dokümantasyon paragrafı. Veriye dokunmaz (docs/yapay-zeka/yz_ekle.py).
"""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
JS = open(ROOT + "/docs/v26/v26-ai.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-ai.css", encoding="utf-8").read().strip()


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


def put(s, pattern, block, anchor, before=True):
    """Blok varsa yerinde yeniler (sırası korunur), yoksa anchor'dan önce ekler. Tekrar çalıştırmada dosya aynı kalır."""
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    if s.count(anchor) != 1:
        fail("bağlantı noktası tek değil: " + anchor[:60])
    return s.replace(anchor, block + anchor if before else anchor + block)


def main():
    if len(sys.argv) != 2:
        fail("kullanım: arayuz_ekle.py <html>")
    path = sys.argv[1]
    s = open(path, encoding="utf-8").read()
    for t in (JS, CSS):
        if "</script" in t.lower() or "<!--" in t:
            fail("kaynakta </script ya da <!-- var")
    if 'id="sideMetaBtn"' not in s:
        fail("önce docs/google/arayuz_ekle.py ve docs/meta/arayuz_ekle.py çalıştırılmalı")

    s = put(s, r'<style id="v26-ai">.*?</style>\n', '<style id="v26-ai">\n' + CSS + '\n</style>\n', '<style id="v26-approval">')
    s = put(s, r"/\*V26-AI:BEGIN\*/.*?/\*V26-AI:END\*/\n", "/*V26-AI:BEGIN*/\n" + JS + "\n/*V26-AI:END*/\n", "function mkRuleGroups(){")

    s = once(s, 's.sub==="meta")?s.sub:(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",google:"",meta:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google Servisleri",meta:"Meta Servisleri",common:"Ortak Bilgiler"}',
             's.sub==="meta"||s.sub==="ai")?s.sub:(s&&s.area)||"project",LAST={project:"project",marketing:"",audit:"",google:"",meta:"",ai:"",common:""},AREA_LB={marketing:"Pazarlama",audit:"SEO Denetimi",google:"Google Servisleri",meta:"Meta Servisleri",ai:"Yapay Zekâ",common:"Ortak Bilgiler"}',
             's.sub==="ai"')
    s = once(s, '<button id="sideMetaBtn" type="button" class="sideSubBtn">Meta Servisleri</button>',
             '<button id="sideMetaBtn" type="button" class="sideSubBtn">Meta Servisleri</button><button id="sideAiBtn" type="button" class="sideSubBtn">Yapay Zekâ</button>', 'id="sideAiBtn"')
    s = once(s, 'a==="google"||a==="meta";', 'a==="google"||a==="meta"||a==="ai";', 'a==="meta"||a==="ai"')
    s = once(s, 'sideMetaBtn.toggleAttribute("aria-current",a==="meta");', 'sideMetaBtn.toggleAttribute("aria-current",a==="meta");sideAiBtn.classList.toggle("active",a==="ai");sideAiBtn.toggleAttribute("aria-current",a==="ai");', 'sideAiBtn.classList.toggle')
    s = once(s, 'sideMetaBtn.onclick=()=>goArea("meta");', 'sideMetaBtn.onclick=()=>goArea("meta");sideAiBtn.onclick=()=>goArea("ai");', 'sideAiBtn.onclick')
    s = once(s, 'ca==="meta"?"Pazarlama › Meta Servisleri":', 'ca==="meta"?"Pazarlama › Meta Servisleri":ca==="ai"?"Pazarlama › Yapay Zekâ":', '"Pazarlama › Yapay Zekâ"')
    s = once(s, 'g.a==="google"||g.a==="meta"?"Pazarlama · ":"")', 'g.a==="google"||g.a==="meta"||g.a==="ai"?"Pazarlama · ":"")', 'g.a==="meta"||g.a==="ai"')
    s = once(s, 'AREA(s)==="meta"?" meta servisleri facebook instagram whatsapp kurulum":""', 'AREA(s)==="meta"?" meta servisleri facebook instagram whatsapp kurulum":AREA(s)==="ai"?" yapay zeka ai chatgpt gemini copilot perplexity":""', '" yapay zeka ai chatgpt')
    s = once(s, 'AREA(s)==="google"||AREA(s)==="meta"?"Pazarlama · ":"")', 'AREA(s)==="google"||AREA(s)==="meta"||AREA(s)==="ai"?"Pazarlama · ":"")', 'AREA(s)==="meta"||AREA(s)==="ai"')

    s = once(s, 'mt=mtRuleGroups(),rg=g=>', 'mt=mtRuleGroups(),yz=yzRuleGroups(),rg=g=>', 'mt=mtRuleGroups(),yz=yzRuleGroups(),')
    s = once(s, """(mt.length?'<h2 class="areaHead">Meta Servisleri</h2>'+mt.map(rg).join(""):"")""",
             """(mt.length?'<h2 class="areaHead">Meta Servisleri</h2>'+mt.map(rg).join(""):"")+(yz.length?'<h2 class="areaHead">Yapay Zekâ</h2>'+yz.map(rg).join(""):"")""",
             '<h2 class="areaHead">Yapay Zekâ</h2>')
    s = once(s, '${mtPrompt(mt)}', '${mtPrompt(mt)}${yzPrompt(yz)}', '${yzPrompt(yz)}')
    s = once(s, 'G:MT});\n return out}',
             'G:MT});\n let YZ=typeof yzRuleGroups==="function"?yzRuleGroups():[];if(YZ.length)out.push({t:"Yapay zekâ görünürlüğü ve ayarları",a:"İşletme, ürün ve hizmet bilgilerinin yapay zekâ asistanlarında doğru görünmesi için robots.txt ve tarayıcı izinlerini, yapısal veriyi, ürün / hizmet beslemelerini ve sitedeki yapay zekâ asistanının bildirimlerini uygulamak; platform kayıtlarını (işletme, satıcı, uygulama) kullanıcıya kontrol listesi olarak vermek.",G:YZ});\n return out}',
             'Yapay zekâ görünürlüğü ve ayarları"')

    s = once(s, 'return a==="marketing"||a==="google"||a==="meta"?"marketing"', 'return a==="marketing"||a==="google"||a==="meta"||a==="ai"?"marketing"', 'a==="meta"||a==="ai"?"marketing"')
    s = once(s, 'return /^(mk|gg|mt)_/.test(k)', 'return /^(mk|gg|mt|yz)_/.test(k)', '/^(mk|gg|mt|yz')
    s = once(s, 'areas:["marketing","google","meta"],', 'areas:["marketing","google","meta","ai"],', 'areas:["marketing","google","meta","ai"')
    s = once(s, 'reklam hesabı, katalog); pazarlama kuralları', 'reklam hesabı, katalog) ve yapay zekâ görünürlüğü ayarları (ChatGPT ve diğer yapay zekâ platformları); pazarlama kuralları', 've yapay zekâ görünürlüğü ayarları')
    s = once(s, 'mkMarketingPrompt(),...ggPf(),...mtPf()};', 'mkMarketingPrompt(),...ggPf(),...mtPf(),...yzPf()};', 'mtPf(),...yzPf()};')
    s = once(s, '...ggPf(),...mtPf(),...dsPf()', '...ggPf(),...mtPf(),...yzPf(),...dsPf()', 'mtPf(),...yzPf(),')
    s = once(s, '+(s.id==="mt_report"?mtExportBox():"")', '+(s.id==="mt_report"?mtExportBox():"")+(s.id==="yz_report"?yzExportBox():"")', 'yzExportBox():""')

    s = once(s, '["meta","Meta","goArea(\'meta\')"],', '["meta","Meta","goArea(\'meta\')"],["ai","Yapay Zekâ","goArea(\'ai\')"],', '["ai","Yapay Zekâ","goArea(\'ai\')"]')
    s = once(s, ' meta:"M7 8c', ' ai:"M12 3l1.8 4.6L18 9.4l-4.2 1.8L12 16l-1.8-4.8L6 9.4l4.2-1.8L12 3ZM19 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8.8-2Z",\n meta:"M7 8c', ' ai:"M12 3l1.8')
    s = once(s, 'mt=ap("meta"),', 'mt=ap("meta"),yz=ap("ai"),', 'yz=ap("ai"),')
    s = once(s, '"Kurulumu planla","goArea(\'meta\')")}', '"Kurulumu planla","goArea(\'meta\')")}${mod("Yapay Zekâ",`${yz[0]} / ${yz[1]} karar verildi.`,"Ayarları planla","goArea(\'ai\')")}', 'goArea(\'ai\')")}')
    s = once(s, '["meta","Meta Servisleri"]]', '["meta","Meta Servisleri"],["ai","Yapay Zekâ"]]', '["ai","Yapay Zekâ"]')

    s = once(s, 'Kampanya stratejisi Pazarlama Kararları › Meta Ads’te kalır.</p></div>',
             'Kampanya stratejisi Pazarlama Kararları › Meta Ads’te kalır.</p><p><b>Yapay Zekâ</b> (Pazarlama’nın alt başlığı; modül şeridinde ayrı menü) işletmenin, ürünlerinin ve hizmetlerinin ChatGPT ve diğer yapay zekâ asistanlarında doğru görünmesi için yapılacakları karar olarak sunar: ChatGPT’de işletme bilgileri, yapay zekâ üzerinden alışveriş, diğer platformların işletme ve ürün programları, yapay zekâ tarayıcılarına izinler, sitedeki yapay zekâ asistanının bildirimleri ve ölçüm. Kararlar Proje Kuralları’nda <b>Yapay Zekâ</b> başlığı altında, Claude promptunda “YAPAY ZEKÂ GÖRÜNÜRLÜĞÜ VE AYARLARI” bölümünde ve talimat dosyasının “Yapay zekâ görünürlüğü ve ayarları” fazında yer alır; <b>Kurulum Planı &amp; Talimat</b> bölümünden ayrı bir talimat (.md) olarak da alınır.</p></div>',
             '<p><b>Yapay Zekâ</b> (Pazarlama’nın alt başlığı')

    open(path, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
