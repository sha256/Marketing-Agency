__author__ = 'sha256'

from django.core.exceptions import ImproperlyConfigured
from django.utils.functional import SimpleLazyObject
from apps.auth.models import User
from apps.auth.authentication import SESSION_KEY


def _get_user(request):
    from django.contrib.auth.models import AnonymousUser
    try:
        user_id = request.session[SESSION_KEY]
        user = User.objects.get(pk=user_id)
    except KeyError:
        user = AnonymousUser()
    except User.DoesNotExist:
        user = AnonymousUser()
    return user


def get_user(request):
    if not hasattr(request, '_cached_user'):
        request._cached_user = _get_user(request)
    return request._cached_user


class AuthenticationMiddleware(object):
    def process_request(self, request):
        assert hasattr(request, 'session'), "The Django authentication middleware requires session middleware to be installed. Edit your MIDDLEWARE_CLASSES setting to insert 'django.contrib.sessions.middleware.SessionMiddleware'."

        request.user = SimpleLazyObject(lambda: get_user(request))