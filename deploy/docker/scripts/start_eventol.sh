#!/bin/bash
python manage.py migrate --noinput && python manage.py runworker

