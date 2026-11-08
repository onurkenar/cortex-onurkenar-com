#!/usr/bin/env python3
"""Ortak Bilgiler bölümlerini DATA'ya işler.

Kullanım:
    python3 -I docs/ortak-bilgiler/ortak_bilgiler_ekle.py web-proje-gelistirme.html docs/ortak-bilgiler/ortak-bilgiler.json

Kaynak: docs/ortak-bilgiler/ortak-bilgiler.json (elle yazılır). Kullanıcı isteği 2026-11-06: birden çok bölümün
kullandığı veriler (site adresi, marka adı, iletişim, renkler, fontlar, sosyal hesaplar, ölçüm kimlikleri,
rakipler) tek menüde yönetilir.

  - sections[]: {id, code, name, desc, en, group, area:"common", icon} — bütün bölümlerin sonuna eklenir,
    kodlar (00–NN) sıradan yeniden üretilir. Arayüzde ayrı menü alanı ("common"); kuralları Proje Kuralları'nda
    ve ana promptta PROJECT RULES içindedir.
  - fields: kaynakta {"id": …, "set": {…}} = mevcut alan bu bölüme TAŞINIR (kimlik aynı kalır, kayıtlı seçimler
    korunur; "set" metinleri üzerine yazar), {"id": …, "new": {…}} = yeni alan. Taşınan ve yeni alanlar alan
    listesinin sonuna kaynak sırasıyla konur.
  - sectionGuides[bölüm id] = guide
  - sectionSet / fieldSet: başka bölüm / alanlarda üzerine yazılacak anahtarlar (açıklama, jump metni …)
  - remove: kaldırılan alanlar (2026-11-06 birleştirme: kayıtlı değerleri arayüzdeki ocMig() yeni alana taşır);
    kaldırıldıktan sonra hiçbir alanın showIf / recommend / jump / derive'ı bunlara başvuramaz.
  - showIfMap: eski alan → {to, map}: koşullardaki eski alan yeni alana, değerler map'e göre çevrilir
    (map'te olmayan değer aynen kalır).
  - textSet: [{path, old, new}] — DATA içindeki bir metinde old → new (zaten new ise atlanır); path
    ["field", alan id, …] ile başlarsa alanın içinden yürür.
  - fieldSet'te derive: {from, fn|map} — alan değeri kaynaktan türetilir (arayüz ocSync / ocDv).
  - refs: bölüm id → ortak alan kimlikleri; o bölümün rehberinde ve "tüm kararlar" görünümünde
    "Ortak Bilgiler'den" kartı (değer + düzenle bağlantısı) çizilir. Önceki bütün refs silinip yeniden yazılır.
  - DATA.commonInfo = {version}

Denetimler: kimlik tekliği, taşınan alanın var olması, yeni alanın zorunlu metinleri (yer tutucu yalnız metin,
adres ve accounts alanında; seçenekli alanda her seçeneğin metinleri, boolean'da yes / no), ajan kimliklerinin şemada
olması, refs'teki alanların ortak bölümde olması, kaynak adreslerinin https olması, </script ve <!-- yokluğu.
Tekrar çalıştırılabilir. SEO Denetimi betiğinden (seo_denetimi_ekle.py) SONRA çalıştırın; o betik denetim
bölümlerini pazarlama bölümlerinin hemen arkasına ekler, bu betik ortak bölümleri en sona ekler.
"""
import hashlib
import json
import re
import sys

MARKER = "<script>const DATA="


def fail(m):
    sys.exit("HATA: " + m)


def positions(dept):
    o = dept.get("org") or {}
    P = {"lider"}
    for u in o.get("units", []) or []:
        P.add(u["id"])
        for r in u.get("roles", []) or []:
            P.add(u["id"] + "/" + r["id"])
        for t in u.get("teams", []) or []:
            P.add(u["id"] + "/" + t["id"])
            for r in t.get("roles", []) or []:
                P.add(u["id"] + "/" + t["id"] + "/" + r["id"])
    return P


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


def main():
    if len(sys.argv) != 3:
        fail("kullanım: ortak_bilgiler_ekle.py <html> <ortak-bilgiler.json>")
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

    area, group = src["area"], src["group"]
    depts = {x["id"]: positions(x) for x in d["departments"] if x.get("org")}

    def agent_ok(a):
        m = re.fullmatch(r"poz:([^:]+):(.+)", a)
        return bool(m) and m.group(1) in depts and m.group(2) in depts[m.group(1)]

    sec_ids = [x["id"] for x in src["sections"]]
    new_ids = [f["id"] for x in src["sections"] for f in x["fields"] if "new" in f]
    move_ids = [f["id"] for x in src["sections"] for f in x["fields"] if "new" not in f]
    if len(set(sec_ids)) != len(sec_ids) or len(set(new_ids + move_ids)) != len(new_ids + move_ids):
        fail("kimlik tekrarı")

    # önceki çalıştırmayı geri al (bölümler, rehberler, yeni alanlar, refs)
    d["sections"] = [x for x in d["sections"] if x.get("area") != area]
    for k in sec_ids:
        d["sectionGuides"].pop(k, None)
    d["fields"] = [f for f in d["fields"] if f["id"] not in new_ids]
    for x in d["sections"]:
        x.pop("refs", None)
    other_secs = {x["id"] for x in d["sections"]}
    if set(sec_ids) & other_secs:
        fail("ortak bölüm kimliği başka bölümle çakışıyor")

    FI = {f["id"]: f for f in d["fields"]}
    moved = []
    for sec in src["sections"]:
        for k in ("name", "en", "desc", "icon"):
            if not str(sec.get(k, "")).strip():
                fail(f"{sec['id']}: {k} boş")
        g = sec["guide"]
        if not g.get("purpose") or len(g.get("criteria", [])) < 3 or len(g.get("pitfalls", [])) < 3 or not g.get("resources"):
            fail(f"{sec['id']}: rehber eksik")
        for r in g["resources"]:
            if not str(r.get("url", "")).startswith("https://") or not r.get("title") or not r.get("note"):
                fail(f"{sec['id']}: kaynak hatalı {r}")
        for spec in sec["fields"]:
            fid = spec["id"]
            if "new" in spec:
                if fid in FI:
                    fail(f"{fid}: yeni alan kimliği zaten var")
                f = {"id": fid, "section": sec["id"]} | spec["new"]
                for k in ("label", "en", "type", "rule", "explanation", "scenario", "example"):
                    if not str(f.get(k, "")).strip():
                        fail(f"{fid}: {k} boş")
                if f["type"] in ("text", "textarea", "url", "accounts") and not str(f.get("placeholder", "")).strip():
                    fail(f"{fid}: placeholder boş")
                if f["type"] in ("select", "multiselect"):
                    for o in f.get("options") or []:
                        for k in ("value", "label", "explanation", "scenario", "example"):
                            if not str(o.get(k, "")).strip():
                                fail(f"{fid}.{o.get('value')}: {k} boş")
                    if len(f.get("options") or []) < 2:
                        fail(f"{fid}: en az 2 seçenek")
                if f["type"] == "boolean" and not (f.get("yes") and f.get("no")):
                    fail(f"{fid}: yes / no eksik")
                if not f.get("agents"):
                    fail(f"{fid}: ajan yok")
            else:
                if fid not in FI:
                    fail(f"{fid}: taşınacak alan yok")
                f = FI[fid]
                f["section"] = sec["id"]
                for k, v in spec.get("set", {}).items():
                    f[k] = v
            for a in f.get("agents", []):
                if not agent_ok(a):
                    fail(f"{fid}: ajan şemada yok {a}")
            moved.append(f)
    ids = {f["id"] for f in moved}
    d["fields"] = [f for f in d["fields"] if f["id"] not in ids] + moved

    d["sections"] += [{"id": x["id"], "code": "", "name": x["name"], "desc": x["desc"], "en": x["en"],
                       "group": group, "area": area, "icon": x["icon"]} for x in src["sections"]]
    for k, x in enumerate(d["sections"]):
        x["code"] = f"{k:02d}"
    for x in src["sections"]:
        d["sectionGuides"][x["id"]] = x["guide"]

    rm = set(src.get("remove", []))
    d["fields"] = [f for f in d["fields"] if f["id"] not in rm]
    for f in d["fields"]:
        for c in f.get("showIf", []) or []:
            m = src.get("showIfMap", {}).get(c["field"])
            if m:
                c["field"] = m["to"]
                c["in"] = list(dict.fromkeys(x for v in c["in"] for x in m["map"].get(v, [v])))
    SI = {x["id"]: x for x in d["sections"]}
    FI = {f["id"]: f for f in d["fields"]}
    for t in src.get("textSet", []):
        o, path = (FI[t["path"][1]], t["path"][2:]) if t["path"][0] == "field" else (d, t["path"])
        for k in path[:-1]:
            o = o[k]
        k = path[-1]
        if t["new"] in o[k]:
            continue
        if o[k].count(t["old"]) != 1:
            fail(f"textSet: metin bulunamadı {t['path']}")
        o[k] = o[k].replace(t["old"], t["new"])
    for sid, kv in src.get("sectionSet", {}).items():
        if sid not in SI:
            fail(f"sectionSet: bölüm yok {sid}")
        SI[sid].update(kv)
    for fid, kv in src.get("fieldSet", {}).items():
        if fid not in FI:
            fail(f"fieldSet: alan yok {fid}")
        if "jump" in kv and kv["jump"]["field"] not in FI:
            fail(f"fieldSet: jump hedefi yok {kv['jump']}")
        FI[fid].update(kv)
    for sid, L in src["refs"].items():
        if sid not in SI or SI[sid].get("area") == area:
            fail(f"refs: bölüm yok ya da ortak bölüm {sid}")
        for fid in L:
            if fid not in FI or SI[FI[fid]["section"]].get("area") != area:
                fail(f"refs: {sid} → {fid} ortak alan değil")
        SI[sid]["refs"] = list(L)
    def vals(f):
        return {"true", "false"} if f["type"] == "boolean" else {o["value"] for o in f.get("options", [])}
    for f in d["fields"]:
        for c in f.get("showIf", []) or []:
            if c["field"] not in FI or not {str(x).lower() if isinstance(x, bool) else x for x in c["in"]} <= vals(FI[c["field"]]):
                fail(f"{f['id']}: showIf hatalı {c}")
        recs = f.get("recommend")
        for m in ([recs] if isinstance(recs, dict) else (recs or [])):
            if m["field"] not in FI:
                fail(f"{f['id']}: recommend alanı yok {m['field']}")
            for k, v in m["map"].items():
                if k not in vals(FI[m["field"]]) or not set(v) <= vals(f):
                    fail(f"{f['id']}: recommend değeri hatalı {m['field']} {k} {v}")
        for k in ("jump", "derive"):
            if f.get(k):
                tgt = f[k].get("field") or f[k].get("from")
                if tgt not in FI:
                    fail(f"{f['id']}: {k} hedefi yok {tgt}")
        if f.get("derive") and "map" in f["derive"] and not set(f["derive"]["map"].values()) <= vals(f):
            fail(f"{f['id']}: derive değeri hatalı")
    d["commonInfo"] = {"version": src["version"]}

    out = s[:i] + json.dumps(d, ensure_ascii=False) + s[end:]
    open(hp, "w", encoding="utf-8").write(out)
    cs = [x for x in d["sections"] if x.get("area") == area]
    print(f"{len(cs)} bölüm ({cs[0]['code']}–{cs[-1]['code']}), {len(moved)} alan ({len(moved) - len(new_ids)} taşındı, "
          f"{len(new_ids)} yeni), {sum(len(v) for v in src['refs'].values())} bağlantı, {len(src['refs'])} bölümde")
    print("md5", hashlib.md5(out.encode("utf-8")).hexdigest())


if __name__ == "__main__":
    main()
