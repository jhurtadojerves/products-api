from django.db.models.deletion import ProtectedError
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.products.models.brand import Brand
from apps.products.serializers.brand import BrandSerializer


@extend_schema(tags=["brands"])
class BrandViewSet(ModelViewSet):
    """
    ViewSet for managing product brands.

    This ViewSet provides CRUD operations for the `Brand` model and includes
    custom behavior for handling deletion when a brand is referenced by other
    objects (e.g., products).

    Attributes:
        queryset (QuerySet): The set of all `Brand` objects.
        serializer_class (Serializer): The serializer used for brand data.
        lookup_field (str): Specifies that the `name` field is used for lookups.

    Methods:
        - destroy: Handles deletion of a brand and prevents deletion if it is
          referenced by other objects.
    """

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    lookup_field = "name"

    def destroy(self, request, *args, **kwargs):
        """
        Delete a brand unless it is referenced by other objects.

        This method attempts to delete a brand instance. If the brand is
        referenced by other objects (e.g., products), the deletion is blocked,
        and a detailed error message is returned.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A 204 No Content response if the deletion is successful,
            or a 400 Bad Request response if the brand is referenced by other objects.
        """
        instance = self.get_object()
        try:
            self.perform_destroy(instance)
        except ProtectedError as e:
            related_objects = ", ".join(str(obj) for obj in e.protected_objects)
            return Response(
                {
                    "detail": f"Cannot delete this brand because it is referenced by the following products: {related_objects}"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
