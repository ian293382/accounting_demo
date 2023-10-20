from django import forms

from .models import Category, FinancialRecord

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class FinancialRecord(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ('name','name', 'description', 'debit', 'credit', 'currency', )

        