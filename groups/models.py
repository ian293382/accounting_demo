from django.db import models

# Create your models here.
from accounts.models import User

class Groups(models.Model):
    group_name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='financial_groups', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.group_name