from sqlalchemy import ForeignKey

from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped

from item_service.storage.annotated_types import str_256
from item_service.storage.annotated_types import text
from item_service.storage.annotated_types import pk
from item_service.storage.annotated_types import timestamp

from typing import Optional

class Base(DeclarativeBase):
   pass

class Item(Base):
    __tablename__ = "items"

    id: Mapped[pk]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    name: Mapped[str_256]
    price: Mapped[float]
    in_stock: Mapped[int]
    image: Mapped[Optional[str_256]]

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[pk]
    name: Mapped[str_256]

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[pk]
    reviewer_id: Mapped[int]  # also a foreign key (to a table in another database)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    text: Mapped[Optional[text]]
    rating: Mapped[Optional[float]]
    reviewed_at: Mapped[timestamp]

class UserItem(Base):
    __tablename__ = "user_items"

    id: Mapped[pk]
    user_id: Mapped[int]
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))



