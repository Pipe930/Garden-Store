# API Rest Garden Store

Esta es una api rest creada con python junto con django, con una base de datos mysql.

# Instalacion de Dependencias

Para poder instalar las dependencias del proyecto esta adjunto un archivo llamado requirements.txt, pero antes crear un entorno virtual con python con el comando python -m venv env y despues con el comando pip install -r requirements.txt, posteriormente se instalaran las dependencias para poder ejecutar el proyecto.

# Ejecucion

Para poder ejecutarlo primero hacer las migraciones de las tablas para la base de datos, cuando te hayas conectado con la base de datos tienes que ejecutar el comando python manage.py makemigrations y posteriormente python manage.py migrate y se realizaran las migraciones.

Y por ultimo con el comando python manage.py runserver correras el servidor local.
