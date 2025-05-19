from django.db import models


class Price(models.Model):
    product = models.ForeignKey(
        "products.Product",
        on_delete=models.CASCADE,
        related_name="prices",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.ForeignKey(
        "products.Channel",
        on_delete=models.CASCADE,
        related_name="prices",
    )

    class Meta:
        unique_together = ("product", "channel")
        verbose_name = "Price"
        verbose_name_plural = "Prices"
