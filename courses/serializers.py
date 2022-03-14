from rest_framework import serializers
import uuid

from accounts.serializers import PersonalizedUserSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created_at = serializers.DateTimeField()

    name = serializers.CharField(unique=True)
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()

    # # if user.is_admin == True:
    # user_instructor = PersonalizedUserSerializer(read_only=True)
    # # if user.is_admin == False:
    # user_students = PersonalizedUserSerializer(many=True, read_only=True)
