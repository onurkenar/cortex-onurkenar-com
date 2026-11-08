#!/usr/bin/env python3
"""Kurumsal içerik kılavuzlarından türeyen pazarlama ve proje alanlarını DATA'ya işler.

Kullanım:
    python3 -I docs/pazarlama/kilavuz_ekle.py web-proje-gelistirme.html docs/pazarlama/kilavuz-alanlari.json

Kaynak: docs/pazarlama/kilavuz-alanlari.json (elle yazılır; kullanıcının Kılavuzlar/ klasöründeki 18 kılavuzdan
türetildi, kullanıcı kararları 2026-11-07: kapsam "hepsi", çelişkide "kılavuz geçerli").

Çalıştırma sırası: seo_denetimi_ekle.py → ortak_bilgiler_ekle.py → BU BETİK. Ortak Bilgiler betiği bütün bölümlerin
refs'ini silip yeniden yazdığı için o betik yeniden çalışırsa bu betiği de yeniden çalıştırın.

Kaynak anahtarları:
  - sections[]: {id, name, en, desc, group, icon, after, guide} — `after` bölümünden hemen sonra eklenir
    (kaynak sırasıyla işlenir; yeni bölümler birbirine başvurabilir). Alan pazarlama ("marketing").
  - fields[]: tam alan nesneleri; isteğe bağlı `after` (aynı bölümdeki alan kimliği) — yoksa bölümün sonuna.
  - optionAdd[]: {field, after?, options[]} — mevcut alana seçenek ekler.
  - optionSet[]: {field, value, set{}} — mevcut seçeneğin anahtarlarını değiştirir (value değişmez).
  - fieldSet[]: {field, set{}} — mevcut alanın anahtarlarını değiştirir (kimlik değişmez).
  - accountsAdd[]: {field, after?, rows[]} — accounts tipindeki alana satır ekler.
  - templateFormats: {kod: {olcu, sure, plat[], gerekce}} — DATA.marketingTemplate.formatlar (içerik planı
    şablonuna yazılan format tablosu) güncellenir / genişler.
  - guideAdd[]: {section, key: criteria|pitfalls, items[]} — mevcut bölüm rehberine madde ekler.
  - refsAdd: {bölüm id: [ortak alan id]} — bölümün "Ortak Bilgiler'den gelen veriler" kartına ekler.

Geri alınabilirlik: eklenen her öğe ve değiştirilen her anahtarın özgün değeri DATA.guideKit'te saklanır; betik her
çalıştırmada önce bunları geri alır, sonra kaynağı yeniden uygular (tekrar çalıştırılabilir, kaynak değişince
eski eklemeler temizlenir).

Denetimler: kimlik ve değer tekliği, zorunlu metinler (label, en, type, explanation, rule, scenario, example; seçenekte
label, explanation, scenario, example; boolean'da yes / no; metin alanında placeholder), rule yer tutucusunun tiple
uyumu, ajan kimliklerinin şemada olması, showIf / recommend / jump başvurularının ve değerlerinin geçerliliği,
pazarlama gruplarının ardışık olması, rehberde amaç + ≥ 3 ölçüt + ≥ 3 tuzak + ≥ 2 https kaynak, refs'in ortak
alan olması, metinlerde </script ve <!-- yokluğu.
"""
import copy
import hashlib
import json
import re
import sys

MARKER = "<script>const DATA="
TYPES = {"select", "multiselect", "boolean", "text", "textarea", "url", "color", "accounts"}
PH = {"select": "{label}", "multiselect": "{labels}", "boolean": "{booltext}", "text": "{value}",
      "textarea": "{value}", "url": "{value}", "color": "{value}", "accounts": "{value}"}
OPT_KEYS = ("label", "explanation", "scenario", "example")
KIT = "guideKit"


def fail(m):
    sys.exit("HATA: " + m)


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def positions(dept):
    o = dept.get("org") or {}
    P = {"lider"}
    if o.get("board"):
        P.add("kurul")
    if o.get("office"):
        P.add("ofis")
    for a in o.get("aides", []) or []:
        P.add("lider/" + a["id"])
    for m in o.get("matrix", []) or []:
        P.add("matris/" + m["id"])
    for u in o.get("units", []) or []:
        P.add(u["id"])
        for r in u.get("roles", []) or []:
            P.add(u["id"] + "/" + r["id"])
        for t in u.get("teams", []) or []:
            P.add(u["id"] + "/" + t["id"])
            for r in t.get("roles", []) or []:
                P.add(u["id"] + "/" + t["id"] + "/" + r["id"])
    return P


def revert(d):
    k = d.pop(KIT, None)
    if not k:
        return
    a = k["added"]
    d["sections"] = [x for x in d["sections"] if x["id"] not in set(a["sections"])]
    for sid in a["sections"]:
        d["sectionGuides"].pop(sid, None)
    d["fields"] = [f for f in d["fields"] if f["id"] not in set(a["fields"])]
    FI = {f["id"]: f for f in d["fields"]}
    SI = {x["id"]: x for x in d["sections"]}
    for fid, vals in a["options"].items():
        if fid in FI:
            FI[fid]["options"] = [o for o in FI[fid].get("options", []) if o["value"] not in set(vals)]
    for fid, ks in a["accounts"].items():
        if fid in FI:
            FI[fid]["accounts"] = [r for r in FI[fid].get("accounts", []) if r["k"] not in set(ks)]
    for sid, ids in a["refs"].items():
        if sid in SI and SI[sid].get("refs"):
            SI[sid]["refs"] = [x for x in SI[sid]["refs"] if x not in set(ids)]
            if not SI[sid]["refs"]:
                SI[sid].pop("refs")
    for sid, kv in a["guide"].items():
        g = d["sectionGuides"].get(sid)
        if g:
            for key, items in kv.items():
                g[key] = [x for x in g.get(key, []) if x not in set(items)]
    fm = d["marketingTemplate"].setdefault("formatlar", {})
    for code in a["formats"]:
        fm.pop(code, None)
    # özgün değerler (ters sırayla)
    for path, had, val in reversed(k["orig"]):
        kind = path[0]
        if kind == "field":
            o = FI.get(path[1])
        elif kind == "option":
            f = FI.get(path[1])
            o = next((x for x in (f or {}).get("options", []) if x["value"] == path[2]), None)
        elif kind == "format":
            o = fm
        else:
            o = None
        if o is None:
            continue
        key = path[-1]
        if had:
            o[key] = val
        else:
            o.pop(key, None)


def main():
    if len(sys.argv) != 3:
        fail("kullanım: kilavuz_ekle.py <html> <kilavuz-alanlari.json>")
    hp, sp = sys.argv[1:]
    src = json.load(open(sp, encoding="utf-8"))
    s = open(hp, encoding="utf-8").read()
    if s.count(MARKER) != 1:
        fail("DATA satırı yok")
    i = s.index(MARKER) + len(MARKER)
    d, end = json.JSONDecoder().raw_decode(s, i)
    for t in strings(src):
        if "</script" in t.lower() or "<!--" in t:
            fail("metinde </script ya da <!--: " + t[:60])

    revert(d)
    kit = {"version": src["version"], "added": {"sections": [], "fields": [], "options": {}, "accounts": {},
                                               "refs": {}, "guide": {}, "formats": []}, "orig": []}
    A, ORIG = kit["added"], kit["orig"]
    depts = {x["id"]: positions(x) for x in d["departments"] if x.get("org")}

    def agent_ok(a):
        m = re.fullmatch(r"poz:([^:]+):(.+)", a)
        return bool(m) and m.group(1) in depts and m.group(2) in depts[m.group(1)]

    def check_opt(fid, o):
        if not re.fullmatch(r"[A-Za-z0-9_+.\- ]+", str(o.get("value", ""))):
            fail(f"{fid}: seçenek değeri hatalı {o.get('value')!r}")
        for k in OPT_KEYS:
            if not str(o.get(k, "")).strip():
                fail(f"{fid}.{o.get('value')}: {k} boş")

    def check_field(f):
        fid = f["id"]
        if not re.fullmatch(r"[a-z][a-z0-9_]*", fid):
            fail(f"alan kimliği hatalı {fid}")
        if f.get("type") not in TYPES:
            fail(f"{fid}: tip hatalı {f.get('type')}")
        for k in ("label", "en", "explanation", "rule", "scenario", "example"):
            if not str(f.get(k, "")).strip():
                fail(f"{fid}: {k} boş")
        if PH[f["type"]] not in f["rule"] and not (f["type"] == "multiselect" and "{label}" in f["rule"]):
            fail(f"{fid}: rule {PH[f['type']]} içermiyor")
        if f["type"] in ("select", "multiselect"):
            ops = f.get("options") or []
            if len(ops) < 2:
                fail(f"{fid}: en az 2 seçenek")
            vals = [o["value"] for o in ops]
            if len(set(vals)) != len(vals):
                fail(f"{fid}: seçenek değeri tekrarı")
            for o in ops:
                check_opt(fid, o)
        elif f["type"] == "boolean":
            for k in ("yes", "no"):
                if not (f.get(k) or {}).get("scenario") or not (f.get(k) or {}).get("example"):
                    fail(f"{fid}: {k} eksik")
        elif f["type"] in ("text", "textarea", "url") and not str(f.get("placeholder", "")).strip():
            fail(f"{fid}: placeholder boş")
        elif f["type"] == "accounts" and not f.get("accounts"):
            fail(f"{fid}: accounts satırı yok")
        if not f.get("agents"):
            fail(f"{fid}: ajan yok")
        for a in f["agents"]:
            if not agent_ok(a):
                fail(f"{fid}: ajan şemada yok {a}")

    # 1. bölümler
    secs = d["sections"]
    squeue, sorder = list(src.get("sections", [])), []
    sids = {x["id"] for x in squeue}
    while squeue:
        rest = [x for x in squeue if x.get("after") in sids and x["after"] not in {y["id"] for y in sorder}]
        ready = [x for x in squeue if x not in rest]
        if not ready:
            fail("sections: after başvuruları döngüsel " + ", ".join(x["id"] for x in rest))
        sorder += ready
        squeue = rest
    for sec in sorder:
        sid = sec["id"]
        if any(x["id"] == sid for x in secs):
            fail(f"bölüm kimliği zaten var {sid}")
        for k in ("name", "en", "desc", "group", "icon", "after"):
            if not str(sec.get(k, "")).strip():
                fail(f"{sid}: {k} boş")
        g = sec.get("guide") or {}
        if not g.get("purpose") or len(g.get("criteria", [])) < 3 or len(g.get("pitfalls", [])) < 3 \
                or len(g.get("resources", [])) < 2:
            fail(f"{sid}: rehber eksik")
        for r in g["resources"]:
            if not str(r.get("url", "")).startswith("https://") or not r.get("title") or not r.get("note"):
                fail(f"{sid}: kaynak hatalı {r}")
        pos = next((k for k, x in enumerate(secs) if x["id"] == sec["after"]), None)
        if pos is None:
            fail(f"{sid}: after bölümü yok {sec['after']}")
        secs.insert(pos + 1, {"id": sid, "code": "", "name": sec["name"], "desc": sec["desc"], "en": sec["en"],
                              "group": sec["group"], "area": "marketing", "icon": sec["icon"]})
        d["sectionGuides"][sid] = {k: g[k] for k in ("purpose", "criteria", "pitfalls", "resources")}
        A["sections"].append(sid)
    SI = {x["id"]: x for x in secs}

    # 2. yeni alanlar
    FI = {f["id"]: f for f in d["fields"]}
    # `after` henüz eklenmemiş bir alana başvuruyorsa o alan sonraya ertelenir (kaynak sırası korunur)
    queue, order = list(src.get("fields", [])), []
    srcids = {x["id"] for x in queue}
    while queue:
        rest = [x for x in queue if x.get("after") in srcids and x["after"] not in {y["id"] for y in order}]
        ready = [x for x in queue if x not in rest]
        if not ready:
            fail("fields: after başvuruları döngüsel " + ", ".join(x["id"] for x in rest))
        order += ready
        queue = rest
    for spec in order:
        f = copy.deepcopy(spec)
        after = f.pop("after", None)
        if f["id"] in FI:
            fail(f"alan kimliği zaten var {f['id']}")
        if f.get("section") not in SI:
            fail(f"{f['id']}: bölüm yok {f.get('section')}")
        check_field(f)
        L = d["fields"]
        if after:
            if after not in FI or FI[after]["section"] != f["section"]:
                fail(f"{f['id']}: after alanı bu bölümde değil {after}")
            pos = next(k for k, x in enumerate(L) if x["id"] == after)
        else:
            idx = [k for k, x in enumerate(L) if x["section"] == f["section"]]
            if idx:
                pos = idx[-1]
            else:  # boş (yeni) bölüm: sıradaki önceki bölümün son alanından sonra
                order = [x["id"] for x in secs]
                prev = order[:order.index(f["section"])]
                pos = max((k for k, x in enumerate(L) if x["section"] in prev), default=len(L) - 1)
        L.insert(pos + 1, f)
        FI[f["id"]] = f
        A["fields"].append(f["id"])
    newf = set(A["fields"])

    # 3. seçenek ekleme
    for spec in src.get("optionAdd", []):
        fid = spec["field"]
        f = FI.get(fid)
        if not f or f["type"] not in ("select", "multiselect"):
            fail(f"optionAdd: alan yok ya da seçenekli değil {fid}")
        ops = f.setdefault("options", [])
        pos = len(ops)
        if spec.get("after"):
            pos = next((k + 1 for k, o in enumerate(ops) if o["value"] == spec["after"]), None)
            if pos is None:
                fail(f"optionAdd {fid}: after değeri yok {spec['after']}")
        for o in spec["options"]:
            check_opt(fid, o)
            if any(x["value"] == o["value"] for x in ops):
                fail(f"optionAdd {fid}: değer zaten var {o['value']}")
            ops.insert(pos, copy.deepcopy(o))
            pos += 1
            if fid not in newf:
                A["options"].setdefault(fid, []).append(o["value"])

    def remember(path, obj, key):
        ORIG.append([path, key in obj, copy.deepcopy(obj.get(key))])

    # 4. seçenek ve alan değişiklikleri
    for spec in src.get("optionSet", []):
        fid, val = spec["field"], spec["value"]
        f = FI.get(fid)
        o = next((x for x in (f or {}).get("options", []) if x["value"] == val), None)
        if o is None:
            fail(f"optionSet: seçenek yok {fid}.{val}")
        if "value" in spec["set"]:
            fail(f"optionSet {fid}.{val}: value değiştirilemez")
        fresh = fid in newf or val in A["options"].get(fid, [])
        for k, v in spec["set"].items():
            if not fresh:
                remember(["option", fid, val, k], o, k)
            o[k] = v
        check_opt(fid, o)
    for spec in src.get("fieldSet", []):
        fid = spec["field"]
        f = FI.get(fid)
        if not f:
            fail(f"fieldSet: alan yok {fid}")
        for k, v in spec["set"].items():
            if k in ("id", "section", "options", "accounts"):
                fail(f"fieldSet {fid}: {k} değiştirilemez")
            if k == "type" and not (f["type"] == "text" and v == "textarea"):
                fail(f"fieldSet {fid}: yalnız text → textarea")
            if fid not in newf:
                remember(["field", fid, k], f, k)
            f[k] = v

    # 5. accounts satırları
    for spec in src.get("accountsAdd", []):
        fid = spec["field"]
        f = FI.get(fid)
        if not f or f["type"] != "accounts":
            fail(f"accountsAdd: accounts alanı değil {fid}")
        rows = f.setdefault("accounts", [])
        pos = len(rows)
        if spec.get("after"):
            pos = next((k + 1 for k, r in enumerate(rows) if r["k"] == spec["after"]), None)
            if pos is None:
                fail(f"accountsAdd {fid}: after yok {spec['after']}")
        for r in spec["rows"]:
            if not r.get("k") or not r.get("label") or not r.get("ph") or any(x["k"] == r["k"] for x in rows):
                fail(f"accountsAdd {fid}: satır hatalı {r}")
            rows.insert(pos, copy.deepcopy(r))
            pos += 1
            if fid not in newf:
                A["accounts"].setdefault(fid, []).append(r["k"])

    # 6. içerik planı format tablosu
    fm = d["marketingTemplate"].setdefault("formatlar", {})
    for code, v in (src.get("templateFormats") or {}).items():
        if not re.fullmatch(r"[A-Z]{1,2}", code):
            fail(f"templateFormats: kod hatalı {code}")
        for k in ("olcu", "sure", "gerekce"):
            if not str(v.get(k, "")).strip():
                fail(f"templateFormats {code}: {k} boş")
        if not v.get("plat"):
            fail(f"templateFormats {code}: plat boş")
        if code in fm:
            remember(["format", code], fm, code)
        else:
            A["formats"].append(code)
        fm[code] = {k: v[k] for k in ("olcu", "sure", "plat", "gerekce")}
    codes = {o["value"] for o in FI["mk_formats"]["options"]}
    for code in A["formats"]:
        if code not in codes:
            fail(f"templateFormats: {code} mk_formats seçeneklerinde yok")

    # 7. rehber eklemeleri
    for spec in src.get("guideAdd", []):
        sid, key = spec["section"], spec["key"]
        g = d["sectionGuides"].get(sid)
        if g is None or key not in ("criteria", "pitfalls") or sid in A["sections"]:
            fail(f"guideAdd: rehber yok ya da yeni bölüm {sid}.{key}")
        for it in spec["items"]:
            if it not in g[key]:
                g[key].append(it)
                A["guide"].setdefault(sid, {}).setdefault(key, []).append(it)

    # 8. refs
    for sid, L in (src.get("refsAdd") or {}).items():
        if sid not in SI or SI[sid].get("area") == "common":
            fail(f"refsAdd: bölüm yok ya da ortak bölüm {sid}")
        for fid in L:
            if fid not in FI or SI[FI[fid]["section"]].get("area") != "common":
                fail(f"refsAdd: {sid} → {fid} ortak alan değil")
            r = SI[sid].setdefault("refs", [])
            if fid not in r:
                r.append(fid)
                A["refs"].setdefault(sid, []).append(fid)

    # 9. kodlar ve gruplar
    for k, x in enumerate(secs):
        x["code"] = f"{k:02d}"
    seen, prev = set(), None
    for x in secs:
        if x.get("area") != "marketing" or x.get("sub"):
            continue
        g = x.get("group")
        if g != prev and g in seen:
            fail(f"pazarlama grubu ardışık değil: {g} ({x['id']})")
        seen.add(g)
        prev = g

    # 10. başvuru denetimi (bütün alanlar)
    def vals(f):
        return {True, False} if f["type"] == "boolean" else {o["value"] for o in f.get("options", [])}
    for f in d["fields"]:
        for c in f.get("showIf", []) or []:
            if c["field"] not in FI:
                fail(f"{f['id']}: showIf alanı yok {c['field']}")
            if not set(c["in"]) <= vals(FI[c["field"]]):
                fail(f"{f['id']}: showIf değeri hatalı {c}")
        recs = f.get("recommend")
        for m in ([recs] if isinstance(recs, dict) else (recs or [])):
            if m["field"] not in FI:
                fail(f"{f['id']}: recommend alanı yok {m['field']}")
            for k, v in m["map"].items():
                kv = True if k == "true" else False if k == "false" else k
                if kv not in vals(FI[m["field"]]) and k not in vals(FI[m["field"]]):
                    fail(f"{f['id']}: recommend kaynak değeri hatalı {m['field']} {k}")
                if not set(v) <= vals(f):
                    fail(f"{f['id']}: recommend hedef değeri hatalı {v}")
        if f.get("jump") and f["jump"]["field"] not in FI:
            fail(f"{f['id']}: jump hedefi yok")
        for r in f.get("accounts", []) or []:
            for c in r.get("when", []) or []:
                if c["field"] not in FI:
                    fail(f"{f['id']}.{r['k']}: when alanı yok {c['field']}")
    ids = [f["id"] for f in d["fields"]]
    if len(set(ids)) != len(ids):
        fail("alan kimliği tekrarı")

    d[KIT] = kit
    out = s[:i] + json.dumps(d, ensure_ascii=False) + s[end:]
    if out.count("</script") != s.count("</script"):
        fail("</script sayısı değişti")
    open(hp, "w", encoding="utf-8").write(out)
    ms = [x for x in secs if x.get("area") == "marketing" and not x.get("sub")]
    print(f"{len(A['sections'])} yeni bölüm, {len(A['fields'])} yeni alan, "
          f"{sum(len(v) for v in A['options'].values())} yeni seçenek, {len(ORIG)} değişen anahtar, "
          f"{sum(len(v) for v in A['accounts'].values())} hesap satırı, {len(A['formats'])} yeni format, "
          f"{sum(len(v) for v in A['refs'].values())} bağlantı; pazarlama {len(ms)} bölüm "
          f"({ms[0]['code']}–{ms[-1]['code']})")
    print("md5", hashlib.md5(out.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
