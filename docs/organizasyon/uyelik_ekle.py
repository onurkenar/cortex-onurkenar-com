"""Kurul / komite / çalışma grubu rol unvanlarının pozisyon eşlemesini web-proje-gelistirme.html içindeki DATA.membership'e işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/uyelik_ekle.py web-proje-gelistirme.html docs/organizasyon/uyelik-eslemesi.json \
        docs/organizasyon/uyelik-ek-koltuklar.json [beklenen-md5]

Girdi (docs/organizasyon/uyelik-eslemesi.json): {"<unvan>": {"seats": [{"dept": "NN", "pos": "<pozisyon kimliği>"}], "note"?}}.
Unvanlar DATA.boards / committees / workingGroups kayıtlarındaki rol alanlarıdır: kurul ve komitede chair (Başkan), vice
(Başkan yardımcısı), secretariat (Sekreterya), members[] (Üye); çalışma grubunda sponsor (Sponsor), lead (Lider). Karşılığı
olmayan unvan seats: [] ve note ile yazılır. Pozisyon kimliği dpPos ile aynı kuraldadır (lider, lider/<id>, ofis, kurul,
kurul/<rol>, matris/<id>, <birim>, <birim>/<ekip>, <birim>/<rol>, <birim>/<ekip>/<rol>); departman "NN" = DATA.departments sırası.

Ek koltuklar (docs/organizasyon/uyelik-ek-koltuklar.json): organın departman listesinde olup hiçbir rol unvanıyla temsil
edilmeyen departmanlar için seçilen pozisyonlar — {"<organ id>": [{dept "NN", pos, role, why}]}. Rol türe göre sabittir: kurulda
"Davetli (raportör)" (kurul tanımında departmanlar gündeme göre davetli, oy hakkı yok), komitede "Departman temsilcisi", çalışma
grubunda "Çekirdek ekip" (ilgili departmanlardan iş sahibi, analist / uzman). Departman organın listesinde olmalı.

Çıktı DATA.membership: {titles: {unvan: [[departman id, pozisyon], …]} (yalnız eşlenenler), unmatched: [unvan],
extra: [{k: kr|km|cg, id, role, pos: [departman id, pozisyon]}]}. Arayüz rolleri
organ kayıtlarından okur; bir pozisyonun ajanı (katalog ajanı ya da pozisyon ajanı) o rolün otomatik üyesidir.
Denetimler: organlardaki her unvan eşlemede var, eşlemede fazladan unvan yok; pozisyon var; karşılıksız unvanın notu var.
Organlar ya da şema yeniden işlenince bu betik de yeniden çalıştırılmalıdır.
"""
import hashlib
import json
import sys

EXTRA = {"boards": ("kr", "Davetli (raportör)"), "committees": ("km", "Departman temsilcisi"), "workingGroups": ("cg", "Çekirdek ekip")}
ROLES = {"boards": ("chair", "vice", "secretariat"), "committees": ("chair", "vice", "secretariat"), "workingGroups": ("sponsor", "lead")}


def positions(d):
    o, P = d["org"], {"lider"}
    P |= {"lider/" + x["id"] for x in o.get("aides", [])} | {"matris/" + x["id"] for x in o.get("matrix", [])}
    if o.get("office"):
        P.add("ofis")
    if o.get("board"):
        P |= {"kurul"} | {"kurul/" + r["id"] for r in o["board"].get("roles", [])}
    for u in o["units"]:
        P.add(u["id"])
        P |= {u["id"] + "/" + r["id"] for r in u.get("roles", [])}
        for t in u["teams"]:
            ti = u["id"] + "/" + t["id"]
            if t.get("manager"):
                P.add(ti)
            P |= {ti + "/" + r["id"] for r in t["roles"]}
    return P


def build(src, data, extra_src):
    deps = data["departments"]
    titles = []
    for key, fields in ROLES.items():
        for it in data[key]["items"]:
            for f in fields:
                if it.get(f):
                    titles.append(it[f].strip())
            titles += [m.strip() for m in it.get("members") or []]
    titles = list(dict.fromkeys(titles))
    miss = [t for t in titles if t not in src]
    extra = [t for t in src if t not in titles]
    assert not miss and not extra, f"eşlemesi eksik: {miss[:10]} · organlarda olmayan: {extra[:10]}"
    P = {f"{n:02d}": (d["id"], positions(d)) for n, d in enumerate(deps, 1)}
    out, unmatched = {}, []
    for t in titles:
        v = src[t]
        assert set(v) <= {"seats", "note"} and isinstance(v["seats"], list), t
        if not v["seats"]:
            assert v.get("note"), f"karşılıksız unvanın notu yok: {t}"
            unmatched.append(t)
            continue
        L = []
        for s in v["seats"]:
            assert set(s) == {"dept", "pos"} and s["dept"] in P and s["pos"] in P[s["dept"]][1], (t, s)
            L.append([P[s["dept"]][0], s["pos"]])
        assert len({tuple(x) for x in L}) == len(L), (t, "tekrar")
        out[t] = L
    body = {it["id"]: (key, it) for key in ROLES for it in data[key]["items"]}
    extra, seen = [], set()
    for bid, L in extra_src.items():
        assert bid in body, f"organ yok: {bid}"
        key, it = body[bid]
        k, role = EXTRA[key]
        for s in L:
            assert set(s) == {"dept", "pos", "role", "why"} and s["role"] == role, (bid, s)
            assert s["dept"] in P and s["pos"] in P[s["dept"]][1], (bid, s)
            did = P[s["dept"]][0]
            assert did in it["depts"], f"{bid}: {s['dept']} organın departman listesinde değil"
            assert (bid, did, s["pos"]) not in seen, (bid, s)
            seen.add((bid, did, s["pos"]))
            extra.append({"k": k, "id": bid, "role": role, "pos": [did, s["pos"]]})
    return {"titles": out, "unmatched": unmatched, "extra": extra}


def main():
    html, jpath, xpath = sys.argv[1:4]
    want = sys.argv[4] if len(sys.argv) > 4 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    data["membership"] = build(json.load(open(jpath, encoding="utf-8")), data, json.load(open(xpath, encoding="utf-8")))
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    m = data["membership"]
    print(f"membership: {len(m['titles'])} unvan eşlendi, {len(m['unmatched'])} karşılıksız, {sum(len(v) for v in m['titles'].values())} pozisyon bağlantısı, {len(m['extra'])} ek koltuk")


if __name__ == "__main__":
    main()
