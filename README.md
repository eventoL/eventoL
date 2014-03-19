eventoL
=========

eventoL is a conference and install fest management software initially developed to manage [FLISoL][1] conference.
It is in developement state and this year (2014) is going to be used for managing the Buenos Aires City FLISoL as a test.

Features
--------------
Actually supports:
- Attendant registration whith email confirmation.
- Collaborators registration.
- Installers registration.
- Attendant and collaborators registration made by another collaborator, to register people the same day of the event.
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
sudo apt-get install python build-essentials python-setuptools python-dev python-pip
sudo apt-get install postgresql postgresql-client-9.1 postgresql-server-dev-9.1 
sudo apt-get install binutils libproj-dev gdal-bin libgeoip1 python-gdal
sudo apt-get install postgresql-9.1-postgis

#Postgres
sudo passwd postgres
sudo su - postgres
psql postgres

postgres=# ALTER ROLE postgres PASSWORD '<password>';
(ctrl-d)
createuser --createdb flisol
postgres=# ALTER ROLE flisol PASSWORD '<password>';

wget https://docs.djangoproject.com/en/dev/_downloads/create_template_postgis-debian.sh
bash create_template_postgis-debian.sh

createdb -T template_postgis flisol

#Python/Django
pip install django
pip install psycopg2
pip install django-generic-confirmation
pip install django-cities
pip install django-tables2
pip install pil
pip install easy-thumbnails
pip install django-image-cropping
```
And change in settings.py URLS, PATHS, DATABASE and EMAIL related settings with your specific configuration.

  [1]: http://flisol.info/
