__author__ = 'sha256'

from django.contrib.auth.decorators import user_passes_test
from apps.auth.authentication import REDIRECT_FIELD_NAME


def staff_only(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def superuseronly(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):

    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated() and u.is_superuser,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
