import allure
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

    @allure.step("Открываю страницу 'Каталог'")
    def open_catalog_page(self, base_url):
        self.browser.get(f"{base_url}/en-gb/catalog/laptop-notebook")
        allure.attach("Открыли страницу 'Каталог'")

    @allure.step("Ищу заголовок браузера")
    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    @allure.step("Ищу наименование товара")
    def find_product_name(self):
        return self.get_element(self.PRODUCT_NAME)

    @allure.step("Ищу счётчик в 'Product Compare'")
    def find_compare_total(self):
        return self.get_element(self.COMPARE_TOTAL)

    @allure.step("Ищу кнопку 'Product Compare'")
    def find_compare_button(self):
        return self.get_element(self.COMPARE_BUTTON)

    @allure.step("Ищу меню смены валют")
    def find_currency_menu(self):
        return self.get_element(self.CURRENCY_MENU)

    @allure.step("Ищу группу товаров Macs")
    def find_group_item(self):
        return self.get_element(self.GROUP_ITEM)

    @allure.step("Ищу все карточки товаров")
    def find_all_product_cards(self):
        return self.get_elements(self.PRODUCT_CARD)

    @allure.step("Ищу первую карточку товара")
    def get_first_product_card(self):
        cards = self.find_all_product_cards()
        if len(cards) > 0:
            return cards[0]
        else:
            raise Exception("No products found on the main page.")

    @allure.step("Ищу последнюю карточку товара")
    def get_last_product_card(self):
        cards = self.find_all_product_cards()
        if len(cards) > 0:
            return cards[-1]
        else:
            raise Exception("No products found on the main page.")

    @allure.step("Ищу цену товара")
    def get_product_card_price(self, card):
        return card.find_element(*self.PRICE_LOCATOR).text.strip()
