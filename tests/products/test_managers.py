from django.contrib.auth import get_user_model
from django.test import TestCase

User = get_user_model()


class UserManagerTest(TestCase):
    def test_create_user_with_valid_email(self):
        user = User.objects.create_user(email="test@example.com", password="123456")
        self.assertEqual(user.email, "test@example.com")
        self.assertTrue(user.check_password("123456"))
        self.assertFalse(user.is_staff)
        self.assertTrue(user.is_active)

    def test_create_user_without_email_raises_error(self):
        with self.assertRaisesMessage(ValueError, "Users must have an email address"):
            User.objects.create_user(email=None, password="123456")

    def test_create_superuser_sets_flags(self):
        superuser = User.objects.create_superuser(
            email="admin@example.com", password="adminpass"
        )
        self.assertTrue(superuser.is_staff)
        self.assertTrue(superuser.is_superuser)
        self.assertEqual(superuser.email, "admin@example.com")
