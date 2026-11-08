"""Komite modeli JSON'unu web-proje-gelistirme.html içindeki DATA.committees'e işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/komite_ekle.py web-proje-gelistirme.html docs/organizasyon/komite-modeli.json [beklenen-md5]

Girdi (kullanıcının yapi/komite/24_Komite_Organizasyon_Modeli.json'u):
  dokuman{baslik "Şirket — Başlık", surum, olusturma_tarihi, dil, nitelik, kapsam, toplam_komite, pilot_komite,
  ikinci_faz_komite}, yonetisim{model, ust_organlar[], rol_turleri[], yetki_ilkesi, veri_mahremiyeti, ozel_kurallar,
  kpi_notu}, karar_sureci[{kod, ad}], komiteler[{kod "KMT-NN", ad, kategori, kategori_kodu, uygulama_durumu, seviye,
  bagli_organ, amac, organizasyon{baskan_unvani, baskan_yardimcisi_unvani, daimi_uyeler_unvanlari[], sekreterya,
  davetli_uzman, uye_atama}, departman_iliskileri{departman_kodlari["NN"], ilgili_sirketler}, gorevler[],
  yetkiler{kapsam, seviye_1, seviye_2, seviye_3, imza_yetkisi}, toplanti{periyot, gundem_paylasim_is_gunu_once,
  tutanak_yayin_is_gunu_sonra, toplanti_yeter_sayisi, karar_yeter_sayisi, acil_toplanti}, karar_akis_kodlari[],
  kpi[{ad, hesaplama, baslangic_hedefi, olcum_sikligi, hedef_tipi}], zorunlu_ciktilar[], iliskili_komite_kodlari[],
  kontrol_noktalari[]}], entegrasyon{onerilen_varliklar[], organizasyon_iliskileri[], guvenlik, karar_kod_sablonu,
  raporlama[]}.

Çıktı DATA.committees: title, company (gösterilmez), version, date, nature, scope (şirket adı içerdiği için
gösterilmez), model, upper[], roles[], principles[[etiket, metin]], kpiNote, flow[{id, name}],
categories[{id, name}] (ilk geçiş sırası), phases[{id, name}], integration{entities, relations, security,
codeTemplate, reports}, common{…}, items[{id, name, cat, phase, organ, purpose, chair, vice, members[],
secretariat, depts[departman id], duties[], authority, period, kpis[{name, calc, target, freq}], outputs[],
related[]} + common'a alınamayan alanlar]. HOIST'taki alanlar bütün komitelerde aynıysa `common`a alınır,
değilse her komitede kalır; arayüz önce komiteye, yoksa common'a bakar (kmV). KPI hedef tipi de aynı kuralla
common.kpiType olur ya da KPI'da `type` kalır.

Denetimler (tutmazsa betik durur): bilinmeyen anahtar yok; kodlar KMT-01'den sırayla; adlar tekil; komite sayısı
ve pilot / ikinci faz sayıları dokuman'daki sayılarla aynı; uygulama durumu, seviye ve ölçüm sıklığı aşağıdaki
sözlüklerde tanımlı; kategori kodu ↔ kategori adı bire bir; departman kodları DATA.departments sırasında var
(NN → departman id'si) ve tekrarsız; ilişkili komiteler var, kendisi değil, tekrarsız; karar akış kodları
karar_sureci'nde ve aynı sırada; baslik'teki şirket adı COMPANY_NAMES'te. Tek yönlü ilişkiler yalnız uyarı olarak
yazılır (veri olduğu gibi işlenir).
"""
import hashlib
import json
import re
import sys

PHASE_NAMES = {"pilot": "Pilot", "ikinci_faz": "İkinci faz"}
LEVEL_NAMES = {"holding_ortak": "Holding ortak komitesi"}
FREQ_NAMES = {"aylik": "Aylık", "uc_aylik": "Üç aylık"}
COMPANY_NAMES = {"Rasyo Holding"}
# Bütün komitelerde aynıysa common'a alınan alanlar
HOIST = ["level", "invited", "appoint", "companies", "levels", "sign", "agendaDays", "minutesDays", "quorum",
         "majority", "urgent", "flow", "controls"]

KEYS = {
    "": {"dokuman", "yonetisim", "karar_sureci", "komiteler", "entegrasyon"},
    "dokuman": {"baslik", "surum", "olusturma_tarihi", "dil", "nitelik", "kapsam", "toplam_komite", "pilot_komite",
                "ikinci_faz_komite"},
    "yonetisim": {"model", "ust_organlar", "rol_turleri", "yetki_ilkesi", "veri_mahremiyeti", "ozel_kurallar",
                  "kpi_notu"},
    "entegrasyon": {"onerilen_varliklar", "organizasyon_iliskileri", "guvenlik", "karar_kod_sablonu", "raporlama"},
    "komite": {"kod", "ad", "kategori", "kategori_kodu", "uygulama_durumu", "seviye", "bagli_organ", "amac",
               "organizasyon", "departman_iliskileri", "gorevler", "yetkiler", "toplanti", "karar_akis_kodlari", "kpi",
               "zorunlu_ciktilar", "iliskili_komite_kodlari", "kontrol_noktalari"},
    "organizasyon": {"baskan_unvani", "baskan_yardimcisi_unvani", "daimi_uyeler_unvanlari", "sekreterya",
                     "davetli_uzman", "uye_atama"},
    "departman_iliskileri": {"departman_kodlari", "ilgili_sirketler"},
    "yetkiler": {"kapsam", "seviye_1", "seviye_2", "seviye_3", "imza_yetkisi"},
    "toplanti": {"periyot", "gundem_paylasim_is_gunu_once", "tutanak_yayin_is_gunu_sonra", "toplanti_yeter_sayisi",
                 "karar_yeter_sayisi", "acil_toplanti"},
    "kpi": {"ad", "hesaplama", "baslangic_hedefi", "olcum_sikligi", "hedef_tipi"},
    "karar": {"kod", "ad"},
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


def model_from(src, depts):
    keys(src, "", "kök")
    doc, gov, integ = src["dokuman"], src["yonetisim"], src["entegrasyon"]
    keys(doc, "dokuman", "dokuman")
    keys(gov, "yonetisim", "yonetisim")
    keys(integ, "entegrasyon", "entegrasyon")
    company, _, title = text(doc["baslik"], "baslik").partition(" — ")
    if not title:
        company, title = "", company
    assert not company or company in COMPANY_NAMES, f"COMPANY_NAMES: {company}"
    flow = []
    for x in src["karar_sureci"]:
        keys(x, "karar", "karar_sureci")
        flow.append({"id": text(x["kod"], "karar kodu"), "name": text(x["ad"], "karar adı")})
    fids = [x["id"] for x in flow]
    assert len(set(fids)) == len(fids), "karar_sureci kodları tekrarlı"
    dept_ids = [d["id"] for d in depts]
    cats, items, names = {}, [], set()
    K = src["komiteler"]
    codes = [k["kod"] for k in K]
    for n, k in enumerate(K, 1):
        w = k.get("kod", f"#{n}")
        keys(k, "komite", w)
        assert k["kod"] == f"KMT-{n:02d}", f"{w}: kod sırası (beklenen KMT-{n:02d})"
        name = text(k["ad"], w)
        assert name not in names, f"{w}: ad tekrarlı"
        names.add(name)
        cc, cn = text(k["kategori_kodu"], w), text(k["kategori"], w)
        assert cats.setdefault(cc, cn) == cn, f"{w}: {cc} kategori adı farklı"
        assert sum(1 for x, y in cats.items() if y == cn) == 1, f"{w}: {cn} iki kategori kodunda"
        assert k["uygulama_durumu"] in PHASE_NAMES, f"PHASE_NAMES: {k['uygulama_durumu']}"
        assert k["seviye"] in LEVEL_NAMES, f"LEVEL_NAMES: {k['seviye']}"
        o, r, y, t = k["organizasyon"], k["departman_iliskileri"], k["yetkiler"], k["toplanti"]
        for sub in ("organizasyon", "departman_iliskileri", "yetkiler", "toplanti"):
            keys(k[sub], sub, f"{w}.{sub}")
        dc = r["departman_kodlari"]
        assert dc and len(set(dc)) == len(dc), f"{w}: departman kodları boş ya da tekrarlı"
        for c in dc:
            assert re.fullmatch(r"\d{2}", c) and 1 <= int(c) <= len(dept_ids), f"{w}: departman kodu {c}"
        rel = k["iliskili_komite_kodlari"]
        assert len(set(rel)) == len(rel), f"{w}: ilişkili komite tekrarlı"
        for c in rel:
            assert c in codes and c != k["kod"], f"{w}: ilişkili komite {c}"
        fl = k["karar_akis_kodlari"]
        assert all(c in fids for c in fl) and fl == [c for c in fids if c in fl], f"{w}: karar akış kodları"
        for sub in ("gundem_paylasim_is_gunu_once", "tutanak_yayin_is_gunu_sonra"):
            assert isinstance(t[sub], int) and t[sub] >= 0, f"{w}: {sub}"
        kpis = []
        for x in k["kpi"]:
            keys(x, "kpi", f"{w}.kpi")
            assert x["olcum_sikligi"] in FREQ_NAMES, f"FREQ_NAMES: {x['olcum_sikligi']}"
            kpis.append({"name": text(x["ad"], w), "calc": text(x["hesaplama"], w),
                         "target": text(x["baslangic_hedefi"], w), "freq": FREQ_NAMES[x["olcum_sikligi"]],
                         "type": text(x["hedef_tipi"], w)})
        assert kpis, f"{w}: KPI yok"
        items.append({
            "id": k["kod"], "name": name, "cat": cc, "phase": k["uygulama_durumu"],
            "level": LEVEL_NAMES[k["seviye"]], "organ": text(k["bagli_organ"], w), "purpose": text(k["amac"], w),
            "chair": text(o["baskan_unvani"], w), "vice": text(o["baskan_yardimcisi_unvani"], w),
            "members": texts(o["daimi_uyeler_unvanlari"], w), "secretariat": text(o["sekreterya"], w),
            "invited": text(o["davetli_uzman"], w), "appoint": text(o["uye_atama"], w),
            "depts": [dept_ids[int(c) - 1] for c in dc], "companies": text(r["ilgili_sirketler"], w),
            "duties": texts(k["gorevler"], w), "authority": text(y["kapsam"], w),
            "levels": [text(y["seviye_1"], w), text(y["seviye_2"], w), text(y["seviye_3"], w)],
            "sign": text(y["imza_yetkisi"], w), "period": text(t["periyot"], w),
            "agendaDays": t["gundem_paylasim_is_gunu_once"], "minutesDays": t["tutanak_yayin_is_gunu_sonra"],
            "quorum": text(t["toplanti_yeter_sayisi"], w), "majority": text(t["karar_yeter_sayisi"], w),
            "urgent": text(t["acil_toplanti"], w), "flow": fl, "kpis": kpis,
            "outputs": texts(k["zorunlu_ciktilar"], w), "related": rel,
            "controls": texts(k["kontrol_noktalari"], w),
        })
    assert len(items) == doc["toplam_komite"], f"komite sayısı {len(items)} ≠ {doc['toplam_komite']}"
    for ph, key in (("pilot", "pilot_komite"), ("ikinci_faz", "ikinci_faz_komite")):
        got = sum(1 for x in items if x["phase"] == ph)
        assert got == doc[key], f"{key}: {got} ≠ {doc[key]}"
    common = {}
    for h in HOIST:
        vals = [json.dumps(x[h], ensure_ascii=False) for x in items]
        if len(set(vals)) == 1:
            common[h] = items[0][h]
            for x in items:
                del x[h]
    types = {x["type"] for c in items for x in c["kpis"]}
    if len(types) == 1:
        common["kpiType"] = types.pop()
        for c in items:
            for x in c["kpis"]:
                del x["type"]
    by = {x["id"]: x for x in items}
    one_way = [(a["id"], b) for a in items for b in a["related"] if a["id"] not in by[b]["related"]]
    unused = [f"{n:02d}" for n, d in enumerate(dept_ids, 1) if not any(d in x["depts"] for x in items)]
    return {
        "title": title, "company": company, "version": text(doc["surum"], "surum"),
        "date": text(doc["olusturma_tarihi"], "tarih"), "nature": text(doc["nitelik"], "nitelik"),
        "scope": text(doc["kapsam"], "kapsam"), "model": text(gov["model"], "model"),
        "upper": texts(gov["ust_organlar"], "ust_organlar"), "roles": texts(gov["rol_turleri"], "rol_turleri"),
        "principles": [["Yetki ilkesi", text(gov["yetki_ilkesi"], "yetki_ilkesi")],
                       ["Veri mahremiyeti", text(gov["veri_mahremiyeti"], "veri_mahremiyeti")],
                       ["Özel kurallar", text(gov["ozel_kurallar"], "ozel_kurallar")]],
        "kpiNote": text(gov["kpi_notu"], "kpi_notu"), "flow": flow,
        "categories": [{"id": c, "name": n} for c, n in cats.items()],
        "phases": [{"id": p, "name": PHASE_NAMES[p]} for p in PHASE_NAMES if any(x["phase"] == p for x in items)],
        "integration": {"entities": texts(integ["onerilen_varliklar"], "onerilen_varliklar"),
                        "relations": texts(integ["organizasyon_iliskileri"], "organizasyon_iliskileri"),
                        "security": text(integ["guvenlik"], "guvenlik"),
                        "codeTemplate": text(integ["karar_kod_sablonu"], "karar_kod_sablonu"),
                        "reports": texts(integ["raporlama"], "raporlama")},
        "common": common, "items": items,
    }, one_way, unused


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
    model, one_way, unused = model_from(src, data["departments"])
    data["committees"] = model
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    it = model["items"]
    print(f"{len(it)} komite ({sum(1 for x in it if x['phase'] == 'pilot')} pilot), {len(model['categories'])} kategori, "
          f"{len(model['flow'])} karar adımı; ortak alanlar: {', '.join(model['common'])}")
    if one_way:
        print(f"Uyarı — tek yönlü ilişki ({len(one_way)}): " + ", ".join(f"{a}→{b}" for a, b in one_way))
    if unused:
        print("Uyarı — hiçbir komitede olmayan departmanlar: " + ", ".join(unused))


if __name__ == "__main__":
    main()
