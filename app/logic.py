import yaml
import os

from app import reader_weatherlink
from app import mqtt_client

def load_config(config_path="config.yaml"):
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"El archivo de configuración no se encontró en la ruta: {config_path}")

    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise ValueError(f"Error al parsear el archivo YAML: {e}")

def weatherlink_read_download(file_path):
    data_frame = reader_weatherlink.read_download(file_path)
    return data_frame

def weatherlink_last_values(data_frame):
    data = reader_weatherlink.last_values(data_frame)
    return data

def read_weatherlink(file_path):
    data_frame = weatherlink_read_download(file_path)
    data = weatherlink_last_values(data_frame)
    return data
    
def mqtt_create_client(broker, port):
    client = mqtt_client.create_client(broker, port)
    return (client)

def mqtt_publish_data(topic_prefix, client_mqtt, data):
    mqtt_client.publish_data(topic_prefix, client_mqtt, data)