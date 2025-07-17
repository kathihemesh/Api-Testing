import pytest
import requests
import logging
import allure
from config import REQRES_API_URL, REQRES_HEADERS,GOREST_API_URL, GOREST_HEADERS

logger = logging.getLogger(__name__)

# Set up logger for test output

def setup_logger(log_filename):
    logger.handlers.clear()
    handler = logging.FileHandler(log_filename, mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


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

    setup_logger("./logs/reqres-api/test_get_user_by_id.log")
    response = get_user(user_id)
    logger.info(f"GET {REQRES_API_URL}/{user_id} - Status: {response.status_code}")
    assert response.status_code == expected_status_code,f"Failed to fetch user - status code: {response.status_code}"
    logger.info("Successfully fetched user")
    if expected_status_code == 200:
        response_json = response.json()
        logger.info(f"Response JSON: {response_json}")
        assert "id" in response_json["data"], "Response JSON should contain 'id'"
        logger.info("Response JSON contains 'id'")
        assert response_json["data"]["id"] == user_id, f"Expected user ID {user_id} not found in response"
        logger.info(f"User ID {user_id} found in response")
    else:
        logger.info(f"expected status for user_id {user_id}: {response.status_code}")
    # Attach log file to Allure report
    with open("./logs/reqres-api/test_get_user_by_id.log", "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)

#FIXTURE WITH TEARDOWN
@pytest.fixture
def new_user():
    filename = "./logs/reqres-api/test_create_user.log"
    setup_logger(filename)
    user_data = {
        "name": "TEST_USER",
        "email": "test_user@gmail.com",

        "gender": "male",
        "status": "active"
    }
    response = requests.post(GOREST_API_URL, headers=GOREST_HEADERS, json=user_data)
    assert response.status_code == 201, f"Failed to create user - status code: {response.status_code}"
    logger.info("User created successfully")
    created_user = response.json()

    yield created_user

    user_id = created_user["id"]
    if user_id:
        response=requests.delete(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)
        assert response.status_code == 204, f"Failed to delete user - status code: {response.status_code}"
        logger.info("User deleted successfully")
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log",attachment_type=allure.attachment_type.TEXT)

def test_get_specific_user(new_user):
    logger.info(f"Created user: {new_user}")
    user_id = new_user["id"]
    response = requests.get(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)
    assert response.status_code == 200, f"Failed to fetch user - status code: {response.status_code}"
    logger.info("Successfully fetched user")
    assert response.json()["name"] == "TEST_USER", f"Unexpected user name - {response.json()['name']}"
    logger.info("user name matches expected value")
    # Attach log file to Allure report
    with open("./logs/reqres-api/test_create_user.log", "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
