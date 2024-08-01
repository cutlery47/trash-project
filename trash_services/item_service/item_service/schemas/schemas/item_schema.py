from pydantic import BaseModel

from typing import Optional

from item_service.schemas.types.annotated_types import PositiveFloat, PositiveInteger

class BaseItemDTO(BaseModel):
    category_id: PositiveInteger
    merchant_id: PositiveInteger
    name: str
    description: str
    price: PositiveFloat
    in_stock: PositiveInteger
    image: Optional[str] = ""

class ItemAddDTO(BaseItemDTO):
    pass

class ItemDTO(BaseItemDTO):
    id: PositiveInteger

    def __str__(self):
        return "Item"
