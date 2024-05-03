from pydantic import BaseModel

class BaseItem(BaseModel):
    category_id: int
    name: str
    description: str
    price: float
    in_stock: int
    image: str | None

class ItemAdd(BaseItem):
    pass

class Item(BaseItem):
    id: int
