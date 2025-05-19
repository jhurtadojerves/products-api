from rest_framework import serializers

from apps.products.models.channel import Channel
from apps.products.models.price import Price


class CreatePriceSerializer(serializers.ModelSerializer):
    """Serializer for the Price model."""

    class Meta:
        model = Price
        fields = ["id", "product", "price", "channel"]
        read_only_fields = ["id"]


class PriceSerializer(serializers.ModelSerializer):
    """Serializer for the Price model."""

    product = serializers.CharField(source="product.sku")

    class Meta:
        model = Price
        fields = ["id", "product", "price", "channel"]


class PriceListSerializer(serializers.ModelSerializer):
    """Serializer for the Price model."""

    prices = PriceSerializer(many=True)

    class Meta:
        model = Channel
        fields = ["prices"]
