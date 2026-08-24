from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps

def test_add_item_and_check_in_cart(auth_page):
    # Инициализируем Step Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем товар в корзину и переходим в неё
    catalog_steps.add_to_cart("Sauce Labs Backpack")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем, что товар есть
    item_name = basket_steps.get_item_name('Sauce Labs Backpack')
    assert item_name.inner_text() == "Sauce Labs Backpack"


def test_add_jacket_and_shirt_and_check_in_cart(auth_page):
    # Инициализируем Step Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем Sauce Labs Fleece Jacket и Sauce Labs Bolt T-Shirt
    catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")
    catalog_steps.add_to_cart("Sauce Labs Bolt T-Shirt")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем, что товары есть
    item_names = basket_steps.get_all_cart_items()
    assert "Sauce Labs Fleece Jacket" in item_names
    assert "Sauce Labs Bolt T-Shirt" in item_names


def test_remove_item_from_cart(auth_page):
    # Инициализируем Step Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем товар в корзину и переходим в неё
    catalog_steps.add_to_cart("Sauce Labs Fleece Jacket")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем что товары в корзине
    item_name = basket_steps.get_item_name('Sauce Labs Fleece Jacket')
    expect(item_name).to_be_visible()

    # Удаляем товар
    basket_steps.remove_item_from_cart('Sauce Labs Fleece Jacket')

    # Проверяем, что товара больше нет в корзине
    expect(item_name).not_to_be_visible()


def test_remove_backpack_and_shirt_from_cart(auth_page):
    # Инициализируем Step Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем товары в корзину
    catalog_steps.add_to_cart("Sauce Labs Backpack")
    catalog_steps.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем что товары в корзине
    backpack = basket_steps.get_item_name('Sauce Labs Backpack')
    expect(backpack).to_be_visible()

    shirt = basket_steps.get_item_name('Test.allTheThings() T-Shirt (Red)')
    expect(shirt).to_be_visible()

    # Удаляем товар
    basket_steps.remove_item_from_cart('Sauce Labs Backpack')
    basket_steps.remove_item_from_cart('Test.allTheThings() T-Shirt (Red)')

    # Проверяем, что товара больше нет в корзине
    expect(backpack).not_to_be_visible()
    expect(shirt).not_to_be_visible()

