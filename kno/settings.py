"""
Django settings for Kno project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
makepath = lambda *x: tuple([os.path.join(BASE_DIR, a) for a in x])

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd@_kvp!ef#u4ms12vihqne+24ek+#u7^9ws&ljx4!sg3v37jc-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'auth',
    'common',
    'django_jinja',
)

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'common.middleware.ExceptionLoggingMiddleware'
]

ROOT_URLCONF = 'kno.urls'

WSGI_APPLICATION = 'kno.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = ('static',)

TEMPLATE_DIRS = makepath('templates/')

# Use jinja for all templates except django admin templates
DEFAULT_JINJA2_TEMPLATE_INTERCEPT_RE = r"^(?!admin/).*"
JINJA2_BYTECODE_CACHE_ENABLE = True

DEFAULT_JINJA2_TEMPLATE_EXTENSION = '.html'

TEMPLATE_LOADERS = (
    'django_jinja.loaders.AppLoader',
    'django_jinja.loaders.FileSystemLoader',
)

AUTH_USER_MODEL = 'auth.User'

BASE_PATH = BASE_DIR
TEST_RUNNER = 'kno.tests.DiscoveryRunner'
TEST_DISCOVERY_ROOT = 'tests'
