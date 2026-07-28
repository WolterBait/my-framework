import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    # Корректное погашение кредита
    def test_credit_repay_valid(self, api_manager: ApiManager, create_user_request_credit: CreditRequestRequest, db_session: Session):
        # 1. Создаём пользователя, авторизуемся, создаём аккаунт
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        # 2. Сохраняем id счёта
        id_account = acc.id

        # 3. Запрашиваем кредит
        credit_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        credit = api_manager.user_steps.credit_request(credit_request, create_user_request_credit)

        id_credit = credit.creditId

        # 4. Полностью закрываем открытый ранее кредит
        credit_repay_request = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=5000)
        response = api_manager.user_steps.credit_repay(credit_repay_request, create_user_request_credit)

        # Проверяем данные из тела ответа на валидность
        assert credit_repay_request.creditId == id_credit
        assert response.amountDeposited == credit_repay_request.amount

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id(db_session, id_account)
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == 0



    # Суммы недостаточно для погашения кредита - ОР 422
    def test_credit_repay_invalid_422(self, api_manager: ApiManager, create_user_request_credit: CreateUserRequest, db_session: Session):
        # 1. Создаём пользователя, авторизуемся, создаём аккаунт
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        # 2. Сохраняем id счёта
        id_account = acc.id

        # 3. Запрашиваем кредит
        credit_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        credit = api_manager.user_steps.credit_request(credit_request, create_user_request_credit)

        id_credit = credit.creditId

        # 4. Неполностью закрываем открытый ранее кредит
        credit_repay_request = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=4000)
        api_manager.user_steps.credit_repay_invalid_422(credit_repay_request, create_user_request_credit)

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id(db_session, id_account)
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -credit_request.amount