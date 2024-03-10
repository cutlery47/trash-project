def test_create_correct_user(client):
    response = client.post(
        "/api/v1/auth/users/create",
        json={
                "email": "something@mail.ru",
                "password": "123123123"
        })
    assert response is not None


def test_get(client):
    response = client.get("/api/v1/auth/users/get/")
    assert response.data is not None