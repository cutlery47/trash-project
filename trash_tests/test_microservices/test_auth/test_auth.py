correct_email_1 = "example@gmail.com"
correct_email_2 = "examasfasdfple@gmail.com"

correct_password_1 = "xyu289_pizd4"
correct_password_2 = "poebota_o4ko_381"

access_token = ""
refresh_token = ""

status_200 = "200 OK"
status_400 = "400 BAD REQUEST"
status_500 = "500 INTERNAL SERVER ERROR"


def test_register_correct_user(client):
    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_200


def test_register_user_missing_email(client):
    response = client.post(
        path="api/v1/auth/register/",
        json={
            "password": correct_password_1
        }
    )
    assert response.status == status_400


def test_register_user_missing_password(client):
    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email_1
        }
    )
    assert response.status == status_400


def test_register_admin_without_access_token(client):
    response = client.post(
        path="api/v1/auth/register_admin/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_400


def test_authorization_with_correct_input(client):
    response = client.post(
        path="api/v1/auth/authorize/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_200