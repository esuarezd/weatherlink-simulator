# Copyright 2025 Edison Suárez Ducón
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import time
import logging

logger = logging.getLogger(__name__)

from app import logic

def load_config(config_path):
    
    try:
        return logic.load_config(config_path)
    except Exception as e:
        logger.error(f"No se pudo cargar la configuración: {e}")
        return  None

def create_client(broker, port):
    try:
        return logic.mqtt_create_client(broker, port)
    except Exception as e:
        logger.error(f"Error al crear cliente al broker {broker}: {e}")

def read_weatherlink(file_path):
    try:
        return logic.read_weatherlink(file_path)
    except Exception as e:
        logger.error(f"Error al leer datos desde WeatherLink: {e}")
        return None

def build_epoch_timestamp(date_str, time_str, timezone_str):
    try:
        return logic.build_epoch_timestamp(date_str, time_str, timezone_str)
    except Exception as e:
        logger.error(f"Error al crear estampa de tiempo: {e}")
    
def publish_data(topic_prefix, client_mqtt, data):
    try:
        logic.mqtt_publish_data(topic_prefix, client_mqtt, data)
        logger.info(f"Datos publicados: \n{data}")
    except Exception as e:
        logger.error(f"Error al publicar datos vía MQTT: {e}")
        
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

    logger.info(f"Iniciando publicación de datos para estación {station_name}")
    logger.info(f"Archivo fuente: {file_path}")
    logger.info(f"Intervalo de lectura: {archive_interval_min} minutos")
    
    # Configuración de MQTT
    host = mqtt_config.get("host")
    port = mqtt_config.get("port")
    topic_prefix = mqtt_config.get("topic_prefix")
    client_mqtt = create_client(host, port)
    last_timestamp = 0
    
    while True:
        data = read_weatherlink(file_path)
        if data:
            date_str = data.get("Date")
            time_str = data.get("Time")
            timezone_str = station_config.get("timezone")
            
            timestamp = build_epoch_timestamp(date_str, time_str, timezone_str)
            
            if timestamp == last_timestamp:
                logger.info(f"No se publica. Timestamp repetido: {timestamp}")
            else:
                data["timestamp"] = timestamp
                publish_data(topic_prefix, client_mqtt, data)
                last_timestamp = timestamp
        
        time.sleep(interval_sec)
    