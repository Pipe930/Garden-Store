## Página Web Garden-Store 🌱

Este es un proyecto de una página web de ventas y compras de productos de jardinería llamada gardenstore.

## Tecnologías

- Python 3.10.4
- HTML5
- CSS3
- Bootstrap 5.2.0
- MySQL 8.0

## Entorno Local

Lo primero que tienes que hacer para poder ejecutar el proyecto es clonar el repositorio en tu computadora:

```bash
git clone https://github.com/Pipe930/Garden-Store.git
cd ./Garden-Store
```

Ahora que clonamos el repositorio, tenemos que crear un entorno virtual de Python para la instalación de dependencias del proyecto:

```bash
python -m venv env
virtualenv env

# Windows
env\Scripts\activate

# Linux o Mac
source env/bin/activate
```

> [!NOTE]
> Si quieres utilizar virtualenv, tienes que instalarlo con pip `pip install virtualenv`.

### Instalación de Dependencias

Con el entorno virtual de Python activado y configurado, instalamos las dependencias del proyecto:

    pip install -r requirements.txt

### Variables de Entorno

Ahora tenemos que configurar las variables de entorno, en la carpeta del proyecto deje un archivo `.env.example` como ejemplo de las variables de entorno que se tienen que utilizar:

```bash
SECRET_KEY='secret-key'

DATABASE_NAME='namedatabase'
DATABASE_USER='root'
DATABASE_PASSWORD='password'
DATABASE_HOST='localhost'
DATABASE_PORT=3306

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='example@gmail.com'
EMAIL_HOST_PASSWORD = 'password12324'
```

> [!NOTE]
> Para la variable de entorno `SECRET_KEY` tienes que ingresar una clave secreta válida para que el proyecto pueda ejecutarse. Puedes conseguir una clave en la siguiente página:**[Djecrety](https://djecrety.ir/)**.

### Migraciones

Con las variables de entorno configuradas, tenemos que realizar las migraciones de los modelos para que se creen las tablas en la base de datos:

```bash
python manage.py makemigrations
python manage.py migrate
```

Con esto se migrarán los modelos a la base de datos y se crearán las tablas correspondientes para el funcionamiento de la aplicación.

### Creación Super Usuario

Ahora que tenemos todo configurado, creemos un superusuario para que puedas acceder a algunas de las funcionalidades de la aplicación que requieren permisos de administración:

```bash
python manage.py createsuperuser
```

### Ejecución

Con todo listo y configurado, ejecutemos el proyecto con el siguiente comando:

    python manage.py runserver

Listo!!, si todo salio bien ya tienes el proyecto corriento en tu computadora de manera local

## Entorno Docker

Lo primero que tienes que hacer para poder ejecutar el proyecto es clonar el repositorio en tu computadora:

```bash
git clone https://github.com/Pipe930/Garden-Store.git
cd ./Garden-Store
```

Ahora espero que tengas instalado en tu computadora el software de contenedores Docker

### Variables de Entorno

Primero, tenemos que configurar las variables de entorno necesarias para la ejecución del proyecto a través de Docker.

```bash
SECRET_KEY='secret-key'

DATABASE_NAME='namedatabase'
DATABASE_USER='root'
DATABASE_PASSWORD='password'
DATABASE_HOST='localhost'
DATABASE_PORT=3306

EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST='smtp.gmail.com'
EMAIL_HOST_USER='example@gmail.com'
EMAIL_HOST_PASSWORD = 'password12324'
```

> [!NOTE]
> Para la variable de entorno `SECRET_KEY` tienes que ingresar una clave secreta válida para que el proyecto pueda ejecutarse. Puedes conseguir una clave en la siguiente página:**[Djecrety](https://djecrety.ir/)**.

### Creación de la Imagen

Ahora que tenemos las variables de entorno configuradas, creemos la imagen de Docker del proyecto:

```bash
docker compose build
```

### Ejecución

Con la imagen de Docker ya creada ejecutaremos el proyecto a traves de Docker:

```bash
docker compose up
```

Si todo salio bien, ya tienes el proyecto corriendo con Docker, igualmente asegúrate de revisar cualquier detalle o error específico que haya ocurrido en el proyecto.
