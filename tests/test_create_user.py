import pytest
import allure

from Task_2.helpers import generate_user_data
from Task_2.data import (
    REQUIRED_FIELDS,
    STATUS_CREATED,
    STATUS_FORBIDDEN,
    USER_ALREADY_EXISTS_MESSAGE,
    MISSING_FIELDS_MESSAGE,
)
from Task_2.urls import register_user


@allure.epic("Stellar Burgers API")
@allure.feature("Cоздание пользователя")
class TestUserCreation:

    @allure.story("Создание пользователя")
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_cleanup):
        # Генерируем уникальные данные пользователя
        user_data = generate_user_data()
        
        with allure.step("Отправляем запрос на создание пользователя"):
            response = register_user(user_data)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и успешное создание"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "user" in body
            assert body["user"].get("email") == user_data["email"]
            assert body["user"].get("name") == user_data["name"]
            assert "accessToken" in body
            assert "refreshToken" in body
            assert body["accessToken"].startswith("Bearer ")
        
        # Передаем токен из ответа регистрации для очистки
        user_cleanup(user_data, token=body.get("accessToken"))

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_duplicate_user(self, user_cleanup):
        # Создаем первого пользователя
        user_data = generate_user_data()
        
        with allure.step("Создаем первого пользователя"):
            first_response = register_user(user_data)
        
        # Пытаемся создать пользователя с тем же email
        duplicate_data = generate_user_data(email=user_data["email"])
        
        with allure.step("Пытаемся создать пользователя с существующим email"):
            response = register_user(duplicate_data)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 403 и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("success") is False
            assert body.get("message") == USER_ALREADY_EXISTS_MESSAGE
        
        # Передаем токен из ответа первой регистрации для очистки
        first_body = first_response.json()
        token = first_body.get("accessToken") if first_response.status_code == STATUS_CREATED else None
        user_cleanup(user_data, token=token)

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", REQUIRED_FIELDS)
    def test_create_user_without_required_field(self, missing_field):
        allure.dynamic.title(f"Создание пользователя без обязательного поля: {missing_field}")
        user_data = generate_user_data()
        user_data.pop(missing_field)
        
        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            response = register_user(user_data)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 403 и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("success") is False
            assert body.get("message") == MISSING_FIELDS_MESSAGE
