# Proyecto de Automatización: **Solicitud de Taxi Comfort en Urban Routes**

## 🚖 Descripción del Proyecto

Este proyecto implementa **pruebas automatizadas end-to-end** para la aplicación **Urban Routes**, enfocada en la solicitud de taxis tipo *Comfort*. Las pruebas simulan el flujo completo de reserva del servicio, validando funcionalidades clave como:

- Selección de origen y destino
- Elección de tarifa Comfort
- Validación de teléfono vía SMS
- Selección de método de pago
- Mensajes al conductor
- Servicios adicionales (mantas, helados, pañuelos)
- Confirmación de viaje
- Visualización de datos clave: nombre del conductor, placas del vehículo, tiempo estimado de llegada

---

## Lista de comprobación automatizada

- [x] Establecer URL del servidor
- [x] Seleccionar ubicación inicial y destino
- [x] Elegir tarifa **Comfort**
- [x] Ingresar número telefónico para validación
- [x] Agregar tarjeta de crédito como método de pago
- [x] Escribir un mensaje al conductor
- [x] Solicitar manta y pañuelos
- [x] Pedir **2 helados**
- [x] Confirmar y activar modal de “Buscando taxi…”

---

## Tecnologías Utilizadas

| Herramienta | Descripción |
|-------------|-------------|
| **Python** | Lenguaje principal del proyecto |
| **PyCharm** | IDE especializado en desarrollo con Python |
| **Selenium** | Automatización de pruebas en navegador |
| **Pytest** | Framework de testing para ejecución y organización de pruebas |
| **Git Bash** | CLI para uso de Git en Windows |
| **GitHub** | Repositorio para versionado y colaboración del código |

---

## Instrucciones de Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/JessicaOchoaG/qa-project-Urban-Routes-es.git
   ```

2. Acceder al directorio del proyecto:
   ```bash
   cd qa-project-Urban-Routes-es
   ```

3. Instalar dependencias necesarias:
   ```bash
   pip install selenium
   pip install pytest
   ```

---

## Ejecución de Pruebas

Para correr las pruebas, utiliza el siguiente comando desde la terminal:

```bash
  pytest -v
```

QA Blanca Sánchez



