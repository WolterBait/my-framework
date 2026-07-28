import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.models.account_table import Account
from src.main.api.fixstures.db_fixture import db_session
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.db.crud.account_crud import AccountCrudDb as Account
from src.main.api.db.crud.transaction_crud import TransactionCrudDb as Transaction
from sqlalchemy.orm import Session
from src.main.api.models.create_user_request import CreateUserRequest


@pytest.mark.api
class TestTransferAccount:
    # Перевод между счетами одного пользователя.
    def test_transfer_account_valid_one_user(self, api_manager: ApiManager, create_user_request: CreateUserRequest, db_session: Session):
        # Создаем 2 аккаунта
        acc_1 = api_manager.user_steps.create_account(create_user_request)
        acc_2 = api_manager.user_steps.create_account(create_user_request)

        # Сохраняем id из тела ответа созданного счёта
        id1_account = acc_1.id
        id2_account = acc_2.id

        # Пополнение счёта созданного пользователем
        deposit_account_request = DepositAccountRequest(accountId=id1_account, amount=1000)
        api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        # Перевод средств с аккаунта 1 на аккаунт 2
        transfer_account_request = TransferAccountRequest(fromAccountId=id1_account, toAccountId=id2_account, amount=500)
        response = api_manager.user_steps.transfer_account(transfer_account_request, create_user_request)

        assert transfer_account_request.fromAccountId == id1_account
        assert transfer_account_request.toAccountId == id2_account
        assert response.fromAccountIdBalance == deposit_account_request.amount - response.fromAccountIdBalance


        # ДОБАВЛЯЕМ ПРОВЕРКИ БД - Таблица Account
        account_from_db = Account.get_account_by_id(db_session, id1_account)
        assert account_from_db.balance == deposit_account_request.amount - transfer_account_request.amount

        # Добавляем проверки БД - Таблица Transaction
        transaction_from_db_t1 = Transaction.get_transaction_by_from_account_id(db_session, id1_account)
        assert transaction_from_db_t1.from_account_id == transfer_account_request.fromAccountId

        transaction_from_db_t2 = Transaction.get_transaction_by_to_account_id(db_session, id2_account)
        assert transaction_from_db_t2.to_account_id == transfer_account_request.toAccountId




    # Проверка отработки ошибки в случае, если пользователь не авторизован
    def test_transfer_account_invalid_401(self, api_manager, create_user_request, db_session: Session):
        # Создаем 2 аккаунта
        acc_1 = api_manager.user_steps.create_account(create_user_request)
        acc_2 = api_manager.user_steps.create_account(create_user_request)

        # Сохраняем id из тела ответа созданного счёта
        id1_account = acc_1.id
        id2_account = acc_2.id

        # Пополнение счёта созданного пользователем
        deposit_account_request = DepositAccountRequest(accountId=id1_account, amount=1000)
        api_manager.user_steps.deposit_account(deposit_account_request, create_user_request)

        # Перевод средств с аккаунта 1 на аккаунт 2
        transfer_account_request = TransferAccountRequest(fromAccountId=id1_account, toAccountId=id2_account, amount=500)
        api_manager.user_steps.transfer_account_invalid_401(transfer_account_request)


        # ДОБАВЛЯЕМ ПРОВЕРКИ БД - Таблица Account
        account_from_db = Account.get_account_by_id(db_session, id2_account)
        assert account_from_db.balance == 0

        # Добавляем проверки БД - Таблица Transaction
        transaction_from_db_t1 = Transaction.get_transaction_by_from_account_id(db_session, id1_account)
        assert transaction_from_db_t1 is None