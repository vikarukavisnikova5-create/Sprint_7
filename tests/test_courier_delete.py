import allure

from courier_api import delete_courier, delete_courier_without_id, login_courier


@allure.feature('Курьер')
@allure.story('Удаление курьера')
class TestCourierDelete:

    @allure.title('Успешное удаление курьера возвращает {{"ok": true}}')
    def test_delete_courier_success(self, registered_courier):
         login_response = login_courier({
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        })
         courier_id = login_response.json()['id']
 
         response = delete_courier(courier_id)
 
         assert response.status_code == 200
         assert response.json() == {'ok': True}

    @allure.title('Запрос без id возвращает ошибку')
    def test_delete_courier_without_id(self):
        response = delete_courier_without_id()
 
        assert response.status_code in (400, 404)
 
    @allure.title('Запрос с несуществующим id возвращает ошибку')
    def test_delete_courier_with_nonexistent_id(self):
        response = delete_courier(999999999)
 
        assert response.status_code == 404
        assert 'message' in response.json()
