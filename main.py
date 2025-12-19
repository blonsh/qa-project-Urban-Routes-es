import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from urban_routes_page import UrbanRoutesPage
from data import BASE_URL


class TestUrbanRoutes:

    def setup_method(self):
        options = Options()
        options.add_argument("--start-maximized")
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(BASE_URL)
        self.page = UrbanRoutesPage(self.driver)

    def teardown_method(self):
        self.driver.quit()

    def test_order_taxi_flow(self):
        self.page.set_addresses("Av. Reforma", "Aeropuerto")
        self.page.select_comfort_tariff()
        self.page.fill_phone("5512345678")
        self.page.add_credit_card("4111111111111111", "123")
        self.page.write_message("Voy con prisa")
        self.page.add_extras()
        self.page.add_ice_creams()
        self.page.order_taxi()

