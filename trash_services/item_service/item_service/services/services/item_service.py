from item_service.services.core.crud_service import CRUDService
from item_service.schemas.schemas.item_schema import ItemAddDTO, ItemDTO
from item_service.models.models import Item


class ItemService(CRUDService[ItemAddDTO, ItemDTO]):
    _entity_class = Item
    _dto_class = ItemDTO
    _add_dto_class = ItemAddDTO
