from src.main.api.foundation.http_requester import HttpRequester
from typing import Optional
from src.main.api.models.base_model import BaseModel
from requests import Response
import requests
import allure
from src.main.api.configs.config import Config

# 1. УСТАНАВЛИВАЕМ ALLURE-PYTEST
     # PIP INSTALL ALLURE-PYTEST

# 2. ИМПОРТ ALLURE


class CrudRequester(HttpRequester):
    def post(self, model: Optional[BaseModel] = None) -> Response:
        body = model.model_dump() if model is not None else ""

        with allure.step(f"POST {Config.fetch("backendUrl")}{self.endpoint.value.url}"):
# allure.step - ШАГ ЛОГИРОВАНИЯ
# f"POST - ПОКАЗЫВАЕМ, ЧТО МЕТОД POST
# {Config.fetch("backendUrl")}{self.endpoint.value.url} - ПОКАЗЫВАЕМ URL

            allure.attach(
                str(body),
                "Request body",
                allure.attachment_type.JSON
            )
# allure.attach - ПРИКРЕПЛЯЕМ ЧТО-ТО К ОТЧЁТУ
# (str(body) - ПРИКРЕПЛЯЕМ ТЕЛО, ПЕРЕВОДИМ ЕГО СРАЗУ В STR
# "Request body" - ДАЁМ НАЗВАНИЕ ТОМУ, ЧТО ПРИКРЕПЛЯЕМ
# allure.attachment_type.JSON) -

        response = requests.post(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}",
            headers=self.request_spec,
            json=body
        )

        allure.attach(
            response.text,
            "Response body",
            allure.attachment_type.JSON
        )
# ВСЁ ПО АНАЛОГИИ С ПРОШЛЫМ ОБЪЯСНЕНИЕМ

# ТЕПЕРЬ ВСЁ, ЧТО БУДЕТ ПРОХОДИТЬ ЧЕРЕЗ CrudRequester ФУНКЦИИ POST,
# БУДЕТ ЦЕПЛЯТЬ КАКОЙ-ТО МЕТОД, ПО КАКОМУ URL МЫ СТУЧИМСЯ, КАКОЙ У
# НАС REQUEST BODY И КАКОЙ У НАС RESPONSE BODY,
# ЧТО ДАЁТ МАССУ ИНФОРМАЦИИ О ЗАПРОСЕ

        self.response_spec(response) # Проверяем статус код
        return response


    def delete(self, user_id: int) -> Response:
        response = requests.delete(
            url=f"{Config.fetch("backendUrl")}{self.endpoint.value.url}/{user_id}",
            headers=self.request_spec
        )
        self.response_spec(response)
        return response

# ПЕРЕХОДИМ В VALIDATE_CRUD_REQUESTER