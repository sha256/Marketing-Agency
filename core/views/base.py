from django.http import HttpResponseRedirect

__author__ = 'sha256'

from django.views.generic import View
from django.shortcuts import render
from django.core import urlresolvers
from core.views.mixins import LoggedInMixin, AdminMixin, CSRFExemptMixin, SuperUserMixin
import json
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


class SmartView(View):

    def get_common_data(self, request):
        return {}

    def clear_args(self):
        pass

    def reverse(self, viewname, urlconf=None, args=None, kwargs=None, prefix=None, current_app=None):
        return urlresolvers.reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, prefix=prefix, current_app=current_app)

    def redirect(self, url):
        return HttpResponseRedirect(url)

    def render(self, request, template, *args, **kwargs):
        common = self.get_common_data(request)
        if isinstance(common, HttpResponseRedirect):
            return common
        common.update(*args)
        return render(request, template, common, **kwargs)

    def json(self, data):
        jsonx = json.JSONEncoder(indent=4)
        ret = jsonx.encode(data)
        return HttpResponse(ret, mimetype="application/json")


class SmartViewWithNoCsrf(SmartView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(SmartViewWithNoCsrf, self).dispatch(request, *args, **kwargs)

class SecuredView(LoggedInMixin, SmartView):
    pass


class SuperUserView(SuperUserMixin, SmartView):
    pass


class AdminView(AdminMixin, SmartView):
    pass


class NoCsrfView(CSRFExemptMixin, SmartView):
    pass



    
    

