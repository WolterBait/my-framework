# Импортируем библиотеку pytest для создания тестов и использования фикстур
import pytest
# Импортируем sync_playwright — контекстный менеджер для инициализации Playwright в синхронном режиме,
# и Page — тип для аннотации страницы, чтобы указать ожидаемый тип в фикстуре
from playwright.sync_api import sync_playwright, Page


# Фикстура с областью видимости "session" (создаётся один раз на все тесты).
# Запускает Playwright и предоставляет экземпляр для управления браузерами.
@pytest.fixture(scope="session")
def playwright_instance():
    # sync_playwright() — контекстный менеджер, который инициализирует Playwright.
    # Используем yield, чтобы фикстура могла передать объект и закрыть его после завершения всех тестов.
    with sync_playwright() as playwright:
        yield playwright  # передаём объект playwright в тесты


# Фикстура "session" — один браузер на весь сеанс тестирования.
# Зависит от playwright_instance, чтобы получить доступ к запуску браузера.
@pytest.fixture(scope="session")
def browser(playwright_instance):
    # Запускаем браузер Chromium в headless-режиме (c интерфейса и таймингами).
    browser = playwright_instance.chromium.launch(headless=False, slow_mo=1000)
    yield browser
    browser.close()  # закрываем браузер после всех тестов


# Фикстура "function" — создаёт новую страницу для каждого теста (новая вкладка).
# Это гарантирует изоляцию между тестами: каждый тест получает чистую страницу.
@pytest.fixture(scope="function")
def page(browser) -> Page:
    # Создаём новый контекст (изолированное хранилище cookies/сессий) для браузера.
    context = browser.new_context()
    # Создаём новую страницу (вкладку) внутри контекста.
    page = context.new_page()
    yield page  # передаём страницу в тест
    context.close()  # закрываем контекст после завершения теста, освобождая ресурсы