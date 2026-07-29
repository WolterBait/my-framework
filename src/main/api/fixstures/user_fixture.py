import pytest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest


@pytest.fixture
def create_user_request(api_manager):
    """Создаёт обычного пользователя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max220", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def create_user_request_credit(api_manager):
    """Создаёт пользователя кредито-получателя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max111", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def deposit_account_request(api_manager):
    """
    Создаёт обычного пользователя, авторизуется, создаёт аккаунт,
    отправляет запрос с валидными данными
    """
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max221", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта
    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=1000)
    return create_user_req, deposit_account_req # Возращаем просто тело запроса


@pytest.fixture
def deposit_account_invalid_request_400(api_manager):
    """
    Создаёт обычного пользователя, авторизуется, создаёт аккаунт,
    отправляет запрос с невалидными данными
    """
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max222", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта
    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=-1000)
    return create_user_req, deposit_account_req # Возращаем просто тело запроса


@pytest.fixture
def deposit_account_invalid_request_401(api_manager):
    """
    Создаёт обычного пользователя, авторизуется, создаёт аккаунт,
    отправляет запрос с невалидными данными
    """
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max223", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта
    id_account = create_account_req.id

    deposit_account_req = DepositAccountRequest(accountId=id_account, amount=1000)
    return deposit_account_req # Возращаем просто тело запроса




