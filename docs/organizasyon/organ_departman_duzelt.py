"""Komite, kurul ve çalışma grubu modellerindeki departman kodlarını DATA.departments sırasına (01–23) uydurur.

Kullanım (proje kökünden, önce _yedek/organizasyon/ altına kopya alın; sonra komite_ekle.py → kurul_ekle.py →
calisma_grubu_ekle.py sırasıyla yeniden çalıştırın):
    python3 -I docs/organizasyon/organ_departman_duzelt.py docs/organizasyon/komite-modeli.json \
        docs/organizasyon/kurul-modeli.json docs/organizasyon/calisma-grubu-modeli.json

Neden (kullanıcı kararı 2026-10-30, "sırayı tutmasını sağlayacak şekilde revizeleri yap"): kaynak modeller bizim listemize
çok yakın bir departman listesiyle yazılmış, sapmalar sistematik:
  - 07 İç Denetim değil "Kurumsal Strateji / İş Geliştirme" anlamında kullanılmış (Strateji / CEO Ofisi sekreteryalı
    organlarda); bizde strateji 01'in, iş geliştirme 08'in içinde → 07 çıkarılır, gerekiyorsa 01 eklenir.
  - 06 Uyum, Kurumsal Risk ve İç Kontrol (KVKK uyumu dahil) hiç kullanılmamış; yerine 16 (Etik Komitesi), 14 ve 16 (Denetim
    Komitesi) yazılmış ya da hiç yazılmamış → üye / başkan / sekreterya metninde Risk, Uyum, İç Kontrol, KVKK geçen organa 06.
  - Üye listesinde adı geçen ama kodu yazılmamış departmanlar eklenir; departmanın kendi verisindeki fonksiyonel bağlılık
    (06 → YK Risk ve Uyum Komitesi, 07 → YK Denetim Komitesi, 21 → YK Risk / Sürdürülebilirlik Komitesi, 22 → Kurumsal Risk
    ve Güvenlik Komitesi, 23 → YK / komite / İcra Kurulu sekreteryası, 19 → CMO) ilgili organa yansıtılır.
Gerekçeler aşağıdaki tabloda organ başına yazılıdır; kodlar düzeltmeden sonra sayıca sıralanır.

Betik tekrar çalıştırılabilir: düzeltmesi zaten uygulanmış organı atlar. Bir organda kaldırılacak kod yoksa ya da eklenecek
kod zaten varsa (kısmen uygulanmış / kaynak değişmiş) durur — o organın gerekçesini kaynağa göre yeniden değerlendirin.
Dosyalar json.dumps(indent=2, ensure_ascii=False) biçiminde geri yazılır (kaynak kopyaların biçimi).
"""
import json
import sys

# organ kodu: (çıkarılacak, eklenecek, gerekçe)
FIX = {
    "KMT-01": (["07"], ["15"], "07 kaynakta Kurumsal Strateji (01'de, zaten var); daimi üye CTO/CIO → 15"),
    "KMT-02": (["07"], [], "07 kaynakta Strateji Direktörü / Yatırım Ofisi (01'de, zaten var)"),
    "KMT-03": ([], ["06", "22"], "Başkan Risk ve Uyum, sekreterya Risk ve Uyum Ofisi, üye İç Kontrol → 06; 22'nin verisinde Kurumsal Risk ve Güvenlik Komitesi"),
    "KMT-04": (["16"], ["06"], "Üyeler İK, Hukuk, İç Kontrol; sekreterya Hukuk / Uyum → 06; Siber Güvenlik üye değil"),
    "KMT-05": (["14", "16"], ["06", "07", "23"], "Davetli iç denetim ve İç Denetim'in YK Denetim Komitesine fonksiyonel bağlılığı → 07; iç kontrol gözetimi → 06; sekreterya Kurul Sekreteryası → 23; Kalite ve Siber Güvenlik üye değil"),
    "KMT-14": ([], ["04"], "Daimi üyelerde İK"),
    "KMT-16": ([], ["20", "22"], "Bağlı CLG-11 İş Sürekliliği tatbikat grubunda ve KRL-07'de; tesis ve fiziksel güvenlik sürekliliği"),
    "KMT-17": (["07"], [], "07 kaynakta İş Geliştirme (08'de, zaten var)"),
    "KMT-18": ([], ["19"], "Tasarım ve Yaratıcı Hizmetler CMO'ya bağlı; marka kimliği ve kampanya kreatifi"),
    "KMT-21": ([], ["03", "04"], "Daimi üyelerde Finans ve İK"),
    "KMT-22": ([], ["06", "12"], "Daimi üyelerde Hukuk / KVKK ve İç Kontrol (KVKK uyumu 06.06) ve Operasyon"),
    "KMT-23": ([], ["06"], "Daimi üyelerde Hukuk / KVKK (KVKK uyumu 06.06)"),
    "KRL-01": ([], ["06", "07", "21"], "06, 07 ve 21 Yönetim Kurulu komitelerine fonksiyonel bağlı / erişimli"),
    "KRL-02": ([], ["06", "07", "21"], "06, 07 ve 21 Yönetim Kurulu komitelerine fonksiyonel bağlı / erişimli"),
    "KRL-04": ([], ["23"], "23'te İcra Kurulu sekreteryası"),
    "KRL-05": (["07"], [], "07 kaynakta Strateji / CEO Ofisi (01'de, zaten var)"),
    "KRL-06": (["07"], ["06"], "07 kaynakta stratejik programlar (01'de, zaten var); üyelerde Risk / Uyum danışmanı → 06"),
    "KRL-07": ([], ["01", "04"], "Üyelerde İK ve ilgili şirket genel müdürü"),
    "KRL-09": (["07"], ["01", "06"], "Sekreterya Kurumsal Strateji → 01; üyelerde Hukuk / Uyum danışmanı → 06"),
    "CLG-01": (["07"], [], "07 kaynakta Strateji (01'de, zaten var)"),
    "CLG-02": (["07"], [], "07 kaynakta Kurumsal Gelişim (01'de, zaten var)"),
    "CLG-03": (["07"], [], "07 kaynakta Strateji / Yatırım (01'de, zaten var)"),
    "CLG-12": ([], ["06"], "KVKK veri envanteri ve uyum; KVKK uyumu 06.06"),
    "CLG-13": (["07"], [], "07 kaynakta İş Geliştirme (08'de, zaten var)"),
}
LISTS = {"komiteler": lambda x: x["departman_iliskileri"], "kurullar": lambda x: x["departman_iliskileri"],
         "calisma_gruplari": lambda x: x}


def main():
    done = set()
    for path in sys.argv[1:]:
        raw = open(path, encoding="utf-8").read()
        data = json.loads(raw)
        nl = raw.endswith("\n")
        assert json.dumps(data, ensure_ascii=False, indent=2) + ("\n" if nl else "") == raw, (path, "biçim farklı")
        key = next(k for k in LISTS if k in data)
        n = 0
        for it in data[key]:
            fx = FIX.get(it["kod"])
            if not fx:
                continue
            done.add(it["kod"])
            box = LISTS[key](it)
            cur, rem, add = box["departman_kodlari"], fx[0], fx[1]
            if all(c not in cur for c in rem) and all(c in cur for c in add):
                print(f"{it['kod']}: zaten uygulanmış")
                continue
            assert all(c in cur for c in rem) and all(c not in cur for c in add), (it["kod"], "kısmen uygulanmış ya da kaynak değişmiş", cur, fx)
            box["departman_kodlari"] = sorted((set(cur) - set(rem)) | set(add), key=int)
            n += 1
            print(f"{it['kod']}: {', '.join(cur)} → {', '.join(box['departman_kodlari'])}")
        open(path, "w", encoding="utf-8").write(json.dumps(data, ensure_ascii=False, indent=2) + ("\n" if nl else ""))
        print(f"{path}: {n} organ düzeltildi")
    miss = sorted(set(FIX) - done)
    assert not miss, "kaynakta bulunmayan organ: " + ", ".join(miss)


if __name__ == "__main__":
    main()
