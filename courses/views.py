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

    def post(self, request):  # Somente Instrutor

        serializer = CourseSerializer(data=request.data)

        if serializer.is_valid():
            Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        course = Courses.objects.create(**serializer.validated_data)

        serialized = CourseSerializer(course)

        return Response(serialized.data, status=status.HTTP_200_OK)


    # def get(self, request): # kwárquium


    # def get(self, request): # kwárquium
    

    # def patch(self, request): # Somente Instrutor


    # def put(self, request): # Somente Instrutor


    # def put(self, request): # Somente Instrutor


    # def delete(self, request): # Somente Instrutor

