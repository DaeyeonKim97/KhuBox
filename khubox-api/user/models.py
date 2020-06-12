from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import datetime


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, name, date_of_birth, password=None):
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            name=name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,         
            name=name,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, date_of_birth, password):
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
            name= "True",
        )
        #user.is_staff = True
        user.is_admin = True
        user.save(using=self._db)
        return user

    


class User(AbstractBaseUser):

    username = None
    email = models.EmailField( unique=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(default=datetime.date.today)
    storage_usage = models.FloatField( default = 0)
    profile = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None)
    
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'date_of_birth','name' ]

    objects = UserManager()

    def __str__(self):
        return self.email
    
    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj = None):
        return True
    
    def has_module_perms(self, app_label):
        return True

