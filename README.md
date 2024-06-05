# 🇲🇽 Proyecto de ETL Anticorrupción México 

## 📑 Tabla de Contenidos
- [Descripción del Proyecto](#descripción-del-proyecto)
- [Descripción del Código Principal](#descripción-de-archivos-en-src)
- [Guía de Usuario](#guía-de-usuario)
- [Cómo Contribuir](#cómo-contribuir)
- [Autores](#autores)

## Descripción del Proyecto
Este proyecto de ETL (Extract, Transform, Load) está enfocado en la lucha contra la corrupción en México. Utiliza datos públicos relacionados con contrataciones y procesos de licitación, siguiendo el estándar de contrataciones abiertas (EDCA). El proyecto permite descargar, transformar y analizar datos utilizando diversas herramientas y tecnologías, incluyendo Docker, Streamlit y Jupyter Notebooks.

### escripción del Código Principal
- **data_download_unzip.py**: Este archivo contiene un script en Python diseñado para descargar archivos zip de una URL especificada y descomprimirlos en un directorio de destino. Utiliza la biblioteca `requests` para manejar la descarga de archivos y `zipfile` para la extracción del contenido. Este script es esencial para la etapa inicial del proceso ETL, asegurando que los datos estén disponibles localmente para su posterior procesamiento y análisis.

- **extraction_mongodb.py**: Este archivo contiene un script en Python diseñado para extraer datos desde una base de datos MongoDB. Utiliza la biblioteca `pymongo` para conectarse a la base de datos y realizar consultas. Los datos extraídos se procesan y transforman para su posterior análisis y almacenamiento. Este script es fundamental en la fase de extracción del proceso ETL, asegurando que los datos necesarios sean recuperados y preparados correctamente para los siguientes pasos.

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

