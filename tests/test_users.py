

def test_get_current_user(client,auth_headers):
    response = client.get("api/v1/user",headers = auth_headers)

    assert response.status_code == 200
    data = response.json()
    assert "id" in data


def test_admin_access_denied(client,auth_headers):
    response = client.get("api/v1/admin/users",headers = auth_headers)

    assert response.status_code == 403