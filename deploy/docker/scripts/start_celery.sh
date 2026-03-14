#!/bin/bash

cd eventol

uv run celery -A eventol.celery worker -l INFO
