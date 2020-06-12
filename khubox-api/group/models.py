from django.db import models
from user.models import User

class UserGroup(models.Model):
    #group_id = models.AutoField(primary_key = True, blank = True)
    group_name = models.CharField(primary_key = True, unique = True, max_length=20)
    owner_email = models.EmailField(max_length=254)
    #owner = models.ForeignKey(User, verbose_name="Group Owner", on_delete=models.CASCADE)
    group_users = models.ManyToManyField(User, verbose_name="Group User")
    
    def user_to_group(self, user):
        self.group_users.add(user)
        #UserGroup.save(using=self._db)
        #return group

# Create your models here.
