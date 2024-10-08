import pytest

from tests.conftest import (example_good_email,
                            example_good_email_2,
                            example_good_password,
                            example_bad_password,
                            example_bad_email)

#@pytest.mark.skip
def test_create_user_with_bad_email(setup_teardown_db, test_client):
    response = test_client.post("/api/v1/register/",
                                json={
                                    "email": example_bad_email,
                                    "password": example_good_password,
                                    "firstname": "dima",
                                    "surname": "xyu"
                                })

    assert response.status_code == 400


#@pytest.mark.skip
def test_create_user_with_bad_password(setup_teardown_db, test_client):
    response = test_client.post("/api/v1/register/",
                                json={
                                    "email": example_good_email,
                                    "password": example_bad_password,
                                    "firstname": "dima",
                                    "surname": "xyu"
                                })

    assert response.status_code == 400


#@pytest.mark.skip
def test_create_user(setup_teardown_db, test_client):
    response = test_client.post("/api/v1/register/",
                                 json={
                                     "email": example_good_email,
                                     "password": example_good_password,
                                     "firstname": "sdfsdfdsfd",
                                     "surname": "123123123"
                                 })

    assert response.status_code == 200


#@pytest.mark.skip
def test_create_admin_as_user(setup_teardown_db, test_client):

    test_client.post("/api/v1/register/",
                     json={
                         "email": example_good_email,
                         "password": example_good_password,
                         "firstname": "dima",
                         "surname": "xyu"
                     })

    res = test_client.post("/api/v1/authorize/",
                     json={
                         "email": example_good_email,
                         "password": example_good_password,
                     })

    print(test_client.cookies)

    creation_response = test_client.post("/api/v1/register_admin/",
                                         json={
                                             "email": example_good_email_2,
                                             "password": example_good_password,
                                             "firstname": "dima",
                                             "surname": "xyu"
                                         })

    assert creation_response.status_code == 403
