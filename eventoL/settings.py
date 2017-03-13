import os

from easy_thumbnails.conf import Settings as thumbnail_settings
from easy_thumbnails.optimize.conf import OptimizeSettings


def str_to_bool(s):
    return s == 'True'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_URL = '/static/'

ON_OPENSHIFT = 'OPENSHIFT_REPO_DIR' in os.environ
if ON_OPENSHIFT:
    import socket

    os.environ.setdefault('DJANGO_SECRET_KEY', os.environ.get('OPENSHIFT_SECRET_TOKEN'))
    os.environ.setdefault('DJANGO_DEBUG', 'False')
    os.environ.setdefault('DJANGO_TEMPLATE_DEBUG', 'False')
    os.environ.setdefault('PSQL_NAME', os.environ.get('OPENSHIFT_APP_NAME'))
    os.environ.setdefault('PSQL_USER', os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME'))
    os.environ.setdefault('PSQL_PASSWORD', os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD'))
    os.environ.setdefault('PSQL_HOST', os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST'))
    os.environ.setdefault('PSQL_PORT', os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT'))
    ALLOWED_HOSTS = [os.environ.get('OPENSHIFT_APP_DNS'), socket.gethostname()]
    STATIC_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static')
    RECAPTCHA_PROXY = os.environ.get('OPENSHIFT_APP_DNS')
    os.environ.setdefault('DJANGO_RECAPTCHA_USE_SSL', 'True')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'manager', 'static')
    ALLOWED_HOSTS = ['*']

if 'OPENSHIFT_DATA_DIR' in os.environ:
    MEDIA_ROOT = os.path.join(os.environ.get('OPENSHIFT_REPO_DIR'), 'wsgi', 'static', 'media')
    MEDIA_URL = STATIC_URL + 'media/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str_to_bool(os.getenv('DJANGO_DEBUG', 'True'))

# Application definition

INSTALLED_APPS = (
    'ckeditor',
    'ckeditor_uploader',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'easy_thumbnails.optimize',
    'image_cropping',
    'autocomplete_light',
    'import_export',
    'manager',
    'autofixture',
    'djangoformsetjs',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.windowslive',
    'captcha'
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
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('PSQL_NAME', 'eventol'),
        'USER': os.getenv('PSQL_USER', 'eventol'),
        'PASSWORD': os.getenv('PSQL_PASSWORD', 'secret'),
        'HOST': os.getenv('PSQL_HOST', 'localhost'),
        'PORT': os.getenv('PSQL_PORT', '5432'),
    }
}

# Travis Configuration
if 'TRAVIS' in os.environ:
    DATABASES['default']['PORT'] = 5000

THUMBNAIL_PROCESSORS = ('image_cropping.thumbnail_processors.crop_corners',) + thumbnail_settings.THUMBNAIL_PROCESSORS

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': os.getenv('DJANGO_TEMPLATE_DEBUG', 'True'),
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request'
            ],
        },
    },
]

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
        'django': {
            'handlers': ['log_to_stdout'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

if 'EVENTOL_EMAIL_BACKEND' in os.environ:
    EMAIL_BACKEND = os.environ.get('EVENTOL_EMAIL_BACKEND', 'django_mailgun.MailgunBackend')
    MAILGUN_ACCESS_KEY = os.environ.get('EVENTOL_MAILGUN_ACCESS_KEY', 'ACCESS-KEY')
    MAILGUN_SERVER_NAME = os.environ.get('EVENTOL_MAILGUN_SERVER_NAME', 'SERVER-NAME')
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.getenv('DJANGO_EMAIL_HOST', 'smtp.unset')
    EMAIL_PORT = os.getenv('DJANGO_EMAIL_PORT', '587')
    EMAIL_HOST_USER = os.getenv('DJANGO_EMAIL_HOST_USER', 'change_unset@mail.com')
    EMAIL_HOST_PASSWORD = os.getenv('DJANGO_EMAIL_HOST_PASSWORD', 'secret')
    EMAIL_USE_TLS = True
    EMAIL_FROM = os.getenv('DJANGO_EMAIL_FROM', 'change_unset@mail.com')

LOGIN_URL = '/accounts/login/'

OptimizeSettings.THUMBNAIL_OPTIMIZE_COMMAND = {
    'png': '/usr/bin/optipng {filename}',
    'jpeg': '/usr/bin/jpegoptim {filename}',
    'jpg': '/usr/bin/jpegoptim {filename}'
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full'
    },
}

CKEDITOR_UPLOAD_PATH = "uploads/"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'],
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',)
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = \
    {
        'facebook': {
            'METHOD': 'oauth2',
            'SCOPE': ['email', 'public_profile'],
            'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
            'FIELDS': [
                'id',
                'email',
                'name',
                'first_name',
                'last_name',
                'verified',
                'locale',
                'timezone',
                'link',
                'gender',
                'updated_time'],
            'EXCHANGE_TOKEN': True,
            'LOCALE_FUNC': lambda request: 'es_AR',
            'VERIFIED_EMAIL': False,
            'VERSION': 'v2.4'
        },
        'google': {
            'SCOPE': ['profile', 'email'],
            'AUTH_PARAMS': {'access_type': 'online'}
        },
        'github': {
            'SCOPE': ['user:email']
        }
    }

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "mandatory"

ACCOUNT_FORMS = {'login': 'manager.forms.LoginForm',
                 'signup': 'manager.forms.SignUpForm',
                 'reset_password': 'manager.forms.ResetPasswordForm',
                 'reset_password_from_key': 'manager.forms.ResetPasswordKeyForm',
                 'change_password': 'manager.forms.ChangePasswordForm',
                 'set_password': 'manager.forms.SetPasswordForm'}

SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
SOCIALACCOUNT_AUTO_SIGNUP = False
SOCIALACCOUNT_FORMS = {'signup': 'manager.forms.SocialSignUpForm'}

ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
LOGIN_REDIRECT_URL = '/'

RECAPTCHA_PUBLIC_KEY = '6LeIxAcTAAAAAJcZVRqyHh71UMIEGNQ_MXjiZKhI'
RECAPTCHA_PRIVATE_KEY = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'
NOCAPTCHA = True
RECAPTCHA_USE_SSL = str_to_bool(os.getenv('DJANGO_RECAPTCHA_USE_SSL', 'False'))
