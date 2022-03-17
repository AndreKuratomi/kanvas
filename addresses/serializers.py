from rest_framework import serializers

from accounts.serializers import PersonalizedUserSerializer


class AddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    city = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    zip_code = serializers.CharField()

    users = PersonalizedUserSerializer(many=True, read_only=True)
