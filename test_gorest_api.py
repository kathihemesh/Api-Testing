import requests

from config import GOREST_HEADERS,GOREST_API_URL

user_id=""

def test_get_users():
    response = requests.get(GOREST_API_URL, headers=GOREST_HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_user():
    global user_id
    payload = {
        "name": "Hemesh",
        "email": "hemesh@gmail.com",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(GOREST_API_URL, headers=GOREST_HEADERS, json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["gender"] == payload["gender"]
    assert data["status"] == payload["status"]
    user_id = data["id"]

def test_update_user():
    global user_id
    update_payload = {
        "name": "Hemesh Updated",
        "status": "inactive"
    }
    response = requests.put(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS, json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["status"] == update_payload["status"]

def test_delete_user():
    global user_id
    response = requests.delete(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)
    assert response.status_code == 204
