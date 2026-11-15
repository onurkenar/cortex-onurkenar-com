#!/usr/bin/env python3
"""Referanslar, sertifikalar ve başarı metriklerini ayrı kararlara böler (2026-11-15).

Kullanım: python3 -I docs/ortak-bilgiler/kanit_ayir_ekle.py web-proje-gelistirme.html \\
              docs/ortak-bilgiler/ortak-bilgiler.json docs/pazarlama/kilavuz-alanlari.json

  - oc_proof ("Referanslar, Sertifikalar ve Başarı Metrikleri") → "Referanslar" (kimlik aynı; kayıtlar, refs ve sorumlu ajan
    değişikliği korunur); hemen arkasına oc_certs "Sertifikalar ve Belgeler" ve oc_metrics "Başarı Metrikleri" (Ortak Bilgiler ›
    İşletme & Pazar). Tanımlar aşağıdaki FIELDS'tadır ve aynı biçimde hem ortak-bilgiler.json'a ({"id","new"}) hem DATA'ya yazılır
    (ortak_bilgiler_ekle.py 2026-11-09'dan beri önceden var olan bir denetimde durduğu için — calisma_saatleri_ekle.py ile aynı yol).
  - oc_proof'u kullanan bölümlerin refs listelerine (DATA sections, DATA.guideKit.added.refs ve kilavuz-alanlari.json › refsAdd)
    oc_certs ve oc_metrics oc_proof'un hemen arkasına eklenir — kilavuz_ekle.py yeniden çalışırsa aynı listeyi yazar.
  - docs/v26/v26-proof.js → ana betikte /*V26-PROOF:BEGIN*/…END*/ (function one(f){ öncesi); kancalar: ocMig sonunda ocProofMig,
    pazarlama promptunun MARKA listesinde oc_certs, oc_metrics.
Tekrar çalıştırılabilir (tanımlar yerinde yenilenir, listelere tekrar eklenmez). Kaynak adresi yoktur; yalnız metin.
"""
import json
import os
import re
import sys

H, OJ, KJ = sys.argv[1:4]
D = os.path.dirname(os.path.abspath(__file__))
V26 = os.path.join(os.path.dirname(D), "v26")
MARKER = "<script>const DATA="

FIELDS = [
 ("oc_proof", {
  "label": "Referanslar", "en": "References", "type": "textarea",
  "placeholder": "Örn. Örnek AŞ | logo ve ad kullanılabilir | yazılı izin, 2026-03\nÖrnek Hastanesi | yalnız anonim (\"özel bir hastane grubu\") | izin yok",
  "explanation": "İçeriklerde, sunumlarda ve tekliflerde gösterilebilecek müşteri, proje ve iş ortağı referanslarıdır. Her satıra “Müşteri ya da proje | kullanım izni (ad, logo, yorum, vaka çalışması) | izin kaynağı ve tarihi” yazın. Sertifikalar ve başarı metrikleri bu bölümdeki ayrı kararlardadır.",
  "rule": "Kullanılabilir referanslar: {value}. Müşteri adı, logosu, yorumu ya da vaka çalışması yalnız bu listede izni yazılı olan kapsamda kullanılır; izni olmayan referans sektör adıyla anonim anılır ya da hiç kullanılmaz; listede olmayan referans uydurulmaz, “Referanslar” bölümü yer tutucuyla bırakılır.",
  "scenario": "Ana sayfa, hizmet sayfası, föy, sunum ya da teklifte müşteri logosu, referans listesi veya vaka çalışması gösterilecekse doldurulur.",
  "example": "Ana sayfadaki “Bize güvenenler” şeridinde yalnız yazılı logo izni olan dört müşteri görünür; izinsiz bir hastane “özel bir hastane grubu” olarak anılır.",
  "agents": ["poz:pazarlama:product_solution_marketing/musteri-pazarlamasi-yoneticisi/musteri-referans-programlari-uzmani",
             "poz:satis:08.06/satis-icerigi-ve-araclari/teklif-ve-vaka-kutuphanesi-uzmani",
             "poz:pazarlama:content_marketing/icerik-uretimi-muduru/vaka-calismasi-uzmani"]}),
 ("oc_certs", {
  "label": "Sertifikalar ve Belgeler", "en": "Certificates & Accreditations", "type": "textarea",
  "placeholder": "Örn. ISO 9001:2015 | Örnek Belgelendirme (TÜRKAK akrediteli), belge no 12345 | 2027-05-14\nTSE Hizmet Yeterlilik Belgesi | TSE, belge no … | 2026-12-01",
  "explanation": "Kurumun sahip olduğu yönetim sistemi sertifikaları, akreditasyonlar, lisanslar, mesleki üyelikler ve ödüllerdir. Her satıra “Belge adı | veren kuruluş ve belge numarası | geçerlilik bitiş tarihi” yazın.",
  "rule": "Gösterilebilecek sertifika ve belgeler: {value}. Yalnız geçerlilik tarihi geçmemiş belgeler kapsamıyla birlikte gösterilir; tarihi geçen belge siteden ve dokümanlardan kaldırılır, liste yılda bir kontrol edilir. Belge logoları belgelendirme kuruluşunun kullanım kurallarına göre kullanılır (ISO'nun kendi logosu sertifika göstermek için kullanılmaz); mümkünse belge numarası ya da doğrulama bağlantısı verilir; listede olmayan belge yazılmaz.",
  "scenario": "Kalite, bilgi güvenliği, çevre, sektör lisansı ya da akreditasyon belgesi olan ve bunu sitede, teklifte veya föyde gösterecek kurumlar.",
  "example": "Hakkımızda sayfasında ISO 9001 ve ISO 27001 belgeleri belge numarası, belgelendirme kuruluşu ve bitiş tarihiyle listelenir; süresi dolan belge yıllık kontrolde kaldırılır.",
  "agents": ["poz:kalite:14.07/dis-denetim-ve-sertifikasyon-koordinasyonu/sertifika-yonetimi-uzmani",
             "poz:kalite:14.02/standartlar-ve-sertifikasyon/sertifikasyon-uzmani"]}),
 ("oc_metrics", {
  "label": "Başarı Metrikleri", "en": "Success Metrics", "type": "textarea",
  "placeholder": "Örn. %98 müşteri memnuniyeti | 2026 yıllık müşteri anketi, 412 yanıt | 2026-01\n1.200+ tamamlanan proje | proje kayıtları | 2026-10",
  "explanation": "İçeriklerde kullanılabilecek sayısal başarı göstergeleridir (müşteri sayısı, memnuniyet oranı, tamamlanan proje, deneyim yılı …). Her satıra “Metrik ve değeri | kaynağı (anket, kayıt, rapor) | ölçüm tarihi ya da dönemi” yazın.",
  "rule": "Kullanılabilir başarı metrikleri: {value}. Metrikler yalnız bu listedeki değer, kaynak ve dönemle kullanılır; yuvarlanacaksa aşağı yuvarlanır; kaynağı ya da dönemi bilinmeyen metrik ve “en iyi”, “lider”, “1 numara” gibi kanıtlanamayan üstünlük iddiası yazılmaz (ticari reklam mevzuatı reklamdaki iddiaların kanıtlanabilir olmasını ister); bir yıldan eski metrik güncellenene kadar dönemiyle birlikte gösterilir.",
  "scenario": "Ana sayfa, hizmet sayfası, sunum ya da teklifte rakamla güven oluşturulacaksa doldurulur.",
  "example": "Ana sayfadaki sayaç “1.200+ tamamlanan proje (Ekim 2026)” gösterir; kaynağı olmayan “sektör lideri” ifadesi kullanılmaz.",
  "agents": ["poz:veri-analitik:17.05/musteri-pazarlama-ve-gelir-analitigi/pazarlama-analitigi-uzmani",
             "poz:pazarlama:content_marketing/icerik-uretimi-muduru/vaka-calismasi-uzmani"]}),
]
NEW = ["oc_certs", "oc_metrics"]


def fail(m):
    sys.exit("HATA: " + m)


def add_after(lst, anchor):
    if anchor not in lst:
        return lst
    out = [x for x in lst if x not in NEW]
    i = out.index(anchor)
    return out[:i + 1] + NEW + out[i + 1:]


# --- ortak-bilgiler.json
O = json.load(open(OJ, encoding="utf-8"))
sec = next((s for s in O["sections"] if any(f.get("id") == "oc_proof" for f in s["fields"])), None) or fail("oc_proof JSON'da yok")
fl = [f for f in sec["fields"] if f.get("id") not in NEW]
i = next(k for k, f in enumerate(fl) if f.get("id") == "oc_proof")
fl[i] = {"id": "oc_proof", "new": dict(FIELDS[0][1])}
fl[i + 1:i + 1] = [{"id": fid, "new": dict(d)} for fid, d in FIELDS[1:]]
sec["fields"] = fl
json.dump(O, open(OJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(OJ, "a", encoding="utf-8").write("\n")

# --- kilavuz-alanlari.json › refsAdd
K = json.load(open(KJ, encoding="utf-8"))
for k, v in K["refsAdd"].items():
    K["refsAdd"][k] = add_after(v, "oc_proof")
json.dump(K, open(KJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)  # dosyanın sonunda satır sonu yok

# --- DATA
s = open(H, encoding="utf-8").read()
a = s.index(MARKER) + len(MARKER)
Dt, e = json.JSONDecoder().raw_decode(s, a)
F = Dt["fields"]
ids = {f["id"] for f in F}
pos = {}
for d in Dt["departments"]:
    pos[d["id"]] = d
for fid, d in FIELDS:
    for ag in d["agents"]:
        m = re.match(r"^poz:([^:]+):(.+)$", ag)
        if not m or m.group(1) not in pos:
            fail("ajan " + ag)
reg = json.load(open(os.path.join(os.path.dirname(D), "ajan-kaydi", "AGENT_REGISTRY.json"), encoding="utf-8"))
known = {x for d in reg["definitions"] for x in (d.get("implementations") or [])}
for fid, d in FIELDS:
    for ag in d["agents"]:
        if ag not in known:
            fail("ajan kayıtta yok: " + ag)
old = next(f for f in F if f["id"] == "oc_proof")
F[:] = [f for f in F if f["id"] not in NEW]
i = next(k for k, f in enumerate(F) if f["id"] == "oc_proof")
def mk(fid, d):
    x = {"id": fid, "section": old["section"]}
    x.update(d)
    return x
F[i] = mk(*FIELDS[0])
F[i + 1:i + 1] = [mk(fid, d) for fid, d in FIELDS[1:]]
for sc in Dt["sections"]:
    if sc.get("refs"):
        sc["refs"] = add_after(sc["refs"], "oc_proof")
gr = Dt.get("guideKit", {}).get("added", {}).get("refs", {})
for k, v in gr.items():
    gr[k] = add_after(v, "oc_proof")
for t in [json.dumps(x, ensure_ascii=False) for x in FIELDS]:
    if "</script" in t or "<!--" in t:
        fail("yasak metin")
s = s[:a] + json.dumps(Dt, ensure_ascii=False) + s[e:]

# --- JS bloğu ve kancalar
js = open(os.path.join(V26, "v26-proof.js"), encoding="utf-8").read().strip()
if "</script" in js or "<!--" in js:
    fail("js")
B, E_ = "/*V26-PROOF:BEGIN*/", "/*V26-PROOF:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    t = "\nfunction one(f){if(f.derive"
    if s.count(t) != 1:
        fail("one")
    s = s.replace(t, "\n" + blk + t[1:])


def once(o, n):
    global s
    if n in s:
        return
    if s.count(o) != 1:
        fail(f"{o[:60]!r} {s.count(o)} kez")
    s = s.replace(o, n)


once('ocTaxMig(st);ocGeoMig(st)}', 'ocTaxMig(st);ocGeoMig(st);if(typeof ocProofMig==="function")ocProofMig(st)}')
once('"oc_services","oc_proof","oc_keywords"', '"oc_services","oc_proof","oc_certs","oc_metrics","oc_keywords"')
open(H, "w", encoding="utf-8").write(s)
print("tamam:", ", ".join(f["id"] for f in F[i:i + 3]))
