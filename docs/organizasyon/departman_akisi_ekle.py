"""Departman iş akışı JSON'larını web-proje-gelistirme.html içindeki DATA.deptFlows'a işler (departman şemasında
"<Departman> İş Akış Şeması" düğmesi).

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/departman_akisi_ekle.py web-proje-gelistirme.html docs/organizasyon/departman-akislari [beklenen-md5]
Klasördeki bütün NN-ad.json dosyaları her çalıştırmada baştan işlenir (DATA.deptFlows tamamen yeniden yazılır).
Departmanın hiyerarşisi (departman_ekle.py) ya da İş Akış Genel Şeması (is_akisi_ekle.py) yeniden işlenirse bu betiği de
yeniden çalıştırın: pozisyon kimlikleri ve genel şema adımları ona göre denetlenir.

Girdi (docs/organizasyon/departman-akislari/NN-ad.json; mevcut yapıdan türetilmiş öneri, kullanıcı düzenleyebilir):
  dept "NN" (dosya adının öneki), title, version, date, status ("taslak" | "onaylandı"), nature, purpose, principles[],
  parent {from, to} (İş Akış Genel Şeması'nda akışın başladığı ve döndüğü adım), phases[{id "A"…, name, desc}],
  steps[{id "<faz><sıra>", phase, type start|process|decision|parallel|end, title, text?, actor? (metin), who?[poz],
         depts?[ref], entries?[{name, ref}] (talep kaynakları), from? "reviews" | "authority", main? "Evet" | "Hayır",
         side? {label, title, text?, depts?[ref], links?[kod], goto?}}],
  types[{type, owner poz (sahip ekip / birim), support[birim id], ext[{dept, unit?}], time}] (talep türleri; departmanın her
         birimi en az bir türün sahibi), reviews[{ref, trigger, binding}], authority[{level, when, ref?, link?}],
  priority[{code, name, when, response}], algorithm[{code, ref ("A2" ya da "C4–C5"; boş olabilir)}].
ref: "poz" (departman içi pozisyon kimliği, dpPos ile aynı: lider · <birim> · <birim>/<ekip> · <birim>/<rol> ·
     <birim>/<ekip>/<rol> …) | {"unit": birim id} (departman içi birim) | {"dept": "NN", "unit"?: birim id} (başka departman).
link / links: komite, kurul ya da çalışma grubu kodu (KMT-NN, KRL-NN, CLG-NN) ya da sekme adı (committees, boards,
     workingGroups).

Çıktı DATA.deptFlows = {departman id: akış} (departman sırasıyla). Ref'ler {dept, pos} / {dept, unit} / {dept, unit?} olur
(departman id'siyle); types[].owner {dept, unit, pos}, support[{dept, unit}]; reviews[] ref'i kayda açılır.
Denetimler (tutmazsa betik durur): bilinmeyen anahtar yok; adım id'leri tekil, fazı tanımlı, faz sırasıyla; ilk adım start,
son adım end; karar adımında main ve side.label biri Evet biri Hayır, başlık dışında içerik yok (karar kutusu yalnız başlığı
çizer); goto, algoritma ve parent adımları var; pozisyon,
birim ve departman var; komite / kurul / çalışma grubu kodu var; destek birimi sahip birimle aynı değil ve tekrarsız; her
birim en az bir talep türünün sahibi.
"""
import hashlib
import json
import os
import re
import sys

TOP = {"dept", "title", "version", "date", "status", "nature", "purpose", "principles", "parent", "phases", "steps",
       "types", "reviews", "authority", "priority", "algorithm"}
STEP = {"id", "phase", "type", "title", "text", "actor", "who", "depts", "entries", "from", "main", "side"}
SIDE = {"label", "title", "text", "depts", "links", "goto"}
TYPES = {"start", "process", "decision", "parallel", "end"}
TABS = {"committees", "boards", "workingGroups"}


def positions(o):
    """dpPos ile aynı pozisyon kimlikleri → (başlık, birim id)."""
    m = {"lider": (o["leader"]["title"], None)}
    for x in o.get("aides", []):
        m["lider/" + x["id"]] = (x["title"], None)
    if o.get("board"):
        m["kurul"] = (o["board"]["title"], None)
        for r in o["board"].get("roles", []):
            m["kurul/" + r["id"]] = (r["title"], None)
        for c in o["board"].get("committees", []):
            m["komite/" + c["id"]] = (c["name"], None)
    if o.get("office"):
        m["ofis"] = (o["office"]["title"], None)
    for x in o.get("matrix", []):
        m["matris/" + x["id"]] = (x["title"], None)
    for u in o["units"]:
        m[u["id"]] = (u["leader"], u["id"])
        for r in u.get("roles", []):
            m[u["id"] + "/" + r["id"]] = (r["title"], u["id"])
        for t in u["teams"]:
            ti = u["id"] + "/" + t["id"]
            if t.get("manager"):
                m[ti] = (t["manager"], u["id"])
            for r in t["roles"]:
                m[ti + "/" + r["id"]] = (r["title"], u["id"])
    return m


def build(src, depts, data, fname):
    assert set(src) == TOP, (fname, "anahtarlar: " + ", ".join(sorted(set(src) ^ TOP)))
    assert re.fullmatch(r"\d\d", src["dept"]) and fname.startswith(src["dept"] + "-"), (fname, "dept öneki")
    n = int(src["dept"])
    assert 1 <= n <= len(depts) and depts[n - 1].get("org"), (fname, "hiyerarşisi olmayan departman")
    D = depts[n - 1]
    did, o = D["id"], D["org"]
    pos = positions(o)
    units = {u["id"] for u in o["units"]}
    org_codes = {**{c["id"]: 1 for c in data["committees"]["items"]}, **{c["id"]: 1 for c in data["boards"]["items"]},
                 **{c["id"]: 1 for c in data["workingGroups"]["items"]}}

    def ref(r, what):
        if isinstance(r, str):
            assert r in pos, (fname, what, "pozisyon yok", r)
            return {"dept": did, "pos": r}
        assert isinstance(r, dict), (fname, what, r)
        if "dept" not in r:
            assert set(r) == {"unit"} and r["unit"] in units, (fname, what, "birim yok", r)
            return {"dept": did, "unit": r["unit"]}
        assert set(r) <= {"dept", "unit"} and re.fullmatch(r"\d\d", r["dept"]), (fname, what, r)
        k = int(r["dept"])
        assert 1 <= k <= len(depts) and k != n, (fname, what, "departman", r)
        d = depts[k - 1]
        out = {"dept": d["id"]}
        if r.get("unit"):
            assert d.get("org") and any(u["id"] == r["unit"] for u in d["org"]["units"]), (fname, what, "birim yok", r)
            out["unit"] = r["unit"]
        return out

    def link(k, what):
        assert k in TABS or k in org_codes, (fname, what, "bağlantı yok", k)
        return k

    assert src["status"] in ("taslak", "onaylandı"), fname
    gen = {s["id"] for s in data["workflow"]["steps"]}
    assert set(src["parent"]) == {"from", "to"} and src["parent"]["from"] in gen and src["parent"]["to"] in gen, (fname, "parent")
    P = [p["id"] for p in src["phases"]]
    assert all(set(p) == {"id", "name", "desc"} for p in src["phases"]) and len(set(P)) == len(P), fname
    S = src["steps"]
    ids = [s["id"] for s in S]
    assert len(set(ids)) == len(ids), (fname, "adım id tekrarı")
    assert all(s["phase"] in P for s in S), (fname, "tanımsız faz")
    assert [P.index(s["phase"]) for s in S] == sorted(P.index(s["phase"]) for s in S), (fname, "adımlar faz sırasında değil")
    assert S[0]["type"] == "start" and S[-1]["type"] == "end", fname
    steps = []
    for s in S:
        w = "adım " + s.get("id", "?")
        assert set(s) <= STEP and re.fullmatch(r"[A-Z]\d+", s["id"]) and s["id"][0] == s["phase"], (fname, w)
        assert s["type"] in TYPES and s["title"].strip(), (fname, w)
        x = {k: s[k] for k in ("id", "phase", "type", "title", "text", "actor") if k in s}
        if s.get("who"):
            assert all(isinstance(r, str) for r in s["who"]), (fname, w, "who yalnız pozisyon")
            x["who"] = [ref(r, w) for r in s["who"]]
        if s.get("depts"):
            x["depts"] = [ref(r, w) for r in s["depts"]]
        if s.get("entries"):
            assert all(set(e) == {"name", "ref"} for e in s["entries"]), (fname, w)
            x["entries"] = [{"name": e["name"], **ref(e["ref"], w)} for e in s["entries"]]
        if "from" in s:
            assert s["from"] in ("reviews", "authority"), (fname, w)
            x["from"] = s["from"]
        if s["type"] == "decision":
            sd = s["side"]
            assert set(sd) <= SIDE and {s["main"], sd["label"]} == {"Evet", "Hayır"}, (fname, w)
            assert not set(s) & {"text", "actor", "who", "depts", "entries", "from"}, (fname, w, "karar kutusu yalnız başlığı çizer; ayrıntı yan dala ya da önceki adıma")
            y = {k: sd[k] for k in ("label", "title", "text", "goto") if k in sd}
            if "goto" in sd:
                assert sd["goto"] in ids and sd["goto"] != s["id"], (fname, w, sd["goto"])
            if sd.get("depts"):
                y["depts"] = [ref(r, w) for r in sd["depts"]]
            if sd.get("links"):
                y["links"] = [link(k, w) for k in sd["links"]]
            x["main"], x["side"] = s["main"], y
        else:
            assert "main" not in s and "side" not in s, (fname, w)
        steps.append(x)
    types, owners = [], set()
    for t in src["types"]:
        w = "talep türü " + t.get("type", "?")
        assert set(t) == {"type", "owner", "support", "ext", "time"} and t["type"].strip() and t["time"].strip(), (fname, w)
        assert t["owner"] in pos and pos[t["owner"]][1], (fname, w, "sahip birimin ya da ekibin pozisyonu olmalı")
        u = pos[t["owner"]][1]
        assert len(set(t["support"])) == len(t["support"]) and u not in t["support"], (fname, w, "destek birimi")
        sup = [ref({"unit": x}, w) for x in t["support"]]
        ext = [ref(x, w) for x in t["ext"]]
        assert all(isinstance(x, dict) and "dept" in x for x in t["ext"]), (fname, w, "ext başka departman olmalı")
        owners.add(u)
        types.append({"type": t["type"], "owner": {"dept": did, "unit": u, "pos": t["owner"]}, "support": sup, "ext": ext,
                      "time": t["time"]})
    miss = [u for u in units if u not in owners]
    assert not miss, (fname, "talep türü sahibi olmayan birim: " + ", ".join(miss))
    reviews = []
    for r in src["reviews"]:
        assert set(r) == {"ref", "trigger", "binding"} and isinstance(r["binding"], bool) and r["trigger"].strip(), (fname, r)
        reviews.append({**ref(r["ref"], "görüş"), "trigger": r["trigger"], "binding": r["binding"]})
    authority = []
    for a in src["authority"]:
        assert set(a) <= {"level", "when", "ref", "link"} and a["level"].strip() and a["when"].strip(), (fname, a)
        y = {"level": a["level"], "when": a["when"]}
        if "ref" in a:
            y["ref"] = ref(a["ref"], "yetki")
        if "link" in a:
            y["link"] = link(a["link"], "yetki")
        authority.append(y)
    assert all(set(p) == {"code", "name", "when", "response"} for p in src["priority"]), fname
    for a in src["algorithm"]:
        assert set(a) == {"code", "ref"} and a["code"].strip(), (fname, a)
        for r in filter(None, re.split(r"–", a["ref"])):
            assert r in ids, (fname, "algoritma ref", a)
    keep = ("title", "version", "date", "status", "nature", "purpose", "principles", "parent", "phases")
    return did, {**{k: src[k] for k in keep}, "steps": steps, "types": types, "reviews": reviews, "authority": authority,
                 "priority": src["priority"], "algorithm": src["algorithm"]}


def main():
    html, folder = sys.argv[1:3]
    want = sys.argv[3] if len(sys.argv) > 3 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    assert data.get("workflow"), "önce is_akisi_ekle.py"
    depts = data["departments"]
    out = {}
    for f in sorted(os.listdir(folder)):
        if not f.endswith(".json"):
            continue
        did, fl = build(json.load(open(os.path.join(folder, f), encoding="utf-8")), depts, data, f)
        assert did not in out, (f, "aynı departmanın ikinci akışı")
        out[did] = fl
    order = [d["id"] for d in depts]
    data["deptFlows"] = {k: out[k] for k in sorted(out, key=order.index)}
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    for k, fl in data["deptFlows"].items():
        S = fl["steps"]
        print(f"{k}: {len(fl['phases'])} faz, {len(S)} adım ({sum(s['type'] == 'decision' for s in S)} karar), "
              f"{len(fl['types'])} talep türü, {len(fl['reviews'])} zorunlu görüş "
              f"({sum(r['binding'] for r in fl['reviews'])} bağlayıcı), {len(fl['authority'])} yetki basamağı")


if __name__ == "__main__":
    main()
