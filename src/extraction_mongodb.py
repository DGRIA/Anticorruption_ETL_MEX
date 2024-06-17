import pandas as pd
from config import DB_NAME, DB_URL, COLLECTION_NAME, path_config
from pymongo import MongoClient
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Contrataciones")

mongo_logger = logging.getLogger("pymongo")
mongo_logger.setLevel(logging.WARNING)


def clean_licitacion(df_licitacion):
    """
    Limpia los datos de licitación
    :param df_licitacion: DataFrame de licitación
    :return: DataFrame de licitación limpio
    """
    df_licitacion['award_end_date'] = pd.to_datetime(df_licitacion['award_end_date'], errors='coerce')
    sorted_df = df_licitacion.sort_values(['cve_expediente', 'award_end_date'], ascending=[True, False])
    most_recent_dates = sorted_df.groupby('cve_expediente')['award_end_date'].max().reset_index()
    df_licitacion = pd.merge(most_recent_dates, sorted_df, on=['cve_expediente', 'award_end_date'], how='inner')

    status_priority = {'complete': 1, 'unsuccessful': 2, 'active': 3}

    df_licitacion['status_priority'] = df_licitacion['status'].map(status_priority)
    df_licitacion = df_licitacion.sort_values(by=['cve_expediente', 'status_priority'])
    df_licitacion = df_licitacion.drop_duplicates(subset='cve_expediente', keep='first')
    df_licitacion = df_licitacion.drop(columns=['status_priority'])

    return df_licitacion


def extract_participantes_proveedores(db, progress_bar=None):
    """
    Extrae los datos de Participantes_Proveedores y los guarda en un archivo csv.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Base de datos de MongoDB
    :return: None
    """
    try:
        logger.info("Iniciando extracción de Participantes Proveedores...")
        # Realiza la consulta a la base de datos
        consulta_actualizada = db[COLLECTION_NAME]
        num_documents = consulta_actualizada.count_documents({})
        logger.info("Número de documentos en la colección: %s", num_documents)
        consulta_actualizada = consulta_actualizada.find({}, {})
        datos = []
        for i, contrato in enumerate(consulta_actualizada):
            for party in contrato.get('releases', [{}])[0].get('parties', []):
                if party:
                    roles = party.get('roles', [])
                    if "tenderer" in roles or all(role in roles for role in ["tenderer", "supplier"]):
                        contrato_dict = {
                            'cve_expediente': contrato.get('releases', [{}])[0].get('tender', {}).get('id', ''),
                            'cve_contrato': contrato.get('releases', [{}])[0].get('awards', [{}])[0].get('id', ''),
                            'identifier_id': party.get('identifier', {}).get('id', ''),
                            'roles': roles,
                            'name': party.get('name', ''),
                            'identifier_legalName': party.get('identifier', {}).get('legalName', ''),
                            'identifier_scheme': party.get('identifier', {}).get('scheme', ''),
                            'identifier_uri': party.get('identifier', {}).get('uri', ''),
                            'address_countryName': party.get('address', {}).get('countryName', ''),
                            'address_locality': party.get('address', {}).get('locality', ''),
                            'address_postalCode': party.get('address', {}).get('postalCode', ''),
                            'address_region': party.get('address', {}).get('region', ''),
                            'address_streetAddress': party.get('address', {}).get('streetAddress', ''),
                            'contactPoint_email': party.get('contactPoint', {}).get('email', ''),
                            'contactPoint_name': party.get('contactPoint', {}).get('name', ''),
                            'contactPoint_telephone': party.get('contactPoint', {}).get('telephone', '')
                        }
                        datos.append(contrato_dict)
            if progress_bar is not None:
                progress_bar.progress((i / num_documents),
                                      f"Extrayendo datos de Participantes Proveedores: "
                                      f"{round((i / num_documents) * 100, 2)}%")

        # Creando el dataframe de Participantes_Proveedores
        df_participantes_proveedores = pd.DataFrame(datos)

        logger.info("El dataframe de Participantes_Proveedores tiene el siguiente tamaño: %s",
                    df_participantes_proveedores.shape)
        # Verifica si se obtuvieron datos
        if not df_participantes_proveedores.empty:
            logger.info("El dataframe de Participantes_Proveedores tiene el siguiente tamaño: %s",
                        df_participantes_proveedores.shape)
            logger.info("Exportando Participantes_Proveedores a un archivo csv")
            df_participantes_proveedores.to_csv(
                path_config.contrataciones_processed_csv_path + 'participantes_proveedores.csv',
                index=False, encoding='utf-8')
            logger.info("Exportación de Participantes_Proveedores a archivo parquet")
            # df_participantes_proveedores.to_parquet(
            #     path_config.contrataciones_processed_parquet_path + 'participantes_proveedores.parquet')
        else:
            logger.warning("No se encontraron datos para extraer.")
    except Exception as e:
        logger.error(f"Error durante la extracción de Participantes_Proveedores: {e}")


def extract_licitacion(db, progress_bar=None):
    """
    Extrae los datos de licitación y los guarda en un archivo CSV.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Base de datos de MongoDB
    :return: None
    """
    try:
        logger.info("Iniciando extracción de datos de licitación...")

        consulta_actualizada = db[COLLECTION_NAME].find({}, {})
        num_documents = db[COLLECTION_NAME].count_documents({})
        datos = []

        for i, contrato in enumerate(consulta_actualizada):
            contrato_dict = {
                'cve_expediente': '',
                'procurementMethod': '',
                'procurementMethod_rationale': '',
                'status': '',
                'title': '',
                'description': '',
                'has_enquiries': '',
                'number_tenderers': '',
                'tender_start_date': '',
                'tender_end_date': '',
                'award_start_date': '',
                'award_end_date': '',
                'enquiry_start_date': '',
                'enquiry_end_date': '',
                'procuring_entity_id': '',
                'procuring_entity_name': '',
                'value_currency_tender': '',
                'value_amount_tender': '',
                'award_criteria': '',
                'framework_agreement': '',
                'framework_agreement_platform': '',
                'framework_agreement_title': '',
                'submission_method': '',
            }
            try:
                tender = contrato.get('releases', [{}])[0].get('tender', {})
                contrato_dict['cve_expediente'] = tender.get('id', '')  # id
                contrato_dict['procurementMethod'] = tender.get('procurementMethod', '')
                contrato_dict['procurementMethod_rationale'] = tender.get('procurementMethodRationale', '')
                contrato_dict['status'] = tender.get('status', '')
                contrato_dict['title'] = tender.get('title', '')
                contrato_dict['description'] = tender.get('description', '')
                contrato_dict['has_enquiries'] = tender.get('hasEnquiries', '')
                contrato_dict['number_tenderers'] = len(tender.get('tenderers', []))
                contrato_dict['tender_start_date'] = tender.get('tenderPeriod', {}).get('startDate', '')
                contrato_dict['tender_end_date'] = tender.get('tenderPeriod', {}).get('endDate', '')
                contrato_dict['award_start_date'] = tender.get('awardPeriod', {}).get('startDate', '')
                contrato_dict['award_end_date'] = tender.get('awardPeriod', {}).get('endDate', '')
                contrato_dict['enquiry_start_date'] = tender.get('enquiryPeriod', {}).get('startDate', '')
                contrato_dict['enquiry_end_date'] = tender.get('enquiryPeriod', {}).get('endDate', '')
                contrato_dict['procuring_entity_id'] = tender.get('procuringEntity', {}).get('id', '')
                contrato_dict['procuring_entity_name'] = tender.get('procuringEntity', {}).get('name', '')
                contrato_dict['value_currency_tender'] = tender.get('value', {}).get('currency', '')
                contrato_dict['value_amount_tender'] = tender.get('value', {}).get('amount', '')
                contrato_dict['award_criteria'] = tender.get('awardCriteria', '')
                contrato_dict['framework_agreement'] = tender.get('frameworkAgreement', '')
                contrato_dict['framework_agreement_platform'] = tender.get('frameworkAgreementPlatform', '')
                contrato_dict['framework_agreement_title'] = tender.get('frameworkAgreementTitle', '')
                contrato_dict['submission_method'] = tender.get('submissionMethod', [''])[0]

                if progress_bar is not None:
                    progress_bar.progress((i / num_documents),
                                          f"Extrayendo datos de licitación: {round((i / num_documents) * 100, 2)}%")
            except AttributeError:
                logger.error("Error al extraer datos de licitación.")
            datos.append(contrato_dict)

        df_licitacion = pd.DataFrame(datos)

        # Data cleaning
        df_licitacion = clean_licitacion(df_licitacion)

        if not df_licitacion.empty:
            logger.info("El dataframe de Licitación tiene el siguiente tamaño: %s", df_licitacion.shape)
            logger.info("Exportando Licitación a un archivo csv")
            df_licitacion.to_csv(path_config.contrataciones_processed_csv_path + 'licitacion_data.csv', index=False,
                                 encoding='utf-8')
            logger.info("Exportación de Licitación a archivo parquet")
            # TODO Solventar la exportacion a parquet
            # He probado con las lineas de abajo pero sigue sin funcionar
            # df_licitacion['value_amount_tender'] = pd.to_numeric(df_licitacion['value_amount_tender'], errors='coerce')
            # df_licitacion['framework_agreement'] = df_licitacion['framework_agreement'].astype('boolean')
            # df_licitacion.to_parquet(path_config.contrataciones_processed_parquet_path + 'licitacion_data.parquet')

            logger.info("Extracción de datos de licitación finalizada.")
            return df_licitacion
        else:
            logger.warning("No se encontraron datos para extraer de licitación.")

    except Exception as e:
        logger.error(f"Error durante la extracción de datos de licitación: {e}")


# Asignación
def extract_asignacion(db, progress_bar=None):
    """
    Extrae los datos de Asignación y los guarda en un archivo CSV.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Base de datos de MongoDB
    :return: None
    """
    documentos = db[COLLECTION_NAME].find({}, {})
    num_documents = db[COLLECTION_NAME].count_documents({})
    datos = []
    for i, contrato in enumerate(documentos):
        for award in contrato.get('releases', [{}])[0].get('awards', []):
            contrato_dict = {
                'cve_expediente': contrato.get('releases', [{}])[0].get('tender', {}).get('id', ''),
                'cve_contrato': award.get('id', ''),
                'status': award.get('status', ''),
                'description_award': award.get('description', ''),
                'title_award': award.get('title', ''),
                'contract_start_date': award.get('contractPeriod', {}).get('startDate', ''),
                'contract_end_date': award.get('contractPeriod', {}).get('endDate', ''),
                'value_amount': award.get('value', {}).get('amount', ''),
                'value_currency': award.get('value', {}).get('currency', ''),
                'suppliers_id': award.get('suppliers', [{}])[0].get('id', ''),
                'suppliers_name': award.get('suppliers', [{}])[0].get('name', ''),
                'docs_url_awards': award.get('documents', [{}])[0].get('url', '') if award.get('documents') else '',
                'docs_title_awards': award.get('documents', [{}])[0].get('title', '') if award.get('documents') else '',
                'docs_language_awards': award.get('documents', [{}])[0].get('language', '') if award.get(
                    'documents') else '',
                'docs_id_awards': award.get('documents', [{}])[0].get('id', '') if award.get('documents') else '',
                'docs_format_awards': award.get('documents', [{}])[0].get('format', '') if award.get(
                    'documents') else '',
                'docs_type_awards': award.get('documents', [{}])[0].get('documentType', '') if award.get(
                    'documents') else '',
                'docs_descr_awards': award.get('documents', [{}])[0].get('description', '') if award.get(
                    'documents') else '',
                'docs_date_published_awards': award.get('documents', [{}])[0].get('datePublished', '') if award.get(
                    'documents') else ''
            }
            datos.append(contrato_dict)
            if progress_bar is not None:
                progress_bar.progress((i / num_documents),
                                      f"Extrayendo datos de Asignación: {round((i / num_documents) * 100, 2)}%")
    df_asignacion = pd.DataFrame(datos)
    df_asignacion = clean_asignacion(df_asignacion)
    if not df_asignacion.empty:
        logger.info("El dataframe de Asignación tiene el siguiente tamaño: %s", df_asignacion.shape)
        logger.info("Exportando Asignación a un archivo csv")
        df_asignacion.to_csv(
            path_config.contrataciones_processed_csv_path + 'asignacion_data.csv',
            index=False, encoding='utf-8')
        # logger.info("Exportación de Asignación a archivo parquet")
        # df_asignacion.to_parquet(
        #     path_config.contrataciones_processed_parquet_path + 'asignacion_data.parquet')
        # logger.info("Extracción de Participantes_Proveedores finalizada.")
    else:
        logger.warning("No se encontraron datos para extraer.")


# Comprador

def extract_comprador(db, progress_bar=None):
    """
    Extrae los datos de Comprador y los guarda en un archivo CSV.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Base de datos de MongoDB
    :return: None
    """
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})
    num_documents = db[COLLECTION_NAME].count_documents({})
    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for i, contrato in enumerate(consulta_actualizada):
        parties = contrato.get('releases', [{}])[0].get('parties', [])
        for party in parties:
            if party:  # Check if party is not None
                roles = party.get('roles', [])
                if 'buyer' in roles or 'procuringEntity' in roles:
                    contrato_dict = {
                        'cve_expediente': contrato.get('releases', [{}])[0].get('tender', {}).get('id', ''),  # id
                        'cve_contrato': contrato.get('releases', [{}])[0].get('awards', [{}])[0].get('id', ''),
                        'identifier_id_inst': party.get('identifier', {}).get('id', ''),
                        'roles': roles[0] if roles else '',
                        'name': party.get('name', ''),
                        'identifier_legal_name': party.get('identifier', {}).get('legalName', ''),
                        'identifier_schema': party.get('identifier', {}).get('scheme', ''),
                        'identifier_uri': party.get('identifier', {}).get('uri', ''),
                        'addres_country_name': party.get('address', {}).get('countryName', ''),
                        'addres_locality': party.get('address', {}).get('locality', ''),
                        'address_postalcode': party.get('address', {}).get('postalCode', ''),
                        'address_region': party.get('address', {}).get('region', ''),
                        'addres_streetaddress': party.get('address', {}).get('streetAddress', ''),
                        'contact_point_email': party.get('contactPoint', {}).get('email', ''),
                        'contact_point_name': party.get('contactPoint', {}).get('name', ''),
                        'contact_point_telephone': party.get('contactPoint', {}).get('telephone', '')
                    }
                    datos.append(contrato_dict)
        if progress_bar is not None:
            progress_bar.progress((i / num_documents),
                                  f"Extrayendo datos de Comprador: {round((i / num_documents) * 100, 2)}%")

    # Creando el dataframe de comprador
    df_comprador = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv_files
    logger.info("El dataframe de Comprador tiene el siguiente tamaño: %s", df_comprador.shape)
    logger.info("Exportando Comprador a un archivo csv")
    df_comprador.to_csv(path_config.contrataciones_processed_csv_path + 'comprador_sesna_data.csv', index=False,
                        encoding='utf-8')
    # logger.info("Exportación de Comprador a archivo parquet")
    # df_comprador.to_parquet(path_config.contrataciones_processed_parquet_path + 'comprador_sesna_data.parquet')


# Documentos TENDER
def extract_documentos_tender(db, progress_bar=None):
    """
    Extrae los datos de Documentos Tender y los guarda en un archivo CSV.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Parámetro de la base de datos de MongoDB
    :return: None
    """
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})
    num_documents = db[COLLECTION_NAME].count_documents({})
    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for i, contrato in enumerate(consulta_actualizada):
        # Accede a cada release. Asumimos que cada contrato tiene al menos un release.
        releases = contrato.get('releases', [])
        for release in releases:
            # Accede a los documentos dentro de 'tender', si existen
            tender = release.get('tender', {})
            documents = tender.get('documents', [])

            if documents:
                for document in documents:
                    contrato_dict = {
                        'cve_expediente': tender.get('id', ''),
                        'docs_title_tender': document.get('title', ''),
                        'docs_type_tender': document.get('documentType', ''),
                        'docs_language_tender': document.get('language', ''),
                        'docs_date_published_tender': document.get('datePublished', ''),
                        'docs_id_tender': document.get('id', ''),
                        'docs_format_tender': document.get('format', ''),
                        'docs_description_tender': document.get('description', ''),
                        'docs_url_tender': document.get('url', '')
                    }
                    datos.append(contrato_dict)
            else:
                # Create a record with empty document fields if there are no documents
                contrato_dict = {
                    'cve_expediente': tender.get('id', ''),
                    'docs_title_tender': '',
                    'docs_type_tender': '',
                    'docs_language_tender': '',
                    'docs_date_published_tender': '',
                    'docs_id_tender': '',
                    'docs_format_tender': '',
                    'docs_description_tender': '',
                    'docs_url_tender': ''
                }
                datos.append(contrato_dict)
        if progress_bar is not None:
            progress_bar.progress((i / num_documents),
                                  f"Extrayendo datos de Documentos Tender: {round((i / num_documents) * 100, 2)}%")

    # Creando el dataframe de documentos tender
    df_documentos_tender = pd.DataFrame(datos)
    df_documentos_tender = clean_documentos_tender(df_documentos_tender)
    # Exportando el dataframe a un archivo csv_files
    logger.info("El dataframe de Documentos Tender tiene el siguiente tamaño: %s", df_documentos_tender.shape)
    logger.info("Exportando Documentos Tender a un archivo csv")
    df_documentos_tender.to_csv(path_config.contrataciones_processed_csv_path + 'documentos_tender_sesna_data.csv',
                                index=False, encoding='utf-8')
    # logger.info("Exportación de Documentos Tender a archivo parquet")
    # df_documentos_tender.to_parquet(
    #     path_config.contrataciones_processed_parquet_path + 'documentos_tender_sesna_data.parquet')


# ITEM_ADQ
def extract_item_adq(db, progress_bar=None):
    """
    Extrae los datos de Item Adquisición y los guarda en un archivo CSV.
    :param progress_bar: Barra de progreso (Streamlit)
    :param db: Parámetro de la base de datos de MongoDB
    :return: None
    """
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})
    num_documents = db[COLLECTION_NAME].count_documents({})
    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for i, contrato in enumerate(consulta_actualizada):
        for award in contrato.get('releases', [{}])[0].get('awards', [{}]):
            for item in award.get('items', []):
                contrato_dict = {
                    'cve_expediente': contrato.get('releases', [{}])[0].get('tender', {}).get('id', ''),  # id
                    'cve_contrato': award.get('id', ''),
                    'items_unit_val_currency_awards': item.get('unit', {}).get('value', {}).get('currency', ''),
                    'items_unit_val_amount_awards': item.get('unit', {}).get('value', {}).get('amount', ''),
                    'items_unit_name_awards': item.get('unit', {}).get('name', ''),
                    'items_classion.uri': item.get('classification', {}).get('uri', ''),
                    'items_classi_scheme_awards': item.get('classification', {}).get('scheme', ''),
                    'items_class_id_awards': item.get('classification', {}).get('id', ''),
                    'items_class_description_awards': item.get('classification', {}).get('description', ''),
                    'items_quantity_awards': item.get('quantity', ''),
                    'items_id_awards': item.get('id', ''),
                    'items_description_awards': item.get('description', ''),
                }
                datos.append(contrato_dict)
        if progress_bar is not None:
            progress_bar.progress((i / num_documents),
                                  f"Extrayendo datos de Item Adquisición: {round((i / num_documents) * 100, 2)}%")

    # Creando el dataframe de ITEMS
    df_items = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv_files
    logger.info("El dataframe de Items tiene el siguiente tamaño: %s", df_items.shape)
    logger.info("Exportando Item Adquisición a un archivo csv")
    df_items.to_csv(path_config.contrataciones_processed_csv_path + 'items_adq_sesna_data.csv', index=False,
                    encoding='utf-8')
    # logger.info("Exportación de Item Adquisición a archivo parquet")
    # df_items.to_parquet(path_config.contrataciones_processed_parquet_path + 'items_adq_sesna_data.parquet')


# ITEM_TENDER
def extract_item_tender(db, progress_bar=None):
    """
    Extrae los datos de Item Tender y los guarda en un archivo CSV.
    :param db: Parámetro de la base de datos de MongoDB
    :return: None
    """
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})
    num_documents = db[COLLECTION_NAME].count_documents({})
    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for i, contrato in enumerate(consulta_actualizada):
        for item in contrato.get('releases', [{}])[0].get('tender', {}).get('items', []):
            contrato_dict = {
                'cve_expediente': contrato.get('releases', [{}])[0].get('tender', {}).get('id', ''),
                'items_unit_name_tender': item.get('unit', {}).get('name', ''),
                'items_class_id_tender': item.get('classification', {}).get('id', ''),
                'items_class_description_tender': item.get('classification', {}).get('description', ''),
                'items_quantity_tender': item.get('quantity', ''),
                'items_id_tender': item.get('id', ''),
                'items_description_tender': item.get('description', ''),
            }
            datos.append(contrato_dict)
        if progress_bar is not None:
            progress_bar.progress((i / num_documents),
                                  f"Extrayendo datos de Item Tender: {round((i / num_documents) * 100, 2)}%")
    # Creando el dataframe de Tender Items
    df_tender_items = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv_files
    logger.info("El dataframe de Tender Items tiene el siguiente tamaño: %s", df_tender_items.shape)
    logger.info("Exportando Item Tender a un archivo csv")
    df_tender_items.to_csv(path_config.contrataciones_processed_csv_path + 'tender_items_sesna_data.csv',
                           index=False,
                           encoding='utf-8')
    # logger.info("Exportación de Item Tender a archivo parquet")
    # df_tender_items.to_parquet(path_config.contrataciones_processed_parquet_path + 'tender_items_sesna_data.parquet')
    # logger.info("Extracción de Tender Items finalizada.")


def clean_asignacion(df_asignacion):
    """
    Limpia los datos de asignación
    :param df_asignacion: DataFrame de asignación
    :return: DataFrame de asignación tras el proceso de limpieza
    """
    df_asignacion['contract_start_date'] = pd.to_datetime(df_asignacion['contract_start_date'], errors='coerce')
    df_asignacion = df_asignacion.sort_values(['cve_contrato', 'contract_start_date'], ascending=[True, False])
    df_asignacion = df_asignacion.drop_duplicates(subset=['cve_contrato'], keep='first')

    return df_asignacion


def clean_documentos_tender(df_documentos_tender):
    """
    Limpia los datos de documentos tender
    :param df_documentos_tender: DataFrame de documentos tender
    :return: DataFrame de documentos tender tras el proceso de limpieza.
    """
    df_documentos_tender['docs_date_published_tender'] = pd.to_datetime(
        df_documentos_tender['docs_date_published_tender'])
    df_documentos_tender = df_documentos_tender.sort_values(by='docs_date_published_tender', ascending=True)
    df_documentos_tender = df_documentos_tender.drop_duplicates(subset='cve_expediente', keep='first')

    return df_documentos_tender
