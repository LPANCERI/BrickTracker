import json
import requests
from bs4 import BeautifulSoup

# carica input
with open("input.json", "r", encoding="utf-8") as f:
    items = json.load(f)

results = []

headers = {
    "User-Agent": "Mozilla/5.0"
}

for item in items:
    url = item["url"]
    name = item["name"]

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    # LEGO spesso espone prezzo in meta o JSON-LD
    price = None

    # prova 1: JSON-LD
    for script in soup.find_all("script", type="application/ld+json"):
        if script.string and "price" in script.string:
            try:
                data = json.loads(script.string)
                if isinstance(data, dict):
                    offers = data.get("offers")
                    if offers and "price" in offers:
                        price = offers["price"]
            except:
                pass

    results.append({
        "name": name,
        "url": url,
        "price": price
    })

with open("output.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Done:", results)
