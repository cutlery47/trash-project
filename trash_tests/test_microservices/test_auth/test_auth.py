correct_email_1 = "example@gmail.com"
correct_email_2 = "examasfasdfple@gmail.com"

correct_password_1 = "xyu289_pizd4"
correct_password_2 = "poebota_o4ko_381"

user_id_1 = 0
user_id_2 = 0

access_token = ""
refresh_token = ""

status_200 = "200 OK"
status_400 = "400 BAD REQUEST"
status_403 = "403 FORBIDDEN"
status_500 = "500 INTERNAL SERVER ERROR"


def test_register_correct_user_1(client):
    global user_id_1

    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_200
    user_id_1 = response.text


def test_register_correct_user_2(client):
    global user_id_2

    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email_2,
            "password": correct_password_2
        }
    )
    assert response.status == status_200
    user_id_2 = response.text


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


def test_register_user_with_existing_email(client):
    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
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
    global access_token
    global refresh_token

    response = client.post(
        path="api/v1/auth/authorize/",
        json={
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_200
    access_token = response.json['access']
    refresh_token = response.json['refresh']


def test_authorization_with_wrong_password(client):
    response = client.post(
        path="api/v1/auth/authorize/",
        json={
            "email": correct_email_1,
            "password": correct_password_2
        }
    )
    assert response.status == status_400


def test_validate_access_token(client):
    response = client.post(
        path="api/v1/auth/validate/",
        json={
            "access": access_token
        }
    )
    assert response.status == status_200


def test_refresh_access_token_without_refresh_token(client):
    response = client.post(
        path="api/v1/auth/refresh/",
        json={
            "access": access_token,
        }
    )
    assert response.status == status_400


def test_refresh_access_token(client):
    global access_token

    response = client.post(
        path="api/v1/auth/refresh/",
        json={
            "refresh": refresh_token,
        }
    )
    assert response.status == status_200
    access_token = response.json['access']


def test_create_admin_as_a_user(client):
    response = client.post(
        path="api/v1/auth/register_admin/",
        json={
            "access": access_token,
            "email": correct_email_1,
            "password": correct_password_1
        }
    )
    assert response.status == status_403


def test_get_all_users_data(client):
    response = client.get(
        path="api/v1/auth/users/",
        json={
            "access": access_token
        }
    )
    assert response.status == status_200


def test_get_all_users_data_without_access_token(client):
    response = client.get(
        path="api/v1/auth/users/",
        json={}
    )
    assert response.status == status_400


def get_user_data_by_respective_id(client):
    response = client.get(
        path=f"api/v1/auth/users/{user_id_1}",
        json={
            "access": access_token
        }
    )
    assert response.status == status_200


def get_user_data_by_wrong_id(client):
    response = client.get(
        path=f"api/v1/auth/users/{user_id_2}",
        json={
            "access": access_token
        }
    )

    assert response.status == status_403