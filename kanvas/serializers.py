from rest_framework import serializers
import uuid


class AddressSerializer(serializers.Model):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False)

    city = serializers.CharField(max_length=255)
    country = serializers.CharField(max_length=255)
    state = serializers.CharField(max_length=255)
    street = serializers.CharField(max_length=255)
    house_number = serializers.IntegerField()
    zip_code = serializers.CharField(max_length=255, unique=False)


class UserSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)

    is_admin = serializers.BooleanField()
    email = serializers.CharField(max_length=255, unique=True)
    password = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)

    address = AddressSerializer(many=True, read_only=True)


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_at = serializers.DateTimeField()

    name = serializers.CharField(max_length=255, unique=True)
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField(max_length=255)

    # if user.is_admin == True:
    user_instructor = UserSerializer(read_only=True)
    # if user.is_admin == False:
    user_students = UserSerializer(many=True, read_only=True)
