from django import forms

from .models import Category, FinancialRecord

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ('name','name','category', 'description', 'debit', 'credit', 'currency', )

