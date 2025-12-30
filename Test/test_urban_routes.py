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
        cls.driver.get(data.urban_routes_url)
        cls.page = UrbanRoutesPage(cls.driver)

    def test_complete_order_flow(self):
        # 1. Direcciones
        self.page.set_route(data.address_from, data.address_to)
        self.page.order_taxi()

        # 2. Selección del modo Comfort
        self.page.select_comfort()

        # 3. Teléfono y SMS
        self.page.fill_phone(data.phone_number)
        code = retrieve_phone_code(self.driver)
        self.page.fill_sms_code(code)

        # 4. Agregar una Tarjeta
        self.page.add_card(data.card_number, data.card_code)

        # 5. Mensaje y extras
        self.page.add_message(data.message_for_driver)
        self.page.add_blanket()
        self.page.add_ice_creams(2)

        # 6. Finalizar y buscar taxi
        self.page.search_taxi()

        # 7. Validar que el modal de búsqueda apareció
        # Buscamos el elemento que tiene la cuenta regresiva o el estado de búsqueda
        self.page.wait_for_driver_info()
        assert self.driver.find_element(By.CLASS_NAME, "order-header-title").is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
