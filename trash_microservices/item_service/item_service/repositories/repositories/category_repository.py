from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.repositories.models.models import Category

class ItemRepository(CRUDRepository[Category]):
    pass