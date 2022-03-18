from uuid import UUID
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import PersonalizedUser
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
        # if Courses.DoesNotExist:  # MUDAR ESTA LINHA
        if not course:
            print("mãe do céu...")
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_200_OK)

    def patch(self, request, course_id=''):  # Somente Instrutor
        course = Courses.objects.get(uuid=course_id)
        # if Courses.DoesNotExist:  # MUDAR ESTA LINHA
        if not course:
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

    def delete(self, request, course_id=''):
        course = Courses.objects.get(uuid=course_id)

        # if Courses.DoesNotExist:  # MUDAR ESTA LINHA
        if not course:
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        Courses.delete(course)

        return Response(status=status.HTTP_204_NO_CONTENT)


class RegisterInstructorToCourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def put(self, request, course_id=''):
        course = Courses.objects.get(uuid=course_id)

        # if Courses.DoesNotExist:  # MUDAR ESTA LINHA
        if not course:
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        candidate_uuid = request.data['instructor_id']
        doesInstructorExist = PersonalizedUser.objects.get(uuid=candidate_uuid)
        if doesInstructorExist.is_admin is not True:
            return Response({"message": "Instructor id does not belong to an admin"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        course.instructor = doesInstructorExist
        course.save()

        serialized = CourseSerializer(course)
        return Response(serialized.data, status=status.HTTP_200_OK)


class EnrollStudentToCourseView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def put(self, request, course_id=''):
        course = Courses.objects.get(uuid=course_id)

        # if Courses.DoesNotExist:  # MUDAR ESTA LINHA
        if not course:
            return Response({"message": "This course does not exist!"}, status=status.HTTP_404_NOT_FOUND)

        students_to_enroll = request.data['students_id']

        for student in students_to_enroll:
            doesUserExist = PersonalizedUser.objects.get(uuid=student)
            # if PersonalizedUser.DoesNotExist:
            if not doesUserExist:
                print('eu, ein..!')
                return Response({"message": "Invalid students_id list"}, status=status.HTTP_404_NOT_FOUND)
            elif doesUserExist.is_admin is True:
                return Response({"message": "Some student id belongs to an Instructor"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        course.students.set(students_to_enroll)
        course.save()

        serialized = CourseSerializer(course)
        return Response(serialized.data, status=status.HTTP_200_OK)
