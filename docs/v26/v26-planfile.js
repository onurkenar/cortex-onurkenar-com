/* Plan Dosyası düzeltmeleri (2026-11-15, kullanıcı kararı: "İçerik Planlama" menüsüne geçmeden önce Plan Dosyası
   aksaklıkları düzeltilsin). mkPlanData'nın çıktısı sarmalanır; temel kod değişmez.
   1) Pazarlama belgeleri şablonun kodlarıyla: ANA ve EK-01…EK-17 (KILAVUZ 18.13); "Marka planları" belge değil, çok
      markalı yapıdır → belgeye yazılmaz. Tek markada pazarlama.marka = önek ve markalar[] tek satır.
   2) Aktarılmayan kararlar bağlanır: kılavuz metinleri (kilavuz.amac / akis / gorsel / seri / dogruluk / kontrol / sonrasi /
      govde ← ilgili kararların kural metni), marka.konum ← Kısa Tanıtım, ads.cta ← Ana CTA, ads.kurulum ← Google Ads
      Asgari Hesap Ayarları, ads.butceTakvim (yalnız hafta içi yayında), hukuk.notlar ← kapsam / durum seti / dayanaklar,
      etkinlikler.tatiller ← dönem yıllarının resmî tatilleri, etkinlikler.kanallar'a seçilen ek kanallar (standart plan
      kanal anahtarlarına bağlı olduğu için var olanlar silinmez).
   3) mkMods: şablonun her zaman açtığı sekmelerden seçime göre boş gelecek olanlar "(boş gelir)" diye işaretlenir.
   Kaynak docs/v26/v26-planfile.js → docs/v26/plan_dosyasi_ekle.py */
(function(){
if(typeof mkPlanData!=="function")return;
const ok=id=>{let f=FI[id];return !!f&&shown(f)&&isset(f)};
const clean=s=>String(s||"").replace(/\s*\(önerilen\)/g,"").trim();
const rl=id=>{if(!ok(id))return "";let r=rule(FI[id]);return r?String(r).trim():""};
const KLV={amac:["mk_goals","mk_north_star"],akis:["mk_flow","mk_flow_legal_required","mk_approvers","mk_brief_delivery","mk_pub_steps"],
 gorsel:["mk_visual_source","mk_visual_meta","mk_blog_cover","mk_logo_use","mk_fz","mk_cta_position","mk_sizes","mk_file_naming"],
 seri:["mk_series"],dogruluk:["mk_ads_claims","mk_ai_content"],kontrol:["mk_text_lengths","mk_blog_limits","mk_emoji","mk_sales_tone","mk_links","mk_utm"],
 sonrasi:["mk_post_check","mk_report_rhythm","mk_measure_scope","mk_backup"]};
const EK={main:["ANA","Kurumsal Pazarlama Planı","Ana plan"],competitor:["EK-02","Rakip Analizi","Araştırma (EK-01…04)"],
 persona:["EK-04","ICP ve Persona Kartları","Araştırma (EK-01…04)"],channel:["EK-11","Dijital Pazarlama Yıllık Aktivite Takvimi","Operasyon (EK-11…17)"],
 budget:["EK-16","Yıllık Pazarlama Bütçesi Planlama Eki","Operasyon (EK-11…17)"]};
const EV_CH={website:{k:"web",ad:"Web sitesi",kaynak:"website",ortam:"referral"},partners:{k:"partner",ad:"İş ortakları",kaynak:"partner",ortam:"referral"},sms:{k:"sms",ad:"SMS",kaynak:"sms",ortam:"sms"}};
const pad=n=>String(n).padStart(2,"0"),iso=(y,m,d)=>y+"-"+pad(m)+"-"+pad(d);
function span(a,b){let r=[],x=new Date(a+"T00:00:00Z"),e=new Date((b||a)+"T00:00:00Z");for(let i=0;x<=e&&i<15;i++){r.push(x.toISOString().slice(0,10));x=new Date(x.getTime()+864e5)}return r}
/* donemler[] {k, ad, bas, son} (KILAVUZ 18.15): plan döneminin değdiği çeyrekler ya da aylar, tam takvim sınırlarıyla */
function periods(a,b,mode){let L=[],y=a.getUTCFullYear(),m=a.getUTCMonth();const last=(Y,M)=>new Date(Date.UTC(Y,M+1,0)).getUTCDate();
 while(y<b.getUTCFullYear()||(y===b.getUTCFullYear()&&m<=b.getUTCMonth())){
  if(mode==="month"){L.push({k:y+"-"+pad(m+1),ad:MK_AY[m]+" "+y,bas:iso(y,m+1,1),son:iso(y,m+1,last(y,m))});m++}
  else{let q=Math.floor(m/3),m0=q*3;L.push({k:y+"-Q"+(q+1),ad:y+" Q"+(q+1),bas:iso(y,m0+1,1),son:iso(y,m0+3,last(y,m0+2))});m=m0+3}
  if(m>11){m-=12;y++}}
 return L}
function holidays(years){let O=(MKT.ozelGunler||{}).liste||[],S=new Set;O.filter(g=>g.resmi).forEach(g=>years.forEach(y=>{
  if(g.yillik&&g.ay&&g.gun)span(iso(y,g.ay,g.gun),g.bitisAy?iso(y,g.bitisAy,g.bitisGun||g.gun):null).forEach(d=>S.add(d));
  else if(g.hareketli&&g.tarihler&&g.tarihler[y])span(g.tarihler[y],g.bitisler&&g.bitisler[y]).forEach(d=>S.add(d))}));return [...S].sort()}
function fix(B){
 let ad=(B.marka&&B.marka.ad)||"",onek=(B.marka&&B.marka.onek)||"";
 // marka.konum ← Kısa Tanıtım
 let tg=String(state.oc_tagline||"").trim();if(tg&&ok("oc_tagline")&&B.marka)B.marka.konum=tg;
 // 8.1 Plan & Dönem (2026-11-15): dönem açıklaması, takvim notu, dönem süzgeci, ek web siteleri
 let tx=id=>ok(id)?String(state[id]).trim():"";
 if(tx("ip_period_desc")&&B.donem)B.donem.aciklama=tx("ip_period_desc");
 if(tx("ip_cal_note"))B.takvimNotu=tx("ip_cal_note");
 let ps=mkDate(mkT("mk_period_start")),pe=ps&&mkEnd(ps),qm=ok("ip_quarters")?state.ip_quarters:"";
 if(ps&&pe&&(qm==="quarter"||qm==="month"))B.donemler=periods(ps,pe,qm);
 if(B.marka){let rows=String(tx("ip_sites")).split(/\r?\n/).map(x=>x.split("|").map(y=>y.trim())).filter(r=>r.length>1&&/^https?:\/\//i.test(r[1])).map(r=>({ad:r[0]||r[1].replace(/^https?:\/\//i,""),url:r[1]}));
  if(rows.length){let ms=B.marka.site&&/^https?:\/\//i.test(B.marka.site)?[{ad:B.marka.site.replace(/^https?:\/\/(www\.)?/i,"").replace(/\/$/,""),url:B.marka.site}]:[];B.marka.siteler=ms.concat(rows.filter(r=>!ms.some(m=>m.url===r.url)))}}
 // kılavuz metinleri
 let K={};Object.entries(KLV).forEach(([k,ids])=>{let L=ids.map(rl).filter(Boolean);if(L.length)K[k]=L});
 if(ok("mk_blog_length"))K.govde=mkLabs("mk_blog_length").map(clean).join(", ");
 if(Object.keys(K).length)B.kilavuz=Object.assign({},B.kilavuz,K);
 // Google Ads
 if(mkHas("mk_ads_channels","google")&&B.ads&&Array.isArray(B.ads.kampanyalar)){
  if(ok("oc_cta_primary"))B.ads.cta=clean(mkLabs("oc_cta_primary")[0]);
  if(ok("gg_ads_settings")){let f=FI.gg_ads_settings,v=state.gg_ads_settings;B.ads.kurulum=opts(f).filter(o=>v.includes(o.value)).map(o=>o.ruleDetail||clean(o.label))}
  let st=mkDate(mkT("mk_period_start")),en=st&&mkEnd(st);
  if(st&&en&&mkV("mk_ads_days")==="weekdays"){B.ads.butceTakvim=mkMonths(st,en).map(([y,m])=>({ay:MK_AY[m]+" "+y,gun:mkWorkdays(y,m)}));B.ads.butceTakvimNot="Reklamlar yalnız hafta içi yayında; aktif gün sayısı her ayın iş günüdür. Resmî tatiller düşülmedi."}}
 // Hukuk notları
 if(B.hukuk){let N=[];if(ok("mk_legal_scope"))N.push("Hukuka gidecek içerikler: "+mkLabs("mk_legal_scope").map(clean).join(", ")+".");
  if(mkV("mk_legal_statuses")==="two")N.push("Durum seti: yalnız Uygun ve Uygun değil kullanılır (şablonun Beklemede, İncelemede, Şartlı uygun, Düzeltme gerekli durumları kullanılmaz).");
  if(ok("mk_legal_basis"))N.push("Değerlendirme dayanakları: "+mkLabs("mk_legal_basis").map(clean).join(", ")+".");
  if(N.length)B.hukuk.notlar=(B.hukuk.notlar||[]).filter(x=>!N.includes(x)).concat(N)}
 // Etkinlikler: tatiller ve ek kanallar
 if(B.etkinlikler){let st=mkDate(mkT("mk_period_start")),en=st&&mkEnd(st),y0=st?st.getUTCFullYear():new Date().getFullYear(),y1=en?en.getUTCFullYear()+1:y0+1,Y=[];for(let y=y0;y<=y1;y++)Y.push(y);
  let H=holidays(Y);if(H.length)B.etkinlikler.tatiller=H;
  let ch=mkV("mk_evt_channels");if(Array.isArray(ch)){let L=B.etkinlikler.kanallar||[];ch.forEach(c=>{let x=EV_CH[c];if(x&&!L.some(k=>k.k===x.k))L.push(Object.assign({},x))});B.etkinlikler.kanallar=L}}
 // Pazarlama belgeleri
 if(B.pazarlama){let docs=(mkV("mk_plan_docs")||[]).filter(d=>EK[d]),per=clean(mkLabs("mk_plan_period")[0]||""),multi=mkV("mk_brand_structure")==="multi"||(mkV("mk_plan_docs")||[]).includes("brand_plans");
  B.pazarlama.belgeler=docs.map(d=>({kod:EK[d][0],ad:EK[d][1],grup:EK[d][2],bolum:"",sahip:"",onayci:"",periyot:per,ozet:"",sablon:""}));
  if(!multi&&onek&&!/[{}]/.test(onek)){B.pazarlama.marka=onek;B.pazarlama.markalar=[{kod:onek,ad,donem:B.pazarlama.donem||"",onay:"",klasor:"",belge:{}}]}
  if(!B.pazarlama.belgeler.length)delete B.pazarlama}
 return B}
const _pd=mkPlanData;mkPlanData=function(){let B=_pd.apply(this,arguments);try{fix(B)}catch(e){console.error("Plan Dosyası düzeltmesi",e)}return B};
const _mm=mkMods;mkMods=function(B){let L=_mm.apply(this,arguments),sc=mkV("mk_measure_scope"),has=x=>Array.isArray(sc)&&sc.includes(x),E0={"Google Ads":!mkHas("mk_ads_channels","google"),"Meta Ads":!mkHas("mk_ads_channels","meta"),"Takipçiler":Array.isArray(sc)&&sc.length>0&&!has("followers"),"Sosyal İstatistik":Array.isArray(sc)&&sc.length>0&&!has("social")&&!has("post")};
 return L.map(x=>E0[x]?x+" (boş gelir)":x)};
window.pfHolidays=holidays;window.PF_EK=EK;
})();
