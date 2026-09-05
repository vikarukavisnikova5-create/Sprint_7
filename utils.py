import random
import string
import time

import allure
import requests


BASE_URL = 'https://qa-scooter.praktikum-services.ru/api/v1'

COLOR_BLACK = 'BLACK'
COLOR_GREY = 'GREY'

RETRYABLE_STATUS_CODES = {502, 503, 504}

@allure.step('Выполнить запрос с повторами при 502/503/504')
def request_with_retry(method: str, url: str, retries: int = 3, delay: float = 1.0, **kwargs):
    """
    Делает запрос requests.request(method, url, **kwargs).
    Если сервис ответил 502/503/504 (его собственный сбой, а не ошибка
    в данных запроса), повторяет запрос ещё несколько раз перед тем,
    как вернуть результат вызывающему коду.
    """
    response = None
    for attempt in range(retries):
        response = requests.request(method, url, **kwargs)
        if response.status_code not in RETRYABLE_STATUS_CODES:
            return response
        if attempt < retries - 1:
            time.sleep(delay)
    return response


def generate_random_string(length: int) -> str:
    """Строка из случайных букв нижнего регистра заданной длины."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_courier_data() -> dict:
    """Генерирует уникальные данные курьера для регистрации."""
    return {
        'login': generate_random_string(10),
        'password': generate_random_string(10),
        'firstName': generate_random_string(10),
    }


def generate_order_data(color: list | None = None) -> dict:
    """Генерирует тело запроса на создание заказа. color можно не передавать."""
    payload = {
        'firstName': generate_random_string(8),
        'lastName': generate_random_string(8),
        'address': f'{generate_random_string(6)} street, 1',
        'metroStation': '4',
        'phone': f'+7{random.randint(1000000000, 9999999999)}',
        'rentTime': random.randint(1, 7),
        'deliveryDate': '2025-12-30',
        'comment': generate_random_string(15),
    }
    if color is not None:
        payload['color'] = color
    return payload
