// claude.ai Skill Dizini (Customize › Skills › Discover) — tarayıcıda çekme betiği.
//
// Resmî, oturumsuz bir API yoktur; dizin yalnız oturum açmış kullanıcıya görünür. Bu betik claude.ai'da,
// kendi oturumunuzla açık bir sekmede (ör. https://claude.ai/customize/skills) geliştirici konsolunda
// ya da Claude in Chrome'un javascript aracıyla çalıştırılır ve claude-skill-dizini.json dosyasını indirir.
// Hesabınıza ait özel skill'ler (eklentisi olmayan kayıtlar) ve kullanıcıya özel alanlar (viewer, usage)
// dosyaya yazılmaz. 3.400 civarı eklenti için birkaç dakika sürer (8 eşzamanlı istek).
//
// Sonra: dosyayı docs/skills/dizin/ altına kaynak olarak işleyin (skill_ekle.py'nin başındaki adımlar).
(async () => {
  // Kuruluş kimliği sayfanın kendi isteklerinden alınır (Skills sayfası açıkken /api/organizations/<uuid>/… istekleri yapılır).
  const org = performance.getEntriesByType('resource').map(e => (e.name.match(/\/api\/organizations\/([0-9a-f-]{36})\//) || [])[1]).find(Boolean);
  if (!org) throw new Error('Kuruluş kimliği bulunamadı: önce https://claude.ai/customize/skills sayfasını açıp yenileyin.');
  const base = `/api/organizations/${org}/library/discover/browse?sort=recent&include_added=true&limit=100`;
  let all = [], cur = null, facets = null;
  do {
    const d = await (await fetch(base + (cur ? '&cursor=' + encodeURIComponent(cur) : ''), {credentials: 'include'})).json();
    facets = facets || d.facets; all.push(...d.items); cur = d.next_cursor;
  } while (cur);
  const P = all.filter(x => x.plugin), q = P.slice(), det = {};
  const pick = o => o && {name: o.name, display_name: o.display_name, description: o.description};
  async function w() {
    while (q.length) {
      const x = q.shift(), id = x.plugin.backend_id;
      for (let t = 0; t < 3; t++) {
        const r = await fetch(`/api/organizations/${org}/plugins/${id}`, {credentials: 'include'});
        if (r.status === 429 || r.status >= 500) { await new Promise(s => setTimeout(s, 1500 * (t + 1))); continue }
        if (!r.ok) break;
        const d = await r.json();
        det[id] = {
          skills: (d.skills || []).map(s => ({name: s.name, display_name: s.display_name, description: s.description, user_invocable: s.user_invocable})),
          commands: (d.commands || []).map(pick), agents: (d.agents || []).map(pick),
          mcp: Object.entries(d.mcp_servers || {}).map(([k, v]) => ({key: k, type: v.type, url: v.url, command: v.command, args: v.args, mcpb: !!v.mcpb})),
          hooks: !!(d.hooks && Object.keys(d.hooks).length), author: d.author, publisher: d.publisher, category: d.category,
          classification: d.classification, upstream: d.upstream, version: d.version, authored_version: d.authored_version, install_count: d.install_count
        };
        break;
      }
    }
  }
  await Promise.all(Array.from({length: 8}, w));
  const items = P.map(x => { const p = x.provenance || {}; return Object.assign({
    id: x.plugin.backend_id, name: x.name, display_name: x.display_name, description: x.description, created_at: x.created_at,
    updated_at: x.updated_at, categories: x.categories, install_count_list: x.install_count, marketplace_id: p.marketplace_id,
    marketplace_name: p.marketplace_name, marketplace_display_name: p.marketplace_display_name, publisher_tier: p.publisher_tier,
    author_list: p.author}, det[x.plugin.backend_id] || {missing: true}) });
  const out = {source: 'claude.ai › Customize › Skills › Discover', fetched: new Date().toISOString(), total: items.length, facets: facets.categories, items};
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(out)], {type: 'application/json'}));
  a.download = 'claude-skill-dizini.json'; document.body.appendChild(a); a.click(); a.remove();
  console.log('Skill dizini:', items.length, 'eklenti,', items.filter(i => i.missing).length, 'eksik detay');
})();
