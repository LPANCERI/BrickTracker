import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.amazon.it/dp/{}"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8"
}


def get_price(asin):
    url = BASE_URL.format(asin)

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)

        if response.status_code != 200:
            print(f"Errore HTTP {response.status_code} per {asin}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        tag = soup.select_one("span.a-offscreen")

        if not tag:
            return None

        price = tag.get_text(strip=True)

        # pulizia € e spazi
        price = price.replace("€", "").strip()

        return price

    except Exception as e:
        print(f"Errore {asin}: {e}")
        return None


def load_prices():
    try:
        with open("prezzi.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def main():
    with open("data.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    prices = load_prices()

    for p in products:
        asin = p["id"]
        name = p.get("name", asin)

        print(f"Controllo {name} ({asin})...")

        price = get_price(asin)

        if price:
            if asin not in prices:
                prices[asin] = {}

            prices[asin]["amazon"] = price

            print("Prezzo:", price)
        else:
            print("Prezzo non trovato")

    with open("prezzi.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
