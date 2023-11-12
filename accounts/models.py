from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# 헬퍼 클래스
class UserManager(BaseUserManager):
    def create_user(self, email, username, profile_image, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=email,
            username=username,
            profile_image=profile_image,
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, username=None, password=None, profile_image=None, **extra_fields):
        superuser = self.create_user(
            email=email,
            username=username,
            password=password,
            profile_image=profile_image,
        )
        
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.is_active = True
        
        superuser.save(using=self._db)
        return superuser

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True, null=False, blank=False)
    username = models.CharField(max_length=100, null=False, blank=False)
    profile_image = models.CharField(max_length=400, null=True)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    
class Item(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField()
    image = models.ImageField(upload_to='accounts\images\item', blank=True, null=True)
    user = models.ManyToManyField(User, related_name='item', blank=True)
    
class Badge(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    description = models.TextField()
    image = models.ImageField(upload_to='accounts\images\badge', blank=True, null=True)
    user = models.ManyToManyField(User, related_name='badge', blank=True)
    
