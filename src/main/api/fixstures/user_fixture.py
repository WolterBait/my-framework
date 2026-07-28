import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.fixture
def create_user_request(api_manager):
    """Создаёт обычного пользователя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def create_user_request_credit(api_manager):
    """Создаёт пользователя кредито-получателя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max111", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса






@pytest.fixture
def create_account_request_1(api_manager, create_user_request):
    """Создаёт банковский счёт для пользователя"""
    account_req = api_manager.user_steps.create_account(create_user_request)
    return account_req.id


@pytest.fixture
def deposit_account_request(api_manager, create_user_request, create_account_request_1):
    """Пополнение созданного счёта"""
    deposit_req = DepositAccountRequest(accountId=create_account_request_1, amount=2000)
    api_manager.user_steps.deposit_account(deposit_req, create_user_request)
    return deposit_req




