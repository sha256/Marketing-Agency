from apps.auth.models import User

import json

from django.http import HttpResponse
from apps.magency.rowmapper import RowMapper

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
            elif what == "newspaperads":
                jsondata = self.get_news_ads(request)
            elif what == "internetads":
                jsondata = self.get_websitead_list(request)
            elif what == "bills":
                jsondata = self.get_bills_list(request)

            elif what == "televisionads":
                jsondata = self.get_tvad_list(request)
            elif what == "billboardsads":
                jsondata = self.get_billboard_list(request)

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

    def get_billboard_list(self, request):

        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        res = RowMapper.call_proc('billboardads(%s, :curr)' % idx,
                                  ['id', 'title', 'validity', 'bill', 'name', 'billboards'])
        jsr = []
        for a in res:
            if idx == 0:
                jsr.append([
                    a.name,
                    a.title,
                    a.billboards,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])
            else:
                jsr.append([
                    a.title,
                    a.billboards,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])

        return {'aaData': jsr}

    def get_bills_list(self, request):

        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        res = RowMapper.call_proc('bills(%s, :curr)' % idx,
                                  ['id', 'title', 'name', 'ammount', 'paid_by', 'time'])

        jsr = []
        for a in res:

            if idx == 0:
                jsr.append([
                    a.name,
                    a.title,
                    a.ammount,
                    a.paid_by,
                    convertDatetimeToString(a.time),
                ])
            else:
                jsr.append([
                    a.title,
                    a.ammount,
                    a.paid_by,
                    convertDatetimeToString(a.time),
                ])

        return {'aaData': jsr}


    def get_websitead_list(self, request):

        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        res = RowMapper.call_proc('internetads(%s, :curr)' % idx,
                                  ['id', 'title', 'validity', 'bill', 'name', 'websites'])
        jsr = []
        for a in res:
            if idx == 0:
                jsr.append([
                    a.name,
                    a.title,
                    a.websites,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])
            else:
                jsr.append([
                    a.title,
                    a.websites,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])

        return {'aaData': jsr}

    def get_news_ads(self, request):
        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        res = RowMapper.call_proc('newspaperads(%s, :curr)' % idx,
                                  ['id', 'title', 'validity', 'bill', 'name', 'width', 'height', 'color', 'newspapers'])
        jsr = []
        for a in res:
            if idx == 0:
                jsr.append([
                    a.name,
                    a.title,
                    a.width,
                    a.height,
                    a.color,
                    a.newspapers,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])
            else:
                jsr.append([
                    a.title,
                    a.width,
                    a.height,
                    a.color,
                    a.newspapers,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])

        return {'aaData': jsr}


    def get_tvad_list(self, request):

        idx = 0
        if not request.user.is_staff:
            idx = request.user.id

        res = RowMapper.call_proc('televisionads(%s, :curr)' % idx,
                                  ['id', 'title', 'validity', 'bill', 'name', 'duration', 'televisions'])
        jsr = []
        for a in res:
            if idx == 0:
                jsr.append([
                    a.name,
                    a.title,
                    a.duration,
                    a.televisions,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])
            else:
                jsr.append([
                    a.title,
                    a.duration,
                    a.televisions,
                    a.bill,
                    convertDatetimeToString(a.validity)
                ])

        return {'aaData': jsr}

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