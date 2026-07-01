import json
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

# 📁 PATH ROBUSTO (NON dipende da dove lanci il file)
INPUT_PATH = Path(__file__).parent / "it" / "data.json"
OUTPUT_PATH = Path(__file__).parent / "output.json"

PRICE_SELECTORS = [
    '[data-test="product-price"]',
    ".price_color",
    "span.a-offscreen"
]

PRICE_REGEX = re.compile(r"[€£$]\s?\d+[.,]\d+")


def extract_price(page):
    # 1. selectors specifici
    for selector in PRICE_SELECTORS:
        el = page.query_selector(selector)
        if el:
            price = el.inner_text().strip()
            if price:
                return price

    # 2. fallback regex
    match = PRICE_REGEX.search(page.content())
    if match:
        return match.group()

    return None


def normalize_url(url: str) -> str:
    if not url:
        return None

    url = url.strip()

    # se è path relativo
    if url.startswith("/"):
        url = "https://lacittadelmattoncino" + url

    # se contiene già dominio vecchio (non necessario ma safe)
    url = url.replace("http://lacittadelmattoncino", "https://lacittadelmattoncino")
    url = url.replace("lacittadelmattoncino", "https://lacittadelmattoncino")

    return url


# 📥 LOAD DATA
if not INPUT_PATH.exists():
    raise FileNotFoundError(f"File non trovato: {INPUT_PATH}")

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    items = json.load(f)

print(f"Loaded items: {len(items)}")

results = []

# 🌐 SCRAPING
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    for item in items:
        product_id = item.get("id")
        raw_url = item.get("lacittadelmattoncino")

        url = normalize_url(raw_url)

        if not url:
            print(f"Skipping {product_id}: missing URL")
            continue

        try:
            print(f"\n--- Processing: {url}")

            page.goto(url, timeout=60000, wait_until="domcontentloaded")

            price = extract_price(page)

            print("Price:", price)

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

    browser.close()

# 💾 OUTPUT
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nDone. Saved to output.json")
