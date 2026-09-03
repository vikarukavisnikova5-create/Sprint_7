import allure
import requests
 
from utils import BASE_URL
 
 
@allure.step('Создать курьера')
def create_courier(payload: dict):
    return requests.post(f'{BASE_URL}/courier', json=payload)
 
 
@allure.step('Авторизовать курьера')
def login_courier(payload: dict):
    return requests.post(f'{BASE_URL}/courier/login', json=payload)
 
 
@allure.step('Удалить курьера с id {courier_id}')
def delete_courier(courier_id):
    return requests.delete(f'{BASE_URL}/courier/{courier_id}')
 
 
@allure.step('Удалить курьера без указания id')
def delete_courier_without_id():
    return requests.delete(f'{BASE_URL}/courier/')