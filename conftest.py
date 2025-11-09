import pytest
from .helpers import generate_user_data
from .urls import register_user, login_user, delete_user


#Фикстура для очистки созданных пользователей после тестов
@pytest.fixture(scope="function")
def user_cleanup():
    created_tokens = []
    
    def add_user_for_cleanup(user_data, token=None):
        #Добавляет пользователя для очистки и получает токен
        if token:
            created_tokens.append(token)
        else:
            # Пытаемся залогиниться, чтобы получить токен для удаления
            login_response = login_user({
                "email": user_data["email"],
                "password": user_data["password"],
            })
            if login_response.status_code == 200:
                body = login_response.json()
                token = body.get("accessToken")
                if token:
                    created_tokens.append(token)
    
    yield add_user_for_cleanup
    
    # Удаляем созданных пользователей
    for token in created_tokens:
        delete_user(token)


#Фикстура для генерации данных пользователя
@pytest.fixture
def user_data():
    return generate_user_data()


#Фикстура для получения свежего токена перед каждым запуском
@pytest.fixture(scope="function")
def authenticated_user(user_cleanup):
    user_data = generate_user_data()
    
    # Регистрируем пользователя
    register_response = register_user(user_data)
    
    register_body = register_response.json()
    token = register_body.get("accessToken")
    refresh_token = register_body.get("refreshToken")
    
    # Добавляем пользователя для очистки
    user_cleanup(user_data, token=token)
    
    # Возвращаем данные пользователя
    yield {
        "token": token,
        "refresh_token": refresh_token,
        "user_data": user_data,
    }

