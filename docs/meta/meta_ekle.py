#!/usr/bin/env python3
"""Meta Servisleri bölümlerini DATA'ya işler (2026-11-11). docs/google/google_ekle.py'nin kopyası.

Kullanım:
    python3 -I docs/meta/kaynak.py docs/meta/meta.json
    python3 -I docs/meta/meta_ekle.py web-proje-gelistirme.html docs/meta/meta.json
    python3 -I docs/meta/arayuz_ekle.py web-proje-gelistirme.html   # arayüz kancaları (tekrar zararsız)

Kaynak docs/meta/kaynak.py (elle yazılır) → meta.json. Bu betik:
  - sections[]: {id, code, name, desc, en, group, area:"marketing", sub:"meta", icon, refs?} — Google Servisleri bölümlerinden
    sonra, Ortak Bilgiler'den önce (menü alanı "meta"; kuralları Proje Kuralları'na ve Claude promptuna girer)
  - fields[]: kaynakta yazıldığı gibi + section; ajan kısaltmaları pozisyon ajanı kimliğine çevrilir
  - sectionGuides[bölüm id] = guide
  - Ortak Bilgiler › Hesap ve Etiket Kimlikleri (mk_ids): idsAdd satırlarını meta_business'tan sonra ekler, idsWhen
    satırlarının `when` listesine mt_services koşulu ekler
  - DATA.metaKit = {version, orig:{idsWhen:{satır: özgün when}, addedIds:[satır]}} — geri alma kaydı
Bölüm kodları (00–NN) bütün bölümler için sıradan yeniden üretilir.
Çalıştırma sırası: SEO Denetimi → Ortak Bilgiler → kılavuz → google_ekle.py → meta_ekle.py.

Denetimler google_ekle.py ile aynı (kimlik öneki mt_, zorunlu metinler, showIf / recommend başvuruları, refs, ajan
kimlikleri, https kaynaklar, </script ve <!-- yok, Kiril harf yok) + eklenen kimlik satırlarının tekliği ve biçimi.
Tekrar çalıştırılabilir: önce önceki mt_* bölüm, alan, rehber, eklenen satırlar ve mk_ids koşulları geri alınır.
"""
import json
import re
import sys

PREFIX = "mt_"
SUB = "meta"
KIT = "metaKit"
SVC = "mt_services"
AFTER_ROW = "meta_business"
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
        fail("kullanım: meta_ekle.py <html> <meta.json>")
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
    kit = d.get(KIT) or {}
    FI0 = {f["id"]: f for f in d["fields"]}
    added = set((kit.get("orig") or {}).get("addedIds") or [])
    FI0["mk_ids"]["accounts"] = [a for a in FI0["mk_ids"]["accounts"] if a["k"] not in added]
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
    d.pop(KIT, None)

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
                 "group": group, "area": "marketing", "sub": SUB, "icon": sec["icon"]}
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

    # mk_ids: yeni kimlik satırları (AFTER_ROW'dan sonra)
    acc = allf["mk_ids"]["accounts"]
    keys = {a["k"] for a in acc}
    pos = next((n for n, a in enumerate(acc) if a["k"] == AFTER_ROW), None)
    if pos is None:
        fail("mk_ids satırı yok: " + AFTER_ROW)
    for n, row in enumerate(src.get("idsAdd", [])):
        if set(row) - {"k", "label", "ph", "re"} or not row.get("k") or not row.get("label") or not row.get("ph"):
            fail("idsAdd satırı hatalı: " + json.dumps(row, ensure_ascii=False))
        if row["k"] in keys:
            fail("idsAdd satırı zaten var: " + row["k"])
        if row.get("re"):
            re.compile(row["re"])
            if not re.search(row["re"], row["ph"]):
                fail(f"idsAdd {row['k']}: örnek değer biçime uymuyor")
        keys.add(row["k"])
        acc.insert(pos + 1 + n, dict(row))

    # mk_ids satırlarına servis koşulu
    svc = allf.get(SVC)
    if not svc:
        fail(SVC + " alanı yok")
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
        row["when"] = list(row.get("when", [])) + [{"field": SVC, "in": list(vs)}]

    # konum: Google Servisleri bölümlerinden sonra
    secs = d["sections"]
    last_audit = max(i for i, x in enumerate(secs) if x.get("sub") in ("audit", "google"))
    d["sections"] = secs[:last_audit + 1] + new_sections + secs[last_audit + 1:]
    for n, x in enumerate(d["sections"]):
        x["code"] = "%02d" % n
    # alanlar: Google Servisleri alanlarından sonra
    fl = d["fields"]
    last_au = max(i for i, x in enumerate(fl) if x["id"].startswith(("au_", "gg_")))
    d["fields"] = fl[:last_au + 1] + new_fields + fl[last_au + 1:]
    d[KIT] = {"version": src.get("version", "1.0"), "orig": {"idsWhen": orig, "addedIds": [a["k"] for a in src.get("idsAdd", [])]}}

    out = s[:i] + json.dumps(d, ensure_ascii=False) + s[end:]
    open(html_path, "w", encoding="utf-8").write(out)
    nf = len(new_fields)
    print(f"tamam: {len(new_sections)} bölüm, {nf} karar, {sum(len(x['guide']['resources']) for x in src['sections'])} kaynak; "
          f"kodlar {new_sections[0]['code']}–{new_sections[-1]['code']}")


if __name__ == "__main__":
    main()
