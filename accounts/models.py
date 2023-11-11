from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    profile_image = models.ImageField(blank=True, upload_to='profile_image')