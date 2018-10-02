# pylint: disable=missing-docstring
# pylint: disable=W0232
# pylint: disable=C0103

import os

from configurations import Configuration
from django.utils.translation import ugettext_lazy as _
from easy_thumbnails.conf import Settings as thumbnail_settings
from easy_thumbnails.optimize.conf import OptimizeSettings


def str_to_bool(str_bool):
    return str_bool == 'True'


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


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
        'django_nose',
        'manager',
        'autofixture',
        'djangoformsetjs',
        'django.contrib.sites',
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.twitter',
        'allauth.socialaccount.providers.google',
        'allauth.socialaccount.providers.github',
        'debug_toolbar',
        'captcha',
        'django.contrib.postgres',
        'webpack_loader',
        'django_filters',
        'rest_framework',
        'channels',
        'django_elasticsearch_dsl',
        'django_extensions',
        'vote',
        'forms_builder.forms',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    ROOT_URLCONF = 'eventol.urls'
    WSGI_APPLICATION = 'eventol.wsgi.application'

    # Database
    # https://docs.djangoproject.com/en/1.11/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    THUMBNAIL_PROCESSORS = (
        'image_cropping.thumbnail_processors.crop_corners',
    ) + thumbnail_settings.THUMBNAIL_PROCESSORS

    # Internationalization
    # https://docs.djangoproject.com/en/1.11/topics/i18n/

    LANGUAGE_CODE = os.getenv('LANGUAGE_CODE', 'en-US')
    LOCALE_PATHS = (os.path.join(BASE_DIR, 'conf/locale'),)
    LANGUAGES = (
        ('es', _('Spanish')),
        ('en', _('English')),
    )

    TIME_ZONE = os.getenv('TIME_ZONE', 'UTC')
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
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
            'toolbar': 'full'
        },
    }

    CKEDITOR_UPLOAD_PATH = 'uploads/'
    FILE_UPLOAD_PERMISSIONS = 0o644

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

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'front/eventol/static'),
    ]

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

    IS_ALPINE = os.getenv('IS_ALPINE', False)
    if IS_ALPINE:
        CHANNEL_LAYERS['default'] = {
            'BACKEND': 'asgi_redis.RedisChannelLayer',
            'CONFIG': {
                'hosts': [(
                    os.getenv('REDIS_HOST', 'redis'),
                    int(os.getenv('REDIS_PORT', '6379')),
                )],
            },
            'ROUTING': 'eventol.routing.channel_routing',
        }

    EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.unset')
    EMAIL_PORT = os.getenv('EMAIL_PORT', '587')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', None)
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', None)
    EMAIL_TIMEOUT = int(os.getenv('EMAIL_TIMEOUT', '10'))
    EMAIL_USE_TLS = str_to_bool(os.getenv('EMAIL_USE_TLS', 'True'))
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'change_unset@mail.com')
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', EMAIL_FROM)

    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = BASE_DIR + 'media/'
    ADMIN_TITLE = os.getenv('ADMIN_TITLE', 'EventoL')
    WS_PROTOCOL = os.getenv('PROTOCOL', 'ws')

    # Change test runner
    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
    NOSE_ARGS = [
        '--with-coverage',
        '--cover-package=manager,eventol',
    ]
    PRIVATE_ACTIVITIES = os.environ.get("PRIVATE_ACTIVITIES", True)


class Staging(Base):
    import socket
    DEBUG = str_to_bool(os.getenv('DEBUG', 'True'))
    SECRET_KEY = os.getenv(
        'SECRET_KEY',
        '!a44%)(r2!1wp89@ds(tqzpo#f0qgfxomik)a$16v5v@b%)ecu')
    ALLOWED_HOSTS = [os.getenv('APP_DNS'), socket.gethostname()]
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('TEMPLATE_DEBUG', 'False')
    os.environ.setdefault('RECAPTCHA_USE_SSL', 'True')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv('PSQL_DBNAME', 'eventol'),
            'USER': os.getenv('PSQL_USER', 'eventol'),
            'PASSWORD': os.getenv('PSQL_PASSWORD', 'secret'),
            'HOST': os.getenv('PSQL_HOST', 'localhost'),
            'PORT': os.getenv('PSQL_PORT', '5432'),
            'OPTIONS': {
                'sslmode': os.environ.get("PSQL_OPTIONS_SSL", "prefer"),
            },
        }
    }
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/prod/',  # end with slash
            'STATS_FILE': os.path.join(
                BASE_DIR, 'front', 'webpack-stats-prod.json'),
        }
    }
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
                    os.getenv('REDIS_HOST', 'redis'),
                    int(os.getenv('REDIS_PORT', '6379')),
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
                'filename': os.getenv('LOG_FILE', '/var/log/eventol.log'),
                'maxBytes': 1024*1024*10,
                'backupCount': 10,
                'formatter': 'logservices'
            },
            'logstash': {
                'level': 'DEBUG',
                'class': 'logstash.TCPLogstashHandler',
                'host': os.getenv('LOGSTASH_HOST', 'logstash'),
                'port': os.getenv('LOGSTASH_PORT', 5000),
                'version': 1,
                'message_type': 'django',
                'fqdn': False,
                'tags': ['eventol', 'django.request', 'django.channels', 'django']
            }
        },
        'loggers': {
            'eventol': {
                'handlers': ['logstash', 'file'],
                'level': 'DEBUG',
                'propagate': True
            },
            'django.channels': {
                'handlers': ['logstash', 'file'],
                'level': 'WARNING',
                'propagate': True
            },
            'django.request': {
                'handlers': ['logstash', 'file'],
                'level': 'WARNING',
                'propagate': True
            },
            'django': {
                'handlers': ['logstash', 'console'],
                'level': 'WARNING',
                'propagate': True
            }
        }
    }
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': '{0}:{1}'.format(
                os.getenv('ELASTICSEARCH_HOST', 'elasticsearch'),
                os.getenv('ELASTICSEARCH_PORT', 9200)
            )
        }
    }
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')
    STATIC_URL = '/static/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'


class Prod(Staging):
    DEBUG = False


class Dev(Base):
    AUTH_PASSWORD_VALIDATORS = []
    WEBPACK_LOADER = {
        'DEFAULT': {
            'BUNDLE_DIR_NAME': 'bundles/local/',  # end with slash
            'STATS_FILE': os.path.join(
                BASE_DIR, 'front', 'webpack-stats-local.json'),
        }
    }
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
    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': '{0}:{1}'.format(
                os.getenv('ELASTICSEARCH_HOST', 'elasticsearch'),
                os.getenv('ELASTICSEARCH_PORT', 9200)
            )
        }
    }


class Test(Dev):
    pass
