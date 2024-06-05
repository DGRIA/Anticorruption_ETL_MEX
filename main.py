import config
from config import *
from src import data_download_unzip
from src.mongodb_utils import connect_to_mongodb, process_large_json
import time

logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)

'''
De cara a usar el codigo en Streamlit habria que trabajar en preguntar al usuario si desea 
descargar de nuevo el json, si lo desea extraer, generar csv, parquet, etc.
'''

if __name__ == '__main__':
    '''
    1. Descarga de datos
    2. Extracción de datos
    3. Insertar datos en MongoDB
    4. Exportar datos a CSV
    5. Exportar datos a Parquet
    
    Para levantar contenedor de MongoDB (y no tener que instalarlo en la máquina local, aunque puedes instalarlo):
    docker run --name mongo -p 27017:27017 -d mongo:latest
    
    Para levantar compose con MongoDB y Jupyter:
    docker-compose up -d --build
    
    # Para ejecutar Streamlit modificar el archivo Dockerfile y ponerlo igual que Fertilizantes (Levanta Streamlit y Jupyter)
    
    '''
    logger.info("Inicio de Ejecución")
    start = time.time()
    db = connect_to_mongodb()
    print("Conectado a MongoDB")
    # data_download_unzip.download_contrataciones_zip() # Tarda unos minutos
    logger.info("Tiempo de descarga: %s", time.time() - start)
    start_zip = time.time()
    # data_download_unzip.unzip() # Tarda unos minutos
    logger.info("Tiempo de extracción: %s", time.time() - start_zip)
    end = time.time()

    db = connect_to_mongodb()
    print("Conectado a MongoDB")
    print("Revisado la colección")
    process_large_json(
        config.path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON)  # Tarda mas de 20 minutos
    logger.info(f"Tiempo de ejecución: {end - start}")
    logger.info("Fin de Ejecución")
