import logging
import yaml
import os

from app import reader_weatherlink
from app import mqtt_client

# Definir la ruta del directorio de logs 
log_file = 'log/logic.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        logging.error(f"[LOGIC] Archivo de configuración no encontrado: {config_path}")
        raise FileNotFoundError(f"[LOGIC] El archivo de configuración no se encontró en la ruta: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logging.info("[LOGIC] Configuración cargada exitosamente.")
            return config
    except yaml.YAMLError as e:
        logging.error(f"[LOGIC] Error al parsear el archivo YAML: {e}")
        raise ValueError(f"[LOGIC] Error al parsear el archivo YAML: {e}")

def weatherlink_read_download(file_path):
    data_frame = reader_weatherlink.read_download(file_path)
    return data_frame

def weatherlink_last_values(data_frame):
    data = reader_weatherlink.last_values(data_frame)
    return data

def read_weatherlink(file_path):
    try:
        data_frame = weatherlink_read_download(file_path)
        data = weatherlink_last_values(data_frame)
        return data
    except Exception as e:
        logging.error(f"[LOGIC] Error interno al leer Weatherlink: {e}")
        raise
    
def mqtt_create_client(broker, port):
    client = mqtt_client.create_client(broker, port)
    return client

def mqtt_publish_data(topic_prefix, client_mqtt, data):
    mqtt_client.publish_data(topic_prefix, client_mqtt, data)