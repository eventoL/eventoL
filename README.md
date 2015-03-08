eventoL
=========

eventoL is a conference and install fest management software initially developed to manage [FLISoL][1] conference.
It is in developement state and this year (2014) is going to be used for managing the Buenos Aires City FLISoL as a test.

Features
--------------
Actually supports:
- Attendee registration whith email confirmation.
- Collaborators registration.
- Installers registration.
- Attendees and collaborators registration made by another collaborator, to register people the same day of the event.
- Mark that a pre-registered participant is present (that efectivelly came to the event).
- Talks, workshops, etc. proposals submit.
- Talks schedule.
- Event location with geodjango and django-cities.
- Collaborators and installers authentication.
- Submit an installation with hardware and software info.
- Full internationalization and localization support.

TODO (this month)
-----------------
- After-event statistics.
- RESTFull API to provide event related data to other apps.
- User Manuals
- Code some tests

Future
-------
- Actually it has many hardcoded parts that are specific to FLISoL. The idea is to make a generic app for any kind of conference or install fest.
- ADMIN interface for the different roles in the event.

Installation
--------------
On Debian like systems:
```sh
$ sudo apt-get install python build-essential python-setuptools python-dev python-pip
$ sudo apt-get install postgresql postgresql-client-9.4 postgresql-server-dev-9.4 
$ sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
$ sudo apt-get install postgresql-9.4-postgis-2.1
$ sudo apt-get install libjpeg-dev libpng3 libpng12-dev libfreetype6-dev zlib1g-dev

#Postgres
$ sudo passwd postgres
$ sudo su - postgres

$ pg_dropcluster --stop 9.4 main
$ pg_createcluster --start -e UTF-8 9.4 main

$ psql postgres

postgres=# ALTER ROLE postgres PASSWORD '<password>';
(ctrl-d)
$ createuser --createdb flisol
postgres=# ALTER ROLE flisol PASSWORD '<password>';

$ createdb  template_postgis
$ psql template_postgis
template_postgis=# CREATE EXTENSION postgis;
template_postgis=# CREATE EXTENSION postgis_topology;

$ psql

postgres# CREATE USER flisol PASSWORD 'my_passwd';
postgres# CREATE DATABASE flisol OWNER flisol TEMPLATE template_postgis ENCODING 'utf8';

#Python/Django

## Install django-generic-confirmation

$ git clone https://github.com/arneb/django-generic-confirmation.git
$ cd django-generic-confirmation
$ python setup.py install


## Install other requirements

$ pip install -r requirements.txt

## Django migrate

$ python manage.py migrate

$ python manage.py makemigrations manager

$ python manage.py migrate

## Importing all cities for django-cities (geolocalization)

$ python manage.py cities --import=all --force #This may take a long time!

```
And change in settings.py URLS, PATHS, DATABASE and EMAIL related settings with your specific configuration.

An easier way
--------------

There is a docker image with the database configuration ready to use:

```sh
$ docker run -dit -p 5432:5432 reyiyo/eventol-postgre
```

And the postgre will be available at port 5432 in the host.


  [1]: http://flisol.info/
