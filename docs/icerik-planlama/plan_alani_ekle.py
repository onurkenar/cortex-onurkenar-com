# -*- coding: utf-8 -*-
"""8. İçerik Planlama menü alanının verisi (2026-11-15).
Kullanım: python3 -I docs/icerik-planlama/plan_alani_ekle.py <html> docs/icerik-planlama/kaynak.json
- Bölümler: ip_plan (yeni, "Plan & Dönem"), ip_products (yeni, "Ürün ve Hizmetler", 2026-11-15) ve mk_planfile (Pazarlama › Plan Dosyası'ndan taşınır, "Dışa Aktarım";
  kimlik aynı kalır çünkü dışa aktarım kartı s.id==="mk_planfile" ile çizilir). İkisi de area:"marketing", sub:"plan",
  group = kaynak.group; yz_report'tan (kaynak.after) hemen sonra, bu sırayla. Bölüm kodları (code) sırayla yeniden verilir.
- Alanlar: moveFields'teki alanların bölümü değişir (kimlik ve kayıtlı değerler aynı); fields[] yeni alanları `after`'dan
  sonra ekler (varsa yerinde günceller).
- Rehberler: ip_plan rehberi yazılır; özgün mk_planfile rehberinin kaynaklarından JSON dışındakiler ip_plan'a,
  JSON kaynağı mk_planfile'da kalır (keepResources).
Özgün değerler ilk çalıştırmada DATA.planKit.orig'e yazılır. Hedef değerleri doğrudan yazar; tekrar çalıştırılabilir.
Diğer veri betiklerinden (kilavuz_ekle.py, Ortak Bilgiler, Google, Meta, Yapay Zekâ) SONRA, docs/v26/tutarlilik_ekle.py'den
ÖNCE çalıştırılır."""
import copy, hashlib, json, sys

PH = {"select": "{label}", "multiselect": "{labels}", "boolean": "{booltext}", "text": "{value}", "textarea": "{value}", "records": "{value}"}
hp, sp = sys.argv[1:3]
h = open(hp, encoding="utf-8").read()
MARK = "const DATA="
if h.count(MARK) != 1:
    sys.exit("HATA: DATA satırı bulunamadı")
i = h.index(MARK) + len(MARK)
D, end = json.JSONDecoder().raw_decode(h, i)
src = json.load(open(sp, encoding="utf-8"))
S, L = D["sections"], D["fields"]
SI = {s["id"]: s for s in S}
FI = {f["id"]: f for f in L}
kit = D.setdefault("planKit", {})
kit["version"] = src["version"]
orig = kit.setdefault("orig", {})
ids = [x["id"] for x in src["sections"]]
if src["after"] not in SI:
    sys.exit("HATA: after bölümü yok " + src["after"])

# 1. bölümler
for spec in src["sections"]:
    sid = spec["id"]
    s = SI.get(sid)
    if s is None:
        s = {"id": sid, "code": ""}
        S.append(s)
        SI[sid] = s
        orig.setdefault("sections", {}).setdefault(sid, None)
    else:
        orig.setdefault("sections", {}).setdefault(sid, copy.deepcopy(s))
    for k in ("name", "en", "desc", "icon"):
        s[k] = spec[k]
    s["group"], s["area"], s["sub"] = src["group"], "marketing", "plan"
    if spec.get("refs"):
        for r in spec["refs"]:
            if r not in FI:
                sys.exit("HATA: refs alanı yok " + r)
        s["refs"] = list(spec["refs"])
    else:
        s.pop("refs", None)
# sıra: after'dan hemen sonra ids sırasıyla
rest = [s for s in S if s["id"] not in ids]
k = next(n for n, s in enumerate(rest) if s["id"] == src["after"]) + 1
S[:] = rest[:k] + [SI[x] for x in ids] + rest[k:]
for n, s in enumerate(S):
    s["code"] = "%02d" % n

# 2. alan taşıma
for fid, sid in src["moveFields"].items():
    f = FI.get(fid)
    if not f:
        sys.exit("HATA: alan yok " + fid)
    orig.setdefault("fieldSection", {}).setdefault(fid, f["section"])
    f["section"] = sid
# taşınan alanlar hedef bölümün başında, kaynak sırasıyla
mv = [FI[x] for x in src["moveFields"]]
for f in mv:
    L.remove(f)
first = next((n for n, f in enumerate(L) if f["section"] == ids[0]), None)
if first is None:
    first = len(L)
L[first:first] = mv

# 3. yeni alanlar — önceki çalıştırmanın eklediği kaynak alanları önce topluca çıkarılır (bir bölüme birden çok yeni alan
#    eklendiğinde tekrar çalıştırma ilk çalıştırmayla aynı sırayı versin), sonra sırayla yeniden yerleştirilir.
SRC_IDS = {x["id"] for x in src["fields"]}
L[:] = [x for x in L if x["id"] not in SRC_IDS]
for spec in src["fields"]:
    f = copy.deepcopy(spec)
    after = f.pop("after")
    for kk in ("label", "en", "type", "explanation", "rule", "scenario", "example", "agents"):
        if not f.get(kk):
            sys.exit("HATA: %s eksik %s" % (f["id"], kk))
    if PH[f["type"]] not in f["rule"]:
        sys.exit("HATA: %s rule yer tutucusu" % f["id"])
    for o in f.get("options") or []:
        for kk in ("label", "explanation", "scenario", "example"):
            if not o.get(kk):
                sys.exit("HATA: %s seçenek %s eksik" % (f["id"], kk))
    if f["id"] not in FI:
        kit.setdefault("added", [])
        if f["id"] not in kit["added"]:
            kit["added"].append(f["id"])
    if not after:  # bölümün ilk alanı: listenin sonuna (bölüm içi sıra yalnız bölümün alanları arasında önemlidir)
        if any(x["section"] == f["section"] for x in L):
            sys.exit("HATA: %s after boş ama bölümde başka alan var" % f["id"])
        L.append(f)
        FI[f["id"]] = f
        continue
    a = next((n for n, x in enumerate(L) if x["id"] == after), None)
    if a is None or L[a]["section"] != f["section"]:
        sys.exit("HATA: %s after alanı bölümde değil %s" % (f["id"], after))
    L.insert(a + 1, f)
    FI[f["id"]] = f

# 4. rehberler
G = D.setdefault("sectionGuides", {})
og = orig.setdefault("guides", {})
if "mk_planfile" not in og:
    og["mk_planfile"] = copy.deepcopy(G.get("mk_planfile"))
base = og["mk_planfile"] or {}
res = base.get("resources") or []
for sid, g in src["guides"].items():
    g = copy.deepcopy(g)
    keep = g.pop("keepResources", False)
    if sid == "mk_planfile":
        r = [x for x in res if "JSON" in x.get("title", "")] if keep else []
    else:
        r = [x for x in res if "JSON" not in x.get("title", "")]
    if r:
        g["resources"] = r
    G[sid] = g

# denetim: plan bölümleri ardışık ve alanları bölüm sırasında
pos = [n for n, s in enumerate(S) if s.get("sub") == "plan"]
if pos != list(range(pos[0], pos[0] + len(pos))):
    sys.exit("HATA: plan bölümleri ardışık değil")
for f in L:
    if f["section"] not in SI:
        sys.exit("HATA: bölümü olmayan alan " + f["id"])
    for c in f.get("showIf") or []:
        if c["field"] not in FI:
            sys.exit("HATA: showIf alanı yok %s → %s" % (f["id"], c["field"]))

out = json.dumps(D, ensure_ascii=False)
for bad in ("</script", "<!--"):
    if bad in out:
        sys.exit("HATA: DATA içinde yasak dizi " + bad)
h = h[:i] + out + h[end:]
open(hp, "w", encoding="utf-8").write(h)
print("tamam · plan bölümleri %s · md5 %s · boyut %d" % ([S[n]["code"] + " " + S[n]["id"] for n in pos], hashlib.md5(h.encode("utf-8")).hexdigest(), len(h.encode("utf-8"))))
