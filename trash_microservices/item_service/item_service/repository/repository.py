from sqlalchemy import create_engine
from sqlalchemy import insert
from sqlalchemy.orm import Session

from item_service.entities.entities import Item

class Repository:
    def __init__(self):
        self.engine = create_engine("postgresql+psycopg2://cutlery:12345@localhost:5432/item_service")

    def add(self, request):
        stmt = insert(Item).values(request.dict())
        with Session(self.engine) as session:
            session.execute(stmt)
            session.commit()