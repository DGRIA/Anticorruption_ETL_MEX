import logging
import os

# Logging configuration
"""""
LEVELS: CRITICAL, ERROR, WARNING, INFO, DEBUG
Para capturar las excepciones en el log, se debe usar el siguiente código:
try:
    ...
except Exception as e:
    logger.exception("Error: %s", e)
"""


class LoggerConfig:
    def __init__(self):
        self.level = os.getenv('LOG_LEVEL', 'WARNING').upper()
        self.format = '[%(levelname)s] - %(asctime)s - %(name)s - %(funcName)s - %(filename)s:%(lineno)d -  %(message)s'
        self.datefmt = '%Y-%m-%d %H:%M:%S'
        self.filename = 'logs/main.log'
        self.log_path = os.path.join(os.getcwd(), "logs")

    def setup(self):
        log_formatter = logging.Formatter(self.format, datefmt=self.datefmt)
        root_logger = logging.getLogger("Contrataciones")
        root_logger.setLevel(self.level)

        file_handler = logging.FileHandler(self.filename)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(log_formatter)
        root_logger.addHandler(file_handler)

        # Add StreamHandler to print logs to terminal
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(log_formatter)
        root_logger.addHandler(stream_handler)


class PathConfig:
    def __init__(self):
        # Directorios
        self.data_path = os.path.join(os.getcwd(), "data")
        self.docs_path = os.path.join(os.getcwd(), "docs")
        self.log_path = os.path.join(os.getcwd(), "logs")
        self.src_path = os.path.join(os.getcwd(), "src")
        self.test_path = os.path.join(os.getcwd(), "test")

        # Archivos y direcciones
        self.contrataciones_url = "https://compranetinfo.hacienda.gob.mx/dabiertos/contrataciones_arr.json.zip"
        self.contrataciones_raw_path = os.path.join(os.getcwd(), "data/Raw/contrataciones_arr.json.zip")
        self.contrataciones_raw_unzip_path = os.path.join(os.getcwd(), "data/Raw/")
        self.contrataciones_processed_raw_path = os.path.join(os.getcwd(), "data/Processed/All_Tables_Raw/")
        self.contrataciones_processed_parquet_path = os.path.join(os.getcwd(), "data/Processed/parquet_files/")
        self.contrataciones_processed_cleaned_path = os.path.join(os.getcwd(), "data/Processed/Cleaned/")
        self.contrataciones_processed_cleaned_parquet_path = os.path.join(os.getcwd(),
                                                                          "data/Processed/Cleaned/parquet_files/")


# Definición de constantes
# MongoDB
DB_NAME = 'Contratos_EDCA'
COLLECTION_NAME = 'Contratos_EDCA_Bulk'
DB_URL = 'mongodb://localhost:27018/'
# JSON Files
CONTRATACIONES_JSON = 'contratacionesabiertas_bulk.json'

# Logger setup
logger_config = LoggerConfig()
logger_config.setup()
path_config = PathConfig()
