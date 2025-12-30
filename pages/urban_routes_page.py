from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
    MODAL_TITLE = (By.XPATH, "//div[text()='Agregar tarjeta']")
    ADD_CARD_SUBMIT = (By.XPATH, "//button[text()='Agregar']")
    MODAL_CONTENT = (By.CLASS_NAME, "payment-picker")
    CLOSE_PAYMENT_MODAL = (By.CSS_SELECTOR, ".payment-picker .close-button")

    DRIVER_MESSAGE = (By.ID, "comment")
    BLANKET = (By.CSS_SELECTOR, "span.slider.round")
    ICE_CREAM_PLUS = (By.CLASS_NAME, "counter-plus")
    SEARCH_TAXI = (By.XPATH, "//span[text()='Pedir un taxi']/parent::button")

    def set_route(self, start, end):
        self.type(self.FROM, start)
        self.type(self.TO, end)

    def order_taxi(self):
        self.click(self.ORDER_BUTTON)

    def select_comfort(self):
        self.click(self.COMFORT)

    def fill_phone(self, phone):
        self.click(self.PHONE_BUTTON)
        self.type(self.PHONE_INPUT, phone)
        self.click(self.CONFIRM_PHONE)

    def fill_sms_code(self, code):
        self.type(self.CODE_INPUT, code)
        self.click(self.CONFIRM_CODE)

    def add_card(self, number, cvv):
        self.click(self.CARD_BUTTON)
        self.click(self.CARD_OPTION)

        # Capturar número de tarjeta
        self.type(self.CARD_INPUT, number)

        # Capturar CVV
        cvv_el = self.driver.find_element(*self.CVV_INPUT)
        cvv_el.send_keys(cvv + Keys.TAB)

        # CLIC EN LA PANTALLA (Para habilitar el botón)
        self.click(self.MODAL_CONTENT)

        # PRESIONAR AGREGAR
        self.click(self.ADD_CARD_SUBMIT)

        # CERRAR MODAL
        self.click(self.CLOSE_PAYMENT_MODAL)

    def add_message(self, message):
        self.type(self.DRIVER_MESSAGE, message)

    def add_blanket(self):
        self.click(self.BLANKET)

    def add_ice_creams(self, amount=2):
        for _ in range(amount):
            self.click(self.ICE_CREAM_PLUS)

    def search_taxi(self):
        wait = WebDriverWait(self.driver, 20)
        button = wait.until(EC.element_to_be_clickable(self.SEARCH_TAXI))
        button.click()

    def wait_for_driver_info(self):
        WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "order-number"))
        )
        time.sleep(2)
