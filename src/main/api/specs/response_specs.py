from requests import Response
from http import HTTPStatus    # Импортируем из библиотеки http - блок HTTPStatus


class ResponseSpecs:

    @staticmethod # просто функция внутри класса, не привязанная ни к объекту, ни к классу.
    def status_code_ok():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm                     # OK == 200    ЕСЛИ СТАТУС КОД НЕ ВЫВОДИМ ТЕКСТ ОТВЕТА

    @staticmethod
    def status_code_created():
        def confirm(response: Response) :
            assert response.status_code == HTTPStatus.CREATED, response.text # OK == 201
        return confirm

    @staticmethod
    def status_code_bad_request():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text # BAD_REQUEST == 400
        return confirm

    @staticmethod
    def status_code_unauthorized():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text # UNAUTHORIZED == 401
        return confirm

    @staticmethod
    def status_code_forbidden():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.FORBIDDEN, response.text # FORBIDDEN == 403
        return confirm

    @staticmethod
    def status_code_not_found():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.NOT_FOUND, response.text # FORBIDDEN == 403
        return confirm

    @staticmethod
    def status_code_unprocessable_entity():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, response.text # FORBIDDEN == 403
        return confirm


