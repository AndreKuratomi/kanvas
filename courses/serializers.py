from rest_framework import serializers

from accounts.serializers import PersonalizedUserSerializer


class CourseSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    name = serializers.CharField()
    demo_time = serializers.TimeField()
    link_repo = serializers.CharField()

    # instructor = serializers.CharField()
    # students = PersonalizedUserSerializer(many=True, read_only=True)

    # # if user.is_admin == True:
    instructor = PersonalizedUserSerializer(read_only=True)
    # # if user.is_admin == False:
    students = PersonalizedUserSerializer(many=True, read_only=True)
