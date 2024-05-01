from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from item_service.storage.models import Item, UserItem

from item_service.storage.models import Base

import json

class Repository:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://cutlery:12345@localhost:5432/item_service")
        Base.metadata.create_all(self.engine)

    def add(self, item: Item, user_item: UserItem):
        with Session(self.engine) as session:
            session.add(item)
            session.add(user_item)
            session.commit()
            