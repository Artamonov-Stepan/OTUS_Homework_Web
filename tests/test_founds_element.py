# from page_objects.admin_page import AdminPage
# from page_objects.catalog_page import CatalogPage
# from page_objects.main_page import MainPage
# from page_objects.product_page import ProductPage
# from page_objects.registration_page import RegistrationPage
#
#
# def test_administration_page(browser, base_url, wait):
#     admin_page = AdminPage(browser, wait)
#     admin_page.open_admin_page(base_url)
#     assert admin_page.find_browser_title(), (
#         "Заголовок страницы не содержит 'Administration'"
#     )
#     admin_page.find_card_name()
#     admin_page.find_card_body()
#     admin_page.find_login_button()
#     admin_page.find_password_field()
#     admin_page.find_link()
#
#
# def test_registration_page(browser, base_url, wait):
#     registration_page = RegistrationPage(browser, wait)
#     registration_page.open_register_page(base_url)
#     assert registration_page.find_browser_title(), (
#         "Заголовок страницы не содержит 'Register Account'"
#     )
#     registration_page.find_card_name()
#     registration_page.find_card_body()
#     registration_page.find_password_field()
#     registration_page.find_check_box()
#     registration_page.find_link()
#
#
# def test_main_page(browser, base_url, wait):
#     main_page = MainPage(browser, wait)
#     main_page.open_main_page(base_url)
#     assert main_page.find_browser_title(), "Заголовок страницы не содержит 'Your Store'"
#     main_page.find_card_name()
#     main_page.find_alert()
#     main_page.find_menu()
#     main_page.find_header()
#     main_page.find_cart_link()
#
#
# def test_catalog_page(browser, base_url, wait):
#     catalog_page = CatalogPage(browser, wait)
#     catalog_page.open_catalog_page(base_url)
#     assert catalog_page.find_browser_title(), (
#         "Заголовок страницы не содержит 'Laptops & Notebooks'"
#     )
#     catalog_page.find_product_name()
#     catalog_page.find_compare_total()
#     catalog_page.find_currency_menu()
#     catalog_page.find_compare_button()
#     catalog_page.find_group_item()
#
#
# def test_product_page(browser, base_url, wait):
#     product_page = ProductPage(browser, wait)
#     product_page.open_product_page(base_url)
#     assert product_page.find_product_page(), "Заголовок страницы не содержит 'sdf'"
#     product_page.find_product_image()
#     product_page.find_product_price()
#     product_page.find_breadcrumb()
#     product_page.find_add_button()
#     product_page.find_card_head()
