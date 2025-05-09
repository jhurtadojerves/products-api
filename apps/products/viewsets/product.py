from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.models.product import Product
from apps.products.serializers.product import ProductSerializer
from apps.products.services import ProductEmailService, ProductVisitMetadataBuilder
from apps.products.tasks import track_product_retrieve


@extend_schema(tags=["products"])
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "sku"

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()
        response = super().retrieve(request, *args, **kwargs)

        if not request.user.is_authenticated:
            metadata = ProductVisitMetadataBuilder(request).build()
            track_product_retrieve.delay(product.id, metadata)

        return response

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ProductEmailService.send_email(product, request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
