import pytest
import requests
from config import REQRES_API_URL, REQRES_HEADERS,GOREST_API_URL, GOREST_HEADERS

#PARAMETERIZATION WITH HELPER FUNCTION
def get_user(user_id):

    url = f"{REQRES_API_URL}/{user_id}"
    return requests.get(url, headers=REQRES_HEADERS)

@pytest.mark.parametrize("user_id, expected_status_code", [
    (1, 200),        
    (2, 200),         
    (999, 404),   
    ("abc", 404),       
])
def test_get_user_by_id(user_id, expected_status_code):

    response = get_user(user_id)
    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        response_json = response.json()
        assert "id" in response_json["data"]
        assert response_json["data"]["id"] == user_id

#FIXTURE WITH TEARDOWN
@pytest.fixture
def new_user():
    user_data = {
        "name": "TEST_USER",
        "email": "test_user@gmail.com",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(GOREST_API_URL, headers=GOREST_HEADERS, json=user_data)
    created_user = response.json()

    yield created_user

    user_id = created_user["id"]
    if user_id:
        requests.delete(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)

def test_get_specific_user(new_user):
    print(new_user)
    user_id = new_user["id"]
    print(user_id)
    response = requests.get(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)
    assert response.status_code == 200
    assert response.json()["name"] == "TEST_USER"