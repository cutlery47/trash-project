from src.services.core.crud_service import CRUDService
from src.schemas.schemas.item_schema import ItemAddDTO, ItemDTO
from src.models.models import Item


class ItemService(CRUDService[ItemAddDTO, ItemDTO]):
    _entity_class = Item
    _dto_class = ItemDTO
    _add_dto_class = ItemAddDTO
