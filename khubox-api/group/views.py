from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.response import Response
from knox.models import AuthToken

from .models import UserGroup
from user.models import User

from .serializers import (UserGroupSerializer, CreateUserGroupSerializer, AddUserSerializer)
from user.serializers import UserSerializer

class CreateGroupAPI(generics.GenericAPIView):
    serializer_class = CreateUserGroupSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_name = request.data["group_name"]
        input_owner = UserSerializer(self.request.user).data

        group, created = UserGroup.objects.get_or_create(group_name = input_name, owner_email = input_owner["email"])   
        if created:
            group.save()
            group.user_to_group(request.user)
            group.save()
        else:
            body = {"message": "already exist"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(UserGroupSerializer(group).data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

class AddUserAPI(generics.GenericAPIView):
    serializer_class = AddUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        input_name = request.data["group_name"]
        input_user = request.data["user_id"]
        input_owner = UserSerializer(self.request.user).data

        group, created = UserGroup.objects.get_or_create(group_name = input_name)   
        
        
        if(input_owner["email"]!=UserGroupSerializer(group).data["owner_email"]):
            body = {"message": "not group owner"}
            return Response(body, status=status.HTTP_401_UNAUTHORIZED)

        if created:
            body = {"message": "group doesn't exist"}
            return Response(body, status=status.HTTP_400_BAD_REQUEST)
        else:
            try :
                user= User.objects.get(id = input_user)
            except User.DoesNotExist:
                body = {"message": "user doesn't exist"}
                return Response(body, status=status.HTTP_400_BAD_REQUEST)
            group.user_to_group(user)
            group.save()
        
        return Response(UserGroupSerializer(group).data)

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class GroupListAPI(generics.ListAPIView):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer

#class GroupListAPI(generics.GenericAPIView):