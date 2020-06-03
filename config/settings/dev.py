from .base import *  # noqa
from .base import env
from .base import INSTALLED_APPS
from .base import MIDDLEWARE
from .base import ROOT_DIR

DEBUG = env("DEBUG")


# https://django-extensions.readthedocs.io/en/latest/installation_instructions.html#configuration
INSTALLED_APPS += ["django_extensions", "debug_toolbar"]  # noqa F405
# https://django-debug-toolbar.readthedocs.io/en/latest/installation.html#middleware
MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa F405

INTERNAL_IPS = ["127.0.0.1", "localhost"]

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(ROOT_DIR / "db.sqlite3"),
    }
}
