from sqlalchemy import ForeignKey

from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase

from item_service.repositories.models.annotated_types import str_256, text, pk, timestamp

from typing import Optional


class Base(DeclarativeBase):
    pass


class Item(Base):
    __tablename__ = "items"

    id: Mapped[pk]
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))
    merchant_id: Mapped[int]
    name: Mapped[str_256]
    description: Mapped[str_256]
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
