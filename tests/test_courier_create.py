import allure
import pytest
import requests

from utils import BASE_URL


@allure.feature('Курьер')
@allure.story('Создание курьера')
class TestCourierCreate:

    @allure.title('Можно создать курьера')
    def test_create_courier_success(self, courier_data):
        response = requests.post(f'{BASE_URL}/courier', json=courier_data)

        assert response.status_code == 201
        assert response.json() == {'ok': True}

    @allure.title('Нельзя создать двух одинаковых курьеров')
    def test_create_duplicate_courier_returns_error(self, courier_data):
        first_response = requests.post(f'{BASE_URL}/courier', json=courier_data)
        assert first_response.status_code == 201

        second_response = requests.post(f'{BASE_URL}/courier', json=courier_data)

        assert second_response.status_code == 409
        assert 'message' in second_response.json()

        # чистим за собой курьера, созданного вручную в этом тесте
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={'login': courier_data['login'], 'password': courier_data['password']},
        )
        courier_id = login_response.json()['id']
        requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title('Нельзя создать курьера без обязательного поля "{missing_field}"')
    @pytest.mark.parametrize('missing_field', ['login', 'password'])
    def test_create_courier_without_required_field(self, courier_data, missing_field):
        # login и password обязательны для создания курьера.
        payload = courier_data.copy()
        payload.pop(missing_field)

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        assert response.status_code == 400
        assert 'message' in response.json()

    @allure.title('Курьера можно создать без необязательного поля "firstName"')
    def test_create_courier_without_first_name(self, courier_data):
        # firstName у этого API не обязателен: курьер создаётся и без него.
        payload = courier_data.copy()
        payload.pop('firstName')

        response = requests.post(f'{BASE_URL}/courier', json=payload)

        assert response.status_code == 201
        assert response.json() == {'ok': True}

        # чистим за собой курьера
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={'login': courier_data['login'], 'password': courier_data['password']},
        )
        courier_id = login_response.json()['id']
        requests.delete(f'{BASE_URL}/courier/{courier_id}')

    @allure.title('Нельзя создать курьера с логином, который уже занят')
    def test_create_courier_with_existing_login(self, courier_data):
        first_response = requests.post(f'{BASE_URL}/courier', json=courier_data)
        assert first_response.status_code == 201

        duplicate_login_payload = {
            'login': courier_data['login'],
            'password': 'anotherPassword123',
            'firstName': 'AnotherName',
        }
        response = requests.post(f'{BASE_URL}/courier', json=duplicate_login_payload)

        assert response.status_code == 409
        assert 'message' in response.json()

        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={'login': courier_data['login'], 'password': courier_data['password']},
        )
        courier_id = login_response.json()['id']
        requests.delete(f'{BASE_URL}/courier/{courier_id}')
