import allure

from order_api import get_order_by_track, get_order_by_track_without_param


@allure.feature('Заказ')
@allure.story('Получить заказ по номеру')
class TestOrderGetByTrack:

    @allure.title('Успешный запрос возвращает объект с заказом')
    def test_get_order_by_track_success(self, created_order):
        response = get_order_by_track(created_order['track'])

        assert response.status_code == 200
        assert 'order' in response.json()

    @allure.title('Запрос без номера заказа возвращает ошибку')
    def test_get_order_by_track_without_track(self):
        response = get_order_by_track_without_param()

        assert response.status_code == 400
        assert 'message' in response.json()

    @allure.title('Запрос с несуществующим номером заказа возвращает ошибку')
    def test_get_order_by_track_nonexistent(self):
        response = get_order_by_track(999999999)

        assert response.status_code == 404
        assert 'message' in response.json()
