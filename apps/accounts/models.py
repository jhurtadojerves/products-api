from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

from apps.accounts.managers import UserManager


class User(AbstractUser, PermissionsMixin):
    """
    Custom User model that uses email as the unique identifier.

    This model extends Django's `AbstractUser` and `PermissionsMixin` to provide
    a customizable user model with email-based authentication. It also includes
    additional fields for tracking creation and modification timestamps.

    Attributes:
        email (EmailField): The unique email address for the user.
        created (DateTimeField): The timestamp when the user was created.
        modified (DateTimeField): The timestamp when the user was last modified.
        USERNAME_FIELD (str): Specifies the field used for authentication (email).
        REQUIRED_FIELDS (list): Specifies additional required fields for user creation.
        objects (UserManager): The custom manager for the User model.
    """

    email = models.EmailField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()
