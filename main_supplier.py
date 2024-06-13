import pandas

import config
from config import *
from src.data_download_unzip import download_contrataciones_zip, unzip
from src.extraction_mongodb import *
from src.mongodb_utils import connect_to_mongodb, process_large_json
import time
import streamlit as st
import subprocess
import logging
import config
import sys
import os
import shutil

if __name__ == '__main__':
    '''
    De cara a usar el codigo en Streamlit habria que trabajar en preguntar al usuario si desea 
    descargar de nuevo el json, si lo desea extraer, generar csv_files, parquet, etc.
    '''

    ''' 
        1. Descarga de datos
        2. Extracción de datos
        3. Insertar datos en MongoDB
        4. Exportar datos a CSV y parquet, clean de algunos
            4.1 Exportar datos de tabla 'Participantes Proveedores'
            4.2 Exportar datos de tabla 'Licitacion'
            4.3 Exportar datos de tabla 'Asignacion'
            4.4 Exportar datos de tabla 'Comprador'
            4.5 Exportar datos de tabla 'Documentos Tender'
            4.6 Exportar datos de tabla 'Items Adq'
            4.7 Exportar datos de tabla 'Items Tender'
            4.8 Opción de todos

        5. Descarga de datos (Comprobar que los archivos anteriores se han generado)
           5.1 Descargas de csv_files de 'Participantes Proveedores'
           5.2 Descargas de csv_files de 'Licitacion'
           5.3 Descargas de csv_files de 'Asignacion'
           5.4 Descargas de csv_files de 'Comprador'
           5.5 Descargas de csv_files de 'Documentos Tender'
           5.6 Descargas de csv_files de 'Items Adq'
           5.7 Descargas de csv_files de 'Items Tender'
           5.8 Opción de todos



        Para levantar contenedor de MongoDB (y no tener que instalarlo en la máquina local, aunque puedes instalarlo):
        docker run --name mongo -p 27017:27017 -d mongo:latest

        Para levantar compose con MongoDB y Jupyter:
        docker-compose up -d --build

        logger.info("Inicio de Ejecución")
        start = time.time()
        db = connect_to_mongodb()
        print("Conectado a MongoDB")
        # Descarga de datos
        # data_download_unzip.download_contrataciones_zip() # Tarda unos minutos
        logger.info("Tiempo de descarga: %s", time.time() - start)
        start_zip = time.time()
        # Descompresión de datos
        # data_download_unzip.unzip() # Tarda unos minutos
        logger.info("Tiempo de extracción: %s", time.time() - start_zip)
        end = time.time()

        db = connect_to_mongodb()
        print("Conectado a MongoDB")
        print("Revisado la colección")
        # Insertar datos en MongoDB -> Aunque mejor hacerlo manual directamente importando en mongodb
        process_large_json(
            config.path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON)  # Tarda mas de 20 minutos
        logger.info(f"Tiempo de ejecución: {end - start}")
        logger.info("Fin de Ejecución")
    '''
    start = time.time()

    # Conexión a MongoDB
    # # Conexión a MongoDB
    db = connect_to_mongodb()
    if db is not None:
        # Extracción de datos de Mongo y generación del archivo CSV
        # extract_participantes_proveedores(db)
        extract_licitacion(db)

        # extract_asignacion(db)
        # extract_comprador(db)
        # extract_documentos_tender(db)
        # extract_item_adq(db)
        # extract_item_tender(db)

        # end = time.time()
        # logger.info(f"Tiempo de ejecución: {end - start}")
        # logger.info("Fin de Ejecución")
    # print(f"Tiempo de ejecución: {time.time() - start} segundos.")
