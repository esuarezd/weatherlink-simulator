import os

# Definir la ruta del directorio de logs 
log_dir = 'log'

# Crear las carpetas log si no existe
os.makedirs(log_dir, exist_ok=True)

from app import view
    
# Main function
def main():
    view.main()


# Main function call to run the program
if __name__ == '__main__':
    main()