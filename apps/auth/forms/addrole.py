__author__ = 'sha256'

from django.forms import ModelForm
from apps.auth.models.role import Role
from django import forms
from apps.auth.models.permission import Permission


class CustomCheckBoxField(forms.ModelMultipleChoiceField):

    def label_from_instance(self, obj):
        return "%s" % (obj.name,)


class AddRoleForm(ModelForm):

    permissions = CustomCheckBoxField(widget=forms.CheckboxSelectMultiple,
                                    queryset=Permission.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        super(AddRoleForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['class'] = 'input-xlarge'
       # self.fields['permissions'].widget.attrs['class'] = 'input-xlarge'

    class Meta:
        model = Role