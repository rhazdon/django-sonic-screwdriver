import os


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = "dummy"

DEBUG = True
TEMPLATE_DEBUG = DEBUG
DEBUG_PROPAGATE_EXCEPTIONS = True

ROOT_URLCONF = "tests.urls"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "django_sonic_screwdriver",
    "django_sonic_screwdriver.apps.admin_comments",
    "django_sonic_screwdriver.apps.ban",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django_sonic_screwdriver.apps.ban.middleware.BanMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": (
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            )
        },
    }
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

USE_I18N = True
USE_L10N = True

TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"

MEDIA_ROOT = ""
MEDIA_URL = ""

STATIC_URL = "/static/"


DJANGO_SONIC_SCREWDRIVER_BAN_REMOTE_ADDR_HEADER = "REMOTE_ADDR"
DJANGO_SONIC_SCREWDRIVER_BAN_DEFAULT_END_TIME = 60 * 60
