from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class  User(AbstractUser):
    line_user_id = models.CharField(max_length=255, null=True, blank=True)

