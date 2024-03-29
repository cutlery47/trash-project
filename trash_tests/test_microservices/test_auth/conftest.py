import json

from psycopg2 import DatabaseError
import pytest

from auth_service.app import TrashAssApplication
from migrator.migrator import Migrator

db_config = "config/db_config.json"
logger_config = "config/logger_config.json"
jwt_secret_path = "config/jwt_secret.txt"

user = json.load(open(db_config)).get('USER')
dbname = json.load(open(db_config)).get('DBNAME')
setup_path = "auth_migrations/setup/"
teardown_path = "auth_migrations/teardown/"


@pytest.fixture(scope='session')
def app():
    app = TrashAssApplication.create(db_config=db_config,
                                     logger_config=logger_config,
                                     jwt_secret_path=jwt_secret_path
                                     )
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

