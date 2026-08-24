from playwright.sync_api import Page


class CheckoutPageOne:
    URL = "https://www.saucedemo.com/checkout-step-one.html"

    def __init__(self, page: Page):
        self.page = page

        self.enter_first_name = page.get_by_role("textbox", name="First Name")
        self.enter_last_name = page.get_by_role("textbox", name="Last Name")
        self.enter_zip = page.get_by_role("textbox", name="Zip/Postal Code")
        self.button_continue = page.get_by_role("button", name="Continue")
        self.error_text = page.locator('[data-test="error"]')

    def enter_checkout(self, first_name: str, last_name: str, zip_code: str):
        """
        Метод заполняет поля ввода First Name, Last Name, Zip/Postal Code
        на странице checkout-step-one и нажимает кнопку Continue
        """
        self.enter_first_name.fill(first_name)
        self.enter_last_name.fill(last_name)
        self.enter_zip.fill(zip_code)
        self.button_continue.click()

