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
import paho.mqtt.client as mqtt
import json
import logging

logger = logging.getLogger(__name__)

# Callback que se ejecuta cuando el cliente se conecta al broker. 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Conectado exitosamente al broker")
    else:
        logger.error(f"Error de conexión: código {rc}")

# Callback que se ejecuta si el cliente se desconecta.
def on_disconnect(client, userdata, rc):
    logger.warning(f"Desconectado. Código: {rc}")
            
def create_client(broker="localhost", port=1883):
    client = mqtt.Client()
    
    # Asignamos funciones de callback
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    
    # Configuramos reconexión automática si se pierde la conexión
    client.reconnect_delay_set(min_delay=1, max_delay=30)
    
    # 🔄 IMPORTANTE: inicia el hilo de red en segundo plano
    # Esto permite que se manejen conexiones, reconexiones y publicaciones sin bloquear el flujo principal
    client.loop_start()
    
    # Intentamos conectarnos por primera vez
    try:
        client.connect(broker, port, 60)
    except Exception as e:
        # Si falla, el cliente seguirá intentando reconectarse en segundo plano gracias a loop_start
        logger.error(f"Error al conectar al broker {broker}:{port} - {e}")
        raise ConnectionError(f"No se pudo conectar al broker MQTT {broker}:{port}") from e
        
    return client

def publish_data(data, client_mqtt, topic_prefix="weatherstation"):
    
    if not client_mqtt.is_connected():
        logger.warning("Cliente no conectado. Se espera que reconecte automáticamente...")
        return
    
    try:
        
        topic = f"{topic_prefix}/data"
        payload = json.dumps(data)
            
        result = client_mqtt.publish(topic, payload)
        result.wait_for_publish()
        
        if result.rc != mqtt.MQTT_ERR_SUCCESS:
            error_msg = mqtt.error_string(result.rc)
            logger.error(f"Publicación fallida: {error_msg}")
            raise RuntimeError(f"Error al publicar en MQTT: {error_msg}")
    
    except Exception as e:
        logger.error(f"Excepción durante la publicación: {e}")
        raise
        