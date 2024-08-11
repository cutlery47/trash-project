from pydantic import BaseModel

from src.schemas.types.annotated_types import PositiveInteger

class BaseCategoryDTO(BaseModel):
    name: str

class CategoryAddDTO(BaseCategoryDTO):
    pass

class CategoryDTO(BaseCategoryDTO):
    id: PositiveInteger

    def __str__(self):
        return "Category"
