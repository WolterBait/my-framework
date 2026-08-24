import allure
from src.main.ui.pages.login_page import LoginPage
from src.main.ui.pages.catalog_page import CatalogPage
from playwright.sync_api import Page, expect


class CatalogSteps:
    """Создаем класс шагов для страницы авторизации"""

    def __init__(self, page: Page):
        self.page = page
        self.catalog_page = CatalogPage(self.page)

    @allure.step("Открываем страницу каталога")
    def open_catalog_page(self):
        """Шаг для открытия страницы логина"""
        self.catalog_page.open()
        return self

    # --- Логаут ---
    @allure.step("Выполняем логаут, проверяем корректность редиректа")
    def logout(self):
        """
        Шаг для выполнения логаута и проверки редиректа,
        отображения кнопки Login на странице авторизации
        """
        self.catalog_page.logout()
        expect(self.page).to_have_url(LoginPage.URL)
        expect(self.page.locator("#login-button")).to_be_visible()
        return self

    # --- Сортировка ---
    @allure.step("Сортируем товары по вписанному фильтру {option}")
    def sort_items(self, option: str):
        """Шаг для сортировки товаров внутри каталога"""
        # Варианты: "az", "za", "lohi", "hilo"
        self.catalog_page.sort_catalog_items(option)
        return self

    # --- Работа с корзиной ---
    @allure.step("Переход на страницу корзины")
    def open_cart(self):
        """Переход на страницу корзины"""
        self.catalog_page.open_cart()
        return self

    @allure.step("Добавляем товар {product_name} в корзину")
    def add_to_cart(self, product_name: str):
        """
        Метод для поиска карточки по имени товара. Находим товар и кликаем.
        Добавляем товар в корзину.
        """
        button = self.catalog_page.add_to_cart(product_name)
        return button

    @allure.step("Удаляем товар {product_name} из корзины")
    def remove_from_cart(self, product_name: str):
        """
        Метод для поиска карточки по имени товара.
        Удаляем товар из корзины
        """
        button = self.catalog_page.remove_from_cart(product_name)
        return button

    @allure.step("Получаем количество товаров в корзине")
    def get_cart_count(self) -> int:
        """Метод возращает количество товаров в корзине"""
        return self.catalog_page.get_cart_count()

    @allure.step("Получаем счётчик товаров в корзине")
    def cart_badge(self):
        """Возращает счётчик товаров в корзине"""
        return self.catalog_page.cart_badge


    # --- Работа с карточками товаров ---
    @allure.step("Получаем количество количество карточек товаров")
    def get_products_count(self) -> int:
        """Метод возращает количество карточек товаров"""
        return self.catalog_page.get_products_count()

    @allure.step("Получаем список названий товаров")
    def get_product_names(self) -> list[str]:
        """Метод для сбора названий всех товаров"""
        return self.catalog_page.get_product_names()

    @allure.step("Получаем список цен товаров")
    def get_product_prices(self) -> list[float]:
        """Метод для сбора цен, удаления знака "$" и перевода в float"""
        return self.catalog_page.get_product_prices()

    @allure.step("Открываем страницу деталей товара: {product_name}")
    def open_product_details(self, product_name: str):
        """
        Берем данные из карточки товара: название, цена;
        открываем страницу товара, считываем оттуда имя и цену;
        а затем возвращаем эти значения
        """
        return self.catalog_page.open_product_details(product_name)