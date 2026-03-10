from django.db import connection

USE_POSTGRES = connection.vendor == 'postgresql'
