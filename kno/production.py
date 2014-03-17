import socket
from .settings import *

TEMPLATE_DEBUG = False
DEBUG = False

ADMINS = (('Matt Stark', 'mattstark75@gmail.com'),)

# TODO: on production server, delete localhost and 127.0.0.1 from this list
ALLOWED_HOSTS = ['kno.blakeservers.com.au', 'kno.blakebytes.com.au', 'server2.blakebytes.com.au', 'server2.chatswoodhighvoting.com']

PROVIDE_STATICFILES = socket.gethostname().startswith('matt-')

if PROVIDE_STATICFILES:
    ALLOWED_HOSTS.extend(['localhost', '127.0.0.1'])

MIDDLEWARE_CLASSES.remove('common.middleware.ExceptionLoggingMiddleware')

WEBSITE_URL = 'kno.blakebytes.com.au'


# TODO: # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/
