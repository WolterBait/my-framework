import pytest

from src.main.api.classes.api_manager import ApiManager
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest

@pytest.fixture
def create_user_info(api_manager: ApiManager):
    """Передаёт данные для создания пользователя и авторизации под ним"""
    create_user_req = CreateUserRequest(username="Max220", password="Pas!sw0rd", role="ROLE_USER")
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def create_user_request(api_manager: ApiManager):
    """Создаёт обычного пользователя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max220", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def create_user_request_credit(api_manager: ApiManager):
    """Создаёт пользователя кредито-получателя и авторизуется под ним"""
    create_user_req = CreateUserRequest(username="Max111", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)
    return create_user_req # Возращаем просто тело запроса


@pytest.fixture
def deposit_account_request(api_manager: ApiManager):
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
def deposit_account_invalid_request_bad_request(api_manager: ApiManager):
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
def deposit_account_invalid_request_unauthorized(api_manager: ApiManager):
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


@pytest.fixture
def transfer_account_request(api_manager: ApiManager):
    """
    Создаёт обычного пользователя, авторизуется, создаёт аккаунт,
    отправляет запрос с валидными данными
    """
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max221", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт №1
    create_account_req_one = api_manager.user_steps.create_account(create_user_req)
    # Создаём аккаунт №2
    create_account_req_two = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта №1
    id_account_one = create_account_req_one.id
    # Сохраняем id из тела ответа созданного счёта №2
    id_account_two = create_account_req_two.id

    # Пополняем банковский счёт
    deposit_account_req = DepositAccountRequest(accountId=id_account_one, amount=1000)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    # Готовим запрос на перевод
    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_one, toAccountId=id_account_two, amount=500)

    return create_user_req, deposit_account_req, transfer_account_req, id_account_one, id_account_two  # Возращаем просто тело запроса


@pytest.fixture
def transfer_account_invalid_request_unauthorized(api_manager: ApiManager):
    """
    Создаёт обычного пользователя, авторизуется, создаёт аккаунт,
    отправляет запрос с невалидными данными
    """
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max224", password="Pas!sw0rd", role="ROLE_USER")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт №1
    create_account_req_one = api_manager.user_steps.create_account(create_user_req)
    # Создаём аккаунт №2
    create_account_req_two = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта №1
    id_account_one = create_account_req_one.id
    # Сохраняем id из тела ответа созданного счёта №2
    id_account_two = create_account_req_two.id

    # Пополняем банковский счёт
    deposit_account_req = DepositAccountRequest(accountId=id_account_one, amount=1000)
    api_manager.user_steps.deposit_account(create_user_req, deposit_account_req)

    # Готовим запрос на перевод
    transfer_account_req = TransferAccountRequest(fromAccountId=id_account_one, toAccountId=id_account_two, amount=500)

    return deposit_account_req, transfer_account_req, id_account_one, id_account_two  # Возращаем просто тело запроса


@pytest.fixture
def credit_repay_request(api_manager: ApiManager):
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max225", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта
    id_account = create_account_req.id

    # Запрашиваем кредит
    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req, create_user_req)

    # Сохраняем id_credit
    id_credit = credit.creditId

    # Полностью закрываем открытый ранее кредит
    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=5000)

    return create_user_req, credit_request_req, credit_repay_req, id_credit  # Возращаем просто тело запроса


@pytest.fixture
def credit_repay_invalid_request_unprocessable_entity(api_manager: ApiManager):
    # Создаем пользователя, авторизуемся
    create_user_req = CreateUserRequest(username="Max225", password="Pas!sw0rd", role="ROLE_CREDIT_SECRET")
    api_manager.admin_steps.create_user(create_user_req)

    # Создаём аккаунт
    create_account_req = api_manager.user_steps.create_account(create_user_req)

    # Сохраняем id из тела ответа созданного счёта
    id_account = create_account_req.id

    # Запрашиваем кредит
    credit_request_req = CreditRequestRequest(accountId=id_account, amount=5000, termMonths=12)
    credit = api_manager.user_steps.credit_request(credit_request_req, create_user_req)

    # Сохраняем id_credit
    id_credit = credit.creditId

    # Не полностью закрываем открытый ранее кредит
    credit_repay_req = CreditRepayRequest(creditId=id_credit, accountId=id_account, amount=4000)

    return create_user_req, credit_request_req, credit_repay_req, id_credit  # Возращаем просто тело запроса

