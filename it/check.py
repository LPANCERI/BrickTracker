import json


def load_json(file_path, default):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return default


def main():
    # carica input
    products = load_json("data.json", [])
    prices = load_json("prezzi.json", {})

    for p in products:
        product_id = p["id"]
        value = p.get("set")

        print(f"ID: {product_id} -> set: {value}")

        if value is None:
            print("⚠ valore 'set' mancante, salto")
            continue

        # inizializza struttura se non esiste
        if product_id not in prices:
            prices[product_id] = {}

        # aggiorna valore amazon
        prices[product_id]["amazon"] = value

        print(f"✔ salvato: {product_id} = {value}")

    # salva file aggiornato
    with open("prezzi.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=4, ensure_ascii=False)

    print("\n✔ Aggiornamento completato")


if __name__ == "__main__":
    main()
