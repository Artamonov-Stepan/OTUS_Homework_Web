from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class CatalogPage(BasePage):
    TITLE_TEXT = "Laptops & Notebooks"
    PRODUCT_NAME = (By.XPATH, "//*[text()='MacBook Air']")
    COMPARE_TOTAL = (By.ID, "compare-total")
    COMPARE_BUTTON = (By.CLASS_NAME, "btn-primary")
    CURRENCY_MENU = (By.CSS_SELECTOR, 'div[class="dropdown"]')
    GROUP_ITEM = (By.PARTIAL_LINK_TEXT, "Mac")
    PRODUCT_CARD = (By.CLASS_NAME, "product-thumb")
    PRICE_LOCATOR = (By.CLASS_NAME, "price-new")

    def open_catalog_page(self, base_url):
        self.browser.get(f"{base_url}/en-gb/catalog/laptop-notebook")

    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    def find_product_name(self):
        return self.get_element(self.PRODUCT_NAME)

    def find_compare_total(self):
        return self.get_element(self.COMPARE_TOTAL)

    def find_compare_button(self):
        return self.get_element(self.COMPARE_BUTTON)

    def find_currency_menu(self):
        return self.get_element(self.CURRENCY_MENU)

    def find_group_item(self):
        return self.get_element(self.GROUP_ITEM)

    def find_all_product_cards(self):
        return self.get_elements(self.PRODUCT_CARD)

    def get_first_product_card(self):
        cards = self.find_all_product_cards()
        if len(cards) > 0:
            return cards[0]
        else:
            raise Exception("No products found on the main page.")

    def get_last_product_card(self):
        cards = self.find_all_product_cards()
        if len(cards) > 0:
            return cards[-1]
        else:
            raise Exception("No products found on the main page.")

    def get_product_card_price(self, card):
        return card.find_element(*self.PRICE_LOCATOR).text.strip()
