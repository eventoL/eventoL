# pylint: disable=missing-docstring
# pylint: disable=W0232
# pylint: disable=C0103
# pylint: disable=W0611

import os
import socket
import environ

import raven
from configurations import Configuration
from django.utils.translation import gettext_lazy as _
from django.contrib.admin import ModelAdmin
from easy_thumbnails.conf import Settings as thumbnail_settings
from easy_thumbnails.optimize.conf import OptimizeSettings

env = environ.Env(
    DEBUG=(bool, os.getenv('DEBUG', True)),
    LANGUAGE_CODE=(str, os.getenv('LANGUAGE_CODE', 'en-US')),
    TIME_ZONE=(str, os.getenv('TIME_ZONE', 'UTC')),
    DONT_SET_FILE_UPLOAD_PERMISSIONS=(bool, os.getenv('DONT_SET_FILE_UPLOAD_PERMISSIONS', False)),
    IS_ALPINE=(str, os.getenv('IS_ALPINE', 'not found')),
    REDIS_HOST=(str, os.getenv('REDIS_HOST', 'redis')),
    REDIS_PORT=(int, os.getenv('REDIS_PORT', 6379)),
    EMAIL_BACKEND=(str, os.getenv('EMAIL_BACKEND',
                   'django.core.mail.backends.console.EmailBackend')),
    EMAIL_HOST=(str, os.getenv('EMAIL_HOST', 'smtp.unset')),
    EMAIL_PORT=(int, os.getenv('EMAIL_PORT', 587)),
    EMAIL_HOST_USER=(str, os.getenv('EMAIL_HOST_USER', None)),
    EMAIL_HOST_PASSWORD=(str, os.getenv('EMAIL_HOST_PASSWORD', None)),
    EMAIL_TIMEOUT=(int, os.getenv('EMAIL_TIMEOUT', 10)),
    EMAIL_USE_TLS=(bool, os.getenv('EMAIL_USE_TLS', True)),
    EMAIL_FROM=(str, os.getenv('EMAIL_FROM', 'change_unset@mail.com')),
    DEFAULT_FROM_EMAIL=(str, os.getenv('EMAIL_FROM', 'change_unset@mail.com')),
    ADMIN_TITLE=(str, os.getenv('ADMIN_TITLE', 'EventoL')),
    PRIVATE_ACTIVITIES=(bool, os.getenv('PRIVATE_ACTIVITIES', True)),
    PROTOCOL=(str, os.getenv('PROTOCOL', 'ws')),
    LIST_PER_PAGE=(int, os.getenv('LIST_PER_PAGE', 25)),
    SECRET_KEY=(str, os.getenv('SECRET_KEY',
                               '!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu')),
    APP_DNS=(str, os.getenv('APP_DNS', socket.gethostname())),
    LOG_FILE=(str, os.getenv('LOG_FILE', '/var/log/eventol/eventol.log')),
    SENTRY_DSN=(str, os.getenv("SENTRY_DSN", "NOT_CONFIGURED")),
    PSQL_DBNAME=(str, os.getenv('PSQL_DBNAME', 'eventol')),
    PSQL_USER=(str, os.getenv('PSQL_USER', 'eventol')),
    PSQL_PASSWORD=(str, os.getenv('PSQL_PASSWORD', 'secret')),
    PSQL_HOST=(str, os.getenv('PSQL_HOST', 'localhost')),
    PSQL_PORT=(int, os.getenv('PSQL_PORT', 5432)),
    PSQL_OPTIONS_SSL=(str, os.getenv('PSQL_OPTIONS_SSL', "prefer")),
    JAZZMIN_SITE_TITLE=(str, os.getenv('JAZZMIN_SITE_TITLE', 'EventoL Admin')),
    JAZZMIN_SITE_HEADER=(str, os.getenv('JAZZMIN_SITE_HEADER', 'EventoL')),
    JAZZMIN_SITE_BRAND=(str, os.getenv('ADMIN_TITLE', 'EventoL')),
    JAZZMIN_WELCOME_SIGN=(str, os.getenv('JAZZMIN_WELCOME_SIGN',
                          'Administration panel of EventoL')),
    JAZZMIN_LANGUAGE_CHOOSER=(bool, os.getenv('JAZZMIN_LANGUAGE_CHOOSER', True))
)

# import ipdb;ipdb.set_trace()


def str_to_bool(str_bool):
    return str_bool.lower() == 'true'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# first try to load .env, second try lo load os.getenv and three use Defaults values
environ.Env.read_env(os.path.join(BASE_DIR, '.env'), overwrite=True)


class Base(Configuration):
    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/
    STATIC_URL = '/static/'

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = '!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu'

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    ALLOWED_HOSTS = ['*']

    # Application definition

    INSTALLED_APPS = (
        'dal',
        'dal_select2',
        'ckeditor',
        'ckeditor_uploader',
        'jazzmin',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'easy_thumbnails',
        'easy_thumbnails.optimize',
        'image_cropping',
        'import_export',
        'manager',
        'djangoformsetjs',
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.twitter',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.github',
        'captcha',
        'django.contrib.postgres',
        'django_filters',
        'rest_framework',
        'django_extensions',
        'vote',
        'tempus_dominus',
    )

    MIDDLEWARE = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'allauth.account.middleware.AccountMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    ROOT_URLCONF = 'eventol.urls'
    WSGI_APPLICATION = 'eventol.wsgi.application'

    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + thumbnail_settings.THUMBNAIL_PROCESSORS

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGE_CODE = env('LANGUAGE_CODE')
    LOCALE_PATHS = (os.path.join(BASE_DIR, 'conf/locale'),)
    LANGUAGES = (
        ('da', _('Danish')),
        ('en', _('English')),
        ('es', _('Spanish')),
        ('fr', _('French')),
        ('nb', _('Norwegian Bokmal')),
        ('nl', _('Dutch')),
        ('sv', _('Swedish')),
        # ('zh', _('Chinese')),
    )

    TIME_ZONE = env('TIME_ZONE')
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = BASE_DIR + 'media/'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                MEDIA_ROOT
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'debug': DEBUG,
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.template.context_processors.debug',
                    'django.template.context_processors.i18n',
                    'django.template.context_processors.media',
                    'django.template.context_processors.static',
                    'django.template.context_processors.tz',
                    'django.contrib.messages.context_processors.messages',
                    'django.template.context_processors.request',
                    'manager.context_processors.eventol_settings',
                ],
            },
        },
    ]

    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/'
    LOGIN_TITLE = 'EventoL'

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
            'toolbar': 'full',
            'width': 'unset',
        },
    }

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    DONT_SET_FILE_UPLOAD_PERMISSIONS = env('DONT_SET_FILE_UPLOAD_PERMISSIONS')
    FILE_UPLOAD_PERMISSIONS = None if DONT_SET_FILE_UPLOAD_PERMISSIONS else 0o644

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
    )

    SITE_ID = 1

    SOCIALACCOUNT_PROVIDERS = \
        {
            'google': {
                'SCOPE': ['profile', 'email'],
                'AUTH_PARAMS': {'access_type': 'online'}
            },
            'github': {
                'SCOPE': ['user:email']
            }
        }

    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = True

    ACCOUNT_FORMS = {
        'login': 'manager.forms.LoginForm',
        'signup': 'manager.forms.SignUpForm',
        'reset_password': 'manager.forms.ResetPasswordForm',
        'reset_password_from_key': 'manager.forms.ResetPasswordKeyForm',
        'change_password': 'manager.forms.ChangePasswordForm',
        'set_password': 'manager.forms.SetPasswordForm'
    }

    SOCIALACCOUNT_EMAIL_REQUIRED = True
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    SOCIALACCOUNT_QUERY_EMAIL = True
    SOCIALACCOUNT_AUTO_SIGNUP = False
    SOCIALACCOUNT_FORMS = {'signup': 'manager.forms.SocialSignUpForm'}

    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
            'OPTIONS': {'min_length': 8}
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    CAPTCHA_CHALLENGE_FUNCT = 'captcha.helpers.random_char_challenge'
    CAPTCHA_NOISE_FUNCTIONS = ('captcha.helpers.noise_null',)
    CAPTCHA_FLITE_PATH = '/usr/bin/flite'
    CAPTCHA_SOX_PATH = '/usr/bin/sox'

    STATICFILES_DIRS = []

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 20,
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.SearchFilter',
            'rest_framework.filters.OrderingFilter',
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        ]
    }

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgi_ipc.IPCChannelLayer',
            'ROUTING': 'eventol.routing.channel_routing',
        },
    }

    IS_ALPINE = env('IS_ALPINE') != "not found"
    if IS_ALPINE:
        CHANNEL_LAYERS['default'] = {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(
                    env('REDIS_HOST'),
                    env('REDIS_PORT'),
                )],
            },
            'ROUTING': 'eventol.routing.channel_routing',
        }

    EMAIL_BACKEND = env('EMAIL_BACKEND')
    EMAIL_HOST = env('EMAIL_HOST')
    EMAIL_PORT = env('EMAIL_PORT')
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
    EMAIL_TIMEOUT = env('EMAIL_TIMEOUT')
    EMAIL_USE_TLS = env('EMAIL_USE_TLS')
    EMAIL_FROM = env('EMAIL_FROM')
    DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')

    ADMIN_TITLE = env('ADMIN_TITLE')
    WS_PROTOCOL = env('PROTOCOL')
    PRIVATE_ACTIVITIES = env('PRIVATE_ACTIVITIES')
    TEMPUS_DOMINUS_LOCALIZE = True
    TEMPUS_DOMINUS_INCLUDE_ASSETS = True

    DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

    # Jazzmin settings
    # https://django-jazzmin.readthedocs.io/
    JAZZMIN_SETTINGS = {
        'site_title': env('JAZZMIN_SITE_TITLE'),
        'site_header': env('JAZZMIN_SITE_HEADER'),
        'site_brand': env('JAZZMIN_SITE_BRAND'),
        'welcome_sign': env('AZZMIN_WELCOME_SIGN'),
        'copyright': env('JAZZMIN_SITE_BRAND'),
        'site_logo': 'manager/img/logo_e.png',
        'login_logo': 'manager/img/logo.png',
        'custom_css': 'manager/css/admin.css',
        'language_chooser': env('JAZZMIN_LANGUAGE_CHOOSER'),
        'order_with_respect_to': [
            'auth',
            'auth.Group',
            'auth.User',
            'account',
            'account.EmailAddress',
            'socialaccount',
            'socialaccount.SocialApp',
            'socialaccount.SocialAccount',
            'socialaccount.SocialToken',
            'manager',
            'manager.EventolSetting',
            'manager.Event',
            'manager.EventTag',
            'manager.EventDate',
            'manager.Organizer',
            'manager.EventUser',
            'manager.EventUserAttendanceDate',
            'manager.Activity',
            'manager.ActivityType',
            'manager.Reviewer',
            'manager.Room',
            'manager.Ticket',
            'manager.Attendee',
            'manager.AttendeeAttendanceDate',
            'manager.Collaborator',
            'manager.Contact',
            'manager.ContactType',
            'manager.ContactMessage',
            'manager.Installer',
            'manager.Installation',
            'manager.Hardware',
            'manager.Software',
            'manager.InstallationMessage',
            'sites',
            'sites.Site',
        ],
        'icons': {
            'auth.Group': 'fas fa-users',
            'auth.User': 'fas fa-user',
            'auth': 'fas fa-users-cog',
            'account.EmailAddress': 'fas fa-envelope',
            'socialaccount.SocialApp': 'fab fa-app-store',
            'socialaccount.SocialAccount': 'fas fa-user-circle',
            'socialaccount.SocialToken': 'fas fa-key',
            'manager.Activity': 'fas fa-calendar-check',
            'manager.ActivityType': 'fas fa-list-alt',
            'manager.AttendeeAttendanceDate': 'fas fa-calendar-day',
            'manager.Attendee': 'fas fa-user-friends',
            'manager.Collaborator': 'fas fa-handshake',
            'manager.ContactMessage': 'fas fa-envelope-open-text',
            'manager.ContactType': 'fas fa-address-book',
            'manager.Contact': 'fas fa-id-card',
            'manager.EventDate': 'fas fa-calendar-alt',
            'manager.EventUser': 'fas fa-user-tag',
            'manager.EventTag': 'fas fa-tags',
            'manager.EventUserAttendanceDate': 'fas fa-calendar-day',
            'manager.EventolSetting': 'fas fa-cogs',
            'manager.Event': 'fas fa-calendar',
            'manager.Hardware': 'fas fa-desktop',
            'manager.Installation': 'fas fa-tools',
            'manager.Installer': 'fas fa-wrench',
            'manager.Organizer': 'fas fa-user-tie',
            'manager.InstallationMessage': 'fas fa-comment-dots',
            'manager.Reviewer': 'fas fa-user-check',
            'manager.Room': 'fas fa-door-open',
            'manager.Software': 'fas fa-code',
            'manager.Ticket': 'fas fa-ticket-alt',
            'sites.Site': 'fas fa-globe',
        },
    }
    JAZZMIN_UI_TWEAKS = {
        'theme': 'flatly',
    }
    LIST_PER_PAGE = int(env('LIST_PER_PAGE'))
    # LIST_PER_PAGE = 25
    ModelAdmin.list_per_page = LIST_PER_PAGE


class Staging(Base):
    DEBUG = env('DEBUG')
    SECRET_KEY = env('SECRET_KEY')
    ALLOWED_HOSTS = [env('APP_DNS')]
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('TEMPLATE_DEBUG', 'False')
    os.environ.setdefault('RECAPTCHA_USE_SSL', 'True')

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
        'PAGE_SIZE': 20,
        'DEFAULT_FILTER_BACKENDS': (
            'rest_framework.filters.SearchFilter',
            'rest_framework.filters.OrderingFilter',
            'django_filters.rest_framework.DjangoFilterBackend',
        ),
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly'
        ],
        'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
        )
    }
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(
                    env('REDIS_HOST'),
                    env('REDIS_PORT'),
                )],
            },
            'ROUTING': 'eventol.routing.channel_routing',
        }
    }
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            },
            'logservices': {
                'format': '[%(asctime)s] [%(levelname)s] %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            },
            'file': {
                'level': 'DEBUG',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': env('LOG_FILE'),
                'maxBytes': 1024 * 1024 * 10,
                'backupCount': 10,
                'formatter': 'logservices'
            }
        },
        'loggers': {
            'eventol': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True
            },
            'django.channels': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': True
            },
            'django.request': {
                'handlers': ['file'],
                'level': 'WARNING',
                'propagate': True
            },
            'django': {
                'handlers': ['console'],
                'level': 'WARNING',
                'propagate': True
            }
        }
    }
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'

    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'raven.contrib.django.raven_compat',
    )

    RAVEN_CONFIG = {
        'dsn': env('SENTRY_DSN')
    }

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('PSQL_DBNAME'),
            'USER': env('PSQL_USER'),
            'PASSWORD': env('PSQL_PASSWORD'),
            'HOST': env('PSQL_HOST'),
            'PORT': env('PSQL_PORT'),
            'OPTIONS': {
                'sslmode': env('PSQL_OPTIONS_SSL'),
            },
        }
    }

    # CSRF
    CSRF_TRUSTED_ORIGINS = [
        f"http://{env('APP_DNS')}",
        f"https://{env('APP_DNS')}"
    ]
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


class Prod(Staging):
    DEBUG = False


class Dev(Base):
    INSTALLED_APPS = Base.INSTALLED_APPS + (
        'autofixture',
        'debug_toolbar',
    )

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': 'eventol_dev_db',
        }
    }

    AUTH_PASSWORD_VALIDATORS = []
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s'
            }
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'simple'
            }
        },
        'loggers': {
            'eventol': {
                'handlers': ['console'],
                'level': 'DEBUG'
            },
            'django.request': {
                'handlers': ['console'],
                'level': 'ERROR'
            },
            'django': {
                'handlers': ['console'],
                'level': 'ERROR',
                'propagate': True
            }
        }
    }


class Test(Dev):
    REST_FRAMEWORK = Prod.REST_FRAMEWORK