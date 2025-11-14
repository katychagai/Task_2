
import allure

from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    UNAUTHORIZED_MESSAGE,
)
from Task_2.api_client import StellarBurgersAPIClient


@allure.epic("Stellar Burgers API")
@allure.feature("Получение заказов пользователя")
class TestGetOrders:

    @allure.story("Получение заказов")
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_authorization(self, authenticated_user):
        # Получаем свежий токен из фикстуры
        token = authenticated_user["token"]
        client = StellarBurgersAPIClient()
        
        # Получаем список ингредиентов
        with allure.step("Получаем список ингредиентов"):
            ingredients_response = client.get_ingredients(token=token)
            ingredients_body = ingredients_response.json()
            
            # Берем первые два ингредиента для создания заказа
            ingredient_ids = [ingredients_body["data"][0]["_id"], ingredients_body["data"][1]["_id"]]
        
        # Создаем заказ, чтобы у пользователя были заказы
        with allure.step("Создаем заказ для пользователя"):
            client.create_order(ingredient_ids, token=token)
        
        # Получаем заказы пользователя
        with allure.step("Получаем заказы пользователя"):
            response = client.get_orders(token=token)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и структуру ответа"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "orders" in body
            assert isinstance(body["orders"], list)
            assert len(body["orders"]) > 0
            assert "total" in body
            assert "totalToday" in body
            
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
        client = StellarBurgersAPIClient()
        
        with allure.step("Пытаемся получить заказы без авторизации"):
            response = client.get_orders(token=None)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == UNAUTHORIZED_MESSAGE

