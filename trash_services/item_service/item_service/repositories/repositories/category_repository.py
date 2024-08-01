from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.models.models import Category

class CategoryRepository(CRUDRepository[Category]):
    _entity_class = Category