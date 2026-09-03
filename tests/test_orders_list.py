import allure

from order_api import get_orders_list


@allure.feature('Заказ')
@allure.story('Список заказов')
class TestOrdersList:

    @allure.title('Тело ответа содержит список заказов')
    def test_get_orders_list_returns_orders(self):
        response = get_orders_list()

        assert response.status_code == 200
        assert 'orders' in response.json()
        assert isinstance(response.json()['orders'], list)
