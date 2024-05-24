from item_service.services.core.crud_service import CRUDService
from item_service.schemas.schemas.category_schema import CategoryDTO, CategoryAddDTO
from item_service.repositories.models.models import Category


class CategoryService(CRUDService[CategoryAddDTO, CategoryDTO]):
    _entity_class = Category
    _dto_class = CategoryDTO
    _add_dto_class = CategoryAddDTO
