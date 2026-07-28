import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        # Создаем аккаунт
        acc = api_manager.user_steps.create_account(create_user_request)

        # Проверка валидности баланса счёта
        assert acc.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = acc.id

        # Пополнение счёта созданного пользователем
        deposit_account_request = DepositAccountRequest(accountId=id_account, amount=1000)
        response = api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД - Таблица Account
        account_from_db = Account.get_account_by_id(db_session, deposit_account_request.accountId)
        assert account_from_db.balance == deposit_account_request.amount, 'Значения баланса не равно значению пополнения в бд'



    # Проверка негативного сценария - некорректное тело запроса - ОР 400
    def test_deposit_account_invalid_400(self, api_manager, create_user_request, db_session: Session):
        # Создаем аккаунт
        acc = api_manager.user_steps.create_account(create_user_request)

        assert acc.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = acc.id

        # Пополнение счёта созданного пользователем
        deposit_account_request = DepositAccountRequest(accountId=id_account, amount=-1000)
        api_manager.user_steps.deposit_account_invalid_400(deposit_account_request, create_user_request)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_request.accountId)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 401"



    # Проверка негативного - пользователь не авторизован - ОР 401
    def test_deposit_account_invalid_401(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        # Создаем аккаунт
        acc = api_manager.user_steps.create_account(create_user_request)

        assert acc.balance == 0

        # Сохраняем id из тела ответа созданного счёта
        id_account = acc.id

        # Пополнение счёта созданного пользователем
        deposit_account_request = DepositAccountRequest(accountId=id_account, amount=1000)
        api_manager.user_steps.deposit_account_invalid_401(deposit_account_request)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, id_account)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 401"


