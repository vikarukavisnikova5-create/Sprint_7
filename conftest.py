import pytest

from courier_api import create_courier, delete_courier, login_courier
from order_api import cancel_order, create_order
from utils import BASE_URL, generate_courier_data, generate_order_data


@pytest.fixture
def courier_data():
    """Данные для регистрации курьера, без создания курьера на сервере.
    Если тест сам создаст курьера этими данными, фикстура удалит его
    после теста"""
    data = generate_courier_data()

    yield data

    login_response = login_courier({'login': data['login'], 'password': data['password']})
    if login_response.status_code == 200:
        delete_courier(login_response.json()['id'])


@pytest.fixture
def registered_courier():
    """
    Создаёт курьера на сервере и гарантированно удаляет его после теста,
    даже если тест сам успел (или не успел) удалить курьера.
    Возвращает dict с login/password/firstName, id и deleted
    """
    data = generate_courier_data()
    create_courier(data)

    state = {**data, 'id': None, 'deleted': False}

    yield state

    if state['deleted']:
        return

    courier_id = state['id']
    if courier_id is None:
        login_response = login_courier({'login': data['login'], 'password': data['password']})
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')

    if courier_id is not None:
        delete_courier(courier_id)


@pytest.fixture
def created_order():
    """Создаёт заказ на сервере и гарантированно отменяет его после теста."""
    data = generate_order_data()

    response = create_order(data)
    track = response.json().get('track')

    state = {
        'response': response,
        'track': track,
    }

    yield state

    if track is not None:
        cancel_order(track)