import requests

print(requests.get("http://127.0.0.1:8000/items/2", timeout=5).json())
print(requests.get("http://127.0.0.1:8000/items?count=5", timeout=5).json())
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
    ).json()
)
