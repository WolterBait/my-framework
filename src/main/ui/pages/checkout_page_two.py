from playwright.sync_api import Page


class CheckoutPageTwo:
    URL = "https://www.saucedemo.com/checkout-step-two.html"

    def __init__(self, page: Page):
        self.item_total = page.locator(".summary_subtotal_label")
        self.tax = page.locator(".summary_tax_label")
        self.total = page.locator(".summary_total_label")
        self.finish_button = page.get_by_role("button", name="Finish")

    # --- Работа на странице со суммой товаров ---
    def get_item_total_price_from_checkout(self):
        """
        Метод возращает сумму товаров поля Item Total
        со страницы checkout-step-two
        """
        item_total_text = self.item_total.text_content()
        item_total = float(item_total_text.replace("Item total: $", ""))
        return item_total

    def get_sum_tax_price_from_checkout(self):
        """
        Метод возращает сумму товаров поля Tax
        со страницы checkout-step-two
        """
        tax_text = self.tax.text_content()
        tax = float(tax_text.replace("Tax: $", ""))
        return tax

    def get_sum_total_price_from_checkout(self):
        """
        Метод возращает сумму товаров поля Total
        со страницы checkout-step-two
        """
        total_text = self.total.text_content()
        total = float(total_text.replace("Total: $", ""))
        return total

    def click_finish_button(self):
        """Метод нажимает на кнопку Finish"""
        self.finish_button.click()