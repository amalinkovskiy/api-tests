
import requests
import pytest

BASE_URL = "http://127.0.0.1:8000/users/"

@pytest.fixture(scope="module")
def create_user():
    data = {
        "name": "Jane Doe",
        "age": 28,
        "profession": "Data Analyst",
        "salary": 65000.00
    }
    response = requests.post(BASE_URL, json=data)
    response.raise_for_status()  # Ensure we notice bad responses
    uuid1 = response.json().get('uuid')
    print("Response from POST request:", response.json())
    print("UUID from POST request:", uuid1)
    return uuid1

def test_create_user(create_user):
    response = requests.get(f"{BASE_URL}{create_user}")
    response.raise_for_status()  # Ensure we notice bad responses
    user_data = response.json()
    assert user_data['name'] == "Jane Doe"
    assert user_data['age'] == 28
    assert user_data['profession'] == "Data Analyst"
    assert user_data['salary'] == 65000.00
    print("Response from GET request:", user_data)

def test_get_user_by_uuid(create_user):
    response = requests.get(f"{BASE_URL}{create_user}")
    response.raise_for_status()  # Ensure we notice bad responses
    user_data = response.json()
    assert user_data['name'] == "Jane Doe"
    assert user_data['age'] == 28
    assert user_data['profession'] == "Data Analyst"
    assert user_data['salary'] == 65000.00
    print("Response from GET request:", user_data)

if __name__ == "__main__":
    pytest.main(['-s'])
