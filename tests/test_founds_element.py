from selenium.webdriver.common.by import By

def test_administration_page(browser, base_url, wait):
    browser.get(base_url + "/administration")
    assert "Administration" in browser.title
    browser.find_element(By.XPATH, "//*[text()=' Please enter your login details.']")
    browser.find_element(By.ID, "input-password")
    browser.find_element(By.CSS_SELECTOR, 'button[class="btn btn-primary"]')
    browser.find_element(By.CLASS_NAME, "card-body")
    browser.find_element(By.PARTIAL_LINK_TEXT, "OpenCart")


def test_registration_page(browser, base_url, wait):
    browser.get(base_url + "/index.php?route=account/register")
    assert "Register Account" in browser.title
    browser.find_element(By.XPATH, "//*[text()='Register Account']")
    browser.find_element(By.ID, "form-register")
    browser.find_element(By.NAME, "password")
    browser.find_element(By.CSS_SELECTOR, 'input[type="checkbox"]')
    browser.find_element(By.PARTIAL_LINK_TEXT, "Shopping Cart")


def test_main_page(browser, base_url, wait):
    browser.get(base_url + "/en-gb?route=common/home")
    assert "Your Store" in browser.title
    browser.find_element(By.XPATH, "//*[text()='Featured']")
    browser.find_element(By.ID, "alert")
    browser.find_element(By.CSS_SELECTOR, 'button[class="navbar-toggler"]')
    browser.find_element(By.CLASS_NAME, "row")
    browser.find_element(By.PARTIAL_LINK_TEXT, "Cart")


def test_catalog_page(browser, base_url, wait):
    browser.get(base_url + "/en-gb/catalog/desktops")
    assert "Desktops" in browser.title
    browser.find_element(By.XPATH, "//*[text()='MacBook Air']")
    browser.find_element(By.ID, "compare-total")
    browser.find_element(By.CSS_SELECTOR, 'div[class="dropdown"]')
    browser.find_element(By.CLASS_NAME, "btn-primary")
    browser.find_element(By.PARTIAL_LINK_TEXT, "Mac")


def test_product_page(browser, base_url, wait):
    browser.get(base_url + "/en-gb/product/desktops/canon-eos-5d")
    assert "sdf" in browser.title
    browser.find_element(By.XPATH, "//*[text()='Add to Cart']")
    browser.find_element(By.ID, "button-cart")
    browser.find_element(By.CSS_SELECTOR, 'img[class="img-thumbnail mb-3"]')
    browser.find_element(By.CLASS_NAME, "price-new")
    browser.find_element(By.PARTIAL_LINK_TEXT, "Desktops")