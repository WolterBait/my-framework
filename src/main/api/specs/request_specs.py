import requests
from src.main.api.models.auth_login_request import LoginUserRequest
from src.main.api.models.auth_login_response import LoginUserResponse
from src.main.api.configs.config import Config

class RequestSpecs:
    @staticmethod
    def base_headers():
        return {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

    @staticmethod
    def auth_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url=f"{Config.fetch('backendUrl')}/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecs.base_headers(),
        )

        # ПРОПИСЫВАЕМ ЛОГИКУ ПОЗИТИВНОГО СЦЕНАРИЯ ОТРАБОТКИ ЗАПРОСА = 200
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token

            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return headers

        # ОБРАБАТЫВАЕМ НЕГАТИВНЫЙ СЦЕНАРИЙ ОТРАБОТКИ ЗАПРОСА = 400. 401...
        raise Exception("Failed to authorization")


    @staticmethod
    def no_auth_headers():
        return RequestSpecs.base_headers()

