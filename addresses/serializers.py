from rest_framework import serializers

import uuid


class AddressSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False)

    city = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    zip_code = serializers.CharField(unique=False)
