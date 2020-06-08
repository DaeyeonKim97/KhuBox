from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'parent_id', 'owner_id', 'uploader_id', 'type', 'name', 'size', 'is_public', 'is_shared',
                  'is_starred', 'is_trahsed', 'created_at']