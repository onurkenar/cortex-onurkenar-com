"""Kurul organizasyon modeli JSON'unu web-proje-gelistirme.html içindeki DATA.boards'a işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/kurul_ekle.py web-proje-gelistirme.html docs/organizasyon/kurul-modeli.json [beklenen-md5]

Girdi (kullanıcının yapi/kurullar/9_Kurul_Organizasyon_Modeli.json'u):
  dokuman{baslik "Şirket — Başlık", surum, olusturma_tarihi, dil, kapsam, nitelik, komite_referans_dosyasi,
  toplam_kurul, referans_komite_sayisi}, yonetisim{ilke, hukuki_ayrim, temsil, yonetim_devri, komite_farki, uyari,
  toplanti_kurali} (→ principles [[etiket, metin]], etiketler PRINCIPLE_NAMES), karar_akis_kodlari[{kod, ad}] (→ flow),
  kurullar[{kod "KRL-NN", ad, kategori, seviye, bagli_organ, kurulus_durumu, amac, organizasyon{baskan_unvani,
  baskan_yardimcisi_unvani, daimi_uyeler_unvanlari[], sekreterya, davetli_uzman, uye_atama, gorev_suresi},
  departman_iliskileri{departman_kodlari["NN"], ilgili_sirketler}, gorevler[], yetkiler{karar_niteligi, kapsam,
  ust_onay, sinirlar[], ozel_not}, toplanti{periyot, gundem_paylasim_is_gunu_once, tutanak_yayin_is_gunu_sonra,
  toplanti_yeter_sayisi, karar_yeter_sayisi, uzaktan_katilim, acil_karar}, karar_akis_kodlari[], kpi[{ad, hesaplama,
  baslangic_hedefi, olcum_sikligi, hedef_tipi}], zorunlu_ciktilar[], iliskili_komite_kodlari["KMT-NN"],
  kontrol_noktalari[]}], entegrasyon{ilgili_komite_json, anahtarlar[], onerilen_varliklar[], erisim, kimliklendirme},
  hiyerarsi[{ust, alt, not}], kaynaklar[{ad, url, ilgili_maddeler?[], not?}].

Çıktı DATA.boards (DATA.committees'in kardeşi): title, company (gösterilmez), version, date, nature, scope (şirket adı
içerdiği için gösterilmez), refCommittees, principles[[etiket, metin]], flow[{id, name}], categories[{id, name}] (ilk
geçiş sırası), integration{entities, access, ids}, hierarchy[{up, down, note}], sources[{name, url, articles?, note?}],
common{…}, items[{id, name, cat, level, organ, up[üst kurul kodları], purpose, chair, vice, members[], secretariat,
depts[departman id], duties[], authority, authNote, period, agendaDays, quorum, majority, kpis[{name, calc, target,
freq}], related[KMT kodları]} + common'a alınamayan alanlar]. HOIST'taki alanlar bütün kurullarda aynıysa `common`a
alınır, değilse her kurulda kalır; arayüz önce kurula, yoksa common'a bakar (krV). KPI hedef tipi de aynı kuralla
common.kpiType olur ya da KPI'da `type` kalır. yetkiler.kapsam amac ile aynı olmalı (iki kez saklanmaz);
entegrasyon.anahtarlar ve ilgili_komite_json yalnız denetlenir (komite dosyası kopyası: komite-modeli.json).

Denetimler (tutmazsa betik durur): bilinmeyen / eksik anahtar yok; metinler boş değil ve kenarında boşluk yok; kodlar
KRL-01'den sırayla, adlar tekil; kurul sayısı toplam_kurul ile aynı; kategori, seviye, kuruluş durumu, ölçüm sıklığı
ve yönetişim anahtarı aşağıdaki sözlüklerde tanımlı; bagli_organ ORGAN_REFS'te tanımlı (→ up; Genel Kurul gibi kurul
dışı makam boş liste), üst kurullar var ve bağlılıkta döngü yok; departman kodları DATA.departments sırasında var
(NN → departman id'si) ve tekrarsız; karar akış kodları karar_akis_kodlari'nda ve aynı sırada; komite kodları KMT-NN,
tekrarsız; DATA.committees varsa orada tanımlı ve referans_komite_sayisi komite sayısıyla aynı (yoksa yalnız biçim
denetlenir — komiteler sonradan işlenirse bu betiği yeniden çalıştırın); baslik'teki şirket adı COMPANY_NAMES'te;
kaynak adresleri https. Hiçbir kurulda olmayan departman ve hiçbir kurula bağlanmamış komite yalnız uyarıdır.
"""
import hashlib
import json
import re
import sys

PRINCIPLE_NAMES = {
    "ilke": "Yönetişim ilkesi",
    "hukuki_ayrim": "Hukuki ayrım",
    "temsil": "Temsil",
    "yonetim_devri": "Yönetim devri",
    "komite_farki": "Kurul ve komite farkı",
    "uyari": "Uyarı",
    "toplanti_kurali": "Toplantı kuralı",
}
CAT_NAMES = {
    "hukuki_yonetim_organi": "Hukuki yönetim organı",
    "icra": "İcra kurulu",
    "koordinasyon": "Koordinasyon kurulu",
    "yonlendirme": "Yönlendirme kurulu",
    "olay_bazli_icra": "Olay bazlı icra kurulu",
    "danisma": "Danışma kurulu",
}
LEVEL_NAMES = {
    "holding": "Holding",
    "sirket": "Grup şirketi",
    "holding_koordinasyon": "Holding koordinasyonu",
    "holding_ortak": "Holding ortak kurulu",
    "holding_ortak_ve_sirket": "Holding ortak ve grup şirketi",
    "holding_ortak_istege_bagli": "Holding ortak kurulu (isteğe bağlı)",
}
STATUS_NAMES = {
    "onerilen_yapi; fiili_hukuki_varlik_ve_atamalar_dogrulanmadi":
        "Önerilen yapı — fiili hukuki varlığı ve atamaları doğrulanmadı",
}
FREQ_NAMES = {"aylik": "Aylık", "uc_aylik": "Üç aylık", "olay_bazli": "Olay bazlı"}
COMPANY_NAMES = {"Rasyo Holding"}
# bagli_organ metni → üst kurul kodları. Genel Kurul kurul değil, dış makamdır (boş liste).
ORGAN_REFS = {
    "Genel Kurul": [],
    "İlgili Şirket Genel Kurulu": [],
    "Holding Yönetim Kurulu / Devredilmiş Yönetim Yetkisi": ["KRL-01"],
    "İlgili Şirket Yönetim Kurulu / Yetkili Yönetici": ["KRL-02"],
    "Holding İcra Kurulu": ["KRL-03"],
    "Holding/Şirket İcra Kurulu; olayın niteliğine göre": ["KRL-03", "KRL-04"],
    "Holding Yönetim Kurulu / İcra Kurulu": ["KRL-01", "KRL-03"],
}
# Bütün kurullarda aynıysa common'a alınan alanlar
HOIST = ["status", "invited", "appoint", "term", "companies", "authority", "approval", "limits", "authNote",
         "agendaDays", "minutesDays", "quorum", "majority", "remote", "urgent", "flow", "outputs", "controls"]
KEYS = {
    "": {"dokuman", "yonetisim", "karar_akis_kodlari", "kurullar", "entegrasyon", "hiyerarsi", "kaynaklar"},
    "dokuman": {"baslik", "surum", "olusturma_tarihi", "dil", "kapsam", "nitelik", "komite_referans_dosyasi",
                "toplam_kurul", "referans_komite_sayisi"},
    "yonetisim": set(PRINCIPLE_NAMES),
    "entegrasyon": {"ilgili_komite_json", "anahtarlar", "onerilen_varliklar", "erisim", "kimliklendirme"},
    "kurul": {"kod", "ad", "kategori", "seviye", "bagli_organ", "kurulus_durumu", "amac", "organizasyon",
              "departman_iliskileri", "gorevler", "yetkiler", "toplanti", "karar_akis_kodlari", "kpi",
              "zorunlu_ciktilar", "iliskili_komite_kodlari", "kontrol_noktalari"},
    "organizasyon": {"baskan_unvani", "baskan_yardimcisi_unvani", "daimi_uyeler_unvanlari", "sekreterya",
                     "davetli_uzman", "uye_atama", "gorev_suresi"},
    "departman_iliskileri": {"departman_kodlari", "ilgili_sirketler"},
    "yetkiler": {"karar_niteligi", "kapsam", "ust_onay", "sinirlar", "ozel_not"},
    "toplanti": {"periyot", "gundem_paylasim_is_gunu_once", "tutanak_yayin_is_gunu_sonra", "toplanti_yeter_sayisi",
                 "karar_yeter_sayisi", "uzaktan_katilim", "acil_karar"},
    "kpi": {"ad", "hesaplama", "baslangic_hedefi", "olcum_sikligi", "hedef_tipi"},
    "karar": {"kod", "ad"},
    "hiyerarsi": {"ust", "alt", "not"},
}


def keys(obj, kind, where):
    extra = set(obj) - KEYS[kind]
    missing = KEYS[kind] - set(obj)
    assert not extra and not missing, f"{where}: tanımsız anahtar {sorted(extra)}, eksik anahtar {sorted(missing)}"


def text(v, where):
    assert isinstance(v, str) and v.strip() == v and v, f"{where}: boş ya da kenarında boşluk olan metin"
    return v


def texts(v, where):
    assert isinstance(v, list) and v, f"{where}: boş liste"
    return [text(x, where) for x in v]


def named(table, key, what, add="Türkçe adını"):
    assert key in table, f"tanımsız {what}: {key!r} — betikteki sözlüğe {add} ekleyin"
    return table[key]


def model_from(src, data):
    depts = data["departments"]
    keys(src, "", "kök")
    doc, gov, integ = src["dokuman"], src["yonetisim"], src["entegrasyon"]
    keys(doc, "dokuman", "dokuman")
    for k in gov:
        named(PRINCIPLE_NAMES, k, "yönetişim anahtarı")
    keys(gov, "yonetisim", "yonetisim")
    keys(integ, "entegrasyon", "entegrasyon")
    company, _, title = text(doc["baslik"], "baslik").partition(" — ")
    if not title:
        company, title = "", company
    assert not company or company in COMPANY_NAMES, f"COMPANY_NAMES: {company}"
    flow = []
    for x in src["karar_akis_kodlari"]:
        keys(x, "karar", "karar_akis_kodlari")
        flow.append({"id": text(x["kod"], "karar kodu"), "name": text(x["ad"], "karar adı")})
    fids = [x["id"] for x in flow]
    assert len(set(fids)) == len(fids), "karar_akis_kodlari tekrarlı"
    dept_ids = [d["id"] for d in depts]
    items, names, cats = [], set(), []
    for n, k in enumerate(src["kurullar"], 1):
        w = k.get("kod", f"#{n}")
        keys(k, "kurul", w)
        assert k["kod"] == f"KRL-{n:02d}", f"{w}: kod sırası (beklenen KRL-{n:02d})"
        name = text(k["ad"], w)
        assert name not in names, f"{w}: ad tekrarlı"
        names.add(name)
        o, r, y, t = k["organizasyon"], k["departman_iliskileri"], k["yetkiler"], k["toplanti"]
        for sub in ("organizasyon", "departman_iliskileri", "yetkiler", "toplanti"):
            keys(k[sub], sub, f"{w}.{sub}")
        cat = k["kategori"]
        if cat not in [c["id"] for c in cats]:
            cats.append({"id": cat, "name": named(CAT_NAMES, cat, "kategori")})
        assert text(y["kapsam"], w) == text(k["amac"], w), f"{w}: yetkiler.kapsam amaçtan farklı"
        dc = r["departman_kodlari"]
        assert dc and len(set(dc)) == len(dc), f"{w}: departman kodları boş ya da tekrarlı"
        for c in dc:
            assert re.fullmatch(r"\d{2}", c) and 1 <= int(c) <= len(dept_ids), f"{w}: departman kodu {c!r}"
        rel = k["iliskili_komite_kodlari"]
        assert len(set(rel)) == len(rel), f"{w}: ilişkili komite tekrarlı"
        for c in rel:
            assert re.fullmatch(r"KMT-\d{2}", c), f"{w}: komite kodu {c!r}"
        fl = k["karar_akis_kodlari"]
        assert all(c in fids for c in fl) and fl == [c for c in fids if c in fl], f"{w}: karar akış kodları"
        for sub in ("gundem_paylasim_is_gunu_once", "tutanak_yayin_is_gunu_sonra"):
            assert isinstance(t[sub], int) and t[sub] >= 0, f"{w}: {sub}"
        kpis = []
        for x in k["kpi"]:
            keys(x, "kpi", f"{w}.kpi")
            kpis.append({"name": text(x["ad"], w), "calc": text(x["hesaplama"], w),
                         "target": text(x["baslangic_hedefi"], w),
                         "freq": named(FREQ_NAMES, x["olcum_sikligi"], "ölçüm sıklığı"),
                         "type": text(x["hedef_tipi"], w)})
        assert kpis, f"{w}: KPI yok"
        items.append({
            "id": k["kod"], "name": name, "cat": cat, "level": named(LEVEL_NAMES, k["seviye"], "seviye"),
            "organ": text(k["bagli_organ"], w),
            "up": named(ORGAN_REFS, k["bagli_organ"], "bağlı organ", "üst kurul kodlarını"),
            "status": named(STATUS_NAMES, k["kurulus_durumu"], "kuruluş durumu"),
            "purpose": k["amac"], "chair": text(o["baskan_unvani"], w), "vice": text(o["baskan_yardimcisi_unvani"], w),
            "members": texts(o["daimi_uyeler_unvanlari"], w), "secretariat": text(o["sekreterya"], w),
            "invited": text(o["davetli_uzman"], w), "appoint": text(o["uye_atama"], w),
            "term": text(o["gorev_suresi"], w),
            "depts": [dept_ids[int(c) - 1] for c in dc], "companies": text(r["ilgili_sirketler"], w),
            "duties": texts(k["gorevler"], w), "authority": text(y["karar_niteligi"], w),
            "approval": text(y["ust_onay"], w), "limits": texts(y["sinirlar"], w), "authNote": text(y["ozel_not"], w),
            "period": text(t["periyot"], w), "agendaDays": t["gundem_paylasim_is_gunu_once"],
            "minutesDays": t["tutanak_yayin_is_gunu_sonra"], "quorum": text(t["toplanti_yeter_sayisi"], w),
            "majority": text(t["karar_yeter_sayisi"], w), "remote": text(t["uzaktan_katilim"], w),
            "urgent": text(t["acil_karar"], w), "flow": fl, "kpis": kpis,
            "outputs": texts(k["zorunlu_ciktilar"], w), "related": rel,
            "controls": texts(k["kontrol_noktalari"], w),
        })
    assert len(items) == doc["toplam_kurul"], f"kurul sayısı {len(items)} ≠ {doc['toplam_kurul']}"
    up = {x["id"]: x["up"] for x in items}
    for x in items:
        for u in x["up"]:
            assert u in up and u != x["id"], f"{x['id']}: üst kurul {u} yok"

    def climb(c, seen=()):
        assert c not in seen, f"kurul bağlılığında döngü: {' → '.join(seen + (c,))}"
        for u in up[c]:
            climb(u, seen + (c,))
    for c in up:
        climb(c)
    kms = data.get("committees")
    known = [x["id"] for x in kms["items"]] if kms else []
    if kms:
        assert doc["referans_komite_sayisi"] == len(known), \
            f"referans_komite_sayisi {doc['referans_komite_sayisi']} ≠ {len(known)} komite"
        for x in items:
            miss = [c for c in x["related"] if c not in known]
            assert not miss, f"{x['id']}: DATA.committees'te olmayan komite {miss}"
    common = {}
    for h in HOIST:
        vals = [json.dumps(x[h], ensure_ascii=False) for x in items]
        if len(set(vals)) == 1:
            common[h] = items[0][h]
            for x in items:
                del x[h]
    types = {x["type"] for b in items for x in b["kpis"]}
    if len(types) == 1:
        common["kpiType"] = types.pop()
        for b in items:
            for x in b["kpis"]:
                del x["type"]
    hier = []
    for h in src["hiyerarsi"]:
        keys(h, "hiyerarsi", "hiyerarsi")
        hier.append({"up": text(h["ust"], "ust"), "down": text(h["alt"], "alt"), "note": text(h["not"], "not")})
    texts(integ["anahtarlar"], "anahtarlar")
    text(integ["ilgili_komite_json"], "ilgili_komite_json")
    sources = []
    for s in src["kaynaklar"]:
        assert {"ad", "url"} <= set(s) <= {"ad", "url", "ilgili_maddeler", "not"}, f"kaynak anahtarları: {sorted(s)}"
        assert text(s["url"], "url").startswith("https://"), f"kaynak adresi https değil: {s['url']}"
        x = {"name": text(s["ad"], "kaynak adı"), "url": s["url"]}
        if "ilgili_maddeler" in s:
            x["articles"] = texts(s["ilgili_maddeler"], "ilgili_maddeler")
        if "not" in s:
            x["note"] = text(s["not"], "kaynak notu")
        sources.append(x)
    unused = [f"{n:02d}" for n, d in enumerate(dept_ids, 1) if not any(d in x["depts"] for x in items)]
    orphan = [c for c in known if not any(c in x["related"] for x in items)]
    return {
        "title": title, "company": company, "version": text(doc["surum"], "surum"),
        "date": text(doc["olusturma_tarihi"], "tarih"), "nature": text(doc["nitelik"], "nitelik"),
        "scope": text(doc["kapsam"], "kapsam"), "refCommittees": doc["referans_komite_sayisi"],
        "principles": [[PRINCIPLE_NAMES[k], text(v, k)] for k, v in gov.items()], "flow": flow, "categories": cats,
        "integration": {"entities": texts(integ["onerilen_varliklar"], "onerilen_varliklar"),
                        "access": text(integ["erisim"], "erisim"), "ids": text(integ["kimliklendirme"], "kimliklendirme")},
        "hierarchy": hier, "sources": sources, "common": common, "items": items,
    }, unused, orphan, bool(kms)


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
    model, unused, orphan, checked = model_from(src, data)
    data["boards"] = model
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    it = model["items"]
    print(f"{len(it)} kurul, {len(model['categories'])} kategori, {len(model['flow'])} karar adımı, "
          f"{sum(len(x['related']) for x in it)} komite bağlantısı "
          f"({'DATA.committees ile denetlendi' if checked else 'DATA.committees yok — yalnız biçim denetlendi'}); "
          f"ortak alanlar: {', '.join(model['common'])}")
    if unused:
        print("Uyarı — hiçbir kurulda olmayan departmanlar: " + ", ".join(unused))
    if orphan:
        print("Uyarı — hiçbir kurula bağlanmamış komiteler: " + ", ".join(orphan))


if __name__ == "__main__":
    main()
