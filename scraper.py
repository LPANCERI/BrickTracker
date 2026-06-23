import json
from playwright.sync_api import sync_playwright

with open("input.json", "r", encoding="utf-8") as f:
    items = json.load(f)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in items:
        page.goto(item["url"], timeout=60000)

        # aspetta caricamento prezzo
        page.wait_for_timeout(3000)

        price = None

        try:
            # selettore LEGO (può cambiare ma questo è il più comune)
            price_el = page.query_selector('[data-test="product-price"]')
            if price_el:
                price = price_el.inner_text()
        except:
            pass

        results.append({
            "name": item["name"],
            "url": item["url"],
            "price": price
        })

    browser.close()

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
