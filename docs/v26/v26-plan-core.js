/* 8. İçerik Planlama — kural ve prompt üreticileri (2026-11-15). Ana betikte, mkRuleGroups'tan önce durur (renderRules ilk
   açılışta bunları çağırır). Bölümler DATA'da area:"marketing", sub:"plan" → AREA "plan" (docs/icerik-planlama/kaynak.json →
   plan_alani_ekle.py). Kaynak docs/v26/v26-plan-core.js → docs/v26/icerik_planlama_ekle.py */
var IP_HEAD="Aşağıdaki kurallar içerik ve reklam planının (İçerik ve Reklam Planı Şablonu) genel ayarları için bağlayıcıdır: seri no öneki, dönem bilgileri, dönem süzgeci, takvim notu ve plan sayfasındaki site bağlantıları. Plan dosyasını üretirken ve içerik kayıtlarını (blog, paylaşım, mailing, etkinlik) hazırlarken bu ayarlara uy.";
function ipRuleGroups(){return areaS("plan").map(s=>({s,rs:F.filter(f=>f.section===s.id&&isset(f)&&shown(f)).map(ruleAg).filter(Boolean)})).filter(g=>g.rs.length)}
function ipPrompt(ip){return ip&&ip.length?"\n\nİÇERİK PLANI AYARLARI\n"+IP_HEAD+"\n"+mkRuleText(ip):""}
