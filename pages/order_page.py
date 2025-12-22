# pages/order_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class OrderPage(BasePage):
    # Localizadores extraídos de tu UrbanRoutesPage original
    PHONE_FIELD = (By.ID, 'phone')
    CODE_PHONE_FIELD = (By.ID, 'code')
    CREDIT_CARD_FIELD = (By.CLASS_NAME, 'card-input')
    CCV_FIELD = (By.NAME, 'code')
    DRIVER_MSJ_FIELD = (By.ID, 'comment')
    ICE_CREAM_COUNTER = (By.XPATH,
                         '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')
    MANTA_CHECKBOX = (By.XPATH,
                      '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')

    # Botones de flujo
    ADD_PHONE_BUTTON = (By.CLASS_NAME, "np-text")
    NEXT_BUTTON_PHONE = (By.XPATH, ".//button[@class='button full']")
    CONFIRM_PHONE_BUTTON = (By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[2]/form/div[2]/button[1]")

    def __init__(self, driver):
        super().__init__(driver)

    # Métodos de interacción (Lógica que estaba en UrbanRoutesPage)
    def set_phone(self, phone_num):
        self.driver.find_element(*self.PHONE_FIELD).send_keys(phone_num)

    def get_phone(self):
        return self.driver.find_element(*self.PHONE_FIELD).get_property('value')

    def set_code_phone(self, phone_code):
        self.driver.find_element(*self.CODE_PHONE_FIELD).send_keys(phone_code)

    def get_code_phone(self):
        return self.driver.find_element(*self.CODE_PHONE_FIELD).get_property('value')

    def set_driver_message(self, message):
        self.driver.find_element(*self.DRIVER_MSJ_FIELD).send_keys(message)

    def get_driver_message(self):
        return self.driver.find_element(*self.DRIVER_MSJ_FIELD).get_property('value')

    def click_add_phone(self):
        self.driver.find_element(*self.ADD_PHONE_BUTTON).click()

    def confirm_phone_process(self):
        self.driver.find_element(*self.NEXT_BUTTON_PHONE).click()