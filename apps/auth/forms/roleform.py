__author__ = 'sha256'

from django.forms import ModelForm
from apps.auth.models import Role
from django import forms
from apps.auth.models.permission import Permission


class CustomCheckBoxField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return ""


class RoleMatrixForm(ModelForm):

    permissions = CustomCheckBoxField(widget=forms.CheckboxSelectMultiple,
                                      queryset=Permission.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(RoleMatrixForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Role
