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
import yaml
import os
import logging

logger = logging.getLogger(__name__)

from app import reader_weatherlink
from app import mqtt_client
from datetime import datetime
from zoneinfo import ZoneInfo

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

def build_epoch_timestamp(date_str="18/06/25", time_str="4:10p", timezone_str="UTC"):
    try:
        if not date_str or not time_str:
            raise ValueError("Faltan datos de fecha u hora")

        # Convertir "12:45p" a formato 24h: "12:45 PM"
        if time_str.endswith('a'):
            time_fmt = time_str[:-1] + " AM"
        elif time_str.endswith('p'):
            time_fmt = time_str[:-1] + " PM"
        else:
            raise ValueError(f"Formato de hora inválido: {time_str}")

        # Construir datetime
        full_str = f"{date_str} {time_fmt}"  # ej: "18/06/25 12:45 PM"
        dt = datetime.strptime(full_str, "%d/%m/%y %I:%M %p")

        # Asignar zona horaria
        tz = ZoneInfo(timezone_str)
        dt = dt.replace(tzinfo=tz)

        # Convertir a epoch (segundos desde 1970 UTC)
        return int(dt.timestamp())

    except Exception as e:
        logger.error(f"Error construyendo timestamp: {e}")
        return None

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