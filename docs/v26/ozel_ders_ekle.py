# -*- coding: utf-8 -*-
"""Özel ders platformları göç kodunu uygulamaya yazar (2026-11-26).
Kullanım: python3 -I docs/v26/ozel_ders_ekle.py web-proje-gelistirme.html
- docs/v26/v26-tutoring.js → ana betikte /*V26-TUTOR:BEGIN*/…/*V26-TUTOR:END*/ (function one(f){ öncesi; varsa yerinde yenilenir)
- kanca: ocMig sonunda ocProofMig çağrısının arkasına ocTutorMig (yalnız eksikse)
Veri (alan tanımları) docs/pazarlama/kilavuz-alanlari.json → alan_ekle.py ile yazılır. Tekrar çalıştırılabilir."""
import hashlib, os, re, sys

hp = sys.argv[1]
h = open(hp, encoding='utf-8').read()
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'v26-tutoring.js'), encoding='utf-8').read().strip()
for bad in ('</script', '<!--'):
    if bad in src:
        sys.exit('HATA: kaynakta ' + bad)
B, E = '/*V26-TUTOR:BEGIN*/', '/*V26-TUTOR:END*/'
block = B + '\n' + src + '\n' + E + '\n'
if h.count(B) == 1 and h.count(E) == 1:
    h = re.sub(re.escape(B) + r'.*?' + re.escape(E) + r'\n?', lambda m: block, h, flags=re.S)
elif h.count(B) == 0 and h.count(E) == 0:
    A = '\nfunction one(f){'  # satır başındaki tanım (yorumlarda da geçiyor)
    if h.count(A) != 1:
        sys.exit('HATA: function one(f){ bulunamadı ya da birden çok')
    h = h.replace(A, '\n' + block + A[1:])
else:
    sys.exit('HATA: V26-TUTOR işaretleri bozuk')
OLD = 'if(typeof ocProofMig==="function")ocProofMig(st)'
HOOK = OLD + ';if(typeof ocTutorMig==="function")ocTutorMig(st)'
if HOOK not in h:
    if h.count(OLD) != 1:
        sys.exit('HATA: ocProofMig kancası bulunamadı ya da birden çok')
    h = h.replace(OLD, HOOK)
elif h.count(HOOK) != 1:
    sys.exit('HATA: ocTutorMig kancası birden çok')
open(hp, 'w', encoding='utf-8').write(h)
print('tamam · md5', hashlib.md5(h.encode('utf-8')).hexdigest(), '· boyut', len(h.encode('utf-8')))
