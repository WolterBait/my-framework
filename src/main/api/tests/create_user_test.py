import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.db.crud.user_crud import UserCrudDb as User
from sqlalchemy.orm import Session


@pytest.mark.api
class TestCreateUser:
    # Создание и получение токена админа для создания обычного юзера
    def test_create_user_valid(self, api_manager: ApiManager, create_user_info, db_session: Session):
        # Создаём пользователя
        create_user_req = create_user_info # Распаковываем
        response = api_manager.admin_steps.create_user(create_user_req)

        assert create_user_info.username == response.username
        assert create_user_info.role == response.role

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        user_from_db = User.get_user_by_username(db_session, create_user_info.username)
        assert user_from_db.username == create_user_info.username, 'Созданного пользователя нет в базе данных'


        # Используем параметризацию pytest для обработки нескольких сценариев
    @pytest.mark.parametrize(
        "username, password",
        [
            ("Никита", "Pas!sw0rd"), # сценарий №1: невалидное имя | кириллица (кириллица - нельзя)
            ("ff", "Pas!sw0rd"),     # сценарий №2: невалидное имя | 2 символа (минимум 3 символа)
            ("abv!", "Pas!sw0rd"),   # сценарий №3: невалидное имя | символ ! (спец. символы запрещены)
            ("max1", "Pas!sw0rд"),   # сценарий №4: невалидный пароль | кириллица (кириллица - нельзя)ww
            ("max2", "Pas!sw0"),     # сценарий №5: невалидный пароль | от 8 символов
            ("max3", "pass!w5rd"),   # сценарий №6: невалидный пароль | Нет хотя-бы одной заглавной буквы
            ("max4", "PASS!W5RD"),   # сценарий №7: невалидный пароль | Нет хотя-бы одной маленькой буквы
            ("max5", "pass!word"),   # сценарий №8: невалидный пароль | Нет хотя-бы одной цифры
            ("max5", "pass5word"),   # сценарий №9: невалидный пароль | Нет хотя-бы одного спец. символа
        ]
    )


    def test_create_user_invalid_bad_request(self, db_session: Session, username: str, password: str, api_manager: ApiManager):
        # Создаём пользователя с заранее некорректными данными (негативные проверки)
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user_bad_request(create_user_request)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'Пользователь создан, ошибка'

    # ОР - 401
    def test_create_user_invalid_unauthorized(self, db_session: Session, api_manager: ApiManager):
        create_user_request = CreateUserRequest(username="Max2", password="Pas!sw0rd", role="ROLE_USER")
        api_manager.admin_steps.create_invalid_user_unauthorized(create_user_request)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        user_from_db = User.get_user_by_username(db_session, create_user_request.username)
        assert user_from_db is None, 'Пользователь создан, ошибка'