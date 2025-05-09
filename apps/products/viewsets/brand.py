from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import ModelViewSet

from apps.products.models.brand import Brand
from apps.products.serializers.brand import BrandSerializer


@extend_schema(tags=["brands"])
class BrandViewSet(ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "name"
