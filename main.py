import os
from app import view

# Definir la ruta del directorio de logs 
log_dir = 'log'

# Crear las carpetas 'logs' y 'logs/collection' si no existen
os.makedirs(log_dir, exist_ok=True)

    
# Main function
def main():
    view.main()


# Main function call to run the program
if __name__ == '__main__':
    main()