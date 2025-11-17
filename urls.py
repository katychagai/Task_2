import requests
from .config import get_settings


def base_url():
    return get_settings().base_url.rstrip("/")

#Создание заголовков с токеном авторизации 
def _get_headers(token):
    return {"Authorization": token} if token else {}

#Создание пользователя
def register_user(payload):
    return requests.post(f"{base_url()}/api/auth/register", json=payload)

#Логин пользователя
def login_user(payload):
    return requests.post(f"{base_url()}/api/auth/login", json=payload)

#Обновление токена
def refresh_token(refresh_token_value):
    return requests.post(f"{base_url()}/api/auth/token", json={"token": refresh_token_value})

#Получение данных о пользователе
def get_user(token):
    return requests.get(f"{base_url()}/api/auth/user", headers=_get_headers(token))

#Изменение данных о пользователе
def update_user(token, payload):
    return requests.patch(f"{base_url()}/api/auth/user", headers=_get_headers(token), json=payload)

#Удаление пользователя
def delete_user(token):
    return requests.delete(f"{base_url()}/api/auth/user", headers=_get_headers(token))

#Получение списка ингредиентов
def get_ingredients(token):
    return requests.get(f"{base_url()}/api/ingredients", headers=_get_headers(token))

#Создание заказа
def create_order(token, payload):
    return requests.post(f"{base_url()}/api/orders", headers=_get_headers(token), json=payload)

#Получение заказов конкретного пользователя
def get_orders(token):
    return requests.get(f"{base_url()}/api/orders", headers=_get_headers(token))

