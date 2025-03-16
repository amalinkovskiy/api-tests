
import requests
import pytest

def test_post_user():
    response = requests.post('http://127.0.0.1:8000/users/', json={
        'name': 'Jane Doe',
        'age': 28,
        'profession': 'Data Analyst',
        'salary': 65000.00
    })
    assert response.status_code == 200
    assert 'uuid' in response.json()
    return response.json().get('uuid')

def test_extract_uuid():
    uuid1 = test_post_user()
    assert isinstance(uuid1, str)
    assert len(uuid1) == 36
