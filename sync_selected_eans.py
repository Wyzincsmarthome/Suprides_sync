import json
from suprides_api import get_product_by_ean
from shopify_api import product_exists, update_product, create_product

def main():
    with open("config.json") as f:
        config = json.load(f)

    with open("eans.txt") as f:
        eans = [line.strip() for line in f if line.strip()]

    for ean in eans:
        print(f"\n🔎 A processar EAN: {ean}")
        product = get_product_by_ean(ean, config)

        if not product:
            print(f"❌ Produto com EAN {ean} não encontrado na Suprides.")
            continue

        shopify_product = product_exists(ean, config)

        if shopify_product:
            variant = shopify_product["variants"][0]
            update_product(shopify_product["id"], variant["id"], product["pvpr"], config)
            print(f"✅ Produto existente atualizado no Shopify: {product['name']}")
        else:
            create_product(product, config)
            print(f"🆕 Produto criado no Shopify: {product['name']}")

if __name__ == "__main__":
    main()
