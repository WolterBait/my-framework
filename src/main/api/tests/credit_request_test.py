import pytest
from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from sqlalchemy.orm import Session
from src.main.api.db.crud.credit_crud import CreditCrudDb as Credit


@pytest.mark.api
class TestCreditRequest:
    # Корректный запрос на кредит
    def test_credit_request_valid(self, api_manager: ApiManager, create_user_request_credit: CreateUserRequest, db_session: Session):
        # 1. Создаём пользователя, авторизуемся, создаём аккаунт
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        # 2. Сохраняем id счёта
        id_account = acc.id

        # 3. Запрашиваем кредит
        credit_request = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        response = api_manager.user_steps.credit_request(credit_request, create_user_request_credit)

        # 4. Проверки на валидность данных
        assert response.amount == credit_request.amount
        assert response.termMonths == credit_request.termMonths

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id(db_session, id_account)
        assert credit_from_db.account_id == credit_request.accountId
        assert credit_from_db.amount == credit_request.amount
        assert credit_from_db.term_months == credit_request.termMonths
        assert credit_from_db.balance == -credit_request.amount


    # Взятие двух кредитов у одного и того же пользователя
    def test_credit_request_invalid_not_found(self, api_manager: ApiManager, create_user_request_credit: CreateUserRequest, db_session: Session):
        # 1. Создаём пользователя, авторизуемся, создаём аккаунт
        acc = api_manager.user_steps.create_account(create_user_request_credit)

        # 2. Сохраняем id счёта
        id_account = acc.id

        # 3. Запрашиваем кредит
        credit_request_one = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        api_manager.user_steps.credit_request(credit_request_one, create_user_request_credit)

        # 4. Запрашиваем кредит №2 (404)
        credit_request_two = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
        api_manager.user_steps.credit_request_invalid_not_found(credit_request_two, create_user_request_credit)

        # Добавляем проверки БД - Таблица Credit
        credit_from_db = Credit.get_credit_by_account_id_all(db_session, id_account)
        assert len(credit_from_db) == 1