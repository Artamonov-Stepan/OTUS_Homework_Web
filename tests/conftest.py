import pytest
import logging
import allure
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService

# Настройка логирования
logging.basicConfig(
    filename="/usr/src/app/logs/app.log",
    level=logging.WARNING,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def pytest_addoption(parser):
    parser.addoption("--browser",
                     help="Browser to run tests (chrome, firefox, edge)",
                     default="chrome",
                     choices=["chrome", "firefox", "edge", "ch", "ff", "me"])
    parser.addoption("--headless",
                     action="store_true",
                     help="Run tests in headless mode")
    parser.addoption("--base_url",
                     help="Base application URL",
                     default="host.docker.internal:8081")


@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption("--base_url")
    if not url.startswith(('http://', 'https://')):
        url = f"http://{url}"
    return url


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, timeout=20, poll_frequency=0.5)


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser").lower()
    headless = request.config.getoption("--headless")
    driver = None

    try:
        if browser_name in ["ch", "chrome"]:
            options = ChromeOptions()
            options.binary_location = '/usr/bin/google-chrome'

            if headless:
                options.add_argument("--headless=new")

            driver = webdriver.Chrome(
                service=ChromeService(executable_path='/usr/bin/chromedriver'),
                options=options
            )

        elif browser_name in ["ff", "firefox"]:
            options = FFOptions()
            options.binary_location = '/usr/bin/firefox'

            if headless:
                options.add_argument("--headless")

            driver = webdriver.Firefox(
                service=FirefoxService(executable_path='/usr/bin/geckodriver'),
                options=options
            )

        elif browser_name in ["me", "edge"]:
            options = EdgeOptions()

            if headless:
                options.add_argument("--headless=new")

            driver = webdriver.Edge(
                service=EdgeService(executable_path='/usr/bin/msedgedriver'),
                options=options
            )

        # Общие настройки
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(30)

        # Логирование
        logging.info(f"Starting test: {request.node.name}")
        allure.attach(
            name=f"{browser_name}-capabilities",
            body=json.dumps(driver.capabilities, indent=2),
            attachment_type=allure.attachment_type.JSON
        )

        yield driver

    except Exception as e:
        logging.error(f"Browser setup failed: {str(e)}")
        allure.attach(
            name="browser-setup-error",
            body=str(e),
            attachment_type=allure.attachment_type.TEXT
        )
        pytest.fail(f"Failed to initialize browser: {str(e)}")

    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception as e:
                logging.warning(f"Error during driver quit: {str(e)}")