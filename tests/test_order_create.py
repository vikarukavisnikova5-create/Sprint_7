import allure
import pytest

from utils import COLOR_BLACK, COLOR_GREY


@allure.feature('Заказ')
@allure.story('Создание заказа')
class TestOrderCreate:

    @allure.title('Можно создать заказ с выбранным набором цветов')
    @pytest.mark.parametrize(
        'created_order',
        [
            None,
            [COLOR_BLACK],
            [COLOR_GREY],
            [COLOR_BLACK, COLOR_GREY],
        ],
        ids=['без цвета', 'BLACK', 'GREY', 'BLACK и GREY'],
        indirect=True,
    )
    def test_create_order_with_different_colors(self, created_order):
        response = created_order['response']

        assert response.status_code == 201
        assert 'track' in response.json()
