# 🇲🇽 Proyecto de ETL Anticorrupción México 

## 📑 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Descripción del Código ETL](#descripción-de-archivos-en-src)
- [Notebooks EDA](#notebooks-eda)
- [Guía de Usuario](#guía-de-usuario)
- [Cómo Contribuir](#cómo-contribuir)
- [Autores](#autores)

## Descripción del Proyecto
Este proyecto de ETL (Extract, Transform, Load) está enfocado en la lucha contra la corrupción en México. Utiliza datos públicos relacionados con contrataciones y procesos de licitación, siguiendo el estándar de contrataciones abiertas (EDCA). El proyecto permite descargar, transformar y analizar datos utilizando diversas herramientas y tecnologías, incluyendo Docker, Streamlit y Jupyter Notebooks.

## Descripción del Código ETL
- **data_download_unzip.py**: Este archivo contiene un script en Python diseñado para descargar archivos zip de una URL especificada y descomprimirlos en un directorio de destino. Utiliza la biblioteca `requests` para manejar la descarga de archivos y `zipfile` para la extracción del contenido. Este script es esencial para la etapa inicial del proceso ETL, asegurando que los datos estén disponibles localmente para su posterior procesamiento y análisis.

- **extraction_mongodb.py**: Este archivo contiene un script en Python diseñado para extraer datos desde una base de datos MongoDB. Utiliza la biblioteca `pymongo` para conectarse a la base de datos y realizar consultas. Los datos extraídos se procesan y transforman para su posterior análisis y almacenamiento. Este script es fundamental en la fase de extracción del proceso ETL, asegurando que los datos necesarios sean recuperados y preparados correctamente para los siguientes pasos.

## Notebooks EDA

### 1. [Data Download & Unzip.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/1_Data%20Download%20&%20Unzip.ipynb)
Este notebook se encarga de descargar y descomprimir los datos necesarios para el análisis. Utiliza bibliotecas como `requests` para descargar archivos desde URLs especificadas y `zipfile` para descomprimir los archivos descargados en el directorio de trabajo.

### 2. [Extraction MongoDB.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/2_Extraction_MongoDB.ipynb)
En este notebook se realiza la extracción de datos desde una base de datos MongoDB. Se conecta a la base de datos utilizando `pymongo`, consulta las colecciones necesarias y extrae los datos relevantes para su posterior procesamiento y análisis.

### 3. [Data Cleaning Parquet.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/3_Data_Cleaning_Parquet.ipynb)
Este notebook está dedicado a la limpieza de datos y la conversión a formato Parquet. Utiliza `pandas` para cargar los datos, realizar operaciones de limpieza como manejo de valores nulos y duplicados, y finalmente guarda los datos limpios en archivos Parquet.

### 4.1. [EDA Licitacion.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.1_EDA_Licitacion.ipynb)
Realiza un análisis exploratorio de datos (EDA) específicamente en los datos de licitaciones. Examina la distribución de las licitaciones, analiza las características principales y visualiza las tendencias y patrones utilizando gráficos.

### 4.2. [EDA Asignacion.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.2_EDA_Asignacion.ipynb)
Este notebook realiza el EDA de los datos de asignación de contratos. Analiza la distribución de contratos asignados, la relación entre diferentes variables y visualiza los resultados para identificar posibles anomalías o patrones.

### 4.3. [EDA Participantes Proveedores.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.3_EDA_Participantes_Proveedores.ipynb)
Analiza los datos relacionados con los participantes y proveedores en los procesos de contratación. Incluye la exploración de datos sobre el número de participantes por licitación, los proveedores más frecuentes y la distribución de contratos entre proveedores.

### 4.4. [EDA Compradores.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.4_EDA_Compradores.ipynb)
Se centra en el análisis de los datos de los compradores. Examina quiénes son los compradores más activos, la cantidad de contratos gestionados por cada comprador y las características de las transacciones realizadas por estos compradores.

### 4.5. [EDA Documentos Tender.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.5_EDA_Documentos_Tender.ipynb)
Este notebook realiza un análisis exploratorio de los documentos asociados a las licitaciones. Revisa la cantidad y tipo de documentos presentados, su relación con los resultados de las licitaciones y visualiza la información para obtener insights útiles.


## Guía de Usuario

### Clonar el Repositorio
Para comenzar, debe clonar este repositorio en su máquina local utilizando el siguiente comando:

```bash 
git clone https://github.com/MottumData/Anticorruption_ETL_MEX.git
```
### Navegar al Directorio del Proyecto
Después de clonar el repositorio, navegue al directorio del proyecto:

```bash
cd Anticorruption_ETL_MEX
```

### Ejecutar el Proyecto
El proyecto utiliza Docker para facilitar la configuración y ejecución del entorno. A continuación, se indican los pasos para iniciar el contenedor Docker y acceder a las diferentes funcionalidades:

```bash
docker-compose up --build
```

### Acceder a las Interfaces de Usuario:
**Interfaz de Streamlit:** [http://localhost:8501/](http://localhost:8501/)
Aquí encontrará una interfaz de usuario en Streamlit donde podrá ejecutar cada uno de los procesos:

- **Descarga y Unzip:** Permite descargar y descomprimir los archivos de datos.
- **Extracción de Datos de MongoDB:** Genera tablas a partir de los datos extraídos de MongoDB.

**Jupyter Notebooks:** [http://localhost:8888/](http://localhost:8888/)
Acceda a los notebooks de Jupyter con todo el código en Python, incluyendo el Análisis Exploratorio de Datos (EDA).

## Cómo Contribuir

Damos la bienvenida a contribuciones de la comunidad:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature-branch`).
3. Confirma tus cambios (`git commit -am 'Agregar nueva característica'`).
4. Empuja a la rama (`git push origin feature-branch`).
5. Crea un nuevo Pull Request.

## Autores

**Mottum Analytica**

- Página web: [Mottum](https://mottum.io/)
- [LinkedIn](https://www.linkedin.com/company/mottum/) <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" height="20">
- Email de contacto: hello@mottum.io

