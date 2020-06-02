import os

import environ

env = environ.Env()
env.read_env(env("APP_CONFIG_PATH", default="./configs/local.env"))

APP_NAME = "simple app"
APP_VERSION = os.getenv("APP_VERSION")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = env("DJANGO_SECRET_KEY")
DEBUG = env.bool("DJANGO_DEBUG", False)

ALLOWED_HOSTS = [env("APP_HOST", default="*")]

# Application definition

INSTALLED_APPS = [
    "django_prometheus",
    # PROJECT_APPS
    "src.health_check",
]

MIDDLEWARE = [
    "django.middleware.common.CommonMiddleware",
    "src.common.RequestLogMiddleware",
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "src.urls"

WSGI_APPLICATION = "src.wsgi.application"
ASGI_APPLICATION = "src.asgi.application"
APPEND_SLASH = False

# Database
DATABASES = {"default": env.db()}
CACHES = {"default": env.cache(default="locmemcache://")}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = False


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {"format": "%(message)s", "()": "src.common.JsonFormatter", "fields": ("status", "path", "spent")}
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "json", "level": "DEBUG"}},
    "loggers": {
        "src": {"handlers": ["console"], "level": env("APP_LOG_LEVEL", default="DEBUG"), "propagate": False},
        "django.request": {"handlers": [], "level": "NOTSET", "propagate": False},
    },
}
