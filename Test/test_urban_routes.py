import data
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
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

    def test_complete_order_flow(self):
        # Establecer ruta de viaje e iniciar la solicitud de transporte
        self.page.set_route(data.ADDRESS_FROM, data.ADDRESS_TO)
        self.page.order_taxi()

        # Selección del modo Comfort
        self.page.select_comfort()

        # Captura de Teléfono y validación de SMS
        self.page.fill_phone(data.PHONE_NUMBER)
        code = retrieve_phone_code(self.driver)
        self.page.fill_sms_code(code)

        # Agregar una Tarjeta y CVV
        self.page.add_card(data.CARD_NUMBER, data.CARD_CODE)

        # Mensaje para el conductor y solicitud de extras
        self.page.add_message(data.MESSAGE_FOR_DRIVER)
        self.page.add_blanket()
        self.page.add_ice_creams(2)

        # Buscar taxi
        self.page.search_taxi()
        self.page.wait_for_driver_info()
        assert self.driver.find_element(By.CLASS_NAME, "order-header-title").is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
