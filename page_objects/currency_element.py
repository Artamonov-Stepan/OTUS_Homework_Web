import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class CurrencyElement:
    CURRENCY_DROPDOWN = (By.CSS_SELECTOR, ".dropdown-toggle")
    USD_OPTION = (By.XPATH, "//a[contains(text(),'US Dollar')]")
    EUR_OPTION = (By.XPATH, "//a[contains(text(),'Euro')]")
    GBP_OPTION = (By.XPATH, "//a[contains(text(),'Pound Sterling')]")
    SYMBOL_ELEMENT = (By.CSS_SELECTOR, ".dropdown-toggle strong")

    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    @allure.step("Меняю валюту")
    def change_currency(self, currency_code):
        dropdown = self.wait.until(
            EC.presence_of_element_located(self.CURRENCY_DROPDOWN)
        )

        actions = ActionChains(self.browser)
        actions.move_to_element(dropdown).click().perform()

        self.wait.until(
            EC.visibility_of_any_elements_located(
                (By.CSS_SELECTOR, ".dropdown-menu.show li")
            )
        )

        if currency_code == "USD":
            option = self.wait.until(EC.element_to_be_clickable(self.USD_OPTION))
            allure.attach("Поменяли валюту на USD")
        elif currency_code == "EUR":
            option = self.wait.until(EC.element_to_be_clickable(self.EUR_OPTION))
            allure.attach("Поменяли валюту на EUR")
        elif currency_code == "GBP":
            option = self.wait.until(EC.element_to_be_clickable(self.GBP_OPTION))
            allure.attach("Поменяли валюту на GBP")
        else:
            raise ValueError(f"Invalid currency code: {currency_code}")

        actions.move_to_element(option).click().perform()

        self.wait.until_not(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".dropdown-menu.show"))
        )

        self.wait.until(EC.presence_of_element_located(self.SYMBOL_ELEMENT))

    @allure.step("Получаю символ текущей валюты")
    def get_current_currency_symbol(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.SYMBOL_ELEMENT)
        ).text.strip()
