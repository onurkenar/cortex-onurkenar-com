"""MCP bağlantı kataloğunu web-proje-gelistirme.html içindeki DATA.mcpCatalog'a işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/mcp/mcp_ekle.py web-proje-gelistirme.html docs/mcp/mcp-katalog.json \
        docs/mcp/anthropic-dizini.json docs/mcp/dizin-ceviri.json docs/mcp/dizin-aciklama-tr.json [beklenen-md5]

Dört kaynak birleşir:
1. mcp-katalog.json — elle yazılmış Türkçe rehberli kayıtlar (59). Alanlar: title, version, date, intro,
   principles[[etiket, metin]], connTypes[[tür, ad, açıklama]] (remote / local / connector / extension / account),
   categories[{id, name, en, desc, depts[]}] (Anthropic dizini kategorileri; id dizindeki slug, depts kategoriden
   türeyen ilgili departmanlar), items[{id, name, vendor, dir, cats, official, desc, about, scenario, example,
   features[[ad, açıklama]], conn{type, url?, header?, command?, args?, env?, auth}, docs, depts[], risk, notes[]}].
   dir = dizindeki slug ("" = dizinde yok; o zaman cats dolu olmalı, varsa cats boş — kategori dizinden gelir).
2. anthropic-dizini.json — dizin_cek.py çıktısı (İngilizce özgün metin, 1.050 civarı bağlayıcı).
3. dizin-ceviri.json — {slug: Türkçe kısa açıklama}; rehberli kayıtların dizin karşılıkları hariç bütün dizin
   bağlayıcıları için zorunlu. Dizin yeniden çekilince yeni slug'lar için betik durur ve eksikleri listeler.
4. dizin-aciklama-tr.json — {slug: uzun açıklamanın Türkçe çevirisi}; açıklaması olan bütün dizin bağlayıcıları
   (rehberliler dahil) için zorunlu, paragraf ("\n") sayısı özgün metinle aynı olmalı. İngilizce özgün metin
   uygulamaya yazılmaz (dizin sayfasında durur).

Çıktı DATA.mcpCatalog: title, version, date, fetched (dizin çekim tarihi), intro, principles, connTypes,
categories, items[{id, name, vendor, cats, dir, verified, official, desc, text? (Türkçe uzun açıklama), tools[], conn, docs, links[[ad,
adres]], add?, added?, signin?, dirUrl?, depts[], guide?{about, scenario, example, features, notes, risk}}] ada göre
sıralı. Rehberli kaydın kimliği kendi id'sidir (kayıtlı seçimler korunur), diğerlerinin dizin slug'ı. Rehberli kayıtta
bağlantı (conn) sağlayıcı belgesinden doğrulanmış olandır; dizindeki adres farklıysa dirUrl olarak ayrıca gösterilir.
Dizin kaydında conn: remote → {url (ilk adres), auth: oturum açma gerekiyorsa oauth}, extension / account → adressiz.

Denetimler (tutmazsa betik durur): bilinmeyen / eksik anahtar yok; metinler boş değil, kenarında boşluk yok;
kimlikler tekil (rehberli id başka bir dizin slug'ıyla çakışmaz); dir dizinde var ve tek kayda bağlı; kategori ve
departmanlar tanımlı; risk low/medium/high; docs ve url https; header gizli değeri ${…} ile verir; env adları
BÜYÜK_HARF; çeviri her dizin bağlayıcısı için var, nokta ile biter ve fazlası yok; dizin kategorileri tanımlı;
hiçbir metinde "</script" ya da "<!--" yok (DATA tek satırlık <script> içinde; gelirse kaynakta düzeltin).
"""
import hashlib
import json
import re
import sys

TOP = ["title", "version", "date", "intro", "principles", "connTypes", "categories", "items"]
ITEM = ["id", "name", "vendor", "dir", "cats", "official", "desc", "about", "scenario", "example", "features",
        "conn", "docs", "depts", "risk", "notes"]
CONN = {"remote": {"type", "url", "auth", "header"}, "local": {"type", "command", "args", "env", "auth"},
        "connector": {"type", "auth"}}
AUTH = {"oauth", "apikey", "token", "none"}
RISK = {"low", "medium", "high"}
LINKS = {"Documentation": "Belgeler", "Support": "Destek", "Privacy policy": "Gizlilik politikası",
         "Enterprise setup guide": "Kurumsal kurulum rehberi"}
MONTHS = dict(zip(["January", "February", "March", "April", "May", "June", "July", "August", "September",
                   "October", "November", "December"],
                  ["Ocak", "Şubat", "Mart", "Nisan", "Mayıs", "Haziran", "Temmuz", "Ağustos", "Eylül", "Ekim",
                   "Kasım", "Aralık"]))


def txt(v, where):
    assert isinstance(v, str) and v and v == v.strip(), f"{where}: boş ya da kenarında boşluk var"
    return v


def check_curated(src, dept_ids, dir_slugs):
    assert list(src) == TOP, f"üst anahtarlar {list(src)} ≠ {TOP}"
    for k in ("title", "version", "intro"):
        txt(src[k], k)
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", src["date"]), "date YYYY-AA-GG olmalı"
    for p in src["principles"]:
        assert len(p) == 2 and txt(p[0], "principles") and txt(p[1], "principles")
    types = [t[0] for t in src["connTypes"]]
    assert sorted(types) == sorted(list(CONN) + ["extension", "account"]), f"connTypes {types}"
    cats = []
    for c in src["categories"]:
        assert list(c) == ["id", "name", "en", "desc", "depts"], f"kategori anahtarları: {c}"
        assert re.fullmatch(r"[a-z0-9-]+", c["id"]) and c["id"] not in cats, f"kategori: {c['id']}"
        for k in ("name", "en", "desc"):
            txt(c[k], c["id"])
        assert all(d in dept_ids for d in c["depts"]) and len(set(c["depts"])) == len(c["depts"]), c["id"]
        cats.append(c["id"])
    assert "other" in cats, "other kategorisi gerekli"
    ids, dirs = set(), set()
    for x in src["items"]:
        w = x.get("id", "?")
        assert list(x) == ITEM, f"{w}: anahtarlar {list(x)} ≠ {ITEM}"
        assert re.fullmatch(r"[a-z0-9-]+", x["id"]) and x["id"] not in ids, f"kimlik: {w}"
        ids.add(x["id"])
        for k in ("name", "vendor", "desc", "about", "scenario", "example"):
            txt(x[k], f"{w}.{k}")
        if x["dir"]:
            assert x["dir"] in dir_slugs, f"{w}: dizinde olmayan dir {x['dir']}"
            assert x["dir"] not in dirs, f"{w}: dir başka kayda bağlı"
            dirs.add(x["dir"])
            assert x["cats"] == [], f"{w}: dizindeki kaydın kategorisi dizinden gelir, cats boş olmalı"
        else:
            assert x["cats"] and all(c in cats for c in x["cats"]), f"{w}: dizin dışı kayıtta cats gerekli"
        if x["id"] in dir_slugs:
            assert x["dir"] == x["id"], f"{w}: kimlik başka bir dizin bağlayıcısının slug'ıyla çakışıyor"
        assert isinstance(x["official"], bool), f"{w}: official true/false olmalı"
        assert len(x["features"]) >= 2, f"{w}: en az iki özellik"
        names = [f[0] for f in x["features"]]
        assert len(set(names)) == len(names), f"{w}: özellik adı tekrarı"
        for f in x["features"]:
            assert len(f) == 2 and txt(f[0], w) and txt(f[1], w)
        c = x["conn"]
        assert c.get("type") in CONN, f"{w}: bağlantı türü {c.get('type')}"
        assert set(c) <= CONN[c["type"]] and {"type", "auth"} <= set(c), f"{w}: bağlantı anahtarları {list(c)}"
        assert c["auth"] in AUTH, f"{w}: auth {c['auth']}"
        if c["type"] == "remote":
            assert c["url"] == "" or c["url"].startswith("https://"), f"{w}: url https olmalı"
            if "header" in c:
                assert re.fullmatch(r"[A-Za-z-]+: .*\$\{[A-Z0-9_]+\}.*", c["header"]), f"{w}: header ${{…}} ile"
        if c["type"] == "local":
            assert isinstance(c["command"], str) and c["command"] == c["command"].strip(), f"{w}: command"
            assert all(isinstance(a, str) and a for a in c["args"]), f"{w}: args"
            assert all(re.fullmatch(r"[A-Z][A-Z0-9_]*", e) for e in c["env"]), f"{w}: env adı"
            assert c["command"] or not c["args"], f"{w}: komutsuz args"
        assert x["docs"].startswith("https://"), f"{w}: docs https olmalı"
        assert x["depts"] and len(set(x["depts"])) == len(x["depts"]), f"{w}: departman listesi"
        assert all(d in dept_ids for d in x["depts"]), f"{w}: tanımsız departman"
        assert x["risk"] in RISK, f"{w}: risk {x['risk']}"
        for n in x["notes"]:
            txt(n, f"{w}.notes")
    return cats


def build(src, dz, tr, ld, dept_ids):
    D = {x["slug"]: x for x in dz["items"]}
    cats = check_curated(src, dept_ids, set(D))
    cat_depts = {c["id"]: c["depts"] for c in src["categories"]}
    by_dir = {x["dir"]: x for x in src["items"] if x["dir"]}
    need = set(D) - set(by_dir)
    miss, extra = sorted(need - set(tr)), sorted(set(tr) - need)
    assert not miss, f"çevirisi olmayan {len(miss)} bağlayıcı: {', '.join(miss[:30])}"
    assert not extra, f"dizinde olmayan ya da rehberli kayda ait çeviri: {', '.join(extra[:30])}"
    for k, v in tr.items():
        txt(v, f"çeviri {k}")
        assert v[-1] in ".!?…", f"çeviri {k}: noktayla bitmeli"
    need_ld = {s for s, y in D.items() if y["description"]}
    miss, extra = sorted(need_ld - set(ld)), sorted(set(ld) - need_ld)
    assert not miss, f"uzun açıklama çevirisi olmayan {len(miss)} bağlayıcı: {', '.join(miss[:30])}"
    assert not extra, f"dizinde açıklaması olmayan çeviri: {', '.join(extra[:30])}"
    for k, v in ld.items():
        txt(v, f"açıklama {k}")
        assert v.count("\n") == D[k]["description"].count("\n"), f"açıklama {k}: paragraf sayısı özgün metinden farklı"

    def dir_part(y):
        dc = [c[0] for c in y["categories"]] or ["other"]
        bad = [c for c in dc if c not in cats]
        assert not bad, f"{y['slug']}: tanımsız dizin kategorisi {bad} — mcp-katalog.json categories'e ekleyin"
        out = {"cats": dc, "verified": True, "dir": y["slug"],
               "tools": y["tools"],
               "links": [[LINKS.get(a, a), u] for a, u in y["links"] if u.startswith("http")]}
        if y["description"]:
            out["text"] = ld[y["slug"]]
        if y.get("add"):
            out["add"] = y["add"]
        if y.get("added"):
            m, _, yr = y["added"].partition(" ")
            out["added"] = MONTHS.get(m, m) + (" " + yr if yr else "")
        if y.get("signin"):
            out["signin"] = {"Required": "Gerekli", "Not required": "Gerekmez"}.get(y["signin"], y["signin"])
        return out

    items = []
    for x in src["items"]:
        it = {"id": x["id"], "name": x["name"], "vendor": x["vendor"], "cats": x["cats"], "dir": "",
              "verified": False, "official": x["official"], "desc": x["desc"], "tools": [], "conn": x["conn"],
              "docs": x["docs"], "links": [], "depts": x["depts"],
              "guide": {k: x[k] for k in ("about", "scenario", "example", "features", "notes", "risk")}}
        if x["dir"]:
            y = D[x["dir"]]
            it.update(dir_part(y))
            u = x["conn"].get("url", "")
            if y["urls"] and y["urls"][0].rstrip("/") != u.rstrip("/"):
                it["dirUrl"] = y["urls"][0]
        items.append(it)
    for s in sorted(need):
        y = D[s]
        conn = {"type": y["kind"], "auth": "oauth" if y.get("signin") == "Required" else "none"}
        if y["kind"] == "remote":
            conn["url"] = y["urls"][0]
        docs = next((u for a, u in y["links"] if a == "Documentation" and u.startswith("https://")), "") \
            or y.get("makerUrl", "") or "https://claude.com/marketplace/connectors/" + s
        dept = []
        for c in ([c[0] for c in y["categories"]] or ["other"]):
            dept += [d for d in cat_depts.get(c, []) if d not in dept]
        it = {"id": s, "name": y["name"], "vendor": y["maker"] or y["name"], "official": True, "desc": tr[s],
              "conn": conn, "docs": docs, "depts": dept}
        it.update(dir_part(y))
        items.append(it)
    order = ["id", "name", "vendor", "cats", "dir", "verified", "official", "desc", "text", "tools", "conn", "docs",
             "links", "add", "added", "signin", "dirUrl", "depts", "guide"]
    items = [{k: it[k] for k in order if k in it} for it in items]
    items.sort(key=lambda i: (i["name"].casefold(), i["id"]))
    model = {k: src[k] for k in ("title", "version", "date")}
    model["fetched"] = dz["fetched"]
    model.update({k: src[k] for k in ("intro", "principles", "connTypes", "categories")})
    model["items"] = items
    return model


def main():
    html, kpath, dpath, tpath, lpath = sys.argv[1:6]
    want = sys.argv[6] if len(sys.argv) > 6 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    src = json.load(open(kpath, encoding="utf-8"))
    dz = json.load(open(dpath, encoding="utf-8"))
    assert not dz["failed"], "dizin çekiminde hata var; önce dizin_cek.py'yi yeniden çalıştırın"
    tr = json.load(open(tpath, encoding="utf-8"))
    ld = json.load(open(lpath, encoding="utf-8"))
    model = build(src, dz, tr, ld, {d["id"] for d in data["departments"]})
    bad = re.findall(r"</script|<!--", json.dumps(model, ensure_ascii=False), re.I)
    assert not bad, f"MCP verisinde <script> bloğunu bozacak metin var ({len(bad)}): kaynakta düzeltin"
    data["mcpCatalog"] = model
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    it = model["items"]
    by = {}
    for x in it:
        by[x["conn"]["type"]] = by.get(x["conn"]["type"], 0) + 1
    print(f"{len(it)} bağlayıcı ({sum(1 for x in it if 'guide' in x)} Türkçe rehberli, "
          f"{sum(1 for x in it if x['verified'])} Anthropic dizininde), {len(model['categories'])} kategori; "
          + ", ".join(f"{k} {v}" for k, v in sorted(by.items()))
          + f"; MCP verisi {len(json.dumps(model, ensure_ascii=False).encode()) // 1024} KB")


if __name__ == "__main__":
    main()
