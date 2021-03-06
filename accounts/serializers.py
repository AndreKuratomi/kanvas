from rest_framework import serializers

# from addresses.serializers import AddressSerializer


class PersonalizedUserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    is_admin = serializers.BooleanField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    # address = AddressSerializer(read_only=True)


class LoginUserSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
