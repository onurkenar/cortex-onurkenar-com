"""Bütün ajanların hiyerarşik listesini (Markdown) uygulamanın verisinden üretir.

Kullanım (proje kökünden):
    python3 -I docs/organizasyon/ajan_listesi.py web-proje-gelistirme.html docs/ajan-listesi.md

Uygulamadaki kurallar aynen uygulanır: her pozisyonun (komite düğümleri hariç) ajanı pozisyonun kendi ajanıdır (pagBase);
DATA.positionAgents'ta içeriği olan pozisyonlarda eski geliştirme / ürün içi ajanların içeriği ve ürün içi görev o ajandadır.
Dosya adı = bütün pozisyon ajanları projeye eklendiğinde zip'te alacağı ad (agSlug + agZipFiles tekrar soneki).
Projedeki kişisel seçimler (state) okunmaz. HTML'e yazmaz.
"""
import json
import re
import sys

FOLD = str.maketrans("çğıöşüâî", "cgiosuai")


def norm(s):
    s = s.replace("I", "ı").replace("İ", "i").lower().translate(FOLD)
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def slug(s):
    return norm(s).replace(" ", "-") or "ajan"


def main():
    html, out = sys.argv[1:3]
    t = open(html, encoding="utf-8").read()
    k = "const DATA="
    D, _ = json.JSONDecoder().raw_decode(t[t.index(k) + len(k):])
    deps, PA = D["departments"], D.get("positionAgents", {})
    code = {d["id"]: f"{n:02d}" for n, d in enumerate(deps, 1)}
    skills = {}
    # Skill dosya adı: dizinle eşleşen skill'in kimliği "dz:<eklenti>/<ad>"dır, listede dosya adı (slug) yazılır.
    sname = {s["id"]: s.get("slug") or s["id"] for s in D.get("skillCatalog", [])}
    for s in D.get("skillCatalog", []):
        for p in s.get("positions") or []:
            skills.setdefault((p["dept"], p["pos"]), []).append(s["id"])
    # Dizin skill'lerinin varsayılan pozisyonları (DATA.skillPositions, docs/skills/pozisyon-eslesme.json); ad = "/" sonrası.
    for sid, L in (D.get("skillPositions") or {}).items():
        sname.setdefault(sid, sid.split("/", 1)[-1])
        for k in L:
            d, _, q = k.partition("|")
            skills.setdefault((d, q), []).append(sid)
    used = {}

    def zipname(base):
        n, i = base, 2
        while n in used:
            n = f"{base}-{i}"
            i += 1
        used[n] = 1
        return n

    stats = {"pos": 0, "auto": 0, "catpos": 0}
    files = {}
    body = []

    def agent(did, pid, title):
        stats["pos"] += 1
        x = PA.get(did + "|" + pid)
        sk = sorted(set(sname.get(k, k) for k in (skills.get((did, pid)) or []) + ((x or {}).get("skills") or [])))
        tail = f" · skill: {', '.join(sk)}" if sk else ""
        f = files[(did, pid)] = zipname(code[did] + "-" + slug(title))
        if x:
            stats["catpos"] += 1
            pr = x.get("product")
            return f"pozisyon ajanı `{f}.md`" + (f" · ürün içi görev: **{pr['name']}**" if pr else "") + tail
        stats["auto"] += 1
        return f"pozisyon ajanı `{f}.md`" + tail

    def line(depth, label, title, did, pid, extra=""):
        body.append(f"{'  ' * depth}- {label}{title}{extra} — {agent(did, pid, title)}")

    for d in deps:
        o, did = d["org"], d["id"]
        before = dict(stats)
        body += ["", ""]
        head_at = len(body)
        body.append("")
        if o.get("board"):
            b = o["board"]
            if b.get("reportsTo"):
                body.append(f"- Bağlı olduğu: {b['reportsTo']}")
            line(0, "**Kurul:** ", b["title"], did, "kurul")
            for r in b.get("roles", []):
                line(1, "", r["title"], did, "kurul/" + r["id"])
            for c in b.get("committees", []):
                body.append(f"  - Komite: {c['name']} (ajanı yok — komite düğümü)")
        elif o.get("reportsTo"):
            body.append(f"- Bağlı olduğu: {o['reportsTo']}" + (f" · fonksiyonel: {o['functional']['title']}" if o.get("functional") else ""))
        lt = o["leader"]["title"] + (f" ({o['leader']['abbr']})" if o["leader"].get("abbr") else "")
        b0 = 1 if o.get("board") else 0  # kurul varsa lider kurulun altında
        line(b0, "**Departman lideri:** ", lt, did, "lider")
        for x in o.get("aides", []):
            line(b0 + 1, "", x["title"], did, "lider/" + x["id"], f" _({x['status']})_" if x.get("status") else "")
        top = b0 + 1
        if o.get("office"):
            line(b0 + 1, "**Ara yönetici:** ", o["office"]["title"], did, "ofis")
            top = b0 + 2
        for x in o.get("matrix", []):
            line(b0 + 1, "Matris rol: ", x["title"], did, "matris/" + x["id"])
        for u in o["units"]:
            line(top, f"**Birim — {u['name']}:** ", u["leader"], did, u["id"])
            for r in u.get("roles", []):
                line(top + 1, "", r["title"], did, u["id"] + "/" + r["id"])
            for tm in u["teams"]:
                ti = u["id"] + "/" + tm["id"]
                if tm.get("manager"):
                    line(top + 1, f"Ekip — {tm['name']}: " if tm.get("name") else "", tm["manager"], did, ti)
                    rd = top + 2
                else:
                    body.append(f"{'  ' * (top + 1)}- Ekip — {tm.get('name') or tm['id']} (ekip yöneticisi yok; roller birim liderine bağlı)")
                    rd = top + 2
                for r in tm["roles"]:
                    line(rd, "", r["title"], did, ti + "/" + r["id"])
        n = stats["pos"] - before["pos"]
        c = stats["catpos"] - before["catpos"]
        body[head_at - 1] = f"## {code[did]} - {d['name']}"
        body[head_at] = f"{len(o['units'])} birim · {n} pozisyon · katalog ajanlı {c} · pozisyon ajanı {n - c}\n"
    n_prod = sum(1 for x in PA.values() if x.get("product"))
    head = [
        "# Ajan listesi — şirket organizasyonuna göre",
        "",
        "_Uygulamanın verisinden üretildi (`docs/organizasyon/ajan_listesi.py`); projedeki kişisel seçimler (projeye eklenen ajanlar, düzenlemeler) dahil değildir._",
        "",
        "## Özet",
        "",
        f"- {len(deps)} departman · {sum(len(d['org']['units']) for d in deps)} birim · {stats['pos']:,} pozisyon".replace(",", "."),
        f"- Her pozisyonun bir ajanı var: {stats['pos']:,} pozisyon ajanı (varsayılan olarak projede değil)".replace(",", "."),
        f"- Ürün içi görevli: {n_prod} pozisyon ajanı (sitede ya da panelde çalışan yapay zekâ özelliğinden sorumlu)",
        "- Dosya adı: ajan projeye eklendiğinde `.claude/agents/` altındaki adı (bütün ajanlar eklendiğinde aynı adlılar `-2` alır).",
        "",
        "## Ana asistan (orkestra şefi)",
        "",
        "- Claude Code'un ana oturumu: isteği okur, departmanı ve sahip birimi belirler, işi o pozisyonun ajanına devreder, sonuçları birleştirir.",
        "- Ajanlar birbirini çağırmaz; departman içindeki sıra raporlama ve sorumluluk düzenidir.",
        "",
        "## Ürün içi görevli pozisyon ajanları",
        "",
        "| Pozisyon ajanı | Ürün içi görev | Departman › pozisyon | Dosya |",
        "|---|---|---|---|",
    ]
    titles = {}
    for d in deps:
        o = d["org"]
        titles[(d["id"], "lider")] = o["leader"]["title"]
        for u in o["units"]:
            titles[(d["id"], u["id"])] = u["leader"]
            for r in u.get("roles", []):
                titles[(d["id"], u["id"] + "/" + r["id"])] = r["title"]
            for tm in u["teams"]:
                ti = u["id"] + "/" + tm["id"]
                if tm.get("manager"):
                    titles[(d["id"], ti)] = tm["manager"]
                for r in tm["roles"]:
                    titles[(d["id"], ti + "/" + r["id"])] = r["title"]
        unit = {u["id"]: u["name"] for u in o["units"]}
        for (did, pid), tt in list(titles.items()):
            if did == d["id"] and pid.split("/")[0] in unit:
                titles[(did, pid)] = unit[pid.split("/")[0]] + " › " + tt
    rows = []
    for key, x in PA.items():
        if not x.get("product"):
            continue
        did, pid = key.split("|", 1)
        tt = titles.get((did, pid), pid)
        where = f"{code[did]} - {next(y['name'] for y in deps if y['id'] == did)} › {tt}"
        rows.append((code[did], f"| {tt.split(' › ')[-1]} | {x['product']['name']} | {where} | KEY:{did}|{pid} |"))
    head += [r[1] for r in sorted(rows)]
    head += ["", "## Departmanlar", "", "Her satır: pozisyon — o pozisyonun ajanı. Girinti raporlama hattını gösterir (birim lideri → ekip yöneticisi → rol)."]
    text = "\n".join(head + body).replace("\n\n\n", "\n\n").rstrip() + "\n"
    for (did, pid), f in files.items():
        text = text.replace(f"KEY:{did}|{pid} |", f"`{f}.md` |")
    open(out, "w", encoding="utf-8").write(text)
    print(f"{stats['pos']} pozisyon ajanı, {n_prod} ürün içi görev → {out}")


if __name__ == "__main__":
    main()
