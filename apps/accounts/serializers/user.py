from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "is_active", "first_name", "last_name", "password"]
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
        }
        read_only_fields = ["id"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        validated_data.pop("password", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance


class PasswordResetSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = self.context["request"].user
        object_user = self.context["object_user"]

        if not user.check_password(attrs["current_password"]):
            raise serializers.ValidationError(
                {"current_password": "Current password is wrong"}
            )

        if user != object_user:
            raise serializers.ValidationError("Only can change your password")

        return attrs
