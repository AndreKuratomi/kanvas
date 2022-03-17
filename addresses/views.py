from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from addresses.serializers import AddressSerializer

from .models import Address

import ipdb


class AddressView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user

        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        address = Address.objects.get_or_create(**serializer.validated_data)[0]

        user.address = address
        user.save()

        serialized = AddressSerializer(address)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
