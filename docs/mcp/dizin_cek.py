"""Anthropic Connectors Directory'deki bütün bağlayıcıları claude.com'dan çekip JSON'a yazar.

Kullanım (proje kökünden; ağ erişimi gerekir, ~1.050 sayfa, birkaç dakika):
    python3 -I docs/mcp/dizin_cek.py docs/mcp/anthropic-dizini.json [eşzamanlı-istek=6]

Kaynak: https://claude.com/sitemap.xml içindeki /marketplace/connectors/<slug> adresleri (robots.txt: Allow /).
Resmî bir listeleme API'si yoktur; her bağlayıcının herkese açık sayfası okunur. Çıktı İngilizce özgün metindir;
Türkçe çeviri ve uygulamaya işleme ayrı adımdır (mcp_ekle.py).

Çıktı: {source, fetched (YYYY-AA-GG), count, failed[], items[{slug, name, verified, subtitle, categories[],
maker, makerUrl?, signin, added, kind (remote = uzak adres / extension = Claude Desktop
uzantısı / account = adres hesaba özel, claude.ai'dan eklenir), add? (claude.ai dizin bağlantısı), urls[], links[[ad, adres]], description, tools[]}]} — slug sırasıyla.
Sayfa yapısı değişirse (ad bulunamazsa) betik o sayfayı failed'a yazar; failed boş değilse
çıkış kodu 1'dir ve dosya yine yazılır (inceleyip yeniden çalıştırın).
"""
import concurrent.futures as cf
import datetime
import html
import json
import re
import sys
import time
import urllib.request
from html.parser import HTMLParser

SITEMAP = "https://claude.com/sitemap.xml"
UA = "Mozilla/5.0 (WP-OnKe connector catalog; +https://claude.com/robots.txt)"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr", "path"}


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en"})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read().decode("utf-8", "replace")
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2 * (i + 1))


class Node:
    __slots__ = ("tag", "cls", "attrs", "kids", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag, self.attrs, self.parent, self.kids = tag, dict(attrs), parent, []
        self.cls = self.attrs.get("class") or ""

    def text(self):
        out = []
        for k in self.kids:
            out.append(k if isinstance(k, str) else k.text())
        return "".join(out)

    def find(self, pred):
        for k in self.kids:
            if isinstance(k, Node):
                if pred(k):
                    yield k
                yield from k.find(pred)


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = self.cur = Node("root", [], None)
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style", "svg"):
            self.skip += 1
            return
        if self.skip:
            return
        n = Node(tag, attrs, self.cur)
        self.cur.kids.append(n)
        if tag not in VOID:
            self.cur = n

    def handle_endtag(self, tag):
        if tag in ("script", "style", "svg"):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        n = self.cur
        while n is not self.root and n.tag != tag:
            n = n.parent
        if n is not self.root:
            self.cur = n.parent

    def handle_data(self, d):
        if not self.skip:
            self.cur.kids.append(d)


def cls(name):
    return lambda n: re.search(r"(^|\s)ConnectorDetail-module[\w-]*__" + name + r"(\s|$)", n.cls)


def clean(t):
    return re.sub(r"\s+", " ", html.unescape(t or "")).strip()


def parse(slug, page):
    tr = Tree()
    tr.feed(page)
    root = tr.root
    main = next(root.find(cls("article")), root)
    h1 = next(main.find(lambda n: n.tag == "h1"), None)
    sub = next(main.find(cls("subheading")), None)
    title_row = next(main.find(cls("titleRow")), None)
    it = {"slug": slug, "name": clean(h1.text()) if h1 else "",
          "verified": bool(title_row and next(title_row.find(cls("verified")), None)),
          "subtitle": clean(sub.text()) if sub else "", "categories": [], "maker": "", "signin": "", "added": "",
          "urls": [], "links": [], "description": "", "tools": []}
    for li in root.find(lambda n: re.search(r"DetailSidebar-module[\w-]*__item(\s|$)", n.cls)):
        lab = next(li.find(lambda n: re.search(r"DetailSidebar-module[\w-]*__label(\s|$)", n.cls)), None)
        val = next(li.find(lambda n: re.search(r"DetailSidebar-module[\w-]*__value(\s|$)", n.cls)), None)
        if not lab or not val:
            continue
        label = clean(lab.text()).lower()
        if label.startswith("categor"):
            it["categories"] = [[re.sub(r".*categories=", "", a.attrs.get("href", "")), clean(a.text())]
                                for a in val.find(lambda n: n.tag == "a")]
        elif label.startswith("made by"):
            a = next(val.find(lambda n: n.tag == "a"), None)
            it["maker"] = clean(val.text()).replace("(opens in new tab)", "").strip()
            if a and a.attrs.get("href", "").startswith("http"):
                it["makerUrl"] = a.attrs["href"]
        elif label.startswith("sign"):
            it["signin"] = clean(val.text())
        elif label.startswith("added"):
            it["added"] = clean(val.text())
    for g in main.find(cls("sidebarGroup")):
        for f in [g] + list(g.find(cls("fact"))):
            lab = next(f.find(cls("sidebarLabel")), None)
            if not lab:
                continue
            label = clean(lab.text()).lower()
            box = next(f.find(cls("sidebarContent")), None) or f
            if "url" in label:
                it["urls"] = [clean(c.text()) for c in box.find(cls("copyPillText"))]
            elif label == "more":
                it["links"] = [[clean(a.text()).replace("(opens in new tab)", "").strip(), a.attrs.get("href", "")] for a in box.find(lambda n: n.tag == "a")
                               if a.attrs.get("href")]
    d = next(main.find(cls("description")), None)
    if d:
        paras = [clean(p.text()) for p in d.find(lambda n: n.tag in ("p", "li"))]
        it["description"] = "\n".join(p for p in paras if p) or clean(d.text())
    it["tools"] = [clean(p.text()) for p in main.find(cls("toolPill")) if clean(p.text())]
    # yedek: araç listesi yalnız gömülü veride olabilir
    if not it["tools"]:
        m = re.search(r'\{\\"tools\\":\[(.*?)\]\}', page)
        if m:
            it["tools"] = json.loads("[" + m.group(1).replace('\\"', '"') + "]")
    it["urls"] = list(dict.fromkeys(u for u in it["urls"] if u))
    it["kind"] = "remote" if it["urls"] else "extension" if "/api/dxt/extensions/" in page else "account"
    add = next(main.find(lambda n: n.tag == "a" and clean(n.text()).startswith("Add to Claude")), None)
    if add and add.attrs.get("href", "").startswith("https://claude.ai/"):
        it["add"] = add.attrs["href"]
    if not it.get("makerUrl"):
        it.pop("makerUrl", None)
    return it


def main():
    out = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    sm = get(SITEMAP)
    urls = sorted(set(re.findall(r"<loc>(https://claude\.com/marketplace/connectors/[a-z0-9-]+)</loc>", sm)))
    assert len(urls) > 100, f"site haritasında az bağlayıcı: {len(urls)}"
    items, failed = [], []

    def one(u):
        slug = u.rsplit("/", 1)[1]
        try:
            it = parse(slug, get(u))
            if not it["name"]:
                return None, f"{slug}: ad bulunamadı"
            return it, None
        except Exception as e:  # ağ ya da ayrıştırma hatası
            return None, f"{slug}: {e}"

    with cf.ThreadPoolExecutor(workers) as ex:
        for k, (it, err) in enumerate(ex.map(one, urls), 1):
            (items.append(it) if it else failed.append(err))
            if k % 100 == 0:
                print(f"{k}/{len(urls)}", file=sys.stderr)
    items.sort(key=lambda x: x["slug"])
    res = {"source": SITEMAP, "fetched": datetime.date.today().isoformat(), "count": len(items),
           "failed": failed, "items": items}
    json.dump(res, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cats = {}
    for x in items:
        for c in x["categories"]:
            cats[c[1]] = cats.get(c[1], 0) + 1
    print(f"{len(items)} bağlayıcı ({sum(x['verified'] for x in items)} doğrulanmış, "
          f"{sum(x['kind'] == 'extension' for x in items)} masaüstü uzantısı, {sum(x['kind'] == 'account' for x in items)} hesaba özel), "
          f"{len(failed)} hata; "
          f"{len(cats)} kategori: " + ", ".join(f"{c} {n}" for c, n in sorted(cats.items(), key=lambda z: -z[1])))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
