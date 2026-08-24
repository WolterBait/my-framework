import allure
from src.main.ui.pages.login_page import LoginPage
from playwright.sync_api import Page, expect


class LoginSteps:
    """Создаем класс шагов для страницы авторизации"""

    def __init__(self, page: Page):
        """
        Конструктор - сохраняем page для взаимодействия.
        Инициализируем login_page, чтобы мы могли пользоваться методами класса LoginPage.
        """
        self.page = page
        self.login_page = LoginPage(page)

    @allure.step("Открываем страницу логина")
    def open_login_page(self):
        """Шаг для открытия страницы логина"""
        self.login_page.open()
        return self

    @allure.step("Логинимся пользователем {username}")
    def login(self, username: str, password: str):
        """Шаг для выполнения логина"""
        self.login_page.login(username, password)
        return self

    @allure.step("Получаем текст ошибки при логине {username}")
    def error_text(self) -> str:
        """Проверка заблокированного пользователя"""
        return self.login_page.get_error_text()