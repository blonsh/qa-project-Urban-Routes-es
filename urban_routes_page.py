from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

class UrbanRoutesPage:
    address_from = (By.ID, "from")
    address_to = (By.ID, "to")
    comfort_tariff = (By.XPATH, "//div[text()='Comfort']")
    phone_input = (By.ID, "phone")
    add_card_button = (By.CLASS_NAME, "pp-button")
    card_number = (By.ID, "number")
    card_code = (By.ID, "code")
    link_card_button = (By.CLASS_NAME, "pp-button")
    message_driver = (By.ID, "comment")
    blanket_checkbox = (By.ID, "blanket")
    tissues_checkbox = (By.ID, "tissues")
    ice_cream_plus = (By.CLASS_NAME, "counter-plus")
    order_button = (By.CLASS_NAME, "order-button")
    modal_search = (By.CLASS_NAME, "order-search")

    def __init__(self, driver):
        self.driver = driver

    def set_addresses(self, from_addr, to_addr):
        self.driver.find_element(*self.address_from).send_keys(from_addr)
        self.driver.find_element(*self.address_to).send_keys(to_addr)

    def select_comfort(self):
        self.driver.find_element(*self.comfort_tariff).click()

    def fill_phone(self, phone):
        self.driver.find_element(*self.phone_input).send_keys(phone)

    def add_card(self, number, code):
        self.driver.find_element(*self.add_card_button).click()
        self.driver.find_element(*self.card_number).send_keys(number)
        code_input = self.driver.find_element(*self.card_code)
        code_input.send_keys(code)
        code_input.send_keys(Keys.TAB)  # perder foco
        self.driver.find_element(*self.link_card_button).click()

    def write_message(self, text):
        self.driver.find_element(*self.message_driver).send_keys(text)

    def add_extras(self):
        self.driver.find_element(*self.blanket_checkbox).click()
        self.driver.find_element(*self.tissues_checkbox).click()

    def add_ice_creams(self):
        plus = self.driver.find_element(*self.ice_cream_plus)
        plus.click()
        plus.click()

    def order_taxi(self):
        self.driver.find_element(*self.order_button).click()
