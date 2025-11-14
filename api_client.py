import requests
from typing import Optional, Dict, Any, List
from .config import get_settings
from .endpoints import (
    REGISTER_USER,
    LOGIN_USER,
    REFRESH_TOKEN,
    GET_USER,
    UPDATE_USER,
    DELETE_USER,
    GET_INGREDIENTS,
    CREATE_ORDER,
    GET_ORDERS,
)

#Клиент для взаимодействия с API Stellar Burgers
class StellarBurgersAPIClient:
    
    def __init__(self, base_url: Optional[str] = None):
        self.base_url = (base_url or get_settings().base_url).rstrip("/")
        self.token: Optional[str] = None
        self.refresh_token: Optional[str] = None
    
    #Создание заголовков с токеном авторизации
    def _get_headers(self, token: Optional[str] = None) -> Dict[str, str]:
        auth_token = token or self.token

        return {"Authorization": auth_token} if auth_token else {}
    
    #Базовый метод для выполнения HTTP запросов
    def _make_request(
        self,
        method: str,
        endpoint: str,
        token: Optional[str] = None,
        json: Optional[Dict[str, Any]] = None
    ) -> requests.Response:
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers(token)

        return requests.request(method=method, url=url, headers=headers, json=json)
    
    # Методы для работы с аутентификацией
    # Регистрация нового пользователя
    def register_user(self, email: str, password: str, name: str) -> requests.Response:
        payload = {"email": email, "password": password, "name": name}
        response = self._make_request("POST", REGISTER_USER, json=payload)
        
        # Сохраняем токены при успешной регистрации
        if response.status_code in [200, 201]:
            body = response.json()
            self.token = body.get("accessToken")
            self.refresh_token = body.get("refreshToken")
        
        return response
    
    # Авторизация пользователя
    def login_user(self, email: str, password: str) -> requests.Response:
        payload = {"email": email, "password": password}
        response = self._make_request("POST", LOGIN_USER, json=payload)
        
        # Сохраняем токены при успешной авторизации
        if response.status_code in [200, 201]:
            body = response.json()
            self.token = body.get("accessToken")
            self.refresh_token = body.get("refreshToken")
        
        return response
    
    # Обновление токена доступа
    def refresh_token(self, refresh_token_value: Optional[str] = None) -> requests.Response:
        token_value = refresh_token_value or self.refresh_token
        payload = {"token": token_value}
        response = self._make_request("POST", REFRESH_TOKEN, json=payload)
        
        # Обновляем токены при успешном обновлении
        if response.status_code in [200, 201]:
            body = response.json()
            self.token = body.get("accessToken")
            self.refresh_token = body.get("refreshToken")
        
        return response
    
    # Получение данных о пользователе
    def get_user(self, token: Optional[str] = None) -> requests.Response:
        return self._make_request("GET", GET_USER, token=token)
    
    # Изменение данных пользователя
    def update_user(
        self,
        payload: Dict[str, Any],
        token: Optional[str] = None
    ) -> requests.Response:

        return self._make_request("PATCH", UPDATE_USER, token=token, json=payload)
    
    # Удаление пользователя
    def delete_user(self, token: Optional[str] = None) -> requests.Response:
        
        return self._make_request("DELETE", DELETE_USER, token=token)
    
    # Методы для работы с ингредиентами
    # Получение списка ингредиентов
    def get_ingredients(self, token: Optional[str] = None) -> requests.Response:
        
        return self._make_request("GET", GET_INGREDIENTS, token=token)
    
    # Методы для работы с заказами
    # Создание заказа
    def create_order(
        self,
        ingredient_ids: List[str],
        token: Optional[str] = None
    ) -> requests.Response:
        payload = {"ingredients": ingredient_ids}

        return self._make_request("POST", CREATE_ORDER, token=token, json=payload)
    
    # Получение заказов пользователя
    def get_orders(self, token: Optional[str] = None) -> requests.Response:
        
        return self._make_request("GET", GET_ORDERS, token=token)
    
    # Установка токена авторизации
    def set_token(self, token: str) -> None:
        self.token = token
    
    # Установка refresh token
    def set_refresh_token(self, refresh_token: str) -> None:
        self.refresh_token = refresh_token

