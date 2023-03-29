from django.contrib.auth import get_user_model
from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.api.services import handle_user


# auth
class CreateUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        model = get_user_model()
        fields = ("email", "password")
        write_only_fields = "password"
        read_only_fields = (
            "staff",
            "admin",
        )

    def create(self, validated_data):
        user = super(CreateUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        handle_user.change_user_last_request_time(user)

        return token


# users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        exclude = ("password", "groups", "user_permissions")


class UserChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "is_active", "email")


class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("last_request", "last_login")
