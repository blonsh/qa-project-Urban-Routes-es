# Ejemplo de lo que debe ir en pages/urban_routes_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class UrbanRoutesPage:
    # Tus selectores
    comfort_rate_icon = (By.XPATH, "//div[contains(text(), 'Comfort')]")

    def __init__(self, driver):
        self.driver = driver

    def click_comfort_rate_icon(self):
        # Esta espera evita el error de "Element not found"
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(self.comfort_rate_icon)
        ).click()
