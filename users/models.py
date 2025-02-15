from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings

# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

# User Model
class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    img = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    google_sign_in = models.BooleanField(default=False)
    
    # Relationships
    projects = models.ManyToManyField('Project', related_name='users', blank=True)
    teams = models.ManyToManyField('Team', related_name='members', blank=True)
    notifications = models.ManyToManyField('Notification', related_name='user_notifications', blank=True)
    works = models.ManyToManyField('Work', related_name='user_works', blank=True)
    tasks = models.ManyToManyField('Task', related_name='user_tasks', blank=True)

    # Additional Fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    def __str__(self):
        return self.name

    # JWT generation method
    def generate_verification_token(self):
        payload = {
            'ID': str(self.id),
            'exp': datetime.utcnow() + timedelta(days=7)
        }
        token = jwt.encode(payload, settings.USER_VERIFICATION_TOKEN_SECRET, algorithm='HS256')
        return token
