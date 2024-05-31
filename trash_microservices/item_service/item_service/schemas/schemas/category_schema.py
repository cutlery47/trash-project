from pydantic import BaseModel

from item_service.schemas.types.annotated_types import PositiveInteger

class BaseCategoryDTO(BaseModel):
    name: str

class CategoryAddDTO(BaseCategoryDTO):
    pass

class CategoryDTO(BaseCategoryDTO):
    id: PositiveInteger

    def __str__(self):
        return "Category"
