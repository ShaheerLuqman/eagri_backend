from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom user model for EAgri application"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    
    # Make first_name and last_name required (they're optional in AbstractUser)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    # Fields that are required by default:
    # - username
    # - password
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    
    def __str__(self):
        return self.username 