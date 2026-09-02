import allure
import requests
from utils import BASE_URL
@allure.feature('Заказ')
@allure.story('Принять заказ')
class TestOrderAccept:
    @allure.title('Успешное принятие заказа возвращает {{"ok": true}}')
    def test_accept_order_success(self, registered_courier, created_order):
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={
                'login': registered_courier['login'],
                'password': registered_courier['password'],
            },
        )
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']
        order_response = requests.get(
            f'{BASE_URL}/orders/track',
            params={'t': created_order['track']},
        )
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        response = requests.put(
            f'{BASE_URL}/orders/accept/{order_id}',
            params={'courierId': courier_id},
        )
        assert response.status_code == 200
        assert response.json() == {'ok': True}
    @allure.title('Принятие заказа без id курьера возвращает ошибку')
    def test_accept_order_without_courier_id(self, created_order):
        order_response = requests.get(
            f'{BASE_URL}/orders/track',
            params={'t': created_order['track']},
        )
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        response = requests.put(
            f'{BASE_URL}/orders/accept/{order_id}',
        )
        assert response.status_code == 400
        assert 'message' in response.json()
    @allure.title('Принятие заказа с неверным id курьера возвращает ошибку')
    def test_accept_order_with_invalid_courier_id(self, created_order):
        order_response = requests.get(
            f'{BASE_URL}/orders/track',
            params={'t': created_order['track']},
        )
        assert order_response.status_code == 200
        order_id = order_response.json()['order']['id']
        response = requests.put(
            f'{BASE_URL}/orders/accept/{order_id}',
            params={'courierId': 999999999},
        )
        assert response.status_code == 404
        assert 'message' in response.json()
    @allure.title('Принятие заказа без id заказа возвращает ошибку')
    def test_accept_order_without_order_id(self, registered_courier):
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={
                'login': registered_courier['login'],
                'password': registered_courier['password'],
            },
        )
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']
        response = requests.put(
            f'{BASE_URL}/orders/accept/',
            params={'courierId': courier_id},
        )
        assert response.status_code in (400, 404)
    @allure.title('Принятие заказа с неверным id заказа возвращает ошибку')
    def test_accept_order_with_invalid_order_id(self, registered_courier):
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={
                'login': registered_courier['login'],
                'password': registered_courier['password'],
            },
        )
        assert login_response.status_code == 200
        courier_id = login_response.json()['id']
        response = requests.put(
            f'{BASE_URL}/orders/accept/999999999',
            params={'courierId': courier_id},
        )
        assert response.status_code == 404
        assert 'message' in response.json()



