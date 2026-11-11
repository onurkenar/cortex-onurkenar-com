#!/usr/bin/env python3
"""Google Servisleri bölümlerini DATA'ya işler (2026-11-11).

Kullanım:
    python3 -I docs/google/kaynak.py docs/google/google.json      # kaynak → JSON
    python3 -I docs/google/google_ekle.py web-proje-gelistirme.html docs/google/google.json
    python3 -I docs/google/arayuz_ekle.py web-proje-gelistirme.html # arayüz kancaları (bir kez yeter; tekrar zararsız)

Kaynak docs/google/kaynak.py (elle yazılır) → google.json. Bu betik:
  - sections[]: {id, code, name, desc, en, group, area:"marketing", sub:"google", icon, refs?} — SEO Denetimi bölümlerinden
    sonra, Ortak Bilgiler'den önce (menü alanı "google"; kuralları Proje Kuralları'na ve Claude promptuna girer)
  - fields[]: kaynakta yazıldığı gibi + section; ajan kısaltmaları pozisyon ajanı kimliğine çevrilir
  - sectionGuides[bölüm id] = guide
  - Ortak Bilgiler › Hesap ve Etiket Kimlikleri (mk_ids) satırlarının `when` listesine gg_services koşulu (idsWhen)
  - DATA.googleKit = {version, orig:{idsWhen:{satır: özgün when}}} — geri alma kaydı
Bölüm kodları (00–NN) bütün bölümler için sıradan yeniden üretilir.

Denetimler: kimlik öneki (gg_) ve tekliği, zorunlu metinler (açıklama, senaryo, örnek, kural; seçeneklerde açıklama,
senaryo, örnek; boolean'da yes / no), seçenek değerlerinin tekliği, showIf ve recommend başvuruları (alan ve değerler),
refs alanlarının varlığı, ajan kimliklerinin şemadaki pozisyonlara karşılığı, kaynak adreslerinin https olması,
metinlerde </script ve <!-- bulunmaması, Kiril harf bulunmaması, idsWhen satırları ve servis değerleri.
Herhangi biri tutmazsa betik durur, dosyaya yazmaz.
Tekrar çalıştırılabilir: önce önceki gg_* bölüm, alan, rehber ve mk_ids koşulları geri alınır, sonra yeniden eklenir.
"""
import json
import re
import sys

PREFIX = "gg_"
TYPES = {"select", "multiselect", "boolean", "text", "textarea"}
MARKER = "<script>const DATA="


def fail(msg):
    sys.exit("HATA: " + msg)


def positions(dept):
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
        fail("kullanım: google_ekle.py <html> <google.json>")
    html_path, src_path = sys.argv[1], sys.argv[2]
    src = json.load(open(src_path, encoding="utf-8"))
    s = open(html_path, encoding="utf-8").read()
    if s.count(MARKER) != 1:
        fail("DATA satırı bulunamadı ya da birden çok")
    i = s.index(MARKER) + len(MARKER)
    d, end = json.JSONDecoder().raw_decode(s, i)

    for t in walk_strings(src):
        if "</script" in t.lower() or "<!--" in t:
            fail("metinde </script ya da <!-- var: " + t[:60])
        if re.search(r"[Ѐ-ӿ]", t):
            fail("metinde Kiril harf var: " + t[:80])

    # --- geri al ---
    kit = d.get("googleKit") or {}
    FI0 = {f["id"]: f for f in d["fields"]}
    for k, w in ((kit.get("orig") or {}).get("idsWhen") or {}).items():
        row = next((a for a in FI0["mk_ids"]["accounts"] if a["k"] == k), None)
        if row is not None:
            if w is None:
                row.pop("when", None)
            else:
                row["when"] = w
    d["sections"] = [x for x in d["sections"] if not x["id"].startswith(PREFIX)]
    d["fields"] = [x for x in d["fields"] if not x["id"].startswith(PREFIX)]
    for k in [k for k in d["sectionGuides"] if k.startswith(PREFIX)]:
        del d["sectionGuides"][k]
    d.pop("googleKit", None)

    group, agents = src["group"], src["agents"]
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
    new_sections, new_fields, ids = [], [], set()
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
        for r in sec.get("refs", []):
            if r not in existing:
                fail(f"{sid}: refs alanı yok: {r}")
        sec_agents = [agent_id(c) for c in sec.get("agents", [])]
        if not sec_agents:
            fail(f"{sid}: varsayılan ajan yok")
        out_s = {"id": sid, "code": "", "name": sec["name"], "desc": sec["desc"], "en": sec["en"],
                 "group": group, "area": "marketing", "sub": "google", "icon": sec["icon"]}
        if sec.get("refs"):
            out_s["refs"] = list(sec["refs"])
        new_sections.append(out_s)
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
            if f["type"] in ("text", "textarea") and not f.get("placeholder"):
                fail(f"{fid}: placeholder yok")
            if f["type"] == "boolean":
                for k in ("yes", "no"):
                    if not (f.get(k) or {}).get("scenario") or not (f.get(k) or {}).get("example"):
                        fail(f"{fid}: {k} eksik")
                if "{booltext}" not in f["rule"]:
                    fail(f"{fid}: boolean kuralında {{booltext}} yok")
            if f["type"] in ("select", "multiselect"):
                vals = [o["value"] for o in f.get("options", [])]
                if not vals or len(vals) != len(set(vals)):
                    fail(f"{fid}: seçenek yok ya da değer tekrarı")
                for o in f["options"]:
                    for k in ("label", "explanation", "scenario", "example"):
                        if not str(o.get(k, "")).strip():
                            fail(f"{fid}.{o['value']}: {k} boş")
                if "{label" not in f["rule"]:
                    fail(f"{fid}: kuralda {{label}} / {{labels}} yok")
            out = dict(f)
            out["section"] = sid
            out["agents"] = [agent_id(c) for c in f["agents"]] if f.get("agents") else list(sec_agents)
            order = ["id", "section", "label", "en", "type"]
            new_fields.append({k: out[k] for k in order} | {k: v for k, v in out.items() if k not in order})

    allf = {f["id"]: f for f in d["fields"]} | {f["id"]: f for f in new_fields}

    def values_of(f):
        if f["type"] == "boolean":
            return {True, False}
        return {o["value"] for o in f.get("options", [])}

    def norm_key(f, k):
        if f["type"] == "boolean":
            return {"true": True, "false": False}.get(str(k).lower(), k)
        return k

    for f in new_fields:
        for c in f.get("showIf", []):
            sf = allf.get(c["field"])
            if not sf or not set(c["in"]) <= values_of(sf):
                fail(f"{f['id']}: showIf hatalı {c}")
        for m in ([f["recommend"]] if isinstance(f.get("recommend"), dict) else f.get("recommend", [])):
            sf = allf.get(m["field"])
            if not sf:
                fail(f"{f['id']}: recommend alanı yok {m['field']}")
            mine = values_of(f)
            for k, v in m["map"].items():
                if norm_key(sf, k) not in values_of(sf):
                    fail(f"{f['id']}: recommend kaynak değeri yok {m['field']}={k}")
                if not set(v) <= mine:
                    fail(f"{f['id']}: recommend hedef değeri yok {v}")

    # mk_ids satırlarına servis koşulu
    svc = allf.get("gg_services")
    if not svc:
        fail("gg_services alanı yok")
    sv_vals = values_of(svc)
    orig = {}
    rows = {a["k"]: a for a in allf["mk_ids"]["accounts"]}
    for k, vs in src.get("idsWhen", {}).items():
        if k not in rows:
            fail("mk_ids satırı yok: " + k)
        if not set(vs) <= sv_vals:
            fail(f"idsWhen {k}: servis değeri yok {vs}")
        row = rows[k]
        orig[k] = json.loads(json.dumps(row.get("when"))) if "when" in row else None
        row["when"] = list(row.get("when", [])) + [{"field": "gg_services", "in": list(vs)}]

    # konum: SEO Denetimi bölümlerinden sonra
    secs = d["sections"]
    last_audit = max(i for i, x in enumerate(secs) if x.get("sub") == "audit")
    d["sections"] = secs[:last_audit + 1] + new_sections + secs[last_audit + 1:]
    for n, x in enumerate(d["sections"]):
        x["code"] = "%02d" % n
    # alanlar: SEO Denetimi alanlarından sonra
    fl = d["fields"]
    last_au = max(i for i, x in enumerate(fl) if x["id"].startswith("au_"))
    d["fields"] = fl[:last_au + 1] + new_fields + fl[last_au + 1:]
    d["googleKit"] = {"version": src.get("version", "1.0"), "orig": {"idsWhen": orig}}

    out = s[:i] + json.dumps(d, ensure_ascii=False) + s[end:]
    open(html_path, "w", encoding="utf-8").write(out)
    nf = len(new_fields)
    print(f"tamam: {len(new_sections)} bölüm, {nf} karar, {sum(len(x['guide']['resources']) for x in src['sections'])} kaynak; "
          f"kodlar {new_sections[0]['code']}–{new_sections[-1]['code']}")


if __name__ == "__main__":
    main()
