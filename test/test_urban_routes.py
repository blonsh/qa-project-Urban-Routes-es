import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from pages.urban_routes_page import UrbanRoutesPage
from helpers import retrieve_phone_code

class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):
        options = Options()
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.maximize_window()
        cls.driver.implicitly_wait(10)
        cls.driver.get(data.URBAN_ROUTES_URL)
        cls.page = UrbanRoutesPage(cls.driver)

    # Configurar la dirección
    def test_set_route(self):
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        assert self.page.get_from_value() == data.ADDRESS_FROM
        assert self.page.get_to_value() == data.ADDRESS_TO

    # Seleccionar la tarifa Comfort
    def test_select_comfort_rate(self):
        self.page.order_taxi()
        self.page.select_comfort()
        assert "Comfort" in self.page.get_selected_rate_text()

    # Rellenar el número de teléfono
    def test_fill_phone_number(self):
        self.page.fill_phone(data.PHONE_NUMBER)
        code = retrieve_phone_code(self.driver)
        self.page.fill_sms_code(code)
        assert self.page.get_phone_value() == data.PHONE_NUMBER

    # Agregar una tarjeta de crédito
    def test_add_credit_card(self):
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)
        assert self.page.is_card_added()

    # Escribir un mensaje para el conductor
    def test_write_message_for_driver(self):
        self.page.add_message(data.MESSAGE_FOR_DRIVER)
        assert self.page.get_message_value() == data.MESSAGE_FOR_DRIVER

    # Pedir una manta y pañuelos
    def test_order_blanket_and_handkerchiefs(self):
        self.page.add_blanket()
        assert self.page.is_blanket_selected()

    # Pedir 2 helados
    def test_order_2_ice_creams(self):
        self.page.add_ice_creams(2)
        assert self.page.get_ice_cream_count() == "2"

    # Verificar que aparece el modal de búsqueda de taxi
    def test_taxi_search_modal_appears(self):
        self.page.search_taxi()
        assert self.page.is_search_modal_visible()

    # 9. Esperar la información del conductor
    def test_wait_for_driver_info(self):
        self.page.wait_for_driver_info()
        assert self.page.is_driver_assigned()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()