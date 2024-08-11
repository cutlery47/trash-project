from src.services.core.crud_service import CRUDService
from src.schemas.schemas.category_schema import CategoryDTO, CategoryAddDTO
from src.models.models import Category


class CategoryService(CRUDService[CategoryAddDTO, CategoryDTO]):
    _entity_class = Category
    _dto_class = CategoryDTO
    _add_dto_class = CategoryAddDTO
