from rest_framework import serializers

from accounts.serializers import PersonalizedUserSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)

    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()
    created_at = serializers.DateTimeField(read_only=True)

    instructor = PersonalizedUserSerializer(read_only=True)
    students = PersonalizedUserSerializer(many=True, read_only=True)
