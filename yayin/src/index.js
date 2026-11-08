// cortex.onurkenar.com — ana sayfa önceden sıkıştırılmış olarak sunulur (2026-11-07).
// Neden: 22 MB'lık index.html'i Cloudflare her istekte anlık sıkıştırırken saniyede ~6 KB'a düşüyordu
// (sıkıştırmasız 116 KB/s, karşılaştırma cdnjs 1,3 MB/s). yayinla.sh yayın sırasında index.html.br ve
// index.html.gz üretir, src/etag.js'e içerik özetini yazar; bu Worker tarayıcının desteklediği sürümü
// olduğu gibi (encodeBody: "manual") gönderir, ETag ile değişmeyen sayfada 304 döner.
// Diğer bütün yollar statik dosya olarak (ASSETS) sunulur; güvenlik başlıkları public/_headers ile aynı tutulmalı.
import { ETAG } from "./etag.js";

const SEC = {
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "strict-origin-when-cross-origin",
  "Content-Security-Policy": "frame-ancestors 'none'",
  "X-Frame-Options": "DENY",
  "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
  "Strict-Transport-Security": "max-age=31536000",
};

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname !== "/" && url.pathname !== "/index.html") return env.ASSETS.fetch(request);
    if (request.method !== "GET" && request.method !== "HEAD") {
      return new Response("Method Not Allowed", { status: 405, headers: { Allow: "GET, HEAD", ...SEC } });
    }
    // Cloudflare Worker'a Accept-Encoding'i normalleştirilmiş verir; istemcinin gerçek başlığı cf.clientAcceptEncoding'te.
    const ae = (request.cf && request.cf.clientAcceptEncoding) ?? request.headers.get("Accept-Encoding") ?? "";
    const enc = /\bbr\b/i.test(ae) ? "br" : /\bgzip\b/i.test(ae) ? "gzip" : "";
    const tag = `"${ETAG}${enc ? "-" + enc : ""}"`;
    const h = new Headers(SEC);
    h.set("Content-Type", "text/html; charset=utf-8");
    // no-transform: Cloudflare yanıtı açıp yeniden sıkıştırmasın (yoksa hazır .br yerine anlık sıkıştırma yapıp ETag'i siliyordu).
    h.set("Cache-Control", "public, max-age=0, must-revalidate, no-transform");
    h.set("ETag", tag);
    h.set("Vary", "Accept-Encoding");
    const inm = request.headers.get("If-None-Match");
    if (inm && inm.split(",").map((s) => s.trim().replace(/^W\//, "")).includes(tag)) {
      return new Response(null, { status: 304, headers: h });
    }
    if (enc) h.set("Content-Encoding", enc);
    const send = (body) => new Response(request.method === "HEAD" ? null : body, { status: 200, headers: h, encodeBody: enc ? "manual" : "automatic" });
    // Kenar önbelleği: statik dosya deposu büyük dosyayı ~200 KB/s veriyordu; hazır sürüm PoP önbelleğinde tutulur.
    // Anahtar içerik özetini taşır, her yayında kendiliğinden yenilenir. Saklanan gövde ham bayttır (Content-Encoding'siz).
    const cache = caches.default;
    const key = new Request(`${url.origin}/__cortex-cache/${ETAG}/${enc || "identity"}`);
    const hit = await cache.match(key);
    if (hit) return send(hit.body);
    const file = enc === "br" ? "/index.html.br" : enc === "gzip" ? "/index.html.gz" : "/index.html";
    const r = await env.ASSETS.fetch(new Request(new URL(file, url.origin), { method: "GET" }));
    if (!r.ok) return env.ASSETS.fetch(request);
    const [a, b] = r.body.tee();
    ctx.waitUntil(cache.put(key, new Response(b, { headers: { "Content-Type": "application/octet-stream", "Cache-Control": "public, max-age=31536000, immutable" } })).catch(() => {}));
    return new Response(request.method === "HEAD" ? null : a, {
      status: 200,
      headers: h,
      encodeBody: enc ? "manual" : "automatic",
    });
  },
};
