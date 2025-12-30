from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
import time


class UrbanRoutesPage(BasePage):
    # Selectores
    FROM = (By.ID, "from")
    TO = (By.ID, "to")
    ORDER_BUTTON = (By.CSS_SELECTOR, ".button.round")
    COMFORT = (By.XPATH, "//div[text()='Comfort']")

    PHONE_BUTTON = (By.CLASS_NAME, "np-text")
    PHONE_INPUT = (By.ID, "phone")
    CODE_INPUT = (By.ID, "code")
    CONFIRM_PHONE = (By.XPATH, "//button[text()='Siguiente']")
    CONFIRM_CODE = (By.XPATH, "//button[text()='Confirmar']")

    CARD_BUTTON = (By.CLASS_NAME, "pp-text")
    CARD_OPTION = (By.CSS_SELECTOR, ".pp-plus-container")
    CARD_INPUT = (By.ID, "number")
    CVV_INPUT = (By.NAME, "code")
    # Añadido para que el clic fuera del CVV funcione:
    MODAL_TITLE = (By.XPATH, "//div[text()='Agregar tarjeta']")
    ADD_CARD_SUBMIT = (By.XPATH, "//button[text()='Agregar']")
    MODAL_CONTENT = (By.CLASS_NAME, "payment-picker")
    CLOSE_PAYMENT_MODAL = (By.CSS_SELECTOR, ".payment-picker .close-button")

    DRIVER_MESSAGE = (By.ID, "comment")
    BLANKET = (By.CSS_SELECTOR, "span.slider.round")
    ICE_CREAM_PLUS = (By.CLASS_NAME, "counter-plus")
    SEARCH_TAXI = (By.CLASS_NAME, "smart-button")

    def set_route(self, start, end):
        self.type(self.FROM, start)
        time.sleep(1)
        self.type(self.TO, end)
        time.sleep(1)

    def order_taxi(self):
        self.click(self.ORDER_BUTTON)

    def select_comfort(self):
        self.click(self.COMFORT)
        time.sleep(1)

    def fill_phone(self, phone):
        self.click(self.PHONE_BUTTON)
        self.type(self.PHONE_INPUT, phone)
        self.click(self.CONFIRM_PHONE)

    def fill_sms_code(self, code):
        self.type(self.CODE_INPUT, code)
        self.click(self.CONFIRM_CODE)
        time.sleep(2)

    def add_card(self, number, cvv):
        self.click(self.CARD_BUTTON)
        self.click(self.CARD_OPTION)
        time.sleep(1)

        # 1. Capturar número de tarjeta
        self.type(self.CARD_INPUT, number)
        time.sleep(1)

        # 2. Capturar CVV
        # Usamos driver.find_element para evitar que el 'type' limpie el campo
        cvv_el = self.driver.find_element(*self.CVV_INPUT)
        cvv_el.send_keys(cvv + Keys.TAB)

        # 3. CLIC EN LA PANTALLA (Para habilitar el botón)
        # Hacemos clic en el fondo del modal para forzar el "desenfoque"
        self.click(self.MODAL_CONTENT)

        # 4. PRESIONAR AGREGAR
        # Tu BasePage esperará hasta 10 segundos a que el botón sea clicable
        self.click(self.ADD_CARD_SUBMIT)
        time.sleep(2)

        # 5. CERRAR MODAL
        self.click(self.CLOSE_PAYMENT_MODAL)
        time.sleep(2)

    def add_message(self, message):
        self.type(self.DRIVER_MESSAGE, message)
        time.sleep(2)

    def add_blanket(self):
        self.click(self.BLANKET)
        time.sleep(2)

    def add_ice_creams(self, amount=2):
        for _ in range(amount):
            self.click(self.ICE_CREAM_PLUS)
        time.sleep(2)

    def search_taxi(self):
        self.click(self.SEARCH_TAXI)

    def add_message(self, message):
        # Escribe el mensaje en el campo correspondiente
        self.type(self.DRIVER_MESSAGE, message)