import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.fixstures.db_fixture import db_session
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from sqlalchemy.orm import Session


@pytest.mark.api
class TestTransferAccount:
    # Перевод между счетами одного пользователя.
    def test_transfer_account_valid_one_user(self, api_manager: ApiManager, transfer_account_request, db_session: Session):
        """Используем фикстуру transfer_account_request из user_fixture"""
        create_user_req, deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_request # распаковываем
        response = api_manager.user_steps.transfer_account(create_user_req, transfer_account_req)

        # Проверки API
        assert response.fromAccountId == transfer_account_req.fromAccountId
        assert response.toAccountId == transfer_account_req.toAccountId
        expected_balance = deposit_account_req.amount - transfer_account_req.amount
        assert response.fromAccountIdBalance == expected_balance

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД - Таблица Account
        account_from_db = Account.get_account_by_id(db_session, id_account_one)
        assert account_from_db.balance == expected_balance

        # Добавляем проверки БД - Таблица Transaction
        transaction_from_db_one = Transaction.get_transaction_by_from_account_id(db_session, id_account_one)
        assert transaction_from_db_one.from_account_id == transfer_account_req.fromAccountId

        transaction_from_db_two = Transaction.get_transaction_by_to_account_id(db_session, id_account_two)
        assert transaction_from_db_two.to_account_id == transfer_account_req.toAccountId



    # Проверка отработки ошибки в случае, если пользователь не авторизован
    def test_transfer_account_invalid_unauthorized(self, api_manager: ApiManager, transfer_account_invalid_request_unauthorized, db_session: Session):
        """Используем фикстуру transfer_account_invalid_request_unauthorized из user_fixture"""
        deposit_account_req, transfer_account_req, id_account_one, id_account_two = transfer_account_invalid_request_unauthorized # распаковываем
        api_manager.user_steps.transfer_account_invalid_unauthorized(transfer_account_req)

        # ДОБАВЛЯЕМ ПРОВЕРКИ БД - Таблица Account
        account_from_db = Account.get_account_by_id(db_session, id_account_two)
        assert account_from_db.balance == 0

        # Добавляем проверки БД - Таблица Transaction
        transaction_from_db_one = Transaction.get_transaction_by_from_account_id(db_session, id_account_two)
        assert transaction_from_db_one is None