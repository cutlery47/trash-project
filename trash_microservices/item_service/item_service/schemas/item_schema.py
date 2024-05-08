from pydantic import BaseModel

from typing import Optional

class BaseItemDTO(BaseModel):
    category_id: int
    merchant_id: int
    name: str
    description: str
    price: float
    in_stock: int
    image: Optional[str] = None

class ItemAddDTO(BaseItemDTO):
    pass

class ItemDTO(BaseItemDTO):
    id: int
