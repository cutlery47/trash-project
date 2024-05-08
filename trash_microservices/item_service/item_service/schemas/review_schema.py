from pydantic import BaseModel

from datetime import datetime

class BaseReviewDTO(BaseModel):
    reviewer_id: int
    item_id: int
    text: str
    rating: float

class ReviewAddDTO(BaseReviewDTO):
    pass

class ReviewDTO(BaseReviewDTO):
    id: int
    uploaded_at: datetime