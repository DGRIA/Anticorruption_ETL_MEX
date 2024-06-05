import config
from config import *
from src import data_download_unzip
from src.mongodb_utils import connect_to_mongodb, process_large_json
import time
import streamlit as st
import subprocess
import logging
import config
import sys
import os
import shutil

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
    inner_cols[0].markdown("<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>", unsafe_allow_html=True) # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True) 


def start_process():
    cols_button = st.columns([1, 3, 1])  # Create three columns for the button
    if cols_button[1].button('Pulsa para comenzar el proceso de descarga y limpieza de datos.',
                             key='start_process_button'):
        st.session_state.button_pressed = True
        st.session_state.main_running = True
        #main()

    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns([1, 1, 1])  # Create three columns
    inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
    inner_cols[0].markdown("<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>", unsafe_allow_html=True) # Center the text, change the font, and add padding
    inner_cols[2].image('docs/images/mottum2.png', use_column_width=True) 

def show_finished():
    if os.path.exists("data/merged_dataset.csv"):
        st.markdown("<h2 style='text-align: center;'>¡El dataset está listo!</h2>", unsafe_allow_html=True)
        cols = st.columns([1, 2, 1])
        with open("data/merged_dataset.csv", "rb") as file:
            button_clicked = cols[1].download_button(
                label="Pulsa aquí para descargar el dataset completo.",
                data=file,
                file_name="merged_dataset.csv",
                mime="text/csv",
            )
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns([1, 1, 1])  # Create three columns
        inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
        inner_cols[0].markdown("<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>", unsafe_allow_html=True) # Center the text, change the font, and add padding
        inner_cols[2].image('docs/images/mottum2.png', use_column_width=True)  # Colocar la im

    else:
        st.markdown(
            "<h2 style='text-align: center;'>Necesitas ejecutar el proceso antes de venir a esta pantalla.</h2>",
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

        cols = st.columns([1, 1, 1])  # Create three columns
        inner_cols = cols[2].columns([1, 1, 1, 1])  # Create two columns inside the middle column
        inner_cols[0].markdown("<p style='text-align: center; font-family: Comic Sans MS; padding-top: 12px; white-space: nowrap;'>Made with love</p>", unsafe_allow_html=True) # Center the text, change the font, and add padding
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

logger = logging.getLogger("Contrataciones")
logger.setLevel(logging.INFO)

def main():
    if not os.path.exists('data'):
            os.makedirs('data')
            print("Directory 'data' missing, creating data directory.")
    if not os.path.exists('data/Raw'):
        os.makedirs('data/productores_autorizados')
        print("Directory 'data/productores_autorizados' missing, creating data/productores_autorizados.")

    clear_directory('data/Raw')

    with st.spinner(
            'Ejecutando scripts... Esto puede tardar unos minutos. No cambie de pestaña hasta que el proceso haya acabado!'):
        logger.info("Inicio de Ejecución")
        scripts = ["src/data_download_unzip.py", "src/extraction_mongodb.py"]
        progress_bar = st.progress(0)  # Initialize progress bar
        for i, script in enumerate(scripts):
            result = subprocess.run([sys.executable, script], check=False, text=True, capture_output=True)
            progress_percent = (i + 1) / len(scripts)  # Calculate progress percentage
            progress_bar.progress(progress_percent)  # Update progress bar
            if result.returncode != 0:
                logger.error(f"{script} failed with error:\n{result.stderr}")
                break

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
    st.session_state.page = st.radio('Process', ['1. Introducción', '2. Descarga y unzip', '3. Extracción de datos de MongoDB'])

    # Display the selected page
    if st.session_state.page == '1. Introducción':
        show_intro()
    elif st.session_state.page == '2. Descarga y unzip':
        start_process()
    elif st.session_state.page == '3. Extracción de datos de MongoDB':
        show_finished()

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
    - [Jupyter](http://localhost:8888/lab) need to change to the correct link.
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
'''
De cara a usar el codigo en Streamlit habria que trabajar en preguntar al usuario si desea 
descargar de nuevo el json, si lo desea extraer, generar csv, parquet, etc.
'''

''' 
    1. Descarga de datos
    2. Extracción de datos
    3. Insertar datos en MongoDB
    4. Exportar datos a CSV
    5. Exportar datos a Parquet
    
    Para levantar contenedor de MongoDB (y no tener que instalarlo en la máquina local, aunque puedes instalarlo):
    docker run --name mongo -p 27017:27017 -d mongo:latest
    
    Para levantar compose con MongoDB y Jupyter:
    docker-compose up -d --build
    
    # Para ejecutar Streamlit modificar el archivo Dockerfile y ponerlo igual que Fertilizantes (Levanta Streamlit y Jupyter)
    
    
    logger.info("Inicio de Ejecución")
    start = time.time()
    db = connect_to_mongodb()
    print("Conectado a MongoDB")
    # data_download_unzip.download_contrataciones_zip() # Tarda unos minutos
    logger.info("Tiempo de descarga: %s", time.time() - start)
    start_zip = time.time()
    # data_download_unzip.unzip() # Tarda unos minutos
    logger.info("Tiempo de extracción: %s", time.time() - start_zip)
    end = time.time()

    db = connect_to_mongodb()
    print("Conectado a MongoDB")
    print("Revisado la colección")
    process_large_json(
        config.path_config.contrataciones_raw_unzip_path + CONTRATACIONES_JSON)  # Tarda mas de 20 minutos
    logger.info(f"Tiempo de ejecución: {end - start}")
    logger.info("Fin de Ejecución")
'''