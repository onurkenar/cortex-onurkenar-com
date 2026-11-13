"""Para birimi biçimi (2026-11-14): tutar alanlarında 30.000,00 TL / USD / EUR — docs/v26/v26-currency.{js,css}.
Kullanım: python3 -I docs/v26/para_birimi_ekle.py <html>
Tekrar çalıştırılabilir: bloklar varsa kaynaktan yerinde yenilenir, kancalar yalnız eksikse eklenir.
Kancalar: one() tutar kutusunu çizer (f.money); ruleBase değeri curShow ile biçimler; accCell / accBad / accList
accounts satırındaki tutarı (a.money) işler; mkNum USD / EUR'yu da okur; mkIssues TL dışı plan tutarını uyarır."""
import os, re, sys
H = sys.argv[1]
D = os.path.dirname(os.path.abspath(__file__))
s = open(H, encoding="utf-8").read()
js = open(os.path.join(D, "v26-currency.js"), encoding="utf-8").read().strip()
css = open(os.path.join(D, "v26-currency.css"), encoding="utf-8").read().strip()
for t in (js, css):
    assert "</script" not in t and "<!--" not in t

def once(a, b):
    global s
    if b in s:
        return
    assert s.count(a) == 1, (s.count(a), a[:80])
    s = s.replace(a, b)

# 1) JS bloğu: one()'ın hemen önünde (FI tanımlıdır; mkNum / mkIssues / accCell daha önce bildirilir)
B, E_ = "/*V26-CURRENCY:BEGIN*/", "/*V26-CURRENCY:END*/"
blk = B + "\n" + js + "\n" + E_ + "\n"
if B in s:
    s = re.sub(re.escape(B) + r".*?" + re.escape(E_) + r"\n", lambda m: blk, s, count=1, flags=re.S)
else:
    a = "\nfunction one(f){if(f.derive"
    assert s.count(a) == 1
    s = s.replace(a, "\n" + blk + a[1:])
# 2) CSS bloğu: v26-mobile'dan önce
st = '<style id="v26-currency">' + css + "</style>"
if '<style id="v26-currency">' in s:
    s = re.sub(r'<style id="v26-currency">.*?</style>', lambda m: st, s, count=1, flags=re.S)
else:
    a = '<style id="v26-mobile">'
    assert s.count(a) == 1
    s = s.replace(a, st + a)
# 3) kancalar
once('else if(f.type==="textarea")c=`<textarea', 'else if(f.money)c=curInput(f);else if(f.type==="textarea")c=`<textarea')
once('let v=f.type==="accounts"?accText(f)', 'let v=f.money?curShow(state[f.id]):f.type==="accounts"?accText(f)')
once('function accCell(f,a){', 'function accCell(f,a){if(a.money)return curAccCell(f,a);')
once('function accBad(a,u){u=String(u||"").trim();', 'function accBad(a,u){u=String(u||"").trim();if(a.money)return !!u&&!curOk(u);')
once('.map(a=>[a.label,String(v[a.k]).trim()])', '.map(a=>[a.label,a.money?curShow(v[a.k]):String(v[a.k]).trim()])')
once('function mkNum(k){let t=mkT(k).replace(/tl|₺|\\s/gi,"");',
     'function mkNum(k){if(typeof curParse==="function"){let x=mkT(k);if(!x)return null;let r=curParse(x);return r&&r.n>0?r.n:NaN}let t=mkT(k).replace(/tl|₺|\\s/gi,"");')
once('if(Number.isNaN(mkNum("mk_labor_rate")))L.push(`Saat ücreti sayı değil (${c("mk_labor_rate")}).`);',
     'if(Number.isNaN(mkNum("mk_labor_rate")))L.push(`Saat ücreti sayı değil (${c("mk_labor_rate")}).`);if(typeof curIssues==="function")curIssues(L,c);')
open(H, "w", encoding="utf-8").write(s)
print("tamam", len(s))
