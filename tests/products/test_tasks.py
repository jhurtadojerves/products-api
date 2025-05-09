from unittest.mock import MagicMock, patch

from django.test import TestCase

from apps.products.models import Brand, Product, ProductRetrieve
from apps.products.tasks import track_product_retrieve


class TrackProductRetrieveTaskTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="GeoTest")
        self.product = Product.objects.create(
            sku="GEO123",
            name="Geo Test Product",
            price=150.00,
            brand=self.brand,
        )

    @patch("apps.products.tasks.Reader")
    def test_track_product_retrieve_enriches_metadata_and_creates_record(
        self, mock_reader_cls
    ):
        mock_reader = MagicMock()
        mock_reader.city.return_value.country.name = "Ecuador"
        mock_reader.city.return_value.city.name = "Quito"
        mock_reader_cls.return_value = mock_reader

        metadata = {"ip": "123.123.123.123", "browser": "Firefox"}

        track_product_retrieve(self.product.id, metadata)

        self.assertEqual(ProductRetrieve.objects.count(), 1)
        visit = ProductRetrieve.objects.first()

        self.assertEqual(visit.product, self.product)
        self.assertEqual(visit.metadata["ip"], "123.123.123.123")
        self.assertEqual(visit.metadata["browser"], "Firefox")
        self.assertEqual(visit.metadata["country"], "Ecuador")
        self.assertEqual(visit.metadata["city"], "Quito")

        mock_reader.city.assert_called_once_with("123.123.123.123")
        mock_reader.close.assert_called_once()

    @patch("apps.products.tasks.Reader")
    def test_city_lookup_exception_uses_defaults(self, mock_reader_cls):
        mock_reader = MagicMock()
        mock_reader.city.side_effect = Exception("GeoIP error")
        mock_reader_cls.return_value = mock_reader

        metadata = {"ip": "1.2.3.4"}

        track_product_retrieve(self.product.id, metadata)

        visit = ProductRetrieve.objects.first()

        self.assertEqual(visit.metadata["country"], "México")
        self.assertEqual(visit.metadata["city"], "Ciudad de México")
        self.assertEqual(visit.metadata["ip"], "1.2.3.4")

        mock_reader.city.assert_called_once_with("1.2.3.4")
        mock_reader.close.assert_called_once()

    def test_product_not_found(self):
        track_product_retrieve(self.product.id + 1, {})
        self.assertEqual(ProductRetrieve.objects.count(), 0)
