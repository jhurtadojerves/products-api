from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from apps.products.models.channel import Channel
from apps.products.serializers.channel import ChannelSerializer


@extend_schema(tags=["channels"])
class ChannelViewSet(viewsets.ModelViewSet):
    """A viewset for viewing and editing channel instances."""

    queryset = Channel.objects.all()
    serializer_class = ChannelSerializer
