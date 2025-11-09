import pytest
import allure

from Task_2.helpers import update_user_with_auto_refresh, generate_field_value
from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    UNAUTHORIZED_MESSAGE,
    USER_UPDATEABLE_FIELDS,
)
from Task_2.urls import update_user


@allure.epic("Stellar Burgers API")
@allure.feature("Изменение данных пользователя")
class TestUserUpdate:

    @allure.story("Изменение данных пользователя")
    @allure.title("Изменение поля пользователя с авторизацией")
    @pytest.mark.parametrize("field", USER_UPDATEABLE_FIELDS)
    def test_update_user_field_with_authorization(self, field, authenticated_user):
        allure.dynamic.title(f"Изменение поля {field} с авторизацией")
        
        # Генерируем новое значение для поля
        new_value = generate_field_value(field)
        
        # Обновляем поле
        update_payload = {field: new_value}

        with allure.step(f"Обновляем поле {field}"):
            response = update_user_with_auto_refresh(authenticated_user, update_payload)
            body = response.json()
            
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и успешное обновление поля"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "user" in body
            # Проверяем, что поле обновлено (для password поле не возвращается в ответе)
            if field != "password":
                assert body["user"].get(field) == new_value

    @allure.story("Update user")
    @allure.title("Изменение поля пользователя без авторизации")
    @pytest.mark.parametrize("field", USER_UPDATEABLE_FIELDS)
    def test_update_user_field_without_authorization(self, field):
        allure.dynamic.title(f"Изменение поля {field} без авторизации")
        
        # Генерируем новое значение для поля
        new_value = generate_field_value(field)
        
        # Пытаемся обновить поле без авторизации
        update_payload = {field: new_value}
        
        with allure.step(f"Пытаемся обновить поле {field} без авторизации"):
            response = update_user(None, update_payload)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == UNAUTHORIZED_MESSAGE
