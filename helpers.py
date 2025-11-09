import time
from faker import Faker
from .urls import update_user, login_user, refresh_token
from .data import STATUS_CREATED, STATUS_UNAUTHORIZED

fake = Faker()

#генерируем уникальные данные пользователя
def generate_user_data(email=None):
    if email is None:
        # Генерируем уникальный email с timestamp для гарантии уникальности
        timestamp = int(time.time() * 1000) 
        base_email = fake.email()
        email = base_email.replace("@", f"+{timestamp}@")
    
    user_data = {
        "email": email,
        "password": fake.password(length=12),
        "name": fake.first_name(),
    }
    return user_data

#Генерирует новое значение для указанного поля пользователя
def generate_field_value(field):
    generators = {
        "email": lambda: generate_user_data()["email"],
        "name": lambda: fake.first_name(),
        "password": lambda: fake.password(length=12),
    }
    return generators[field]()

#Обновляет данные пользователя с автоматическим обновлением токена при необходимости
def update_user_with_auto_refresh(authenticated_user, payload):
    
    token = authenticated_user["token"]
    user_data = authenticated_user["user_data"]
    
    # Делаем запрос на обновление
    response = update_user(token, payload)
    
    # Если токен истек (401), обновляем его
    if response.status_code == STATUS_UNAUTHORIZED:
        refresh_token_value = authenticated_user.get("refresh_token")
        
        # Пробуем обновить через refresh_token
        if refresh_token_value:
            refresh_response = refresh_token(refresh_token_value)
            if refresh_response.status_code == STATUS_CREATED:
                refresh_body = refresh_response.json()
                token = refresh_body.get("accessToken")
                authenticated_user["token"] = token
                authenticated_user["refresh_token"] = refresh_body.get("refreshToken")
                # Повторяем запрос с новым токеном
                response = update_user(token, payload)
        
        # Если refresh_token не сработал или все еще 401, перелогиниваемся
        if response.status_code == STATUS_UNAUTHORIZED:
            login_response = login_user({
                "email": user_data["email"],
                "password": user_data["password"]
            })
            if login_response.status_code == STATUS_CREATED:
                login_body = login_response.json()
                token = login_body.get("accessToken")
                authenticated_user["token"] = token
                authenticated_user["refresh_token"] = login_body.get("refreshToken")
                # Повторяем запрос с новым токеном
                response = update_user(token, payload)
    
    return response
