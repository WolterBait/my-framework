from src.main.api.foundation.requesters.validate_crud_requester import ValidateCrudRequester
from src.main.api.foundation.requesters.crud_requester import CrudRequester
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.deposit_account_request import DepositAccountRequest
from src.main.api.models.transfer_account_request import TransferAccountRequest
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
from src.main.api.steps.base_steps import BaseSteps
from src.main.api.foundation.endpoint import Endpoint


class UserSteps(BaseSteps):
    def create_account(self, create_user_request: CreateUserRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.ACCOUNT_CREATE,
            ResponseSpecs.status_code_created()
        ).post()
        return response


    def create_account_invalid_forbidden(self):
        CrudRequester(
            RequestSpecs.auth_headers(username="admin", password="123456"),
            Endpoint.ACCOUNT_CREATE,
            ResponseSpecs.status_code_forbidden()
        ).post()

#_______________________________________________________________________________________
#_______________________________________________________________________________________

    def deposit_account(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_ok()
        ).post(deposit_account_request)
        return response


    def deposit_account_invalid_bad_request(self, create_user_request: CreateUserRequest, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_bad_request()
        ).post(deposit_account_request)


    def deposit_account_invalid_unauthorized(self, deposit_account_request: DepositAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.DEPOSIT_ACCOUNT,
            ResponseSpecs.status_code_unauthorized()
        ).post(deposit_account_request)

#_______________________________________________________________________________________
#_______________________________________________________________________________________


    def transfer_account(self, create_user_request: CreateUserRequest, transfer_account_request: TransferAccountRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request.username, password=create_user_request.password),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_ok()
        ).post(transfer_account_request)
        return response


    def transfer_account_invalid_unauthorized(self, transfer_account_request: TransferAccountRequest):
        CrudRequester(
            RequestSpecs.no_auth_headers(),
            Endpoint.TRANSFER_ACCOUNT,
            ResponseSpecs.status_code_unauthorized()
        ).post(transfer_account_request)

#_______________________________________________________________________________________
#_______________________________________________________________________________________

    def credit_request(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_created()
        ).post(credit_request_request)
        return response


    def credit_request_invalid_not_found(self, credit_request_request: CreditRequestRequest, create_user_request_credit):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REQUEST,
            ResponseSpecs.status_code_not_found()
        ).post(credit_request_request)

#_______________________________________________________________________________________
#_______________________________________________________________________________________

    def credit_repay(self, create_user_request_credit, credit_repay_request: CreditRepayRequest):
        response = ValidateCrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_ok()
        ).post(credit_repay_request)
        return response


    def credit_repay_invalid_unprocessable_entity(self, create_user_request_credit, credit_repay_request: CreditRepayRequest):
        CrudRequester(
            RequestSpecs.auth_headers(username=create_user_request_credit.username, password=create_user_request_credit.password),
            Endpoint.CREDIT_REPAY,
            ResponseSpecs.status_code_unprocessable_entity()
        ).post(credit_repay_request)