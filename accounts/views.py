from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from django.contrib.auth import authenticate

from accounts.serializers import PersonalizedUserSerializer, LoginUserSerializer
from .models import PersonalizedUser

import ipdb


class PersonalizedUserView(APIView):
    def post(self, request):
        serializer = PersonalizedUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        find_user = PersonalizedUser.objects.filter(email=serializer.validated_data['email']).exists()
        if find_user is True:
            return Response({"message": "User already exists"}, status.HTTP_422_UNPROCESSABLE_ENTITY)

        # ipdb.set_trace()
        user = PersonalizedUser.objects.create_user(**serializer.validated_data)
        serializer = PersonalizedUserSerializer(user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginUserView(APIView):
    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])

        if user is not None:
            token = Token.objects.get_or_create(user=user)[0]
            return Response({'token': token.key})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
