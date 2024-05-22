from item_service.services.core.crud_service import CRUDService
from item_service.schemas.schemas.review_schema import ReviewAddDTO, ReviewDTO
from item_service.repositories.models.models import Review


class CategoryService(CRUDService[ReviewAddDTO, ReviewDTO]):
    _entity_class = Review
