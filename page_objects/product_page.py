import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class ProductPage(BasePage):
    TITLE_TEXT = "sdf"
    ADD_BUTTON = (By.ID, "button-cart")
    CARD_HEAD = (By.XPATH, "//*[text()='Canon EOS 5D']")
    PRODUCT_IMAGE = (By.CSS_SELECTOR, 'img[class="img-thumbnail mb-3"]')
    PRODUCT_PRICE = (By.CLASS_NAME, "price-new")
    BREADCRUMB = (By.PARTIAL_LINK_TEXT, "Desktops")

    @allure.step("Открываю карточку товара 'Canon EOS 5D'")
    def open_product_page(self, base_url):
        self.browser.get(f"{base_url}/en-gb/product/desktops/canon-eos-5d")
        allure.attach("Открыли карточку товара 'Canon EOS 5D'")

    @allure.step("Ищу заголовок браузера")
    def find_product_page(self):
        return self.browser.title == self.TITLE_TEXT

    @allure.step("Ищу заголовок карточки товара")
    def find_card_head(self):
        return self.get_element(self.CARD_HEAD)

    @allure.step("Ищу фото товара")
    def find_product_image(self):
        return self.get_element(self.PRODUCT_IMAGE)

    @allure.step("Ищу цену товра")
    def find_product_price(self):
        return self.get_element(self.PRODUCT_PRICE)

    @allure.step("Ищу 'хлебные крошки'")
    def find_breadcrumb(self):
        return self.get_element(self.BREADCRUMB)

    @allure.step("Ищу кнопку 'Добавить в корзину'")
    def find_add_button(self):
        return self.get_element(self.ADD_BUTTON)
