import pytest
import allure

from Task_2.helpers import generate_user_data
from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    INCORRECT_CREDENTIALS_MESSAGE,
    INCORRECT_CREDENTIALS,
    INCORRECT_LOGIN_FIELDS,
)
from Task_2.urls import register_user, login_user


#Тесты для логина пользователя
@allure.epic("Stellar Burgers API")
@allure.feature("Авторизация пользователя")
class TestUserLogin:
    

    @allure.story("Авторизация пользователя")
    @allure.title("Логин под существующим пользователем")
    def test_login_existing_user(self, user_cleanup):
        # Создаем пользователя
        user_data = generate_user_data()
        
        with allure.step("Создаем пользователя"):
            register_response = register_user(user_data)
            register_body = register_response.json()
            register_token = register_body.get("accessToken")
        
        # Логинимся под пользователем
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"],
        }
        
        with allure.step("Отправляем запрос на логин"):
            response = login_user(login_payload)
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
        
        with allure.step(f"Отправляем запрос с {incorrect_credentials['description']}"):
            response = login_user({
                "email": incorrect_credentials["email"],
                "password": incorrect_credentials["password"],
            })
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
        
        with allure.step("Создаем пользователя"):
            register_user(user_data)
        
        # Формируем данные для логина с неверным полем
        login_payload = {
            "email": user_data["email"],
            "password": user_data["password"],
        }
        login_payload[incorrect_field["field"]] = incorrect_field["incorrect_value"]
        
        with allure.step(f"Пытаемся залогиниться с {incorrect_field['description']}"):
            response = login_user(login_payload)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == INCORRECT_CREDENTIALS_MESSAGE
        
        user_cleanup(user_data)
