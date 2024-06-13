from tqdm import tqdm
import urllib3
import requests
from zipfile import ZipFile
import os
import logging
import sys

# Save the original working directory
#
# current_file_path = os.path.abspath(__file__)
#
# # Get the parent directory of the current file
# parent_dir = os.path.dirname(current_file_path)
#
# # Get the base directory of the repository
# base_dir = os.path.dirname(parent_dir)
#
# config_path = os.path.join(base_dir, 'config.py')
#
# # Add the base directory to the system path
# sys.path.append(base_dir)

# Now you can import the config module
from config import *

# Deshabilitar los warnings de certificados SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuración del logger
logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)

# Definición de las rutas de los archivos
URL_CONTRATACIONES = CONTRATACIONES_URL
RAW_DATA_PATH = path_config.contrataciones_raw_path
UNZIP_DATA_PATH = path_config.contrataciones_raw_unzip_path


def download_contrataciones_zip(url=URL_CONTRATACIONES, pb=None):
    check_path(RAW_DATA_PATH)
    response = requests.get(url, stream=True, verify=False)
    response.raise_for_status()

    total_size_in_bytes = int(response.headers.get('content-length', 0))
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

    with open(RAW_DATA_PATH, 'wb') as f:
        for chunk in response.iter_content(chunk_size=2048 * 2048):
            progress_bar.update(len(chunk))
            f.write(chunk)
            if pb is not None:
                pb.progress((progress_bar.n / total_size_in_bytes) / 2,
                            f'Descargando archivo JSON de Compranet...')
    progress_bar.close()

    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        logger.error("ERROR, ha ocurrido un error al descargar el archivo")

    logger.info("Archivo descargado")


def unzip(zip_file_path=RAW_DATA_PATH, unzip_path=UNZIP_DATA_PATH, pb=None):
    if os.path.exists(zip_file_path):
        with ZipFile(zip_file_path, 'r') as zip_file:
            file = zip_file.namelist()[0]
            file_info = zip_file.getinfo(file)

            with tqdm(total=file_info.file_size, desc="Extrayendo JSON", unit="B", unit_scale=True) as pbar:
                with zip_file.open(file) as zf, open(os.path.join(unzip_path, file), 'wb') as fout:
                    for chunk in iter(lambda: zf.read(2048 * 2048), b''):
                        fout.write(chunk)
                        pbar.update(len(chunk))
                        if pb is not None:
                            pb.progress(0.5 + (pbar.n / file_info.file_size) / 2,
                                        f'Extrayendo Documentos JSON del archivo descargado...')

        logger.info("Extracción completada con éxito.")
        logger.info(f"Archivo extraído: {file}")
    else:
        logger.error(
            f"Error: No se encontró el archivo '{zip_file_path}'. Asegúrate de que la ruta y el nombre del archivo "
            f"sean correctos.")


def check_path(path):
    if os.path.exists(path):
        logger.info("El archivo ya existe")
    else:
        logger.info("El archivo no existe")
