/* v26-textcheck — metin kararlarında yumuşak biçim denetimi (2026-11-23, YOL-HARITASI: "mk_prefix, mk_period_start …
   alanlarında yumuşak doğrulama (şu an yalnız dışa aktarım kartında uyarı var)").
   TC tablosundaki metin kararının kutusu yazarken denetlenir: biçim tutmazsa kutu aria-invalid="true" olur ve altında
   uyarı çıkar. Değer yine kaydedilir (url / accounts kutularındaki gibi); veri, kural ve kayıt değişmez.
   renderFields ve refreshField sarmalanır. Yeni alan eklemek için TC'ye {test(v) → "" | uyarı} yazın.
   Test kancası: window.tcMsg(id, değer). */
(function () {
  if (typeof renderFields !== "function") return;
  const digits = v => v.replace(/\D/g, "");
  function phone(v, wa) {
    if (/[^0-9+()\-.\s\/]/.test(v)) return "Telefon numarasında yalnız rakam, boşluk, +, ( ) ve - kullanılır.";
    let d = digits(v), intl = /^\s*(\+|00)/.test(v);
    if (d.length < 7 || d.length > 15) return "Telefon numarası 7–15 haneli olmalı.";
    if (/^\s*\+90/.test(v) && d.length !== 12) return "+90'dan sonra 10 hane olmalı. Örnek: +90 212 000 00 00";
    if (!intl && d[0] === "0" && d.length !== 11) return "0 ile başlayan numara 11 haneli olmalı. Örnek: 0212 000 00 00";
    if (wa && !intl) return "wa.me bağlantısı için numarayı ülke koduyla yazın. Örnek: +90 532 000 00 00";
    return "";
  }
  const TC = {
    mk_prefix: v => /^[A-Z]{2,5}$/.test(v) ? "" : "2–5 büyük Latin harfi olmalı; Türkçe karakter, rakam ve boşluk olmaz. Örnek: GLM",
    mk_period_start: v => {
      let m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(v);
      if (!m) return "YYYY-AA-GG biçiminde yazın. Örnek: 2026-10-05";
      let d = new Date(Date.UTC(+m[1], +m[2] - 1, +m[3]));
      return d.getUTCMonth() === +m[2] - 1 && d.getUTCDate() === +m[3] ? "" : "Takvimde olmayan bir tarih.";
    },
    mk_sms_sender: v => v.length > 11 ? "En çok 11 karakter olmalı (şu an " + v.length + ")."
      : /^[A-Za-z0-9 .\-]+$/.test(v) ? "" : "Yalnız Latin harfi, rakam, boşluk, nokta ve tire kullanın; Türkçe karakter çoğu operatörde görünmez.",
    mk_utm_campaign: v => /^[a-z0-9_\-]+$/.test(v) ? "" : "Küçük harf, rakam, alt çizgi ve tire kullanın; boşluk ve Türkçe karakter olmasın. Örnek: 2026-q4",
    oc_phone: v => phone(v, false),
    oc_support_phone: v => phone(v, false),
    oc_whatsapp: v => phone(v, true)
  };
  window.tcMsg = function (id, v) { v = String(v || "").trim(); return v && TC[id] ? TC[id](v) : ""; };
  function paint(inp, id) {
    let msg = window.tcMsg(id, inp.value), h = inp.nextElementSibling;
    if (!h || !h.classList.contains("tcHint")) {
      h = document.createElement("small");
      h.className = "fontInfo tcHint"; h.id = "tc-" + id; h.setAttribute("aria-live", "polite");
      inp.after(h); inp.setAttribute("aria-describedby", h.id);
    }
    inp.setAttribute("aria-invalid", msg ? "true" : "false");
    h.innerHTML = msg ? '<span class="fiWarn">Biçim:</span> ' + E(msg) : "";
  }
  function scan() {
    Object.keys(TC).forEach(id => {
      document.querySelectorAll('.field[data-field-id="' + id + '"] input.control').forEach(inp => {
        if (inp.type !== "text" && inp.type !== "") return;
        if (!inp.dataset.tc) { inp.dataset.tc = "1"; inp.addEventListener("input", () => paint(inp, id)); }
        paint(inp, id);
      });
    });
  }
  window.tcScan = scan;
  const _rf = renderFields;
  renderFields = function () { let r = _rf.apply(this, arguments); scan(); return r; };
  if (typeof refreshField === "function") {
    const _rr = refreshField;
    refreshField = function () { let r = _rr.apply(this, arguments); scan(); return r; };
  }
  scan();
})();
