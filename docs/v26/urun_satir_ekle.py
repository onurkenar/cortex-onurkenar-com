"""Ürün / Hizmet Listesi satır düzenleyicisi (2026-11-15) — docs/v26/v26-svc.{js,css}.
Kullanım: python3 -I docs/v26/urun_satir_ekle.py <html> [docs/ortak-bilgiler/ortak-bilgiler.json]
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kanca ve metinler yalnız eksikse yazılır.
Kanca: one() — SVC_F'deki metin kararı (oc_services) textarea yerine satır düzenleyicisiyle (svcInput) çizilir. Değer metin olarak
kalır ("Ad | /sayfa-adresi/" satırları), bu yüzden isset / ruleBase / ocVal / dışa aktarım ve v26-products.js items() kancası
gerekmez. Alanın açıklaması ve örneği (EXPL / EXAMPLE) hem DATA'ya hem ortak-bilgiler.json'a ({"id","new"}) yazılır."""
import json, os, re, sys
H = sys.argv[1]
OJ = sys.argv[2] if len(sys.argv) > 2 else None
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-svc.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-svc.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

OLD_EXPL = "Satılan ürün ve hizmetler; her satıra bir kalem “Ad | sayfa adresi” biçiminde (adres isteğe bağlı). Ana kalemleri yazın; varyantları ayrıca listelemeyin."
EXPL = "Satılan ürün ve hizmetler; her kalemi ayrı satıra girin: ürün / hizmet adı ve sayfa adresi (isteğe bağlı; “/implant-tedavisi/” gibi yol ya da tam adres); yeni kalem için “Kalem ekle”. Ana kalemleri yazın; varyantları ayrıca listelemeyin."
OLD_EX = "“İmplant tedavisi | /implant-tedavisi/” satırı hizmet sayfasının, Service yapısal verisinin ve “İmplant” Google Ads kampanyasının adı olur."
EXAMPLE = "Adı “İmplant tedavisi”, sayfa adresi “/implant-tedavisi/” olan kalem hizmet sayfasının, Service yapısal verisinin ve “İmplant” Google Ads kampanyasının adı olur."


def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)


B, E_ = "/*V26-SVC:BEGIN*/", "/*V26-SVC:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
st = '<style id="v26-svc">' + css + "</style>"
if '<style id="v26-svc">' in s:
    s = re.sub(r'<style id="v26-svc">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
once('else if(REF_F[f.id])c=refInput(f);', 'else if(SVC_F[f.id])c=svcInput(f);else if(REF_F[f.id])c=refInput(f);')
once(json.dumps(OLD_EXPL, ensure_ascii=False), json.dumps(EXPL, ensure_ascii=False))
once(json.dumps(OLD_EX, ensure_ascii=False), json.dumps(EXAMPLE, ensure_ascii=False))
open(H, "w", encoding="utf-8").write(s)

if OJ:
    raw = open(OJ, encoding="utf-8").read()
    n = 0
    for o, x in ((OLD_EXPL, EXPL), (OLD_EX, EXAMPLE)):
        jo, jx = json.dumps(o, ensure_ascii=False), json.dumps(x, ensure_ascii=False)
        if jx in raw:
            continue
        assert raw.count(jo) == 1, (raw.count(jo), o[:60])
        raw = raw.replace(jo, jx)
        n += 1
    json.loads(raw)
    open(OJ, "w", encoding="utf-8").write(raw)
    print("json:", n, "metin")
print("tamam", len(s))
