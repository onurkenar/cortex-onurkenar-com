#!/bin/sh
# WP-OnKe → cortex.onurkenar.com
# 2026-11-07: ana sayfa yayın sırasında önceden sıkıştırılır (index.html.br / .gz) — Cloudflare'in 22 MB'lık
# dosyayı anlık sıkıştırması çok yavaştı. Worker (src/index.js) uygun sürümü gönderir; ETag = içerik md5.
set -eu
cd "$(dirname "$0")"
SRC=../web-proje-gelistirme.html
LIMIT=26214400  # Cloudflare statik dosya sınırı: 25 MiB
# 2026-11-11: büyük veriler (skillDirectory, skillCatalog, mcpCatalog) yayın kopyasında gzip + base64 olarak gömülür,
# tarayıcı açılışta açar (sikistir.py). Kaynak dosya değişmez; sınır yalnız yayın kopyasına uygulanır.
PREV_ETAG=$(sed -n 's/.*"\([0-9a-f]*\)".*/\1/p' src/etag.js 2>/dev/null || true)
python3 -I sikistir.py "$SRC" public/index.html.tmp
SIZE=$(wc -c < public/index.html.tmp | tr -d ' ')
if [ "$SIZE" -ge "$LIMIT" ]; then
  rm -f public/index.html.tmp
  echo "HATA: yayın kopyası $SIZE bayt — 25 MiB sınırını aşıyor, yayınlanamaz." >&2
  exit 1
fi
mv public/index.html.tmp public/index.html
echo "index.html: $SIZE bayt (sınırın %$((SIZE * 100 / LIMIT))'i; kaynak $(wc -c < "$SRC" | tr -d ' ') bayt)"
node -e '
const fs=require("fs"),z=require("zlib"),c=require("crypto");
const b=fs.readFileSync("public/index.html");
fs.writeFileSync("public/index.html.br.tmp",z.brotliCompressSync(b,{params:{[z.constants.BROTLI_PARAM_QUALITY]:11,[z.constants.BROTLI_PARAM_LGWIN]:24,[z.constants.BROTLI_PARAM_SIZE_HINT]:b.length,[z.constants.BROTLI_PARAM_MODE]:z.constants.BROTLI_MODE_TEXT}}));
fs.renameSync("public/index.html.br.tmp","public/index.html.br");
fs.writeFileSync("public/index.html.gz.tmp",z.gzipSync(b,{level:9}));
fs.renameSync("public/index.html.gz.tmp","public/index.html.gz");
const tag=c.createHash("md5").update(b).digest("hex");
fs.writeFileSync("src/etag.js","export const ETAG = \""+tag+"\";\n");
console.log("index.html.br: "+fs.statSync("public/index.html.br").size+" bayt · index.html.gz: "+fs.statSync("public/index.html.gz").size+" bayt · ETag "+tag);
'
npx wrangler deploy "$@"

# 2026-11-12: IndexNow — sayfa içeriği değiştiyse (ETag farklı) ana sayfa adresi IndexNow'a bildirilir; tek gönderim
# Bing, Yandex, Naver, Seznam ve Yep ile paylaşılır (Google katılmıyor). Değişmemiş adres gönderilmez. Anahtar dosyası
# public/<32 hex>.txt (içinde yalnız anahtar, kökte); önce canlıda erişilebildiği doğrulanır. Bildirim hatası yayını
# başarısız saymaz, yalnız uyarı yazar. Elle zorlamak için: INDEXNOW_FORCE=1 npm run yayinla
HOST=cortex.onurkenar.com
KEY=$(ls public | sed -n 's/^\([0-9a-f]\{32\}\)\.txt$/\1/p' | head -1)
NEW_ETAG=$(sed -n 's/.*"\([0-9a-f]*\)".*/\1/p' src/etag.js)
if [ -z "$KEY" ]; then
  echo "IndexNow: anahtar dosyası yok (public/<anahtar>.txt) — bildirim atlandı." >&2
elif [ "$NEW_ETAG" = "$PREV_ETAG" ] && [ "${INDEXNOW_FORCE:-0}" != "1" ]; then
  echo "IndexNow: sayfa içeriği değişmedi (ETag aynı) — bildirim gönderilmedi."
else
  LIVE=""; i=0
  while [ $i -lt 6 ]; do
    LIVE=$(curl -s -m 15 "https://$HOST/$KEY.txt" || true)
    [ "$LIVE" = "$KEY" ] && break
    i=$((i+1)); sleep 5
  done
  if [ "$LIVE" != "$KEY" ]; then
    echo "IndexNow: https://$HOST/$KEY.txt canlıda anahtarı döndürmüyor — bildirim gönderilmedi." >&2
  else
    CODE=$(curl -s -m 30 -o /dev/null -w "%{http_code}" -X POST "https://api.indexnow.org/indexnow" \
      -H "Content-Type: application/json; charset=utf-8" \
      -d "{\"host\":\"$HOST\",\"key\":\"$KEY\",\"keyLocation\":\"https://$HOST/$KEY.txt\",\"urlList\":[\"https://$HOST/\"]}" || true)
    case "$CODE" in
      200|202) echo "IndexNow: https://$HOST/ bildirildi (HTTP $CODE)." ;;
      *) echo "IndexNow: bildirim yanıtı HTTP $CODE (400 biçim, 403 anahtar, 422 alan adı / anahtar uyumsuz, 429 çok sık) — yayın etkilenmedi." >&2 ;;
    esac
  fi
fi
