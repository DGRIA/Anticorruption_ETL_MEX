import config
import logging
from src import data_download_unzip
import time
import pandas as pd
from pymongo import MongoClient
from src.extraction_mongodb import connect_to_mongodb, extract_participantes_proveedores

logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)

if __name__ == '__main__':
    logger.info("Inicio de Ejecución")
    start = time.time()
    data_download_unzip.download_contrataciones_zip()
    logger.info("Tiempo de descarga: %s", time.time() - start)
    start_zip = time.time()
    data_download_unzip.unzip()
    logger.info("Tiempo de extracción: %s", time.time() - start_zip)
    end = time.time()
    logger.info(f"Tiempo de ejecución: {end - start}")
    logger.info("Fin de Ejecución")












