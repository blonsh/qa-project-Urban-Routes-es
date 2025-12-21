"""
Script para inspeccionar la página Urban Routes y encontrar los selectores correctos
Este script abre la página y muestra información útil sobre los elementos disponibles
"""
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from data import BASE_URL

print("=== Script de Inspección de Página Urban Routes ===\n")

# Configurar Chrome
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=chrome_options)
driver.maximize_window()

print(f"Abriendo URL: {BASE_URL}")
driver.get(BASE_URL)

print("\nEsperando 10 segundos para que la página cargue completamente...")
time.sleep(10)

print("\n" + "="*60)
print("INFORMACIÓN DE LA PÁGINA")
print("="*60)

# Obtener el título de la página
try:
    print(f"Título de la página: {driver.title}")
except:
    print("No se pudo obtener el título")

# Buscar todos los inputs
print("\n--- INPUTS ENCONTRADOS ---")
inputs = driver.find_elements(By.TAG_NAME, "input")
print(f"Total de inputs: {len(inputs)}\n")

for i, inp in enumerate(inputs, 1):
    inp_id = inp.get_attribute('id') or 'sin ID'
    inp_name = inp.get_attribute('name') or 'sin name'
    inp_placeholder = inp.get_attribute('placeholder') or 'sin placeholder'
    inp_type = inp.get_attribute('type') or 'sin type'
    inp_class = inp.get_attribute('class') or 'sin class'
    
    print(f"Input {i}:")
    print(f"  ID: {inp_id}")
    print(f"  Name: {inp_name}")
    print(f"  Placeholder: {inp_placeholder}")
    print(f"  Type: {inp_type}")
    print(f"  Class: {inp_class[:50]}...")  # Limitar tamaño
    print()

# Buscar todos los botones
print("\n--- BOTONES ENCONTRADOS ---")
buttons = driver.find_elements(By.TAG_NAME, "button")
print(f"Total de botones: {len(buttons)}\n")

for i, btn in enumerate(buttons[:10], 1):  # Mostrar solo los primeros 10
    btn_id = btn.get_attribute('id') or 'sin ID'
    btn_text = btn.text[:30] or 'sin texto'
    btn_class = btn.get_attribute('class') or 'sin class'
    
    print(f"Botón {i}:")
    print(f"  ID: {btn_id}")
    print(f"  Texto: {btn_text}")
    print(f"  Class: {btn_class[:50]}...")
    print()

# Buscar elementos con texto "Comfort"
print("\n--- ELEMENTOS QUE CONTIENEN 'Comfort' ---")
comfort_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Comfort')]")
print(f"Total de elementos con 'Comfort': {len(comfort_elements)}\n")

for i, elem in enumerate(comfort_elements[:5], 1):  # Mostrar solo los primeros 5
    elem_tag = elem.tag_name
    elem_text = elem.text[:50] or 'sin texto'
    elem_id = elem.get_attribute('id') or 'sin ID'
    elem_class = elem.get_attribute('class') or 'sin class'
    
    print(f"Elemento {i}:")
    print(f"  Tag: {elem_tag}")
    print(f"  ID: {elem_id}")
    print(f"  Class: {elem_class[:50]}...")
    print(f"  Texto: {elem_text}")
    print()

# Buscar divs con clases comunes
print("\n--- DIVS CON CLASES INTERESANTES ---")
interesting_classes = ['pac-item', 'tariff', 'button', 'input', 'field']
for class_name in interesting_classes:
    try:
        divs = driver.find_elements(By.XPATH, f"//*[contains(@class, '{class_name}')]")
        if divs:
            print(f"Elementos con clase '{class_name}': {len(divs)}")
            for i, div in enumerate(divs[:3], 1):  # Mostrar solo los primeros 3
                div_id = div.get_attribute('id') or 'sin ID'
                div_text = div.text[:30] or 'sin texto'
                print(f"  [{i}] ID: {div_id}, Texto: {div_text}")
            print()
    except:
        pass

print("\n" + "="*60)
print("EL NAVEGADOR PERMANECERÁ ABIERTO POR 5 MINUTOS")
print("Puedes usar F12 para inspeccionar elementos manualmente")
print("="*60)

# Mantener el navegador abierto
try:
    time.sleep(300)  # 5 minutos
except KeyboardInterrupt:
    print("\n\nCerrando navegador...")

driver.quit()
print("\nNavegador cerrado.")

