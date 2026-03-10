import os

import configurations
import environ
from celery import Celery
from configurations import importer as _configs_importer
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'eventol.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Prod')

env = environ.Env(
    CELERY_BROKER_URL=(str, os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379')),
    CELERY_RESULT_BACKEND=(str, os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379')),
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, '../.env'), overwrite=True)

if not _configs_importer.installed:
    configurations.setup()

app = Celery(
    'manager',
    broker=env('CELERY_BROKER_URL'),
    backend=env('CELERY_BROKER_URL'),
    autodiscover_tasks=True,
    broker_connection_retry_on_startup=True,
    timezone=env('TIME_ZONE'),
    task_eager_propagates=True,
    task_always_eager=False,
    include=['manager.tasks', 'manager.utils.email'],
)
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
