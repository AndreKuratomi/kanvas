from rest_framework import serializers

from ..addresses.serializers import AddressSerializer


class PersonalizedUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()

    is_admin = serializers.BooleanField()
    email = serializers.CharField(unique=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    address = AddressSerializer(many=True, read_only=True)