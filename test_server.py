import sqlite3 as sq

import requests

print("Getting all items")
print(requests.get("http://127.0.0.1:8000/", timeout=5).json())

print("Getting item by id")
print(requests.get("http://127.0.0.1:8000/items/1", timeout=5).json())

print("Quering items")

# Direct query for direct query option in main.py module.
print(
    requests.get(
        "http://127.0.0.1:8000/items/?price=400&category=consumables",
        timeout=5,
    ).json(),
)
# Getting items by json
# query_date = {"price": 400, "category": "consumables"}
# print(
#     requests.get("http://127.0.0.1:8000/items/", timeout=5, json=query_date).json(),
# )

print("Adding an item")
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={
            "name": "Saw",
            "price": "799.99",
            "count": 1,
            "category": "tools",
        },
        timeout=5,
    ).json(),
)

print("Updating item")
update_data = {"price": 1089.99, "count": 2}
print(
    requests.patch(
        "http://127.0.0.1:8000/items/4",
        json=update_data,
        timeout=5,
    ).json(),
)

print("Deleting item")
print(requests.delete("http://127.0.0.1:8000/items/6", timeout=5).json())

print("SQL direct query:")
con = sq.connect("items.db")
cur = con.cursor()
cur.execute("""SELECT * from items""")
print(cur.fetchall())
