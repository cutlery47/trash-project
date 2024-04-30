from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from item_service.storage.entities import Item

from item_service.storage.entities import Base

import json

class Repository:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://cutlery:12345@localhost:5432/item_service")
        Base.metadata.create_all(self.engine)

    def add(self, request):
        request = json.loads(request.body.decode())
        obj = Item(**request)
        with Session(self.engine) as session:
            session.add(obj)
            session.commit()