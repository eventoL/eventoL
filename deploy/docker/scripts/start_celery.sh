#!/bin/bash

cd eventol

celery -A eventol.celery worker -l INFO
