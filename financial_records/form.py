from django import forms

from .models import Category, FinancialRecord

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)

class FinancialRecordForm(forms.ModelForm):
    class Meta:
        model = FinancialRecord
        fields = ('name','category', 'description', 'debit', 'credit', 'currency', )


# forms.py

from django import forms

class CSVUploadForm(forms.Form):
    data_file = forms.FileField(
        label='選擇CSV文件',
        help_text='目前只使用CSV格式'
    )