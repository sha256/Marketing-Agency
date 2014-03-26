from apps.auth.models import User, Role

import json

from django.http import HttpResponse

from core.views import SecuredView, SmartView
from core.utils.misc import convertDatetimeToString


class AjaxView(SmartView):

    def get(self, request, *args, **kwargs):
        ret = ''
        jsondata = ''
        if "get" in request.GET:
            what = request.GET.get('get')
            if what == "users":
                jsondata = self.get_users(request)

            jsonx = json.JSONEncoder(indent=4)
            ret = jsonx.encode(jsondata)

        return HttpResponse(ret, mimetype="application/json")

    def post(self, request, *args, **kwargs):
        ret = ''
        if "del" in request.POST:
            what = request.POST.get('del')
            ret = what
            idx = request.POST.get('id')

        return HttpResponse(ret)

    def get_users(self, request):
        users = User.objects.filter(is_staff=False).order_by('-date_joined')
        jsr = []
        for a in users:

            jsr.append([
                a.name,
                a.phone,
                a.email,
                convertDatetimeToString(a.date_joined),
                convertDatetimeToString(a.last_login),
            ])

        return {'aaData': jsr}