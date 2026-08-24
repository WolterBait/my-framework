import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest

@pytest.mark.api
class TestDepositAccount:
    def test_deposit_account_valid(self, api_manager: ApiManager, deposit_account_request, db_session: Session):
        """Используем фикстуру deposit_account_request из user_fixture"""
        create_user_req, deposit_account_req = deposit_account_request  # распаковываем
        response = api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

        # Проверка баланса из ответа
        assert response.balance == deposit_account_req.amount

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db.balance == deposit_account_req.amount, 'Баланс в БД не совпадает с суммой пополнения'



    # Проверка негативного сценария - некорректное тело запроса - ОР 400
    def test_deposit_account_invalid_bad_request(self, api_manager, deposit_account_invalid_request_bad_request, db_session: Session):
        """Используем фикстуру deposit_account_request_bad_request из user_fixture"""
        create_user_req, deposit_account_req = deposit_account_invalid_request_bad_request  # распаковываем
        api_manager.user_steps.deposit_account_invalid_bad_request(create_user_req, deposit_account_req)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 400"



    # Проверка негативного - пользователь не авторизован - ОР 401
    def test_deposit_account_invalid_unauthorized(self, api_manager: ApiManager, create_user_request: CreateUserRequest, deposit_account_invalid_request_unauthorized, db_session: Session):
        """Используем фикстуру deposit_account_request_unauthorized из user_fixture"""
        deposit_account_req = deposit_account_invalid_request_unauthorized  # распаковываем
        api_manager.user_steps.deposit_account_invalid_unauthorized(deposit_account_req)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД
        account_from_db = Account.get_account_by_id(db_session, deposit_account_req.accountId)
        assert account_from_db is not None, "Счет должен существовать"
        assert account_from_db.balance == 0, "Баланс не должен измениться при ошибке 401"


