import pytest

from tests.conftest import setup_teardown_db, test_client, user


#@pytest.mark.skip
def test_read_all_users(setup_teardown_db, test_client, user):
    response = test_client.get("/api/v1/users/")

    assert response.status_code == 200 and len(response.json()) == 3

#@pytest.mark.skip
def test_read_user(setup_teardown_db, test_client, user):
    response = test_client.get("/api/v1/users/" + str(user.id))

    assert response.status_code == 200 and response.json() is not None

