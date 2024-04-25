## Sistema de Descarga y transformación de los Datos de Contrataciones Públicas (Sistema 6) 👇


*Esta herramienta digital forma parte de la Secretaría Ejecutiva del Sistema Nacional de Anticorrupción de la República de México [https://www.sesna.gob.mx/](www.sesna.gob.mx)*
- code coverage percentage: ![coverage](https://img.shields.io/badge/coverage-10%25-yellowgreen)
- stable release version: ![version](https://img.shields.io/badge/version-1.2.3-blue)
- package manager release: ![gem](https://img.shields.io/badge/gem-2.2.0-blue)

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
Este repositorio aloja el código y la documentación encargados del procesamiento y limpieza de los datos del Sistema Seis de la [Plataforma Nacional Digital](https://www.plataformadigitalnacional.org/contrataciones). Concretamente, el presente código en python se encarga de seguir los siguientes pasos:

1. Descarga de la base de datos
2. Carga de datos en MongoDB y creación de archivos .csv
3. Limpieza de datos

Adicionalmente, este repositorio tendrá la documentación en formato Word y pdf para facilitar la lectura y entendimiento del proceso. Esta información se pueden encontrar en la carpeta /DOCUMENTACIÓN

### 1. Descarga de la base de datos
    Scripts en python encargados de descargar de la web (XXX) el dataset comprimido en formato .zip. Este script también se encargan de descomprimir y renombrar el archivo para llevar un buen control de versiones.

    Este proceso se hace de manera semi-automática, es decir, el usuario es responsable de configurar los ambientes, instalar el MongoDB en local y ejecutar el script. En la documentación se provee una guía de todos estos pasos.

    Como proceso adicional, se diseña un sistema automático de descarga de datos en la nube; sin embargo este repositorio sólo incluye el diseño teórico de dicho sistema (Ver documentación).

### 2. Carga de datos en MongoDB y creación de archivos .csv
_...In progress..._

### 3. Limpieza de datos
    _...In progress..._

## Estructura de carpetas

**Limpieza datos de contrataciones**

- `README.md`  # Descripción del proyecto, instrucciones de instalación y uso
- `.gitignore` # Archivos y carpetas a ignorar en git
- `bin`        # Scripts ejecutables y binarios
- `data`       # Scripts para descargar o generar datos
  - `raw`
  - `processed`
- `notebooks`  # Jupyter notebooks (para exploración y presentación)
- `documentación` # Documentación (alternativamente /doc)
  - `reporte1.pdf`
  - `reporte2.pdf`
  - `reporte3.pdf`
- `src`        # Código fuente del proyecto
  - `__init__.py`
  - `data`     # Scripts para configurar tu base de datos MongoDB
  - `1.1 Data Download.ipynb` # Script para descargar los datos
- `LICENSE.txt`      # Licencia del proyecto
- `requirements.txt` # Dependencias del proyecto

## Guía de usuario
---
_Explica los pasos básicos sobre cómo usar la herramienta digital. Es una buena sección para mostrar capturas de antalla o gifs que ayuden a entender la herramienta digital._
Este código se debe ejecutar manualmente cada vez que el usuario desee actualizar el historial de datos de contrataciones públicas. Para ello el usuario deberá seguir los siguientes pasos:
1. _In progress_
2. _In progress_
3. _..._
 	
## Guía de instalación
---
Antes de ejecutar el código, el usuario debe asegurarse que tiene instalados los siguientes componentes:
- Python
- MongoDB

Una vez instalados esos componentes, el usuario debe ejecutar los scripts en el siguiente orden:

_La guía de instalación debe contener de manera específica:_
_- Los requisitos del sistema operativo para la compilación (versiones específicas de librerías, software de gestión de paquetes y dependencias, SDKs y compiladores, etc.)._
_- Las dependencias propias del proyecto, tanto externas como internas (orden de compilación de sub-módulos, configuración de ubicación de librerías dinámicas, etc.)._
_- Pasos específicos para la compilación del código fuente y ejecución de tests unitarios en caso de que el proyecto disponga de ellos._

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
