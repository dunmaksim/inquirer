u"""
Настройки.

По-хорошему должны загружаться из файла settings.conf, но сейчас нет времени
писать этот код.
"""

import uuid
from os.path import join as pathjoin
from os.path import dirname, abspath
from os import getenv # SECRET_KEY
import sys # exit
import random
import string

_SECRET_KEY_LENGTH = 30


def generate_secret_key():
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(_SECRET_KEY_LENGTH))

BASE_DIR = dirname(dirname(abspath(__file__)))

SECRET_KEY = None
DEBUG = getenv('DEBUG', True)

if DEBUG:
    # Для отладки можно и сгенеренный на ходу использовать
    SECRET_KEY = getenv('SECRET_KEY', generate_secret_key())
else:
    # На боевом сервере SECRET_KEY должен быть объявлен как переменная окружения
    print("Для работы приложения требуется наличие переменной окружения SECRET_KEY.")
    sys.exit()

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'core',
    'api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inquirer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'inquirer.wsgi.application'


# Пока без PostgreSQL, там проще
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': pathjoin(BASE_DIR, 'db.sqlite3'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = pathjoin(BASE_DIR, 'static')
MEDIA_ROOT = pathjoin(BASE_DIR, 'media')

SESSION_SAVE_EVERY_REQUEST = True # Сохранять данные о сессии при каждом запросе.

REST_FRAMEWORK ={
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ]
}
