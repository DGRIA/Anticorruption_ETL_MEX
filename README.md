## Sistema de Descarga y transformación de los Datos de Contrataciones Públicas (Sistema 6) 👇


**Objetivo**: Descarga y transformación de datos del histórico de contratos de México para facilitar las labores de análisis y extracción de conocimiento.

*Esta herramienta digital forma parte de la Secretaría Ejecutiva del Sistema Nacional de Anticorrupción de la República de México [https://www.sesna.gob.mx/](www.sesna.gob.mx)*

- ![Static Badge](https://img.shields.io/badge/Language-Python-blue?style=plastic)
- ![Static Badge](https://img.shields.io/badge/Language-pySpark-green?style=plastic)
- ![Static Badge](https://img.shields.io/badge/Language-MongoDB-yellow?style=plastic)
- ![Static Badge](https://img.shields.io/badge/Status-Development-orange?style=for-the-badge)
- ![Static Badge](https://img.shields.io/badge/Coverage-40%25-blue?style=for-the-badge)


## Tabla de contenidos:
---
- [Descripción y contexto](#descripción-y-contexto)
- [Guía de usuario](#guía-de-usuario)
- [Guía de instalación](#guía-de-instalación)
- [Cómo contribuir](#cómo-contribuir)
- [Código de conducta](#código-de-conducta)
- [Autor/es](#autores)
- [Información adicional](#información-adicional)
- [Licencia](#licencia)
- [Limitación de responsabilidades - Solo BID](#limitación-de-responsabilidades)

## Descripción y contexto
---
Este repositorio aloja el código y la documentación encargados del procesamiento y limpieza de los datos del Sistema Seis de la [Plataforma Nacional Digital](https://www.plataformadigitalnacional.org/contrataciones). A alto nivel, este código en python se encarga de seguir los siguientes pasos:

1. Descarga de la base de datos y descompresión del archivo .zip a json.
2. Creación de las 7 tablas en formato .csv
3. Limpieza de datos

Adicionalmente, este repositorio tendrá la documentación en formato Word y pdf para facilitar la lectura y entendimiento del proceso. Esta información se pueden encontrar en la carpeta /DOCUMENTACIÓN

### 1. Descarga de la base de datos y descompresión del archivo .zip a json.
Scripts en python encargados de descargar de la web (Compranetinfo) el dataset comprimido en formato .zip. Este script también se encargan de descomprimir y renombrar el archivo para llevar un buen control de versiones.

Este proceso se hace de manera semi-automática, es decir, el usuario es responsable de configurar los ambientes, instalar las herramientas en local y ejecutar el script. Visitar la carpeta de Tutoriales para más información.

Como proceso adicional, se diseña un sistema automático de descarga de datos en la nube; sin embargo este repositorio sólo incluye el diseño teórico de dicho sistema (Ver carpeta documentación Entregable 1).

  **-->** Web de decarga de datos: https://compranetinfo.hacienda.gob.mx/dabiertos/contrataciones_arr.json.zip

### 2. Creación de las 7 tablas en formato .csv
  _...Esta sección se encuentra en progreso..._
El formato de origen de estos datos presenta dos inconvenientes que este código resuelve:

- Formato json: El formato de los datos sigue el estándar EDCA, un formato json con múltiples jerarquías en sus campos.
- Tamaño del archivo: El archivo json descomprimido pesa 25 GB, lo que hace que para el procesado se necesiten técnicas optimizadas de computación.

El Entregable número 2 dentro de la carpeta de Documentos explica la metodología seguida para resolver estos dos inconvenientes.

### 3. Limpieza de datos
  _...Esta sección se encuentra en progreso..._

El proceso de limpieza de datos se centra en la identificación de las siguientes inconsistencias.
- Estadísticas descriptivas por tipo de procedimientos.
- Estadísticas de calidad de la información
- Duplicado de expedientes con más de un estatus.
- Duplicado de expedientes con más de una fecha de contratación
- Registro de asignaciones duplicados

## Estructura de carpetas

**Limpieza datos de contrataciones**

- `README.md`  # Descripción del proyecto, instrucciones de instalación y uso
- `notebooks`  # Jupyter notebooks (para exploración y presentación)
  - `1_Data Download & Unzip.ipynb` # Jupyter Notebook para descargar los datos y descomprimirlos
  - `2_Extraction_MongoDB.ipynb` # Lectura de los datos en Mongo y generación de tablas (de una muestra pequeña de los datos)
  - `3_Extraction_Pyspark.ipynb` # Lectura de los datos en Pyspark y generación de tablas (del universo de datos completo)
  - `3_Data Cleaning.ipynb` # Jupyter Notebook para la limpieza de los datos
  - `test pysparkjson.ipynb` # Jupyter Notebook de Test
- `docs` # Documentación (alternativamente /doc)
  - `Entregable 1.pdf`
  - `Entregable 2.pdf`
  - `Entregable 3.pdf` *En progreso*
  - `Anexo1_Diagrama ER de base de datos EDCA.pdf`
  - `Relación variables EDCA-MODELO ER.xlsx`
- `data`       # Scripts para descargar o generar datos (En github se mantienen vacíos)
  - `raw`
  - `processed`
- `LICENSE.txt`      # Licencia del proyecto
- `requirements.txt` # Dependencias del proyecto
- `.gitignore` # Archivos y carpetas a ignorar en git

## Guía de instalación
---
Antes de ejecutar el código, el usuario debe asegurarse que tiene un ambiente preparado con todas las dependencias intaladas. Este conjunto de datos es muy pesado y el proceso puede demorarse si se corre en una máquina sin las capacidades adecuadas. Por razones externas al proyecto se ha decidido no ejecutar el proceso en una nube virtual, sino en una máquina física con las siguientes características:
  - Windows
  - RAM de 32 Gb
  - 4 Cores

Durante esta consultoría, y para replicar estas características, se ha replicado esta máquina en un ambiente de Azure.

Siga los siguientes pasos para instalar todas las herramientas necesarias:
  1. Instale python. Se recomienda la versión de Anaconda.
  2. Instale Pyspark, para ello necesita instalar:
    - Java
    - Editar las variables de ambiente
    - Instalar Pyspark
    Consulte el siguiente link para más información: https://www.datacamp.com/tutorial/installation-of-pyspark


Antes de ejecutar el código, el usuario debe asegurarse que tiene un ambiente de python con todas las dependencias instaladas. En Mottum se lo hemos querido hacer fácil y por eso te recomendamos que crees un nuevo "Environment" con las librerías necesarias. Para eso te recomentamos que sigas los siguientes pasos:

1. Crea un ambiente
`python3 -m venv [nombre del environment]`

2. Activa el ambiente
`source [nombre del enviromenmt]/bin/activate #Para iOS`
`source [nombre del enviromenmt]/bin/activate.bat #Para Windows`

3. Instala todas las librerías necesarias
`pip install -r requirements.txt`

Una vez instalados esos componentes, el usuario debe ejecutar los scripts en el siguiente orden:

_La guía de instalación debe contener de manera específica:_
_- Los requisitos del sistema operativo para la compilación (versiones específicas de librerías, software de gestión de paquetes y dependencias, SDKs y compiladores, etc.)._
_- Las dependencias propias del proyecto, tanto externas como internas (orden de compilación de sub-módulos, configuración de ubicación de librerías dinámicas, etc.)._
_- Pasos específicos para la compilación del código fuente y ejecución de tests unitarios en caso de que el proyecto disponga de ellos._

## Guía de usuario
---
_Explica los pasos básicos sobre cómo usar la herramienta digital. Es una buena sección para mostrar capturas de antalla o gifs que ayuden a entender la herramienta digital._
Este código se debe ejecutar manualmente cada vez que el usuario desee actualizar el historial de datos de contrataciones públicas. Para ello el usuario deberá seguir los siguientes pasos:
1. _In progress_
2. _In progress_
3. _..._

## Tutoriales
---
_Paso a paso de cómo instalar la herramienta digital. Videos a Youtube?_

### Dependencias
Descripción de los recursos externos que generan una dependencia para la reutilización de la herramienta digital (librerías, frameworks, acceso a bases de datos y licencias de cada recurso). Es una buena práctica describir las últimas versiones en las que ha sido probada la herramienta digital. 

    pip install -r requirements.txt

## Cómo contribuir
---
Esta sección explica a desarrolladores cuáles son las maneras habituales de enviar una solicitud de adhesión de nuevo código (“pull requests”), cómo declarar fallos en la herramienta y qué guías de estilo se deben usar al escribir más líneas de código. También puedes hacer un listado de puntos que se pueden mejorar de tu código para crear ideas de mejora.

## Código de conducta 
---
El código de conducta establece las normas sociales, reglas y responsabilidades que los individuos y organizaciones deben seguir al interactuar de alguna manera con la herramienta digital o su comunidad. Es una buena práctica para crear un ambiente de respeto e inclusión en las contribuciones al proyecto. 

La plataforma Github premia y ayuda a los repositorios dispongan de este archivo. Al crear CODE_OF_CONDUCT.md puedes empezar desde una plantilla sugerida por ellos. Puedes leer más sobre cómo crear un archivo de Código de Conducta (aquí)[https://help.github.com/articles/adding-a-code-of-conduct-to-your-project/]

## Autor/es
---
Nombra a el/los autor/es original/es. Consulta con ellos antes de publicar un email o un nombre personal. Una manera muy común es dirigirlos a sus cuentas de redes sociales.

## Información adicional
---
Esta es la sección que permite agregar más información de contexto al proyecto como alguna web de relevancia, proyectos similares o que hayan usado la misma tecnología.

## Licencia 
---

La licencia especifica los permisos y las condiciones de uso que el desarrollador otorga a otros desarrolladores que usen y/o modifiquen la herramienta digital.

Incluye en esta sección una nota con el tipo de licencia otorgado a esta herramienta digital. El texto de la licencia debe estar incluído en un archivo *LICENSE.md* o *LICENSE.txt* en la raíz del repositorio.

Si desconoces qué tipos de licencias existen y cuál es la mejor para cada caso, te recomendamos visitar la página https://choosealicense.com/.
