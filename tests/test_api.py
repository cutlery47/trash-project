correct_email = "example@gmail.com"
correct_password = "xyu289_pizd4"
status_200 = "200 OK"
status_400 = "400 BAD REQUEST"


def test_create_correct_user(client):
    # everything is fine
    response = client.post(
        path="/api/v1/auth/users/create/",
        json={
                "email": correct_email,
                "password": correct_password
        })
    assert response.status == status_200


def test_create_incorrect_user_1(client):
    # missing email
    response = client.post(
        path="/api/v1/auth/users/create/",
        json={
            "password": correct_password
        })
    assert response.status == status_400


def test_create_incorrect_user_2(client):
    # missing password
    response = client.post(
        path="/api/v1/auth/users/create/",
        json={
            "email": correct_email
        })
    assert response.status == status_400


def test_create_incorrect_user_3(client):
    # blank password and email
    response = client.post(
        path="/api/v1/auth/users/create/",
        json={
            "email": "",
            "password": ""
        })
    assert response.status == status_400


def test_create_incorrect_user_4(client):
    # added forbidden field
    response = client.post(
        path="/api/v1/auth/users/create/",
        json={
            "id": "23",
            "email": "123123",
            "password": "123432"
        })
    assert response.status != status_200


def test_get_all(client):
    response = client.get(path="/api/v1/auth/users/get/")
    assert response.status == status_200
