import requests
import json

def get_product_by_ean(ean, config):
    user = config["suprides"]["user"]
    password = config["suprides"]["password"]
    url = f"https://www.suprides.pt/rest/V1/integration/products-list?user={user}&password={password}&EAN={ean}"

    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        print(f"Erro ao consultar EAN {ean}: {response.status_code}")
        return None
