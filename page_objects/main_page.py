from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class MainPage(BasePage):
    TITLE_TEXT = "Your Store"
    CARD_HEAD = (By.XPATH, "//*[text()='Featured']")
    ALERT = (By.ID, "alert")
    MENU = (By.CSS_SELECTOR, 'button[class="navbar-toggler"]')
    HEADER = (By.CLASS_NAME, "row")
    CART = (By.PARTIAL_LINK_TEXT, "Cart")
    ADD_BUTTON = (By.CSS_SELECTOR, 'button[formaction*="checkout/cart.add"]')
    PRODUCT_CARD = (By.CLASS_NAME, "product-thumb")
    NAME_LOCATOR = (By.CSS_SELECTOR, "h4 a")
    CART_TABLE_BODY = (By.CSS_SELECTOR, "#shopping-cart tbody")
    CART_ITEM_ROW = (By.TAG_NAME, "tr")
    ITEM_NAME_CELL = (By.CSS_SELECTOR, "td:nth-child(2) a")

    def open_main_page(self, base_url):
        self.browser.get(f"{base_url}/en-gb?route=common/home")

    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    def find_card_name(self):
        return self.get_element(self.CARD_HEAD)

    def find_alert(self):
        return self.get_element(self.ALERT)

    def find_menu(self):
        return self.get_element(self.MENU)

    def find_header(self):
        return self.get_element(self.HEADER)

    def find_cart_link(self):
        return self.get_element(self.CART)

    def find_all_product_cards(self):
        return self.get_elements(self.PRODUCT_CARD)

    def open_first_product_card(self):
        cards = self.find_all_product_cards()
        if len(cards) > 0:
            return cards[0]
        else:
            raise Exception("No products found on the main page.")

    def get_cart_table_body(self):
        return self.get_element(self.CART_TABLE_BODY)

    def get_cart_item_rows(self):
        table_body = self.get_cart_table_body()
        return table_body.find_elements(*self.CART_ITEM_ROW)

    def get_item_name_from_row(self, row):
        return row.find_element(*self.ITEM_NAME_CELL).text

    def submit_add_button(self):
        button = self.get_element(self.ADD_BUTTON)
        actions = ActionChains(self.browser)
        actions.move_to_element(button).click().perform()
