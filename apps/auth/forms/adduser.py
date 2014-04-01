

from apps.auth.models import User
from django import forms
from django.utils import timezone
from django.contrib.auth.hashers import make_password



class UserAddForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True)
    repassword = forms.CharField(widget=forms.PasswordInput(), required=True)
    date_joined = forms.DateTimeField(required=False)
    last_login = forms.DateTimeField(required=False)

    def __init__(self, *args, **kwargs):
        super(UserAddForm, self).__init__(*args, **kwargs)
        #self.fields['role'].empty_label = "Select a Role"
       # self.fields['country'].queryset = Country.objects.exclude(code="all")
       # self.fields['country'].label_from_instance = lambda ob: ob.name

    def clean(self):
        form_data = self.cleaned_data
        form_data["last_login"] = timezone.now()
        form_data["date_joined"] = timezone.now()
        form_data["is_active"] = True
        form_data['is_superuser'] = False
        password = form_data.get("password", None)
        repassword = form_data.get("repassword", None)

        #var_dump(form_data)

        us = User.objects.filter(username=form_data['username']).count()
        if us > 0:
            raise forms.ValidationError("Choose a different username!")

        try:
            User.objects.get(email=form_data['email'])
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError("Choose a different Email!")

        if password is None or repassword is None or form_data['password'] != form_data['repassword']:
            raise forms.ValidationError("Password did not match!")

        form_data["password"] = make_password(form_data["password"])

        return form_data

    class Meta:
        model = User


class UserUpdateForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    repassword = forms.CharField(widget=forms.PasswordInput(), required=False)


    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['role'].empty_label = "Select a Role"
       # self.fields['country'].queryset = Country.objects.exclude(code="all")
        #self.fields['country'].label_from_instance = lambda ob: ob.name

    def clean(self):
        form_data = self.cleaned_data
        if form_data['username'] != self.instance.username:
            us = User.objects.filter(username=form_data['username']).count()
            if us > 0:
                raise forms.ValidationError("Choose a different username!")

        if form_data['email'] != self.instance.email:
            us = User.objects.filter(email=form_data['email']).count()
            if us > 0:
                raise forms.ValidationError("Choose a different Email!")

        if "password" in form_data and len(form_data['password']) < 1:
            form_data['password'] = self.instance.password
        elif form_data['password'] != form_data['repassword']:
            raise forms.ValidationError("Password did not match!")
        elif form_data['password'] == form_data['repassword'] and len(form_data['password']) > 1:
            form_data["password"] = make_password(form_data["password"])

        return form_data

    class Meta:
        model = User
        exclude = ('date_joined', 'last_login', 'is_superuser', 'password_reset', 'password_reset_expire')


class MyInfoUpdateForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), required=False)
    repassword = forms.CharField(widget=forms.PasswordInput(), required=False)

    def __init__(self, *args, **kwargs):
        super(MyInfoUpdateForm, self).__init__(*args, **kwargs)

    def clean(self):
        form_data = self.cleaned_data
        if form_data['username'] != self.instance.username:
            us = User.objects.filter(username=form_data['username']).count()
            if us > 0:
                raise forms.ValidationError("Choose a different username!")

        if form_data['email'] != self.instance.email:
            us = User.objects.filter(email=form_data['email']).count()
            if us > 0:
                raise forms.ValidationError("Choose a different Email!")

        if "password" in form_data and len(form_data['password']) < 1:
            form_data['password'] = self.instance.password
        elif form_data['password'] != form_data['repassword']:
            raise forms.ValidationError("Password did not match!")
        elif form_data['password'] == form_data['repassword'] and len(form_data['password']) > 0:
            form_data["password"] = make_password(form_data["password"].strip())

        return form_data

    class Meta:
        model = User
        exclude = ('date_joined', 'last_login', 'is_active', 'role', 'is_superuser', 'propic', 'password_reset', 'password_reset_expire')


class PasswordResetForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=1)
    repassword = forms.CharField(widget=forms.PasswordInput(), required=True, min_length=1)

    class Meta:
        model = User
        fields = ('password', 'repassword')

    def clean(self):
        form_data = self.cleaned_data

        if form_data['password'] != form_data['repassword']:
            raise forms.ValidationError("Password did not match!")
        elif form_data['password'] == form_data['repassword'] and len(form_data['password']) > 0:
            form_data["password"] = make_password(form_data["password"].strip())

        return form_data
