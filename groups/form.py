from django import forms

from .models import Groups

class GroupForm(forms.ModelForm):
    class Meta:
        model = Groups
        fields = ('group_name',)