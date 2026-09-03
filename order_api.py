import allure
import requests
 
from utils import BASE_URL
 
 
@allure.step('Создать заказ')
def create_order(payload: dict):
    return requests.post(f'{BASE_URL}/orders', json=payload)
 
 
@allure.step('Получить список заказов')
def get_orders_list():
    return requests.get(f'{BASE_URL}/orders')
 
 
@allure.step('Получить заказ по номеру {track}')
def get_order_by_track(track):
    return requests.get(f'{BASE_URL}/orders/track', params={'t': track})
 
 
@allure.step('Получить заказ без указания номера')
def get_order_by_track_without_param():
    return requests.get(f'{BASE_URL}/orders/track')
 
 
@allure.step('Отменить заказ с номером {track}')
def cancel_order(track):
    return requests.put(f'{BASE_URL}/orders/cancel', params={'track': track})
 
 
@allure.step('Принять заказ {order_id} курьером {courier_id}')
def accept_order(order_id, courier_id):
    return requests.put(
        f'{BASE_URL}/orders/accept/{order_id}',
        params={'courierId': courier_id},
    )
 
 
@allure.step('Принять заказ {order_id} без указания курьера')
def accept_order_without_courier_id(order_id):
    return requests.put(f'{BASE_URL}/orders/accept/{order_id}')
 
 
@allure.step('Принять заказ без указания id заказа, курьер {courier_id}')
def accept_order_without_order_id(courier_id):
    return requests.put(
        f'{BASE_URL}/orders/accept/',
        params={'courierId': courier_id},
    )