import allure
import requests

from utils import BASE_URL


@allure.feature('Заказ')
@allure.story('Список заказов')
class TestOrdersList:

    @allure.title('Тело ответа содержит список заказов')
    def test_get_orders_list_returns_orders(self):
        response = requests.get(f'{BASE_URL}/orders')

        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)
