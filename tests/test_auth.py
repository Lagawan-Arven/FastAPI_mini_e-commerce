

def test_register_user(client):
    payload = {
        "firstname":"James",
        "lastname":"Bond",
        "age":30,
        "gender":"Male",
        "occupation":"Secret Agent",
        "username":"james007",
        "email":"james007@gmail.com",
        "password":"james007"
    }

    response = client.post("api/v1/register",json = payload)

    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "james007"


def test_login_user(client):
    response = client.post("api/v1/login",params = {"username":"james007","password":"james007"})

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

