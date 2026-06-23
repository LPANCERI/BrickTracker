import json
import re
from playwright.sync_api import sync_playwright

with open("input.json", "r", encoding="utf-8") as f:
    items = json.load(f)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in items:
        url = item["url"]

        try:
            # 🔥 NON usare networkidle (LEGO non lo raggiunge mai)
            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            # aspetta che React carichi contenuti
            page.wait_for_selector("body", timeout=60000)
            page.wait_for_timeout(8000)

            price = None

            # -------------------------
            # 1. prova selector LEGO (se esiste)
            # -------------------------
            try:
                el = page.query_selector('[data-test="product-price"]')
                if el:
                    price = el.inner_text().strip()
            except:
                pass

            # -------------------------
            # 2. fallback DOM (Amazon / altri)
            # -------------------------
            if not price:
                price = page.evaluate("""
                () => {
                    const el = document.querySelector('span.a-offscreen');
                    return el ? el.innerText : null;
                }
                """)

            # -------------------------
            # 3. fallback universale (€ regex)
            # -------------------------
            if not price:
                content = page.content()
                match = re.search(r"€\s?\d+[.,]\d+", content)
                if match:
                    price = match.group()

            results.append({
                "name": item["name"],
                "url": url,
                "price": price
            })

        except Exception as e:
            results.append({
                "name": item["name"],
                "url": url,
                "price": None,
                "error": str(e)
            })

    browser.close()

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Done:", results)
