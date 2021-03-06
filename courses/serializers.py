from rest_framework import serializers

from accounts.serializers import PersonalizedUserSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()

    instructor = PersonalizedUserSerializer(read_only=True)
    students = PersonalizedUserSerializer(many=True, read_only=True)


class CourseToUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(required=False)
    demo_time = serializers.TimeField(required=False)
    link_repo = serializers.CharField(required=False)
