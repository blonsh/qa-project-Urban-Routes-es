import json
import time
import data

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from pages.order_page import OrderPage


# --- FUNCIÓN AUXILIAR PARA RECUPERAR EL CÓDIGO SMS ---
def retrieve_phone_code(driver):
    code = None
    for _ in range(10):
        logs = driver.get_log('performance')
        for entry in logs:
            message = json.loads(entry['message'])['message']
            if message.get('method') == 'Network.responseReceived':
                url = message.get('params', {}).get('response', {}).get('url', '')
                if 'code=' in url:
                    return url.split('code=')[-1]
        time.sleep(1)
    return code


class TestUrbanRoutes:
    driver = None
    wait = None

    @classmethod
    def setup_class(cls):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability(
            "goog:loggingPrefs", {'performance': 'ALL'}
        )

        cls.driver = webdriver.Chrome(
            service=Service(),
            options=chrome_options
        )
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.wait = WebDriverWait(cls.driver, 15)

    # 1. Configurar las direcciones
    def test_set_route(self):
        from_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'from'))
        )
        to_field = self.wait.until(
            EC.element_to_be_clickable((By.ID, 'to'))
        )

        from_field.send_keys(data.address_from)
        to_field.send_keys(data.address_to)

        time.sleep(2)

        assert from_field.get_attribute('value') == data.address_from
        assert to_field.get_attribute('value') == data.address_to

    # 2. Seleccionar la tarifa Comfort
    def test_select_comfort_rate(self):
        from_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "from"))
        )
        to_field = self.wait.until(
            EC.presence_of_element_located((By.ID, "to"))
        )

        if not from_field.get_attribute("value"):
            from_field.send_keys(data.address_from)

        if not to_field.get_attribute("value"):
            to_field.send_keys(data.address_to)

        time.sleep(2)

        order_page = OrderPage(self.driver)
        order_page.open_tariffs()
        order_page.select_comfort()

        assert order_page.is_comfort_selected(), \
            "La tarifa Comfort NO quedó seleccionada"

    # 3. Rellenar el número de teléfono
    def test_set_phone_number(self):
        phone_opener = self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'np-text'))
        )
        phone_opener.click()

        self.wait.until(
            EC.visibility_of_element_located((By.ID, 'phone'))
        ).send_keys(data.phone_number)

        self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Siguiente')]"
        ).click()

        code = retrieve_phone_code(self.driver)
        assert code is not None, "No se capturó el código SMS"

        self.wait.until(
            EC.visibility_of_element_located((By.ID, 'code'))
        ).send_keys(code)

        self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Confirmar')]"
        ).click()

        assert phone_opener.text == data.phone_number

    # 4. Agregar una tarjeta de crédito
    def test_add_credit_card(self):
        self.driver.find_element(By.CLASS_NAME, 'pp-text').click()

        self.wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'pp-plus'))
        ).click()

        card_input = self.wait.until(
            EC.visibility_of_element_located((By.ID, 'number'))
        )
        card_input.send_keys(data.card_number)

        cvv_input = self.driver.find_element(By.ID, 'code')
        cvv_input.send_keys(data.card_code)
        cvv_input.send_keys(Keys.TAB)

        self.driver.find_element(
            By.XPATH, "//button[contains(text(),'Enlace')]"
        ).click()

        self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[1]/button")
            )
        ).click()

        payment_status = self.driver.find_element(
            By.CLASS_NAME, 'pp-value-text'
        ).text

        assert "Tarjeta" in payment_status

    # 5. Escribir un mensaje para el conductor
    def test_message_for_driver(self):
        comment_input = self.driver.find_element(By.ID, 'comment')
        comment_input.send_keys(data.message_for_driver)

        assert comment_input.get_attribute('value') == data.message_for_driver

    # 6. Pedir manta y pañuelos
    def test_order_blanket_and_tissues(self):
        blanket_btn = self.driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Manta y pañuelos')]/..//span[@class='slider round']"
        )
        blanket_btn.click()

        checkbox = self.driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Manta y pañuelos')]/..//input"
        )

        assert checkbox.is_selected()

    # 7. Pedir 2 helados
    def test_order_ice_creams(self):
        plus_btn = self.driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Helado')]/..//div[@class='counter-plus']"
        )
        plus_btn.click()
        plus_btn.click()

        counter = self.driver.find_element(
            By.XPATH,
            "//*[contains(text(),'Helado')]/..//div[@class='counter-value']"
        ).text

        assert counter == "2"

    # 8. Aparece el modal de búsqueda de taxi
    def test_search_taxi_modal(self):
        self.driver.find_element(By.CLASS_NAME, 'smart-button').click()

        order_body = self.wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'order-body'))
        )

        assert order_body.is_displayed()

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()

