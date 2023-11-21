from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
from django.core.validators import RegexValidator
from .validators import validate_iranian_phoneNumber
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None,is_active=True ,**extra_fields):
        if not email:
            raise ValueError("شماره تلفن الزامی است.")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username,is_active=True, **extra_fields)
        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)
    phoneNumber = models.CharField(
        max_length=11,
        validators=[validate_iranian_phoneNumber]
    )
    national_code = models.CharField(
        max_length=10,
        validators=[RegexValidator(regex=r'^\d{10}$', message='کد ملی باید ۱۰ رقم باشد.')]
    )
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'name', 'phoneNumber']

    def __str__(self):
        return self.name
    


    
    def has_module_perms(self, app_label):
        
        return True

    def has_perm(self, perm, obj=None):
        
        return True