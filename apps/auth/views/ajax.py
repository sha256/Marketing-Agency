__author__ = 'sha256'

from django.contrib.auth.models import User
from django.http import HttpResponse
import json
import datetime
from django.db.models import F
from core.views import SecuredView
from apps.auth.models.role import Role


class DataTableAjax(SecuredView):

    def get(self, request, *args, **kwargs):
        ret = ''
        jsondata = ''
        if "get" in request.GET:
            what = request.GET.get('get')
            if what == 'roles':
                jsondata = self.get_roles(request)

            jsonx = json.JSONEncoder(indent=4)
            ret = jsonx.encode(jsondata)

        return HttpResponse(ret, mimetype="application/json")

    def post(self, request, *args, **kwargs):

        return HttpResponse("")

    def get_roles(self, request):
        roles = Role.objects.all()
        jsr = []
        for role in roles:
            if request.user.has_perm("auth.delete_role"):
                action_string = "<a class='btn btn-danger actionDelete' data-id='%s' \
                             data-toggle='modal' href='#xModal'>  \
                            <i class='icon-trash icon-white'></i> </a>" % role.id
            else:
                action_string = ""

            jsr.append([
                role.name,
                ", ".join([perm.name for perm in role.permissions.all()]),
                action_string
            ])

        data = {}
        data['aaData'] = jsr
        return data

