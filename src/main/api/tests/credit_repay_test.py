import pytest
from sqlalchemy.orm import Session
from src.main.api.classes.api_manager import ApiManager
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRepay:
    # Корректное погашение кредита
    def test_credit_repay_valid(self, api_manager: ApiManager, credit_repay_request, db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_request
        response = api_manager.user_steps.credit_repay(create_user_req, credit_repay_req)

        # Проверяем данные из тела ответа на валидность
        assert credit_repay_req.creditId == id_credit
        assert response.amountDeposited == credit_repay_req.amount

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_repay_req.accountId
        assert credit_from_db.amount == credit_repay_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths
        assert credit_from_db.balance == 0



    # Суммы недостаточно для погашения кредита - ОР 422
    def test_credit_repay_invalid_unprocessable_entity(self, api_manager: ApiManager, credit_repay_invalid_request_unprocessable_entity, db_session: Session):
        create_user_req, credit_request_req, credit_repay_req, id_credit = credit_repay_invalid_request_unprocessable_entity
        api_manager.user_steps.credit_repay_invalid_unprocessable_entity(create_user_req, credit_repay_req)

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id(db_session, credit_request_req.accountId)
        assert credit_from_db.account_id == credit_request_req.accountId
        assert credit_from_db.amount == credit_request_req.amount
        assert credit_from_db.term_months == credit_request_req.termMonths
        assert credit_from_db.balance == -credit_request_req.amount