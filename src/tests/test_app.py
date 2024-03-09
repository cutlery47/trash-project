from src.tests.conftest import setup_databse, teardown_database

def test_get(client):
    setup_databse()
    response = client.get("/api/v1/users/get/1")
    teardown_database()
    assert "200" in response.data.decode()
