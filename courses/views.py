from uuid import UUID
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

        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def get(self, request):

        all_courses = Courses.objects.all()
        serialized = CourseSerializer(all_courses, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


class CourseByIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, course_id=''):

        course = Courses.objects.get(uuid=course_id)
        if not course: # MUDAR ESTA LINHA
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, course_id=''):  # Somente Instrutor
        course = Courses.objects.get(uuid=course_id)
        if not course:  # MUDAR ESTA LINHA
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)
        # print(course)

        # COMO DEIXAR OS CAMPOS DE REQUEST.FIELDS OPCIONAIS????
        # valid_keys = ['name', 'demo_time', 'link_repo']
        # keys = request.data.keys()
        # for elems in keys:
        #     for sub_elems in valid_keys:
        #         if elems != sub_elems:

        # to_update_data = request.data
        serializer = CourseSerializer(data=request.data)
        # print(serializer.get_fields())
        if not serializer.is_valid():
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # if 'name' in keys:
        doesUpdatedNameAlreadyExists = Courses.objects.filter(name=serializer.validated_data['name']).exists()
        if doesUpdatedNameAlreadyExists:
            return Response({"message": "There is already a course with this name!"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        to_update = Courses.objects.update(**serializer.validated_data)
        serialized = CourseSerializer(to_update)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, course_id=''): # Somente Instrutor
        course = Courses.objects.get(uuid=course_id)

        if not course:  # MUDAR ESTA LINHA
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        Courses.delete(course)

        return Response(status=status.HTTP_204_NO_CONTENT)


# class ManipulateCourseView(APIView):

    # def put(self, request): # Somente Instrutor


    # def put(self, request): # Somente Instrutor


    # def delete(self, request): # Somente Instrutor
