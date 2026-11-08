"""Ajan kimlik defteri: her pozisyona kalıcı bir Agent ID verir ve DATA.agentIds'e işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/ajan_kimlik_ekle.py web-proje-gelistirme.html docs/ajan-kaydi/agent-id-ledger.json [beklenen-md5]

Neden defter: pozisyon kimlikleri (dpPos) bazı departmanlarda unvandan türer; unvan değişince pozisyon kimliği de
değişebilir. Agent ID ise hiç değişmemeli. Defter "departman|pozisyon" anahtarını bir kez verilen kimliğe bağlar:
- Defterde olan anahtar her çalıştırmada aynı kimliği alır (betik idempotenttir; ikinci çalıştırma hiçbir şey
  değiştirmez).
- Yeni pozisyon departmanın sıradaki numarasını alır (AGT-<departman kodu>-<4 hane>), dpPos sırasıyla.
- Kaynakta artık olmayan anahtar silinmez, "retired" olur; numarası bir daha verilmez.
- Pozisyon kimliği değişmişse (ör. unvan değişikliği) eski anahtarı yenisine `aliases` ile bağlayın:
  {"departman|eski-pozisyon": "departman|yeni-pozisyon"}; kimlik yeni anahtara taşınır. Betik aynı çalıştırmada
  hem emekliye ayrılan hem yeni eklenen pozisyon görürse bunları "olası yeniden adlandırma" diye yazar.
- Departman kodu (NN) ilk atamadaki sıradan alınır ve defterde sabit kalır; departman sırası değişse de kimlik
  değişmez.

Pozisyon kümesi arayüzdeki dpPos ile aynıdır (yönetim kurulu komite düğümleri hariç — pozisyon ajanlarıyla ve
dpStats().p ile aynı küme). Sıra: lider, yönetim pozisyonları (aides), kurul, kurul rolleri, ofis, matris roller,
birimler (birim lideri, birime bağlı roller, ekip yöneticisi, ekip rolleri).

Çıktı DATA.agentIds: {"orchestrator": "AGT-00-0001", "depts": {departman id: "NN"},
"pos": {departman id: {pozisyon id: sıra no}}} — yalnız etkin kayıtlar. Arayüz kimliği
"AGT-" + depts[d] + "-" + 4 haneli sıra no olarak kurar (rgId).
"""
import datetime
import hashlib
import json
import os
import sys

ORCH = "AGT-00-0001"


def positions(d):
    """dpPos ile aynı sırada (pozisyon id, unvan, birim id) listesi; komite düğümleri hariç."""
    o = d.get("org")
    if not o:
        return None
    out = [("lider", o["leader"]["title"], "")]
    for x in o.get("aides") or []:
        out.append(("lider/" + x["id"], x["title"], ""))
    if o.get("board"):
        out.append(("kurul", o["board"]["title"], ""))
        for r in o["board"].get("roles") or []:
            out.append(("kurul/" + r["id"], r["title"], ""))
    if o.get("office"):
        out.append(("ofis", o["office"]["title"], ""))
    for x in o.get("matrix") or []:
        out.append(("matris/" + x["id"], x["title"], ""))
    for u in o["units"]:
        out.append((u["id"], u["leader"], u["id"]))
        for r in u.get("roles") or []:
            out.append((u["id"] + "/" + r["id"], r["title"], u["id"]))
        for t in u["teams"]:
            ti = u["id"] + "/" + t["id"]
            if t.get("manager"):
                out.append((ti, t["manager"], u["id"]))
            for r in t["roles"]:
                out.append((ti + "/" + r["id"], r["title"], u["id"]))
    ids = [p[0] for p in out]
    assert len(ids) == len(set(ids)), f"{d['id']}: tekrarlayan pozisyon kimliği"
    return out


def main():
    html, lpath = sys.argv[1:3]
    want = sys.argv[3] if len(sys.argv) > 3 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    today = datetime.date.today().isoformat()
    if os.path.exists(lpath):
        led = json.load(open(lpath, encoding="utf-8"))
        assert led.get("format") == "wp-onke-agent-id-ledger", "defter biçimi tanınmadı"
    else:
        led = {"format": "wp-onke-agent-id-ledger", "version": 1, "orchestrator": ORCH, "depts": {}, "entries": {},
               "aliases": {}}
    E, A = led["entries"], led["aliases"]
    # takma adlar: eski anahtarın kimliği yeni anahtara taşınır. Yeni anahtar önceki çalıştırmada geçici bir kimlik
    # almışsa o kimlik `replaced_id` olarak not edilir; sayaç geri alınmadığı için bir daha verilmez.
    for old, new in A.items():
        if old in E and (new not in E or E[old].get("status") == "retired"):
            tmp = E[new]["id"] if new in E else None
            E[new] = dict(E.pop(old), status="active", alias_of=old)
            E[new].pop("retired", None)
            if tmp:
                E[new]["replaced_id"] = tmp
    used = {e["id"] for e in E.values()}
    assert len(used) == len(E), "defterde tekrarlayan kimlik"
    seen, added, revived, missing = set(), [], [], []
    for n, d in enumerate(data["departments"], 1):
        P = positions(d)
        if P is None:
            missing.append(d["id"])
            continue
        dd = led["depts"].setdefault(d["id"], {"code": f"{n:02d}", "next": 1})
        for pid, title, unit in P:
            k = d["id"] + "|" + pid
            seen.add(k)
            e = E.get(k)
            if e is None:
                aid = f"AGT-{dd['code']}-{dd['next']:04d}"
                assert aid not in used, f"kimlik çakışması: {aid}"
                dd["next"] += 1
                used.add(aid)
                E[k] = {"id": aid, "title": title, "unit": unit, "since": today, "status": "active"}
                added.append(k)
            else:
                if e.get("status") != "active":
                    e["status"] = "active"
                    e.pop("retired", None)
                    revived.append(k)
                e["title"], e["unit"] = title, unit
    retired = []
    for k, e in E.items():
        if k not in seen and e.get("status") == "active":
            e["status"], e["retired"] = "retired", today
            retired.append(k)
    # DATA.agentIds: yalnız etkin kayıtlar, sıra no ile
    pos = {}
    for k, e in E.items():
        if e["status"] != "active":
            continue
        dept, pid = k.split("|", 1)
        pos.setdefault(dept, {})[pid] = int(e["id"].rsplit("-", 1)[1])
    ids = {"orchestrator": led["orchestrator"], "depts": {k: v["code"] for k, v in led["depts"].items()},
           "pos": {d["id"]: pos[d["id"]] for d in data["departments"] if d["id"] in pos}}
    changed = data.get("agentIds") != ids
    data["agentIds"] = ids
    json.dump(led, open(lpath, "w", encoding="utf-8"), ensure_ascii=False, indent=1, sort_keys=False)
    if changed:
        t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
        open(html, "w", encoding="utf-8").write(t)
    act = sum(1 for e in E.values() if e["status"] == "active")
    print(f"{act} etkin kimlik ({len(E) - act} emekli), {len(led['depts'])} departman; bu çalıştırmada "
          f"{len(added)} yeni, {len(revived)} yeniden etkin, {len(retired)} emekliye ayrıldı; "
          f"DATA.agentIds {'güncellendi' if changed else 'değişmedi'}")
    if missing:
        print("Kaynak verisi olmayan departmanlar (missing_source): " + ", ".join(missing))
    if added and retired and len(added) != act:
        cand = [(o, n) for o in retired for n in added
                if o.split("|")[0] == n.split("|")[0] and E[o].get("unit") == E[n].get("unit")]
        if cand:
            print("Olası yeniden adlandırma (doğruysa aliases'a ekleyip yeniden çalıştırın): "
                  + "; ".join(f"{o} → {n}" for o, n in cand[:20]))


if __name__ == "__main__":
    main()
