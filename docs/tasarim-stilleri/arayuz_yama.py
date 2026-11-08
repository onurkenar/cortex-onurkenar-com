import sys,re,json
p,js_p,lib_p,css2_p=sys.argv[1:5]
s=open(p,encoding='utf-8').read()
i=s.find('<script>const DATA=')+19;D,end=json.JSONDecoder().raw_decode(s,i)
head,data,tail=s[:i],s[i:end],s[end:]
def conv(c):
    c=re.sub(r'(-?)(?<![\w.])(\d*\.?\d+)cqw',lambda m:'calc(%s%s * var(--q))'%('-1 * ' if m.group(1) else '',m.group(2)),c)
    return c.replace('100CQW','100cqw')
nc=lambda c:re.sub(r'/\*.*?\*/','',c,flags=re.S)
css2=conv(open(css2_p,encoding='utf-8').read().rstrip('\n'));assert nc(css2).count('cqw')==1
js=open(js_p,encoding='utf-8').read().rstrip('\n');lib=open(lib_p,encoding='utf-8').read().rstrip('\n')
for bad in ('</script','<!--'):
    assert bad not in js and bad not in lib
a=tail.find('/* Tasarım kütüphanesi (DATA.designStyleKit)');endm='dsZoom(t.dataset.dszF,t.dataset.dszV,t.dataset.dszI)},true);'
b=tail.find(endm);assert a>0 and b>a and tail.count(endm)==1
tail=tail[:a]+js+tail[b+len(endm):]
m='<script id="v26-design-library">\n';k=tail.find(m);assert k>0 and tail.count(m)==1;e=tail.find('\n</script>',k)
tail=tail[:k+len(m)]+lib+tail[e:]
m='<style id="v26-design-library">\n';k=head.find(m);assert k>0;e=head.find('\n</style>',k)
head=head[:k+len(m)]+css2+head[e:]
R=[('ruleGroups.insertAdjacentHTML("beforeend",agRuleGroups());','ruleGroups.insertAdjacentHTML("beforeend",dsRuleGroups()+agRuleGroups());',1),
   ('${mkPrompt(mg)}${agPrompt()}','${mkPrompt(mg)}${dsPrompt()}${agPrompt()}',1),
   ('...mcPf(),claudePrompt:master.value','...mcPf(),...dsPf(),claudePrompt:master.value',1),
   ('...mcPf(),...auPf(),claudePrompt:master.value','...mcPf(),...auPf(),...dsPf(),claudePrompt:master.value',1)]
for x,y,n in R:
    assert tail.count(x)==n,(x,tail.count(x));tail=tail.replace(x,y)
d1='Bu ayarlar kararlarınızı değiştirmez.</li>'
assert head.count(d1)==1
head=head.replace(d1,d1+'<li><b>Tasarım Parametreleri ve teknik çıktı:</b> yoğunluk, ızgara, yüzey, görsel işleme, hizalama, açılış, bölüm ritmi, kapsayıcı, etkileşim yoğunluğu ve gezinme kararları ana stile göre önerilir (yalnız “Öneriyi uygula” ile). Layout kararında gerekçeli, kural tabanlı öneri puanı ve sayfa türüne göre ayrı layout seçimi vardır. Bu kararlardan tasarım yapılandırması (JSON), CSS token\'ları ve Claude promptundaki “TASARIM ŞARTNAMESİ” üretilir; renk ve font Ortak Bilgiler\'den gelir.</li>')
open(p,'w',encoding='utf-8').write(head+data+tail);print('ok')
