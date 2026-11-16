# -*- coding: utf-8 -*-
"""8. İçerik Planlama menü alanını uygulamaya bağlar (2026-11-15; ilk sürüm aynı gün yer tutucu sayfaydı).
Kullanım: python3 -I docs/v26/icerik_planlama_ekle.py web-proje-gelistirme.html
docs/yapay-zeka/arayuz_ekle.py'den SONRA çalışır (kancalar onun metnine yazılır). Veri: docs/icerik-planlama/plan_alani_ekle.py.
Yaptıkları (tekrar çalıştırılabilir):
- ana betikte /*V26-PLAN:BEGIN*/…END*/ ← docs/v26/v26-plan-core.js (ipRuleGroups, ipPrompt; mkRuleGroups'tan önce)
- <style id="v26-content-plan"> ve <script id="v26-content-plan"> ← v26-content-plan.{css,js} (v26-mobile'dan önce, v26-todo'dan sonra)
- kancalar: AREA / LAST / AREA_LB'ye "plan" ("İçerik Planlama"); sol menü başlık şeridi; arama kelimeleri; Proje Kuralları'nda
  "İçerik Planlama" başlığı ve Claude promptunda İÇERİK PLANI AYARLARI; talimat dosyasında "İçerik planı ayarları" fazı;
  JSON'da Pazarlama Kararları (ip_ → marketing, areas'a "plan"); Özet'te İçerik Planlama kartı; İndirmeler alan listesi;
  modül şeridinde "İçerik Planlama" (MODS + ICON). Pazarlama alt başlıklarına girmez (kendi ana menüsü)."""
import re
import sys

ROOT = __file__.rsplit("/docs/", 1)[0]
CORE = open(ROOT + "/docs/v26/v26-plan-core.js", encoding="utf-8").read().strip()
JS = open(ROOT + "/docs/v26/v26-content-plan.js", encoding="utf-8").read().strip()
CSS = open(ROOT + "/docs/v26/v26-content-plan.css", encoding="utf-8").read().strip()
ICON = "M7 3v3M17 3v3M4 9h16M5.5 5h13A1.5 1.5 0 0 1 20 6.5v12a1.5 1.5 0 0 1-1.5 1.5h-13A1.5 1.5 0 0 1 4 18.5v-12A1.5 1.5 0 0 1 5.5 5ZM8 13h3M8 16.5h7"


def fail(m):
    sys.exit("HATA: " + m)


def once(s, old, new, done):
    if done in s:
        return s
    n = s.count(old)
    if n != 1:
        fail(f"{n} eşleşme: {old[:90]!r}")
    return s.replace(old, new)


def put(s, pattern, block, anchor):
    m = re.search(pattern, s, flags=re.S)
    if m:
        return s[:m.start()] + block + s[m.end():]
    if s.count(anchor) != 1:
        fail("bağlantı noktası tek değil: " + anchor[:60])
    return s.replace(anchor, block + anchor)


def main():
    if len(sys.argv) != 2:
        fail("kullanım: icerik_planlama_ekle.py <html>")
    p = sys.argv[1]
    s = open(p, encoding="utf-8").read()
    for t in (CORE, JS, CSS):
        if "</script" in t.lower() or "<!--" in t:
            fail("kaynakta </script ya da <!-- var")
    if 'id="sideAiBtn"' not in s:
        fail("önce docs/yapay-zeka/arayuz_ekle.py çalıştırılmalı")

    s = put(s, r"/\*V26-PLAN:BEGIN\*/.*?/\*V26-PLAN:END\*/\n", "/*V26-PLAN:BEGIN*/\n" + CORE + "\n/*V26-PLAN:END*/\n", "function mkRuleGroups(){")
    for a in ('<style id="v26-mobile">', '<script id="v26-mobile">'):
        if s.count(a) != 1:
            fail("tek olmalı: " + a)
    s = put(s, r'<style id="v26-content-plan">.*?</style>\n', '<style id="v26-content-plan">\n' + CSS + "\n</style>\n", '<style id="v26-mobile">')
    s = put(s, r'<script id="v26-content-plan">.*?</script>\n', '<script id="v26-content-plan">\n' + JS + "\n</script>\n", '<script id="v26-mobile">')

    s = once(s, 's.sub==="ai")?s.sub', 's.sub==="ai"||s.sub==="plan")?s.sub', 's.sub==="plan")?s.sub')
    s = once(s, 'ai:"",common:""}', 'ai:"",plan:"",common:""}', 'plan:"",common:""}')
    s = once(s, 'ai:"Yapay Zekâ",common:"Ortak Bilgiler"}', 'ai:"Yapay Zekâ",plan:"İçerik Planlama",common:"Ortak Bilgiler"}', 'plan:"İçerik Planlama",common:"Ortak Bilgiler"}')
    s = once(s, 'ca==="ai"?"Pazarlama › Yapay Zekâ":', 'ca==="ai"?"Pazarlama › Yapay Zekâ":ca==="plan"?"İçerik Planlama":', 'ca==="plan"?"İçerik Planlama":')
    s = once(s, 'AREA(s)==="ai"?" yapay zeka ai chatgpt gemini copilot perplexity":""',
             'AREA(s)==="ai"?" yapay zeka ai chatgpt gemini copilot perplexity":AREA(s)==="plan"?" içerik planlama icerik plani takvim donem dışa aktarım plan dosyası":""',
             'AREA(s)==="plan"?" içerik planlama')
    s = once(s, 'yz=yzRuleGroups(),rg=g=>', 'yz=yzRuleGroups(),ip=ipRuleGroups(),rg=g=>', 'ip=ipRuleGroups(),rg=g=>')
    s = once(s, """(yz.length?'<h2 class="areaHead">Yapay Zekâ</h2>'+yz.map(rg).join(""):"")""",
             """(yz.length?'<h2 class="areaHead">Yapay Zekâ</h2>'+yz.map(rg).join(""):"")+(ip.length?'<h2 class="areaHead">İçerik Planlama</h2>'+ip.map(rg).join(""):"")""",
             '<h2 class="areaHead">İçerik Planlama</h2>')
    s = once(s, '${yzPrompt(yz)}', '${yzPrompt(yz)}${ipPrompt(ip)}', '${ipPrompt(ip)}')
    s = once(s, 'G:YZ});\n return out}',
             'G:YZ});\n let IP=typeof ipRuleGroups==="function"?ipRuleGroups():[];if(IP.length)out.push({t:"İçerik planı ayarları",a:"İçerik ve reklam planının genel ayarlarını (seri no öneki, dönem bilgileri, dönem süzgeci, takvim notu, site bağlantıları) plan dosyasına ve içerik kayıtlarına uygulamak.",G:IP});\n return out}',
             't:"İçerik planı ayarları"')
    s = once(s, 'a==="ai"?"marketing"', 'a==="ai"||a==="plan"?"marketing"', 'a==="plan"?"marketing"')
    s = once(s, '/^(mk|gg|mt|yz)_/', '/^(mk|gg|mt|yz|ip)_/', '/^(mk|gg|mt|yz|ip)_/')
    s = once(s, 'areas:["marketing","google","meta","ai"],', 'areas:["marketing","google","meta","ai","plan"],', 'areas:["marketing","google","meta","ai","plan"],')
    s = once(s, 'yz=ap("ai"),', 'yz=ap("ai"),ip=ap("plan"),', 'ip=ap("plan"),')
    s = once(s, '"Ayarları planla","goArea(\'ai\')")}',
             '"Ayarları planla","goArea(\'ai\')")}${mod("İçerik Planlama",`${ip[0]} / ${ip[1]} karar verildi.`,"Planı aç","goArea(\'plan\')")}',
             '"Planı aç","goArea(\'plan\')")}')
    s = once(s, '["meta","Meta Servisleri"],["ai","Yapay Zekâ"]];\nfunction dlStat',
             '["meta","Meta Servisleri"],["ai","Yapay Zekâ"],["plan","İçerik Planlama"]];\nfunction dlStat', '["plan","İçerik Planlama"]];\nfunction dlStat')
    s = once(s, '["ai","Yapay Zekâ","goArea(\'ai\')"],', '["ai","Yapay Zekâ","goArea(\'ai\')"],["plan","İçerik Planlama","goArea(\'plan\')"],', '["plan","İçerik Planlama","goArea(\'plan\')"]')
    s = once(s, ' ai:"M12 3l1.8', ' plan:"' + ICON + '",\n ai:"M12 3l1.8', ' plan:"M7 3v3')

    open(p, "w", encoding="utf-8").write(s)
    print("tamam")


if __name__ == "__main__":
    main()
