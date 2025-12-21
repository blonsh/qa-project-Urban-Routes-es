# Proyecto de Automatización: **Solicitud de Taxi Comfort en Urban Routes**
![image](https://github.com/user-attachments/assets/a682bd95-b471-47ff-b172-db9a418a01f3)

## 🚖 Descripción del Proyecto

Este proyecto implementa **pruebas automatizadas end-to-end** para la aplicación **Urban Routes**, enfocada en la solicitud de taxis tipo *Comfort*. 

Las pruebas simulan el flujo completo de reserva del servicio, validando funcionalidades clave como:

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

** [ ] Configurar dirección (origen y destino)
** [ ] Seleccionar tarifa Comfort
** [ ] Rellenar número de teléfono
** [ ] Agregar tarjeta de crédito (con manejo del CVV y pérdida de foco)
** [ ] Escribir mensaje al conductor
** [ ] Pedir manta y pañuelos
** [ ] Pedir 2 helados
** [ ] Aparece modal para buscar taxi
** [ ] (Opcional) Esperar información del conductor

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
![image](https://github.com/user-attachments/assets/09c36110-0e94-453d-ae46-e5b4cb562fb8)

##QA Blanca Sánchez



