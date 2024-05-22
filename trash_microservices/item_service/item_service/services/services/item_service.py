from item_service.services.core.crud_service import CRUDService
from item_service.schemas.schemas.item_schema import ItemAddDTO, ItemDTO
from item_service.repositories.models.models import Item


class ItemService(CRUDService[ItemAddDTO, ItemDTO]):
    _entity_class = Item
