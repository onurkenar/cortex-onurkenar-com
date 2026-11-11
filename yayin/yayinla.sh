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
