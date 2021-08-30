from .base import *  # noqa
from .base import env
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import ROOT_DIR

DEBUG = env("DEBUG")

# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

INTERNAL_IPS = ["127.0.0.1", "localhost"]

ALLOWED_HOSTS = ["*"]



# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = "localhost"
# https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 1025
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
