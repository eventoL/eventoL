import os

from channels.asgi import get_channel_layer
from configurations import importer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventol.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

importer.install()

channel_layer = get_channel_layer()
