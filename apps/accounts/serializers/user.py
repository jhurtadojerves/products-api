from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for managing admin user data.

    This serializer allows the creation and update of admin users,
    ensuring secure password handling. Passwords are write-only
    and are encrypted before being stored.

    Meta:
        - model: User model.
        - fields: Includes ID, email, active status, first name, last name, and password.
        - extra_kwargs: Specifies that the password field is write-only and required.
        - read_only_fields: Specifies that the ID field is read-only.

    Methods:
        - create: Creates a new admin user with an encrypted password.
    """

    class Meta:
        model = User
        fields = ["id", "email", "is_active", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }
        read_only_fields = ["id"]

    def create(self, validated_data):
        """
        Create a new admin user with an encrypted password.

        Args:
            validated_data (dict): The validated data for the user.

        Returns:
            User: The created user instance.
        """
        return User.objects.create_user(**validated_data)


class AdminUserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user data.

    This serializer allows updating the `is_active`, `first_name`, and
    `last_name` fields of an existing user.
    """

    class Meta:
        model = User
        fields = ["is_active", "first_name", "last_name"]


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset functionality.

    This serializer validates the current password and allows the user
    to set a new password. It ensures that only the authenticated user
    can change their own password.

    Fields:
        - current_password: The user's current password (write-only).
        - new_password: The user's new password (write-only).

    Methods:
        - validate: Validates the current password and checks user permissions.
    """

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate the current password and checks user permissions.

        Args:
            attrs (dict): The data provided to the serializer.

        Raises:
            serializers.ValidationError: If the current password is incorrect
            or if the user is not authorized to change the password.

        Returns:
            dict: The validated data.
        """
        user = self.context["request"].user
        object_user = self.context["object_user"]

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "The current password is incorrect."}
            )

        if user != object_user:
            raise serializers.ValidationError("You can only change your own password.")

        return attrs
