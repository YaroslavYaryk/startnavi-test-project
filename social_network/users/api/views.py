from django.contrib.auth.models import update_last_login

from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.views import (
    TokenObtainPairView
)

from .serializers import CreateUserSerializer, MyTokenObtainPairSerializer, UserSerializer, UserChangeSerializer, \
    UserActivitySerializer
from .utils import BaseAPIView


# auth
class CreateUserAPIView(CreateAPIView):
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = serializer.save()
            update_last_login(None, user)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {**serializer.data, "user_id": user.id},
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        except Exception as err:
            return Response({"message": str(err)}, status.HTTP_401_UNAUTHORIZED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# user
class UserApiView(BaseAPIView):

    def get(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status.HTTP_200_OK)

    def patch(self, request):
        serializer = UserChangeSerializer(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserActivityApiView(BaseAPIView):

    def get(self, request, *args, **kwargs):
        serializer = UserActivitySerializer(instance=request.user)
        return Response(serializer.data, status.HTTP_200_OK)
