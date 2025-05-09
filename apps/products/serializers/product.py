from rest_framework import serializers

from apps.products.models.product import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "sku",
            "name",
            "price",
            "brand",
        )
