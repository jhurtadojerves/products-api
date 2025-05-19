from drf_spectacular.utils import extend_schema
from rest_framework import mixins, viewsets

from apps.products.models.channel import Channel
from apps.products.models.price import Price
from apps.products.serializers.price import (
    CreatePriceSerializer,
    PriceListSerializer,
    PriceSerializer,
)


@extend_schema(tags=["prices"])
class PriceViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
):
    """Price viewset for listing and retrieving prices."""

    queryset = Price.objects.all()
    serializer_class = PriceSerializer

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePriceSerializer
        return PriceSerializer


@extend_schema(tags=["prices"])
class PriceListViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    """Price list viewset for listing prices by channel."""

    serializer_class = PriceListSerializer

    queryset = Channel.objects.all()
