from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page_one import CheckoutPageOne
from src.main.ui.pages.checkout_page_two import CheckoutPageTwo
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.basket_steps import BasketSteps
from src.main.ui.steps.checkout_steps import CheckoutSteps

def test_checkout_cart(auth_page):
    # Инициализируем Step Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)
    checkout_steps = CheckoutSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем Sauce Labs Backpack и Sauce Labs Bolt T-Shirt
    catalog_steps.add_to_cart("Sauce Labs Backpack")
    catalog_steps.add_to_cart("Sauce Labs Bolt T-Shirt")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем, что товары есть в корзине
    item_names = basket_steps.get_all_cart_items()
    assert "Sauce Labs Backpack" in item_names
    assert "Sauce Labs Bolt T-Shirt" in item_names

    # Считаем сумму товаров в корзине
    prices_sum_from_cart = basket_steps.get_sum_all_price_item_from_cart()

    # Переходим на страницу Checkout
    basket_steps.open_checkout()

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CheckoutPageOne.URL)

    # Заполняем поля ввода страницы Checkout | Нажимаем кнопку Continue
    checkout_steps.enter_checkout("First Name", "Last Name", "123")

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CheckoutPageTwo.URL)

    # Считаем сумму Item total, проверяем, что она равна сумме товаров в корзине
    item_total_text = checkout_steps.get_item_total_price_from_checkout()
    print(item_total_text)
    assert item_total_text == prices_sum_from_cart

    # Считаем сумму Tax
    tax_text = checkout_steps.get_sum_tax_price_from_checkout()
    print(tax_text)

    # Считаем итоговую сумму с учётом налога (Tax)
    final_sum_price = item_total_text + tax_text
    print(final_sum_price)

    # Выводим сумму Total со страницы
    total_text = checkout_steps.get_sum_total_price_from_checkout()
    print(total_text)

    # Сравниваем значение final_sum_price с суммой total на странице
    assert final_sum_price == final_sum_price

    # Завершаем покупку
    checkout_steps.click_finish_button()

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url("https://www.saucedemo.com/checkout-complete.html")

    # Проверяем корректность отображения надписи
    thank_text = auth_page.locator('.complete-header', has_text='Thank you for your order!')
    expect(thank_text).to_be_visible()



def test_checkout_invalid_last_name(auth_page):
    # Инициализируем Page Object классы
    catalog_steps = CatalogSteps(auth_page)
    basket_steps = BasketSteps(auth_page)
    checkout_steps = CheckoutSteps(auth_page)

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CatalogPage.URL)

    # Добавляем Sauce Labs Backpack
    catalog_steps.add_to_cart("Sauce Labs Backpack")

    # Переходим в корзину
    catalog_steps.open_cart()

    # Проверяем, что товары есть в корзине
    item_names = basket_steps.get_all_cart_items()
    assert "Sauce Labs Backpack" in item_names

    # Переходим на страницу Checkout
    basket_steps.open_checkout()

    # Проверяем редирект на нужный URL
    expect(auth_page).to_have_url(CheckoutPageOne.URL)

    # Заполняем поля ввода страницы Checkout | Нажимаем кнопку Continue
    checkout_steps.enter_checkout("Test", "", "123")

    # Проверяем наличие сообщения об ошибки
    assert "Error: Last Name is required" in checkout_steps.get_error_text()

