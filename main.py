from decimal import Decimal
from enum import Enum
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel

# Uvicorn runs with command uvicorn main:app --reload

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
    2: Item(name="Planks", price=400, count=5, id=2, category=Category.CONSUMABLES),
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
            status_code=400,
            detail=f"Item with {item.id} already exists.",
        )
    items[item.id] = item
    return {
        "added": item,
    }


@app.put("/items/{item_id}")
def update_item(
    item_id: Annotated[int | None, Path(ge=0)],
    name: Annotated[str | None, Query(min_length=1, max_length=12)] = None,
    price: Annotated[Decimal | None, Query(gt=0)] = None,
    count: Annotated[int | None, Query(ge=0)] = None,
    category: Category | None = None,
) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} not found.")
    if all(params is None for params in (name, price, count, category)):
        HTTPException(status_code=400, detail="Parameters to update not provided.")
    item = items[item_id]
    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count
    if category is not None:
        item.category = category
    return {"updated": item}


@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:
    if item_id not in items:
        raise HTTPException(status_code=404, detail=f"Item with {item_id=} not found.")
    item = items.pop(item_id)
    return {"deleted": item}


def main():
    print("Hello from fastapi-test!")


if __name__ == "__main__":
    main()
