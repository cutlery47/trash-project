import pytest

from tests.conftest import setup_teardown_db, test_client, user

#@pytest.mark.skip
def test_delete_self(setup_teardown_db, test_client, user):
    response = test_client.delete("/api/v1/users/" + str(user.id))
    print(response.text)

    assert response.status_code == 200

#@pytest.mark.skip
def test_delete_nonexistant(setup_teardown_db, test_client, user):
    response = test_client.delete("/api/v1/users/1000")

    assert response.status_code == 403

#@pytest.mark.skip
def test_delete_other(setup_teardown_db, test_client, user):
    response = test_client.delete("/api/v1/users/1")

    assert response.status_code == 403

#@pytest.mark.skip
def test_delete_admin(setup_teardown_db, test_client, user):
    response = test_client.delete("/api/v1/users/2")

    assert response.status_code == 403


