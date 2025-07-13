from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# user authentication, profile and permissions
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)# want email to be unique
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'# defne field for login
    
    def __str__(self):
        return self.username 