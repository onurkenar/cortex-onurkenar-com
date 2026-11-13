"""Ek açıklama (2026-11-13): her karara isteğe bağlı açıklama — docs/v26/v26-notes.{js,css}.
Kullanım: python3 -I docs/v26/ek_aciklama_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kancalar yalnız eksikse eklenir.
Kancalar: rule() sonucu fnAdd'den geçer; one() seçeneklerden sonra fnBox çizer; exState / exImport
state.fieldNotes'u alan sahibine göre böler (fieldAgents gibi); auTxt kontrol listesi ve çoklu seçimde notu ekler."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-notes.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-notes.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1) JS bloğu: one()'ın hemen önünde
B, E_ = "/*V26-NOTES:BEGIN*/", "/*V26-NOTES:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
# 2) CSS bloğu: v26-mobile'dan önce
st = '<style id="v26-notes">' + css + "</style>"
if '<style id="v26-notes">' in s:
    s = re.sub(r'<style id="v26-notes">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
# 3) kancalar
once('return x.length?r+" "+x.join(" "):r}', 'return fnAdd(f,x.length?r+" "+x.join(" "):r)}')
once('${hiddenNote(f)}${faRow(f)}', '${hiddenNote(f)}${fnBox(f)}${faRow(f)}')
once('function exState(p){let o={};Object.keys(state).forEach(k=>{if(k!=="fieldAgents"&&exOwn(k)===p)o[k]=state[k]});let fa=state.fieldAgents;if(fa&&typeof fa==="object"){let x={};Object.keys(fa).forEach(k=>{if(exOwn(k)===p)x[k]=fa[k]});if(Object.keys(x).length)o.fieldAgents=x}return o}',
     'function exState(p){let o={};Object.keys(state).forEach(k=>{if(k!=="fieldAgents"&&k!=="fieldNotes"&&exOwn(k)===p)o[k]=state[k]});["fieldAgents","fieldNotes"].forEach(n=>{let fa=state[n];if(fa&&typeof fa==="object"){let x={};Object.keys(fa).forEach(k=>{if(exOwn(k)===p)x[k]=fa[k]});if(Object.keys(x).length)o[n]=x}});return o}')
once('if(Object.keys(state).some(k=>k!=="fieldAgents"&&exOwn(k)===p&&!empty(state[k]))',
     'if(Object.keys(state).some(k=>k!=="fieldAgents"&&k!=="fieldNotes"&&exOwn(k)===p&&!empty(state[k]))')
once('let s={...state},fa={...(s.fieldAgents||{})};Object.keys(s).forEach(k=>{if(k!=="fieldAgents"&&exOwn(k)===p)delete s[k]});Object.keys(fa).forEach(k=>{if(exOwn(k)===p)delete fa[k]});Object.entries(d.state).forEach(([k,v])=>{if(k==="fieldAgents"){if(v&&typeof v==="object")Object.assign(fa,v)}else if(exOwn(k)===p)s[k]=v});if(Object.keys(fa).length)s.fieldAgents=fa;else delete s.fieldAgents;',
     'let s={...state},fa={...(s.fieldAgents||{})},fnn={...(s.fieldNotes&&typeof s.fieldNotes==="object"?s.fieldNotes:{})};Object.keys(s).forEach(k=>{if(k!=="fieldAgents"&&k!=="fieldNotes"&&exOwn(k)===p)delete s[k]});Object.keys(fa).forEach(k=>{if(exOwn(k)===p)delete fa[k]});Object.keys(fnn).forEach(k=>{if(exOwn(k)===p)delete fnn[k]});Object.entries(d.state).forEach(([k,v])=>{if(k==="fieldAgents"){if(v&&typeof v==="object")Object.assign(fa,v)}else if(k==="fieldNotes"){if(v&&typeof v==="object")Object.keys(v).forEach(x=>{if(exOwn(x)===p&&typeof v[x]==="string")fnn[x]=v[x]})}else if(exOwn(k)===p)s[k]=v});if(Object.keys(fa).length)s.fieldAgents=fa;else delete s.fieldAgents;if(Object.keys(fnn).length)s.fieldNotes=fnn;else delete s.fieldNotes;')
once('return `   ${i+1}. ${o.label} — ${o.ruleDetail}${m.length?` [Gerekli veri: ${m.map(k=>A[k]||k).join(", ")}. Bu erişim verilmedi: kontrolü “Veri yok” olarak işaretle ve verinin nasıl alınacağını yaz.]`:""}`}).join("\\n")}if(f.type==="multiselect")return ruleBase(f)+auSel(f).filter(o=>o.ruleDetail).map(o=>"\\n   - "+o.ruleDetail).join("");return rule(f)}',
     'return `   ${i+1}. ${o.label} — ${o.ruleDetail}${m.length?` [Gerekli veri: ${m.map(k=>A[k]||k).join(", ")}. Bu erişim verilmedi: kontrolü “Veri yok” olarak işaretle ve verinin nasıl alınacağını yaz.]`:""}`}).join("\\n")+auNote(f)}if(f.type==="multiselect")return ruleBase(f)+auSel(f).filter(o=>o.ruleDetail).map(o=>"\\n   - "+o.ruleDetail).join("")+auNote(f);return rule(f)}function auNote(f){let t=fnClean(fnGet(f.id));return t?"\\n   Ek açıklama: "+t:""}')
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
