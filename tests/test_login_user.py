import pytest
import allure

from Task_2.helpers import generate_user_data, prepare_login_data
from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    INCORRECT_CREDENTIALS_MESSAGE,
    INCORRECT_CREDENTIALS,
    INCORRECT_LOGIN_FIELDS,
)
from Task_2.api_client import StellarBurgersAPIClient


#Тесты для логина пользователя
@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestUserLogin:
    

    @allure.story("Авторизация пользователя")
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, user_cleanup):
        # Создаем пользователя
        user_data = generate_user_data()
        client = StellarBurgersAPIClient()
        
        with allure.step("Создаем пользователя"):
            register_response = client.register_user(
                user_data["email"],
                user_data["password"],
                user_data["name"]
            )
            register_body = register_response.json()
            register_token = register_body.get("accessToken")
        
        # Логинимся под пользователем
        with allure.step("Отправляем запрос на логин"):
            response = client.login_user(
                user_data["email"],
                user_data["password"]
            )
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и успешный логин"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "accessToken" in body
            assert "refreshToken" in body
            assert body["accessToken"].startswith("Bearer ")
            assert "user" in body
            assert body["user"].get("email") == user_data["email"]
        
        # Передаем токен из ответа регистрации для очистки (не из логина)
        user_cleanup(user_data, token=register_token)

    @allure.story("Login user")
    @allure.title("Логин с несуществующими логином и паролем")
    @pytest.mark.parametrize("incorrect_credentials", INCORRECT_CREDENTIALS)
    def test_login_with_incorrect_credentials(self, incorrect_credentials):
        allure.dynamic.title(f"Логин с {incorrect_credentials['description']}")
        client = StellarBurgersAPIClient()
        
        with allure.step(f"Отправляем запрос с {incorrect_credentials['description']}"):
            response = client.login_user(
                incorrect_credentials["email"],
                incorrect_credentials["password"]
            )
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == INCORRECT_CREDENTIALS_MESSAGE

    @allure.story("Авторизация пользователя")
    @allure.title("Логин существующего пользователя с неверным полем (email или password)")
    @pytest.mark.parametrize("incorrect_field", INCORRECT_LOGIN_FIELDS)
    def test_login_with_incorrect_field(self, incorrect_field, user_cleanup):
        allure.dynamic.title(f"Логин с {incorrect_field['description']}")
        
        # Создаем пользователя
        user_data = generate_user_data()
        client = StellarBurgersAPIClient()
        
        with allure.step("Создаем пользователя"):
            client.register_user(
                user_data["email"],
                user_data["password"],
                user_data["name"]
            )
        
        # Формируем данные для логина с неверным полем
        email, password = prepare_login_data(user_data, incorrect_field)
        
        with allure.step(f"Пытаемся залогиниться с {incorrect_field['description']}"):
            response = client.login_user(email, password)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == INCORRECT_CREDENTIALS_MESSAGE
        
        user_cleanup(user_data)
