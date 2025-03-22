#!/usr/bin/env bash

pip install -r requirements.txt -r requirements-dev.txt

cd eventol

./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata manager/initial_data/initial_data.json
./manage.py loaddata manager/initial_data/security.json
./manage.py loaddata manager/initial_data/software.json
./manage.py collectstatic --no-input
