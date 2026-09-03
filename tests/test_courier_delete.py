import allure
import requests

from utils import BASE_URL


@allure.feature('Курьер')
@allure.story('Удаление курьера')
class TestCourierDelete:

    @allure.title('Успешное удаление курьера возвращает {{"ok": true}}')
    def test_delete_courier_success(self, registered_courier):
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={
                'login': registered_courier['login'],
                'password': registered_courier['password'],
            },
        )
        courier_id = login_response.json()['id']

        response = requests.delete(f'{BASE_URL}/courier/{courier_id}')

        assert response.status_code == 200
        assert response.json() == {'ok': True}

        registered_courier['deleted'] = True

    @allure.title('Запрос без id возвращает ошибку')
    def test_delete_courier_without_id(self):
        response = requests.delete(f'{BASE_URL}/courier/')

        assert response.status_code in (400, 404)

    @allure.title('Запрос с несуществующим id возвращает ошибку')
    def test_delete_courier_with_nonexistent_id(self):
        response = requests.delete(f'{BASE_URL}/courier/999999999')

        assert response.status_code == 404
        assert 'message' in response.json()
