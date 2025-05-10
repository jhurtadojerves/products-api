from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer for managing admin user data.

    This serializer handles the creation and update of admin users,
    including secure password handling. It ensures that passwords
    are write-only and enforces required fields.

    Meta:
        - model: The User model.
        - fields: Includes user ID, email, active status, first name,
          last name, and password.
        - extra_kwargs: Specifies that the password field is write-only
          and required.
        - read_only_fields: Specifies that the ID field is read-only.

    Methods:
        - create: Creates a new user with an encrypted password.
        - update: Updates an existing user, excluding the password.
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
        Create a new admin user with a hashed password.

        Args:
            validated_data (dict): The validated data for the user.

        Returns:
            User: The created user instance.
        """
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update an existing admin user, excluding the password.

        Args:
            instance (User): The user instance to update.
            validated_data (dict): The validated data for the update.

        Returns:
            User: The updated user instance.
        """
        validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for handling password reset functionality.

    This serializer validates the current password and allows the user
    to set a new password. It ensures that only the authenticated user
    can change their own password.
    """

    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        """
        Validate the current password and checks user permissions.

        Args:
            attrs (dict): The data passed to the serializer.

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
                {"current_password": "Current password is wrong"}
            )

        if user != object_user:
            raise serializers.ValidationError("Only can change your password")

        return attrs
