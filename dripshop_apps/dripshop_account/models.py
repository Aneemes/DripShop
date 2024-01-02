from django.db import models
from django.contrib.auth.models import AbstractUser

class UserAccount(AbstractUser):
    phone = models.CharField(max_length=10, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.username
