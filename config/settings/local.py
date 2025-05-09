from .base import *  # NOQA

DEBUG = True
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "local_secret_key"

INSTALLED_APPS += ["django_extensions"]  # noqa F405
