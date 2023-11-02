from django.db import models

# Create your models here.

from accounts.models import User

# Create your models here.
from groups.models import Groups

import ast

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
    debit = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    credit = models.DecimalField(max_digits=16, decimal_places=6, default=0)
    currency = models.DecimalField(max_digits=16, decimal_places=6,default=1.00)
    balance = models.DecimalField(max_digits=16, decimal_places=6, null=True, blank=True)
    created_by = models.ForeignKey(User, related_name='records', null=True , on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    @property
    def balance(self):
       # 使用 round 函数将结果四舍五入到两位小数
       
        previous_balance = 0
        records = FinancialRecord.objects.filter(group=self.group, created_at__lte=self.created_at)
       
        for record in records:
            previous_balance += (record.credit - record.debit) * record.currency
        return round(previous_balance, 2)

    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-created_at',)

