from pydantic import BaseModel

from datetime import datetime

class BaseReview(BaseModel):
    reviewer_id: int
    item_id: int
    text: str
    rating: float

class ReviewAdd(BaseReview):
    pass

class Review(BaseReview):
    id: int
    uploaded_at: datetime