# WeatherLink MQTT Publisher

Este proyecto permite leer datos generados por una estación meteorológica Davis desde un archivo plano exportado por WeatherLink, y publicarlos en un broker MQTT para su posterior uso en aplicaciones IoT o repositorio de datos.

---

## Requisitos

- Python 3.8 o superior
- Acceso al archivo `.txt` generado por WeatherLink

---

## Instalación

1. **Crea un entorno de trabajo y prepara el proyecto:**
   - **Clona este repositorio:**

     ```bash
     git clone https://github.com/tu_usuario/weatherlink-mqtt.git
     cd weatherlink-mqtt
     ```

   - **Crea y activa un entorno virtual:**

     ```bash
     python -m venv .venv
     ```

     - En Windows:
       ```bash
       .venv\Scripts\activate
       ```
     - En macOS/Linux:
       ```bash
       source .venv/bin/activate
       ```

   - **Instala las dependencias:**

     ```bash
     pip install -r requirements.txt
     ```

---

## Ejecución

1. Configura el archivo `config.yaml` con la ruta al archivo de WeatherLink y la información del broker MQTT.

2. Ejecuta la aplicación:

   ```bash
   python main.py
   ```

Los logs se almacenarán en la carpeta `log/`, con un archivo para cada módulo (`view.log`, `logic.log`, `mqtt_client.log`, etc.).

---

## Licencia

Este proyecto está licenciado bajo los términos de la [Licencia Apache 2.0](LICENSE).

---

## Autor

Edison Suárez Ducón

---

## Contacto

Para dudas o contribuciones, por favor abre un issue en el repositorio o contáctame directamente.
