import requests

def product_exists(ean, config):
    headers = {
        "X-Shopify-Access-Token": config["shopify"]["access_token"]
    }
    url = f"https://{config['shopify']['store_domain']}/admin/api/2023-07/products.json?fields=id,title,variants&barcode={ean}"
    response = requests.get(url, headers=headers)
    products = response.json().get("products", [])
    return products[0] if products else None

def update_product(product_id, variant_id, new_price, config):
    headers = {
        "X-Shopify-Access-Token": config["shopify"]["access_token"],
        "Content-Type": "application/json"
    }
    url = f"https://{config['shopify']['store_domain']}/admin/api/2023-07/variants/{variant_id}.json"
    payload = {
        "variant": {
            "id": variant_id,
            "price": new_price
        }
    }
    requests.put(url, json=payload, headers=headers)

def create_product(product_data, config):
    headers = {
        "X-Shopify-Access-Token": config["shopify"]["access_token"],
        "Content-Type": "application/json"
    }

    images = [{"src": img} for img in product_data.get("images", [])]
    payload = {
        "product": {
            "title": product_data["name"],
            "body_html": f"<p>{product_data['brand']} - {product_data['part_number']}</p>",
            "vendor": product_data["brand"],
            "product_type": product_data["family"],
            "variants": [{
                "sku": product_data["ean"],
                "price": product_data["pvpr"],
                "inventory_quantity": 10 if "Disponível" in product_data["stock"] else 0,
                "barcode": product_data["ean"]
            }],
            "images": images
        }
    }

    url = f"https://{config['shopify']['store_domain']}/admin/api/2023-07/products.json"
    requests.post(url, json=payload, headers=headers)
