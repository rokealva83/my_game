# -*- coding: utf-8 -*-

"""
Django settings for my_game project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

import djcelery
# указываем на то, что расписание будет задаваться посредством django-ORM
CELERYBEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
# # указываем брокер сообщений
BROKER_URL = 'redis://127.0.0.1:6379/1'
# # указываем хранилище результатов (можете не указывать)
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'
# # формат хранения задач (можете не указывать)
CELERY_TASK_SERIALIZER = 'json'
# # формат хранения результатов (можете не указывать)
CELERY_RESULT_SERIALIZER = 'json'
# если настроены джанговские параметры уведомлений по почте
# и данный параметр True, то исключения в задачах будут
# фиксироваться на почте администраторов приложения
CELERY_SEND_TASK_ERROR_EMAILS = True
# # инициализация django-celery
djcelery.setup_loader()



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yr(ogw485*#7bf2o$me0x680@^40*@zwya6rqmtc8o=@!huc2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition


INSTALLED_APPS = (
    'suit',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_game',
    'my_game.templatetags.my_filter',
    'my_game.space_forces.fleet_management',
    'djcelery',
    'redis',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'my_game.urls'

WSGI_APPLICATION = 'my_game.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'CHARSET': 'utf8',
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'libre',
        'USER': 'root',
        'PASSWORD': 'tolik2000',

    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    BASE_DIR + '/static-files',
    BASE_DIR
)

MEDIA_URL = '/media/'
MEDIAFILES_DIRS = (
    BASE_DIR + '/media-files',
    BASE_DIR
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


SUIT_CONFIG = {
    'ADMIN_NAME': 'LIBRE',

    'SHOW_REQUIRED_ASTERISK': True,
    'CONFIRM_UNSAVED_CHANGES': True,
    'MENU_EXCLUDE': ('auth.group', 'auth'),
    'LIST_PER_PAGE': 20
}