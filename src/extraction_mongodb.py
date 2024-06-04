import pandas as pd
from pymongo import MongoClient
import logging

# Configuración del logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def connect_to_mongodb():
    """Conexión a la base de datos MongoDB en local."""
    try:
        logger.info("Conectando a la base de datos MongoDB...")
        client = MongoClient('mongodb://localhost:27017/', connectTimeoutMS=30000)
        db = client['Contratos_EDCA']
        logger.info("Conexión exitosa a la base de datos.")
        return db
    except Exception as e:
        logger.error(f"Error al conectar a la base de datos: {e}")
        return None

def extract_participantes_proveedores(db):
    """Extrae los datos de Participantes_Proveedores y los guarda en un archivo csv."""
    try:
        logger.info("Iniciando extracción de Participantes_Proveedores...")
        # Realiza la consulta a la base de datos
        consulta_actualizada = db['Contratos_EDCA_Bulk'].find({}, {})
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
            df_participantes_proveedores.to_csv('../data/Processed/All_Tables_Raw/participantes_proveedores_v2_Raw.csv', index=False, encoding='utf-8')
            logger.info("Extracción de Participantes_Proveedores finalizada.")
        else:
            logger.warning("No se encontraron datos para extraer.")
    except Exception as e:
        logger.error(f"Error durante la extracción de Participantes_Proveedores: {e}")


def extract_licitacion_data(db):
    """Extrae los datos de licitación y los guarda en un archivo CSV."""
    try:
        logger.info("Iniciando extracción de datos de licitación...")

        consulta_actualizada = db['Contratos_EDCA_Bulk'].find({}, {})

        datos = []
        for contrato in consulta_actualizada:
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

            except AttributeError:
                pass
            datos.append(contrato_dict)

        df_licitacion = pd.DataFrame(datos)

        if not df_licitacion.empty:
            df_licitacion.to_csv('../data/Processed/All_Tables_Raw/licitacion_data_Raw.csv', index=False, encoding='utf-8')
            logger.info("Extracción de datos de licitación finalizada.")
        else:
            logger.warning("No se encontraron datos para extraer de licitación.")

    except Exception as e:
        logger.error(f"Error durante la extracción de datos de licitación: {e}")


# Este bloque solo se ejecuta si ejecutas este script directamente
if __name__ == "__main__":
    # Conexión a MongoDB
    db = connect_to_mongodb()
    if db is not None:
        # Extracción de datos y generación del archivo CSV
        extract_participantes_proveedores(db)
        extract_licitacion_data(db)
