#!/usr/bin/env python3
"""Yayın kopyasında büyük verileri sıkıştırır (2026-11-11, kullanıcı kararı: "büyük veriyi dosyanın içinde sıkıştırmak").

Kullanım (yayinla.sh çağırır): python3 -I sikistir.py <kaynak.html> <çıktı.html>

Neden yayında: kaynak dosyadaki `<script>const DATA={…}` satırını bütün veri betikleri (skill, MCP, departman, Google,
Meta …) okuyup yeniden yazar; kaynak değişmez, yalnız canlıya giden kopya dönüştürülür. Cloudflare'in dosya başına
25 MiB sınırı da yalnız bu kopyaya uygulanır.

Dönüşüm:
  1. DATA'daki KEYS anahtarlarının değeri null yapılır (anahtar sırası korunur); değerleri tek JSON nesnesi olarak gzip
     (seviye 9) + base64 ile <script type="application/octet-stream" id="wpc-dataz"> içine gömülür.
  2. Ana betik (const DATA'lı) ve ondan sonraki bütün üst düzey <script> blokları type="text/x-wpc-boot" olur (id korunur);
     ana betikte DATA nesnesinden hemen sonra Object.assign(DATA, window.__WPC_Z) eklenir.
  3. <head> sonuna açılış stili ve sınıfı (html.wpcBoot → gövde gizli), </body> öncesine açıcı betik: belge
     ayrıştırılınca veriyi DecompressionStream("gzip") ile açar, JSON.parse eder, sonra bekleyen betikleri aynı sırayla
     satır içi betik olarak ekler (eklenen satır içi betik eşzamanlı çalışır; üst düzey const / let paylaşımı aynıdır),
     sınıfı kaldırır. Açılamazsa uyarı gösterir.
Denetimler: DATA bulunur ve tek; KEYS DATA'da var; betiklerin içeriği </script içermez; açıcı ve yük metninde </script ya
da <!-- yok; çıktıdaki yük geri açılınca özgün değerlerle aynı.
"""
import base64
import gzip
import json
import re
import sys

KEYS = ["skillDirectory", "skillCatalog", "mcpCatalog"]
MARK = "<script>const DATA="
BOOT_TYPE = "text/x-wpc-boot"

HEAD = ('<style id="wpc-boot-css">html.wpcBoot body{visibility:hidden}</style>'
        '<script id="wpc-boot-flag">document.documentElement.classList.add("wpcBoot")</script>\n')

LOADER = r"""<script type="application/octet-stream" id="wpc-dataz">%s</script>
<script id="wpc-boot">(async()=>{const H=document.documentElement,fail=e=>{H.classList.remove("wpcBoot");console.error(e);document.body.insertAdjacentHTML("afterbegin",'<div role="alert" style="position:fixed;inset:16px 16px auto;z-index:99999;padding:16px 20px;border-radius:12px;background:#fdeceb;color:#9f1c12;font:600 15px/1.5 system-ui,sans-serif;box-shadow:0 6px 24px rgba(0,0,0,.2)">Sayfa verisi açılamadı. Tarayıcınızı güncelleyip sayfayı yenileyin (gerekli özellik: DecompressionStream).</div>')};
try{if(document.readyState==="loading")await new Promise(r=>document.addEventListener("DOMContentLoaded",r,{once:true}));
const z=document.getElementById("wpc-dataz"),b=z.textContent.trim();let u;if(Uint8Array.fromBase64)u=Uint8Array.fromBase64(b);else{const s=atob(b);u=new Uint8Array(s.length);for(let i=0;i<s.length;i++)u[i]=s.charCodeAt(i)}
window.__WPC_Z=JSON.parse(await new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream("gzip"))).text());z.remove()}catch(e){fail(e);return}
for(const o of [...document.querySelectorAll('script[type="%s"]')]){const n=document.createElement("script");if(o.id)n.id=o.id;n.textContent=o.textContent;o.replaceWith(n)}
window.__WPC_Z=null;H.classList.remove("wpcBoot")})()</script>
"""


def fail(m):
    sys.exit("HATA (sikistir.py): " + m)


def main():
    if len(sys.argv) != 3:
        fail("kullanım: sikistir.py <kaynak.html> <çıktı.html>")
    s = open(sys.argv[1], encoding="utf-8").read()
    if s.count(MARK) != 1:
        fail("DATA satırı bulunamadı ya da birden çok")
    a = s.index(MARK)
    i = a + len(MARK)
    d, e = json.JSONDecoder().raw_decode(s, i)
    for k in KEYS:
        if k not in d:
            fail("DATA'da anahtar yok: " + k)
    pay = {k: d[k] for k in KEYS}
    rest = dict(d)
    for k in KEYS:
        rest[k] = None
    raw = json.dumps(pay, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    b64 = base64.b64encode(gzip.compress(raw, 9, mtime=0)).decode("ascii")
    loader = LOADER % (b64, BOOT_TYPE)
    if not re.fullmatch(r"[A-Za-z0-9+/=]+", b64):
        fail("yük base64 değil")
    # ana betik: DATA'yı değiştir, birleştirme satırını ekle
    head_part = s[:a]
    main_body = json.dumps(rest, ensure_ascii=False) + ";Object.assign(DATA,window.__WPC_Z);" + s[e:]
    s2 = head_part + '<script type="' + BOOT_TYPE + '">const DATA=' + main_body
    # ana betikten sonraki üst düzey betikler
    pos = len(head_part)
    end_main = s2.index("</script>", pos)
    out = [s2[:end_main + 9]]
    p = end_main + 9
    n_boot = 1
    while True:
        j = s2.find("<script", p)
        if j < 0:
            out.append(s2[p:])
            break
        k = s2.index(">", j)
        attrs = s2[j + 7:k]
        c = s2.index("</script>", k)
        if "type=" in attrs or "src=" in attrs:
            fail("beklenmeyen betik özniteliği: " + attrs[:80])
        out.append(s2[p:j] + '<script type="' + BOOT_TYPE + '"' + attrs + ">" + s2[k + 1:c] + "</script>")
        n_boot += 1
        p = c + 9
    s3 = "".join(out)
    if s3.count("</head>") != 1 or s3.count("</body>") != 1:
        fail("</head> ya da </body> tek değil")
    s3 = s3.replace("</head>", HEAD + "</head>").replace("</body>", loader + "</body>")
    # denetim: yük geri açılınca aynı
    m = re.search(r'<script type="application/octet-stream" id="wpc-dataz">([A-Za-z0-9+/=]+)</script>', s3)
    back = json.loads(gzip.decompress(base64.b64decode(m.group(1))).decode("utf-8"))
    if back != pay:
        fail("yük geri açılınca özgün veriyle aynı değil")
    open(sys.argv[2], "w", encoding="utf-8").write(s3)
    print(f"sıkıştırıldı: {', '.join(KEYS)} {len(raw)/1e6:.2f} MB → {len(b64)/1e6:.2f} MB (gzip + base64); "
          f"ertelenen betik {n_boot}; çıktı {len(s3.encode())/1e6:.2f} MB")


if __name__ == "__main__":
    main()
