__author__ = 'sha256'
__time__ = '6/18/13 2:11 AM'

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from apps.auth.decorators import staff_only
from django.views.decorators.csrf import csrf_exempt


class LoggedInMixin(object):

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoggedInMixin, self).dispatch(request, *args, **kwargs)


class AdminMixin(object):

    @method_decorator(staff_only)
    def dispatch(self, request, *args, **kwargs):
        return super(AdminMixin, self).dispatch(request, *args, **kwargs)


class CSRFExemptMixin(object):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(CSRFExemptMixin, self).dispatch(*args, **kwargs)


