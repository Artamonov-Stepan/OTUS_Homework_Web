import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver

from selenium.webdriver.chromium.options import ChromiumOptions
from selenium.webdriver.chromium.service import ChromiumService
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as MEOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions


def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption(
        "--drivers", help="Drivers storage", default=r"C:\Users\glazg\Downloads\Drivers"
    )
    parser.addoption(
        "--base_url", help="Base application url", default="192.168.0.7:8081"
    )


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
                executable_path=f"{drivers_storage}\msedgedriver.exe"
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
                executable_path=f"{drivers_storage}\yandexdriver.exe"
            ),
        )

    yield driver

    driver.quit()
