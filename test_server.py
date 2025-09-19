import requests

print("Getting item")
print(requests.get("http://127.0.0.1:8000/items/2", timeout=5).json())

print("Quering items")
print(requests.get("http://127.0.0.1:8000/items?count=5", timeout=5).json())

print("Adding an item")
print(
    requests.post(
        "http://127.0.0.1:8000/",
        json={
            "name": "Nails",
            "price": "199.99",
            "count": 10,
            "id": 3,
            "category": "consumables",
        },
        timeout=5,
    ).json(),
)
print(requests.get("http://127.0.0.1:8000/", timeout=5).json())

print("Updating item")
# Will fail due to exceeding max length of name
print(
    requests.put(
        "http://127.0.0.1:8000/items/2?name=Plankswithpotatos",
        timeout=5,
    ).json(),
)
print(requests.get("http://127.0.0.1:8000/", timeout=5).json())

print("Deleting item")
print(requests.delete("http://127.0.0.1:8000/items/2", timeout=5).json())
print(requests.get("http://127.0.0.1:8000/", timeout=5).json())
