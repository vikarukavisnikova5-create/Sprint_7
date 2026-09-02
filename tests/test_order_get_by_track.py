import allure
import requests

from utils import BASE_URL


@allure.feature('Заказ')
@allure.story('Получить заказ по номеру')
class TestOrderGetByTrack:

    @allure.title('Успешный запрос возвращает объект с заказом')
    def test_get_order_by_track_success(self, created_order):
        response = requests.get(
            f'{BASE_URL}/orders/track',
            params={'t': created_order['track']},
        )

        assert response.status_code == 200
        assert 'order' in response.json()

    @allure.title('Запрос без номера заказа возвращает ошибку')
    def test_get_order_by_track_without_track(self):
        response = requests.get(f'{BASE_URL}/orders/track')

        assert response.status_code == 400
        assert 'message' in response.json()

    @allure.title('Запрос с несуществующим номером заказа возвращает ошибку')
    def test_get_order_by_track_nonexistent(self):
        response = requests.get(f'{BASE_URL}/orders/track', params={'t': 999999999})

        assert response.status_code == 404
        assert 'message' in response.json()
