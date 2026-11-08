"""Anthropic skill'lerini ve claude.ai Skill Dizini'ni web-proje-gelistirme.html'deki DATA'ya işler.

Kullanım (proje kökünden):
    python3 -I docs/skills/skill_ekle.py web-proje-gelistirme.html

Kaynaklar (bu klasörde; hepsi elle ya da betikle üretilir, uygulama yalnız buradan beslenir):
  anthropic/kaynak.json      github.com/anthropics/skills'in çekildiği commit, skill başına lisans, metin dosyaları
                             ve gömülmeyen ikili dosyalar ([yol, bayt]).
  anthropic/kaynak/<skill>/  Apache 2.0 lisanslı skill'lerin bütün METİN dosyaları, özgün haliyle (SKILL.md dahil).
                             Word / PDF / PowerPoint / Excel skill'leri (docx, pdf, pptx, xlsx) özel lisanslıdır
                             (kopyalama, saklama ve türev eser yasak): içerikleri burada yoktur, uygulamada yalnız
                             kendi yazdığımız Türkçe tanıtım ve kurulum komutuyla "başvuru" kaydı olarak durur.
  anthropic/tr/<skill>.md    SKILL.md gövdesinin (frontmatter hariç) Türkçe çevirisi — kod blokları, satır içi kod
                             ve başlıklar özgün metinle aynı olmalı (betik denetler).
  anthropic/tr/<skill>.json  {name, desc, trigger, scenario, example}: trigger = frontmatter description'ın çevirisi
                             (SKILL.md'ye description olarak yazılır), desc = kart açıklaması.
  anthropic/meta.json        kategori, sahip pozisyon, risk; özel lisanslı dört skill'in Türkçe tanıtımı; kurulum.
  dizin/claude-dizini.json   claude.ai › Customize › Skills › Discover dizini (dizin/dizin_cek.js ile çekilir).
  dizin/ceviri.json          {sha1(metin)[:12]: Türkçe} — eklenti açıklamalarının hepsi ve Anthropic, iş ortağı,
                             Knowledge Work eklentilerindeki skill açıklamaları. Topluluk skill'leri ve bütün
                             komut / alt ajan açıklamaları şimdilik İngilizce (aşamalı çeviri: yeni çeviri bu
                             dosyaya eklenir, betik bulduğunu Türkçe yazar).
  eslesme.json               Skill Kütüphanesi'ndeki proje skill'leri ve Anthropic GitHub skill'lerinin dizindeki
                             karşılıkları {eski kimlik: {plugin: eklenti id, skill: skill adı}} (kullanıcı onayı 2026-11-01).
  pozisyon-eslesme.json      skill → pozisyon ajanı eşleştirmesi {skill kimliği: {pos: ["departman|pozisyon", …],
                             neden}} (2026-11-01, kullanıcı isteği; kapsam: proje + Anthropic GitHub skill'leri ve Anthropic,
                             Knowledge Work eklentilerindeki dizin skill'leri). Katalog skill'inde positions'a yazılır; dizin
                             skill'inde DATA.skillPositions {kimlik: ["departman|pozisyon", …]}. Pozisyonun ajanı projeye
                             eklenince eşlenen skill'ler ona bağlanır.
  dizin/meta.json            57 kategorinin Türkçe adı ve ilgili departmanları, yayıncı türleri, güven uyarısı.

Çıktı:
  DATA.skillCatalog   Anthropic skill'leri (src.repo == "anthropics/skills") her çalıştırmada silinip yeniden
                      eklenir; diğer katalog skill'lerine dokunulmaz. Alanlar: id, cat, name, desc, scenario,
                      example, trigger, body (Türkçe Markdown), md:true, tools:[], files [[yol, içerik]],
                      bins [[yol, bayt, GitHub adresi]], src{org, repo, path, url, commit, date, license, lic},
                      owner, risk; özel lisanslıda body / files yerine ref:true ve install.
  DATA.skillDirectory {title, intro, fetched, source, trust, tiers, cats[{id,name,en,n,depts}], items[...]} —
                      öğe: id, n (eklenti adı), mk (pazaryeri), t (görünen ad), a (yayıncı), tier, cats,
                      ins (kurulum), v (sürüm), c / u (eklenme / güncelleme tarihi), up [depo, yol], d (Türkçe
                      açıklama), sk [[ad, açıklama, 1 = Türkçe / 0 = İngilizce]], cm / ag [[ad, açıklama]] (İngilizce),
                      mcp [[ad, tür, adres ya da komut]], hk (hook var), depts (kategoriden). Kurulum sayısına göre
                      sıralı.
HTML güvenliği: DATA tek satırlık <script> içindedir; metinde "</" ya da "<!--" geçerse betik erken kapanır. Anthropic
skill'lerinin gövde ve dosyalarında "<" ile sonraki "/" ya da "!" arasına NUL (\u0000) konur (guard); uygulama
açılışta kaldırır (skUnguard). Dizin metinlerinde </script ya da <!-- bulunursa betik durur.
Eşleştirme (eslesme.json): eşleşen katalog skill'inin kimliği "dz:<eklenti id>/<skill adı>" olur; dir:true, plug,
slug (dosya adı = dizindeki skill adı), ddesc / dtr (dizindeki açıklama, Türkçe mi) ve legacy (eski kimlik) eklenir;
ad, açıklama, talimat, dosyalar, pozisyonlar, sahip ve risk korunur. DATA.skillLegacy = {eski: yeni}; positionAgents'taki
skills ve product.skills listeleri yeni kimliklere çevrilir. Eski kimlik bir sonraki çalıştırmada legacy'den okunur.
Denetimler: kaynak commit / lisans; çeviride kod bloğu, satır içi kod ve başlık eşleşmesi; sahip pozisyonların
şemada bulunması; dizinde bilinmeyen kategori ya da yayıncı türü; eksik çeviri (eklenti açıklaması ve topluluk dışı
skill açıklaması zorunlu). Herhangi biri tutmazsa betik durur, HTML'e yazmaz. DATA dışında HTML değişmez.
Departman listesi ya da şema değişirse yeniden çalıştırın (sahip pozisyon ve departman denetimi).
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROP = {"docx", "pdf", "pptx", "xlsx"}
MARK = "const DATA="


def fail(msg):
    sys.exit("DURDU: " + msg)


def load(p):
    with open(os.path.join(HERE, p), encoding="utf-8") as f:
        return json.load(f)


def h12(t):
    return hashlib.sha1(t.encode()).hexdigest()[:12]


def positions(d):
    """dpPos ile aynı kimlik kuralları (yaklaşık): lider, ofis, kurul…, birim, birim/ekip, birim/rol, birim/ekip/rol."""
    o = d.get("org") or {}
    P = {"lider"}
    if o.get("office"):
        P.add("ofis")
    if o.get("board"):
        P.add("kurul")
        P.update("kurul/" + r["id"] for r in o["board"].get("roles", []))
    P.update("lider/" + a["id"] for a in o.get("aides", []))
    P.update("matris/" + m["id"] for m in o.get("matrix", []))
    for u in o.get("units", []):
        P.add(u["id"])
        P.update(u["id"] + "/" + r["id"] for r in u.get("roles", []))
        for t in u.get("teams", []):
            P.add(u["id"] + "/" + t["id"])
            P.update(u["id"] + "/" + t["id"] + "/" + r["id"] for r in t.get("roles", []))
    return P


def guard(t):
    return re.sub(r"<([/!])", "<\u0000\\1", t)


def md_parts(s):
    nocode = re.sub(r"```.*?```", "", s, flags=re.S)
    return (re.findall(r"```.*?```", s, re.S),
            sorted(re.findall(r"(?<!`)`[^`\n]+`(?!`)", nocode)),
            [l.split(" ")[0] for l in nocode.split("\n") if re.match(r"#{1,6} ", l)])


def anthropic(depts):
    K, M = load("anthropic/kaynak.json"), load("anthropic/meta.json")
    if not re.fullmatch(r"[0-9a-f]{40}", K["commit"]):
        fail("kaynak.json commit geçersiz")
    if set(K["skills"]) != set(M["skills"]):
        fail("kaynak.json ile meta.json skill listesi farklı: %s" % sorted(set(K["skills"]) ^ set(M["skills"])))
    raw = "https://raw.githubusercontent.com/%s/%s/skills/" % (K["repo"], K["commit"])
    out = []
    for sid, m in M["skills"].items():
        k = K["skills"][sid]
        if m["cat"] not in M["cats"]:
            fail(sid + ": bilinmeyen kategori " + m["cat"])
        if m.get("risk") not in ("low", "medium", "high"):
            fail(sid + ": risk")
        o = m["owner"]
        if o["dept"] not in depts or o["pos"] not in depts[o["dept"]]:
            fail("%s: sahip pozisyonu şemada yok: %s › %s" % (sid, o["dept"], o["pos"]))
        src = {"org": "Anthropic", "repo": K["repo"], "path": "skills/" + sid,
               "url": "%s/tree/%s/skills/%s" % (K["url"], K["commit"], sid), "commit": K["commit"],
               "date": K["date"], "license": k["license"], "lic": k.get("licLine")}
        x = {"id": sid, "cat": M["cats"][m["cat"]]}
        if sid in PROP:
            if k["license"] != "Proprietary":
                fail(sid + ": özel lisans bekleniyordu")
            x.update({"name": m["name"], "desc": m["desc"], "scenario": m["scenario"], "example": m["example"],
                      "ref": True, "tools": [], "install": M["install"]["document"], "src": src})
        else:
            if k["license"] != "Apache-2.0":
                fail(sid + ": lisans Apache-2.0 değil")
            d = os.path.join(HERE, "anthropic/kaynak", sid)
            orig = open(os.path.join(d, "SKILL.md"), encoding="utf-8").read()
            body = re.sub(r"^---\n.*?\n---\n", "", orig, count=1, flags=re.S)
            tr = open(os.path.join(HERE, "anthropic/tr", sid + ".md"), encoding="utf-8").read()
            if md_parts(body) != md_parts(tr):
                fail(sid + ": çeviride kod bloğu / satır içi kod / başlık özgün metinle tutmuyor")
            j = load("anthropic/tr/%s.json" % sid)
            if sorted(j) != ["desc", "example", "name", "scenario", "trigger"] or not all(j.values()):
                fail(sid + ": tr json alanları eksik")
            files = []
            for rel in k["files"]:
                if rel == "SKILL.md":
                    continue
                files.append([rel, open(os.path.join(d, rel), encoding="utf-8").read()])
            have = sorted(os.path.relpath(os.path.join(r, f), d) for r, _, fs in os.walk(d) for f in fs)
            if have != sorted(k["files"]):
                fail(sid + ": kaynak klasörü kaynak.json'daki dosya listesiyle tutmuyor")
            x.update({"name": j["name"], "desc": j["desc"], "scenario": j["scenario"], "example": j["example"],
                      "trigger": j["trigger"], "body": guard(tr.strip("\n") + "\n"), "md": True, "tools": [],
                      "files": [[p, guard(c)] for p, c in files], "bins": [[p, n, raw + sid + "/" + p] for p, n in k["binaries"]],
                      "src": src})
        x.update({"owner": o, "risk": m["risk"]})
        out.append(x)
    return out


def directory(depts):
    S, T, M = load("dizin/claude-dizini.json"), load("dizin/ceviri.json"), load("dizin/meta.json")
    facets = [f["key"] for f in S["facets"]]
    if set(facets) != set(M["cats"]):
        fail("dizin kategorileri meta.json ile tutmuyor: %s" % sorted(set(facets) ^ set(M["cats"])))
    for k, (_, ds) in M["cats"].items():
        bad = [d for d in ds if d not in depts]
        if bad:
            fail("kategori %s: bilinmeyen departman %s" % (k, bad))
    miss = []

    def tr(t, need):
        t = (t or "").strip()
        if not t:
            return "", 1
        v = T.get(h12(t))
        if v:
            return v, 1
        if need:
            miss.append(t[:80])
        return t, 0

    def short(n, plug):
        return n.split(":", 1)[1] if n.startswith(plug + ":") else n

    items = []
    for x in S["items"]:
        if x["tier"] not in M["tiers"]:
            fail("bilinmeyen yayıncı türü: %s (%s)" % (x["tier"], x["display_name"]))
        for c in x["categories"]:
            if c not in M["cats"]:
                fail("bilinmeyen kategori: " + c)
        comm = x["tier"] == "community"
        d, _ = tr(x["description"], True)
        dp = []
        for c in x["categories"]:
            for v in M["cats"][c][1]:
                if v not in dp:
                    dp.append(v)
        o = {"id": x["id"], "n": x["name"], "mk": x["marketplace_name"], "t": x["display_name"] or x["name"],
             "a": x["author"] or "", "tier": x["tier"], "cats": x["categories"], "ins": x["install_count"] or 0,
             "v": x["version"] or "", "c": (x["created_at"] or "")[:10], "u": (x["updated_at"] or "")[:10], "d": d,
             "sk": [[s["display_name"] or short(s["name"], x["name"])] + list(tr(s["description"], not comm))
                    for s in x["skills"]],
             "cm": [[short(c["name"] or "", x["name"]), (c["description"] or "").strip()] for c in x["commands"]],
             "ag": [[short(a["name"] or "", x["name"]), (a["description"] or "").strip()] for a in x["agents"]],
             "mcp": [[m["key"], m["type"] or ("stdio" if m["command"] else ""),
                      m["url"] or " ".join([m["command"] or ""] + (m["args"] or [])).strip()] for m in x["mcp"]],
             "depts": dp[:3]}
        if x["upstream"] and x["upstream"].get("repo_url"):
            o["up"] = [x["upstream"]["repo_url"], x["upstream"].get("plugin_path") or ""]
        if x["hooks"]:
            o["hk"] = 1
        items.append(o)
    if miss:
        fail("%d metnin çevirisi eksik (ilk: %s)" % (len(miss), miss[0]))
    if re.search(r"</script|<!--", json.dumps(items, ensure_ascii=False), re.I):
        fail("dizin metninde </script ya da <!-- var (DATA <script> içinde betiği kapatır)")
    items.sort(key=lambda o: (-o["ins"], o["t"].lower()))
    cats = [{"id": f["key"], "name": M["cats"][f["key"]][0], "en": f["key"].replace("-", " "), "n": f["count"],
             "depts": M["cats"][f["key"]][1]} for f in S["facets"]]
    return {"title": M["title"], "intro": M["intro"], "fetched": S["fetched"], "source": S["source"],
            "trust": M["trust"], "tiers": M["tiers"], "cats": cats, "items": items}


def link(D):
    E = load("eslesme.json")["map"]
    sk = {o["id"]: o for o in D["skillDirectory"]["items"]}
    legacy, done = {}, set()
    for x in D["skillCatalog"]:
        old = x.get("legacy") or x["id"]
        m = E.get(old)
        if not m:
            continue
        p = sk.get(m["plugin"])
        t = p and next((s for s in p["sk"] if s[0] == m["skill"]), None)
        if not t:
            fail("eşleştirme bulunamadı: %s → %s / %s" % (old, m["plugin"], m["skill"]))
        new = "dz:%s/%s" % (m["plugin"], m["skill"])
        x.update({"id": new, "legacy": old, "dir": True, "plug": m["plugin"], "slug": m["skill"], "ddesc": t[1],
                  "dtr": t[2]})
        legacy[old] = new
        done.add(old)
    miss = sorted(set(E) - done)
    if miss:
        fail("eşleştirmedeki skill katalogda yok: %s" % miss)
    ids = [x["id"] for x in D["skillCatalog"]]
    if len(ids) != len(set(ids)):
        fail("eşleştirme sonrası aynı kimlikli iki skill var")
    for v in D["positionAgents"].values():
        for o in (v, v.get("product") or {}):
            if o.get("skills"):
                o["skills"] = list(dict.fromkeys(legacy.get(k, k) for k in o["skills"]))
    D["skillLegacy"] = legacy
    return legacy


def place(D, depts):
    M = load("pozisyon-eslesme.json")["map"]
    cat = {x["id"]: x for x in D["skillCatalog"]}
    dz = {"dz:%s/%s" % (o["id"], s[0]) for o in D["skillDirectory"]["items"] for s in o["sk"]}
    bad, out = [], {}
    for sid, v in M.items():
        P = []
        for k in v.get("pos") or []:
            d, _, q = k.partition("|")
            if d not in depts or q not in depts[d]:
                bad.append("%s → %s" % (sid, k))
            elif k not in P:
                P.append(k)
        if sid in cat:
            x = cat[sid]
            have = ["%s|%s" % (p["dept"], p["pos"]) for p in x.get("positions") or []]
            x["positions"] = [{"dept": k.partition("|")[0], "pos": k.partition("|")[2]} for k in dict.fromkeys(have + P)]
            if not x["positions"]:
                del x["positions"]
        elif sid in dz:
            if P:
                out[sid] = P
        else:
            bad.append("bilinmeyen skill: " + sid)
    if bad:
        fail("pozisyon eşleştirmesinde %d hata (ilk: %s)" % (len(bad), bad[0]))
    D["skillPositions"] = out
    return sum(1 for x in D["skillCatalog"] if x.get("positions")), len(out)


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    path = sys.argv[1]
    html = open(path, encoding="utf-8").read()
    if html.count(MARK) != 1:
        fail("DATA satırı bulunamadı")
    k = html.index(MARK) + len(MARK)
    D, e = json.JSONDecoder().raw_decode(html[k:])
    if json.dumps(D, ensure_ascii=False) != html[k:k + e]:
        fail("DATA serileştirmesi birebir değil")
    depts = {d["id"]: positions(d) for d in D["departments"]}
    A = anthropic(depts)
    ids = {x["id"] for x in A}
    keep = [x for x in D["skillCatalog"] if (x.get("src") or {}).get("repo") != "anthropics/skills"]
    clash = [x["id"] for x in keep if x["id"] in ids]
    if clash:
        fail("katalogda aynı kimlikli skill var: %s" % clash)
    D["skillCatalog"] = keep + A
    D["skillDirectory"] = directory(depts)
    L = link(D)
    PC, PD = place(D, depts)
    new = html[:k] + json.dumps(D, ensure_ascii=False) + html[k + e:]
    if re.search(r"</script|<!--", json.dumps(D["skillCatalog"], ensure_ascii=False), re.I):
        fail("skillCatalog'da korunmamış </script ya da <!-- kaldı")
    open(path, "w", encoding="utf-8").write(new)
    sd = D["skillDirectory"]
    print("Anthropic skill: %d (%d gömülü, %d başvuru) · dizin: %d eklenti, %d skill (%d Türkçe), %d kategori"
          % (len(A), sum(1 for x in A if x.get("md")), sum(1 for x in A if x.get("ref")), len(sd["items"]),
             sum(len(o["sk"]) for o in sd["items"]), sum(s[2] for o in sd["items"] for s in o["sk"]),
             len(sd["cats"])))
    print("Dizinle eşleşen katalog skill'i: %d · pozisyona bağlı: %d katalog, %d dizin skill'i" % (len(L), PC, PD))
    print("HTML: %d → %d bayt" % (len(html.encode()), len(new.encode())))


if __name__ == "__main__":
    main()
