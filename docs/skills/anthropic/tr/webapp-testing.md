
# Web Uygulaması Testi

Yerel web uygulamalarını test etmek için yerel (native) Python Playwright betikleri yaz.

**Kullanılabilir Yardımcı Betikler**:
- `scripts/with_server.py` - Sunucu yaşam döngüsünü yönetir (birden çok sunucuyu destekler)

**Kullanımı görmek için betikleri her zaman önce `--help` ile çalıştır**. Betiği önce çalıştırmayı deneyip özelleştirilmiş bir çözümün kesinlikle gerekli olduğunu görmeden kaynak kodunu OKUMA. Bu betikler çok büyük olabilir ve bu yüzden bağlam pencereni kirletebilir. Bağlam pencerene alınmak için değil, doğrudan kara kutu betikler olarak çağrılmak için vardırlar.

## Karar Ağacı: Yaklaşımını Seçmek

```
User task → Is it static HTML?
    ├─ Yes → Read HTML file directly to identify selectors
    │         ├─ Success → Write Playwright script using selectors
    │         └─ Fails/Incomplete → Treat as dynamic (below)
    │
    └─ No (dynamic webapp) → Is the server already running?
        ├─ No → Run: python scripts/with_server.py --help
        │        Then use the helper + write simplified Playwright script
        │
        └─ Yes → Reconnaissance-then-action:
            1. Navigate and wait for networkidle
            2. Take screenshot or inspect DOM
            3. Identify selectors from rendered state
            4. Execute actions with discovered selectors
```

## Örnek: with_server.py Kullanımı

Bir sunucu başlatmak için önce `--help` çalıştır, ardından yardımcıyı kullan:

**Tek sunucu:**
```bash
python scripts/with_server.py --server "npm run dev" --port 5173 -- python your_automation.py
```

**Birden çok sunucu (ör. backend + frontend):**
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python your_automation.py
```

Bir otomasyon betiği oluşturmak için yalnızca Playwright mantığını ekle (sunucular otomatik olarak yönetilir):
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True) # Always launch chromium in headless mode
    page = browser.new_page()
    page.goto('http://localhost:5173') # Server already running and ready
    page.wait_for_load_state('networkidle') # CRITICAL: Wait for JS to execute
    # ... your automation logic
    browser.close()
```

## Önce Keşif, Sonra Eylem Kalıbı

1. **Çizilmiş (render edilmiş) DOM'u incele**:
   ```python
   page.screenshot(path='/tmp/inspect.png', full_page=True)
   content = page.content()
   page.locator('button').all()
   ```

2. İnceleme sonuçlarından **seçicileri belirle**

3. Keşfedilen seçicileri kullanarak **eylemleri yürüt**

## Yaygın Tuzak

❌ Dinamik uygulamalarda `networkidle` beklemeden DOM'u **inceleme**
✅ İncelemeden önce `page.wait_for_load_state('networkidle')` ile **bekle**

## En İyi Uygulamalar

- **Paketle gelen betikleri kara kutu olarak kullan** - Bir görevi yerine getirmek için `scripts/` içindeki betiklerden birinin yardımcı olup olamayacağını düşün. Bu betikler yaygın, karmaşık iş akışlarını bağlam penceresini doldurmadan güvenilir biçimde ele alır. Kullanımı görmek için `--help` kullan, ardından doğrudan çağır. 
- Eşzamanlı betikler için `sync_playwright()` kullan
- İşin bitince tarayıcıyı her zaman kapat
- Açıklayıcı seçiciler kullan: `text=`, `role=`, CSS seçicileri ya da kimlikler (ID)
- Uygun beklemeler ekle: `page.wait_for_selector()` ya da `page.wait_for_timeout()`

## Başvuru Dosyaları

- **examples/** - Yaygın kalıpları gösteren örnekler:
  - `element_discovery.py` - Bir sayfadaki düğmeleri, bağlantıları ve giriş alanlarını keşfetme
  - `static_html_automation.py` - Yerel HTML için file:// URL'lerini kullanma
  - `console_logging.py` - Otomasyon sırasında konsol loglarını yakalama