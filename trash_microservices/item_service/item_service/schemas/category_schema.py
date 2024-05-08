from pydantic import BaseModel

class BaseCategoryDTO(BaseModel):
    name: str

class CategoryAddDTO(BaseCategoryDTO):
    pass

class CategoryDTO(BaseCategoryDTO):
    id: int