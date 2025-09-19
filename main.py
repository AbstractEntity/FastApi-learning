from decimal import Decimal
from enum import Enum

from fastapi import FastAPI, HTTPException, requests
from pydantic import BaseModel

app = FastAPI()


class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: Decimal
    count: int
    id: int
    category: Category


items = {
    0: Item(name="Axe", price=999.99, count=1, id=0, category=Category.TOOLS),
    1: Item(name="Hammer", price=690.59, count=1, id=1, category=Category.TOOLS),
    2: Item(name="Planks", price=400, count=5, id=3, category=Category.CONSUMABLES),
}


@app.get("/")
def index() -> dict[str, dict[int, Item]]:
    return {"items": items}


@app.get("/items/{item_id}")
def get_item_by_id(item_id: int) -> Item:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id} not found.")
    return items[item_id]


Selection = dict[str, str | int | Decimal | Category | None]


@app.get("/items/")
def get_items_by_parameters(
    name: str | None = None,
    price: Decimal | None = None,
    count: int | None = None,
    category: Category | None = None,
) -> dict[str, Selection | list]:
    def check_item(item: Item) -> bool:
        return all(
            (
                name is None or item.name == name,
                price is None or item.price == price,
                count is None or item.count == count,
                category is None or item.category is category,
            ),
        )

    selection = [item for item in items.values() if check_item(item)]
    return {
        "query": {"name": name, "price": price, "count": count, "category": category},
        "selection": selection,
    }


@app.post("/")
def post_item(item: Item) -> dict[str, Item]:
    if item.id in items:
        raise HTTPException(
            status_code=400, detail=f"Item with {item.id} already exists."
        )
    items[item.id] = item
    return {
        "added": item,
    }


def main():
    print("Hello from fastapi-test!")


if __name__ == "__main__":
    main()
