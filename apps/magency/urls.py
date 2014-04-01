
from django.conf.urls import patterns, url
from apps.magency.views.advertisement import AdvertisementAddView, AdvertisementListView
from apps.magency.views.ajax import AjaxView
from apps.magency.views.bill import BillsView
from apps.magency.views.company_list import CompanyListView
from apps.magency.views.dashboard import DashboardView
from apps.magency.views.domain import DomainView
from apps.magency.views.edit import DomainEditView
from apps.magency.views.report import ReportView, ReportDownloadView

urlpatterns = patterns('',
    url(r'^$', DashboardView.as_view(), name='dashboard'),
    url(r'companies/$', CompanyListView.as_view(), name="company_list"),
    url(r'domains/(?P<what>([a-z]+))$', DomainView.as_view(), name="domain"),
    url(r'domains/(?P<what>([a-z]+))/edit/(?P<idx>([0-9]+))/$', DomainEditView.as_view(), name="domain-edit"),
    url(r'advertisements/(?P<what>([a-z]+))/add$', AdvertisementAddView.as_view(), name="advadd"),
    url(r'advertisements/(?P<what>([a-z]+))$', AdvertisementListView.as_view(), name="advlist"),
    url(r'ajax$', AjaxView.as_view(), name="ajax"),
    url(r'bills/$', BillsView.as_view(), name="bills"),
    url(r'bills/add$', 'apps.magency.views.bill.add_bills', name="bills-add"),
    url(r'^reports/$', ReportView.as_view(), name="reports"),
    url(r'reports/download/(?P<what>([a-z]+))$', ReportDownloadView.as_view(), name="reportdl"),

)
