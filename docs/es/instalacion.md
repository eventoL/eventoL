# Base de datos

Nosotros estamos usando postgres. Para desarrollar existen 2 opciones:

## Usar la base de datos desde un container de docker

Correr el container:

```sh
docker run --name eventol-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=eventol -e POSTGRES_DB=eventol -p 5432:5432 -d postgres
```
Y la base de datos ahora esta mágicamente habilitada en localhost:5432!

Dependencias necesarios para la maquina servidor (probado para Debian jessie y sid):

```sh
$ sudo apt-get install python build-essential python-setuptools python-dev python-pip
$ sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
$ sudo apt-get install libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev
$ sudo apt-get install jpegoptim optipng
$ sudo apt-get install libffi-dev libxml2-dev libxslt1-dev
$ sudo apt-get install postgresql-server-dev-9.4
```

## Instalación en sistemas basados en Debian (jessie+):

Instalamos postgres, python y mas dependencias
```sh
$ sudo apt-get install python build-essential python-setuptools python-dev python-pip
$ sudo apt-get install postgresql postgresql-client-9.4 postgresql-server-dev-9.4 
$ sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
$ sudo apt-get install postgresql-9.4-postgis-2.2
$ sudo apt-get install libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev
$ sudo apt-get install jpegoptim optipng
```

Configuración de postgres
```sh
$ sudo passwd postgres
$ sudo su - postgres

$ pg_dropcluster --stop 9.4 main
$ pg_createcluster --start -e UTF-8 9.4 main

$ psql postgres

postgres=# ALTER ROLE postgres PASSWORD '<password>';
(ctrl-d)
$ createuser --createdb eventol
postgres=# ALTER ROLE eventol PASSWORD '<password>';

$ psql

postgres# CREATE USER eventol PASSWORD 'my_passwd';
postgres# CREATE DATABASE eventol OWNER eventol ENCODING 'utf8';
```

## Si estas buscando alguna herramienta de administración para la base de datos

```sh
$ sudo apt-get install pgadmin3
```

# Dependencias de Python/Django

### Instalar las dependencias de python

```sh
$ pip install -U -r requirements.txt
```

### Bower
Nosotros estamos usando bower para dependencias en el frontend. Instalación:

* [Instalar npm y nodejs](https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager)
* [Instalar bower](http://bower.io/#install-bower)
* Instalar dependencias de bower:

```sh
@/project-root$ bower install
```

### Compilar less de desarrollo

```sh
$ sudo npm install -g less

```

### Compilando

Todo el tiempo que generamos cambios a los archivos less, es necesario que se compilen de nuevo.
También, la primera vez que clonas del repo, es necesario que compiles los less.

```sh
@/project-root$ lessc manager/static/manager/less/flisol.less > manager/static/manager/css/flisol.css
@/project-root$ lessc manager/static/manager/less/flisol-bootstrap.less > manager/static/manager/css/flisol-bootstrap.css
```

### Conficuración de Django

Primero que todo, hay que cambiar configuraciones en el settings.py URLS, PATHS, DATABASE y EMAIL con tu configuración determinada.

Entonces, cargamos la base de datos y preparamos los estáticos:

```sh
$ python manage.py migrate
$ python manage.py makemigrations manager
$ python manage.py migrate
$ python manage.py syncdb
$ python manage.py collectstatic
```

### Si estas buscando cargar datos de ejemplo para probar la aplicación

```sh
$ python manage.py loaddata manager/initial_data/initial_data.json
$ python manage.py loaddata manager/initial_data/security.json
$ python manage.py loaddata manager/initial_data/software.json
$ python manage.py loaddata manager/initial_data/attendee_data.json
$ python manage.py loaddata manager/initial_data/email_addresses.json
```

### Actualizar traducciones

```sh
$ django-admin makemessages --locale=es
$ django-admin compilemessages
```

# Configuración para inicio de sesión desde redes sociales

Una vez iniciado el server, visitamos la pagina de administración (Ejemplo: `http://localhost:8000/admin/`) y seguir los siguientes pasos:

* Añadir un sitio para su dominio, que se corresponda con `settings.SITE_ID` (` django.contrib.sites app`).
* Para cada proveedor basado en OAuth, añadir un Social App (socialaccount app).
* Complete los datos con el sitio y las credenciales de aplicaciones OAuth obtenidos del proveedor.

Para cualquier problema con las cuentas sociales, por favor verifique en la [documentación de django-allauth](http://django-allauth.readthedocs.org).
