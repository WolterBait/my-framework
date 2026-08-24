from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps


class TestCatalog:
    def test_catalog_count_product(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # проверяем редирект на нужный URL
        expect(auth_page).to_have_url(CatalogPage.URL)

        # Проверяем количество товаров
        count_products = catalog_steps.get_products_count()
        assert count_products == 6

    def test_sorted_by_name_a_z(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # проверяем редирект на нужный URL
        expect(auth_page).to_have_url(CatalogPage.URL)

        # Сортируем от A до Z и получаем список названий товаров
        names = catalog_steps.sort_items("az").get_product_names()

        # Проверяем, что список отсортирован по имени
        assert names == sorted(names), "Товары не отсортированы по имени A-Z"

    def test_sorted_by_name_z_a(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # проверяем редирект на нужный URL
        expect(auth_page).to_have_url(CatalogPage.URL)

        # Сортируем от Z до A и получаем список названий товаров
        names = catalog_steps.sort_items("za").get_product_names()

        # Проверяем, что список отсортирован по имени
        assert names == sorted(names, reverse=True), "Товары не отсортированы по имени Z-A"

    def test_sort_by_price_low_high(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # проверяем редирект на нужный URL
        expect(auth_page).to_have_url(CatalogPage.URL)

        # Сортировка по цене от low → high и получаем список цен
        prices = catalog_steps.sort_items("lohi").get_product_prices()

        # Проверяем сортировку по возрастанию
        assert prices == sorted(prices), "Товары не отсортированы по цене low → high"

    def test_sort_by_price_high_low(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # проверяем редирект на нужный URL
        expect(auth_page).to_have_url(CatalogPage.URL)

        # Сортировка по цене от high → low и получаем список цен
        prices = catalog_steps.sort_items("hilo").get_product_prices()

        # Проверяем сортировку по возрастанию
        assert prices == sorted(prices, reverse=True), "Товары не отсортированы по цене high → low"

    def test_add_to_cart(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # Добавляем товар в корзину
        button = catalog_steps.add_to_cart("Sauce Labs Bike Light")

        # Проверяем, что кнопка изменилась на Remove
        expect(button).to_have_text("Remove")

        # Проверяем счётчик корзины
        assert catalog_steps.get_cart_count() == 1

    def test_add_to_cart_and_remove(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # Добавляем товар в корзину
        button_add = catalog_steps.add_to_cart("Sauce Labs Onesie")

        # Проверяем, что кнопка изменилась на Remove
        expect(button_add).to_have_text("Remove")

        # Проверяем счётчик корзины
        assert catalog_steps.get_cart_count() == 1

        # Удаляем товар из корзины
        button_remove = catalog_steps.remove_from_cart("Sauce Labs Onesie")

        # Проверяем, что кнопка изменилась на Add to cart
        expect(button_remove).to_have_text("Add to cart")

        # Проверяем, что товаров в корзине нет
        assert catalog_steps.get_cart_count() == 0

    def test_product_details_onesie(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # Находим карточку товара | Сохраняем название и цену с карточки
        # Переходим на страницу товара | Сохраняем название и цену на детальной странице
        name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Onesie")

        # Сверяем название и цену на странице деталей
        assert name == detail_name, "Название товара не совпадает"
        assert price == detail_price, "Цена товара не совпадает"

    def test_product_details_jacket(self, auth_page):
        # Инициализируем CatalogSteps
        catalog_steps = CatalogSteps(auth_page)

        # Находим карточку товара | Сохраняем название и цену с карточки
        # Переход на страницу товара | Сохраняем название и цену на детальной странице
        name, price, detail_name, detail_price = catalog_steps.open_product_details("Sauce Labs Fleece Jacket")

        # Сверяем название и цену на странице деталей
        assert name == detail_name, "Название товара не совпадает"
        assert price == detail_price, "Цена товара не совпадает"