#!/usr/bin/env bash

pip3 install -r requirements.txt -r requirements-dev.txt
cd eventol
./manage.py migrate
./manage.py createsuperuser
./manage.py loaddata manager/initial_data/initial_data.json
./manage.py loaddata manager/initial_data/security.json
./manage.py loaddata manager/initial_data/software.json

sudo npm install -g yarn
cd front
yarn install
cd -

./manage.py collectstatic --no-input
