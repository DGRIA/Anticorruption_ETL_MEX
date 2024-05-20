import os
import logging
import sys
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


@pytest.fixture(autouse=True)
def setup_logger():
    import config
    logger = logging.getLogger("Contrataciones")
    logger.setLevel(logging.INFO)
    yield logger


def test_data_path(setup_logger):
    from config import path_config
    setup_logger.info("Ejecutando test de directorio de datos.")
    assert os.path.exists(path_config.data_path)
    assert os.path.isdir(path_config.data_path)


def test_docs_path(setup_logger):
    from config import path_config
    setup_logger.info("Ejecutando test de directorio de documentación.")
    assert os.path.exists(path_config.docs_path)
    assert os.path.isdir(path_config.docs_path)


def test_log_file(setup_logger):
    from config import logger_config
    setup_logger.info("Ejecutando test de archivo de logs.")
    assert os.path.exists(logger_config.log_path)
    assert os.path.isdir(logger_config.log_path)


def test_src_path(setup_logger):
    from config import path_config
    setup_logger.info("Ejecutando test de directorio de código fuente.")
    assert os.path.exists(path_config.src_path)
    assert os.path.isdir(path_config.src_path)
