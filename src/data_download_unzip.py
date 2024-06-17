from tqdm import tqdm
import urllib3
import requests
from zipfile import ZipFile
import os
import logging
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
    """
    Función para descargar el archivo zip de las contrataciones
    por partes.
    :param url: Url del archivo a descargar
    :param pb: Progreso de la descarga expresado en decimal
    :return: None
    """
    check_path(RAW_DATA_PATH)
    with requests.get(url, stream=False, verify=False) as response:
        response.raise_for_status()

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)

        with open(RAW_DATA_PATH, 'wb') as f:
            for chunk in response.iter_content(chunk_size=2048 * 2048):
                progress_bar.update(len(chunk))
                f.write(chunk)
                if pb is not None:
                    pb.progress((progress_bar.n / total_size_in_bytes) / 2,
                                f'Descargando archivo JSON de Compranet: '
                                f'{round(((progress_bar.n / total_size_in_bytes) / 2) * 100, 2)} %')
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            logger.error("ERROR, ha ocurrido un error al descargar el archivo")

        logger.info("Archivo descargado")


def unzip(zip_file_path=RAW_DATA_PATH, unzip_path=UNZIP_DATA_PATH, pb=None, progress=None):
    """
    Función para extraer por partes (chunks) el archivo zip descargado
    :param zip_file_path: Ruta del archivo zip
    :param unzip_path: Ruta de la carpeta donde se extraerá el archivo
    :param pb: Barra de progreso (Streamlit
    :param progress: Progreso de la extracción expresado en decimal
    :return: None
    """
    if os.path.exists(zip_file_path):
        with ZipFile(zip_file_path, 'r') as zip_file:
            file = zip_file.namelist()[0]
            file_info = zip_file.getinfo(file)

            with tqdm(total=file_info.file_size, desc="Extrayendo JSON", unit="B", unit_scale=True) as pbar:
                with zip_file.open(file) as zf, open(os.path.join(unzip_path, file), 'wb') as fout:
                    for chunk in iter(lambda: zf.read(2048 * 2048), b''):
                        fout.write(chunk)
                        pbar.update(len(chunk))
                        if pb is not None and progress is None:
                            pb.progress((pbar.n / file_info.file_size),
                                        f'Extrayendo Documentos JSON del archivo adjuntado: '
                                        f'{round((pbar.n / file_info.file_size) * 100, 2)} %')
                        if pb is not None and progress is not None:
                            pb.progress(progress + (pbar.n / file_info.file_size) / 2,
                                        f'Extrayendo Documentos JSON del archivo descargado: {round((progress + (pbar.n / file_info.file_size) / 2) * 100, 2)} %')

        logger.info("Extracción completada con éxito.")
        logger.info(f"Archivo extraído: {file}")
    else:
        logger.error(
            f"Error: No se encontró el archivo '{zip_file_path}'. Asegúrate de que la ruta y el nombre del archivo "
            f"sean correctos.")


def check_path(path):
    """
    Función para verificar si la ruta del archivo existe
    :param path: Ruta del archivo
    :return: None
    """
    if os.path.exists(path):
        logger.info("El archivo ya existe")
    else:
        logger.info("El archivo no existe")


def check_files_exist(file_list, directory):
    """
    Esta función comprueba si todos los archivos en una lista existen en un directorio específico.
    :param directory: Directorio donde se encuentran los archivos.
    :param file_list: Lista de archivos a comprobar.
    :return: True si todos los archivos existen, False en caso contrario.
    """
    for filename in file_list:
        if not os.path.exists(os.path.join(directory, filename)):
            print(f"Archivo {filename} no encontrado en {directory}")
            return False

    return True
