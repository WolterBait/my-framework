from enum import Enum
from dataclasses import dataclass
from typing import Optional, Type
from src.main.api.models.base_model import BaseModel
from src.main.api.models.auth_login_response import LoginUserResponse
from src.main.api.models.auth_login_request import LoginUserRequest
from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_repay_response import CreditRepayResponse
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.deposit_account_response import DepositAccountResponse
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.models.transfer_account_response import TransferAccountResponse


@dataclass
class EndpointConfiguration:
    url: str
    request_model: Optional[Type[BaseModel]]
    response_model: Optional[Type[BaseModel]]


class Endpoint(Enum):
    ADMIN_CREATE_USER = EndpointConfiguration(
        url='/admin/create',
        request_model=CreateUserRequest,
        response_model=CreateUserResponse
    )

    LOGIN_USER = EndpointConfiguration(
        url='/auth/token/login',
        request_model=LoginUserRequest,
        response_model=LoginUserResponse
    )

    ACCOUNT_CREATE = EndpointConfiguration(
        url='/account/create',
        request_model=None,
        response_model=CreateAccountResponse
    )

    DEPOSIT_ACCOUNT = EndpointConfiguration(
        url='/account/deposit',
        request_model=DepositAccountRequest,
        response_model=DepositAccountResponse
    )

    TRANSFER_ACCOUNT = EndpointConfiguration(
        url='/account/transfer',
        request_model=TransferAccountRequest,
        response_model=TransferAccountResponse
    )

    CREDIT_REQUEST = EndpointConfiguration(
        url='/credit/request',
        request_model=CreditRequestRequest,
        response_model=CreditRequestResponse
    )

    CREDIT_REPAY = EndpointConfiguration(
        url='/credit/repay',
        request_model=CreditRepayRequest,
        response_model=CreditRepayResponse
    )

    ADMIN_DELETE_USER = EndpointConfiguration(
        url='/admin/users',
        request_model=None,
        response_model=None
    )



