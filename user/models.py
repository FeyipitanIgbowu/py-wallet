from django.db import models
from django.contrib.auth.models import User, AbstractUser


# Create your models here.
class User(AbstractUser):
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    phone_number = models.CharField(max_length=11, null=False)
    password = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)


