# 1) изменение себя
# 2) изменение несущ
# 3) изменение другого
# 4) изменение админа
# 5) невалидное изменение пароля
# 6) невалидное изменение почты

import pytest

from tests.conftest import setup_teardown_db, user, test_client, example_good_email_2, example_good_password

#@pytest.mark.skip
def test_update_self(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/" + str(user.id),
                               json={
                                   "email": example_good_email_2,
                                   "password": example_good_password
                               })

    assert response.status_code == 200

#@pytest.mark.skip
def test_update_nonexistant(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/1337",
                               json={
                                   'email': 'sommosm@mail.ru'
                               })

    assert response.status_code == 403

#@pytest.mark.skip
def test_update_other(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/1",
                               json={
                                   'email': 'sommosm@mail.ru'
                               })

    assert response.status_code == 403


#@pytest.mark.skip
def test_update_admin(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/2",
                               json={
                                   'email': 'sommosm@mail.ru'
                               })

    assert response.status_code == 403

#@pytest.mark.skip
def test_update_self_with_invalid_email(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/" + str(user.id),
                               json={
                                   'email': 'sommosm'
                               })

    assert response.status_code == 400

#@pytest.mark.skip
def test_update_self_with_invalid_password(setup_teardown_db, test_client, user):
    response = test_client.put("/api/v1/users/" + str(user.id),
                               json={
                                   'password': ''
                               })

    assert response.status_code == 400

