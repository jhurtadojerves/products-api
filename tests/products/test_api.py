from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.products.models import Brand, Product

User = get_user_model()


class ProductRetrieveAPITest(APITestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="TestBrand")
        self.product = Product.objects.create(
            sku="TEST123",
            name="Test Product",
            price=100.00,
            brand=self.brand,
        )
        self.url = reverse("product-detail", args=[self.product.sku])

    @patch("apps.products.tasks.track_product_retrieve.delay")
    @patch(
        "apps.products.services.ProductVisitMetadataBuilder.build",
        return_value={"ip": "1.1.1.1"},
    )
    def test_retrieve_as_anonymous_triggers_tracking(self, mock_build, mock_delay):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_build.assert_called_once()
        mock_delay.assert_called_once_with(self.product.id, {"ip": "1.1.1.1"})

    @patch("apps.products.tasks.track_product_retrieve.delay")
    @patch(
        "apps.products.services.ProductVisitMetadataBuilder.build",
        return_value={"ip": "1.1.1.1"},
    )
    def test_retrieve_as_authenticated_does_not_trigger_tracking(
        self, mock_build, mock_delay
    ):
        user = User.objects.create_user(email="user@example.com", password="pass123")
        self.client.force_authenticate(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_build.assert_not_called()
        mock_delay.assert_not_called()

    @patch("apps.products.services.ProductEmailService.send_email")
    def test_update_product_call_email_service(self, mock_service):
        user = User.objects.create_user(email="user@example.com", password="pass123")
        self.client.force_authenticate(user=user)
        response = self.client.patch(
            self.url,
            data={"name": "New Product Name"},
            format="json",
        )
        data = response.json()

        self.assertEqual(data.get("name"), "New Product Name")
        mock_service.assert_called_with(self.product, user)
