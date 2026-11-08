#!/usr/bin/env python3
"""SEO Denetimi bölümlerini DATA'ya işler.

Kullanım:
    python3 -I docs/seo-denetimi/seo_denetimi_ekle.py web-proje-gelistirme.html docs/seo-denetimi/seo-denetimi.json

Kaynak: docs/seo-denetimi/seo-denetimi.json (elle yazılır; uygulamadaki veri bu betikle üretilir).
Pazarlama alanının sonuna "SEO Denetimi" kategorisinde bölümler ekler:
  - sections[]: {id, code, name, desc, en, group, area:"marketing", sub:"audit", icon}
    (sub:"audit" bölümleri Proje Kuralları'na, ana Claude promptuna, pazarlama promptuna,
    proje dosyasının kurallarına ve ajan dosyalarındaki "sorumlu olduğu proje kararları"na girmez;
    seçimler yalnız Denetim Raporu & Prompt bölümündeki denetim promptunda kullanılır)
  - fields[]: kaynakta yazıldığı gibi + section; ajan kısaltmaları (M, T …) pozisyon ajanı kimliğine çevrilir.
    Ek alan anahtarları: auList (kontrol listesi; promptta numaralı maddeler), seçenekte needs
    (gereken erişim anahtarları, DATA.seoAudit.access), boolean'da promptYes / promptNo.
  - sectionGuides[bölüm id] = guide
  - DATA.seoAudit = {version, access}
Bölüm kodları (00–NN) bütün bölümler için sıradan yeniden üretilir.

Denetimler: kimlik öneki ve tekliği, zorunlu metinler (açıklama, senaryo, örnek; boolean'da yes / no),
seçenek değerlerinin tekliği, showIf ve recommend başvuruları (alan ve değerler), needs anahtarları,
ajan kimliklerinin şemadaki pozisyonlara karşılığı, kaynak adreslerinin https olması, metinlerde
</script ve <!-- bulunmaması, Kiril harf bulunmaması. Herhangi biri tutmazsa betik durur, dosyaya yazmaz.
Tekrar çalıştırılabilir: önceki au_* bölüm, alan ve rehberleri silinip yeniden eklenir.
"""
import hashlib
import json
import re
import sys

PREFIX = "au_"
TYPES = {"select", "multiselect", "boolean", "text", "textarea", "url"}
MARKER = "<script>const DATA="


def fail(msg):
    sys.exit("HATA: " + msg)


def load_html(path):
    s = open(path, encoding="utf-8").read()
    if s.count(MARKER) != 1:
        fail("DATA satırı bulunamadı ya da birden çok")
    i = s.index(MARKER) + len(MARKER)
    d, end = json.JSONDecoder().raw_decode(s, i)
    return s, d, i, end


def positions(dept):
    """dpPos ile aynı kimlik kümesi (komite düğümleri hariç)."""
    o = dept.get("org") or {}
    P = set()
    if o.get("board"):
        P.add("kurul")
        for r in o["board"].get("roles", []):
            P.add("kurul/" + r["id"])
    if o.get("office"):
        P.add("ofis")
    P.add("lider")
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


def walk_strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from walk_strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from walk_strings(v)


def main():
    if len(sys.argv) != 3:
        fail("kullanım: seo_denetimi_ekle.py <html> <seo-denetimi.json>")
    html_path, src_path = sys.argv[1], sys.argv[2]
    src = json.load(open(src_path, encoding="utf-8"))
    s, d, i, end = load_html(html_path)

    for t in walk_strings(src):
        if "</script" in t.lower() or "<!--" in t:
            fail("metinde </script ya da <!-- var: " + t[:60])
        if re.search(r"[Ѐ-ӿ]", t):
            fail("metinde Kiril harf var: " + t[:80])

    group = src["group"]
    agents = src["agents"]
    access = src["access"]

    # mevcut au_* kayıtlarını çıkar
    d["sections"] = [x for x in d["sections"] if not x["id"].startswith(PREFIX)]
    d["fields"] = [x for x in d["fields"] if not x["id"].startswith(PREFIX)]
    for k in [k for k in d["sectionGuides"] if k.startswith(PREFIX)]:
        del d["sectionGuides"][k]

    depts = {x["id"]: positions(x) for x in d["departments"] if x.get("org")}

    def agent_id(code):
        if code not in agents:
            fail("tanımsız ajan kısaltması: " + code)
        aid = agents[code]
        m = re.fullmatch(r"poz:([^:]+):(.+)", aid)
        if not m or m.group(1) not in depts or m.group(2) not in depts[m.group(1)]:
            fail("ajan kimliği şemada yok: " + aid)
        return aid

    existing = {f["id"]: f for f in d["fields"]}
    new_sections, new_fields = [], []
    ids = set()
    for sec in src["sections"]:
        sid = sec["id"]
        if not sid.startswith(PREFIX) or sid in ids:
            fail("bölüm kimliği hatalı ya da tekrar: " + sid)
        ids.add(sid)
        for k in ("name", "en", "desc", "icon"):
            if not str(sec.get(k, "")).strip():
                fail(f"{sid}: {k} boş")
        g = sec["guide"]
        if not g.get("purpose") or len(g.get("criteria", [])) < 3 or len(g.get("pitfalls", [])) < 3 or not g.get("resources"):
            fail(f"{sid}: rehber eksik")
        for r in g["resources"]:
            if not r.get("title") or not r.get("note") or not str(r.get("url", "")).startswith("https://"):
                fail(f"{sid}: kaynak hatalı: {r}")
        sec_agents = [agent_id(c) for c in sec.get("agents", [])]
        if not sec_agents:
            fail(f"{sid}: varsayılan ajan yok")
        new_sections.append({"id": sid, "code": "", "name": sec["name"], "desc": sec["desc"], "en": sec["en"],
                             "group": group, "area": "marketing", "sub": "audit", "icon": sec["icon"]})
        d["sectionGuides"][sid] = g
        for f in sec["fields"]:
            fid = f["id"]
            if not fid.startswith(PREFIX) or fid in ids or fid in existing:
                fail("alan kimliği hatalı ya da tekrar: " + fid)
            ids.add(fid)
            if f["type"] not in TYPES:
                fail(f"{fid}: tür {f['type']}")
            for k in ("label", "en", "explanation", "scenario", "example", "rule"):
                if not str(f.get(k, "")).strip():
                    fail(f"{fid}: {k} boş")
            if f["type"] in ("text", "textarea", "url") and not f.get("placeholder"):
                fail(f"{fid}: placeholder yok")
            if f["type"] == "boolean":
                for k in ("yes", "no"):
                    if not (f.get(k) or {}).get("scenario") or not (f.get(k) or {}).get("example"):
                        fail(f"{fid}: {k} eksik")
                if "promptYes" not in f or "promptNo" not in f:
                    fail(f"{fid}: promptYes / promptNo yok")
            if f.get("auList") and f["type"] != "multiselect":
                fail(f"{fid}: auList yalnız multiselect")
            if f["type"] in ("select", "multiselect"):
                vals = [o["value"] for o in f.get("options", [])]
                if not vals or len(vals) != len(set(vals)):
                    fail(f"{fid}: seçenek yok ya da değer tekrarı")
                for o in f["options"]:
                    for k in ("label", "explanation", "scenario", "example"):
                        if not str(o.get(k, "")).strip():
                            fail(f"{fid}.{o['value']}: {k} boş")
                    if f.get("auList") and not o.get("ruleDetail"):
                        fail(f"{fid}.{o['value']}: kontrol ayrıntısı (ruleDetail) yok")
                    for n in o.get("needs", []):
                        if n not in access:
                            fail(f"{fid}.{o['value']}: needs {n} tanımsız")
            out = dict(f)
            out["section"] = sid
            out["agents"] = [agent_id(c) for c in f["agents"]] if f.get("agents") else list(sec_agents)
            order = ["id", "section", "label", "en", "type"]
            new_fields.append({k: out[k] for k in order} | {k: v for k, v in out.items() if k not in order})

    allf = {f["id"]: f for f in d["fields"]} | {f["id"]: f for f in new_fields}

    def values_of(f):
        if f["type"] == "boolean":
            return {"true", "false", True, False}
        return {o["value"] for o in f.get("options", [])}

    for f in new_fields:
        for c in f.get("showIf", []):
            src_f = allf.get(c["field"])
            if not src_f or not set(c["in"]) <= values_of(src_f):
                fail(f"{f['id']}: showIf hatalı {c}")
        for m in ([f["recommend"]] if isinstance(f.get("recommend"), dict) else f.get("recommend", [])):
            src_f = allf.get(m["field"])
            if not src_f:
                fail(f"{f['id']}: recommend alanı yok {m['field']}")
            mine = values_of(f)
            for k, v in m["map"].items():
                if k not in values_of(src_f) and str(k) not in {str(x) for x in values_of(src_f)}:
                    fail(f"{f['id']}: recommend anahtarı {k} {m['field']}'de yok")
                if not set(v) <= mine:
                    fail(f"{f['id']}: recommend değeri yok {set(v) - mine}")

    # pazarlama bölümlerinin sonuna ekle, kodları yeniden üret
    secs = d["sections"]
    last = max(k for k, x in enumerate(secs) if x.get("area") == "marketing")
    secs[last + 1:last + 1] = new_sections
    for k, x in enumerate(secs):
        x["code"] = f"{k:02d}"
    # alanlar: bölüm sırasına göre, au_* en sonda (mevcut alan sırası değişmez)
    d["fields"].extend(new_fields)
    d["seoAudit"] = {"version": src["version"], "access": access}

    out = s[:i] + json.dumps(d, ensure_ascii=False) + s[end:]
    if out.count(MARKER) != 1:
        fail("çıktı doğrulanamadı")
    open(html_path, "w", encoding="utf-8").write(out)
    nchk = sum(len(f.get("options", [])) for f in new_fields if f.get("auList"))
    print(f"{len(new_sections)} bölüm ({new_sections[0]['code']}–{new_sections[-1]['code']}), "
          f"{len(new_fields)} alan, {nchk} kontrol, "
          f"{sum(len(src_s['guide']['resources']) for src_s in src['sections'])} kaynak")
    print("md5", hashlib.md5(out.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
