from django.db import models
from django.forms.models import modelform_factory
from django.shortcuts import render
from apps.auth.decorators import staff_only
from apps.magency.models import Bill
from core.views import SmartView, SecuredView

__author__ = 'sha256'



class BillsView(SecuredView):

    def get(self, request):
        return self.render(request, "magency/bills.html", {})


def formfield_call_back(field, **kwargs):
    if isinstance(field, models.ForeignKey):
        fies = field.formfield(**kwargs)
        fies.label_from_instance = lambda ob: ob.title
        return fies
    else:
        return field.formfield(**kwargs)


@staff_only
def add_bills(request):
    data = {}
    BillForm = modelform_factory(Bill, formfield_callback=formfield_call_back)
    bForm = BillForm(request.POST or None)
    if bForm.is_valid():
        bForm.save()
        bForm = BillForm()

    data['form1'] = bForm

    return render(request, "magency/domains.html", data)