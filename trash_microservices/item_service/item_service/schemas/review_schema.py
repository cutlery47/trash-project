from pydantic import BaseModel

from datetime import datetime

from item_service.schemas.annotated_types import PositiveInteger, PositiveFloat

class BaseReviewDTO(BaseModel):
    reviewer_id: PositiveInteger
    item_id: PositiveInteger
    text: str
    rating: PositiveFloat

class ReviewAddDTO(BaseReviewDTO):
    pass

class ReviewDTO(BaseReviewDTO):
    id: PositiveInteger
    uploaded_at: datetime
