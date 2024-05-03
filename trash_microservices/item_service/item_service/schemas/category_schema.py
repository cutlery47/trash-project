from pydantic import BaseModel

class BaseCategory(BaseModel):
    name: str

class CategoryAdd(BaseCategory):
    pass

class Category(BaseCategory):
    id: int