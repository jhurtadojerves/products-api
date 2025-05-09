from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
