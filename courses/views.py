from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from courses.serializers import CourseSerializer

from .models import Courses
from .permissions import IsAdmin

import ipdb


class CoursesView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        find_course = Courses.objects.filter(name=serializer.validated_data['name']).exists()
        if find_course is True:
            return Response({'message': 'Course already created!'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        course = Courses.objects.create(**serializer.validated_data)
        print(course)
        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        all_courses = Courses.objects.all()
        serialized = CourseSerializer(all_courses, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


    # def get(self, request): # kwárquium


    # def patch(self, request): # Somente Instrutor


    # def put(self, request): # Somente Instrutor


    # def put(self, request): # Somente Instrutor


    # def delete(self, request): # Somente Instrutor

