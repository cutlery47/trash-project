from psycopg2 import DatabaseError
import pytest
import json


from microservices.auth_service.auth.app import TrashAssApplication
from migrator.migrator import Migrator

db_config = "tests/config/db_config.json"

user = json.load(open(db_config)).get('USER')
dbname = json.load(open(db_config)).get('DBNAME')
setup_path = "microservices/auth_service/storage/migrations/setup/"
teardown_path = "microservices/auth_service/storage/migrations/teardown/"


@pytest.fixture(scope='session')
def app():
    app = TrashAssApplication.create(db_config=db_config)
    app.testing = True

    try:
        setup_database()
    except DatabaseError:
        print("Tables already exist --- not creating new ones")

    yield app

    teardown_database()


@pytest.fixture()
def client(app):
    return app.test_client()


def setup_database():
    migrator_up = Migrator(dbname=dbname, user=user, dirpath=setup_path)
    migrator_up.exec()


def teardown_database():
    migrator_down = Migrator(dbname=dbname, user=user, dirpath=teardown_path)
    migrator_down.exec()

