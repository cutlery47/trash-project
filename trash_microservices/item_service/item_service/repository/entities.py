from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column

from typing import Optional

class Base(DeclarativeBase):
    pass

class Item(Base):
    __tablename__ = "items"

    id = mapped_column(primary_key=True)
    name = mapped_column(type=str)
    description = mapped_column(type=str)
    price = mapped_column(type=float)
    rating = mapped_column(type=float)
    image = Optional[mapped_column(type=str)]