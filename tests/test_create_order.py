
import allure
from Task_2.data import (
    STATUS_CREATED,
    STATUS_UNAUTHORIZED,
    STATUS_BAD_REQUEST,
    STATUS_INTERNAL_SERVER_ERROR,
    UNAUTHORIZED_MESSAGE,
    INGREDIENT_IDS_MUST_BE_PROVIDED_MESSAGE,
    TEST_INGREDIENT_IDS,
)
from Task_2.api_client import StellarBurgersAPIClient


@allure.epic("Stellar Burgers API")
@allure.feature("Создание заказа")
class TestCreateOrder:

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_authorization_and_ingredients(self, authenticated_user):
        # Получаем свежий токен из фикстуры
        token = authenticated_user["token"]
        client = StellarBurgersAPIClient()
        
        # Получаем список ингредиентов
        with allure.step("Получаем список ингредиентов"):
            ingredients_response = client.get_ingredients(token=token)
            ingredients_body = ingredients_response.json()
            
            # Берем первые два ингредиента
            ingredient_ids = [ingredients_body["data"][0]["_id"], ingredients_body["data"][1]["_id"]]
        
        # Создаем заказ
        with allure.step("Создаем заказ с ингредиентами"):
            response = client.create_order(ingredient_ids, token=token)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 200 и успешное создание заказа"):
            assert response.status_code == STATUS_CREATED
            assert body.get("success") is True
            assert "name" in body
            assert "order" in body
            assert "number" in body["order"]

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с авторизацией без ингредиентов")
    def test_create_order_with_authorization_without_ingredients(self, authenticated_user):
        # Получаем свежий токен из фикстуры
        token = authenticated_user["token"]
        client = StellarBurgersAPIClient()
        
        # Создаем заказ без ингредиентов
        with allure.step("Создаем заказ без ингредиентов"):
            response = client.create_order([], token=token)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 400 и сообщение об ошибке"):
            assert response.status_code == STATUS_BAD_REQUEST
            assert body.get("success") is False
            assert body.get("message") == INGREDIENT_IDS_MUST_BE_PROVIDED_MESSAGE

    @allure.story("Создание заказа")
    @allure.title("Создание заказа без авторизации. тест ожидает 401. API позволяет создавать заказы без авторизации, поэтому тест падает")
    def test_create_order_without_authorization(self):
        client = StellarBurgersAPIClient()
        
        # Создаем заказ без авторизации
        with allure.step("Создаем заказ без авторизации"):
            response = client.create_order(TEST_INGREDIENT_IDS, token=None)
            body = response.json()
            allure.attach(str(body), "response.json", allure.attachment_type.JSON)
        
        with allure.step("Проверяем код ответа 401 и сообщение об ошибке"):
            #API возвращает 200, а тест ожидает 401. API позволяет создавать заказы без авторизации, поэтому тест падает.
            assert response.status_code == STATUS_UNAUTHORIZED
            assert body.get("success") is False
            assert body.get("message") == UNAUTHORIZED_MESSAGE

    @allure.story("Создание заказа")
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    def test_create_order_with_invalid_ingredients(self, authenticated_user):
        # Получаем свежий токен из фикстуры
        token = authenticated_user["token"]
        client = StellarBurgersAPIClient()
        
        # Создаем заказ с неверным хешем ингредиентов
        with allure.step("Создаем заказ с неверным хешем ингредиентов"):
            response = client.create_order(
                ["invalid_hash_123", "invalid_hash_456"],
                token=token
            )
        
        with allure.step("Проверяем код ответа 500 Internal Server Error"):
            assert response.status_code == STATUS_INTERNAL_SERVER_ERROR

