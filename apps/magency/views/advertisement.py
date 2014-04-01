from django.db import models
from django.forms.models import modelform_factory
from apps.magency.models import Advertisement, NewspaperAd, TelevisionAd, BillboardAd
from apps.magency.models.advertisement import WebsiteAd
from core.views.base import SecuredView

__author__ = 'sha256'


class AdvertisementListView(SecuredView):

    def get(self, request, what):
        data = {}
        data['what'] = what
        return self.render(request, "magency/ads_list.html", data)


class AdvertisementAddView(SecuredView):

    def formfield_call_back(self, field, **kwargs):
        if isinstance(field, models.ManyToManyField):
            fies = field.formfield(**kwargs)
            if hasattr(field.related.parent_model, 'parent'):
                fies.label_from_instance = lambda ob: ob.parent.title + " - " + ob.title
            else:
                fies.label_from_instance = lambda ob: ob.title
            return fies
        elif isinstance(field, models.BooleanField):
            fies = field.formfield(**kwargs)
            fies.widget.attrs['class'] = "ace-switch ace-switch-5"
            return fies
        else:
            return field.formfield(**kwargs)

    def get_common_data(self, request):
        data = {}
        form2_klass = None
        if self.what == "newspaper":
            form2_klass = NewspaperAd
        elif self.what == "television":
            form2_klass = TelevisionAd
        elif self.what == "billboard":
            form2_klass = BillboardAd
        elif self.what == "internet":
            form2_klass = WebsiteAd

        Form1 = modelform_factory(Advertisement, exclude=('company', 'bill'))
        Form2 = modelform_factory(form2_klass, exclude=('advertisement',), formfield_callback=self.formfield_call_back)
        form1 = Form1(request.POST or None, request.FILES or None)
        form2 = Form2(request.POST or None)

        if form1.is_valid() and form2.is_valid():
            f1 = form1.save(commit=False)
            f1.company_id = request.user.id
            f1.save()

            f2 = form2.save(commit=False)
            f2.advertisement_id = f1.id
            f2.save()
            form2.save_m2m()

            form1 = Form1()
            form2 = Form2()

        data['form1'] = form1
        data['form2'] = form2

        return data

    def get(self, request, what):
        self.what = what
        return self.render(request, "magency/ads_add.html", {})

    def post(self, request, what):
        self.what = what
        return self.render(request, "magency/ads_add.html", {})