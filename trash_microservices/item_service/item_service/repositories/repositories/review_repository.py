from item_service.repositories.core.crud_repository import CRUDRepository
from item_service.models.models import Review

class ReviewRepository(CRUDRepository[Review]):
    _entity_class = Review