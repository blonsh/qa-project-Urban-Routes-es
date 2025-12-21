from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time
import json
from selenium.common import WebDriverException

class UrbanRoutesPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)
        
        # Localizadores - Direcciones
        self.from_field = (By.ID, "from")
        self.to_field = (By.ID, "to")
        self.suggested_route_from = (By.XPATH, "//div[@class='pac-item'][1]")
        self.suggested_route_to = (By.XPATH, "//div[@class='pac-item'][1]")
        
        # Localizadores - Tarifa
        self.comfort_tariff = (By.XPATH, "//div[contains(@class, 'tariff-picker')]//div[contains(text(), 'Comfort')]")
        
        # Localizadores - Teléfono
        self.phone_number_button = (By.XPATH, "//div[contains(@class, 'np-button')]")
        self.phone_number_field = (By.ID, "phone")
        self.phone_number_next_button = (By.XPATH, "//button[contains(@class, 'button') and contains(@class, 'full')]")
        self.phone_code_field = (By.ID, "code")
        self.phone_code_confirm_button = (By.XPATH, "//button[contains(@class, 'button') and contains(@class, 'full')]")
        
        # Localizadores - Tarjeta de crédito
        self.payment_method_button = (By.XPATH, "//div[contains(@class, 'pp-button')]")
        self.add_card_button = (By.XPATH, "//div[contains(@class, 'pp-plus-container')]")
        self.card_number_field = (By.ID, "number")
        self.card_code_field = (By.ID, "code")  # CVV - id="code" class="card-input"
        self.card_code_field_selector = (By.XPATH, "//input[@id='code' and contains(@class, 'card-input')]")
        self.card_link_button = (By.XPATH, "//button[contains(@class, 'button') and contains(text(), 'Enlazar') or contains(text(), 'link')]")
        
        # Localizadores - Mensaje al conductor
        self.comment_for_driver_field = (By.ID, "comment")
        
        # Localizadores - Servicios adicionales
        self.blanket_switch = (By.XPATH, "//div[@class='switch' and contains(., 'Manta')]//span[@class='switch__slider']")
        self.tissues_switch = (By.XPATH, "//div[@class='switch' and contains(., 'Pañuelos')]//span[@class='switch__slider']")
        self.ice_cream_counter = (By.XPATH, "//div[contains(@class, 'counter')]//div[contains(@class, 'counter__plus')]")
        self.ice_cream_value = (By.XPATH, "//div[contains(@class, 'counter')]//div[@class='counter__value']")
        
        # Localizadores - Confirmar taxi
        self.order_button = (By.XPATH, "//button[contains(@class, 'smart-button')]")
        self.order_button_enabled = (By.XPATH, "//button[contains(@class, 'smart-button') and not(contains(@class, 'smart-button_disabled'))]")
        self.order_confirmed_modal = (By.XPATH, "//div[contains(@class, 'order-header')]")
        
        # Localizadores - Información del conductor (opcional)
        self.driver_modal = (By.XPATH, "//div[contains(@class, 'order-body')]")
        self.driver_name = (By.XPATH, "//div[@class='order-header-title']")
        self.driver_vehicle_plate = (By.XPATH, "//div[@class='order-header-subtitle']")

    def set_route(self, from_address, to_address):
        """Configura la ruta con origen y destino"""
        # Ingresar dirección de origen
        from_input = self.wait.until(EC.presence_of_element_located(self.from_field))
        from_input.clear()
        from_input.send_keys(from_address)
        time.sleep(1)  # Esperar a que aparezcan las sugerencias
        # Seleccionar primera sugerencia
        self.wait.until(EC.element_to_be_clickable(self.suggested_route_from)).click()
        
        # Ingresar dirección de destino
        to_input = self.wait.until(EC.presence_of_element_located(self.to_field))
        to_input.clear()
        to_input.send_keys(to_address)
        time.sleep(1)  # Esperar a que aparezcan las sugerencias
        # Seleccionar primera sugerencia
        self.wait.until(EC.element_to_be_clickable(self.suggested_route_to)).click()
        
        time.sleep(1)  # Esperar a que se actualice la ruta

    def select_comfort_tariff(self):
        """Selecciona la tarifa Comfort"""
        comfort_option = self.wait.until(EC.element_to_be_clickable(self.comfort_tariff))
        comfort_option.click()
        time.sleep(0.5)

    def fill_phone_number(self, phone_number):
        """Rellena el número de teléfono y valida con código SMS"""
        # Hacer clic en el botón para agregar teléfono
        phone_button = self.wait.until(EC.element_to_be_clickable(self.phone_number_button))
        phone_button.click()
        
        # Ingresar número de teléfono
        phone_field = self.wait.until(EC.presence_of_element_located(self.phone_number_field))
        phone_field.clear()
        phone_field.send_keys(phone_number)
        
        # Hacer clic en siguiente
        next_button = self.wait.until(EC.element_to_be_clickable(self.phone_number_next_button))
        next_button.click()
        
        # Esperar a que aparezca el campo de código
        time.sleep(2)  # Dar tiempo para que se envíe el SMS
        
        # Obtener código usando retrieve_phone_code
        code = self.retrieve_phone_code()
        
        # Ingresar código de confirmación
        code_field = self.wait.until(EC.presence_of_element_located(self.phone_code_field))
        code_field.clear()
        code_field.send_keys(code)
        
        # Confirmar código
        confirm_button = self.wait.until(EC.element_to_be_clickable(self.phone_code_confirm_button))
        confirm_button.click()
        
        time.sleep(1)

    def add_credit_card(self, card_number, card_code):
        """Agrega una tarjeta de crédito. El botón 'link' se activa cuando el campo CVV pierde el foco"""
        # Hacer clic en el botón de método de pago
        payment_button = self.wait.until(EC.element_to_be_clickable(self.payment_method_button))
        payment_button.click()
        
        # Hacer clic en agregar tarjeta
        add_card_btn = self.wait.until(EC.element_to_be_clickable(self.add_card_button))
        add_card_btn.click()
        
        # Ingresar número de tarjeta
        card_number_input = self.wait.until(EC.presence_of_element_located(self.card_number_field))
        card_number_input.clear()
        card_number_input.send_keys(card_number)
        
        # Ingresar CVV en el campo con id="code" class="card-input"
        cvv_field = self.wait.until(EC.presence_of_element_located(self.card_code_field_selector))
        cvv_field.clear()
        cvv_field.send_keys(card_code)
        
        # CRÍTICO: El botón 'link' no se activa hasta que el campo CVV pierde el enfoque
        # Simular pérdida de foco presionando TAB o haciendo clic en otro lugar
        cvv_field.send_keys(Keys.TAB)
        # Alternativa: hacer clic en otro elemento para cambiar el foco
        time.sleep(0.5)  # Pequeña espera para que se procese el cambio de foco
        
        # Esperar a que el botón link se habilite
        link_button = self.wait.until(EC.element_to_be_clickable(self.card_link_button))
        link_button.click()
        
        # Cerrar el modal de tarjeta (si es necesario)
        time.sleep(1)

    def set_message_to_driver(self, message):
        """Escribe un mensaje para el conductor"""
        comment_field = self.wait.until(EC.presence_of_element_located(self.comment_for_driver_field))
        comment_field.clear()
        comment_field.send_keys(message)
        time.sleep(0.5)

    def request_blanket_and_tissues(self):
        """Solicita manta y pañuelos"""
        # Activar switch de manta
        blanket_switch = self.wait.until(EC.element_to_be_clickable(self.blanket_switch))
        if not blanket_switch.get_attribute("class") or "switch__slider_active" not in blanket_switch.get_attribute("class"):
            blanket_switch.click()
        
        # Activar switch de pañuelos
        tissues_switch = self.wait.until(EC.element_to_be_clickable(self.tissues_switch))
        if not tissues_switch.get_attribute("class") or "switch__slider_active" not in tissues_switch.get_attribute("class"):
            tissues_switch.click()
        
        time.sleep(0.5)

    def request_ice_creams(self, quantity=2):
        """Solicita helados. Por defecto 2 helados"""
        # Obtener el contador actual
        current_value_element = self.wait.until(EC.presence_of_element_located(self.ice_cream_value))
        current_value = int(current_value_element.text) if current_value_element.text else 0
        
        # Calcular cuántos clics necesitamos
        clicks_needed = quantity - current_value
        
        # Hacer clic en el botón de incremento las veces necesarias
        if clicks_needed > 0:
            plus_button = self.wait.until(EC.element_to_be_clickable(self.ice_cream_counter))
            for _ in range(clicks_needed):
                plus_button.click()
                time.sleep(0.2)
        
        time.sleep(0.5)

    def confirm_taxi_search(self):
        """Confirma y activa el modal de búsqueda de taxi"""
        # Esperar a que el botón de ordenar esté habilitado
        order_button = self.wait.until(EC.element_to_be_clickable(self.order_button_enabled))
        order_button.click()
        
        # Esperar a que aparezca el modal de confirmación
        self.wait.until(EC.presence_of_element_located(self.order_confirmed_modal))
        time.sleep(1)

    def wait_for_driver_info(self, timeout=30):
        """Espera a que aparezca la información del conductor en el modal (opcional)"""
        try:
            # Esperar a que el modal cambie de "Buscando taxi" a mostrar información del conductor
            driver_info = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(self.driver_name)
            )
            return driver_info.text
        except TimeoutException:
            return None

    # no modificar
    def retrieve_phone_code(self) -> str:
        """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
        Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
        El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""
        code = None
        for i in range(10):
            try:
                logs = [log["message"] for log in self.driver.get_log('performance') if log.get("message")
                        and 'api/v1/number?number' in log.get("message")]
                for log in reversed(logs):
                    message_data = json.loads(log)["message"]
                    body = self.driver.execute_cdp_cmd('Network.getResponseBody',
                                                      {'requestId': message_data["params"]["requestId"]})
                    code = ''.join([x for x in body['body'] if x.isdigit()])
            except WebDriverException:
                time.sleep(1)
                continue
            if not code:
                raise Exception("No se encontró el código de confirmación del teléfono.\n"
                                "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
            return code
