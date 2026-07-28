import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.auth_login_request import LoginUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm import Session

from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestLoginUser:
    def test_login_admin(self, api_manager):
        auth_login_request = LoginUserRequest(username="admin", password="123456")
        response = api_manager.admin_steps.login_user(auth_login_request)

        assert response.user.username == auth_login_request.username
        assert response.user.role == "ROLE_ADMIN"



    @pytest.mark.parametrize(
        "username, password",
        [
            ("", "123456"),  # Отсутствует логин - ОР 400
            ("admin", ""),   # Отсутствует пароль - ОР 400
        ]
    )
    # Негативный кейс авторизации ADMIN - ОР 400
    def test_auth_admin_invalid_400(self, username, password, api_manager):
        # Использую pydantic модель
        auth_login_request = LoginUserRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid_400(auth_login_request)



    @pytest.mark.parametrize(
        "username, password",
        [
            ("admin", "12345"),   # Корректный логин    | Некорректный пароль
            ("adminn", "123456"), # Некорректный логин  | Корректный пароль
        ]
    )
    # Негативный тест-кейс авторизации ADMIN
    def test_auth_admin_invalid_401(self, username, password, api_manager):
        # Использую pydantic модель
        auth_login_request = LoginUserRequest(username=username, password=password)
        api_manager.admin_steps.login_user_invalid_401(auth_login_request)


    # Позитивный кейс авторизации под USER
    def test_login_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        response = api_manager.admin_steps.login_user(create_user_request)

        assert response.user.username == create_user_request.username
        assert response.user.role == create_user_request.role

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db.username == create_user_request.username, 'Созданного пользователя нет в базе данных'


# Некорректная авторизация под пользователем, некорректный пароль
    def test_auth_user_invalid_401(self, api_manager, create_user_request):
        auth_login_request = LoginUserRequest(username="Max000", password="Pas!sw0rd")
        api_manager.admin_steps.login_user_invalid_401(auth_login_request)


