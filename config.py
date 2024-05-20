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


# TODO Ver si dejar el nombre de la función

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
        self.data_path = os.path.join(os.getcwd(), "data")
        self.docs_path = os.path.join(os.getcwd(), "docs")
        self.log_path = os.path.join(os.getcwd(), "logs")
        self.src_path = os.path.join(os.getcwd(), "src")
        self.test_path = os.path.join(os.getcwd(), "test")


logger_config = LoggerConfig()
logger_config.setup()
path_config = PathConfig()
