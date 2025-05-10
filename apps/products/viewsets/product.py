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
    """
    ViewSet for managing products.

    This ViewSet provides CRUD operations for products and includes additional
    functionality for tracking product views and sending email notifications
    when a product is updated.

    Attributes:
        queryset (QuerySet): The set of all products in the database.
        serializer_class (Serializer): The serializer used for product data.
        lookup_field (str): The field used to look up a product (SKU in this case).

    Methods:
        - retrieve: Retrieves a product and tracks unauthenticated user visits.
        - update: Updates a product and sends an email notification to administrators.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "sku"

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product by its SKU.

        If the user is not authenticated, it tracks the product visit by
        collecting metadata (e.g., IP address, device type) and sending it
        to a background task.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The serialized product data.
        """
        product = self.get_object()
        response = super().retrieve(request, *args, **kwargs)

        if not request.user.is_authenticated:
            metadata = ProductVisitMetadataBuilder(request).build()
            track_product_retrieve.delay(product.id, metadata)

        return response

    def update(self, request, *args, **kwargs):
        """
        Update a product and sends an email notification.

        This method updates the product with the provided data and sends an
        email notification to administrators about the update.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: The serialized updated product data.
        """
        product = self.get_object()
        partial = kwargs.pop("partial", False)
        serializer = self.get_serializer(product, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        ProductEmailService.send_email(product, request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
