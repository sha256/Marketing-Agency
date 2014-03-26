from django.shortcuts import get_object_or_404
from apps.auth.models import User

__author__ = 'sha256'

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from apps.auth.forms.adduser import UserAddForm, UserUpdateForm, MyInfoUpdateForm
from core.views import SecuredView, SmartView


class UserView(SecuredView):

    def get_common_data(self, request):
        data = {}
        data['form'] = UserAddForm()
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        if "adduser" in request.POST and request.user.has_perm("auth.create_user"):
            form = UserAddForm(request.POST)
            if form.is_valid():
                form.save()
                data['success'] = "User successfully added!"
            else:
                data['form'] = form

        return self.render(request, 'auth/user.html', data)

    def get(self, request, redirect_field_name="foo", *args, **kwargs):
        data = {}
        data['form'] = UserAddForm()
        return self.render(request, 'auth/user.html', data)


class UserEditView(SecuredView):

    def get_common_data(self, request):
        user = get_object_or_404(User, pk=self.user_id)
        form = UserUpdateForm(request.POST or None, instance=user)
        if form.is_valid():
            form.save()
            return self.redirect(self.reverse("auth-users"))

        return {'form': form}

    def post(self, request, user_id, *args, **kwargs):
        data = {}
        self.user_id = user_id
        return self.render(request, 'auth/user_edit.html', data)

    def get(self, request, user_id, *args, **kwargs):
        data = {}
        self.user_id = user_id
        return self.render(request, 'auth/user_edit.html', data)


class MyAccountView(SecuredView):

    def get_common_data(self, request):
        form = MyInfoUpdateForm(request.POST or None, instance=request.user)
        if form.is_valid():
            form.save()
            return self.redirect(request.path)

        return {'form': form}

    def post(self, request, *args, **kwargs):
        return self.render(request, 'auth/myaccount.html', {})

    def get(self, request, *args, **kwargs):
        return self.render(request, 'auth/myaccount.html', {})