from rest_framework import serializers

from apps.products.models.channel import Channel


class ChannelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Channel
        fields = ["id", "name"]
        read_only_fields = ["id"]
