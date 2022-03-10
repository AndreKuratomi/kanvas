from rest_framework import serializers
import uuid

from users.serializers import PersonalizedUserSerializer


class AddressSerializer(serializers.Model):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False)

    city = serializers.CharField()
    country = serializers.CharField()
    state = serializers.CharField()
    street = serializers.CharField()
    house_number = serializers.IntegerField()
    zip_code = serializers.CharField(unique=False)


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_at = serializers.DateTimeField()

    name = serializers.CharField(unique=True)
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()

    # if user.is_admin == True:
    user_instructor = PersonalizedUserSerializer(read_only=True)
    # if user.is_admin == False:
    user_students = PersonalizedUserSerializer(many=True, read_only=True)
