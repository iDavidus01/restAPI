import pytest
from main import app, users

@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def init_users():
    users.clear()
    users.append({"id": 1, "name": "Jan", "lastname": "Kowalski"})
    users.append({"id": 2, "name": "Anna", "lastname": "Nowak"})
    return users

def test_get_users(client, init_users):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json == [{"id": 1, "name": "Jan", "lastname": "Kowalski"}, {"id": 2, "name": "Anna", "lastname": "Nowak"}]

def test_get_user_by_id(client, init_users):
    response = client.get('/users/1')
    assert response.status_code == 200
    assert response.json == {"id": 1, "name": "Jan", "lastname": "Kowalski"}

def test_create_user(client, init_users):
    response = client.post('/users', json={"name": "David", "lastname": "Zieliński"})
    assert response.status_code == 201
    assert response.json["name"] == "David"
    assert response.json["lastname"] == "Zieliński"
    assert response.json["id"] == 3

def test_patch_user(client, init_users):
    response = client.patch('/users/1', json={"name": "Anotnio"})
    assert response.status_code == 204
    assert users[0]["name"] == "Anotnio"

def test_put_user(client, init_users):
    response = client.put('/users/1', json={"name": "Gregor", "lastname": "Sigma"})
    assert response.status_code == 204
    assert users[0]["name"] == "Gregor"
    assert users[0]["lastname"] == "Sigma"

def test_delete_user(client, init_users):
    response = client.delete('/users/1')
    assert response.status_code == 204
    assert len(users) == 1

def test_user_not_found(client):
    response = client.get('/users/999')
    assert response.status_code == 404

def test_invalid_patch(client, init_users):
    response = client.patch('/users/1', json={"invalid_field": "test"})
    assert response.status_code == 400

def test_invalid_put(client, init_users):
    response = client.put('/users/1', json={"name": "Kamil"})
    assert response.status_code == 400
