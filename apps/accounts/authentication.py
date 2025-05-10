from django.contrib.auth import authenticate, get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom serializer for obtaining JWT tokens.

    This serializer extends the default `TokenObtainPairSerializer` to use
    the user's email as the username field and includes additional user
    information (user ID and email) in the token response.

    Attributes:
        username_field (str): Specifies the field to use as the username (email in this case).

    Methods:
        - validate: Authenticates the user and customizes the token response.
    """

    username_field = User.EMAIL_FIELD

    def validate(self, attrs):
        """
        Validate the user's credentials and generates a JWT token.

        Args:
            attrs (dict): The data passed to the serializer, including email and password.

        Raises:
            serializers.ValidationError: If the credentials are invalid.

        Returns:
            dict: The token data, including the access and refresh tokens,
                  along with the user's ID and email.
        """
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"), email=email, password=password
        )

        if not user:
            raise serializers.ValidationError("Invalid credentials")

        data = super().validate(attrs)
        data.update(
            {
                "user_id": user.id,
                "email": user.email,
            }
        )

        return data


@extend_schema(tags=["auth"])
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom view for obtaining JWT tokens.

    This view uses the `CustomTokenObtainPairSerializer` to authenticate
    users and generate JWT tokens. It is tagged under "auth" for API documentation.
    """

    serializer_class = CustomTokenObtainPairSerializer


@extend_schema(tags=["auth"])
class CustomTokenRefreshView(TokenRefreshView):
    """
    Custom view for refreshing JWT tokens.

    This view extends the default `TokenRefreshView` and is tagged under "auth"
    for API documentation. It allows users to refresh their access tokens
    using a valid refresh token.
    """

    pass
