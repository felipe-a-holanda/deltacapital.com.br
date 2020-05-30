from .base import *  # noqa
from .base import ROOT_DIR

DEBUG = False

ALLOWED_HOSTS = ["clevenus.com", ".herokuapp.com/"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(ROOT_DIR / "db.sqlite3"),
    }
}
