import streamlit as st
import subprocess
import logging
import sys
import os
import shutil
from config import *
import config
from src.data_download_unzip import download_contrataciones_zip, unzip
from src.extraction_mongodb import extract_participantes_proveedores, extract_licitacion, extract_asignacion, \
    extract_comprador, extract_documentos_tender, extract_item_adq, extract_item_tender, clean_licitacion, clean_asignacion, clean_documentos_tender
from pymongo import MongoClient, errors
import base64
import pandas as pd
import zipfile

from src.mongodb_utils import connect_to_mongodb

logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)


def create_download_link(original_filename, download_filename):
    def download():
        # Create a new ZIP file
        zip_filename = f"{download_filename}.zip"
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(original_filename, arcname=os.path.basename(original_filename))

        # Read the ZIP file into
        with open(zip_filename, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/zip;base64,{b64}" download="{zip_filename}">Download {zip_filename}</a>'
            return href

    return download

def create_download_link2(filenames, zip_filename):
    def download():
        # Create a new ZIP file
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename in filenames:
                zipf.write(filename, arcname=os.path.basename(filename))

        # Read the ZIP file into memory
        with open(zip_filename, 'rb') as f:
            bytes = f.read()
            b64 = base64.b64encode(bytes).decode()  # some strings <-> bytes conversions necessary here
            href = f'<a href="data:file/zip;base64,{b64}" download="{zip_filename}">Download {zip_filename}</a>'
            return href

    return download


def show_intro():
    st.markdown((
        """
            La siguiente aplicacion ha sido desarrollada para [SESNA](https://www.sesna.gob.mx/).
            El propósito de esta aplicación es la descarga, limpieza y unión de las bases de datos
            publicadas en la siguiente URL: [Programa de Anticorrupción](https://compranetinfo.hacienda.gob.mx/dabiertos/contrataciones_arr.json.zip).
            Este proyecto contribuirá con la creación de políticas integrales y anteproyectos de metodologías e indicadores para evaluar el fenómeno de la corrupción en México.
        """
    ))

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1])  # Create three columns
    inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
    inner_cols[0].markdown(
        "<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with "
        "love</p>",
        unsafe_allow_html=True)  # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)


def start_download_and_unzip():
    st.markdown((
        """
            En esta pestaña realizamos la descarga de contrataciones_arr.json.zip, y lo extraemos en 
            la carpeta contrataciones_raw_unzip.
        """
    ))
    cols_button = st.columns([1, 3, 1])  # Create three columns for the button
    if cols_button[1].button('Pulsa para comenzar el proceso de descarga y limpieza de datos.', key='unique_key'):
        main()

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1])  # Create three columns
    inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
    inner_cols[0].markdown("<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>", unsafe_allow_html=True) # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)


def start_extraction():
    db = connect_to_mongodb()
    # Set a uniform width for all buttons
    '''
    Haz click en la tabla(s) que deseas exportar y continúa al siguiente paso
    '''
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a row of columns for the buttons
    cols = st.columns(3)
    cols2 = st.columns(3)
    cols3 = st.columns(2)

    # Create a button in each column
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols[0].button('Extract Proveedores', key='button1'):
            extract_participantes_proveedores(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols[1].button('Extract Licitaciones', key='button2'):
            extract_licitacion(db)
            clean_licitacion(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols[2].button('Extract Asignaciones', key='button3'):
            extract_asignacion(db)
            clean_asignacion(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols2[0].button('Extract Compradores', key='button4'):
            extract_comprador(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols2[1].button('Extract Documentos Tender', key='button5'):
            extract_documentos_tender(db)
            clean_documentos_tender(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols2[2].button('Extract Item Adq', key='button6'):
            extract_item_adq(db)
    with st.spinner('Extrayendo datos de MongoDB...'):
        if cols3[0].button('Extract Item Tender', key='button7'):
            extract_item_tender(db)

    if cols3[1].button('Extract All Tables', key='button8'):
        extract_participantes_proveedores(db)
        extract_licitacion(db)
        clean_licitacion(db)
        extract_asignacion(db)
        clean_asignacion(db)
        extract_comprador(db)
        extract_documentos_tender(db)
        clean_documentos_tender(db)
        extract_item_adq(db)

    # Change the color of the 'Extract All Tables' button

    st.markdown("<br>", unsafe_allow_html=True)
    cols4 = st.columns([1, 1, 1])  # Create three columns
    inner_cols = cols4[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
    inner_cols[0].markdown(
        "<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>",
        unsafe_allow_html=True)  # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)  # Colocar la imagen


def download_results():
    st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    # Create a row of columns for the buttons
    cols = [st.columns(2) for _ in range(3)]

    filenames = [
        'Participantes_Proveedores',
        'Licitaciones',
        'Asignaciones',
        'Compradores',
        'Documentos_Tender',
        'Items_Adquisiciones',
        'Items_Tender'
    ]
    # Create a download button for each dataset
    filelinks = [
        path_config.contrataciones_processed_csv_path + 'participantes_proveedores_V2_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'licitacion_data_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'asignacion_data_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'comprador_data_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'documentos_tender_data_V2_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'items_adq_data_Raw.csv',
        path_config.contrataciones_processed_csv_path + 'tender_items_data_Raw.csv',
    ]

    # Ensure cols has enough elements
    while len(cols) < len(filelinks) // 2 + 1:
        cols.append([None, None])

    for i, (filename, filelink) in enumerate(zip(filenames, filelinks)):
        if i < len(filelinks) - 1 or len(filelinks) % 2 == 0:  # Regular case
            if cols[i // 2][i % 2].button(f'Download {filename}', key=f'download_{i}'):
                with st.spinner(f'Downloading {filename}...'):
                    href = create_download_link(filelinks[i], filenames[i])()
                    st.markdown(href, unsafe_allow_html=True)
        else:  # Special case for the last button when the number of elements is odd
            if st.button(f'Download {filename}', key=f'download_{i}'):
                with st.spinner(f'Downloading {filename}...'):
                    href = create_download_link(filelinks[i], filenames[i])()
                    st.markdown(href, unsafe_allow_html=True)

    # Add the 'Download All' button
    if st.button('Download All', key='download_all'):
        href = create_download_link2(filelinks, 'all_data.zip')()
        st.markdown(href, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    cols4 = st.columns([1, 1, 1])  # Create three columns
    inner_cols = cols4[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
    inner_cols[0].markdown(
        "<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>",
        unsafe_allow_html=True)  # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)


def clear_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')


def main():
    if not os.path.exists(config.path_config.data_path):
        os.makedirs(config.path_config.data_path)
        logger.info("Directory 'data' missing, creating 'data' directory.")
    if not os.path.exists(config.path_config.contrataciones_raw_unzip_path):
        os.makedirs(config.path_config.contrataciones_raw_unzip_path)
        logger.info("Directory %s missing, creating %s", config.path_config.contrataciones_raw_unzip_path,
                    config.path_config.contrataciones_raw_unzip_path)

    clear_directory(config.path_config.contrataciones_raw_unzip_path)

    with st.spinner(
            'Ejecutando scripts... Esto puede tardar unos minutos. No cambie de pestaña hasta que el proceso haya '
            'acabado!'):
        logger.info("Inicio de Descarga y Extracción de datos")
        # scripts = ["src/data_download_unzip.py"]
        # progress_bar = st.progress(0)  # Initialize progress bar
        # for i, script in enumerate(scripts):
        #     result = subprocess.run([sys.executable, script], check=False, text=True, capture_output=True)
        #     progress_percent = (i + 1) / len(scripts)  # Calculate progress percentage
        #     progress_bar.progress(progress_percent)  # Update progress bar
        #     if result.returncode != 0:
        #         logger.error(f"{script} failed with error:\n{result.stderr}")
        #         st.error(f"{script} failed with error:\n{result.stderr}")
        #         break

        progress_bar = st.progress(0)  # Initialize progress bar
        try:
            download_contrataciones_zip()
            progress_bar.progress(0.5)  # Update progress bar to 100% as we only have one function
            unzip()
            progress_bar.progress(1)  # Update progress bar to 100% as we only have one function
        except Exception as e:
            logger.error(f"download_and_unzip failed with error:\n{str(e)}")
            st.error(f"download_and_unzip failed with error:\n{str(e)}")


if __name__ == '__main__':
    st.markdown('''
                <h1 style='text-align: center; color: black; font-size: 30px;'>Servicio de ingeniería de datos para la extracción,
                transformación y carga del Programa de Anticorrupción.
                </h1> 
                '''
                , unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    # Sidebar
    st.sidebar.image('docs/images/SESNA-logo.png', use_column_width=True)

    st.sidebar.markdown(
        """
        La secretaria ejecutiva del Sistema Nacional Anticorrupción 
        (SESNA) es el organismo de apoyo técnico dedicado al combate 
        contra la corrupción en México.
        """
    )

    st.sidebar.markdown("<br>", unsafe_allow_html=True)

    st.sidebar.markdown(
        """
        Esta página ha sido desarrollada por [mottum](https://mottum.io/) con el fin de
        estandarizar, transformar y analizar los datos del Programa de anticorrupción.
        """
    )
    # Initialize session state variables
    if 'page' not in st.session_state:
        st.session_state.page = '1. Introducción'

    # Create navigation menu

    st.session_state.page = st.radio('Process',
                                     ['1. Introducción', '2. Descarga y unzip', '3. Extracción de datos de MongoDB',
                                      '4. Descarga de resultados'])

    # Display the selected page
    if st.session_state.page == '1. Introducción':
        show_intro()
    elif st.session_state.page == '2. Descarga y unzip':
        start_download_and_unzip()
    elif st.session_state.page == '3. Extracción de datos de MongoDB':
        start_extraction()
    elif st.session_state.page == '4. Descarga de resultados':
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
        Visita los siguientes links para más información:
        """
    )

    st.sidebar.markdown(
        """
    - [Link al repositorio](https://github.com/MottumData/Anticorruption_ETL_MEX)
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

# image_placeholder.image('docs/images/mottum.svg', width=500)
