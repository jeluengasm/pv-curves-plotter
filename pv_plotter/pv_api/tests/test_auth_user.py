import pytest
from rest_framework.test import APIClient

client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = {
        'email': 'tester@mail.com',
        'password': 'Hard6573Password',
        'password2': 'Hard6573Password',
        'first_name': 'John',
        'last_name': 'Doe',
        'username': 'doe_john',
        'phone_number': '3456546789',
    }

    response = client.post('/api/v1/register/', payload)

    data = response.data.get('user')

    assert data['first_name'] == payload['first_name']
    assert data['last_name'] == payload['last_name']
    assert data['email'] == payload['email']
    assert data['username'] == payload['username']
    assert payload['password'] not in data


@pytest.mark.django_db
def test_login_user_success(user):
    payload = {
        'email': 'tester@mail.com',
        'password': 'Hard6573Password',
    }

    response = client.post('/api/v1/login/', payload)

    data = response.data

    assert response.status_code == 200
    assert data.get('token', False)
    assert data.get('user', False)

    user_data = data.get('user')

    assert user_data['email'] == payload['email']
    assert user_data.get('first_name', False)
    assert user_data.get('last_name', False)
    assert user_data.get('username', False)


@pytest.mark.django_db
def test_login_user_fail():
    payload = {
        'email': 'tester_false@mail.com',
        'password': 'HardPassword',
    }

    response = client.post('/api/v1/login/', payload)

    assert response.status_code == 400


@pytest.mark.django_db
def test_logout_user(user):
    response = client.post('/api/v1/logout/')

    assert response.status_code == 200
