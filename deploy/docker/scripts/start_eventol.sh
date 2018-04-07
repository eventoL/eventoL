#!/bin/bash

cd eventol
if [ -e ./eventol.deployed ]
then
  python manage.py runworker
else
  python manage.py makemigrations manager --noinput
  python manage.py migrate --noinput
  python manage.py collectstatic --noinput
  python manage.py loaddata manager/initial_data/admin.json
  python manage.py loaddata manager/initial_data/attendee_data.json
  python manage.py loaddata manager/initial_data/email_addresses.json
  python manage.py loaddata manager/initial_data/initial_data.json
  python manage.py loaddata manager/initial_data/sites.json
  python manage.py loaddata manager/initial_data/social.json
  touch ./eventol.deployed
  python manage.py runworker
fi
