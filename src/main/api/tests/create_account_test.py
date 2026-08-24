import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestCreateAccount:
    # Создание и получение токена админа для создания обычного юзера
    def test_create_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        # Создаём пользователя, авторизуемся, создаём аккаунт
        response = api_manager.user_steps.create_account(create_user_request)

        # Проверка корректности создания и баланса
        assert response.balance == 0

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, response.id)
        assert account_from_db.id == response.id, 'Аккаунт не создан, ID нет в бд'
        assert account_from_db.balance is not None, 'Поле balance отсутствует в БД'

    # Проверка сценария попытки создать счёт под авторизацией admin - ОР 403
    def test_create_account_invalid_forbidden(self, api_manager: ApiManager, db_session: Session):
        before_count = Account.count_all(db_session)
        api_manager.user_steps.create_account_invalid_forbidden()

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        after_count = Account.count_all(db_session)
        assert before_count == after_count, 'Аккаунт создан, хотя ожидалась ошибка 403'