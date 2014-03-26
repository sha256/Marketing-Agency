__author__ = 'sha256'

from django import forms
from apps.auth.models import User
from apps.auth.middleware import SESSION_KEY
from apps.auth.authentication import authenticate


class AuthenticationForm(forms.Form):

    username = forms.CharField(label="Username", max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    rememberme = forms.BooleanField(required=False)

    error_messages = {
        'invalid_login': "Please enter a correct username/email and password. "
                         "Note that both fields may be case-sensitive.",
        'no_cookies': "Your Web browser doesn't appear to have cookies "
                      "enabled. Cookies are required for logging in.",
        'inactive': "This account is inactive.",
        }

    def __init__(self, request=None, *args, **kwargs):

        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['size'] = 35
        self.fields['password'].widget.attrs['size'] = 35

        # Set the label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        if not self.fields['username'].label:
            self.fields['username'].label = 'Username'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'] % {
                        'username': self.username_field.verbose_name
                    })
            elif not self.user_cache.is_active:
                raise forms.ValidationError(self.error_messages['inactive'])
        self.check_for_test_cookie()
        return self.cleaned_data

    def check_for_test_cookie(self):
        if self.request and not self.request.session.test_cookie_worked():
            raise forms.ValidationError(self.error_messages['no_cookies'])

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache