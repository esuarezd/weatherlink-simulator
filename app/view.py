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
        # Si hubo error, entra aquí
        print(f"[ERROR] No se pudo cargar la configuración: {e}")
        return  # Salimos de la función, nada más se ejecuta
    
    # Obtener nombre de la estación y ruta al archivo generado por WeatherLink
    station_config = config["station"]
    station_name = station_config["name"]
    file_path = station_config["file_path"]

    # Leer intervalo de archivo (en minutos) y convertir a segundos para el sleep
    archive_interval_min = station_config.get("archive_interval", 5)
    interval_sec = archive_interval_min * 60

    # Configuración de MQTT
    mqtt_config = config["mqtt"]
    
    client_mqtt = logic.mqtt_create_client(mqtt_config)

    print(f"[INFO] Iniciando publicación de datos para estación {station_name}")
    print(f"[INFO] Archivo fuente: {file_path}")
    print(f"[INFO] Intervalo de lectura: {archive_interval_min} minutos")
    
    
    while True:
        try:
            df = logic.read_download(file_path)
            data = logic.last_values(df)
            logic.mqtt_publish_data(mqtt_config, client_mqtt, data)
            print(f"[OK] Datos publicados: \n{data}")
        except Exception as e:
            print(f"[ERROR] {e}")
        time.sleep(interval_sec)
    