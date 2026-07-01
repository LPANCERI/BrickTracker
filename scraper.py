import json
import re
from playwright.sync_api import sync_playwright
from pathlib import Path

INPUT_PATH = Path("it/harry-potter/data.json")

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for item in json.load(open(INPUT_PATH, "r", encoding="utf-8")):
        
        # 🔥 QUI LA MODIFICA
        url = item.get("lacittadelmattoncino")
        product_id = item.get("id")

        if not url:
            print(f"Skipping item {product_id}: missing lacittadelmattoncino")
            continue

        page = browser.new_page()

        try:
            print(f"\n--- Processing: {url}")

            page.goto(url, timeout=60000, wait_until="domcontentloaded")
            page.wait_for_selector("body", timeout=60000)

            price = None

            # LEGO
            el = page.query_selector('[data-test="product-price"]')
            if el:
                price = el.inner_text().strip()

            # BooksToScrape
            if not price:
                el = page.query_selector(".price_color")
                if el:
                    price = el.inner_text().strip()

            # Amazon
            if not price:
                el = page.query_selector("span.a-offscreen")
                if el:
                    price = el.inner_text().strip()

            # fallback regex
            if not price:
                match = re.search(r"[€£$]\s?\d+[.,]\d+", page.content())
                if match:
                    price = match.group()

            results.append({
                "id": product_id,
                "url": url,
                "price": price
            })

        except Exception as e:
            results.append({
                "id": product_id,
                "url": url,
                "price": None,
                "error": str(e)
            })

        finally:
            page.close()

    browser.close()

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nDone")
