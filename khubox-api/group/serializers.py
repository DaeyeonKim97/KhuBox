from rest_framework import serializers
from .models import UserGroup

class CreateUserGroupSerializer(serializers.Serializer):
    group_name = serializers.CharField(allow_blank=False, max_length = 100)
    
class AddUserSerializer(serializers.Serializer):
    group_name = serializers.CharField(allow_blank=False, max_length = 100)
    user_id = serializers.IntegerField()

class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGroup
        fields = ("group_name","owner_email","group_users")
