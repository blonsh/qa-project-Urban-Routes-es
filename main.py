import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1) #sleep incluido con el codigo base donde las instricciones dice NO MODIFICAR
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    #CSS selector es utilizado en la funcion: test_select_comfort
    from_field = (By.ID, 'from') #selector 1 ID
    to_field = (By.ID, 'to')
    phone_field = (By.ID, 'phone')
    code_phone_field = (By.ID, 'code')
    creditCard_field = (By.CLASS_NAME, 'card-input') #Selector 2 nombre de la clase
    ccv_field = (By.NAME, 'code') # selector 3 nombre
    driver_msj_field = (By.ID, 'comment')
    ice_cream_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[2]')
    manta_field = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')

    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_phone(self, phone_num):
        self.driver.find_element(*self.phone_field).send_keys(phone_num)

    def get_phone(self):
        return self.driver.find_element(*self.phone_field).get_property('value')

    def set_code_phone(self, phone_code):
        self.driver.find_element(*self.code_phone_field).send_keys(phone_code)

    def get_code_phone(self):
        return self.driver.find_element(*self.code_phone_field).get_property('value')

    def set_creditCard(self, credit_cart):
        self.driver.find_element(*self.creditCard_field).send_keys(credit_cart)

    def get_creditCard(self):
        return self.driver.find_element(*self.creditCard_field).get_property('value')

    def set_ccv(self, ccv):
        self.driver.find_element(*self.ccv_field).send_keys(ccv)

    def get_ccv(self):
        return self.driver.find_element(*self.ccv_field).get_property('value')

    def set_driver_msj(self, msj):
        self.driver.find_element(*self.driver_msj_field).send_keys(msj)

    def get_driver_msj(self):
        return self.driver.find_element(*self.driver_msj_field).get_property('value')

    def get_ice_cream(self):
        return self.driver.find_element(*self.ice_cream_field).text

    def get_manta(self):
        return self.driver.find_element(*self.manta_field).is_enabled()

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        from selenium.webdriver import DesiredCapabilities
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
        cls.driver = webdriver.Chrome()

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        self.driver.implicitly_wait(3)
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_select_comfort(self):
        #self.test_set_route()
        # Buscar el botón pedir taxi y hacer clic en él
        self.driver.find_element(By.XPATH, ".//button[@class='button round']").click()
        # Buscar opcion Comfort y hacer clic
        self.driver.find_element(By.CSS_SELECTOR, '[alt="Comfort"]').click()
        assert expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, '[alt="Comfort"]'))

    def test_fill_phone(self):
        #self.test_select_comfort()
        self.driver.find_element(By.CLASS_NAME, "np-text").click()
        routes_page = UrbanRoutesPage(self.driver)
        #Llenar campo de telefono
        phone_num = data.phone_number
        routes_page.set_phone(phone_num)
        assert routes_page.get_phone() == phone_num
        self.driver.find_element(By.XPATH, ".//button[@class='button full']").click()
        #Encontrar codigo de confirmacion
        phone_code = retrieve_phone_code(self.driver)
        #Lenar campo con codigo de confirmacion
        routes_page.set_code_phone(phone_code)
        assert routes_page.get_code_phone() == phone_code
        self.driver.find_element(By.XPATH, "//*[@id='root']/div/div[1]/div[2]/div[2]/form/div[2]/button[1]").click()

    def test_add_credit_card(self):
        #self.test_fill_phone()
        self.driver.find_element(By.XPATH, ".//div[@class='pp-button filled']").click()
        #Seleccionar opcion tarjeta de credito
        self.driver.find_element(By.XPATH, "//*[@id ='root']/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]").click()

        card_num = data.card_number
        ccv_num = data.card_code
        routes_page = UrbanRoutesPage(self.driver)

        routes_page.set_creditCard(card_num)
        routes_page.set_ccv(ccv_num)
        assert routes_page.get_creditCard() == card_num
        assert routes_page.get_ccv() == ccv_num
        #Activar boton 'Agregar'
        self.driver.find_element(By.XPATH, "//*[@id='number']").click()
        #click boton 'Agregar'
        self.driver.find_element(By.XPATH, "//*[@id='root']/div/div[2]/div[2]/div[2]/form/div[3]/button[1]").click()
        # cerrar pantalla de efectivo/ tarjeta
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button').click()

    def test_msj_driver(self):
        #self.test_add_credit_card()
        routes_page = UrbanRoutesPage(self.driver)
        msj = data.message_for_driver
        routes_page.set_driver_msj(msj)
        assert routes_page.get_driver_msj() == msj

    def test_manta_panuelos(self):
        #self.test_msj_driver()
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span').click()
        assert routes_page.get_manta() == True


    def test_ice_cream(self):
        #self.test_manta_panuelos()
        num_iceCream = '2'
        routes_page = UrbanRoutesPage(self.driver)
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]').click()
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]').click()
        assert routes_page.get_ice_cream() == num_iceCream

    def test_search_taxi(self):
        #self.test_ice_cream()
        self.driver.find_element(By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button/span[2]').click()

    def teardown_class(cls):
        cls.driver.quit()