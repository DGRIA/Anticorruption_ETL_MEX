import streamlit as st
import logging
import os
import shutil
from config import *
import config
from src.mongodb_utils import process_large_json, get_file_size, get_collection_count
from src.data_download_unzip import download_contrataciones_zip, unzip, check_files_exist
from src.extraction_mongodb import extract_participantes_proveedores, extract_licitacion, extract_asignacion, \
    extract_comprador, extract_documentos_tender, extract_item_adq, extract_item_tender

import base64
import zipfile

from src.mongodb_utils import connect_to_mongodb

logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)


def show_footer(show=False):
    """
    Función que muestra el footer de la página
    :return: None
    """
    if show:
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns([1, 1, 1])  # Create three columns
        inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
        inner_cols[0].markdown(
            "<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with "
            "love</p>",
            unsafe_allow_html=True)  # Center the text, change the font, and add padding
        inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)


def create_download_link(table, filename):
    def download():
        # Create a new ZIP file
        zip_filename = f"{filename.split('.')[0]}.zip"
        zip_path = path_config.data_path + '/' + zip_filename
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(path_config.contrataciones_processed_csv_path + filename, arcname=filename)

        # Read the ZIP file into
        with open(zip_path, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/zip;base64,{b64}" download="{zip_filename}">Download {zip_filename}</a>'
            return href

    return download


def create_download_link_all(directory, zip_filename):
    def download():
        # Get a list of all CSV files in the directory
        filenames = [f for f in os.listdir(directory) if f.endswith('.csv')]

        # Create a new ZIP file
        with zipfile.ZipFile(path_config.data_path + '/' + zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in filenames:
                logger.info(f"Adding {filename} to ZIP file.")
                zipf.write(os.path.join(directory, filename), arcname=filename)

        # Read the ZIP file into memory
        with open(path_config.data_path + '/' + zip_filename, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/zip;base64,{b64}" download="{zip_filename}">Download {zip_filename}</a>'
            return href

    return download


def show_intro():
    st.markdown((
        """
            La siguiente aplicación ha sido desarrollada para [SESNA](https://www.sesna.gob.mx/).
            El propósito de esta aplicación es la descarga, limpieza y unión de las bases de datos
            publicadas en la siguiente URL: [Programa de Anticorrupción](https://compranetinfo.hacienda.gob.mx/dabiertos/contrataciones_arr.json.zip).
            Este proyecto contribuirá con la creación de políticas integrales y anteproyectos de metodologías e indicadores para evaluar el fenómeno de la corrupción en México.
        """
    ))

    show_footer(True)


def start_download_and_unzip():
    st.markdown(f"En esta pestaña se realiza la descarga desde [Compranet]({CONTRATACIONES_URL}) y propia extracción.")

    if os.path.exists(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON):
        st.info(
            f"El archivo `{CONTRATACIONES_JSON}` ya se encuentra en el directorio "
            f"`{path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON}`. "
            f"Tiene un tamaño de {get_file_size(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON)} GB."
            f" Si desea volver a descargarlo inicie el proceso de descarga")
    else:
        st.error(
            f"El archivo de Contrataciones no se encuentra descargado."
            f" Es necesario descargarlo para continuar con el proceso o adjuntarlo para su descompresión en la "
            f"siguiente sección.")

    cols_button = st.columns([1, 1, 1])  # Create three columns for the button
    if cols_button[1].button('Inicio de descarga'):
        main()
    show_footer(True)


def start_upload_and_unzip():
    st.markdown(
        "En el caso de que ya tengas el archivo descargado, puedes subirlo y descomprimirlo aquí. Para la descarga "
        "manual del archivo, puedes hacerlo desde [Compranet]("
        "https://compranetinfo.hacienda.gob.mx/dabiertos/contrataciones_arr.json.zip)."
        " En el caso de que ya esté subido el archivo, puedes descomprimirlo de nuevo.")

    if os.path.exists(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON):
        print("El archivo ya se encuentra en el directorio.")
        st.info(
            f"El archivo `{CONTRATACIONES_ZIP}` ya se encuentra en el directorio "
            f"`{path_config.contrataciones_raw_unzip_path}`. Tiene un tamaño de "
            f"{get_file_size(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_ZIP)} GB.")
    elif os.path.exists(path_config.contrataciones_raw_path):
        st.info(
            f"El archivo `{CONTRATACIONES_ZIP}` ya se encuentra en el directorio "
            f"`{path_config.contrataciones_raw_path}`. Tiene un tamaño de "
            f"{get_file_size(path_config.contrataciones_raw_path)} GB. Sólo es necesaria la descompresión.")
    uploaded_file = st.file_uploader("Elige el archivo JSON comprimido", type=['zip'])
    with st.spinner('Subiendo archivo...'):
        logger.info(f"Subiendo archivo {uploaded_file}")
        if uploaded_file is not None:
            logger.info(f"El archivo no está vacío")
            try:
                with open(os.path.join(path_config.contrataciones_raw_unzip_path, 'contrataciones_arr.json.zip'),
                          'wb') as f:
                    logger.info(f"Guardando archivo en {path_config.contrataciones_raw_unzip_path}")
                    for chunk in iter(lambda: uploaded_file.read(1024 * 1024), b''):
                        f.write(chunk)
                    logger.info(f"Archivo guardado con éxito.")
                st.success(
                    f"Archivo ZIP subido: {uploaded_file.name}. Guardado en Streamlit como `contrataciones_arr.json.zip`.")
            except Exception as e:
                st.error(f"Error al guardar el archivo: {str(e)}")

    if os.path.exists(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_ZIP):
        logger.info(f"El archivo {CONTRATACIONES_JSON} ya se encuentra en el directorio.")
        cols_button = st.columns([1, 1, 1])
        if cols_button[1].button('Descomprimir archivo', key='upload_unzip', type='secondary'):
            with st.spinner(f"Descomprimiendo archivo {CONTRATACIONES_ZIP}..."):
                try:
                    progress_bar = st.progress(0, 'Iniciando descompresión...')
                    unzip(pb=progress_bar)
                    progress_bar.progress(100)
                    st.success('Archivo descomprimido con éxito. Ya puede popular la base de datos.')
                except Exception as e:
                    st.error(f"Error al descomprimir el archivo: {str(e)}")

    show_footer(True)


def start_populate():
    st.markdown(
        f"El siguiente paso es la inserción de los datos en MongoDB. La base de datos establecida en la configuración "
        f"es: `{DB_NAME}`. La colección establecida en la configuración es: `{COLLECTION_NAME}`.")

    if os.path.exists(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON):
        st.markdown(
            f"El archivo `{CONTRATACIONES_JSON}` se usará para popular la base de datos."
            f" Tiene un tamaño de {get_file_size(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON)} GB.")
        cols_button = st.columns([1, 1, 1])
        if cols_button[1].button('Iniciar Populate'):
            with st.spinner('Insertando datos en MongoDB...'):
                progress_bar = st.progress(0, 'Conectando con la base de datos...')
                process_large_json(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON,
                                   progress_bar=progress_bar)
                progress_bar.progress(100, 'Datos insertados en MongoDB.')

    elif (os.path.exists(path_config.contrataciones_raw_path) and
          (not os.path.exists(path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON))):
        st.warning(
            f"El archivo `{CONTRATACIONES_JSON}` no se encuentra en el directorio "
            f"`{path_config.contrataciones_raw_unzip_path}`. Pero sí está `{CONTRATACIONES_ZIP}`. Sólo "
            f"es necesario descomprimirlo en el paso previo.")
    else:
        st.error(
            f"El archivo `{CONTRATACIONES_JSON}` no se encuentra en el directorio "
            f"`{path_config.contrataciones_raw_path}`. Es necesario descargarlo y descomprimirlo los pasos previos.")
    show_footer(True)


def start_extraction():
    db = connect_to_mongodb()
    # Set a uniform width for all buttons
    '''
    Haz clic en la tabla(s) que deseas exportar y continúa al siguiente paso. Las limpiezas 
    necesarias se realizan de manera implícita en aquellas que las requieran.
    '''
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # Proveedores
    if st.button('Extraer Proveedores', key='button1', type='secondary'):
        with st.spinner('Extrayendo la tabla de Participantes Proveedores de MongoDB...'):
            progress_bar_proveedores = st.progress(0, 'Extrayendo Participantes Proveedores...')
            extract_participantes_proveedores(db, progress_bar_proveedores)
            st.success('Extracción de Participantes Proveedores fue un éxito.')
    # Licitaciones
    if st.button('Extraer Licitaciones', key='button2', type='secondary'):
        with st.spinner('Extrayendo la tabla de Licitaciones de MongoDB...'):
            progress_bar_licitaciones = st.progress(0, 'Extrayendo Licitaciones...')
            extract_licitacion(db, progress_bar_licitaciones)
            st.success('Extracción de Licitaciones fue un éxito.')
    # Asignaciones
    if st.button('Extraer Asignaciones', key='button3', type='secondary'):
        with st.spinner('Extrayendo la tabla de Asignaciones de MongoDB...'):
            progress_bar_asignaciones = st.progress(0, 'Extrayendo Asignaciones...')
            extract_asignacion(db, progress_bar_asignaciones)
            st.success('Extracción de Asignaciones fue un éxito.')
    # Compradores
    if st.button('Extraer Compradores', key='button4', type='secondary'):
        with st.spinner('Extrayendo la tabla de Compradores de MongoDB...'):
            progress_bar_compradores = st.progress(0, 'Extrayendo Compradores...')
            extract_comprador(db, progress_bar_compradores)
            st.success('Extracción de Compradores fue un éxito.')
    # Documentos Tender
    if st.button('Extraer Documentos Tender', key='button5', type='secondary'):
        with st.spinner('Extrayendo la tabla de Documentos Tender de MongoDB...'):
            progress_bar_documentos_tender = st.progress(0, 'Extrayendo Documentos Tender...')
            extract_documentos_tender(db, progress_bar_documentos_tender)
            st.success('Extracción de Documentos Tender fue un éxito.')
    # Items ADQ
    if st.button('Extraer Ítem ADQ', key='button6', type='secondary'):
        with st.spinner('Extrayendo la tabla de Item ADQ de MongoDB...'):
            progress_bar_item_adq = st.progress(0, 'Extrayendo Items ADQ...')
            extract_item_adq(db, progress_bar_item_adq)
            st.success('Extracción de Items ADQ fue un éxito.')
    # Items Tender
    if st.button('Extraer Ítem Tender', key='button7', type='secondary'):
        with st.spinner('Extrayendo la tabla de Item Tender de MongoDB...'):
            progress_bar_item_tender = st.progress(0, 'Extrayendo Items Tender...')
            extract_item_tender(db, progress_bar_item_tender)
            st.success('Extracción de Items Tender fue un éxito.')
    # Extract all tables
    if st.button('Extraer todas las tablas', key='button8', type='primary'):
        extract_progress_bar = st.progress(0, 'Extrayendo todas las tablas de MongoDB...')
        with st.spinner('Extrayendo todas las tablas de MongoDB...'):
            extract_progress_bar.progress(0 / 7, 'Extrayendo Participantes Proveedores...')
            extract_participantes_proveedores(db)
            extract_progress_bar.progress(1 / 7, 'Extrayendo Licitaciones...')
            extract_licitacion(db)
            extract_progress_bar.progress(2 / 7, 'Extrayendo Asignaciones...')
            extract_asignacion(db)
            extract_progress_bar.progress(3 / 7, 'Extrayendo Compradores...')
            extract_comprador(db)
            extract_progress_bar.progress(4 / 7, 'Extrayendo Documentos Tender...')
            extract_item_adq(db)
            extract_progress_bar.progress(5 / 7, 'Extrayendo Items ADQ...')
            extract_item_tender(db)
            extract_progress_bar.progress(6 / 7, 'Extrayendo Items Tender...')
            extract_documentos_tender(db)
            extract_progress_bar.progress(7 / 7, 'Extracción completa.')
        st.success('La extracción fue un éxito.')

    show_footer(True)


def create_download_button(table, filename, key, path=None, filenames=[]):
    st.markdown("""
        <style>
        .stDownloadButton>button {
            width: 100%;
        }
        </style>
        """, unsafe_allow_html=True)
    if path:
        if os.path.exists(path + filename):
            with st.spinner(f'Generando link de descarga para {table}...'):
                if st.download_button(f'Descargar {table}', data=create_download_link(table, filename)(),
                                      file_name=f'{filename.split(".")[0]}.zip', key=key,
                                      type='secondary'):
                    st.success(f"Archivo {filename[:-4]}.zip guardado con éxito.")

        elif table == 'todas las tablas' and check_files_exist(filenames,
                                                               path_config.contrataciones_processed_csv_path):
            with st.spinner(f'Generando link de descarga para {table}...'):
                if st.download_button(
                        f'Descargar {table}', data=create_download_link_all(filename, 'all_data.zip')(), key=key,
                        type='primary', file_name='all_data.zip'):
                    st.success(f"Archivo all_data.zip guardado con éxito.")
                    # href = create_download_link_all(filename, 'all_data.zip')()
                    # st.markdown(href, unsafe_allow_html=True)
        else:
            if table == 'todas las tablas':
                st.error(f'No se han generado los archivos CSV necesarios para la descarga de {table}.')
            else:
                st.error(f'El archivo de {table} no existe.')


def download_results():
    st.markdown((
        """Esta sección es para la descarga de los archivos generados en la sección de extracción de datos. Son 
        archivos grandes con lo cual puede tardar un poco en descargarlos."""
    ))
    st.markdown((
        """ :warning: En el caso de que los ficheros CSV no se hayan generado, no aparecerá el botón de descarga."""
    ))
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    files = {
        'Participantes Proveedores': 'participantes_proveedores.csv',
        'Licitaciones': 'licitacion_data.csv',
        'Asignaciones': 'asignacion_data.csv',
        'Compradores': 'comprador_sesna_data.csv',
        'Documentos Tender':
            'documentos_tender_sesna_data.csv',
        'Items ADQ': 'items_adq_sesna_data.csv',
        'Items Tender': 'tender_items_sesna_data.csv',
        'todas las tablas': path_config.contrataciones_processed_csv_path
    }

    # Add buttons to columns
    for i, (table, file_name) in enumerate(files.items()):
        if table != 'todas las tablas':
            create_download_button(table=table, filename=file_name, key=f'download_{i}',
                                   path=path_config.contrataciones_processed_csv_path)
        else:
            create_download_button(table='todas las tablas', filename=files['todas las tablas'],
                                   filenames=[v for (_, v) in files.items()], key=f'download_{i}',
                                   path=path_config.contrataciones_processed_csv_path)


    show_footer(True)


def main():
    if not os.path.exists(config.path_config.data_path):
        os.makedirs(config.path_config.data_path)
        logger.info("Directory 'data' missing, creating 'data' directory.")
    if not os.path.exists(config.path_config.contrataciones_raw_unzip_path):
        os.makedirs(config.path_config.contrataciones_raw_unzip_path)
        logger.info("Directory %s missing, creating %s", config.path_config.contrataciones_raw_unzip_path,
                    config.path_config.contrataciones_raw_unzip_path)

    with st.spinner(
            'Este proceso puede tardar unos minutos dependiendo de su conexión a internet'):
        logger.info("Inicio de Descarga y Extracción de datos")
        progress_bar = st.progress(0, 'Estableciendo conexión con el servidor')  # Initialize progress bar
        try:
            download_contrataciones_zip(pb=progress_bar)
            progress_bar.progress(50,
                                  'Descomprimiendo documentos')
            unzip(pb=progress_bar, progress=0.5)
            progress_bar.progress(100)  # Update progress bar to 100% as we only have one function
        # process_large_json(config.path_config.contrataciones_raw_path)
        except Exception as e:
            logger.error(f"download_and_unzip failed with error:\n{str(e)}")
            st.error(f"download_and_unzip failed with error:\n{str(e)}")


if __name__ == '__main__':
    st.markdown('''
                <h1 style='text-align: center; color: black; font-size: 30px;'>Servicio de ingeniería de datos para la extracción,
                transformación y carga (ETL) del Programa de Anticorrupción
                </h1> 
                '''
                , unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # Sidebar
    st.sidebar.image('docs/images/SESNA-logo.png', use_column_width=True)

    st.sidebar.markdown(
        """
        La Secretaria Ejecutiva del Sistema Nacional Anticorrupción 
        (SESNA) es el organismo de apoyo técnico dedicado al combate 
        contra la corrupción en México.
        """
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        Esta página ha sido desarrollada por [mottum](https://mottum.io/) con el fin de
        estandarizar, transformar y analizar los datos del Programa de Anticorrupción.
        """
    )
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = '1. Introducción'

    # Create navigation menu

    st.session_state.page = st.radio('Ejecución del ETL',
                                     ['1. Introducción',
                                      '2. Descarga del servidor y descompresión',
                                      'Subida y descompresión de archivos',
                                      '3. Populate MongoDB',
                                      '4. Extracción de datos de MongoDB',
                                      '5. Acceso a tablas de resultados [.csv]'])

    # Display the selected page
    if st.session_state.page == '1. Introducción':
        show_intro()
    elif st.session_state.page == '2. Descarga del servidor y descompresión':
        start_download_and_unzip()
    elif st.session_state.page == 'Subida y descompresión de archivos':
        start_upload_and_unzip()
    elif st.session_state.page == '3. Populate MongoDB':
        with st.spinner('Recopilando información de MongoDB...'):
            start_populate()
    elif st.session_state.page == '4. Extracción de datos de MongoDB':
        start_extraction()
    elif st.session_state.page == '5. Acceso a tablas de resultados [.csv]':
        download_results()

    st.markdown(
        """
        <style>
            [data-testid=stSidebar] [data-testid=stImage]{
                text-align: center;
                display: block;
                margin-left: auto;
                margin-right: auto;
                width: 100%;
            }
        </style>
        """, unsafe_allow_html=True
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        Visita los siguientes enlaces para más información:
        """
    )

    st.sidebar.markdown(
        """
    - [Repositorio](https://github.com/MottumData/Anticorruption_ETL_MEX)
    - [Jupyter](http://localhost:8889/lab)
    """
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(
        '**Financiado por:**',
        unsafe_allow_html=True
    )
    cols = st.columns([1, 1, 1])

    st.sidebar.image('docs/images/UNDP2.png', width=100)

    if 'button_pressed' not in st.session_state:
        st.session_state.button_pressed = False

    st.markdown("<br>", unsafe_allow_html=True)
