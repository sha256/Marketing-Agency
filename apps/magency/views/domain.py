from django import forms
from django.http import Http404
from apps.magency.models import Newspaper, Section, Television, Program, Billboard, Website
from core.views import SmartView
from django.forms.models import modelform_factory
from django.db import models

__author__ = 'sha256'


class DomainView(SmartView):

    def formfield_call_back(self, field, **kwargs):
        if isinstance(field, models.ForeignKey):
            fies = field.formfield(**kwargs)
            fies.label_from_instance = lambda ob: ob.title
            return fies
        elif isinstance(field, models.BooleanField):
            fies = field.formfield(**kwargs)
            fies.widget.attrs['class'] = "ace-switch ace-switch-5"
            return fies
        else:
            return field.formfield(**kwargs)

    def get_common_data(self, request):
        if self.what not in ("newspaper", "internet", "television", "billboard"):
            raise Http404()

        data = {}

        form1_klass = None
        form2_klass = None
        valid = False

        if self.what == "newspaper":
            form1_klass = Newspaper
            form2_klass = Section
        elif self.what == "television":
            form1_klass = Television
            form2_klass = Program
        elif self.what == "billboard":
            form1_klass = Billboard
        elif self.what == "internet":
            form1_klass = Website

        Form1 = modelform_factory(form1_klass, formfield_callback=self.formfield_call_back)
        newsf = Form1(request.POST or None)

        if form2_klass is not None:
            Form2 = modelform_factory(form2_klass, formfield_callback=self.formfield_call_back)
            secf = Form2(request.POST or None)

        if "form1" in request.POST:
            if newsf.is_valid():
                newsf.save()
                valid = True

        elif "form2" in request.POST:
            if secf.is_valid():
                secf.save()
                valid = True

        if valid:
            newsf = Form1()

        if valid and form2_klass is not None:
            secf = Form2()

        if form2_klass is not None:
            data['form2'] = secf

        data['form1'] = newsf

        return data


    def get(self, request, what):
        self.what = what
        return self.render(request, "magency/domains.html", {})

    def post(self, request, what):
        self.what = what
        return self.render(request, "magency/domains.html", {})

