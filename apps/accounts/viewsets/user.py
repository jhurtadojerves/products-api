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
    queryset = User.objects.filter(is_staff=True)
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(is_staff=True, is_active=True)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance == request.user:
            return Response(
                {"detail": "You can't delete yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=["post"], url_path="reset-password")
    def reset_password(self, request, pk=None):
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
