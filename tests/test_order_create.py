import allure
import pytest
import requests

from utils import BASE_URL, COLOR_BLACK, COLOR_GREY, generate_order_data


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
    def test_create_order_with_different_colors(self, color):
        payload = generate_order_data(color=color)

        response = requests.post(f'{BASE_URL}/orders', json=payload)

        assert response.status_code == 201
        assert 'track' in response.json()

        track = response.json()['track']
        requests.put(f'{BASE_URL}/orders/cancel', params={'track': track})
