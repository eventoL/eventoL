# DB

We're using postgres. For development there are 2 options:

## Use a docker container for DB

Run the container:

```sh
docker run --name eventol-postgres -e POSTGRES_PASSWORD=secret -e POSTGRES_USER=eventol -e POSTGRES_DB=eventol -p 5432:5432 -d postgres
```
And the database will be magically available on localhost:5432!

Dependencies needed on dev machine (tested for Debian jessie and sid):

```sh
$ sudo apt-get install python build-essential python-setuptools python-dev python-pip
$ sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
$ sudo apt-get install libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev
$ sudo apt-get install jpegoptim optipng
$ sudo apt-get install postgresql-server-dev-9.4
```

## Installation on Debian like systems (jessie+):

Install postgre, python and some dependencies
```sh
$ sudo apt-get install python build-essential python-setuptools python-dev python-pip
$ sudo apt-get install postgresql postgresql-client-9.4 postgresql-server-dev-9.4 
$ sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
$ sudo apt-get install postgresql-9.4-postgis-2.2
$ sudo apt-get install libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev
$ sudo apt-get install jpegoptim optipng
```
Configure postgre
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

## If you want some administration tool for the database

```sh
$ sudo apt-get install pgadmin3
```

# Python/Django project dependencies

### Install python requirements

```sh
$ pip install -U -r requirements.txt
```

### Django stuff

First of all, change in settings.py URLS, PATHS, DATABASE and EMAIL related settings with your specific configuration.

Then, model related stuff:

```sh
$ python manage.py migrate
$ python manage.py makemigrations manager
$ python manage.py migrate
$ python manage.py syncdb
$ python manage.py collectstatic
```

### If you want to populate the db with some initial example data

```sh
$ python manage.py loaddata manager/initial_data.json
```

### Update tranlations

```sh
$ django-admin makemessages --locale=es
$ django-admin compilemessages
```
