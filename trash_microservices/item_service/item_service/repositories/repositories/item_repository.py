from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.repositories.models.models import Item

class ItemRepository(CRUDRepository[Item]):
    _entity_class = Item