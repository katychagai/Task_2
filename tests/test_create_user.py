import pytest
import allure

from Task_2.helpers import generate_user_data, prepare_register_data_without_field
from Task_2.data import (
    REQUIRED_FIELDS,
    STATUS_CREATED,
    STATUS_FORBIDDEN,
    USER_ALREADY_EXISTS_MESSAGE,
    MISSING_FIELDS_MESSAGE,
)
from Task_2.api_client import StellarBurgersAPIClient


@allure.epic("Stellar Burgers API")
@allure.feature("Cоздание пользователя")
class TestUserCreation:

    @allure.story("Создание пользователя")
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, user_cleanup):
        # Генерируем уникальные данные пользователя
        user_data = generate_user_data()
        client = StellarBurgersAPIClient()
        
        with allure.step("Отправляем запрос на создание пользователя"):
            response = client.register_user(
                user_data["email"],
                user_data["password"],
                user_data["name"]
            )
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
        client = StellarBurgersAPIClient()
        
        with allure.step("Создаем первого пользователя"):
            first_response = client.register_user(
                user_data["email"],
                user_data["password"],
                user_data["name"]
            )
            first_body = first_response.json()
            token = first_body["accessToken"]
        
        # Пытаемся создать пользователя с тем же email
        duplicate_data = generate_user_data(email=user_data["email"])
        
        with allure.step("Пытаемся создать пользователя с существующим email"):
            response = client.register_user(
                duplicate_data["email"],
                duplicate_data["password"],
                duplicate_data["name"]
            )
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 403 и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("success") is False
            assert body.get("message") == USER_ALREADY_EXISTS_MESSAGE
        
        # Передаем токен из ответа первой регистрации для очистки
        user_cleanup(user_data, token=token)

    @allure.story("Создание пользователя")
    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", REQUIRED_FIELDS)
    def test_create_user_without_required_field(self, missing_field):
        allure.dynamic.title(f"Создание пользователя без обязательного поля: {missing_field}")
        user_data = generate_user_data()
        client = StellarBurgersAPIClient()
        
        # Формируем данные с пустым значением для отсутствующего поля
        email, password, name = prepare_register_data_without_field(user_data, missing_field)
        
        with allure.step(f"Отправляем запрос без поля {missing_field}"):
            response = client.register_user(email, password, name)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 403 и сообщение об ошибке"):
            assert response.status_code == STATUS_FORBIDDEN
            assert body.get("success") is False
            assert body.get("message") == MISSING_FIELDS_MESSAGE
