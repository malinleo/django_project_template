from .base import *


SITE_ID = 1
ENVIRONMENT = 'local'
TESTING = False

if DEBUG:
    INSTALLED_APPS += (
        'debug_toolbar',
    )
