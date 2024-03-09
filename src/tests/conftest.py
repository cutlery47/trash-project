import pytest
import json

from src.auth_service.app import TrashAssApplication
from src.migrator.migrator import Migrator

user = json.load(open("config/db_config.json")).get('USER')
dbname = json.load(open("config/db_config.json")).get('DBNAME')
setup_path = "../auth_service/storage/migrations/setup/"
teardown_path = "../auth_service/storage/migrations/teardown/"


@pytest.fixture()
def app():
    app = TrashAssApplication.create(db_config="config/db_config.json")
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

def setup_databse():
    migrator_up = Migrator(dbname=dbname, user=user, dirpath=setup_path)
    migrator_up.exec()

def teardown_database():
    migrator_down = Migrator(dbname=dbname, user=user, dirpath=teardown_path)
    migrator_down.exec()

