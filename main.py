from decimal import Decimal
from enum import Enum
from typing import Annotated, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy import Column, Integer, Numeric, String, create_engine
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

# Create FastAPI app
app = FastAPI()


# Define the Items SQLAlchemy model
Base = declarative_base()


# Define Category enum to force category options
class Category(Enum):
    tools = "tools"
    consumables = "consumables"


class DBItems(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    price = Column(Numeric(10, 2, asdecimal=True))
    count = Column(Integer)
    category = Column(SQLEnum(Category, name="category_enum", create_constraint=True))


# Create the SQLite database engine
DATABASE_URL = "sqlite:///./items.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)


# Define Pydantic Items model
class Items(BaseModel):
    id: Optional[int] = None
    name: Annotated[str, Query(min_length=1, max_length=12)]
    price: Annotated[Decimal, Query(gt=0)]
    count: Annotated[int, Query(ge=0)]
    category: Category


# Define Pydantic Item model for querying and updating
class UpdateItem(BaseModel):
    name: Annotated[str | None, Query(min_length=1, max_length=12)] = None
    price: Annotated[Decimal | None, Query(gt=0)] = None
    count: Annotated[int | None, Query(ge=0)] = None
    category: Optional[Category] = None


# Dependency: Get the session
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Add an Item
@app.post("/", response_model=Items)
def post_item(item: Items, session: Session = Depends(get_session)):
    db_item = DBItems(**item.model_dump())
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# Get list of items
@app.get("/", response_model=list[Items])
def get_items(skip: int = 0, limit: int = 50, session: Session = Depends(get_session)):
    items = session.query(DBItems).offset(skip).limit(limit).all()
    return items


# Get an item by ID
@app.get("/items/{item_id}", response_model=Items)
def read_item(item_id: int, session: Session = Depends(get_session)):
    item = session.query(DBItems).filter(DBItems.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# Get items by query with json payload
# @app.get("/items/", response_model=list[Items])
# def query_items(
#     item: UpdateItem,
#     limit: int = 50,
#     session: Session = Depends(get_session),
# ):
#     selection = (
#         session.query(DBItems)
#         .filter(
#             item.name is None or DBItems.name == item.name,
#             item.price is None or DBItems.price == item.price,
#             item.count is None or DBItems.count == item.count,
#             item.category is None or DBItems.category == item.category,
#         )
#         .limit(limit)
#     )
#     if not selection.first():
#         raise HTTPException(status_code=404, detail="Items not found")
#     return selection


# Get items by query
@app.get("/items/", response_model=list[Items])
def query_items(
    name: str | None = None,
    price: Decimal | None = None,
    count: int | None = None,
    category: str | None = None,
    limit: int = 50,
    session: Session = Depends(get_session),
):
    selection = (
        session.query(DBItems)
        .filter(
            name is None or DBItems.name == name,
            price is None or DBItems.price == price,
            count is None or DBItems.count == count,
            category is None or DBItems.category == category,
        )
        .limit(limit)
    )
    if not selection.first():
        raise HTTPException(status_code=404, detail="Items not found")
    return selection


# Delete Item by item_id
@app.delete("/items/{item_id}", response_model=Items)
def delete_item(item_id: int, session: Session = Depends(get_session)):
    item = session.query(DBItems).filter(DBItems.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    session.delete(item)
    session.commit()
    return item


# Update an Item
@app.patch("/items/{item_id}", response_model=Items)
def update_item(
    item_id: int,
    item_data: UpdateItem,
    session: Session = Depends(get_session),
):
    item = session.query(DBItems).filter(DBItems.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in item_data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    session.commit()
    session.refresh(item)
    return item


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
