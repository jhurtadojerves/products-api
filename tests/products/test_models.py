from django.db import IntegrityError
from django.test import TestCase

from apps.products.models import Brand, Product


class ProductModelTest(TestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name="TestBrand")

    def test_create_product(self):
        product = Product.objects.create(
            sku="TEST123", name="Test Product", price=150.00, brand=self.brand
        )
        self.assertIsNotNone(product.id)
        self.assertEqual(str(product), "Test Product (TEST123)")
        self.assertEqual(product.brand.name, "TestBrand")

    def test_unique_sku_constraint(self):
        Product.objects.create(
            sku="UNIQUE123", name="Item 1", price=99.00, brand=self.brand
        )

        with self.assertRaises(IntegrityError):
            Product.objects.create(
                sku="UNIQUE123", name="Item 2", price=110.00, brand=self.brand
            )


class BrandoModelTest(TestCase):
    def test_create_brand(self):
        brand = Brand.objects.create(name="TestBrand")
        self.assertIsNotNone(brand.id)
        self.assertEqual(brand.name, "TestBrand")
        self.assertEqual(str(brand), "TestBrand")

    def test_unique_name_constraint(self):
        Brand.objects.create(name="TestBrand")

        with self.assertRaises(IntegrityError):
            Brand.objects.create(name="TestBrand")
