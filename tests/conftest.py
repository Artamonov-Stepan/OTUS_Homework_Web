import pytest
import logging
import allure
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as MEOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


logging.basicConfig(
    filename="logs/app.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption(
        "--drivers", help="Drivers storage", default=r"C:\Users\glazg\Downloads\Drivers"
    )
    parser.addoption(
        "--base_url", help="Base application url", default="192.168.0.7:8081"
    )

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        if rep.outcome != 'passed':
            item.status = 'failed'
            driver = getattr(item, "_driver", None)
            if driver is not None:
                screenshot_path = os.path.join(os.getcwd(), "screenshots", f"{item.name}_failure.png")
                os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
                driver.get_screenshot_as_file(screenshot_path)
                allure.attach.file(screenshot_path, name="Failure Screenshot",
                                    attachment_type=allure.attachment_type.PNG)
        else:
            item.status = 'passed'

@pytest.fixture(scope="session")
def base_url(request):
    return "http://" + request.config.getoption("--base_url")

@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)

@pytest.fixture()
def browser(request):
    driver = None
    browser_name = request.config.getoption("--browser")
    drivers_storage = request.config.getoption("--drivers")
    headless = request.config.getoption("--headless")

    if browser_name in ["ch", "chrome"]:
        options = ChromeOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser_name in ["ff", "firefox"]:
        options = FFOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name in ["me", "edge"]:
        options = MEOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Edge(
            service=ChromiumService(
                executable_path=f"{drivers_storage}/msedgedriver.exe"
            ),
            options=options,
        )
    elif browser_name in ["ya", "yandex"]:
        options = ChromiumOptions()
        if headless:
            options.add_argument("headless=new")
        driver = webdriver.Chrome(
            options=options,
            service=ChromiumService(
                executable_path=f"{drivers_storage}/yandexdriver.exe"
            ),
        )

    logging.info(f"Starting test: {request.node.name}")

    allure.attach(
        name=driver.session_id,
        body=json.dumps(driver.capabilities, indent=4, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON
    )

    driver.test_name = request.node.name
    driver.log_level = logging.DEBUG

    yield driver

    driver.quit()