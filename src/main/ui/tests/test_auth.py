from playwright.sync_api import expect
from src.main.ui.steps.login_steps import LoginSteps
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.pages.catalog_page import CatalogPage

class TestAuth():
    def test_only_auth_logout_standard_user(self, page):
        # Инициализируем LoginSteps
        steps = LoginSteps(page)

        # Авторизация и проверка корректного редиректа
        steps.open_login_page().login("standard_user", "secret_sauce")
        expect(page).to_have_url(CatalogPage.URL)

    def test_auth_logout_standard_user(self, page):
        # Инициализируем LoginSteps
        login_steps = LoginSteps(page)
        login_catalog = CatalogSteps(page)

        # Авторизация и проверка корректного редиректа
        login_steps.open_login_page().login("standard_user", "secret_sauce")
        expect(page).to_have_url(CatalogPage.URL)

        # Логаут и проверка корректного редиректа
        login_catalog.logout()

    def test_auth_logout_visual_user(self, page):
        # Инициализируем LoginSteps
        login_steps = LoginSteps(page)
        login_catalog = CatalogSteps(page)

        # Авторизация и проверка корректного редиректа
        login_steps.open_login_page().login("visual_user", "secret_sauce")
        expect(page).to_have_url(CatalogPage.URL)

        # Логаут и проверка корректного редиректа
        login_catalog.logout()

    def test_auth_invalid_locked_out_user(self, page):
        # Инициализируем LoginSteps
        login_steps = LoginSteps(page)

        # Авторизация и проверка всплывающего окна ошибки
        error_text = login_steps.open_login_page().login("locked_out_user", "secret_sauce").login_page.get_error_text()
        assert "locked out" in error_text, "Ожидаем сообщение о заблокированном пользователе"
