"""
Django settings for eventoL project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import django.conf.global_settings as DEFAULT_SETTINGS
from easy_thumbnails.conf import Settings as thumbnail_settings
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from easy_thumbnails.optimize.conf import OptimizeSettings
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'grappelli',
    'ckeditor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'cities',
    'generic_confirmation',
    'django_tables2',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'image_cropping',
    'autocomplete_light',
    'compressor',
    'manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'eventoL.urls'

WSGI_APPLICATION = 'eventoL.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',  # 'django.db.backends.postgresql_psycopg2',
        'NAME': 'flisol',
        'USER': 'flisol',
        'PASSWORD': 'flisol',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

THUMBNAIL_PROCESSORS = (
                           'image_cropping.thumbnail_processors.crop_corners',
                       ) + thumbnail_settings.THUMBNAIL_PROCESSORS

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-US'

LOCALE_PATHS = (os.path.join(BASE_DIR, 'conf/locale'),)

LANGUAGES = (
    ('es', 'Spanish'),
    ('en', 'English'),
)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'manager', 'static')

TEMPLATE_CONTEXT_PROCESSORS = DEFAULT_SETTINGS.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)

CITIES_FILES = {
    'city': {
        'filename': 'AR.zip',
        'urls': ['http://download.geonames.org/export/dump/' + '{filename}']
    },
}

CITIES_LOCALES = ['es-AR']

CITIES_POSTAL_CODES = ['ARG']

CITIES_PLUGINS = []

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'log_to_stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'cities': {
            'handlers': ['log_to_stdout'],
            'level': 'INFO',
            'propagate': True,
        },
        'django': {
            'handlers': ['log_to_stdout'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_HOST_USER = 'YOUR USERNAME'
EMAIL_HOST_PASSWORD = 'YOUR PASSWORD'
EMAIL_USE_TLS = True
LOGIN_URL = '/accounts/login/'

OptimizeSettings.THUMBNAIL_OPTIMIZE_COMMAND = {
    'png': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}',
    'jpg': '/usr/bin/jpegoptim {filename}'
}

GRAPPELLI_ADMIN_TITLE = 'Flisol 2015'

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_ENABLED = False

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"