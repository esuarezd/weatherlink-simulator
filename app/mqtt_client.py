import paho.mqtt.client as mqtt
import json
import logging

# Definir la ruta del directorio de logs 
log_file = 'log/mqtt_client.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

# Callback que se ejecuta cuando el cliente se conecta al broker. 
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("[MQTT] Conectado exitosamente al broker")
    else:
        logging.error(f"[MQTT] Error de conexión: código {rc}")

# Callback que se ejecuta si el cliente se desconecta.
def on_disconnect(client, userdata, rc):
    logging.warning(f"[MQTT] Desconectado. Código: {rc}")
            
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
        logging.error(f"[MQTT] Error al conectar al broker {broker}:{port} - {e}")
        raise ConnectionError(f"No se pudo conectar al broker MQTT {broker}:{port}") from e
        
    return client

def publish_data(topic_prefix, client, data):
    
    if not client.is_connected():
        logging.warning("[MQTT] Cliente no conectado. Se espera que reconecte automáticamente...")
        return
    
    topic = f"{topic_prefix}/data"
    payload = json.dumps(data)
        
    result = client.publish(topic, payload)
    result.wait_for_publish()
    
    if result.rc != mqtt.MQTT_ERR_SUCCESS:
        logging.error(f"[MQTT] Publicación fallida: {mqtt.error_string(result.rc)}")