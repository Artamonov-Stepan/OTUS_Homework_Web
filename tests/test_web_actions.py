import pytest
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def test_check_login_button(browser, base_url, wait):
    browser.get(base_url + "/administration")
    login_field = browser.find_element(By.ID, 'input-username')
    password_field = browser.find_element(By.ID, 'input-password')
    login_field.send_keys('user')
    password_field.send_keys('bitnami')
    login_button = browser.find_element(By.XPATH, "//*[text()=' Login']")
    login_button.click()

    wait.until(EC.title_is("Dashboard"))

    expected_title = "Dashboard"
    actual_title = browser.title
    assert expected_title == actual_title, f"Ожидаем получить заголовок страницы '{expected_title}', а получили '{actual_title}'"



def test_added_to_cart(browser, base_url, wait):
    browser.get(base_url + "/en-gb?route=common/home")

    product_cards = browser.find_elements(By.CLASS_NAME, 'product-thumb')
    first_card = product_cards[0]

    product_name = first_card.find_element(By.CSS_SELECTOR, 'h4 a').text

    add_button = first_card.find_element(By.CSS_SELECTOR, 'button[formaction*="checkout/cart.add"]')
    actions = ActionChains(browser)
    actions.move_to_element(add_button).click().perform()

    success_message = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.alert-success')))
    assert "Success: You have added" in success_message.text, "Сообщение об успешном добавлении товара не появилось"

    browser.get(base_url + "/en-gb?route=checkout/cart")

    cart_table = browser.find_element(By.CSS_SELECTOR, '#shopping-cart tbody')
    cart_items = cart_table.find_elements(By.TAG_NAME, 'tr')

    for item in cart_items:
        item_name = item.find_element(By.CSS_SELECTOR, 'td:nth-child(2) a').text
        if item_name == product_name:
            break
    else:
        assert False, f"Товар {product_name} не найден в корзине"


@pytest.fixture
def change_currency(browser, wait):
    def _change_to(code):
        currency_form = browser.find_element(By.ID, 'form-currency')
        currency_dropdown = currency_form.find_element(By.CLASS_NAME, 'dropdown-toggle')
        currency_dropdown.click()

        new_currency_link = browser.find_element(By.XPATH, f'//a[@href="{code}"]')
        new_currency_link.click()

        wait.until(EC.staleness_of(currency_form))
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.price-new')))

    return _change_to


def test_change_price_product_page(browser, base_url, wait, change_currency):
    browser.get(base_url + "/en-gb/product/macbook")

    change_currency('USD')
    def get_price_and_currency():
        usd_currency_symbol = browser.find_element(By.CSS_SELECTOR, '.dropdown-toggle strong').text.strip()
        usd_price_text = browser.find_element(By.CSS_SELECTOR, '.price-new').text.strip()
        return  usd_currency_symbol, usd_price_text
    usd_currency_symbol, usd_price_text = get_price_and_currency()


    change_currency('EUR')
    eur_currency_symbol, eur_price_text = get_price_and_currency()
    assert usd_currency_symbol != eur_currency_symbol, "Валюта не была изменена при переходе на EUR!"
    assert usd_price_text != eur_price_text, "Цена осталась прежней при смене на EUR!"


    change_currency('GBP')
    gbp_currency_symbol, gbp_price_text = get_price_and_currency()
    assert eur_currency_symbol != gbp_currency_symbol, "Валюта не была изменена при переходе на GBP!"
    assert eur_price_text != gbp_price_text, "Цена осталась прежней при смене на GBP!"


    change_currency('USD')
    new_usd_currency_symbol, new_usd_price_text = get_price_and_currency()
    assert new_usd_currency_symbol == usd_currency_symbol, "Символ валюты изменился при восстановлении исходного состояния!"
    assert new_usd_price_text == usd_price_text, "Цена изменилась при восстановлении исходного состояния!"


def test_change_price_catalog_page(browser, base_url, wait, change_currency):
    browser.get(base_url + "/en-gb/catalog/laptop-notebook")

    change_currency('USD')

    def get_prices_and_currency():
        product_cards = browser.find_elements(By.CLASS_NAME, 'product-thumb')
        first_card = product_cards[0]
        last_card = product_cards[-1]
        first_price = first_card.find_element(By.CLASS_NAME, 'price-new').text.strip()
        last_price = last_card.find_element(By.CLASS_NAME, 'price-new').text.strip()
        currency_symbol = browser.find_element(By.CSS_SELECTOR, '.dropdown-toggle strong').text.strip()
        return first_price, last_price, currency_symbol
    first_price_in_usd, last_price_in_usd, usd_currency_symbol = get_prices_and_currency()

    change_currency('EUR')
    first_price_in_eur, last_price_in_eur, eur_currency_symbol = get_prices_and_currency()
    assert usd_currency_symbol != eur_currency_symbol, "Валюта не была изменена при переходе на EUR!"
    assert first_price_in_usd != first_price_in_eur, f"Цена первого товара ($first_price_in_usd) не изменилась при переходе на EUR!"
    assert last_price_in_usd != last_price_in_eur, f"Цена последнего товара ($last_price_in_usd) не изменилась при переходе на EUR!"

    change_currency('GBP')
    first_price_in_gbp, last_price_in_gbp, gbp_currency_symbol = get_prices_and_currency()
    assert eur_currency_symbol != gbp_currency_symbol, "Валюта не была изменена при переходе на GBP!"
    assert first_price_in_eur != first_price_in_gbp, f"Цена первого товара  ($first_price_in_eur) не изменилась при переходе на GBP!"
    assert last_price_in_eur != last_price_in_gbp, f"Цена последнего товара ($last_price_in_eur) не изменилась при переходе на GBP!"

    change_currency('USD')
    new_first_price_in_usd, new_last_price_in_usd, new_usd_currency_symbol = get_prices_and_currency()
    assert new_usd_currency_symbol == usd_currency_symbol, "Символ валюты изменился при восстановлении исходного состояния!"
    assert first_price_in_usd == new_first_price_in_usd, f"Цена первого товара ($first_price_in_usd) вернулась некорректно!"
    assert last_price_in_usd == new_last_price_in_usd, f"Цена последнего товара ($last_price_in_usd) вернулась некорректно!"