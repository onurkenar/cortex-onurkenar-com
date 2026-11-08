"""Hazır Prompt Kütüphanesi bloklarını uygulamaya ekler / günceller (2026-11-08).

Kullanım: python3 -I docs/v26/prompt_kutuphanesi_ekle.py <girdi.html> <çıktı.html>

- <style id="v26-prompt-library"> : docs/v26/v26-prompt-library.css (head'de v26-panel-portal stilinden sonra)
- <script id="v26-prompt-library">: docs/v26/v26-prompt-library.js, içindeki /*PL_DATA*/ yerine
  docs/v26/v26-prompt-library-data.js (body sonunda, son betik)
- Hazır modül metinleri docs/v26/prompt-kutuphanesi/: veride /*PL_FILE:ad*/"" yerine dosyanın JSON metni,
  /*PL_IMGS:klasör*/[] yerine klasördeki gorseller.json sırasıyla WebP görseller (alt metin ve açıklama dokümandan)
- Sayfa 25 MiB'ı (Cloudflare statik dosya sınırı) aşarsa durur
- Dokümantasyon sayfasına "Hazır Prompt Kütüphanesi" maddesi (Pazarlama maddesinden önce)
Bloklar zaten varsa içerikleri yenilenir (tekrar çalıştırılabilir). DATA satırına dokunmaz.
"""
import base64, json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
src, dst = sys.argv[1], sys.argv[2]
html = open(src, encoding="utf-8").read()
css = open(os.path.join(HERE, "v26-prompt-library.css"), encoding="utf-8").read().strip()
js = open(os.path.join(HERE, "v26-prompt-library.js"), encoding="utf-8").read()
data = open(os.path.join(HERE, "v26-prompt-library-data.js"), encoding="utf-8").read().strip()
assert js.count("/*PL_DATA*/") == 1
LIB = os.path.join(HERE, "prompt-kutuphanesi")


def pl_file(m):
    txt = open(os.path.join(LIB, m.group(1)), encoding="utf-8").read().strip()
    return json.dumps(txt, ensure_ascii=False)


def pl_imgs(m):
    d = os.path.join(LIB, m.group(1))
    man = json.load(open(os.path.join(d, "gorseller.json"), encoding="utf-8"))
    doc = open(os.path.join(LIB, man["dokuman"]), encoding="utf-8").read()
    out = []
    for i, name in enumerate(man["sira"]):
        ref = re.search(r"!\[([^\]]*)\]\([^)]*?/" + re.escape(name) + r"\.png\)", doc)
        assert ref, "dokümanda görsel yok: " + name
        heads = [h for h in re.finditer(r"^#{2,3}\s+(.+)$", doc[:ref.start()], re.M)]
        cap = heads[-1].group(1).strip() if heads else ""
        cap = ("§" + cap) if re.match(r"\d", cap) else cap
        raw = open(os.path.join(d, name + ".webp"), "rb").read()
        assert raw[:4] == b"RIFF" and raw[8:12] == b"WEBP", name
        out.append({"id": "img-%d" % (i + 1), "name": name, "src": "data:image/webp;base64," + base64.b64encode(raw).decode(),
                    "alt": ref.group(1).strip(), "caption": cap})
    return json.dumps(out, ensure_ascii=False)


data, n1 = re.subn(r'/\*PL_FILE:([\w.-]+)\*/""', pl_file, data)
data, n2 = re.subn(r"/\*PL_IMGS:([\w.-]+)\*/\[\]", pl_imgs, data)
assert n1 == 3 and n2 == 1, (n1, n2)
for need in ("17. Kabul Kriterleri", "Kaynak kullanım kuralları", "## 20. Tamamlanma ve Kabul Kriterleri", "### Nihai teslimat"):
    assert need in data, need
js = js.replace("/*PL_DATA*/", data).strip()
for name, body in (("css", css), ("js", js)):
    low = body.lower()
    assert "</script" not in low and "</style" not in low and "<!--" not in body, name

STYLE = '<style id="v26-prompt-library">' + css + "</style>"
SCRIPT = '<script id="v26-prompt-library">' + js + "</script>"
DOC = ('<div class="rulegroup" id="docPromptLib"><h3>Hazır Prompt Kütüphanesi</h3><p>Modül şeridindeki <b>Promptlar</b> '
       '(mobilde menünün altındaki <b>Hazır Prompt Kütüphanesi</b>) sık tekrarlanan geliştirme işlerini hazır modüller olarak saklar. '
       'Her modülde başlık, açıklama, kategori, etiketler, kısa prompt, Markdown teknik doküman, referans görseller, kabul kriterleri, '
       'bağımlılıklar ve sürüm bulunur. Başlangıçta iki hazır modül vardır: <b>KVKK / GDPR &amp; Çerez Yönetimi</b> ve <b>Erişilebilirlik (WCAG 2.2 AA)</b>; her biri tek prompt ve tek kabul listesiyle, bölümleri teknik dokümanın içinde. Güvenlik, Performans, SEO, Ödeme gibi '
       'kategorilere kendi modüllerinizi ekleyebilir, kendi kategorilerinizi oluşturabilirsiniz.</p><ul>'
       '<li><b>Arama ve filtre:</b> başlık, açıklama, etiket ve içerikte arar; kategori ve etiket çipleriyle süzer.</li>'
       '<li><b>Ekleme, düzenleme, kopyalama, silme:</b> her kayıtta sürüm yükselir ve önceki metin sürüm geçmişinde saklanır. '
       'Hazır modülleri düzenlemek ya da gizlemek geri alınabilir ("Hazır sürüme dön", "Geri getir").</li>'
       '<li><b>Birleştirilmiş talimat:</b> işaretlediğiniz modüller bağımlılıklarıyla birlikte doğru sırada tek bir geliştirme talimatında '
       'birleşir; kopyalayabilir, <code>GELISTIRME-TALIMATI.md</code> ya da dokümanlar ve görsellerle zip olarak indirebilirsiniz.</li>'
       '<li><b>İçe / dışa aktarma:</b> kütüphanenin tamamı, seçilenler ya da tek modül JSON olarak taşınır.</li>'
       '<li><b>Saklama:</b> kütüphane bu tarayıcıda saklanır ve bütün projelerde ortaktır; başka bir cihaza dışa aktararak taşıyın. '
       'Projede hangi modüllerin seçildiği proje dosyasına yazılır. Kütüphane Proje Kuralları\'nı ve Claude promptunu değiştirmez.</li></ul></div>')

# Stil
if '<style id="v26-prompt-library">' in html:
    html, n = re.subn(r'<style id="v26-prompt-library">.*?</style>', lambda m: STYLE, html, count=1, flags=re.S)
    assert n == 1
else:
    a = html.index('<style id="v26-panel-portal">')
    b = html.index("</style>", a) + len("</style>")
    assert html.count('<style id="v26-panel-portal">') == 1
    html = html[:b] + STYLE + html[b:]

# Betik
if '<script id="v26-prompt-library">' in html:
    a = html.index('<script id="v26-prompt-library">')
    b = html.index("</script>", a) + len("</script>")
    html = html[:a] + SCRIPT + html[b:]
else:
    tail = "</body></html>"
    assert html.rstrip().endswith(tail)
    i = html.rstrip().rfind(tail)
    html = html[:i] + SCRIPT + html[i:]

# Doküman
if 'id="docPromptLib"' in html:
    html, n = re.subn(r'<div class="rulegroup" id="docPromptLib">.*?</ul></div>', lambda m: DOC, html, count=1, flags=re.S)
    assert n == 1
else:
    anchor = '<div class="rulegroup"><h3>Pazarlama</h3>'
    assert html.count(anchor) == 1, html.count(anchor)
    html = html.replace(anchor, DOC + anchor)

for k in ('<style id="v26-prompt-library">', '<script id="v26-prompt-library">', 'id="docPromptLib"'):
    assert html.count(k) == 1, k
size = len(html.encode("utf-8"))
assert size < 25 * 1024 * 1024, "sayfa 25 MiB sınırını aşıyor: %d" % size
open(dst, "w", encoding="utf-8").write(html)
print("ok", len(html))
