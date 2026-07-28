from http import HTTPStatus

import requests

from src.main.api.models.auth_login_request import LoginUserRequest
from src.main.api.models.auth_login_response import LoginUserResponse
from src.main.api.requests.requester import Requester
from requests import Response



class LoginUserRequester(Requester):
    def post(self, auth_login_request: LoginUserRequest) -> LoginUserResponse | Response:
        # СОБРАЛИ URL
        url=f"{self.base_url}/auth/token/login"

        # СОБИРАЕМ ЗАПРОС
        response = requests.post(
            url=url,
            json=auth_login_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)

        if response.status_code == HTTPStatus.OK:
            return LoginUserResponse(**response.json())
        return response


