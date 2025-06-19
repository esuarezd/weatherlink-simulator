import pandas as pd
import logging
from io import StringIO

# Definir la ruta del directorio de logs 
log_file = 'log/reader_weatherlink.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

def read_download(file_path):
    try:
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 4:
            raise ValueError("El archivo no contiene suficientes líneas de encabezado y datos.")

        header_line1 = lines[0]
        header_line2 = lines[1]
        data_lines = lines[3:]  # omitir línea de separación

        data_text = "".join(data_lines)

        colspecs = [ 
            (0, 8), (8, 16), (16, 23), (23, 30), (30, 36), (36, 43), (43, 49), (49, 55), (55, 62), (62, 68),
            (68, 75), (75, 80), (80, 87), (87, 94), (94, 101), (101, 108), (108, 116), (116, 122), (122, 128), (128, 135),
            (135, 143), (143, 152), (152, 158), (158, 165), (165, 171), (171, 179), (179, 187), (187, 193), (193, 200), (200, 207), 
            (207, 214), (214, 220), (220, 232), (232, 236), (236, 242), (242, 248), (248, 256), (256, 264)
        ]

        column_names = []
        for start, end in colspecs:
            p1 = header_line1[start:end].strip()
            p2 = header_line2[start:end].strip()
            name = (p1 + p2).strip()
            name.replace(" ", "_")
            column_names.append(name)

        df = pd.read_fwf(StringIO(data_text), colspecs=colspecs)
        df.columns = column_names
        return df
    
    except FileNotFoundError:
        logging.error(f"[READER] El archivo no fue encontrado: {file_path}")
        raise
    except ValueError as ve:
        logging.error(f"[READER] Valor inválido en el archivo '{file_path}': {ve}")
        raise
    except IndexError:
        logging.error(f"[READER] El archivo tiene un formato inválido (faltan líneas): {file_path}")
        raise
    except Exception as e:
        logging.error(f"[READER] Error inesperado al leer el archivo '{file_path}': {e}")
        raise

def last_values(df):
    try:
        latest_row = df.iloc[-1]
        return latest_row.to_dict()
    except IndexError:
        logging.error("[READER] El DataFrame está vacío, no se pueden obtener valores.")
        raise
    except Exception as e:
        logging.error(f"[READER] Error inesperado al obtener la última fila del DataFrame: {e}")
        raise