import allure
from selenium.webdriver.common.by import By
from page_objects.base_page import BasePage


class RegistrationPage(BasePage):
    TITLE_TEXT = "Register Account"
    FN_INPUT = (By.ID, "input-firstname")
    LN_INPUT = (By.ID, "input-lastname")
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    POLICY_CHECK = (By.CSS_SELECTOR, 'input[name="agree"][value="1"].form-check-input')
    REGISTER_BUTTON = (By.XPATH, "//button[contains(text(), 'Continue')]")
    REGISTER_HEAD = (By.XPATH, '//h1[text()="Register Account"]')
    REGISTER_BODY = (By.ID, "form-register")
    SHOP_CART_LINK = (By.PARTIAL_LINK_TEXT, "Shopping Cart")

    @allure.step("Открываю страницу 'Регистрации'")
    def open_register_page(self, base_url):
        self.browser.get(f"{base_url}/index.php?route=account/register")
        allure.attach("Открыли страницу 'Регистрации'")

    @allure.step("Ищу заголовок браузера")
    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    @allure.step("Ищу заголовок карточки регистрации")
    def find_card_name(self):
        return self.get_element(self.REGISTER_HEAD)

    @allure.step("Ищу тело карточки регистрации")
    def find_card_body(self):
        return self.get_element(self.REGISTER_BODY)

    @allure.step("Ищу ссылку на 'Shopping Cart'")
    def find_link(self):
        return self.get_element(self.SHOP_CART_LINK)

    @allure.step("Ищу поле 'Пароль'")
    def find_password_field(self):
        return self.get_element(self.PASSWORD_INPUT)

    @allure.step("Ищу Privacy Policy")
    def find_check_box(self):
        return self.get_element(self.POLICY_CHECK)

    @allure.step("Ввожу данные в поле Имя")
    def enter_firstname(self, firstname):
        self.input_value(self.FN_INPUT, firstname)

    @allure.step("Ввожу данные в поле Фамилия")
    def enter_lastname(self, lastname):
        self.input_value(self.LN_INPUT, lastname)

    @allure.step("Ввожу данные в поле Email")
    def enter_email(self, email):
        self.input_value(self.EMAIL_INPUT, email)

    @allure.step("Ввожу данные в поле Пароль")
    def enter_password(self, password):
        self.input_value(self.PASSWORD_INPUT, password)

    @allure.step("Соглашаюсь с Privacy Policy")
    def agree_to_policy(self):
        checkbox = self.get_element(self.POLICY_CHECK)
        if not checkbox.is_selected():
            checkbox.click()
            allure.attach("Активировал чек-бокс Privacy Policy")

    @allure.step("Нажимаю кнопку 'Регистрация'")
    def submit_login(self):
        self.click(self.REGISTER_BUTTON)
        allure.attach("Кликнули по кнопке 'Регистрация'")

    @allure.step("Ищу подтверждение регистрации")
    def is_account_created(self):
        return self.wait.until(lambda x: x.title == "Your Account Has Been Created!")
