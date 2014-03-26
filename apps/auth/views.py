__author__ = 'sha256'

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from django.http import HttpResponseRedirect, QueryDict
from apps.auth.models import User
from django.utils.http import base36_to_int, is_safe_url
from django.shortcuts import resolve_url, render, redirect
from django.contrib.auth import REDIRECT_FIELD_NAME, login as autha_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm as Foo, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from apps.auth.authentication import login as auth_login
from apps.auth.forms import AuthenticationForm
from apps.auth.forms import UserAddForm
from quint.settings import STATIC_ROOT, LOGIN_REDIRECT_URL
from core.views.base import SecuredView, SmartView


class UserView(SecuredView):

    def get_common_data(self):
        lata = {}
        lata['users'] = User.objects.all()
        return lata

    def post(self, request, *args, **kwargs):
        form = UserAddForm(request.POST)
        data = {}
        if form.is_valid():
            user = User.objects.create_user(form.cleaned_data['username'], password=form.cleaned_data['password'])
            #user.is_staff = True
            user.save()
            data['success'] = "User successfully added!"

        data['form'] = form
        return self.render(request, 'users.html', data)

    def get(self, request, redirect_field_name="foo", *args, **kwargs):
        data = {}
        data['form'] = UserAddForm()

        return self.render(request, 'users.html', data)


class UserSettings(SecuredView):

    def get(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user)
        data = {}
        data['passForm'] = form
        return self.render(request, "my_account.html", data)

    def post(self, request, *args, **kwargs):
        data = {}
        form = PasswordChangeForm(user=request.user)
        if "changepass" in request.POST:
            form = PasswordChangeForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                data['success'] = "Password successfully changed!"

        data['passForm'] = form

        return self.render(request, "my_account.html", data)



