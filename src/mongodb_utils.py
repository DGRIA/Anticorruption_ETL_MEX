import logging
from decimal import Decimal

import ijson
from bson import Decimal128
from pymongo import MongoClient
from tqdm import tqdm

from config import DB_NAME, DB_URL, COLLECTION_NAME

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Contrataciones")


def connect_to_mongodb():
    """Conexión a la base de datos MongoDB"""
    try:
        logger.info("Conectando a la base de datos MongoDB...")
        client = MongoClient(DB_URL, connectTimeoutMS=5000)
        db = client[DB_NAME]
        logger.info("Conexión exitosa a la base de datos.")
        return db
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None


def convert_decimal_to_decimal128(item):
    if isinstance(item, list):
        for i in range(len(item)):
            item[i] = convert_decimal_to_decimal128(item[i])
    elif isinstance(item, dict):
        for key, value in list(item.items()):  # Use list to avoid 'dictionary changed size during iteration' error
            if key.startswith('$'):
                new_key = key.replace('$', '')  # Remove the dollar sign
                item[new_key] = convert_decimal_to_decimal128(value)
                del item[key]  # Remove the old key
            else:
                item[key] = convert_decimal_to_decimal128(value)
    elif isinstance(item, Decimal):
        return Decimal128(str(item))
    return item


def insert_data_to_mongodb(data):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    for i in range(len(data)):
        data[i] = convert_decimal_to_decimal128(data[i])

    if isinstance(data, list):
        collection.insert_many(data)
    else:
        collection.insert_one(data)


def process_large_json(file_path, max_lines=5000):
    client = MongoClient(DB_URL)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    logger.info(f"Inserting data into collection '{COLLECTION_NAME}' in database '{DB_NAME}'...")

    with open(file_path, 'rb') as file:
        objects = ijson.items(file, 'item')
        objects = tqdm(objects, desc="Processing JSON file", unit=" record", dynamic_ncols=True, leave=True,
                       smoothing=0.05)
        chunk = []
        for i, obj in enumerate(objects):
            chunk.append(obj)
            if (i + 1) % max_lines == 0:
                insert_data_to_mongodb(chunk)
                chunk = []
        if chunk:  # insert remaining records in the chunk
            insert_data_to_mongodb(chunk)
