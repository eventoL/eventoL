#!/bin/bash

cd eventol
if [ -e ./eventol.deployed ] || [ "$LOAD_INITIAL_DATA" = 'false' ]
then
  uv run python manage.py migrate --noinput
  uv run python manage.py collectstatic --noinput
  uv run python manage.py compilemessages
  uv run gunicorn eventol.wsgi -b 0.0.0.0:8000
else
  uv run python manage.py makemigrations manager --noinput
  uv run python manage.py migrate --noinput
  uv run python manage.py collectstatic --noinput
  uv run python manage.py loaddata manager/initial_data/admin.json
  uv run python manage.py loaddata manager/initial_data/initial_data.json
  uv run python manage.py loaddata manager/initial_data/sites.json
  uv run python manage.py loaddata manager/initial_data/social.json
  touch ./eventol.deployed
  export LOAD_INITIAL_DATA=false
  uv run gunicorn eventol.wsgi -b 0.0.0.0:8000
fi
