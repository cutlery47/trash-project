correct_email = "example@gmail.com"
correct_password = "xyu289_pizd4"
status_200 = "200 OK"
status_400 = "400 BAD REQUEST"

def test_register_correct_user(client):
    response = client.post(
        path="api/v1/auth/register/",
        json={
            "email": correct_email,
            "password": correct_password
        }
    )
    assert response == status_200
