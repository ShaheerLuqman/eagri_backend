from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

class User(AbstractUser):
    """Custom user model for EAgri application"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    
    # Make first_name and last_name required (they're optional in AbstractUser)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'phone_number']
    
    class Meta:
        db_table = 'users_user'
        # Add this to ensure related objects are deleted
        default_related_name = 'users'

    def delete(self, *args, **kwargs):
        # Delete auth tokens first
        self.auth_token.all().delete()
        super().delete(*args, **kwargs)
    
    def __str__(self):
        return self.username
@receiver(pre_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # This will delete the user's auth token
    from rest_framework.authtoken.models import Token
    Token.objects.filter(user=instance).delete()
