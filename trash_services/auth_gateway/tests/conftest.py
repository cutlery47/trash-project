import pytest
import json

from src.application.factory import ApplicationFactory
from src.storage.entities.entities import User

from migrator.migrator import Migrator

example_good_email = "some@mail.ru"
example_good_email_2 = "some123@mail.ru"
example_bad_email = "123123"

example_good_password = "123123ffsdfD"
example_bad_password = "o"


@pytest.fixture(scope="session")
def app():
    app = ApplicationFactory.create(db_config_path="tests/config/db/db_config.json")

    yield app


@pytest.fixture(scope="module")
def test_client(app):
    yield app.test_client()


@pytest.fixture(scope="module")
def init_db():
    migrator = Migrator(dbname="auth_service",
                        user="cutlery",
                        dirpath="src/storage/schema/")

    migrator.exec()

    return


@pytest.fixture(scope="module")
def setup_teardown_db(init_db):
    migrator = Migrator(dbname="auth_service",
                        user="cutlery",
                        dirpath="migrator/migrations/setup/")

    migrator.exec()

    yield

    migrator = Migrator(dbname="auth_service",
                        user="cutlery",
                        dirpath="migrator/migrations/teardown/")

    migrator.exec()


@pytest.fixture(scope="module")
def user(setup_teardown_db, test_client):
    response = test_client.post('/api/v1/register/',
                                json={
                                    'email': example_good_email,
                                    'password': example_good_password,
                                    'firstname': "Big",
                                    'surname': 'RunningBack'
                                })

    user = User(**json.loads(response.text))

    authorized_user = test_client.post('/api/v1/authorize/',
                                       json={
                                           'email': example_good_email,
                                           'password': example_good_password
                                       })

    return user
