import pytest
import requests

from utils import BASE_URL, generate_courier_data, generate_order_data


@pytest.fixture
def courier_data():
    """Просто данные для регистрации курьера, без создания на сервере."""
    return generate_courier_data()


@pytest.fixture
def registered_courier():
    """
    Создаёт курьера на сервере и гарантированно удаляет его после теста,
    даже если тест сам успел (или не успел) удалить курьера.
    Возвращает dict с login/password/firstName и id (id заполняется лениво).
    """
    data = generate_courier_data()
    response = requests.post(f'{BASE_URL}/courier', json=data)
    assert response.status_code == 201, 'Не удалось создать курьера для теста'

    state = {**data, 'id': None, 'deleted': False}

    yield state

    if state['deleted']:
        return

    courier_id = state['id']
    if courier_id is None:
        login_response = requests.post(
            f'{BASE_URL}/courier/login',
            json={'login': data['login'], 'password': data['password']},
        )
        if login_response.status_code == 200:
            courier_id = login_response.json().get('id')

    if courier_id is not None:
        requests.delete(f'{BASE_URL}/courier/{courier_id}')


@pytest.fixture
def created_order():
    data = generate_order_data()

    response = requests.post(
        f'{BASE_URL}/orders',
        json=data,
    )

    assert response.status_code == 201, (
        f'Не удалось создать заказ для теста: '
        f'{response.status_code} {response.text}'
    )

    track = response.json().get('track')

    assert track is not None, 'API не вернул track созданного заказа'

    state = {
        'response': response,
        'track': track,
    }

    yield state

    requests.put(
        f'{BASE_URL}/orders/cancel',
        params={'track': track},
    )




