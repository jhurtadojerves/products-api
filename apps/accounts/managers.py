from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    """
    Custom manager for the User model.

    This manager provides methods for creating regular users and superusers,
    ensuring that email is used as the unique identifier for authentication.

    Methods:
        - create_user: Creates and returns a regular user with the given email and password.
        - create_superuser: Creates and returns a superuser with the given email and password.
    """

    def create_user(
        self, email, password=None, is_staff=False, is_active=True, **extra_fields
    ):
        """
        Create and returns a regular user.

        Args:
            email (str): The email address of the user.
            password (str, optional): The password for the user. Defaults to None.
            is_staff (bool, optional): Whether the user has staff privileges. Defaults to False.
            is_active (bool, optional): Whether the user is active. Defaults to True.
            **extra_fields: Additional fields to set on the user.

        Raises:
            ValueError: If the email is not provided.

        Returns:
            User: The created user instance.
        """
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_active=is_active,
            is_staff=is_staff,
            username=email,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and returns a superuser.

        Args:
            email (str): The email address of the superuser.
            password (str, optional): The password for the superuser. Defaults to None.
            **extra_fields: Additional fields to set on the superuser.

        Returns:
            User: The created superuser instance.
        """
        return self.create_user(
            email, password, is_staff=True, is_superuser=True, **extra_fields
        )
