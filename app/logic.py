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

    
def read_download(file_path):
    df = reader_weatherlink.read_download(file_path)
    return df

def last_values(df):
    data = reader_weatherlink.last_values(df)
    return data

def mqtt_create_client(mqtt_config):
    broker = mqtt_config["host"]
    port = mqtt_config["port"]
    client = mqtt_client.create_client(broker, port)
    return (client)

def mqtt_publish_data(mqtt_config, client_mqtt, data):
    topic_prefix = mqtt_config["topic_prefix"]
    mqtt_client.publish_data(topic_prefix, client_mqtt, data)