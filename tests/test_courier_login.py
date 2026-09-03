import allure
import pytest

from courier_api import login_courier

@allure.feature('Курьер')
@allure.story('Авторизация курьера')
class TestCourierLogin:

    @allure.title('Курьер может авторизоваться с корректными данными')
    def test_login_success_returns_id(self, registered_courier):
         response = login_courier({
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        })
 
         assert response.status_code == 200
         assert 'id' in response.json()

    @allure.title('Нельзя авторизоваться без поля "{missing_field}"')
    @pytest.mark.parametrize(
        'missing_field, expected_status',
        [
            ('login', 400),
            ('password', 504),
        ],
    )
    def test_login_without_required_field(
        self,
        registered_courier,
        missing_field,
        expected_status,
    ):
        payload = {
            'login': registered_courier['login'],
            'password': registered_courier['password'],
        }
        payload.pop(missing_field)

        response = login_courier(payload)

        assert response.status_code == expected_status

    @allure.title('Нельзя авторизоваться с неверным паролем')
    def test_login_with_wrong_password(self, registered_courier):
        response = login_courier({
            'login': registered_courier['login'],
            'password': 'wrongPassword',
        })

        assert response.status_code == 404
        assert 'message' in response.json()

    @allure.title('Нельзя авторизоваться с несуществующим логином')
    def test_login_with_nonexistent_login(self):
        response = login_courier({
            'login': 'nonexistent_login_xyz',
            'password': 'somePassword',
        })

        assert response.status_code == 404
        assert 'message' in response.json()