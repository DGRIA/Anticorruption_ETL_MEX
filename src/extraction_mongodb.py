import pandas as pd
from config import DB_NAME, DB_URL, COLLECTION_NAME, path_config
from pymongo import MongoClient
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Contrataciones")

mongo_logger = logging.getLogger("pymongo")
mongo_logger.setLevel(logging.WARNING)


# TODO Solventar el problemas de las rutas
def extract_participantes_proveedores(db):
    """Extrae los datos de Participantes_Proveedores y los guarda en un archivo csv."""
    try:
        logger.info("Iniciando extracción de Participantes Proveedores...")
        # Realiza la consulta a la base de datos
        consulta_actualizada = db[COLLECTION_NAME]
        num_documents = consulta_actualizada.count_documents({})

        print(f'La colección tiene {num_documents} documentos.')
        consulta_actualizada = consulta_actualizada.find({}, {})
        datos = []
        for contrato in consulta_actualizada:
            for release in contrato.get('releases', []):
                for party in release.get('parties', []):
                    roles = party.get('roles', [])
                    if "tenderer" in roles or all(role in roles for role in ["tenderer", "supplier"]):
                        contrato_dict = {
                            'cve_expediente': release.get('tender', {}).get('id', ''),
                            'cve_contrato': release.get('awards', [{}])[0].get('id', ''),
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

        df_participantes_proveedores = pd.DataFrame(datos)
        # Verifica si se obtuvieron datos
        if not df_participantes_proveedores.empty:
            df_participantes_proveedores.to_csv(
                path_config.contrataciones_processed_raw_path + 'participantes_proveedores_raw.csv',
                index=False, encoding='utf-8')
            logger.info("Extracción de Participantes_Proveedores finalizada.")
        else:
            logger.warning("No se encontraron datos para extraer.")
    except Exception as e:
        logger.error(f"Error durante la extracción de Participantes_Proveedores: {e}")


def extract_licitacion(db):
    """Extrae los datos de licitación y los guarda en un archivo CSV."""
    try:
        logger.info("Iniciando extracción de datos de licitación...")

        consulta_actualizada = db[COLLECTION_NAME].find({}, {})

        datos = []
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
        for contrato in consulta_actualizada:

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

            except AttributeError:
                logger.error("Error al extraer datos de licitación.")
            datos.append(contrato_dict)

        df_licitacion = pd.DataFrame(datos)

        if not df_licitacion.empty:
            df_licitacion.to_csv(path_config.contrataciones_raw_path + 'licitacion_data_raw.csv', index=False,
                                 encoding='utf-8')
            logger.info("Extracción de datos de licitación finalizada.")
        else:
            logger.warning("No se encontraron datos para extraer de licitación.")

    except Exception as e:
        logger.error(f"Error durante la extracción de datos de licitación: {e}")


# Asignación
def extract_asignacion(db):
    documentos = db[COLLECTION_NAME].find({}, {})
    datos = []
    for contrato in documentos:
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
    df_asignacion = pd.DataFrame(datos)
    if not df_asignacion.empty:
        df_asignacion.to_csv(
            path_config.contrataciones_processed_raw_path + 'participantes_proveedores_raw.csv',
            index=False, encoding='utf-8')
        logger.info("Extracción de Participantes_Proveedores finalizada.")
    else:
        logger.warning("No se encontraron datos para extraer.")
    # Exportando el dataframe a un archivo csv
    df_asignacion.to_csv(path_config.contrataciones_processed + 'asignacion_sesna_data.csv', index=False,
                         encoding='utf-8')
    print("Proceso terminado. \n     El dataset de Asignación tiene el siguiente tamaño: (filas x columnas)")
    print(df_asignacion.shape)


# Comprador

def extract_comprador(db):
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})
    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for contrato in consulta_actualizada:
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

    # Creando el dataframe de comprador
    df_comprador = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv
    df_comprador.to_csv(path_config.contrataciones_processed + 'comprador_sesna_data.csv', index=False,
                        encoding='utf-8')
    print("Proceso terminado. \n     El dataset de Comprador tiene el siguiente tamaño: (filas x columnas)")

    print(df_comprador.shape)


# Documentos TENDER
def extract_documentos_tender(db):
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})

    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for contrato in consulta_actualizada:
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

    # Creando el dataframe de documentos tender
    df_documentos_tender = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv
    df_documentos_tender.to_csv(path_config.contrataciones_processed + 'documentos_tender_sesna_data_V2.csv',
                                index=False, encoding='utf-8')
    print("Proceso terminado. \n     El dataset de Documentos Tender tiene el siguiente tamaño: (filas x columnas)")
    print(df_documentos_tender.shape)


# ITEM_ADQ
def extract_item_adq(db):
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})

    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for contrato in consulta_actualizada:
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

    # Creando el dataframe de ITEMS
    df_items = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv
    df_items.to_csv(path_config.contrataciones_processed + 'items_adq_sesna_data.csv', index=False, encoding='utf-8')
    print("Proceso terminado. \n     El dataset de Items tiene el siguiente tamaño: (filas x columnas)")

    print(df_items.shape)


# ITEM_TENDER TODO: Revisar
def extract_item_tender(db):
    consulta_actualizada = db[COLLECTION_NAME].find({}, {})

    # Creando una lista de diccionarios para facilitar la creación del dataframe
    datos = []
    for contrato in consulta_actualizada:
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

    # Creando el dataframe de Tender Items
    df_tender_items = pd.DataFrame(datos)

    # Exportando el dataframe a un archivo csv
    df_tender_items.to_csv(path_config.contrataciones_processed + 'tender_items_sesna_data.csv', index=False,
                           encoding='utf-8')
    print("Proceso terminado. \n     El dataset de Tender Items tiene el siguiente tamaño: (filas x columnas)")