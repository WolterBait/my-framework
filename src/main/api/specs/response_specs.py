from requests import Response
from http import HTTPStatus    # Импортируем из библиотеки http - блок HTTPStatus


class ResponseSpecs:

    @staticmethod # просто функция внутри класса, не привязанная ни к объекту, ни к классу.
    def status_code_200():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm                     # OK == 200    ЕСЛИ СТАТУС КОД НЕ ВЫВОДИМ ТЕКСТ ОТВЕТА

    @staticmethod
    def status_code_201():
        def confirm(response: Response) :
            assert response.status_code == HTTPStatus.CREATED, response.text # OK == 201
        return confirm

    @staticmethod
    def status_code_400():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text # BAD_REQUEST == 400
        return confirm

    @staticmethod
    def status_code_401():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text # UNAUTHORIZED == 401
        return confirm

    @staticmethod
    def status_code_403():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text # FORBIDDEN == 403
        return confirm

    @staticmethod
    def status_code_404():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text # FORBIDDEN == 403
        return confirm

    @staticmethod
    def status_code_422():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text # FORBIDDEN == 403
        return confirm


