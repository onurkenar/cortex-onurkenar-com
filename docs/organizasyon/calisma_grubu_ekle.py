"""Çalışma grubu modeli JSON'unu web-proje-gelistirme.html içindeki DATA.workingGroups'a işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın; komite ve kurul modelleri işlendikten sonra çalıştırın):
    python3 -I docs/organizasyon/calisma_grubu_ekle.py web-proje-gelistirme.html docs/organizasyon/calisma-grubu-modeli.json [beklenen-md5]

Girdi (kullanıcının yapi/çalışma gruplerı/Calisma_Grubu_Organizasyon_Modeli.json'u):
  dokuman{baslik "Şirket Başlık" (şirket adı COMPANY_NAMES'ten biriyle başlar ya da "Şirket — Başlık"), surum,
  olusturma_tarihi, dil, nitelik, toplam_sablon, referans_komite_sayisi, referans_kurul_turu_sayisi},
  yonetisim{temel_ilke, ayrim{kurul, komite, calisma_grubu}, kurulus, uyari, oncelik},
  grup_yasam_dongusu[{kod, ad, cikis_kriteri}], standart_isleyis{grup_kurulus_belgesi_zorunlu_alanlar[],
  roller{sponsor, lider, uye, konu_uzmani, surec_sahibi}, eskalasyon[], karar_kaydi[]},
  calisma_gruplari[{kod "CLG-NN", ad, kategori, tip, sablon_mu (true), durum, olusturma_tetikleyicisi, seviye,
  bagli_kurul_kodlari["KRL-NN"], bagli_komite_kodlari["KMT-NN"], departman_kodlari["NN"], amac,
  organizasyon{sponsor_unvani, calisma_grubu_lideri_unvani, cekirdek_uyeler, onerilen_uye_sayisi{min, max},
  uzman_davetliler, sekreterya, atanma_usulu, raporlama}, gorevler[], karar_yetkisi{grup_ici, ust_onay, yasaklar[],
  imza_yetkisi}, calisma_plani{onerilen_azami_sure_gun, toplanti_sikligi, ilerleme_raporu, gundem_on_hazirlik_is_gunu,
  tutanak_aksiyon_kaydi_is_gunu, kapsam_degisiminde}, teslimatlar[{ad, kabul_kriteri, sorumlu_rol}],
  kpi[{ad, hedef_onerisi, olcum}], cikis_ve_kapanis{kapanis_sartlari[], basarisizlik_durumu, kapanis_otoritesi},
  risk_ve_kontroller[], ornek_is_paketleri[] (teslimat adlarıyla aynı olmalı; iki kez saklanmaz)}],
  entegrasyon{kod_sablonu, iliskiler{…}, veri_varliklari[], durumlar[], onay_kontrolu, guvenlik, dashboard[]}.

Çıktı DATA.workingGroups (DATA.committees ve DATA.boards'un kardeşi): title, company (gösterilmez), version, date,
nature, refCommittees, refBoards, principle, compare[[etiket, metin]] (kurul / komite / çalışma grubu), founding,
warning, priority, lifecycle[{id, name, exit}], charter[], roles[[ad, metin]], escalation[], decisionLog[],
categories[{id, name}] (ilk geçiş sırası; id addan türetilir), integration{codeTemplate, relations[[etiket, değer]],
entities[], statuses[], approval, security, dashboard[]}, common{…}, items[{id, name, cat, purpose, sponsor,
sponsorRef? (sponsor bir komite/kurul başkanı ya da temsilcisiyse o organın kodu), lead, boards[KRL], committees[KMT],
depts[departman id], days, deliverables[ad], kpis[{name, target, calc?}]} + common'a alınamayan alanlar].
HOIST'taki alanlar bütün şablonlarda aynıysa `common`a alınır, değilse her şablonda kalır; arayüz önce şablona, yoksa
common'a bakar (cgV). Bütün şablonlarda aynı olan KPI'lar common.kpis olur; kalan KPI'ların ölçümü hepsinde aynıysa
common.kpiCalc olur. Teslimatların kabul kriteri ve sorumlu rolü şablon içinde tek olmalıdır (accept, owner).

Denetimler (tutmazsa betik durur): bilinmeyen / eksik anahtar yok; metinler boş değil ve kenarında boşluk yok; kodlar
CLG-01'den sırayla, adlar tekil; şablon sayısı toplam_sablon ile aynı; tip, durum, seviye, rol, ayrım, grup durumu
ve ilişki anahtarı aşağıdaki sözlüklerde tanımlı; sablon_mu true; üye sayısı ve süre pozitif tam sayı, min ≤ max;
departman kodları DATA.departments sırasında var (NN → departman id'si) ve tekrarsız; kurul / komite kodları
KRL-NN / KMT-NN, tekrarsız ve DATA.boards / DATA.committees'te tanımlı (o model yoksa yalnız biçim denetlenir —
sonradan işlenirse bu betiği yeniden çalıştırın), referans sayıları model sayılarıyla aynı; eskalasyon metnindeki
kodlar da tanımlı; ornek_is_paketleri teslimat adlarıyla aynı; yaşam döngüsü kodları tekil; sponsor unvanı bir
komite ya da kurul adı içeriyorsa organ tanımlı (tam ad ya da SPONSOR_ALIASES'teki kısa ad) ve şablonun bağlı
komite / kurullarından biri. Hiçbir şablonda olmayan departman / komite / kurul ve ortak KPI ile örtüşebilecek KPI
yalnız uyarıdır.
"""
import hashlib
import json
import re
import sys

COMPANY_NAMES = {"Rasyo Holding"}
TYPE_NAMES = {"gecici_cok_fonksiyonlu": "Geçici, çok fonksiyonlu"}
STATUS_NAMES = {"taslak_sablon": "Taslak şablon"}
LEVEL_NAMES = {"holding_ortak_veya_sirket_bazli": "Holding ortak ya da şirket bazlı"}
COMPARE_NAMES = {"kurul": "Kurul", "komite": "Komite", "calisma_grubu": "Çalışma grubu"}
ROLE_NAMES = {"sponsor": "Sponsor", "lider": "Çalışma grubu lideri", "uye": "Üye", "konu_uzmani": "Konu uzmanı",
              "surec_sahibi": "Süreç sahibi"}
GROUP_STATUS_NAMES = {"taslak": "Taslak", "onay_bekliyor": "Onay bekliyor", "aktif": "Aktif", "askida": "Askıda",
                      "kabul_bekliyor": "Kabul bekliyor", "tamamlandi": "Tamamlandı", "iptal": "İptal"}
RELATION_NAMES = {"sablon": "Şablon", "olusan_grup": "Oluşan grup", "sponsor": "Sponsor", "lider": "Lider",
                  "uyelik": "Üyelik", "komite": "Komite", "kurul": "Kurul", "sirket": "Şirket",
                  "departman": "Departman"}
# Sponsor unvanındaki kısa organ adı → kod (adı komite / kurul modelindeki adla birebir tutmayanlar)
SPONSOR_ALIASES = {
    "Kalite Yönetimi Komitesi": "KMT-14",
    "Müşteri Deneyimi Komitesi": "KMT-19",
    "Veri Analitik ve Yapay Zekâ Komitesi": "KMT-23",
}
# Bütün şablonlarda aynıysa common'a alınan alanlar
HOIST = ["type", "status", "trigger", "level", "core", "size", "invited", "secretariat", "appoint", "reporting",
         "duties", "authority", "approval", "bans", "sign", "days", "meeting", "progress", "agendaDays", "minutesDays",
         "scopeChange", "accept", "owner", "closeReqs", "failure", "closeAuth", "risks"]
KEYS = {
    "": {"dokuman", "yonetisim", "grup_yasam_dongusu", "standart_isleyis", "calisma_gruplari", "entegrasyon"},
    "dokuman": {"baslik", "surum", "olusturma_tarihi", "dil", "nitelik", "toplam_sablon", "referans_komite_sayisi",
                "referans_kurul_turu_sayisi"},
    "yonetisim": {"temel_ilke", "ayrim", "kurulus", "uyari", "oncelik"},
    "ayrim": set(COMPARE_NAMES),
    "evre": {"kod", "ad", "cikis_kriteri"},
    "standart_isleyis": {"grup_kurulus_belgesi_zorunlu_alanlar", "roller", "eskalasyon", "karar_kaydi"},
    "roller": set(ROLE_NAMES),
    "entegrasyon": {"kod_sablonu", "iliskiler", "veri_varliklari", "durumlar", "onay_kontrolu", "guvenlik",
                    "dashboard"},
    "grup": {"kod", "ad", "kategori", "tip", "sablon_mu", "durum", "olusturma_tetikleyicisi", "seviye",
             "bagli_kurul_kodlari", "bagli_komite_kodlari", "departman_kodlari", "amac", "organizasyon", "gorevler",
             "karar_yetkisi", "calisma_plani", "teslimatlar", "kpi", "cikis_ve_kapanis", "risk_ve_kontroller",
             "ornek_is_paketleri"},
    "organizasyon": {"sponsor_unvani", "calisma_grubu_lideri_unvani", "cekirdek_uyeler", "onerilen_uye_sayisi",
                     "uzman_davetliler", "sekreterya", "atanma_usulu", "raporlama"},
    "uye_sayisi": {"min", "max"},
    "karar_yetkisi": {"grup_ici", "ust_onay", "yasaklar", "imza_yetkisi"},
    "calisma_plani": {"onerilen_azami_sure_gun", "toplanti_sikligi", "ilerleme_raporu", "gundem_on_hazirlik_is_gunu",
                      "tutanak_aksiyon_kaydi_is_gunu", "kapsam_degisiminde"},
    "teslimat": {"ad", "kabul_kriteri", "sorumlu_rol"},
    "kpi": {"ad", "hedef_onerisi", "olcum"},
    "cikis_ve_kapanis": {"kapanis_sartlari", "basarisizlik_durumu", "kapanis_otoritesi"},
}
FOLD = str.maketrans("çğıöşüâîûÇĞİÖŞÜÂÎÛ", "cgiosuaiuCGIOSUAIU")


def keys(obj, kind, where):
    assert isinstance(obj, dict), f"{where}: nesne değil"
    extra = set(obj) - KEYS[kind]
    missing = KEYS[kind] - set(obj)
    assert not extra and not missing, f"{where}: tanımsız anahtar {sorted(extra)}, eksik anahtar {sorted(missing)}"


def text(v, where):
    assert isinstance(v, str) and v.strip() == v and v, f"{where}: boş ya da kenarında boşluk olan metin"
    return v


def texts(v, where):
    assert isinstance(v, list) and v, f"{where}: boş liste"
    return [text(x, where) for x in v]


def count(v, where, low=1):
    assert isinstance(v, int) and not isinstance(v, bool) and v >= low, f"{where}: {low} ya da büyük tam sayı değil"
    return v


def named(table, key, what, add="Türkçe adını"):
    assert key in table, f"tanımsız {what}: {key!r} — betikteki sözlüğe {add} ekleyin"
    return table[key]


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.translate(FOLD).lower()).strip("-")


def words(s):
    return set(re.findall(r"\w+", s.lower()))


def codes(v, prefix, known, where):
    assert isinstance(v, list) and len(set(v)) == len(v), f"{where}: {prefix} kodları liste değil ya da tekrarlı"
    for c in v:
        assert re.fullmatch(prefix + r"-\d{2}", c), f"{where}: {prefix} kodu {c!r}"
        assert known is None or c in known, f"{where}: tanımsız {prefix} kodu {c}"
    return v


def model_from(src, data):
    keys(src, "", "kök")
    doc, gov, std, integ = src["dokuman"], src["yonetisim"], src["standart_isleyis"], src["entegrasyon"]
    keys(doc, "dokuman", "dokuman")
    keys(gov, "yonetisim", "yonetisim")
    keys(gov["ayrim"], "ayrim", "yonetisim.ayrim")
    keys(std, "standart_isleyis", "standart_isleyis")
    keys(std["roller"], "roller", "standart_isleyis.roller")
    keys(integ, "entegrasyon", "entegrasyon")
    base = text(doc["baslik"], "baslik")
    company, title = "", base
    if " — " in base:
        company, _, title = base.partition(" — ")
        assert company in COMPANY_NAMES, f"COMPANY_NAMES: {company}"
    else:
        for c in COMPANY_NAMES:
            if base.startswith(c + " "):
                company, title = c, base[len(c) + 1:]
    depts = data["departments"]
    dept_ids = [d["id"] for d in depts]
    kms, krs = data.get("committees"), data.get("boards")
    km_names = {x["id"]: x["name"] for x in kms["items"]} if kms else None
    kr_names = {x["id"]: x["name"] for x in krs["items"]} if krs else None
    if kms:
        assert doc["referans_komite_sayisi"] == len(km_names), \
            f"referans_komite_sayisi {doc['referans_komite_sayisi']} ≠ {len(km_names)} komite"
    if krs:
        assert doc["referans_kurul_turu_sayisi"] == len(kr_names), \
            f"referans_kurul_turu_sayisi {doc['referans_kurul_turu_sayisi']} ≠ {len(kr_names)} kurul"
    organs = dict((v, k) for k, v in list((km_names or {}).items()) + list((kr_names or {}).items()))
    for a, c in SPONSOR_ALIASES.items():
        pool = km_names if c.startswith("KMT") else kr_names
        assert pool is None or c in pool, f"SPONSOR_ALIASES: {c} tanımsız"
        organs.setdefault(a, c)
    lifecycle = []
    for x in src["grup_yasam_dongusu"]:
        keys(x, "evre", "grup_yasam_dongusu")
        lifecycle.append({"id": text(x["kod"], "evre kodu"), "name": text(x["ad"], "evre adı"),
                          "exit": text(x["cikis_kriteri"], "çıkış kriteri")})
    assert lifecycle and len({x["id"] for x in lifecycle}) == len(lifecycle), "yaşam döngüsü kodları boş ya da tekrarlı"
    escalation = texts(std["eskalasyon"], "eskalasyon")
    for e in escalation:
        codes(re.findall(r"KRL-\d{2}", e), "KRL", kr_names, "eskalasyon")
        codes(re.findall(r"KMT-\d{2}", e), "KMT", km_names, "eskalasyon")
    statuses = [named(GROUP_STATUS_NAMES, s, "grup durumu") for s in integ["durumlar"]]
    assert statuses and len(set(statuses)) == len(statuses), "durumlar boş ya da tekrarlı"
    assert integ["iliskiler"], "entegrasyon.iliskiler boş"
    relations = [[named(RELATION_NAMES, k, "ilişki anahtarı"), text(v, k)] for k, v in integ["iliskiler"].items()]
    items, names, cats = [], set(), []
    for n, g in enumerate(src["calisma_gruplari"], 1):
        w = g.get("kod", f"#{n}")
        keys(g, "grup", w)
        assert g["kod"] == f"CLG-{n:02d}", f"{w}: kod sırası (beklenen CLG-{n:02d})"
        name = text(g["ad"], w)
        assert name not in names, f"{w}: ad tekrarlı"
        names.add(name)
        assert g["sablon_mu"] is True, f"{w}: sablon_mu true değil"
        o, y, p, c = g["organizasyon"], g["karar_yetkisi"], g["calisma_plani"], g["cikis_ve_kapanis"]
        for sub in ("organizasyon", "karar_yetkisi", "calisma_plani", "cikis_ve_kapanis"):
            keys(g[sub], sub, f"{w}.{sub}")
        keys(o["onerilen_uye_sayisi"], "uye_sayisi", f"{w}.onerilen_uye_sayisi")
        lo, hi = count(o["onerilen_uye_sayisi"]["min"], w), count(o["onerilen_uye_sayisi"]["max"], w)
        assert lo <= hi, f"{w}: üye sayısı min > max"
        cn = text(g["kategori"], w)
        cid = slug(cn)
        known = {x["id"]: x["name"] for x in cats}
        assert known.setdefault(cid, cn) == cn, f"{w}: {cn} kategori kimliği başka kategoriyle çakışıyor"
        if cid not in [x["id"] for x in cats]:
            cats.append({"id": cid, "name": cn})
        dc = g["departman_kodlari"]
        assert dc and len(set(dc)) == len(dc), f"{w}: departman kodları boş ya da tekrarlı"
        for x in dc:
            assert re.fullmatch(r"\d{2}", x) and 1 <= int(x) <= len(dept_ids), f"{w}: departman kodu {x!r}"
        boards = codes(g["bagli_kurul_kodlari"], "KRL", kr_names, w)
        comms = codes(g["bagli_komite_kodlari"], "KMT", km_names, w)
        assert boards or comms, f"{w}: bağlı kurul ya da komite yok"
        sponsor = text(o["sponsor_unvani"], w)
        ref = next((c2 for nm, c2 in sorted(organs.items(), key=lambda z: -len(z[0])) if nm in sponsor), None)
        if re.search(r"Komitesi|Kurulu", sponsor):
            assert ref or (km_names is None and "Komitesi" in sponsor) or (kr_names is None and "Kurulu" in sponsor), \
                f"{w}: sponsor unvanındaki organ tanımsız ({sponsor}) — adı düzeltin ya da SPONSOR_ALIASES'e ekleyin"
            assert not ref or ref in boards + comms, f"{w}: sponsor organı {ref} şablonun bağlı organlarında yok"
        dl = []
        for x in g["teslimatlar"]:
            keys(x, "teslimat", f"{w}.teslimatlar")
            dl.append((text(x["ad"], w), text(x["kabul_kriteri"], w), text(x["sorumlu_rol"], w)))
        assert dl, f"{w}: teslimat yok"
        assert len({x[1] for x in dl}) == 1 and len({x[2] for x in dl}) == 1, \
            f"{w}: teslimatların kabul kriteri ya da sorumlu rolü farklı — arayüz şablon başına tek değer gösterir"
        assert texts(g["ornek_is_paketleri"], w) == [x[0] for x in dl], f"{w}: ornek_is_paketleri teslimat adlarından farklı"
        kpis = []
        for x in g["kpi"]:
            keys(x, "kpi", f"{w}.kpi")
            kpis.append({"name": text(x["ad"], w), "target": text(x["hedef_onerisi"], w), "calc": text(x["olcum"], w)})
        assert kpis and len({x["name"] for x in kpis}) == len(kpis), f"{w}: KPI yok ya da adı tekrarlı"
        item = {
            "id": g["kod"], "name": name, "cat": cid, "type": named(TYPE_NAMES, g["tip"], "tip"),
            "status": named(STATUS_NAMES, g["durum"], "durum"), "trigger": text(g["olusturma_tetikleyicisi"], w),
            "level": named(LEVEL_NAMES, g["seviye"], "seviye"), "purpose": text(g["amac"], w), "sponsor": sponsor,
            "lead": text(o["calisma_grubu_lideri_unvani"], w), "boards": boards, "committees": comms,
            "depts": [dept_ids[int(x) - 1] for x in dc], "core": text(o["cekirdek_uyeler"], w), "size": [lo, hi],
            "invited": text(o["uzman_davetliler"], w), "secretariat": text(o["sekreterya"], w),
            "appoint": text(o["atanma_usulu"], w), "reporting": text(o["raporlama"], w),
            "duties": texts(g["gorevler"], w), "authority": text(y["grup_ici"], w), "approval": text(y["ust_onay"], w),
            "bans": texts(y["yasaklar"], w), "sign": text(y["imza_yetkisi"], w),
            "days": count(p["onerilen_azami_sure_gun"], w), "meeting": text(p["toplanti_sikligi"], w),
            "progress": text(p["ilerleme_raporu"], w), "agendaDays": count(p["gundem_on_hazirlik_is_gunu"], w, 0),
            "minutesDays": count(p["tutanak_aksiyon_kaydi_is_gunu"], w, 0),
            "scopeChange": text(p["kapsam_degisiminde"], w), "deliverables": [x[0] for x in dl], "accept": dl[0][1],
            "owner": dl[0][2], "kpis": kpis, "closeReqs": texts(c["kapanis_sartlari"], w),
            "failure": text(c["basarisizlik_durumu"], w), "closeAuth": text(c["kapanis_otoritesi"], w),
            "risks": texts(g["risk_ve_kontroller"], w),
        }
        if ref:
            item["sponsorRef"] = ref
        items.append(item)
    assert len(items) == doc["toplam_sablon"], f"şablon sayısı {len(items)} ≠ {doc['toplam_sablon']}"
    common = {}
    for h in HOIST:
        vals = [json.dumps(x[h], ensure_ascii=False) for x in items]
        if len(set(vals)) == 1:
            common[h] = items[0][h]
            for x in items:
                del x[h]
    sig = lambda k: json.dumps(k, ensure_ascii=False, sort_keys=True)
    shared = [k for k in items[0]["kpis"] if all(sig(k) in {sig(z) for z in x["kpis"]} for x in items)]
    if shared:
        common["kpis"] = shared
        for x in items:
            x["kpis"] = [k for k in x["kpis"] if sig(k) not in {sig(z) for z in shared}]
    calcs = {k["calc"] for x in items for k in x["kpis"]}
    if len(calcs) == 1:
        common["kpiCalc"] = calcs.pop()
        for x in items:
            for k in x["kpis"]:
                del k["calc"]
    overlap = [(x["id"], k["name"], s["name"]) for x in items for k in x["kpis"] for s in shared
               if words(k["name"]) < words(s["name"])]
    unused = {
        "departman": [f"{n:02d}" for n, d in enumerate(dept_ids, 1) if not any(d in x["depts"] for x in items)],
        "komite": [c for c in (km_names or {}) if not any(c in x["committees"] for x in items)],
        "kurul": [c for c in (kr_names or {}) if not any(c in x["boards"] for x in items)],
    }
    return {
        "title": title, "company": company, "version": text(doc["surum"], "surum"),
        "date": text(doc["olusturma_tarihi"], "tarih"), "nature": text(doc["nitelik"], "nitelik"),
        "refCommittees": doc["referans_komite_sayisi"], "refBoards": doc["referans_kurul_turu_sayisi"],
        "principle": text(gov["temel_ilke"], "temel_ilke"),
        "compare": [[COMPARE_NAMES[k], text(v, k)] for k, v in gov["ayrim"].items()],
        "founding": text(gov["kurulus"], "kurulus"), "warning": text(gov["uyari"], "uyari"),
        "priority": text(gov["oncelik"], "oncelik"), "lifecycle": lifecycle,
        "charter": texts(std["grup_kurulus_belgesi_zorunlu_alanlar"], "zorunlu alanlar"),
        "roles": [[ROLE_NAMES[k], text(v, k)] for k, v in std["roller"].items()], "escalation": escalation,
        "decisionLog": texts(std["karar_kaydi"], "karar_kaydi"), "categories": cats,
        "integration": {"codeTemplate": text(integ["kod_sablonu"], "kod_sablonu"), "relations": relations,
                        "entities": texts(integ["veri_varliklari"], "veri_varliklari"), "statuses": statuses,
                        "approval": text(integ["onay_kontrolu"], "onay_kontrolu"),
                        "security": text(integ["guvenlik"], "guvenlik"),
                        "dashboard": texts(integ["dashboard"], "dashboard")},
        "common": common, "items": items,
    }, unused, overlap, (kms is not None, krs is not None)


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
    src = json.load(open(jpath, encoding="utf-8"))
    model, unused, overlap, (km_ok, kr_ok) = model_from(src, data)
    data["workingGroups"] = model
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    it = model["items"]
    chk = [n for n, ok in (("DATA.committees", km_ok), ("DATA.boards", kr_ok)) if ok]
    print(f"{len(it)} şablon, {len(model['categories'])} kategori, {len(model['lifecycle'])} yaşam döngüsü evresi, "
          f"{sum(len(x['committees']) for x in it)} komite ve {sum(len(x['boards']) for x in it)} kurul bağlantısı "
          f"({' ve '.join(chk) + ' ile denetlendi' if chk else 'komite / kurul modeli yok — yalnız biçim denetlendi'}); "
          f"sponsoru organ olan: {sum(1 for x in it if 'sponsorRef' in x)}; ortak alanlar: {', '.join(model['common'])}")
    for k, v in unused.items():
        if v:
            print(f"Uyarı — hiçbir şablonda olmayan {k}: " + ", ".join(v))
    if overlap:
        print("Uyarı — ortak KPI ile örtüşebilecek KPI: " + "; ".join(f"{a} “{b}” ⊂ “{c}”" for a, b, c in overlap))


if __name__ == "__main__":
    main()
