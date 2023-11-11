from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    profile_image = models.ImageField(blank=True, upload_to='profile_image')