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
            print(f"HTTP {response.status_code} per {asin}")
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # 1️⃣ metodo principale (più affidabile)
        price_tag = soup.select_one("span.a-price span.a-offscreen")

        # 2️⃣ fallback se Amazon cambia layout
        if not price_tag:
            price_tag = soup.select_one("#priceblock_ourprice")
        if not price_tag:
            price_tag = soup.select_one("#priceblock_dealprice")

        if not price_tag:
            return None

        price = price_tag.get_text(strip=True)

        # pulizia semplice
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
    # prodotti fissi
    with open("data.json", "r", encoding="utf-8") as f:
        products = json.load(f)

    # storico prezzi
    prices = load_prices()

    for p in products:
        asin = p["id"]
        name = p.get("name", asin)

        print(f"\nControllo {name} ({asin})...")

        price = get_price(asin)

        # inizializza struttura se non esiste
        if asin not in prices:
            prices[asin] = {"history": []}

        if price:
            print(f"Prezzo trovato: {price}")

            # salva solo se cambia
            last_price = prices[asin]["history"][-1] if prices[asin]["history"] else None

            if price != last_price:
                prices[asin]["history"].append(price)
                print("✔ Prezzo aggiornato nel file")
            else:
                print("↻ Prezzo invariato")

        else:
            print("⚠ Prezzo non trovato")

    # salva tutto
    with open("prezzi.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    main()
