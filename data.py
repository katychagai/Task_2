# Обязательные поля для создания пользователя
REQUIRED_FIELDS = ["email", "password", "name"]

# Статус коды ответов
STATUS_CREATED = 200
STATUS_FORBIDDEN = 403
STATUS_UNAUTHORIZED = 401
STATUS_BAD_REQUEST = 400
STATUS_INTERNAL_SERVER_ERROR = 500

# Сообщения об ошибках
USER_ALREADY_EXISTS_MESSAGE = "User already exists"
MISSING_FIELDS_MESSAGE = "Email, password and name are required fields"
INCORRECT_CREDENTIALS_MESSAGE = "email or password are incorrect"
UNAUTHORIZED_MESSAGE = "You should be authorised"

# Поля пользователя, которые можно изменить
USER_UPDATEABLE_FIELDS = ["email", "name", "password"]

# Тестовые данные для логина с неверными учетными данными
INCORRECT_CREDENTIALS = [
    {
        "email": "nonexistent@test.ru",
        "password": "wrongpassword",
        "description": "неверный email и пароль"
    },
    {
        "email": "wrongemail@test.ru",
        "password": "wrongpassword",
        "description": "неверный email и пароль"
    }
]

# Поля для проверки логина с неверными данными (для существующего пользователя)
INCORRECT_LOGIN_FIELDS = [
    {
        "field": "password",
        "incorrect_value": "wrongpassword",
        "description": "неверный пароль"
    },
    {
        "field": "email",
        "incorrect_value": "wrongemail@test.ru",
        "description": "неверный email"
    }
]

# Сообщения об ошибках для заказов
INVALID_INGREDIENTS_MESSAGE = "Invalid ingredients"
INGREDIENT_IDS_MUST_BE_PROVIDED_MESSAGE = "Ingredient ids must be provided"

# Тестовые ID ингредиентов для создания заказов
TEST_INGREDIENT_IDS = ["61c0c5a71d1f82001bdaaa6d", "61c0c5a71d1f82001bdaaa6f"]

