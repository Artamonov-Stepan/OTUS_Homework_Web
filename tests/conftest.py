import pytest
import logging
import allure
import json
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FFOptions
from selenium.webdriver.edge.options import Options as MEOptions
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

# Настройка логирования в stdout (лучше для Docker)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Пишем в консоль
    ]
)

def pytest_addoption(parser):
    parser.addoption("--browser", help="Browser to run tests", default="chrome")
    parser.addoption("--headless", action="store_true", help="Activate headless mode")
    parser.addoption("--remote", action="store_true", help="Run tests on Selenoid", default=True)
    parser.addoption("--browser-version", help="Browser version for Selenoid", default="118.0")
    parser.addoption("--enable-vnc", action="store_true", help="Enable VNC for Selenoid", default=True)
    parser.addoption("--enable-video", action="store_true", help="Enable video recording", default=True)
    parser.addoption("--drivers", help="Drivers storage", default="/drivers")  # Заглушка
    parser.addoption("--base_url", help="Base application url", default="opencart:8080")
    parser.addoption("--selenoid-url", help="Selenoid hub URL", default="http://selenoid:4444/wd/hub")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call":
        if rep.outcome != 'passed':
            item.status = 'failed'
            driver = getattr(item, "_driver", None)
            if driver is not None:
                screenshot_path = os.path.join("screenshots", f"{item.name}_failure.png")
                os.makedirs("screenshots", exist_ok=True)
                driver.get_screenshot_as_file(screenshot_path)
                allure.attach.file(screenshot_path, name="Failure Screenshot",
                                   attachment_type=allure.attachment_type.PNG)
        else:
            item.status = 'passed'


@pytest.fixture(scope="session")
def base_url(request):
    url = request.config.getoption("--base_url")
    if not url.startswith("http"):
        url = "http://" + url
    return url


@pytest.fixture
def wait(browser):
    return WebDriverWait(browser, 10)


def _create_remote_driver(request, browser_name):
    options = None

    if browser_name == "chrome":
        options = ChromeOptions()
    elif browser_name == "firefox":
        options = FFOptions()
    elif browser_name == "edge":
        options = MEOptions()
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # Установка версии браузера
    options.browser_version = request.config.getoption("--browser-version")

    # Headless
    if request.config.getoption("--headless"):
        if browser_name == "firefox":
            options.add_argument("--headless")
        else:
            options.add_argument("headless=new")

    # Selenoid capabilities
    options.set_capability("selenoid:options", {
        "enableVNC": request.config.getoption("--enable-vnc"),
        "enableVideo": request.config.getoption("--enable-video"),
        "name": request.node.name,  # ✅ Теперь request доступен
        "sessionTimeout": "15m"
    })

    driver = RemoteWebDriver(
        command_executor=request.config.getoption("--selenoid-url"),
        options=options
    )

    return driver


def _create_local_driver(request, browser_name, drivers_storage):
    # В Docker-сборке этот путь не используется, но оставим для локального запуска
    if browser_name == "chrome":
        options = ChromeOptions()
        if request.config.getoption("--headless"):
            options.add_argument("headless=new")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FFOptions()
        if request.config.getoption("--headless"):
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = MEOptions()
        if request.config.getoption("--headless"):
            options.add_argument("headless=new")
        # Упрощённо: предполагаем, что драйвер в PATH
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    return driver


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption("--browser")
    drivers_storage = request.config.getoption("--drivers")

    browser_mapping = {
        "ch": "chrome", "chrome": "chrome",
        "ff": "firefox", "firefox": "firefox",
        "me": "edge", "edge": "edge"
    }

    standard_browser_name = browser_mapping.get(browser_name.lower(), "chrome")

    if request.config.getoption("--remote"):
        driver = _create_remote_driver(request, standard_browser_name)
    else:
        driver = _create_local_driver(request, standard_browser_name, drivers_storage)

    logging.info(f"Starting test: {request.node.name}")

    # Прикрепление capabilities
    allure.attach(
        name="capabilities",
        body=json.dumps(driver.capabilities, indent=4, ensure_ascii=False),
        attachment_type=allure.attachment_type.JSON
    )

    # Сохраняем driver в объекте теста
    request.node._driver = driver

    yield driver

    driver.quit()