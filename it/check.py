import json


def load_json(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def main():
    products = load_json("data.json")
    prices = load_json("prezzi.json")

    # se non è dizionario, lo resetta (fix automatico)
    if not isinstance(prices, dict):
        prices = {}

    for p in products:
        product_id = str(p.get("id"))
        set_value = p.get("set")

        print(f"ID: {product_id} -> set: {set_value}")

        if not set_value:
            print("⚠ set mancante")
            continue

        # struttura corretta per ogni ID
        if product_id not in prices:
            prices[product_id] = {}

        prices[product_id]["amazon"] = set_value

        print(f"✔ salvato {product_id}")

    with open("prezzi.json", "w", encoding="utf-8") as f:
        json.dump(prices, f, indent=4, ensure_ascii=False)

    print("\n✔ completato")


if __name__ == "__main__":
    main()
