# #celery.py
from __future__ import absolute_import, unicode_literals
import os
import environ
from celery import Celery

env = environ.Env(
    CELERY_BROKER_URL=(str,  os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379')),
    CELERY_RESULT_BACKEND=(str,  os.getenv('CELERY_BROKER_URL', 'redis://127.0.0.1:6379')),
)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

environ.Env.read_env(os.path.join(BASE_DIR, '../.env'), overwrite=True)

app = Celery('manager',
             broker=env('CELERY_BROKER_URL'), 
             backend=env('CELERY_BROKER_URL'),
             autodiscover_tasks=True,
             broker_connection_retry_on_startup=True,
             timezone=env('TIME_ZONE'),
             task_eager_propagates=True,
             task_always_eager=False,
             include=['manager.tasks','manager.utils.email']
             )

# Load task modules from all registered Django app configs.

@app.task(bind=True)
def debug_task(self):
    '''
    Debug Task to test celery connection
    '''
    print('Request: {0!r}'.format(self.request))