import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class AdminPage(BasePage):
    TITLE_TEXT = "Administration"
    LOGIN_INPUT = (By.ID, "input-username")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.XPATH, "//button[contains(text(), 'Login')]")
    CARD_HEAD = (By.XPATH, "//*[text()=' Please enter your login details.']")
    CARD_BODY = (By.CLASS_NAME, "card-body")
    OPEN_CART_LINK = (By.PARTIAL_LINK_TEXT, "OpenCart")
    HEADER_MENU = (By.ID, "button-menu")
    MENU_CATALOG = (By.ID, "menu-catalog")
    PRODUCTS = (By.PARTIAL_LINK_TEXT, "Products")
    ADD_NEW = (By.XPATH, '//a/i[@class="fa-solid fa-plus"]/parent::*')
    PRODUCT_NAME = (By.ID, "input-name-1")
    META_TAG_TITLE = (By.ID, "input-meta-title-1")
    DATA_TAB = (By.XPATH, "//*[text()='Data']")
    MODEL = (By.ID, "input-model")
    SEO_TAB = (By.XPATH, "//*[text()='SEO']")
    KEYWORD = (By.ID, "input-keyword-0-1")
    SAVE_BUTTON = (By.CSS_SELECTOR, "button i.fa-solid.fa-floppy-disk")
    CHEKBOX_PRODUCT = (By.CSS_SELECTOR, 'input[name="selected[]"]')
    DELETE_BUTTON = (
        By.CSS_SELECTOR,
        'button[form="form-product"][formaction*="product.delete"]',
    )

    @allure.step("Открываю страницу 'Administration'")
    def open_admin_page(self, base_url):
        self.browser.get(f"{base_url}/administration")
        allure.attach("Открыли страницу 'Administration'")

    @allure.step("Открываю страницу 'Dashboard'")
    def is_dashboard_opened(self):
        return self.wait.until(lambda x: x.title == "Dashboard")

    @allure.step("Ищу заголовок браузера")
    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    @allure.step("Ищу наименование карточки")
    def find_card_name(self):
        return self.get_element(self.CARD_HEAD)

    @allure.step("Ищу тело карточки")
    def find_card_body(self):
        return self.get_element(self.CARD_BODY)

    @allure.step("Ищу кнопку 'Логин'")
    def find_login_button(self):
        return self.get_element(self.LOGIN_BUTTON)

    @allure.step("Ищу ссылку на OpenCart")
    def find_link(self):
        return self.get_element(self.OPEN_CART_LINK)

    @allure.step("Ищу поле 'Пароль'")
    def find_password_field(self):
        return self.get_element(self.PASSWORD_INPUT)

    @allure.step("Ввожу данные в поле Логин")
    def enter_username(self, username):
        self.input_value(self.LOGIN_INPUT, username)

    @allure.step("Ввожу данные в поле Пароль")
    def enter_password(self, password):
        self.input_value(self.PASSWORD_INPUT, password)

    @allure.step("Нажимаю кнопку 'Логин'")
    def submit_login(self):
        self.click(self.LOGIN_BUTTON)
        allure.attach("Кликнули по кнопке 'Логин'")

    @allure.step("Нажимаю кнопку 'Меню'")
    def click_to_menu(self):
        self.click(self.MENU_CATALOG)
        allure.attach("Кликнули по кнопке 'Меню'")

    @allure.step("Нажимаю кнопку 'Продукт'")
    def click_to_products(self):
        self.click(self.PRODUCTS)
        allure.attach("Кликнули по кнопке 'Продукт'")

    @allure.step("Нажимаю кнопку 'Add New'")
    def click_add_new(self):
        self.click(self.ADD_NEW)
        allure.attach("Кликнули по кнопке 'Add New'")

    @allure.step("Ввожу данные в поле Product name")
    def enter_product_name(self, product_name):
        self.input_value(self.PRODUCT_NAME, product_name)
        allure.attach("Указали данные в поле Product Name")

    @allure.step("Ввожу данные в поле Tag title")
    def enter_tag_title(self, tag_title):
        self.input_value(self.META_TAG_TITLE, tag_title)
        allure.attach("Указали данные в поле Tag title")

    @allure.step("Нажимаю на наименование вкладки 'Data'")
    def click_data_tab(self):
        self.click(self.DATA_TAB)
        allure.attach("Нажали на наименование вкладки 'Data'")

    @allure.step("Ввожу данные в поле Model")
    def enter_model(self, model):
        self.input_value(self.MODEL, model)
        allure.attach("Указали данные в поле Model")

    @allure.step("Нажимаю на наименование вкладки SEO")
    def click_seo_tab(self):
        self.click(self.SEO_TAB)
        allure.attach("Нажали на наименование вкладки SEO")

    @allure.step("Ввожу данные в поле Keyword")
    def enter_keyword(self, keyword):
        self.input_value(self.KEYWORD, keyword)
        allure.attach("Указали данные в поле Keyword")

    @allure.step("Нажимаю кнопку Сохранить")
    def click_save_button(self):
        self.click(self.SAVE_BUTTON)
        allure.attach("Кликнули по кнопке 'Сохранить'")

    @allure.step("Нажимаю на 'Бургер меню'")
    def click_header_menu(self):
        self.click(self.HEADER_MENU)
        allure.attach("Кликнули по 'Бурге меню'")

    @allure.step("Нажимаю кнопку чек-бокс у продукта")
    def select_product(self):
        self.click(self.CHEKBOX_PRODUCT)
        allure.attach("Активировал чек-бокс у продукта")

    @allure.step("Нажимаю кнопку 'Удалить'")
    def click_delete_button(self):
        self.click(self.DELETE_BUTTON)
        allure.attach("Кликнули по кнопке 'Удалить'")
