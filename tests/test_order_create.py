import allure
import pytest

from order_api import cancel_order, create_order
from utils import COLOR_BLACK, COLOR_GREY, generate_order_data


@allure.feature('Заказ')
@allure.story('Создание заказа')
class TestOrderCreate:

    @allure.title('Можно создать заказ с цветом(-ами): {color}')
    @pytest.mark.parametrize(
        'color',
        [
            None,
            [COLOR_BLACK],
            [COLOR_GREY],
            [COLOR_BLACK, COLOR_GREY],
        ],
        ids=['без цвета', 'BLACK', 'GREY', 'BLACK и GREY'],
    )
    def test_create_order_with_different_colors(self, color, request):
        payload = generate_order_data(color=color)

        response = create_order(payload)
        track = response.json().get('track')
        if track is not None:

         request.addfinalizer(lambda: cancel_order(track))

        assert response.status_code == 201
        assert 'track' in response.json()
