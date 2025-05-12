from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class CustomTokenObtainPairTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com",
            password="testpassword",
        )
        self.url = reverse("token_obtain_pair")

    def test_login_with_valid_credentials_returns_tokens_and_user_data(self):
        response = self.client.post(
            self.url, {"email": "user@example.com", "password": "testpassword"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)
        self.assertEqual(response.data["email"], self.user.email)
        self.assertEqual(response.data["user_id"], self.user.id)

    def test_login_with_invalid_credentials_returns_error(self):
        response = self.client.post(
            self.url, {"email": "user@example.com", "password": "wrongpass"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"non_field_errors": ["Invalid credentials"]})


class UserAdminTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            email="admin@example.com",
            password="admin123",
            is_staff=True,
            is_active=True,
        )

        self.other_admin = User.objects.create_user(
            email="other@example.com",
            password="admin456",
            is_staff=True,
            is_active=True,
        )

        self.client.force_authenticate(user=self.admin)

    def test_admin_can_reset_own_password(self):
        url = reverse("user-reset-password", args=[self.admin.id])
        data = {"current_password": "admin123", "new_password": "newpassword123"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Password updated successfully.", response.data["detail"])

        self.admin.refresh_from_db()
        self.assertTrue(self.admin.check_password("newpassword123"))

    def test_reset_password_wrong_current_password_fails(self):
        url = reverse("user-reset-password", args=[self.admin.id])
        data = {"current_password": "wrongpassword", "new_password": "newpassword123"}

        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("current_password", response.data)

    def test_admin_cannot_reset_other_admin_password(self):
        url = reverse("user-reset-password", args=[self.other_admin.id])
        data = {
            "current_password": "admin123",
            "new_password": "newpassword456",
        }

        response = self.client.post(url, data, format="json")
        data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            data.get("non_field_errors", [])[0],
            "You can only change your own password.",
        )

    def test_admin_cannot_delete_yourself(self):
        url = reverse("user-detail", args=[self.admin.id])
        response = self.client.delete(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("You can't delete yourself", response.data["detail"])

    def test_admin_can_delete_other_user(self):
        url = reverse("user-detail", args=[self.other_admin.id])
        response = self.client.delete(url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_admin_can_create_user(self):
        url = reverse("user-list")
        data = {
            "email": "third@example.com",
            "first_name": "Jon",
            "last_name": "Do",
            "password": "fake_temp_pass",
        }
        response = self.client.post(url, data, format="json")
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("email"), "third@example.com")
        self.assertEqual(
            data,
            {
                "id": 3,
                "email": "third@example.com",
                "is_active": True,
                "first_name": "Jon",
                "last_name": "Do",
            },
        )
