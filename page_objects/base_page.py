import logging
import os
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


class BasePage:
    def __init__(self, browser, wait):
        self.browser = browser
        self.wait = wait
        self.__config_logger()

    def __config_logger(self, to_file=False):
        self.logger = logging.getLogger(type(self).__name__)
        os.makedirs("logs", exist_ok=True)
        if to_file:
            self.logger.addHandler(logging.FileHandler(f"logs/{self.browser.test_name}.log"))
        self.logger.setLevel(level=self.browser.log_level)

    def _text_xpath(self, text):
        xpath_expression = f"//*[text()='{text}']"
        self.logger.debug(f"XPath путь: {xpath_expression}")
        return xpath_expression

    def get_element(self, locator: tuple):
        self.logger.info(f"Получен {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator))

    def get_elements(self, locator: tuple):
        self.logger.info(f"Получены {locator}")
        return self.wait.until(EC.visibility_of_all_elements_located(locator))

    def click(self, locator: tuple):
        self.logger.info(f"Нажат {locator}")
        ActionChains(self.browser).move_to_element(self.get_element(locator)).pause(
            0.9
        ).click().perform()

    def input_value(self, locator: tuple, text: str):
        self.logger.info(f"Ввод текста '{text}' в элемент {locator}")
        self.get_element(locator).click()
        self.get_element(locator).clear()
        for letter in text:
            self.get_element(locator).send_keys(letter)
        self.logger.debug(f"Успех: введён текст '{text}' в элемент {locator}")
