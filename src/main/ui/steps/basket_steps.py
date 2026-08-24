import allure
from src.main.ui.pages.basket_page import BasketPage
from playwright.sync_api import Page, expect

class BasketSteps:
    """Создаем класс шагов для страницы авторизации"""

    def __init__(self, page: Page):
        self.page = page
        self.basket_page = BasketPage(self.page)

    @allure.step("Открываем страницу корзины")
    def open_basket_page(self):
        """Шаг для открытия страницы логина"""
        self.basket_page.open()
        return self


    # --- Работа внутри корзины ---
    @allure.step("Получаем товар из корзины {product_name}")
    def get_item_name(self, product_name: str):
        """Метод возращает товар по наименованию"""
        return self.basket_page.get_item_name(product_name)

    @allure.step("Получаем все товары из корзины")
    def get_all_cart_items(self):
        """Метод возращает наименования всех товаров в корзине"""
        return self.basket_page.get_all_cart_items()

    @allure.step("Удаляем товар {product_name} из корзины")
    def remove_item_from_cart(self, product_name: str):
        """Метод принимает название товара и удаляет его из корзины"""
        return self.basket_page.remove_item_from_cart(product_name)

    @allure.step("Считаем сумму всех товаров в корзине")
    def get_sum_all_price_item_from_cart(self):
        """Метод возращает сумму всех товаров в корзине"""
        return self.basket_page.get_sum_all_price_item_from_cart()


    # --- Переход на страницу checkout ---
    @allure.step("Переход на страницу checkout")
    def open_checkout(self):
        """Переход на страницу checkout"""
        self.basket_page.open_checkout()
        return self