"""İş akışı JSON'unu web-proje-gelistirme.html içindeki DATA.workflow'a işler ("İş Akış Genel Şeması", Ajan Yapısı sekmesi).

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/is_akisi_ekle.py web-proje-gelistirme.html docs/organizasyon/is-akisi.json [beklenen-md5]

Girdi (docs/organizasyon/is-akisi.json; mevcut yapıdan türetilmiş öneri, kullanıcı düzenleyebilir):
  title, version, date, status ("taslak" | "onaylandı"), nature, purpose, principles[],
  phases[{id "A"…, name, desc}],
  steps[{id "<faz><sıra>" (ör. A1), phase, type start|process|decision|parallel|end, title, text?, actor?,
         depts?[{dept "NN", unit?}], entries?[{name, dept, unit?}] (giriş noktaları), from? "reviews" | "authority"
         (adımın içinde o tablo çizilir), main? (karar: ana yolda devam eden yanıt "Evet" | "Hayır"),
         side? {label (öteki yanıt), title, text?, depts?, links?[committees|boards|workingGroups], goto? (adım id)}}],
  routes[{type, owner{dept, unit}, support[dept]}] (yönlendirme tablosu; 23 departmanın her biri en az bir kez sahip),
  reviews[{dept, unit?, trigger, binding}] (zorunlu görüşler), authority[{level, when, dept?, link?}] (yetki basamakları),
  priority[{code, name, when, response}], algorithm[{code, ref ("A2" ya da "B2–B3"; boş olabilir)}].
Departman "NN" = DATA.departments sırası (01–23); unit = o departmandaki birim id'si (şemadaki kimlik).

Çıktı DATA.workflow: aynı yapı; departman alanları departman id'sine çevrilir (dept "NN" → "muhasebe" …).
Denetimler (tutmazsa betik durur): bilinmeyen anahtar yok; adım id'leri tekil, fazı tanımlı ve faz sırasıyla; ilk adım start,
son adım end; karar adımında main ve side.label biri Evet biri Hayır; goto ve algoritma ref'leri var olan adım; departman ve
birim var; destek departmanı sahibiyle aynı değil ve tekrarsız; her departman en az bir talep türünün sahibi.
"""
import hashlib
import json
import re
import sys

TOP = {"title", "version", "date", "status", "nature", "purpose", "principles", "phases", "steps", "routes", "reviews",
       "authority", "priority", "algorithm"}
STEP = {"id", "phase", "type", "title", "text", "actor", "depts", "entries", "from", "main", "side"}
SIDE = {"label", "title", "text", "depts", "links", "goto"}
TYPES = {"start", "process", "decision", "parallel", "end"}
LINKS = {"committees", "boards", "workingGroups"}


def ref(r, depts, what, unit_ok=True):
    assert isinstance(r, dict) and set(r) <= {"dept", "unit", "name"} and re.fullmatch(r"\d\d", r.get("dept", "")), (what, r)
    n = int(r["dept"])
    assert 1 <= n <= len(depts), (what, r)
    d = depts[n - 1]
    out = {"dept": d["id"]}
    if r.get("unit"):
        assert unit_ok and any(u["id"] == r["unit"] for u in d["org"]["units"]), (what, "birim yok", r)
        out["unit"] = r["unit"]
    if "name" in r:
        out = {"name": r["name"], **out}
    return out


def build(src, depts):
    assert set(src) == TOP, "anahtarlar: " + ", ".join(sorted(set(src) ^ TOP))
    assert src["status"] in ("taslak", "onaylandı")
    P = [p["id"] for p in src["phases"]]
    assert all(set(p) == {"id", "name", "desc"} for p in src["phases"]) and len(set(P)) == len(P)
    S = src["steps"]
    ids = [s["id"] for s in S]
    assert len(set(ids)) == len(ids), "adım id tekrarı"
    assert [P.index(s["phase"]) for s in S] == sorted(P.index(s["phase"]) for s in S), "adımlar faz sırasında değil"
    assert S[0]["type"] == "start" and S[-1]["type"] == "end"
    steps = []
    for s in S:
        w = "adım " + s.get("id", "?")
        assert set(s) <= STEP and re.fullmatch(r"[A-Z]\d+", s["id"]) and s["id"][0] == s["phase"], w
        assert s["type"] in TYPES and s["title"].strip(), w
        x = {k: s[k] for k in ("id", "phase", "type", "title", "text", "actor") if k in s}
        if s.get("depts"):
            x["depts"] = [ref(r, depts, w) for r in s["depts"]]
        if s.get("entries"):
            x["entries"] = [ref(r, depts, w) for r in s["entries"]]
        if "from" in s:
            assert s["from"] in ("reviews", "authority"), w
            x["from"] = s["from"]
        if s["type"] == "decision":
            sd = s["side"]
            assert set(sd) <= SIDE and {s["main"], sd["label"]} == {"Evet", "Hayır"}, w
            y = {k: sd[k] for k in ("label", "title", "text", "goto") if k in sd}
            if "goto" in sd:
                assert sd["goto"] in ids and sd["goto"] != s["id"], (w, sd["goto"])
            if sd.get("depts"):
                y["depts"] = [ref(r, depts, w) for r in sd["depts"]]
            if sd.get("links"):
                assert set(sd["links"]) <= LINKS, w
                y["links"] = sd["links"]
            x["main"], x["side"] = s["main"], y
        else:
            assert "main" not in s and "side" not in s, w
        steps.append(x)
    routes, owners = [], set()
    for r in src["routes"]:
        assert set(r) == {"type", "owner", "support"}, r
        o = ref(r["owner"], depts, r["type"])
        sup = [ref({"dept": d}, depts, r["type"])["dept"] for d in r["support"]]
        assert len(set(sup)) == len(sup) and o["dept"] not in sup, r
        owners.add(o["dept"])
        routes.append({"type": r["type"], "owner": o, "support": sup})
    miss = [d["id"] for d in depts if d["id"] not in owners]
    assert not miss, "talep türü sahibi olmayan departman: " + ", ".join(miss)
    reviews = []
    for r in src["reviews"]:
        assert set(r) <= {"dept", "unit", "trigger", "binding"} and isinstance(r["binding"], bool), r
        reviews.append({**ref({k: r[k] for k in ("dept", "unit") if k in r}, depts, "görüş"), "trigger": r["trigger"], "binding": r["binding"]})
    authority = []
    for a in src["authority"]:
        assert set(a) <= {"level", "when", "dept", "link"} and a.get("link", "committees") in LINKS, a
        y = {"level": a["level"], "when": a["when"]}
        if "dept" in a:
            y["dept"] = ref({"dept": a["dept"]}, depts, "yetki")["dept"]
        if "link" in a:
            y["link"] = a["link"]
        authority.append(y)
    assert all(set(p) == {"code", "name", "when", "response"} for p in src["priority"])
    for a in src["algorithm"]:
        assert set(a) == {"code", "ref"} and a["code"].strip(), a
        for r in filter(None, re.split(r"–", a["ref"])):
            assert r in ids, ("algoritma ref", a)
    return {**{k: src[k] for k in ("title", "version", "date", "status", "nature", "purpose", "principles", "phases")},
            "steps": steps, "routes": routes, "reviews": reviews, "authority": authority, "priority": src["priority"],
            "algorithm": src["algorithm"]}


def main():
    html, jpath = sys.argv[1:3]
    want = sys.argv[3] if len(sys.argv) > 3 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    wf = build(json.load(open(jpath, encoding="utf-8")), data["departments"])
    data["workflow"] = wf
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    print(f"workflow: {len(wf['phases'])} faz, {len(wf['steps'])} adım ({sum(s['type'] == 'decision' for s in wf['steps'])} karar), "
          f"{len(wf['routes'])} talep türü, {len(wf['reviews'])} zorunlu görüş, {len(wf['authority'])} yetki basamağı")


if __name__ == "__main__":
    main()
