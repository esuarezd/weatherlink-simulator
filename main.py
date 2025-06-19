import logging
import os

# Definir la ruta del directorio de logs 
log_dir = 'log'

# Crear las carpetas log si no existe
os.makedirs(log_dir, exist_ok=True)

# Definir la ruta del directorio de logs 
log_file = 'log/app.log'

# Configurar el sistema de logging
logging.basicConfig(
    level=logging.INFO,  # Nivel de severidad (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",  # Formato del mensaje
    handlers=[
        logging.StreamHandler(),  # Mostrar en la terminal
        logging.FileHandler(log_file, mode="a")  # Registrar en un archivo
    ]
)

from app import view
    
# Main function
def main():
    view.main()


# Main function call to run the program
if __name__ == '__main__':
    main()