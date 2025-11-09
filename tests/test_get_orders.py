import pytest
import allure

from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    UNAUTHORIZED_MESSAGE,
)
from Task_2.urls import get_ingredients, create_order, get_orders


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestGetOrders:

    @allure.story("Получение заказов")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_authorization(self, authenticated_user):
        # Получаем свежий токен из фикстуры
        token = authenticated_user["token"]
        
        # Получаем список ингредиентов
        with allure.step("Получаем список ингредиентов"):
            ingredients_response = get_ingredients(token)
            ingredients_body = ingredients_response.json()
            
            # Берем первые два ингредиента для создания заказа
            ingredient_ids = [ingredients_body["data"][0]["_id"], ingredients_body["data"][1]["_id"]]
        
        # Создаем заказ, чтобы у пользователя были заказы
        order_payload = {"ingredients": ingredient_ids}
        
        with allure.step("Создаем заказ для пользователя"):
            create_order(token, order_payload)
        
        # Получаем заказы пользователя
        with allure.step("Получаем заказы пользователя"):
            response = get_orders(token)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и структуру ответа"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "orders" in body
            assert isinstance(body["orders"], list)
            assert "total" in body
            assert "totalToday" in body
            # Проверяем структуру заказа, если есть заказы
            if body["orders"]:
                order = body["orders"][0]
                assert "_id" in order
                assert "ingredients" in order
                assert "status" in order
                assert "name" in order
                assert "createdAt" in order
                assert "updatedAt" in order
                assert "number" in order

    @allure.story("Получение заказов")
    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_authorization(self):
        with allure.step("Пытаемся получить заказы без авторизации"):
            response = get_orders(None)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == UNAUTHORIZED_MESSAGE

