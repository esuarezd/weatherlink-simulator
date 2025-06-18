import time

from app import logic

def load_config(config_path):
    config = logic.load_config(config_path)
    return config

def main():
    try:
        # Solo este bloque se intenta ejecutar
        config = load_config(config_path="config.yaml")
    except Exception as e:
        print(f"[ERROR] No se pudo cargar la configuración: {e}")
        return  # Sale de main y finaliza app
    
    # Obtener coniguraciones
    station_config = config["station"]
    mqtt_config = config["mqtt"]
    
    # Configuraciones de lectura para weatherlink
    station_name = station_config["name"]
    file_path = station_config["file_path"]
    archive_interval_min = station_config.get("archive_interval", 5)
    interval_sec = archive_interval_min * 60

    print(f"[INFO] Iniciando publicación de datos para estación {station_name}")
    print(f"[INFO] Archivo fuente: {file_path}")
    print(f"[INFO] Intervalo de lectura: {archive_interval_min} minutos")
    
    # Configuración de MQTT
    client_mqtt = logic.mqtt_create_client(mqtt_config["host"], mqtt_config["port"])
    
    while True:
        try:
            data = logic.read_weatherlink(file_path)
            logic.mqtt_publish_data(mqtt_config["topic_prefix"], client_mqtt, data)
            print(f"[OK] Datos publicados: \n{data}")
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(interval_sec)
    