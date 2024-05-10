from pydantic import BaseModel

from typing import Optional

from item_service.schemas.annotated_types import PositiveFloat, PositiveInteger

class BaseItemDTO(BaseModel):
    category_id: PositiveInteger
    merchant_id: PositiveInteger
    name: str
    description: str
    price: PositiveFloat
    in_stock: PositiveInteger
    image: Optional[str] = None

class ItemAddDTO(BaseItemDTO):
    pass

class ItemDTO(BaseItemDTO):
    id: PositiveInteger
