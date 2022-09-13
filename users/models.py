from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    ROLES = [
        ('manager', 'manager'),
        ('developer', 'dev')
    ]
    role = models.CharField(choices=ROLES, default='dev', max_length=10)
