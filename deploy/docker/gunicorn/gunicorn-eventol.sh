#!/bin/bash

NAME="eventol" # Name of the application
DJANGODIR=/var/www/eventol/ # Django project directory
SOCKFILE=/var/www/eventol/gunicorn/gunicorn.sock # we will communicate using this unix socket
USER=root # the user to run as
GROUP=root # the group to run as
NUM_WORKERS=3 # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=eventoL.settings # which settings file should Django use
DJANGO_WSGI_MODULE=eventoL.wsgi # WSGI module name

# Activate the virtual environment
cd ${DJANGODIR}
export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname ${SOCKFILE})
test -d ${RUNDIR} || mkdir -p ${RUNDIR}

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
source /var/www/eventol/venv/bin/activate
exec gunicorn ${DJANGO_WSGI_MODULE}:application \
--name ${NAME} \
--workers ${NUM_WORKERS} \
--user=${USER} \
--group=${GROUP} \
--bind=unix:${SOCKFILE} \
--log-level=debug \
--timeout=300 \
--log-file=/var/www/eventol/log/gunicorn.log \
--reload
