import pytest
from rest_framework.test import APIClient
from datetime import datetime
# from .test_auth_user import test_login_user_success

client = APIClient()


@pytest.mark.django_db
def test_pv_view_post(user):
    payload = {
        'email': 'tester@mail.com',
        'password': 'Hard6573Password',
    }

    response = client.post('/api/v1/login/', payload)

    # POST TEST

    for i in range(1, 4):
        payload = {
            'file': open(
                f'pv_api/tests/files/file_measure_{i}.csv', 'r'
            )
        }

        response = client.post('/api/v1/pv-analysis/', payload)

        assert response.status_code == 201
        assert response.data.get('pv_data', False)

    # GET TEST
    payload = {
        'min_temperature': 52
    }

    response = client.get('/api/v1/pv-analysis/', payload)

    assert response.status_code == 200
    assert response.data[0].get('temperature', False)
    assert response.data[0].get('temperature') == 55.7
    assert response.data[0].get('module_type') == 'Dato1'
    assert response.data[0].get('reference') == 'Dato2'

    payload = {
        'max_temperature': 52
    }

    response = client.get('/api/v1/pv-analysis/', payload)

    assert response.status_code == 200
    assert response.data[0].get('temperature', False)
    assert response.data[0].get('temperature') == 51.2
    assert response.data[1].get('temperature', False)
    assert response.data[1].get('temperature') == 40.8
    assert response.data[0].get('module_type') == 'Dato1'
    assert response.data[1].get('module_type') == 'Dato1'
    assert response.data[0].get('reference') == 'Dato2'
    assert response.data[1].get('reference') == 'Dato2'

    # PUT TEST

    id_test = response.data[0].get('id')

    payload = {
        'id': id_test,
        'temperature': 50.2,
        'module_type': 'Policristalino',
        'reference': 'Blue Sun solar',
        'measure_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    response = client.put('/api/v1/pv-analysis/', payload)

    assert response.status_code == 201
    assert response.data.get('temperature', False)
    assert response.data.get('temperature') == '50.2'
    assert response.data.get('module_type') == 'Policristalino'
    assert response.data.get('reference') == 'Blue Sun solar'

    # DELETE TEST
    id_test = response.data.get('id')

    payload = {'id': id_test}

    response = client.delete('/api/v1/pv-analysis/', payload)

    assert response.status_code == 200

    response = client.get('/api/v1/pv-analysis/')
    assert response.status_code == 200
    assert not any([int(id_test) == item['id'] for item in response.data])
