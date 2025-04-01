import requests
import csv
import os
from collections import defaultdict

API_KEY = "101c8e9a0f9ed4ffe77b2c8658a85f57bd6e1296"
URL = f"https://www.symphonya.eu/api/getProducts/{API_KEY}"

response = requests.get(URL)
products = response.json()["raspuns"]

# Agrupa os produtos por categoria
categorias = defaultdict(list)
for p in products:
    categorias[p["category"]].append(p)

# Garante a pasta de saída
os.makedirs("csvs", exist_ok=True)

# Cabeçalho Shopify
cabecalho = [
    "Handle", "Title", "Body (HTML)", "Vendor", "Type", "Tags", "Published",
    "Option1 Name", "Option1 Value", "Variant SKU", "Variant Price", "Variant Inventory Qty"
]

# Cria um CSV por categoria
for categoria, items in categorias.items():
    filename = f"csvs/produtos_{categoria.lower().replace(' ', '_')}.csv"
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(cabecalho)

        for p in items:
            handle = p["name"].lower().replace(" ", "-")
            writer.writerow([
                handle,
                p["name"],
                "",
                p["brand"],
                p["category"],
                f"{p['gender']}, {p['type']}",
                "TRUE",
                "Title",
                "Default Title",
                p["ean"],
                p["price"],
                p["stock"]
            ])
