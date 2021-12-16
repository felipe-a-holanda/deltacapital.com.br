"""
Django settings for Delta Capital project.

Generated by 'django-admin startproject' using Django 3.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""
import sys
import warnings
from pathlib import Path

import environ

warnings.filterwarnings("ignore", category=UserWarning, module=r".*environ")


ROOT_DIR = Path(__file__).parents[2]  # user-records/)
BASE_DIR = str(ROOT_DIR)
APPS_DIR = ROOT_DIR / "apps"  # user-records/)

env = environ.Env(DEBUG=(bool, False))
env.read_env(str(ROOT_DIR / ".env"))

# insert apps folder to sys path: apps don't need to be in project root
sys.path.insert(0, str(ROOT_DIR / "apps"))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "iqk^jqy+ewr#%hwt5cq2v0e%u%-+0i9j(6p@4x#*9*+t%y4hl8"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=False)
DEBUG_TEMPLATE = DEBUG

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.humanize",
    "django.forms",
]

THIRD_PARTY_APPS = [
    # "webpack_loader",
    "compressor",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "rest_framework",
    "constance",  # https://github.com/jazzband/django-constance
    "constance.backends.database",
    "crispy_forms",
    "widget_tweaks",
    "django_extensions",
    "django_admin_listfilter_dropdown",
    "admin_auto_filters",
    "django_json_widget",
]


LOCAL_APPS = [
    "apps.users.apps.UsersConfig",
    "apps.delta.apps.DeltaConfig",
    "apps.porto.apps.PortoConfig",
    "apps.gestao.apps.GestaoConfig",
    "apps.consultas.apps.ShiftdataConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    # "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.utils.middleware.WwwRedirectMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        # "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
                "admin_tools.template_loaders.Loader",
            ],
            "debug": DEBUG_TEMPLATE,
        },
    }
]

WSGI_APPLICATION = "config.wsgi.application"

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"
# Database
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

AUTH_USER_MODEL = "users.User"


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [  # type: ignore
    # {
    #    "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    # },
    # {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    # {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    # {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
    # `allauth` specific authentication methods, such as login by e-mail
    "apps.users.auth_backends.CPFBackend",
]

# All-Auth
# ------------------------------------------------------------------------------
LOGIN_REDIRECT_URL = "porto:proposta-create"
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_ADAPTER = "apps.users.account_adapter.NoNewUsersAccountAdapter"


# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
# TIME_ZONE = "UTC"
TIME_ZONE = "America/Fortaleza"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "pt-br"

LANGUAGES = (("pt-br", u"Português"),)
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(ROOT_DIR / "locale")]

DECIMAL_SEPARATOR = ","
THOUSAND_SEPARATOR = "."
USE_THOUSAND_SEPARATOR = True
NUMBER_GROUPING = 3


ADMIN_URL = env("DJANGO_ADMIN_URL", default="admin/")
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


STATIC_ROOT = str(ROOT_DIR / "staticfiles")
STATIC_URL = "/static/"
STATICFILES_DIRS = [str(ROOT_DIR / "static")]


STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
]

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


MEDIA_URL = "/media/"
MEDIA_ROOT = str(ROOT_DIR / "media")


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    "DJANGO_DEFAULT_FROM_EMAIL", default="Delta Capital <contato@deltacapital.com.br>"
)
DEFAULT_TO_EMAIL = env("DJANGO_DEFAULT_TO_EMAIL", default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env("DJANGO_SERVER_EMAIL", default=DEFAULT_FROM_EMAIL)

# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env("DJANGO_EMAIL_SUBJECT_PREFIX", default="[Delta Capital]")


# Anymail
# ------------------------------------------------------------------------------
# https://anymail.readthedocs.io/en/stable/installation/#installing-anymail
INSTALLED_APPS += ["anymail"]  # noqa F405
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
# https://anymail.readthedocs.io/en/stable/installation/#anymail-settings-reference
# https://anymail.readthedocs.io/en/stable/esps/mailgun/
EMAIL_BACKEND = "anymail.backends.amazon_ses.EmailBackend"
ANYMAIL = {
    "AMAZON_SES_CLIENT_PARAMS": {
        "aws_access_key_id": env("AWS_ACCESS_KEY_FOR_ANYMAIL_SES"),
        "aws_secret_access_key": env("AWS_SECRET_KEY_FOR_ANYMAIL_SES"),
        "region_name": "sa-east-1",
    }
}


CRISPY_TEMPLATE_PACK = "bootstrap4"

DATE_FORMAT = "%d/%m/%Y"
# CELERY SETTINGS
CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env.str("REDIS_URL", default="")
CELERY_TASK_ALWAYS_EAGER = not CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_BACKEND = env.str("REDIS_URL", default=None)

# OTHER


GOOGLE_CHROME_PATH = env.str(
    "GOOGLE_CHROME_PATH", default="/app/.apt/usr/bin/google-chrome"
)
CHROMEDRIVER_PATH = env.str(
    "CHROMEDRIVER_PATH", default="/app/.chromedriver/bin/chromedriver"
)

WEBPACK_LOADER = {
    "DEFAULT": {
        "CACHE": not DEBUG,
        "BUNDLE_DIR_NAME": "webpack_bundles/",  # must end with slash
        "STATS_FILE": str(ROOT_DIR / "webpack-stats.json"),
        "POLL_INTERVAL": 0.1,
        "TIMEOUT": None,
        "IGNORE": [r".+\.hot-update.js", r".+\.map"],
        "LOADER_CLASS": "webpack_loader.loader.WebpackLoader",
    }
}

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_ROOT = STATIC_ROOT


# django-constance
CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
# CONSTANCE_DATABASE_CACHE_BACKEND = "default"

CONSTANCE_CONFIG = {
    "WHATSAPP_NUMERO": ("558540422050", "Número de contato Whatsapp"),
    "WHATSAPP_MENSAGEM": (
        "Olá, vi o site DeltaCapital.com.br e gostaria de mais informações.",
        "Texto da mensagem do Whatsapp",
    ),
    "INSTAGRAM_USUARIO": ("delta.capital", "Nome de usuário do Instagram"),
    "FACEBOOK_USUARIO": ("deltacapital.com.br", "Nome de usuário do Facebook"),
}


SHIFTDATA_API_KEY = env.str("SHIFTDATA_API_KEY")
