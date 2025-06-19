import logging
import time

from app import logic

# Definir la ruta del directorio de logs 
log_file = 'log/view.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

def load_config(config_path):
    
    try:
        return logic.load_config(config_path)
    except Exception as e:
        logging.error(f"[VIEW] No se pudo cargar la configuración: {e}")
        return  None

def read_weatherlink(file_path):
    try:
        return logic.read_weatherlink(file_path)
    except Exception as e:
        logging.error(f"[VIEW] Error al leer datos desde WeatherLink: {e}")
        return None

def publish_data(topic_prefix, client_mqtt, data):
    try:
        logic.mqtt_publish_data(topic_prefix, client_mqtt, data)
        logging.info(f"[VIEW] Datos publicados: \n{data}")
    except Exception as e:
        logging.error(f"[VIEW] Error al publicar datos vía MQTT: {e}")
        
def main():
    
    config = load_config(config_path="config.yaml")
    
    if not config:
        return
    
    # Obtener coniguraciones
    station_config = config["station"]
    mqtt_config = config["mqtt"]
    
    # Configuraciones de lectura para weatherlink
    station_name = station_config["name"]
    file_path = station_config["file_path"]
    archive_interval_min = station_config.get("archive_interval", 5)
    interval_sec = archive_interval_min * 60

    logging.info(f"[VIEW] Iniciando publicación de datos para estación {station_name}")
    logging.info(f"[VIEW] Archivo fuente: {file_path}")
    logging.info(f"[VIEW] Intervalo de lectura: {archive_interval_min} minutos")
    
    # Configuración de MQTT
    client_mqtt = logic.mqtt_create_client(mqtt_config["host"], mqtt_config["port"])
    
    while True:
        data = read_weatherlink(file_path)
        if data:
            publish_data(mqtt_config["topic_prefix"], client_mqtt, data)
        time.sleep(interval_sec)
    