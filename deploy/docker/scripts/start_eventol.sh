#!/bin/bash

cd eventol
python manage.py makemigrations manager --noinput
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py loaddata manager/initial_data/attendee_data.json
python manage.py loaddata manager/initial_data/email_addresses.json
python manage.py loaddata manager/initial_data/initial_data.json
python manage.py runworker
