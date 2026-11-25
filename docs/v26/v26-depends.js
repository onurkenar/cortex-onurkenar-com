/* v26-depends — bağımlı seçimleri koruma (2026-11-23, YOL-HARITASI Faz 4 §34: "db_engine değişince
   db_provider / orm seçimi sessizce siliniyor → uyarı + onay").
   Ana betikteki setv(), bir karar değişince ona `dependsOn` ile bağlı kararları koşulsuz siler (aynı seçeneğe
   yeniden tıklayınca bile). Bu sarmalayıcı:
   - yeni seçimde de geçerli olan bağımlı değeri korur (ör. Prisma hem PostgreSQL hem MySQL'de var),
   - geçersiz kalacak bağımlı değer varsa önce onay sorar; İptal edilirse hiçbir şey değişmez,
   - aynı seçeneğe yeniden tıklamak bağımlı kararları artık silmez.
   Veri, kural ve kayıt biçimi değişmez. Test kancası: window.depLost(id, v). */
(function () {
  if (typeof setv !== "function" || typeof F === "undefined") return;
  function valid(x, v, cur) {
    let o = (x.optionMap && x.optionMap[v]) || [];
    let ok = val => o.some(p => p.value === val);
    return Array.isArray(cur) ? cur.filter(ok) : ok(cur) ? cur : undefined;
  }
  function has(cur) { return Array.isArray(cur) ? cur.length > 0 : cur != null && cur !== ""; }
  // id kararı v olursa kaybolacak bağımlı seçimler: [{f, cur, keep}]
  function plan(id, v) {
    return F.filter(x => x.dependsOn === id && has(state[x.id])).map(x => {
      let cur = state[x.id], keep = valid(x, v, cur);
      return { f: x, cur, keep };
    });
  }
  function show(x, cur) { return (Array.isArray(cur) ? cur : [cur]).map(c => lab(x, c)).join(", "); }
  window.depLost = function (id, v) {
    return plan(id, v).filter(p => !has(p.keep) || (Array.isArray(p.cur) && p.keep.length < p.cur.length))
      .map(p => p.f.label + " (" + show(p.f, p.cur) + ")");
  };
  const _sv = setv;
  setv = function (id, v, multi) {
    let P = multi ? [] : plan(id, v);
    if (!P.length || !projectReady()) return _sv.apply(this, arguments);
    let lost = window.depLost(id, v);
    if (lost.length && state[id] !== v) {
      let f = FI[id], nv = f ? lab(f, v) : v;
      if (!window.confirm("“" + nv + "” seçilirse şu kararlar bu seçimle uyumlu olmadığı için temizlenecek:\n\n• "
        + lost.join("\n• ") + "\n\nDevam edilsin mi?")) return;
    }
    let r = _sv.apply(this, arguments);
    let back = P.filter(p => has(p.keep));
    if (back.length && state[id] === v) {
      back.forEach(p => { state[p.f.id] = p.keep; });
      save();
      renderFields(); renderProgress(); renderRules();
    }
    return r;
  };
})();
