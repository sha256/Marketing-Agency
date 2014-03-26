
__author__ = 'sha256'

try:
    from urllib.parse import urlparse, urlunparse
except ImportError:     # Python 2
    from urlparse import urlparse, urlunparse

from apps.auth.forms.adduser import UserAddForm, UserUpdateForm, MyInfoUpdateForm
from core.views import SecuredView, SmartView


class SignupView(SmartView):

    def get_common_data(self, request):
        data = {}
        data['form'] = UserAddForm()
        return data

    def post(self, request, *args, **kwargs):
        data = {}
        if "adduser" in request.POST:
            form = UserAddForm(request.POST)
            if form.is_valid():
                form.save()
                data['success'] = "User successfully added!"
                return self.redirect(self.reverse('auth-login'))
            else:
                data['form'] = form

        return self.render(request, 'auth/registration.html', data)

    def get(self, request, redirect_field_name="foo", *args, **kwargs):
        data = {}
        data['form'] = UserAddForm()
        return self.render(request, 'auth/registration.html', data)