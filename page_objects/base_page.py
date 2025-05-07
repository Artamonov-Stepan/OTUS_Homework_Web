from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait

    def _text_xpath(self, text):
        return f"//*[text()='{text}']"

    def get_element(self, locator: tuple):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator: tuple):
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple):
        ActionChains(self.browser).move_to_element(self.get_element(locator)).pause(
            0.5
        ).click().perform()

    def input_value(self, locator: tuple, text: str):
        self.get_element(locator).click()
        self.get_element(locator).clear()
        for letter in text:
            self.get_element(locator).send_keys(letter)
