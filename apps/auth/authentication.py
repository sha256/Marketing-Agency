__author__ = 'sha256'

from apps.auth.models import User

SESSION_KEY = '_auth_user_id'
REDIRECT_FIELD_NAME = 'next'


def login(request, user):

    if user is None:
        user = request.user

    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.pk:
            # To avoid reusing another user's session, create a new, empty
            # session if the existing session corresponds to a different
            # authenticated user.
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.pk
    if hasattr(request, 'user'):
        request.user = user


def authenticate(username=None, password=None, **kwargs):

    if '@' in username:
        kwargs = {'email': username}
    else:
        kwargs = {'username': username}
    try:
        user = User.objects.get(**kwargs)
        if user.check_password(password):
            return user
    except User.DoesNotExist:
        return None

