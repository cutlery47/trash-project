import pytest

from tests.conftest import setup_teardown_db, test_client, user

#@pytest.mark.skip
def test_validate_access_token(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_access/')

    assert response.status_code == 200

#@pytest.mark.skip
def test_validate_access_to_own_id(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_access/' + str(user.id))

    assert response.status_code == 200

#@pytest.mark.skip
def test_validate_access_to_other_id(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_access/' + '1337')

    assert response.status_code == 403

#@pytest.mark.skip
def test_validate_admin_as_user(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_admin/')

    assert response.status_code == 403

#@pytest.mark.skip
def test_validate_access_and_id(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_access_and_id/' + str(user.id))

    assert response.status_code == 200

#@pytest.mark.skip
def test_validate_access_and_admin_as_user(setup_teardown_db, test_client, user):
    response = test_client.get('/api/v1/validate_access_and_admin/')

    assert response.status_code == 403



