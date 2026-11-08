"""Departman hiyerarşisi JSON'unu web-proje-gelistirme.html içindeki DATA.departments'a işler.

Kullanım (proje kökünden, önce _yedek/ altına kopya alın):
    python3 -I docs/organizasyon/departman_ekle.py web-proje-gelistirme.html <departman-id> docs/organizasyon/<NN-ad>.json [beklenen-md5]

İki girdi biçimi okunur:
  A) department{name_tr,leader,scope,boundary,…}, units[].teams[].manager/roles, isteğe bağlı *_handoff,
     title_standard[{level,title_tr,title_en}], department_kpis{grup: [...]}  (ör. 02, 09)
  B) department_name, department_head, mission, scope_exclusions, units[].teams[].name/roles (ekip lideri
     rol listesinde "Takım Lideri" geçen roldür ve ekibin lideri yapılır), units[].responsibilities,
     cross_department_boundaries[{department, <x>_owns, other_owns}], title_standard["TR / EN"],
     implementation_note  (ör. 03)
  C) departman_kodu, departman, ust_bagli, direktor, birimler[{ad, mudur, pozisyonlar[]}] (ekip yok; "Takım
     Lideri" geçen pozisyon birimin diğer pozisyonlarının lideri yapılır, yoksa pozisyonlar doğrudan müdüre
     bağlanır), gorev_sinirlari{kısa ad: cümle} (kısa ad IF_DEPTS ile departmana eşlenir)  (ör. 04)
  D) departman_kodu, departman_adi, amac, organizasyon{yonetim_kurulu{title, alt_roller[], gorevler[]},
     ceo{title, raporlar, kurul, dogrudan_bagli_birimler[{birim, yonetici, pozisyonlar[], gorevler[]}]}},
     gorev_sinirlari[cümle], not; unvanlar "TR / EN"  (ör. 01). Yönetim kurulu `board` olur ve departman
     liderinin (CEO) üstünde durur: pozisyonları "kurul" (başkan) ve "kurul/<rol slug>".
  E) department_code, department_name_tr/_en, model, headcount, headcount_excludes, positions[{id, title_tr,
     title_en, level, reports_to, unit_id?, responsibilities}], units[{unit_id, name_tr, position_ids}],
     department_boundaries{kısa ad: cümle}, notes[]  (ör. 05). Hiyerarşi reports_to zincirinden kurulur:
     reports_to'su boş tek pozisyon dış raporlama makamıdır (reportsTo), ona bağlı tek pozisyon departman
     lideridir, lidere bağlı her pozisyon bir birimin lideridir (unit_id yoksa birim adı unvandan türer),
     onlara bağlı pozisyonlar birime doğrudan bağlı rollerdir. Rolün görevleri birim liderininkinden
     farklıysa rolde `resp` olarak saklanır. reporting_line ve schema_version şemadan türetilebildiği için
     saklanmaz.
  F) schema_version, department{id, code, name_tr, name_en, purpose, administrative_reporting_to,
     governance_principle}, organization_chart{root}, executive_positions[{code, title_tr, title_en, level,
     reports_to, responsibilities}], units[{id, name_tr, name_en, manager_title_tr/_en, reports_to,
     positions[{title_tr, title_en, level, responsibility}]}], board_committees[{name_tr, name_en,
     recommended_chair, oversight_scope}], staffing_models[], <şirket>_recommended_staffing{total_headcount_min/
     _max, composition[{role_group, count_min, count_max}]}, responsibility_boundaries{in_scope, out_of_scope,
     interfaces[{department: "N. Ad", division_of_responsibility}]}  (ör. 01 V2). Şema ağacı Genel Kurul →
     Yönetim Kurulu (roller + komite grubu) → CEO (departman lideri) → isteğe bağlı ara yönetici (ör. CEO Ofisi
     Başkanı, `office`) → unit_ref'ler biçiminde olmalı; her düğüm executive_positions ve units ile
     karşılaştırılır (reports_to zinciri, komite adları, birim referansları tutmazsa betik durur). Kök `board.reportsTo`
     olur; komiteler `board.committees`, pozisyonları "komite/<slug>"; ara yönetici "ofis", birim liderleri ona
     bağlanır. governance_principle → `boundary`, in_scope → `scope`, out_of_scope → `exclusions`, interfaces
     → `interfaces` (numara ve ad DATA.departments ile denetlenir), staffing_models → `staffing`, önerilen kadro
     → `staffPlan` (toplam, satırların toplamıyla denetlenir) ve şirket adı `company` (COMPANY_NAMES).
  G) schema_version, department{code, name_tr, name_en, mission, administrative_reporting_to{title_tr,title_en},
     department_head, deputy_head{…, status}}, organization_chart{root: üst makam → departman lideri →
     unit_ref'ler} (executive_positions YOK — F'den bu ayırt eder), units[{id, name_tr, name_en, activation_rule?,
     manager{title_tr,title_en}, teams[{name_tr, name_en, positions[{title_tr,title_en}]}], responsibilities}],
     *_role{title_tr, title_en, organizational_model, responsibilities} (matris rol → `matrix`, pozisyon
     "matris/<slug>"), title_standard[{level,title_tr,title_en}], cross_department_boundaries[{process,
     <x>_owns, other_department, other_department_owns}] (→ interfaces + `process`), scope_exclusions,
     implementation_notes[]  (ör. 03 V2). Ekipte "Takım Lideri" geçen pozisyon ekibin lideridir (B gibi);
     activation_rule → birimin `optional`'ı; deputy_head → `aides`. 05 V2 de G'dir: department.reporting_to (yerine),
     model, hierarchy_standard (→ `levels`), department_leadership[] (lider görevleri → leader.resp; lidere bağlı
     diğerleri → `aides`, pozisyon "lider/<slug>"), ekipte `lead` (ekip lideri; yoksa "Takım Lideri" kuralı),
     department_boundaries[{interface_department, <x>_owns, other_department_owns}], staffing_models[{model,
     recommended_structure}] (→ `staffing[{model,text}]`), organization_summary (sayılar şemayla denetlenir,
     staffing_note → `staffNote`), notes[]. 06 da G'dir: functional_reporting_to (şema ağacı kökten Yönetim Kurulu →
     komite → lider zinciri; zincir başlıkları birleşince fonksiyonel makamı vermeli, liderin administrative_reporting_to'su
     idari makamda geçmeli) → `functional{title,en,relationship}`, `reportsTo` idari makamdır; independence_principle →
     `boundary`; organization_summary.specialist_position_types = uzman pozisyon sayısı. 07: governance_model[{subject,
     <x>_authority…}] → `authority{cols,rows[{subject,vals}]}` (sütun adları AUTH_NAMES), three_lines_model[{line, name_tr,
     owner, responsibility}] → `lines`; ikisi de görev/yetki bilgisidir, DP_DUTIES kapalıyken gösterilmez. 08: *_lifecycle[{stage,
     name_tr, primary_owner, output}] → `lifecycles[{title,rows}]` (başlık LIFECYCLE_NAMES; süreç sahipliği, gizli); raporlama
     makamı şemada kısaltmasız geçebilir ("Ticari İşler Başkanı / CCO" ↔ "Ticari İşler Başkanı"). 10: content_ownership[{content_type,
     primary_owner}] → `ownership[{type,owner}]` (içerik sahipliği; gizli).
  H) schema_version, department{code, name_tr, name_en, organization_model, reports_to, purpose, head{title_tr, title_en,
     alternative_executive_title, reports_to, direct_reports[], key_accountabilities[]}, hierarchy_standard, units[{unit_code,
     name_tr, name_en, manager, mission, teams[{team_code, name_tr, name_en, lead, positions[], responsibilities[]}]}],
     governance{core_kpis[], cadence[{forum, focus}]}, scope_boundaries{kısa ad: cümle}, staffing_guidance{model,
     minimum_core_headcount, minimum_core_headcount_note, capacity_drivers[]}, organization_summary{…, core_principle}}  (ör. 11–21).
     Şema ağacı yok; her şey department içinde. mission → birimin `resp`'i, ekip responsibilities → ekibin `resp`'i,
     alternative_executive_title → leader.alt, core_kpis → kpis, cadence → `cadence` (gizli), staffing_guidance → `staffGuide`
     (asgari çekirdek kadro = 1 + birim + ekip yöneticisi denetlenir), core_principle → `boundary` (gizli).
     12/13 varyantı: üstte document{name, created_at, language} (yalnız denetlenir: ad "NN - Departman" ile başlamalı), lider
     görevleri key_accountabilities yerine accountabilities. head.reports_to departmanın reports_to'sundan farklıysa yalnız
     alternative_executive_title varken kabul edilir (lider o unvanı alırsa head.reports_to'ya bağlanır; 12: COO, 13: CSCO)
     → leader.altUp ("Bu unvanla bağlı olduğu" çipi). position_code / reports_to verilmişse zincir denetlenir
     (müdür → lider, ekip yöneticisi → müdür, uzman → ekip yöneticisi; kod tekrarı yok).
     14: department.independence_principle → `bounds` (Sınır kartında madde; gizli — `boundary` core_principle'da kalır).
     Departmana ait olmayan sınır anahtarı (document_management) IF_DEPTS'te boş id ile "Tüm iş birimleri" satırı olur;
     aynı anahtar bir departmanda farklı kapsamdaysa IF_DEPTS_BY_DEPT (14'te operations = 12 ve 13).
     16: reports_to{primary{title_tr, title_en}, functional_access[]} → `reportsTo` = primary, functional_access →
     `functional` ("Bağlı olduğu" satırında "· Fonksiyonel: …", ilişki "Doğrudan fonksiyonel erişim").
     17–21: operating_principle → `bounds` (independence_principle'dan sonra), alternative_executive_titles[] → leader.alt
     dizi ("Alternatif unvanlar" çipi). F (01): CEO düğümünün birimi olmayan çocukları (CFO, COO, CCO, CTO/CIO, CPO) →
     `aides` (lider düğümünde seviye çipli satır, pozisyon "lider/<slug>"); executive_positions'ta reports_to CEO olmalı.
  I) schema_version, document{type, language, created_at, project}, department{code, name_tr, name_en, operating_model,
     purpose}, reports_to{primary (metin), administrative_alternative, independent_escalation[], functional_alignment,
     governance_coordination[]}, head{position_code, title_tr, title_en, alternative_executive_title, direct_reports[müdür
     kodları], accountabilities[]}, hierarchy_standard{levels[{level, role, scope}]}, units[{unit_code, name_tr, name_en,
     manager{position_code, title_tr, title_en}, teams[{team_code, name_tr, lead{…}, roles["Türkçe / English"]}]}],
     governance{core_kpis[], cadences[{frequency, forum}]}, scope_boundaries[{adjacent_department "NN - Ad" (" / " ile
     birden çok; numarasız kısa ad DEPT_ALIASES'te), boundary}], staffing_guidance{minimum_core_headcount,
     minimum_core_composition{director, unit_managers, team_leads}, specialist_staffing, shift_note,
     executive_assistant_ratio, confidentiality_principle, outsourcing_principle}, organization_summary{director_count,
     unit_count, manager_count, team_count, team_lead_count, specialist_role_type_count, minimum_core_headcount}  (ör. 22, 23).
     Kök düzeyde units/head/reports_to. primary → `reportsTo`; administrative_alternative, independent_escalation,
     governance_coordination → leader.upNotes [[etiket, değer]] (lider düğümünde çip); functional_alignment → `functional`.
     levels[].role → `levels`, scope → `levelScopes` (gizli, "Hiyerarşi seviyeleri" tablosu). cadences → `cadence`
     ({forum, freq}; tabloda "Sıklık" sütunu, gizli). specialist_staffing → staffGuide.model, composition → staffGuide.note,
     metin notları → staffGuide.notes [[etiket, metin]] (görünür); gizlilik ve dış kaynak ilkesi → staffGuide.policies (gizli). Sayılar ve kadro bileşimi şemayla denetlenir.
Her biçimde isteğe bağlı üst düzey "standard" anahtarı (departman ve müdürlük standardı; şema seçiminden önce ayrılır):
  status ("taslak" | "onaylandı"), prepared_at, note, department{responsibilities[], authorities[], collaborations[{department
  "NN - Ad", unit (o departmandaki müdürlük adı ya da ""), topic}], kpis[] / title_standard[{level,title_tr,title_en}] /
  staffing_models[Yalın, Standart, Genişletilmiş {model,min,max}] / recommended_staffing{total_min,total_max,composition[{role_group,
  min,max}]} — bu dördü yalnız departman JSON'unda karşılığı (KPI, unvan standardı, kadro modelleri, önerilen kadro) yoksa ve o
  zaman zorunlu}, units[{unit_id, name_tr, responsibilities[], authorities[], collaborations[] (aynı biçim; kendi departmanından
  başka bir müdürlük de olabilir), kpis[], title_standard[{position, level, title_tr, title_en}], staffing_models[Yalın, Standart,
  Genişletilmiş], recommended_staffing[{position, title_tr, min, max}]}] — birimler şemadaki sırayla, pozisyonlar dpPos sırasıyla
  (birim lideri, birime bağlı roller, ekip yöneticisi ve rolleri); pozisyon unvanı ve şemada varsa İngilizcesi aynı olmalı.
  Denetimler: müdürlüğün Standart modeli = önerilen kadro toplamı, Yalın ≤ Standart ≤ Genişletilmiş; departman dağılımı =
  "Departman yönetimi" (lider + ara yönetici + matris roller + yönetim pozisyonları; opsiyonel olan alt sınırda sayılmaz) +
  müdürlük pozisyonlarının seviyeye göre toplamı, departmanın Standart modeli = dağılım toplamı, Yalın / Genişletilmiş = yönetim
  (alt / üst) + müdürlüklerin Yalın / Genişletilmiş toplamı. Çıktı: org.std {status, resp, auth, with[{dept, unit, topic}],
  kpis?, titles?, staffing?, staffPlan?} ve units[].std {resp, auth, with, kpis, pos[{id, level, en, min, max}], staffing}.
Pozisyon kimlikleri: "lider" (departman lideri) · <birim id> (birim lideri) · <birim id>/<ekip slug> (ekip
lideri; ekip lideri yoksa pozisyon değildir, rolleri doğrudan birim liderine bağlanır) ·
<birim id>/<rol slug> (birim liderine doğrudan bağlı rol, birimin `roles` listesi) ·
<birim id>/<ekip slug>/<rol slug>. A'da ekip slug'ı yöneticiden, B'de ekip adından, C'de takım liderinden
türer; C'de birim id'si birim adının slug'ıdır.
Slug = Türkçe harfler katlanmış, küçük harf, '-' ayraçlı. Bilinmeyen anahtar gelirse betik durur.
Ajanların varsayılan pozisyonu (agentCatalog[].pos) bu betikle değil, elle atanır.
"""
import hashlib
import json
import re
import sys

TR = str.maketrans("çğıöşüâîÇĞİÖŞÜÂÎ", "cgiosuaiCGIOSUAI")
# Yeni bir departmanda bilinmeyen KPI grubu veya devir tarafı gelirse betik durur; Türkçe adını buraya ekleyin.
KPI_NAMES = {
    "demand_and_revenue": "Talep ve gelir",
    "brand_and_visibility": "Marka ve görünürlük",
    "conversion": "Dönüşüm",
    "operations": "Operasyon",
    "accounting_quality": "Muhasebe kalitesi",
    "compliance_and_tax": "Uyum ve vergi",
    "closing_and_reporting": "Kapanış ve raporlama",
    "operations_and_audit": "Operasyon ve denetim",
}
SIDE_NAMES = {
    "marketing": "Pazarlama",
    "sales": "Satış",
    "accounting": "Muhasebe",
    "finance_and_treasury": "Finans ve Hazine",
}
# F: "<şirket>_recommended_staffing" anahtarındaki şirket öneki → şirket adı
COMPANY_NAMES = {
    "rasyo_holding": "Rasyo Holding",
}
# Sınır anahtarları (C: gorev_sinirlari, E: department_boundaries) → departman id'si veya (id, ayırıcı ek); id boşsa
# satırda yalnız ek yazılır (bir departmana değil bütün birimlere ait sınır)
IF_DEPTS = {
    "hukuk": "hukuk",
    "muhasebe": "muhasebe",
    "finans": "finans",
    "iletisim": "kurumsal-iletisim",
    "tasarim": "tasarim",
    "legal_affairs": "hukuk",
    "compliance": ("uyum-risk", "Uyum"),
    "enterprise_risk_internal_control": ("uyum-risk", "Kurumsal risk ve iç kontrol"),
    "internal_audit": "ic-denetim",
    "human_resources": "insan-kaynaklari",
    "finance": "finans",
    "accounting": "muhasebe",
    "sales": "satis",
    "marketing": "pazarlama",
    "operations": "operasyon",
    "product": "urun-arge",
    "technical_it": ("bilgi-teknolojileri", "Teknik ekipler ve BT"),
    "technology": ("bilgi-teknolojileri", "Teknik ekipler ve BT"),
    "customer_experience": "musteri-deneyimi",
    "procurement": ("uretim-tedarik", "Satın Alma"),
    "risk_compliance": "uyum-risk",
    "operations_management": "operasyon",
    "product_rd": "urun-arge",
    "sustainability": "isg-cevre",
    "legal": "hukuk",
    "quality": "kalite",
    "compliance_risk": "uyum-risk",
    "document_management": ("", "Tüm iş birimleri (doküman yönetimi)"),
    "business_units": ("", "Tüm iş birimleri"),
    "data_governance": ("", "Tüm iş birimleri (veri sahipliği)"),
    "cybersecurity": "siber-guvenlik",
    "customer_support": ("musteri-deneyimi", "Müşteri Destek"),
    "information_technology": "bilgi-teknolojileri",
    "legal_privacy": ["hukuk", "uyum-risk"],  # "Hukuk ve KVKK fonksiyonları" — KVKK hem 05'te hem 06'da
    "product_engineering": ["urun-arge", "bilgi-teknolojileri"],  # "Ürün ve Yazılım ekipleri"
    "corporate_communications": "kurumsal-iletisim",
    "marketing_sales": ["pazarlama", "satis"],
    "data_ai": "veri-analitik",
    "legal_ip": "hukuk",
    "product_management": "urun-arge",
    "content": ["pazarlama", "kurumsal-iletisim"],  # "İçerik ekipleri" — içerik pazarlaması ve kurumsal yayınlar
    "occupational_health_safety": "isg-cevre",
    "security_cyber": "siber-guvenlik",
    "corporate_security": "kurumsal-guvenlik",
    "legal_compliance": ["hukuk", "uyum-risk"],
    "administrative_affairs": "idari-isler",
    "supply_chain": "uretim-tedarik",
}
# Aynı kısa anahtar bir departmanın JSON'unda farklı kapsamdaysa: departman id → {anahtar: IF_DEPTS değeri}; liste = birden çok departman
IF_DEPTS_BY_DEPT = {
    "kalite": {"operations": ["operasyon", "uretim-tedarik"]},  # "Operasyon ve Üretim süreçlerin günlük uygulanması…"
}
KEYS_E = {"schema_version", "organization", "department_code", "department_name_tr", "department_name_en", "model",
          "headcount", "headcount_excludes", "reporting_line", "positions", "units", "department_boundaries", "notes"}
KEYS_A = {"department", "units", "title_standard", "department_kpis"}
KEYS_C = {"departman_kodu", "departman", "ust_bagli", "direktor", "birimler", "gorev_sinirlari"}
KEYS_D = {"departman_kodu", "departman_adi", "amac", "organizasyon", "gorev_sinirlari", "not"}
KEYS_F = {"schema_version", "department", "organization_chart", "executive_positions", "units", "board_committees",
          "staffing_models", "responsibility_boundaries"}
KEYS_G = {"schema_version", "organization", "department", "organization_chart", "department_leadership", "units",
          "organization_summary", "staffing_models", "title_standard", "cross_department_boundaries", "department_boundaries",
          "scope_exclusions", "implementation_notes", "notes", "governance_model", "three_lines_model", "content_ownership"}
# G: sınır satırlarında departmanın kısaltılmış adı → departman id'si (numara ayrıca denetlenir; tabloda resmî ad yazılır)
DEPT_ALIASES = {
    "İSG, Çevre ve Sürdürülebilirlik": "isg-cevre",
    "İnsan Kaynakları": "insan-kaynaklari",
}
# G: *_lifecycle anahtarı → tablo başlığı
LIFECYCLE_NAMES = {
    "sales_lifecycle": "Satış yaşam döngüsü",
}
# G: governance_model satırlarındaki yetki sütunları → tablo başlığı
AUTH_NAMES = {
    "audit_committee_authority": "Denetim Komitesi",
    "ceo_administrative_authority": "CEO (idari)",
}
RESERVED = {"lider", "kurul", "ofis", "komite", "matris"}
KEYS_B = {"department_code", "department_name", "department_name_en", "reports_to", "department_head", "mission",
          "scope", "boundary", "scope_exclusions", "units", "cross_department_boundaries", "title_standard",
          "implementation_note"}


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.translate(TR).lower()).strip("-")


def check_units(units):
    uids = set()
    for u in units:
        assert u["id"] not in uids and "/" not in u["id"] and u["id"] not in RESERVED, u["id"]
        uids.add(u["id"])
        tids = {r["id"] for r in u.get("roles", [])}
        assert all(tids) and len(tids) == len(u.get("roles", [])), (u["id"], "roles")
        for t in u["teams"]:
            assert t["id"] and t["id"] not in tids, (u["id"], t)
            tids.add(t["id"])
            rids = set()
            for r in t["roles"]:
                assert r["id"] and r["id"] not in rids, (u["id"], t["id"], r)
                rids.add(r["id"])


def org_from_a(src, missing):
    missing += [k for k in src if k not in KEYS_A and not k.endswith("_handoff")]
    d = src["department"]
    L = d["leader"]
    org = {
        "title": d.get("name_tr", ""),
        "en": d.get("name_en", ""),
        "purpose": d.get("purpose", ""),
        "reportsTo": d.get("reports_to", ""),
        "leader": {"title": L["title_tr"], "en": L.get("title_en", ""), "abbr": L.get("abbreviation", "")},
        "scope": d.get("scope", []),
        "boundary": d.get("boundary", ""),
        "units": [
            {"id": u["id"], "name": u["name_tr"], "leader": u["leader"], "teams": [
                {"id": slug(t["manager"]), "manager": t["manager"], "roles": [{"id": slug(r), "title": r} for r in t["roles"]]}
                for t in u["teams"]]}
            for u in src["units"]],
    }
    for k, v in src.items():
        if k.endswith("_handoff"):
            cols, sides = [], []
            for kk, items in v.items():
                if kk == "joint_ownership":
                    cols.append({"name": "Ortak", "items": items})
                elif kk.endswith("_owns"):
                    side = kk[: -len("_owns")]
                    if side not in SIDE_NAMES:
                        missing.append("SIDE_NAMES: " + side)
                        continue
                    sides.append(SIDE_NAMES[side])
                    cols.append({"name": SIDE_NAMES[side], "items": items})
                elif kk != "handoff_point":
                    missing.append(k + "." + kk)
            title = " → ".join(sides) + " devri" if len(sides) > 1 else "Devir ve sorumluluk"
            org["handoff"] = {"title": title, "cols": cols, "point": v.get("handoff_point", "")}
    if "title_standard" in src:
        org["titles"] = [{"level": x["level"], "tr": x["title_tr"], "en": x.get("title_en", "")} for x in src["title_standard"]]
    if "department_kpis" in src:
        missing += ["KPI_NAMES: " + k for k in src["department_kpis"] if k not in KPI_NAMES]
        org["kpis"] = [{"name": KPI_NAMES.get(k, k), "items": v} for k, v in src["department_kpis"].items()]
    return org


def org_from_b(src, missing):
    missing += [k for k in src if k not in KEYS_B]
    H = src["department_head"]
    org = {
        "title": src["department_name"],
        "en": src.get("department_name_en", ""),
        "purpose": src.get("mission", ""),
        "reportsTo": src.get("reports_to", ""),
        "leader": {"title": H["title_tr"], "en": H.get("title_en", ""), "abbr": H.get("abbreviation", "")},
        "scope": src.get("scope", []),
        "boundary": src.get("boundary", ""),
        "units": [],
    }
    if src.get("scope_exclusions"):
        org["exclusions"] = src["scope_exclusions"]
    for u in src["units"]:
        missing += [u["id"] + "." + k for k in u if k not in {"id", "name", "manager", "manager_en", "teams", "responsibilities"}]
        U = {"id": u["id"], "name": u["name"], "leader": u["manager"]}
        if u.get("manager_en"):
            U["leaderEn"] = u["manager_en"]
        if u.get("responsibilities"):
            U["resp"] = u["responsibilities"]
        U["teams"] = []
        for t in u["teams"]:
            roles = list(t["roles"])
            leads = [r for r in roles if "Takım Lideri" in r]
            assert len(leads) <= 1, (u["id"], t["name"], leads)
            T = {"id": slug(t["name"]), "name": t["name"]}
            if leads:
                roles.remove(leads[0])
                T["manager"] = leads[0]
            T["roles"] = [{"id": slug(r), "title": r} for r in roles]
            U["teams"].append(T)
        org["units"].append(U)
    ifs = []
    for x in src.get("cross_department_boundaries", []):
        ours = [k for k in x if k.endswith("_owns") and k != "other_owns"]
        missing += [k for k in x if k not in {"department", "other_owns"} and k not in ours]
        assert len(ours) == 1, x
        ifs.append({"dept": x["department"], "ours": x[ours[0]], "theirs": x.get("other_owns", "")})
    if ifs:
        org["interfaces"] = ifs
    if "title_standard" in src:
        org["titles"] = []
        for s in src["title_standard"]:
            tr, _, en = s.partition(" / ")
            org["titles"].append({"level": "", "tr": tr.strip(), "en": en.strip()})
    if src.get("implementation_note"):
        org["note"] = src["implementation_note"]
    return org


def org_from_c(src, missing, depts):
    missing += [k for k in src if k not in KEYS_C]
    H = src["direktor"]
    org = {
        "title": src["departman"],
        "en": "",
        "purpose": "",
        "reportsTo": src.get("ust_bagli", ""),
        "leader": {"title": H["title_tr"], "en": H.get("title_en", ""), "abbr": ""},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    for u in src["birimler"]:
        missing += [u["ad"] + "." + k for k in u if k not in {"ad", "mudur", "pozisyonlar"}]
        roles = list(u["pozisyonlar"])
        leads = [r for r in roles if "Takım Lideri" in r]
        assert len(leads) <= 1, (u["ad"], leads)
        U = {"id": slug(u["ad"]), "name": u["ad"], "leader": u["mudur"], "teams": []}
        if leads:
            roles.remove(leads[0])
            U["teams"].append({"id": slug(leads[0]), "manager": leads[0], "roles": [{"id": slug(r), "title": r} for r in roles]})
        else:
            U["roles"] = [{"id": slug(r), "title": r} for r in roles]
        org["units"].append(U)
    ifs = if_rows(src.get("gorev_sinirlari", {}), missing, depts, None)
    if ifs:
        org["interfaces"] = ifs
    return org


def if_rows(bounds, missing, depts, self_id):
    names = {d["id"]: f"{n + 1:02d} - {d['name']}" for n, d in enumerate(depts)}
    rows = []
    M = {**IF_DEPTS, **IF_DEPTS_BY_DEPT.get(self_id, {})}
    for k, v in bounds.items():
        if k not in M:
            missing.append("IF_DEPTS: " + k)
            continue
        if isinstance(M[k], list):
            label = " · ".join(names[x] for x in M[k])
        else:
            did, extra = M[k] if isinstance(M[k], tuple) else (M[k], "")
            label = (names[did] + (f" ({extra})" if extra else "") if did else extra) + (" (bu departman)" if did == self_id else "")
        rows.append({"dept": label, "ours": "", "theirs": v})
    return rows


def org_from_e(src, missing, depts, self_id):
    missing += [k for k in src if k not in KEYS_E]
    P = src["positions"]
    ids = [p["id"] for p in P]
    assert len(set(ids)) == len(ids)
    for p in P:
        missing += [p["id"] + "." + k for k in p if k not in {"id", "title_tr", "title_en", "level", "headcount", "reports_to", "unit_id", "responsibilities"}]
    kids = lambda pid: [p for p in P if p.get("reports_to") == pid]
    roots = [p for p in P if not p.get("reports_to")]
    assert len(roots) == 1, roots
    leads = kids(roots[0]["id"])
    assert len(leads) == 1, leads
    L = leads[0]
    org = {
        "title": src["department_name_tr"],
        "en": src.get("department_name_en", ""),
        "purpose": "",
        "reportsTo": roots[0]["title_tr"],
        "leader": {"title": L["title_tr"], "en": L.get("title_en", ""), "abbr": ""},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    if L.get("responsibilities"):
        org["leader"]["resp"] = L["responsibilities"]
    for k in ("model", "organization"):
        if src.get(k):
            org["company" if k == "organization" else k] = src[k]
    if src.get("headcount"):
        org["headcount"] = src["headcount"]
        org["headcountExcl"] = src.get("headcount_excludes", [])
        hc = sum(p.get("headcount", 1) for p in P if p is not roots[0])
        assert hc == src["headcount"], f"kadro tutmuyor: pozisyonlar {hc}, headcount {src['headcount']}"
    units = {u["unit_id"]: u for u in src.get("units", [])}
    for u in src.get("units", []):
        missing += ["units." + k for k in u if k not in {"unit_id", "name_tr", "name_en", "position_ids", "headcount"}]
    order = {u["unit_id"]: n for n, u in enumerate(src.get("units", []))}
    used = {roots[0]["id"], L["id"]}
    for m in sorted(kids(L["id"]), key=lambda m: order.get(m.get("unit_id"), len(order))):
        sub = kids(m["id"])
        if m.get("unit_id"):
            U0 = units[m["unit_id"]]
            assert set(U0["position_ids"]) == {m["id"]} | {k["id"] for k in sub}, m["unit_id"]
            name = U0["name_tr"]
        else:
            name = re.sub(r"\s+(Yöneticisi|Müdürü)$", "", m["title_tr"])
        U = {"id": slug(name), "name": name, "leader": m["title_tr"]}
        if m.get("title_en"):
            U["leaderEn"] = m["title_en"]
        if m.get("responsibilities"):
            U["resp"] = m["responsibilities"]
        U["roles"] = []
        for k in sub:
            assert not kids(k["id"]), "dördüncü seviye bu şemada desteklenmiyor: " + k["id"]
            R = {"id": slug(k["title_tr"]), "title": k["title_tr"]}
            if k.get("responsibilities") and k["responsibilities"] != m.get("responsibilities"):
                R["resp"] = k["responsibilities"]
            U["roles"].append(R)
            used.add(k["id"])
        U["teams"] = []
        used.add(m["id"])
        org["units"].append(U)
    assert used == set(ids), set(ids) - used
    ifs = if_rows(src.get("department_boundaries", {}), missing, depts, self_id)
    if ifs:
        org["interfaces"] = ifs
    if src.get("notes"):
        org["notes"] = src["notes"]
    return org


def tr_en(s):
    tr, _, en = s.partition(" / ")
    return tr.strip(), en.strip()


def org_from_d(src, missing):
    missing += [k for k in src if k not in KEYS_D]
    O = src["organizasyon"]
    missing += ["organizasyon." + k for k in O if k not in {"yonetim_kurulu", "ceo"}]
    Y, C = O["yonetim_kurulu"], O["ceo"]
    missing += ["yonetim_kurulu." + k for k in Y if k not in {"title", "alt_roller", "gorevler"}]
    missing += ["ceo." + k for k in C if k not in {"title", "raporlar", "kurul", "dogrudan_bagli_birimler"}]
    ct, ce = tr_en(C["title"])
    kt, ke = tr_en(C.get("kurul", ""))
    bt, be = tr_en(Y["title"])
    org = {
        "title": src["departman_adi"],
        "en": "",
        "purpose": src.get("amac", ""),
        "reportsTo": C.get("raporlar", ""),
        "leader": {"title": ct, "en": ce, "abbr": ""},
        "board": {"title": bt, "en": be, "roles": [{"id": slug(tr_en(r)[0]), "title": tr_en(r)[0]} for r in Y.get("alt_roller", [])], "duties": Y.get("gorevler", [])},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    assert len({r["id"] for r in org["board"]["roles"]}) == len(org["board"]["roles"])
    if kt:
        org["leader"]["committee"] = kt + (f" ({ke})" if ke else "")
    for u in C["dogrudan_bagli_birimler"]:
        missing += [u["birim"] + "." + k for k in u if k not in {"birim", "yonetici", "pozisyonlar", "gorevler"}]
        lt, le = tr_en(u["yonetici"])
        U = {"id": slug(u["birim"]), "name": u["birim"], "leader": lt}
        assert U["id"] != "kurul"
        if le:
            U["leaderEn"] = le
        if u.get("gorevler"):
            U["resp"] = u["gorevler"]
        U["roles"] = [{"id": slug(tr_en(p)[0]), "title": tr_en(p)[0]} for p in u["pozisyonlar"]]
        U["teams"] = []
        org["units"].append(U)
    if src.get("gorev_sinirlari"):
        org["bounds"] = src["gorev_sinirlari"]
    if src.get("not"):
        org["note"] = src["not"]
    return org


def org_from_f(src, missing, depts, self_id):
    missing += [k for k in src if k not in KEYS_F and not k.endswith("_recommended_staffing")]
    D = src["department"]
    missing += ["department." + k for k in D if k not in {"id", "code", "name_tr", "name_en", "purpose",
                                                           "administrative_reporting_to", "governance_principle"}]
    names = [x["name"] for x in depts]
    assert D["name_tr"] == names[[x["id"] for x in depts].index(self_id)], D["name_tr"]
    X = {p["title_tr"]: p for p in src.get("executive_positions", [])}
    assert len(X) == len(src.get("executive_positions", []))
    for p in X.values():
        missing += [p["title_tr"] + "." + k for k in p if k not in {"code", "title_tr", "title_en", "level", "reports_to", "responsibilities"}]
    used = set()

    def exe(title, up):
        p = X[title]
        assert p.get("reports_to") == up, (title, p.get("reports_to"), up)
        used.add(title)
        r = {"title": title, "en": p.get("title_en", "")}
        if p.get("level"):
            r["level"] = p["level"]
        if p.get("responsibilities"):
            r["resp"] = p["responsibilities"]
        return r

    def walk(n):
        missing.extend(n.get("id", "?") + "." + k for k in n
                       if k not in {"id", "position_tr", "position_en", "roles", "children", "name_tr", "name_en", "unit_ref"})
        for c in n.get("children", []):
            walk(c)

    missing += ["organization_chart." + k for k in src["organization_chart"] if k != "root"]
    root = src["organization_chart"]["root"]
    walk(root)
    assert len(root["children"]) == 1, "Genel Kurul altında tek düğüm (Yönetim Kurulu) beklenir"
    B = root["children"][0]
    assert B.get("roles") and D.get("administrative_reporting_to") == B["position_tr"], B.get("position_tr")
    board = {"title": B["position_tr"], "en": B.get("position_en", ""), "reportsTo": root["position_tr"], "roles": []}
    for r in B["roles"]:
        t, e = tr_en(r)
        R = {"id": slug(t), "title": t, "en": e}
        if t in X:
            x = exe(t, root["position_tr"])
            R["en"] = x["en"] or e
            R.update({k: x[k] for k in ("level", "resp") if k in x})
        board["roles"].append(R)
    assert len({r["id"] for r in board["roles"]}) == len(board["roles"])
    groups = [n for n in B.get("children", []) if n.get("children") and all("name_tr" in c for c in n["children"])]
    execs = [n for n in B.get("children", []) if n not in groups]
    assert len(groups) <= 1 and len(execs) == 1, "Yönetim Kurulu altında bir komite grubu ve tek icra düğümü beklenir"
    BC = {c["name_tr"]: c for c in src.get("board_committees", [])}
    for c in BC.values():
        missing += [c["name_tr"] + "." + k for k in c if k not in {"name_tr", "name_en", "recommended_chair", "oversight_scope"}]
    chart_c = [c["name_tr"] for c in groups[0]["children"]] if groups else []
    assert sorted(chart_c) == sorted(BC) and len(set(chart_c)) == len(chart_c), "komite adları şema ile board_committees arasında tutmuyor"
    if chart_c:
        board["committeesTitle"] = groups[0]["position_tr"]
        board["committees"] = [{"id": slug(n), "name": n, "en": BC[n].get("name_en", ""), "chair": BC[n].get("recommended_chair", ""),
                                "scope": BC[n].get("oversight_scope", [])} for n in chart_c]
        assert len({c["id"] for c in board["committees"]}) == len(chart_c)
    C = execs[0]
    leader = exe(C["position_tr"], B["position_tr"])
    leader = {"title": leader["title"], "en": leader["en"], "abbr": "", **{k: leader[k] for k in ("level", "resp") if k in leader}}
    kids, top, office, aides = C.get("children", []), C["position_tr"], None, []
    if kids and not any("unit_ref" in k for k in kids):
        # CEO'ya doğrudan bağlı, altında birim olmayan üst yöneticiler (CFO, COO…) → `aides` (pozisyon "lider/<slug>")
        for k in [k for k in kids if not k.get("children")]:
            x = exe(k["position_tr"], top)
            aides.append({"id": slug(x["title"]), "title": x["title"], "en": x["en"], "status": x.get("level", ""), **({"resp": x["resp"]} if "resp" in x else {})})
        kids = [k for k in kids if k.get("children")]
        assert len(kids) == 1, "CEO altında tek ara yönetici beklenir"
        office = exe(kids[0]["position_tr"], top)
        top, kids = kids[0]["position_tr"], kids[0].get("children", [])
    assert kids and all("unit_ref" in k for k in kids), "ara yöneticinin altında yalnız unit_ref beklenir"
    assert used == set(X), set(X) - used
    U = {u["id"]: u for u in src["units"]}
    refs = [k["unit_ref"] for k in kids]
    assert sorted(refs) == sorted(U) and len(set(refs)) == len(refs), "unit_ref'ler units ile tutmuyor"
    units = []
    for ref in refs:
        u = U[ref]
        missing += [ref + "." + k for k in u if k not in {"id", "name_tr", "name_en", "manager_title_tr", "manager_title_en", "reports_to", "positions"}]
        assert u.get("reports_to") == top, (ref, u.get("reports_to"), top)
        V = {"id": slug(u["name_tr"]), "name": u["name_tr"], "en": u.get("name_en", ""), "leader": u["manager_title_tr"]}
        if u.get("manager_title_en"):
            V["leaderEn"] = u["manager_title_en"]
        V["roles"] = []
        for p in u["positions"]:
            missing += [ref + "." + p["title_tr"] + "." + k for k in p if k not in {"title_tr", "title_en", "level", "responsibility"}]
            R = {"id": slug(p["title_tr"]), "title": p["title_tr"], "en": p.get("title_en", "")}
            if p.get("level"):
                R["level"] = p["level"]
            if p.get("responsibility"):
                R["resp"] = [p["responsibility"]]
            V["roles"].append(R)
        V["teams"] = []
        units.append(V)
    RB = src.get("responsibility_boundaries", {})
    missing += ["responsibility_boundaries." + k for k in RB if k not in {"in_scope", "out_of_scope", "interfaces"}]
    org = {
        "title": D["name_tr"],
        "en": D.get("name_en", ""),
        "purpose": D.get("purpose", ""),
        "reportsTo": B["position_tr"],
        "leader": leader,
        "board": board,
    }
    if office:
        org["office"] = office
    if aides:
        assert len({x["id"] for x in aides}) == len(aides)
        org["aides"] = aides
    org.update({"scope": RB.get("in_scope", []), "boundary": D.get("governance_principle", "")})
    if RB.get("out_of_scope"):
        org["exclusions"] = RB["out_of_scope"]
    org["units"] = units
    ifs = []
    for x in RB.get("interfaces", []):
        missing += ["interfaces." + k for k in x if k not in {"department", "division_of_responsibility"}]
        m = re.match(r"(\d+)\.\s*(.+)$", x["department"])
        n = int(m.group(1))
        assert 1 <= n <= len(names) and names[n - 1] == m.group(2).strip(), (x["department"], names[n - 1] if n <= len(names) else "?")
        ifs.append({"dept": f"{n:02d} - {names[n - 1]}" + (" (bu departman)" if depts[n - 1]["id"] == self_id else ""), "ours": "",
                    "theirs": x["division_of_responsibility"]})
    if ifs:
        org["interfaces"] = ifs
    st = src.get("staffing_models", [])
    for x in st:
        missing += ["staffing_models." + k for k in x if k not in {"model", "recommended_headcount_min", "recommended_headcount_max"}]
    if st:
        org["staffing"] = [{"model": x["model"], "min": x.get("recommended_headcount_min"), "max": x.get("recommended_headcount_max")} for x in st]
    plans = [k for k in src if k.endswith("_recommended_staffing")]
    assert len(plans) <= 1, plans
    for k in plans:
        co, v = k[: -len("_recommended_staffing")], src[k]
        if co not in COMPANY_NAMES:
            missing.append("COMPANY_NAMES: " + co)
            continue
        missing += [k + "." + kk for kk in v if kk not in {"total_headcount_min", "total_headcount_max", "composition"}]
        rows = [{"group": c["role_group"], "min": c["count_min"], "max": c["count_max"]} for c in v["composition"]]
        assert sum(r["min"] for r in rows) == v["total_headcount_min"] and sum(r["max"] for r in rows) == v["total_headcount_max"], "önerilen kadro toplamı satırlarla tutmuyor"
        org["staffPlan"] = {"min": v["total_headcount_min"], "max": v["total_headcount_max"], "rows": rows}
        org["company"] = COMPANY_NAMES[co]
    return org


def org_from_g(src, missing, depts, self_id):
    missing += [k for k in src if k not in KEYS_G and not k.endswith("_role") and not k.endswith("_lifecycle")]
    D = src["department"]
    missing += ["department." + k for k in D if k not in {"code", "name_tr", "name_en", "mission", "model", "administrative_reporting_to",
                                                           "reporting_to", "functional_reporting_to", "department_head", "deputy_head",
                                                           "hierarchy_standard", "independence_principle"}]
    names = [x["name"] for x in depts]
    assert D["name_tr"] == names[[x["id"] for x in depts].index(self_id)], D["name_tr"]
    rep = D.get("administrative_reporting_to") or D.get("reporting_to")
    root = src["organization_chart"]["root"]
    missing += ["organization_chart." + k for k in src["organization_chart"] if k != "root"]
    # Kökten departman liderine tek çocuklu zincir: [idari raporlama makamı] ya da fonksiyonel hat [Yönetim Kurulu, komite]
    chain, H = [], root
    while H["title_tr"] != D["department_head"]["title_tr"]:
        assert len(H.get("children", [])) == 1, "departman liderine giden yol tek çocuklu olmalı: " + H["title_tr"]
        chain.append(H)
        H = H["children"][0]
    assert chain, "kök departman lideri olamaz"
    fr = D.get("functional_reporting_to")
    if fr:
        assert " ".join(c["title_tr"] for c in chain) == fr["title_tr"], "fonksiyonel hat şemayla tutmuyor"
        assert H.get("administrative_reporting_to") and H["administrative_reporting_to"] in rep["title_tr"], "idari raporlama şemayla tutmuyor"
    else:
        # "Ticari İşler Başkanı / CCO" gibi kısaltmalı makam adı şemada kısaltmasız geçebilir
        assert len(chain) == 1 and chain[0]["title_tr"] in (rep["title_tr"], rep["title_tr"].split(" / ")[0].strip()), "kök ≠ raporlama makamı"
    refs = [c["unit_ref"] for c in H.get("children", [])]
    assert len(refs) == len(H.get("children", [])), "departman liderinin altında yalnız unit_ref beklenir"
    U = {u["id"]: u for u in src["units"]}
    assert sorted(refs) == sorted(U) and len(set(refs)) == len(refs), "unit_ref'ler units ile tutmuyor"
    org = {
        "title": D["name_tr"],
        "en": D.get("name_en", ""),
        "purpose": D.get("mission", ""),
        "reportsTo": rep["title_tr"],
        "leader": {"title": H["title_tr"], "en": H.get("title_en", "") or D["department_head"].get("title_en", ""), "abbr": ""},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    if D.get("model"):
        org["model"] = D["model"]
    if src.get("organization"):
        org["company"] = src["organization"]
    if D.get("hierarchy_standard"):
        org["levels"] = D["hierarchy_standard"]
    if fr:
        org["functional"] = {"title": fr["title_tr"], "en": fr.get("title_en", ""), "relationship": chain[-1].get("relationship", "")}
    if D.get("independence_principle"):
        org["boundary"] = D["independence_principle"]
    # Departman liderine bağlı, birimi olmayan yönetim pozisyonları (direktör yardımcısı, yönetici müşavir…) → `aides`
    aides = []
    if D.get("deputy_head"):
        x = D["deputy_head"]
        aides.append({"id": slug(x["title_tr"]), "title": x["title_tr"], "en": x.get("title_en", ""), "status": x.get("status", "")})
    LS = src.get("department_leadership", [])
    for x in LS:
        missing += ["department_leadership." + x.get("id", "?") + "." + k for k in x
                    if k not in {"id", "title_tr", "title_en", "level", "reports_to", "reports_administratively_to", "reports_functionally_to",
                                 "responsibilities", "status"}]
    head = [x for x in LS if x.get("id") == H.get("id")]
    assert len(head) <= 1
    if head:
        ra = head[0].get("reports_to") or head[0].get("reports_administratively_to")
        assert head[0]["title_tr"] == H["title_tr"] and ra in (chain[-1].get("id"), H.get("administrative_reporting_to")), "department_leadership lideri şemayla tutmuyor"
        if head[0].get("reports_functionally_to"):
            assert fr and head[0]["reports_functionally_to"] == fr["title_tr"], "fonksiyonel raporlama tutmuyor"
        if head[0].get("responsibilities"):
            org["leader"]["resp"] = head[0]["responsibilities"]
    for x in LS:
        if x in head:
            continue
        assert x.get("reports_to") == H.get("id"), "departman yönetiminde lidere bağlı olmayan pozisyon: " + x.get("id", "?")
        a = {"id": slug(x["title_tr"]), "title": x["title_tr"], "en": x.get("title_en", ""), "status": x.get("status", "")}
        if x.get("responsibilities"):
            a["resp"] = x["responsibilities"]
        aides.append(a)
    assert len({a["id"] for a in aides}) == len(aides)
    if aides:
        org["aides"] = aides
    if src.get("scope_exclusions"):
        org["exclusions"] = src["scope_exclusions"]
    for ref in refs:
        u = U[ref]
        missing += [ref + "." + k for k in u if k not in {"id", "name_tr", "name_en", "activation_rule", "manager", "teams", "responsibilities"}]
        V = {"id": u["id"], "name": u["name_tr"], "en": u.get("name_en", ""), "leader": u["manager"]["title_tr"]}
        if u["manager"].get("title_en"):
            V["leaderEn"] = u["manager"]["title_en"]
        if u.get("responsibilities"):
            V["resp"] = u["responsibilities"]
        if u.get("activation_rule"):
            V["optional"] = u["activation_rule"]
        V["teams"] = []
        for t in u["teams"]:
            missing += [ref + "." + t["name_tr"] + "." + k for k in t if k not in {"name_tr", "name_en", "lead", "positions"}]
            P = t["positions"]
            T = {"id": slug(t["name_tr"]), "name": t["name_tr"], "en": t.get("name_en", "")}
            if t.get("lead"):
                leads = []
                T["manager"] = t["lead"]["title_tr"]
                if t["lead"].get("title_en"):
                    T["managerEn"] = t["lead"]["title_en"]
            else:
                leads = [p for p in P if "Takım Lideri" in p["title_tr"]]
                assert len(leads) <= 1, (ref, t["name_tr"], leads)
                if leads:
                    T["manager"] = leads[0]["title_tr"]
            T["roles"] = [{"id": slug(p["title_tr"]), "title": p["title_tr"], "en": p.get("title_en", "")} for p in P if p not in leads]
            V["teams"].append(T)
        org["units"].append(V)
    matrix = []
    for k in [k for k in src if k.endswith("_role")]:
        r = src[k]
        missing += [k + "." + kk for kk in r if kk not in {"title_tr", "title_en", "organizational_model", "responsibilities"}]
        matrix.append({"id": slug(r["title_tr"]), "title": r["title_tr"], "en": r.get("title_en", ""), "model": r.get("organizational_model", ""),
                       "resp": r.get("responsibilities", [])})
    assert len({m["id"] for m in matrix}) == len(matrix)
    if matrix:
        org["matrix"] = matrix
    ifs = []
    for x in src.get("cross_department_boundaries", []) + src.get("department_boundaries", []):
        dk = "other_department" if "other_department" in x else "interface_department"
        ours = [k for k in x if k.endswith("_owns") and k != "other_department_owns"]
        missing += [k for k in x if k not in {"process", dk, "other_department_owns"} and k not in ours]
        assert len(ours) == 1, x
        m = re.match(r"(\d+)\s*-\s*(.+)$", x[dk])
        label = x[dk]
        if m:
            n, nm = int(m.group(1)), m.group(2).strip()
            assert 1 <= n <= len(names), x[dk]
            if names[n - 1] != nm:
                assert DEPT_ALIASES.get(nm) == depts[n - 1]["id"], (x[dk], names[n - 1])
            label = f"{n:02d} - {names[n - 1]}"
        row = {"dept": label}
        if x.get("process"):
            row["process"] = x["process"]
        row.update({"ours": x[ours[0]], "theirs": x.get("other_department_owns", "")})
        ifs.append(row)
    if ifs:
        org["interfaces"] = ifs
    if "title_standard" in src:
        org["titles"] = [{"level": x.get("level", ""), "tr": x["title_tr"], "en": x.get("title_en", "")} for x in src["title_standard"]]
    st = src.get("staffing_models", [])
    for x in st:
        missing += ["staffing_models." + k for k in x if k not in {"model", "recommended_structure"}]
    if st:
        org["staffing"] = [{"model": x["model"], "text": x.get("recommended_structure", "")} for x in st]
    S = src.get("organization_summary")
    if S:
        missing += ["organization_summary." + k for k in S
                    if k not in {"department_heads", "unit_count", "unit_manager_count", "team_count", "team_lead_count",
                                 "specialist_position_types", "staffing_note"}]
        nt = sum(len(u["teams"]) for u in org["units"])
        nl = sum(1 for u in org["units"] for t in u["teams"] if t.get("manager"))
        nr = sum(len(t["roles"]) for u in org["units"] for t in u["teams"]) + sum(len(u.get("roles", [])) for u in org["units"])
        for k, v in (("department_heads", 1), ("unit_count", len(org["units"])), ("unit_manager_count", len(org["units"])),
                     ("team_count", nt), ("team_lead_count", nl), ("specialist_position_types", nr)):
            assert S.get(k, v) == v, f"organization_summary.{k} = {S.get(k)}, şemadan {v}"
        if S.get("staffing_note"):
            org["staffNote"] = S["staffing_note"]
    gm = src.get("governance_model", [])
    if gm:
        cols = []
        for x in gm:
            cols += [k for k in x if k != "subject" and k not in cols]
        missing += ["AUTH_NAMES: " + k for k in cols if k not in AUTH_NAMES]
        org["authority"] = {"cols": [AUTH_NAMES.get(k, k) for k in cols],
                            "rows": [{"subject": x["subject"], "vals": [x.get(k, "") for k in cols]} for x in gm]}
    co = src.get("content_ownership", [])
    for x in co:
        missing += ["content_ownership." + k for k in x if k not in {"content_type", "primary_owner"}]
    if co:
        org["ownership"] = [{"type": x["content_type"], "owner": x["primary_owner"]} for x in co]
    lcs = []
    for k in [k for k in src if k.endswith("_lifecycle")]:
        if k not in LIFECYCLE_NAMES:
            missing.append("LIFECYCLE_NAMES: " + k)
            continue
        for x in src[k]:
            missing += [k + "." + kk for kk in x if kk not in {"stage", "name_tr", "primary_owner", "output"}]
        lcs.append({"title": LIFECYCLE_NAMES[k], "rows": [{"stage": x["stage"], "name": x["name_tr"], "owner": x.get("primary_owner", ""),
                                                            "output": x.get("output", "")} for x in src[k]]})
    if lcs:
        org["lifecycles"] = lcs
    tl = src.get("three_lines_model", [])
    for x in tl:
        missing += ["three_lines_model." + k for k in x if k not in {"line", "name_tr", "owner", "responsibility"}]
    if tl:
        org["lines"] = [{"line": x["line"], "name": x["name_tr"], "owner": x["owner"], "resp": x.get("responsibility", "")} for x in tl]
    notes = src.get("implementation_notes") or src.get("notes")
    if notes:
        org["notes"] = notes
    return org

KEYS_H = {"code", "name_tr", "name_en", "organization_model", "reports_to", "purpose", "head", "hierarchy_standard", "units",
          "governance", "scope_boundaries", "staffing_guidance", "organization_summary", "independence_principle",
          "operating_principle"}


def org_from_h(src, missing, depts, self_id):
    missing += [k for k in src if k not in {"schema_version", "document", "department"}]
    D = src["department"]
    missing += ["department." + k for k in D if k not in KEYS_H]
    names = [x["name"] for x in depts]
    no = f"{[x['id'] for x in depts].index(self_id) + 1:02d}"
    assert D["name_tr"] == names[int(no) - 1], D["name_tr"]
    assert D.get("code", no) == no, D.get("code")
    Doc = src.get("document", {})
    missing += ["document." + k for k in Doc if k not in {"name", "created_at", "language"}]
    assert Doc.get("name", no + " - " + D["name_tr"]).startswith(no + " - " + D["name_tr"]), Doc.get("name")
    Hd = D["head"]
    missing += ["head." + k for k in Hd if k not in {"position_code", "title_tr", "title_en", "alternative_executive_title",
                                                    "alternative_executive_titles", "reports_to", "direct_reports",
                                                    "key_accountabilities", "accountabilities"}]
    assert not ("key_accountabilities" in Hd and "accountabilities" in Hd), "head: iki görev listesi"
    assert not ("alternative_executive_title" in Hd and "alternative_executive_titles" in Hd), "head: iki alternatif unvan alanı"
    alt = Hd.get("alternative_executive_title") or Hd.get("alternative_executive_titles")
    rep = D["reports_to"]
    missing += ["reports_to." + k for k in rep if k not in {"title_tr", "title_en", "primary", "functional_access"}]
    fa = rep.get("functional_access", [])
    if "primary" in rep:
        assert "title_tr" not in rep, "reports_to: primary ile title_tr birlikte"
        rep = rep["primary"]
        missing += ["reports_to.primary." + k for k in rep if k not in {"title_tr", "title_en"}]
    up = Hd.get("reports_to", rep["title_tr"])
    same = up.split(" / ")[0].strip() == rep["title_tr"].split(" / ")[0].strip()
    # Lider başka makama bağlıysa bu yalnız alternatif (üst yönetim) unvanıyla açıklanabilir: lider o unvanı alırsa head.reports_to'ya bağlanır
    assert same or alt, "head.reports_to ≠ reports_to (alternatif unvan yok)"
    pcs = []

    def pos_chk(x, boss, where):
        missing.extend(where + "." + k for k in x if k not in {"position_code", "title_tr", "title_en", "reports_to"})
        if x.get("position_code"):
            pcs.append(x["position_code"])
        assert not (x.get("reports_to") and boss) or x["reports_to"] == boss, f"{where}: reports_to {x.get('reports_to')} ≠ {boss}"

    if Hd.get("position_code"):
        pcs.append(Hd["position_code"])
    codes = [u["unit_code"] for u in D["units"]]
    assert len(set(codes)) == len(codes) and sorted(Hd.get("direct_reports", codes)) == sorted(codes), "direct_reports birimlerle tutmuyor"
    org = {
        "title": D["name_tr"],
        "en": D.get("name_en", ""),
        "purpose": D.get("purpose", ""),
        "reportsTo": rep["title_tr"],
        "leader": {"title": Hd["title_tr"], "en": Hd.get("title_en", ""), "abbr": ""},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    if alt:
        org["leader"]["alt"] = alt
        if not same:
            org["leader"]["altUp"] = up
    if Hd.get("key_accountabilities") or Hd.get("accountabilities"):
        org["leader"]["resp"] = Hd.get("key_accountabilities") or Hd["accountabilities"]
    if D.get("organization_model"):
        org["model"] = D["organization_model"]
    if D.get("hierarchy_standard"):
        org["levels"] = D["hierarchy_standard"]
    if fa:
        org["functional"] = {"title": ", ".join(fa), "en": "", "relationship": "Doğrudan fonksiyonel erişim"}
    if D.get("independence_principle") or D.get("operating_principle"):
        org["bounds"] = [D[k] for k in ("independence_principle", "operating_principle") if D.get(k)]
    for u in D["units"]:
        missing += [u["unit_code"] + "." + k for k in u if k not in {"unit_code", "name_tr", "name_en", "manager", "mission", "teams"}]
        pos_chk(u["manager"], Hd.get("position_code"), u["unit_code"] + ".manager")
        V = {"id": u["unit_code"], "name": u["name_tr"], "en": u.get("name_en", ""), "leader": u["manager"]["title_tr"]}
        if u["manager"].get("title_en"):
            V["leaderEn"] = u["manager"]["title_en"]
        if u.get("mission"):
            V["resp"] = [u["mission"]]
        V["teams"] = []
        for t in u["teams"]:
            missing += [u["unit_code"] + "." + t["name_tr"] + "." + k for k in t
                        if k not in {"team_code", "name_tr", "name_en", "lead", "positions", "responsibilities"}]
            assert t.get("team_code", u["unit_code"] + ".").startswith(u["unit_code"] + "."), t.get("team_code")
            T = {"id": slug(t["name_tr"]), "name": t["name_tr"], "en": t.get("name_en", "")}
            if t.get("lead"):
                pos_chk(t["lead"], u["manager"].get("position_code"), t.get("team_code", T["id"]) + ".lead")
                T["manager"] = t["lead"]["title_tr"]
                if t["lead"].get("title_en"):
                    T["managerEn"] = t["lead"]["title_en"]
            if t.get("responsibilities"):
                T["resp"] = t["responsibilities"]
            for x in t["positions"]:
                pos_chk(x, (t.get("lead") or u["manager"]).get("position_code"), t.get("team_code", T["id"]) + "." + x["title_tr"])
            T["roles"] = [{"id": slug(x["title_tr"]), "title": x["title_tr"], "en": x.get("title_en", "")} for x in t["positions"]]
            V["teams"].append(T)
        org["units"].append(V)
    assert len(set(pcs)) == len(pcs), "position_code tekrarı"
    G = D.get("governance", {})
    missing += ["governance." + k for k in G if k not in {"core_kpis", "cadence"}]
    if G.get("core_kpis"):
        org["kpis"] = [{"name": "Temel KPI'lar", "items": G["core_kpis"]}]
    for x in G.get("cadence", []):
        missing += ["cadence." + k for k in x if k not in {"forum", "focus"}]
    if G.get("cadence"):
        org["cadence"] = [{"forum": x["forum"], "focus": x.get("focus", "")} for x in G["cadence"]]
    ifs = if_rows(D.get("scope_boundaries", {}), missing, depts, self_id)
    if ifs:
        org["interfaces"] = ifs
    SG = D.get("staffing_guidance")
    if SG:
        missing += ["staffing_guidance." + k for k in SG
                    if k not in {"model", "minimum_core_headcount", "minimum_core_headcount_note", "capacity_drivers"}]
        nl = sum(1 for u in org["units"] for x in u["teams"] if x.get("manager"))
        if SG.get("minimum_core_headcount") is not None:
            assert SG["minimum_core_headcount"] == 1 + len(org["units"]) + nl, f"asgari çekirdek kadro {SG['minimum_core_headcount']} ≠ 1 + birim + ekip yöneticisi"
        org["staffGuide"] = {"model": SG.get("model", ""), "min": SG.get("minimum_core_headcount"),
                             "note": SG.get("minimum_core_headcount_note", ""), "drivers": SG.get("capacity_drivers", [])}
    S = D.get("organization_summary")
    if S:
        missing += ["organization_summary." + k for k in S if k not in {"department_heads", "units", "team_leads", "specialist_role_types", "core_principle"}]
        nl = sum(1 for u in org["units"] for x in u["teams"] if x.get("manager"))
        nr = sum(len(x["roles"]) for u in org["units"] for x in u["teams"])
        for k, v in (("department_heads", 1), ("units", len(org["units"])), ("team_leads", nl), ("specialist_role_types", nr)):
            assert S.get(k, v) == v, f"organization_summary.{k} = {S.get(k)}, şemadan {v}"
        if S.get("core_principle"):
            org["boundary"] = S["core_principle"]
    return org


# I: 22 ve 23 — units, head, reports_to kök düzeyde; roller "Türkçe / English" metni
KEYS_I = {"schema_version", "document", "department", "reports_to", "head", "hierarchy_standard", "units", "governance",
          "scope_boundaries", "staffing_guidance", "organization_summary"}
# I: staffing_guidance metin notları → "Kadro planlaması" kartında etiketli paragraf
STAFF_NOTES = {
    "shift_note": "Vardiya",
    "executive_assistant_ratio": "Yönetici asistanı oranı",
    "confidentiality_principle": "Gizlilik ilkesi",
    "outsourcing_principle": "Dış kaynak ilkesi",
}
# Görev/sınır niteliğindeki kadro notları → staffGuide.policies (DP_DUTIES kapalıyken gizli; kullanıcı kararı 2026-10-29)
STAFF_POLICIES = {"confidentiality_principle", "outsourcing_principle"}


# I: "NN - Ad" (birden çoksa " / " ile) ya da DEPT_ALIASES'teki numarasız kısa ad → departman id'leri
def dept_ref(s, depts):
    ids = []
    for part in s.split(" / "):
        part = part.strip()
        m = re.match(r"^(\d\d) - (.+)$", part)
        if m:
            n, nm = int(m.group(1)), m.group(2)
            assert 1 <= n <= len(depts) and (nm == depts[n - 1]["name"] or DEPT_ALIASES.get(nm) == depts[n - 1]["id"]), part
            ids.append(depts[n - 1]["id"])
        else:
            assert part in DEPT_ALIASES, "DEPT_ALIASES: " + part
            ids.append(DEPT_ALIASES[part])
    return ids


def org_from_i(src, missing, depts, self_id):
    missing += [k for k in src if k not in KEYS_I]
    names = {d["id"]: f"{n + 1:02d} - {d['name']}" for n, d in enumerate(depts)}
    no = f"{[x['id'] for x in depts].index(self_id) + 1:02d}"
    D = src["department"]
    missing += ["department." + k for k in D if k not in {"code", "name_tr", "name_en", "operating_model", "purpose"}]
    assert D["name_tr"] == depts[int(no) - 1]["name"] and D.get("code", no) == no, (D.get("code"), D["name_tr"])
    Doc = src.get("document", {})
    missing += ["document." + k for k in Doc if k not in {"type", "language", "created_at", "project"}]
    assert Doc.get("type", "department_organization_model") == "department_organization_model", Doc.get("type")
    R = src["reports_to"]
    missing += ["reports_to." + k for k in R if k not in {"primary", "administrative_alternative", "independent_escalation",
                                                        "functional_alignment", "governance_coordination"}]
    Hd = src["head"]
    missing += ["head." + k for k in Hd if k not in {"position_code", "title_tr", "title_en", "alternative_executive_title",
                                                    "direct_reports", "accountabilities"}]
    org = {
        "title": D["name_tr"],
        "en": D.get("name_en", ""),
        "purpose": D.get("purpose", ""),
        "reportsTo": R["primary"],
        "leader": {"title": Hd["title_tr"], "en": Hd.get("title_en", ""), "abbr": ""},
        "scope": [],
        "boundary": "",
        "units": [],
    }
    if Hd.get("alternative_executive_title"):
        org["leader"]["alt"] = Hd["alternative_executive_title"]
    # Asıl makam dışındaki bağlılıklar lider düğümünde etiketli çip olur
    up = [[lbl, ", ".join(R[k]) if isinstance(R[k], list) else R[k]] for k, lbl in (
        ("administrative_alternative", "Alternatif idari bağlılık"), ("independent_escalation", "Bağımsız eskalasyon"),
        ("governance_coordination", "Yönetişim koordinasyonu")) if R.get(k)]
    if up:
        org["leader"]["upNotes"] = up
    if Hd.get("accountabilities"):
        org["leader"]["resp"] = Hd["accountabilities"]
    if D.get("operating_model"):
        org["model"] = D["operating_model"]
    if R.get("functional_alignment"):
        org["functional"] = {"title": R["functional_alignment"], "en": "", "relationship": "Fonksiyonel hizalanma"}
    HS = src.get("hierarchy_standard", {})
    missing += ["hierarchy_standard." + k for k in HS if k != "levels"]
    LV = HS.get("levels", [])
    for x in LV:
        missing += ["levels." + k for k in x if k not in {"level", "role", "scope"}]
    assert [x["level"] for x in LV] == list(range(1, len(LV) + 1)), "hierarchy_standard.levels sırası"
    if LV:
        org["levels"] = [x["role"] for x in LV]
    if any(x.get("scope") for x in LV):
        org["levelScopes"] = [{"role": x["role"], "scope": x.get("scope", "")} for x in LV]
    pcs = [Hd["position_code"]] if Hd.get("position_code") else []
    mgrs = []
    for u in src["units"]:
        missing += [u["unit_code"] + "." + k for k in u if k not in {"unit_code", "name_tr", "name_en", "manager", "teams"}]
        M = u["manager"]
        missing += [u["unit_code"] + ".manager." + k for k in M if k not in {"position_code", "title_tr", "title_en"}]
        mgrs.append(M.get("position_code"))
        V = {"id": u["unit_code"], "name": u["name_tr"], "en": u.get("name_en", ""), "leader": M["title_tr"]}
        if M.get("title_en"):
            V["leaderEn"] = M["title_en"]
        V["teams"] = []
        for x in u["teams"]:
            missing += [x["team_code"] + "." + k for k in x if k not in {"team_code", "name_tr", "name_en", "lead", "roles"}]
            assert x["team_code"].startswith(u["unit_code"] + "."), x["team_code"]
            T = {"id": slug(x["name_tr"]), "name": x["name_tr"], "en": x.get("name_en", "")}
            if x.get("lead"):
                L = x["lead"]
                missing += [x["team_code"] + ".lead." + k for k in L if k not in {"position_code", "title_tr", "title_en"}]
                pcs.append(L.get("position_code"))
                T["manager"] = L["title_tr"]
                if L.get("title_en"):
                    T["managerEn"] = L["title_en"]
            T["roles"] = []
            for r in x["roles"]:
                tr_en = r.split(" / ")
                assert len(tr_en) == 2, r
                T["roles"].append({"id": slug(tr_en[0]), "title": tr_en[0].strip(), "en": tr_en[1].strip()})
            V["teams"].append(T)
        org["units"].append(V)
    pcs += mgrs
    pcs = [x for x in pcs if x]
    assert len(set(pcs)) == len(pcs), "position_code tekrarı"
    assert sorted(Hd.get("direct_reports", mgrs)) == sorted(mgrs), "direct_reports birim müdürleriyle tutmuyor"
    G = src.get("governance", {})
    missing += ["governance." + k for k in G if k not in {"core_kpis", "cadences"}]
    if G.get("core_kpis"):
        org["kpis"] = [{"name": "Temel KPI'lar", "items": G["core_kpis"]}]
    for x in G.get("cadences", []):
        missing += ["cadences." + k for k in x if k not in {"frequency", "forum", "focus"}]
    if G.get("cadences"):
        org["cadence"] = [{"forum": x["forum"], "focus": x.get("focus", ""), "freq": x.get("frequency", "")} for x in G["cadences"]]
    rows = []
    for x in src.get("scope_boundaries", []):
        missing += ["scope_boundaries." + k for k in x if k not in {"adjacent_department", "boundary"}]
        rows.append({"dept": " · ".join(names[i] for i in dept_ref(x["adjacent_department"], depts)), "ours": "", "theirs": x["boundary"]})
    if rows:
        org["interfaces"] = rows
    nu = len(org["units"])
    nl = sum(1 for u in org["units"] for x in u["teams"] if x.get("manager"))
    nt = sum(len(u["teams"]) for u in org["units"])
    nr = sum(len(x["roles"]) for u in org["units"] for x in u["teams"])
    SG = src.get("staffing_guidance", {})
    missing += ["staffing_guidance." + k for k in SG
                if k not in {"minimum_core_headcount", "minimum_core_composition", "specialist_staffing"} | set(STAFF_NOTES)]
    C = SG.get("minimum_core_composition", {})
    missing += ["minimum_core_composition." + k for k in C if k not in {"director", "unit_managers", "team_leads"}]
    assert (C.get("director", 1), C.get("unit_managers", nu), C.get("team_leads", nl)) == (1, nu, nl), C
    if SG.get("minimum_core_headcount") is not None:
        assert SG["minimum_core_headcount"] == 1 + nu + nl, f"asgari çekirdek kadro {SG['minimum_core_headcount']} ≠ 1 + birim + takım lideri"
    if SG:
        org["staffGuide"] = {"model": SG.get("specialist_staffing", ""), "min": SG.get("minimum_core_headcount"),
                             "note": f"{C['director']} direktör + {C['unit_managers']} birim müdürü + {C['team_leads']} takım lideri" if C else "",
                             "drivers": []}
        notes = [[STAFF_NOTES[k], v] for k, v in SG.items() if k in STAFF_NOTES and k not in STAFF_POLICIES]
        pols = [[STAFF_NOTES[k], v] for k, v in SG.items() if k in STAFF_POLICIES]
        if notes:
            org["staffGuide"]["notes"] = notes
        if pols:
            org["staffGuide"]["policies"] = pols
    S = src.get("organization_summary", {})
    want = {"director_count": 1, "unit_count": nu, "manager_count": nu, "team_count": nt, "team_lead_count": nl,
            "specialist_role_type_count": nr, "minimum_core_headcount": 1 + nu + nl}
    missing += ["organization_summary." + k for k in S if k not in want]
    for k, v in want.items():
        assert S.get(k, v) == v, f"organization_summary.{k} = {S.get(k)}, şemadan {v}"
    return org


def std_from(S, org, depts, self_id):
    assert set(S) == {"status", "prepared_at", "note", "department", "units"}, "standard anahtarları: " + ", ".join(sorted(S))
    assert S["status"] in ("taslak", "onaylandı"), S["status"]

    def strs(v, what):
        assert isinstance(v, list) and v and all(isinstance(x, str) and x.strip() == x and x for x in v), what
        assert len(set(v)) == len(v), what + ": tekrar eden madde"
        return v

    def rng(m, what):
        assert isinstance(m["min"], int) and isinstance(m["max"], int) and 0 <= m["min"] <= m["max"], (what, m)
        return m["min"], m["max"]

    def withs(L, what, unit=None):
        out, seen = [], set()
        for c in L:
            assert set(c) == {"department", "unit", "topic"} and c["topic"].strip(), (what, c)
            ids = dept_ref(c["department"], depts)
            assert len(ids) == 1, (what, c["department"])
            did = ids[0]
            units = org["units"] if did == self_id else depts[[x["id"] for x in depts].index(did)]["org"]["units"]
            uid = ""
            if c["unit"]:
                m = [u["id"] for u in units if u["name"] == c["unit"]]
                assert len(m) == 1, f"{what}: {c['department']} departmanında '{c['unit']}' müdürlüğü yok"
                uid = m[0]
            if did == self_id:
                assert unit is not None and uid and uid != unit, f"{what}: kendi departmanından yalnız başka bir müdürlük yazılır"
            assert (did, uid) not in seen, (what, "tekrar", c)
            seen.add((did, uid))
            out.append({"dept": did, "unit": uid, "topic": c["topic"]})
        assert out, what
        return out

    def models(L, what):
        assert [m.get("model") for m in L] == ["Yalın", "Standart", "Genişletilmiş"], f"{what}: modeller Yalın, Standart, Genişletilmiş"
        r = [rng(m, what) for m in L]
        assert r[0][0] <= r[1][0] <= r[2][0] and r[0][1] <= r[1][1] <= r[2][1], f"{what}: Yalın ≤ Standart ≤ Genişletilmiş olmalı {r}"
        return [{"model": m["model"], "min": m["min"], "max": m["max"]} for m in L], r

    # dpPos sırası: birim lideri, birime bağlı roller, ekip yöneticisi + rolleri
    def positions(u):
        P = [(u["id"], u["leader"], u.get("leaderEn"))] + [(u["id"] + "/" + r["id"], r["title"], r.get("en")) for r in u.get("roles", [])]
        for t in u["teams"]:
            ti = u["id"] + "/" + t["id"]
            if t.get("manager"):
                P.append((ti, t["manager"], t.get("managerEn")))
            P += [(ti + "/" + r["id"], r["title"], r.get("en")) for r in t["roles"]]
        return P

    U = S["units"]
    assert [x.get("unit_id") for x in U] == [u["id"] for u in org["units"]], "standard.units şemadaki müdürlüklerle aynı sırada olmalı"
    by_level, sums = {}, [0, 0, 0, 0, 0, 0]
    for x, u in zip(U, org["units"]):
        w = f"standard.units[{u['id']}]"
        assert set(x) == {"unit_id", "name_tr", "responsibilities", "authorities", "collaborations", "kpis", "title_standard",
                          "staffing_models", "recommended_staffing"}, w + ": anahtarlar"
        assert x["name_tr"] == u["name"], (w, x["name_tr"], u["name"])
        P = positions(u)
        ts, rs = x["title_standard"], x["recommended_staffing"]
        assert [r.get("position") for r in ts] == [p[0] for p in P], w + ".title_standard: her pozisyon şema sırasıyla bir kez"
        assert [r.get("position") for r in rs] == [p[0] for p in P], w + ".recommended_staffing: her pozisyon şema sırasıyla bir kez"
        pos = []
        for p, a, b in zip(P, ts, rs):
            assert set(a) == {"position", "level", "title_tr", "title_en"} and a["title_tr"] == p[1] == b["title_tr"], (w, a, b)
            assert a["level"].strip() and a["title_en"].strip() and (not p[2] or p[2] == a["title_en"]), (w, a, p[2])
            assert set(b) == {"position", "title_tr", "min", "max"}, (w, b)
            lo, hi = rng(b, w)
            assert lo >= 1, (w, b)
            lv = by_level.setdefault(a["level"], [0, 0])
            lv[0] += lo
            lv[1] += hi
            pos.append({"id": p[0], "level": a["level"], "en": a["title_en"], "min": lo, "max": hi})
        st, r = models(x["staffing_models"], w)
        assert r[1] == (sum(p["min"] for p in pos), sum(p["max"] for p in pos)), \
            f"{w}: Standart model önerilen kadro toplamı olmalı ({sum(p['min'] for p in pos)}-{sum(p['max'] for p in pos)})"
        for i, v in enumerate(r[0] + r[2]):
            sums[i] += v
        u["std"] = {"resp": strs(x["responsibilities"], w), "auth": strs(x["authorities"], w),
                    "with": withs(x["collaborations"], w + ".collaborations", u["id"]), "kpis": strs(x["kpis"], w), "pos": pos,
                    "staffing": st}
    Dp = S["department"]
    w = "standard.department"
    opt = {"kpis": "kpis", "title_standard": "titles", "staffing_models": "staffing", "recommended_staffing": "staffPlan"}
    want = {"responsibilities", "authorities", "collaborations"} | {k for k, v in opt.items() if not org.get(v)}
    assert set(Dp) == want, f"{w} anahtarları {sorted(want)} olmalı (departman JSON'unda karşılığı olanlar yazılmaz)"
    std = {"status": S["status"], "resp": strs(Dp["responsibilities"], w), "auth": strs(Dp["authorities"], w),
           "with": withs(Dp["collaborations"], w + ".collaborations")}
    if "kpis" in Dp:
        std["kpis"] = strs(Dp["kpis"], w + ".kpis")
    if "title_standard" in Dp:
        assert all(set(r) == {"level", "title_tr", "title_en"} and all(r[k].strip() for k in r) for r in Dp["title_standard"]), w
        std["titles"] = [{"level": r["level"], "tr": r["title_tr"], "en": r["title_en"]} for r in Dp["title_standard"]]
    aides = org.get("aides", [])
    fixed = 1 + ("office" in org) + len(org.get("matrix", []))
    mg = (fixed + sum(not re.search(r"opsiyonel|birleştirilebilir", a.get("status") or "", re.I) for a in aides), fixed + len(aides))
    if "recommended_staffing" in Dp:
        R = Dp["recommended_staffing"]
        assert set(R) == {"total_min", "total_max", "composition"}, w
        rows = [{"group": c["role_group"], "min": c["min"], "max": c["max"]} for c in R["composition"]]
        assert rows[0]["group"] == "Departman yönetimi" and (rows[0]["min"], rows[0]["max"]) == mg, f"{w}: ilk satır Departman yönetimi {mg}"
        got = {c["group"]: [c["min"], c["max"]] for c in rows[1:]}
        assert got == by_level and len(got) == len(rows) - 1, f"{w}: seviye toplamları {by_level} olmalı"
        tot = (sum(c["min"] for c in rows), sum(c["max"] for c in rows))
        assert (R["total_min"], R["total_max"]) == tot, f"{w}: toplam {tot}"
        std["staffPlan"] = {"min": tot[0], "max": tot[1], "rows": rows}
    if "staffing_models" in Dp:
        st, r = models(Dp["staffing_models"], w)
        tot = (mg[0] + sum(v[0] for v in by_level.values()), mg[1] + sum(v[1] for v in by_level.values()))
        exp = [(mg[0] + sums[0], mg[1] + sums[1]), tot, (mg[1] + sums[2], mg[1] + sums[3])]
        assert r == exp, f"{w}.staffing_models: {exp} olmalı"
        std["staffing"] = st
    org["std"] = std


def org_from(src, depts, self_id):
    missing = []
    if "units" in (src.get("department") or {}):
        org = org_from_h(src, missing, depts, self_id)
    elif "units" in src and "head" in src:
        org = org_from_i(src, missing, depts, self_id)
    elif "organization_chart" in src and "executive_positions" not in src:
        org = org_from_g(src, missing, depts, self_id)
    elif "organization_chart" in src:
        org = org_from_f(src, missing, depts, self_id)
    elif "department" in src:
        org = org_from_a(src, missing)
    elif "positions" in src:
        org = org_from_e(src, missing, depts, self_id)
    elif "department_name" in src:
        org = org_from_b(src, missing)
    elif "departman" in src:
        org = org_from_c(src, missing, depts)
    elif "organizasyon" in src:
        org = org_from_d(src, missing)
    else:
        sys.exit("Tanınmayan departman JSON biçimi")
    if missing:
        sys.exit("Türkçe karşılığı ya da işlenişi tanımsız anahtarlar: " + ", ".join(missing))
    check_units(org["units"])
    return org


def main():
    html, dept, jpath = sys.argv[1:4]
    want = sys.argv[4] if len(sys.argv) > 4 else None
    raw = open(html, "rb").read()
    if want:
        assert hashlib.md5(raw).hexdigest() == want, "dosya değişmiş"
    t = raw.decode("utf-8")
    key = "const DATA="
    i = t.index(key) + len(key)
    data, end = json.JSONDecoder().raw_decode(t[i:])
    assert json.dumps(data, ensure_ascii=False) == t[i:i + end], "serileştirme farklı"
    idx = [n for n, x in enumerate(data["departments"]) if x["id"] == dept]
    assert len(idx) == 1, dept
    src = json.load(open(jpath, encoding="utf-8"))
    std = src.pop("standard", None)
    D = src.get("department") or {}
    code = src.get("department_code") or src.get("departman_kodu") or D.get("code") or D.get("id")
    if code is not None:
        assert int(code) == idx[0] + 1, f"departman numarası uyuşmuyor: {code} ≠ {idx[0] + 1:02d}"
    org = org_from(src, data["departments"], dept)
    if std is not None:
        std_from(std, org, data["departments"], dept)
    data["departments"][idx[0]]["org"] = org
    t = t[:i] + json.dumps(data, ensure_ascii=False) + t[i + end:]
    open(html, "w", encoding="utf-8").write(t)
    teams = sum(len(u["teams"]) for u in org["units"])
    leads = sum(1 for u in org["units"] for x in u["teams"] if x.get("manager"))
    roles = sum(len(x["roles"]) for u in org["units"] for x in u["teams"]) + sum(len(u.get("roles", [])) for u in org["units"])
    board = 1 + len(org["board"]["roles"]) if "board" in org else 0
    comms = len(org.get("board", {}).get("committees", []))
    office = 1 if "office" in org else 0
    print(f"{dept}: {len(org['units'])} birim, {teams} ekip ({leads} ekip lideri), {roles} rol, {board} kurul, {comms} komite, {office} ara yönetici, "
          f"{len(org.get('matrix', []))} matris rol, {len(org.get('aides', []))} yönetim pozisyonu, {'standart: ' + org['std']['status'] + ', ' if 'std' in org else ''}{1 + office + len(org['units']) + leads + roles + board + len(org.get('matrix', [])) + len(org.get('aides', []))} pozisyon")


if __name__ == "__main__":
    main()
