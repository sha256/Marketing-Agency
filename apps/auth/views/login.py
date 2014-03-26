__author__ = 'sha256'

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from django.http import HttpResponseRedirect, QueryDict
from apps.auth.models import User
from django.utils.http import base36_to_int, is_safe_url
from django.shortcuts import resolve_url, render, redirect
from apps.auth.authentication import login as auth_login
from apps.auth.forms import AuthenticationForm
from quint.settings import STATIC_ROOT, LOGIN_REDIRECT_URL
from core.views.base import SecuredView, SmartView
from django.contrib.auth import logout as auth_logout
from django.core.urlresolvers import reverse


class LoginView(SmartView):

    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return self.render(request, "auth/login.html", {'form': form, })

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(data=request.POST)
        redirect_to = request.REQUEST.get('next', '')
        if form.is_valid():
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url('/')
            auth_login(request, form.get_user())

            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()

            if not form.cleaned_data['rememberme']:
                request.session.set_expiry(0)

            return HttpResponseRedirect(redirect_to)

        else:
            return self.render(request, "auth/login.html", {"form": form, })


class LogoutView(SmartView):

    def get(self, request, *arg, **kwargs):
        auth_logout(request)

        return HttpResponseRedirect(reverse("auth-login"))