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



# def handle_user_input(input_text):
#     # 假設用戶輸入的格式是：/b 一支筆 100元 或 /c 薪資收入500
#     parts = input_text.split()
#     if len(parts) >= 4:
#         if parts[0] == "/b":
#             # 處理支出
#             category_name = "line 支出"
#             amount = float(parts[3].rstrip("元"))
#         elif parts[0] == "/c":
#             # 處理收益
#             category_name = "line 收益"
#             amount = float(parts[3])
#         else:
#             return "無法處理此輸入。"
        
#         # 找到相應的類別
#         try:
#             category = Category.objects.get(name=category_name)
#         except Category.DoesNotExist:
#             # 如果類別不存在，您可以創建一個新的類別
#             category = Category.objects.create(name=category_name, created_by=User.objects.first())

#         # 創建新的FinancialRecord對象
#         record = FinancialRecord(
#             group=group,  # 設定相應的群組
#             name=parts[1],  # 使用用戶輸入的名稱
#             debit=0 if parts[0] == "/c" else amount,  # 如果是/c，debit設為0，否則設為金額
#             credit=amount if parts[0] == "/c" else 0,  # 如果是/c，credit設為金額，否則設為0
#             currency=1.00,  # 設定幣值
#             created_by=User.objects.first()  # 設定建立者，您可以更改為實際用戶
#         )
        
#         # 保存新的FinancialRecord
#         record.save()
        
#         return f"已成功記錄{'收益' if parts[0] == '/c' else '支出'} {amount} 元到類別 '{category_name}'。"

#     return "無法處理此輸入。"