from unittest.mock import MagicMock, patch

from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from apps.products.models.brand import Brand
from apps.products.models.product import Product
from apps.products.services import ProductEmailService, ProductVisitMetadataBuilder

User = get_user_model()


class ProductVisitMetadataBuilderTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X)"
        self.referer = "https://example.com"
        self.ip = "123.123.123.123"

    def test_build_metadata_from_request(self):
        request = self.factory.get(
            "/products/TEST123",
            HTTP_USER_AGENT=self.user_agent,
            HTTP_REFERER=self.referer,
            REMOTE_ADDR=self.ip,
        )

        builder = ProductVisitMetadataBuilder(request)
        metadata = builder.build()

        self.assertEqual(metadata["ip"], self.ip)
        self.assertEqual(metadata["user_agent"], self.user_agent)
        self.assertEqual(metadata["referer"], self.referer)
        self.assertEqual(metadata["device_type"], "mobile")
        self.assertEqual(metadata["device"], "iPhone")
        self.assertEqual(metadata["os"], "iOS")
        self.assertTrue(metadata["browser"].startswith("Mobile Safari"))
        self.assertTrue(metadata["is_mobile"])
        self.assertFalse(metadata["is_tablet"])
        self.assertFalse(metadata["is_pc"])

    def test_ip_from_x_forwarded_for(self):
        forwarded_ip = "203.0.113.1, 70.41.3.18"
        request = self.factory.get(
            "/products/TEST123",
            HTTP_USER_AGENT=self.user_agent,
            HTTP_X_FORWARDED_FOR=forwarded_ip,
            REMOTE_ADDR="should-not-be-used",
        )

        builder = ProductVisitMetadataBuilder(request)
        metadata = builder.build()

        self.assertEqual(metadata["ip"], "203.0.113.1")

    def test_get_device_type_variants(self):
        cases = [
            {"flags": {"is_mobile": True}, "expected": "mobile"},
            {"flags": {"is_tablet": True}, "expected": "tablet"},
            {"flags": {"is_pc": True}, "expected": "pc"},
            {"flags": {"is_bot": True}, "expected": "bot"},
            {"flags": {}, "expected": "unknown"},
        ]

        for case in cases:
            with self.subTest(case=case):
                builder = ProductVisitMetadataBuilder(self.factory.get("/"))
                builder.ua = MagicMock()
                builder.ua.device.family = "TestDevice"
                builder.ua.os.family = "TestOS"
                builder.ua.browser.family = "TestBrowser"
                builder.ua.is_mobile = case["flags"].get("is_mobile", False)
                builder.ua.is_tablet = case["flags"].get("is_tablet", False)
                builder.ua.is_pc = case["flags"].get("is_pc", False)
                builder.ua.is_bot = case["flags"].get("is_bot", False)

                self.assertEqual(builder._get_device_type(), case["expected"])


class ProductEmailServiceTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="TestBrand")
        self.product = Product.objects.create(
            sku="SKU123", name="Zapatos Deportivos", price=99.99, brand=self.brand
        )
        self.user = User.objects.create_user(
            email="user@example.com", password="pass", is_staff=True, is_active=True
        )

    def test_build_generates_subject_and_body(self):
        subject, body = ProductEmailService.build(self.product, self.user)

        self.assertIn("[Catálogo] Producto actualizado", subject)
        self.assertIn(self.product.name, subject)
        self.assertIn(self.product.sku, subject)
        self.assertIn("Zapatos Deportivos", body)
        self.assertIn("user@example.com", body)

    @patch("apps.products.tasks.send_product_update_email.delay")
    def test_send_email_calls_task_with_correct_arguments(self, mock_delay):
        User.objects.create_user(
            email="admin@example.com", password="pass", is_staff=True, is_active=True
        )

        ProductEmailService.send_email(self.product, self.user)

        self.assertTrue(mock_delay.called)
        args, kwargs = mock_delay.call_args
        self.assertIn("Zapatos Deportivos", args[0])
        self.assertIn("SKU123", args[1])
        self.assertEqual(args[2], ["admin@example.com"])

    @patch("apps.products.tasks.send_product_update_email.delay")
    def test_send_email_does_nothing_if_no_other_admins(self, mock_delay):
        ProductEmailService.send_email(self.product, self.user)
        mock_delay.assert_not_called()
