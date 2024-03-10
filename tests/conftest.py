from psycopg2 import DatabaseError
import pytest
import json


from src.auth_service.app import TrashAssApplication
from migrator.migrator import Migrator

db_config = "tests/config/db_config.json"

user = json.load(open(db_config)).get('USER')
dbname = json.load(open(db_config)).get('DBNAME')
setup_path = "src/auth_service/storage/migrations/setup/"
teardown_path = "src/auth_service/storage/migrations/teardown/"


@pytest.fixture()
def app():
    app = TrashAssApplication.create(db_config=db_config)

    # try:
    #     # setup_database()
    # except DatabaseError as err:
    #     print(f"Error: {str(err)}")
    #     print("Tables already exist --- not creating new ones")

    yield app
    #teardown_database()


@pytest.fixture()
def client(app):
    return app.test_client()


def setup_database():
    migrator_up = Migrator(dbname=dbname, user=user, dirpath=setup_path)
    migrator_up.exec()


def teardown_database():
    migrator_down = Migrator(dbname=dbname, user=user, dirpath=teardown_path)
    migrator_down.exec()

