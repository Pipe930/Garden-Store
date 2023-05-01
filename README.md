# API Rest Garden Store

Esta es una api rest creada con python junto con django, con una base de datos mysql. Para el proyecto de garden store que es una aplicacion web de venta de productos de jardineria

Tecnologias:
    - Python (Version 3.10.9)
    - Django con Django Rest Framework
    - Base de Datos relacional MySql

# Instalacion de Dependencias

Para poder instalar las dependencias del proyecto esta adjunto un archivo llamado requirements.txt, pero antes crear un entorno virtual con python con el comando:

    python -m venv env 

despues de haber ejecutado el comando, se creara una carpeta con el entorno virtual, para activar el entorno virtual con el archivo activate.bat que esta en la ruta de env\Scripts\activate.bat, ahora activado el entorno virtual instalar las dependencias del proyecto, para instalar las dependencias del proyecto es con el comando:

    pip install -r requirements.txt p

Posteriormente se instalaran las dependencias para poder ejecutar el proyecto.

# Migraciones

Para poder hacer las migraciones de las tablas para la base de datos, primero haber configurado los datos en el artivo settings.py, cuando te hayas conectado con la base de datos tienes que ejecutar el comando:

    python manage.py makemigrations

Creara los archivos de migracion y posteriormente el comando:

    python manage.py migrate 

Se realizaran todas las migraciones a la base de datos creando las tablas.

# Ejecucion

Para la ejecucion del proyecto tener activado el entorno virtual con las dependencias instaladas y posteriormente con el comando:

    python manage.py runserver (numero de puerto opcional)

El numero de puerto es opcional, si no pondes el puerto el servidor correra por el puerto 8000 en localhost

