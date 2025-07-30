import requests
import json

def get_token(config):
    login_url = "https://www.suprides.pt/rest/V1/integration/admin/token"
    response = requests.post(login_url, json={
        "username": config["suprides"]["user"],
        "password": config["suprides"]["password"]
    })

    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao obter token:", response.status_code, response.text)
        return None

def get_product_by_ean(ean, config):
    token = get_token(config)
    if not token:
        return None

    url = f"https://www.suprides.pt/rest/V1/integration/products-list?EAN={ean}"
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data[0] if data else None
    else:
        print(f"Erro ao consultar EAN {ean}: {response.status_code} → {response.text}")
        return None
