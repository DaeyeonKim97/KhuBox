from rest_framework import serializers
from .models import User
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate


# 회원가입 시리얼라이저

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "date_of_birth", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"],
            validated_data["name"],
            validated_data["date_of_birth"],
            validated_data["password"]
        )
        return user


# 접속 유지중인지 확인할 시리얼라이저

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id","email", "name","date_of_birth","storage_usage")


# 로그인 시리얼라이저 

class LoginUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "name", "date_of_birth","storage_usage", "password")
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = ('email',"storage_usage")

    def update(self, instance, validated_data):

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance

class GroupSerializer (serializers.HyperlinkedModelSerializer):
    class Meta