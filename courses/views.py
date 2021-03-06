from django.db import IntegrityError
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import PersonalizedUser
from courses.serializers import CourseSerializer, CourseToUpdateSerializer

from .models import Courses
from .permissions import IsAdmin
from .services import is_valid_UUID

import ipdb


class CoursesView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def post(self, request):
        try:
            serializer = CourseSerializer(data=request.data)

            if serializer.is_valid():
                Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            find_course = Courses.objects.filter(name=serializer.validated_data['name']).exists()
            if find_course is True:
                return Response({'message': 'Course already exists'}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            course = Courses.objects.create(**serializer.validated_data)

            serialized = CourseSerializer(course)

            return Response(serialized.data, status=status.HTTP_201_CREATED)

        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):

        all_courses = Courses.objects.all()
        serialized = CourseSerializer(all_courses, many=True)

        return Response(serialized.data, status=status.HTTP_200_OK)


class CourseByIdView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, course_id=''):
        try:
            if is_valid_UUID(course_id):
                course = Courses.objects.get(uuid=course_id)

                serialized = CourseSerializer(course)

                return Response(serialized.data, status=status.HTTP_200_OK)

            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Courses.DoesNotExist:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, course_id=''):

        serializer = CourseToUpdateSerializer(data=request.data)
        valid = serializer.is_valid()

        try:
            valid_uuid = is_valid_UUID(course_id)
            if valid_uuid:
                doesCourseExist = Courses.objects.get(uuid=course_id)
        except Courses.DoesNotExist:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "No valid UUID"}, status=status.HTTP_404_NOT_FOUND)

        try:
            course = Courses.objects.filter(uuid=course_id).update(**serializer.validated_data)

        except IntegrityError:
            return Response({"message": "This course name already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        updated = Courses.objects.get(uuid=course_id)

        serialized = CourseSerializer(updated)


        return Response(serialized.data, status=status.HTTP_200_OK)

    def delete(self, request, course_id=''):
        try:
            if is_valid_UUID(course_id):
                course = Courses.objects.get(uuid=course_id)
                Courses.delete(course)

                return Response(status=status.HTTP_204_NO_CONTENT)

            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Courses.DoesNotExist:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)


class RegisterInstructorToCourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def put(self, request, course_id=''):
        try:
            if is_valid_UUID(course_id):
                course = Courses.objects.get(uuid=course_id)

                candidate_uuid = request.data['instructor_id']
                doesInstructorExist = PersonalizedUser.objects.get(uuid=candidate_uuid)

                if doesInstructorExist.is_admin is not True:
                    return Response({"message": "Instructor id does not belong to an admin"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                course.instructor = doesInstructorExist
                course.save()

                serialized = CourseSerializer(course)

                return Response(serialized.data, status=status.HTTP_200_OK)

            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Courses.DoesNotExist:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)


class EnrollStudentToCourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def put(self, request, course_id=''):
        try:
            if is_valid_UUID(course_id):
                course = Courses.objects.get(uuid=course_id)

                students_to_enroll = request.data['students_id']

                for student in students_to_enroll:
                    try:
                        doesUserExist = PersonalizedUser.objects.get(uuid=student)
                    except:
                        return Response({"message": "Invalid students_id list"}, status=status.HTTP_400_BAD_REQUEST)

                    if doesUserExist.is_admin is True:
                        return Response({"message": "Some student id belongs to an Instructor"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

                course.students.set(students_to_enroll)
                course.save()

                serialized = CourseSerializer(course)
                return Response(serialized.data, status=status.HTTP_200_OK)

            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)

        except Courses.DoesNotExist:
            return Response({"message": "Course does not exist"}, status=status.HTTP_404_NOT_FOUND)
