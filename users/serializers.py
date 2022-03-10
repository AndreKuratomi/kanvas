from rest_framework import serializers
import uuid

from addresses.serializers import AddressSerializer


class PersonalizedUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    is_admin = serializers.BooleanField()
    email = serializers.CharField(unique=True)
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    address = AddressSerializer(many=True, read_only=True)
