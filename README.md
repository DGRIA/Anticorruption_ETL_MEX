# 🇲🇽 Proyecto de ETL Anticorrupción México

## 📑 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Descripción del Código ETL](#descripción-de-archivos-en-src)
- [Notebooks EDA](#notebooks-eda)
- [Guía de Usuario](#guía-de-usuario)
- [Cómo Contribuir](#cómo-contribuir)
- [Autores](#autores)

## Descripción del Proyecto

Este proyecto de ETL (Extract, Transform, Load) está enfocado en la lucha contra la corrupción en México. Utiliza datos
públicos relacionados con contrataciones y procesos de licitación, siguiendo el estándar de contrataciones abiertas (
EDCA). El proyecto permite descargar, transformar y analizar datos utilizando diversas herramientas y tecnologías,
incluyendo Docker, Streamlit y Jupyter Notebooks.

## Estructura del Proyecto

Este proyecto está estructurado en varios directorios, cada uno con un propósito específico. Sus funciones son las
siguientes:

- `data/`: Contiene los datos de entrada y salida del proyecto. Así como los diccionarios de datos.
- `docs/`: Contiene la documentación del proyecto.
- `logs/`: Contiene los logs o registros generados por el proyecto.
- `src/`: Contiene el código fuente del proyecto.
- `src/notebooks`: Contiene los Jupyter Notebooks.
- `tests/`: Contiene los tests del proyecto.
- `/`: Contiene los archivos de configuración y scripts de ejecución.

## Descripción del Código ETL

- **data_download_unzip.py**: Este archivo contiene un script en Python diseñado para descargar archivos zip de una URL
  especificada y descomprimirlos en un directorio de destino. Utiliza la biblioteca `requests` para manejar la descarga
  de archivos y `zipfile` para la extracción del contenido. Este script es esencial para la etapa inicial del proceso
  ETL, asegurando que los datos estén disponibles localmente para su posterior procesamiento y análisis.

- **extraction_mongodb.py**: Este archivo contiene un script en Python diseñado para extraer datos desde una base de
  datos MongoDB. Utiliza la biblioteca `pymongo` para conectarse a la base de datos y realizar consultas. Los datos
  extraídos se procesan y transforman para su posterior análisis y almacenamiento. Este script es fundamental en la fase
  de extracción del proceso ETL, asegurando que los datos necesarios sean recuperados y preparados correctamente para
  los siguientes pasos.

## Notebooks EDA

### 1. [Data Download & Unzip.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/1_Data%20Download%20&%20Unzip.ipynb)

Este notebook se encarga de descargar y descomprimir los datos necesarios para el análisis. Utiliza bibliotecas
como `requests` para descargar archivos desde URLs especificadas y `zipfile` para descomprimir los archivos descargados
en el directorio de trabajo.

### 2. [Extraction MongoDB.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/2_Extraction_MongoDB.ipynb)

En este notebook se realiza la extracción de datos desde una base de datos MongoDB. Se conecta a la base de datos
utilizando `pymongo`, consulta las colecciones necesarias y extrae los datos relevantes para su posterior procesamiento
y análisis.

### 3. [Data Cleaning Parquet.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/3_Data_Cleaning_Parquet.ipynb)

Este notebook está dedicado a la limpieza de datos y la conversión a formato Parquet. Utiliza `pandas` para cargar los
datos, realizar operaciones de limpieza como manejo de valores nulos y duplicados, y finalmente guarda los datos limpios
en archivos Parquet.

### 4.1. [EDA Licitacion.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.1_EDA_Licitacion.ipynb)

Realiza un análisis exploratorio de datos (EDA) específicamente en los datos de licitaciones. Examina la distribución de
las licitaciones, analiza las características principales y visualiza las tendencias y patrones utilizando gráficos.

### 4.2. [EDA Asignacion.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.2_EDA_Asignacion.ipynb)

Este notebook realiza el EDA de los datos de asignación de contratos. Analiza la distribución de contratos asignados, la
relación entre diferentes variables y visualiza los resultados para identificar posibles anomalías o patrones.

### 4.3. [EDA Participantes Proveedores.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.3_EDA_Participantes_Proveedores.ipynb)

Analiza los datos relacionados con los participantes y proveedores en los procesos de contratación. Incluye la
exploración de datos sobre el número de participantes por licitación, los proveedores más frecuentes y la distribución
de contratos entre proveedores.

### 4.4. [EDA Compradores.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.4_EDA_Compradores.ipynb)

Se centra en el análisis de los datos de los compradores. Examina quiénes son los compradores más activos, la cantidad
de contratos gestionados por cada comprador y las características de las transacciones realizadas por estos compradores.

### 4.5. [EDA Documentos Tender.ipynb](https://github.com/MottumData/Anticorruption_ETL_MEX/blob/eda_scripts/src/Notebooks/4.5_EDA_Documentos_Tender.ipynb)

Este notebook realiza un análisis exploratorio de los documentos asociados a las licitaciones. Revisa la cantidad y tipo
de documentos presentados, su relación con los resultados de las licitaciones y visualiza la información para obtener
insights útiles.

## Guía de Usuario

### Ejecución Local :house: :computer:

Para la ejecución de este proyecto en su máquina local, son necesarios los siguientes requerimientos:

- Python 3.9-3.11
- MongoDB

Se recomienda el uso de un entorno virtual para la ejecución de este proyecto. Para crear un entorno virtual puede
consultar la siguiente documentación:

- [Entornos Virtuales en Python](https://docs.python.org/3/library/venv.html)
- [Entornos Virtuales en Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html)
- [Entornos Virtuales en Pipenv](https://pipenv-es.readthedocs.io/es/stable/basics.html)

Una vez creado y activado el entorno virtual siga los siguientes pasos para ejecutar el proyecto:

1. **Clonar el Repositorio**. Para comenzar, debe clonar este repositorio en su máquina local utilizando el siguiente
   comando:

```bash 
git clone https://github.com/MottumData/Anticorruption_ETL_MEX.git
```

2. **Navegar al directorio del proyecto**. Después de clonar el repositorio, navegue al directorio del proyecto:

```bash
cd Anticorruption_ETL_MEX
```

3. **Instalar dependencias** Para instalar las dependencias del proyecto, ejecute el siguiente comando:

```bash
pip install -r requirements.txt
```

4. **Ejecutar el proyecto**. Para ejecutar el proyecto, ejecute el siguiente comando:

```bash 
streamlit run main.py
```

A continuación, se mostrará un mensaje similar al siguiente:

```bash
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://0.0.0.0:8501
```

### Ejecución en Docker :whale:

El proyecto utiliza Docker para facilitar la configuración y ejecución del entorno. Para ello puede descargar la
herramienta Docker Desktop desde el siguiente enlace:

- [Docker Desktop](https://www.docker.com/products/docker-desktop)

A continuación, se indican los pasos para iniciar el contenedor Docker y acceder a las diferentes funcionalidades.

1. **Clonar el Repositorio**. Para comenzar, debe clonar este repositorio en su máquina local utilizando el siguiente
   comando:

```bash 
git clone https://github.com/MottumData/Anticorruption_ETL_MEX.git
```

2. **Navegar al directorio del proyecto**. Después de clonar el repositorio, navegue al directorio del proyecto:

```bash
cd Anticorruption_ETL_MEX
```

3. **Construir y ejecutar el contenedor Docker**. Para construir y ejecutar el contenedor Docker, ejecute el siguiente
   comando:

```bash
docker-compose up --build # -d para ejecutar en segundo plano
```

Una vez ejecutado el contenedor de Docker, podrá acceder a las interfaces de usuario a través de los siguientes enlaces:

- **Interfaz de Streamlit**: [http://localhost:8502/](http://localhost:8502/)
- **Jupyter Notebooks**: [http://localhost:8889/](http://localhost:8889/)

### Descargar la última versión

Para usar la última versión del proyecto, sitúese en la carpeta del proyecto y ejecute el siguiente comando:

```bash
git pull
```

A continuación puede ejecutar el proyecto con la última versión siguiendo los pasos de ejecución anteriores.

## Autores

**Mottum Analytica**

- Página web: [Mottum](https://mottum.io/)
- [LinkedIn](https://www.linkedin.com/company/mottum/) <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" height="20">
- Email de contacto: hello@mottum.io