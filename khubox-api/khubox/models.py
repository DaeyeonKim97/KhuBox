from django.db import models


class File(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    parent_id = models.CharField(max_length=36, blank=True, null=True)
    owner_user_id = models.IntegerField(blank=True, null=True)
    owner_group_id = models.IntegerField(blank=True, null=True)
    uploader_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6)
    name = models.CharField(max_length=255)
    size = models.BigIntegerField()
    is_public = models.IntegerField(default=0)
    is_starred = models.IntegerField(default=0)
    is_trashed = models.IntegerField(default=0)
    created_at = models.DateTimeField()
    deleted_at = models.DateTimeField(blank=True, null=True)


class Group(models.Model):
    owner_id = models.IntegerField()
    name = models.CharField(max_length=50)
    root_folder = models.CharField(max_length=36)
    invite_code = models.CharField(max_length=36)
    created_at = models.DateTimeField()


class GroupUser(models.Model):
    group_id = models.IntegerField()
    user_id = models.IntegerField()
    joined_at = models.DateTimeField()


class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=60)
    name = models.CharField(max_length=50)
    root_folder = models.CharField(max_length=36)
    created_at = models.DateTimeField()
