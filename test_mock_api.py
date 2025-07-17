import pytest
import requests
import logging
import allure
logger = logging.getLogger(__name__)

# Set up logger for test output

def setup_logger(log_filename):
    logger.handlers.clear()
    handler =logging.FileHandler(log_filename, mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

# Helper function for assertions and logging

def log_assert(condition, message, results):
    try:
        assert condition
        logger.info(f"Assertion passed: {message}")
    except Exception as e:
        logger.error(f"Assertion failed: {message} : {e}")
        results.append(f"Assertion failed: {message} : {e}")

# Function to get user data from API

def get_user(n):
    response = requests.get(f"https://jsonplaceholder.typicode.com/users/{n}")
    return response

# Test GET user with mock response

def test_get_mock_user(mocker):
    filename = "./logs/mock-api/test_get_mock_user.log"
    setup_logger(filename)
    results = []
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Leanne Graham",
        "username": "Bret",
        "email": "Sincere@april.biz"
    }
    mocker.patch("requests.get", return_value=mock_response)
    user = get_user(1)
    logger.info(f"Mocked GET user - Status: {user.status_code}")
    logger.info(f"Mocked Response JSON: {user.json()}")
    print(user.json())
    log_assert(user.status_code == 200, "User status code is 200", results)
    log_assert(user.json() == mock_response.json.return_value, "User JSON response matched", results)
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:{results}"

# Test POST user with mock response

def test_post_mock_user(mocker):
    filename = "./logs/mock-api/test_post_mock_user.log"
    setup_logger(filename)
    results = []
    mock_response = mocker.Mock()
    mock_response.status_code = 201
    mock_response.json.return_value = {
        "id": 11,
        "name": "New User",
        "username": "newuser",
        "email": "newuser@example.com"
    }
    mocker.patch("requests.post", return_value=mock_response)
    payload = {
        "name": "New User",
        "username": "newuser",
        "email": "newuser@example.com"
    }
    response = requests.post("https://jsonplaceholder.typicode.com/users", json=payload)
    logger.info(f"Mocked POST user - Status: {response.status_code}")
    logger.info(f"Mocked POST Response JSON: {response.json()}")
    log_assert(response.status_code == 201, "User created with status 201", results)
    log_assert(response.json()["name"] == payload["name"], "User name matches", results)
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log POST", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:{results}"

# Test PUT user with mock response

def test_put_mock_user(mocker):
    filename = "./logs/mock-api/test_put_mock_user.log"
    setup_logger(filename)
    results = []
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Updated User",
        "username": "Bret",
        "email": "updated@example.com"
    }
    mocker.patch("requests.put", return_value=mock_response)
    payload = {
        "name": "Updated User",
        "username": "Bret",
        "email": "updated@example.com"
    }
    response = requests.put("https://jsonplaceholder.typicode.com/users/1", json=payload)
    logger.info(f"Mocked PUT user - Status: {response.status_code}")
    logger.info(f"Mocked PUT Response JSON: {response.json()}")
    log_assert(response.status_code == 200, "User updated with status 200", results)
    log_assert(response.json()["name"] == payload["name"], "User name updated", results)
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log PUT", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:{results}"

# Test DELETE user with mock response

def test_delete_mock_user(mocker):
    filename = "./logs/mock-api/test_delete_mock_user.log"
    setup_logger(filename)
    results = []
    mock_response = mocker.Mock()
    mock_response.status_code = 204
    mock_response.text = ""
    mocker.patch("requests.delete", return_value=mock_response)
    response = requests.delete("https://jsonplaceholder.typicode.com/users/1")
    logger.info(f"Mocked DELETE user - Status: {response.status_code}")
    log_assert(response.status_code == 204, "User deleted with status 204", results)
    with open(filename, "r") as log_file:
        allure.attach(log_file.read(), name="Test Log DELETE", attachment_type=allure.attachment_type.TEXT)
    assert not results, f"Test failed with errors:{results}"