import json
import re
from playwright.sync_api import sync_playwright

with open("input.json", "r", encoding="utf-8") as f:
    items = json.load(f)

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)

    for item in items:
        url = item["url"]

        # usa sempre id (standardizzato)
        product_id = item.get("id")

        page = browser.new_page()

        try:
            print(f"\n--- Processing: {url}")

            page.goto(
                url,
                timeout=60000,
                wait_until="domcontentloaded"
            )

            page.wait_for_selector("body", timeout=60000)
            page.wait_for_timeout(5000)

            price = None

            # LEGO
            try:
                el = page.query_selector('[data-test="product-price"]')
                if el:
                    price = el.inner_text().strip()
                    print("Found LEGO price:", price)
            except Exception:
                pass

            # BooksToScrape
            if not price:
                try:
                    el = page.query_selector(".price_color")
                    if el:
                        price = el.inner_text().strip()
                        print("Found BooksToScrape price:", price)
                except Exception:
                    pass

            # Amazon
            if not price:
                try:
                    el = page.query_selector("span.a-offscreen")
                    if el:
                        price = el.inner_text().strip()
                        print("Found Amazon price:", price)
                except Exception:
                    pass

            # Fallback regex
            if not price:
                content = page.content()

                match = re.search(
                    r"[€£$]\s?\d+[.,]\d+",
                    content
                )

                if match:
                    price = match.group()
                    print("Found regex price:", price)

            print("Final price:", price)

            results.append({
                "id": product_id,
                "url": url,
                "price": price
            })

        except Exception as e:
            print("ERROR:", str(e))

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

print("\nDone:")
print(json.dumps(results, indent=2, ensure_ascii=False))
