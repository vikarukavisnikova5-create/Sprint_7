import allure

from courier_api import login_courier
from order_api import (
    accept_order,
    accept_order_without_courier_id,
    accept_order_without_order_id,
    get_order_by_track,
)

@allure.feature('Заказ')
@allure.story('Принять заказ')
class TestOrderAccept:

    @allure.title('Успешное принятие заказа возвращает {{"ok": true}}')
    def test_accept_order_success(self, registered_courier, created_order):
        login_response = login_courier({
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        })
        courier_id = login_response.json()['id']
 
        order_response = get_order_by_track(created_order['track'])
        order_id = order_response.json()['order']['id']
 
        response = accept_order(order_id, courier_id)
 
        assert response.status_code == 200
        assert response.json() == {'ok': True}
 
    @allure.title('Принятие заказа без id курьера возвращает ошибку')
    def test_accept_order_without_courier_id(self, created_order):
        order_response = get_order_by_track(created_order['track'])
        order_id = order_response.json()['order']['id']
 
        response = accept_order_without_courier_id(order_id)
 
        assert response.status_code == 400
        assert 'message' in response.json()
 
    @allure.title('Принятие заказа с неверным id курьера возвращает ошибку')
    def test_accept_order_with_invalid_courier_id(self, created_order):
        order_response = get_order_by_track(created_order['track'])
        order_id = order_response.json()['order']['id']
 
        response = accept_order(order_id, 999999999)
 
        assert response.status_code == 404
        assert 'message' in response.json()
 
    @allure.title('Принятие заказа без id заказа возвращает ошибку')
    def test_accept_order_without_order_id(self, registered_courier):
        login_response = login_courier({
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        })
        courier_id = login_response.json()['id']
 
        response = accept_order_without_order_id(courier_id)
 
        assert response.status_code in (400, 404)
 
    @allure.title('Принятие заказа с неверным id заказа возвращает ошибку')
    def test_accept_order_with_invalid_order_id(self, registered_courier):
        login_response = login_courier({
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        })
        courier_id = login_response.json()['id']
 
        response = accept_order(999999999, courier_id)
 
        assert response.status_code == 404
        assert 'message' in response.json()
 