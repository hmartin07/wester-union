from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    verification_code = models.CharField(max_length=4, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
