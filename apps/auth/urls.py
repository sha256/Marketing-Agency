from apps.auth.views.pwd_reset import PasswordResetView
from apps.auth.views.signup import SignupView

__author__ = 'sha256'

from django.conf.urls import patterns, url
from apps.auth.views.login import LoginView, LogoutView
from apps.auth.views.roles import RolesView
from apps.auth.views.ajax import DataTableAjax
from apps.auth.views.user import UserView, UserEditView, MyAccountView

urlpatterns = patterns('',
    url(r'login/$', LoginView.as_view(), name='auth-login'),
    url(r'signup/$', SignupView.as_view(), name="auth-signup"),
    url(r'logout/$', LogoutView.as_view(), name="auth-logout"),
)
