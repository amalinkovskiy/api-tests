
import pytest
import requests

BASE_URL = "http://127.0.0.1:8000"

@pytest.fixture
def uuid1():
    user_data = {
        "name": "Jane Doe",
        "age": 28,
        "profession": "Data Analyst",
        "salary": 65000.00
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    response.raise_for_status()
    user = response.json()
    print(user)
    assert "uuid" in user
    return user["uuid"]

def test_create_user(uuid1):
    assert uuid1 is not None

def test_get_user_by_uuid(uuid1):
    response = requests.get(f"{BASE_URL}/users/{uuid1}")
    response.raise_for_status()
    user = response.json()
    assert user["name"] == "Jane Doe"
    assert user["age"] == 28
    assert user["profession"] == "Data Analyst"
    assert user["salary"] == 65000.00

def test_create_second_user():
    user_data = {
        "name": "John Doe",
        "age": 22,
        "profession": "Project Manager",
        "salary": 90001.0
    }
    response = requests.post(f"{BASE_URL}/users/", json=user_data)
    response.raise_for_status()
    user = response.json()
    assert "uuid" in user
    assert user["name"] == "John Doe"
    assert user["age"] == 22
    assert user["profession"] == "Project Manager"
    assert user["salary"] == 90001.0
