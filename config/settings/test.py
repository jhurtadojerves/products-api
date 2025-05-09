from .base import *  # NOQA

SECRET_KEY = "fake_secret"
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True
AWS_ACCESS_KEY_ID = "fake-key"
AWS_SECRET_ACCESS_KEY = "fake-secret"
AWS_REGION_NAME = "us-east-1"
FROM_EMAIL = "no-reply@example.com"
