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

    def open_register_page(self, base_url):
        self.browser.get(f"{base_url}/index.php?route=account/register")

    def find_browser_title(self):
        return self.browser.title == self.TITLE_TEXT

    def find_card_name(self):
        return self.get_element(self.REGISTER_HEAD)

    def find_card_body(self):
        return self.get_element(self.REGISTER_BODY)

    def find_link(self):
        return self.get_element(self.SHOP_CART_LINK)

    def find_password_field(self):
        return self.get_element(self.PASSWORD_INPUT)

    def find_check_box(self):
        return self.get_element(self.POLICY_CHECK)

    def enter_firstname(self, firstname):
        self.input_value(self.FN_INPUT, firstname)

    def enter_lastname(self, lastname):
        self.input_value(self.LN_INPUT, lastname)

    def enter_email(self, email):
        self.input_value(self.EMAIL_INPUT, email)

    def enter_password(self, password):
        self.input_value(self.PASSWORD_INPUT, password)

    def agree_to_policy(self):
        checkbox = self.get_element(self.POLICY_CHECK)
        if not checkbox.is_selected():
            checkbox.click()

    def submit_login(self):
        self.click(self.REGISTER_BUTTON)

    def is_account_created(self):
        return self.wait.until(lambda x: x.title == "Your Account Has Been Created!")
