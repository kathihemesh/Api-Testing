import requests
import logging
from config import GOREST_HEADERS,GOREST_API_URL
import allure

logger = logging.getLogger(__name__)  # Logger setup

def setup_logger(log_filename):
    "Set up a file logger for each test."
    logger.handlers.clear()
    handler = logging.FileHandler(log_filename, mode="w")
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    # Set up file logger for each test

def log_assert(condition, message, results,):
    "Custom assertion helper for logging and collecting failures."
    try:
        assert condition
        logger.info(f"Assertion passed: {message}")
    except AssertionError as e:
        logger.error(f"Assertion failed: {message} : {e}")
        results.append(f"Assertion failed: {message} : {e}")

user_id=""

    # Global variable to store user id

def test_get_users():
    "Test fetching all users and checking response is a list."
    filename = "./logs/gorest-api/test_get_users.log"
    setup_logger(filename)
    results = []
    response = requests.get(GOREST_API_URL)
    logger.info(f"GET {GOREST_API_URL} - Status: {response.status_code}")
    logger.info(f"Response JSON: {response.text}")
    assert response.status_code == 200, f"Failed to fetch users - status code: {response.status_code}"
    logger.info("Successfully fetched users")
    log_assert(isinstance(response.json(), list), "Response is a list", results)
    # Attach log to Allure report
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:\n {results}"

    # Test fetching all users

def test_create_user():
    "Test creating a user and checking all fields."
    global user_id
    filename = "./logs/gorest-api/test_create_user.log"
    setup_logger(filename)
    results = []
    payload = {
        "name": "ganesh123",
        "email": "ganesh12@gmail.com",
        "gender": "male",
        "status": "active"
    }
    response = requests.post(GOREST_API_URL, headers=GOREST_HEADERS, json=payload)
    logger.info(f"POST {GOREST_API_URL} - Status: {response.status_code}")
    logger.info(f"Payload: {payload}")
    logger.info(f"Response JSON: {response.text}")
    assert response.status_code == 201, f"Failed to create user - status code: {response.status_code}"
    logger.info("User created successfully")
    data = response.json()
    # Intentionally failing assertion for demonstration
    log_assert(data["name"] == payload["name"], "User name matches", results)
    log_assert(data["email"]+"999" == payload["email"], "User email matches", results)
    log_assert(data["gender"] == payload["gender"], "User gender matches", results)
    log_assert(data["status"] == payload["status"], "User status matches", results)
    user_id = data["id"]
    # Attach log to Allure report
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
    print(results)
    assert not results, f"Test failed with errors: {results}"

    # Test creating a user

def test_update_user():
    "Test updating a user and checking updated fields."
    global user_id
    filename = "./logs/gorest-api/test_update_user.log"
    setup_logger(filename)
    results = []
    update_payload = {
        "name": "ganesh12 Updated",
        "status": "inactive" 
    }
    response = requests.put(f"{GOREST_API_URL}/{user_id+99}", headers=GOREST_HEADERS, json=update_payload)
    logger.info(f"PUT {GOREST_API_URL}/{user_id+99} - Status: {response.status_code}")
    logger.info(f"Payload: {update_payload}")
    logger.info(f"Response JSON: {response.text}")
    assert response.status_code == 200, f"Failed to update user - status code: {response.status_code}"
    logger.info("User updated successfully")
    data = response.json()
    log_assert(data["name"] == update_payload["name"], "User name updated", results)
    log_assert(data["status"] == update_payload["status"], "User status updated", results)
    # Attach log to Allure report
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:\n {results}"

    # Test updating a user

def test_delete_user():
    "Test deleting a user and checking for successful deletion."
    global user_id
    filename = "./logs/gorest-api/test_delete_user.log"
    setup_logger(filename)
    results = []
    response = requests.delete(f"{GOREST_API_URL}/{user_id}", headers=GOREST_HEADERS)
    logger.info(f"DELETE {user_id}")
    assert response.status_code == 204, f"Failed to delete user - status code: {response.status_code}"
    logger.info("User deleted successfully")
    # Attach log to Allure report
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:\n {results}"

    # Test deleting a user
