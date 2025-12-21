import pytest
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from urban_routes_page import UrbanRoutesPage
from data import BASE_URL


class TestUrbanRoutes:
    @pytest.fixture(scope='class', autouse=True)
    def setup(self):
        """Fixture para configurar el driver antes de las pruebas"""
        # Configurar opciones de Chrome
        chrome_options = Options()
        # Opciones para evitar problemas en macOS
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        # NO cerrar el navegador automáticamente cuando el script termine (útil para debugging)
        chrome_options.add_experimental_option("detach", True)
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        driver.get(BASE_URL)
        
        # Esperar a que la página cargue completamente (incluyendo JavaScript)
        # Esto es crítico ya que la página parece cargar su contenido dinámicamente
        time.sleep(5)  # Esperar inicial para que el contenido se renderice
        
        # Esperar a que el documento esté listo y el JavaScript haya terminado
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        
        # Esperar adicional para que los elementos dinámicos se rendericen
        time.sleep(3)
        
        page = UrbanRoutesPage(driver)
        
        # Asignar a la clase para que esté disponible en los métodos de prueba
        TestUrbanRoutes.driver = driver
        TestUrbanRoutes.page = page
        
        yield
        
        # Mantener el navegador abierto por más tiempo para inspección manual
        # El navegador se mantendrá abierto 60 segundos antes de cerrarse
        print("\n=== Navegador se mantendrá abierto por 60 segundos para inspección ===")
        print("Puedes usar las herramientas de desarrollador (F12) para inspeccionar los elementos")
        time.sleep(60)
        driver.quit()
        print("\n=== Navegador cerrado ===")

    def test_01_set_route(self):
        """Paso 1: Configurar la dirección (origen y destino)"""
        print("\n=== Ejecutando: Configurar dirección ===")
        print("Esperando 5 segundos para que la página cargue completamente...")
        time.sleep(5)
        
        try:
            self.page.set_route("East 2nd Street, 601", "1300 1st St")
            print("✓ Dirección configurada correctamente")
        except Exception as e:
            print(f"\n❌ ERROR en set_route: {e}")
            print("\nEl navegador se mantendrá abierto para que puedas inspeccionar los elementos.")
            print("Busca el campo de dirección de origen en la página y anota su selector (ID, clase, XPath)")
            time.sleep(30)  # Mantener abierto 30 segundos adicionales si hay error
            raise
    
    def test_02_select_comfort_tariff(self):
        """Paso 2: Seleccionar la tarifa Comfort"""
        print("\n=== Ejecutando: Seleccionar tarifa Comfort ===")
        self.page.select_comfort_tariff()
        print("✓ Tarifa Comfort seleccionada")
        time.sleep(2)
    
    def test_03_fill_phone_number(self):
        """Paso 3: Rellenar el número de teléfono"""
        print("\n=== Ejecutando: Rellenar número de teléfono ===")
        self.page.fill_phone_number("+1 123 123 1234")
        print("✓ Número de teléfono configurado")
        time.sleep(2)
    
    def test_04_add_credit_card(self):
        """Paso 4: Agregar una tarjeta de crédito"""
        print("\n=== Ejecutando: Agregar tarjeta de crédito ===")
        self.page.add_credit_card("1234 5678 9012 3456", "123")
        print("✓ Tarjeta de crédito agregada")
        time.sleep(2)
    
    def test_05_set_message_to_driver(self):
        """Paso 5: Escribir un mensaje para el conductor"""
        print("\n=== Ejecutando: Escribir mensaje al conductor ===")
        self.page.set_message_to_driver("Llegar rápido, por favor")
        print("✓ Mensaje al conductor escrito")
        time.sleep(2)
    
    def test_06_request_blanket_and_tissues(self):
        """Paso 6: Pedir una manta y pañuelos"""
        print("\n=== Ejecutando: Solicitar manta y pañuelos ===")
        self.page.request_blanket_and_tissues()
        print("✓ Manta y pañuelos solicitados")
        time.sleep(2)
    
    def test_07_request_ice_creams(self):
        """Paso 7: Pedir 2 helados"""
        print("\n=== Ejecutando: Solicitar 2 helados ===")
        self.page.request_ice_creams(2)
        print("✓ 2 helados solicitados")
        time.sleep(2)
    
    def test_08_confirm_taxi_search(self):
        """Paso 8: Confirmar y activar modal para buscar taxi"""
        print("\n=== Ejecutando: Confirmar búsqueda de taxi ===")
        self.page.confirm_taxi_search()
        print("✓ Búsqueda de taxi confirmada")
        time.sleep(2)
    
    def test_09_wait_for_driver_info(self):
        """Paso 9 (Opcional): Esperar información del conductor"""
        print("\n=== Ejecutando: Esperar información del conductor ===")
        driver_name = self.page.wait_for_driver_info(timeout=30)
        assert driver_name is not None, "No se encontró la información del conductor"
        print(f"✓ Información del conductor encontrada: {driver_name}")
        time.sleep(2)
    
    def test_complete_taxi_booking_flow(self):
        """Prueba completa del flujo de pedido de taxi Comfort"""
        print("\n=== Ejecutando flujo completo ===")
        time.sleep(3)
        
        self.page.set_route("East 2nd Street, 601", "1300 1st St")
        self.page.select_comfort_tariff()
        self.page.fill_phone_number("+1 123 123 1234")
        self.page.add_credit_card("1234 5678 9012 3456", "123")
        self.page.set_message_to_driver("Llegar rápido, por favor")
        self.page.request_blanket_and_tissues()
        self.page.request_ice_creams(2)
        self.page.confirm_taxi_search()
        driver_name = self.page.wait_for_driver_info(timeout=30)
        assert driver_name is not None, "No se encontró la información del conductor"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
