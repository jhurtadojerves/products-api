from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.accounts.serializers.user import AdminUserSerializer, PasswordResetSerializer

User = get_user_model()


@extend_schema(tags=["accounts"])
@extend_schema_view(
    reset_password=extend_schema(
        request=PasswordResetSerializer,
        responses={200: None},
        description="Reset de contraseña por email",
    )
)
class AdminUserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing admin users.

    This ViewSet provides CRUD operations for admin users (`is_staff=True`)
    and includes additional functionality for resetting passwords and
    preventing self-deletion.

    Attributes:
        queryset (QuerySet): Filters the user model to include only staff users.
        serializer_class (Serializer): Specifies the serializer used for admin user data.
        permission_classes (list): Restricts access to admin users only.

    Methods:
        - perform_create: Ensures that new users are created as active staff members.
        - destroy: Prevents an admin user from deleting their own account.
        - reset_password: Allows resetting the password of a specific admin user.
    """

    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        """
        Ensure that new admin users are created as active staff members.

        Args:
            serializer (Serializer): The serializer instance containing validated data.

        Returns:
            None
        """
        serializer.save(is_staff=True, is_active=True)

    def destroy(self, request, *args, **kwargs):
        """
        Prevents an admin user from deleting their own account.

        Args:
            request (Request): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Response: A response indicating success or failure of the deletion.
        """
        instance = self.get_object()

        if instance == request.user:
            return Response(
                {"detail": "You can't delete yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="reset-password")
    def reset_password(self, request, pk=None):
        """
        Reset the password of a specific admin user.

        This action validates the current password and sets a new password
        for the specified user.

        Args:
            request (Request): The HTTP request object.
            pk (str): The primary key of the user whose password is being reset.

        Returns:
            Response: A response indicating the success of the password reset.
        """
        user = self.get_object()
        serializer = PasswordResetSerializer(
            data=request.data, context={"request": request, "object_user": user}
        )
        serializer.is_valid(raise_exception=True)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response(
            {"detail": "Password updated successfully."},
            status=status.HTTP_200_OK,
        )
