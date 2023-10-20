from django.db import models

# Create your models here.

from accounts.models import User

# Create your models here.
from groups.models import Groups

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, related_name='categories',  on_delete=models.CASCADE)
    group = models.ForeignKey(Groups, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name
    
class FinancialRecord(models.Model):
    group = models.ForeignKey(Groups, on_delete=models.CASCADE)
    category = models.ManyToManyField(Category, related_name='records', blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    debit = models.DecimalField(max_digits=16, decimal_places=6)
    credit = models.DecimalField(max_digits=16, decimal_places=6)
    currency = models.FloatField(default=1.00)
    balance = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def balance(self):
        return (self.credit - self.debit) * self.currency
    

    def __str__(self):
        return self.name