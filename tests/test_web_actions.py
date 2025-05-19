from page_objects.admin_page import AdminPage
from page_objects.alert_element import AlertSuccessElement
from page_objects.catalog_page import CatalogPage
from page_objects.currency_element import CurrencyElement
from page_objects.main_page import MainPage
from page_objects.product_page import ProductPage
from page_objects.registration_page import RegistrationPage
from .utils import generate_random_data
from selenium.webdriver.common.alert import Alert


def test_check_login_button(browser, base_url, wait):
    admin_page = AdminPage(browser, wait)
    admin_page.open_admin_page(base_url)
    admin_page.enter_username("user")
    admin_page.enter_password("bitnami")
    admin_page.submit_login()
    assert admin_page.is_dashboard_opened(), (
        "Ожидаем получить заголовок страницы Dashboard!"
    )


def test_added_to_cart(browser, base_url, wait):
    main_page = MainPage(browser, wait)
    main_page.open_main_page(base_url)
    first_card = main_page.open_first_product_card()
    product_name = first_card.find_element(*main_page.NAME_LOCATOR).text
    main_page.submit_add_button()
    alert_success = AlertSuccessElement(browser, wait)
    assert "Success: You have added" in alert_success.alert.text, (
        "Сообщение об успешном добавлении товара не появилось"
    )
    alert_success.shopping_cart.click()
    rows = main_page.get_cart_item_rows()
    for row in rows:
        item_name = main_page.get_item_name_from_row(row)
        if item_name == product_name:
            break
    else:
        assert False, "Товар '{product_name}' не найден в корзине"


def test_change_price_product_page(browser, base_url, wait):
    product_page = ProductPage(browser, wait)
    product_page.open_product_page(base_url)

    currency = CurrencyElement(browser, wait)

    currency.change_currency("USD")
    usd_symbol = currency.get_current_currency_symbol()
    usd_price = product_page.find_product_price().text.strip()

    currency.change_currency("EUR")
    eur_symbol = currency.get_current_currency_symbol()
    eur_price = product_page.find_product_price().text.strip()
    assert usd_symbol != eur_symbol, "Валюта не изменилась при переходе на EUR!"
    assert usd_price != eur_price, "Цена не изменилась при смене на EUR!"

    currency.change_currency("GBP")
    gbp_symbol = currency.get_current_currency_symbol()
    gbp_price = product_page.find_product_price().text.strip()
    assert eur_symbol != gbp_symbol, "Валюта не изменилась при переходе на GBP!"
    assert eur_price != gbp_price, "Цена не изменилась при смене на GBP!"

    currency.change_currency("USD")
    final_usd_symbol = currency.get_current_currency_symbol()
    final_usd_price = product_page.find_product_price().text.strip()
    assert final_usd_symbol == usd_symbol, "Символ валюты изменился при возврате к USD!"
    assert final_usd_price == usd_price, "Цена изменилась при возврате к USD!"


def test_change_price_catalog_page(browser, base_url, wait):
    catalog_page = CatalogPage(browser, wait)
    catalog_page.open_catalog_page(base_url)

    currency = CurrencyElement(browser, wait)

    currency.change_currency("USD")
    usd_symbol = currency.get_current_currency_symbol()
    first_card = catalog_page.get_first_product_card()
    last_card = catalog_page.get_last_product_card()
    first_usd_price = catalog_page.get_product_card_price(first_card)
    last_usd_price = catalog_page.get_product_card_price(last_card)

    currency.change_currency("EUR")
    eur_symbol = currency.get_current_currency_symbol()
    first_card = catalog_page.get_first_product_card()
    last_card = catalog_page.get_last_product_card()
    first_eur_price = catalog_page.get_product_card_price(first_card)
    last_eur_price = catalog_page.get_product_card_price(last_card)
    assert usd_symbol != eur_symbol, "Валюта не изменилась при переходе на EUR!"
    assert first_usd_price != first_eur_price, (
        "Цена первого товара не изменилась при переходе на EUR!"
    )
    assert last_usd_price != last_eur_price, (
        "Цена последнего товара не изменилась при переходе на EUR!"
    )

    currency.change_currency("GBP")
    gbp_symbol = currency.get_current_currency_symbol()
    first_card = catalog_page.get_first_product_card()
    last_card = catalog_page.get_last_product_card()
    first_gbp_price = catalog_page.get_product_card_price(first_card)
    last_gbp_price = catalog_page.get_product_card_price(last_card)
    assert eur_symbol != gbp_symbol, "Валюта не изменилась при переходе на GBP!"
    assert first_eur_price != first_gbp_price, (
        "Цена первого товара не изменилась при переходе на GBP!"
    )
    assert last_eur_price != last_gbp_price, (
        "Цена последнего товара не изменилась при переходе на GBP!"
    )

    currency.change_currency("USD")
    final_usd_symbol = currency.get_current_currency_symbol()
    first_card = catalog_page.get_first_product_card()
    last_card = catalog_page.get_last_product_card()
    final_first_usd_price = catalog_page.get_product_card_price(first_card)
    final_last_usd_price = catalog_page.get_product_card_price(last_card)
    assert final_usd_symbol == usd_symbol, "Символ валюты изменился при возврате к USD!"
    assert final_first_usd_price == first_usd_price, (
        "Цена первого товара изменилась при возврате к USD!"
    )
    assert final_last_usd_price == last_usd_price, (
        "Цена последнего товара изменилась при возврате к USD!"
    )


def test_add_new_product(browser, base_url, wait):
    admin_page = AdminPage(browser, wait)
    admin_page.open_admin_page(base_url)
    admin_page.enter_username("user")
    admin_page.enter_password("bitnami")
    admin_page.submit_login()
    assert admin_page.is_dashboard_opened(), (
        "Ожидаем получить заголовок страницы Dashboard!"
    )

    admin_page.click_header_menu()
    admin_page.click_to_menu()
    admin_page.click_to_products()
    admin_page.click_add_new()

    user_data = generate_random_data()
    admin_page.enter_product_name(user_data["product_name"])
    admin_page.enter_tag_title(user_data["tag_title"])
    admin_page.click_data_tab()
    admin_page.enter_model(user_data["model"])
    admin_page.click_seo_tab()
    admin_page.enter_keyword(user_data["keyword"])
    admin_page.click_save_button()

    alert_success = AlertSuccessElement(browser, wait)
    assert "Success: You have modified products!" in alert_success.alert.text, (
        "Сообщение об успешном добавлении товара не появилось"
    )


def test_remove_new_product(browser, base_url, wait):
    admin_page = AdminPage(browser, wait)
    admin_page.open_admin_page(base_url)
    admin_page.enter_username("user")
    admin_page.enter_password("bitnami")
    admin_page.submit_login()
    assert admin_page.is_dashboard_opened(), (
        "Ожидаем получить заголовок страницы Dashboard!"
    )

    admin_page.click_header_menu()
    admin_page.click_to_menu()
    admin_page.click_to_products()
    admin_page.select_product()
    admin_page.click_delete_button()

    alert = Alert(browser)
    alert.accept()

    alert_success = AlertSuccessElement(browser, wait)
    assert "Success: You have modified products!" in alert_success.alert.text, (
        "Сообщение об успешном удалении товара не появилось"
    )


def test_currency_switch(browser, base_url, wait):
    main_page = MainPage(browser, wait)
    main_page.open_main_page(base_url)

    currency = CurrencyElement(browser, wait)

    currency.change_currency("USD")
    usd_symbol = currency.get_current_currency_symbol()
    assert usd_symbol == "$", "Валюта не изменилась на USD!"

    currency.change_currency("EUR")
    eur_symbol = currency.get_current_currency_symbol()
    assert eur_symbol == "€", "Валюта не изменилась на EUR!"

    currency.change_currency("GBP")
    gbp_symbol = currency.get_current_currency_symbol()
    assert gbp_symbol == "£", "Валюта не изменилась на GBP!"

    currency.change_currency("USD")
    final_usd_symbol = currency.get_current_currency_symbol()
    assert final_usd_symbol == "$", "Валюта не вернулась к USD!"


def test_register_new_user(browser, base_url, wait):
    register_page = RegistrationPage(browser, wait)
    register_page.open_register_page(base_url)

    user_data = generate_random_data()

    register_page.enter_firstname(user_data["first_name"])
    register_page.enter_lastname(user_data["last_name"])
    register_page.enter_email(user_data["email"])
    register_page.enter_password(user_data["password"])

    register_page.agree_to_policy()
    register_page.submit_login()
    assert register_page.is_account_created(), (
        "Ожидаем получить заголовок страницы Your Account Has Been Created!!"
    )
