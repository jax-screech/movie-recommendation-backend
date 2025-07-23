# users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
import os
from uuid import uuid4

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid4().hex}.{ext}"
    return os.path.join('avatars', str(instance.id), filename)

class CustomUser(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.username