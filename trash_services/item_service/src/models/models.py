from sqlalchemy import ForeignKey

from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs

from src.models.annotated_types import str_256, text, pk, timestamp

from typing import Optional


class Base(DeclarativeBase, AsyncAttrs):
    id: Mapped[pk]

    def serialize(self):
        dict_data = self.__dict__
        dict_data.pop('_sa_instance_state', None)
        return dict_data


class Item(Base):
    __tablename__ = "items"

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    merchant_id: Mapped[int]
    name: Mapped[str_256]
    description: Mapped[str_256]
    price: Mapped[float]
    in_stock: Mapped[int]
    image: Mapped[Optional[str_256]]


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str_256]


class Review(Base):
    __tablename__ = "reviews"

    reviewer_id: Mapped[int]  # also a foreign key (to a table in another database)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id"))
    text: Mapped[Optional[text]]
    rating: Mapped[Optional[float]]
    reviewed_at: Mapped[timestamp]
