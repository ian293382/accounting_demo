from django.db import models
from accounts.models import User
class Line_User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    line_user_id = models.CharField(max_length=255, null=True, unique=True) 

    def __str__(self):
        return self.user.username