from django.db import models

from .brand import Brand


class Product(models.Model):
    sku = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")

    def __str__(self):
        """
        Return a string representation of the Product instance.

        This method returns the name and SKU of the product, which is useful
        for displaying the product in the Django admin or other interfaces.

        Returns:
            str: The name and SKU of the product in the format "name (SKU)".
        """
        return f"{self.name} ({self.sku})"


class ProductRetrieve(models.Model):
    visited_at = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="retrieves"
    )
