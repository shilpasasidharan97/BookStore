from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone

# Create your models here.

class User(AbstractUser):
    """Custom User model where email is the unique identifier."""
    
    email = models.EmailField(unique=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.get_full_name()} <{self.username}>"
    