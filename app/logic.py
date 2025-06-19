import yaml
import os
import logging

logger = logging.getLogger(__name__)

from app import reader_weatherlink
from app import mqtt_client

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        logger.error(f"Archivo de configuración no encontrado: {config_path}")
        raise FileNotFoundError(f"El archivo de configuración no se encontró en la ruta: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
            logger.info("Configuración cargada exitosamente.")
            return config
    except yaml.YAMLError as e:
        logger.error(f"Error al parsear el archivo YAML: {e}")
        raise ValueError(f"Error al parsear el archivo YAML: {e}")

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
        logger.error(f"Error interno al leer Weatherlink: {e}")
        raise
    
def mqtt_create_client(broker, port):
    client = mqtt_client.create_client(broker, port)
    return client

def mqtt_publish_data(topic_prefix, client_mqtt, data):
    mqtt_client.publish_data(topic_prefix, client_mqtt, data)